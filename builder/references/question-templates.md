# Builder Question Templates Reference

YAML templates for `AskUserQuestion` tool at INTERACTION_TRIGGER decision points.

## ON_AMBIGUOUS_SPEC

```yaml
questions:
  - question: "There are ambiguities in the specification. How should they be interpreted?"
    header: "Specification"
    options:
      - label: "Option A: [Specific interpretation] (Recommended)"
        description: "[Rationale and impact of this interpretation]"
      - label: "Option B: [Alternative interpretation]"
        description: "[Rationale and impact of this interpretation]"
      - label: "Support both"
        description: "Make it switchable via configuration or flag"
      - label: "Clarify specification before implementation"
        description: "Pause implementation and confirm detailed specification"
    multiSelect: false
```

## ON_PERFORMANCE_CONCERN

```yaml
questions:
  - question: "There are design decisions affecting performance. How should we proceed?"
    header: "Performance"
    options:
      - label: "Implement optimization upfront (Recommended)"
        description: "Build in N+1 prevention, indexes, caching from the start"
      - label: "Simple implementation + optimize later"
        description: "Make it work first, improve after confirming bottlenecks"
      - label: "Request analysis from Tuner"
        description: "Delegate optimization to DB performance specialist agent"
    multiSelect: false
```

## ON_DB_MIGRATION

```yaml
questions:
  - question: "Introduce a new database migration?"
    header: "DB Migration"
    options:
      - label: "Review migration plan (Recommended)"
        description: "Confirm changes and rollback procedures"
      - label: "Execute as-is"
        description: "Apply migration directly"
      - label: "Defer this change"
        description: "Skip schema change and consider alternative approach"
    multiSelect: false
```

## ON_CORE_REFACTOR

```yaml
questions:
  - question: "Refactor a core utility used by the entire app?"
    header: "Core Change"
    options:
      - label: "Analyze impact first (Recommended)"
        description: "List all dependent locations for review"
      - label: "Refactor incrementally"
        description: "Split small changes across multiple PRs"
      - label: "Maintain current state"
        description: "Skip core utility changes"
    multiSelect: false
```

## ON_PATTERN_CHOICE

```yaml
questions:
  - question: "Which DDD pattern should be applied?"
    header: "DDD Pattern"
    options:
      - label: "Entity (Recommended)"
        description: "Persistent object identified by ID"
      - label: "Value Object"
        description: "Immutable object compared by value"
      - label: "Aggregate Root"
        description: "Boundary grouping related entities"
      - label: "Domain Service"
        description: "Logic not belonging to a single entity"
    multiSelect: false
```
