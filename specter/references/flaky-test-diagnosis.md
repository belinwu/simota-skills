# Flaky Test Diagnosis Reference

Purpose: Diagnose and tame intermittent test failures by root-cause category instead of blanket retries. Flakiness is a symptom — Specter categorizes the cause (async / ordering / state / external), recommends quarantine + retry-with-record strategy, and verifies test isolation so genuine concurrency bugs are not masked by CI retry policies.

## Scope Boundary

- **Specter `flaky`**: Intermittent-test root-cause categorization, quarantine policy, retry-with-record design, CI rerun signal detection, test-isolation verification.
- **Probe**: Type / contract / static-analysis issues that *appear* flaky (serialization drift, nullable field assumptions, schema mismatch across environments). If the failure is deterministic once the type is fixed, route to Probe.
- **Sentinel (resource perf)**: Performance-regression flakes where timeouts fire due to slow queries, cache miss storms, or CPU throttling. If wall-clock exceeds budget but logic is correct, route to Sentinel.
- **Forge**: Prototype code where flakiness is expected and ignored; Specter does not hunt flakes in throwaway PoCs.

If the test fails under TSan but not otherwise → real race, stay in `race`. If it fails only in CI and never locally → stay in `flaky` and investigate parallelism / resource contention / ordering.

## Root-Cause Categories

| Category | Signal | Common source | Fix direction |
|----------|--------|---------------|---------------|
| `async` | `setTimeout` / `sleep` waits; `expect` before promise settles | Missing `await`, implicit microtask ordering | Await the actual condition; use `waitFor` with explicit predicate |
| `ordering` | Passes alone, fails in suite; depends on file-sort order | Shared module state, test interdependence | Isolate per-test state; randomize order to expose |
| `state` | First run passes, rerun fails | DB / filesystem / singleton not reset | Transaction rollback, tmpdir per test, fresh DI container |
| `external` | Fails on flaky network / 3rd-party API / clock | Real HTTP, real time, real FS | Mock boundary; record-replay; freeze clock |

Rule: never retry a test before the category is identified. A blind retry masks `ordering` and `state` flakes that indicate real production bugs.

## Workflow

```
TRIAGE  →  collect last N CI reruns; compute pass-rate per test
        →  bucket into 4 categories above via log pattern match
        →  generate 3 hypotheses for the top offender

SCAN    →  async:    grep for setTimeout / sleep / implicit await gaps
        →  ordering: run suite in --random / --shuffle mode
        →  state:    diff DB / fs / globals before and after each test
        →  external: list network + clock + random calls, verify mocks

ANALYZE →  reproduce locally with same seed and order
        →  if fails ≥ 3/10: quarantine + open ticket with category tag
        →  if fails 1-2/10: retry-with-record (capture full state)

SCORE   →  Impact = breakage × CI cost; Detectability = reproduction rate
        →  flaky masking a race = CRITICAL, flaky timer = MEDIUM

REPORT  →  category, evidence, Bad→Good, quarantine decision, Radar tests
```

## Retry-with-Record Pattern

Blind retries hide the cause. Retry-with-record captures state on every attempt so the failed run is debuggable.

```ts
// Bad: blind retry hides real races
test.retry(3)('creates user', async () => { ... });

// Good: retry with recording
test('creates user', async () => {
  const attempt = getAttemptNumber();
  try {
    await runTest();
  } catch (err) {
    await captureArtifact({
      attempt,
      dbSnapshot: await db.dump(),
      timeline: getEventTimeline(),
      seed: getRandomSeed(),
    });
    throw err;
  }
});
```

Every retry must produce an artifact. No artifact = no retry budget next cycle.

## Quarantine Policy

| Pass rate | Action |
|-----------|--------|
| ≥ 99% | Keep in main suite; category-tag and watch |
| 95-99% | Quarantine to `@flaky` tag; run separately; block on 3 consecutive fails |
| < 95% | Quarantine + open P2 ticket; Builder fixes within sprint |
| < 80% | Disable; open P1; never ignore — this often masks a production race |

Quarantine is temporary. Each quarantined test needs an exit criterion (fix or delete) within 30 days, or it becomes permanently disabled and drops coverage silently.

## Test Isolation Verification

Run these three checks — they catch most `ordering` and `state` flakes in one pass.

```bash
# 1. Random order: exposes hidden inter-test dependencies
jest --randomize
pytest -p random_order --random-order

# 2. Run each test alone: exposes shared-state reliance
jest --runInBand --testPathPattern=<file>
pytest --forked

# 3. Run twice in same process: exposes non-reset singletons
jest --testRunner=custom-double-runner
```

If the same test passes alone, fails in suite, and passes again after a clean module cache → `state` category, not `async`.

## CI Rerun-Detection Signals

GitHub Actions / CircleCI / Buildkite all expose rerun metadata. Use it.

- `GITHUB_RUN_ATTEMPT > 1` → the previous attempt failed; record why.
- Historical CI data → compute per-test pass-rate. Any test passing only after retry is a flake candidate.
- If a PR merges only after 3+ reruns, the merged commit carries hidden flakes into main — flag to Scout for regression bisect.

## Anti-Patterns

- Adding `test.retry(N)` without categorizing the cause — hides real races and state bugs.
- Increasing timeouts until the test passes — converts `async` flakes into latent perf regressions.
- Using `sleep(ms)` instead of `waitFor(condition)` — brittle to CI load variance.
- Sharing a single in-memory DB across parallel tests — the classic `ordering` + `state` hybrid flake.
- Skipping tests instead of quarantining them — coverage silently drops, regressions land.
- Treating Jest / Vitest random order as noise — random order is the cheapest isolation verifier available.
- Retrying on CI but not locally — creates ghost failures only post-merge, when they are most expensive.

## Handoff

**To Builder** (when fix is code):
- Category label (`async` / `ordering` / `state` / `external`).
- Reproduction: exact seed, order, env. Reproduction rate observed.
- Bad → Good snippet (await fix, isolation fix, mock at boundary).
- Whether a production code path is implicated (state/ordering flakes often are).

**To Radar** (when fix is test infra):
- Suggested test-isolation harness (transaction rollback, per-test tmpdir, DI reset).
- Record-replay setup for `external` flakes.
- Random-order CI job spec.

**To Scout** (when the flake masks a real bug):
- Production code regions touched by the failing assertion.
- Timeline of when flake rate rose — often correlates with a feature merge.
