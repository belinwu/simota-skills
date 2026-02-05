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
      action: "Analyze gaps, update patterns"
    blocked:
      meaning: "Critical issues missed"
      action: "Review prediction thresholds"

  issue_categorization:
    bugs: "Logic errors, null pointers, race conditions"
    security: "Vulnerabilities, injection risks"
    quality: "Naming, structure, complexity"
    tests: "Missing coverage, weak assertions"
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
- True Positives: 2
- False Positives: 1
- False Negatives: 1
- Accuracy: 50%

### New Issues Found by Judge (Missed by Guardian)
| File | Line | Issue | Severity | Pattern to Add |
|------|------|-------|----------|----------------|
| callback.ts | 72 | XSS via innerHTML | HIGH | dangerous_dom_manipulation |
| handler.ts | 45 | Unhandled rejection | MEDIUM | async_error_handling |

### Project-Specific Observations
- Team prefers explicit null checks over optional chaining
- Magic numbers in constants.ts are acceptable
- Complex conditions in validators are allowed

### Calibration Suggestions
- Increase innerHTML detection sensitivity
- Add async error handling pattern
- Decrease false positive rate for race conditions
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
      - Review triggering conditions
      - Add exception if project-specific

    false_negative:
      - Add new pattern if repeated
      - Increase detection sensitivity
      - Lower threshold for similar patterns
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
      - Pattern exceptions
      - Custom thresholds
      - Team preferences
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
      correlation: "Overestimated"

  adjustment:
    overestimated:
      action: "Lower scores by observed gap"
      example: "If predicted A but took 3 cycles, reduce future similar by 10%"

    underestimated:
      action: "Raise scores by observed gap"
      example: "If predicted B but merged in 1 cycle, increase future similar by 5%"
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
│    Process Feedback                  │
│    - Update pattern weights          │
│    - Add new patterns if needed      │
│    - Store exceptions                │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│    Save to .agents/guardian.md       │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│    Apply to Future PRs               │
└─────────────────────────────────────┘
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

  quality_score_correlation:
    target: "> 0.80"
    current: "Track from outcomes"
    impact: "More accurate quality assessment"

  review_cycle_reduction:
    target: "1 cycle average"
    baseline: "Historical average"
    improvement: "Track delta"
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

  application:
    - Seed initial predictions
    - Validate against history
    - Detect pattern drift
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
    - Use historical outcomes
    - Weight recent more heavily
    - Adjust for context differences
```
