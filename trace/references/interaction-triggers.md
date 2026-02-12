# Interaction Trigger Templates

Question templates for `AskUserQuestion` at Trace decision points.
See `_common/INTERACTION.md` for standard formats.

---

## ON_PERSONA_SEGMENT

```yaml
questions:
  - question: "Which persona segments should be analyzed?"
    header: "Segments"
    options:
      - label: "All defined personas (Recommended)"
        description: "Compare behavior across all Researcher-defined personas"
      - label: "Specific persona"
        description: "Focus on one persona for deep analysis"
      - label: "Behavior-based clusters"
        description: "Let data reveal natural user groupings"
      - label: "New vs returning users"
        description: "Segment by user lifecycle stage"
    multiSelect: false
```

## ON_ANALYSIS_SCOPE

```yaml
questions:
  - question: "What is the analysis scope?"
    header: "Scope"
    options:
      - label: "Specific flow (Recommended)"
        description: "Analyze a particular user journey (e.g., checkout, onboarding)"
      - label: "Full session"
        description: "Analyze complete user sessions end-to-end"
      - label: "Problem area"
        description: "Focus on known high-friction areas"
      - label: "Comparison"
        description: "Compare behavior before/after a change"
    multiSelect: false
```

## ON_RESEARCHER_HANDOFF

```yaml
questions:
  - question: "Persona validation findings are ready. How should we proceed?"
    header: "Handoff"
    options:
      - label: "Hand off to Researcher (Recommended)"
        description: "Researcher will update persona definitions based on findings"
      - label: "Generate report only"
        description: "Create validation report without handoff"
      - label: "Continue with Echo validation"
        description: "Test findings with Echo simulation before Researcher handoff"
    multiSelect: false
```
