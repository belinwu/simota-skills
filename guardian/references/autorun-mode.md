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

  analysis_timeout:
    detection: "Analysis exceeds 30s per 100 files"
    action: "Switch to chunked analysis mode"
    recovery: "Progressive results, continue in background"

  noise_ratio_extreme:
    detection: "Noise ratio > 80%"
    action: "Handoff to Zen for bulk cleanup"
    recovery: "Wait for cleanup, re-analyze clean diff"

  quality_score_critical:
    detection: "Quality score < 35"
    action: "Pause for user decision"
    recovery: "Wait for split/restructure decision"

  risk_score_critical:
    detection: "Risk score > 85"
    action: "Require Sentinel review"
    recovery: "Wait for security clearance"

  hotspot_overload:
    detection: "More than 5 Problem Child hotspots modified"
    action: "Recommend Zen refactoring first"
    recovery: "Continue after cleanup or user override"

  branch_health_severe:
    detection: "Health score < 25"
    action: "Recommend rebase/split"
    recovery: "Continue after remediation"
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
      size: 65
      focus: 70
      commits: 80
      tests: 60
      docs: 75
      risk: 55

  # New: Risk Assessment
  risk:
    score: 72
    category: HIGH
    factors:
      sensitivity: 80
      complexity: 65
      hotspot_overlap: 75
      dependency_impact: 60
      test_coverage: 70
      author_familiarity: 55
    high_risk_files:
      - path: src/auth/jwt.ts
        score: 92
        reason: "Auth + hotspot"
    mitigations:
      - "Sentinel security review"
      - "Add token refresh tests"

  # New: Branch Health
  branch_health:
    score: 65
    grade: warning
    indicators:
      sync: 75  # 12 behind
      age: 60   # 8 days
      conflict_risk: 100
      ci_status: 100
      size_creep: 50

  # New: Commit Analysis
  commit_analysis:
    count: 5
    avg_score: 72
    wip_count: 1
    rebase_needed: true
    issues:
      - commit: d4e5f6
        score: 25
        issue: "Vague message"

  # New: Hotspots
  hotspots:
    modified_count: 3
    problem_children: 2
    files:
      - path: src/api/users.ts
        type: problem_child
        churn: 68%
        bugs: 8

  # New: Reviewer Recommendations
  reviewers:
    primary:
      id: "@alice"
      ownership: 45%
      score: 92
    secondary:
      id: "@bob"
      ownership: 32%
      score: 85

  change_breakdown:
    essential: 12 files (25%)
    supporting: 8 files (17%)
    noise: 27 files (58%)

  noise_details:
    - type: formatting
      files: 25
      recommendation: separate_commit
    - type: lock_file
      files: 2
      recommendation: exclude_from_review

  recommendations:
    - action: SPLIT_PR
      confidence: HIGH
      reason: "47 files exceeds reviewability threshold"
      suggested_splits: 3

    - action: SEPARATE_NOISE
      confidence: HIGH
      reason: "58% noise ratio detected"

    - action: SECURITY_REVIEW
      confidence: HIGH
      reason: "Risk score 72, auth files modified"

    - action: REBASE
      confidence: MEDIUM
      reason: "12 commits behind main"

  suggested:
    branch_name: "feat/oauth2-provider"
    merge_strategy: "squash"
    pr_title: "feat(auth): add OAuth2 provider integration"

  # New: Pre-Merge Checklist
  pre_merge_checklist:
    required:
      - item: "CI passing"
        status: true
      - item: "No conflicts"
        status: true
      - item: "Approvals obtained"
        status: false
    conditional:
      - item: "Security review"
        status: false
        reason: "Auth changes detected"
      - item: "Test coverage"
        status: false
        reason: "High-risk files need tests"

  next_steps:
    - "Review suggested PR splits"
    - "Separate formatting changes"
    - "Request Sentinel security review"
    - "Rebase onto main"
    - "Generate PR description"
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
      merge: squash
      split_needed: false
    analysis:
      essential: 8
      supporting: 4
      noise: 2

    # New: Quality Assessment
    quality:
      score: 78
      grade: "B+"
      improvements:
        - "Add edge case tests (+5)"
        - "Update API docs (+3)"

    # New: Risk Assessment
    risk:
      score: 65
      category: MEDIUM
      mitigations_needed:
        - "Integration testing"
        - "Monitor after deploy"

    # New: Branch Health
    branch_health:
      score: 85
      issues: []

    # New: Commit Quality
    commit_quality:
      avg_score: 85
      rebase_needed: false

    # New: Hotspots
    hotspots:
      count: 1
      action_needed: false

    # New: Reviewers
    reviewers:
      recommended: ["@alice", "@bob"]
      coverage: 87%

    # New: Checklist
    pre_merge:
      blockers: 0
      warnings: 2
      items:
        - "CI passing: true"
        - "Security review: not required"

  Handoff:
    Format: GUARDIAN_TO_BUILDER_HANDOFF | GUARDIAN_TO_JUDGE_HANDOFF
    Content: [Full handoff content]

  Next: Builder | Judge | Canvas | Sherpa | Sentinel | Radar | Zen | DONE

  Notes: [Any important observations or warnings]
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

  recovery_in_progress:
    - Zen cleanup requested, awaiting completion
    - Scout investigation requested
    - Retry after timeout in progress
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
    - Agent: Sentinel
      Request: Security audit
      Blocking: true
    - Agent: Judge
      Request: AI code and dependency verification
      Blocking: false

  Partial_Results:
    commit_plan: [...]  # Available
    pr_description: [...] # Available
    merge_strategy: null  # Awaiting security review

  Resume_Condition: "Sentinel security audit complete"
  Next: WAIT_FOR_SENTINEL
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
