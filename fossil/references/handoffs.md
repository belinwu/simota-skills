# Fossil Handoff Templates

## Receiving Handoffs

### From Trail (Git History Context)

```yaml
TRAIL_TO_FOSSIL_HANDOFF:
  source: Trail
  content:
    investigation_target: "[module or file path]"
    key_commits: ["[commit hashes with summaries]"]
    reverted_changes: ["[reverted commits and their context]"]
    contributor_patterns: "[who changed what and when]"
  request: "Use git history context to extract business rules"
```

### From Lens (Code Structure)

```yaml
LENS_TO_FOSSIL_HANDOFF:
  source: Lens
  content:
    module_map: "[dependency graph or module structure]"
    entry_points: ["[key entry points for investigation]"]
    complexity_hotspots: ["[high-complexity areas]"]
  request: "Focus archaeological investigation on identified hotspots"
```

## Sending Handoffs

### To Shift (Migration Planning)

```yaml
FOSSIL_TO_SHIFT_HANDOFF:
  source: Fossil
  destination: Shift
  content:
    rule_catalog: "[path to rule catalog]"
    migration_risks:
      high: [N]
      medium: [N]
      low: [N]
    critical_rules: ["[rules that must be preserved in migration]"]
    hidden_dependencies: ["[non-obvious dependencies discovered]"]
    untested_rules: ["[rules without test coverage]"]
  request: "Plan migration incorporating discovered rules and risks"
```

### To Scribe (Specification)

```yaml
FOSSIL_TO_SCRIBE_HANDOFF:
  source: Fossil
  destination: Scribe
  content:
    rule_catalog: "[path to rule catalog]"
    rules_needing_spec:
      - rule_id: "[ID]"
        description: "[rule description]"
        confidence: "[level]"
        current_source: "[where it lives in code]"
    domain_context: "[business domain notes discovered during analysis]"
  request: "Create formal specifications from extracted business rules"
```

### To Builder (Reimplementation)

```yaml
FOSSIL_TO_BUILDER_HANDOFF:
  source: Fossil
  destination: Builder
  content:
    rule_catalog: "[path to rule catalog]"
    implementation_guide:
      - rule_id: "[ID]"
        current_location: "[file:line]"
        behavior: "[exact behavior description]"
        edge_cases: ["[discovered edge cases]"]
        test_references: ["[existing test paths]"]
    warnings: ["[gotchas discovered during archaeology]"]
  request: "Reimplement extracted business rules in new architecture"
```
