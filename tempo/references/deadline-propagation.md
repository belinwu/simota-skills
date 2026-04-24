# Deadline Propagation Across Async Boundaries

Purpose: Design a coherent deadline that travels with a request across process, network, and service boundaries so every downstream call inherits the remaining budget. Deadlines turn an unbounded retry storm into a bounded, predictable failure, and they let partial-progress return beat a full timeout hang. Read this when a request crosses two or more hops and no single component owns the end-to-end time budget.

## Scope Boundary

- **Tempo `deadline`**: end-to-end time-budget chain, context deadline propagation semantics, partial-progress-on-deadline policy, deadline-exceeded observability contract, cascading-timeout math.
- **Stream (elsewhere)**: pipeline and DAG implementation — deadline is one input Stream consumes; pipeline wiring, batching, and backpressure live there.
- **Gateway (elsewhere)**: HTTP/RPC layer timeout configuration (server read/write, client idle, keep-alive). Gateway owns the wire timeout; Tempo owns the logical deadline that must be shorter than it.
- **Beacon (elsewhere)**: SLO definition and time-budget monitoring (p99 latency, deadline-exceeded rate, error-budget burn). Tempo hands Beacon the target; Beacon alerts.

If the question is "what is the deadline budget and how is it split?" → `deadline`. If it is "how do I wire this through a Kafka/Airflow DAG?" → Stream. If it is "how do I configure nginx/envoy timeouts?" → Gateway. If it is "what alert fires when deadlines are exceeded?" → Beacon.

## Deadline vs Timeout

| Concept | Definition | Propagates? | Example |
|---------|-----------|-------------|---------|
| Timeout | Duration relative to NOW (`5s from here`) | No — resets at each hop | `fetch(url, { signal: AbortSignal.timeout(5000) })` |
| Deadline | Absolute instant (`finish by 10:00:03.200Z`) | Yes — encoded as a wall-clock or monotonic instant | Go `context.WithDeadline`, gRPC `grpc-timeout` header |

Deadlines are strictly more correct for multi-hop requests. Prefer deadlines; derive per-hop timeouts from the remaining deadline budget.

## Budget Chain Math

The budget chain rule: every hop spends some of the budget; downstream hops receive `deadline - (time_spent_upstream + network_margin)`.

```
Client budget   = 3000ms  ┐
                          │ network 50ms + queue 10ms
Gateway receives = 2940ms ┐
                          │ own work 80ms + network 30ms
Service A receives = 2830ms ┐
                          │ own work 200ms + DB call 150ms + fanout margin 50ms
Service B receives = 2430ms
```

Rule of thumb: reserve at least `RTT + 50ms` margin at each hop so the downstream sees a deadline it can actually meet, and so cancellation travels back up before the client gives up.

## Language / Runtime Patterns

### Go — `context.Context`

```go
ctx, cancel := context.WithDeadline(parent, deadline)
defer cancel()

if dl, ok := ctx.Deadline(); ok {
    remaining := time.Until(dl)
    if remaining < 100*time.Millisecond {
        return nil, fmt.Errorf("insufficient budget: %v", remaining)
    }
}

resp, err := client.Do(ctx, req) // ctx carries deadline down
```

### TypeScript / JS — `AbortSignal` with deadline

```ts
const deadline = Date.now() + 3000;
const signal = AbortSignal.timeout(deadline - Date.now());

async function hop(path: string, deadlineMs: number) {
  const remaining = deadlineMs - Date.now();
  if (remaining <= 50) throw new Error('deadline-exceeded');
  return fetch(path, { signal: AbortSignal.timeout(remaining - 20) });
}
```

Propagate the deadline as a header (`x-deadline-ms` or `grpc-timeout`), not as a relative timeout.

### gRPC — `grpc-timeout` header

Every gRPC call carries `grpc-timeout: <value><unit>` (e.g., `200m` for 200ms). The server computes the effective deadline and passes it into its own outbound calls. Do not add app-level timeouts on top — use `ctx.Deadline()` directly.

### Python — `asyncio.timeout` + context var

```python
deadline = loop.time() + 3.0
async with asyncio.timeout_at(deadline):
    result = await downstream(deadline=deadline)
```

Carry `deadline` as a function parameter (or a `contextvars.ContextVar`) across async boundaries.

## Partial Progress on Deadline

When the deadline fires mid-fanout, returning "everything or nothing" wastes the work done so far. Patterns:

| Pattern | When to use | Trade-off |
|---------|-------------|-----------|
| Best-effort batch | Fanout query (search, scatter-gather) | Return completed shards + mark missing with `partial=true` |
| Checkpoint + resume | Long-running job (ETL, backfill) | Persist watermark; resume from `watermark + 1` on next run |
| Degraded response | Enrichment layer (recommendations, ranking) | Return base result without the enrichment; flag `degraded=true` |
| Hard fail | Strict consistency (payment, booking) | Return deadline-exceeded; never partial-commit |

Document which pattern applies per endpoint. Silent partial returns are the worst outcome.

## Observability Contract

Every deadline-aware path emits:

- `deadline_ms_received` — budget at ingress
- `deadline_ms_remaining_on_exit` — budget handed to next hop
- `deadline_exceeded_total{hop,reason}` — counter
- `budget_consumed_ratio` — histogram of `1 - (remaining / received)`; helps find hops that eat too much

Hand these targets to Beacon at design time.

## Anti-Patterns

- Propagating a relative timeout (`timeout=3s`) across hops — each hop restarts the clock; total budget balloons.
- Setting per-hop timeouts greater than the inherited deadline — the deadline wins; the longer timeout is dead code and misleads readers.
- No margin between logical deadline and wire timeout — wire times out first, client sees a network error instead of a clean deadline-exceeded signal.
- Swallowing `context.Canceled` / `AbortError` as a generic error — loses the signal that the upstream already gave up.
- Retrying after deadline-exceeded — the caller is gone; retry is guaranteed waste.
- Cascading timeout trap: caller 2s, service 2s, DB 2s — any slow hop blows the whole chain; each inner hop must be strictly shorter than the inherited deadline.
- Hard-coded sleeps / fixed delays inside a deadline-bounded path — breaks the budget contract.
- Missing deadline on fanout — slowest shard drags the whole response; always apply `min(deadline, per_shard_budget)` per shard.

## Handoff

**To Builder:** deliver the budget chain table (per-hop allocation + margin), the propagation mechanism (context / header / signal), the partial-progress policy per endpoint, and the cancel-signal propagation path.

**To Gateway:** deliver the wire-timeout upper bound (must be ≥ logical deadline + margin) and the header name used to carry the deadline downstream.

**To Beacon:** deliver `deadline_exceeded_total`, `budget_consumed_ratio`, and the SLO target (e.g., `p99 remaining_on_exit > 200ms`) for alerting.

**To Voyager:** deliver test scenarios — deadline exactly at boundary, deadline already exceeded at entry, cancel mid-flight, partial fanout completion.
