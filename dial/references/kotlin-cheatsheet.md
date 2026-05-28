# Kotlin Auto-Tuning Cheatsheet (Dial)

Agent-specific slice for **Dial** (continuous parameter auto-tuning — the `profile → tune → verify` feedback loop). Baseline assumes Kotlin 2.3+ / K2 compiler / JDK 21+ (as of 2026-05).

This file does **not** duplicate the source of truth. Read it alongside:

- [`builder/references/kotlin-best-practices.md`](../../builder/references/kotlin-best-practices.md) — coroutines, Flow patterns, JVM interop, server-side frameworks
- [`builder/references/kotlin-anti-patterns.md`](../../builder/references/kotlin-anti-patterns.md) — leaks, blocking IO, GlobalScope, dispatcher misuse
- [`builder/references/kotlin-language-spec.md`](../../builder/references/kotlin-language-spec.md) — Kotlin 2.x semantics, K2 compiler, KMP, K/Native

The role of this cheatsheet: **catalogue the tunable parameters of a typical 2026 Kotlin service (server-side JVM + Android), the signals that justify changing each, and the hot-config primitives that let Dial close the loop without restarting**.

---

## 1. Parameter catalogue

Primary tunables in a typical 2026 Kotlin app. Each row: parameter / typical range / measurement signal / API.

### 1.1 Coroutines — Dispatchers

| Parameter | Typical range | Signal to tune | API |
|-----------|---------------|----------------|-----|
| `Dispatchers.Default` thread count | `Runtime.getRuntime().availableProcessors()` | CPU-bound saturation | Override via `kotlinx.coroutines.scheduler.core.pool.size` system prop |
| `Dispatchers.IO` max threads | `64`..`1024` (default expands to 64-cap) | Blocking IO saturation; thread count | `kotlinx.coroutines.io.parallelism` system prop |
| `Dispatchers.IO.limitedParallelism(n)` | `8`..`200` | Bounded subset for one workload | Per-workload at use site |
| Custom dispatcher (fixed pool) | physical-cores ± | When work has different priority class | `Executors.newFixedThreadPool(n).asCoroutineDispatcher()` |
| Virtual-thread dispatcher (JDK 21+) | unbounded | Blocking IO with high fanout | `Executors.newVirtualThreadPerTaskExecutor().asCoroutineDispatcher()` |

**JDK 21+ pattern** — virtual threads for blocking IO:

```kotlin
val loomIO = Executors.newVirtualThreadPerTaskExecutor().asCoroutineDispatcher()

suspend fun fetchUser(id: Long): User = withContext(loomIO) {
    jdbi.withHandle { it.queryUser(id) }  // blocking JDBC — fine on virtual thread
}
```

~30x faster than `Dispatchers.IO` for blocking-IO-heavy workloads (2025 measurements). Caveat: `synchronized` still pins to carrier thread until JDK 23.

### 1.2 Connection pool — HikariCP

| Parameter | Typical range | Signal | API |
|-----------|---------------|--------|-----|
| `maximumPoolSize` | `5`..`50` (rarely higher) | Acquire wait p99 / DB-side connection cap | `HikariConfig.maximumPoolSize` |
| `minimumIdle` | `0`..`maximumPoolSize` (often == max) | Cold-start latency on first request | `HikariConfig.minimumIdle` |
| `connectionTimeout` | `1s`..`30s` | "Acquire timeout" exception rate | `HikariConfig.connectionTimeout` |
| `idleTimeout` | `60s`..`10min` | LB/firewall idle disconnects | `HikariConfig.idleTimeout` |
| `maxLifetime` | `30min`..`30min` (DB-side cap aware) | Stale connections through LBs | `HikariConfig.maxLifetime` |
| `leakDetectionThreshold` | `30s`..`60s` (dev) / off (prod) | Connection-leak alerts | `HikariConfig.leakDetectionThreshold` |
| `validationTimeout` | `5s` | Liveness check time budget | `HikariConfig.validationTimeout` |

**Rule of thumb**: `maximumPoolSize ≈ cores_db_machine * 2 + spindles`. Higher is usually slower (DB-side contention exceeds throughput gain). Source: HikariCP own docs + the classic PostgreSQL benchmark series.

### 1.3 Ktor server

| Parameter | Typical range | Signal | API |
|-----------|---------------|--------|-----|
| `workerGroup` size (CIO) | physical cores | Worker idle %; saturated loops | `embeddedServer(CIO) { connectionGroupSize = N; workerGroupSize = N; callGroupSize = N }` |
| `callGroup` size | `2 * cores` to `4 * cores` | Request-handling stalls | Same |
| `connectionGroup` size | `1`..`physical cores / 2` | Accept-loop backlog | Same |
| `responseWriteTimeoutSeconds` | `10s`..`60s` | Slow-client drain | `application.install(...)` per-engine |
| `requestQueueLimit` (Netty) | `16`..`1024` | Overload shedding threshold | Engine-specific |

### 1.4 Ktor client

| Parameter | Typical range | Signal | API |
|-----------|---------------|--------|-----|
| Engine choice | CIO / OkHttp / Apache | Per-engine perf differs | `HttpClient(CIO)` or `HttpClient(OkHttp)` |
| Connection pool (engine-specific) | `10`..`100 per host` | Per-host queueing | OkHttp: `OkHttpClient.Builder().connectionPool(...)`; CIO: `engine { endpoint { maxConnectionsPerRoute = N } }` |
| Request timeout | `5s`..`60s` | Tail latency on slow upstreams | `HttpTimeout` plugin |
| Connect timeout | `1s`..`10s` | DNS / SYN tail | Same |
| Socket timeout | `30s`..`5min` | Per-byte read budget | Same |
| Keep-alive | (engine default) | Re-handshake rate | Engine-specific |

### 1.5 kotlinx.serialization JSON

| Parameter | Typical setting | Signal | API |
|-----------|----------------|--------|-----|
| `encodeDefaults` | `false` (default) | Output size; downstream parser cost | `Json { encodeDefaults = false }` |
| `ignoreUnknownKeys` | `true` for resilient clients | Schema-drift failure rate | Same |
| `prettyPrint` | `false` in prod | Output size + CPU | Same |
| `coerceInputValues` | `false` default | Skips strict validation | Same |
| `explicitNulls` | `false` (Kotlin 1.7+) | Smaller output | Same |

Json instance is `Serializable` and thread-safe; reuse as a singleton.

### 1.6 StateFlow / SharedFlow

| Parameter | Typical range | Signal | API |
|-----------|---------------|--------|-----|
| `MutableSharedFlow(replay)` | `0`..`64` | Late-subscriber catch-up needs | `MutableSharedFlow<T>(replay = N)` |
| `extraBufferCapacity` | `0`..`128` | Producer/consumer rate mismatch | `MutableSharedFlow<T>(extraBufferCapacity = N)` |
| `onBufferOverflow` | `SUSPEND` / `DROP_OLDEST` / `DROP_LATEST` | Backpressure semantics | Same |
| StateFlow (always replay=1) | (no knob) | Cold-subscribe consistency | `MutableStateFlow(initial)` |

### 1.7 Channel

| Parameter | Typical range | Signal | API |
|-----------|---------------|--------|-----|
| `Channel<T>()` (default RENDEZVOUS) | `0` capacity | Strict producer-consumer sync | `Channel<T>()` |
| `Channel<T>(N)` (buffered) | `16`..`1024` | Producer outruns consumer | `Channel<T>(N)` |
| `Channel<T>(Channel.CONFLATED)` | conflates to latest | UI state / sensor stream | `Channel<T>(Channel.CONFLATED)` |
| `Channel<T>(Channel.UNLIMITED)` | unbounded — danger | Memory blowup if consumer lags | Avoid in prod |

### 1.8 JVM heap + GC

| Parameter | Typical range | Signal | Flag |
|-----------|---------------|--------|------|
| `-Xmx` (max heap) | Application-specific | OOM risk; container memory limit | `-Xmx4g` |
| `-Xms` (initial heap) | == `-Xmx` for servers | Allocation expansion pauses | `-Xms4g` |
| `-XX:MaxGCPauseMillis` | `100`..`500` (G1) | Tail latency vs throughput | `-XX:MaxGCPauseMillis=200` |
| GC algorithm | G1 / ZGC / Shenandoah / Parallel | Pause budget vs throughput | `-XX:+UseG1GC` / `-XX:+UseZGC` |
| `-XX:TieredCompilation` | `true` default | Warm-up time vs steady-state | Default on |
| `-XX:ReservedCodeCacheSize` | `240m`..`512m` | "Code Cache full" warning | `-XX:ReservedCodeCacheSize=512m` |
| `-XX:+UseStringDeduplication` (G1) | toggle | String-heavy heap savings | Same |
| AOT class data (CDS) | filename | Startup time | `-XX:SharedArchiveFile=app.jsa` |

**For server-side 2026 default**: G1GC with default settings is fine for most apps; switch to ZGC when tail-latency is the goal (p99 GC pause > business SLA).

### 1.9 Project Loom (JDK 21+)

| Parameter | Typical range | Signal | API |
|-----------|---------------|--------|-----|
| Virtual-thread executor | unbounded by design | Blocking-IO scalability ceiling | `Executors.newVirtualThreadPerTaskExecutor()` |
| Carrier thread pool size | `Runtime.cores` default | Capacity of pinned operations | `-Djdk.virtualThreadScheduler.parallelism=N` |
| Pinned-operation diagnosis | (telemetry only) | `synchronized` blocks pinning | `-Djdk.tracePinnedThreads=full` |

Pinning audit is critical before switching to virtual threads — any `synchronized` block (incl. internals of libraries) defeats the purpose by pinning to the carrier OS thread.

### 1.10 Kotlin/Native memory manager

| Parameter | Typical range | Signal | API |
|-----------|---------------|--------|-----|
| `Worker` count (K/Native) | Application-specific | Concurrent work scaling | `Worker.start()` per worker |
| Memory model | strict (default since 1.7.20) | Crash on cross-worker freeze violations | (Build option) |
| GC trigger threshold | (K/Native internal) | Heap shape, allocation rate | Build flags |

K/Native runtime tuning is rougher and less mature than JVM. See [`kotlin-language-spec.md §7`](../../builder/references/kotlin-language-spec.md) for the K/Native runtime detail.

---

## 2. Telemetry plumbing — what feeds the loop

Without telemetry, the tuning loop is open-loop and unsafe. Dial requires these signals exported before tuning starts.

### 2.1 Micrometer + Prometheus

```kotlin
import io.micrometer.core.instrument.MeterRegistry
import io.micrometer.prometheusmetrics.PrometheusMeterRegistry

val registry: MeterRegistry = PrometheusMeterRegistry(PrometheusConfig.DEFAULT)

registry.timer("pool.acquire").record(Duration.ofMillis(latency))
registry.gauge("pool.active", pool, { it.activeConnections.toDouble() })
registry.counter("requests.total", "endpoint", path).increment()
```

Standard for Spring / Ktor / Vert.x — exposes `/metrics` (Prometheus format) or push to InfluxDB / OTLP.

### 2.2 OpenTelemetry (OTel)

```kotlin
val tracer = openTelemetry.getTracer("com.app.service")
val span = tracer.spanBuilder("fetchUser").startSpan()
span.setAttribute("user.id", id)
try { /* work */ } finally { span.end() }
```

Auto-instrumentation agent (`-javaagent:opentelemetry-javaagent.jar`) covers JDBC, HTTP client/server, Kafka, Redis, etc. without code changes.

### 2.3 kotlinx.coroutines DebugProbes

```kotlin
// In tests / canary instances only — significant overhead
DebugProbes.install()

// Dump coroutine state
DebugProbes.dumpCoroutines(System.out)
```

Production-safe variants ship in `kotlinx-coroutines-debug` artifact; use sparingly (10-30% overhead).

### 2.4 JMX / JFR

JMX exposes JVM internals (GC, threads, memory pools) for any monitoring tool. JFR is the production-grade always-on profiler — emit a continuous `.jfr` file with `-XX:StartFlightRecording=filename=app.jfr,maxage=4h,settings=profile`.

### 2.5 Required signals (Dial pre-flight)

Dial refuses to tune if these aren't exported:

- Wall-clock service p50/p95/p99 latency (per endpoint).
- Pool acquire wait histogram (HikariCP `hikaricp_pending_threads` + acquire timer).
- Coroutine debug count (or task count proxy).
- JVM heap utilization + GC pause histogram.
- Thread count over time.
- Error/timeout rate.

---

## 3. Feedback-loop architecture (text diagram)

```
                  ┌──────────────────────────────────────┐
                  │  App (Ktor / Spring / Compose)        │
                  │                                       │
                  │   ConfigSnapshot ◀── StateFlow ◀───┐  │
                  │       │                            │  │
                  │       ▼                            │  │
                  │  HikariCP / Ktor / Coroutines / ...│  │
                  └────────┬──────────────────────────┬┘  │
              Micrometer / OTel / JFR / JMX           │   │
                          ▼                           │   │
                ┌──────────────────────────┐          │   │
                │ Prometheus / Tempo /     │          │   │
                │ Loki / OTLP collector    │          │   │
                └────────────┬─────────────┘          │   │
                             │                        │   │
                             ▼                        │   │
                ┌──────────────────────────┐          │   │
                │ Dial: candidate proposer │          │   │
                │   (Bayesian / grid)      │          │   │
                └────────────┬─────────────┘          │   │
                             │                        │   │
                             ▼                        │   │
                ┌──────────────────────────┐          │   │
                │ Candidate validator      │  reject ◀┘   │
                │ (A/B verify, JMH check)  │              │
                └────────────┬─────────────┘              │
                             │ accept                     │
                             ▼                            │
                ┌──────────────────────────────────────┐  │
                │ ConfigBus (StateFlow / Spring Cloud)  │──┘
                └──────────────────────────────────────┘
```

### 3.1 Hot-reload primitives

| Primitive | Use |
|-----------|-----|
| `MutableStateFlow<Config>` | Push-current snapshot to all consumers |
| `MutableSharedFlow<Config>(replay = 1)` | Same but no required initial |
| Spring Cloud `@RefreshScope` | Spring-native config refresh |
| Konsist + validation | Compile-time config schema |
| Flagsmith / LaunchDarkly Kotlin SDK | Centralised feature-flag-style toggles |
| Custom `ConfigStore` actor (single-writer) | Strongly-typed in-process bus |

### 3.2 No-restart parameter swap pattern

```kotlin
class ConfigStore(initial: Config) {
    private val _config = MutableStateFlow(initial)
    val config: StateFlow<Config> = _config.asStateFlow()

    fun update(new: Config) { _config.value = new }
}

// Consumer
configStore.config
    .map { it.connectionTimeout }
    .distinctUntilChanged()
    .collect { newTimeout ->
        hikari.connectionTimeout = newTimeout.toMillis()  // HikariCP supports runtime change
    }
```

HikariCP supports many parameters at runtime (`maximumPoolSize`, `connectionTimeout`, `idleTimeout`, `maxLifetime`). Some require pool drain + rebuild (`username`, `jdbcUrl`).

For Ktor servers, engine config changes require server restart — pattern: spawn a new engine with the new config, drain the old one, point load balancer.

---

## 4. Auto-tuning experiment harness

| Approach | Tool | When |
|----------|------|------|
| Manual sweep | `kotlinx-benchmark` (JMH) | First baseline; quick parameter screening |
| Bayesian opt | OpenJDK Loom + custom; `Java-BayesOpt` libs | Continuous parameters with expensive evaluation |
| Multi-armed bandit | Hand-rolled with Micrometer reward | Online tuning, low risk per decision |
| A/B (feature flag) | Flagsmith / LaunchDarkly SDK | Production rollout, statistical sig from Prometheus |
| Statistical significance | JMH built-in (Wilcoxon), or t-test on Prometheus query | "Did this change actually move the needle?" |

JMH harness setup is identical to the Bolt cheatsheet — see [`bolt/references/kotlin-cheatsheet.md §2`](../../bolt/references/kotlin-cheatsheet.md).

**Sample size discipline**: bumping pool size 8→16 and seeing a 3% p95 drop is *noise* below ~10k requests. Wait for statistical significance before promoting.

---

## 5. JVM auto-tuning specifics

### 5.1 Hotspot ergonomics — default heap sizing

JVM picks initial / max heap based on system memory:

- Server-class machines (cores ≥ 2 + memory ≥ 2GB): `-Xms` = 1/64th, `-Xmx` = 1/4th of system RAM (capped at 25GB on most platforms).
- Container-aware sizing (JDK 10+): `+UseContainerSupport` reads cgroup limits.

For tuned servers, **set `-Xms == -Xmx`** to avoid the resize pause; pick the value based on JFR heap histogram + GC frequency.

### 5.2 ZGC vs G1 — when each wins

| Workload | Winner | Why |
|----------|--------|-----|
| Default web service, 2-8 GB heap, P99 SLA ≥ 200ms | **G1GC** | Throughput edge; default works |
| Same but P99 GC-pause budget < 10ms | **ZGC** | Sub-millisecond pauses |
| Heap > 32 GB | **ZGC** | G1 pause time grows with heap |
| Batch / throughput-only | **ParallelGC** | Max throughput; long pauses OK |
| Short-lived CLI (Gradle worker, scripts) | **Epsilon** (no-op) | Doesn't GC at all |

Decision rule: enable ZGC if your p99 GC pause histogram (from JFR) exceeds your latency budget. Otherwise stay on G1.

### 5.3 Coroutine debug mode

```bash
-Dkotlinx.coroutines.debug=on
```

Adds coroutine identity tags to stack traces. ~5% overhead; reasonable for canary instances. Not for production.

---

## 6. Cost surfaces unique to Kotlin / JVM

| Knob | Hidden cost |
|------|------------|
| Raising HikariCP `maximumPoolSize` | DB-side connection count up; lock contention rises non-linearly |
| Raising `Dispatchers.IO` parallelism | Context-switch cost; doesn't help if real bottleneck is downstream |
| Switching to virtual threads | `synchronized` blocks now hurt; cgroup-bound IO is the new ceiling |
| Lowering connection timeout | False-positive failures under tail latency |
| Increasing `Channel` capacity | Latency floor up under saturation; hides backpressure |
| `extraBufferCapacity` on SharedFlow | Memory growth; late-subscribers see stale data |
| Switching to ZGC | 2-15% throughput trade for pause goal |
| Increased `-Xmx` | Cold-start initialization longer; bigger checkpoint cost in container restarts |
| `replay > 0` on SharedFlow | Memory growth per subscriber |
| Larger compiled binary (compose, KSP) | Cold-start time up; bigger CDS archive |

---

## 7. Anti-patterns Dial must avoid

| Anti-pattern | Why it bites |
|--------------|-------------|
| **`maximumPoolSize = 200` "for safety"** | DB-side runs out of file descriptors / processes before pool fills |
| **Tuning `Dispatchers.IO` parallelism for CPU-bound work** | Wrong dispatcher; switch to `Default` or custom CPU pool |
| **Switching to virtual threads without auditing `synchronized`** | Pins to carrier thread; perf can *regress* |
| **`Channel.UNLIMITED` everywhere** | Hides backpressure; OOM time bomb |
| **`-Xmx16g` because "memory is cheap"** | Cold start + checkpoint cost up; container kill on OOM still happens |
| **Tuning without JFR pause histogram** | "Long GC pauses" without evidence is folklore |
| **One-knob-at-a-time skipped because "obvious correlation"** | Joint effects (pool size × timeout) misattributed |
| **Tuning in dev environment** | JIT warm-up, heap shape, DB load differ — meaningless |
| **GlobalScope.launch for "isolation"** | Leaks coroutines; no parent cancellation |
| **`runBlocking` in HTTP handler** | DoS surface; blocks event loop |
| **Continuous tuning across deploys with feature changes** | Cost model shifted; re-baseline before re-tune |

---

## 8. Dial-specific routing rules

1. **Refuse to tune without telemetry.** If the user can't show Micrometer histograms for p99, pool wait, and GC pause, the first action is to instrument.
2. **JVM tunables vs Kotlin tunables vs app tunables — distinct.** GC choice (JVM), dispatcher parallelism (Kotlin runtime), pool sizes (app) need separate playbooks.
3. **One knob at a time.** Multi-variable changes can't be statistically attributed. Bayesian opt is the exception.
4. **Hot-reload first, restart last.** `StateFlow<Config>` + HikariCP runtime setters cover most params. Restart only when the type itself changes.
5. **Virtual threads need pinning audit first.** Don't switch blindly; verify `synchronized` blocks aren't on hot paths.
6. **ZGC is not free.** Don't switch without measuring G1 baseline first.
7. **Coroutine count is a signal, not a target.** Many cheap coroutines are fine; expensive ones in `runBlocking` are not.
8. **Build-time vs runtime knobs separated.** Kotlin compiler flags / Compose stable annotations are per-release; pool sizes are online.

---

## Sources

- Micrometer — https://micrometer.io/
- OpenTelemetry Java — https://opentelemetry.io/docs/instrumentation/java/
- kotlinx.coroutines debug — https://github.com/Kotlin/kotlinx.coroutines/blob/master/kotlinx-coroutines-debug/README.md
- HikariCP wiki — https://github.com/brettwooldridge/HikariCP/wiki
- Ktor server configuration — https://ktor.io/docs/server-engines.html
- Ktor client engines — https://ktor.io/docs/client-engines.html
- JEP 444 Virtual Threads — https://openjdk.org/jeps/444
- JEP 439 Generational ZGC — https://openjdk.org/jeps/439
- G1GC tuning — https://docs.oracle.com/en/java/javase/21/gctuning/garbage-first-g1-garbage-collector1.html
- Kotlin Flow — https://kotlinlang.org/docs/flow.html
- Spring Cloud Config — https://spring.io/projects/spring-cloud-config
- kotlinx-benchmark — https://github.com/Kotlin/kotlinx-benchmark
- Source of truth: [`builder/references/kotlin-best-practices.md`](../../builder/references/kotlin-best-practices.md), [`kotlin-anti-patterns.md`](../../builder/references/kotlin-anti-patterns.md), [`kotlin-language-spec.md`](../../builder/references/kotlin-language-spec.md)
