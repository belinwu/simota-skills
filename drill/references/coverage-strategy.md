# Coverage Strategy

How Drill organizes test cases into tiers, builds traceability, and detects coverage gaps.

---

## Test Tier Pyramid (Manual QA)

```
                    /\
                   /UAT\           ~5%  — business sign-off
                  /------\
                 /Regress \        ~25% — full pre-release
                /----------\
               /  Sanity    \      ~30% — daily / per-branch
              /--------------\
             /     Smoke      \    ~40% — every build, ≤15 min
            /------------------\
```

Percentages are case-count, not effort.

| Tier | Purpose | Time-box | Trigger | Membership Rule |
|------|---------|----------|---------|-----------------|
| **Smoke** | "Is the build alive?" | ≤15 min | Every build / PR | P0 happy paths only; one case per critical user journey |
| **Sanity** | "Did the changed area break?" | ≤45 min | Daily / per-branch / per-feature-flag flip | All P0 + impacted P1 cases for the changed module |
| **Regression** | "Did anything else break?" | 4-16 h | Pre-release / weekly | All P0 + all P1 + sampled P2 |
| **UAT** | "Does the business accept it?" | 1-3 days | Pre-GA / contract | Business-critical scenarios only; signed off by product / stakeholders |

---

## Tier Selection Rules

A test case enters a tier by satisfying **all** of the criteria for that tier — not by inheritance from a lower tier.

| Criterion | Smoke | Sanity | Regression | UAT |
|-----------|-------|--------|------------|-----|
| Priority | P0 | P0-P1 | P0-P2 | P0-P1 (business-critical only) |
| Duration | ≤3 min/case | ≤5 min/case | any | any |
| Stable (not flaky) | Required | Required | Required | Required |
| Covers critical user journey | Required | Optional | Optional | Required |
| Includes negative path | No | Yes | Yes | Optional |
| Requires production-like data | No | No | Yes | Yes |
| Requires stakeholder presence | No | No | No | Yes |

A case in Smoke that fails its stability or duration constraint demotes to Sanity. Never silently drop — emit a `DEMOTE` row in the regression curation report.

---

## Traceability Matrix

A bidirectional map between requirements and test cases. Drill emits two views:

### Requirements → Test Cases

| Req ID | Description | TC Count | Smoke | Sanity | Regression | UAT | Status |
|--------|-------------|----------|-------|--------|------------|-----|--------|
| FR-AUTH-12 | Reject expired password | 3 | 1 | 1 | 3 | 0 | COVERED |
| FR-AUTH-13 | Lockout after 5 failures | 4 | 0 | 1 | 4 | 0 | COVERED |
| FR-AUTH-14 | Reset link expires in 1h | 2 | 0 | 0 | 2 | 0 | COVERED |
| FR-AUTH-15 | Magic-link login | 0 | 0 | 0 | 0 | 0 | **GAP** |
| NFR-AUTH-01 | Login p95 ≤500ms | 0 | 0 | 0 | 0 | 0 | OUT_OF_SCOPE (→ Siege) |

### Test Cases → Requirements (for impact analysis)

| TC-ID | Title | Linked Req IDs |
|-------|-------|----------------|
| TC-AUTH-001 | Reject login with expired password | FR-AUTH-12, AC-AUTH-005 |
| TC-AUTH-002 | Reset link expires after 1h | FR-AUTH-14 |

---

## Coverage Gap Severity

Not every gap is equal. Classify each gap:

| Severity | Condition | Action |
|----------|-----------|--------|
| `CRITICAL` | P0 requirement with zero cases | Block delivery; author cases before release |
| `HIGH` | P1 requirement with zero cases | Author before release-candidate |
| `MEDIUM` | Requirement with only happy-path coverage (no negative / boundary) | Author negative case in same sprint |
| `LOW` | Requirement covered by ≥1 case but lacks a specific technique recommended for its shape | Backlog; revisit on regression refresh |
| `OUT_OF_SCOPE` | Requirement is non-functional and routed to another agent (Siege / Sentinel / Voyager-a11y) | Annotate, do not count as gap |

---

## Coverage Anti-Patterns

| Anti-pattern | Why it's bad | Fix |
|--------------|--------------|-----|
| **100% pass rate as a goal** | Suite has no teeth — it's not exercising risk | Mutation testing (route to Radar) or chaos (route to Siege) reveals false confidence |
| **Vanity coverage (100% case-count or 100% line-coverage as the goal)** | Coverage % is a vanity metric — it does not encode risk per case | Report **Risk-Weighted Coverage** (cases × priority × technique-fitness) alongside raw %. [Source: https://medium.com/@yashbatra11111/100-test-coverage-is-useless-heres-what-actually-works-for-quality-software-3e807fd23a03] |
| **Counting cases instead of risks covered** | 500 trivial cases ≠ 50 risk-targeted cases | Report coverage by `requirement × technique` matrix, not raw case count |
| **Inherited tier membership** | Smoke bloats over time as someone moves cases up | Tier membership is computed each cycle from the rules above; never grandfathered |
| **Single-tier suite** | A suite that runs in full every time wastes time | Tier into smoke/sanity/full so signal arrives fast |
| **Happy-path-only coverage** | 70% of real defects live in negative / boundary / concurrent paths | Apply Negative Path Coverage Floor (`scenario-design-techniques.md` §10) |
| **No charter for unspecified areas** | Spec gaps go untested entirely | Author SBTM charters for any feature area with <70% AC clarity |
| **Low assertion density** | Cases that "run" but assert little catch nothing; mutation studies show up to 28% of human-written tests fail to detect injected bugs | Apply the **Assertion Density Check** below; route to Radar for mutation-score validation. [Source: https://www.sciencedirect.com/science/article/abs/pii/S0950584924000739] |

---

## Assertion Density Check

For every Drill-authored case, verify before delivery:

| Heuristic | Threshold | If failing |
|-----------|-----------|------------|
| Expected Results per step | ≥1 observable assertion per step (verb + observable object) | Rewrite empty / "no error" steps with concrete checks |
| Negative observables per case | If the case has a `Negative` type, at least one step asserts an **error message text or audit log entry**, not just absence of success | Add the missing observable |
| Cross-layer assertions on P0 cases | UI + persistence + audit/log assertions all present | Add the missing layer or document why it is N/A |

When the same suite is later automated, hand the assertion checklist to Radar so mutation testing has a real target.

---

## Coverage Reporting Format

```markdown
## Coverage Summary

| Metric | Value |
|--------|-------|
| Total test cases | 87 |
| Requirements covered | 32 / 35 (91%) |
| Risk-Weighted Coverage | 0.84 (Σ(case priority-weight × technique-fitness) / Σ(requirement risk-weight)) |
| Coverage gaps | 3 (1 CRITICAL, 2 MEDIUM) |
| P0 cases | 18 |
| P1 cases | 34 |
| P2 cases | 28 |
| P3 cases | 7 |
| Negative-to-Positive ratio | 0.68 (AI self-check ≥0.6 PASS) |
| Techniques applied | BVA(22), EP(31), DT(12), ST(8), UC(9), EG(15), A11y(6) |
| Tier distribution | Smoke 7, Sanity 24, Regression 68, UAT 12 |
| Estimated full-regression duration | 11h 30m |

## Coverage Gaps

| Severity | Req ID | Description | Recommendation |
|----------|--------|-------------|----------------|
| CRITICAL | FR-AUTH-15 | Magic-link login | Author 4 cases (happy, expired, replay, wrong-device) before release |
| MEDIUM | FR-CART-08 | Quantity update | Add 1 boundary case at max (99→100) |
| MEDIUM | FR-PROFILE-03 | Avatar upload | Add 1 negative case (oversized file rejection) |
```

---

## Refresh Cadence

| Tier | Refresh Trigger | Action |
|------|-----------------|--------|
| Smoke | Every sprint | Audit duration; demote any case >3 min; retire any case that hasn't found a regression in 3 quarters |
| Sanity | Every release | Re-prioritize by recent defect density per module |
| Regression | Quarterly | Retire cases for retired features; add cases for the last quarter's production defects |
| UAT | Per release | Re-derive from current business contracts; do not auto-inherit |

Retired cases move to an `archive/` folder with a one-line reason — never deleted, in case the feature returns.

### Quarterly Hygiene Cycle (Smartesting pattern)

Each quarter, run a structured hygiene pass on the regression pool measuring **defects-found per execution** and retiring zombies. [Source: https://www.smartesting.com/en/fixing-regression-test-suite-bloat-with-ai/]

**Zombie Test Detection Heuristics**

| Symptom | Threshold | Action |
|---------|-----------|--------|
| No failure in production-data form for 4+ quarters | True | Demote one tier; flag for retirement next cycle |
| `defects-found per 100 executions` = 0 across last 2 releases | True | Retire unless covering a compliance / contract requirement |
| Duplicate steps ≥80% overlap with another case | True | Merge or retire the redundant case |
| Tied to a feature flag that has been 100% rolled out for ≥1 quarter | True | Promote to permanent regression and drop the flag-gating language |
| Tied to a feature flag that was rolled back | True | Retire unless the rollback is temporary |
| Case duration > tier ceiling (Smoke >3 min, Sanity >5 min) and stable | True | Demote tier; do not delete |
| Author left the team and ≥2 reviewers cannot describe the intent | True | Retire — institutional knowledge has decayed |

Emit hygiene results as `RETIRE / MERGE / DEMOTE / KEEP` rows; never silently delete.
