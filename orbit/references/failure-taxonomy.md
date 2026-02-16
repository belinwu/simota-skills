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
