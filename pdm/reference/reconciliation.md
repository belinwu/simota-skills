# Reconciliation Reference

**Purpose:** The plan↔code matching method, status assignment, confidence scoring, and drift detection.
**Read when:** You are at RECONCILE assigning statuses or hunting drift.

## Contents
- Matching Method
- Status Decision Table
- Issue-State Cross-Signal
- Partial Implementation (In-Progress)
- Drift Detection
- Confidence Scoring
- Absence Discipline
- Reconciliation Output

---

## Matching Method

For each planned feature, find its implemented counterpart; then reverse-scan for implemented features with no plan.

```
for each plan_item:
    candidates = code features matching by name / entry point / domain terms
    if strong match:    pair(plan_item, code_evidence)
    if partial match:   pair(plan_item, partial_code_evidence)
    if no match:        pair(plan_item, NONE)   # Not-Started candidate
for each code_feature not yet paired:
    pair(NONE, code_feature)                    # Undocumented candidate
```

Match on behavior and entry points, not just string similarity — a spec "password reset" maps to `POST /auth/reset` even if names differ. Verify, never assume the mapping.

---

## Status Decision Table

| Plan side | Code side | Status |
|-----------|-----------|--------|
| Present | Full implementation + tests | `Done` |
| Present | Partial / flagged-off / stubbed | `In-Progress` |
| Present | None found (after coverage) | `Not-Started` |
| None | Present | `Undocumented` |
| None | None | not a feature — drop |

---

## Issue-State Cross-Signal

When the plan side is an issue tracker, the issue *state* sharpens (but never replaces) the status. A closed issue is an intent signal, not proof of delivery — always require code evidence.

| Issue state | Code side | Reading |
|-------------|-----------|---------|
| Open | none found | `Not-Started` (planned, queued) |
| Open | partial / stub / flag-off | `In-Progress` |
| Closed | full implementation | `Done` — confirm code exists; closed ≠ shipped without code |
| Closed | none found | `Drift: closed-but-absent` — reverted, moved, or closed-as-wontfix; investigate before trusting |
| Reopened | any | `In-Progress` + regression/rework signal (consider Trail for history) |
| Open + linked PR merged | full implementation | `Done` — tracker lag; flag the stale-open as minor drift |

Milestones/labels refine grouping, not status: a `v2` label says *when planned*, not *whether built*.

---

## Partial Implementation (In-Progress)

`In-Progress` requires naming *what is missing*, not just "some code exists":
- entry point present but core logic stubbed/`TODO`
- feature flag exists and is off or default-off
- happy path only; error/edge handling absent per spec
- implemented but no tests for a spec'd behavior

State the missing pieces explicitly so the gap is actionable (handoff to Sherpa/Builder is the user's choice, not PDM's action).

---

## Drift Detection

Drift = plan and code disagree about state. The highest-value finding. Flag, never smooth over.

| Drift type | Symptom | Report as |
|------------|---------|-----------|
| Phantom-shipped | CHANGELOG/roadmap says done; no/partial code | `Drift: claimed-done, evidence-partial` |
| Ghost feature | Code implements it; no plan/spec covers it | `Undocumented` + drift note |
| Stale plan | Spec describes behavior the code has since changed | `Drift: spec-stale` (consider Trail for when) |
| Abandoned | Code stub + open issue, no progress signal | `Drift: stalled` |

---

## Confidence Scoring

| Confidence | Condition |
|-----------|-----------|
| High | Plan text read AND code read/verified for the same scope |
| Medium | One side strong, the other inferred (e.g. issue title + single entry point) |
| Low | Intent-only (roadmap line, no spec detail) OR static-only (code presence, behavior unconfirmed) |

Always downgrade for: dynamic dispatch / flags hiding runtime behavior, generated code presence without behavior confirmation, plan sources that are themselves auto-generated. State the downgrade reason.

---

## Absence Discipline

Inherited from Lens. Declaring `Not-Started` is a positive claim about absence and must state coverage:

> "Not-Started — searched `src/payments/**`, route table, and `gh issue` for 'refund'; no entry point, module, or test found. Coverage: 3 search passes. Confidence: Medium (could exist under different terminology)."

Absence of evidence ≠ evidence of absence. If coverage is shallow (<2 passes or single search term), broaden before declaring, or mark confidence Low.

---

## Reconciliation Output

Feeds REPORT. One row per feature:

```yaml
- feature: "Refund processing"
  area: "Payments"
  status: Not-Started
  confidence: Medium
  plan_ref: "issue #142, ROADMAP.md 'v2 Payments'"
  code_evidence: "none — searched src/payments/**, routes, tests"
  missing: "no refund endpoint or service"
  drift: none
```
