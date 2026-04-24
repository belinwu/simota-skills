# Tradeoff Analysis Reference

Purpose: Surface architectural tradeoffs, sensitivities, and risks using the SEI ATAM (Architecture Tradeoff Analysis Method, Kazman/Klein/Clements). For each architectural approach, identify which quality attributes it improves, which it harms, which decision points dominate one attribute (sensitivity), and which dominate multiple in conflicting directions (tradeoff). CBAM extends ATAM with cost-benefit quantification when budget allocation is the question. Stratum produces the analysis artifact; the *decision* lives in an ADR.

## Scope Boundary

- **stratum `tradeoff`**: ATAM-style analysis on a *defined* architecture against *prioritized* scenarios. Produces sensitivity points, tradeoff points, risks, non-risks, and (with CBAM) cost-benefit ratios.
- **stratum `evaluate` (elsewhere)**: full ATAM/SAAM run including stakeholder workshops. `tradeoff` is the analysis core; `evaluate` is the wrapper process.
- **stratum `quality-attr` (elsewhere)**: scenario elicitation. `tradeoff` consumes the prioritized utility tree; it does not build it.
- **stratum `model` / `c4` / `dsl` (elsewhere)**: structural modeling. The model is the *subject* of tradeoff analysis, not its output.
- **stratum `adr` (elsewhere)**: decision recording. Tradeoff analysis informs the ADR; the ADR captures the chosen path with its accepted downsides.
- **atlas (elsewhere)**: dependency analysis. Atlas surfaces structural tradeoffs (coupling vs cohesion); `tradeoff` evaluates them against quality scenarios.
- **magi (elsewhere)**: multi-perspective deliberation when stakeholders disagree on which attribute to favor. `tradeoff` produces *the matrix*; Magi *chooses* on contested points. Invoke Magi when the tradeoff has no analytical winner — values diverge.
- **accord (elsewhere)**: requirements. Tradeoffs may force requirement renegotiation; Accord folds the result back in.
- **scribe (elsewhere)**: document authoring. Scribe embeds the analysis report into HLD; it does not run the analysis.

## Workflow (ATAM Phase 2 Core)

```
INPUT    →  defined architectural approach(es) + prioritized scenarios
            (utility tree top-tier from `quality-attr`)

ENUMERATE →  list architectural approaches per quality attribute (e.g.,
             "active-active replication" for availability, "CQRS" for performance)

ANALYZE  →  for each (approach × scenario) pair, walk through:
            - effect on the scenario's response measure
            - confidence level (high/medium/low)

CLASSIFY →  per decision/parameter, label as:
            - SENSITIVITY POINT: heavily affects ONE quality attribute
            - TRADEOFF POINT:    heavily affects TWO+ in conflicting directions
            - RISK:              decision whose consequence is unknown or bad
            - NON-RISK:          decision whose consequence is known and good

(CBAM)   →  optional: estimate cost(approach) and benefit(scenario satisfied)
          →  rank by benefit-to-cost ratio (ROI proxy)

REPORT   →  table of sensitivities/tradeoffs/risks; rationale captured per
            decision; hand off to `adr` for decisions to record, Magi for
            contested ones, Scribe for HLD inclusion
```

## Concept Definitions

| Term | Meaning | Example |
|------|---------|---------|
| Architectural approach | Pattern/tactic applied to address a QA | Active-active replication; CQRS; bulkhead |
| Sensitivity point | Decision/parameter where a small change strongly moves *one* QA | Replication lag threshold ↔ availability |
| Tradeoff point | Sensitivity for *two or more* QAs, in conflict | Replication sync mode ↔ availability ⇅ performance |
| Risk | Decision whose effect is unknown, unmeasured, or known-bad | "We use eventual consistency but no bound on lag" |
| Non-risk | Decision validated against scenarios with confidence | "JWT 15-min expiry; meets security S-3, no perf impact" |

A decision is *not* a tradeoff just because it has cost. Tradeoff = conflicting directional effect on ≥2 QAs at the same decision lever.

## ATAM Phases (full method, for context)

| Phase | Step | Output |
|-------|------|--------|
| 1. Presentation | Present method, business drivers, architecture | Shared context |
| 2. Investigation | **Identify approaches → utility tree → analyze approaches** | Sensitivities, tradeoffs, risks, non-risks |
| 3. Testing | Brainstorm scenarios, prioritize, re-analyze | Refined risk list |
| 4. Reporting | Present results | Findings, risk themes, recommendations |

`tradeoff` recipe owns the bolded Phase 2 core. `evaluate` runs the full four phases.

## Sensitivity / Tradeoff / Risk Capture Format

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

## CBAM Extension (Cost-Benefit Analysis Method)

When the question is *which approaches to fund*, extend ATAM with cost and benefit estimation:

| Step | Action |
|------|--------|
| 1 | For each scenario, define a utility curve: response-measure value → utility (0-100). Anchor at worst-current and best-desired. |
| 2 | For each approach, estimate the response-measure improvement → utility gain per scenario. |
| 3 | Sum utility across scenarios weighted by scenario importance. |
| 4 | Estimate approach cost (engineering, infra, opportunity). |
| 5 | Compute benefit/cost ratio; rank approaches; choose under budget constraint. |

CBAM works when scenarios have measurable response measures and stakeholders can agree on utility anchors. Skip CBAM when scenarios are qualitative (security posture, ergonomics) — the precision is illusory.

## Decision Rationale Capture

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

## When to Invoke `tradeoff` vs Magi

| Situation | Invoke |
|-----------|--------|
| Architectural approach defined; quantitative scenarios; need analytical surfacing | **Stratum `tradeoff`** |
| Multiple approaches; cost is the question; utility curves estimable | **Stratum `tradeoff`** + CBAM |
| Stakeholders disagree on which QA to prioritize (values conflict, no analytical winner) | **Magi** |
| Decision is known but rationale must be recorded | **Stratum `adr`** |
| Scenarios not yet elicited or prioritized | **Stratum `quality-attr`** first |
| Full evaluation including workshops and presentation | **Stratum `evaluate`** |

`tradeoff` is *analytical surfacing*. Magi is *value deliberation*. They compose: surface with `tradeoff`, deliberate contested points with Magi, record outcome with `adr`.

## Anti-Patterns

- Calling every cost a tradeoff — cost is not conflict. Tradeoff requires opposing directional effects on ≥2 QAs at one lever.
- Sensitivity without measurement — claiming a parameter is "sensitive" without a response-measure delta. Sensitivity is quantitative; without numbers, it is opinion.
- Risk lists without rationale — "risk: we use Kafka." A risk is a *decision with bad/unknown consequence under the scenarios*. Name the scenario it threatens.
- CBAM with invented utilities — assigning 0-100 utility scores without anchors or stakeholder calibration. The numbers acquire false authority. Either anchor rigorously or stay qualitative.
- Analysis without ADR handoff — surfaced tradeoffs that never get recorded as decisions decay into tribal knowledge within months.
- Single-approach analysis — comparing one approach to nothing yields no tradeoff. Always enumerate ≥2 approaches per attribute, even if one is the straw-man status quo.
- Classifying every decision — most decisions are non-risks. Forcing every parameter into sensitivity/tradeoff/risk dilutes signal. Highlight only the architecturally significant levers.
- Skipping confidence — "high confidence" claims without evidence (load test, prior art, calculation). Mark medium/low when grounding is thin; reviewers learn where to probe.
- Conflating tradeoff with stakeholder disagreement — if the conflict is between *quality attributes*, it's a tradeoff (analyze with `tradeoff`). If it's between *people about which QA to favor*, it's deliberation (Magi).

## Handoff

- **To Stratum `adr`**: each classified tradeoff/sensitivity with rationale captured → one ADR per architecturally significant decision.
- **To Magi**: contested tradeoff points where the analysis surfaces conflict but stakeholders disagree on which QA to favor.
- **To Stratum `quality-attr`**: scenarios revealed as missing or underspecified during analysis — round-trip for refinement.
- **To Stratum `evaluate`**: when full ATAM Phase 1/3/4 wrapper is needed (presentation, scenario brainstorm round 2, reporting).
- **To Atlas**: structural tradeoffs (coupling vs cohesion, layered vs hexagonal) — Atlas validates against dependency reality.
- **To Accord**: tradeoffs that force requirement renegotiation (e.g., "p99 ≤ 300ms unachievable under current budget").
- **To Scribe**: tradeoff/sensitivity/risk tables for embedding in HLD's "Architectural Decisions and Tradeoffs" section.
