# AI-Assisted Documentation Anti-Patterns

Purpose: Use this file when AI-generated documentation is generic, over-instructed, structurally weak, or missing review discipline.

Contents:

- `AD-01` to `AD-07`
- Spec-Driven Development
- AI quality management
- context strategy

## `AD-01` to `AD-07`

| ID | Anti-Pattern | Risk | Prevention |
|----|--------------|------|------------|
| `AD-01` | Context overload | Redundant output, poor focus, high token cost | Load only structured minimum context. |
| `AD-02` | Skipping human review | Missed tacit knowledge and bad assumptions | Treat AI output as draft; require human review. |
| `AD-03` | Curse of instructions | Prompt quality degrades when rules are excessive | Keep prompts below the level where they become self-conflicting; prompts over `300` lines are a warning sign. |
| `AD-04` | Generic filler | Documentation lacks project specificity | Require project-specific examples and constraints. |
| `AD-05` | Template monoculture | The wrong structure for the reader or document type | Choose template by document type and audience. |
| `AD-06` | Implementation without specification | Hard-to-maintain code and hidden assumptions | Use Spec-Driven Development. |
| `AD-07` | No feedback loop | Same documentation failures repeat | Run INSCRIBE and update patterns. |

## Spec-Driven Development

Preferred sequence:

`SPECIFY -> PLAN -> TASKS -> IMPLEMENT`

Rules:

- Documentation comes before implementation when ambiguity is material.
- AI can draft any phase, but a human reviews before progression.
- Use Scribe for specification, Sherpa for breakdown, Builder for implementation.

## AI Quality Management

Require:

- explicit source inputs
- project-specific constraints
- audience declaration
- acceptance criteria and traceability
- human review before finalization

Reject:

- unedited AI output
- project-agnostic filler
- duplicated sections caused by broad context dumps

## Context Strategy

| Rule | Guidance |
|------|----------|
| Load only what is needed | Keep active context below `30%` of available budget when possible. |
| Prioritize hierarchy | main contract -> relevant template -> one targeted anti-pattern ref |
| Keep rules explicit | Do not hide critical thresholds in narrative prose. |
| Separate draft from approval | AI drafts; humans approve. |

## Scribe Usage

Use this file during:

- `UNDERSTAND` to choose context scope
- `DRAFT` to avoid generic filler
- `REVIEW` to enforce human quality gates
- `INSCRIBE` to improve future prompt and template choices
