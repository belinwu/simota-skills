# Time-Window Semantics for Analytics and Streams

Purpose: Define the time-window math that analytics and streaming workloads need — the shape of the window (tumbling / sliding / session), where the watermark sits, what counts as "late", and how two windowed streams join. A window specification is a contract: given input event-times, the system MUST emit one answer per window, and MUST be deterministic about which events belong to which window. Read this when aggregating events over time or building a windowed join.

## Scope Boundary

- **Tempo `window`**: window shape + watermark strategy + allowed-lateness + late-arrival policy + window-join semantics. Pure time math, platform-neutral.
- **Stream (elsewhere)**: pipeline implementation — Flink/Beam/Kafka Streams/Spark Structured Streaming wiring, operators, state backends, checkpointing. Stream consumes Tempo's window spec.
- **Gateway (elsewhere)**: request/response HTTP concerns — unrelated to event-time windowing.
- **Beacon (elsewhere)**: watermark-lag SLO, late-event rate dashboard, window-emission freshness alerts. Tempo hands the targets; Beacon observes.

If the question is "which events belong to which window, and when does the window close?" → `window`. If it is "how do I configure the Flink watermark strategy API?" → Stream. If it is "what alert fires when watermark lag exceeds 5 minutes?" → Beacon.

## Window Shapes

| Shape | Definition | Emits per | Use for |
|-------|-----------|-----------|---------|
| Tumbling | Fixed, non-overlapping, contiguous intervals of size `S` | Window | Hourly/daily aggregates, periodic rollups |
| Sliding | Fixed size `S`, advances by step `P` (where `P < S`); windows overlap | Slide step | Moving averages, N-minute rolling counts |
| Session | Dynamic; opens on event, closes after `gap` of inactivity | Session | User sessions, device bursts, conversation turns |
| Global + trigger | One unbounded window; custom trigger fires emission | Trigger | Custom aggregations with bespoke firing logic |

```
Tumbling (S=5m):
[00:00-00:05)[00:05-00:10)[00:10-00:15) ...

Sliding (S=5m, P=1m):
[00:00-00:05)
  [00:01-00:06)
    [00:02-00:07) ...

Session (gap=30m):
e1--e2---e3-------------e4---e5
└─── session A ─┘       └session B┘
      (gap < 30m)       (gap > 30m)
```

Event-time vs processing-time: always prefer **event-time** for windows. Processing-time windows look simple but silently mis-bucket under backpressure, replay, or clock skew.

## Watermark Design

A watermark is a monotonic marker asserting "no event older than T will arrive." It drives when a window is safe to close.

| Strategy | Definition | Trade-off |
|---------|-----------|-----------|
| Perfect | Watermark = max(event_time) seen, minus 0 | Lowest latency, wrong if any event is late |
| Bounded-out-of-orderness | max(event_time) - `maxDelay` | Common default; pick `maxDelay` from observed p99 lateness |
| Punctuated | Emit watermark on explicit marker events | Accurate when source emits completion markers (end-of-partition) |
| Periodic | Emit watermark on a wall-clock tick | Simple; tune emit interval (typically 200ms - 1s) |
| Idle-source fallback | Advance watermark on idle partition after `idleTimeout` | Prevents stuck pipelines when one partition has no traffic |

Rule: set `maxDelay` from a measured lateness distribution, not a guess. If p99 observed lateness is 2m, a 30s bound drops 1%+ of events silently.

## Allowed Lateness & Late-Arrival Handling

After the watermark closes a window, events can still arrive (clock skew, mobile buffering, upstream outage recovery). Policy options:

| Policy | Behavior | Cost |
|--------|----------|------|
| Drop | Discard events arriving after window close | Cheapest; data loss |
| Side output | Route late events to a dedicated "late" stream/topic | Preserves data; downstream must re-ingest |
| Allowed lateness + re-fire | Keep window state for `allowedLateness`; re-emit updated result on late event | Correct; state cost |
| Retraction | Emit negative delta to revise the prior window answer | Consumer must handle retractions |

Pick one policy per window and document it. Default for analytics dashboards: `allowedLateness = maxDelay × 2` with re-fire semantics.

## Window Join

Two streams can be joined within a window. The join semantics depend on the window shape:

```ts
// Stream A ⨝ Stream B on key within ±2m
streamA
  .keyBy(e => e.userId)
  .intervalJoin(streamB.keyBy(e => e.userId))
  .between(Time.minutes(-2), Time.minutes(2))
  .process((a, b, ctx, out) => out.collect({ a, b }));
```

| Join type | Semantics |
|-----------|-----------|
| Tumbling window join | Pair events falling in the SAME tumbling window |
| Sliding window join | Pair events falling in at least one shared sliding window |
| Interval join | Pair event A with B if `A.time + lowerBound ≤ B.time ≤ A.time + upperBound` |
| Session window join | Pair events belonging to the SAME session (per key) |

Key hazard: asymmetric lateness between A and B. If A is 30s late and B is on time, the window must wait for A's watermark, not just B's — watermark in a join = min(upstream watermarks).

## Language Sketches

### Python (pure, no framework)

```python
from collections import defaultdict

def tumbling(events, size_s: int):
    buckets = defaultdict(list)
    for e in events:
        key = (e.event_time // size_s) * size_s
        buckets[key].append(e)
    return buckets

def session(events, gap_s: int):
    events = sorted(events, key=lambda e: e.event_time)
    sessions, current, last_t = [], [], None
    for e in events:
        if last_t is None or e.event_time - last_t <= gap_s:
            current.append(e)
        else:
            sessions.append(current); current = [e]
        last_t = e.event_time
    if current: sessions.append(current)
    return sessions
```

### TypeScript (sliding window count)

```ts
function slidingCount(events: Event[], sizeMs: number, stepMs: number) {
  const out: { start: number; end: number; count: number }[] = [];
  const minT = Math.min(...events.map(e => e.t));
  const maxT = Math.max(...events.map(e => e.t));
  for (let s = minT; s < maxT; s += stepMs) {
    const e = s + sizeMs;
    const count = events.filter(x => x.t >= s && x.t < e).length;
    out.push({ start: s, end: e, count });
  }
  return out;
}
```

## Anti-Patterns

- Mixing processing-time and event-time windows in the same pipeline — results become non-reproducible.
- Using wall-clock `NOW` as the watermark — any backpressure corrupts every window.
- `allowedLateness = 0` with `drop` policy, then surprise at "missing" data — it was silently discarded.
- Tumbling windows aligned to epoch 0 in a specific timezone without stating which — the first window of the day shifts by DST.
- Session gap shorter than p99 inter-event time — splits real sessions into fragments.
- Sliding windows with step much smaller than size (`S=1h, P=1s`) — emits 3600× more output than intended; explodes downstream state.
- Window join without ensuring matching key partitioning on both streams — runs, produces empty results, no error.
- Trusting the wall clock of the producer — device clocks drift; for mobile events, bound `maxDelay` by observed skew (often multi-minute).

## Handoff

**To Stream:** deliver the window shape (tumbling/sliding/session with parameters), the watermark strategy, `maxDelay`, `allowedLateness`, late-event policy, and join semantics. Stream chooses the framework operator and state backend.

**To Beacon:** deliver watermark-lag SLO (e.g., `p99 < 30s`), late-event rate budget, and window-emission freshness alert (`no emission > 2 × size`).

**To Voyager:** deliver test scenarios — exact-boundary events, p99-late events, out-of-order bursts, idle-partition watermark advance, and window-join with asymmetric lateness.

**To Builder:** deliver the window-output contract (schema of emitted rows, retraction policy if any, key type, timestamp field) so the downstream consumer handles it correctly.
