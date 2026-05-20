# Tri-Engine Architecture Deliberation

Default flow for `/atlas multi`. Run Codex, Antigravity, and Claude Code in parallel via subagents to produce architectural assessments and ADR drafts, integrate results across two axes (concurrence + divergence), and deliver a **consensus ADR with explicit dissenting options** so the trade-off matrix becomes exhaustive rather than the single-engine narrow.

**Pattern type:** H (Hybrid — concurrence calibrates confidence, divergence enriches the Options section).

**Why three engines for architecture (different from Judge or Spark):** Judge optimizes for *agreement on a single defect* — concurrence is the quality signal. Spark optimizes for *creative recombination of existing data/logic* — divergence is the breakthrough. Atlas sits between the two: an ADR is a **decision document**, so concurrence on the *problem framing* and *forces at play* raises confidence, while divergence on the *recommended option* exposes architectural-style trade-offs that a single engine would silently flatten. Codex carries GitHub-heavy OSS architecture priors (layered, hexagonal, Spring/Rails canon), Antigravity carries Google-product priors (microservices, event-driven, scale-first), Claude carries Anthropic-curated priors (DDD, modular monolith, evolutionary architecture). Surfacing all three as named Options inside one ADR delivers a richer trade-off matrix than the canonical "1 recommendation + 2 strawman alternatives" template ever produces.

**Adapted from `_common/MULTI_ENGINE_RECIPE.md` Pattern H.** Re-uses PREFLIGHT, FAN-OUT, NORMALIZE, CLUSTER stages from `judge/references/tri-engine-review.md §2-3` and divergence-preserving SYNTHESIZE from `spark/references/tri-engine-proposal.md §8`. The differential below covers Atlas-specific schema, clustering, scoring, grounding, and merge rules.

---

## Flow

```
SCOPE → PREFLIGHT → FAN-OUT (parallel subagents) → NORMALIZE → CLUSTER → SCORE (confidence + perspective) → GROUND/CALIBRATE → SYNTHESIZE (consensus ADR + dissenting options) → PRESENT
```

PREFLIGHT and the engine availability matrix are identical to `_common/MULTI_ENGINE_RECIPE.md §PREFLIGHT`. Do not duplicate detection logic — call the canonical probe from Atlas main context.

---

## 1. SCOPE

Define the architecture target once. All three subagents share the same scope; differences come from training-data priors, not from prompt variation.

- System / module / boundary under analysis (with concrete file or package references when available)
- Architectural concern: greenfield design / structural bottleneck / debt remediation / modernization / boundary redesign
- Forces at play: scaling target, team topology, regulatory constraints, deployment surface, latency budget
- Existing artifacts: prior ADRs, current dependency graph, coupling metrics, fitness functions in place
- Constraint anchors: must-keep contracts, banned dependencies, language/runtime fences, headcount realities

---

## 2. FAN-OUT — parallel subagents

Spawn **three Agent calls in a single message** so they run concurrently. Each subagent has an independent context and produces an **architecture assessment + draft ADR option** independently.

| Subagent | Engine | Baseline command |
|----------|--------|------------------|
| `architect-codex` | Codex CLI | `codex exec --full-auto "<prompt>"` |
| `architect-agy` | Antigravity CLI | `agy -p "<prompt>" --dangerously-skip-permissions` |
| `architect-claude` | Claude Code CLI (subagent) | Agent tool with `subagent_type: general-purpose` |

**Loose prompt rule (per `_common/MULTI_ENGINE_RECIPE.md`):** pass only Role + Target + Output format. Do NOT pass MADR templates, ISO/IEC/IEEE 42010 framing, Vertical-Slice/Modular-Monolith defaults, or fitness-function lists — those defaults are Atlas-main-context conventions and applied at SYNTHESIZE. Letting each engine reach for its own architectural-style prior is the entire point of the recipe.

### Required JSON output schema

Every subagent returns one JSON object matching this exact schema (no commentary outside the JSON):

```json
{
  "engine": "codex|agy|claude",
  "architectural_smells": [
    {
      "smell": "Cyclic dependency between Auth and Billing modules",
      "evidence": "file/path or metric — Ca=12, Ce=9, instability I=0.43",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "concern_class": "coupling|cohesion|layering|boundary|complexity|scalability|reliability|evolvability"
    }
  ],
  "adr_options": [
    {
      "option_name": "Extract shared Identity module via Dependency Inversion",
      "architectural_style": "Layered | Hexagonal | DDD | Event-Driven | Modular-Monolith | Microservices | CQRS | Vertical-Slice | Pipeline | Plugin",
      "problem_statement": "Forces at play — what the decision must reconcile",
      "recommendation": "One-paragraph description of the proposed approach",
      "trade_offs": {
        "positive": ["consequence 1", "consequence 2"],
        "negative": ["consequence 1", "consequence 2"]
      },
      "risks": ["risk 1 with likelihood/impact", "risk 2"],
      "migration_strategy": "Strangler Fig phases | Branch-by-Abstraction | Big-bang justification | Incremental refactor sequence",
      "rollback_plan": "Concrete rollback step or feature-flag fallback",
      "fitness_function": "CI-integrated check that would detect regression (ArchUnit / dependency-cruiser / custom rule)",
      "effort_class": "S|M|L|XL",
      "reversibility": "TYPE-1 (one-way door) | TYPE-2 (reversible)"
    }
  ],
  "engine_notes": "Optional: which architectural-style priors this engine knows it brings (e.g., 'Codex GitHub-OSS lean toward Hexagonal+Spring conventions')"
}
```

Recommended per-engine output volume: 2-3 smells, 1-2 ADR options. Encourage focus — exhaustiveness comes from cross-engine union, not per-engine flood.

If an engine returns Markdown, ask its subagent to re-emit JSON before integrating. Engines genuinely unavailable per PREFLIGHT are dropped and noted; runtime errors are surfaced.

---

## 3. CLUSTER — Atlas identity rules

Atlas clusters two output streams separately because they merge differently downstream.

### 3a. Architectural-smell clustering (concurrence-primary)

Group `architectural_smells` from different engines that describe the same concern. Two smells match when **all three** hold:

- Same primary subject — same module, same boundary pair, same dependency cycle (file/package overlap, not necessarily identical names)
- Same `concern_class`
- Semantic overlap in the `smell` statement (e.g., "Auth ↔ Billing cycle" matches "circular import between authentication and billing" — same SCC, different wording)

Record the engine set per cluster. Smells benefit from concurrence (3/3 = high-confidence problem identification).

### 3b. ADR-option clustering — DIVERGENT BY DESIGN (critical Atlas rule)

**Do NOT merge options across engines just because they target the same problem.** Two options match for clustering only when **all three** hold:

- Same `architectural_style`
- Same primary intervention (e.g., both extract a shared module + apply DIP; both introduce an event bus)
- Same migration-strategy class (both Strangler Fig, both big-bang, both Branch-by-Abstraction)

If two engines target the same smell but propose **different architectural styles** (e.g., Codex says "extract shared Identity module" while Antigravity says "split into separate services via event bus"), they are **divergent options on the same problem** — keep both as separate clusters. This is the entire reason Atlas runs `multi`: a single engine would silently pick one style and lose the other as a trade-off lens. The Options section of the consensus ADR will preserve both.

Record per cluster:
- The engine set that proposed it
- Which smell-cluster(s) it addresses (link by cluster id)

---

## 4. SCORE — Pattern H (two axes)

Atlas uses both confidence and perspective axes from `_common/MULTI_ENGINE_RECIPE.md §Pattern H`.

### 4a. Smell scoring (confidence axis)

| Engines in cluster | Confidence label | Action |
|--------------------|------------------|--------|
| 3 / 3 | `CONFIRMED` | Ship as a confirmed problem in the ADR Context. Light grounding (read the cited evidence). |
| 2 / 3 | `LIKELY` | Ship with the dissenting engine's silence noted. Standard grounding. |
| 1 / 3 | `CANDIDATE` | Must pass strict grounding (step 5) to survive. May be a hallucinated smell. |

### 4b. Option scoring (perspective axis)

| Engines in cluster | Perspective label | Action |
|--------------------|-------------------|--------|
| 3 / 3 (same style + same intervention + same migration class) | `CONVERGENT` | Strong signal that this is the canonical answer. Promote to the **Recommended Option** position. |
| 2 / 3 | `CONVERGENT-PARTIAL` | Two engines agree; the dissenter's alternative goes into the Options section as a documented trade-off. |
| 1 / 3 | `DIVERGENT-{style}` | Single-engine option. Preserved in Options section as `Option-B` / `Option-C` so the ADR carries 2-3 styles instead of 1. NOT auto-low-value — the dissent is the value-add. |

**Critical Atlas rule:** Architectural style is reversibility-asymmetric. A `CONVERGENT` recommendation should still be paired with at least one `DIVERGENT` option in the ADR Options section, because architecture decisions are TYPE-1 (one-way door) more often than TYPE-2. Documenting the dissent in the ADR itself is what makes future supersession defensible.

---

## 5. GROUND or CALIBRATE — Atlas main context, never delegated

Read the actual code/system. Subagents can hallucinate modules, metrics, or dependencies — Atlas main context verifies before any option ships in the final ADR.

For every **smell cluster**:
1. **Existence check** — does the cited module / dependency / SCC actually exist in the repo? (Read tool against the cited path; or run a coupling probe.)
2. **Mitigation check** — is the smell already addressed by an existing ADR, fitness function, or recent refactor? If so, mark `REJECTED-MITIGATED` (do not waste the new ADR on a closed concern).
3. **Severity calibration** — re-rate severity against `architecture-health-metrics.md` thresholds; engines tend to inflate severity in greenfield/abstract scopes.
4. Mark `VERIFIED` / `LIKELY-VERIFIED` / `REJECTED-{reason}` / `NEEDS-INFO`.

For every **option cluster**:
1. **Feasibility check** — does the proposed style actually fit the existing constraints (language runtime, team topology, deployment surface)? An event-driven option in a synchronous-required low-latency context is `REJECTED-INFEASIBLE`.
2. **Reversibility check** — re-classify TYPE-1 / TYPE-2 against the actual blast radius (data migrations, public-API breaks → TYPE-1).
3. **Anti-pattern scan** — apply Atlas anti-patterns:
   - **Fairy Tale ADR** (only pros, no cons) — force trade-offs both ways
   - **Tunnel Vision ADR** (no downstream-consumer or ops perspective) — verify cross-cutting concerns are addressed
   - **Resume-Driven Development** — flag if the option imports a fashionable style without a force-at-play justification
   - **Distributed Monolith** trap — flag if microservices/event-driven options retain synchronous request-chains
4. Mark `VERIFIED` / `REJECTED-{reason}` / `NEEDS-TRADE-OFF` (option survives but trade-offs need Atlas-supplied augmentation).

For `CONFIRMED` smells and `CONVERGENT` options, perform a lightweight spot-check only — three engines rarely hallucinate the same module simultaneously, but they may all reach for the same trending architectural style without justification (the "everyone picked microservices" failure mode).

---

## 6. SYNTHESIZE — Consensus ADR + Dissenting Options

Atlas's distinctive merge: emit **one ADR document** structured as `Consensus core + Dissenting options as named alternatives`. This is richer than the canonical MADR 4.0 template's "Considered Options" because each Option section here is an entire engine's independently-reasoned recommendation, not a strawman written by the recommendation's author.

### Output document — extended MADR 4.0 structure

```markdown
---
status: Proposed
date: YYYY-MM-DD
deciders: [team or stakeholder list]
tri_engine:
  engines_run: [codex, agy, claude]
  engines_failed: [list or none]
  smell_confidence: CONFIRMED=N, LIKELY=N, VERIFIED-CANDIDATE=N
  option_perspective: CONVERGENT=N, CONVERGENT-PARTIAL=N, DIVERGENT=N
---

# ADR-NNNN: {Problem-named title}

## Context and Problem Statement
{Consensus framing — write from CONFIRMED + LIKELY-VERIFIED smells. Cite engine concurrence inline (e.g., "All three engines independently flagged the Auth ↔ Billing SCC [codex+agy+claude]").}

## Decision Drivers
{Forces at play — synthesized union across engines}

## Considered Options
1. **{Recommended option name}** — {one-line summary} `[CONVERGENT 3/3 codex+agy+claude]`
2. **{Dissenting option A name}** — {one-line summary} `[DIVERGENT-{style} codex-verified]`
3. **{Dissenting option B name}** — {one-line summary} `[DIVERGENT-{style} agy-verified]`

## Decision Outcome
Chosen option: **{Recommended option name}**, because {justification — reference the cross-engine convergence as one input, but the final rationale is Atlas's own reasoning over forces vs trade-offs}.

### Trade-off Matrix

| Criterion | Option 1 (Recommended) | Option 2 (Dissenting) | Option 3 (Dissenting) |
|-----------|------------------------|------------------------|------------------------|
| Coupling impact | … | … | … |
| Operational burden | … | … | … |
| Migration cost | … | … | … |
| Reversibility | TYPE-1/2 | TYPE-1/2 | TYPE-1/2 |
| Team-topology fit | … | … | … |
| Fitness-function coverage | … | … | … |

### Positive Consequences
{Union of Option 1's `trade_offs.positive` across engines}

### Negative Consequences
{Union of Option 1's `trade_offs.negative` across engines — plus any negatives Atlas main context discovered during grounding}

### Risks and Mitigations
{Per-risk; flag risks unique to the chosen option that the dissenting options would not have incurred — this is the cross-engine trade-off insight}

## Pros and Cons of Each Dissenting Option

### Option 2 — {Dissenting option A name} `[DIVERGENT-{style} {engine}-verified]`
- Architectural style: {style}
- Trade-offs / Risks / Migration / Reversibility
- **Why not chosen:** {explicit reason — what force did Option 1 weight more heavily}
- **Conditions under which this would be re-considered:** {trigger conditions for supersession}

### Option 3 — {Dissenting option B name} `[DIVERGENT-{style} {engine}-verified]`
{same structure}

## Migration Strategy
{Strangler Fig phases / Branch-by-Abstraction / Incremental — from the chosen option's `migration_strategy`}

## Rollback Plan
{From the chosen option's `rollback_plan`}

## Fitness Functions
{CI-integrated checks from the chosen option's `fitness_function`. Per Atlas core contract, every non-deprecated ADR maps to ≥1 fitness function.}

## Engine Concurrence Notes
- Smell coverage: {how many smells each engine surfaced; which were unique}
- Option diversity: {which architectural styles surfaced across engines and which didn't — explicit acknowledgement of what training-data common ground may have hidden}
- Rejected during grounding: {count by category — hallucinated module / already mitigated / infeasible / anti-pattern}
```

### Why "Consensus + Dissenting Options" beats "single-engine ADR"

A normal ADR's "Considered Options" section is written by the author of the recommendation, so the alternatives are strawmen — present to satisfy the "≥2 alternatives" rule, not to genuinely compete. Atlas `multi` replaces those strawmen with **three independently-reasoned options from non-overlapping training data**. The trade-off matrix becomes load-bearing instead of decorative, and future supersession ADRs can reference the rejected options directly rather than re-discovering them.

### Engine-attribution tag conventions

Every shipped Option and Smell carries a tag. Atlas Pattern H uses both concurrence and perspective tags:

| Engines in cluster | Tag (smell) | Tag (option) |
|--------------------|-------------|--------------|
| 3 / 3 | `[codex+agy+claude] [CONFIRMED]` | `[codex+agy+claude] [CONVERGENT]` |
| 2 / 3 | `[codex+agy] [LIKELY]` (etc.) | `[codex+claude] [CONVERGENT-PARTIAL]` (etc.) |
| 1 / 3 verified | `[codex-verified] [VERIFIED-CANDIDATE]` | `[agy-verified] [DIVERGENT-{style}]` |
| 1 / 3 rejected | (not shipped) | (not shipped) |

---

## 7. PRESENT

Default output: a single ADR file at `docs/architecture/decisions/ADR-NNNN-{slug}.md` matching the extended MADR structure above. If the user asked for an RFC instead, swap to the RFC template from `references/adr-rfc-templates.md` and keep the same Consensus + Dissenting Options spine.

Always include:
- Engine status header (which engines ran, which failed)
- Confidence + Perspective distributions
- Trade-off matrix (mandatory — this is the load-bearing artifact of `multi`)
- Rejection ledger (condensed, by category) — preserves SNR transparency
- Fitness-function spec for the chosen option
- Recommended next agent for handoff (Zen for refactor, Builder for implementation, Quill for ADR publishing, Sherpa for migration plan, Canvas for diagrams)

Do not include rejected smells/options in the main flow. Do not surface engine-raw output.

---

## Parallel Subagent Prompt Skeleton

Use the Agent tool three times **in the same message**. Each subagent prompt:

```
You are the {engine} architect subagent for Atlas.

# Role
Produce an architectural assessment and 1-2 draft ADR options for the target below. You are one of three engines working independently — do not try to be exhaustive across architectural styles; surface the option(s) your training data suggests as the strongest fit, and name the style explicitly. Other engines will surface other styles. Atlas main context will integrate.

# Target
- System / module under analysis: {scope}
- Architectural concern: {greenfield | bottleneck | debt | modernization | boundary redesign}
- Forces at play: {scaling, team topology, regulatory, latency, deployment surface}
- Existing artifacts: {prior ADRs, dependency-graph snippets, coupling metrics, fitness functions in place}
- Constraints: {must-keep contracts, banned deps, runtime fences, team realities}

# Output format
Return ONLY JSON matching this exact schema (no commentary outside the JSON):

{JSON schema from §2}

# Constraints
- Each ADR option must name a specific architectural_style (do not write style-agnostic recommendations)
- Each option must include both positive AND negative trade-offs (no Fairy Tale ADRs)
- Each option must include a migration_strategy and rollback_plan (no Sprint ADRs)
- Each option must classify reversibility (TYPE-1 vs TYPE-2)
- If you assert that a module / metric / dependency exists, name it specifically — do not invent
- Open with the deliverable (no completion preamble)
```

The three subagents return JSON; Atlas main context handles NORMALIZE through PRESENT.

---

## Degraded Modes

| Situation | Behavior |
|-----------|----------|
| 1 engine binary missing | Run the other two; note reduced architectural-style diversity; `DIVERGENT` options from the single surviving engine require stricter grounding |
| 2 engines fail | Single-engine ADR with reduced confidence and only one Option section; flag "tri-engine degraded — consider re-running" in front matter |
| All 3 fail | Abort `multi` flow; degrade to standard `adr` Recipe in Atlas main context |
| User explicitly requests single engine | Skip fan-out; use standard `adr` / `analyze` Recipe |
| Scope obviously trivial (e.g., "should this private helper be a class or function") | Skip multi; recommend `analyze` or `zen` instead |

---

## Why This Works for Architecture (Pattern H specifics)

- **Concurrence on smells calibrates the Context section.** When all three engines independently flag the same SCC or boundary leak, the ADR Context section can assert the problem without hedging — and future readers can audit the convergence.
- **Divergence on options enriches the Considered Options section.** Each engine's training-data prior surfaces a different architectural-style angle. Forcing all three into the same ADR makes the trade-off matrix exhaustive in a way the canonical MADR template cannot achieve solo.
- **The Consensus + Dissenting Options structure is supersession-friendly.** When the chosen option ages out, the next architect can revisit the dissenting options in the same document instead of re-discovering them from scratch — preserving the historical rationale that Atlas's ADR-immutability rule depends on.
- **Trade-off-matrix as load-bearing artifact.** In single-engine ADRs the matrix is often filled by the author's imagination of "what someone else might say." Here it's filled by what someone else *did* say, independently. The signal-to-noise ratio of trade-off content rises sharply.

---

## Cross-References

- `_common/MULTI_ENGINE_RECIPE.md` — base protocol; Pattern H details, PREFLIGHT, FAN-OUT mechanics, degraded modes
- `_common/SUBAGENT.md` — MULTI_ENGINE engine dispatch table, loose prompt rules
- `judge/references/tri-engine-review.md` — canonical Pattern C (concurrence-primary) implementation; PREFLIGHT logic mirrored here
- `spark/references/tri-engine-proposal.md` — canonical Pattern D (divergence-primary) implementation; divergence-preserving SYNTHESIZE adapted here
- `atlas/references/adr-rfc-templates.md` — MADR 4.0 base template that the Consensus + Dissenting Options structure extends
- `atlas/references/architecture-decision-anti-patterns.md` — Fairy Tale / Sprint / Mega / Tunnel-Vision ADR checks applied at GROUND
- `atlas/references/architecture-health-metrics.md` — thresholds used to calibrate smell severity during grounding
- `atlas/references/architecture-patterns.md` — style catalog (Layered / Hexagonal / DDD / Event-Driven / Modular-Monolith / Vertical-Slice / etc.) referenced when classifying option styles
