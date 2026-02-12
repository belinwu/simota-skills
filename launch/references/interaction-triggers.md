# Launch Interaction Triggers

Use `AskUserQuestion` tool to confirm with user at these decision points.

## ON_VERSION_DECISION

```yaml
trigger: release_scope_defined
questions:
  - question: "What type of release is this?"
    header: "Version"
    options:
      - label: "Patch (bug fixes only)"
        description: "Backwards compatible bug fixes (x.x.PATCH)"
      - label: "Minor (new features)"
        description: "Backwards compatible features (x.MINOR.x)"
      - label: "Major (breaking changes)"
        description: "Incompatible API changes (MAJOR.x.x)"
      - label: "Pre-release (alpha/beta/rc)"
        description: "Testing release before stable"
    multiSelect: false
```

## ON_RELEASE_SCOPE

```yaml
trigger: release_planning_start
questions:
  - question: "What should be included in this release?"
    header: "Scope"
    options:
      - label: "All merged PRs since last release (Recommended)"
        description: "Standard release with all changes"
      - label: "Specific features only"
        description: "Cherry-pick selected features"
      - label: "Hotfix only"
        description: "Emergency fix, minimal scope"
    multiSelect: false
```

## ON_ROLLBACK_STRATEGY

```yaml
trigger: rollback_plan_creation
questions:
  - question: "What rollback capabilities are available?"
    header: "Rollback"
    options:
      - label: "Feature flags (instant rollback)"
        description: "Toggle feature off without deployment"
      - label: "Container rollback (2-5 minutes)"
        description: "Kubernetes/Docker rollback"
      - label: "Full deployment rollback (5-15 minutes)"
        description: "Redeploy previous version"
      - label: "Manual procedure required"
        description: "Custom steps needed"
    multiSelect: true
```

## ON_FEATURE_FLAG_ROLLOUT

```yaml
trigger: feature_flag_planning
questions:
  - question: "How should this feature be rolled out?"
    header: "Rollout"
    options:
      - label: "Gradual rollout (Recommended)"
        description: "5% → 25% → 50% → 100% over days"
      - label: "Beta users first"
        description: "Start with opt-in users"
      - label: "Internal only"
        description: "Team testing before any users"
      - label: "Full release"
        description: "100% immediately (not recommended)"
    multiSelect: false
```

## ON_RELEASE_TIMING

```yaml
trigger: release_scheduling
questions:
  - question: "When should this release go out?"
    header: "Timing"
    options:
      - label: "Next release window (Recommended)"
        description: "Tuesday-Thursday during business hours"
      - label: "ASAP (expedited)"
        description: "Critical fix, minimal testing"
      - label: "Schedule for specific date"
        description: "Coordinate with external timeline"
      - label: "After freeze period"
        description: "Queue for post-freeze"
    multiSelect: false
```
