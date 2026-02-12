# Interaction Trigger Templates

## ON_INDEX_RECOMMENDATION

```yaml
questions:
  - question: "I recommend adding a new index. How would you like to proceed?"
    header: "Add Index"
    options:
      - label: "Verify in dev environment (Recommended)"
        description: "Confirm performance improvement in dev before applying to prod"
      - label: "Apply to prod during off-peak"
        description: "Apply to production during low-traffic hours"
      - label: "Detailed impact analysis"
        description: "Analyze impact on write performance in detail"
    multiSelect: false
```

## ON_QUERY_REWRITE

```yaml
questions:
  - question: "I recommend rewriting the query. How would you like to proceed?"
    header: "Query Change"
    options:
      - label: "Maintain existing behavior (Recommended)"
        description: "Optimize while confirming results remain the same"
      - label: "Prioritize performance"
        description: "Allow minor behavior changes for optimization"
      - label: "Gradual migration"
        description: "Run both queries in parallel for verification"
    multiSelect: false
```
