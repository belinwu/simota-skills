# Question Templates

Standard question templates for Sherpa's INTERACTION_TRIGGERS decision points.
See `_common/INTERACTION.md` for standard formats.

---

## BEFORE_DECOMPOSITION

```yaml
questions:
  - question: "How should I approach breaking down this task?"
    header: "Approach"
    options:
      - label: "Incremental with checkpoints (Recommended)"
        description: "Confirm completion at each step before proceeding"
      - label: "Show full plan first"
        description: "Present entire breakdown, then start first step"
      - label: "Minimal steps"
        description: "Larger chunks for faster progress"
    multiSelect: false
```

## ON_SCOPE_UNCLEAR

```yaml
questions:
  - question: "Task scope is unclear. What should be included?"
    header: "Scope"
    options:
      - label: "Minimum viable only"
        description: "Core functionality only, defer extras"
      - label: "Include related features"
        description: "Address surrounding concerns as well"
      - label: "Need more details"
        description: "Request Scout investigation first"
    multiSelect: false
```

## ON_HIGH_RISK

```yaml
questions:
  - question: "This step has high risk. How to proceed?"
    header: "Risk"
    options:
      - label: "Investigate first (Recommended)"
        description: "Request Scout investigation before starting"
      - label: "Proceed with caution"
        description: "Start but monitor closely, prepare fallback"
      - label: "Find alternative approach"
        description: "Look for lower-risk solution"
    multiSelect: false
```

## ON_BLOCKER_DETECTED

```yaml
questions:
  - question: "External blocker detected. How to handle?"
    header: "Blocker"
    options:
      - label: "Work around with mock (Recommended)"
        description: "Create mock/stub to unblock progress"
      - label: "Wait for resolution"
        description: "Pause this path, work on parallel tasks"
      - label: "Escalate immediately"
        description: "This is critical, needs immediate attention"
    multiSelect: false
```
