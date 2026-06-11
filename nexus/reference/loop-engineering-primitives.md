# Loop-Engineering Primitives — Claude Code & Codex (2026-06)

How the **loop engineering** pattern maps onto concrete orchestration primitives in each hub engine. Nexus stays the routing/recipe layer; this file is the reference for *which primitive implements which loop part* when designing a `/goal`-style or apex/summit loop. For the concept, lineage, and applicability limits see `orbit/reference/loop-engineering.md`.

> Snapshot date: 2026-06-11. Versions move within weeks — verify against primary docs (`code.claude.com/docs`, `developers.openai.com/codex`) before quoting a version number.

## The pattern → primitive map

A loop = scheduled execution + isolated workspaces + maker/checker separation + persistent memory. Both hub engines now ship all parts natively (previously hand-rolled bash).

| Loop part | Claude Code | Codex |
|-----------|-------------|-------|
| Heartbeat (recurring) | `/loop` (cron syntax, v2.1.72+, e.g. `0 9 * * 1-5`); hooks; GitHub Actions for laptop-closed runs | Automations tab (project + prompt + cadence + local/worktree target); Triage inbox for findings |
| Stop-when-done (in-session) | `/goal` (v2.1.139+): runs until a written condition holds; **a separate fast model — default Haiku — checks completion each turn**, so the maker isn't the grader | `/goal`: same primitive — works across turns until a verifiable stop condition, with pause/resume/clear |
| Workspace isolation | `git worktree`; `--worktree`/`-w` → `.claude/worktrees/<value>/` on branch `worktree-<value>` (v2.1.50); `isolation: worktree` in subagent frontmatter (temp worktree auto-removed if subagent finishes with no changes) | Built-in worktree support; multiple threads hit one repo without collision |
| Maker/checker separation | subagents (`.claude/agents/`, markdown) + agent teams; worktrees isolate *file edits*, subagents/teams coordinate *the work* | subagents spawned in parallel (≤8), results merged into one response; built-in `default`/`worker`/`explorer`; custom agents require `name`/`description`/`developer_instructions` (model + sandbox_mode inherited from parent); on-demand spawn only |
| Persistent memory | markdown / Linear / state files on disk — "the agent forgets, the repo doesn't" | same: state file outside the conversation as the loop's spine |

## Engine framing (official)

- Anthropic frames Claude Code itself as the **agentic harness** around Claude: tools + context management + execution environment that turn an LLM into a coding agent. The agentic loop = *models that reason* + *tools that act*; each tool result feeds back to inform the next decision.
- Claude Code's loop is three blended phases — **gather context → take action → verify results** — repeated adaptively until the task is complete (a question may need only context-gathering; a bug fix cycles all three repeatedly).

## How this informs Nexus routing

- **`goal` recipe** (`reference/goal-recipe.md`): `/goal`'s fresh-model completion check *is* the maker/checker split applied to the stop condition. When setting up a goal loop, require a verifiable stop condition (e.g. "all tests in test/auth pass and lint clean"), not a vague "done".
- **`apex` Phase 6 / `summit` Phase 5**: these are loop-engineering loops driven by Orbit. Worktree-per-iteration + independent critic model are the load-bearing reliability primitives — see `reference/apex-recipe.md`, `reference/summit-recipe.md`.
- **Cross-engine portability**: connectors on both engines speak MCP, so a connector written for one usually works in the other. The loop *shape* is engine-agnostic — design the recipe once; bind primitives per `Orchestrator Detection`.
- **Known issue**: Claude Code GitHub issue #50357 — `isolation: worktree` is not applied via top-level `claude --agent`; it works via frontmatter. Surface this if recommending CLI-flag-based isolation.

## Caveats / gaps

- No public, verifiable ROI case study for loop engineering exists yet (esp. solo/consumer-plan). Don't assert efficiency gains as fact.
- Attribution detail and applicability limits live in `orbit/reference/loop-engineering.md`; this file is primitives-only.
