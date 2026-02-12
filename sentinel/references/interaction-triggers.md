# Interaction Triggers — Question Templates

YAML templates for Sentinel's `AskUserQuestion` decision points.
See `_common/INTERACTION.md` for standard formats.

---

## ON_SECURITY_DEPENDENCY

```yaml
questions:
  - question: "Security-related dependency needs to be added. How would you like to proceed?"
    header: "Add Dependency"
    options:
      - label: "Use existing library (Recommended)"
        description: "Implement using existing library in project"
      - label: "Add new library"
        description: "Introduce new security-specific library"
      - label: "Manual implementation"
        description: "Implement without external dependency (review required)"
    multiSelect: false
```

## ON_AUTH_CHANGE

```yaml
questions:
  - question: "Authentication/authorization logic change is required. How would you like to proceed?"
    header: "Auth Change"
    options:
      - label: "Keep changes minimal (Recommended)"
        description: "Maintain existing auth flow, implement only required changes"
      - label: "Change after comprehensive review"
        description: "Review entire auth flow before making changes"
      - label: "Defer changes"
        description: "Handle as separate task after detailed design review"
    multiSelect: false
```

## ON_OWASP_VIOLATION

```yaml
questions:
  - question: "OWASP Top 10 vulnerability detected. Please select a response strategy."
    header: "OWASP Violation"
    options:
      - label: "Fix immediately (Recommended)"
        description: "Fix detected vulnerability right away"
      - label: "Investigate impact scope"
        description: "Investigate impact scope in detail before fix"
      - label: "Report to team"
        description: "Report to security team before fix"
    multiSelect: false
```

## ON_DEPENDENCY_CVE

```yaml
questions:
  - question: "Known vulnerability (CVE) found in dependency. How would you like to handle it?"
    header: "CVE Detected"
    options:
      - label: "Update to patch version (Recommended)"
        description: "Update to compatible patch version"
      - label: "Update to major version"
        description: "Update with potential breaking changes"
      - label: "Migrate to alternative library"
        description: "Replace with different library"
      - label: "Accept risk"
        description: "Record as minor risk, address later"
    multiSelect: false
```
