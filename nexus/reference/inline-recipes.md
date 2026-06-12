# Inline Recipes — `kaizen` / `essential` / `killer`

**Purpose:** Full phase contracts for the three Recipes that have no separate reference file. SKILL.md `## Subcommand Dispatch` keeps only a summary; this file holds the complete contracts.

**Read when:** Executing one of `kaizen`, `essential`, or `killer` Recipes.

---

## `kaizen` — Multi-axis iterative improvement of an existing feature

> **Kaizen is a PDCA loop, not a single pass.** The contract below runs Phase 3↔4 as a bounded improvement cycle against a quantified target, and stops on target-met OR diminishing-returns — never "one improvement and done". Default Mode: `AUTORUN` (each cycle is scope-bounded and reversible); escalate to `GUIDED` when an axis touches 10+ files or structural boundaries (then Magi confirms the axis plan before Phase 3). Engine routing follows summit principles: Codex owns code-gen (Bolt/Tuner/Zen/Sweep/Artisan/Builder), Claude owns judgment/measurement (Lens/Pulse/Echo/Magi/Radar-gate/Guardian).

- **Phase 1 DIAGNOSE + BASELINE (parallel)** — Lens[claude map-current-implementation] unconditionally; conditionally add Pulse[claude KPI-measure] if metrics instrumentation exists, Echo[claude UX-walkthrough] if UI surface, Voice[claude sentiment]/Trace[claude session-replay] if user-feedback or session data is available. **Capture a quantified baseline per candidate axis** (perf: latency/render numbers; code-quality: complexity/coverage; UX: friction/task-success; feature-extension: usage gap). Non-instrumented surfaces → record a qualitative baseline (Echo/Voice rubric score). Goal: multi-signal picture **with a measurable starting point** to compare against later.
- **Phase 2 PROPOSE + TARGET GATE (sequential)** — Spark[claude improvement-spec, **constrained to enhancing existing data/logic** — not new feature ideation] → Magi[claude axis-prioritize] selects **one or two** axes from `{perf, UX, code-quality, feature-extension}` AND, for each, fixes a **stop criterion**: a target value (e.g. "p95 < 200ms", "coverage ≥ 80%") and a **max iteration count** (default 3). Rejects "improve everything" plans; rejects axes with no measurable target ("improve without measuring" cannot enter Phase 3).
- **Phase 3 IMPROVE (axis-bounded, parallel within axis)** — perf → Bolt[codex frontend]/Tuner[codex explain]; UX → Palette[codex usability]/Prose[codex microcopy]/Flow[codex motion]; code-quality → Zen[codex refactor]/Sweep[codex dead-code]; feature-extension → Artisan[codex component]/Builder[codex api]. Independent sub-axes parallel; dependent ones serialize.
- **Phase 4 VERIFY + CROSS-AXIS GUARD (the loop gate)** — Radar[claude-gated regression] blocks any regression of existing behavior. Re-measure the Phase 1 baseline metric for the worked axis (Pulse/Echo Before/After). **Cross-axis guard**: confirm the improvement did not regress a *non-worked* axis (e.g. a perf change that hurt UX, or a refactor that dropped coverage) — if it did, the cycle fails the gate. Then branch:
  - **Target met** (metric reached the Phase 2 stop value, no regression) → exit loop → Phase 5.
  - **Target not met AND iterations remain AND last cycle's marginal gain ≥ threshold** → loop back to Phase 3 for the next cycle (carry forward the delta, not a fresh diagnose).
  - **Diminishing returns** (marginal gain below threshold) OR **iteration cap reached** → Void[claude] confirms the stop, records "remaining gap vs target", → Phase 5 with partial-improvement note. Never burn cycles past the point of marginal value.
- **Phase 5 SHIP** — Guardian[claude PR-prep] produces PR with embedded Before/After report: baseline → final per axis, cycles run, stop reason (target-met | diminishing-returns | cap), and any residual gap.
- **Boundaries**: vs `refactor` (internal-only, no external delta) — kaizen explicitly improves externally-observable quality alongside internal hygiene. vs `optimize` (perf-only) — kaizen treats perf as one axis. vs `feature` (new capability) — kaizen polishes a shipped feature. vs `apex`/loop recipes — kaizen's loop is *scope-bounded to chosen axes against a fixed target*, not open-ended discovery.
- **Anti-patterns prevented**: (1) "rewrite the whole module under improvement banner" (Magi axis-cap), (2) "improve without measuring" (Phase 1 baseline + Phase 2 target gate are mandatory entry conditions for Phase 3), (3) "improvement that regresses something else" (Phase 4 Radar + cross-axis guard), (4) **"single-pass masquerading as kaizen"** (Phase 3↔4 loop with quantified stop criterion), (5) **"polish past the point of value"** (diminishing-returns + iteration cap force a Void-confirmed stop).
- **Add-ons**: +Scout for deeper root-cause when Lens insufficient, +Atlas for structural change, +Ripple for cross-module impact before committing to an axis, +Experiment to A/B-validate a user-facing improvement against the baseline when traffic allows.

---

## `essential` — Single must-have verdict + conditional implementation

- **Phase 1-4 Verdict (sequential refinement funnel)** — Plea[claude pain-extraction] → Spark[claude spec] → Magi[claude necessity-arbitration] → Rank[claude MoSCoW-must]. Each step narrows the previous output; parallelization would force redundant re-synthesis. Subtraction-oriented — Magi's Sophia filters "Should-have" posing as "Must-have".
- **Convergence rule**: Rank's MoSCoW output filtered to **the single top Must-have** (highest necessity score). Tie-break: defer to Magi's Sophia; still tied → escalate to user via AskUserQuestion with tied candidates.
- **Phase 5 DELIVER verdict via AskUserQuestion** — card format: `## Essential Verdict / Recommended must-have: <single feature> / Why: <2-3 lines> / Source of conviction: Plea→Spark→Magi→Rank summary / Considered but rejected: <2-3 alternatives, one-line reasons> / → Build this? [Yes / No / Modify]`.
- **Phase 6 Conditional Implementation (only if Yes)**: Sherpa[claude atomic-decomposition] → Builder[codex] → Radar[codex] → Guardian[claude] → DELIVER working feature + tests + PR. Engine routing follows summit principles (Codex owns code-gen, Claude owns judgment).
- **If No**: DELIVER verdict artifact as "decided-not-to-build" record; do not run Phase 6.
- **If Modify**: capture user input (what to change), loop back to Phase 1 with the modification as additional constraint.
- **Failure mode prevented**: over-engineering (Phase 1-5) + unbounded implementation scope (Phase 6 inherits the single-feature constraint).
- **Add-ons**: +Void for aggressive scope cut, +Accord for atomic-unit specs in Phase 1-4.

---

## `killer` — Single differentiator verdict + conditional flagged implementation

- **Phase 1 (parallel hub-spoke, cross-engine triangulation, dual-engine baseline)** — Default baseline distributes Phase 1 branches across **both Claude and Codex** to preserve perspective independence at the model-priors level (not just prompt-frame level): Compete[**claude** + WebSearch tool for current market gap-analysis, framed as "industry analyst"] ‖ Flux[**codex** sandbox-execution priors, framed as "what would the market gap look like in code / infrastructure / developer-experience terms" — Codex's GitHub-heavy training surfaces gaps a market-focused model misses] ‖ Plea[**claude** empathy/latent-needs, framed as "user advocate"]. **Optional agy lift (when AVAILABLE at PREFLIGHT)**: Compete adds a second branch on agy (Search-grounded for fresher market data than Claude's training cutoff), Flux adds a second branch on agy (Deep Think mode for cross-domain analogy generation) — agy's training-data priors give an additional independence axis. Failure mode prevented: model-monoculture in the triangulation step. Engine-attribution tags: `[claude-compete]`, `[codex-flux]`, `[claude-plea]` for the dual-engine baseline; add `[agy-search]`, `[agy-deepthink]` when the optional lift is active.
- **Phase 2 (sequential synthesis)** — Spark[claude] aggregates the independent perspectives into **the single most decisive killer feature** (one feature, not a ranked list).
- **Phase 3 DEFEND + VERIFY (the killer-grade gate — a decisive feature that can't survive this is just a nice-to-have)** —
  - **Moat check** — Compete[claude] classifies defensibility: **time-to-copy** (can a competitor replicate within one release cycle?) and **moat class** (data / network-effect / integration-depth / switching-cost / brand / none). A feature with `moat=none` AND time-to-copy < one cycle is **downgraded from "killer" to "nice-to-have"** and must not pass as a killer verdict — Magi weighs the moat class as a first-class GO criterion, not an afterthought.
  - **Adversarial refutation (cross-engine, high-stakes)** — 2-3 independent skeptics, distributed across engines for prior-diversity (claude + codex), each prompted to **REFUTE** the killer claim from a distinct angle: "this gap is already served by <X>" (market), "users don't actually want this enough to switch" (demand), "infeasible at our scale/timeline" (delivery). Default to refuted when uncertain. **Majority-refute → forces NO-GO or Modify** (a flagged production build must not launch on an unrefuted-but-unchallenged claim).
  - Then **Magi[claude] binary Go/No-Go** incorporating moat class + refutation survival.
- **Convergence rule**: Spark MUST synthesize one feature (not a ranked list); Magi delivers binary Go/No-Go gated on moat-class + refutation-survival. Tie-break: Magi forces selection via strategic-impact criterion (market timing × differentiation depth × **moat durability** × feasibility); NO-GO still surfaces runner-up with "weakest-link" annotation.
- **Phase 4 DELIVER verdict via AskUserQuestion** — card with perspective-attributed evidence (mark which frame produced which insight; note which branches were agy-backed vs Claude-frame-only) + **moat class + time-to-copy + which refutations the feature survived** + Magi verdict (GO confidence H/M/L | NO-GO reason) → Ship this? [Yes / No / Modify].
- **Phase 5 Conditional Implementation (only if Yes)**: Sherpa[claude decomposition] → if `ui_dimension != none`: Forge[codex prototype-validation] → Artisan[codex frontend-production] → Builder[codex backend/logic] → Radar[codex edge cases for differentiator] → judge[claude multi-engine review — killer features are high-stakes] → Guardian[claude] **with feature-flag recommendation** for controlled rollout (differentiation risk) → DELIVER working feature + tests + PR + flag config + rollout plan. **The flag is not a bare on/off** — it carries (a) the **differentiation KPI** (the measurable form of the Phase 3 killer hypothesis: the adoption / retention / switching signal that proves the edge is real), (b) a **ramp schedule** (e.g. 5% → 25% → 100% gated on the KPI clearing a threshold), and (c) a **kill criterion** (the KPI value below which the differentiation hypothesis is falsified and the flag rolls back). Hand off to `growth-acceptance` when the +14/+30/+90d measurement loop is warranted.
- **If No**: DELIVER "decided-not-to-ship" strategic record (include the moat verdict + surviving/failed refutations so the decision is auditable).
- **If Modify**: loop back to Phase 1 with the modification as an **added constraint** (e.g., "reframe around X constraint" → Flux re-runs with updated directive); **carry forward the refuted claims as exclusions** so the reframe does not re-derive an already-refuted feature. Bound to 2 Modify loops, then escalate to user.
- **Add-ons**: +Riff for iterative deep-dive on Spark output in Phase 2, +Field for additional market trend grounding in Phase 1, +Omen for a pre-mortem on the differentiation bet before Phase 5 commits.

---

## Visualizations

Mermaid flow diagrams (render via mermaid.live or compatible viewer):
- [`essential-recipe-flow.mmd`](essential-recipe-flow.mmd) — verdict funnel + conditional impl branch
- [`killer-recipe-flow.mmd`](killer-recipe-flow.mmd) — cross-engine triangulation topology
