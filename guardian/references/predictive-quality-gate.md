# Predictive Quality Gate Reference

Guardian's system for predicting Judge/Zen feedback before review.

## Overview

The Predictive Quality Gate analyzes code changes and predicts potential issues that Judge or Zen would typically flag, allowing preemptive fixes.

**Expected Impact**: Reduce review cycles by **1 iteration (40%)**

---

## Judge Issue Prediction

### Common Judge Findings Patterns

```yaml
judge_patterns:
  bug_detection:
    null_pointer:
      pattern: "optional_access_without_check"
      example: "user.profile.name without null check"
      detection:
        - "Accessing nested properties"
        - "No optional chaining (?.) used"
        - "No null/undefined guard"
      prediction_confidence: 85%

    race_condition:
      pattern: "async_state_mutation"
      example: "Multiple async ops on same state"
      detection:
# ...
```

### Judge Prediction Algorithm

```yaml
judge_prediction:
  analyze:
    1: "Scan changed code for known patterns"
    2: "Match against historical Judge findings"
    3: "Weight by project-specific frequency"
    4: "Calculate prediction confidence"

  scoring:
    high_confidence: ">= 80%"
    medium_confidence: "60-79%"
    low_confidence: "< 60%"

  threshold_for_warning:
    high_confidence: "Always warn"
    medium_confidence: "Warn if risk_score > 50"
# ...
```

---

## Zen Issue Prediction

### Common Zen Refactoring Patterns

```yaml
zen_patterns:
  naming:
    generic_names:
      pattern: "non_descriptive_identifier"
      examples: ["data", "temp", "result", "value", "item"]
      detection:
        - "Variable name matches generic list"
        - "Function parameter is generic"
        - "Loop variable reused"
      prediction_confidence: 90%

    inconsistent_naming:
      pattern: "mixed_conventions"
      examples: ["camelCase vs snake_case mixed"]
      detection:
# ...
```

### Zen Prediction Algorithm

```yaml
zen_prediction:
  analyze:
    1: "Apply static analysis patterns"
    2: "Compare with project style guide"
    3: "Match against historical Zen suggestions"
    4: "Prioritize by impact"

  categories:
    must_fix: "Significantly impacts readability/maintainability"
    should_fix: "Improves code quality"
    nice_to_have: "Minor improvements"
```

---

## Historical Pattern Learning

### Learning from Past Reviews

```yaml
historical_learning:
  data_sources:
    judge_reviews:
      - Issues found in past PRs
      - Fix patterns applied
      - False positives identified

    zen_refactorings:
      - Refactoring suggestions made
      - Accepted vs rejected
      - Project-specific preferences

  pattern_extraction:
    frequency_analysis:
      - Count occurrence of each issue type
# ...
```

### Project-Specific Calibration

```yaml
project_calibration:
  style_preferences:
    - Preferred naming conventions
    - Accepted complexity levels
    - Team-specific patterns

  exception_rules:
    - Generated code patterns to ignore
    - Legacy code areas with different standards
    - Third-party integration patterns

  weight_adjustments:
    - Increase weight for frequently flagged issues
    - Decrease for consistently ignored suggestions
    - Add new patterns from repeated findings
```

---

## Prediction Report

### Predictive Analysis Template

```markdown
## Predictive Quality Gate Analysis

**PR**: #123 - feat(auth): add OAuth2 support
**Files Analyzed**: 12

### Predicted Judge Findings

| Severity | File | Line | Issue | Confidence |
|----------|------|------|-------|------------|
| HIGH | oauth.ts | 45 | Potential null pointer | 85% |
| HIGH | callback.ts | 72 | Missing error handling | 80% |
| MEDIUM | token.ts | 33 | Race condition risk | 75% |
| LOW | utils.ts | 15 | Possible off-by-one | 65% |

### Predicted Zen Suggestions
...
```

---

## Integration with Review Flow

### Pre-Review Gate

```yaml
pre_review_gate:
  trigger: "Before GUARDIAN_TO_JUDGE_HANDOFF"

  actions:
    1: "Run predictive analysis"
    2: "Generate predictions report"
    3: "Calculate fix effort"
    4: "Present to developer"

  options:
    fix_now:
      description: "Address predicted issues before review"
      benefit: "Fewer review cycles"

    review_anyway:
# ...
```

### AUTORUN Integration

```yaml
autorun_prediction:
  auto_execute:
    - Run all predictions
    - Generate report
    - Include in handoff

  auto_fix:
    condition: "autorun_mode AND confidence > 90%"
    scope: "Code quality issues only (not logic bugs)"
    handoff: Zen

  pause_conditions:
    - "Predicted security issue"
    - "High confidence logic bug"
    - "Multiple conflicting fixes"
# ...
```

---

## Accuracy Tracking

### Prediction Metrics

```yaml
prediction_metrics:
  tracked:
    - true_positives: "Predicted and confirmed by reviewer"
    - false_positives: "Predicted but not flagged"
    - false_negatives: "Not predicted but found by reviewer"
    - prediction_accuracy: "TP / (TP + FP + FN)"

  targets:
    judge_accuracy: "> 75%"
    zen_accuracy: "> 80%"
    false_positive_rate: "< 20%"

  calibration:
    on_false_positive:
      - Decrease pattern confidence by 5%
# ...
```

### Accuracy Report Template

```markdown
## Prediction Accuracy Report (Last 30 Days)

### Judge Predictions
| Metric | Value |
|--------|-------|
| Predictions Made | 145 |
| True Positives | 98 |
| False Positives | 25 |
| False Negatives | 22 |
| **Accuracy** | **67.6%** |

### Zen Predictions
| Metric | Value |
|--------|-------|
| Predictions Made | 230 |
...
```
