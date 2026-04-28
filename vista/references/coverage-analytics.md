# Coverage Analytics

**Purpose:** Coverage math, risk weighting, and gap detection rules.
**Read when:** You are at MAP/ANNOTATE phase computing coverage metrics or detecting gaps.

> **2025-2026 Update — Three shifts to apply:**
>
> 1. **Diff coverage > total coverage as PR gate.** Russ Cox (research.swtch.com/diffcover), `diff-cover`, Codacy, and Codecov 2025 standardize "lines you touched should be covered" — typically ≥80% diff coverage — over chasing total coverage. Demote total coverage to a trend sparkline.
> 2. **Mutation overlay catches vanity coverage.** Stryker incremental mode runs PR-time mutation in 1-5 minutes. Meta's ACH (FSE 2025) uses LLMs for fault-class mutants and equivalent-mutant detection. AI-generated code shows 15-25% lower mutation kill rates at equal line coverage. Vista flags `100% line / <60% mutation` as `LINE-NOT-MUTATION` vanity zones.
> 3. **MC/DC is leaving avionics.** GCC 14 added masking MC/DC; arXiv 2501.02133 extends to Rust. ISO 26262 ASIL D, EN 50128, IEC 62304, NASA still require MC/DC, but more mainstream tooling now supports it. Surface MC/DC view when criticality=high.
>
> **Risk-weighted coverage** (Lighthouse pattern, blog 2025-09-02): blend `(1 - branch_pct) × git_churn × incident_count` to produce HIGH/MED/LOW per file. This replaces flat coverage thresholds with operational risk.

## Contents
- Coverage Type Definitions
- Per-File Aggregation
- Per-Directory Roll-up
- Risk Weighting
- COVERAGE-DESERT Detection
- PR Coverage Diff
- Coverage Quality Anti-Patterns
- Output Annotations

---

## Coverage Type Definitions

| Type | Definition | When to Trust |
|------|-----------|----------------|
| Line | % of source lines executed at least once | Quick triage; misleading for complex conditions |
| Statement | % of statement nodes executed | More precise than line for compound expressions |
| Branch | % of conditional branch outcomes (true AND false) executed | Best signal for logic correctness |
| Function | % of functions called at least once | Useful for dead-code detection |
| Condition / MC/DC | Each condition independently affecting outcome | Safety-critical (DO-178C, ISO 26262) |

**Always render branch and line separately.** Common pitfall: "100% line coverage" with 40% branch coverage means half of conditional logic is untested.

---

## Per-File Aggregation

For each source file, Vista produces:

```yaml
file: src/payments/charge.ts
metrics:
  lines:
    covered: 42
    total: 60
    pct: 70.0
  branches:
    covered: 8
    total: 16
    pct: 50.0
  statements:
    covered: 45
    total: 65
    pct: 69.2
  functions:
    covered: 5
    total: 7
    pct: 71.4
recency:
  last_modified: 2026-04-15
  days_since_change: 13
  commits_30d: 7
criticality:
  user_marked: high  # from .vista/criticality.yaml or path-based heuristic
  path_signal: payments  # high-risk path keyword match
risk_score: 78  # see Risk Weighting below
```

---

## Per-Directory Roll-up

When a directory contains multiple files:

```
total_lines = Σ file.lines.total
covered_lines = Σ file.lines.covered
dir.line_pct = covered_lines / total_lines × 100
```

Do **not** average per-file percentages — that biases small files. Always use line-weighted aggregation.

---

## Risk Weighting

Coverage gaps are not equal. Weight by recency, criticality, and exposure.

### Formula

```
risk_score = (100 - branch_pct)
           × recency_weight
           × criticality_weight
           × exposure_weight
```

### Recency weight

| Days since last change | Weight |
|------------------------|--------|
| 0-7 | 1.5 |
| 8-30 | 1.2 |
| 31-90 | 1.0 |
| 91-365 | 0.7 |
| 366+ | 0.4 |

### Criticality weight

Sources, in priority order:
1. User-provided `.vista/criticality.yaml` mapping path globs → `high|medium|low`
2. Path keyword match: `payments|auth|billing|security` → high (1.5); `admin|internal` → medium (1.2); else → low (1.0)
3. Default: medium

### Exposure weight

| Signal | Weight |
|--------|--------|
| File has public API export | 1.3 |
| File is referenced by E2E entry path | 1.2 |
| File only consumed internally | 1.0 |
| File is a test fixture / mock | 0.5 |

### Output ordering

Risk-weighted gaps in `Findings` block are sorted descending by `risk_score`. Cap to top 5.

---

## COVERAGE-DESERT Detection

Definition: ≥10 contiguous untested files in a critical directory.

### Detection rule

```yaml
COVERAGE_DESERT:
  signals_required: 2
  signals:
    - contiguous_untested_files: ">= 10"
    - directory_criticality: "high or medium"
    - branch_pct: "< 30 across the directory"
    - days_since_any_test_in_dir: "> 90"
```

When ≥2 signals match, emit:

```yaml
finding:
  id: COVERAGE-DESERT
  summary: "src/billing/ has 14 contiguous files at <20% branch coverage"
  signals: [contiguous_untested_files=14, directory_criticality=high, branch_pct=18]
  recommendation: "Hand off to Radar for targeted test addition; suggested entry point: src/billing/invoice.ts (highest risk_score)"
```

---

## PR Coverage Diff

For the `diff` Recipe, compute base vs head:

```yaml
diff:
  base:
    sha: <base_sha>
    coverage:
      line_pct: 78.0
      branch_pct: 64.0
  head:
    sha: <head_sha>
    coverage:
      line_pct: 80.5
      branch_pct: 66.5
  delta:
    line_pct: +2.5
    branch_pct: +2.5
files_added:
  - path: src/payments/refund.ts
    line_pct: 92  # new file
files_decreased:
  - path: src/auth/session.ts
    line_pct_before: 88
    line_pct_after: 84
    delta: -4
    reason: "new untested branch added at line 47"
```

### PR signal classification

| Δ line | Δ branch | Classification |
|--------|----------|---------------|
| ≥0 | ≥0 | IMPROVE |
| ≥0 | <0 | LINE-ONLY (warn — likely added uncovered branches) |
| <0 | ≥0 | UNUSUAL (verify — sometimes refactor removes dead code) |
| <0 | <0 | REGRESS |

---

## Coverage Quality Anti-Patterns

Surface in `Findings` when matched:

| ID | Signal | Diagnosis |
|----|--------|-----------|
| `LINE-NOT-BRANCH` | line_pct − branch_pct ≥ 30 percentage points | Tests touch lines but skip branches. Mutation testing recommended. |
| `LINE-NOT-MUTATION` (2025) | 100% line coverage AND mutation kill rate < 60% | Vanity zone — code runs but assertions don't catch regressions. Use Stryker incremental to verify. |
| `COVERAGE-FEVER` (Goodhart 2025) | ≥3 files at exactly 80.0-80.5% (threshold gaming) AND assertion-density mean < 1 | Coverage Fever: chasing numbers. Recommend cutting threshold gates and relying on mutation + diff coverage. |
| `COVERAGE-DESERT` | ≥10 contiguous untested files in critical dir | Entire feature area untested. |
| `STALE-COVERAGE` | global branch_pct unchanged ±1pp over 90 days | Tests not evolving with code. |
| `ASSERT-DESERT` | files at 80%+ line coverage but mutation score <20% (when available) | Tests execute code but assert nothing. |
| `THRESHOLD-GAMING` | many files at exactly the threshold (e.g., 80.1%) | Coverage gating without quality intent. |
| `SETUP-PADDING` | beforeAll/setUp lines counted in coverage but no assertion in tests | Inflated numbers. |
| `MC-DC-MISSING` (2025) | criticality=high AND MC/DC unavailable while branch coverage flagged green | Safety-critical or regulated code (DO-178C / ISO 26262 ASIL D / IEC 62304) needs MC/DC; flat branch coverage misleads. |

---

## Output Annotations

Every coverage visualization includes:

```yaml
Source:
  artifacts:
    - coverage/lcov.info (parser: lcov-1.16, parsed_at: <ISO-8601>)
  time_window: "single run / commit <sha>"
Sample_Size:
  files: 312
  lines_total: 18420
  branches_total: 4882
Findings:
  - id: COVERAGE-DESERT | LINE-NOT-BRANCH | STALE-COVERAGE | ...
    summary: <one line>
    signals: [...]
Risk_Weighted_Gaps:
  - target: src/payments/charge.ts
    risk_score: 78
    reason: "branch=50%, modified 13d ago, criticality=high (payments)"
    recommendation: "Radar: add edge-case tests for refund failure path (lines 42-58, branches 6,7,9)"
Limitations:
  - "Branch coverage requires `coverage run --branch`; 4 files reported branch_pct=0 due to missing flag"
```
