# Timezone & DST Safety — UTC Discipline and Library Guide

Complete reference for timezone-safe datetime handling. Read when auditing TZ/DST code or selecting a library.

---

## The UTC Discipline

A single rule: **store UTC, render local**.

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Input     │───▶│   Parse to  │───▶│  Store as   │───▶│  Render in  │
│ (user input │    │    UTC      │    │    UTC      │    │ user's TZ   │
│  or event)  │    │             │    │             │    │ at the edge │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       ↑                                                        │
       └────────────── round-trip should be lossless ──────────┘
```

### Storage rules

- **PostgreSQL**: Always `timestamptz` (= `timestamp with time zone`). Internally stored as UTC; converts to session TZ on SELECT. **Never** use `timestamp` (no TZ) for event times — it silently loses the TZ on write.
- **MySQL**: No native TZ-aware type. Use `DATETIME` + application-level UTC convention, or `TIMESTAMP` (which auto-converts via `time_zone` session variable — footgun). Store explicitly in UTC.
- **SQLite**: No native type; store ISO 8601 UTC strings or Unix epoch integer.
- **MongoDB**: `Date` BSON type is UTC milliseconds since epoch. Safe by default; be careful with driver auto-conversions.
- **Redis**: Store as Unix epoch seconds/milliseconds; strings preserve what you write.

### Wire-format rules

- **REST/JSON**: ISO 8601 with offset: `2026-04-22T10:00:00+09:00` or `2026-04-22T01:00:00Z`. Never emit a TZ-naive string (`2026-04-22 10:00:00`) — ambiguous.
- **gRPC/Protobuf**: Use `google.protobuf.Timestamp` (UTC; seconds + nanos since epoch).
- **Kafka/events**: Store epoch milliseconds in payload; include a separate `occurred_at_tz` field if the local time matters semantically (e.g., "user's local workday").

### Rendering rules

- Determine user TZ from:
  1. User profile preference (explicit > implicit).
  2. Browser: `Intl.DateTimeFormat().resolvedOptions().timeZone` (returns IANA name like `Asia/Tokyo`).
  3. Fallback: UTC + explicit label (never silently default to server TZ).
- Render with locale-aware formatter: `Intl.DateTimeFormat`, Luxon `DateTime.toLocaleString`, Python `babel`.

---

## IANA tz Database

The canonical source for timezone rules is the **IANA tz database** (`tzdata`), updated several times per year as governments change DST rules.

### Naming

- Format: `Region/City` or `Region/Subregion/City`.
- Examples: `Asia/Tokyo`, `America/New_York`, `Europe/London`, `Pacific/Auckland`, `America/Argentina/Buenos_Aires`.
- Deprecated names (still work, but avoid): `Asia/Calcutta` → `Asia/Kolkata`; `Europe/Kiev` → `Europe/Kyiv`.

### Why abbreviations are dangerous

| Abbreviation | Possible meanings |
|-------------|-------------------|
| `CST` | Central Standard Time (US, UTC-6) OR China Standard Time (UTC+8) OR Cuba Standard Time (UTC-5) |
| `IST` | India Standard Time (UTC+5:30) OR Irish Standard Time (UTC+1) OR Israel Standard Time (UTC+2/+3) |
| `EST` | Eastern Standard Time (US, UTC-5) OR Eastern Standard Time (Australia, UTC+10) |
| `BST` | British Summer Time (UTC+1) OR Bangladesh Standard Time (UTC+6) |

Never accept user input as an abbreviation. Always normalize to IANA or reject.

### tzdata updates

- Distributed via OS packages (`tzdata` on Debian/Ubuntu), Python `zoneinfo` via `tzdata` PyPI package on Windows, JVM `$JAVA_HOME/lib/tzdb.dat`, browser/Node.js via embedded ICU.
- **Container gotcha**: A long-lived container may ship with stale tzdata. Update base image or mount `/etc/timezone` + `/usr/share/zoneinfo` from host.
- Schedule a quarterly review of tzdata version in production.

---

## DST Boundary Pitfalls

### Spring-forward (gap)

At DST start, the clock jumps forward — typically 02:00 → 03:00 local. The wall-clock interval **02:00–02:59 does not exist**.

**Example**: `America/New_York`, 2026-03-08 (second Sunday of March):
- 01:59:59 EST (UTC-5)
- 03:00:00 EDT (UTC-4)  ← jumped; 02:00-02:59 never happens

A schedule set for 02:30 daily:
- Most days: fires at 02:30 local.
- Mar 8, 2026: **undefined** unless the scheduler has an explicit policy.

**Library behavior**:
- **Python `zoneinfo`**: Constructing `datetime(2026, 3, 8, 2, 30, tzinfo=ZoneInfo("America/New_York"))` succeeds, but the resulting instant corresponds to 03:30 EDT (the "next valid" interpretation). To reject, use `fold=0` and check `datetime.utcoffset()` consistency.
- **Temporal API**: `Temporal.ZonedDateTime.from({...}, {disambiguation: 'reject'})` throws.
- **Luxon**: `DateTime.fromObject({...}, {zone: 'America/New_York'}).isValid` returns false with reason `'unsupported_zone'`; `.invalidReason === 'unsupported_zone'` or similar.
- **Quartz**: Skips the missing hour; fires at the next valid time (03:30 on the transition day).

### Fall-back (overlap)

At DST end, the clock goes back — typically 02:00 → 01:00 local. The interval **01:00–01:59 happens TWICE**.

**Example**: `America/New_York`, 2026-11-01 (first Sunday of November):
- 01:59:59 EDT (UTC-4)
- 01:00:00 EST (UTC-5)  ← the hour repeats

A schedule set for 01:30 daily:
- Most days: fires at 01:30 local.
- Nov 1, 2026: **fires twice** unless guarded.

**Library behavior**:
- **Python `zoneinfo`**: Default `fold=0` picks the EARLIER (EDT) instance; `fold=1` picks the LATER (EST) instance.
- **Temporal API**: `disambiguation` option: `'earlier'` (EDT), `'later'` (EST), `'compatible'` (POSIX: earlier for gaps, later for overlaps), `'reject'`.
- **Luxon**: No direct disambiguation for overlap in older versions; recent versions respect `keepCalendarTime`.
- **Quartz**: Fires once (at the first valid occurrence — the EDT instance).

### Resolution strategies

| Strategy | Applies to | Python | Temporal | Luxon |
|---------|-----------|--------|----------|-------|
| Earlier instance (overlap) | Fall-back | `fold=0` | `disambiguation: 'earlier'` | zone default |
| Later instance (overlap) | Fall-back | `fold=1` | `disambiguation: 'later'` | explicit set |
| Skip (gap) | Spring-forward | not applicable | `disambiguation: 'reject'` | `.invalid` |
| Clamp forward (gap) | Spring-forward | construct normally | `disambiguation: 'compatible'` | default |
| Reject | Both | manual check | `disambiguation: 'reject'` | check `.isValid` |

### Zones with unusual DST rules

- **Australia**: `Australia/Lord_Howe` has a **30-minute DST shift** (not 60). Wall-clock arithmetic assumptions break.
- **Antarctica**: `Antarctica/Troll` shifts by **2 hours** at DST.
- **Chile**: `America/Santiago` DST at **midnight** — a schedule at 00:30 can skip.
- **No DST**: `Asia/Tokyo`, `Asia/Shanghai`, `Asia/Kolkata` (+5:30), `Pacific/Honolulu`. Safe for wall-clock scheduling.

---

## Temporal API (ECMAScript)

Stage 3 proposal; polyfill available (`@js-temporal/polyfill`). Expected to be the standard going forward.

### Types

| Type | Represents | Use for |
|------|------------|---------|
| `Temporal.Instant` | A specific moment in time, UTC-ish | Event timestamps, DB primary keys |
| `Temporal.PlainDate` | Calendar date, no time, no TZ | Birthdays, deadlines |
| `Temporal.PlainTime` | Wall time, no date, no TZ | Daily alarm times |
| `Temporal.PlainDateTime` | Date + time, no TZ | Local-only events (meeting "3pm", TZ TBD) |
| `Temporal.ZonedDateTime` | Instant + TZ + calendar | User-facing schedules |
| `Temporal.Duration` | Amount of time | Retry delays, intervals |

### Example: ambiguous-time handling

```javascript
import { Temporal } from '@js-temporal/polyfill';

// Spring-forward day in NY
const zdt = Temporal.ZonedDateTime.from({
  year: 2026, month: 3, day: 8,
  hour: 2, minute: 30,
  timeZone: 'America/New_York',
}, { disambiguation: 'reject' });
// throws RangeError

const deferred = Temporal.ZonedDateTime.from({
  year: 2026, month: 3, day: 8,
  hour: 2, minute: 30,
  timeZone: 'America/New_York',
}, { disambiguation: 'compatible' });
// ZonedDateTime 2026-03-08T03:30:00-04:00[America/New_York]
```

### Best practice for new JS/TS projects

- Use `Temporal.ZonedDateTime` for scheduled events.
- Use `Temporal.Instant` for storage and transport.
- Convert to `Temporal.PlainDate` / `PlainTime` only when the TZ is genuinely irrelevant.

---

## Luxon

Mature alternative to Temporal; production-ready today. `DateTime.setZone(zone, {keepLocalTime?})` is the workhorse.

```javascript
import { DateTime } from 'luxon';

const now = DateTime.now().setZone('Asia/Tokyo');
const utc = now.toUTC();
const fromISO = DateTime.fromISO('2026-04-22T10:00:00+09:00', { setZone: true });
```

### Common mistakes

- `DateTime.local()` uses the runtime's system TZ — avoid; use `DateTime.now().setZone(...)` explicitly.
- `.setZone('X', { keepLocalTime: true })`: changes the TZ but reinterprets the wall-clock at the new TZ (12:00 JST → 12:00 EST, different instant). Without `keepLocalTime`, the instant is preserved and only the display changes.
- Omitting `{ setZone: true }` on `fromISO` causes the result to be in the runtime TZ after parsing.
- `DateTime.fromJSDate(new Date())` loses any TZ info — `Date` is always UTC instant.

---

## date-fns-tz

Companion to date-fns for TZ support; smaller than Luxon or Moment, tree-shakable.

```javascript
import { formatInTimeZone, zonedTimeToUtc, utcToZonedTime } from 'date-fns-tz';

// Format a UTC Date in a target TZ
formatInTimeZone(new Date(), 'Asia/Tokyo', 'yyyy-MM-dd HH:mm:ssXXX');

// Convert user-input local time to UTC for storage
const utcDate = zonedTimeToUtc('2026-04-22 10:00:00', 'Asia/Tokyo');

// Convert stored UTC to user-facing local Date (for formatting)
const localDate = utcToZonedTime(utcDate, 'America/New_York');
```

### Gotchas

- `utcToZonedTime` returns a `Date` whose **numeric value is shifted** to make the local wall-clock match — do NOT `.toISOString()` the result; it produces a wrong instant. Use `formatInTimeZone` for rendering instead.
- `zonedTimeToUtc` interprets string inputs with the given TZ; interpret ISO 8601 strings with explicit offset via `new Date(iso)` + direct formatting instead.

---

## Moment.js — Legacy

**Do not use in new code.** Moment is in maintenance mode since 2020:

- Mutable API — `moment().add(1, 'day')` mutates; surprising bugs.
- Large bundle (~70KB minified + moment-timezone data).
- Not tree-shakable.
- Official recommendation: migrate to Luxon, date-fns-tz, Day.js, or Temporal.

### Migration targets

| From Moment | To Luxon | To date-fns-tz |
|------------|----------|-----------------|
| `moment().tz('Asia/Tokyo')` | `DateTime.now().setZone('Asia/Tokyo')` | `utcToZonedTime(new Date(), 'Asia/Tokyo')` |
| `moment(iso).utc()` | `DateTime.fromISO(iso).toUTC()` | `new Date(iso)` |
| `moment().format('YYYY-MM-DD')` | `DateTime.now().toFormat('yyyy-MM-dd')` | `format(new Date(), 'yyyy-MM-dd')` |
| `moment(a).diff(b, 'hours')` | `a.diff(b, 'hours').hours` | `differenceInHours(a, b)` |

Migrate file-by-file with regression tests around DST dates.

---

## Python Libraries

### `zoneinfo` (stdlib, 3.9+) — preferred

```python
from datetime import datetime
from zoneinfo import ZoneInfo

tokyo = datetime(2026, 4, 22, 10, 0, tzinfo=ZoneInfo("Asia/Tokyo"))
utc = tokyo.astimezone(ZoneInfo("UTC"))
```

- On Windows, `zoneinfo` requires the `tzdata` PyPI package.
- `fold=0|1` on `datetime` for fall-back disambiguation.

### `pytz` — legacy but common

```python
import pytz
from datetime import datetime

tokyo = pytz.timezone("Asia/Tokyo")
# WRONG — does not apply DST correctly:
dt_wrong = datetime(2026, 4, 22, 10, 0, tzinfo=tokyo)
# RIGHT — use .localize() to attach TZ:
dt_right = tokyo.localize(datetime(2026, 4, 22, 10, 0))
```

Replace with `zoneinfo` in new code.

---

## Clock and Testing

### Freeze / mock the clock in tests

| Language | Library | Example |
|---------|---------|---------|
| Node.js | `@sinonjs/fake-timers` | `FakeTimers.install({ now: new Date('2026-03-08T06:30:00Z') })` |
| Python | `freezegun` | `@freeze_time("2026-03-08 06:30:00")` |
| Java | Inject `java.time.Clock` | `Clock.fixed(Instant.parse("2026-03-08T06:30:00Z"), ZoneOffset.UTC)` |
| Ruby | `timecop` | `Timecop.freeze(Time.utc(2026, 3, 8, 6, 30))` |

### Required test scenarios for any scheduled code

- DST spring-forward day in the target TZ.
- DST fall-back day in the target TZ.
- Feb-29 in a leap year (2028, 2032).
- Year-end rollover (Dec 31 → Jan 1).
- Last day of 28/29/30/31-day months.
- Timezone with non-hour offset (India +5:30, Nepal +5:45).
- TZ with reverse DST (Southern Hemisphere — Australia's April / October).

### User-preferred TZ detection in the browser

```javascript
const userTz = Intl.DateTimeFormat().resolvedOptions().timeZone;
// e.g., "Asia/Tokyo"
```

Store this on the user profile at signup. Prefer an explicit setting over re-detecting on every request (users may travel).

---

## Checklist: TZ audit

- [ ] Every `timestamp` column is `timestamptz` (or explicit UTC convention documented).
- [ ] No `datetime.now()` / `new Date()` / `time.time()` without TZ awareness in scheduling code.
- [ ] Every IANA TZ name (not abbreviation) stored and transported.
- [ ] DST policy documented for every local-wall-clock schedule.
- [ ] Tests cover at least one DST boundary per relevant TZ.
- [ ] tzdata version pinned in container images; refresh cadence documented.
- [ ] No Moment.js in new code; existing Moment usage has a migration ticket.
- [ ] User TZ preference stored, not inferred per-request.
