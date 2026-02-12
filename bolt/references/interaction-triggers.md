# Interaction Trigger Templates

Use `AskUserQuestion` tool at decision points. See `_common/INTERACTION.md` for standard formats.

## ON_PERF_TRADEOFF

```yaml
questions:
  - question: "There are tradeoffs in performance improvement. Which approach would you like to take?"
    header: "Optimization Policy"
    options:
      - label: "Maintain readability (Recommended)"
        description: "Modest performance improvement while maintaining code maintainability"
      - label: "Prioritize performance"
        description: "Aim for maximum speed improvement, accept complexity"
      - label: "Present both options"
        description: "Implement both approaches for comparison"
    multiSelect: false
```

## ON_CACHE_STRATEGY

```yaml
questions:
  - question: "Please select a cache strategy."
    header: "Cache"
    options:
      - label: "In-memory cache (Recommended)"
        description: "Simple with no dependencies, for single instance"
      - label: "Redis/External cache"
        description: "Supports distributed environment, requires additional infrastructure"
      - label: "HTTP cache headers"
        description: "Client-side cache, requires API changes"
    multiSelect: false
```

## ON_BREAKING_OPTIMIZATION

```yaml
questions:
  - question: "This optimization may affect APIs or behavior. How would you like to proceed?"
    header: "Breaking Optimization"
    options:
      - label: "Investigate impact scope (Recommended)"
        description: "Present list of affected code before making changes"
      - label: "Consider non-breaking alternatives"
        description: "Find alternative approaches that maintain compatibility"
      - label: "Execute changes"
        description: "Implement optimization with understanding of the impact"
    multiSelect: false
```

## ON_BUNDLE_STRATEGY

```yaml
questions:
  - question: "Please select a bundle optimization approach."
    header: "Bundle Optimization"
    options:
      - label: "Route-based splitting (Recommended)"
        description: "Code split by page, most effective"
      - label: "Component-based splitting"
        description: "Split by large component units"
      - label: "Library replacement"
        description: "Replace heavy libraries with lightweight alternatives"
    multiSelect: false
```
