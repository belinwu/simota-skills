# Orbit Anti-Patterns

Common pitfalls in loop automation and how to avoid them.

## AP-1: The Infinite Retry

RETRY_LIMIT not set or set too high, causing endless retry loops.

❌ **Bad:** `RETRY_LIMIT=999` or no RETRY_LIMIT at all
✅ **Good:** `RETRY_LIMIT=3` — bounded, escalates to BLOCKED after 3 attempts

**Why:** Unbounded retries waste resources and mask failures. After RETRY_LIMIT, the runner transitions to BLOCKED and records TOOL_FAILURE in progress.md.

## AP-2: The Silent SKIP

verify.sh not generated, causing all iterations to pass verification with SKIP.

❌ **Bad:** goal.md has no `## Verification Command` section → verify.sh never generated → every iteration SKIP → done.md alone triggers DONE
✅ **Good:** Add `## Verification Command` with `npm test && npm run lint` → verify.sh generated → DONE requires PASS

**Why:** SKIP means "no verification exists" — it is NOT evidence of success. Goals without verify commands produce unauditable DONE claims.

## AP-3: The Overloaded Goal

Multiple unrelated objectives crammed into a single loop.

❌ **Bad:** `## Objective: Refactor auth, add dark mode, and fix payment bug`
✅ **Good:** One objective per loop with specific ACs. Chain with Sequential Loop Handoff for multi-goal work.

**Why:** Overloaded goals produce ambiguous acceptance criteria, making verification impossible and DONE unauditable.

## AP-4: The Zombie Loop

BLOCKED loop left with stale lock files, preventing new executions.

❌ **Bad:** `.run-loop.lock` exists with dead PID — no one clears it → new runs abort
✅ **Good:** Pre-flight PID liveness check: read lock PID, `kill -0` test, remove if dead

**Why:** Zombie loops block execution without useful feedback. Stale locks must be auto-cleared with PID liveness checks.

## AP-5: The Immeasurable AC

Acceptance criteria that cannot be verified by a command.

❌ **Bad:** "Code is clean", "Performance is acceptable", "UI looks good"
✅ **Good:** `npm run lint` exits 0, `npm test` ≥80% coverage, Lighthouse ≥ 90

**Why:** Subjective criteria cannot be encoded in verify.sh. Every AC must map to a command with a deterministic exit code.

## AP-6: The Copy-Paste Contract

Reusing a previous loop's contract without adapting acceptance criteria.

❌ **Bad:** ACs copied from loop-1 ("Build passes", "Tests pass") — irrelevant to loop-2's goal
✅ **Good:** ACs written specifically for current goal with matching verify commands

**Why:** Copied contracts create false verification — tests pass because they test the old goal, not the current one.

## AP-7: The Manual State Edit

Directly editing state.env by hand instead of using recover.sh.

❌ **Bad:** `echo "NEXT_ITERATION=5" > state.env` — missing LAST_UPDATED_AT, no recovery note
✅ **Good:** `bash .nexus-loop/recover.sh` — reads progress.md, rebuilds state.env atomically, appends recovery note

**Why:** Manual edits skip validation, break atomicity, and leave no audit trail. Always use recover.sh for state corrections.

## AP-8: The Partial Recovery

Fixing state.env but ignoring progress.md inconsistency.

❌ **Bad:** state.env rebuilt but progress.md has duplicate BLOCKED entries, no recovery note → STATE_DRIFT
✅ **Good:** `bash recover.sh` — rebuilds from progress.md evidence, appends timestamped recovery note

**Why:** State recovery must be holistic. state.env and progress.md must be consistent, and recovery actions must be logged.

## AP-9: The Global Stage

Using `git add -A` when dirty baseline paths exist.

❌ **Bad:** `git add -A && git commit` — includes user's unrelated uncommitted changes in loop commit
✅ **Good:** Snapshot baseline at start (`dirty-start-paths.txt`), exclude baseline paths at commit time with scoped staging

**Why:** Global staging mixes unrelated changes into loop commits, making rollback dangerous and commit scope unauditable.

## AP-10: The Premature DONE

Declaring DONE when verification has failed.

❌ **Bad:** done.md exists + verify.sh exits 1 → STATUS="DONE" (ignores verify failure)
✅ **Good:** Dual gate — DONE requires both done.md AND VERIFY_RESULT=PASS/SKIP. If verify fails, STATUS="CONTINUE".

**Why:** DONE is an auditable claim, not a mood. The dual gate (done.md + verify) exists precisely to prevent premature completion.

## AP-11: Manual Branch Switch During Loop

Switching branches manually while run-loop.sh is active with BRANCH_ISOLATION.

❌ **Bad:** `git checkout main` during loop — auto-commits land on wrong branch
✅ **Good:** Stop the loop first (SIGINT), then switch. Or wait for DONE.

**Why:** Branch isolation requires run-loop.sh to stay on the iteration branch. Auto-commits on the wrong branch cannot be squash-merged correctly.

---

## Prevention Checklist

Run before launching any loop:

- [ ] **AP-1**: `RETRY_LIMIT` is set and ≤ 5
- [ ] **AP-2**: `verify.sh` exists and tests all acceptance criteria
- [ ] **AP-3**: `goal.md` has exactly one objective
- [ ] **AP-4**: No stale `.run-loop.lock` files in loop directory
- [ ] **AP-5**: Every AC maps to a command with deterministic exit code
- [ ] **AP-6**: All ACs are specific to this loop's goal (not copied)
- [ ] **AP-7**: No manual edits to `state.env` — use `recover.sh`
- [ ] **AP-8**: `state.env` and `progress.md` are consistent
- [ ] **AP-9**: `dirty-start-paths.txt` exists when `AUTOCOMMIT=true`
- [ ] **AP-10**: DONE gate requires both `done.md` AND verify PASS/SKIP
- [ ] **AP-11**: No manual `git checkout` during active loop with `BRANCH_ISOLATION=true`

## Quick Reference

| Anti-Pattern | Risk | Detection |
|---|---|---|
| AP-1: Infinite Retry | Resource waste, masked failures | `RETRY_LIMIT > 5` or unset |
| AP-2: Silent SKIP | Unauditable DONE | `verify.sh` missing |
| AP-3: Overloaded Goal | Ambiguous verification | Multiple objectives in `goal.md` |
| AP-4: Zombie Loop | Execution blocked | `.run-loop.lock` + dead PID |
| AP-5: Immeasurable AC | Untestable criteria | AC without command mapping |
| AP-6: Copy-Paste Contract | False verification | ACs unrelated to current goal |
| AP-7: Manual State Edit | Audit trail broken | `state.env` without recovery note |
| AP-8: Partial Recovery | STATE_DRIFT | state.env/progress.md mismatch |
| AP-9: Global Stage | Commit scope leak | `git add -A` with dirty baseline |
| AP-10: Premature DONE | False completion | DONE with VERIFY_RESULT=FAIL |
| AP-11: Manual Branch Switch | Squash failure, misplaced commits | `git checkout` during active BRANCH_ISOLATION loop |
