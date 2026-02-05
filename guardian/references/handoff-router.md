# Automated Handoff Router Reference

Guardian's intelligent routing system for automatic handoffs to specialized agents.

## Overview

The Handoff Router enables Guardian to automatically delegate specific issues to appropriate agents, reducing manual intervention by **80%**.

---

## Routing Rules Engine

### Rule Priority Order

```yaml
routing_priority:
  1_security:
    description: "Security issues have highest priority"
    target: Sentinel
    blocking: true

  2_coverage:
    description: "Coverage gaps before refactoring"
    target: Radar
    blocking: false

  3_noise:
    description: "Noise cleanup can run parallel"
    target: Zen
    blocking: false

  4_architecture:
    description: "Architecture impact when cross-module"
    target: Atlas
    blocking: false

  5_investigation:
    description: "Investigation when context unclear"
    target: Scout
    blocking: true
```

---

## Routing Rules

### 1. Noise to Zen Router

**Trigger**: Noise ratio > 30% OR formatting changes > 20 files

```yaml
noise_to_zen:
  triggers:
    - condition: "noise_ratio > 0.30"
      confidence: HIGH
    - condition: "formatting_files > 20"
      confidence: HIGH
    - condition: "import_reorder_files > 10"
      confidence: MEDIUM
    - condition: "whitespace_only_changes > 5"
      confidence: MEDIUM

  evaluation:
    threshold: 1 HIGH trigger OR 2 MEDIUM triggers
    auto_handoff: true

  handoff_action:
    type: GUARDIAN_TO_ZEN_HANDOFF
    mode: CLEANUP
    blocking: false  # Can continue analysis in parallel
    return_expected: true

  success_criteria:
    - Noise separated into dedicated commits
    - Formatting standardized
    - Essential changes isolated

  output:
    status: PARTIAL
    next: ZEN
    notes: "Noise cleanup requested, continuing essential analysis"
```

### 2. Security to Sentinel Router

**Trigger**: CRITICAL or SENSITIVE security classification

```yaml
security_to_sentinel:
  triggers:
    - condition: "security_classification == CRITICAL"
      confidence: HIGH
      blocking: true
    - condition: "security_classification == SENSITIVE AND auth_files_changed"
      confidence: HIGH
      blocking: true
    - condition: "dangerous_pattern_count > 0"
      confidence: HIGH
      blocking: true
    - condition: "secret_exposure_risk"
      confidence: CRITICAL
      blocking: true

  evaluation:
    any_trigger_fires: true
    auto_handoff: true
    user_notification: true

  handoff_action:
    type: GUARDIAN_TO_SENTINEL_HANDOFF
    mode: SECURITY_AUDIT
    blocking: true  # Must wait for clearance
    return_expected: true

  escalation_levels:
    critical:
      wait_for_completion: true
      max_wait: "24h"
      fallback: "BLOCKED"

    sensitive:
      wait_for_completion: false
      proceed_with_warning: true
      flag_in_pr: true

  output:
    status: PARTIAL
    next: WAIT_FOR_SENTINEL
    notes: "Security review required before merge approval"
```

### 3. Coverage to Radar Router

**Trigger**: High-risk files with coverage gap > 40%

```yaml
coverage_to_radar:
  triggers:
    - condition: "high_risk_file AND coverage_gap > 0.40"
      confidence: HIGH
    - condition: "hotspot_file AND coverage < 0.50"
      confidence: HIGH
    - condition: "critical_file AND no_tests"
      confidence: CRITICAL
    - condition: "regression_risk > 0.70"
      confidence: HIGH

  evaluation:
    threshold: 1 HIGH trigger OR 1 CRITICAL trigger
    auto_handoff: true

  handoff_action:
    type: GUARDIAN_TO_RADAR_HANDOFF
    mode: COVERAGE_IMPROVEMENT
    blocking: false  # Recommendations can be advisory
    return_expected: true

  coverage_goals:
    critical_files: 90%
    high_risk_files: 80%
    hotspot_files: 70%
    standard_files: 60%

  output:
    status: SUCCESS  # Can proceed with warnings
    next: RADAR | Judge  # Parallel or sequential
    notes: "Coverage improvement recommended"
```

### 4. Architecture to Atlas Router

**Trigger**: Cross-module changes or dependency additions

```yaml
architecture_to_atlas:
  triggers:
    - condition: "cross_module_changes > 3"
      confidence: HIGH
    - condition: "new_dependency_added AND shared_module"
      confidence: HIGH
    - condition: "circular_dependency_risk"
      confidence: CRITICAL
    - condition: "breaking_api_change"
      confidence: HIGH

  evaluation:
    threshold: 1 trigger
    auto_handoff: true

  handoff_action:
    type: GUARDIAN_TO_ATLAS_HANDOFF
    mode: IMPACT_ANALYSIS
    blocking: false
    return_expected: true

  output:
    status: SUCCESS
    next: Atlas
    notes: "Architecture impact analysis requested"
```

### 5. Investigation to Scout Router

**Trigger**: Unresolved conflicts or unclear intent

```yaml
investigation_to_scout:
  triggers:
    - condition: "merge_conflict_semantic"
      confidence: HIGH
      blocking: true
    - condition: "intent_unclear AND high_risk"
      confidence: HIGH
      blocking: true
    - condition: "historical_context_needed"
      confidence: MEDIUM
      blocking: false

  evaluation:
    semantic_conflict: blocking
    other: advisory

  handoff_action:
    type: GUARDIAN_TO_SCOUT_HANDOFF
    mode: INVESTIGATION
    blocking: varies
    return_expected: true

  output:
    status: BLOCKED | PARTIAL
    next: Scout
    notes: "Investigation required for resolution"
```

---

## Multi-Route Orchestration

### Parallel Routing

When multiple routes trigger simultaneously, Guardian orchestrates them efficiently.

```yaml
parallel_routing:
  allowed_combinations:
    - [zen, radar]           # Cleanup and coverage can parallel
    - [zen, atlas]           # Cleanup and architecture can parallel
    - [radar, atlas]         # Coverage and architecture can parallel

  sequential_requirements:
    - sentinel_before_all    # Security must complete first
    - scout_before_commit    # Investigation before decisions
    - zen_before_judge       # Cleanup before review

  orchestration_example:
    scenario: "Security issue + Noise + Coverage gap"
    execution:
      1: sentinel (blocking)
      2_parallel: [zen, radar]
      3: judge (after zen completes)
```

### Routing Decision Matrix

| Condition | Route | Blocking | Priority |
|-----------|-------|----------|----------|
| CRITICAL security | Sentinel | Yes | 1 |
| SENSITIVE + auth | Sentinel | Yes | 1 |
| Dangerous patterns | Sentinel | Yes | 1 |
| Noise > 30% | Zen | No | 3 |
| Coverage gap > 40% + risk | Radar | No | 2 |
| Cross-module > 3 | Atlas | No | 4 |
| Semantic conflict | Scout | Yes | 1 |

---

## Auto-Handoff Decision Flow

```
┌─────────────────────────────────────┐
│       Guardian Analysis Start        │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│    Evaluate Security Classification  │
└─────────────────┬───────────────────┘
                  ↓
         ┌───────────────┐
         │ CRITICAL or   │──YES──→ [Route to Sentinel]
         │ SENSITIVE?    │              (BLOCKING)
         └───────┬───────┘
                 │NO
                 ↓
┌─────────────────────────────────────┐
│       Evaluate Noise Ratio           │
└─────────────────┬───────────────────┘
                  ↓
         ┌───────────────┐
         │ Noise > 30%?  │──YES──→ [Route to Zen]
         └───────┬───────┘              (PARALLEL)
                 │NO
                 ↓
┌─────────────────────────────────────┐
│      Evaluate Coverage Gaps          │
└─────────────────┬───────────────────┘
                  ↓
         ┌───────────────┐
         │ Gap > 40% +   │──YES──→ [Route to Radar]
         │ High Risk?    │              (PARALLEL)
         └───────┬───────┘
                 │NO
                 ↓
┌─────────────────────────────────────┐
│    Evaluate Architecture Impact      │
└─────────────────┬───────────────────┘
                  ↓
         ┌───────────────┐
         │ Cross-module  │──YES──→ [Route to Atlas]
         │ > 3 modules?  │              (PARALLEL)
         └───────┬───────┘
                 │NO
                 ↓
┌─────────────────────────────────────┐
│        Continue Normal Flow          │
└─────────────────────────────────────┘
```

---

## Handoff Response Handling

### Sentinel Response Handler

```yaml
sentinel_response:
  on_approved:
    action: "Continue to Judge"
    status: SUCCESS
    notes: "Security clearance obtained"

  on_issues_found:
    action: "Return to Builder for fixes"
    status: BLOCKED
    issues: [list_from_sentinel]
    notes: "Security issues must be resolved"

  on_timeout:
    action: "Escalate to human"
    status: BLOCKED
    alert: true
```

### Zen Response Handler

```yaml
zen_response:
  on_cleanup_complete:
    action: "Re-analyze clean diff"
    merge_commits: true
    notes: "Noise separated successfully"

  on_partial_cleanup:
    action: "Accept partial, flag remaining"
    status: SUCCESS
    warnings: [remaining_noise]
```

### Radar Response Handler

```yaml
radar_response:
  on_tests_added:
    action: "Update coverage score"
    recalculate_risk: true
    notes: "Coverage improved"

  on_recommendations_only:
    action: "Include in PR description"
    status: SUCCESS
    recommendations: [list_from_radar]
```

---

## AUTORUN Integration

```yaml
autorun_routing:
  mode: AUTONOMOUS

  auto_execute:
    - Route evaluation
    - Non-blocking handoffs
    - Parallel orchestration
    - Response handling

  pause_for_confirmation:
    - CRITICAL security issues
    - Multiple blocking routes
    - Conflicting recommendations
    - Timeout situations

  status_mapping:
    all_routes_complete: SUCCESS
    blocking_route_pending: PARTIAL
    route_failed: BLOCKED
```

---

## Metrics and Monitoring

### Routing Effectiveness

```yaml
routing_metrics:
  tracked:
    - handoff_count_per_type
    - auto_vs_manual_ratio
    - route_success_rate
    - average_resolution_time
    - false_positive_rate

  targets:
    auto_handoff_rate: "> 80%"
    successful_resolution: "> 95%"
    false_positive_rate: "< 5%"

  improvements:
    - Adjust thresholds based on outcomes
    - Learn from manual overrides
    - Refine trigger conditions
```

### Route Analytics Template

```markdown
## Handoff Route Analytics

**Period**: Last 30 days
**Total PRs Analyzed**: 150

### Route Distribution
| Route | Count | Auto% | Success% |
|-------|-------|-------|----------|
| Sentinel | 23 | 95% | 100% |
| Zen | 45 | 92% | 98% |
| Radar | 38 | 88% | 95% |
| Atlas | 12 | 85% | 92% |
| Scout | 8 | 75% | 90% |

### Manual Override Analysis
- Total manual overrides: 12 (8%)
- Reason breakdown:
  - False positive: 5
  - Threshold adjustment needed: 4
  - Edge case: 3

### Recommendations
- Increase noise threshold to 35%
- Add exception for generated files
```
