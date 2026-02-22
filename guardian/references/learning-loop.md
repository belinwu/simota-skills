# Learning Feedback Loop Reference

Guardian's mechanism for learning from Judge feedback and improving prediction accuracy.

## Overview

The Learning Feedback Loop enables Guardian to:
- Incorporate Judge review findings into future predictions
- Calibrate quality scores based on actual review outcomes
- Store and apply project-specific patterns
- Continuously improve accuracy over time

**Expected Impact**: Quality score accuracy improvement by **25%**

---

## Feedback Sources

### Judge Feedback Processing

```yaml
judge_feedback_sources:
  review_completion:
    trigger: "JUDGE_TO_GUARDIAN_FEEDBACK received"
    data:
      - Issues found by Judge
      - Severity classifications
      - Fix patterns applied
      - False positives identified

  verdict_tracking:
    approved:
      meaning: "Guardian's assessment was accurate"
      action: "Reinforce current patterns"
    changes_requested:
      meaning: "Issues missed by prediction"
# ...
```

### Zen Feedback Processing

```yaml
zen_feedback_sources:
  refactoring_outcomes:
    trigger: "ZEN_TO_GUARDIAN_HANDOFF received"
    data:
      - Suggestions accepted vs rejected
      - Refactoring types applied
      - Project-specific preferences

  pattern_learning:
    accepted_suggestions:
      action: "Increase pattern weight"
    rejected_suggestions:
      action: "Decrease pattern weight, add exception"
```

---

## JUDGE_TO_GUARDIAN_FEEDBACK Handoff

### Request Format

```markdown
## JUDGE_TO_GUARDIAN_FEEDBACK

**PR**: #123 - feat(auth): add OAuth2 support
**Review Status**: CHANGES_REQUESTED

### Guardian's Predictions vs Actual Findings

| Predicted Issue | Predicted Severity | Actual Finding | Match |
|-----------------|-------------------|----------------|-------|
| Null pointer oauth.ts:45 | HIGH | Confirmed | TRUE_POSITIVE |
| Race condition token.ts:33 | MEDIUM | Not found | FALSE_POSITIVE |
| - | - | XSS in callback.ts:72 | FALSE_NEGATIVE |
| Large function oauth.ts | HIGH | Confirmed | TRUE_POSITIVE |

### Prediction Accuracy for This PR
...
```

### Response Processing

```yaml
feedback_processing:
  on_receive:
    1: "Parse prediction comparison"
    2: "Update pattern weights"
    3: "Add new patterns if needed"
    4: "Store project preferences"
    5: "Recalibrate thresholds"

  actions:
    true_positive:
      - Increase pattern confidence by 5%
      - Log successful detection

    false_positive:
      - Decrease pattern confidence by 10%
# ...
```

---

## Calibration Mechanism

### Pattern Weight Calibration

```yaml
pattern_calibration:
  initial_confidence: 70%
  adjustment_rules:
    true_positive: "+5% confidence (max 95%)"
    false_positive: "-10% confidence (min 30%)"
    false_negative: "+10% sensitivity for similar"

  threshold_calibration:
    trigger: "3 consecutive same-direction adjustments"
    action: "Review and permanently adjust threshold"

  project_specific:
    storage: ".agents/guardian.md"
    format: "YAML metadata block"
    includes:
# ...
```

### Quality Score Calibration

```yaml
quality_calibration:
  tracking:
    - Guardian's predicted quality score
    - Actual review cycles needed
    - Final merge success/failure

  correlation_analysis:
    excellent_prediction:
      predicted: "A+ (95+)"
      actual_cycles: "<= 1"
      correlation: "Accurate"

    poor_prediction:
      predicted: "A (85-94)"
      actual_cycles: "> 2"
# ...
```

---

## Project-Specific Storage

### .agents/guardian.md Format

```markdown
# Guardian Calibration Data

## Last Updated
{timestamp}

## Pattern Exceptions

### Naming Patterns
```yaml
exceptions:
  - pattern: generic_names
    scope: "**/*.test.ts"
    reason: "Test files allow generic names"
  - pattern: magic_numbers
    scope: "**/constants/**"
    reason: "Constants files define magic numbers"
```

### Complexity Thresholds
```yaml
custom_thresholds:
  god_function:
    default: 50
    custom: 80
    scope: "**/validators/**"
    reason: "Validators are intentionally comprehensive"

  deep_nesting:
    default: 4
    custom: 6
    scope: "**/parsers/**"
    reason: "Parser logic requires deep nesting"
```

## Team Preferences

```yaml
preferences:
  null_handling:
    preferred: "explicit_check"
    avoid: "optional_chaining"
    reason: "Team preference for explicit guards"

  naming_convention:
    variables: "camelCase"
    constants: "SCREAMING_SNAKE"
    files: "kebab-case"
```

## Historical Accuracy

### Last 30 Days
```yaml
accuracy:
  judge_predictions:
    total: 145
    true_positives: 98
    false_positives: 25
    false_negatives: 22
    accuracy: 67.6%

  zen_predictions:
    total: 230
    accepted: 185
    rejected: 45
    acceptance_rate: 80.4%

  quality_scores:
    correlation: 0.78
    avg_deviation: 8.3%
```

## Pattern Weights

```yaml
pattern_weights:
  null_pointer:
    default: 85%
    current: 88%
    last_adjusted: {date}

  race_condition:
    default: 75%
    current: 65%
    last_adjusted: {date}
    note: "Decreased due to false positives in this codebase"

  generic_naming:
    default: 90%
    current: 85%
    last_adjusted: {date}
    exceptions: ["test files", "mocks"]
```
```

---

## Learning Loop Workflow

```
┌─────────────────────────────────────┐
│    Guardian Makes Predictions        │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│    Judge Reviews PR                  │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│    JUDGE_TO_GUARDIAN_FEEDBACK        │
│    - Compare predictions vs actual   │
│    - Identify TP/FP/FN              │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
...
```

---

## Continuous Improvement Metrics

### Tracking Dashboard

```yaml
learning_metrics:
  prediction_accuracy:
    target: "> 75%"
    current: "Track from feedback"
    trend: "Improving/Stable/Declining"

  false_positive_rate:
    target: "< 20%"
    current: "Track from feedback"
    impact: "Reduces unnecessary flags"

  false_negative_rate:
    target: "< 15%"
    current: "Track from feedback"
    impact: "Catches more issues pre-review"
# ...
```

### Improvement Actions

```yaml
improvement_actions:
  weekly_review:
    - Check accuracy trends
    - Review new false negatives
    - Adjust thresholds if needed

  monthly_calibration:
    - Full pattern weight review
    - Quality score correlation check
    - Project preference audit

  quarterly_assessment:
    - Learning effectiveness report
    - Pattern library review
    - Cross-project pattern sharing
```

---

## Squash Learning

### Feedback Sources

```yaml
squash_feedback_sources:
  user_rebase_acceptance:
    trigger: "User executes or modifies Guardian's rebase script"
    data:
      accepted_as_is: "Reinforce current scoring thresholds"
      modified_script: "Analyze delta — which groups were changed?"
      rejected: "Review scoring factors for this branch"

  judge_post_squash_review:
    trigger: "JUDGE_TO_GUARDIAN_FEEDBACK after squashed PR review"
    data:
      commit_quality_scores: "Per-commit message quality assessment"
      atomicity_issues: "Were squashed commits still multi-concern?"
      attribution_issues: "Were Co-authored-by lines missing?"
```

### Calibration Rules

```yaml
squash_calibration:
  threshold_adjustment:
    trigger: "3 consecutive over-squash OR under-squash signals"
    over_squash_signals:
      - "User splits Guardian's squash groups"
      - "Judge flags atomicity issues after squash"
      - "User adds commits that were fixuped"
    under_squash_signals:
      - "User further squashes Guardian's pick recommendations"
      - "Judge recommends squashing commits Guardian kept separate"
    adjustment: "±5 points on squash_threshold"
    bounds:
      min_threshold: "+5"   # Never auto-squash everything
      max_threshold: "+45"  # Never refuse to squash

  factor_weight_tuning:
    trigger: "5+ data points on specific factor misalignment"
    example: "If file_overlap consistently under-weighted → increase by 5pt"
    bounds:
      min_weight: 5
      max_weight: 35
    note: "Total weight across 6 factors should remain ~100"
```

### Storage

```yaml
squash_calibration_storage:
  location: ".agents/guardian.md → squash_calibration"
  format: |
    ## Squash Calibration
    ```yaml
    squash_thresholds:
      strong_squash: 30    # default 30, adjusted from feedback
      suggest_squash: 15   # default 15
    factor_adjustments:
      temporal_proximity: 0   # delta from default weight
      subject_relationship: 0
      file_overlap: 0
      author_attribution: 0
      atomicity_impact: 0
      test_coupling: 0
    last_calibrated: {timestamp}
    data_points: {count}
    ```
```

---

## AUTORUN Integration

```yaml
autorun_learning:
  auto_actions:
    - Apply current calibration
    - Use project-specific exceptions
    - Track predictions for feedback

  feedback_processing:
    mode: BATCH
    timing: "After PR merge or close"
    action: "Process all feedback, update calibration"

  storage_update:
    frequency: "After each feedback round"
    validation: "Ensure no regression in accuracy"
```

---

## Harvest Data Integration

### Historical Pattern Mining

```yaml
harvest_integration:
  data_request:
    type: HARVEST_TO_GUARDIAN_HANDOFF
    includes:
      - Historical issue patterns
      - Common review findings
      - Team-specific preferences
      - Seasonal trends

  pattern_extraction:
    from_history:
      - Frequently flagged issues
      - Common fixes applied
      - Reviewer preferences

# ...
```

### Cross-PR Learning

```yaml
cross_pr_learning:
  similar_pr_detection:
    criteria:
      - Same files modified
      - Same author
      - Similar change type

  outcome_prediction:
    source: "Historical similar PRs"
    factors:
      - Review cycles needed
      - Issues found
      - Final outcome

  calibration_input:
# ...
```
