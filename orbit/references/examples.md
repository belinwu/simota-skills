# Orbit Examples

## Example A: DONE Verification Gap

Input:
- `done.md` exists
- `progress.md` last entry says lint failed
- `NEXUS_LOOP_STATUS: DONE`

Expected Orbit output:
- `status_assessment: VERIFY_GAP`
- `recommended_next_action: CONTINUE`
- `handoff_target: Radar`

## Example B: Dirty Start Auto-Commit

Input:
- dirty baseline exists
- iteration adds new files under `apps/backend/internal/handler/`

Expected Orbit output:
- `status_assessment: COMMIT_SCOPE_RISK`
- `recommended_next_action: stage candidate-only paths`
- `handoff_target: Guardian`

## Example C: Resume State Drift

Input:
- `state.env` says `NEXT_ITERATION=11`
- `progress.md` latest is iteration 9

Expected Orbit output:
- `status_assessment: STATE_DRIFT`
- `recommended_next_action: rebuild state from progress evidence`
- `handoff_target: Builder`
