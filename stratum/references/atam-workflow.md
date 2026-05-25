# ATAM Workflow Reference

Purpose: End-to-end SEI ATAM (Architecture Tradeoff Analysis Method, Kazman/Klein/Clements) workflow — from eliciting quality attribute scenarios through utility-tree prioritization to sensitivity/tradeoff/risk classification. Makes non-functional requirements testable as 6-part scenarios, structures them into a utility tree, then walks each architectural approach against the prioritized top-tier leaves to surface sensitivities, tradeoffs, and risks. Stratum produces the analysis artifact; the *decision* lives in an ADR.

## Scope Boundary

- **stratum `quality-attr`**: elicit, structure, and prioritize quality attribute scenarios; build utility trees; facilitate QAW. Produces scenario catalog + utility tree + prioritization matrix.
- **stratum `tradeoff`**: ATAM Phase 2 analysis on a *defined* architecture against *prioritized* scenarios. Produces sensitivity points, tradeoff points, risks, non-risks, and (with CBAM) cost-benefit ratios.
- **stratum `evaluate` (elsewhere)**: full ATAM/SAAM run including stakeholder workshops. `quality-attr` and `tradeoff` are the analysis core; `evaluate` is the wrapper process.
- **stratum `model` / `c4` / `dsl` (elsewhere)**: structural modeling. The model is the *subject* of analysis, not its output. Scenarios constrain the model but are not part of it.
- **stratum `adr` (elsewhere)**: decision recording. Analysis informs the ADR; the ADR captures the chosen path with its accepted downsides.
- **atlas (elsewhere)**: dependency analysis. Atlas surfaces structural tradeoffs (coupling vs cohesion); analysis here evaluates them against quality scenarios.
- **magi (elsewhere)**: multi-perspective deliberation when stakeholders disagree on which attribute to favor. ATAM produces *the matrix*; Magi *chooses* on contested points. Invoke Magi when the tradeoff has no analytical winner — values diverge.
- **accord (elsewhere)**: requirements package. Accord owns the broad NFR/FR catalog; ATAM produces the *architecturally significant* subset as 6-part scenarios. Tradeoffs may force requirement renegotiation; Accord folds the result back in.
- **scribe (elsewhere)**: document authoring. Scribe embeds the finalized scenario catalog and analysis report in HLD; it does not run elicitation or analysis.

## End-to-End Flow

```
PREP        →  identify stakeholders (PO, ops, security, domain, dev lead)
            →  pick QA categories in scope (performance, availability, security,
               modifiability, usability, testability, deployability, ...)

ELICIT      →  QAW workshop (4-6 hours): brainstorm raw scenarios per category
            →  stakeholders speak, facilitator captures; do not refine yet

REFINE      →  convert each raw scenario to 6-part form
               (source, stimulus, artifact, environment, response, response measure)
            →  drop ambiguity; every scenario must be testable in principle

TREE        →  build utility tree: Utility → QA category → refinement → scenario leaf
            →  each leaf scored (Importance × Difficulty), both H/M/L

PRIO        →  sort by (H,H) > (H,M) > (M,H) > ... ; top tier becomes ATAM input

──────────────────────────────────────────────────────────────────────────────
                      ATAM Phase 2 Core (tradeoff)
──────────────────────────────────────────────────────────────────────────────

ENUMERATE   →  list architectural approaches per quality attribute (e.g.,
               "active-active replication" for availability, "CQRS" for performance)

ANALYZE     →  for each (approach × scenario) pair, walk through:
               - effect on the scenario's response measure
               - confidence level (high/medium/low)

CLASSIFY    →  per decision/parameter, label as:
               - SENSITIVITY POINT: heavily affects ONE quality attribute
               - TRADEOFF POINT:    heavily affects TWO+ in conflicting directions
               - RISK:              decision whose consequence is unknown or bad
               - NON-RISK:          decision whose consequence is known and good

(CBAM)      →  optional: estimate cost(approach) and benefit(scenario satisfied)
            →  rank by benefit-to-cost ratio (ROI proxy)

REPORT      →  table of sensitivities/tradeoffs/risks; rationale captured per
               decision; hand off to `adr` for decisions to record, Magi for
               contested ones, Scribe for HLD inclusion
```

---

## Part 1: Quality Attribute Scenarios

Make non-functional requirements testable by expressing them as SEI 6-part scenarios. Vague goals like "the system shall be performant" become falsifiable: under load X, response Y must hold. Scenarios serve as the leaf nodes of a utility tree to drive ATAM evaluation and as acceptance criteria for architectural decisions.

### 6-Part Scenario Template (SEI / Bass-Clements-Kazman)

| Part | Question | Example (Performance) |
|------|----------|------------------------|
| Source | Who/what triggers? | External user via web client |
| Stimulus | What event arrives? | Burst of 1,000 requests/sec |
| Artifact | What part of the system? | Order API gateway |
| Environment | Under what conditions? | Black-Friday peak load, normal infra |
| Response | How does the system react? | Requests processed, queue drained |
| Response Measure | Quantified success criterion | p99 latency ≤ 300 ms; 0 dropped requests |

A scenario without all six parts is incomplete and not ATAM-ready. The Response Measure is the testable bar — without it, the scenario degrades to a wish.

### QA Category Cheat Sheet

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

### Utility Tree Structure

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

Rules: leaves are 6-part scenarios. Internal nodes are *refinements*, not scenarios. Each leaf carries `(Importance, Difficulty)` ∈ {H,M,L}². The tree is a deliverable — Stratum hands it to `tradeoff` for ATAM Phase 2.

### QAW (Quality Attribute Workshop) Facilitation

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

### Prioritization: Importance × Difficulty Matrix

| | Difficulty L | Difficulty M | Difficulty H |
|--|--|--|--|
| **Importance H** | (H,L) — quick win | (H,M) — schedule early | **(H,H) — top tier, ATAM core** |
| **Importance M** | (M,L) — opportunistic | (M,M) — backlog | (M,H) — defer or descope |
| **Importance L** | (L,*) — drop or footnote | drop | drop |

ATAM analyzes the (H,H) and (H,M) leaves. The (M,H) cell is the danger zone — moderately important and hard. Surface explicitly as a tradeoff candidate; do not leave silent.

### Anti-Patterns (Scenarios)

- Vague response measures ("system shall be fast") — defeats the testability promise. Demand units and thresholds: ms, %, count, or person-days.
- Conflating stimulus and response — "system experiences high load and responds slowly" is one half-formed scenario, not a 6-part one. Separate cause and effect.
- Architect-led elicitation — architects propose scenarios that fit their planned solution; stakeholder bias is lost. Facilitator must be neutral; architect listens.
- Utility tree as a flat list — flattening to a 1-level list loses the QA category structure that drives breadth coverage. Always stratify by category.
- Skipping prioritization — treating all scenarios equally inflates ATAM scope from days to weeks and dilutes findings. Score every leaf.
- Missing Environment part — "p99 latency ≤ 300ms" without "under what load / failure / config" is unfalsifiable. Environment is the most-skipped of the six.
- Performance-only catalog — eliciting performance scenarios because they're easy, ignoring modifiability/security. Bass et al. note modifiability is usually the most strategic and most omitted category.
- One-shot QAW — single workshop captures the loud voices; quiet domain experts lose. Run ≥1 follow-up to add late scenarios.
- Treating scenarios as static — scenarios drift as business goals shift. Re-validate top-tier scenarios at each major release; archive obsoleted ones with rationale.

---

## Part 2: Tradeoff Analysis (ATAM Phase 2)

Surface architectural tradeoffs, sensitivities, and risks. For each architectural approach, identify which quality attributes it improves, which it harms, which decision points dominate one attribute (sensitivity), and which dominate multiple in conflicting directions (tradeoff). CBAM extends ATAM with cost-benefit quantification when budget allocation is the question.

### Concept Definitions

| Term | Meaning | Example |
|------|---------|---------|
| Architectural approach | Pattern/tactic applied to address a QA | Active-active replication; CQRS; bulkhead |
| Sensitivity point | Decision/parameter where a small change strongly moves *one* QA | Replication lag threshold ↔ availability |
| Tradeoff point | Sensitivity for *two or more* QAs, in conflict | Replication sync mode ↔ availability ⇅ performance |
| Risk | Decision whose effect is unknown, unmeasured, or known-bad | "We use eventual consistency but no bound on lag" |
| Non-risk | Decision validated against scenarios with confidence | "JWT 15-min expiry; meets security S-3, no perf impact" |

A decision is *not* a tradeoff just because it has cost. Tradeoff = conflicting directional effect on ≥2 QAs at the same decision lever.

### ATAM Phases (Full Method, for Context)

| Phase | Step | Output |
|-------|------|--------|
| 1. Presentation | Present method, business drivers, architecture | Shared context |
| 2. Investigation | **Identify approaches → utility tree → analyze approaches** | Sensitivities, tradeoffs, risks, non-risks |
| 3. Testing | Brainstorm scenarios, prioritize, re-analyze | Refined risk list |
| 4. Reporting | Present results | Findings, risk themes, recommendations |

`tradeoff` recipe owns the bolded Phase 2 core. `evaluate` runs the full four phases.

### Sensitivity / Tradeoff / Risk Capture Format

```yaml
decision: "replication-mode = synchronous | asynchronous"
approach: "active-active database replication"
scenarios_touched:
  - id: AVAIL-2 (single-AZ failure, recovery ≤ 60s)
    effect: synchronous improves; asynchronous risks data loss
  - id: PERF-1 (p99 latency ≤ 300ms under 1k rps)
    effect: synchronous degrades p99 by ~30-80ms; asynchronous neutral
classification: TRADEOFF POINT      # affects 2 QAs in conflict
sensitivity_for: [availability, performance]
risks:
  - "If async chosen, no documented bound on replication lag (R-7)"
non_risks:
  - "Read scaling unaffected by mode (validated)"
rationale: "Chose async + 200ms lag SLA + monitored alert; aligns with PERF-1
            primacy at peak; AVAIL-2 met via failover with bounded data loss
            window accepted in ADR-0042."
confidence: medium  # depends on lag bound holding under load
```

Every classified item must carry rationale. A tradeoff point without rationale is a deferred decision, not an analysis result.

### CBAM Extension (Cost-Benefit Analysis Method)

When the question is *which approaches to fund*, extend ATAM with cost and benefit estimation:

| Step | Action |
|------|--------|
| 1 | For each scenario, define a utility curve: response-measure value → utility (0-100). Anchor at worst-current and best-desired. |
| 2 | For each approach, estimate the response-measure improvement → utility gain per scenario. |
| 3 | Sum utility across scenarios weighted by scenario importance. |
| 4 | Estimate approach cost (engineering, infra, opportunity). |
| 5 | Compute benefit/cost ratio; rank approaches; choose under budget constraint. |

CBAM works when scenarios have measurable response measures and stakeholders can agree on utility anchors. Skip CBAM when scenarios are qualitative (security posture, ergonomics) — the precision is illusory.

### Decision Rationale Capture

Every classified tradeoff/sensitivity must be paired with:

| Field | Purpose |
|-------|---------|
| Chosen position on the lever | What value/option was picked |
| Alternatives rejected | What else was on the table |
| Why this position | Forces that dominated (refer to scenario IDs) |
| Accepted downsides | What we knowingly gave up |
| Reversal cost | Estimated effort if we change later |
| Owning ADR | Link to the ADR that records the decision |

Rationale capture is the bridge from analysis to ADR. Without it, the analysis is an academic artifact; with it, future readers can reconstruct *why this lever sits where it does*.

### When to Invoke `tradeoff` vs Magi

| Situation | Invoke |
|-----------|--------|
| Architectural approach defined; quantitative scenarios; need analytical surfacing | **Stratum `tradeoff`** |
| Multiple approaches; cost is the question; utility curves estimable | **Stratum `tradeoff`** + CBAM |
| Stakeholders disagree on which QA to prioritize (values conflict, no analytical winner) | **Magi** |
| Decision is known but rationale must be recorded | **Stratum `adr`** |
| Scenarios not yet elicited or prioritized | **Stratum `quality-attr`** first |
| Full evaluation including workshops and presentation | **Stratum `evaluate`** |

`tradeoff` is *analytical surfacing*. Magi is *value deliberation*. They compose: surface with `tradeoff`, deliberate contested points with Magi, record outcome with `adr`.

### Anti-Patterns (Tradeoff Analysis)

- Calling every cost a tradeoff — cost is not conflict. Tradeoff requires opposing directional effects on ≥2 QAs at one lever.
- Sensitivity without measurement — claiming a parameter is "sensitive" without a response-measure delta. Sensitivity is quantitative; without numbers, it is opinion.
- Risk lists without rationale — "risk: we use Kafka." A risk is a *decision with bad/unknown consequence under the scenarios*. Name the scenario it threatens.
- CBAM with invented utilities — assigning 0-100 utility scores without anchors or stakeholder calibration. The numbers acquire false authority. Either anchor rigorously or stay qualitative.
- Analysis without ADR handoff — surfaced tradeoffs that never get recorded as decisions decay into tribal knowledge within months.
- Single-approach analysis — comparing one approach to nothing yields no tradeoff. Always enumerate ≥2 approaches per attribute, even if one is the straw-man status quo.
- Classifying every decision — most decisions are non-risks. Forcing every parameter into sensitivity/tradeoff/risk dilutes signal. Highlight only the architecturally significant levers.
- Skipping confidence — "high confidence" claims without evidence (load test, prior art, calculation). Mark medium/low when grounding is thin; reviewers learn where to probe.
- Conflating tradeoff with stakeholder disagreement — if the conflict is between *quality attributes*, it's a tradeoff (analyze with `tradeoff`). If it's between *people about which QA to favor*, it's deliberation (Magi).

---

## Handoff

**From `quality-attr` (within ATAM workflow):**
- **To Stratum `tradeoff`**: top-tier (H,H)/(H,M) scenarios as ATAM Phase 2 utility tree input. Scenario pairs with conflicting forces (e.g., performance vs security) for sensitivity/tradeoff identification.

**From `tradeoff`:**
- **To Stratum `adr`**: each classified tradeoff/sensitivity with rationale captured → one ADR per architecturally significant decision. Also: scenarios that drove an architectural decision — cite as Decision Driver in MADR.
- **To Stratum `quality-attr`**: scenarios revealed as missing or underspecified during analysis — round-trip for refinement.
- **To Stratum `evaluate`**: when full ATAM Phase 1/3/4 wrapper is needed (presentation, scenario brainstorm round 2, reporting).

**From either phase (external handoff):**
- **To Magi**: scenario pairs that cannot both be fully satisfied / contested tradeoff points where the analysis surfaces conflict but stakeholders disagree on which QA to favor — escalate for multi-perspective tradeoff deliberation.
- **To Accord**: finalized scenario catalog merged into the NFR section of the requirements package. Tradeoffs that force requirement renegotiation (e.g., "p99 ≤ 300ms unachievable under current budget").
- **To Scribe**: scenario catalog + utility tree for embedding into HLD's "Architecturally Significant Requirements" section. Tradeoff/sensitivity/risk tables for embedding in HLD's "Architectural Decisions and Tradeoffs" section.
- **To Atlas**: modifiability scenarios that constrain dependency structure (e.g., "add payment provider in 5 days" → loose coupling target). Structural tradeoffs (coupling vs cohesion, layered vs hexagonal) — Atlas validates against dependency reality.
