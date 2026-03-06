# Design Document Anti-Patterns

Purpose: Use this file when HLD or LLD drafts are structurally weak, disconnected from requirements, or mismatched to the intended audience.

Contents:

- HLD anti-patterns `HD-01` to `HD-07`
- LLD anti-patterns `LD-01` to `LD-06`
- mandatory sections
- quality metrics and Scribe gates

## HLD Anti-Patterns

| ID | Anti-Pattern | Risk | Prevention |
|----|--------------|------|------------|
| `HD-01` | Skipping requirements | Design drifts from actual needs | Enforce `Requirements -> HLD -> LLD` order. |
| `HD-02` | Over-engineering | Complexity and delay | Design only for current requirements plus clear extension points. |
| `HD-03` | Ignoring scalability | Late architectural rewrites | Add measurable NFRs early. |
| `HD-04` | Undefined component relationships | Hidden coupling and unstable boundaries | Define interfaces and dependency diagrams. |
| `HD-05` | Security as an afterthought | Expensive late fixes | Include threat modeling in HLD. |
| `HD-06` | Low document quality | Misinterpretation by implementers | Require diagrams, updates, and review. |
| `HD-07` | Audience mismatch | The document is not usable for decisions | State audience and tune detail to that audience. |

## LLD Anti-Patterns

| ID | Anti-Pattern | Risk | Prevention |
|----|--------------|------|------------|
| `LD-01` | Ignoring SOLID | God classes and brittle changes | Apply SOLID checks during design. |
| `LD-02` | Re-inventing patterns | Inconsistent implementation | Select known patterns and record why. |
| `LD-03` | Unclear code shape | Implementers misread intent | Use naming rules, examples, and sequence diagrams. |
| `LD-04` | Missing test strategy | Hard-to-test implementations | Add unit, integration, and E2E strategy. |
| `LD-05` | Excessive implementation detail | The document becomes stale code shadow | Focus on decisions, contracts, and flows. |
| `LD-06` | Breaking from HLD | Architectural drift and debt | Preserve HLD-to-LLD traceability. |

## Mandatory Sections

### HLD

- system overview, scope, and audience
- architecture and component interactions
- technology choices with alternatives and tradeoffs
- measurable NFRs
- deployment and environment model

### LLD

- module or class design
- sequence and error flows
- data design and access patterns
- test strategy
- traceability back to HLD decisions

## Quantitative Signals

- PMI reports `39%` of project failure is tied to weak requirements or design.
- Missing design review can increase downstream cost by `10-100x`.

Use these as pressure, not decoration. If the draft lacks traceability, NFRs, diagrams, or explicit interfaces, revise before handoff.

## Scribe Quality Gates

- No requirements document -> block HLD and request requirements first.
- Missing NFR section -> add before review passes.
- Undefined interfaces -> add before handoff.
- Missing audience -> add before finalization.
- No HLD reference in LLD -> add traceability.
- No design review or update path -> mark incomplete.

Source:

- Coudo AI, "HLD and LLD - Best Practices for Better Software Design"
- PMI, "Pulse of the Profession - Requirements Management"
