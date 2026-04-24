# Quality Attribute Scenarios Reference

Purpose: Make non-functional requirements testable by expressing them as SEI 6-part scenarios (source, stimulus, artifact, environment, response, response measure). Vague goals like "the system shall be performant" become falsifiable: under load X, response Y must hold. Stratum uses scenarios as the leaf nodes of a utility tree to drive ATAM evaluation and as acceptance criteria for architectural decisions.

## Scope Boundary

- **stratum `quality-attr`**: elicit, structure, and prioritize quality attribute scenarios; build utility trees; facilitate QAW. Produces scenario catalog + utility tree + prioritization matrix.
- **stratum `evaluate` (elsewhere)**: ATAM/SAAM execution. `quality-attr` produces the *input* utility tree; `evaluate` runs the analysis.
- **stratum `tradeoff` (elsewhere)**: tradeoff/sensitivity/risk identification. Scenarios feed `tradeoff`; this recipe does not analyze them.
- **stratum `model` / `c4` / `dsl` (elsewhere)**: structural modeling. Scenarios constrain the model but are not part of it.
- **atlas (elsewhere)**: dependency analysis. Quality scenarios may target dependency structure (e.g., modifiability), but Atlas does not author scenarios.
- **magi (elsewhere)**: tradeoff deliberation between competing scenarios. `quality-attr` lists; Magi arbitrates.
- **accord (elsewhere)**: requirements package. Accord owns the broad NFR/FR catalog; `quality-attr` produces the *architecturally significant* subset as 6-part scenarios.
- **scribe (elsewhere)**: document authoring. Scribe embeds the finalized scenario catalog in HLD; it does not run elicitation.

## Workflow

```
PREP     →  identify stakeholders (PO, ops, security, domain, dev lead)
         →  pick QA categories in scope (performance, availability, security,
            modifiability, usability, testability, deployability, ...)

ELICIT   →  QAW workshop (4-6 hours): brainstorm raw scenarios per category
         →  stakeholders speak, facilitator captures; do not refine yet

REFINE   →  convert each raw scenario to 6-part form
            (source, stimulus, artifact, environment, response, response measure)
         →  drop ambiguity; every scenario must be testable in principle

TREE     →  build utility tree: Utility → QA category → refinement → scenario leaf
         →  each leaf scored (Importance × Difficulty), both H/M/L

PRIO     →  sort by (H,H) > (H,M) > (M,H) > ... ; top tier becomes ATAM input
         →  hand off prioritized leaves to `evaluate` / `tradeoff`
```

## 6-Part Scenario Template (SEI / Bass-Clements-Kazman)

| Part | Question | Example (Performance) |
|------|----------|------------------------|
| Source | Who/what triggers? | External user via web client |
| Stimulus | What event arrives? | Burst of 1,000 requests/sec |
| Artifact | What part of the system? | Order API gateway |
| Environment | Under what conditions? | Black-Friday peak load, normal infra |
| Response | How does the system react? | Requests processed, queue drained |
| Response Measure | Quantified success criterion | p99 latency ≤ 300 ms; 0 dropped requests |

A scenario without all six parts is incomplete and not ATAM-ready. The Response Measure is the testable bar — without it, the scenario degrades to a wish.

## QA Category Cheat Sheet

| Category | Typical stimulus | Typical measure |
|----------|------------------|------------------|
| Performance | Request burst, batch job arrival | Latency p50/p99, throughput, deadline miss rate |
| Availability | Component failure, network partition | Uptime %, MTTR, MTBF, recovery time |
| Security | Auth attempt, malicious payload | Time to detect, % attacks blocked, audit completeness |
| Modifiability | Change request, new feature | Person-days to change, # modules touched, regression count |
| Usability | User goal pursuit | Task completion rate, time-on-task, error count |
| Testability | New code committed | % branch coverage, time to test failure isolation |
| Deployability | Release event | Deployment frequency, lead time, rollback time |
| Interoperability | Integration request | # integrations supported, time to add one |

## Utility Tree Structure

```
Utility (root)
├── Performance
│   ├── Data Latency
│   │   ├── [H,M] Order p99 ≤ 300ms under 1k rps          ← scenario leaf
│   │   └── [M,L] Reporting query ≤ 5s under nominal load
│   └── Transaction Throughput
│       └── [H,H] Sustained 5k orders/min for 1h          ← top-tier leaf
├── Availability
│   ├── Hardware Failure
│   │   └── [H,H] Single AZ loss, recovery ≤ 60s          ← top-tier leaf
│   └── Software Failure
│       └── [M,M] Non-critical service crash, ≤ 0 user impact
├── Modifiability
│   └── New Payment Method
│       └── [H,M] Add provider in ≤ 5 person-days, 0 regressions
└── Security
    └── Credential Theft
        └── [H,H] Detect anomalous login ≤ 5 min          ← top-tier leaf
```

Rules: leaves are 6-part scenarios. Internal nodes are *refinements*, not scenarios. Each leaf carries `(Importance, Difficulty)` ∈ {H,M,L}². The tree is a deliverable — Stratum hands it to `evaluate` for ATAM Phase 2.

## QAW (Quality Attribute Workshop) Facilitation

| Step | Time | Output |
|------|------|--------|
| 1. Business goals briefing | 30 min | Shared mission/driver list |
| 2. Architectural plan presentation | 30 min | Proposed approach (or "TBD" early) |
| 3. Stakeholder identification | 15 min | Roles in room and missing |
| 4. Architectural driver brainstorm | 45 min | Raw drivers (cards on wall) |
| 5. Scenario brainstorm (round-robin) | 60 min | Raw scenarios, 1 per card |
| 6. Scenario consolidation | 45 min | Deduped, gap-filled list |
| 7. Scenario prioritization (vote) | 30 min | Each stakeholder gets N votes |
| 8. Scenario refinement to 6-part | 60 min | Top-tier scenarios formalized |

Run with 5-10 stakeholders. Smaller misses perspectives; larger fragments. The facilitator must *not* be the architect — observer role keeps the room from defending one approach.

## Prioritization: Importance × Difficulty Matrix

| | Difficulty L | Difficulty M | Difficulty H |
|--|--|--|--|
| **Importance H** | (H,L) — quick win | (H,M) — schedule early | **(H,H) — top tier, ATAM core** |
| **Importance M** | (M,L) — opportunistic | (M,M) — backlog | (M,H) — defer or descope |
| **Importance L** | (L,*) — drop or footnote | drop | drop |

ATAM analyzes the (H,H) and (H,M) leaves. The (M,H) cell is the danger zone — moderately important and hard. Surface explicitly as a tradeoff candidate; do not leave silent.

## Anti-Patterns

- Vague response measures ("system shall be fast") — defeats the testability promise. Demand units and thresholds: ms, %, count, or person-days.
- Conflating stimulus and response — "system experiences high load and responds slowly" is one half-formed scenario, not a 6-part one. Separate cause and effect.
- Architect-led elicitation — architects propose scenarios that fit their planned solution; stakeholder bias is lost. Facilitator must be neutral; architect listens.
- Utility tree as a flat list — flattening to a 1-level list loses the QA category structure that drives breadth coverage. Always stratify by category.
- Skipping prioritization — treating all scenarios equally inflates ATAM scope from days to weeks and dilutes findings. Score every leaf.
- Missing Environment part — "p99 latency ≤ 300ms" without "under what load / failure / config" is unfalsifiable. Environment is the most-skipped of the six.
- Performance-only catalog — eliciting performance scenarios because they're easy, ignoring modifiability/security. Bass et al. note modifiability is usually the most strategic and most omitted category.
- One-shot QAW — single workshop captures the loud voices; quiet domain experts lose. Run ≥1 follow-up to add late scenarios.
- Treating scenarios as static — scenarios drift as business goals shift. Re-validate top-tier scenarios at each major release; archive obsoleted ones with rationale.

## Handoff

- **To Stratum `evaluate`**: top-tier (H,H)/(H,M) scenarios as ATAM Phase 2 utility tree input.
- **To Stratum `tradeoff`**: scenario pairs with conflicting forces (e.g., performance vs security) for sensitivity/tradeoff identification.
- **To Stratum `adr`**: scenarios that drove an architectural decision — cite as Decision Driver in MADR.
- **To Magi**: scenario pairs that cannot both be fully satisfied — escalate for multi-perspective tradeoff deliberation.
- **To Accord**: finalized scenario catalog merged into the NFR section of the requirements package.
- **To Scribe**: scenario catalog + utility tree for embedding into HLD's "Architecturally Significant Requirements" section.
- **To Atlas**: modifiability scenarios that constrain dependency structure (e.g., "add payment provider in 5 days" → loose coupling target).
