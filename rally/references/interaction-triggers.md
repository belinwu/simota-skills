# Rally Interaction Trigger Templates

Use with `AskUserQuestion` tool. See `_common/INTERACTION.md` for standard formats.

---

## ON_TEAM_DESIGN

```yaml
questions:
  - question: "Shall we proceed with the following team composition?"
    header: "Team Design"
    options:
      - label: "Proceed with this composition (Recommended)"
        description: "Execute with the proposed team structure, role assignments, and file ownership"
      - label: "Change team size"
        description: "Increase or decrease the number of teammates"
      - label: "Change role assignments"
        description: "Adjust each teammate's scope of responsibility"
    multiSelect: false
```

## ON_FILE_CONFLICT_RISK

```yaml
questions:
  - question: "File ownership overlap detected. How should we resolve it?"
    header: "Ownership"
    options:
      - label: "Re-partition ownership (Recommended)"
        description: "Consolidate overlapping files to one teammate, set others to shared_read"
      - label: "Switch to sequential execution"
        description: "Execute changes to the affected files in order"
      - label: "Accept risk and continue in parallel"
        description: "Proceed in parallel despite potential merge conflicts"
    multiSelect: false
```

## ON_LARGE_TEAM

```yaml
questions:
  - question: "About to spawn 5+ teammates. This increases cost. Shall we proceed?"
    header: "Team Size"
    options:
      - label: "Approve"
        description: "Spawn the proposed team size"
      - label: "Split into smaller teams (Recommended)"
        description: "Re-partition tasks to fit within a 3-4 person team"
      - label: "Spawn progressively"
        description: "Spawn a subset first, then start the next group after completion"
    multiSelect: false
```

## ON_HIGH_RISK_DELEGATION

```yaml
questions:
  - question: "About to delegate a high-risk task to a teammate. Please confirm."
    header: "Risk"
    options:
      - label: "Approve delegation"
        description: "Delegate with plan_mode_required set on the teammate"
      - label: "Handle directly"
        description: "Do not parallelize this task; Rally manages it directly"
      - label: "Skip task"
        description: "Exclude this high-risk task from the current scope"
    multiSelect: false
```

## ON_TEAMMATE_FAILURE

```yaml
questions:
  - question: "A teammate has failed its task. How should we respond?"
    header: "Recovery"
    options:
      - label: "Retry (Recommended)"
        description: "Provide additional context to the same teammate and retry"
      - label: "Replace with new teammate"
        description: "Shut down the failed teammate and spawn a new one"
      - label: "Resolve manually"
        description: "Switch this task to manual handling"
    multiSelect: false
```

## ON_RESULT_CONFLICT

```yaml
questions:
  - question: "Teammate outputs conflict with each other. How should we resolve?"
    header: "Conflict"
    options:
      - label: "Auto-merge (Recommended)"
        description: "Analyze conflict points and attempt automatic merge"
      - label: "Designate priority teammate"
        description: "Adopt one teammate's output as the canonical version"
      - label: "Manual merge"
        description: "Present conflict points to the user for judgment"
    multiSelect: false
```
