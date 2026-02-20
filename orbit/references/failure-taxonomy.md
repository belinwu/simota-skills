# Failure Taxonomy

## Class Definitions

### CONTRACT_MISSING

Missing or invalid loop artifacts preventing deterministic execution.

| Signal | First Response | What to Check | Recovery Script |
|--------|---------------|---------------|-----------------|
| `goal.md` does not exist | Classify P1, halt execution | Is this a new loop (bootstrap needed) or accidental deletion? | `bash bootstrap.sh ${LOOP_DIR}` |
| `goal.md` exists but AC section empty | Classify P1, trigger ON_GOAL_CONTRACT_WEAK | Are ACs genuinely missing or just poorly formatted? | Rewrite AC section with measurable criteria + verify commands |
| `progress.md` empty or missing | Classify P1, initialize iteration 0 | Was bootstrap skipped? Is there a `runner.log` with iteration evidence? | Append `## Iteration 0 — Bootstrap` entry |
| `state.env` missing | Classify P1, generate defaults | Is `progress.md` available as evidence source? | `bash recover.sh` or generate `NEXT_ITERATION=1, LAST_STATUS=READY` |
| Status footer malformed | Classify P1, re-apply | Is the footer present but with invalid values, or completely absent? | Emit valid `NEXUS_LOOP_STATUS` + `NEXUS_LOOP_SUMMARY` |
| Template partial (some artifacts exist) | Classify P1, identify gaps | Which specific artifacts are missing vs present? | Rebuild only missing artifacts, preserve existing ones |
| AC not measurable (subjective criteria) | Classify P1, strengthen ACs | Can each AC be mapped to a command with exit code? | Apply AC Strengthening Templates from `vague-goal-handling.md` |

### STATE_DRIFT

Iteration counters or status disagree across artifacts.

| Signal | First Response | What to Check | Recovery Script |
|--------|---------------|---------------|-----------------|
| `NEXT_ITERATION` > progress.md last iteration + 1 | Re-sync from progress.md | Were iterations skipped? Manual state.env edit? | `bash recover.sh` — rebuilds from progress evidence |
| `NEXT_ITERATION` < progress.md last iteration + 1 | Re-sync from progress.md | Was state.env restored from backup? Interrupted recovery? | `bash recover.sh` — advances to correct iteration |
| `NEXT_ITERATION` matches but `LAST_STATUS` contradicts progress.md | Update LAST_STATUS from progress evidence | Did cleanup() write partial state? Was signal received mid-write? | `bash recover.sh` — derives status from last 20 lines |
| `state.env.sha256` checksum mismatch | Trigger automatic recovery | Was state.env manually edited? Disk corruption? | Runner auto-runs `recover.sh` on checksum mismatch |
| **Escalation condition:** drift detected on 2+ consecutive iterations | Classify P0, pause loop | Is there a systematic cause (e.g., concurrent access, broken recovery)? | Pause execution, manual investigation required |

### VERIFY_GAP

DONE claimed without successful verification evidence.

| Signal | First Response | What to Check | Recovery Script |
|--------|---------------|---------------|-----------------|
| `verify.sh` does not exist | Classify P0, downgrade to CONTINUE | Was verify.sh intentionally omitted? Does goal.md have a Verification Command? | Generate verify.sh from goal.md AC section |
| `verify.sh` exists but exits non-zero (FAIL) | Classify P0, downgrade to CONTINUE | Which specific checks failed? Is it a flaky test or genuine failure? | Re-run `bash verify.sh` to confirm, then address failures |
| `done.md` exists but no verify evidence in `progress.md` | Classify P0, downgrade to CONTINUE | Was verification skipped? Did verify.sh timeout? | Run verification independently: `bash verify.sh && echo VERIFIED` |
| Partial verification pass (some checks PASS, some FAIL) | Classify P1, record partial results | Are failing checks critical or informational? | Log partial results in progress.md, continue with failing ACs as focus |
| VERIFY_RESULT=SKIP with done.md present | Classify P1, warn (SKIP ≠ PASS) | Is SKIP acceptable for this goal? (see AP-2: Silent SKIP) | Generate verify.sh if missing, re-evaluate DONE claim |

### COMMIT_SCOPE_RISK

Potential inclusion of unrelated changes in auto-commit scope.

| Signal | First Response | What to Check | Recovery Script |
|--------|---------------|---------------|-----------------|
| `dirty-start-paths.txt` missing but `AUTOCOMMIT=true` | Classify P1, regenerate baseline | Was bootstrap.sh run? Did run-loop.sh skip baseline snapshot? | Re-snapshot: `git diff --name-only \| sort -u > dirty-start-paths.txt` |
| Staged files include paths from `dirty-start-paths.txt` | Classify P0, unstage baseline paths | Is `comm -23` filtering working? Are paths exact matches? | `git reset HEAD -- <baseline_paths>` |
| **Single-loop:** candidate paths outside goal scope | Classify P1, restrict staging | Are the files genuinely loop artifacts or incidental changes? | Manually verify each candidate path against goal.md scope |
| **Cross-loop:** parallel loops staging overlapping paths | Classify P1, suspend affected loop | Which loop owns each overlapping path? (see Pattern 5) | Delegate to Guardian via `ORBIT_TO_GUARDIAN_HANDOFF` |
| `git add -A` used with dirty baseline present | Classify P0, revert commit | Was `dirty-start-paths.txt` empty/missing causing fallback? | `git reset HEAD~1`, fix baseline, re-commit with scoped staging |

### TOOL_FAILURE

Runner or executor repeated failures preventing iteration progress.

| Signal | First Response | What to Check | Recovery Script |
|--------|---------------|---------------|-----------------|
| **Network:** connection timeout / DNS failure | Apply retry with backoff | Is the network reachable? Proxy/VPN issues? | Retry with `RETRY_BACKOFF_BASE=5` for network-dependent operations |
| **Resource:** OOM killed (exit 137) / disk full | Classify P1, pause loop | `df -h` for disk, `free -m` for memory — is the machine under-resourced? | Free resources, then `bash recover.sh && bash run-loop.sh` |
| **Auth:** permission denied / token expired | Classify P1, pause for credential refresh | Is the token/API key still valid? Has it been rotated? | Refresh credentials, then resume from current NEXT_ITERATION |
| **Timeout:** EXEC_CMD exceeded EXEC_TIMEOUT | Retry once, then classify P1 | Is the task genuinely slow or is the executor hung? Consider `ADAPTIVE_TIMEOUT=true` | Increase `EXEC_TIMEOUT` or enable adaptive timeout |
| **Exit code mismatch:** unexpected non-zero exit | Apply retry policy | Is it a transient failure or a deterministic bug in the task? | If deterministic (same exit on retry), escalate to Builder |
| **Escalation:** RETRY_LIMIT exhausted | Classify P1, record BLOCKED | Is the failure environment or task-related? | Investigate via `ORBIT_TO_SCOUT_HANDOFF`, then decide: fix environment or revise goal |

## Priority

| Severity | Classes | Action |
|----------|---------|--------|
| P0 | VERIFY_GAP (false DONE), destructive COMMIT_SCOPE_RISK, escalated STATE_DRIFT | Stop and confirm |
| P1 | STATE_DRIFT, CONTRACT_MISSING, TOOL_FAILURE (retry exhausted) | Recover then continue |
| P2 | TOOL_FAILURE (intermittent, within retry budget) | Retry policy |

## Reporting Schema

```yaml
ORBIT_FAILURE_REPORT:
  class: "<taxonomy class>"
  severity: "P0|P1|P2"
  sub_class: "<specific signal from table above>"
  evidence:
    - "<file:line>"
  impact: "<what breaks>"
  recommendation: "<smallest reversible action>"
  recovery_cmd: "<command from Recovery Script column>"
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
