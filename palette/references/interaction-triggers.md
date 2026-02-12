# Interaction Trigger Templates

Use `AskUserQuestion` tool with these YAML templates.
See `_common/INTERACTION.md` for standard formats.

---

## ON_UX_APPROACH

```yaml
questions:
  - question: "Multiple UX improvement approaches available. Which priority?"
    header: "UX Focus"
    options:
      - label: "Feedback improvement (Recommended)"
        description: "Prioritize clear action results for users"
      - label: "Cognitive load reduction"
        description: "Reduce information and emphasize simplicity"
      - label: "Error prevention"
        description: "Design to prevent user mistakes upfront"
    multiSelect: false
```

## ON_A11Y_TRADEOFF

```yaml
questions:
  - question: "Accessibility improvement affects design. How to proceed?"
    header: "A11y"
    options:
      - label: "Accessibility first (Recommended)"
        description: "Prioritize design usable by more users"
      - label: "Balance both"
        description: "Find middle ground between visual and a11y"
      - label: "Minimal compliance"
        description: "Address only required a11y requirements"
    multiSelect: false
```

## ON_INTERACTION_PATTERN

```yaml
questions:
  - question: "Select interaction pattern for this action"
    header: "Pattern"
    options:
      - label: "Confirmation dialog (Recommended)"
        description: "Request confirmation before destructive action"
      - label: "Undo capability"
        description: "Allow reversal after action"
      - label: "Inline confirmation"
        description: "Confirm in-place before execution"
    multiSelect: false
```

## ON_HEURISTIC_EVAL

```yaml
questions:
  - question: "Heuristic evaluation complete. Which areas to focus on?"
    header: "Focus"
    options:
      - label: "Critical areas only (Recommended)"
        description: "Address scores of 1-2 first"
      - label: "Quick wins"
        description: "Low-effort improvements across all areas"
      - label: "Comprehensive"
        description: "Address all areas below score 4"
    multiSelect: false
```

## ON_ECHO_VALIDATION

```yaml
questions:
  - question: "Should this UX change be validated with Echo persona testing?"
    header: "Validate"
    options:
      - label: "Yes, test with personas (Recommended)"
        description: "Get feedback from simulated user perspectives"
      - label: "Skip validation"
        description: "Proceed without persona testing"
    multiSelect: false
```

## ON_FLOW_HANDOFF

```yaml
questions:
  - question: "This interaction needs animation. Hand off to Flow?"
    header: "Animation"
    options:
      - label: "Yes, create Flow handoff"
        description: "Generate animation spec for Flow agent"
      - label: "Use CSS only"
        description: "Implement with basic CSS transitions"
      - label: "Skip animation"
        description: "Proceed without animation"
    multiSelect: false
```

## ON_MOBILE_UX

```yaml
questions:
  - question: "Mobile-specific improvement detected. How to proceed?"
    header: "Mobile"
    options:
      - label: "Optimize for mobile first (Recommended)"
        description: "Prioritize touch targets, thumb zone, and gestures"
      - label: "Desktop-first with mobile fallback"
        description: "Optimize desktop, ensure mobile works"
      - label: "Progressive enhancement"
        description: "Base experience works everywhere, enhance for capable devices"
    multiSelect: false
```

## ON_CANVAS_HANDOFF

```yaml
questions:
  - question: "Document this UX improvement with Canvas visualization?"
    header: "Document"
    options:
      - label: "Yes, create Before/After comparison (Recommended)"
        description: "Generate visual diff for stakeholder review"
      - label: "Heuristic score chart only"
        description: "Show improvement in metrics"
      - label: "Skip documentation"
        description: "Proceed without Canvas handoff"
    multiSelect: false
```
