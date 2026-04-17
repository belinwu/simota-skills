# Figma Make Constraints

Purpose: Use this reference when Loom must reason about current Figma Make limits, reliability tradeoffs, or package-aware generation rules.

## Contents
- Stable constraints
- Reliability limits
- Prompt packaging rules
- Design-system package rules
- Guardrail checklist

## Stable Constraints

Treat these as conservative operating assumptions:

| Constraint | Why it matters | Loom response |
|---|---|---|
| `React` is the safe code-generation target | non-React output is not a reliable default | treat non-React projects as design-output-first unless explicitly handled elsewhere |
| Guidelines are package- or file-scoped | Make consumes local context, not one global enterprise brain | generate a rooted package and keep scope explicit |
| Prompt retries are costly | low-quality prompts waste credits and time | front-load detail and split work into stages |
| Complex Auto Layout inference is fragile | deep or mixed layout structures degrade reliability | keep nesting to `3` levels or fewer |

## Reliability Limits

Use these conservative planning bands:

| Scope | Reliability | Strategy |
|---|---|---|
| `1` screen | `90%+` | single focused prompt |
| `2-3` screens | `80%+` | staged prompt or component-first assembly |
| `4-7` screens | `65%+` | split by components and flows |
| `8-15` screens | `50-70%` | system -> pattern -> screen -> polish |
| `15+` screens | `<50%` | ask first; split by module |

## Prompt Packaging Rules

- Prefer `1-2` screens per prompt.
- Keep Auto Layout nesting at `3` levels or fewer.
- Generate `4` or fewer variants per generation step.
- Explicitly name the default variant when a component has variants.
- Use explicit `gap`, `padding`, and sizing rules instead of vague layout intent.

## Design-System Package Rules

If a package-backed design system is available:
- reference package component names instead of redescribing every structure
- focus Guidelines on composition, layout, naming, and prohibitions
- treat package tokens and variants as the primary source of truth unless Muse reports drift

## Make Attachments

Make Attachments let users add files directly to prompts for one-off context. Supported types: PDF, markdown, code (TSX/JS/CSS), CSV, JSON, media (JPEG/PNG/GIF/MP4/MP3), SVG.

| Use case | Mechanism | Rationale |
|---|---|---|
| Persistent design system rules | Guidelines.md | Reused across sessions, shared via kits |
| One-off project context (PRD, brand guide, reference images) | Attachments | Session-specific, not part of design system |
| Data-driven prototypes (CSV, JSON) | Attachments | Real data shapes the output, not a reusable rule |

Rules:
- Keep attachments focused — attaching too many files floods the context window
- Name the role of each attachment in the prompt ("Use the attached CSV as the data source for the table")
- Do not duplicate persistent rules in attachments — reference Guidelines instead

## Known Failure Cases

Watch for:
- image-heavy or content-heavy screens
- ambiguous reference attachments
- too many screens in one prompt
- too many variants in one step
- mixed layout directions with weak constraints
- brand-sensitive screens generating designs resembling well-known apps (design leakage)

## Guardrail Checklist

- [ ] Prompt scope is small enough
- [ ] Attachment role is explicit
- [ ] Auto Layout nesting is `3` levels or fewer
- [ ] Variant count per step is `4` or fewer
- [ ] Token names are exact
- [ ] Package component names are referenced when available
- [ ] Large generation plans are split before delivery
