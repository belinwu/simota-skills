# Interaction Triggers Reference

## ON_SCOPE_AMBIGUOUS

```yaml
questions:
  - question: "This question could refer to multiple areas. Which scope should I investigate?"
    header: "Scope"
    options:
      - label: "[Module/Feature A] (Recommended)"
        description: "[Brief description of what this covers]"
      - label: "[Module/Feature B]"
        description: "[Brief description of what this covers]"
      - label: "All of the above"
        description: "Investigate all matching areas (takes longer)"
    multiSelect: false
```

## ON_MULTIPLE_MATCHES

```yaml
questions:
  - question: "Found multiple implementations matching your query. Which should I investigate?"
    header: "Target"
    options:
      - label: "[Implementation A] (Recommended)"
        description: "[File path and brief context]"
      - label: "[Implementation B]"
        description: "[File path and brief context]"
      - label: "Compare all"
        description: "Analyze and compare all implementations"
    multiSelect: false
```
