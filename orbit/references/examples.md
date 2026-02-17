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

## Example F: Parallel Loop State Contamination (COMMIT_SCOPE_RISK cross-loop)

Input:
- Two loops running in parallel: `loop-a` (API refactor) and `loop-b` (UI migration)
- `loop-a/state.env` says `NEXT_ITERATION=5`, `LAST_STATUS=CONTINUE`
- `loop-b/state.env` says `NEXT_ITERATION=3`, `LAST_STATUS=CONTINUE`
- `git diff --cached` shows staged files from both `apps/api/` and `apps/frontend/`
- `loop-a/dirty-start-paths.txt` does not list `apps/frontend/` paths
- `loop-b/dirty-start-paths.txt` does not list `apps/api/` paths

Expected Orbit output:
- `status_assessment: COMMIT_SCOPE_RISK`
- `severity: P1`
- `evidence_gaps`:
  - `loop-a staging scope: includes apps/frontend/ paths that belong to loop-b`
  - `loop-b staging scope: includes apps/api/ paths that belong to loop-a`
  - `cross-loop contamination: neither loop's dirty-start-paths accounts for the other loop's working set`
- `recommended_next_action: isolate commit scopes per loop`
  - Step 1: Unstage all files
  - Step 2: For each loop, stage only paths matching its goal scope
  - Step 3: Commit loop-a changes with `loop-a(iter-5):` prefix, then loop-b with `loop-b(iter-3):` prefix
  - Step 4: Add cross-loop path exclusion to each loop's `dirty-start-paths.txt`
- `handoff_target: Guardian` (commit scope policy enforcement)

## Example G: Sequential Loop Handoff Gap (CONTRACT_MISSING handoff)

Input:
- `loop-1` completed: `loop-1/done.md` exists, `loop-1/state.env` says `LAST_STATUS=DONE`
- `loop-2` started: `loop-2/goal.md` references "continue from loop-1 results"
- `loop-2/goal.md` has no explicit acceptance criteria — only "finish what loop-1 started"
- `loop-2/progress.md` has iteration 1 entry but no reference to `loop-1/done.md`
- No handoff checklist exists between loops

Expected Orbit output:
- `status_assessment: CONTRACT_MISSING`
- `severity: P1`
- `evidence_gaps`:
  - `loop-2/goal.md: acceptance criteria missing — "finish what loop-1 started" is not measurable`
  - `loop-2/progress.md: no reference to loop-1/done.md — implicit assumption that loop-1 output is correct`
  - `handoff checklist: absent — no explicit verification that loop-1 deliverables meet loop-2 prerequisites`
- `recommended_next_action: rebuild loop-2 contract with explicit handoff`
  - Step 1: Extract loop-1's acceptance criteria from `loop-1/done.md` and verify each is met
  - Step 2: Rewrite `loop-2/goal.md` with measurable acceptance criteria independent of loop-1 prose
  - Step 3: Add handoff checklist to `loop-2/progress.md` iteration 0 entry referencing `loop-1/done.md` line-by-line
  - Step 4: Trigger `ON_GOAL_CONTRACT_WEAK` for user confirmation of revised goal
- `handoff_target: Nexus` (request goal clarification)

## Example H: Loop of Loops Inner Failure (TOOL_FAILURE scoped)

Input:
- Meta-loop manages 3 inner loops: `inner-a` (build), `inner-b` (test), `inner-c` (deploy)
- `meta/state.env` says `NEXT_ITERATION=2`, `LAST_STATUS=CONTINUE`
- `inner-a/state.env` says `LAST_STATUS=DONE` (build succeeded)
- `inner-b/state.env` says `LAST_STATUS=CONTINUE`, `runner.log` shows 3 consecutive test failures
- `inner-c` has not started (no `state.env`)
- `meta/progress.md` last entry: "inner-a completed, proceeding to inner-b"

Expected Orbit output:
- `status_assessment: TOOL_FAILURE`
- `severity: P1` (inner failure blocks meta-loop progression)
- `evidence_gaps`:
  - `inner-b/runner.log: 3 consecutive test failures — meta-loop cannot proceed to inner-c`
  - `meta/progress.md: does not reflect inner-b failure — last entry implies normal progression`
  - `inner-c: not started — blocked by inner-b failure (correct behavior)`
- `recommended_next_action: contain inner-b failure, update meta-loop state`
  - Step 1: Classify inner-b failure independently (do not mix with meta-loop status)
  - Step 2: Update `meta/progress.md` with inner-b failure record and blocked status
  - Step 3: Apply inner-b retry policy (bounded, per inner-b's RETRY_LIMIT)
  - Step 4: If inner-b retries exhausted, escalate to P0 at meta-loop level and pause
  - Step 5: Do NOT attempt inner-c until inner-b reaches DONE
- `handoff_target: Builder` (if inner-b failure is implementation-related) or `NONE` (if retry resolves)
