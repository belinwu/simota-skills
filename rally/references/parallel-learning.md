# Parallel Learning (HARMONIZE)

## Overview

Rally's learning subsystem for improving parallel execution outcomes through cross-session analysis of team composition, sizing, and coordination effectiveness.

**Responsibility separation:**

| Subsystem | Owner | Focus |
|-----------|-------|-------|
| Parallel execution learning | Rally (HARMONIZE) | Team composition effectiveness, sizing optimization, subagent_type/model selection tuning |
| Cross-agent knowledge synthesis | Lore | Pattern aggregation across all agents |
| Quality PDCA | Hone | Output quality measurement and improvement cycles |
| Known-pattern auto-remediation | Mend | Automated fixes for recognized failure patterns |

HARMONIZE learns *within* Rally's parallel-orchestration domain — which team compositions excel at which task types, when larger teams outperform smaller ones, and what subagent_type/model combinations yield optimal results. Extracted patterns are shared to Lore for cross-agent synthesis; quality metrics flow to Hone for PDCA integration.

---

## HARMONIZE Workflow

```
COLLECT → EVALUATE → EXTRACT → ADAPT → SAFEGUARD → RECORD
```

| Phase | Purpose | Key Actions |
|-------|---------|-------------|
| COLLECT | Parallel execution result gathering | Capture session completion data: team_size, subagent_types, models, task_count, ownership_conflicts, timing, user_interventions |
| EVALUATE | Effectiveness assessment | Calculate TES, update Team Design Matrix, compare against historical baseline |
| EXTRACT | Pattern identification | Identify team composition × task-type success rate patterns, optimal team size conditions, subagent_type effectiveness |
| ADAPT | Adaptation proposal | Update team size defaults, improve subagent_type/model selection heuristics, adjust file ownership patterns |
| SAFEGUARD | Change verification | Verify consistency with existing file-ownership-protocol, create rollback snapshot |
| RECORD | Learning persistence | Write journal entry, share patterns with Lore, share quality data with Hone |

### Phase Details

#### COLLECT

Capture after every team execution (RY-01):

```yaml
EXECUTION_DATA:
  session_id: <unique session identifier>
  task_type: <feature | bugfix | refactor | migration | test>
  team_pattern: <Frontend+Backend | Feature_Parallel | Pipeline | Specialist_Team | Code+Test+Docs>
  team_size: <int>
  subagent_types:
    - name: <teammate name>
      type: <general-purpose | Explore | Plan>
      model: <sonnet | opus | haiku>
      role: <description>
  task_count: <int>
  completed_tasks: <int>
  retried_tasks: <int>
  ownership_conflicts: <int>
  total_file_ops: <int>
  timing:
    total_seconds: <int>
    estimated_sequential_seconds: <int>
  integration_checks:
    build_pass: <bool>
    tests_pass: <bool>
    lint_pass: <bool>
  user_interventions:
    - type: <team_size_override | composition_override | task_reassign | manual_fix | abort>
      detail: <description>
  final_status: <SUCCESS | PARTIAL | BLOCKED | FAILED>
```

#### EVALUATE

Calculate Team Effectiveness Score (see TES section below). Compare against:
- Historical average for same team pattern
- Historical average for same task type
- Previous execution with same team composition (if applicable)

#### EXTRACT

Identify patterns from accumulated data (minimum 3 data points):
- **Composition-task fitness**: Which team patterns consistently succeed for which task types
- **Size optimization**: Conditions where larger/smaller teams outperform defaults
- **Subagent effectiveness**: Which subagent_type/model combinations yield best results per role
- **Conflict patterns**: File ownership configurations that prevent or cause conflicts

#### ADAPT

Generate concrete adaptation proposals:
- Team size default updates (e.g., "default to 3 for bugfix tasks based on TES data")
- Subagent_type/model selection heuristic improvements (e.g., "prefer Explore for investigation subtasks in refactor")
- File ownership pattern adjustments (e.g., "split shared test directories for Feature_Parallel pattern")
- Team pattern recommendations (e.g., "recommend Pipeline for migration tasks based on TES gap")

Each proposal must include: rationale, expected TES impact, rollback plan.

#### SAFEGUARD

Before applying any adaptation:
1. Verify existing file-ownership-protocol is preserved (exclusive_write/shared_read rules) — **invariant, never modify**
2. Check proposal against established Team Design Patterns — reject if contradiction
3. Create snapshot of current defaults and heuristic state
4. Verify minimum evidence threshold (≥ 3 data points)
5. For TES ≥ B configurations: require human approval (do not auto-adapt)
6. Ensure change volume stays within session limit (max 3 parameter changes)

#### RECORD

Record learning outcomes:
1. Write feedback record to `.agents/rally.md`
2. Share extracted patterns to Lore via `RALLY_TO_LORE_HANDOFF`
3. Share quality metrics to Hone via quality data channel
4. Update Team Design Matrix if sufficient data accumulated

---

## Learning Triggers

| ID | Condition | Scope | Actions |
|----|-----------|-------|---------|
| RY-01 | Team execution complete (every time) | Lightweight | COLLECT + EVALUATE only |
| RY-02 | Same team pattern fails/conflicts 3+ times | Full cycle | All 6 HARMONIZE phases |
| RY-03 | User manually overrides team size or composition | Full cycle | All 6 HARMONIZE phases |
| RY-04 | Quality feedback arrives from Judge or Hone | Medium | COLLECT + EVALUATE + EXTRACT + RECORD |
| RY-05 | Lore sends parallel execution pattern notification | Medium | COLLECT + EVALUATE + EXTRACT + RECORD |
| RY-06 | 30+ days since last full HARMONIZE cycle | Full cycle | All 6 HARMONIZE phases |

### Trigger Priority

When multiple triggers fire simultaneously:
1. RY-03 (user override — highest signal value)
2. RY-02 (repeated failures — urgent)
3. RY-04 (quality feedback — actionable)
4. RY-05 (Lore pattern — opportunity)
5. RY-06 (scheduled review — lowest urgency)
6. RY-01 (routine collection — always runs)

---

## Team Effectiveness Score (TES)

```
TES = Parallel_Efficiency × 0.30
    + Task_Economy × 0.20
    + Conflict_Prevention × 0.20
    + Integration_Quality × 0.20
    + User_Autonomy × 0.10
```

### Components

| Component | Weight | Definition | Range |
|-----------|--------|------------|-------|
| Parallel_Efficiency | 0.30 | Speedup ratio from parallelization: `estimated_sequential_time / actual_parallel_time` (capped at 1.0) | 0.0–1.0 |
| Task_Economy | 0.20 | Task completion rate adjusted for retries: `completed_tasks / total_tasks × (1 - retry_rate)` | 0.0–1.0 |
| Conflict_Prevention | 0.20 | File ownership conflict avoidance rate: `1 - (conflicts / total_file_ops)` | 0.0–1.0 |
| Integration_Quality | 0.20 | Integration verification pass rate: `(build + tests + lint) / total_checks` | 0.0–1.0 |
| User_Autonomy | 0.10 | Absence of user intervention: `1 - (user_overrides / total_decisions)` | 0.0–1.0 |

### Grading Scale

| Grade | TES Range | Interpretation |
|-------|-----------|----------------|
| A | ≥ 0.90 | Excellent — configuration is well-optimized |
| B | ≥ 0.80 | Good — no auto-changes permitted (human approval required) |
| C | ≥ 0.70 | Acceptable — adaptation candidates |
| D | ≥ 0.60 | Below standard — systematic review recommended |
| F | < 0.60 | Poor — full HARMONIZE cycle required |

### Data Requirements

- TES calculation requires ≥ 3 data points for the same task-type/team-pattern combination
- Grades are provisional until ≥ 5 data points
- Trend analysis requires ≥ 10 data points
- Below minimum threshold, TES is reported as `INSUFFICIENT_DATA`

---

## Team Design Matrix

Track cumulative team composition effectiveness by task type. Each cell represents a grade derived from historical TES data.

```
                 | feature | bugfix | refactor | migration | test |
Frontend+Backend |    —    |   —    |    —     |     —     |  —   |
Feature Parallel |    —    |   —    |    —     |     —     |  —   |
Pipeline         |    —    |   —    |    —     |     —     |  —   |
Specialist Team  |    —    |   —    |    —     |     —     |  —   |
Code+Test+Docs   |    —    |   —    |    —     |     —     |  —   |
```

`—` = `INSUFFICIENT_DATA` (fewer than 3 data points). Default grade is B until sufficient data.

### Update Rules

1. After each team session (RY-01), record team-pattern × task-type outcome
2. When a cell reaches ≥ 3 data points, calculate grade from TES average
3. Apply same A/B/C/D/F grading scale as TES
4. Matrix informs team pattern selection for future sessions

### Usage in Execution

- When designing a team for a task, consult the matrix for the task-type column
- Prefer team patterns with higher grades for the given task type
- If all patterns show `INSUFFICIENT_DATA`, use default selection heuristics from `references/team-design-patterns.md`

---

## Adaptation Rules

### Allowed Scope by Grade

| Current TES Grade | Allowed Adaptations | Approval |
|-------------------|---------------------|----------|
| A (≥ 0.90) | No auto-changes — human approval required for any modification | Human required |
| B (≥ 0.80) | No auto-changes — human approval required | Human required |
| C (≥ 0.70) | Team size default adjustments, subagent_type preference tuning | Auto with snapshot |
| D (≥ 0.60) | Size defaults + model selection heuristics + pattern recommendations | Auto with snapshot |
| F (< 0.60) | Full review — team pattern, size, subagent_type, model, and ownership reassessment | Auto with snapshot |

### Adaptation Types

| Type | Example | Max per Session |
|------|---------|-----------------|
| Team size default change | Default to 3 for bugfix tasks (was 2) | 2 |
| Subagent_type preference | Prefer Explore for investigation subtasks in refactor | 1 |
| Model selection heuristic | Use opus for complex migration subtasks | 1 |
| Team pattern recommendation | Recommend Pipeline for migration tasks | 1 |
| Ownership pattern refinement | Split shared test directories for parallel patterns | 1 |

**Total maximum: 3 parameter default changes per session.**

### Application Process

1. **Propose**: Generate adaptation with rationale and expected TES impact
2. **Validate**: Run SAFEGUARD checks (file-ownership invariant, evidence threshold, grade ceiling)
3. **Snapshot**: Save current configuration state for rollback
4. **Apply**: Implement the adaptation
5. **Monitor**: Track TES for next 3 executions to verify improvement

---

## Safety Guardrails

| Mechanism | Rule | Rationale |
|-----------|------|-----------|
| Change volume limit | Maximum 3 parameter default changes per session | Prevent cascading unintended effects |
| Auto-adaptation ceiling | TES ≥ B configurations require human approval | Protect well-performing configurations |
| Rollback snapshot | Save configuration state before every adaptation | Enable instant rollback on regression |
| Diminishing returns detection | 3 consecutive TES improvements < 0.02 → pause HARMONIZE | Avoid churn on marginal gains |
| Lore sync mandatory | All extracted patterns must be shared to Lore | Prevent knowledge silos |
| Minimum evidence | No adaptation with < 3 execution data points | Prevent overfitting to outliers |
| File ownership invariant | Never modify existing exclusive_write/shared_read protocol | Preserve parallel safety guarantees |

### Rollback Protocol

1. Detect regression: TES drops ≥ 0.10 after adaptation (monitored over next 3 executions)
2. Load pre-adaptation snapshot
3. Restore previous defaults and heuristic state
4. Record rollback event in journal with root cause analysis
5. Share rollback event to Lore as negative pattern

---

## Integration Points

| Partner | Direction | Data Exchanged |
|---------|-----------|----------------|
| Lore | Rally → Lore | Team composition patterns, TES trends, conflict taxonomies |
| Lore | Lore → Rally | Cross-agent parallel patterns, validated best practices |
| Hone | Rally → Hone | Parallel execution quality data (TES scores, completion rates) |
| Hone/Judge | Hone/Judge → Rally | Quality feedback, output quality assessment (RY-04) |
| Nexus | Rally → Nexus | Team execution reports, parallel performance data |
| Guardian | Rally → Guardian | Merged output for PR preparation |
| Radar | Rally → Radar | Integrated results for test verification |

### Lore Sync Protocol

**Rally → Lore (pattern share):**

```yaml
RALLY_TO_LORE_PATTERN:
  type: PARALLEL_EXECUTION_PATTERN
  pattern_name: <descriptive name>
  source_data:
    task_type: <task type>
    team_pattern: <team pattern>
    team_size: <int>
    sample_size: <int>
    tes_impact: <float>
  pattern_detail: <description>
  confidence: <HIGH | MEDIUM | LOW>
  actionable: <bool>
```

**Lore → Rally (pattern notification):**

```yaml
LORE_TO_RALLY_PATTERN:
  type: PARALLEL_PATTERN_UPDATE
  pattern_name: <descriptive name>
  source_agents: <list of contributing agents>
  recommendation: <action to consider>
  priority: <HIGH | MEDIUM | LOW>
```

---

## Templates

### Session Feedback Record

```markdown
## Team Session Feedback — <session_id>

**Date:** YYYY-MM-DD
**Task Type:** <feature | bugfix | refactor | migration | test>
**Team Pattern:** <Frontend+Backend | Feature_Parallel | Pipeline | Specialist_Team | Code+Test+Docs>
**Team Size:** <int> | **Subagent Types:** <type list> | **Models:** <model list>
**Final Status:** <SUCCESS | PARTIAL | BLOCKED | FAILED>
**TES:** <score> (Grade: <A-F>) | **Previous TES:** <score> (Grade: <A-F>)

### Component Scores
| Component | Score | Note |
|-----------|-------|------|
| Parallel_Efficiency | <0.00-1.00> | |
| Task_Economy | <0.00-1.00> | |
| Conflict_Prevention | <0.00-1.00> | |
| Integration_Quality | <0.00-1.00> | |
| User_Autonomy | <0.00-1.00> | |

### Task Summary
- Total tasks: <int> | Completed: <int> | Retried: <int>
- Ownership conflicts: <int> / <total_file_ops> file operations

### User Interventions
- <intervention or "None">

### Observations
- <key observation 1>
- <key observation 2>
```

### Team Profile Update

```markdown
## Team Profile Update — <date>

**Team Pattern:** <pattern name>
**Task Type:** <task type>
**Previous Grade:** <grade or INSUFFICIENT_DATA>
**New Grade:** <grade>
**Data Points:** <count>

### Evidence
- TES average: <float> over <count> sessions
- Conflict rate: <percentage>
- Notable strengths: <list>
- Notable weaknesses: <list>
```

### Adaptation Log

```markdown
## Adaptation Log — <date>

**Trigger:** <RY-xx>
**Current TES:** <score> (Grade: <grade>)
**Target TES:** <expected score>

### Change
- **Type:** <adaptation type>
- **Detail:** <specific change>
- **Rationale:** <why this change>

### Safeguard Check
- File ownership invariant: PASS / FAIL
- Evidence threshold (≥ 3): PASS / FAIL
- Grade ceiling check: PASS / FAIL
- Snapshot saved: <snapshot identifier>

### Outcome (post-monitoring)
- TES after 3 executions: <score>
- Rollback needed: YES / NO
```
