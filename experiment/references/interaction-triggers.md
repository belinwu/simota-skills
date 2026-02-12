# Interaction Trigger Question Templates

## ON_HYPOTHESIS

```yaml
questions:
  - question: "Please select the hypothesis you want to test in this experiment."
    header: "Hypothesis Type"
    options:
      - label: "Conversion improvement (Recommended)"
        description: "Improve completion rate of specific actions"
      - label: "Engagement improvement"
        description: "Improve user frequency or session duration"
      - label: "Retention improvement"
        description: "Improve user retention rate"
      - label: "Revenue improvement"
        description: "Improve ARPU/LTV"
    multiSelect: false
```

## ON_METRIC_SELECTION

```yaml
questions:
  - question: "Please select the measurement method for the primary metric."
    header: "Metric Type"
    options:
      - label: "Binary metric (Recommended)"
        description: "Measured as Yes/No, such as conversion rate"
      - label: "Continuous metric"
        description: "Measured as numeric value, such as average purchase amount"
      - label: "Ratio metric"
        description: "Measured as numerator/denominator, such as click-through rate"
    multiSelect: false
```

## ON_EARLY_STOPPING

```yaml
questions:
  - question: "Please select the reason for stopping the experiment early."
    header: "Early Stop Reason"
    options:
      - label: "Guardrail violation"
        description: "Negative impact on user experience detected"
      - label: "Technical issues"
        description: "Bugs or tracking errors occurred"
      - label: "Business requirements changed"
        description: "Priorities or direction changed"
      - label: "Continue"
        description: "Continue experiment as planned"
    multiSelect: false
```
