# Loop Engineering — Concept, Lineage, and Applicability

External context for *why* a loop exists, *who* shaped the pattern, and *when not to build one*. Orbit owns the mechanics (contracts, scripts, recovery); this file owns the framing that decides whether a loop is the right answer at all.

> Snapshot date: 2026-06-11. Fast-moving topic — term and feature versions can shift within weeks. Verify version numbers against primary docs before quoting.

## Definition

**Loop engineering** = replacing *yourself as the person who prompts the agent* with a system that does the prompting. A loop is a **recursive goal**: define a purpose, let the agent iterate until a verifiable stop condition holds. It is an orchestration pattern that combines four parts:

1. **Scheduled/recurring execution** (the heartbeat)
2. **Isolated workspaces** (parallel agents don't collide)
3. **Verification agents** (a checker separate from the maker)
4. **Persistent memory** (state outside the conversation, on disk)

This is exactly Orbit's territory: 1 → `run-loop.sh` cadence, 2 → `git worktree` isolation, 3 → independent `CRITIC_MODEL` DONE gate, 4 → `state.env` / `progress.md` / `done.md` filesystem-as-memory.

## Lineage (who said what)

| Person | Role | Claim | Confidence |
|--------|------|-------|------------|
| **Peter Steinberger** (@steipete) | OpenClaw steward | "You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents." Runs a supervisory multi-agent loop (`claw` supervising multiple Codex instances). | high |
| **Boris Cherny** (@bcherny) | Creator / head of Claude Code, Anthropic | "I don't prompt Claude anymore. I have loops running that prompt Claude… My job is to write loops." Reported (Fortune, 2026-06-08) to have not written code for ~8 months while supervising tens of thousands of agents. | high |
| **Addy Osmani** | Google engineer | **Named** (not invented) the pattern "loop engineering" in a blog post on 2026-06-07. Stresses "Verification is still on you." | high |

- Primary sources: addyosmani.com/blog/loop-engineering, thenewstack.io/loop-engineering, developers.openai.com/codex/subagents, code.claude.com/docs.
- Note: X/Twitter source URLs return HTTP 402 (text confirmed via Fortune / Lenny's / Digg secondaries). Steinberger's exact claw→Codex topology mechanics (prompt handoff, stop conditions, cost control) remain undisclosed.

## When NOT to build a loop (applicability limits)

A loop is *not* always the right answer. For one-off tasks, a single well-aimed prompt is faster and cheaper. Skip loops when:

1. **Solo builder on a consumer usage-based plan** — token cost dominates; loop ROI is unproven (no public verifiable case study exists yet).
2. **The code has no automated verification** — an unattended loop is a loop making mistakes unattended; without a real checker, "done" is a claim, not a proof.
3. **The real constraint is review capacity, not typing speed** — loops lengthen the review queue rather than shortening delivery.

These map to Orbit guardrails already in the SKILL: external termination enforcement, independent `CRITIC_MODEL` DONE gate (never trust verify-PASS alone — see AP-12/AP-18), and `USD_PER_RUN_CAP` / `BURN_RATE_ANOMALY` cost caps.

Confidence on this section: medium (critique synthesized largely from secondary sources, e.g. AlphaSignal 2026-06-08). Treat as directional, not absolute. The stronger claim "loops only pay off when all four of {weekly repetition, automated verification, slack token budget, senior-engineer tooling} hold" was weakly refuted in verification (1-2) — necessary-condition framing is too strict.

## Canonical loop shapes (verified 2026-06-15)

Two well-documented loops anchor the design space — one official, one community:

- **evaluator-optimizer** (Anthropic, *Building Effective Agents* + cookbook): a generator LLM produces, a *separate* evaluator LLM returns PASS or feedback inside the loop; **PASS is the only exit** (`while True: if evaluation == "PASS": return result` — no max-iteration cap by itself), and feedback folds into the next generation's context. This is the maker/checker split as a control loop.
- **Ralph** (Geoffrey Huntley / HumanLayer origin; `snarktank/ralph` reference impl): a bash `while` loop re-piping a static prompt into a fresh agent instance. The load-bearing ideas, all verified:
  - **Fresh context per iteration** — state lives *outside* the conversation: git history + `progress.txt` + `prd.json`, not in-context memory.
  - **Per-iteration cycle is observe → decide → act → verify**: pick the highest-priority `passes:false` story → implement *one* → run typecheck/tests → commit only if green → update `prd.json` / append `progress.txt`.
  - **Loop-until-done via completeness sentinel**: when all stories are `passes:true`, the agent emits `<promise>COMPLETE</promise>` and the loop `grep`s for it to exit. (The original Huntley one-liner had *no* auto-exit — operator stopped it by hand; later variants added Stop-hook / max-iterations / sentinel exits.)
  - **The loop only functions with a real verification gate** (typecheck/tests/green CI). No checker → broken code compounds across iterations. Each story must fit in one context window.

**Drift / "overbaking"** is the signature failure of running too long: bizarre emergent scope creep (the canonical anecdote: a loop adding unrequested post-quantum crypto). Mitigation that practitioners converge on — **bound the loop**: tight spec, iteration/time limit, acceptance tests, and for desired-state loops, **run ONCE on an overnight cron merging small increments** rather than unbounded continuous runs. (Practitioner consensus, not benchmarked.)

> Refuted in verification — do not repeat: `/loop` "expires after 3 days" (it's **7 days**); Ralph being "cost-efficient at ~$10-12/hr indefinitely"; "frequent context resets/compaction are *essential* to loop reliability" (fresh-context-per-iteration is one valid design, not a universal requirement).

## How this informs Orbit decisions

- At `INTAKE`/`CONTRACT`: if the goal matches a "skip a loop" case above, say so and recommend a direct prompt instead of generating a runner. A loop with no automated verification command should fail `ON_GOAL_CONTRACT_WEAK`.
- At `CONTRACT`: the maker/checker split is the load-bearing primitive — it is what makes "I can walk away" true. This is the same idea as Claude Code `/goal` (a fresh fast model decides completion) applied to the stop condition itself.
- At `HANDOFF`/`LEARN`: when no verifiable ROI evidence exists for the loop class, record it as an open risk rather than asserting efficiency gains.
