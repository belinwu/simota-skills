# Loop Execution Learning (REFINE)

## Overview

Orbit's learning subsystem for improving loop execution through outcome analysis.

**Responsibility separation:**

| Subsystem | Owner | Focus |
|-----------|-------|-------|
| Loop execution learning | Orbit (REFINE) | Contract design effectiveness, parameter optimization, failure pattern tracking |
| Cross-agent knowledge synthesis | Lore | Pattern aggregation across all agents |
| Quality PDCA | Judge | Output quality measurement and improvement cycles |
| Known-pattern auto-remediation | Mend | Automated fixes for recognized failure patterns |

REFINE learns *within* Orbit's loop-ops domain — which contract designs succeed, which parameters are optimal per tier, and which failure patterns recur. Extracted patterns are shared to Lore for cross-agent synthesis; quality metrics flow to Judge for PDCA integration.

---

## REFINE Workflow

```
OBSERVE → MEASURE → ANALYZE → IMPROVE → SAFEGUARD → JOURNAL
```

| Phase | Purpose | Key Actions |
|-------|---------|-------------|
| OBSERVE | Execution result collection | Capture loop completion data: iterations, final status, failure events, recovery actions, user interventions, timing per iteration |
| MEASURE | Effectiveness evaluation | Calculate LES, compare against historical baseline for same tier/complexity |
| ANALYZE | Pattern identification | Identify success/failure patterns, root cause analysis, tier/parameter fitness evaluation |
| IMPROVE | Adaptation proposal | Propose contract template improvements, default parameter adjustments, failure taxonomy refinements |
| SAFEGUARD | Change verification | Verify consistency with existing Patterns (1-9) and Anti-patterns (AP-1~11), create rollback snapshot |
| JOURNAL | Learning record | Record findings in journal, share patterns to Lore, share quality data to Judge |

### Phase Details

#### OBSERVE

Capture after every loop completion (RF-01):

```yaml
OBSERVATION_DATA:
  loop_id: <loop directory name>
  tier: <Light | Standard | Heavy | Marathon>
  total_iterations: <int>
  max_iterations: <configured limit>
  final_status: <DONE | BLOCKED | MAX_ITER | USER_ABORT>
  failure_events:
    - iteration: <int>
      category: <taxonomy class>
      recovery_action: <action taken>
      recovery_success: <bool>
  user_interventions:
    - iteration: <int>
      type: <parameter_change | manual_fix | abort>
      detail: <description>
  timing:
    total_seconds: <int>
    avg_iteration_seconds: <float>
  contract_quality:
    ac_count: <int>
    ac_measurable_ratio: <float>
    goal_clarity: <Strong | Adequate | Weak | Vague>
```

#### MEASURE

Calculate Loop Effectiveness Score (see LES section below). Compare against:
- Historical average for same tier
- Historical average for same goal complexity (AC count range)
- Previous execution of same/similar loop (if re-run)

#### ANALYZE

Identify patterns from accumulated data (minimum 3 data points):
- **Success patterns**: Parameter combinations with consistently high LES
- **Failure patterns**: Recurring failure category sequences, tier mismatches
- **Parameter fitness**: Which defaults work well per tier vs. which get overridden

#### IMPROVE

Generate concrete adaptation proposals:
- Contract template adjustments (e.g., add checklist item for common failure mode)
- Default parameter value changes (e.g., increase RETRY_LIMIT for Heavy tier)
- Failure taxonomy refinements (e.g., new sub-category for recurring pattern)

Each proposal must include: rationale, expected LES impact, rollback plan.

#### SAFEGUARD

Before applying any adaptation:
1. Check proposal against Anti-patterns AP-1~AP-11 — reject if any violation
2. Check proposal against established Patterns 1-9 — reject if contradiction
3. Create snapshot of current defaults and taxonomy state
4. Verify minimum evidence threshold (≥ 3 data points)
5. For LES ≥ B configurations: require human approval (do not auto-adapt)

#### JOURNAL

Record learning outcomes:
1. Write feedback record to `.agents/orbit.md`
2. Share extracted patterns to Lore via `ORBIT_TO_LORE_HANDOFF`
3. Share quality metrics to Judge via quality data channel
4. Update local parameter baseline if adaptation was applied

---

## Learning Triggers

| ID | Condition | Scope | Actions |
|----|-----------|-------|---------|
| RF-01 | Loop execution complete (every time) | Lightweight | OBSERVE + MEASURE only |
| RF-02 | Same tier hits BLOCKED or MAX_ITER 3+ times | Full cycle | All 6 REFINE phases |
| RF-03 | User manually overrides parameters | Full cycle | All 6 REFINE phases (parameter fitness signal) |
| RF-04 | Quality feedback arrives from Judge | Medium | OBSERVE + MEASURE + ANALYZE + JOURNAL |
| RF-05 | Lore sends loop-related pattern notification | Medium | OBSERVE + MEASURE + ANALYZE + JOURNAL |
| RF-06 | 30+ days since last full REFINE cycle | Full cycle | All 6 REFINE phases (staleness prevention) |

**Priority when multiple triggers fire:** RF-02/RF-03 (full cycle) takes precedence. Lightweight RF-01 data is consumed by any concurrent full/medium cycle.

---

## Loop Effectiveness Score (LES)

```
LES = Completion_Rate × 0.30
    + Iteration_Economy × 0.25
    + Recovery_Effectiveness × 0.20
    + Contract_Quality × 0.15
    + User_Autonomy × 0.10
```

### Components

| Component | Weight | Definition | Range |
|-----------|--------|------------|-------|
| Completion_Rate | 0.30 | Fraction of loops reaching DONE (per tier, trailing 10 executions) | 0.0–1.0 |
| Iteration_Economy | 0.25 | `1 - (actual_iterations / max_iterations)` — higher is better | 0.0–1.0 |
| Recovery_Effectiveness | 0.20 | Fraction of failure events successfully recovered without user intervention | 0.0–1.0 |
| Contract_Quality | 0.15 | `ac_measurable_ratio × goal_clarity_score` (Strong=1.0, Adequate=0.8, Weak=0.5, Vague=0.2) | 0.0–1.0 |
| User_Autonomy | 0.10 | `1 - (user_interventions / total_iterations)` — fewer interventions is better | 0.0–1.0 |

### Grading Scale

| Grade | LES Range | Interpretation |
|-------|-----------|----------------|
| A | ≥ 0.90 | Excellent — configuration is well-optimized |
| B | ≥ 0.80 | Good — minor improvements possible |
| C | ≥ 0.70 | Adequate — specific areas need attention |
| D | ≥ 0.60 | Below standard — systematic review required |
| F | < 0.60 | Poor — fundamental issues in contract or parameters |

**Data requirements:** LES requires ≥ 3 completed loop executions for the same tier to be considered valid. Below 3 data points, LES is reported as `INSUFFICIENT_DATA`.

---

## Adaptation Rules

### Allowed Scope by Grade

| Current Grade | Allowed Adaptations | Approval |
|---------------|---------------------|----------|
| A (≥ 0.90) | No auto-changes — human approval required for any modification | Human required |
| B (≥ 0.80) | No auto-changes — human approval required | Human required |
| C (≥ 0.70) | Default parameter adjustments within tier bounds | Auto with snapshot |
| D (≥ 0.60) | Parameter adjustments + contract template suggestions | Auto with snapshot |
| F (< 0.60) | Full review — parameter, contract, and tier reassignment proposals | Auto with snapshot |

### Adaptation Types

| Type | Example | Max per Session |
|------|---------|-----------------|
| Parameter default change | Increase RETRY_LIMIT from 3 to 4 for Heavy tier | 3 total |
| Tier threshold adjustment | Lower Heavy tier AC threshold from 6 to 5 | 1 |
| Contract template addition | Add recovery checklist to goal.md template | 1 |
| Failure taxonomy refinement | Add TOOL_FAILURE sub-category for timeout vs. crash | 1 |
| Verification gate tightening | Require dual verification for Marathon tier | 1 |
| Default script enhancement | Add health check to bootstrap.sh template | 1 |

### Application Process

1. **Propose**: Generate adaptation with rationale and expected LES impact
2. **Validate**: Run SAFEGUARD checks (anti-pattern, pattern consistency, evidence threshold)
3. **Snapshot**: Save current configuration state for rollback
4. **Apply**: Implement the adaptation
5. **Monitor**: Track LES for next 3 executions to verify improvement

---

## Safety Guardrails

| Mechanism | Rule | Rationale |
|-----------|------|-----------|
| Change volume limit | Maximum 3 parameter default changes per session | Prevent cascading unintended effects |
| Auto-adaptation ceiling | LES ≥ B configurations require human approval | Protect well-performing configurations |
| Rollback snapshot | Save configuration state before every adaptation | Enable instant rollback on regression |
| Diminishing returns detection | 3 consecutive LES improvements < 0.02 → pause REFINE | Avoid churn on marginal gains |
| Lore sync mandatory | All extracted patterns must be shared to Lore | Prevent knowledge silos |
| Minimum evidence | No adaptation with < 3 execution data points | Prevent overfitting to outliers |
| Anti-pattern invariant | Reject any change that violates AP-1~AP-11 | Preserve established safety boundaries |

### Rollback Protocol

1. Detect regression: LES drops ≥ 0.05 after adaptation
2. Load pre-adaptation snapshot
3. Restore previous parameter/template state
4. Record rollback event in journal with root cause
5. Share rollback event to Lore as negative pattern

---

## Integration Points

| Partner | Direction | Data Exchanged |
|---------|-----------|----------------|
| Lore | Orbit → Lore | Loop execution patterns, failure taxonomy data, LES trends |
| Lore | Lore → Orbit | Cross-agent loop patterns, validated best practices |
| Judge | Orbit → Judge | Loop quality data (LES scores, completion rates) |
| Judge | Judge → Orbit | Quality feedback, verification assessment (RF-04) |
| Nexus | Orbit → Nexus | Loop performance reports, tier effectiveness data |
| Builder | Orbit → Builder | Script template improvement patches |
| Guardian | Orbit → Guardian | Commit scope policy refinements from loop analysis |

### Lore Sync Protocol

**Orbit → Lore (pattern share):**

```yaml
ORBIT_TO_LORE_PATTERN:
  type: LOOP_EXECUTION_PATTERN
  pattern_name: <descriptive name>
  source_data:
    tier: <tier>
    sample_size: <int>
    les_impact: <float>
  pattern_detail: <description>
  confidence: <HIGH | MEDIUM | LOW>
  actionable: <bool>
```

**Lore → Orbit (pattern notification):**

```yaml
LORE_TO_ORBIT_PATTERN:
  type: LOOP_PATTERN_UPDATE
  pattern_name: <descriptive name>
  source_agents: <list of contributing agents>
  recommendation: <action to consider>
  priority: <HIGH | MEDIUM | LOW>
```

---

## Templates

### Feedback Record

```markdown
## Loop Feedback Record — <loop_id>

**Date:** YYYY-MM-DD
**Tier:** <Light | Standard | Heavy | Marathon>
**Final Status:** <DONE | BLOCKED | MAX_ITER | USER_ABORT>
**Iterations:** <actual> / <max>
**LES:** <score> (Grade: <A-F>)

### Component Scores
| Component | Score | Note |
|-----------|-------|------|
| Completion_Rate | <0.00-1.00> | |
| Iteration_Economy | <0.00-1.00> | |
| Recovery_Effectiveness | <0.00-1.00> | |
| Contract_Quality | <0.00-1.00> | |
| User_Autonomy | <0.00-1.00> | |

### Observations
- <key observation 1>
- <key observation 2>

### Patterns Identified
- <pattern or "None">
```

### Adaptation Log

```markdown
## Adaptation Log — <date>

**Trigger:** <RF-xx>
**Current LES:** <score> (Grade: <grade>)
**Target LES:** <expected score>

### Change
- **Type:** <adaptation type>
- **Detail:** <specific change>
- **Rationale:** <why this change>

### Safeguard Check
- Anti-pattern compliance: PASS / FAIL
- Pattern consistency: PASS / FAIL
- Evidence threshold (≥ 3): PASS / FAIL
- Snapshot saved: <path>

### Outcome (post-monitoring)
- LES after 3 executions: <score>
- Rollback needed: YES / NO
```
