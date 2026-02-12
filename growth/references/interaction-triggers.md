# Interaction Trigger Question Templates

YAML templates for `AskUserQuestion` tool at decision points.

## ON_SEO_STRATEGY

```yaml
questions:
  - question: "Please select an SEO strategy. Which approach would you like to use?"
    header: "SEO Strategy"
    options:
      - label: "Content optimization (Recommended)"
        description: "Improve meta tags and structure of existing content"
      - label: "Technical SEO"
        description: "Improve site structure, speed, and crawlability"
      - label: "Add structured data"
        description: "Implement JSON-LD rich snippets"
    multiSelect: false
```

## ON_CRO_APPROACH

```yaml
questions:
  - question: "Please select a conversion optimization approach. Which method would you like to use?"
    header: "CRO Approach"
    options:
      - label: "Direct improvement (Recommended)"
        description: "Apply changes directly based on best practices"
      - label: "A/B test design"
        description: "Design tests to measure the effect of changes"
      - label: "Analysis first"
        description: "Analyze current issues in detail before proposing improvements"
    multiSelect: false
```
