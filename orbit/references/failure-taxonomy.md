# Failure Taxonomy

## Class Definitions

### CONTRACT_MISSING
- Missing/invalid loop artifacts
- Typical causes: bootstrap skipped, malformed goal template
- First response: rebuild minimal contract files

### STATE_DRIFT
- Iteration counters disagree across artifacts
- Typical causes: interrupted run, manual edit to `state.env`
- First response: re-sync to latest evidence source

### VERIFY_GAP
- DONE emitted without successful verification evidence
- Typical causes: premature completion, skipped verify command
- First response: downgrade to CONTINUE and run missing checks

### COMMIT_SCOPE_RISK
- Potential inclusion of unrelated baseline dirty paths
- Typical causes: global `git add -A` usage
- First response: candidate path extraction and scoped staging

### TOOL_FAILURE
- Runner or executor repeated failures
- Typical causes: environment mismatch, auth/session issues
- First response: bounded retry and targeted recovery branch

## Priority

| Severity | Classes | Action |
|----------|---------|--------|
| P0 | VERIFY_GAP (critical), destructive COMMIT_SCOPE_RISK | stop and confirm |
| P1 | STATE_DRIFT, CONTRACT_MISSING | recover then continue |
| P2 | TOOL_FAILURE (intermittent) | retry policy |

## Reporting Schema

```yaml
ORBIT_FAILURE_REPORT:
  class: "<taxonomy class>"
  severity: "P0|P1|P2"
  evidence:
    - "<file:line>"
  impact: "<what breaks>"
  recommendation: "<smallest reversible action>"
```

## Risk Classification ↔ Failure Taxonomy Mapping

Full mapping from Daily Process Step 2 (Contract Check score) through Step 3 (Risk Classification) to Step 3 next action.

| Step 2 Score | Step 2 Finding | Failure Class | Severity | Step 3 Next Action |
|-------------|--------------|--------------|---------|------------------|
| Missing | goal.md does not exist | CONTRACT_MISSING | P1 | Rebuild contract in bootstrap mode |
| Missing | progress.md is empty | CONTRACT_MISSING | P1 | Initialize iteration 0 entry |
| Missing | state.env does not exist | CONTRACT_MISSING | P1 | Generate with NEXT_ITERATION=1, LAST_STATUS=READY |
| Partial | Status footer missing or malformed | CONTRACT_MISSING | P1 | Re-apply footer and repair structure |
| Partial | state.env and progress.md iteration mismatch | STATE_DRIFT | P1 | Re-sync state.env using progress as source of truth |
| Partial | done.md present + verify evidence unclear | VERIFY_GAP | P0 | Downgrade DONE to CONTINUE |
| Partial | Candidate scope may include baseline paths | COMMIT_SCOPE_RISK | P0 | Delegate commit arbitration to Guardian |
| Partial | runner.log contains 1+ failure entries | TOOL_FAILURE | P2 | Apply retry policy and check environment |
| Complete | TOOL_FAILURE reached RETRY_LIMIT | TOOL_FAILURE | P1 | Investigate via ORBIT_TO_SCOUT_HANDOFF |
| Complete | All artifacts consistent, no anomalies | (none) | — | Safely proceed to next iteration |

### Rules for Multiple Failure Classes

- **Treat highest severity as primary** — when multiple classes are detected simultaneously, process the highest severity class first
- **P0 always takes precedence** — defer P1/P2 processing until all P0 issues are resolved
- **One handoff at a time** — even with multiple issues, only handoff the highest-priority class. Record remaining issues as "pending issues" in progress.md for the next audit cycle
