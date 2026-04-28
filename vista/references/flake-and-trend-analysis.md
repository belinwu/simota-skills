# Flake and Trend Analysis

**Purpose:** Flake rate computation, FLAKE-CLUSTER detection, and regression timeline analytics.
**Read when:** You are running the `flake` or `timeline` Recipes.

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

### Threshold

| Flake rate | Classification | Action |
|------------|---------------|--------|
| <1% | STABLE | none |
| 1-5% | WATCH | monitor; no action |
| 5-15% | QUARANTINE-CANDIDATE | recommend Radar `flake_quarantine` |
| ≥15% | URGENT-QUARANTINE | recommend immediate Radar action; mark blocking |

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
