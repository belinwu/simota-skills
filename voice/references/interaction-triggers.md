# Voice - Interaction Trigger Templates

## ON_SURVEY_DESIGN

```yaml
questions:
  - question: "Please select a feedback collection method."
    header: "Collection Method"
    options:
      - label: "NPS survey (Recommended)"
        description: "Collect standardized loyalty metrics"
      - label: "CSAT survey"
        description: "Measure satisfaction at specific touchpoints"
      - label: "Open feedback"
        description: "Collect free-form feedback"
      - label: "In-app widget"
        description: "Collect feedback in real-time during usage"
    multiSelect: false
```

## ON_COLLECTION_METHOD

```yaml
questions:
  - question: "Please select feedback timing."
    header: "Timing"
    options:
      - label: "After action completion (Recommended)"
        description: "Send after purchase, feature use, etc."
      - label: "Periodic"
        description: "Run NPS surveys monthly/quarterly"
      - label: "At churn"
        description: "Collect reasons at cancellation or churn"
      - label: "Always available"
        description: "Keep feedback widget always present"
    multiSelect: true
```

## ON_INSIGHT_ACTION

```yaml
questions:
  - question: "Please select actions based on feedback."
    header: "Action"
    options:
      - label: "Feature improvement"
        description: "Fix issues in existing features"
      - label: "New feature proposal"
        description: "Add new features to roadmap"
      - label: "UX improvement"
        description: "Solve usability issues"
      - label: "Communication improvement"
        description: "Improve explanations and guidance"
    multiSelect: true
```
