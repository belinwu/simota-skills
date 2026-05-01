# Specter LLM Fix Prompt Generation

**Purpose:** Specter-specific action verbs, suppression cases, template fields, and worked example for the `## LLM Fix Prompt` block that pairs every confirmed concurrency, async, or resource-management finding with a paste-ready handoff to Builder.
**Read when:** Specter has confirmed a ghost (race, leak, deadlock, resource exhaustion) and is handing remediation to Builder rather than running in detection-only mode.

> Universal authoring rules and prompt structure: `_common/LLM_PROMPT_GENERATION.md`.
> This file documents only Specter-specific verbs, suppression cases, template fields, and an example.

## Contents

- When Specter emits a Fix Prompt vs withholds
- Specter action verbs
- Verb selection heuristic
- Specter-specific suppression cases
- Per-finding fix prompt template (Specter-specific fields)
- Worked example

---

## When Specter Emits a Fix Prompt vs Withholds

Specter never modifies code (Core Contract: "Never modify code; hand all fixes to Builder"). The Fix Prompt is the handoff artifact for every confirmed finding. The decision is whether to emit one at all:

| Situation | Action |
|-----------|--------|
| Confirmed race/leak/deadlock/resource finding with HIGH or MEDIUM confidence | Emit Fix Prompt + hand off to Builder |
| Detection-only mode (user explicitly asked for scan results, no remediation) | Suppress prompt with note |
| Finding is actually a security vulnerability (e.g., TOCTOU) | Suppress prompt; escalate to Sentinel |
| Finding is structural — needs architecture redesign, not a bug fix | Emit `REFACTOR-FIX` prompt addressed to Atlas → Builder |
| Finding is a performance optimization, not a correctness defect | Suppress prompt; escalate to Bolt |
| LOW confidence + no reliable reproducer | Emit `INVESTIGATE-FURTHER` prompt with verification plan |
| Multiple ghost categories equally probable | Stop and ask user (per Core Contract); suppress prompt until disambiguated |

The `SPECTER_TO_BUILDER` handoff carries a `fix_prompt` field; populate it whenever Specter confirms a finding and is not escalating to Sentinel/Bolt/Atlas.

---

## Specter Action Verbs

Each fix prompt declares one verb at the top of `# Your task`.

| Verb | When to use | Receiving agent |
|------|-------------|----------------|
| `RACE-FIX` | Confirmed race condition with reproducer (TSAN/DataRace detector or repeated trial flip) | Builder |
| `LEAK-FIX` | Memory or resource leak with retention path / handle leak source identified | Builder |
| `LOCK-FIX` | Deadlock with documented lock acquisition order | Builder |
| `RESOURCE-FIX` | Resource exhaustion (file handle, connection pool, goroutine/thread leak) with budget plan | Builder |
| `MITIGATE` | Workaround (timeout, circuit breaker, retry budget) while underlying fix is blocked | Builder |
| `INVESTIGATE-FURTHER` | Low confidence — needs runtime instrumentation, profiler, or deeper trace | Claude/Codex (investigation mode) or Specter re-entry |
| `REFACTOR-FIX` | Structural concurrency redesign needed (e.g., remove shared mutable state, switch to actor model) | Atlas → Builder |

---

## Verb Selection Heuristic

```
Ghost category == Race ─┬─ HIGH confidence + reproducer ──→ RACE-FIX
                        ├─ HIGH confidence + structural redesign ──→ REFACTOR-FIX
                        └─ LOW/MEDIUM, intermittent only ──→ INVESTIGATE-FURTHER

Ghost category == Memory leak / Resource leak ─┬─ retention path identified ──→ LEAK-FIX
                                                ├─ pool exhaustion + budget plan ──→ RESOURCE-FIX
                                                └─ growth observed but source unclear ──→ INVESTIGATE-FURTHER

Ghost category == Deadlock ─┬─ lock order documented ──→ LOCK-FIX
                             └─ structural (circular ownership) ──→ REFACTOR-FIX

Underlying fix blocked / out of scope ──→ MITIGATE
```

Tiebreakers:
- If the finding spans 4+ files or requires removing shared mutable state, prefer `REFACTOR-FIX` over `RACE-FIX` / `LOCK-FIX`.
- If a race is reproducible only under TSAN but not in production-equivalent runs, prefer `INVESTIGATE-FURTHER` over `RACE-FIX` and require Builder to confirm reproduction first.
- Pool-exhaustion findings (`totalCount === max && idleCount === 0 && waitingCount > 0` sustained) always emit `RESOURCE-FIX` (not `LEAK-FIX`) because the fix scope includes acquire/release discipline AND budget configuration.
- `MITIGATE` is never the first choice — emit it only after documenting why the underlying fix is blocked.

---

## Specter-Specific Suppression Cases

Universal cases live in `_common/LLM_PROMPT_GENERATION.md`. Specter adds:

| Case | Reason | Note in report |
|------|--------|----------------|
| Specter escalates to Sentinel (concurrency issue is actually a security vuln like TOCTOU) | Sentinel owns secure-fix prompts | "Fix prompt suppressed — Sentinel owns remediation prompt." |
| Specter escalates to Atlas (structural design issue, not a single bug) | Atlas owns the architectural redesign | "Fix prompt withheld — finding routed to Atlas as architectural concern." |
| Specter escalates to Bolt (resource issue is performance optimization, not correctness) | Bolt owns the optimization prompt | "Fix prompt suppressed — Bolt owns optimization prompt." |
| Detection-only mode (no fix scope) | Out of scope for this engagement | "Fix prompt N/A — detection-only." |

---

## Per-Finding Fix Prompt Template (Specter Fields)

Specter adds these Specter-specific blocks on top of the universal skeleton:

- `Detection method` — TSAN / Helgrind / Go race detector / heap snapshot / pprof / RacerD / Fray / MemLab / etc.
- `Reproducibility` — trial count + flip rate (e.g., "10/100 trials" for races) OR "deterministic"
- `Concurrency model` — thread / goroutine / async-await / actor model
- `Synchronization primitives involved` — mutex names, channel ops, atomic ops, etc.
- `Risk breakdown` — Detectability/Impact/Frequency/Recovery/DataRisk scores from the risk matrix
- `Suggested tests` — regression and stress test specs for Radar handoff

````markdown
## LLM Fix Prompt

```text
# Your task
<VERB> the concurrency/resource finding described below.

# Finding context
- Title: [brief description]
- Ghost category: [Race | Memory leak | Resource leak | Deadlock | Unhandled rejection | Distributed race]
- Severity: [CRITICAL | HIGH | MEDIUM | LOW]
- Confidence: [HIGH | MEDIUM | LOW] (Specter's pattern + analysis confidence)
- Risk score: [composite from D×0.20 + I×0.30 + F×0.20 + R×0.15 + DR×0.15]

# Detection method
- Tool: [TSAN | Go race detector | RacerD | Fray | MemLab | pprof | heap snapshot | static pattern]
- Reproducibility: [e.g., "12/100 trials under -race" | "deterministic" | "intermittent in CI only"]
- Concurrency model: [thread | goroutine | async-await | actor]
- Synchronization primitives involved: [mutex names, channel ops, atomic ops, pool handles]

# Root cause
[What invariant is violated and under what interleaving / lifecycle path]

Location: `<file>:<line>` in `<function>()`

# Evidence
Bad code:
```
[verbatim code snippet showing the unsafe access / missing release / lock order]
```

Detector output (if any):
```
[verbatim TSAN report, race trace, leak summary, or pool-stat snapshot]
```

# Recommended fix
Approach: [strategy — e.g., guard with mutex, convert to channel, defer release, switch to scoped lifetime]
Files to modify: [list with expected change per file]
Synchronization plan:
- [primitive choice and why — e.g., "sync.RWMutex because reads dominate"]
- [lock acquisition order if multiple locks are involved]
Constraints:
- [coupling / backward-compat note]
- [hot-path performance budget — concurrency fixes must not regress p99]

# [MITIGATE only — Underlying status]
- Why the underlying fix is blocked: [reason]
- Workaround scope: [timeout / circuit breaker / retry budget value]
- Re-open trigger: [condition under which the underlying fix is unblocked]

# [REFACTOR-FIX only — Structural concern]
- Why a single-file patch is insufficient: [evidence — shared mutable state, ownership ambiguity, etc.]
- Proposed structural change: [e.g., move ownership into a single goroutine, adopt actor model, replace shared map with channel]

# Acceptance criteria
- [ ] Detection method above no longer reports the finding (e.g., `go test -race ./pkg/...` clean)
- [ ] Reproducer (if present) flips to 0/100 trials
- [ ] Regression test added covering the interleaving / lifecycle path
- [ ] No new test failures in the affected module
- [ ] No p99 latency regression > 5% in the touched hot path (when measurable)
- [ ] [LEAK-FIX / RESOURCE-FIX] Pool / heap / handle counters return to baseline after soak test

# Ruled-out alternatives (do not revisit)
- [alternative 1] — eliminated because [evidence, e.g., "atomic.Value insufficient — read-modify-write pattern requires lock"]
- [alternative 2] — eliminated because [evidence, e.g., "channel-based redesign blocked by external API contract"]

# What NOT to do
- Do not silence the symptom (catch-and-ignore, broad try/except, swallow detector warnings, retry-until-it-passes)
- Do not "fix" by adding sleeps, polling delays, or retry loops to mask the race
- Do not disable the race detector / leak check in CI
- Do not widen lock scope beyond what evidence requires (lock contention is a real cost)
- Do not bundle unrelated concurrency changes into the same PR
- Do not expand scope beyond the cited files unless evidence demands it

# Suggested tests (for Radar)
- [stress test scenario, e.g., "N=1000 parallel goroutines invoking SetUser/GetUser"]
- [soak test, e.g., "24h run with pg pool stats sampled every 30s"]
- [interleaving test, e.g., "Fray controlled-interleaving for 200 schedules"]
```
````

For `INVESTIGATE-FURTHER`, replace "Recommended fix" with "Verification plan" (instrumentation steps, profiler runs, traces to capture before changing code).

---

## Worked Example (RACE-FIX)

**Scenario:** A Go HTTP service stores per-user session state in a shared `map[string]*Session` guarded only by a `sync.RWMutex` on read paths but missing the lock on a fast-path optimization in `Touch()`. Under load, the Go race detector flags concurrent map writes from `Touch()` racing with `SetUser()`, occasionally panicking the process.

````markdown
## LLM Fix Prompt

```text
# Your task
RACE-FIX the concurrency/resource finding described below.

# Finding context
- Title: Concurrent map write race in SessionStore.Touch vs SetUser
- Ghost category: Race
- Severity: CRITICAL
- Confidence: HIGH (deterministic under `go test -race`; production crash dump matches)
- Risk score: 8.7 (D=8, I=10, F=6, R=8, DR=7)

# Detection method
- Tool: Go race detector (`go test -race ./internal/session/...`)
- Reproducibility: 100/100 trials under -race; ~1/10000 requests in production (matches crash logs)
- Concurrency model: goroutine (one per HTTP request via net/http)
- Synchronization primitives involved: `sync.RWMutex` (sessionMu), shared `map[string]*Session` (sessions)

# Root cause
`SessionStore.Touch(id)` updates `s.sessions[id].LastSeen = time.Now()` without
acquiring `sessionMu`. The author intended this as a "fast path" for hot
sessions, but the underlying map and the *Session struct are both shared.
Concurrent `SetUser()` calls (which hold the write lock and may rehash the
map on insert) race with the unguarded write in `Touch()`, producing the
classic "fatal error: concurrent map writes" panic.

Location: `internal/session/store.go:142` in `Touch()`

# Evidence
Bad code:
```
func (s *SessionStore) Touch(id string) {
    // fast path: no lock — assumes session already exists
    if sess, ok := s.sessions[id]; ok {
        sess.LastSeen = time.Now()
    }
}

func (s *SessionStore) SetUser(id string, u *User) {
    s.sessionMu.Lock()
    defer s.sessionMu.Unlock()
    s.sessions[id] = &Session{User: u, LastSeen: time.Now()}
}
```

Detector output:
```
WARNING: DATA RACE
Write at 0x00c000123450 by goroutine 47:
  internal/session.(*SessionStore).Touch
      internal/session/store.go:144 +0x6c
Previous write at 0x00c000123450 by goroutine 23:
  internal/session.(*SessionStore).SetUser
      internal/session/store.go:158 +0x84
```

# Recommended fix
Approach: Acquire `sessionMu.RLock()` to safely read the map, then upgrade to
the per-session lock for the `LastSeen` write. Add a per-`Session` mutex
(or use `atomic.Pointer[time.Time]`) so `Touch` does not block on the global
write lock and stays cheap on the hot path.

Files to modify:
- internal/session/store.go — guard map read in `Touch` with `RLock`; protect
  `LastSeen` write with per-session primitive
- internal/session/session.go — add `lastSeen atomic.Int64` (UnixNano)
  replacing `LastSeen time.Time`; expose `Session.Touch()` and `Session.LastSeenAt()`
- internal/session/store_test.go — add `-race`-clean concurrent stress test

Synchronization plan:
- `SessionStore.sessionMu`: `sync.RWMutex` — readers (`Touch`, `Get`) take RLock;
  writers (`SetUser`, `Delete`) take Lock
- Per-session `lastSeen`: `atomic.Int64` storing UnixNano — no lock needed,
  scales linearly with cores
- Lock acquisition order (when both are held): `sessionMu` always before any
  per-session lock; never the reverse

Constraints:
- `Touch` is on the hot request path — must remain allocation-free and lock-free
  on success
- Public API of `SessionStore` must remain stable (`Touch`, `SetUser`, `Get`, `Delete`)
- `Session.LastSeen` field rename requires updating two callers in
  `internal/api/middleware.go` (verified)

# Acceptance criteria
- [ ] `go test -race ./internal/session/...` reports 0 races (was 100/100)
- [ ] New stress test (`TestStore_TouchSetUserRace`) runs 1000 parallel
      goroutines for 5s under `-race` with 0 panics
- [ ] No p99 latency regression > 5% on `/api/session/touch` benchmark
      (`go test -bench=BenchmarkTouch`)
- [ ] Pool / heap counters unchanged after 10-min soak (no leak introduced
      by the new atomic)
- [ ] No new test failures in `internal/session/` or `internal/api/`

# Ruled-out alternatives (do not revisit)
- Wrap `Touch` in `sessionMu.Lock()` (full write lock) — eliminated:
  benchmarked at 4.2x latency increase under 100-goroutine contention; defeats
  the point of having a fast path
- Replace `map[string]*Session` with `sync.Map` — eliminated: `sync.Map` is
  optimized for write-once / read-many; this workload has frequent
  per-session updates, where `sync.Map` is measurably slower than
  `RWMutex + map` (per Go stdlib godoc)
- Drop `Touch` entirely and update LastSeen on every read — eliminated:
  inflates write traffic ~10x for an analytics-only field

# What NOT to do
- Do not silence the symptom by recovering from the panic in middleware
  (catch-and-ignore the "concurrent map writes" runtime error)
- Do not "fix" by adding `time.Sleep` or retry loops around `Touch`
- Do not disable `-race` in CI to make tests green
- Do not widen `sessionMu` to a global service-wide mutex — keep scope to
  the `SessionStore`
- Do not bundle unrelated session changes (cookie format, expiry policy)
  into this PR
- Do not expand scope beyond `internal/session/` and the two cited callers

# Suggested tests (for Radar)
- Stress: 1000 parallel goroutines, mix of 70% Touch / 20% Get / 10% SetUser,
  5s duration, run under `-race`
- Soak: 30-minute run with pprof heap snapshots every 5 min — confirm no
  goroutine or heap growth from the new atomic
- Negative: deliberately violate lock order in a test to confirm the race
  detector still catches it (defends against future regressions)
```
````

This prompt is self-contained: a coding LLM can act on it without seeing the rest of the Specter ghost report.
