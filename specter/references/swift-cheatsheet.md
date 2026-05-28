# Swift Concurrency Audit Cheatsheet — Specter

Focused checklist for concurrency, actor, and race-condition review of Swift codebases. Baseline: **Swift 6.2+ / Xcode 26** with **Swift 6.3 outlook** (2026-05).

> Source-of-truth references (full catalog lives in Builder):
> - Constructive concurrency stack: [`builder/references/swift-best-practices.md` §2 Concurrency Best Practices](../../builder/references/swift-best-practices.md#2-concurrency-best-practices-swift-62-era)
> - Concurrency pitfalls (3.1–3.6): [`builder/references/swift-anti-patterns.md` §3 Concurrency pitfalls](../../builder/references/swift-anti-patterns.md#3-concurrency-pitfalls-swift-62-era)
> - Reference cycle / closure capture pitfalls: [`builder/references/swift-anti-patterns.md` §2 Reference cycle pitfalls](../../builder/references/swift-anti-patterns.md#2-reference-cycle-pitfalls)
> - Memory model, Sendable, isolation, region-based isolation, `sending`, `nonisolated(nonsending)`: [`builder/references/swift-language-spec.md` §3 Concurrency Model](../../builder/references/swift-language-spec.md#3-concurrency-model)
> - Low-level synchronization (Swift 6.0 `Mutex`, `Atomic`): [`builder/references/swift-language-spec.md` §3.14](../../builder/references/swift-language-spec.md#314-low-level-synchronization-swift-60)

**Do not duplicate the catalogs above.** This cheatsheet is the *audit order* Specter applies on Swift Concurrency code; it links rather than restates.

Companion cheatsheets (same agent):
- SAST / code-level security: [`sentinel/references/swift-cheatsheet.md`](../../sentinel/references/swift-cheatsheet.md)
- Crypto design: [`crypt/references/swift-cheatsheet.md`](../../crypt/references/swift-cheatsheet.md)

Swift prevents **data races** at compile time when Strict Concurrency Checking is enabled (Swift 6 default). It does **not** prevent **logical race conditions** — actor reentrancy, lost updates, deadlocks, cancellation-related state loss. Specter's primary value on Swift code is the latter, plus reviewing the soundness of escape hatches (`@unchecked Sendable`, `nonisolated(unsafe)`).

---

## When auditing a Swift concurrency surface, walk this checklist:

### 1. Map the isolation model

| Question | How |
|----------|-----|
| Swift 6.2 default isolation? | `rg -n 'defaultIsolation' Package.swift` — Swift 6.2 packages can opt the *whole module* into `MainActor` default; check both `swiftSettings` and `.enableExperimentalFeature("DefaultMainActorIsolation")`. |
| Strict Concurrency level? | Swift 6 = `complete` by default; Swift 5 modules may have `.enableUpcomingFeature("StrictConcurrency")`. Audit any `targetedDataRaceSafety` deviation. |
| Actor surface? | `rg -n '^actor \|@MainActor\|@globalActor' --type swift` |
| Sendable conformances? | `rg -n ': Sendable\|@unchecked Sendable\|nonisolated\(unsafe\)' --type swift` |
| Task spawn surface? | `rg -n 'Task\s*{\|Task\.detached\|withTaskGroup\|withDiscardingTaskGroup\|TaskGroup\|withThrowingTaskGroup' --type swift` |
| Continuation usage? | `rg -n 'withCheckedContinuation\|withUnsafeContinuation\|withCheckedThrowingContinuation\|withUnsafeThrowingContinuation' --type swift` |

### 2. Actor reentrancy — the most under-reviewed concurrency bug

Actors **serialize** access to their state, but they are **reentrant**. When an actor method `await`s, the actor unlocks, other messages can run, and the original method resumes with **state that may have changed**.

| Symptom | Cause |
|---------|-------|
| "Sometimes we issue duplicate API requests" | Single-flight cache misses the in-flight check after `await` resume — see [anti-patterns §3.2](../../builder/references/swift-anti-patterns.md#32-actor-reentrancy-the-classic-state-stale-bug). |
| "Counter occasionally jumps by 2 instead of 1" | `let n = self.count; await something(); self.count = n + 1` — classic lost update across reentrancy. |
| "Login validates but then runs against the previous user's session" | State capture across `await` returned to stale value |

**Canonical wrong pattern** (full discussion in [anti-patterns §3.2](../../builder/references/swift-anti-patterns.md#32-actor-reentrancy-the-classic-state-stale-bug)):

```swift
actor ImageLoader {
    private var cache: [URL: UIImage] = [:]
    func load(_ url: URL) async -> UIImage {
        if let cached = cache[url] { return cached }     // CHECK
        let img = await download(url)                    // ← reentrancy window
        cache[url] = img                                 // STORE — may overwrite a peer's work
        return img
    }
}
```

Two callers with the same URL both miss the cache, both await `download`, both write — wasted work + cache-write race semantics.

**Single-flight + token pattern**:

```swift
actor ImageLoader {
    private enum Entry { case ready(UIImage); case inflight(Task<UIImage, Never>) }
    private var cache: [URL: Entry] = [:]

    func load(_ url: URL) async -> UIImage {
        if case .ready(let img) = cache[url] { return img }
        if case .inflight(let t) = cache[url] { return await t.value }   // join in-flight

        let task = Task<UIImage, Never> { await self.download(url) }
        cache[url] = .inflight(task)
        let img = await task.value
        cache[url] = .ready(img)
        return img
    }
}
```

**Audit rule**: any actor method that mutates state across `await` is a reentrancy candidate. Check whether peer messages can invalidate the captured state.

### 3. `@MainActor` everywhere — the escape hatch becomes the architecture

Liberal `@MainActor` was a Swift 5 workaround for Sendable noise. In Swift 6.2 with Approachable Concurrency, the migration target is **explicit isolation per type, not per method**.

| Pattern | Verdict |
|---------|---------|
| `@MainActor class Service` for pure compute | Wrong tool — pinned to UI thread, blocks UI render. Move compute off `@MainActor`. |
| `@MainActor` on a ViewModel that calls async `Repository` | Acceptable; ViewModel is UI-adjacent. Repository should be its own actor or `nonisolated(nonsending)`. |
| `@MainActor` on every method instead of the type | Re-isolation fragmentation. If most methods are main-isolated, isolate the type. |
| `@MainActor` propagated up through `async` boundary into background-suitable code | Audit: does the call really need main-thread? `nonisolated` the leaf compute fn. |
| Swift 6.2 module-level `defaultIsolation: MainActor` | Acceptable for UI-heavy modules (app target); reject for library targets that must work off main. |

Reference: [best-practices §2.2 Approachable Concurrency](../../builder/references/swift-best-practices.md#22-approachable-concurrency-se-0466--default-isolation), [§2.5 actor vs class+Lock decision matrix](../../builder/references/swift-best-practices.md#25-actor-vs-class--lock--decision-matrix).

### 4. `nonisolated(nonsending)` default — the 6.2 semantic change

Swift 6.2's biggest behavioral change: a `nonisolated` async function **inherits** the caller's isolation by default (was: ran on the global executor). Old Swift 5 / early-6 code may rely on the previous behavior.

| Behavior | Pre-6.2 default | 6.2 default |
|----------|-----------------|-------------|
| `nonisolated func foo() async` called from `@MainActor` | Hopped to global executor | Stays on `@MainActor` |
| To get background execution | `nonisolated func foo() async` | `@concurrent func foo() async` (explicit) OR `nonisolated(nonsending)` (explicit inherit) |

**Audit during migration**: every old `nonisolated func` async marked because it "did expensive work off-main" needs to be reviewed — under 6.2 default, that call **stays on main**.

```swift
// Old expectation: hopped off main
nonisolated func sortLargeDataset(_ xs: [Int]) async -> [Int] { xs.sorted() }

// Caller from MainActor; in Swift 6.2 default, sortLargeDataset runs on main thread.
// Fix: annotate explicitly.
@concurrent func sortLargeDataset(_ xs: [Int]) async -> [Int] { xs.sorted() }
```

Reference: [language-spec §3.11](../../builder/references/swift-language-spec.md#311-nonisolatednonsending--concurrent-swift-62--the-biggest-2026-semantic-change).

### 5. `@concurrent` placement decision matrix

| Function shape | Annotation | Reason |
|----------------|------------|--------|
| Synchronous compute, called from `@MainActor` | `nonisolated` (default) | Sync calls stay on caller's thread anyway |
| Async I/O bound, called from `@MainActor`, doesn't touch UI | `@concurrent` | Off-main I/O explicitly |
| Async compute, doesn't care about isolation, must inherit caller's | `nonisolated(nonsending)` (or just `nonisolated` in 6.2) | New default behavior — explicit document |
| Async actor method | actor isolation default | No annotation needed |
| Sendable-bound work | `@concurrent` if must run off caller | Forces explicit background execution |

### 6. Region-based isolation (Swift 6.1+) — `sending` rules

Region-based isolation lets the compiler pass non-`Sendable` values across isolation boundaries when the **sender no longer uses them**. `sending` parameters opt in.

```swift
// `sending` lets caller pass a non-Sendable value, transferring ownership
func process(_ value: sending NonSendableState) async {
    // value is now owned in this isolation
}
```

| Audit | What |
|-------|------|
| `sending T` parameter | Document that caller transfers ownership; verify caller doesn't access after the call |
| `sending` return type | Function transfers ownership of the returned value out |
| Diamond capture (one value captured by two closures running in different isolations) | Compiler rejects under region isolation; verify no `@unchecked Sendable` hack-around |

Reference: [language-spec §3.9, §3.10](../../builder/references/swift-language-spec.md#39-region-based-isolation-se-0414-swift-60-refined-61).

### 7. `@unchecked Sendable` — runtime crash mode

Same scope as Sentinel §3, audited from concurrency-semantic angle: does the soundness argument actually hold under concurrent calls?

| Pattern | Soundness audit |
|---------|-----------------|
| `final class Foo: @unchecked Sendable` with `var` stored properties | Reject unless every `var` is lock-protected with explicit `Mutex<T>` (Swift 6.0) or `OSAllocatedUnfairLock` |
| `@unchecked Sendable` over a struct containing a `class` reference | Audit reachability — the inner class itself must be Sendable, else publishing the struct publishes a non-Sendable reference |
| `@unchecked Sendable` over `NSCache`/`NSMapTable` | Acceptable — Foundation thread-safe; document why in `// SAFETY:` |
| `@unchecked Sendable` over a UIKit/AppKit object | Reject categorically — UI objects are main-thread-bound |
| `@unchecked Sendable` over a Combine `Subject` (Subjects are thread-safe) | Acceptable for the wrapper, but the values flowing through must themselves be Sendable |

Reference: [anti-patterns §3.3](../../builder/references/swift-anti-patterns.md#33-unchecked-sendable-runtime-crash-mode).

### 8. `Task { }` capture cycles and orphan tasks

Unlike async/await in some languages, Swift's `Task { }` has **no implicit JoinHandle equivalent**. You must store the returned `Task<T, Error>` and `cancel()` it to terminate the work.

| Pattern | Risk |
|---------|------|
| `Task { await self.work() }` inside a class init | Captures `self` strongly → cycle if `self` also stores the Task. Use `[weak self]`. |
| `Task { ... }` started in a view's `.task { }` modifier | Auto-cancelled on view disappear (good) |
| `Task { ... }` returned and discarded (`_ = Task { ... }`) | **Orphan task** — runs to completion, even after the conceptual owner is gone. No way to surface failures. |
| `let t = Task { ... }; t` never cancelled, never awaited | Leaks the task; if it captures resources, leaks those too |
| `Task.detached(priority:operation:)` | Doesn't inherit isolation or task-local values. Audit for unintended privilege drop or task-local loss (auth context, logging context). |

**Canonical pattern**:

```swift
@MainActor
final class ViewModel {
    private var loadTask: Task<Void, Never>?

    func startLoading() {
        loadTask?.cancel()       // cancel any prior load
        loadTask = Task { [weak self] in
            guard let self else { return }
            await self.load()
        }
    }

    deinit { loadTask?.cancel() }   // ensure no orphan
}
```

Reference: [best-practices §2.7 Structured Concurrency Over Unstructured `Task { }`](../../builder/references/swift-best-practices.md#27-structured-concurrency-over-unstructured-task), [anti-patterns §2.4](../../builder/references/swift-anti-patterns.md#24-task-retain-cycle-subtlety).

### 9. Structured cancellation in `TaskGroup` / `withTaskGroup`

| Tool | Use |
|------|-----|
| `withTaskGroup(of:returning:)` | Children produce values; group collects them |
| `withDiscardingTaskGroup` (6.0+) | Children are fire-and-forget; group waits for all to finish; results discarded |
| `withThrowingTaskGroup` | Any child throwing cancels siblings (default) |
| `withThrowingDiscardingTaskGroup` | Throwing + discarding combo |

| Audit | Check |
|-------|-------|
| Long-running group with many children | Use `.discardingTaskGroup` if results aren't collected — saves memory |
| Child task doesn't honor `Task.isCancelled` / `try Task.checkCancellation()` | Cancellation propagates by **request**, not preemption — uncooperative work runs to completion |
| `group.addTask` inside a loop that may overflow | Backpressure: add a `await group.next()` pattern to bound concurrency. See [best-practices §2.7](../../builder/references/swift-best-practices.md#27-structured-concurrency-over-unstructured-task). |
| `group.cancelAll()` not called on early exit | Sibling children continue running |

```swift
// Bounded concurrency pattern — 8 in flight max
try await withThrowingTaskGroup(of: Result.self) { group in
    var inflight = 0
    for url in urls {
        if inflight >= 8 { _ = try await group.next(); inflight -= 1 }
        group.addTask { try await fetch(url) }
        inflight += 1
    }
    for try await result in group { /* collect */ }
}
```

### 10. Continuation patterns (single-resume invariant)

`withCheckedContinuation` (and its throwing/unsafe variants) MUST resume **exactly once**:

- Zero resumes → task hangs forever, structural concurrency awaits indefinitely
- Two resumes → `withCheckedContinuation` crashes ("CHECKED_CONTINUATION_MISUSE"); `withUnsafeContinuation` is UB
- Race between paths (one path resumes, other path also resumes) → same crash

| Audit | How |
|-------|-----|
| Every continuation closure has exactly one `continuation.resume(...)` per code path | Trace each `if/else`, `do/catch`, `switch` arm |
| Callback APIs guarantee exactly one of {success, error} | Often legacy APIs call both under timeout — wrap in atomic flag |
| Continuation captured in `@escaping` closure outliving the function | Audit for the closure being invoked twice (e.g. retry frameworks) |
| Timeout race (an outer `withTimeout` wrapper cancels) | Verify the inner closure cannot also resume — use AtomicBool gate |

Canonical safe wrapper from [anti-patterns §3.6](../../builder/references/swift-anti-patterns.md#36-continuation-safety-wrapper):

```swift
import os
// AtomicBool-based gate
final class ContinuationGate: Sendable {
    private let resumed = OSAllocatedUnfairLock<Bool>(initialState: false)
    func tryConsume() -> Bool {
        resumed.withLock { r in if r { false } else { r = true; return true } }
    }
}
```

### 11. Mixing GCD inside async functions

`DispatchQueue.main.async { ... }` inside an `async` function is a smell — it bypasses the isolation system.

| Pattern | Verdict |
|---------|---------|
| `await MainActor.run { ... }` for one-shot main-thread work from `nonisolated async` | Acceptable transition |
| `DispatchQueue.main.async { ... }` inside `async fn` | Reject — invisible to actor isolation, can race with concurrent main-isolated work |
| `DispatchQueue.global().async { ... }` inside `async fn` | Reject — use `Task.detached` or `@concurrent fn` |
| Async wrapping legacy GCD-completion-handler API | Acceptable via `withCheckedContinuation`; audit single-resume invariant |
| `DispatchSemaphore` in async code | Reject — blocking, defeats cooperation; use actor or `AsyncSemaphore` (vapor/`swift-async-algorithms`) |
| `dispatchPrecondition(condition: .onQueue(...))` for runtime check | Acceptable for diagnostics; remove from release |

### 12. `Mutex<T>` (Swift 6.0 stdlib) vs `actor` — when to use which

| Need | Choose | Why |
|------|--------|-----|
| Protected state accessed mostly from one isolation | `actor` | Isolation is the natural model |
| State that must be read/written across many isolations *synchronously* | `Mutex<T>` | Actors require `await`; `Mutex` is sync |
| Hot, fine-grained counter | `Atomic<Int>` (Swift 6.0) | Lockless, fastest |
| Reader-many, writer-rare | `OSAllocatedUnfairLock<T>` (or `pthread_rwlock` via wrapper) | RW lock semantics |
| Lazy initialization across threads | `Mutex<T>` + check pattern, or `LockIsolated<T>` (Point-Free) | See [best-practices §6.6 Pattern: Lazy Initialization with `Mutex`](../../builder/references/swift-best-practices.md#66-pattern-lazy-initialization-with-mutex) |

Reference: [language-spec §3.14](../../builder/references/swift-language-spec.md#314-low-level-synchronization-swift-60), [best-practices §2.5, §2.6](../../builder/references/swift-best-practices.md#25-actor-vs-class--lock--decision-matrix).

### 13. `AsyncSequence` cancellation propagation

`AsyncSequence.makeAsyncIterator()` produces an iterator whose `next()` is async — cancellation propagates by **the iterator returning `nil`** or `next()` throwing `CancellationError`.

| Pattern | Audit |
|---------|-------|
| `for try await x in stream { ... }` inside a `Task` | Cancelling the task → iterator's `next()` returns `nil` if the stream is cancellation-aware. Verify the stream impl checks `Task.isCancelled`. |
| `AsyncStream` continuation closed externally | Consumer's `for await` loop ends naturally |
| Hand-rolled `AsyncSequence` that does I/O in `next()` | Audit: does it check `Task.isCancelled` between yields? Otherwise cancellation only takes effect at the next yield point. |
| `AsyncSequence` combined with `.timeout` (`swift-async-algorithms`) | Wrapped iterator handles cancellation; verify the inner iterator is **cancel-safe** (no commit-then-await-then-rollback patterns). |
| `Combine.Publisher.values` (Combine → AsyncSequence bridge) | Iterator cancellation cancels the underlying subscription |

### 14. `Atomic<T>` (Swift 6.0) memory orderings

Swift's `Atomic<T>` adopts the C++20 memory model (the same as Rust). Common pitfalls:

| Ordering | Use |
|----------|-----|
| `.relaxed` | Counters with no dependency on other atomics (metrics, debug) |
| `.acquiring` (load) + `.releasing` (store) | Flag publishing a payload — reader acquires, sees prior releases |
| `.acquiringAndReleasing` | RMW that consumes and publishes |
| `.sequentiallyConsistent` | Multi-atomic protocols needing a single global order — rare; default if uncertain, optimize down later |

Audit grep:

```sh
rg -n 'Atomic<\|\.load\|\.store\|\.compareExchange\|\.weakCompareExchange' --type swift
```

For every `load(.acquiring)`, find the paired `store(.releasing)`. Mismatched orderings → readers see stale payload.

### 15. Concurrency-related CI gate

```yaml
# Build with Strict Concurrency = complete
- run: |
    xcodebuild build -project App.xcodeproj -scheme App \
      OTHER_SWIFT_FLAGS='-strict-concurrency=complete -warnings-as-errors'

# SwiftLint concurrency-aware rules
# .swiftlint.yml
opt_in_rules:
  - prefer_zero_over_explicit_init
  - explicit_acl
  - unowned_variable_capture           # unowned + weak audit
  - weak_delegate
  - last_where
  - prefer_self_in_static_references
  - sorted_first_last
  - no_extension_access_modifier
analyzer_rules:
  - capture_variable                   # closure captures audit
  - unused_declaration
disabled_rules:
  - block_based_kvo                    # noisy; review per-project
```

For TaskGroup-heavy code, run with thread sanitizer in tests:

```yaml
- run: |
    xcodebuild test -project App.xcodeproj -scheme AppTests \
      -enableThreadSanitizer YES -destination 'platform=iOS Simulator,name=iPhone 15'
```

---

## Triage priorities

When multiple findings stack, rank by:

1. **Continuation double-resume / never-resume** — `withCheckedContinuation` crashes on second resume; `withUnsafeContinuation` is UB; never-resume hangs entire task tree.
2. **Actor reentrancy logic bug** (lost update, stale state after `await`) — produces duplicate API calls, lost writes; appears as "intermittent" production bug.
3. **`@unchecked Sendable` over mutable state** — data race in release; corrupts ARC, untraceable crashes.
4. **Orphan `Task { }`** — silent panic/failure loss; leaks resources; auth-context drift via `Task.detached` losing task-locals.
5. **`@MainActor` everywhere** — UI thread saturation, jank, watchdog termination.
6. **GCD mixed into async** — bypasses isolation system; race-prone main-thread coordination.
7. **`TaskGroup` cancellation not cooperated with** — siblings continue past cancel; resource waste; sometimes side-effect duplication.
8. **`AsyncSequence` cancel-unaware** — iterator commits state then awaits, cancel mid-flight loses or commits twice.
9. **Atomic ordering mismatch** — manifests under load; require structured reasoning (no `loom` in Swift world — TSan + property tests).
10. **6.2 isolation semantic change unreviewed** — old `nonisolated async` code now stays on main; perf regression masquerading as "the app got slow."
11. **`DispatchSemaphore`-blocking inside `async`** — pinned worker, deadlock in current-thread executor configurations.

---

## Sources

- Swift Evolution — Approachable Concurrency (SE-0466): https://github.com/swiftlang/swift-evolution/blob/main/proposals/0466-control-default-actor-isolation.md
- Swift Evolution — Region-based isolation (SE-0414): https://github.com/swiftlang/swift-evolution/blob/main/proposals/0414-region-based-isolation.md
- Swift Evolution — `sending` (SE-0430): https://github.com/swiftlang/swift-evolution/blob/main/proposals/0430-transferring-parameters-and-results.md
- Swift Evolution — `nonisolated(nonsending)` + `@concurrent` (SE-0431): https://github.com/swiftlang/swift-evolution/blob/main/proposals/0431-isolated-any-functions.md
- Apple — Updating an App to Use Strict Concurrency: https://developer.apple.com/documentation/swift/updating_an_app_to_use_strict_concurrency
- Apple — `Atomic` (Swift 6.0 Synchronization): https://developer.apple.com/documentation/synchronization
- Apple — `Mutex`: https://developer.apple.com/documentation/synchronization/mutex
- Apple — `withCheckedContinuation`: https://developer.apple.com/documentation/swift/withcheckedcontinuation(function:_:)
- swift-async-algorithms (timeout, combineLatest, debounce): https://github.com/apple/swift-async-algorithms
- Point-Free — `LockIsolated`: https://github.com/pointfreeco/swift-concurrency-extras
- Doug Gregor on actor reentrancy: https://forums.swift.org/t/reentrancy-in-actor-isolated-code/
- WWDC23 "Beyond the basics of structured concurrency" (Apple)
- WWDC24 "Embracing Swift concurrency" (Apple)
