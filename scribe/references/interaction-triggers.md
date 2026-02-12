# Interaction Trigger Templates

Use `AskUserQuestion` tool with these YAML templates.
See `_common/INTERACTION.md` for standard formats.

---

## ON_DOC_TYPE

```yaml
questions:
  - question: "Which document type should I create?"
    header: "Document Type"
    options:
      - label: "Specification (PRD/SRS) (Recommended)"
        description: "Define functional requirements and acceptance criteria. Input for Builder"
      - label: "Design Document (HLD/LLD)"
        description: "Architecture and detailed design. Implementation guide"
      - label: "Implementation Checklist"
        description: "Task list for developers. For progress tracking"
      - label: "Test Specification"
        description: "Test cases and expected results. For QA/Radar"
    multiSelect: false
```

## ON_DETAIL_LEVEL

```yaml
questions:
  - question: "Select the detail level for the document."
    header: "Detail Level"
    options:
      - label: "Overview Level (Recommended)"
        description: "Main requirements and constraints only. Quick creation"
      - label: "Standard Level"
        description: "All requirements, acceptance criteria, edge cases included"
      - label: "Detailed Level"
        description: "All branches, error cases, non-functional requirements included"
    multiSelect: false
```

## ON_AUDIENCE

```yaml
questions:
  - question: "Who is the primary audience for this document?"
    header: "Target Audience"
    options:
      - label: "Developers (Recommended)"
        description: "Focus on technical details and implementation guidance"
      - label: "QA Engineers"
        description: "Focus on test perspectives and expected behavior"
      - label: "Product Managers"
        description: "Focus on business requirements and user value"
      - label: "All Stakeholders"
        description: "Balanced and comprehensive content"
    multiSelect: false
```

## ON_ATLAS_NEEDED

```yaml
questions:
  - question: "Architecture decision is needed. Should I request Atlas assistance?"
    header: "Design Decision"
    options:
      - label: "Request Atlas (Recommended)"
        description: "Create design document after ADR is created"
      - label: "Follow existing patterns"
        description: "Conform to project's existing architecture"
      - label: "Proceed with assumptions documented"
        description: "Document design decisions as assumptions, confirm later"
    multiSelect: false
```
