# Requirements Writing Anti-Patterns

Purpose: Use this file when a PRD or SRS is bloated, vague, strategically disconnected, or difficult to test.

Contents:

- `RW-01` to `RW-07`
- requirement quality foundations
- AI-era requirement traps
- Scribe quality gates

## `RW-01` to `RW-07`

| ID | Anti-Pattern | Risk | Prevention |
|----|--------------|------|------------|
| `RW-01` | Mistaking length for quality | Long PRDs hide the core ask. | Keep PRDs to `2-5 pages`; prioritize hypotheses and metrics. |
| `RW-02` | Missing non-goals | Scope creep and stakeholder mismatch | Make a `Non-Goals` section mandatory. |
| `RW-03` | Vague success criteria | No completion signal | Require KPI, target value, and measurement method. |
| `RW-04` | Over-specifying implementation | Removes engineering discretion | Keep PRD focused on `What` and `Why`; move `How` to design docs. |
| `RW-05` | Missing business context | Weak prioritization and poor tradeoffs | Add business context, hypothesis, and expected impact. |
| `RW-06` | Unedited AI expansion | Generic, repetitive, non-project-specific text | Treat AI output as draft only; require human review. |
| `RW-07` | Untestable requirements | No reliable acceptance decision | Add Given-When-Then acceptance criteria for every requirement. |

## Requirement Quality Foundations

Use these as a review grid:

- Commands and operations are explicit.
- Test strategy is named and scoped.
- Project structure and ownership are visible where relevant.
- Naming and error-handling expectations are stated when needed.
- Workflow and approval paths are clear.
- `Always / Ask first / Never` boundaries are explicit.

## AI-Era Requirement Traps

| Trap | Failure Mode | Guardrail |
|------|--------------|-----------|
| Instruction overload | Prompts over `300` lines degrade quality | Keep only the highest-priority rules. |
| Vibe coding without specs | Fast start, weak maintenance | Follow `Specify -> Plan -> Tasks -> Implement`. |
| Context overload | Token waste and weak focus | Load only the minimum structured context. |
| Human-review skip | Misses project-specific tacit knowledge | Require human review before finalization. |

## Modern PRD Quality Gates

- PRD length above `5 pages` -> compress.
- Missing `Non-Goals` -> add before finalization.
- Missing quantitative metrics -> add KPI, target, and measurement.
- Technical implementation detail inside PRD -> move to HLD or LLD.
- Missing business context -> request strategic framing.
- Unedited AI-generated text -> review and rewrite.
- Missing Given-When-Then -> add acceptance criteria.

## Scribe Usage

Use this file during:

- `UNDERSTAND` to screen `RW-01` to `RW-07`
- `STRUCTURE` to decide whether PRD or SRS is the right document
- `REVIEW` to reject vague or overgrown specs

Source:

- Addy Osmani, "The Best Way to Build AI Agent Specs"
- Aakash Gupta, "How to Write an Effective PRD in the AI Era"
