# Interaction Triggers

YAML templates for Titan's 4 interaction triggers — the fewest in the ecosystem.

Titan asks users only as an absolute last resort. These 4 triggers are the ONLY situations requiring user input. All other decisions are made autonomously via Decision Matrix and Magi consultation.

---

## Trigger 1: ON_AMBIGUOUS_GOAL

**Purpose**: Resolve fundamental product direction ambiguity.
**Condition**: Cipher analysis produces 2+ interpretations leading to fundamentally different products.
**NOT triggered**: When Cipher resolves to single interpretation, or differences are implementation-only.

```yaml
trigger: ON_AMBIGUOUS_GOAL
timing: BEFORE_START
phase: DISCOVER
condition: |
  cipher_analysis.interpretations >= 2
  AND interpretations_are_fundamentally_different
  AND cannot_merge_into_single_product

template:
  question: "Your product goal can be interpreted in fundamentally different ways. Which direction matches your vision?"
  header: "Product Direction"
  context: |
    Goal: "[user's original goal]"
    Cipher analysis found [N] distinct interpretations:
  options:
    - label: "[Interpretation 1 title]"
      description: "[What this product would be — target users, key features, market position]"
    - label: "[Interpretation 2 title]"
      description: "[What this product would be — target users, key features, market position]"
  default: "[Most likely interpretation based on context]"

post_action: Record in Decision Log as DEC-001 → Update TITAN_STATE → Proceed with selected direction
```

---

## Trigger 2: ON_EXTERNAL_DEPENDENCY

**Purpose**: Obtain credentials or approve paid service usage.
**Condition**: Required external service not available, no free alternative exists.
**NOT triggered**: When free/OSS alternative can substitute, or feature can be stubbed/mocked.

```yaml
trigger: ON_EXTERNAL_DEPENDENCY
timing: ON_NEED
phase: ANY
condition: |
  required_service NOT IN environment_variables
  AND no_free_alternative_exists
  AND cannot_stub_without_losing_core_functionality

template:
  question: "An external service is required but not configured in your environment."
  header: "External Service"
  context: |
    Service: [service name]
    Purpose: [why needed]
    Feature: [which feature requires it]
  options:
    - label: "Provide credentials"
      description: "I'll set up [service] and provide the API key / connection string"
    - label: "Use alternative: [free_alternative]"
      description: "[Description of alternative and trade-offs]"
    - label: "Skip this feature"
      description: "Remove [feature] from scope"
    - label: "Stub for now"
      description: "Create interface stub, implement later"

post_action: Credentials → integrate · Alternative → update architecture, log · Skip → remove from roadmap · Stub → add to backlog
```

---

## Trigger 3: ON_CRITICAL_RISK_BUDGET

**Purpose**: Present accumulated decisions for user review at risk threshold.
**Condition**: Cumulative risk score ≥ 100.
**NOT triggered**: When risk budget is below threshold.

```yaml
trigger: ON_CRITICAL_RISK_BUDGET
timing: ON_THRESHOLD
phase: ANY
condition: cumulative_risk_score >= 100

template:
  question: "Titan has made several significant decisions autonomously. Review and approve to continue."
  header: "Risk Review"
  context: |
    Cumulative risk score: [score]/100 threshold
    Decisions since last review: [count]
    Key decisions:
    - DEC-[N]: [title] (risk: [score]) — [choice]
  options:
    - label: "Approve all and continue"
      description: "Reset risk budget to 0, proceed with current decisions"
    - label: "Review individually"
      description: "I'll review each decision and may request changes"
    - label: "Rollback high-risk decisions"
      description: "Undo decisions with risk score ≥ [threshold]"

post_action: Approve → reset score, continue · Review → present individually · Rollback → revert, re-run chains
```

---

## Trigger 4: ON_PHASE_REVIEW

**Purpose**: Present phase summary when user opted into phased review mode.
**Condition**: `TITAN_PHASED_REVIEW` mode active AND phase boundary reached with exit criteria met.
**NOT triggered**: In default AUTORUN_FULL mode.

```yaml
trigger: ON_PHASE_REVIEW
timing: ON_PHASE_BOUNDARY
phase: ANY (at boundary)
condition: |
  mode == TITAN_PHASED_REVIEW
  AND phase_exit_criteria_met

template:
  question: "Phase [PHASE_NAME] is complete. Review the results and decide how to proceed."
  header: "Phase Review"
  context: |
    ## TITAN_PHASE_COMPLETE: [PHASE_NAME]
    [Full TITAN_PHASE_COMPLETE output — see output-formats.md]
  options:
    - label: "Proceed to [next phase]"
      description: "Phase results satisfactory, continue"
    - label: "Revise current phase"
      description: "Some items need rework"
    - label: "Adjust scope"
      description: "Change project scope or roadmap"
    - label: "Pause project"
      description: "Save state for later resumption"

post_action: Proceed → advance · Revise → re-enter phase · Adjust → update roadmap · Pause → save TITAN_STATE
```

---

## Trigger Frequency Expectations

| Trigger | Expected | Per S | Per L | Per XL |
|---------|----------|-------|-------|--------|
| ON_AMBIGUOUS_GOAL | Once at start (if needed) | 0-1 | 0-1 | 0-1 |
| ON_EXTERNAL_DEPENDENCY | Per service needed | 0-1 | 1-3 | 2-5 |
| ON_CRITICAL_RISK_BUDGET | When budget fills | 0 | 0-1 | 1-2 |
| ON_PHASE_REVIEW | Per phase (opt-in) | 0 | 0-9 | 0-9 |

**Total for AUTORUN_FULL mode**: S: 0-2 · M: 0-3 · L: 1-5 · XL: 2-8 questions.
