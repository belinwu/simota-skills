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
        - "Multiple setState/dispatch in async"
        - "No mutex or lock pattern"
        - "Shared mutable state"
      prediction_confidence: 75%

    off_by_one:
      pattern: "boundary_calculation"
      example: "Array index or loop boundary"
      detection:
        - "Manual index calculations"
        - "Loop with <= vs <"
        - "Substring with length"
      prediction_confidence: 70%

    resource_leak:
      pattern: "unmanaged_resource"
      example: "File handle not closed"
      detection:
        - "Resource opened without try-finally"
        - "No using/with statement"
        - "Missing cleanup in error path"
      prediction_confidence: 80%

  security_issues:
    injection:
      pattern: "unsanitized_input"
      example: "User input in SQL/HTML"
      detection:
        - "String concatenation with user input"
        - "Template literals with request params"
        - "No sanitization function call"
      prediction_confidence: 90%

    auth_bypass:
      pattern: "missing_auth_check"
      example: "Endpoint without auth middleware"
      detection:
        - "Route without auth decorator"
        - "Missing permission check"
        - "Early return before auth"
      prediction_confidence: 85%

  logic_errors:
    inverted_condition:
      pattern: "condition_inversion"
      example: "if (!valid) proceed instead of if (valid)"
      detection:
        - "Negated boolean in condition"
        - "Early return logic"
        - "Guard clause patterns"
      prediction_confidence: 65%

    missing_case:
      pattern: "incomplete_switch"
      example: "Switch without default/exhaustive"
      detection:
        - "Switch statement"
        - "No default case"
        - "Enum not fully covered"
      prediction_confidence: 80%
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
    low_confidence: "Include in suggestions only"
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
        - "Multiple naming styles in same file"
        - "Different from project convention"
      prediction_confidence: 85%

  structure:
    god_function:
      pattern: "function_too_large"
      threshold: "> 50 lines or > 5 responsibilities"
      detection:
        - "Function line count"
        - "Multiple distinct operations"
        - "Nested conditionals > 3 levels"
      prediction_confidence: 80%

    magic_numbers:
      pattern: "hardcoded_literals"
      examples: ["if (status === 3)", "timeout = 5000"]
      detection:
        - "Numeric literals in conditions"
        - "String literals not from constants"
        - "Unexplained numbers"
      prediction_confidence: 85%

    duplication:
      pattern: "code_duplication"
      threshold: "> 5 lines repeated"
      detection:
        - "Similar code blocks"
        - "Copy-paste patterns"
        - "Repeated logic"
      prediction_confidence: 75%

  complexity:
    deep_nesting:
      pattern: "excessive_nesting"
      threshold: "> 4 levels"
      detection:
        - "Count nesting depth"
        - "Multiple nested callbacks"
        - "Chained conditionals"
      prediction_confidence: 90%

    complex_conditional:
      pattern: "boolean_complexity"
      threshold: "> 3 conditions in single expression"
      detection:
        - "Multiple && or || operators"
        - "Nested ternaries"
        - "Complex boolean algebra"
      prediction_confidence: 85%

  best_practices:
    missing_error_handling:
      pattern: "unhandled_promise"
      detection:
        - "Promise without .catch()"
        - "Async without try-catch"
        - "Callback without error param"
      prediction_confidence: 85%

    type_coercion:
      pattern: "implicit_conversion"
      examples: ["== instead of ===", "+ for string concat"]
      detection:
        - "Loose equality"
        - "Type mixing in operations"
      prediction_confidence: 80%
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
      - Track by file type/directory
      - Note author patterns

    effectiveness_tracking:
      - Did fix resolve the issue?
      - Was suggestion accepted?
      - Did it prevent future issues?

  model_calibration:
    update_frequency: "After each review cycle"
    confidence_adjustment: "+/-5% based on accuracy"
    false_positive_threshold: "> 20% triggers review"
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

| Priority | File | Line | Issue | Confidence |
|----------|------|------|-------|------------|
| HIGH | oauth.ts | 20-80 | Function too large (65 lines) | 90% |
| HIGH | handler.ts | 45 | Magic number: 3600 | 85% |
| MEDIUM | callback.ts | 30-35 | Nested callbacks > 4 | 85% |
| MEDIUM | token.ts | 10 | Generic name: 'data' | 90% |
| LOW | utils.ts | 55-60 | Similar to lines 25-30 | 75% |

### Recommended Pre-Review Fixes

**High Priority** (Will likely be flagged):
1. `oauth.ts:45` - Add null check for user.profile
2. `oauth.ts:20-80` - Split into smaller functions
3. `callback.ts:72` - Add try-catch for async operation
4. `handler.ts:45` - Extract 3600 to TOKEN_EXPIRY constant

**Medium Priority** (May be flagged):
1. `token.ts:10` - Rename 'data' to 'tokenPayload'
2. `callback.ts:30-35` - Flatten nested callbacks

### Impact if Fixed Pre-Review

- Estimated Judge issues prevented: 4
- Estimated Zen suggestions addressed: 5
- Predicted review cycles saved: 1
- Quality score improvement: +8 points
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
      description: "Proceed with predictions as warnings"
      benefit: "Faster initial review"

    request_zen:
      description: "Auto-fix code quality issues via Zen"
      benefit: "Automated cleanup"
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

  output:
    predictions:
      judge:
        high: 2
        medium: 2
        low: 1
      zen:
        high: 3
        medium: 2
        low: 1
    pre_fix_recommended: true
    estimated_savings: "1 review cycle"
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
      - Review pattern conditions
      - Add exception if project-specific

    on_false_negative:
      - Add new pattern if repeated
      - Increase similar pattern weight
      - Review detection rules
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
| True Positives | 185 |
| False Positives | 35 |
| False Negatives | 10 |
| **Accuracy** | **80.4%** |

### Top False Positives
1. Generic names in test files (15)
2. Magic numbers in config (8)
3. Complex conditions in validators (7)

### Recommended Adjustments
- Exclude test files from naming checks
- Add config file exception for magic numbers
- Increase complexity threshold for validators
```
