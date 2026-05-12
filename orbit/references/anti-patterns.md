# Orbit Anti-Patterns

Purpose: load this during review, post-mortem, or safety checks to detect known loop-operation failure shapes before they become incidents.

## Contents

1. Anti-pattern catalog
2. Prevention checklist
3. Quick reference

## Anti-Pattern Catalog

| ID | Anti-pattern | Risk | Safe rule |
|----|--------------|------|-----------|
| `AP-1` | Infinite retry | resource waste and hidden failures | keep `RETRY_LIMIT <= 5`, default `3` |
| `AP-2` | Silent SKIP | unauditable `DONE` | generate `verify.sh` from measurable verification commands |
| `AP-3` | Overloaded goal | ambiguous verification | keep one objective per loop |
| `AP-4` | Zombie loop | execution blocked by stale lock | auto-clear dead PID locks |
| `AP-5` | Immeasurable AC | unverifiable contract | map every AC to a command with deterministic exit code |
| `AP-6` | Copy-paste contract | false verification | rewrite ACs for the current goal |
| `AP-7` | Manual state edit | broken audit trail | use `recover.sh`, not manual edits |
| `AP-8` | Partial recovery | `STATE_DRIFT` persists | recover `state.env` and annotate `progress.md` together |
| `AP-9` | Global stage | unrelated changes leak into commit scope | snapshot dirty baseline and use scoped staging |
| `AP-10` | Premature `DONE` | false completion | require both `done.md` and verify `PASS`/`SKIP` |
| `AP-11` | Manual branch switch during active loop | squash failure and misplaced commits | stop the loop before changing branches |
| `AP-12` | Validator gap (stub compiles → DONE) | placeholder code passes verify because tests are too coarse | `verify.sh` must grep `TODO`/`NotImplementedError`/`return None`/`pass` in changed source + run behavioural assertions derived from AC [Source: dev.to/itsuzef — The Judge Gate] |
| `AP-13` | Reward hacking via test inspection | agent mutates `tests/` or `verify.sh` to soften assertions ("test cheating") | `tests/` and `verify.sh` are `chmod 0444` + pre-commit rejects any diff touching them + run verify from a separate worktree the loop cannot write [Source: metr.org — Recent Reward Hacking; nist.gov — Cheating AI Agent Evaluations] |
| `AP-14` | Worktree cleanup → repo destruction | parallel subagent's cleanup removes parent `.git/`; loop continues on a hollow tree | iter prologue runs `git fsck` + monitors `.git/` inode; cleanup restricted to a path allowlist scoped to the worktree dir [Source: github.com/anthropics/claude-code — issue #48927] |
| `AP-15` | Context poisoning (error log accumulation) | past-iter error traces persist in `goal.md`/scratchpad, later iters treat hallucinated constraints as spec | rotate scratchpad at 60% context, end-of-iter summary keeps decisions only (no failure traces), `goal.md` size is monotonically tracked [Source: mindstudio.ai — Context Rot; dbreunig.com — How Long Contexts Fail] |
| `AP-16` | Goal drift / goalpost moving in `goal.md` | agent edits `goal.md` to weaken AC verbs (`must` → `should` → `may`) then claims DONE | `goal.md` and AC files are `chmod 0444` + sha256-pinned at loop start; any change ABORTs the loop [Source: usewire.io — Agent Drift; lakera.ai — Agentic AI Threats] |
| `AP-17` | Token burn-rate anomaly (pre-$47k signal) | rate-limit reset triggers exponential consumption, loop burns tokens without artifact change | EWMA burn-rate alert (5-min window vs prior window > 3x → PAUSE) + absolute USD/iter cap + USD/run cap + auto-reload billing disabled [Source: byteiota.com — Uber Claude Code; mfyz.com — Claude Code on Loop] |
| `AP-18` | Architectural incoherence blindness | verify only checks "works", duplicate impls / layer violations / naming drift accumulate exponentially over 4h+ runs | verify includes architectural lint (`jscpd` duplication, `dependency-cruiser` cycles, `ts-prune` deadcode); thresholds fail the iter [Source: asdlc.io — Ralph Loop pattern] |
| `AP-19` | Compaction-induced decision amnesia | auto-compaction discards "why" notes; next iter re-litigates or reverses prior design decisions | pre-compaction extract to append-only `decisions.md` (≤ 30 lines), first iter after compaction is required to read it [Source: gist — Compaction Memory; cipherbuilds.ai — Day 30 Agent Memory] |
| `AP-20` | Permission mode hijack via settings.json | agent rewrites `.claude/settings.json` `permissions.defaultMode` to `bypassPermissions` mid-run; deny rules silently removed | `.claude/settings*.json` sha256-pinned at start; any change ABORTs; verify runs in a separate process with its own settings file [Source: cryptika.com — Claude Code rule bypass; repello.ai — Claude Code Security Checklist] |
| `AP-21` | Identical retry without diff (token loop) | same tool call argv repeats N times with no file mtime change; pure token burn (distinct from AP-1 retry count) | argv-hash dedup: 2 identical hashes in window forces a `reframe` prompt; 3 ABORTs [Source: quickleap.io — AI Agents Reasoning Loops; agentpatterns.tech — Infinite Agent Loop] |

**High-impact Top 3** (apply first when generating new runners):

1. `AP-13` Reward Hacking — METR/NIST 2025-2026 demonstrate this across multiple models. `tests/` immutability is a one-line fix with outsized safety value.
2. `AP-14` Worktree Cleanup — destructive data loss reproducible per Claude Code issue #48927. Inode monitoring is cheap; the alternative is unrecoverable.
3. `AP-17` Burn-Rate Anomaly — multiple 2026 incidents ($6k overnight, Uber-scale events). EWMA monitoring is orthogonal to existing `RETRY_LIMIT` and `TOKEN_BUDGET`.

## Prevention Checklist

Run before launching a loop:

- [ ] `RETRY_LIMIT` is set and `<= 5`
- [ ] `verify.sh` exists and covers all acceptance criteria
- [ ] `goal.md` has exactly one objective
- [ ] no stale `.run-loop.lock` exists
- [ ] every AC maps to a deterministic command
- [ ] ACs were written for this loop, not copied from another
- [ ] `state.env` has not been edited manually
- [ ] `state.env` and `progress.md` are consistent
- [ ] `dirty-start-paths.txt` exists when `AUTOCOMMIT=true`
- [ ] the `DONE` gate requires `done.md` and verify `PASS`/`SKIP`
- [ ] no manual `git checkout` will happen during active `BRANCH_ISOLATION`
- [ ] `verify.sh` includes a placeholder-detection step (TODO / `pass` / `NotImplementedError`)
- [ ] `tests/` and `verify.sh` are read-only or protected by pre-commit
- [ ] `git fsck` and `.git/` inode monitoring run at iter start under `WORKTREE_ISOLATION`
- [ ] scratchpad rotation policy is set; `goal.md` size is tracked iter-over-iter
- [ ] `goal.md` and AC files are sha256-pinned and read-only
- [ ] `BURN_RATE_THRESHOLD`, `USD_PER_ITER_CAP`, `USD_PER_RUN_CAP` are configured; auto-reload billing is disabled
- [ ] `verify.sh` includes architectural lint (duplication / cycles / dead code)
- [ ] `decisions.md` (append-only) is referenced; first post-compaction iter re-reads it
- [ ] `.claude/settings*.json` sha256-pinned at loop start
- [ ] tool-call argv dedup is active (last `DEDUP_WINDOW` calls hashed)

## Quick Reference

| Anti-pattern | Detection |
|--------------|-----------|
| `AP-1` | `RETRY_LIMIT > 5` or unset |
| `AP-2` | `verify.sh` missing |
| `AP-3` | multiple objectives in `goal.md` |
| `AP-4` | `.run-loop.lock` with dead PID |
| `AP-5` | AC without command mapping |
| `AP-6` | ACs unrelated to current goal |
| `AP-7` | `state.env` changed without recovery note |
| `AP-8` | `state.env` / `progress.md` mismatch |
| `AP-9` | `git add -A` with dirty baseline |
| `AP-10` | `DONE` with `VERIFY_RESULT=FAIL` |
| `AP-11` | `git checkout` during active branch-isolated loop |
| `AP-12` | placeholder tokens (`TODO`, `pass`, `NotImplementedError`) in changed src with verify PASS |
| `AP-13` | `tests/` or `verify.sh` modified in same iter as `src/` |
| `AP-14` | `git rev-parse --git-dir` fails at iter start, or `.git/` inode changed |
| `AP-15` | `goal.md` size strictly increasing across 3+ iters, or same error string in 3+ iters |
| `AP-16` | `goal.md`/AC sha256 changed mid-run |
| `AP-17` | 5-min token rate > 3x prior window, or USD/iter > cap |
| `AP-18` | `jscpd`/`dependency-cruiser`/`ts-prune` threshold exceeded |
| `AP-19` | post-compaction iter produces diff > 2x baseline, or ADR contradicts implementation |
| `AP-20` | `.claude/settings*.json` sha256 changed mid-run |
| `AP-21` | last `DEDUP_WINDOW` tool argv hashes contain a duplicate with no mtime change |
