# Interaction Trigger Templates

Question templates for `AskUserQuestion` at Probe decision points.
See `_common/INTERACTION.md` for standard formats.

## ON_SCOPE_DEFINITION

```yaml
questions:
  - question: "Please confirm the scope of security testing."
    header: "Test Scope"
    options:
      - label: "Development environment only (Recommended)"
        description: "Run tests in local/staging environment"
      - label: "Specific endpoints only"
        description: "Limit to designated API endpoints"
      - label: "Full application"
        description: "Include all authorized scope in testing"
    multiSelect: false
```

## ON_PRODUCTION_TEST

```yaml
questions:
  - question: "Production environment testing is required. How would you like to proceed?"
    header: "Production Test"
    options:
      - label: "Use staging as alternative (Recommended)"
        description: "Test on production-equivalent staging environment"
      - label: "Read-only tests only"
        description: "Execute only scans with no production impact"
      - label: "Execute during maintenance window"
        description: "Run during low-impact time window"
    multiSelect: false
```

## ON_DESTRUCTIVE_TEST

```yaml
questions:
  - question: "This test scenario may cause service disruption. How would you like to proceed?"
    header: "Destructive Test"
    options:
      - label: "Skip destructive tests (Recommended)"
        description: "Run only non-destructive tests"
      - label: "Execute in isolated environment"
        description: "Use a dedicated test environment"
      - label: "Proceed with monitoring"
        description: "Execute with real-time monitoring and rollback plan"
    multiSelect: false
```

## ON_CREDENTIAL_TEST

```yaml
questions:
  - question: "Authentication mechanism testing requires credential operations. How would you like to proceed?"
    header: "Credential Test"
    options:
      - label: "Use test accounts only (Recommended)"
        description: "Test with dedicated test credentials"
      - label: "Token validation only"
        description: "Test token handling without credential operations"
      - label: "Full authentication testing"
        description: "Include password policy and brute force protection tests"
    multiSelect: false
```

## ON_HIGH_SEVERITY

```yaml
questions:
  - question: "A critical vulnerability has been confirmed. Please select a response strategy."
    header: "Critical Vulnerability"
    options:
      - label: "Report to team immediately (Recommended)"
        description: "Urgent report to security team, prioritize fix"
      - label: "Conduct additional verification"
        description: "Investigate impact scope in detail before reporting"
      - label: "Report with fix proposal"
        description: "Request Builder to fix and report together"
    multiSelect: false
```

## ON_SENTINEL_HANDOFF

```yaml
questions:
  - question: "Validation of Sentinel's static analysis findings is complete. How would you like to proceed?"
    header: "Sentinel Handoff"
    options:
      - label: "Return validated results to Sentinel (Recommended)"
        description: "Send confirmation/rejection of each finding"
      - label: "Hand off to Builder for fixes"
        description: "Send confirmed vulnerabilities directly for remediation"
      - label: "Generate full report first"
        description: "Create comprehensive report before handoff"
    multiSelect: false
```
