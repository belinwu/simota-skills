# Vision — Interaction Trigger Templates

Question templates for `AskUserQuestion` tool at each decision point.
See `_common/INTERACTION.md` for standard formats.

---

## ON_DESIGN_DIRECTION

```yaml
questions:
  - question: "Which design direction should we pursue?"
    header: "Direction"
    options:
      - label: "Option A: [Name] (Recommended)"
        description: "[Key characteristics and why recommended]"
      - label: "Option B: [Name]"
        description: "[Key characteristics and trade-offs]"
      - label: "Option C: [Name]"
        description: "[Key characteristics and trade-offs]"
    multiSelect: false
```

## ON_BRAND_CHANGE

```yaml
questions:
  - question: "This proposal includes changes to brand identity. How should we proceed?"
    header: "Brand"
    options:
      - label: "Approve brand evolution"
        description: "Update brand guidelines to reflect new direction"
      - label: "Minimize changes (Recommended)"
        description: "Adjust proposal to stay within current brand boundaries"
      - label: "Cancel this direction"
        description: "Explore alternatives that preserve existing identity"
    multiSelect: false
```

## ON_TREND_APPLICATION

```yaml
questions:
  - question: "Apply this design trend to the project?"
    header: "Trend"
    options:
      - label: "Gradual rollout (Recommended)"
        description: "Start with pilot area, expand based on feedback"
      - label: "Full application"
        description: "Apply across entire product immediately"
      - label: "Skip this trend"
        description: "Maintain current style, revisit later"
    multiSelect: false
```

## ON_SCOPE_EXPANSION

```yaml
questions:
  - question: "Design scope has expanded. How should we proceed?"
    header: "Scope"
    options:
      - label: "Phase the work (Recommended)"
        description: "Prioritize high-impact items, defer others"
      - label: "Approve expanded scope"
        description: "Include all identified improvements"
      - label: "Return to original scope"
        description: "Focus only on initially requested changes"
    multiSelect: false
```

## ON_ACCESSIBILITY_TRADEOFF

```yaml
questions:
  - question: "This design choice affects accessibility. What's the priority?"
    header: "A11y"
    options:
      - label: "Accessibility first (Recommended)"
        description: "Maintain WCAG AA compliance, adjust visual approach"
      - label: "Provide alternatives"
        description: "Keep visual design, add accessible alternative"
      - label: "Accept reduced accessibility"
        description: "Proceed with documented accessibility limitation"
    multiSelect: false
```

## ON_BUSINESS_CONSTRAINT

```yaml
questions:
  - question: "Design direction conflicts with business constraints. How should we proceed?"
    header: "Business"
    options:
      - label: "Adjust direction to fit constraints (Recommended)"
        description: "Modify design approach to align with budget, scope, and timeline"
      - label: "Request constraint relaxation"
        description: "Ask Bridge to negotiate adjusted constraints with stakeholders"
      - label: "Proceed with risk documented"
        description: "Continue with acknowledged business risk"
    multiSelect: false
```

## ON_VAIRE_PRECHECK_FAIL

```yaml
questions:
  - question: "Warden V.A.I.R.E. pre-check flagged issues. How should we proceed?"
    header: "Quality"
    options:
      - label: "Address all findings (Recommended)"
        description: "Adjust design direction to satisfy V.A.I.R.E. criteria before delegation"
      - label: "Address critical only"
        description: "Fix FAIL items, accept CONDITIONAL with mitigation plan"
      - label: "Override with justification"
        description: "Proceed with documented rationale for deviation"
    multiSelect: false
```
