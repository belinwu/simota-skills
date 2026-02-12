# Grove Interaction Triggers

Question templates for `AskUserQuestion` at decision points.

---

## ON_STRUCTURE_CHOICE

```yaml
questions:
  - question: "Multiple valid directory structures. Which approach?"
    header: "Structure"
    options:
      - label: "Feature-based (Recommended)"
        description: "Group by feature/domain. Best for most projects"
      - label: "Layer-based"
        description: "Group by technical layer (controllers/services/models)"
      - label: "Hybrid"
        description: "Features for domain, shared for cross-cutting concerns"
    multiSelect: false
```

---

## ON_MIGRATION_RISK

```yaml
questions:
  - question: "Migration involves moving 50+ files. How to proceed?"
    header: "Migration"
    options:
      - label: "Incremental PRs (Recommended)"
        description: "One module per PR, safest approach"
      - label: "Single PR"
        description: "All changes in one PR, faster but higher risk"
      - label: "Create migration plan only"
        description: "Document plan without executing"
    multiSelect: false
```

---

## ON_AUDIT_RESULTS

```yaml
questions:
  - question: "Structure audit found issues. How to handle?"
    header: "Audit"
    options:
      - label: "Fix high severity only (Recommended)"
        description: "Address God Directory, Doc Desert, Missing Specs"
      - label: "Fix all issues"
        description: "Comprehensive restructure"
      - label: "Generate report only"
        description: "Document issues for later"
    multiSelect: false
```
