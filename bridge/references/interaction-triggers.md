# Bridge Interaction Trigger Templates

Use `AskUserQuestion` tool at these decision points. See `_common/INTERACTION.md` for standard formats.

---

## ON_REQUIREMENT_AMBIGUITY

```yaml
questions:
  - question: "This requirement has multiple valid interpretations. Which interpretation should we proceed with?"
    header: "Interpretation"
    options:
      - label: "Interpretation A: [specific interpretation]"
        description: "[Meaning and impact of this interpretation]"
      - label: "Interpretation B: [specific interpretation]"
        description: "[Meaning and impact of this interpretation]"
      - label: "Need stakeholder confirmation"
        description: "Gather additional context before deciding"
    multiSelect: false
```

## ON_SCOPE_CHANGE_DETECTED

```yaml
questions:
  - question: "Scope change detected. How should we proceed?"
    header: "Scope"
    options:
      - label: "Approve change and assess impact (Recommended)"
        description: "Clarify schedule/resource impact and proceed"
      - label: "Maintain original scope"
        description: "Move additional requirements to backlog"
      - label: "Redefine scope"
        description: "Review priorities together with stakeholders"
    multiSelect: false
```

## ON_STAKEHOLDER_CONFLICT

```yaml
questions:
  - question: "There is a gap in stakeholder expectations. How should we align?"
    header: "Alignment"
    options:
      - label: "Identify common priorities (Recommended)"
        description: "Define MVP scope that both parties can agree on"
      - label: "Propose phased approach"
        description: "Split into phases to satisfy both requirements"
      - label: "Escalate to decision maker"
        description: "Seek higher-level judgment"
    multiSelect: false
```

## ON_FEASIBILITY_CONCERN

```yaml
questions:
  - question: "There are concerns about technical feasibility. How should we proceed?"
    header: "Feasibility"
    options:
      - label: "Conduct technical investigation (Recommended)"
        description: "Request detailed feasibility assessment from Atlas/Builder"
      - label: "Present alternatives"
        description: "Propose approach within feasible scope"
      - label: "Proceed with documented constraints"
        description: "Document technical limitations and share with stakeholders"
    multiSelect: false
```

## ON_TRADE_OFF_DECISION

```yaml
questions:
  - question: "Trade-off required. Which direction should we prioritize?"
    header: "Trade-off"
    options:
      - label: "Speed priority"
        description: "Defer some features for earlier release"
      - label: "Quality priority"
        description: "Adjust schedule for sufficient testing/review"
      - label: "Scope priority"
        description: "Add resources to include all features"
      - label: "Balanced approach (Recommended)"
        description: "Define MVP and deliver prioritized features incrementally"
    multiSelect: false
```
