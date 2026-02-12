# Rewind Interaction Trigger Templates

## ON_BISECT_START

```yaml
questions:
  - question: "Starting git bisect. Please confirm the test command and search range."
    header: "Bisect Confirm"
    options:
      - label: "Start (Recommended)"
        description: "good: {good_commit}, bad: {bad_commit}, test: {test_command}"
      - label: "Adjust range"
        description: "Manually specify good/bad commits"
      - label: "Manual bisect"
        description: "Step through each iteration manually"
    multiSelect: false
```

## ON_CRITICAL_COMMIT

```yaml
questions:
  - question: "A critical commit ({commit_type}) has been identified as the cause. How should we proceed?"
    header: "Critical Finding"
    options:
      - label: "Continue investigation (Recommended)"
        description: "Deep dive into why this change caused the issue"
      - label: "Propose revert"
        description: "Provide safe revert instructions"
      - label: "Hand off to Builder"
        description: "Pass fix context to Builder agent"
    multiSelect: false
```
