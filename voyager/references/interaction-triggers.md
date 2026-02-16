# Interaction Trigger Question Templates

Question templates for `AskUserQuestion` at Voyager decision points.
See `_common/INTERACTION.md` for standard formats.

---

## ON_FRAMEWORK_SELECTION

```yaml
questions:
  - question: "Please select an E2E test framework. Which one would you like to use?"
    header: "Framework"
    options:
      - label: "Playwright (Recommended)"
        description: "Fast, stable, cross-browser, auto-waiting, free parallel execution"
      - label: "Cypress"
        description: "Great DX, real-time reload, rich plugin ecosystem, component testing"
      - label: "WebdriverIO"
        description: "Selenium-compatible, mobile native via Appium, broad ecosystem"
      - label: "Use existing framework"
        description: "Continue with framework already in use"
    multiSelect: false
```

---

## ON_CRITICAL_PATH

```yaml
questions:
  - question: "Please select critical paths to cover with E2E tests."
    header: "Test Target"
    options:
      - label: "Authentication flow (Recommended)"
        description: "Signup, login, password reset"
      - label: "Core features"
        description: "Main value-delivering features of the app"
      - label: "Payment/checkout flow"
        description: "Cart, checkout, payment"
      - label: "All of the above"
        description: "Cover all critical paths"
    multiSelect: true
```

---

## ON_FLAKY_TEST

```yaml
questions:
  - question: "A flaky test has been detected. How would you like to handle it?"
    header: "Flaky Test"
    options:
      - label: "Improve wait strategy (Recommended)"
        description: "Add appropriate waitFor to stabilize"
      - label: "Add retry configuration"
        description: "Set up retry as a temporary workaround"
      - label: "Split the test"
        description: "Break test into smaller parts to isolate issue"
    multiSelect: false
```

---

## ON_BROWSER_MATRIX

```yaml
questions:
  - question: "Which browsers/devices should be included in the test matrix?"
    header: "Browsers"
    options:
      - label: "Chromium only (Recommended)"
        description: "Fastest CI, covers majority of users"
      - label: "Chromium + Firefox + WebKit"
        description: "Full cross-browser coverage"
      - label: "Desktop + Mobile emulation"
        description: "Responsive testing with device presets"
      - label: "Custom matrix"
        description: "Specify browsers and devices manually"
    multiSelect: false
```

---

## ON_CI_INTEGRATION

```yaml
questions:
  - question: "Which CI platform should E2E tests be integrated with?"
    header: "CI Platform"
    options:
      - label: "GitHub Actions (Recommended)"
        description: "Native integration, artifact upload, sharding support"
      - label: "Use existing CI"
        description: "Add E2E stage to current CI pipeline"
      - label: "Skip CI for now"
        description: "Run locally only, configure CI later"
    multiSelect: false
```

---

## ON_PERFORMANCE_BUDGET

```yaml
questions:
  - question: "Would you like to set up performance budgets for E2E tests?"
    header: "Perf Budget"
    options:
      - label: "Core Web Vitals only (Recommended)"
        description: "LCP ≤ 2.5s, CLS ≤ 0.1, INP ≤ 200ms"
      - label: "CWV + Bundle size"
        description: "Add bundle size budget assertions"
      - label: "Full Lighthouse CI"
        description: "Comprehensive Lighthouse scoring in CI"
      - label: "Skip performance budgets"
        description: "Focus on functional E2E only"
    multiSelect: false
```

---

## ON_ENVIRONMENT_SETUP

```yaml
questions:
  - question: "How should the E2E test environment be provisioned?"
    header: "Environment"
    options:
      - label: "Local dev server (Recommended)"
        description: "Run against localhost with webServer config"
      - label: "Docker Compose"
        description: "Full stack in containers with DB seeding"
      - label: "Preview/staging URL"
        description: "Test against deployed preview environment"
      - label: "Custom setup"
        description: "Specify environment configuration manually"
    multiSelect: false
```

---

## ON_COMPLEX_SCENARIO

```yaml
questions:
  - question: "Which complex scenario pattern should be implemented?"
    header: "Scenario"
    options:
      - label: "Multi-tab / popup handling"
        description: "Browser context management for multi-window flows"
      - label: "iframe interaction"
        description: "Cross-frame element access and assertions"
      - label: "WebSocket / real-time"
        description: "WebSocket message interception and verification"
      - label: "File upload/download"
        description: "File handling with download path configuration"
    multiSelect: true
```

---

## ON_REVERSE_FEEDBACK

```yaml
ON_REVERSE_FEEDBACK:
  timing: ON_RECEIVE
  template:
    questions:
      - question: "Downstream agent reported an issue with E2E test output. How should we handle it?"
        header: "Feedback"
        options:
          - label: "Fix immediately (Recommended)"
            description: "Address the reported issue in the current session"
          - label: "Schedule for next cycle"
            description: "Add to improvement queue for next session"
          - label: "Reject with reason"
            description: "Provide explanation why feedback is not applicable"
        multiSelect: false
```
