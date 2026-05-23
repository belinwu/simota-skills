# Flake and Trend Analysis

**Purpose:** Flake rate computation, FLAKE-CLUSTER detection, and regression timeline analytics.
**Read when:** You are running the `flake` or `timeline` Recipes.

> **2025-2026 Update — Six rules to apply:**
>
> 1. **Wilson score lower-bound** is the consensus statistical method for flake rate (Wilson 95% CI lower bound). Use the lower bound, not the raw rate, to avoid over-quarantining at small `n`.
> 2. **Confidence floor: ≥10 historical runs/test** (Trunk 2025). Below floor, declare LOW-CONFIDENCE — do not classify.
> 3. **Infra-failure mask:** drop runs where >80% of tests failed in that run (likely infra/DNS/auth incident, not test flake). Trunk 2025 standard pre-processing step.
> 4. **Quarantine SLA: 14 days** (Microsoft policy → 18% flakiness reduction in 6 months). Past SLA → disable or delete. Quarantine without SLA = debt accumulator.
> 5. **E-Divisive Means** is the de-facto change-point algorithm for CI perf and pass-rate regression (MongoDB-origin, ICPE). PELT and BOCPD are also viable alternatives (2025 PELT: ACMCISIA 2025; BOCPD: ACMCSMT 2025). For pass-rate timelines E-Divisive remains preferred; for real-time online detection BOCPD (hazard rate λ=100) outperforms GLR and K-S tests.
> 6. **Bayesian flake scoring** (beyond Wilson lower-bound): high-maturity teams use a Beta-Binomial prior updated per run. The posterior gives a probability distribution over true flake rate, not just a point estimate. Use Bayesian posterior mean when n<30 and Wilson interval is too wide to be actionable.
>
> **Tag taxonomy** (Datadog 2025 standard): `is_flaky`, `is_new_flaky`, `is_known_flaky` — adopt these labels in Vista output for cross-platform compatibility. Datadog Early Flake Detection runs new tests multiple times before merge and identifies ~75% of flakies. Source: https://docs.datadoghq.com/tests/flaky_test_management/early_flake_detection/
>
> **Buildkite Test Engine** (2025) monitors: *transition count*, *passed on retry*, *probabilistic flakiness* — all three can be surfaced in Vista's flake dashboard as platform-native signals. Source: https://buildkite.com/resources/blog/introducing-test-engine-workflows/
>
> **AI-assisted flake fix:** Datadog Bits AI Dev Agent and FlakyGuard (ASE 2025; 47.6% repair rate, 51.8% accepted, 22%+ over prior SOTA) auto-PR fixes for flaky tests. Vista can hand off quarantine candidates to such agents (but Vista itself does not write fixes). Source: https://arxiv.org/abs/2511.14002
>
> **FlakeSync** (ICSE 2024): auto-repairs async-flaky tests; complements FlakyGuard for async/timing root causes. Source: https://dl.acm.org/doi/10.1145/3597503.3639115

## Contents
- Flake Rate Definition
- Sample Size Requirements
- Quarantine Candidate Selection
- FLAKE-CLUSTER Detection
- Failure Cluster Analysis
- Regression Timeline Construction
- Regression Detection
- Output Annotations

---

## Flake Rate Definition

A test is **flaky** when it produces different outcomes for the same code (same SHA) across runs.

### Per-test flake rate

```
flake_rate(test) = (failed_runs_followed_by_pass + passed_runs_after_retry) / total_runs
```

Where:
- `failed_runs_followed_by_pass`: same test, same SHA, ran multiple times — failed at least once and passed at least once.
- `passed_runs_after_retry`: Playwright/Cypress retry counted (status=passed, retry>0).

### Threshold (apply to **Wilson 95% lower-bound**, not raw rate)

| Flake rate (Wilson lower) | Classification | Action |
|------------|---------------|--------|
| <1% | STABLE | none |
| 1-5% | WATCH | monitor; no action |
| 5-15% | QUARANTINE-CANDIDATE | recommend Radar `flake_quarantine` |
| ≥15% | URGENT-QUARANTINE | recommend immediate Radar action; mark blocking |

### Wilson 95% lower-bound formula

For `k` failures in `n` runs (with `p = k/n`, `z = 1.96`):

```
Wilson_lower = (p + z²/(2n) − z·sqrt(p(1−p)/n + z²/(4n²))) / (1 + z²/n)
```

Use `Wilson_lower` for classification; print both raw `p` and Wilson interval in the dashboard so reviewers can see the confidence band.

### Pre-processing (Trunk 2025)

Before computing per-test flake rate:
1. Load runs in time window.
2. **Drop runs where `(failed_tests / total_tests_in_run) > 0.80`** — these are likely infra incidents, not test flakes.
3. Require `n ≥ 10` per test post-mask. Below floor → emit `LOW-CONFIDENCE` and skip classification.

### Quarantine SLA

- Standard SLA: **14 days** from quarantine date (Microsoft 2024 standard, Trunk 2025 default).
- Past SLA without fix → recommend disable or delete.
- Surface `days_in_quarantine` and `days_to_breach` in flake dashboard timeline.

---

## Sample Size Requirements

Vista refuses to compute flake metrics with insufficient data.

| Recipe | Minimum Runs | Minimum Window |
|--------|--------------|---------------|
| `flake` (per-test) | 30 runs | 7 days |
| `flake` (per-suite) | 50 runs | 7 days |
| `timeline` (regression) | 20 runs | 14 days |
| Per-test flake confidence | 30 runs | — |

When below threshold, emit a `LOW-CONFIDENCE` warning in `Limitations` and present results with explicit `n=<count>` annotation. Do not compute aggregated flake rates with n<10 — refuse and report.

### Statistical note

For n<100, prefer Wilson score interval over raw percentage when reporting confidence. Show both: `flake = 8% (Wilson 95%: 4-14%)`.

For n<30 where the Wilson interval is too wide, supplement with the **Beta-Binomial posterior**: initialize a Beta(1,1) (uniform) prior; after observing `k` failures in `n` runs, the posterior is Beta(k+1, n-k+1) with mean `(k+1)/(n+2)` and credible interval computable via `scipy.stats.beta.interval(0.95, k+1, n-k+1)`. Report: `flake ~ 12% (Beta posterior 95% CI: 3-28%, n=18)`. Avoid hard classification below n=10 regardless of method.

---

## Quarantine Candidate Selection

Output a ranked list:

```yaml
quarantine_candidates:
  - test_id: "payments.charge#refund_partial"
    flake_rate: 0.18
    sample_size: 47
    confidence: "Wilson 95%: 9-32%"
    last_failures: 5
    common_failure_signature: "TimeoutError: waiting for locator '#confirm'"
    recommendation: "URGENT-QUARANTINE; hand off to Radar with quarantine + root-cause investigation"
  - test_id: "auth.session#expiry_renewal"
    flake_rate: 0.07
    sample_size: 60
    confidence: "Wilson 95%: 2-15%"
    last_failures: 3
    common_failure_signature: "Network timeout on /auth/refresh"
    recommendation: "QUARANTINE-CANDIDATE; hand off to Radar"
```

Always pair flake_rate with sample_size and confidence interval.

---

## FLAKE-CLUSTER Detection

When ≥3 tests share the same failure signature, they form a cluster — usually pointing to a shared root cause (network, timing, fixture).

### Cluster definition

Group by:
1. Same `failure.type` (TimeoutError, NetworkError, AssertionError)
2. First 3 stack frames identical (after symbolication and path normalization)
3. Same time window (within 4 hours)

### Detection rule

```yaml
FLAKE_CLUSTER:
  signals_required: 2
  signals:
    - tests_in_cluster: ">= 3"
    - shared_first_3_stack_frames: true
    - common_time_window: "<= 4h"
    - distinct_files: ">= 2"  # rules out single-test repeated flake
```

### Output

```yaml
finding:
  id: FLAKE-CLUSTER
  summary: "5 tests fail with shared signature 'TimeoutError @ getByRole(\"button\", { name: /confirm/i })'"
  signals: [tests=5, distinct_files=4, time_window=2h]
  affected_tests:
    - "checkout.spec.ts:submit"
    - "refund.spec.ts:confirm"
    - "subscribe.spec.ts:upgrade"
    - "cart.spec.ts:checkout"
    - "billing.spec.ts:upgrade_plan"
  recommendation: "Likely shared root cause (locator strategy or shared fixture). Hand off to Scout for root-cause investigation."
```

---

## Failure Cluster Analysis

For non-flaky failures (consistent fail across runs), still cluster by signature for review readability.

| Cluster Threshold | Action |
|-------------------|--------|
| ≥3 occurrences in window | Cluster as FAILURE-CLUSTER, recommend Scout |
| 1-2 occurrences | List individually, no cluster |

---

## Regression Timeline Construction

For the `timeline` Recipe.

### Required input

- Per-run outcome: pass / fail / flake / skip / error
- Per-run commit SHA (for git correlation)
- Per-run timestamp

### Per-test timeline

```yaml
test_id: "payments.charge#full_refund"
window: 30 days
runs: 47
outcomes:
  - run: 142
    sha: a1b2c3d
    date: 2026-04-01
    outcome: pass
    duration_ms: 1240
  - run: 144
    sha: a1b2c3d  # same SHA, different run = potential flake
    date: 2026-04-01
    outcome: fail
    duration_ms: 30000  # timeout
    retry: 0
```

### Aggregate per-day pass rate

```
pass_rate(day) = passed_runs / total_runs(day)
```

Render as XY chart (see `visualization-patterns.md`).

---

## Regression Detection

A test is in **regression** when its rolling pass rate degrades.

### Detection rule

```yaml
REGRESSION:
  window_a: "last 7 days"
  window_b: "previous 7 days (8-14 days ago)"
  signal: "pass_rate(window_a) - pass_rate(window_b) <= -0.10"
  minimum_runs_per_window: 10
```

When matched, emit:

```yaml
finding:
  id: REGRESSION
  test_id: "payments.charge#full_refund"
  pass_rate_recent: 0.72
  pass_rate_baseline: 0.95
  delta: -0.23
  first_failure_sha: <sha>
  first_failure_pr: "#4521"
  recommendation: "Hand off to Trail for git-history bisection + Scout for root cause"
```

### Change-point algorithm selection

| Algorithm | When to use | Notes |
|-----------|-------------|-------|
| **E-Divisive** | Batch analysis over full history; exact commit pinpointing | MongoDB-origin (ICPE); preferred for pass-rate regression |
| **PELT** | Larger datasets where E-Divisive is slow; O(n) amortized | Exact linear time; 2025 empirical evidence on S&P/CSI 300 time series confirms robustness (ACM CISIA 2025) |
| **BOCPD** | Online / real-time streams where new runs arrive continuously | hazard rate λ=100 outperforms GLR and K-S (ACM CSMT 2025); good for live dashboards |

When git SHA correlation is available, prefer E-Divisive to pinpoint the exact breaking commit. When processing a live stream (e.g., webhook-driven dashboard), use BOCPD.

### Linking to commits

When `first_failure_sha` is identifiable (first failure that breaks the trend), surface:
- The commit message (first line)
- The PR number (if discoverable from `gh pr list --search <sha>`)
- The author (if available)

---

## Output Annotations

```yaml
Source:
  artifacts:
    - "GitHub Actions runs #110-#157 (workflow: test.yml)"
  time_window: "2026-03-30..2026-04-28 (30 days)"
  parser_versions: [junit-xml-v5, playwright-1.49+]
Sample_Size:
  runs: 47
  tests_observed: 312
  total_test_executions: 14640
Findings:
  - id: FLAKE-CLUSTER | REGRESSION | URGENT-QUARANTINE | LOW-CONFIDENCE
    summary: <one line>
    signals: [...]
Quarantine_Candidates:
  - test_id: ...
    flake_rate: 0.18 (Wilson 95%: 9-32%)
    recommendation: ...
Regressions:
  - test_id: ...
    delta_pass_rate: -0.23
    first_failure_sha: ...
Limitations:
  - "12 of 47 runs missing junit.xml artifact; flake rates computed on n=35"
  - "Commit SHA correlation unavailable for 5 runs (CI configuration drift)"
```
