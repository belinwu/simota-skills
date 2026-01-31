# Nexus Guardrail System Reference

Guardrails, context management, and state tracking for AUTORUN_FULL.

---

## Guardrail Levels

| Level | Name | Trigger | Action |
|-------|------|---------|--------|
| L1 | MONITORING | minor_warning, lint_warning | Log only, continue execution |
| L2 | CHECKPOINT | test_failure<20%, security_warning | Auto-verify, conditional continue |
| L3 | PAUSE | test_failure>50%, breaking_change | Pause, attempt auto-recovery |
| L4 | ABORT | critical_security, data_integrity_risk | Immediate stop, rollback |

---

## Guardrail Configuration by Task Type

| Task Type | Default Level | Pre-check | Post-check |
|-----------|---------------|-----------|------------|
| FEATURE | L2 | - | Tests pass |
| SECURITY | L2 | Sentinel scan | No new vulnerabilities |
| REFACTOR | L2 | - | Tests unchanged |
| API (breaking) | L3 | Atlas impact | All consumers updated |
| INCIDENT | L3 | - | Service restored |
| INFRA | L3 | - | Health checks pass |

---

## Auto-Recovery Actions

| Trigger | Level | Auto-Recovery |
|---------|-------|---------------|
| test_failure<20% | L2 | Re-run failed tests, fix if obvious |
| test_failure 20-50% | L2 | Inject Builder for targeted fixes |
| test_failure>50% | L3 | Rollback to last checkpoint, re-decompose with Sherpa |
| security_warning | L2 | Add Sentinel scan, block if critical |
| breaking_change | L3 | Pause, verify with Atlas, require migration plan |
| type_error | L2 | Return to Builder for type strengthening |

---

## Guardrail Event Format

```
_GUARDRAIL_EVENT:
  Level: [L1|L2|L3|L4]
  Trigger: [What triggered this]
  Step: [X/Y]
  Agent: [Current agent]
  Action: [CONTINUE|VERIFY|PAUSE|ROLLBACK|ABORT]
  Details: [Specifics]
  Recovery: [Recovery action if applicable]
```

---

## Context Hierarchy

```
L1_GLOBAL (Chain-wide)
├── goal: "User's original request"
├── acceptance_criteria: ["Criterion 1", "Criterion 2"]
├── chain_overview: "Agent1 → Agent2 → Agent3"
└── shared_knowledge: {key findings from all agents}

L2_PHASE (Per phase)
├── phase_inputs: {data entering this phase}
├── phase_outputs: {data produced by this phase}
└── dependencies: {what this phase needs/provides}

L3_STEP (Per agent step)
├── artifacts: [files, commands, links]
├── decisions: [key choices made]
└── risks: [identified risks]

L4_AGENT (Agent-specific)
├── agent_state: {internal state}
└── pending_confirmations: {questions for user}
```

---

## State Record Format

```
_NEXUS_STATE:
  Task: [Task name]
  Type: [BUG|INCIDENT|API|FEATURE|REFACTOR|OPTIMIZE|SECURITY|DOCS|INFRA]
  Mode: [AUTORUN_FULL|AUTORUN|GUIDED|INTERACTIVE]
  Phase: [PLAN|PREPARE|CHAIN_SELECT|EXECUTE|AGGREGATE|VERIFY|DELIVER]
  Chain: Agent1(DONE) → Agent2(DOING) → Agent3(PENDING)
  Step: [X/Y]
  Status: [ON_TRACK|BLOCKED|RECOVERING|PAUSED]
  Guardrail: [L1|L2|L3|L4] - [Last event summary]
  Acceptance: [Condition1: OK | Condition2: PENDING | ...]
```

---

## Parallel Branch Context

```
_PARALLEL_CONTEXT:
  main_context: [snapshot_id of fork point]
  branches:
    - branch_id: A
      context_delta: {...}
    - branch_id: B
      context_delta: {...}
  merge_strategy: [CONCAT|OVERRIDE|MANUAL]
```
