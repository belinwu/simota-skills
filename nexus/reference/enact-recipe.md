# Nexus Enact Recipe Reference

**Purpose:** Read an existing **Charter**, construct the team from its roster, and **orchestrate every work package end-to-end** until the work is shipped. Enact is the execution half of the `charter → enact` pair.
**Read when:** User invokes `/nexus enact`, or asks to "run the Charter", "build the team from the instruction document and execute it", or "execute `docs/CHARTER.md` start to finish". For *authoring* the Charter, see `reference/charter-recipe.md`.

## Contents
- Overview
- Input: the Charter contract
- Invocation Modes
- Topology
- Phase 1: Team Construction
- ★ Confirm Gate
- Phase 2: End-to-End Orchestration
- Phase 3: Verify & Deliver
- Conditional Inclusion
- AUTORUN Chain Template
- Failure Escalation
- Cost and Latency Profile

---

## Overview

Enact turns a Charter into shipped work. It does **no analysis and no planning** — the Charter (authored by `charter`, or hand-written to the same schema) is the complete source of truth. Enact:

1. **Constructs the team** strictly from Charter §5 (roster) — resolving each role→skill→spawn config and verifying spawn prereqs. The team is a pure function of the document, so re-running enact on the same Charter rebuilds the identical team.
2. **Orchestrates** Charter §4 (work breakdown) via the §6 plan — spawning each work package's owner, running build loops via Orbit, enforcing guardrails, and aggregating hub-spoke.
3. **Verifies & delivers** against §7 (verification plan), then updates the Charter's §9 Execution Log so the document reflects what was actually done — the living Charter.

Because authoring is already paid for, enact is opt-in and explicit: it spawns the full execution team and writes code, so it confirms before building (the ★ Confirm Gate).

## Input: the Charter contract

Enact requires a Charter conforming to the schema in `reference/charter-recipe.md` § Charter Document Schema. It reads:

| Section | Used by | For |
|---------|---------|-----|
| §3 Conventions & Guardrails | all phases | commit/test/lint/build commands, branch policy, L4 rules |
| §4 Work Breakdown | Phase 2 | atomic steps, dependencies, sequencing, per-package AC |
| §5 Team Roster | Phase 1 | owner skill + model tier + engine + spawn config per package |
| §6 Orchestration Plan | Phase 2 | chain order, parallel branches + file ownership, checkpoints |
| §7 Verification Plan | Phase 3 | per-package + final gates |
| §8 Escalation & Rollback | all phases | failure tiers, circuit breaker, rollback boundaries |
| §9 Execution Log | Phase 2-3 | append progress; resume from last checkpoint |

The machine-readable companion (`CHARTER.roster.yaml`) is preferred for §5-§6 when present. If the Charter is missing a required section or a roster entry names a non-existent skill, enact stops at Phase 1 and reports the gap rather than improvising (the missing design belongs in `charter`, not here).

## Invocation Modes

| Form | Behavior |
|------|----------|
| `/nexus enact` (no args) | Read `docs/CHARTER.md` (default), construct + run. |
| `/nexus enact <path>` | Read the Charter at `<path>`, construct + run. |
| `/nexus enact dry-run` | Phase 1 only — construct + verify the team, report constructability, **do not execute**. |
| `/nexus enact resume` | Resume from the last §9 Execution Log checkpoint (skips completed packages). |

## Topology

```
                Phase 1                  ★ Confirm   Phase 2                          Phase 3
                [Team Construction]                  [End-to-End Orchestration]       [Verify & Deliver]
read Charter    ┌──────────────────┐     ┌───────┐  ┌────────────────────────────┐   ┌──────────────┐
docs/CHARTER.md │ §5 → bind        │     │ 👤    │  │ per §4 work package (§6 order):│   │ §7 gates     │
+ roster.yaml ─▶│  role→skill→spawn│ ──▶ │ build │─▶│  spawn assigned owner       │ ─▶│ radar?/judge?│
                │ verify prereqs   │     │ team? │  │  ‖ parallel + file ownership│   │ guardian?    │
                │ sub-orch setup   │     │ cost  │  │  build loops → orbit (sub)  │   │ launch?      │
                │ dry-run check    │     └───────┘  │  checkpoints + guardrails   │   │ → update §9  │
                └──────────────────┘                │  hub-spoke aggregate → §9   │   │ → DELIVER    │
                                                    └────────────────────────────┘   └──────────────┘
                          ◀──────── Failure escalation (per Charter §8) ───────────────────┘
```

Hub-and-spoke is preserved: Nexus is the only top-level orchestrator. Where Charter §5 nominates a sub-orchestrator (Vision for UX clusters, Orbit for build loops, Rally for parallel sessions), Nexus spawns it as a ≤7-specialist sub-hub — never agent-to-agent.

## Phase 1: Team Construction

Instantiate the team strictly from Charter §5. This is "build the dev team from the Charter".

| Step | Action |
|------|--------|
| Bind | For each roster entry, resolve role → skill SKILL.md path, model tier, engine (per Orchestrator Detection), and spawn config |
| Verify prereqs | Confirm the active hub's spawn tool + per-CLI prereqs (`reference/execution-layers.md`); for Codex/agy clusters, check `_common/CLI_COMPATIBILITY.md §9` |
| Sub-orchestrator setup | Where §5 nominates Vision/Orbit/Rally, prepare its sub-hub contract (≤7 specialists each) |
| Dry-run check | Validate that every §4 work package has a constructable owner; any unconstructable entry escalates before execution begins |

**Exit gate:** every work package has a verified, spawnable owner. Unresolvable roster entries do **not** get improvised — enact reports the gap and recommends re-authoring via `charter` (§5). `dry-run` mode stops here and delivers the constructability report.

## ★ Confirm Gate

Team construction + full orchestration spawns the execution team and writes code (potentially many spawns + iterations + file writes). The gate sits at Phase 1 exit and is the single human checkpoint under `AUTORUN_FULL`.

| Mode | Behavior |
|------|----------|
| `INTERACTIVE` | Always confirm; user may adjust before build |
| `GUIDED` | Always confirm; approve / abort |
| `AUTORUN` | Explicit Y/N; default abort on no response |
| `AUTORUN_FULL` | Present construction summary (work-package count, roster size, estimated agent count / cost / time), **wait 60s for objection**, then proceed. Any input within the window pauses. |

`dry-run` never reaches execution regardless of mode.

## Phase 2: End-to-End Orchestration

Execute Charter §4 via the §6 Orchestration Plan. Standard Nexus EXECUTE → AGGREGATE machinery, parameterized by the Charter.

- **Spawn per work package** in §4 order; pass only state deltas (`reference/context-strategy.md`). Independent packages run as parallel branches with file ownership from §6 (`_common/PARALLEL.md`); no shared mutable state.
- **Build loops** (multi-iteration implementation packages) delegate to `orbit` as a sub-orchestrator (build → judge → test → converge), as in Apex Phase 6. Engine per Charter §5 (Codex CLI for high-volume coding loops where available).
- **Guardrails** L1-L4 + checkpoint-resume on 4+ step chains; circuit breaker on 3 consecutive package failures; max-hop limit enforced; destructive/L4 actions per §3/§8 confirm.
- **Aggregate** branch outputs hub-spoke; validate schema + semantic correctness at each boundary.
- **Append** progress to Charter §9 (Execution Log) at each package boundary so the document stays the source of truth and `enact resume` can restart from the last logged checkpoint.

**Exit gate:** all non-blocked work packages reach SUCCESS/PARTIAL with outputs aggregated; blocked packages logged in §9 with unblock conditions.

## Phase 3: Verify & Deliver

| Agent | Role | Required |
|-------|------|----------|
| `radar` | Fill test gaps / run the verification suite per §7 | Conditional: code changed |
| `judge` | Final review of aggregated changes | Conditional: code changed |
| `guardian` | Commit policy, branch strategy, PR preparation | Yes (if code changed) |
| `launch` | Release/rollback plan | Conditional: release in scope |

Run §7 gates (tests/build/security/AC). Update the Charter (§9 + any §4 AC status) so the delivered document reflects what was actually done — the living Charter. `DELIVER` returns `NEXUS_COMPLETE` with the Charter path, per-package status, verification results, and follow-ups.

**Exit gate:** §7 verification passes (or failures surfaced honestly with output, per global quality rules); Charter persisted and current.

## Conditional Inclusion

| Condition | Add | Skip |
|-----------|-----|------|
| `dry-run` | — | ★ Confirm, Phase 2, Phase 3 |
| `resume` | — | already-completed §9 packages |
| No code changes (docs/plan-only Charter) | — | radar, judge, guardian, launch |
| Work cluster needs hierarchy (per §5) | Vision/Orbit/Rally sub-orchestrator | — |
| Release in scope (per §7/§8) | launch | — |

## AUTORUN Chain Template

```
Nexus AUTORUN enact docs/CHARTER.md
  ── read Charter ─────────────────────────────────────
  → parse docs/CHARTER.md (+ CHARTER.roster.yaml if present)
  → validate required sections (§3-§8); missing/invalid → stop + report gap
  ── Phase 1 Team Construction ────────────────────────
  → for each §5 roster entry: bind(role→skill→spawn) + verify prereqs
  → sub-orchestrator setup (Vision/Orbit/Rally)? → dry-run check
     (enact dry-run → STOP + deliver constructability report)
  ── ★ Confirm Gate ───────────────────────────────────
  → AUTORUN_FULL: construction summary + 60s objection window → proceed
  ── Phase 2 End-to-End Orchestration ─────────────────
  → for each §4 work package in §6 order:
       spawn(owner_skill, contract=package.AC, model=§5.tier, engine=§5.engine)
       ‖ parallel branches with §6 file ownership
       build-loop packages → orbit(sub-orchestrator)
       checkpoints + guardrails + circuit breaker
       append §9 Execution Log per package boundary
  → aggregate hub-spoke
  ── Phase 3 Verify & Deliver ─────────────────────────
  → radar? + judge? → §7 gates (tests/build/sec/AC)
  → guardian(commit/PR)? → launch(release)?
  → update Charter (§9 + AC status) → NEXUS_COMPLETE(charter_path, statuses)
```

## Failure Escalation

| Failure | Detected by | Escalation |
|---------|-------------|------------|
| Charter missing/invalid section | enact parse | Stop; report which section; recommend `charter` to re-author |
| §5 roster names a non-existent skill | enact bind | Stop at Phase 1; report the gap; do not improvise an owner |
| Phase 1 roster entry unconstructable (spawn prereq unmet) | Nexus | Stop; report blocker (per `reference/execution-layers.md`); recommend §5 fix or prereq setup |
| ★ Confirm rejected | user | Abort; Charter unchanged |
| Phase 2 package repeat failure | judge/radar | Scout investigation → back to the package owner; circuit breaker after 3 (per §8) |
| Build loop stuck / over budget | orbit | Triage handoff; user confirm before continuation |
| §7 verification fails | radar/judge | Report honestly with output; do not mask (global quality rule) |

## Cost and Latency Profile

| Profile | Phases active | Approx agent count | Approx cost |
|---------|---------------|--------------------|-------------|
| dry-run | 1 | per §5 roster size (no execution) | Low |
| small Charter (no build loops) | 1, 2, 3 | 6-12 | Medium |
| standard Charter (1-2 build loops) | All | 12-20 | Medium-High |
| large Charter (multiple build loops + sub-orchestrators) | All + orbit loops + Vision/Rally | 20-30+ | High |

Enact is the expensive half of the pair; the ★ Confirm Gate, 5+-agent chain confirmation, orbit cost-per-task tracking, and L4 gates bound spend. Because the team is reconstructed from the Charter, `enact` can be re-run (or `resume`d) without re-paying for analysis/authoring.

---

## Visualization

Topology ASCII above. Enact consumes `docs/CHARTER.md` (+ `CHARTER.roster.yaml`) and writes back §9; the Charter remains the single source of truth across runs.
