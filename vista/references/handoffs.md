# Handoff Templates

**Purpose:** Standardized handoff payloads for incoming and outgoing collaborators.
**Read when:** You are at DELIVER phase and need to format a handoff to/from another agent.

## Contents
- Inbound Handoffs (Vista receives)
- Outbound Handoffs (Vista sends)
- Field Conventions
- Examples

---

## Inbound Handoffs (Vista receives)

### `RADAR_TO_VISTA_HANDOFF`

```yaml
RADAR_TO_VISTA_HANDOFF:
  source: Radar
  recipe_request: coverage | results | flake | report
  artifacts:
    junit_xml: <path>
    coverage:
      lcov: <path>
      jest_json: <path>
    runs_window: <YYYY-MM-DD..YYYY-MM-DD>
  scope:
    paths: [<glob>]
    languages: [<js | ts | py | go | rust | java>]
  audience: engineer | qa | pm | exec
  thresholds:
    line_pct: 80
    branch_pct: 70
    flake_rate: 0.05
  context: <one-paragraph why visualization is needed>
```

### `VOYAGER_TO_VISTA_HANDOFF`

```yaml
VOYAGER_TO_VISTA_HANDOFF:
  source: Voyager
  recipe_request: results | journey | flake | timeline
  artifacts:
    playwright_report: <path>
    junit_xml: <path>
    traces_dir: <path>
    runs_window: <YYYY-MM-DD..YYYY-MM-DD>
  user_journey_source: <path or "echo:journey-id">
  audience: engineer | qa | pm
```

### `SIEGE_TO_VISTA_HANDOFF`

```yaml
SIEGE_TO_VISTA_HANDOFF:
  source: Siege
  recipe_request: results | timeline
  artifacts:
    load_results: <path>
    chaos_results: <path>
    mutation_results: <path>
  metric_focus: latency_p95 | error_rate | mutation_score
```

### `JUDGE_TO_VISTA_REQUEST`

```yaml
JUDGE_TO_VISTA_REQUEST:
  source: Judge
  recipe_request: diff | flake
  pr:
    base_sha: <sha>
    head_sha: <sha>
    pr_number: <n>
  required_evidence:
    - coverage_delta
    - flake_rate_delta
    - new_test_count
  format: pr_comment_markdown
```

### `ATTEST_TO_VISTA_HANDOFF`

```yaml
ATTEST_TO_VISTA_HANDOFF:
  source: Attest
  recipe_request: trace
  spec_source:
    type: markdown_frontmatter | gherkin | jira_export
    path: <path or url>
  required_columns: [req_id, description, criticality, ac_id]
  audience: compliance | qa | exec
```

### `MATRIX_TO_VISTA_HANDOFF`

```yaml
MATRIX_TO_VISTA_HANDOFF:
  source: Matrix
  recipe_request: coverage
  planned_combinations: <path to plan>
  actual_results: <path to junit/allure>
  axes: [<axis_1>, <axis_2>, ...]
```

---

## Outbound Handoffs (Vista sends)

### `VISTA_TO_RADAR_HANDOFF`

```yaml
VISTA_TO_RADAR_HANDOFF:
  source: Vista
  reason: coverage_gap | flake_quarantine | regression
  visualizations:
    - path: docs/test-vis/coverage/2026-04-28/payments.md
      finding: COVERAGE-DESERT
  prioritized_targets:
    - file: src/payments/refund.ts
      risk_score: 78
      uncovered_branches: [3, 7, 12]
      recommended_action: "Add edge-case tests for partial refund failure path"
    - file: src/billing/invoice.ts
      risk_score: 65
      uncovered_branches: [22, 24]
      recommended_action: "Add regression tests for tax line items"
  flake_quarantine_list:
    - test_id: "payments.charge#refund_partial"
      flake_rate: 0.18
      sample_size: 47
      common_failure: "TimeoutError @ getByRole(button, name=/confirm/i)"
      recommended_action: "Quarantine + investigate locator strategy"
  thresholds_used:
    line_pct: 80
    branch_pct: 70
    flake_rate: 0.05
  audience: engineer
```

### `VISTA_TO_VOYAGER_HANDOFF`

```yaml
VISTA_TO_VOYAGER_HANDOFF:
  source: Vista
  reason: e2e_journey_gap
  uncovered_steps:
    - journey_id: checkout
      step: "Enter shipping"
      criticality: high
      recommended_test: "e2e/checkout.spec.ts:enterShipping"
  flaky_e2e:
    - test_id: "e2e/checkout.spec.ts:payment"
      flake_rate: 0.08
      recommended_action: "Stabilize via deterministic fixture"
```

### `VISTA_TO_JUDGE_HANDOFF`

```yaml
VISTA_TO_JUDGE_HANDOFF:
  source: Vista
  reason: review_evidence
  pr_number: <n>
  evidence:
    coverage_delta:
      line_pct: +2.5
      branch_pct: -1.2  # WARN
    new_tests: 8
    flake_introduced: 0
    visualizations:
      - path: docs/test-vis/diff/2026-04-28/pr-4521.md
  verdict_signals:
    - "branch coverage decreased by 1.2pp; verify new untested branches"
    - "flake rate unchanged"
    - "8 new tests added, all passing"
```

### `VISTA_TO_PULSE_HANDOFF`

```yaml
VISTA_TO_PULSE_HANDOFF:
  source: Vista
  reason: test_quality_kpi
  metrics:
    line_coverage_global: 78.5
    branch_coverage_global: 64.0
    flake_rate_global: 0.04
    test_pyramid:
      unit: 70
      integration: 22
      e2e: 8
    requirements_coverage_pct: 77
  trend_window: 30d
  recommendation: "Surface in product quality dashboard alongside churn and incident metrics"
```

### `VISTA_TO_CANVAS_HANDOFF`

```yaml
VISTA_TO_CANVAS_HANDOFF:
  source: Vista
  reason: generic_diagram_request
  context: <user asked for a non-test diagram during a Vista session>
  request_summary: <one line>
  forwarded_input: <original user request>
```

### `VISTA_TO_SHERPA_HANDOFF`

```yaml
VISTA_TO_SHERPA_HANDOFF:
  source: Vista
  reason: flake_remediation_backlog
  backlog_items:
    - test_id: "payments.charge#refund_partial"
      effort_estimate: medium
      blocking: false
    - test_id: "auth.session#expiry_renewal"
      effort_estimate: small
      blocking: false
    - test_id: "billing.invoice#monthly_aggregate"
      effort_estimate: large
      blocking: true
  decomposition_request: "Break into atomic ≤15min steps prioritized by blocking + criticality"
```

---

## Field Conventions

| Field | Convention |
|-------|------------|
| `source` | Always the agent name in canonical case |
| `recipe_request` | Match Vista subcommand names exactly |
| `artifacts` | Absolute or repo-relative paths |
| `runs_window` | ISO-8601 date range |
| `time_window` | Same as runs_window or `Nd`-style shorthand |
| `audience` | engineer / qa / pm / exec / compliance |
| `thresholds` | Always declare line / branch / flake when computing classifications |
| `risk_score` | 0-100 integer; see `coverage-analytics.md` for formula |
| `confidence` | "Wilson 95%: low-high%" format for flake metrics |

Vista refuses to act on incoming handoffs missing `artifacts`. If the caller asks for a recipe but provides no artifact path, Vista responds with a structured `MISSING_ARTIFACT` error and lists the expected paths.

---

## Examples

### Example 1: Inbound from Radar (coverage Recipe)

```yaml
RADAR_TO_VISTA_HANDOFF:
  source: Radar
  recipe_request: coverage
  artifacts:
    coverage:
      lcov: coverage/lcov.info
    runs_window: "2026-04-28..2026-04-28"
  scope:
    paths: ["src/**"]
    languages: [ts]
  audience: engineer
  thresholds:
    line_pct: 80
    branch_pct: 70
  context: "Sprint 24 wrap-up; flagged regression in branch coverage during retro"
```

### Example 2: Outbound to Radar (gap → new tests)

```yaml
VISTA_TO_RADAR_HANDOFF:
  source: Vista
  reason: coverage_gap
  visualizations:
    - path: docs/test-vis/coverage/2026-04-28/sprint-24-treemap.md
      finding: COVERAGE-DESERT
  prioritized_targets:
    - file: src/billing/invoice.ts
      risk_score: 82
      uncovered_branches: [44, 51, 58]
      recommended_action: "Add edge-case tests for proration on mid-cycle plan changes"
  thresholds_used:
    line_pct: 80
    branch_pct: 70
  audience: engineer
```
