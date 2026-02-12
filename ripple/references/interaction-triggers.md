# Interaction Triggers - Question Templates

Use `AskUserQuestion` tool at these decision points. See `_common/INTERACTION.md` for standard formats.

## ON_HIGH_RISK

```yaml
questions:
  - question: "High risk detected (score: X/10). How would you like to proceed?"
    header: "Risk Level"
    options:
      - label: "Review detailed analysis (Recommended)"
        description: "Examine full impact report before deciding"
      - label: "Proceed with mitigation plan"
        description: "Continue with documented risk mitigations"
      - label: "Reduce scope"
        description: "Break into smaller, lower-risk changes"
      - label: "Defer change"
        description: "Postpone until better understood"
    multiSelect: false
```

## ON_BREAKING_CHANGE

```yaml
questions:
  - question: "Breaking change detected. This will affect X dependent files. How would you like to handle this?"
    header: "Breaking Change"
    options:
      - label: "Add compatibility layer (Recommended)"
        description: "Maintain old API while introducing new one"
      - label: "Coordinate bulk update"
        description: "Update all dependents simultaneously"
      - label: "Document as breaking"
        description: "Proceed with breaking change, update CHANGELOG"
      - label: "Redesign approach"
        description: "Find alternative that avoids breaking changes"
    multiSelect: false
```

## ON_PATTERN_CONFLICT

```yaml
questions:
  - question: "The proposed change deviates from established patterns. Which approach would you prefer?"
    header: "Pattern Policy"
    options:
      - label: "Follow existing pattern (Recommended)"
        description: "Modify approach to match project conventions"
      - label: "Document as intentional deviation"
        description: "Proceed with deviation, add ADR explaining why"
      - label: "Propose pattern update"
        description: "Start RFC to update project-wide pattern"
    multiSelect: false
```

## ON_SCOPE_EXPANSION

```yaml
questions:
  - question: "Impact scope is larger than expected (X files affected vs Y estimated). How should we proceed?"
    header: "Scope Change"
    options:
      - label: "Continue with full scope"
        description: "Accept larger scope and proceed"
      - label: "Break into phases (Recommended)"
        description: "Split into smaller, manageable changes"
      - label: "Re-evaluate approach"
        description: "Consider alternative with smaller footprint"
    multiSelect: false
```

## ON_COVERAGE_GAP

```yaml
questions:
  - question: "Test coverage gap detected in affected areas. Recommended action?"
    header: "Test Coverage"
    options:
      - label: "Add tests before change (Recommended)"
        description: "Establish baseline tests first via Radar"
      - label: "Add tests after change"
        description: "Proceed now, add tests later"
      - label: "Accept risk"
        description: "Proceed without additional tests"
    multiSelect: false
```
