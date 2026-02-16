# Orbit Examples

## Example A: DONE Verification Gap (VERIFY_GAP)

Input:
- `done.md` exists
- `progress.md` last entry says lint failed
- `NEXUS_LOOP_STATUS: DONE`

Expected Orbit output:
- `status_assessment: VERIFY_GAP`
- `recommended_next_action: CONTINUE`
- `handoff_target: Radar`

## Example B: Dirty Start Auto-Commit (COMMIT_SCOPE_RISK)

Input:
- dirty baseline exists
- iteration adds new files under `apps/backend/internal/handler/`

Expected Orbit output:
- `status_assessment: COMMIT_SCOPE_RISK`
- `recommended_next_action: stage candidate-only paths`
- `handoff_target: Guardian`

## Example C: Resume State Drift (STATE_DRIFT)

Input:
- `state.env` says `NEXT_ITERATION=11`
- `progress.md` latest is iteration 9

Expected Orbit output:
- `status_assessment: STATE_DRIFT`
- `recommended_next_action: rebuild state from progress evidence`
- `handoff_target: Builder`

## Example D: Contract Missing (CONTRACT_MISSING)

Input:
- `goal.md` does not exist
- `progress.md` exists but is empty (0 iteration entries)
- `state.env` says `NEXT_ITERATION=1`, `LAST_STATUS=READY`
- No `NEXUS_LOOP_STATUS` footer in any prior response

Expected Orbit output:
- `status_assessment: CONTRACT_MISSING`
- `severity: P1`
- `evidence_gaps`:
  - `goal.md: missing — loop has no defined objective or acceptance criteria`
  - `progress.md: empty — no iteration history to infer intent`
  - `status_footer: absent — no deterministic status signal`
- `recommended_next_action: rebuild contract files before any execution`
  - Step 1: Create `goal.md` with measurable acceptance criteria (trigger `ON_GOAL_CONTRACT_WEAK`)
  - Step 2: Initialize `progress.md` with iteration 0 bootstrap entry
  - Step 3: Emit `NEXUS_LOOP_STATUS: READY` footer
- `handoff_target: Nexus` (request goal clarification from user or upstream)

## Example E: Tool Failure (TOOL_FAILURE)

Input:
- `runner.log` shows 3 consecutive `codex exec` failures:
  - Attempt 1: `exit_code=1, stderr="connection timeout"`
  - Attempt 2: `exit_code=1, stderr="connection timeout"`
  - Attempt 3: `exit_code=137, stderr="killed by OOM"`
- `progress.md` last successful entry is iteration 7 (all checks passed)
- `state.env` says `NEXT_ITERATION=8`, `LAST_STATUS=CONTINUE`

Expected Orbit output:
- `status_assessment: TOOL_FAILURE`
- `severity: P2` (escalate to P1 if retry budget exhausted)
- `evidence_gaps`:
  - `runner.log: 3 consecutive failures — mixed failure modes (network + OOM)`
  - `progress.md: stalled at iteration 7 — no entry for iteration 8`
- `recommended_next_action: apply bounded retry with environment check`
  - Step 1: Classify failure modes (network vs resource — do not mix into single fix)
  - Step 2: Check environment prerequisites (connectivity, memory limits)
  - Step 3: If environment healthy, retry iteration 8 with `NEXT_ITERATION=8` preserved
  - Step 4: If 2 more failures, escalate to P1 and pause for user confirmation
- `handoff_target: Builder` (if environment fix needed) or `NONE` (if retry succeeds)
