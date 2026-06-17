# Value Proposition Canvas

Purpose: test fit between what a user actually needs and what a proposed feature offers
*before* writing a spec. The Value Proposition Canvas (Strategyzer, Osterwalder) is the
zoom-in companion to JTBD — it takes the job statement from `persona-jtbd.md` and forces
an explicit match between customer reality and the proposed value.

Use this when a proposal needs a sharper value argument, when the team disagrees on "why
the user wants this", or when an idea feels like a solution looking for a problem.

## Contents
- The two halves
- Customer Profile (right circle)
- Value Map (left square)
- Fit assessment
- Connection to JTBD and proposals

## The Two Halves

The canvas has a **Customer Profile** (the user's world — observed, not invented) and a
**Value Map** (the offering — designed). The work is achieving **fit** between them.

```
   VALUE MAP (offering)            CUSTOMER PROFILE (user reality)
   ┌──────────────────┐           ┌──────────────────┐
   │ Products &       │  ── fit ──▶│ Customer Jobs    │
   │ Services         │           │                  │
   │ Pain Relievers   │  ── fit ──▶│ Pains            │
   │ Gain Creators    │  ── fit ──▶│ Gains            │
   └──────────────────┘           └──────────────────┘
        designed                       observed
```

Build the **Customer Profile first**, from evidence (Field interviews, Voice feedback,
analytics). Designing the Value Map first is the classic trap — it bakes in the solution
you already wanted to build.

## Customer Profile (right circle)

| Block | Definition | Source |
|-------|------------|--------|
| `Customer Jobs` | Functional, emotional, and social jobs the user is trying to get done | JTBD statement from `persona-jtbd.md` |
| `Pains` | Bad outcomes, obstacles, risks before/during/after the job | Field research, Voice, support tickets |
| `Gains` | Outcomes and benefits the user wants — required, expected, desired, unexpected | interviews, analytics, stated goals |

Rank each block by importance to the user (not by how easy it is to address). The top
1-2 jobs/pains/gains are the only ones that matter for fit.

## Value Map (left square)

| Block | Definition | Must answer |
|-------|------------|-------------|
| `Products & Services` | What the feature/offering concretely provides | does it let the user *do* the top job? |
| `Pain Relievers` | How the offering removes/reduces the ranked pains | which specific pain, by how much? |
| `Gain Creators` | How the offering produces the ranked gains | which specific gain, beyond table stakes? |

A value map that relieves a pain the user did not rank, or creates a gain nobody wants,
is wasted scope — feed it to `void` for subtraction.

## Fit Assessment

Three levels of fit, used as a gate before a proposal proceeds:

1. **Problem–Solution fit** (on paper): pain relievers + gain creators map to *ranked*
   pains + gains. Validated here on the canvas.
2. **Product–Market fit** (in market): users actually adopt the value. Validated by
   `experiment` / launch metrics, not by the canvas.
3. **Business-model fit**: the value can be delivered profitably. Escalate to `helm`
   (`business-model-canvas.md`).

**Gate rule:** a proposal claiming a value proposition must show at least one
pain-reliever or gain-creator that maps to a **top-ranked, evidence-backed** pain/gain.
"Nice to have" maps to low-ranked items → kill or defer.

## Connection to JTBD and Proposals
- The VPC `Customer Jobs` block **is** the JTBD output — do not re-derive it; pull the
  `When [situation], I want [motivation], so I can [outcome]` statement from
  `persona-jtbd.md` and its four forces of progress.
- Feed the validated Value Map into the proposal's hypothesis and value rationale
  (`proposal-templates.md`): the top pain-reliever/gain-creator becomes the measurable
  hypothesis, and the un-addressed-but-ranked pains become explicit out-of-scope notes.
- For business-model / monetization fit (revenue streams, cost structure, channels),
  hand off to `helm` `business-model-canvas.md` — the VPC is the customer-fit zoom-in,
  the BMC is the whole-business zoom-out.
