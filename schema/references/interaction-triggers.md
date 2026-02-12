# Interaction Trigger Templates

## ON_SCHEMA_DESIGN

```yaml
questions:
  - question: "Proceed with this table design?"
    header: "Schema Confirmation"
    options:
      - label: "Proceed with this design (Recommended)"
        description: "Implement with proposed table structure"
      - label: "Adjust relations"
        description: "Modify relationships between tables"
      - label: "Change normalization level"
        description: "Consider denormalization for performance"
    multiSelect: false
```

## ON_BREAKING_CHANGE

```yaml
questions:
  - question: "This change affects existing data. Continue?"
    header: "Breaking Change"
    options:
      - label: "Continue with backup"
        description: "Back up data before running migration"
      - label: "Switch to gradual migration"
        description: "Use migration strategy with old/new columns coexisting"
      - label: "Abort"
        description: "Cancel this change"
    multiSelect: false
```
