# Nexus Orchestration Patterns Reference

Detailed patterns for agent chain execution.

---

## Pattern A: Sequential Chain

```
Nexus → NEXUS_ROUTING → Agent1 → NEXUS_HANDOFF
                           ↓
Nexus → NEXUS_ROUTING → Agent2 → NEXUS_HANDOFF
                           ↓
Nexus → NEXUS_ROUTING → Agent3 → NEXUS_HANDOFF
                           ↓
Nexus → VERIFY → DELIVER
```

**Use when**: Steps have strict dependencies (output of one is input of next)

---

## Pattern B: Parallel Branches

```
Nexus → NEXUS_ROUTING (Branch A) → [Agent1 → Agent2] → NEXUS_HANDOFF
      → NEXUS_ROUTING (Branch B) → [Agent3 → Agent4] → NEXUS_HANDOFF
                                        ↓
Nexus → AGGREGATE (Merge branches) → NEXUS_ROUTING → MergeAgent
                                        ↓
Nexus → VERIFY → DELIVER
```

**Use when**: Independent tasks can execute simultaneously (e.g., separate features)

---

## Pattern C: Conditional Routing

```
Nexus → NEXUS_ROUTING → Agent1 → NEXUS_HANDOFF
                           ↓
Nexus → Analyze findings
           │
           ├─ [Security issue] → Sentinel → NEXUS_HANDOFF
           ├─ [Performance issue] → Bolt → NEXUS_HANDOFF
           └─ [No issues] → Continue to next step
```

**Use when**: Next agent depends on findings (e.g., Judge → Builder OR Sentinel)

---

## Pattern D: Recovery Loop

```
Nexus → NEXUS_ROUTING → Agent → NEXUS_HANDOFF
                           │
                           ├─ [SUCCESS] → Continue
                           │
                           └─ [FAILED] → Error Handler
                                    ↓
                              ┌─────────────────┐
                              │ Recovery Action │
                              │ - Retry (L1)    │
                              │ - Inject fix (L2)│
                              │ - Rollback (L3) │
                              └────────┬────────┘
                                       ↓
                              Re-execute or Escalate
```

**Use when**: Errors occur during execution (auto-recovery enabled)

---

## Pattern E: Escalation Path

```
Nexus → NEXUS_ROUTING → Agent → NEXUS_HANDOFF (Pending Confirmation)
                                        ↓
Nexus → Present to User (AskUserQuestion)
                                        ↓
User → Select option
                                        ↓
Nexus → NEXUS_ROUTING (with User Confirmation) → Agent continues
```

**Use when**: Agent encounters decision requiring user input (L4 guardrail or GUIDED mode)

---

## Pattern F: Verification Gate

```
Nexus → Chain execution complete
                   ↓
          ┌───────────────────┐
          │ VERIFICATION GATE │
          │ - Tests pass?     │
          │ - Build OK?       │
          │ - Security OK?    │
          └─────────┬─────────┘
                    │
          ┌────────┴────────┐
          ↓ PASS            ↓ FAIL
      DELIVER          RECOVERY
                           │
                    ┌──────┴──────┐
                    │ Rollback OR │
                    │ Re-execute  │
                    └─────────────┘
```

**Use when**: Critical verification before final delivery (always used in AUTORUN_FULL)

---

## Hub Communication Protocol

```
User Request
     ↓
  NEXUS (Classify & Design Chain)
     ↓
  ┌──────────────────────────────────────────────────────────────┐
  │                    NEXUS_ROUTING                             │
  │  (Context, Goal, Step, Constraints, Expected Output)         │
  └──────────────────────────────────────────────────────────────┘
     ↓
  Agent A executes
     ↓
  ┌──────────────────────────────────────────────────────────────┐
  │                    NEXUS_HANDOFF                             │
  │  (Summary, Artifacts, Risks, Suggested Next, _STEP_COMPLETE) │
  └──────────────────────────────────────────────────────────────┘
     ↓
  NEXUS (Aggregate, Route, or Verify)
     ↓
  Next Agent or DELIVER
```
