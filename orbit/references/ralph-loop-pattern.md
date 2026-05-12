# Ralph Loop Pattern (Huntley-style autonomous loop)

Purpose: load this when generating, auditing, or hardening a `nexus-autoloop` runner that follows the **Ralph Loop** lineage (Geoffrey Huntley, 2025-07). Ralph Loop is one specific implementation philosophy within Orbit's broader autonomous-loop scope. When a goal explicitly invokes Ralph (`ralph`, `PROMPT.md`, `<promise>COMPLETE</promise>`, `ghuntley`-style scripts, `cat PROMPT.md | claude` shapes), prefer this pattern over generic loop templates.

## Contents

1. Origin and core definition
2. Eight design principles
3. Two-mode pattern (plan / build)
4. 9xx guardrail numbering
5. AGENTS.md constraints
6. Subagent constraints
7. Plan disposability rule
8. Filesystem-as-Memory model
9. Termination conditions
10. Green-field-only constraint
11. Huntley's anti-pattern warnings
12. Adjacent best practices (non-default)
13. Quick reference

## 1. Origin and Core Definition

- Author: Geoffrey Huntley, "Ralph Wiggum as a 'software engineer'", published 2025-07-14. [Source: https://ghuntley.com/ralph/]
- Reference implementation: [ghuntley/how-to-ralph-wiggum](https://github.com/ghuntley/how-to-ralph-wiggum)
- Subsequent evolution: [everything is a ralph loop](https://ghuntley.com/loop/) (2026-01-17, introduces "The Weaving Loom" — evolutionary multi-loop orchestration)
- Community lineage write-up: [A Brief History of Ralph — HumanLayer](https://www.humanlayer.dev/blog/brief-history-of-ralph)

**Core definition**: A single immutable prompt file (`PROMPT.md`) is piped to a coding agent inside an unbounded `while` loop. The prompt does not change between iterations; only the on-disk artifacts (plan, spec, AGENTS.md, code, tests) change. The agent re-reads disk every iteration, picks the **single most important next task**, and implements it. Determinism comes from disk state, not from prompt evolution.

Minimal canonical form:

```bash
while :; do cat PROMPT.md | claude --dangerously-skip-permissions \
  --output-format=stream-json --model opus ; done
```

Ralph Loop is **filesystem-as-memory** plus **fresh-context-per-iteration**. This is the structural opposite of conversation-resend loops (`/loop` style), which replay full chat history every call and scale token cost linearly with iteration count.

## 2. Eight Design Principles

| # | Principle | Operational rule |
|---|-----------|------------------|
| `RP-1` | PROMPT.md is immutable | The agent must never edit `PROMPT.md`. Pin its `sha256` at loop start; abort on change. |
| `RP-2` | Two-mode separation | Keep `PROMPT_plan.md` (gap analysis) and `PROMPT_build.md` (implementation) as distinct files. Never mix. |
| `RP-3` | 9xx guardrail numbering | Rules with leading `9xx` (e.g. `999_NO_PLACEHOLDERS`) are critical and non-negotiable. Higher number = more inviolable. |
| `RP-4` | AGENTS.md ≤ 60 lines | Operational only (build/test/run commands). No status notes, no progress, no decisions. Anything beyond goes to `IMPLEMENTATION_PLAN.md`. |
| `RP-5` | One build/test subagent | Build and test must be serialised through a single subagent. Parallel build subagents cause backpressure collapse. |
| `RP-6` | Plan is disposable | When the agent detects circular work or scope drift, regenerate the plan; never re-anchor to a stale plan. |
| `RP-7` | Filesystem-as-memory | All state lives in tracked files (`fix_plan.md`, `progress.md`, git history). Context is fresh every iteration. |
| `RP-8` | Green-field only | Ralph Loop is designed for new projects. Huntley explicitly disqualifies it for existing codebases. |

## 3. Two-Mode Pattern (plan / build)

The loop alternates between two distinct prompt files. Mode is selected by a small dispatcher (env var, marker file, or alternating iterations).

| Mode | File | Purpose | Allowed writes | Forbidden |
|------|------|---------|----------------|-----------|
| `plan` | `PROMPT_plan.md` | Gap analysis vs. `specs/` and `AGENTS.md` | `fix_plan.md`, `IMPLEMENTATION_PLAN.md` | source code, tests |
| `build` | `PROMPT_build.md` | Pick top item from `fix_plan.md` and implement | source, tests, `progress.md` | spec, plan, AGENTS.md |

Switching rules:
- Start in `plan` until `fix_plan.md` has ≥ 1 prioritised item.
- Stay in `build` while `fix_plan.md` has unblocked items.
- Re-enter `plan` on `CONVERGENCE_STALL`, `OSCILLATION_LOOP`, or when `fix_plan.md` is exhausted but DONE gate is unmet.

## 4. 9xx Guardrail Numbering Convention

Critical rules in `PROMPT.md` are numbered `9xx` (or `99x` for absolutes). Larger number = harder constraint. The numbering acts as a salience anchor for the model.

Example (canonical Huntley):

```
901_LOOK_FOR_EXISTING_IMPLEMENTATIONS
902_TESTS_BEFORE_IMPLEMENTATION
910_NEVER_COMMIT_SECRETS
990_DO_NOT_IMPLEMENT_PLACEHOLDERS
995_DO_NOT_ASSUME_NOT_IMPLEMENTED
999_DO_NOT_EDIT_PROMPT_MD
```

Orbit-generated `PROMPT.md` must include at minimum:

- `990_DO_NOT_IMPLEMENT_PLACEHOLDERS` (covers AP-12 Validator Gap)
- `995_DO_NOT_ASSUME_NOT_IMPLEMENTED` (forces grep before claiming missing)
- `999_DO_NOT_EDIT_PROMPT_MD` (covers RP-1 immutability)
- `998_DO_NOT_EDIT_GOAL_MD` (covers AP-16 Goal Drift)
- `997_DO_NOT_EDIT_TESTS_OR_VERIFY` (covers AP-13 Reward Hacking)

## 5. AGENTS.md Constraints

`AGENTS.md` is the agent-facing operations file. Strict rules:

- **Maximum 60 lines**. Hard cap. If it grows past 60, audit for status leakage.
- **Operational content only**: how to build, test, run, format, lint.
- **No progress notes, no decisions, no history**. Those belong in `IMPLEMENTATION_PLAN.md` and `progress.md`.
- **No prose explanation**. Imperative form: `npm test`, not "we use jest to run tests".
- Pin `sha256` at loop start and warn (not abort) on changes — AGENTS.md may legitimately evolve but contamination is the most common Ralph failure.

[Source: https://ghuntley.com/ralph/, https://www.humanlayer.dev/blog/brief-history-of-ralph]

## 6. Subagent Constraints

| Operation | Subagent count | Reason |
|-----------|----------------|--------|
| Build verification | exactly `1` | Parallel builds cause backpressure collapse and contradictory results |
| Test verification | exactly `1` | Same as build; also test isolation breaks under parallel writes |
| Plan/spec generation | `1` per concern | Independent contexts prevent cross-contamination |
| Independent critic (BP-4) | exactly `1`, different model | False-DONE detection requires an independent reviewer |

Never parallelise build or test in a Ralph Loop. Huntley's original warning: "unbounded parallelism collapses".

## 7. Plan Disposability Rule

The plan is a scratchpad, not a contract. When the agent detects any of the following, regenerate the plan instead of repairing it:

- Same top item in `fix_plan.md` for ≥ 3 consecutive `build` iterations (CONVERGENCE_STALL).
- A→B→A→B alternation in `fix_plan.md` (OSCILLATION_LOOP).
- An item references a file or symbol that no longer exists.
- An item depends on an assumption contradicted by current `progress.md`.

Regeneration steps:

1. Archive the current plan to `IMPLEMENTATION_PLAN_archive_<ISO8601>.md` (do not delete).
2. Re-enter `plan` mode.
3. Re-derive `fix_plan.md` from `specs/` and current code state.
4. Continue.

## 8. Filesystem-as-Memory Model

| Aspect | Ralph (filesystem-as-memory) | `/loop`-style (conversation-resend) |
|--------|------------------------------|--------------------------------------|
| Context per iteration | fresh (re-read disk) | replay full chat history |
| Token cost growth | sub-linear (cache hits) | linear or super-linear |
| Memory backbone | `progress.md` + `fix_plan.md` + git | conversation log |
| Failure recovery | rerun from disk | replay log up to crash |
| Documented cost incident | $14k over 3 months (Cursed) | $6k overnight ($/loop 30m`) |

[Source: https://intelligenttools.co/blog/claude-code-unsupervised-8-hours-ralph-loop, https://pageai.pro/blog/long-running-ai-coding-agents-ralph-loop, https://x.com/amaanbuilds/status/2050561260782297336 (HTTP 429 — cited via secondary aggregation)]

**Rule**: Orbit-generated runners must use filesystem-as-memory. Never use conversation-resend models for `MAX_ITERATIONS ≥ 20`.

## 9. Termination Conditions

Ralph Loop is unbounded by construction. Termination must be enforced externally. Acceptable terminators (any one is sufficient):

| Terminator | Mechanism | When to use |
|------------|-----------|-------------|
| `<promise>COMPLETE</promise>` | Agent emits sentinel in stdout; runner greps and exits | well-defined goal with clear completion semantics (snarktank/ralph style) |
| `MAX_ITERATIONS` cap | Runner counter | safety cap regardless of agent claim |
| `LOOP_TIMEOUT` | Runner wall clock | overnight runs |
| `TOKEN_BUDGET` USD cap | Runner accumulator | every Ralph Loop must have this |
| `verify.sh PASS` + `done.md` | DONE Evidence Gate | Orbit standard |

[Source: https://github.com/snarktank/ralph]

**Hard rule**: Never rely on the agent's self-assessment alone. A Ralph Loop must have at least two independent terminators active.

## 10. Green-field-only Constraint

Huntley's strong claim: "There's no way in heck would I use Ralph in an existing code base." [Source: https://ghuntley.com/ralph/]

Operational rule for Orbit:

- During `INTAKE`, check whether the target directory has prior commits, a populated `src/`, or non-trivial dependency manifest.
- If yes → classify as **brownfield**. Refuse to generate a Ralph-style loop. Recommend Orbit's standard `nexus-autoloop` template (scoped, branch-isolated, evidence-gated) instead, which is safer for existing code.
- If no → green-field permitted. Generate Ralph-style runner.

Detection heuristic (any one triggers brownfield):

```bash
[[ $(git rev-list --count HEAD 2>/dev/null || echo 0) -gt 10 ]] \
 || [[ $(find src -type f 2>/dev/null | wc -l) -gt 20 ]] \
 || [[ -f package-lock.json && $(jq '.packages | length' package-lock.json) -gt 50 ]]
```

If a user explicitly forces Ralph in a brownfield, log a warning, require `RALPH_BROWNFIELD_ACK=true`, and tighten guardrails: `WORKTREE_ISOLATION=true`, mandatory `997_DO_NOT_EDIT_TESTS_OR_VERIFY`, mandatory rollback rehearsal.

## 11. Huntley's Anti-Pattern Warnings

These are warnings Huntley himself documents. Orbit must surface them when generating or auditing a Ralph-style loop.

| Warning | Source mechanism | Orbit mitigation |
|---------|------------------|------------------|
| "Don't assume not implemented" | `ripgrep` miss → agent claims missing → reimplements | `995_DO_NOT_ASSUME_NOT_IMPLEMENTED` rule + require `rg -i` + symbol search before claim |
| Placeholder implementations | Agent stubs to pass build | `990_DO_NOT_IMPLEMENT_PLACEHOLDERS` rule + AP-12 detection in verify (grep TODO/`return None`/`NotImplementedError`) |
| Unbounded parallelism | All build/test as subagents | RP-5: serialise to 1 subagent for build/test |
| Runtime filtering | Agent filters tasks at runtime → 70-80% reliability | Lock scope in `plan` mode; `build` mode picks top item, no filtering |
| Stale plan fixation | Agent loops on outdated plan | RP-6 plan disposability + Orbit's CONVERGENCE_STALL detection |
| AGENTS.md contamination | Progress notes leak into AGENTS.md | RP-4: 60-line cap, hash pin warning |
| Existing codebase use | Ralph applied to brownfield | Section 10 detection + refusal |

## 12. Adjacent Best Practices (non-default, opt-in)

These are documented practices from 2025-2026 sources that complement Ralph but are not yet default in Orbit. Enable via env var or explicit goal directive.

| ID | Practice | Trigger | Source |
|----|----------|---------|--------|
| `BP-2` | Property-based verify oracle | Goal has `VERIFY_STYLE=property` | [PGS paper](https://arxiv.org/html/2506.18315v1), [Mutation testing post](https://dev.to/rsri/mutation-testing-the-missing-safety-net-for-ai-generated-code-54kn) |
| `BP-3` | Mutation testing as convergence signal | `MUTATION_GATE=true` and `mutmut`/`Stryker` available | [Test Double](https://testdouble.com/insights/keep-your-coding-agent-on-task-with-mutation-testing) |
| `BP-5` | Model cascade routing (cheap→expensive) | `MODEL_TIER_DEFAULT` ≠ `MODEL_TIER_VERIFY` | [Paxrel](https://paxrel.com/blog/ai-agent-cost-optimization), [OpenReview](https://openreview.net/forum?id=AAl89VNNy1) |
| `BP-6` | microVM / gVisor hardware sandbox | `SANDBOX_MODE=microvm` | [Northflank](https://northflank.com/blog/how-to-sandbox-ai-agents), [Microsoft Security](https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/) |
| `BP-8` | Screenshot multimodal verify | `MULTIMODAL_VERIFY=true` + Vision model configured | [DEV.to](https://dev.to/custodiaadmin/how-multi-agent-ai-systems-use-screenshots-as-shared-ground-truth-3poh) |
| `BP-10` | Vertical-slice atomic task sizing (45-120 min) | `TASK_SIZING=vertical_slice` | [CodeSignal](https://codesignal.com/learn/courses/task-decomposition-execution-with-claude-code/lessons/atomic-task-design) |

Orbit's three already-promoted defaults (BP-1 cache, BP-4 critic, BP-7 worktree) appear in `SKILL.md` and `patterns.md`, not here.

## 13. Quick Reference

**Decision checklist before generating a Ralph runner**:

- [ ] Goal directory is green-field (Section 10 heuristic passes).
- [ ] `PROMPT.md`, `PROMPT_plan.md`, `PROMPT_build.md` are planned distinct files (RP-2).
- [ ] `AGENTS.md` skeleton ≤ 60 lines (RP-4).
- [ ] At least two independent terminators configured (Section 9).
- [ ] `<promise>COMPLETE</promise>` sentinel or equivalent included.
- [ ] `9xx` critical rules cover placeholders, assume-missing, prompt-immutability, tests-immutability, goal-immutability (Section 4).
- [ ] Build/test subagent count is exactly 1 (RP-5).
- [ ] `WORKTREE_ISOLATION=true` and `TOKEN_BUDGET > 0` (default-on).
- [ ] Plan disposability triggers wired to CONVERGENCE_STALL / OSCILLATION_LOOP (RP-6).
- [ ] User has acknowledged green-field constraint if running long unattended sessions.

**Detection signals for a runner claiming to be Ralph but breaking the pattern**:

| Signal | Likely violation |
|--------|------------------|
| `PROMPT.md` mtime changes mid-run | RP-1 (immutability) |
| `AGENTS.md` > 60 lines or contains "completed", "done", "progress" | RP-4 (contamination) |
| `claude` invoked with prior `--resume` flag | RP-7 (filesystem-as-memory broken) |
| Multiple `claude` build invocations in a single iteration | RP-5 (subagent rule) |
| `fix_plan.md` top item unchanged for 3+ iters with no progress | RP-6 (plan should regenerate) |
| Initial commit count > 10 or large dependency manifest | Section 10 (green-field check failed) |
