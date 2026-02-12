# Interaction Triggers - Question Templates

## ON_MODE_SELECTION

```yaml
questions:
  - question: "How should I approach quality improvement?"
    header: "Mode"
    options:
      - label: "STANDARD (Recommended)"
        description: "3 cycles, target UQS 80, balanced effort"
      - label: "QUICK"
        description: "1-2 cycles, target UQS 70, fast turnaround"
      - label: "INTENSIVE"
        description: "Up to 5 cycles, target UQS 90, thorough improvement"
    multiSelect: false
```

## ON_QUALITY_PROFILE

```yaml
questions:
  - question: "Which quality profile matches this project?"
    header: "Profile"
    options:
      - label: "Full-Stack (Recommended)"
        description: "Balanced 7-dimension quality assessment"
      - label: "API-Heavy"
        description: "Correctness, API consistency, test coverage"
      - label: "UI-Heavy"
        description: "UX quality, visual consistency, component docs"
      - label: "Library/SDK"
        description: "API consistency, documentation, public API coverage"
    multiSelect: false
```

## ON_DOMAIN_SCOPE

```yaml
questions:
  - question: "Which quality domains should I focus on?"
    header: "Domains"
    options:
      - label: "All domains (Recommended)"
        description: "Code, tests, consistency, docs, UX - comprehensive"
      - label: "Code + Consistency"
        description: "Focus on bugs, complexity, and pattern uniformity"
      - label: "Tests + Test Quality"
        description: "Focus on coverage, reliability, and test structure"
      - label: "UX only"
        description: "Focus on V.A.I.R.E. compliance"
    multiSelect: true
```

## ON_EXCEED_CYCLES

```yaml
questions:
  - question: "Max cycles reached but UQS is {current} (target: {target}). Continue?"
    header: "Continue?"
    options:
      - label: "Stop here"
        description: "Accept current quality level"
      - label: "One more cycle"
        description: "Try one additional improvement pass"
      - label: "Intensive mode"
        description: "Switch to intensive mode (up to 5 total cycles)"
    multiSelect: false
```
