# Canon Interaction Trigger Templates

Use with `AskUserQuestion` tool. See `_common/INTERACTION.md` for standard formats.

## ON_STANDARD_SELECTION

```yaml
questions:
  - question: "Multiple standards apply to this domain. Which should take priority?"
    header: "Standard Priority"
    options:
      - label: "OWASP ASVS (Recommended)"
        description: "Comprehensive security verification standard"
      - label: "NIST CSF"
        description: "Federal framework, broader scope"
      - label: "CIS Controls"
        description: "Prioritized security controls"
      - label: "Evaluate all applicable standards"
        description: "Comprehensive but time-intensive assessment"
    multiSelect: false
```

## ON_COMPLIANCE_LEVEL

```yaml
questions:
  - question: "What compliance level should we target?"
    header: "Compliance Level"
    options:
      - label: "Level A / Basic (Recommended)"
        description: "Minimum compliance, lower cost, addresses critical issues"
      - label: "Level AA / Standard"
        description: "Industry standard compliance, moderate effort"
      - label: "Level AAA / Advanced"
        description: "Maximum compliance, significant investment required"
      - label: "Custom level"
        description: "Define specific requirements subset"
    multiSelect: false
```

## ON_COST_BENEFIT

```yaml
questions:
  - question: "Compliance cost for this requirement is high. How would you like to proceed?"
    header: "Cost-Benefit"
    options:
      - label: "Document as accepted risk (Recommended)"
        description: "Record decision, revisit later when resources allow"
      - label: "Implement partial compliance"
        description: "Address highest impact items only"
      - label: "Full compliance"
        description: "Invest required resources for complete compliance"
      - label: "Seek alternative approach"
        description: "Find different solution that meets intent at lower cost"
    multiSelect: false
```

## ON_INDUSTRY_SPECIFIC

```yaml
questions:
  - question: "Industry-specific regulations may apply. Please confirm applicable regulations."
    header: "Regulations"
    options:
      - label: "No specific regulations"
        description: "General software, no industry requirements"
      - label: "PCI-DSS (Payment)"
        description: "Payment card handling requirements"
      - label: "HIPAA (Healthcare)"
        description: "Protected health information requirements"
      - label: "GDPR (Privacy)"
        description: "EU data protection requirements"
    multiSelect: true
```

## ON_STANDARD_CONFLICT

```yaml
questions:
  - question: "Standards conflict on this requirement. Which takes precedence?"
    header: "Conflict Resolution"
    options:
      - label: "Security standard (Recommended)"
        description: "Prioritize security over other concerns"
      - label: "Newer standard version"
        description: "Follow most recent guidance"
      - label: "Project-specific decision"
        description: "Decide based on project context"
      - label: "Seek clarification"
        description: "Consult standard bodies or legal team"
    multiSelect: false
```

## ON_MIGRATION_STRATEGY

```yaml
questions:
  - question: "Standard version upgrade is available. How should we handle migration?"
    header: "Migration Strategy"
    options:
      - label: "Gradual migration (Recommended)"
        description: "Adopt new version incrementally, maintain old compliance"
      - label: "Immediate adoption"
        description: "Upgrade to new version immediately"
      - label: "Maintain current version"
        description: "Stay on current version until end-of-support"
      - label: "Gap analysis first"
        description: "Analyze differences before deciding"
    multiSelect: false
```
