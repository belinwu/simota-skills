# Interaction Triggers — Question Templates

Use `AskUserQuestion` tool at these decision points.

## ON_HIGH_COMPLEXITY

```yaml
questions:
  - question: "High complexity detected. How should we proceed?"
    header: "Complexity"
    options:
      - label: "Refactor to reduce complexity (Recommended)"
        description: "Apply Extract Method, Guard Clauses to simplify"
      - label: "Document and defer"
        description: "Add TODO comment, address in separate PR"
      - label: "Accept current complexity"
        description: "Complexity is justified for this use case"
    multiSelect: false
```

## ON_CODE_SMELL_DETECTED

```yaml
questions:
  - question: "Code smell detected: [smell type]. How to handle?"
    header: "Code Smell"
    options:
      - label: "Fix now (Recommended)"
        description: "Apply the appropriate refactoring"
      - label: "Fix if related to current task"
        description: "Only fix if touching this code anyway"
      - label: "Log for later"
        description: "Document but don't fix in this PR"
    multiSelect: false
```

## ON_RADAR_VERIFICATION

```yaml
questions:
  - question: "Test coverage is below 80%. How to proceed?"
    header: "Coverage"
    options:
      - label: "Add tests first (Recommended)"
        description: "Ensure adequate coverage before refactoring"
      - label: "Proceed with caution"
        description: "Refactor carefully, add tests after"
      - label: "Skip this refactoring"
        description: "Too risky without test coverage"
    multiSelect: false
```

## ON_REVIEW_LEVEL

```yaml
questions:
  - question: "Which review depth do you need?"
    header: "Review Level"
    options:
      - label: "Standard (Recommended)"
        description: "Function-level analysis with full review report"
      - label: "Quick Scan"
        description: "File-level overview, key findings only"
      - label: "Deep Dive"
        description: "Logic-level analysis with Before/After proposals"
    multiSelect: false
```

## ON_LARGE_REFACTOR

```yaml
questions:
  - question: "This refactoring affects >50 lines or multiple files. How to proceed?"
    header: "Scope"
    options:
      - label: "Proceed with full refactoring (Recommended)"
        description: "Apply changes across all affected files"
      - label: "Split into smaller PRs"
        description: "Break down into focused, incremental changes"
      - label: "Create migration plan only"
        description: "Document the plan without executing changes"
    multiSelect: false
```

## ON_BEHAVIOR_RISK

```yaml
questions:
  - question: "This change might affect runtime behavior. How to proceed?"
    header: "Risk"
    options:
      - label: "Add tests first, then refactor (Recommended)"
        description: "Ensure behavior is captured before changing structure"
      - label: "Proceed carefully with manual verification"
        description: "Make changes and verify manually"
      - label: "Skip this refactoring"
        description: "Too risky without guarantees"
    multiSelect: false
```

## ON_CODE_STYLE

```yaml
questions:
  - question: "Multiple valid approaches exist for this refactoring. Which style?"
    header: "Style"
    options:
      - label: "Match existing codebase style (Recommended)"
        description: "Follow dominant patterns in the project"
      - label: "Use language best practices"
        description: "Apply idiomatic patterns even if different from current code"
      - label: "Let me specify"
        description: "I'll provide the preferred approach"
    multiSelect: false
```

## ON_PUBLIC_API_CHANGE

```yaml
questions:
  - question: "Renaming will affect exported interface. Proceed?"
    header: "API Change"
    options:
      - label: "Rename with deprecation alias (Recommended)"
        description: "Keep old name as deprecated re-export"
      - label: "Rename without alias"
        description: "Breaking change, update all consumers"
      - label: "Skip this rename"
        description: "Keep current name to avoid breaking changes"
    multiSelect: false
```

## ON_DEAD_CODE_REMOVAL

```yaml
questions:
  - question: "This code appears unused but might be dynamically invoked. Remove?"
    header: "Dead Code"
    options:
      - label: "Remove with comment noting removal (Recommended)"
        description: "Delete code, add commit message noting what was removed"
      - label: "Comment out for now"
        description: "Disable but keep for reference"
      - label: "Keep as-is"
        description: "Leave the code, it might be needed"
    multiSelect: false
```
