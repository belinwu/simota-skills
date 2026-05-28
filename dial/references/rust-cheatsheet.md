# Rust Auto-Tuning Cheatsheet (Dial)

Agent-specific slice for **Dial** (continuous parameter auto-tuning — the `profile → tune → verify` feedback loop). Baseline assumes Rust 1.85+ / Edition 2024 (as of 2026-05).

This file does **not** duplicate the source of truth. Read it alongside:

- [`builder/references/rust-best-practices.md §6 Performance practices`](../../builder/references/rust-best-practices.md) — profilers, allocators, build-profile tuning
- [`builder/references/rust-best-practices.md §8 Async ecosystem`](../../builder/references/rust-best-practices.md) — Tokio runtime, Tower backpressure, structured concurrency
- [`builder/references/rust-best-practices.md §9 Production crate matrix`](../../builder/references/rust-best-practices.md) — connection pooling, caching, logging/tracing
- [`builder/references/rust-anti-patterns.md §6 Performance Pitfalls`](../../builder/references/rust-anti-patterns.md)

The role of this cheatsheet: **catalogue the tunable parameters of a typical 2026 Rust service, the signals that justify changing each, and the hot-reload primitives that let Dial close the loop without a restart**.

---

## 1. Why Rust has no GC tuning

The first surprise migrating tuning playbooks from JVM/Go: **there is no GC** to tune in Rust. The equivalent levers are:

| What you'd tune on JVM | Rust equivalent |
|------------------------|----------------|
| Heap size (`-Xmx`) | Allocator + `Vec::with_capacity` discipline |
| Young gen ratio | (No equivalent — no generational allocator) |
| GC algorithm (G1, ZGC, Shenandoah) | Global allocator (mimalloc / jemalloc / snmalloc) |
| GC pause budget | Allocation churn (drop is deterministic, eager) |
| `MaxDirectMemorySize` | Buffer/pool sizes (`bytes::BytesMut::with_capacity`, `bumpalo::Bump`) |
| Thread pool (Tomcat workers, Vert.x event loop) | Tokio worker thread count + Tower concurrency limit |
| JIT compilation thresholds | LTO / PGO build-time decision (one-shot, not runtime) |
| `-XX:+UseG1GC -XX:MaxGCPauseMillis=...` | Allocator choice + `#[global_allocator]` |

**Implication for Dial**: the tuning surface is *structural* (pool sizes, channel capacities, allocator) and *build-time* (LTO, codegen-units, opt-level), not runtime-pause-driven. The optimization loop has fewer continuous knobs but higher per-knob effect.

---

## 2. Parameter catalogue

Primary tunables in a typical 2026 Rust service (Tokio + axum + sqlx + reqwest + moka). Each row: parameter / typical range / measurement signal / crate.

### 2.1 Async runtime

| Parameter | Typical range | Signal to tune | Crate / API |
|-----------|---------------|----------------|------------|
| `worker_threads` | `1`..`num_cpus` | Worker idle %; sample with `tokio-metrics` | `tokio::runtime::Builder::worker_threads(N)` |
| `max_blocking_threads` | `64`..`2048` | Blocking pool exhaustion via `RuntimeMetrics::num_alive_tasks()` | `tokio::runtime::Builder::max_blocking_threads(N)` |
| `event_interval` | `61` (default) | Poll fairness vs throughput trade | `Builder::event_interval(N)` |
| `global_queue_interval` | `61` (default) | Same — fairness for global queue | `Builder::global_queue_interval(N)` |
| `thread_stack_size` | `2 MiB` default | Stack overflow under deep recursion | `Builder::thread_stack_size(N)` |

### 2.2 Connection pools

| Parameter | Typical range | Signal | Crate |
|-----------|---------------|--------|-------|
| `max_connections` (DB) | `5`..`200` | `pool_wait_time` p99 high → raise; idle high → lower | `sqlx::pool::PoolOptions::max_connections` |
| `min_connections` (DB) | `1`..`10` | Cold-start latency on first request | `PoolOptions::min_connections` |
| `acquire_timeout` | `1s`..`30s` | Caller p99 = timeout exactly → pool starvation | `PoolOptions::acquire_timeout` |
| `idle_timeout` | `60s`..`10min` | Server-side connection-kill events | `PoolOptions::idle_timeout` |
| `max_lifetime` | `30min`..`24h` | Avoid stale connections through load balancers | `PoolOptions::max_lifetime` |
| `bb8 pool size` | same as above | bb8 has `max_size`, `min_idle` | `bb8::Pool::builder().max_size()` |
| `deadpool size` | same | deadpool has `max_size`, `timeouts` | `deadpool::managed::PoolBuilder` |

### 2.3 HTTP client pool (`reqwest`)

| Parameter | Typical range | Signal | API |
|-----------|---------------|--------|-----|
| `pool_max_idle_per_host` | `10`..`200` | Per-host SYN storms under burst | `ClientBuilder::pool_max_idle_per_host(N)` |
| `pool_idle_timeout` | `30s`..`5min` | Bursty traffic re-handshakes TLS | `ClientBuilder::pool_idle_timeout(d)` |
| `connect_timeout` | `1s`..`10s` | Tail latency on slow upstreams | `ClientBuilder::connect_timeout(d)` |
| `timeout` (overall) | `5s`..`60s` | Same | `ClientBuilder::timeout(d)` |
| `tcp_keepalive` | `60s`..`5min` | LB idle disconnects | `ClientBuilder::tcp_keepalive(d)` |

### 2.4 Cache sizes

| Parameter | Typical range | Signal | Crate |
|-----------|---------------|--------|-------|
| `moka::Cache` capacity | size-based: bytes; entry-based: count | Hit rate < 0.8 → increase; memory pressure → decrease | `moka::sync::CacheBuilder::max_capacity` / `weighter` |
| `moka` TTL | `1min`..`24h` | Stale reads vs hit rate trade | `CacheBuilder::time_to_live` |
| `moka` TTI (time-to-idle) | `5min`..`1h` | Working-set eviction tuning | `CacheBuilder::time_to_idle` |
| `cached::TimedCache` size | entry count | Same as moka but simpler | `cached::TimedCache::with_lifespan_and_capacity` |
| LRU shards | power of 2 | Shard contention via `tokio-console` | `moka` is internally sharded; no direct knob |

### 2.5 Channels (`tokio::sync::mpsc`, `flume`)

| Parameter | Typical range | Signal | API |
|-----------|---------------|--------|-----|
| `mpsc::channel(N)` capacity | `16`..`4096` | Producer block rate vs receiver lag | `tokio::sync::mpsc::channel(N)` |
| `broadcast::channel(N)` capacity | `16`..`1024` | Lagged subscriber count | `tokio::sync::broadcast::channel(N)` |
| `flume::bounded(N)` | same range | Same | `flume::bounded(N)` |
| Unbounded channels | (avoid in prod paths) | Memory growth → bound it | See [anti-patterns §4.D](../../builder/references/rust-anti-patterns.md#4d-unbounded-channel-memory-blow-up) |

### 2.6 Tower middleware (Backpressure)

| Parameter | Typical range | Signal | Crate |
|-----------|---------------|--------|-------|
| `ConcurrencyLimit` | `64`..`8192` | Inner service latency rises with concurrency → cap it | `tower::limit::ConcurrencyLimit` |
| `RateLimit` rps | service-specific | 429 rate at downstream | `tower::limit::RateLimit` |
| `LoadShed` threshold | (implicit) | 503 rate vs queue depth | `tower::load_shed::LoadShed` |
| `Buffer` capacity | `16`..`1024` | Queue depth, tail latency | `tower::buffer::Buffer` |

### 2.7 Allocator parameters

Allocator-level tunables are usually env vars or build flags (not Rust API), so Dial sets them via the process environment:

| Allocator | Knob | Env var / API |
|-----------|------|--------------|
| mimalloc | Page reset / large pages | `MIMALLOC_ALLOW_LARGE_OS_PAGES=1`, `MIMALLOC_RESERVE_HUGE_OS_PAGES=N` |
| jemalloc | tcache, narenas | `MALLOC_CONF=narenas:N,tcache:true,dirty_decay_ms:10000` |
| snmalloc | Chunk size | Build-time feature flags (`stats`, `1mib`) |

Allocator detail: [best-practices §6.2](../../builder/references/rust-best-practices.md#62-allocator-choice).

### 2.8 Rayon (CPU parallelism)

| Parameter | Typical range | Signal | API |
|-----------|---------------|--------|-----|
| Global thread pool size | physical cores | Hyperthread contention on numeric work | `rayon::ThreadPoolBuilder::num_threads(N).build_global()` |
| `par_iter` chunk size | auto | Tiny per-element work → set explicitly via `with_min_len`/`with_max_len` | `IndexedParallelIterator` adaptors |

### 2.9 Build profile (one-shot tuning, not runtime)

| Parameter | Production default | Trade |
|-----------|-------------------|-------|
| `opt-level` | `3` | `"s"`/`"z"` for binary size |
| `lto` | `"fat"` | `"thin"` = 90% gain at 50% compile cost |
| `codegen-units` | `1` (release) | Higher = faster build, slower binary |
| `panic` | `"abort"` | Smaller binary, no `catch_unwind`. Trade with FFI |
| `strip` | `"symbols"` | Lose backtraces; pair with `release-with-debug` profile |

Full profile reference: [best-practices §6.6](../../builder/references/rust-best-practices.md#66-release-profile-tuning).

---

## 3. Telemetry plumbing — what feeds the loop

Without telemetry, the tuning loop is open-loop and unsafe. Dial requires these signals exported before tuning starts.

### 3.1 Tracing + OpenTelemetry

```rust
use tracing_subscriber::{prelude::*, EnvFilter};
use tracing_opentelemetry::OpenTelemetryLayer;

tracing_subscriber::registry()
    .with(EnvFilter::from_default_env())
    .with(tracing_subscriber::fmt::layer())
    .with(OpenTelemetryLayer::new(tracer))
    .init();
```

Span attributes carry tuning-relevant context (pool size, cache hit/miss, queue depth).

### 3.2 Metrics — Prometheus exporter

```rust
use metrics_exporter_prometheus::PrometheusBuilder;
PrometheusBuilder::new()
    .with_http_listener(([0,0,0,0], 9000))
    .install()?;

// Anywhere:
metrics::histogram!("pool.acquire.us").record(elapsed_us as f64);
metrics::gauge!("pool.size").set(pool.size() as f64);
```

### 3.3 Tokio-specific metrics

```rust
use tokio_metrics::RuntimeMonitor;

let handle = tokio::runtime::Handle::current();
let monitor = RuntimeMonitor::new(&handle);
for interval in monitor.intervals() {
    tracing::info!(
        worker_busy_ns = interval.busy_duration.as_nanos() as u64,
        polls = interval.total_polls_count,
        ?interval,
    );
}
```

Per-task instrumentation via `TaskMonitor::instrument` gives p99 poll time per logical task — the canonical signal for "this task starves the runtime".

### 3.4 Required signals (Dial pre-flight)

Dial refuses to tune if these aren't exported:

- Wall-clock service p50/p95/p99 latency
- Pool wait time histogram (DB, HTTP client)
- Cache hit rate
- Tokio busy ratio per worker
- Allocator RSS over time (process-level — easy from `/proc/self/status` or `psutil`)
- Error/timeout rate

---

## 4. Feedback-loop architecture (text diagram)

```
                        ┌─────────────────────────────────────┐
                        │  Application (axum + tokio + sqlx)  │
                        │                                     │
                        │   ConfigSnapshot ◀── arc-swap ◀──┐  │
                        │       │                          │  │
                        │       ▼                          │  │
                        │  Pool / Cache / Tower / ...      │  │
                        └─────────┬───────────────────────┬┘  │
              tracing + metrics   │                       │   │
                        ▼         ▼                       │   │
                ┌──────────────────────────┐              │   │
                │ Prometheus / OTel /      │              │   │
                │ tokio-metrics            │              │   │
                └────────────┬─────────────┘              │   │
                             │                            │   │
                             ▼                            │   │
                ┌──────────────────────────┐              │   │
                │ Dial: candidate proposer │              │   │
                │   (Bayesian / grid)      │              │   │
                └────────────┬─────────────┘              │   │
                             │                            │   │
                             ▼                            │   │
                ┌──────────────────────────┐              │   │
                │ Candidate validator      │  reject ◀────┘   │
                │ (canary or A/B verify)   │                  │
                └────────────┬─────────────┘                  │
                             │ accept                         │
                             ▼                                │
                ┌──────────────────────────────────────────┐  │
                │ ConfigBus (tokio::sync::watch)           │──┘
                └──────────────────────────────────────────┘
```

Hot-reload primitives:

| Primitive | Use |
|-----------|-----|
| `arc_swap::ArcSwap<Config>` | Wait-free read; producer swaps atomically. Default choice |
| `tokio::sync::watch::Sender<Config>` | Notify-on-change for async consumers |
| `std::sync::atomic::Atomic{Usize,Bool}` | Single-scalar knobs (pool size, feature flag) |
| `OnceLock<Config>` | One-shot init only; cannot retune |

**No-restart parameter swap** pattern:

```rust
use arc_swap::ArcSwap;
use std::sync::Arc;

static CONFIG: LazyLock<ArcSwap<Config>> =
    LazyLock::new(|| ArcSwap::from_pointee(Config::default()));

// Reader (zero overhead per call)
let cfg = CONFIG.load();
let timeout = cfg.connect_timeout;

// Writer (Dial pushes new tuning)
CONFIG.store(Arc::new(new_cfg));
```

For pool *capacity*, most pool crates can resize at runtime (`sqlx::Pool::set_max_connections(N)`); for those that can't, the pattern is to spawn a new pool, hand it to readers via `arc-swap`, then drain the old one.

---

## 5. Auto-tuning experiment harness

| Approach | Crate | When |
|----------|-------|------|
| Manual grid sweep | `criterion` + driver script | First baseline; quick parameter screening |
| Bayesian optimization | `argmin` + `gp` features, `bayesopt-rs` | Continuous parameters with expensive evaluation (real workload) |
| Multi-armed bandit | hand-rolled with `metrics`-driven reward | Online tuning, low risk per decision |
| Statistical significance | `criterion` defaults (Mann-Whitney) | "Did this change actually move the needle?" |

**Sample size discipline**: changing pool size from 10→20 and seeing a 3% latency drop is *noise* below ~10k requests. Dial waits for statistical significance before promoting a candidate to production.

Bench tooling depth: [best-practices §5.8](../../builder/references/rust-best-practices.md#58-benchmarks--criterion-vs-divan).

---

## 6. Cost surfaces unique to Rust

When Dial reports a tuning recommendation, these Rust-specific costs need to be flagged:

| Knob | Hidden cost |
|------|------------|
| Adding a generic where `dyn Trait` would do | Monomorphization → bigger binary, slower compile, possibly worse I-cache |
| `lto = "fat"` | 2-3x compile time; throttles CI cost |
| `codegen-units = 1` | Same — kills build parallelism |
| Bumping mimalloc/jemalloc/snmalloc | RSS shape changes (some allocators retain more for speed) |
| Pool size up | Each connection has TLS / TCP / kernel cost — not free |
| Cache size up | Memory + sometimes hash collision degradation on tiny variants |
| `worker_threads` up | Context-switch cost; cache contention; useless past physical cores for compute-bound |
| Tower `Buffer(N)` up | Latency floor goes up under saturation |

---

## 7. Anti-patterns Dial must avoid

| Anti-pattern | Why it bites |
|--------------|-------------|
| **Tuning `Mutex` vs `RwLock` without measurement** | Outcome depends on read/write ratio. RwLock-write under heavy reads is slower than Mutex (writers wait for *all* readers) |
| **`Vec::with_capacity(N)` cargo-cult sizes** | A "1024" picked from a Stack Overflow answer is no better than the default in 90% of cases. Measure |
| **Premature mimalloc / jemalloc switch** | Many workloads see ≤ 1% gain; always benchmark baseline allocator first |
| **Tuning compile-time flags into prod without re-running PGO** | LTO + PGO are interactive — change one and the other must re-bake |
| **Pool size = "the number Prometheus suggests"** | Pool size and DB connection limit are joint — raising one without checking the other = DB exhaustion |
| **Continuous tuning of a workload that just got a new feature** | The cost model just shifted. Re-baseline before tuning |
| **`opt-level = "z"` everywhere "for size"** | `"z"` can be **slower than `"s"`** *and* not much smaller. Measure both |
| **Channel capacity tuning without backpressure design** | Bigger buffer hides the backpressure problem, doesn't solve it. See [anti-patterns §4.D](../../builder/references/rust-anti-patterns.md#4d-unbounded-channel-memory-blow-up) |
| **Tuning without `tokio-console`** | "I think the runtime is starved" without `tokio-console` evidence is folklore, not data |

---

## 8. Dial-specific routing rules

1. **Refuse to tune without telemetry.** If the user can't show histograms for pool wait, p99 latency, and tokio busy ratio, the first action is to instrument.
2. **Build-time vs runtime knobs separated.** `lto`/`codegen-units`/`opt-level` get tuned once per release. Pool / cache / channel sizes get tuned online.
3. **One knob at a time.** Multi-variable changes can't be statistically attributed. Bayesian opt is the exception (it explicitly models joint effects).
4. **Allocator is a build-time decision, but a runtime *measurement*.** Bench mimalloc vs jemalloc with the real workload, not microbenches.
5. **Hot-reload first, restart last.** `arc-swap` + `tokio::sync::watch` cover almost every parameter. Restart only when the type itself changes.
6. **Verify after each change.** Statistical significance (`criterion` defaults or t-test) before promotion. Otherwise the loop drifts on noise.

---

## Sources

- The Rust Performance Book — https://nnethercote.github.io/perf-book/
- tokio-console — https://github.com/tokio-rs/console
- tokio-metrics — https://github.com/tokio-rs/tokio-metrics
- metrics-exporter-prometheus — https://github.com/metrics-rs/metrics
- arc-swap — https://github.com/vorner/arc-swap
- moka — https://github.com/moka-rs/moka
- sqlx pool configuration — https://docs.rs/sqlx/latest/sqlx/pool/struct.PoolOptions.html
- bb8 / deadpool — https://github.com/djc/bb8, https://github.com/bikeshedder/deadpool
- tower middleware — https://github.com/tower-rs/tower
- argmin (optimization) — https://argmin-rs.github.io/argmin/
- mimalloc / jemalloc / snmalloc env-config docs — see allocator README files
- Source of truth: [`builder/references/rust-best-practices.md §6+§8`](../../builder/references/rust-best-practices.md), [`rust-anti-patterns.md §6`](../../builder/references/rust-anti-patterns.md)
