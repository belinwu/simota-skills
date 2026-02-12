# Interaction Trigger Templates

## ON_METRIC_DEFINITION

```yaml
questions:
  - question: "Please select the North Star metric for this product."
    header: "Success Metric"
    options:
      - label: "Active users (Recommended)"
        description: "Measure growth with DAU/WAU/MAU"
      - label: "Conversion rate"
        description: "Measure completion rate of specific actions"
      - label: "Retention rate"
        description: "Measure continued usage rate"
      - label: "Revenue metrics"
        description: "Measure ARPU/LTV/MRR"
    multiSelect: false
```

## ON_EVENT_SCHEMA

```yaml
questions:
  - question: "Please select event schema design approach."
    header: "Event Design"
    options:
      - label: "Simple (Recommended)"
        description: "Start with minimum required properties"
      - label: "Detailed"
        description: "Include detailed properties for future analysis"
      - label: "Follow existing schema"
        description: "Match existing event structure"
    multiSelect: false
```

## ON_PLATFORM_CHOICE

```yaml
questions:
  - question: "Please select an analytics platform."
    header: "Analytics Platform"
    options:
      - label: "GA4 (Recommended)"
        description: "Free basic analytics capability"
      - label: "Amplitude"
        description: "Advanced tool specialized for product analytics"
      - label: "Mixpanel"
        description: "Detailed event-based analytics capability"
      - label: "Custom"
        description: "Use in-house data platform"
    multiSelect: false
```
