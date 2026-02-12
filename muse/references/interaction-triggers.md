# Muse Interaction Trigger Templates

YAML question templates for `AskUserQuestion` tool.
See `_common/INTERACTION.md` for standard formats.

---

## ON_DESIGN_DIRECTION

```yaml
questions:
  - question: "Multiple valid design approaches. Which direction?"
    header: "Direction"
    options:
      - label: "Match existing patterns (Recommended)"
        description: "Consistent with current design system"
      - label: "Introduce new pattern"
        description: "Better design but needs system-wide review"
      - label: "Minimal change"
        description: "Smallest possible impact"
    multiSelect: false
```

## ON_TOKEN_AUDIT

```yaml
questions:
  - question: "Token audit found hardcoded values. How to proceed?"
    header: "Audit"
    options:
      - label: "Fix critical issues only (Recommended)"
        description: "Address high-impact hardcoded values"
      - label: "Fix all issues"
        description: "Comprehensive tokenization"
      - label: "Document for later"
        description: "Log issues but don't fix now"
    multiSelect: false
```

## ON_DARK_MODE_CHECK

```yaml
questions:
  - question: "Dark mode issues found. How to handle?"
    header: "Dark Mode"
    options:
      - label: "Fix all issues (Recommended)"
        description: "Ensure full dark mode support"
      - label: "Fix critical only"
        description: "Address contrast and visibility issues"
      - label: "Skip dark mode"
        description: "Component not used in dark mode context"
    multiSelect: false
```

## ON_PALETTE_REVIEW

```yaml
questions:
  - question: "Color change affects accessibility. Request Palette review?"
    header: "A11y Review"
    options:
      - label: "Yes, verify with Palette (Recommended)"
        description: "Ensure WCAG compliance before proceeding"
      - label: "Self-verify contrast"
        description: "Check contrast ratios manually"
      - label: "Proceed without review"
        description: "Minor change, low risk"
    multiSelect: false
```

## ON_TOKEN_LIFECYCLE

```yaml
questions:
  - question: "Token lifecycle transition requires review. How to proceed?"
    header: "Lifecycle"
    options:
      - label: "Approve transition (Recommended)"
        description: "Proceed with state change and notify affected agents"
      - label: "Request impact analysis first"
        description: "Run Ripple scan before proceeding"
      - label: "Defer transition"
        description: "Keep current state, revisit next sprint"
    multiSelect: false
```

## ON_REVERSE_FEEDBACK

```yaml
questions:
  - question: "Downstream agent reported a token issue. How to handle?"
    header: "Feedback"
    options:
      - label: "Fix immediately (Recommended)"
        description: "Address the reported issue now"
      - label: "Schedule for next cycle"
        description: "Add to backlog, fix in next design system update"
      - label: "Reject feedback"
        description: "Issue is by design or out of scope"
    multiSelect: false
```
