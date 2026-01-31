# Nexus Output Formats Reference

Final output formats and handoff protocols.

---

## NEXUS_COMPLETE (AUTORUN)

```
## NEXUS_COMPLETE
Task: [Task name]
Type: [BUG|FEATURE|REFACTOR|...]
Chain: [Executed chain]

### Changes
- [File1]: [Change description]
- [File2]: [Change description]

### Verification
- Tests: [PASS/FAIL + details]
- Build: [status]

### How to Verify
1. [Verification step 1]
2. [Verification step 2]

### Risks / Follow-ups
- [Remaining risks]
- [Recommended follow-ups]
```

---

## NEXUS_COMPLETE_FULL (AUTORUN_FULL)

```
## NEXUS_COMPLETE_FULL
Task: [Task name]
Type: [BUG|FEATURE|REFACTOR|...]
Mode: AUTORUN_FULL
Complexity: [SIMPLE|MEDIUM|COMPLEX]

### Execution Summary
- Total Steps: [N]
- Parallel Branches: [N branches if any]
- Duration: [Phases completed]
- Recovery Actions: [N if any]

### Chain Executed
Sequential: [Agent1] → [Agent2] → [Agent3]
Parallel (if any):
  Branch A: [Agent4] → [Agent5]
  Branch B: [Agent6] → [Agent7]
  Merge: [Agent8]

### Changes
- [File1]: [Change description]

### Guardrail Events
| Step | Level | Trigger | Action | Result |
|------|-------|---------|--------|--------|
| 3/7 | L2 | test_failure | auto_fix | SUCCESS |

### Verification
- Tests: [PASS/FAIL + details]
- Build: [status]
- Security: [Sentinel result if applicable]
- Final Guardrail: [L2 CHECKPOINT result]

### Context Summary
- Goal: [Original goal]
- Acceptance: [All criteria met / Partial]
- Key Decisions: [List of major decisions made]

### How to Verify
1. [Verification step 1]
2. [Verification step 2]

### Risks / Follow-ups
- [Remaining risks]
- [Recommended follow-ups]

### Rollback (if needed)
- Rollback available: [Yes/No]
- Command: [git checkout / restore command]
```

---

## NEXUS_HANDOFF (Standard)

```
## NEXUS_HANDOFF
- Step: [X/Y]
- Agent: [AgentName]
- Summary: 1-3 lines
- Key findings / decisions:
  - ...
- Artifacts (files/commands/links):
  - ...
- Risks / trade-offs:
  - ...
- Open questions (blocking/non-blocking):
  - ...
- Pending Confirmations:
  - Trigger: [INTERACTION_TRIGGER name]
  - Question: [Question]
  - Options: [Available options]
  - Recommended: [Recommended option]
- User Confirmations:
  - Q: [Previous question] → A: [User's answer]
- Suggested next agent: [AgentName] (reason)
- Next action: CONTINUE
```

---

## NEXUS_HANDOFF (Extended - AUTORUN_FULL)

```
## NEXUS_HANDOFF
- Step: [X/Y]
- Branch: [branch_id or "main"]
- Agent: [AgentName]
- Summary: 1-3 lines
- Key findings / decisions:
  - ...
- Artifacts (files/commands/links):
  - ...
- Files Modified: [List of files]
- Risks / trade-offs:
  - ...
- Guardrail Events:
  - Level: [L1|L2|L3|L4 or "none"]
  - Trigger: [What triggered if any]
  - Action: [Action taken]
  - Result: [SUCCESS|FAILED|ESCALATED]
- Context Delta:
  - Added: [New knowledge/artifacts]
  - Changed: [Modified state]
- Suggested next agent: [AgentName]
- Next action: [CONTINUE|MERGE|VERIFY|ESCALATE|ABORT]
```

---

## _STEP_COMPLETE Format

```
_STEP_COMPLETE:
  Agent: [Name]
  Branch: [branch_id if parallel, else "main"]
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    type: [Output type]
    summary: [Brief summary]
    files_changed: [List if applicable]
  Handoff:
    Format: [AGENT_TO_AGENT_HANDOFF format]
    Content: [Full handoff for next agent]
  Artifacts:
    - [List of produced artifacts]
  Next: [NextAgent] | VERIFY | DONE
  Reason: [Why this next step]
```
