# Scaffold Interaction Trigger Templates

YAML question templates for `AskUserQuestion` at Scaffold's decision points.

## ON_CLOUD_PROVIDER

```yaml
questions:
  - question: "Which cloud provider would you like to use?"
    header: "Cloud"
    options:
      - label: "AWS (Recommended)"
        description: "Amazon Web Services - Widest service range"
      - label: "GCP"
        description: "Google Cloud Platform - Strong in Kubernetes/data analytics"
      - label: "Azure"
        description: "Microsoft Azure - Enterprise/Windows integration"
      - label: "Multi-cloud"
        description: "Use combination of multiple providers"
    multiSelect: false
```

## ON_ENVIRONMENT

```yaml
questions:
  - question: "Which environment are you building for?"
    header: "Environment"
    options:
      - label: "Development (Recommended)"
        description: "For local dev and testing, minimal resources"
      - label: "Staging"
        description: "Production-equivalent config for pre-release validation"
      - label: "Production"
        description: "Production environment, high availability config"
      - label: "All environments"
        description: "Configure dev/staging/prod all at once"
    multiSelect: false
```

## ON_COST_IMPACT

```yaml
questions:
  - question: "This resource will impact monthly costs. How would you like to proceed?"
    header: "Cost"
    options:
      - label: "Review cost estimate (Recommended)"
        description: "Calculate estimated cost before deciding"
      - label: "Start with minimal config"
        description: "Start small and scale as needed"
      - label: "Build production-grade"
        description: "Build with production config, accepting costs"
    multiSelect: false
```

## ON_DESTROY

```yaml
questions:
  - question: "Deleting resources. This operation cannot be undone."
    header: "Destroy"
    options:
      - label: "Review deletion targets (Recommended)"
        description: "Show list of resources to be deleted"
      - label: "Execute deletion"
        description: "Execute deletion with understanding of risks"
      - label: "Cancel deletion"
        description: "Abort deletion and maintain current state"
    multiSelect: false
```

## Environment Configuration Matrix

| Aspect | Development | Staging | Production |
|--------|-------------|---------|------------|
| **Resource Size** | Minimum (t3.micro) | Medium (50% of prod) | Production spec |
| **Instance Count** | 1 | 2+ | Scale as needed |
| **Availability** | Single AZ | Multi-AZ | Multi-AZ + DR |
| **Backup** | None/manual | Daily | Continuous + PITR |
| **Encryption** | Optional | Required | Required + CMK |
| **Monitoring** | Basic metrics | Detailed metrics | Detailed + alerts |
| **Log Retention** | 7 days | 30 days | 90+ days |
| **Delete Protection** | None | Recommended | Required |
