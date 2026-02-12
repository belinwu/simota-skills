# Interaction Triggers — YAML Templates

## ON_AGENT_OVERLAP

```yaml
questions:
  - question: "Functional overlap of {overlap_percentage}% detected with existing agent '{agent}'. How do you want to proceed?"
    header: "Overlap"
    options:
      - label: "Clarify differentiation and continue (Recommended)"
        description: "Narrow scope and clearly define role separation from existing agent"
      - label: "Propose extending existing agent"
        description: "Add capabilities to {agent} instead of creating new agent"
      - label: "Redesign with agent split"
        description: "Redesign related agents including the new one"
      - label: "Cancel design"
        description: "Current ecosystem is sufficient"
    multiSelect: false
```

## ON_VALUE_UNCLEAR

```yaml
questions:
  - question: "The value proposition for this agent is unclear. Which aspect is most important?"
    header: "Value"
    options:
      - label: "Time saving (Recommended)"
        description: "Reduces time spent on specific tasks"
      - label: "Quality improvement"
        description: "Improves output quality or consistency"
      - label: "New capability"
        description: "Enables something previously impossible"
      - label: "Risk reduction"
        description: "Reduces errors or security risks"
    multiSelect: false
```

## ON_QUALITY_FEEDBACK

```yaml
questions:
  - question: "Judge reported quality issues in '{agent}' SKILL.md. How should we proceed?"
    header: "Feedback"
    options:
      - label: "Fix immediately (Recommended)"
        description: "Address high-priority issues in current session"
      - label: "Schedule for next review cycle"
        description: "Add to improvement queue for planned maintenance"
      - label: "Request more details from Judge"
        description: "Ask Judge for specific line-level feedback before acting"
    multiSelect: false
```

## ON_ENHANCEMENT_PRIORITY

```yaml
questions:
  - question: "Multiple enhancements identified for '{agent}'. Which priority tier should we implement?"
    header: "Priority"
    options:
      - label: "P1 only (Recommended)"
        description: "Implement critical gaps only — highest impact, minimal changes"
      - label: "P1 + P2"
        description: "Implement critical gaps and important improvements"
      - label: "All (P1 + P2 + P3)"
        description: "Comprehensive enhancement — most changes, highest effort"
    multiSelect: false
```

## ON_COMPRESSION_SCOPE

```yaml
questions:
  - question: "How deep should the compression analysis be for '{agent}'?"
    header: "Scope"
    options:
      - label: "Quick scan (Recommended)"
        description: "Boilerplate ratio + token estimate only — fastest, low risk"
      - label: "Standard analysis"
        description: "All 5 strategies evaluated with per-section breakdown"
      - label: "Deep optimization"
        description: "Full Ma/間 restructure + equivalence verification included"
    multiSelect: false
```

## ON_COMPRESSION_AGGRESSIVE

```yaml
questions:
  - question: "Compression proposal for '{agent}' reduces content by {reduction}% (>{threshold}%). How should we proceed?"
    header: "Reduction"
    options:
      - label: "Apply conservative subset (Recommended)"
        description: "Apply only dedup and density strategies — keep hierarchy and loose prompt for later"
      - label: "Apply full proposal"
        description: "Apply all proposed compressions — run full equivalence check afterward"
      - label: "Review per-section"
        description: "Show me section-by-section breakdown before deciding"
    multiSelect: false
```

## ON_MA_RESTRUCTURE

```yaml
questions:
  - question: "Ma/間 analysis suggests reordering sections in '{agent}' SKILL.md. This changes the section layout significantly. Proceed?"
    header: "Restructure"
    options:
      - label: "Apply Zone placement (Recommended)"
        description: "Move sections to optimal zones per Ma/間 principles"
      - label: "Partial — Zone 1 and 4 only"
        description: "Only optimize high-attention zones (first/last 15%)"
      - label: "Skip restructure"
        description: "Keep current section order — apply other compressions only"
    multiSelect: false
```
