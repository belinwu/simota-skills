# Orbit Patterns

## 1. Contract-First Stabilization

Use when loop behavior is unstable or non-deterministic.

1. Validate artifact presence and schema.
2. Validate footer semantics.
3. Validate resume consistency.
4. Only then propose implementation fixes.

## 2. Evidence-Gated DONE

Use when `DONE` is claimed.

- Require acceptance checklist mapping.
- Require verification commands and outcomes.
- Require rollback note for last mutation.
- If any missing: recommend `CONTINUE`.

## 3. Dirty-Baseline Safe Commit

Use when worktree is dirty at loop start.

- Snapshot baseline dirty paths.
- Build candidate path list from current delta.
- Exclude baseline paths.
- Stage/commit only candidate paths.

## 4. Resume Drift Recovery

Use when `state.env` and progress timeline diverge.

- Parse latest iteration record from progress.
- Compare with `NEXT_ITERATION` and `LAST_STATUS`.
- Reconstruct state from evidence source.
- Annotate decision and reason.

## 5. Parallel Loop Commit Scope Conflict Detection

Use when multiple loops are running concurrently and may touch overlapping paths.

```bash
# 1. Enumerate active loops (collect loop dirs with LAST_STATUS=CONTINUE)
active_loops=$(find . -name "state.env" -exec grep -l "LAST_STATUS=CONTINUE" {} \; | xargs dirname)

# 2. Extract candidate paths per loop (changes excluding baseline delta)
for loop_dir in $active_loops; do
  git diff --name-only | sort | comm -23 - "${loop_dir}/dirty-start-paths.txt" \
    > "${loop_dir}/.candidate-paths.tmp"
done

# 3. Detect overlapping paths → report CROSS_LOOP_CONFLICT
cat */.candidate-paths.tmp | sort | uniq -d > .conflict-paths.tmp
if [[ -s .conflict-paths.tmp ]]; then
  echo "CROSS_LOOP_CONFLICT: $(cat .conflict-paths.tmp)" # → delegate to Guardian
fi
```

**When CROSS_LOOP_CONFLICT is detected:**
1. Suspend the loop containing conflicting paths (keep `LAST_STATUS=CONTINUE`)
2. Delegate commit order arbitration to Guardian via `ORBIT_TO_GUARDIAN_HANDOFF`
3. Skip commit processing for the affected loop until Guardian's decision is received

## 6. Sequential Loop Handoff Implementation Guide

Protocol for explicitly referencing predecessor loop completion as the start condition of the successor loop.

### Append Handoff Checklist to done.md

```markdown
## Handoff Checklist (for successor loop)
- [ ] Criterion 1: <verified by: command>
- [ ] Criterion 2: <verified by: command>
- [ ] Artifacts produced: <file list>
- [ ] Known limitations: <list>
```

### Link prerequisites in successor loop's goal.md

```markdown
## Prerequisites (from predecessor loop)
- Loop: <predecessor loop dir>
- Done file: <path/to/done.md>
- Verified criteria:
  - [ ] Criterion 1: `<verification command>`
  - [ ] Criterion 2: `<verification command>`

> Orbit MUST validate each prerequisite independently before proceeding.
```

**Rules:**
- Always check the `prerequisites` section during successor loop Intake phase
- Existence of predecessor `done.md` alone is insufficient — verify each AC independently
- If any prerequisite is unverified, classify as `CONTRACT_MISSING`

## 7. Loop-of-Loops Isolation Rule

Rule table defining the boundary between the meta-loop (outer) and inner loops.

| Operation | Meta-loop Allowed? | Reason |
|------|--------------------------|------|
| Consume inner loop's `_STEP_COMPLETE` | ✅ Permitted | Designed communication channel |
| Read inner loop's `state.env` | ✅ Read-only permitted | Status check only |
| Write inner loop's `state.env` | ❌ Prohibited | Induces STATE_DRIFT |
| Append to inner loop's `progress.md` | ❌ Prohibited | Contaminates inner loop evidence trail |
| Delete/move inner loop's `done.md` | ❌ Prohibited | Irreversible and destroys evidence |
| Force-terminate inner loop | ⚠️ Guardian approval required | Impact scope assessment needed |
| Classify inner loop failures independently | ✅ Recommended | Prevents propagation to meta-loop |

**Principle:** The meta-loop is an "observer" of inner loops, not an "intervener."

## 8. Dirty Baseline Edge Cases

Edge cases and handling for `dirty-start-paths.txt`.

| Case | Problem | Mitigation |
|--------|------|--------|
| Partial path match | Loop artifact path matches a baseline path prefix | `comm -23` does exact line matching, so naturally avoided. Manually verify if an entire subdirectory is dirty |
| Same file modified by parallel loops | Commit conflict proceeds undetected without CROSS_LOOP_CONFLICT | Pre-detect using Pattern 5 algorithm. Delegate arbitration to Guardian |
| gitignore-listed tracked files | `git check-ignore` does not ignore tracked files | `git ls-files --others --exclude-standard` only covers untracked. Tracked+ignored appear in `git diff` and are included in baseline. Create an explicit exclusion list |
| symlink / submodule | `git diff --name-only` reports symlink targets | Record the symlink path itself in baseline. Recommended: exclude submodules with `--ignore-submodules=all` |
