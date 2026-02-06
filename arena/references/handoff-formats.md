# Handoff Formats

Input and output handoff templates for Arena's inter-agent collaboration.

---

## Input Handoffs (Receiving)

### SHERPA_TO_ARENA_HANDOFF

Task decomposed into atomic steps, ready for multi-variant implementation.

```yaml
SHERPA_TO_ARENA_HANDOFF:
  Task: "[Task name]"
  Atomic_Steps:
    - step_id: 1
      description: "[Step description]"
      estimated_complexity: "[S/M/L]"
  Recommended_Variants: "[N]"
  Recommended_Engine: "[engine or 'all']"
  Quality_Requirements:
    - "[Requirement 1]"
    - "[Requirement 2]"
```

### SCOUT_TO_ARENA_HANDOFF

Bug investigation complete, multiple fix approaches identified for comparison.

```yaml
SCOUT_TO_ARENA_HANDOFF:
  Bug_Analysis:
    root_cause: "[Root cause description]"
    impact: "[Impact assessment]"
    affected_files:
      - "[File path 1]"
      - "[File path 2]"
  Fix_Approaches:
    - approach_id: A
      description: "[Approach A description]"
      risk: "[Low/Medium/High]"
    - approach_id: B
      description: "[Approach B description]"
      risk: "[Low/Medium/High]"
  Recommended_Variants: "[N]"
```

### SPARK_TO_ARENA_HANDOFF

Feature proposal with multiple implementation options for parallel exploration.

```yaml
SPARK_TO_ARENA_HANDOFF:
  Feature_Proposal:
    name: "[Feature name]"
    description: "[Feature description]"
    value_proposition: "[Why this feature]"
  Implementation_Options:
    - option_id: 1
      approach: "[Approach description]"
      complexity: "[S/M/L]"
    - option_id: 2
      approach: "[Approach description]"
      complexity: "[S/M/L]"
  Recommended_Variants: "[N]"
```

---

## Output Handoffs (Sending)

### ARENA_TO_GUARDIAN_HANDOFF

Implementation selected and ready for PR preparation.

```yaml
ARENA_TO_GUARDIAN_HANDOFF:
  Implementation:
    run_id: "[aiw run ID]"
    selected_variant: "[variant_id]"
    selection_rationale: "[Why this variant was chosen]"
  Files_Changed:
    - path: "[File path]"
      change_type: "[Added/Modified/Deleted]"
      summary: "[Change summary]"
  Comparison_Summary:
    total_variants: "[N]"
    engines_used:
      - "[engine 1]"
    evaluation_criteria: "[Criteria used]"
  Test_Status: "[PASS/FAIL/PENDING]"
  Ready_For_Review: "[true/false]"
```

### ARENA_TO_RADAR_HANDOFF

Implementation adopted, test coverage needed.

```yaml
ARENA_TO_RADAR_HANDOFF:
  Implementation:
    run_id: "[aiw run ID]"
    selected_variant: "[variant_id]"
    files_changed:
      - "[File path 1]"
      - "[File path 2]"
  Test_Requirements:
    - requirement: "[What to test]"
      priority: "[High/Medium/Low]"
  Edge_Cases_Identified:
    - "[Edge case 1]"
    - "[Edge case 2]"
  Variant_Comparison:
    - variant_id: "[ID]"
      approach_summary: "[Summary]"
      testability_notes: "[Notes for testing]"
```

### ARENA_TO_JUDGE_HANDOFF

Request code review of selected variant.

```yaml
ARENA_TO_JUDGE_HANDOFF:
  Implementation:
    run_id: "[aiw run ID]"
    selected_variant: "[variant_id]"
    selection_rationale: "[Brief rationale]"
  Review_Focus:
    - "[Area needing particular attention]"
  Files_To_Review:
    - "[File path 1]"
    - "[File path 2]"
  Context:
    total_variants: "[N]"
    rejected_approaches: "[Why alternatives were rejected]"
```

### ARENA_TO_SENTINEL_HANDOFF

Request security review of selected variant.

```yaml
ARENA_TO_SENTINEL_HANDOFF:
  Implementation:
    run_id: "[aiw run ID]"
    selected_variant: "[variant_id]"
  Security_Concerns:
    - "[Identified concern 1]"
    - "[Identified concern 2]"
  Files_Changed:
    - "[File path 1]"
  Context:
    spec_security_requirements: "[From original spec]"
    variant_safety_score: "[Score from evaluation]"
```
