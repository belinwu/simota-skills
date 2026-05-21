# QA Workflow Integration

How Drill-authored test cases fit into sprint cadence, release cycles, defect lifecycle, and agent handoffs.

---

## Sprint Cadence

| Sprint Day | QA Activity | Drill's Role |
|------------|-------------|--------------|
| Planning (D0) | Story estimation, AC review | Spot ACs that are untestable or ambiguous; emit `OPEN_QUESTION` list to spec owner |
| Day 1-2 | Test design for upcoming stories | Author test cases per AC; build traceability stub |
| Day 3-5 | Implementation in progress | Refine test cases as ACs clarify; pre-build test data references for `Mint` |
| Day 6-7 | Code complete, QA execution starts | Cases are execution-ready; QA testers run them per priority order |
| Day 8 | Defect triage | Author missing regression cases for confirmed defects (input from `Scout`) |
| Day 9 | Release candidate cut | Final pass: traceability complete, no `COVERAGE_GAP=CRITICAL` |
| Day 10 | Release / UAT | Sign-off handoff to `Guardian`; archive sprint suite into regression pool |

Drill is most active in **D1-D5** (design + refinement) and **D8** (regression authoring from defects).

---

## Release Cycle Activities

| Phase | Activity | Trigger | Input | Output |
|-------|----------|---------|-------|--------|
| **Pre-design** | Test-affordable AC review | New PRD lands | PRD from `Scribe` / `Accord` | List of untestable ACs |
| **Design** | Author sprint test suite | ACs finalized | ACs + risk inputs | Test cases + traceability matrix |
| **Pre-RC** | Regression curation | Feature freeze | Current regression pool + sprint additions | Curated tiers (smoke/sanity/full/UAT) |
| **RC validation** | Full regression execution support | RC built | Tiered suite | Execution results, defects |
| **Pre-GA** | UAT scenario prep | RC signed off internally | Business contracts | UAT scenarios for stakeholders |
| **Post-release** | Production-defect regression authoring | Hotfix defect closed | Defect report from `Scout` | Permanent regression case for the defect |

---

## Defect Lifecycle Integration

When a Drill-authored test case **fails**:

1. **Capture**: tester fills the case's paired `Defect Template` block (severity, reproduction, evidence).
2. **File**: open a defect in the tracker (Jira / Linear / etc.) linking back to the `TC-ID`.
3. **Triage**: triage team confirms severity, assigns to engineering.
4. **Fix → Verify**: same test case re-run after fix; pass closes the defect.
5. **Regression lift**: if the defect was a regression (worked before, broke now), author a **new** regression test case targeting the specific root cause, even if the original case covers the symptom. Tag `Type: Regression, Linked-Defect: BUG-NNNN`.

### Severity vs Priority Disambiguation

| Term | Lives On | Question It Answers |
|------|----------|---------------------|
| Test Case `Priority` | Test case | How urgently should we test this? |
| Defect `Severity` | Defect record | How bad is this defect technically? |
| Defect `Priority` | Defect record | How urgently should we fix this defect? |

A P3 test case can find a Critical-severity defect (cosmetic test reveals data leak). A P0 test case can find a Low-severity defect (smoke check finds a typo).

---

## Handoff Protocols

### Scribe → Drill

```yaml
SCRIBE_TO_DRILL_HANDOFF:
  source_artifact: <path or URL to spec/PRD>     # source URL must be preserved end-to-end
  acceptance_criteria: [<AC-ID>, ...]
  in_scope_modules: [<module>, ...]
  target_tool: TestRail | Zephyr | Xray | Qase | Markdown
  required_techniques_hint: [BVA, DT, ...]   # optional
  external_issue_id: <Jira/GitHub issue ID>      # optional but preferred (Qase AIDEN traceability)
  due_date: YYYY-MM-DD
```

### Attest → Drill

```yaml
ATTEST_TO_DRILL_HANDOFF:
  bdd_scenarios: [<scenario-ID>, ...]
  expand_to_manual_procedure: true
  retain_traceability_to: [<AC-ID>, ...]
```

### Matrix → Drill

```yaml
MATRIX_TO_DRILL_HANDOFF:
  selected_combinations: [{<axis>: <value>, ...}, ...]
  coverage_strength: pairwise | 3-wise
  invalid_pairs_excluded: [<{axis, value}, ...>]
  author_one_case_per_combination: true
```

### Scout → Drill

```yaml
SCOUT_TO_DRILL_HANDOFF:
  defect_id: BUG-NNNN
  root_cause: <summary>
  reproduction_steps: [...]
  affected_modules: [<module>]
  request: author_permanent_regression_case
```

### Drill → Voyager

```yaml
DRILL_TO_VOYAGER_HANDOFF:
  test_cases: [<TC-ID>, ...]
  automation_candidate_filter: Yes
  rationale: high_value_high_frequency
  target_framework_hint: Playwright | Cypress
```

### Drill → Radar

```yaml
DRILL_TO_RADAR_HANDOFF:
  test_cases: [<TC-ID>, ...]
  abstraction_target: unit | integration
  reason: deterministic + isolated + below E2E threshold
```

### Drill → Mint

```yaml
DRILL_TO_MINT_HANDOFF:
  data_requirements:
    - precondition: <text>
      values_needed: [<field>: <constraint>, ...]
      volume: <int>
  request: generate_or_register_fixtures
```

### Drill → Guardian

```yaml
DRILL_TO_GUARDIAN_HANDOFF:
  release_candidate: <version or tag>
  smoke_results: PASS | FAIL
  sanity_results: PASS | FAIL
  regression_results: PASS | <failed_TC_count>
  uat_results: PASS | FAIL | PENDING
  open_defects: [<BUG-ID>, ...]
  recommendation: GO | NO-GO | CONDITIONAL
```

---

## Exploratory Session Integration

Exploratory charters (SBTM) feed back into Drill's permanent regression pool:

```
Charter → Session → Findings → Bug Reports + New Regression Cases
              ↓
          Notetaking template
              ↓
          Debrief with PM/Dev
              ↓
          Lift discovered scenarios to permanent TCs (Drill `author` recipe)
```

Drill is responsible for the **lift** step: when a charter session ends, convert each Class-A bug and each "almost-bug" observation into a permanent `Type: Regression` test case in the regression pool.

---

## Prompt Provenance (AI-assisted authoring)

When Drill (or an upstream agent / TM-tool AI) drafts test cases via an LLM, every AI-touched case carries provenance so reviewers can reproduce and re-evaluate the draft. Aligns with **ISTQB CT-GenAI v1.1** (2026-04). [Source: https://istqb.org/istqb-certified-tester-specialist-level-testing-with-generative-ai-ct-genai-press-release/]

Required fields on the case (also defined in `test-case-templates.md` Optional Provenance Fields):

| Field | Example |
|-------|---------|
| `ai_generated` | `true` |
| `ai_review_status` | `approved` (Qase AIDEN-style human-in-the-loop gate) |
| `model_id` | `claude-opus-4-7@2026-01` |
| `prompt_id_or_hash` | `prompt-v3-sha256:ab12…` (reference to the canonical prompt, not the raw text if it contains sensitive context) |
| `temperature` / `top_p` / `seed` | `0.0` / `1.0` / `42` |
| `non_determinism_disclosure` | `same prompt + temperature=0 → identical output (5 runs verified)` or `temperature=0.7 → variance band documented` |
| `human_reviewer` | `<name or role>` (mandatory before `ai_review_status: approved`) |

Drill refuses to mark `ai_review_status: approved` without a `human_reviewer` value.

---

## Maintenance Rhythm

| Cadence | Activity |
|---------|----------|
| Every sprint | Add sprint cases to regression pool; archive retired-feature cases |
| Every release | Re-tier (smoke / sanity / regression / UAT) per current risk |
| Quarterly | Re-score priorities; audit duplicate cases; mutation-test the suite (route to `Radar`); run **Zombie Test Detection** (see `coverage-strategy.md`) |
| Annually | Retire deprecated cases (no defect found in 4 quarters AND feature unchanged) |

### Contract Testing vs Manual UAT (boundary)

Contract testing (Pact, Spring Cloud Contract) verifies **API-boundary compatibility** between provider and consumer; it does **not** replace UAT or end-to-end manual scenarios that exercise business flows across the full stack. [Source: https://totalshiftleft.ai/blog/what-is-api-contract-testing] Drill manual cases stay responsible for:
- Multi-step business flows that span ≥2 services
- UI / a11y / cognitive checks that Pact cannot express
- Stakeholder-facing UAT sign-off scenarios

Pact-style contract tests live with Radar / Builder; Drill notes the contract-covered boundary in `Preconditions` ("provider-side contract X is green") so manual cases do not re-test API shape.

---

## Common Workflow Anti-Patterns

| Anti-pattern | Symptom | Fix |
|--------------|---------|-----|
| QA receives ACs at D6 | Cases not ready when build is | Move test design left to D1-D5; emit `BLOCKED_ON_SPEC` if ACs are late |
| Cases written in defect tracker comments | Knowledge dies with the ticket | Author in TM tool; reference defect from case, not the inverse |
| Regression suite never shrinks | Suite runtime grows unbounded | Quarterly retirement; mutation-score retirement triggers |
| Smoke = "the cases that happen to be fast" | No risk targeting | Apply tier rules from `coverage-strategy.md`; revisit each sprint |
| Exploratory results not lifted | Bugs recur because tests don't exist | After every charter, lift findings within 1 business day |
| One person owns the suite | Single point of failure | Pair authoring; require ≥1 reviewer per new case before it enters regression |
