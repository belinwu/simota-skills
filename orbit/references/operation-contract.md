# Operation Contract

## Contract Checklist

- `goal.md` includes:
  - Goal statement
  - Why this matters
  - 3-6 measurable acceptance criteria
  - Out-of-scope notes
- `progress.md` per iteration includes:
  - UTC timestamp
  - iteration number
  - changed files + summary
  - verification commands + outcomes
  - remaining work
  - decision (`CONTINUE` or `DONE`)
- `done.md` includes:
  - completion timestamp
  - acceptance checklist + evidence
  - rollback note

## Footer Contract

Required response footer:

```text
NEXUS_LOOP_STATUS: READY | CONTINUE | DONE
NEXUS_LOOP_SUMMARY: <single-line summary>
```

Rules:
- `NEXUS_LOOP_STATUS` must be exact token.
- Summary should stay concise and operational.
- Missing footer defaults to `CONTINUE` in conservative mode.

## Resume Contract

`state.env` should keep:
- `NEXT_ITERATION`
- `LAST_STATUS`
- `LAST_UPDATED_AT`
- session resume flags

Recovery priority:
1. `progress.md` timeline
2. `runner.log` status stamps
3. `state.env`
