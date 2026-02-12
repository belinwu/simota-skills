# Interaction Triggers - Question Templates

Use `AskUserQuestion` tool to confirm with user at these decision points.
See `_common/INTERACTION.md` for standard formats.

## ON_ARCH_DECISION

```yaml
questions:
  - question: "Proposing an architecture pattern change. Which direction would you like to take?"
    header: "Design Policy"
    options:
      - label: "Gradual migration (Recommended)"
        description: "Migrate to new pattern gradually while maintaining existing code"
      - label: "Apply to new parts only"
        description: "Apply new pattern only to new development, leave existing code untouched"
      - label: "Investigate impact scope"
        description: "Present list of affected modules before making changes"
    multiSelect: false
```

## ON_BREAKING_DEPENDENCY

```yaml
questions:
  - question: "Breaking changes to dependencies are required. How would you like to handle this?"
    header: "Dependency Change"
    options:
      - label: "Add compatibility layer (Recommended)"
        description: "Migrate internal implementation to new structure while maintaining existing API"
      - label: "Execute bulk changes"
        description: "Update all affected areas simultaneously"
      - label: "Defer changes"
        description: "Do not change at this time, consider alternatives"
    multiSelect: false
```

## ON_ADR_CREATION

```yaml
questions:
  - question: "Would you like to create an ADR (Architecture Decision Record)?"
    header: "ADR Creation"
    options:
      - label: "Create ADR (Recommended)"
        description: "Document background, rationale, and tradeoffs of the decision"
      - label: "Brief notes only"
        description: "Lightly record in PR description or comments"
      - label: "No documentation needed"
        description: "Skip documentation for small-scale changes"
    multiSelect: false
```

## ON_TECH_DEBT_PRIORITY

```yaml
questions:
  - question: "Multiple technical debts were found. Which would you like to address first?"
    header: "Debt Priority"
    options:
      - label: "Highest impact (Recommended)"
        description: "Address debt affecting the most code first"
      - label: "Lowest fix cost"
        description: "Quick wins for fast improvement"
      - label: "Highest risk"
        description: "Prioritize debt related to security or stability"
    multiSelect: false
```
