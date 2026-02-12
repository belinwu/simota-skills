# Radar Interaction Trigger Templates

YAML templates for `AskUserQuestion` tool. See `_common/INTERACTION.md` for standard formats.

---

## ON_TEST_STRATEGY

```yaml
questions:
  - question: "Which test strategy should we use?"
    header: "Strategy"
    options:
      - label: "Unit test focused (Recommended)"
        description: "Fast and stable unit tests for business logic"
      - label: "Integration test focused"
        description: "Verify component interactions with real dependencies"
      - label: "Coverage gap focused"
        description: "Target uncovered critical paths regardless of test type"
    multiSelect: false
```

## ON_COVERAGE_TARGET

```yaml
questions:
  - question: "What coverage target are you aiming for?"
    header: "Coverage"
    options:
      - label: "Critical paths only (Recommended)"
        description: "Cover only business-critical logic"
      - label: "80% coverage"
        description: "Target 80% as a common standard"
      - label: "Edge case focused"
        description: "Prioritize boundary values and error cases over coverage rate"
    multiSelect: false
```

## ON_FLAKY_TEST

```yaml
questions:
  - question: "Flaky test detected. How should we handle it?"
    header: "Flaky Test"
    options:
      - label: "Investigate and fix (Recommended)"
        description: "Identify root cause and rewrite to stable test"
      - label: "Skip temporarily"
        description: "Create investigation ticket and skip for now"
      - label: "Delete test"
        description: "Delete low-value test and redesign"
    multiSelect: false
```

## ON_ADVANCED_TECHNIQUE

```yaml
questions:
  - question: "Which advanced testing technique should we apply?"
    header: "Technique"
    options:
      - label: "Property-based testing (Recommended)"
        description: "Generate random inputs to find edge cases automatically"
      - label: "Contract testing (Pact)"
        description: "Verify API contracts between services"
      - label: "Mutation testing (Stryker)"
        description: "Verify tests actually catch bugs by introducing mutations"
    multiSelect: false
```

## ON_TEST_SELECTION

```yaml
questions:
  - question: "Which test selection strategy should we use for CI?"
    header: "Selection"
    options:
      - label: "Changed-file based (Recommended)"
        description: "Run tests related to changed files only (fastest)"
      - label: "Fail-likely-first"
        description: "Prioritize previously failed tests, then changed-related"
      - label: "3-gate incremental"
        description: "Fast Gate → Integration Gate → Full Suite pipeline"
    multiSelect: false
```

## ON_COVERAGE_STRATEGY

```yaml
questions:
  - question: "Which coverage strategy should we apply?"
    header: "Coverage"
    options:
      - label: "Diff coverage only (Recommended)"
        description: "Enforce coverage on new/changed lines only"
      - label: "Ratchet strategy"
        description: "Never allow coverage to decrease from current level"
      - label: "Per-module thresholds"
        description: "Set different targets per module based on criticality"
    multiSelect: false
```
