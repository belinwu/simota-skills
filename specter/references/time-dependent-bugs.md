# Time-Dependent Bug Reference

Purpose: Detect bugs that appear only at specific times or under clock-related conditions — timezone / DST boundaries, monotonic vs wall-clock confusion, clock skew across hosts, leap seconds, and tests that break when real time is used. Specter flags these as latent ghosts; Builder fixes them with proper time abstractions.

## Scope Boundary

- **Specter `time`**: Detection of time-dependent correctness bugs (DST, TZ, skew, monotonic misuse, leap seconds, unfrozen test clocks).
- **Tempo**: Scheduler / cron / retry / business-calendar *design*. If the task is "design a retry schedule" or "choose a cron expression", route to Tempo.
- **Probe**: Type-level date issues (Date vs string serialization, ISO-8601 contract drift). If TypeScript / schema work catches it, route to Probe.
- **Sentinel (resource perf)**: Timeout tuning and latency budgets. Specter detects *logic-breaking* time issues, not performance ones.

If the bug is "wrong result at DST boundary" → `time`. If it's "wrong cron schedule design" → Tempo. If it's "timeout too short under load" → Sentinel.

## Time Hazard Catalog

| Hazard | Example trigger | Typical symptom |
|--------|-----------------|-----------------|
| DST spring-forward | 2:30 AM on DST day | Off-by-one hour, duplicate or missing records at boundary |
| DST fall-back | 1:30 AM occurs twice | Double-execution of hourly job, ambiguous timestamps |
| TZ conversion drift | `new Date('2025-01-01')` parsed as UTC vs local | Dates shift by ±1 day near midnight |
| Wall-clock backstep | NTP slew, VM pause/resume, manual clock set | Negative durations, cache TTL wraparound |
| Monotonic misuse | `Date.now()` for elapsed time | Negative or zero elapsed across NTP adjust |
| Clock skew across hosts | Distributed lock, JWT `exp`, event ordering | Early token expiry, out-of-order log merge, double-lock |
| Leap second | 23:59:60 UTC | Duration math produces 0 or negative; sort order breaks |
| Unfrozen test clock | `new Date()` in test body | Test passes today, fails next month / next TZ |
| Epoch overflow | 32-bit `time_t` past 2038-01-19 | Wraparound to 1901 or negative |
| ISO format ambiguity | `2025-01-01` vs `2025-01-01T00:00:00Z` | Local vs UTC interpretation drift |

## Workflow

```
TRIAGE  →  map symptom: off-by-one, duplicate, missing, negative duration, skew
        →  3 hypotheses: (TZ/DST) (monotonic misuse) (test clock / skew)
        →  scope: business logic, scheduling, distributed coordination, or test

SCAN    →  grep: new Date\(\), Date.now\(\), time.time\(\), datetime.now\(\)
        →  grep TZ: getTimezoneOffset, tzset, pytz, zoneinfo, moment.tz
        →  grep monotonic: performance.now, process.hrtime, time.monotonic, CLOCK_MONOTONIC
        →  list cron / scheduled jobs; check DST handling
        →  list distributed locks, JWT, nonce, event ordering

ANALYZE →  classify each call: wall-clock-ok, needs-monotonic, needs-TZ-aware
        →  trace test fixtures for frozen vs real clock
        →  check skew tolerance on cross-host time comparisons

SCORE   →  DST/TZ bug affecting money or medical → CRITICAL
        →  monotonic misuse causing cache wrap → HIGH
        →  unfrozen test clock → MEDIUM (but wide blast radius)

REPORT  →  Bad→Good with the correct primitive; Builder handoff
```

## Monotonic vs Wall-Clock Decision Rule

```ts
// Bad: wall-clock for duration — NTP slew causes negative elapsed
const start = Date.now();
doWork();
const elapsed = Date.now() - start; // may be negative

// Good: monotonic for duration
const start = performance.now();    // or process.hrtime.bigint()
doWork();
const elapsed = performance.now() - start;

// Wall-clock is only correct for: display, audit log, business dates, TTL with skew tolerance
// Monotonic is required for: duration, rate-limit windows, timeouts, benchmarks
```

Rule: if the value is *compared with another clock value* in the same process, use monotonic. If it is *shown to a user or stored as a date*, use wall clock.

## TZ/DST Safe Patterns

```ts
// Bad: implicit local TZ, breaks across DST
const nextRun = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1, 2, 30);

// Good: explicit TZ-aware library (Temporal / Luxon / date-fns-tz)
import { Temporal } from '@js-temporal/polyfill';
const nextRun = Temporal.ZonedDateTime
  .from({ year, month, day, hour: 2, minute: 30, timeZone: 'America/Los_Angeles' })
  .add({ days: 1 });
// DST-aware: 2:30 AM on spring-forward day is automatically adjusted
```

For storage: always persist UTC + original TZ name (`America/Los_Angeles`), never a fixed offset (`-08:00`). Offsets become wrong twice a year.

## Clock-Skew Tolerance

Distributed systems need explicit skew windows.

```ts
// Bad: strict expiry check
if (jwt.exp < now) reject();

// Good: accept ±2min skew for token validation
const SKEW_MS = 2 * 60 * 1000;
if (jwt.exp * 1000 < now - SKEW_MS) reject();
```

Typical budgets: NTP-synced cluster ±100ms, cross-cloud ±500ms, client devices ±2min, ancient mobile ±5min. Design explicit tolerance — never assume clocks agree.

## Test-Clock Freeze

Unfrozen tests are latent time bombs. Freeze at suite boundary, not ad-hoc.

```ts
// Jest
beforeEach(() => { jest.useFakeTimers().setSystemTime(new Date('2025-06-15T12:00:00Z')); });
afterEach(() => { jest.useRealTimers(); });

// Sinon
const clock = sinon.useFakeTimers(new Date('2025-06-15T12:00:00Z'));

// Python
from freezegun import freeze_time
@freeze_time('2025-06-15 12:00:00')
```

Specter flags any test using `new Date()`, `Date.now()`, or equivalents without a freeze — these will eventually flake when the business date crosses a boundary (month end, year end, DST).

## Anti-Patterns

- Using `Date.now()` for rate-limit or timeout windows — NTP slew breaks it.
- Storing dates as `YYYY-MM-DD` strings without TZ — midnight drift across client/server.
- Using fixed offsets (`-08:00`) instead of TZ names (`America/Los_Angeles`) — wrong after DST.
- Writing cron at `2:30 AM` without documenting DST intent — spring-forward skips, fall-back duplicates.
- Comparing wall-clock timestamps across hosts without a skew window — silent JWT / lock bugs.
- Using `setTimeout(fn, dayMs)` for "run tomorrow" — DST adjusts the interval.
- Tests with real `Date()` that pass today — check them on 2025-03-09 (US DST) or Feb 29.
- Assuming `performance.now()` is wall-clock — it is process-relative only.
- 32-bit `time_t` in embedded / legacy C — 2038 problem.

## Handoff

**To Builder** (fix in code):
- Which primitive to use (monotonic vs wall-clock vs TZ-aware).
- TZ-name and skew budget to adopt.
- Required test-clock freeze points.
- Bad → Good snippet with concrete library choice.

**To Tempo** (scheduling redesign):
- When a recurring schedule spans DST, business calendars, or complex retry policies.
- Cron expressions needing TZ-aware rewrite.

**To Radar** (test additions):
- DST-boundary test cases (spring-forward, fall-back).
- Skew-tolerance tests for distributed lock / JWT.
- Leap-day / month-end / year-end fixtures.

**To Scout** (prior incidents):
- Any past outage correlated with DST, leap day, NTP resync, or year rollover.
