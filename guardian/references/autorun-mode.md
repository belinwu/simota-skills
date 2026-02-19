# Guardian AUTORUN Mode Reference

Details for autonomous operation in Nexus agent chains.

## AUTORUN Context Format

```yaml
_AGENT_CONTEXT:
  Role: Guardian
  Task: [Specific task from Nexus]
  Mode: AUTORUN
  Chain: [Previous agents in chain]
  Input: [Handoff received from previous agent]
```

## Auto-Execute (No Confirmation)

- Change category classification
- Branch name generation (suggestions)
- PR size assessment
- Noise detection and reporting
- Release notes draft generation
- Handoff format generation
- **Quality score calculation**
- **Commit message analysis**
- **Risk factor assessment**
- **Hotspot detection**
- **Reviewer recommendations**
- **Branch health check**
- **Pre-merge checklist generation**

## Pause for Confirmation

- PR split recommendations
- Merge strategy selection
- Force-push suggestions
- History rewriting operations
- Destructive Git operations
- **Quality score < 35 (F grade)**
- **Risk score > 85 (CRITICAL)**
- **High-risk file changes without security review**
- **Hotspot refactoring recommendations**

## Guardian-Specific Guardrails

```yaml
error_handling:
  git_conflict_unresolved:
    detection: "Merge conflict markers in files"
    action: "Handoff to Scout for conflict investigation"
    recovery: "Resume after Scout provides resolution context"

  pr_too_large:
    detection: "PR size > XL threshold"
    action: "Auto-generate split proposal"
    recovery: "Continue with chunked analysis"

  branch_name_collision:
    detection: "Branch name already exists"
    action: "Generate alternative with suffix (-v2, -alt)"
    recovery: "Propose alternatives to user"
# ...
```

## Recovery Strategies

```yaml
recovery_strategies:
  retry_with_reduced_scope:
    triggers: [analysis_timeout, memory_limit]
    action: "Reduce analysis to essential files only"
    max_retries: 2

  fallback_to_manual:
    triggers: [git_conflict_unresolved, semantic_conflict]
    action: "Provide manual resolution guidance"
    handoff: Scout

  escalate_to_human:
    triggers: [3_consecutive_failures, security_concern]
    action: "Pause AUTORUN, request human intervention"
    format: "BLOCKED status with context"
```

## AUTORUN Output Format

```yaml
guardian_analysis:
  branch: feat/oauth-integration
  target: main

  summary:
    total_files: 47
    total_lines: +1234/-567
    size_rating: L
    reviewability: 4/10

  # New: Quality Metrics
  quality:
    score: 68
    grade: B
    components:
# ...
```

## _STEP_COMPLETE Format

```yaml
_STEP_COMPLETE:
  Agent: Guardian
  Status: SUCCESS | PARTIAL | BLOCKED

  Output:
    branch_name: "feat/oauth2-provider"
    commit_plan:
      - order: 1
        message: "feat(auth): add OAuth2 provider"
        files: ["oauth.ts", "types.d.ts"]
      - order: 2
        message: "test(auth): add OAuth2 tests"
        files: ["oauth.test.ts"]
    pr_strategy:
      size: M
# ...
```

## Status Definitions

| Status | Meaning | Next Action |
|--------|---------|-------------|
| **SUCCESS** | Analysis complete, ready for handoff | Proceed to Next agent |
| **PARTIAL** | Analysis done but needs user decision | Pause for confirmation |
| **BLOCKED** | Cannot proceed (conflicts, missing info) | Request intervention |

## PARTIAL Status Conditions

```yaml
partial_conditions:
  awaiting_decision:
    - PR split strategy needs approval
    - Merge strategy selection required
    - Security concerns need acknowledgment

  external_verification:
    - Sentinel security review in progress
    - Judge quality gate verification pending
    - Atlas architecture analysis pending

  incomplete_data:
    - Large PR chunked analysis ongoing
    - Some files inaccessible
    - Git history incomplete
# ...
```

---

## Decision Matrix

### Action Decision Framework

Guardian uses this matrix to determine actions during AUTORUN:

```yaml
decision_matrix:
  # Format: condition -> action + blocking

  security:
    critical_classification:
      action: HANDOFF_SENTINEL
      blocking: true
      auto_proceed: false
    sensitive_with_auth:
      action: HANDOFF_SENTINEL
      blocking: false
      auto_proceed: true
    dangerous_pattern:
      action: PAUSE_FOR_CONFIRMATION
      blocking: true
# ...
```

### Decision Priority Order

```yaml
decision_priority:
  1_security: "Always evaluate first, can block everything"
  2_conflicts: "Cannot proceed with unresolved conflicts"
  3_quality: "Poor quality may need restructure"
  4_risk: "High risk may need additional review"
  5_coverage: "Coverage gaps may need tests"
  6_noise: "Noise cleanup can often parallel"
  7_architecture: "Architecture usually advisory"
```

### Multi-Condition Resolution

```yaml
multi_condition_resolution:
  strategy: "Most restrictive wins"

  examples:
    security_critical_and_noise_high:
      result: PAUSE (security blocking)
      parallel: Zen can prepare while waiting

    quality_poor_and_coverage_critical:
      result: PAUSE (coverage blocking)
      sequence: Fix coverage → Re-evaluate quality

    risk_high_and_architecture_cross_module:
      result: PROCEED_WITH_ATTENTION
      parallel: [Atlas analysis, Normal flow]
```

---

## Partial Execution Support

### PARTIAL Status Detailed Behavior

```yaml
partial_execution:
  definition: |
    PARTIAL status indicates Guardian has completed some work
    but requires external input before full completion.

  characteristics:
    - Partial results are available
    - Some handoffs are pending
    - User decision may be needed
    - Recovery path is defined

  output_structure:
    completed_work:
      - Analysis results
      - Partial recommendations
# ...
```

### Partial Execution Scenarios

```yaml
partial_scenarios:
  scenario_1_sentinel_review:
    trigger: "CRITICAL security classification"
    completed:
      - Change analysis
      - Branch naming
      - Commit structure
      - PR description draft
    pending:
      - Sentinel security approval
    blocking: true
    resume_on: "SENTINEL_TO_GUARDIAN_RESPONSE"
    output_status: PARTIAL

  scenario_2_zen_cleanup:
# ...
```

### Partial _STEP_COMPLETE Format

```yaml
_STEP_COMPLETE:
  Agent: Guardian
  Status: PARTIAL
  Reason: "[Specific reason for partial status]"

  Completed:
    analysis:
      essential: 12
      supporting: 5
      noise: 28
    branch_name: "feat/oauth2-provider"
    commit_plan:
      - order: 1
        message: "feat(auth): add OAuth2"
        files: [list]
# ...
```

---

## Recovery Strategies (Enhanced)

### Comprehensive Recovery Matrix

```yaml
recovery_matrix:
  handoff_timeout:
    sentinel:
      timeout: "24h"
      recovery:
        1: "Send reminder notification"
        2: "Escalate to security team lead"
        3: "Request manual override from PR author"
      fallback: BLOCKED

    zen:
      timeout: "30m"
      recovery:
        1: "Continue without cleanup"
        2: "Flag noise in PR description"
# ...
```

### Recovery Execution Flow

```
┌─────────────────────────────────────┐
│         Issue Detected               │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│    Lookup Recovery Strategy          │
└─────────────────┬───────────────────┘
                  ↓
         ┌───────────────┐
         │ Auto-Retry    │──YES──→ Execute Retry
         │ Available?    │              ↓
         └───────┬───────┘         Success? ──YES──→ Continue
                 │                      │
                 │NO                    │NO
                 ↓                      ↓
...
```

## PARTIAL _STEP_COMPLETE Example

```yaml
_STEP_COMPLETE:
  Agent: Guardian
  Status: PARTIAL
  Reason: "Security review required before merge approval"

  Output:
    branch_name: "feat/auth-update"
    analysis:
      essential: 8
      noise: 5
    security:
      classification: CRITICAL
      sentinel_required: true

  Pending:
# ...
```

## Chain Integration Examples

**Plan → Guardian → Builder**:
```yaml
_STEP_COMPLETE:
  Agent: Guardian
  Status: SUCCESS
  Output:
    branch_name: "feat/user-export"
    commit_plan: [...]
  Next: Builder
```

**Builder → Guardian → Judge**:
```yaml
_STEP_COMPLETE:
  Agent: Guardian
  Status: SUCCESS
  Output:
    pr_strategy: {...}
    analysis: {...}
  Handoff:
    Format: GUARDIAN_TO_JUDGE_HANDOFF
    Content: [...]
  Next: Judge
```

**Guardian → Zen (Noise Loop)**:
```yaml
_STEP_COMPLETE:
  Agent: Guardian
  Status: PARTIAL
  Output:
    noise_detected: 58%
    cleanup_needed: true
  Next: Zen
  Notes: "High noise ratio - requesting Zen cleanup before continuing"
```
