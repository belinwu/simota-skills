# Guardrail Integration

Defines how `_common/GUARDRAIL.md` (L1-L4) integrates with Titan's Anti-Stall Engine (L1-L5).

---

## Overview

Two safety systems operate during Titan's lifecycle:

| System | Scope | Levels | Purpose |
|--------|-------|--------|---------|
| **Guardrail** (`_common/GUARDRAIL.md`) | Per-chain execution | L1-L4 | Prevent code/security failures |
| **Anti-Stall** (Titan) | Per-phase/project | L1-L5 | Prevent delivery stalling |

These systems are complementary, operating as a three-layer defense model:

### Three-Layer Defense Model

```
┌──────────────────────────────────────────────────────────────────┐
│ Layer 3: Anti-Stall Engine (L1-L5) — Delivery Recovery          │
│ Owner: Titan                                                     │
│ Scope: Per-phase / per-project                                   │
│ Triggers: Zero progress, blocked epics, repeated failures        │
│ Actions: Retry, agent swap, scope reduction, user escalation     │
├──────────────────────────────────────────────────────────────────┤
│ Layer 2: Nexus Error Handling (L1-L5) — Chain Recovery           │
│ Owner: Nexus                                                     │
│ Scope: Per-chain execution                                       │
│ Triggers: Agent failure, chain errors, test failures             │
│ Actions: Auto-retry, inject agent, rollback, escalate to Titan   │
│ Reports: recovery_attempted field in NEXUS_COMPLETE              │
├──────────────────────────────────────────────────────────────────┤
│ Layer 1: Guardrail System (L1-L4) — Execution Quality Guard     │
│ Owner: _common/GUARDRAIL.md (enforced by Nexus)                  │
│ Scope: Per-task execution                                        │
│ Triggers: Lint warnings, test failures, security issues          │
│ Actions: Log, auto-verify, auto-recover, abort                   │
└──────────────────────────────────────────────────────────────────┘

Escalation flow: Layer 1 → Layer 2 → Layer 3
- Guardrail recovery success → no escalation (budget-free)
- Guardrail recovery failure → Nexus Error Handling (recovery_attempted tracking)
- Nexus recovery failure → Anti-Stall Engine (conditionalized entry per recovery_attempted)
```

**Key principle**: Each layer handles recovery at its scope. Higher layers only activate when lower layers exhaust their recovery options. The `recovery_attempted` field (see `nexus-integration.md`) prevents duplicate retries across layers.

---

## Trigger Integration Matrix

Guardrail events are mapped to Anti-Stall levels:

| Guardrail Level | Guardrail Action | Anti-Stall Mapping | Titan Response |
|----------------|-----------------|-------------------|---------------|
| **L1 MONITORING** | Log only | No Anti-Stall action | Continue, log in TITAN_STATE |
| **L2 CHECKPOINT** | Auto-verify | **Anti-Stall L1** if recovery fails | Retry with context → Agent swap |
| **L3 PAUSE** | Auto-recover or wait | **Anti-Stall L1-L2** | L1 retry → L2 alt approach if L1 exhausted |
| **L4 ABORT** | Immediate stop | **Immediate halt** | Rollback → assess → resume or escalate |

### Detailed Mappings

#### Guardrail L2 → Anti-Stall L1

| Guardrail Trigger | Auto-Recovery | If Recovery Fails |
|-------------------|--------------|-------------------|
| test_failure_minor (<20%) | Builder auto-fix | Anti-Stall L1.1 Retry |
| type_error | Builder type fix | Anti-Stall L1.2 Agent swap |
| security_warning | Sentinel scan | Anti-Stall L1.1 Retry with scan results |
| performance_regression (<10%) | Bolt optimization | Anti-Stall L1.3 Decompose |

#### Guardrail L3 → Anti-Stall L1-L2

| Guardrail Trigger | First Response | Escalation |
|-------------------|---------------|-----------|
| test_failure_major (>50%) | Rollback + L1.3 Decompose | L2.3 Scope Reduction |
| breaking_change | Atlas analysis + L1.1 Retry | L2.2 Skip+return |
| security_critical | Sentinel mandatory | L2.1 Alt approach |
| build_failure | Rollback + L1.1 Retry | L2.1 Alt approach |
| merge_conflict | Sequential re-exec | L2.2 Skip+return |

#### Guardrail L4 → Immediate Action

| Guardrail Trigger | Action | Recovery Path |
|-------------------|--------|-------------|
| critical_security | Rollback immediately | Sentinel full audit → resume |
| data_integrity_risk | Rollback immediately | Assess damage → manual review |
| infinite_loop_detected | Stop current chain | Anti-Stall L2+ from clean state |
| user_abort | Stop everything | Wait for user instruction |

---

## Guardrail Application Flow

During phase execution, Titan ensures Guardrails are active:

```
Titan issues NEXUS_AUTORUN_FULL
  ├─ Nexus applies Guardrail config per task type
  │   ├─ FEATURE → L2 default (post: tests_pass, build_success)
  │   ├─ SECURITY → L2 default (pre: sentinel_scan)
  │   ├─ REFACTOR → L2 default (post: tests_unchanged)
  │   └─ API_BREAKING → L3 default (pre: atlas_impact_analysis)
  ├─ On Guardrail event:
  │   ├─ L1/L2: Nexus handles internally → reports in NEXUS_HANDOFF
  │   ├─ L3: Nexus pauses → reports to Titan → Titan activates Anti-Stall
  │   └─ L4: Nexus aborts → reports to Titan → Titan rollback + assess
  └─ Titan tracks Guardrail events in TITAN_STATE
```

### Guardrail Config per Phase

| Phase | Default Level | Pre-Checks | Post-Checks |
|-------|--------------|------------|-------------|
| DISCOVER | L1 | — | Artifacts exist |
| DEFINE | L1 | — | Specs complete |
| ARCHITECT | L2 | — | ADR valid, no circular deps |
| BUILD | L2 | — | Tests pass, build success |
| HARDEN | L2 | sentinel_scan | No new vulnerabilities |
| VALIDATE | L2 | — | E2E pass, UX approved |
| LAUNCH | L3 | dry_run | Deployment healthy |
| GROW | L2 | — | Metrics tracking active |
| EVOLVE | L1 | — | Feedback collected |

---

## Anti-Stall Budget and Guardrail Interaction

### Budget Consumption Rules

| Guardrail Event | Anti-Stall Budget Consumed |
|----------------|--------------------------|
| L1 MONITORING | None (no Anti-Stall triggered) |
| L2 auto-recovery SUCCESS | None (Guardrail handled it) |
| L2 auto-recovery FAILED | 1× L1 budget |
| L3 with Titan recovery | 1× L1 or L2 budget (per recovery level used) |
| L4 ABORT | No budget — forced halt and reassess |

### Key Rules

1. **Guardrail recoveries don't consume Anti-Stall budget** — only failures that reach Titan do
2. **L4 ABORT bypasses Anti-Stall entirely** — it's an emergency stop, not a stall
3. **Multiple L2 failures in same chain** → escalate to Anti-Stall L1 (count as single attempt)
4. **L3 PAUSE duration** → if >2 cycles, treat as stall and activate Anti-Stall

---

## L4 ABORT Rollback Procedure

When Guardrail L4 triggers:

1. **Immediate halt**: Stop all running chains and Rally teams
2. **Rollback**: Revert to last known-good state (git ref or snapshot)
3. **Assess**: Classify the abort cause
4. **Report**: Update TITAN_STATE with abort details
5. **Resume path**:
   - `critical_security` → Sentinel full audit required before resume
   - `data_integrity_risk` → Manual review required before resume
   - `infinite_loop_detected` → Anti-Stall L2+ from clean state
   - `user_abort` → Wait for explicit user instruction

### Post-Abort Recovery

```
L4 ABORT received
  ├─ 1. Halt all execution
  ├─ 2. Rollback to last good state
  ├─ 3. Log: cause, affected files, chain state
  ├─ 4. Classify recovery path
  │     ├─ Recoverable → Anti-Stall L2 (skip failing component)
  │     └─ Not recoverable → L4.1 Partial delivery or L5 User
  └─ 5. Resume when recovery conditions met
```
