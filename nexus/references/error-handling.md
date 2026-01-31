# Nexus Error Handling Reference

Error levels, recovery flow, and escalation procedures.

---

## Error Levels

### Level 1 - AUTO_RETRY (Transient Errors)
- Syntax error → Re-execute with the same agent (max 3 retries)
- Test failure (1st time) → Fix with Builder and retest
- Lint error → Auto-fix
- Network timeout → Retry with backoff

### Level 2 - AUTO_ADJUST (Recoverable Issues)
- test_failure<50% → Inject recovery agent (Builder for fixes)
- Type errors → Return to Builder for type strengthening
- Minor security warning → Add Sentinel scan step
- Performance degradation detected → Insert Bolt

### Level 3 - ROLLBACK (Significant Failures)
- test_failure≥50% → Rollback to last checkpoint, re-decompose with Sherpa
- Breaking change detected → Rollback, require migration plan
- Merge conflict in parallel execution → Rollback branch, resolve sequentially

### Level 4 - ESCALATE (Human Required)
- Blocking unknowns → Ask user (max 5 questions)
- Missing prerequisites → Pause task, confirm requirements
- External dependency issues → Check environment with Gear
- Recovery failed after 3 attempts → Request human guidance
- Ambiguous acceptance criteria → Clarify with user

### Level 5 - ABORT (Critical Issues)
- No resolution after 3 escalations
- User explicitly requests abort
- Fatal system error
- Critical security vulnerability detected (L4 guardrail)
- Data integrity risk detected

---

## Recovery Flow

```
Error Detected
    │
    ▼
┌─────────────┐
│ Classify    │ → Determine error level
└─────────────┘
    │
    ▼ (L1-L3)
┌─────────────┐
│ Auto-Handle │ → Execute recovery action
└─────────────┘
    │
    ├─ Success → Continue execution
    │
    ▼ (Failed)
┌─────────────┐
│ Escalate    │ → Bump to next level
└─────────────┘
    │
    ├─ L4: Human intervention
    │
    ▼ (No resolution)
┌─────────────┐
│ Abort       │ → L5: Stop and rollback
└─────────────┘
```

---

## Error Event Format

```
_ERROR_EVENT:
  Level: [L1|L2|L3|L4|L5]
  Type: [Error type]
  Step: [X/Y]
  Agent: [Current agent]
  Details: [Error details]
  Action: [Recovery action taken]
  Result: [SUCCESS|FAILED|ESCALATED|ABORTED]
```
