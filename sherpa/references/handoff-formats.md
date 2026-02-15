# Handoff Formats

Input and output handoff templates for Sherpa's inter-agent collaboration.

---

## Output Handoffs (Sending)

### SHERPA_TO_SCOUT_HANDOFF

Investigation needed before proceeding with step.

```yaml
SHERPA_TO_SCOUT_HANDOFF:
  Context:
    epic: "[Epic name]"
    current_step: "[Step number and name]"
    risk_level: "[Low / Medium / High]"
  Investigation_Request:
    unknown: "[What needs investigation]"
    questions:
      - "[Specific question 1]"
      - "[Specific question 2]"
    scope: "[What to investigate, what to ignore]"
    time_budget: "[Maximum investigation time]"
  After_Investigation:
    - "Update step breakdown based on findings"
    - "Revise risk assessment"
    - "Adjust dependencies if needed"
```

### SHERPA_TO_CANVAS_HANDOFF

Workflow visualization needed.

```yaml
SHERPA_TO_CANVAS_HANDOFF:
  Visualization_Request:
    type: "[dependency_graph / progress_timeline / risk_map]"
    epic: "[Epic name]"
  Data:
    steps:
      - name: "[Step name]"
        status: "[done / in_progress / pending / blocked]"
        depends_on: "[step numbers]"
    critical_path: "[step sequence]"
    parallel_groups: "[step groups]"
  Output_Format: "mermaid"
```

### SHERPA_TO_BUILDER_HANDOFF

Implementation step ready for execution.

```yaml
SHERPA_TO_BUILDER_HANDOFF:
  Step:
    number: "[N]"
    name: "[Step name]"
    description: "[What to build]"
    estimated_time: "[minutes]"
    risk_level: "[Low / Medium / High]"
  Context:
    epic: "[Epic name]"
    dependencies_met: "[list of completed prerequisite steps]"
    files_involved: "[expected files]"
  Acceptance_Criteria:
    - "[Criterion 1]"
    - "[Criterion 2]"
  After_Completion:
    - "Run tests"
    - "Commit with message: [suggested message]"
    - "Return to Sherpa for next step"
```

### SHERPA_TO_TRIAGE_HANDOFF

Emergency escalation.

```yaml
SHERPA_TO_TRIAGE_HANDOFF:
  Emergency:
    level: "[Yellow / Red / Evacuation]"
    triggered_by: "[Condition]"
  Situation:
    epic: "[Epic name]"
    progress: "[X/Y steps, Z%]"
    blocker: "[Description]"
    impact: "[What is affected]"
    deadline: "[When]"
  Current_State:
    last_commit: "[hash]"
    uncommitted_work: "[description]"
    steps_blocked: "[count and list]"
  Request:
    - "Prioritized recovery options"
    - "Impact assessment"
    - "Stakeholder communication guidance"
```

### SHERPA_TO_GUARDIAN_HANDOFF

Complex commit strategy needed.

```yaml
SHERPA_TO_GUARDIAN_HANDOFF:
  Epic:
    name: "[Epic name]"
    total_steps: "[N]"
    completed_steps: "[M]"
  Commit_Points:
    - step: "[Step N]"
      changes: "[Files changed]"
      suggested_message: "[Commit message]"
  Request:
    - "Review commit granularity"
    - "Suggest PR strategy if multi-commit"
```

### SHERPA_TO_RALLY_HANDOFF

Parallel execution request for independent task groups.

```yaml
SHERPA_TO_RALLY_HANDOFF:
  Context:
    epic: "[Epic name]"
    scope: "[S / M / L / XL]"
    phase: "[Current phase]"
  Parallel_Groups:
    - group: "[Group name]"
      chain: "[Agent1 → Agent2 → Agent3]"
      task: "[Task description]"
      files:
        exclusive_write: "[file/dir list]"
        shared_read: "[file/dir list]"
      acceptance: "[Criteria]"
    - group: "[Group name]"
      chain: "[Agent4 → Agent5]"
      task: "[Task description]"
      files:
        exclusive_write: "[file/dir list]"
        shared_read: "[file/dir list]"
      acceptance: "[Criteria]"
  Integration:
    shared_deps: "[types, config — resolved before groups start]"
    merge_strategy: "[sequential-merge | branch-merge]"
    integration_chain: "Atlas → Radar → Judge"
  After_Rally:
    - "Verify integration chain passes"
    - "Update progress tracking"
    - "Return to Sherpa for next epic step"
```

---

## Input Handoffs (Receiving)

### MAGI_TO_SHERPA_HANDOFF

Prioritized task list from Magi deliberation.

```yaml
MAGI_TO_SHERPA_HANDOFF:
  Decision:
    type: "priority"
    verdict: "[Decision summary]"
    consensus: "[3-0 / 2-1 / etc.]"
  Prioritized_Tasks:
    - task: "[Task 1]"
      priority: "P0"
      rationale: "[Why highest priority]"
    - task: "[Task 2]"
      priority: "P1"
      rationale: "[Why this order]"
  Constraints:
    - "[Constraint from deliberation]"
  Request:
    - "Break down tasks in priority order"
    - "Create dependency graph"
```

### NEXUS_TO_SHERPA_HANDOFF

Complex task needing decomposition.

```yaml
NEXUS_TO_SHERPA_HANDOFF:
  Task:
    description: "[Complex task from user]"
    agent_chain: "[Planned chain]"
  Context:
    project: "[Project context]"
    constraints: "[Time/scope constraints]"
  Request:
    - "Break down into Atomic Steps"
    - "Identify agent for each step"
    - "Create dependency graph"
    - "Assess risks"
```

### SCOUT_TO_SHERPA_HANDOFF

Investigation results to update plan.

```yaml
SCOUT_TO_SHERPA_HANDOFF:
  Investigation:
    topic: "[What was investigated]"
    findings:
      - "[Finding 1]"
      - "[Finding 2]"
    recommendations:
      - "[Recommendation 1]"
  Plan_Impact:
    - "Step X: [Modification needed]"
    - "New Step: [Discovery requires new step]"
    - "Risk Update: Step Y risk reduced"
```

---

## Output Format Template

Standard response format for every Sherpa output:

```markdown
## Sherpa's Guide

**Epic**: [Goal Name]
**Progress**: [X]/[Y] steps completed
**Risk Level**: Low / Medium / High

### NOW: [The One Thing to Do]

[Specific instruction or question for the current step]
**Risk**: [Level] [Risk description if any]
**Agent**: [Suggested agent if applicable]

### Dependencies
- Waiting on: [Any blockers]
- Unblocks: [What this enables]

### Upcoming Path
- [ ] [Next Step] [Risk]
- [ ] [Step After] [Risk]
*(...rest hidden for focus)*

---
**Status**: On Track / Drifting / Blocked
**Next Commit Point**: After this step / After step X
```
