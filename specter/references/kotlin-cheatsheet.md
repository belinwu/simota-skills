# Kotlin Concurrency Audit Cheatsheet — Specter

Focused checklist for concurrency, coroutine, and race-condition review of Kotlin codebases. Baseline: **Kotlin 2.3+ / K2 / kotlinx.coroutines 1.10+** with **2.4 EAP outlook** (2026-05).

> Source-of-truth references (full catalog lives in Builder):
> - Constructive coroutines stack (3.1–3.10): [`builder/references/kotlin-best-practices.md` §3 Coroutines Best Practices](../../builder/references/kotlin-best-practices.md#3-coroutines-best-practices-2026-era)
> - Coroutines pitfalls (launch/async, GlobalScope, runBlocking, propagation): [`builder/references/kotlin-anti-patterns.md` §2 Coroutines Pitfalls](../../builder/references/kotlin-anti-patterns.md#2-coroutines-pitfalls)
> - Memory & threading (leak detection, atomicfu): [`builder/references/kotlin-best-practices.md` §9 Memory & Threading](../../builder/references/kotlin-best-practices.md#9-memory--threading)
> - Coroutines language spec (suspend, dispatchers, cancellation, exception propagation rules): [`builder/references/kotlin-language-spec.md` §4 Coroutines](../../builder/references/kotlin-language-spec.md#4-coroutines--suspend-dispatchers-structured-concurrency)
> - Smart cast under K2 (concurrent-safe patterns): [`builder/references/kotlin-anti-patterns.md` §10 Smart Cast Pitfalls](../../builder/references/kotlin-anti-patterns.md#10-smart-cast-pitfalls)
> - Detekt rule index — coroutines section: [`builder/references/kotlin-anti-patterns.md` Appendix A `coroutines`](../../builder/references/kotlin-anti-patterns.md#appendix-a--detekt--ktlint-rule-quick-lookup-index)

**Do not duplicate the catalogs above.** This cheatsheet is the *audit order* Specter applies on Kotlin Coroutines code; it links rather than restates.

Companion cheatsheets (same agent):
- SAST / code-level security: [`sentinel/references/kotlin-cheatsheet.md`](../../sentinel/references/kotlin-cheatsheet.md)
- Crypto design: [`crypt/references/kotlin-cheatsheet.md`](../../crypt/references/kotlin-cheatsheet.md)

Kotlin Coroutines do not have a compile-time data-race-safety system — they rely on **structured concurrency** + **immutable data + Flow/StateFlow updates**. Specter's audit angle covers both data races (concurrent mutation of plain `var`) and logical race conditions (lost update on `StateFlow`, cancellation cooperation, dispatcher saturation).

---

## When auditing a Kotlin concurrency surface, walk this checklist:

### 1. Map the concurrency model

| Question | How |
|----------|-----|
| Coroutine builders? | `rg -n 'launch\s*[\({]\|async\s*[\({]\|runBlocking\|coroutineScope\|supervisorScope\|withContext' --type kotlin` |
| Scope ownership? | `rg -n 'CoroutineScope(\|MainScope\|GlobalScope\|viewModelScope\|lifecycleScope\|applicationScope' --type kotlin` |
| Dispatcher selection? | `rg -n 'Dispatchers\.\(Main\|IO\|Default\|Unconfined\)\|newSingleThreadContext\|newFixedThreadPoolContext' --type kotlin` |
| Flow surface? | `rg -n 'Flow<\|MutableStateFlow<\|MutableSharedFlow<\|Channel<\|callbackFlow\|channelFlow' --type kotlin` |
| Mutex / atomics? | `rg -n 'Mutex(\|Semaphore(\|atomic<\|AtomicReference\|AtomicInteger\|atomicfu' --type kotlin` |

### 2. `runBlocking` in production code path

`runBlocking` parks the calling thread until the coroutine completes. In an async stack, that thread can be:

- A Tomcat/Netty worker — request DoS
- An Android UI thread — ANR
- A coroutine dispatcher thread — **nested runBlocking deadlock**

| Location | Verdict |
|----------|---------|
| `main()` entry of a CLI / `fun main() = runBlocking { ... }` | Acceptable |
| Top-level test boundary (consider `runTest` instead) | Acceptable; `runTest` preferred for time-skipping |
| Inside a request handler (`@RestController`, Ktor route) | **Reject** |
| Inside a `suspend fun` (nested) | **Deadlock risk** if the inner coroutine ends up needing the outer dispatcher |
| Inside `Dispatchers.IO` worker | Saturates the IO pool; can deadlock if all IO threads block on each other |
| Bridge sync Java framework into coroutines | Acceptable only with explicit bounded executor |

Reference: [best-practices §3.2 Never `runBlocking` in production code](../../builder/references/kotlin-best-practices.md#32-never-runblocking-in-production-code).

### 3. `GlobalScope.launch` and scope ownership

`GlobalScope` has lifetime == process. Any work launched there outlives every meaningful unit boundary.

| Pattern | Verdict |
|---------|---------|
| `GlobalScope.launch { ... }` in app code | **Reject** | [anti-patterns §2](../../builder/references/kotlin-anti-patterns.md#2-coroutines-pitfalls) |
| `GlobalScope.launch { ... }` in tests (cleanup not guaranteed) | Reject — use `TestScope` |
| `CoroutineScope(SupervisorJob() + Dispatchers.IO)` stored as field | Audit: who calls `.cancel()`? In Spring, hook to `@PreDestroy`. |
| `MainScope()` created and never cancelled | Reject — must be cancelled in lifecycle teardown |
| `viewModelScope` / `lifecycleScope` (Android) / Ktor `application` scope | Framework-managed — acceptable |

**Scope ownership rules** ([best-practices §3.3](../../builder/references/kotlin-best-practices.md#33-scope-ownership-rules)):
- Every `CoroutineScope` must have a documented owner that calls `.cancel()`.
- Class-level scope: cancel in `close()` / `onDestroy` / DI lifecycle.
- Function-level scope: prefer `coroutineScope { }` (suspends until all children done; auto-cancels on caller cancel).

Detekt: `coroutines:GlobalCoroutineUsage`.

### 4. `Dispatchers.IO` and bounded pools

`Dispatchers.IO` has 64 threads by default (or `kotlinx.coroutines.io.parallelism` system prop). Using it without bounds:

- A bursty caller exhausts the 64 threads.
- Blocked IO threads aren't reclaimed (the dispatcher is for **blocking IO**; thread parks until JVM unblocks it).
- IO work doing a `withContext(Dispatchers.IO)` then itself launching IO can saturate.

**`.limitedParallelism(n)`** carves a bounded slice from `Dispatchers.IO`:

```kotlin
private val dbDispatcher = Dispatchers.IO.limitedParallelism(8)    // max 8 concurrent DB ops
private val fileDispatcher = Dispatchers.IO.limitedParallelism(4)
```

| Audit | Why |
|-------|-----|
| Every long-running IO-bound subsystem gets its own `.limitedParallelism(n)` slice | Prevents one subsystem from starving others |
| `n` is sized to the downstream concurrency budget (DB pool size, file handle limit) | Don't request more IO threads than the resource supports |
| `Dispatchers.Default` (CPU-bound) sized to `min(2, cores)` minimum | Default is `max(2, cores)` — good; only audit if overridden |
| `newSingleThreadContext("name")` / `newFixedThreadPoolContext` | Audit for leak — these own a thread; must `.close()` when scope ends |

Reference: [best-practices §3.4](../../builder/references/kotlin-best-practices.md#34-dispatchersiolimitedparallelismn-for-bounded-pools).

### 5. `async { }` exception swallowing

`async` returns a `Deferred<T>`. **Exceptions thrown in the body are stored in the Deferred and surface only when `.await()` is called.** If you never await, you never see the exception.

| Pattern | Verdict |
|---------|---------|
| `val d = async { mayFail() }`; later `d.await()` | Acceptable |
| `async { mayFail() }` and never awaiting | **Reject — silent swallow** |
| Multiple `async` for parallel work; `awaitAll(d1, d2)` | Acceptable |
| `async` inside `coroutineScope { }` (default Job) | Failure in one cancels siblings (fail-fast) |
| `async` inside `supervisorScope { }` | Failure in one does NOT cancel siblings — use when callers handle each independently |
| `async(start = CoroutineStart.LAZY) { ... }` then never `.start()` or `.await()` | Never runs; usually a bug |

Reference: [anti-patterns §2.A](../../builder/references/kotlin-anti-patterns.md#2a-visual-launch-vs-async-exception-propagation) for the visual launch-vs-async propagation matrix.

### 6. `coroutineScope` vs `supervisorScope`

| Need | Use |
|------|-----|
| All children must succeed; any failure cancels siblings | `coroutineScope { ... }` |
| Children are independent; one failure shouldn't kill others | `supervisorScope { ... }` |
| Top-level structured concurrency block in suspend fn | `coroutineScope { ... }` (default) |
| Long-lived dispatcher loop with per-event tasks | `supervisorScope { ... }` so a single event failure doesn't kill the loop |

**Bug class**: putting a `try { ... } catch { ... }` inside `coroutineScope { ... }` around the child `launch` does NOT catch the failure — failures propagate via the parent scope's Job, not back through the inline call site. Use `supervisorScope` or `CoroutineExceptionHandler`.

```kotlin
// FLAG: catch never triggers; failure cancels coroutineScope and surfaces from the outer scope
coroutineScope {
    try {
        launch { throw RuntimeException("boom") }
    } catch (e: Throwable) { /* never reached */ }
}

// FIX: supervisorScope + per-child handler
supervisorScope {
    launch(CoroutineExceptionHandler { _, e -> log(e) }) {
        throw RuntimeException("boom")
    }
}
```

### 7. `StateFlow` lost-update — `update { }` over `value = value.copy()`

`MutableStateFlow.value = ...` is atomic for the **assignment**, but **not** for read-modify-write. Two concurrent updates → lost update.

```kotlin
// FLAG: classic lost update
state.value = state.value.copy(count = state.value.count + 1)

// FIX: atomic update (kotlinx.coroutines 1.7+)
state.update { it.copy(count = it.count + 1) }
```

`update { transform }` retries internally via `compareAndSet` until the swap succeeds.

| Audit grep | Verdict |
|-----------|---------|
| `state.value = state.value.copy(...)` | Reject when called from concurrent writers — use `update { }` |
| `state.value = computeFromState(state.value)` | Same — reject |
| `state.update { ... }` | Acceptable; verify the transform is pure (no side effects, since it may retry) |

Reference: [best-practices §3.6 `MutableStateFlow.update { }` over `.value = .value.copy()`](../../builder/references/kotlin-best-practices.md#36-mutablestateflowupdate--over-value--valuecopy).

### 8. `SharedFlow` replay / buffer / drop policy

`MutableSharedFlow<T>(replay, extraBufferCapacity, onBufferOverflow)`:

| Use | Configuration |
|-----|---------------|
| State (latest value matters; new subscribers see current) | `StateFlow` — purpose-built for this |
| Events (each emission must reach every subscriber once) | `SharedFlow(replay = 0, extraBufferCapacity = N, onBufferOverflow = SUSPEND)` |
| Hot-event stream where slow consumer can drop | `onBufferOverflow = DROP_OLDEST` (recent matters) or `DROP_LATEST` |
| Buffer everything and let slow consumer fall behind | `extraBufferCapacity = Int.MAX_VALUE` — **OOM risk** |

| Audit | Verdict |
|-------|---------|
| `SharedFlow` with `replay > 0` used for events | Reject — new subscribers re-execute side effects on the replayed events |
| `SharedFlow(onBufferOverflow = SUSPEND)` consumed slowly | The producer suspends; verify the producer isn't on a hot path that can't suspend |
| `extraBufferCapacity = 0, onBufferOverflow = SUSPEND` (default) | Producer blocks on every emit until consumer reads — verify acceptable |
| `tryEmit()` for non-suspend emit | Returns `false` on overflow — verify caller checks; many ignore it |

### 9. `flowOn` placement

`flowOn(dispatcher)` affects **upstream** of where it's called — emissions before `flowOn` run on the specified dispatcher; downstream stays on collector's dispatcher.

```kotlin
// CORRECT: upstream IO work on Dispatchers.IO; collector on Main
flow {
    val data = readFile()           // ← runs on Dispatchers.IO
    emit(data)
}
.map { it.parse() }                 // ← runs on Dispatchers.IO (still upstream of flowOn)
.flowOn(Dispatchers.IO)
.collect { ui.show(it) }            // ← runs on collector dispatcher (Main)

// FLAG: flowOn on terminal — no-op, collect controls its own dispatcher
flow.collect { ... }.flowOn(Dispatchers.IO)   // doesn't compile, but conceptual confusion

// FLAG: multiple flowOn — only the closest-upstream wins for each operator
flow { ... }.flowOn(Default).map { ... }.flowOn(IO)
// .map runs on IO, flow { } runs on Default (downstream-most flowOn wins per-op)
```

Audit: every `flowOn(X)` should be placed immediately downstream of the operators that actually want X.

### 10. `combine` of state flows — latest-only semantics

`combine(flow1, flow2) { a, b -> ... }` emits whenever EITHER source emits, with the latest values of both. Bursty producers can suppress intermediate emissions:

| Pattern | Behavior |
|---------|----------|
| `combine(state1, state2) { a, b -> Pair(a, b) }` | Each `state1.value = ...` triggers combine with current `state2.value` — every pair |
| Burst of 10 state1 updates while state2 is constant | Conflation may merge — `combine` doesn't guarantee every (a, b) pair is observed if collector is slow |
| `combine` for "any change → recompute UI" | Acceptable |
| `combine` to drive a transactional side effect | Reject — collector may miss intermediate states |

Reference: [language-spec §4.10 Hot flows](../../builder/references/kotlin-language-spec.md#410-hot-flows-stateflow-and-sharedflow).

### 11. `Channel` vs `SharedFlow` — choice matters

| Need | Choose |
|------|--------|
| Single producer, single consumer; fan-out NOT needed | `Channel` (capacity bounded; one consumer pulls) |
| One producer, N consumers (each sees every value) | `SharedFlow` |
| Producer hands ownership of each value to one consumer | `Channel` |
| Hot-event broadcast with no replay | `SharedFlow(replay = 0)` |
| `select { onSend / onReceive }` (multi-channel select) | `Channel` (Flow doesn't natively support) |

**Audit**: `Channel` consumed by `for ch in channel` in one place, then someone adds a second consumer → silent ownership confusion. `consumeAsFlow()` is single-shot; second collector throws.

### 12. `withContext` nested same dispatcher

`withContext(Dispatchers.IO) { ... }` while already on `Dispatchers.IO` does nothing useful but incurs an overhead and adds confusion.

```kotlin
suspend fun outerIO() = withContext(Dispatchers.IO) {
    innerIO()
}

suspend fun innerIO() = withContext(Dispatchers.IO) {   // ← no-op, but allocates
    File("x").readText()
}
```

| Audit | Verdict |
|-------|---------|
| `withContext(SameDispatcher) { ... }` nested with caller already on that dispatcher | Reject — remove inner |
| `withContext(Dispatchers.Default) { cpuWork() }` from a controller method | Acceptable |
| `withContext(NonCancellable) { ... }` | Audit — bypass cancellation. Justify with cleanup-must-complete reason. |

### 13. Cancellation cooperation

Coroutines cancel **cooperatively** — code that doesn't check for cancellation runs until completion.

| Pattern | Cooperate? |
|---------|------------|
| `delay(n)` | ✓ — throws `CancellationException` on cancel |
| `withContext(...)` | ✓ — checks at boundary |
| `yield()` | ✓ — explicit yield |
| `ensureActive()` | ✓ — throws if cancelled |
| `for x in someFlow.collect { ... }` | ✓ — Flow checks |
| Tight CPU loop `for i in 1..1_000_000 { ... }` | ✗ — uncooperative, runs to completion |
| `Thread.sleep(ms)` | ✗ — Java sleep; doesn't honor cancel |
| Blocking JDBC / blocking IO call | ✗ — runs to completion |

**Fix patterns**:

```kotlin
// CPU loop — call ensureActive periodically
for (i in 1..1_000_000) {
    coroutineContext.ensureActive()      // throws CancellationException on cancel
    process(i)
}

// Or use yield() to also be a good citizen for fairness
for (i in 1..1_000_000) {
    yield()
    process(i)
}
```

Reference: [language-spec §4.6 Cooperative cancellation](../../builder/references/kotlin-language-spec.md#46-cooperative-cancellation).

### 14. Coroutine exception transparency in Flow

`Flow` has a strict rule: a downstream operator's exception must not be caught by an upstream `catch` operator. `Flow.catch { ... }` only catches exceptions from operators UPSTREAM of the `catch` call.

```kotlin
// FLAG: catch above the throwing operator — never fires
flow {
    emit(1)
}
.catch { /* upstream errors */ }
.map { throw RuntimeException() }     // ← not caught by above

// FIX: catch placed below all throwing operators
flow { emit(1) }
.map { throw RuntimeException() }
.catch { /* fires */ }
```

Audit grep:

```sh
rg -n '\.catch\s*\{' --type kotlin -B 3 -A 3
```

For each, verify it's downstream of the operators that may throw.

### 15. Detekt rules — concurrency CI minimum

```yaml
# detekt.yml
coroutines:
  active: true
  GlobalCoroutineUsage: { active: true }                    # GlobalScope.launch
  InjectDispatcher: { active: true }                         # inject vs hard-code Dispatchers.X
  RedundantSuspendModifier: { active: true }                 # suspend fn that doesn't suspend
  SleepInsteadOfDelay: { active: true }                      # Thread.sleep in suspend
  SuspendFunWithFlowReturnType: { active: true }             # suspend fun foo(): Flow<X> — wrong shape
  SuspendFunSwallowedCancellation: { active: true }          # catch (e: Exception) swallowing CancellationException
  SuspendFunWithCoroutineScopeReceiver: { active: true }     # mixing suspend + CoroutineScope receiver
```

CancellationException handling discipline (the second-most subtle Kotlin coroutine bug):

```kotlin
// FLAG: catch (e: Exception) catches CancellationException — coroutine no longer cancellable
try {
    work()
} catch (e: Exception) {
    log(e)                               // swallows cancellation
}

// FIX: re-throw CancellationException
try {
    work()
} catch (e: CancellationException) {
    throw e
} catch (e: Exception) {
    log(e)
}
```

Detekt: `coroutines:SuspendFunSwallowedCancellation`.

---

## Triage priorities

When multiple findings stack, rank by:

1. **`runBlocking` on request hot path** — single attacker request pins a worker; saturates worker pool for DoS.
2. **`GlobalScope.launch` orphan coroutine** — outlives every meaningful lifecycle; leaks resources; in tests, leaks across tests producing flake.
3. **`StateFlow` `value = value.copy()` lost update under concurrent writers** — silent data loss.
4. **`async { }` never awaited → swallowed exception** — failures vanish; production diagnostics blind to this class of bug.
5. **CancellationException swallowed by `catch (Exception)`** — coroutine becomes uncancellable; resource and lifecycle bugs.
6. **`coroutineScope` vs `supervisorScope` misuse** — sibling cancellation when callers expected independence (or vice-versa).
7. **`Dispatchers.IO` unbounded / no `.limitedParallelism`** — bursts saturate, cascade slowness across subsystems.
8. **`SharedFlow(replay > 0)` for events** — replay re-executes side effects.
9. **Uncooperative CPU loops** — cancellation requested but loop runs to completion; user-visible "won't cancel".
10. **`Channel` accidentally consumed twice** — `consumeAsFlow().collect` twice throws at runtime; second collect path may live in untested code.
11. **`Flow.catch` above the throwing operator** — exception bypasses handler; uncaught upward.
12. **`Mutex` held across long suspend** — fairness collapse; effective single-thread for that data.

---

## Sources

- Kotlin coroutines guide — Exception handling and supervision: https://kotlinlang.org/docs/exception-handling.html
- Kotlin coroutines — Cancellation and timeouts: https://kotlinlang.org/docs/cancellation-and-timeouts.html
- Kotlin Flow guide: https://kotlinlang.org/docs/flow.html
- Roman Elizarov — Structured Concurrency talk
- Roman Elizarov — "Cold flows, hot channels" (Medium): https://elizarov.medium.com/
- `kotlinx.coroutines.test` — runTest and dispatchers: https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-test/
- Detekt coroutines rules: https://detekt.dev/docs/rules/coroutines
- `kotlinx.atomicfu`: https://github.com/Kotlin/kotlinx-atomicfu
- Turbine (Flow testing): https://github.com/cashapp/turbine
- Square — "Effective coroutines" series
- A Survey of Bug Detection in Kotlin (arxiv 2306.10515)
