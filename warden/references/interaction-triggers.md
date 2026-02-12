# Warden Interaction Triggers

Use `AskUserQuestion` tool to confirm with user at these decision points.
See `_common/INTERACTION.md` for standard formats.

---

## ON_EVALUATION_SCOPE

**Timing**: BEFORE_START — When evaluation target is unclear (feature, flow, page, release)

```yaml
questions:
  - question: "Let me confirm the V.A.I.R.E. evaluation target. What should I evaluate?"
    header: "Target"
    options:
      - label: "Specific feature (Recommended)"
        description: "Detailed evaluation of a single feature or flow"
      - label: "Entire page"
        description: "Evaluate all elements within a page"
      - label: "Entire release"
        description: "Evaluate all changes included in the release"
      - label: "Re-evaluate existing feature"
        description: "Re-check an already released feature"
    multiSelect: false
```

---

## ON_LEVEL_SELECTION

**Timing**: BEFORE_START — When choosing L0/L1/L2 compliance level

```yaml
questions:
  - question: "Which V.A.I.R.E. compliance level should I evaluate against?"
    header: "Level"
    options:
      - label: "L0: Minimum (MVS) (Recommended)"
        description: "Required for all features. No blind spots"
      - label: "L1: Standard"
        description: "Required for main features (core flows)"
      - label: "L2: Differentiation"
        description: "Target for core product and brand experiences"
    multiSelect: false
```

---

## ON_FAIL_VERDICT

**Timing**: ON_COMPLETION — When issuing FAIL, confirm remediation path

```yaml
questions:
  - question: "The evaluation result is FAIL. How should we proceed?"
    header: "FAIL Response"
    options:
      - label: "Fix then re-evaluate (Recommended)"
        description: "Request Palette to fix, then re-evaluate after completion"
      - label: "Consider exception approval"
        description: "Consider passing exceptionally for business reasons"
      - label: "Postpone release"
        description: "Hold release until quality standards are met"
    multiSelect: false
```

---

## ON_EXCEPTION_REQUEST

**Timing**: ON_RISK — When user requests override of FAIL verdict

```yaml
questions:
  - question: "This is an exception approval request. Which risk do you accept?"
    header: "Exception Review"
    options:
      - label: "Reject (Recommended)"
        description: "Maintain quality standards, do not grant exception"
      - label: "Time-limited exception"
        description: "Temporarily approve with condition to fix within X days"
      - label: "Document and approve"
        description: "Document risk explicitly and proceed with responsible party approval"
    multiSelect: false
```

---

## ON_PARTIAL_EVALUATION

**Timing**: ON_AMBIGUITY — When some dimensions cannot be evaluated

This trigger uses the standard `_common/INTERACTION.md` format. Present available options for how to handle dimensions that lack sufficient evidence for scoring.

---

## ON_DARK_PATTERN_DETECTED

**Timing**: ON_RISK — When potential manipulation pattern found

```yaml
questions:
  - question: "Potential dark pattern detected. How should we respond?"
    header: "Ethics Review"
    options:
      - label: "Immediate FAIL (Recommended)"
        description: "Dark patterns result in automatic failure without exception"
      - label: "Confirm intent"
        description: "Verify design intent before making judgment"
      - label: "Record as minor only"
        description: "If not a clear dark pattern"
    multiSelect: false
```

---

## ON_AGENCY_VIOLATION

**Timing**: ON_RISK — When consent/opt-out issues detected

```yaml
questions:
  - question: "Agency (user control) violation detected. What is the severity?"
    header: "Agency"
    options:
      - label: "Critical (Blocking)"
        description: "User has no right to refuse, or it's hidden"
      - label: "Medium"
        description: "Refusal is possible but hard to find"
      - label: "Minor"
        description: "Room for improvement but minimum is met"
    multiSelect: false
```
