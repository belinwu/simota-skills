# Rust Concurrency Audit Cheatsheet — Specter

Focused checklist for concurrency, async, and race-condition review of Rust codebases. Baseline: **Rust 1.85+ / Edition 2024 / tokio 1.40+** (2026-05).

> Source-of-truth references (full catalog lives in Builder):
> - Constructive async stack: [`builder/references/rust-best-practices.md` §7 Security](../../builder/references/rust-best-practices.md#7-security-practices) (overlapping `await_holding_lock` lint) and [§8 Async ecosystem — structured concurrency](../../builder/references/rust-best-practices.md#8-async-ecosystem--structured-concurrency)
> - Async pitfalls (4.1–4.25 + 4.A–4.E): [`builder/references/rust-anti-patterns.md` §4 Async / Await Pitfalls](../../builder/references/rust-anti-patterns.md#4-async--await-pitfalls-extensive)
> - Memory model, atomics, `Send`/`Sync` semantics: [`builder/references/rust-language-spec.md` §7 Memory Model & Concurrency Primitives](../../builder/references/rust-language-spec.md#7-memory-model--concurrency-primitives)
> - Cancellation safety definition: [`builder/references/rust-language-spec.md` §4.7 Cancellation safety](../../builder/references/rust-language-spec.md#47-cancellation-safety)

**Do not duplicate the catalogs above.** This cheatsheet is the *audit order* Specter applies; it links rather than restates.

Rust prevents **data races** at the type-system level (Send/Sync + borrow checker). It does **not** prevent **race conditions** (TOCTOU, lost-update, deadlock, livelock, priority inversion, lost-wakeup). Specter's primary value on Rust code is the latter.

---

## When auditing a Rust concurrency surface, walk this checklist:

### 1. Map the threading model

| Question | How |
|----------|-----|
| Runtime? | `rg '#\[tokio::main\]\|#\[async_std::main\]\|smol::block_on' --type rust` |
| Multi-thread vs current-thread runtime? | Look at `#[tokio::main(flavor = "multi_thread"|"current_thread")]` and `Runtime::Builder` |
| Spawn surface? | `rg 'tokio::spawn\|std::thread::spawn\|rayon::spawn\|spawn_blocking' --type rust` |
| Shared mutable state? | `rg 'Mutex<\|RwLock<\|AtomicU\|Atomic[BIU]\|DashMap\|Arc<' --type rust` |
| Channels? | `rg 'mpsc::\|broadcast::\|watch::\|crossbeam_channel\|flume' --type rust` |

### 2. `Send` / `Sync` semantics — what the type system already does

Specter usually does not need to flag `Send`/`Sync` violations directly (the compiler will). Audit for **manual `unsafe impl Send`/`Sync`** which bypasses the check:

```rust
// FLAG: any `unsafe impl Send/Sync` requires a written SAFETY proof.
unsafe impl Send for MyWrapper {}   // ← why is this sound? where's the comment?
```

Key auto-trait rules:

| Type | `Send` | `Sync` | Notes |
|------|--------|--------|-------|
| `Rc<T>` | ❌ | ❌ | non-atomic refcount |
| `Arc<T>` | ✓ if `T: Send + Sync` | ✓ if `T: Send + Sync` | atomic refcount |
| `Cell<T>` | ✓ if `T: Send` | ❌ | single-thread interior mutation |
| `RefCell<T>` | ✓ if `T: Send` | ❌ | runtime borrow check, single-thread |
| `Mutex<T>` | ✓ if `T: Send` | ✓ if `T: Send` | |
| `RwLock<T>` | ✓ if `T: Send` | ✓ if `T: Send + Sync` | reader needs `T: Sync` |
| `MutexGuard<'_, T>` | platform-dependent (often **!Send**) | ✓ if `T: Sync` | **see §3** |
| `*const T` / `*mut T` | ❌ | ❌ | raw pointers opt out |

Full table: [language-spec §7.1](../../builder/references/rust-language-spec.md#7-memory-model--concurrency-primitives).

Common bug: sharing `RefCell<T>` across threads via `Arc<RefCell<T>>`. Compiler rejects (`RefCell: !Sync`). If you see `unsafe impl Sync for Wrapper(RefCell<T>) {}`, reject — there is no sound way.

### 3. `MutexGuard` across `.await` — the most common async bug

`std::sync::MutexGuard` is `!Send` on most platforms (pthread mutexes are owner-thread-bound). Holding one across `.await`:

- Makes the future `!Send` → `tokio::spawn` rejects it at compile time.
- Even when `Send` (e.g. `parking_lot::Mutex` on some configs), it can deadlock if the awaited task needs the same lock.

**Lint**: `clippy::await_holding_lock` and `clippy::await_holding_refcell_ref`. Enforce as `-D` in CI.

```rust
// BAD — guard alive across .await
async fn bad(m: &std::sync::Mutex<i32>) {
    let mut g = m.lock().unwrap();
    *g += 1;
    tokio::time::sleep(Duration::from_millis(10)).await;   // !Send
    *g += 1;
}

// FIX 1 — scope the lock; drop guard before .await
async fn good(m: &std::sync::Mutex<i32>) {
    {
        let mut g = m.lock().unwrap();
        *g += 1;
    } // ← guard dropped here
    tokio::time::sleep(Duration::from_millis(10)).await;
    {
        let mut g = m.lock().unwrap();
        *g += 1;
    }
}
```

**Common wrong fix**: swap `std::sync::Mutex` for `tokio::sync::Mutex` "to make it `Send` across await". This is rarely correct — `tokio::sync::Mutex` is heavier, has cancel-safety footguns (cancelling `lock()` loses queue position), and most call sites can simply restructure to drop before await. See [anti-patterns §4.3, §4.4, §4.A](../../builder/references/rust-anti-patterns.md#4-async--await-pitfalls-extensive).

**When `tokio::sync::Mutex` is actually correct**: you provably must hold the lock across an await (e.g. holding write access while issuing an async I/O write to disk under that lock).

### 4. Cancellation safety — `select!` is dangerous

A future is **cancellation-safe** if dropping it mid-poll leaves the world in a consistent state. `tokio::select!` drops the losing branches mid-future. Every `select!` branch must be cancel-safe.

| Cancel-safe (✓) | NOT cancel-safe (✗) |
|------------------|---------------------|
| `tokio::sync::mpsc::Receiver::recv` | `tokio::io::AsyncReadExt::read_exact` (drops partial bytes) |
| `tokio::sync::broadcast::Receiver::recv` | `tokio::io::AsyncBufReadExt::read_line` (drops partial line) |
| `tokio::sync::watch::Receiver::changed` | `tokio::io::AsyncWriteExt::write_all` (commits partial writes) |
| `tokio::time::sleep`, `sleep_until` | Any `async {}` block that has `.await` after committing state |
| `tokio::time::interval::tick` | `tokio::sync::Mutex::lock` (loses queue position) |
| `tokio::io::AsyncReadExt::read` (single-shot) | `tokio::sync::Semaphore::acquire` (loses permit reservation) |
| `JoinSet::join_next` | `Stream::next` of a non-cancel-safe stream |

**Pattern: wrap a cancel-unsafe future in its own task; select on the channel** ([anti-patterns §4.7, §4.B](../../builder/references/rust-anti-patterns.md#4-async--await-pitfalls-extensive)):

```rust
// BAD — read_exact loses partial bytes when timeout wins
loop {
    tokio::select! {
        r = socket.read_exact(&mut buf) => { /* handle */ }
        _ = tokio::time::sleep(Duration::from_secs(1)) => { /* tick */ }
    }
}

// GOOD — spawn a task that owns the cancel-unsafe future;
// select on a cancel-safe mpsc::Receiver instead.
let (tx, mut rx) = tokio::sync::mpsc::channel(8);
tokio::spawn(async move {
    let mut buf = [0u8; 1024];
    while let Ok(n) = socket.read_exact(&mut buf).await {
        if tx.send(buf[..n].to_vec()).await.is_err() { break; }
    }
});
loop {
    tokio::select! {
        biased;
        Some(msg) = rx.recv() => { /* handle */ }
        _ = tokio::time::sleep(Duration::from_secs(1)) => { /* tick */ }
    }
}
```

**`tokio::time::timeout(d, fut)`**: if `fut` is not cancel-safe, the timeout drops it mid-poll. Treat `timeout` as the same cancel-safety contract as `select!`.

**`biased;` in `select!`**: required when one branch (shutdown, error) must always be polled first. Default polling is round-robin random — a hot stream branch can starve shutdown. See §4.8.

### 5. `tokio::spawn` task ownership — orphans hide panics

`tokio::spawn(fut)` returns a `JoinHandle` that, if dropped, **detaches** the task. The task keeps running; if it panics, the panic is **silently swallowed**.

| Symptom | Cause |
|---------|-------|
| "Sometimes my background task stops working but the process keeps running" | Orphaned `JoinHandle`, task panicked, nothing surfaced it |
| "Tests pass but CI sometimes hangs" | Orphan worker holds resources tests can't release |
| "Graceful shutdown doesn't drain" | No supervisor — spawned tasks not joined |

```rust
// BAD — orphan
tokio::spawn(async { panic!("oh no") });
// No log, no exit-code change. Problem festers.

// GOOD — JoinSet propagates panics
let mut set = tokio::task::JoinSet::new();
set.spawn(async { panic!("oh no") });
while let Some(res) = set.join_next().await {
    if let Err(e) = res {
        if e.is_panic() { std::panic::resume_unwind(e.into_panic()); }
    }
}
```

**Required patterns** (full text in [best-practices §8.2, §8.3](../../builder/references/rust-best-practices.md#8-async-ecosystem--structured-concurrency)):

| Tool | Use |
|------|-----|
| `tokio::task::JoinSet` | Dynamic task group with await-all and abort-all |
| `tokio_util::task::AbortOnDropHandle` | Wraps `JoinHandle`; aborts task when dropped |
| `tokio_util::task::TaskTracker` | Track spawned tasks for graceful shutdown without owning them all |
| `tokio_util::sync::CancellationToken` | Tree-shaped cooperative cancellation; clones cancel together |
| `tokio_graceful` / `tokio-graceful-shutdown` | High-level coordinator with signal handling + deadline |

**Graceful shutdown protocol** (full skeleton in best-practices §8.3):

1. Create `CancellationToken` + `TaskTracker`.
2. Spawn all tasks via the tracker; each clones the token.
3. `tracker.close()` (no more new tasks).
4. Wait for SIGINT/SIGTERM.
5. `cancel.cancel()` — signals all tasks.
6. `tokio::time::timeout(deadline, tracker.wait()).await` — bounded wait; force-exit on timeout.

### 6. Pin / Unpin projection

Audit any hand-rolled `Pin` projection. Real-world Pin bugs are the third-biggest async UB source (after MutexGuard-across-await and orphan spawn).

| Rule | Audit |
|------|-------|
| Self-referential structs require Pin | If you see `Pin<&mut Self>`, look for owned references |
| Field projection: structural vs non-structural | `pin-project-lite` macro handles this correctly. Hand-rolled `Pin::get_unchecked_mut` requires manual proof. |
| Never expose `&mut field` for a structurally-pinned field | Moving the field invalidates the pin guarantee |

Reject hand-rolled projection unless there is a `// SAFETY:` comment listing every pinned field. See [anti-patterns §4.11, §9.7](../../builder/references/rust-anti-patterns.md#4-async--await-pitfalls-extensive). Use [`pin-project-lite`](https://docs.rs/pin-project-lite/) — derive-style, no proc-macro dep.

### 7. Atomic memory orderings

Specter's audit angle: ordering choice is correct *for the pattern*. Rust adopts C++20 memory model exactly (full table: [language-spec §7.3](../../builder/references/rust-language-spec.md#7-memory-model--concurrency-primitives)).

| Ordering | When |
|----------|------|
| `Relaxed` | Counters not protecting other data (e.g. metrics, statistics, debug counters) |
| `Acquire` (load) + `Release` (store) | Lock-free flag protecting a payload; reader Acquires the flag, gains visibility into prior Releases |
| `AcqRel` | RMW (`fetch_add`, `compare_exchange`) that both consumes and publishes |
| `SeqCst` | When you need a single global order across **multiple** atomics — rare, expensive |

**Common bugs**:

- Mixing orderings across atomics in the same protocol — sequentially-consistent reasoning requires `SeqCst` on **all** participants.
- Using `SeqCst` everywhere "to be safe" — masks intent, costs performance, can hide a missing pairing.
- Using `Relaxed` for the flag in a load-acquire-then-read-payload pattern — the reader may read stale payload.

```rust
// Producer
PAYLOAD.store(value, Ordering::Relaxed);   // ← does NOT publish
READY.store(true, Ordering::Release);      // ← publishes prior Relaxed store

// Consumer
if READY.load(Ordering::Acquire) {         // ← pairs with Release
    let v = PAYLOAD.load(Ordering::Relaxed);   // safe: visible due to Acquire
}
```

If the load above were `Relaxed`, the consumer could observe `READY=true` with a stale `PAYLOAD` value.

### 8. Channel selection and backpressure

| Channel | Use | Anti-pattern |
|---------|-----|--------------|
| `tokio::sync::mpsc::channel(N)` (bounded) | **Default for task→task communication**. Backpressure built in. | — |
| `tokio::sync::mpsc::unbounded_channel` | Rarely correct. Producer outruns consumer → OOM. | Default to bounded; pick N explicitly. See [anti-patterns §4.10, §4.D](../../builder/references/rust-anti-patterns.md#4-async--await-pitfalls-extensive). |
| `tokio::sync::broadcast` | Fan-out 1→N. Receivers buffer per-subscriber. | Slow receiver → `RecvError::Lagged(n)`. Audit for `recv()` error handling — many call sites just unwrap and silently drop the lag. |
| `tokio::sync::watch` | Single-value notify (latest-wins). Config reload, shutdown flag. | Don't use for general events — receivers only see the latest. |
| `crossbeam_channel` (sync) | Std-thread MPMC; supports `select!`. | Don't bridge into async without `spawn_blocking`. |
| `flume` | Async-aware drop-in for `crossbeam`. | — |
| `std::sync::mpsc` | Std-thread MPSC, rewritten on `crossbeam` internals 1.67+. | OK; prefer `crossbeam_channel` if you need MPMC or `select!`. |

**Bounded channel from a `Drop` impl**:

```rust
// BAD — Drop is sync, send is async, try_send may fail under load
impl Drop for Worker {
    fn drop(&mut self) {
        let _ = self.shutdown_tx.try_send(());   // ← can silently drop
    }
}

// FIX — restructure shutdown to use an atomic flag or watch channel
//        that doesn't need .send() from Drop
```

See [anti-patterns §4.18](../../builder/references/rust-anti-patterns.md#4-async--await-pitfalls-extensive).

### 9. Lock primitive selection

| Primitive | When |
|-----------|------|
| `std::sync::Mutex<T>` | **Default**. Custom futex-backed on Linux (1.62+), competitive with parking_lot. Supports poisoning. |
| `parking_lot::Mutex<T>` | When you need non-poisoning, fairness configuration, or `Condvar::wait_for` sub-ms resolution on older platforms. |
| `tokio::sync::Mutex<T>` | **Only** when the lock must be held across `.await` AND no restructure is possible. Heavier, cancel-safety footgun. |
| `std::sync::RwLock<T>` | Read-heavy workloads where reads outweigh writes ≥5×. Otherwise `Mutex` is faster (no read/write coordination). |
| `tokio::sync::RwLock<T>` | Async equivalent of std RwLock + the across-await caveat. |
| `dashmap::DashMap<K, V>` | Sharded concurrent hashmap. Better than `Arc<RwLock<HashMap>>` for hot caches. |
| `crossbeam::atomic::AtomicCell<T>` | Lock-free single-cell `Copy` type. |

**RwLock write-starvation**: with reader-preference RwLocks (default in `parking_lot` historically, and std on some platforms), a continuous stream of readers can starve writers indefinitely. Use writer-preference or strict-fairness variants when writes carry liveness requirements.

**RwLock inversion** (write-heavy workload hurts with RwLock): if writes outnumber reads, `Mutex` is typically faster because RwLock coordinates reader counts on every access.

**Async `RwLock` for hot caches** is rarely the right choice — see [anti-patterns §4.19](../../builder/references/rust-anti-patterns.md#4-async--await-pitfalls-extensive). Prefer `DashMap` or sharded `Arc<[Mutex<HashMap>]>`.

### 10. Data race vs race condition

Rust prevents data races (concurrent unsynchronized access where at least one is a write) by type system. It does **not** prevent **logical race conditions**:

| Race condition class | Example |
|---------------------|---------|
| **TOCTOU** | `if cache.contains_key(&k) { cache[&k] } else { ... }` — concurrent writer can remove between check and use |
| **Lost update** | Two tasks each `load → modify → store`; one overwrites the other. Use `fetch_update` / CAS loop |
| **Deadlock** | Two tasks each acquire lock A then B in opposite order |
| **Livelock** | Cooperative retry loop where two participants keep yielding to each other |
| **Lost wakeup** | `Condvar::wait` without checking the predicate before sleeping; signal arrives between predicate read and wait |
| **Time-of-snapshot bug** | `Arc<RwLock<Snapshot>>` reader sees consistent snapshot, but two reads at different times see different snapshots |

**Lost-update audit grep**:

```sh
rg 'load\(.*Ordering' --type rust -A 3 | rg 'store\('
```

Look for `load → arithmetic → store` triples that should be `fetch_add` / `fetch_update` / `compare_exchange`.

### 11. Blocking inside async — the silent killer

| Pattern | Why it's bad |
|---------|--------------|
| `std::fs::read` in `async fn` | Stalls the worker thread for ms-to-s |
| `std::thread::sleep` | Same |
| `reqwest::blocking::*` | Same |
| `for x in big_vec { hash(x) }` directly in `async fn` | CPU-bound loop monopolizes worker; no yield points |
| `block_on(fut)` inside an `async fn` running on tokio | Deadlocks current-thread runtime; throughput loss on multi-thread |
| `block_in_place` on `current_thread` runtime | Panics — only works on multi-thread |

```rust
// FIX patterns
let data = tokio::fs::read(path).await?;                       // async I/O
tokio::time::sleep(d).await;                                   // async sleep
let h = tokio::task::spawn_blocking(move || cpu_work(input)).await?;   // offload
tokio::task::yield_now().await;                                // cooperative
```

See [anti-patterns §4.1, §4.2, §4.E](../../builder/references/rust-anti-patterns.md#4-async--await-pitfalls-extensive).

### 12. Concurrency-related Clippy lints — CI minimum

```yaml
- run: |
    cargo clippy --all-targets -- \
      -D warnings \
      -D clippy::await_holding_lock \
      -D clippy::await_holding_refcell_ref \
      -D clippy::await_holding_invalid_type \
      -D clippy::mutex_atomic \
      -D clippy::mutex_integer \
      -D clippy::rc_mutate \
      -D clippy::large_futures
```

Plus `loom` testing for any non-trivial atomic protocol:

```rust
#[cfg(loom)]
mod tests {
    use loom::sync::Arc;
    use loom::sync::atomic::*;

    #[test]
    fn flag_payload_protocol() {
        loom::model(|| {
            // Loom exhaustively explores interleavings for this snippet
        });
    }
}
```

`loom` exhaustively explores thread interleavings on `--cfg loom` builds. Mandatory for hand-rolled lock-free data structures.

### 13. `async fn` in traits — Send-bound surprise (1.75+)

```rust
// Native async fn in trait (stable 1.75) — returns Future, but NOT necessarily Send
pub trait Repo {
    async fn find(&self, id: Uuid) -> Result<User, Err>;
}

// FLAG: spawning a Repo method may fail to compile if the impl's future isn't Send
tokio::spawn(async move { repo.find(id).await });   // ← may reject
```

Fixes:

```rust
// Option A — RPITIT with explicit Send bound
pub trait Repo {
    fn find(&self, id: Uuid) -> impl Future<Output = Result<User, Err>> + Send;
}

// Option B — async-trait (heap-allocates Box<dyn Future>, but always Send)
#[async_trait::async_trait]
pub trait Repo: Send + Sync {
    async fn find(&self, id: Uuid) -> Result<User, Err>;
}

// Option C — trait_variant::make for both flavors from one definition
```

See [best-practices §8.7](../../builder/references/rust-best-practices.md#8-async-ecosystem--structured-concurrency) and [anti-patterns §4.13](../../builder/references/rust-anti-patterns.md#4-async--await-pitfalls-extensive).

---

## Triage priorities

When multiple findings stack, rank by:

1. **MutexGuard across `.await`** (`clippy::await_holding_lock`) — directly reachable deadlock or `!Send` compile errors masked by single-thread runtime.
2. **Orphaned `tokio::spawn`** — silent panic loss, the most underdiagnosed production bug class in async Rust.
3. **`select!` branch with non-cancel-safe future** — data loss on every cancellation, no exception.
4. **`Pin` projection bug** — UB, but mostly behind `unsafe`; defer to Sentinel for the unsafe-block aspect, Specter for the soundness reasoning.
5. **Unbounded channel** — sustained backpressure → OOM.
6. **Atomic ordering mismatch** — invisible in test, manifests under load; require `loom` for any non-trivial protocol.
7. **Lock primitive misfit** (RwLock for write-heavy, tokio::Mutex when std would do) — performance, but also cancel-safety footgun.
8. **Race-condition logic** (lost update, TOCTOU on shared state) — correctness, not data race.
9. **Blocking inside async** — silent throughput killer.
10. **`async fn` in trait Send-bound** — compile fault more than runtime risk, but blocks production architecture.

---

## Sources

- Tokio docs: https://docs.rs/tokio/
- Alice Ryhl, "Async: What is blocking?": https://ryhl.io/blog/async-what-is-blocking/
- Tokio tutorial — shared state: https://tokio.rs/tokio/tutorial/shared-state
- Tokio testing topics: https://tokio.rs/tokio/topics/testing
- Oxide RFD 400 — Cancellation safety: https://rfd.shared.oxide.computer/rfd/0400
- `tokio::select!` documentation: https://docs.rs/tokio/latest/tokio/macro.select.html
- `loom` (concurrency permutation tester): https://docs.rs/loom/
- `pin-project-lite`: https://docs.rs/pin-project-lite/
- `tokio-util` (CancellationToken, TaskTracker, AbortOnDropHandle): https://docs.rs/tokio-util/
- Baby Steps, "async fn in trait Send bounds": https://smallcultfollowing.com/babysteps/blog/2023/02/01/async-trait-send-bounds-part-1-intro/
- Rust Reference — memory model: https://doc.rust-lang.org/reference/memory-model.html
- A Preliminary Study of Fixed Flaky Tests in Rust Projects (arxiv 2502.02760)
