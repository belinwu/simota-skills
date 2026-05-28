# Swift Auto-Tuning Cheatsheet (Dial)

Agent-specific slice for **Dial** (continuous parameter auto-tuning — the `profile → tune → verify` feedback loop). Baseline assumes Swift 6.2+ / Xcode 26 (as of 2026-05).

This file does **not** duplicate the source of truth. Read it alongside:

- [`builder/references/swift-best-practices.md`](../../builder/references/swift-best-practices.md) — concurrency, networking, frameworks
- [`builder/references/swift-anti-patterns.md`](../../builder/references/swift-anti-patterns.md) — perf footguns, retain cycles, leak patterns
- [`builder/references/swift-language-spec.md`](../../builder/references/swift-language-spec.md) — Swift 6 concurrency, isolation regions, embedded constraints

The role of this cheatsheet: **catalogue the tunable parameters of a typical 2026 Swift app (iOS + server-side), the signals that justify changing each, and the hot-config primitives that let Dial close the loop without restarting**.

---

## 1. Why Swift has no GC tuning

Swift uses ARC (Automatic Reference Counting), not GC. The equivalent tuning surface is different:

| What you'd tune on JVM | Swift equivalent |
|------------------------|------------------|
| Heap size (`-Xmx`) | Process memory ceiling (system-defined; tune large-object lifecycle) |
| GC algorithm | (None — ARC is deterministic; tune `autoreleasepool` placement) |
| GC pause budget | Allocation churn (`drop` is deterministic, eager) |
| Object pool sizes | `NSCache` cost limits, `URLCache` capacity, your own pools |
| Thread pool count | `OperationQueue.maxConcurrentOperationCount`, `DispatchQueue` QoS |
| JIT thresholds | (None — Swift is AOT-compiled) |

**Implication for Dial**: the tuning surface is *structural* (pool sizes, queue concurrency, cache limits, request coalescing) and *temporal* (timeouts, debounce intervals, retry policies), not GC-pause-driven. Fewer continuous knobs, higher per-knob effect.

The closest analog to GC tuning is **autoreleasepool placement** in tight Foundation loops — see [`bolt/references/swift-cheatsheet.md §6`](../../bolt/references/swift-cheatsheet.md). Misplaced pools cause RSS climbs that look like leaks.

---

## 2. Parameter catalogue

Primary tunables in a typical 2026 Swift app. Each row: parameter / typical range / measurement signal / API.

### 2.1 URLSession

| Parameter | Typical range | Signal to tune | API |
|-----------|---------------|----------------|-----|
| `httpMaximumConnectionsPerHost` | `4`..`16` | SYN storms / per-host queueing under burst | `URLSessionConfiguration.httpMaximumConnectionsPerHost` |
| `timeoutIntervalForRequest` | `15s`..`60s` | Per-call timeout; tail of slow upstreams | `URLSessionConfiguration.timeoutIntervalForRequest` |
| `timeoutIntervalForResource` | `60s`..`24h` | End-to-end budget (esp. background download) | `URLSessionConfiguration.timeoutIntervalForResource` |
| `httpShouldUsePipelining` | `false` (default) | Rarely worth — HTTP/2 multiplexes already | Same |
| `waitsForConnectivity` | `true` for offline-tolerant | Spinner UX while waiting for network | `URLSessionConfiguration.waitsForConnectivity` |
| `requestCachePolicy` | `.useProtocolCachePolicy` default | Per-request override common | Same |
| `urlCache` | size param below | Per-session cache vs shared | `URLSessionConfiguration.urlCache` |

### 2.2 URLCache

| Parameter | Typical range | Signal | API |
|-----------|---------------|--------|-----|
| `memoryCapacity` | `4 MiB`..`64 MiB` | Memory budget; iOS termination signals | `URLCache(memoryCapacity:diskCapacity:)` |
| `diskCapacity` | `50 MiB`..`500 MiB` | Disk usage warning; eviction rate | Same |

**Common anti-pattern**: setting `URLCache.shared.memoryCapacity = 100MB` "for safety" with no measurement. iOS will respond to memory pressure by terminating; over-sizing the cache makes that more likely.

### 2.3 OperationQueue / Concurrency

| Parameter | Typical range | Signal | API |
|-----------|---------------|--------|-----|
| `maxConcurrentOperationCount` | `1`..`ProcessInfo.processInfo.activeProcessorCount * 2` | Throughput plateau / overcommit | `OperationQueue.maxConcurrentOperationCount` |
| `qualityOfService` | `.userInitiated` / `.utility` / `.background` | Energy / UI-priority trade | `OperationQueue.qualityOfService` |
| Task group concurrency | logical-cores ± | Same | `withTaskGroup { for _ in 0..<n { group.addTask {...} } }` |

For Swift Concurrency: `Task` does not have a thread-pool-size knob — the cooperative thread pool sizes itself to `processorCount` and adds blocking-aware spillover. You influence concurrency via:

- `TaskGroup` cap (semantic per-call concurrency).
- `Semaphore` / `AsyncSemaphore`.
- Custom `Executor` (Swift 6.0+).

### 2.4 DispatchQueue

| Parameter | Typical range | Signal | API |
|-----------|---------------|--------|-----|
| Concurrent count via QoS | Implicit (system-managed) | Thread explosion in Instruments → reduce QoS or batch | `DispatchQueue(label:..., attributes: .concurrent, target: ...)` |
| `setSpecific` for queue identification | (Identification, not capacity) | Detect queue reentrancy | `DispatchQueue.setSpecific(key:value:)` |
| `target` queue | Cascading priority | Coordinate priority hierarchy | `DispatchQueue(... target: rootQueue)` |

### 2.5 JSONDecoder / JSONEncoder

| Parameter | Typical range | Signal | API |
|-----------|---------------|--------|-----|
| `keyDecodingStrategy` | `.convertFromSnakeCase` common | Decode CPU per request | `JSONDecoder.keyDecodingStrategy` |
| `dateDecodingStrategy` | `.iso8601` for APIs | Date-parse CPU | `JSONDecoder.dateDecodingStrategy` |
| `nonConformingFloatDecodingStrategy` | `.throw` default | Inf/NaN handling | Same |
| Decoder reuse (per-actor static) | One-time-init perf | Constructor cost dominates on hot endpoints | See [`bolt/references/swift-cheatsheet.md §7`](../../bolt/references/swift-cheatsheet.md) |

### 2.6 UI debounce / coalescing

| Parameter | Typical range | Signal | API |
|-----------|---------------|--------|-----|
| Text-input debounce | `200ms`..`500ms` | Search-as-you-type API call rate | `Task.sleep`, Combine `.debounce`, AsyncSequence `.debounce` |
| Scroll-end coalescing | `100ms`..`300ms` | Frame drops during scroll | Same |
| Request coalescing | (semantic) | Duplicate in-flight requests | Actor-protected `[URLRequest: Task<...>]` registry |
| Task cancellation threshold | Per-feature | Cancel-on-rapid-input bursts | `Task.cancel()` + `Task.isCancelled` checks |

### 2.7 Combine throttle / debounce

| Parameter | Typical range | Signal | API |
|-----------|---------------|--------|-----|
| `.debounce(for: interval, scheduler: ...)` | Same as above | Same | `Publisher.debounce` |
| `.throttle(for: interval, scheduler: ..., latest: Bool)` | `latest: true` common | Spammy event stream | `Publisher.throttle` |

### 2.8 AsyncSequence buffer sizing

| Parameter | Typical range | Signal | API |
|-----------|---------------|--------|-----|
| `.buffer(_:)` | `1`..`128` | Producer outruns consumer | `AsyncSequence.buffer` (AsyncAlgorithms package) |
| Stream `bufferingPolicy` | `.bufferingNewest(N)` common | Backpressure / drop policy | `AsyncStream(bufferingPolicy:)` |

### 2.9 NSCache (image / data caches)

| Parameter | Typical range | Signal | API |
|-----------|---------------|--------|-----|
| `totalCostLimit` | `50 MiB`..`200 MiB` | Memory pressure; eviction rate | `NSCache.totalCostLimit` |
| `countLimit` | Per-resource | Long-tail of unique resources | `NSCache.countLimit` |
| `evictsObjectsWithDiscardedContent` | `true` default | iOS-only flag | `NSCache.evictsObjectsWithDiscardedContent` |

**Anti-pattern**: `NSCache.totalCostLimit = 1GB` without measuring cost-of-cost-eviction; cost computation runs on every `setObject(_, cost:)`.

### 2.10 Server-side Swift (Vapor / Hummingbird) tunables

| Parameter | Typical range | Signal | API |
|-----------|---------------|--------|-----|
| Event-loop count | physical cores | Worker idle %; saturated loops | `NIOMultiThreadedEventLoopGroup(numberOfThreads: N)` |
| DB connection pool (PostgresNIO) | `5`..`200` | Acquire wait p99; idle count | `PostgresClient.Configuration.maxConnections` |
| Connection idle timeout | `60s`..`10min` | LB/firewall idle disconnects | Same |
| HTTP/2 max streams per conn | `100`..`1000` | Per-conn fanout limits | Server config |
| Channel pool (RediStack) | `5`..`50` | Same as DB | `RedisConnectionPool.Configuration` |

---

## 3. Telemetry plumbing — what feeds the loop

Without telemetry, the tuning loop is open-loop and unsafe. Dial requires these signals exported before tuning starts.

### 3.1 OSLog `Logger`

```swift
import os

let logger = Logger(subsystem: "com.app.network", category: "session")
logger.log("request started \(request.url?.absoluteString ?? "")")
logger.debug("pool: \(pool.activeCount)/\(pool.maxCount)")
```

Structured signposts via `OSSignposter` (Xcode 13+):

```swift
let signposter = OSSignposter(subsystem: "com.app.tune", category: "pool")
let state = signposter.beginInterval("acquire", id: signposter.makeSignpostID())
// ... acquire connection
signposter.endInterval("acquire", state)
```

### 3.2 MetricKit (iOS, on-device)

Apple-provided production metrics, no opt-in needed beyond `MXMetricManager.shared.add(self)`:

- App launch time (cold / resume).
- Hangs (>250ms main-thread stalls).
- Crashes.
- Energy / CPU / location / cellular / WiFi metrics.
- Disk write / network.

```swift
class MetricsReceiver: NSObject, MXMetricManagerSubscriber {
    func didReceive(_ payloads: [MXMetricPayload]) {
        for p in payloads {
            // forward to Prometheus / Sentry / your TSDB
        }
    }
}
```

`MXDiagnosticPayload` (iOS 14+) gives in-the-field hang reports with stack traces.

### 3.3 swift-metrics + swift-distributed-tracing (server-side)

```swift
import Metrics
Counter(label: "requests_total").increment()
Timer(label: "pool.acquire.us").recordNanoseconds(elapsed)
Gauge(label: "pool.size").record(Double(pool.size))
```

Bootstrap with `PrometheusMetricsFactory` (swift-prometheus) for `/metrics` endpoint.

For traces: `swift-distributed-tracing` + an OTel exporter for end-to-end span propagation.

### 3.4 Required signals (Dial pre-flight)

Dial refuses to tune if these aren't exported:

- Wall-clock service p50/p95/p99 latency.
- Pool acquire-wait histogram (DB, HTTP client).
- Cache hit rate.
- Main-thread hang count (iOS — via MetricKit).
- RSS over time.
- Error / timeout rate.

---

## 4. Feedback-loop architecture (text diagram)

```
                  ┌──────────────────────────────────────┐
                  │  App (iOS or Server-side Swift)       │
                  │                                       │
                  │   ConfigSnapshot ◀── AsyncStream ◀──┐ │
                  │       │                             │ │
                  │       ▼                             │ │
                  │  URLSession / Pool / Cache / ...    │ │
                  └────────┬───────────────────────────┬┘ │
              OSLog/MetricKit/swift-metrics            │  │
                          ▼                            │  │
                ┌──────────────────────────┐           │  │
                │ Prometheus / TSDB /       │           │  │
                │ MetricKit aggregator      │           │  │
                └────────────┬─────────────┘           │  │
                             │                         │  │
                             ▼                         │  │
                ┌──────────────────────────┐           │  │
                │ Dial: candidate proposer │           │  │
                │   (Bayesian / grid)      │           │  │
                └────────────┬─────────────┘           │  │
                             │                         │  │
                             ▼                         │  │
                ┌──────────────────────────┐           │  │
                │ Candidate validator      │  reject ◀─┘  │
                │ (XCTMetric / A/B verify) │              │
                └────────────┬─────────────┘              │
                             │ accept                     │
                             ▼                            │
                ┌──────────────────────────────────────┐  │
                │ ConfigBus (UserDefaults / AsyncStream)│──┘
                └──────────────────────────────────────┘
```

### 4.1 Hot-reload primitives

| Primitive | Use |
|-----------|-----|
| `UserDefaults` + KVO | Single-scalar config (iOS); persists, observable |
| `NotificationCenter` | Broadcast config-change events to many listeners |
| `AsyncStream<Config>` | Modern push channel for config snapshots |
| `Actor.config: Config` (locked via actor isolation) | Strongly-typed actor-bounded config |
| Combine `CurrentValueSubject<Config, Never>` | Combine-native current+stream |
| Firebase Remote Config / LaunchDarkly | Server-driven config (background fetch) |

### 4.2 No-restart parameter swap pattern

```swift
actor ConfigStore {
    private(set) var current: Config

    private let continuation: AsyncStream<Config>.Continuation
    let updates: AsyncStream<Config>

    init(initial: Config) {
        self.current = initial
        var c: AsyncStream<Config>.Continuation!
        self.updates = AsyncStream { c = $0 }
        self.continuation = c
    }

    func set(_ new: Config) {
        current = new
        continuation.yield(new)
    }
}
```

Consumers:

```swift
for await cfg in configStore.updates {
    urlSession.configuration.timeoutIntervalForRequest = cfg.requestTimeout
}
```

For URLSession specifically, **changing the configuration on an existing `URLSession` does not affect in-flight tasks** — most properties take effect at session creation. Pattern: hold an `actor`-protected `URLSession` reference; on config change, build a new session and atomically swap. Drain the old one with a deadline.

---

## 5. Auto-tuning experiment harness

| Approach | Tool | When |
|----------|------|------|
| Manual sweep | XCTest + `XCTMetric` | First baseline; quick parameter screening |
| `XCTMetric` regression detection | XCTest performance | "Did this change move p95?" — built into Xcode |
| Bayesian opt | Custom (no canonical Swift lib) | Continuous params with expensive evaluation |
| Multi-armed bandit | Hand-rolled with metrics-driven reward | Online tuning, low risk per decision |
| Statistical significance | `XCTMetric` defaults | Built-in regression detection |

```swift
func testRequestThroughput() throws {
    let options = XCTMeasureOptions()
    options.iterationCount = 10
    measure(metrics: [XCTClockMetric(), XCTMemoryMetric()], options: options) {
        // workload to measure
    }
}
```

**Sample size discipline**: changing connection pool from 4→8 and seeing a 3% p95 drop is *noise* below ~10k requests. Wait for statistical significance (CI overlap test) before promoting a candidate to production.

For server-side, run a load test (`wrk`, `k6`, `vegeta`) against parameter variants and t-test the results.

---

## 6. Cost surfaces unique to Swift

When Dial reports a tuning recommendation, these Swift-specific costs need to be flagged:

| Knob | Hidden cost |
|------|------------|
| Raising `httpMaximumConnectionsPerHost` | TLS handshake count up; battery on cellular |
| Raising `URLCache.memoryCapacity` | iOS termination probability up under pressure |
| Raising `OperationQueue.maxConcurrentOperationCount` | Context-switch cost; main-thread starvation on lower QoS |
| Lowering `timeoutIntervalForRequest` | False-positive failures under tail latency |
| Adding `autoreleasepool` to every loop | Overhead per pool drain; usually only helps Foundation-heavy loops |
| Decreasing debounce | More API calls; battery / 429 risk |
| Increasing `NSCache.totalCostLimit` | iOS eviction unpredictable; not a strict bound |
| Raising server connection pool | DB-side connection limits / memory |
| Tuning per-environment (Debug vs Release) | Release optimizations change cost model; never tune in Debug |

---

## 7. Anti-patterns Dial must avoid

| Anti-pattern | Why it bites |
|--------------|-------------|
| **Setting `URLCache.shared.memoryCapacity` without measuring** | iOS responds to memory pressure unpredictably; oversize cache → app kill |
| **`NSCache.totalCostLimit` cargo cult** | "100 MB" picked from a Stack Overflow answer is no better than the default |
| **Tuning iOS knobs in Simulator** | Different memory ceiling, different ARC behavior, different network stack |
| **Tuning without MetricKit hang signal** | Hang rate is the *user-visible* metric; throughput without it is misleading |
| **Cancelling all in-flight Tasks on config swap** | Loses user work; design for graceful drain |
| **Continuous tuning of a workload that just got a new feature** | Cost model shifted. Re-baseline before tuning |
| **Pool size up + leave timeout same** | Joint knob: longer queue + same timeout = same error rate |
| **Optimizing for Debug build perf** | Different generic specialization, different ARC; meaningless |
| **JSONDecoder reuse vs concurrency safety** | `JSONDecoder` is safe to share IFF its state isn't mutated; verify before sharing |
| **MetricKit reports treated as real-time** | Daily batches by design — not for closed-loop tuning of sub-day signals |

---

## 8. Dial-specific routing rules

1. **Refuse to tune without telemetry.** If the user can't show histograms for latency p99, pool wait, and (iOS) MetricKit hang count, the first action is to instrument.
2. **iOS-app tunables vs server-side tunables differ.** Per-app session limits vs DB-side connection caps need separate playbooks.
3. **One knob at a time.** Multi-variable changes can't be statistically attributed.
4. **Build-time vs runtime knobs separated.** `SWIFT_OPTIMIZATION_LEVEL` is per-release; `httpMaximumConnectionsPerHost` is online.
5. **Hot-reload first, restart last.** `AsyncStream<Config>` covers almost every parameter. Restart only when the type itself changes (e.g., switching `URLSession` instance).
6. **Verify after each change.** `XCTMetric` regression check or A/B test with significance gate before promotion.
7. **Don't mistake autoreleasepool for GC.** It's a memory-locality knob, not a runtime GC dial.
8. **MetricKit is daily.** For sub-day loops, use OSLog signposts + your own TSDB.

---

## Sources

- WWDC — "What's new in MetricKit", "Get started with instruments", "Discover concurrency in SwiftUI"
- `OSSignposter` reference — https://developer.apple.com/documentation/os/ossignposter
- `MetricKit` reference — https://developer.apple.com/documentation/metrickit
- `XCTMetric` / XCTest performance — https://developer.apple.com/documentation/xctest/performance_tests
- swift-metrics — https://github.com/apple/swift-metrics
- swift-distributed-tracing — https://github.com/apple/swift-distributed-tracing
- swift-prometheus — https://github.com/swift-server-community/SwiftPrometheus
- URLSessionConfiguration — https://developer.apple.com/documentation/foundation/urlsessionconfiguration
- NSCache — https://developer.apple.com/documentation/foundation/nscache
- AsyncStream — https://developer.apple.com/documentation/swift/asyncstream
- Source of truth: [`builder/references/swift-best-practices.md`](../../builder/references/swift-best-practices.md), [`swift-anti-patterns.md`](../../builder/references/swift-anti-patterns.md), [`swift-language-spec.md`](../../builder/references/swift-language-spec.md)
