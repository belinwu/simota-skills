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
