# Interaction Trigger Templates

YAML templates for `AskUserQuestion` tool. See `_common/INTERACTION.md` for standard formats.

## ON_FRAMEWORK_REPLACE

```yaml
questions:
  - question: "Replace core framework? This is a large-scale change."
    header: "FW Replace"
    options:
      - label: "Investigate impact first (Recommended)"
        description: "Analyze impact scope and migration cost"
      - label: "Plan gradual migration"
        description: "Migrate gradually using Strangler Fig pattern"
      - label: "Skip this change"
        description: "Maintain current framework"
    multiSelect: false
```

## ON_HEAVY_LIBRARY

```yaml
questions:
  - question: "Add dependency over 30KB?"
    header: "Heavy Dependency"
    options:
      - label: "Use native API instead (Recommended)"
        description: "Consider if browser standard features can substitute"
      - label: "Check bundle size and add"
        description: "Measure actual impact before deciding"
      - label: "Don't add"
        description: "Skip adding this dependency"
    multiSelect: false
```

## ON_TECH_MIGRATION

```yaml
questions:
  - question: "Please select migration strategy for deprecated library."
    header: "Migration Strategy"
    options:
      - label: "Strangler Fig pattern (Recommended)"
        description: "Migrate gradually with old/new running in parallel"
      - label: "Branch by Abstraction"
        description: "Introduce abstraction layer before replacing"
      - label: "Parallel Run"
        description: "Run both old and new, compare results for verification"
    multiSelect: false
```
