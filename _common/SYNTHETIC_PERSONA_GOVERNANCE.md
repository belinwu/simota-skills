# Synthetic Persona Governance

Cross-agent rules for AI-generated personas. Referenced by Cast, Echo, Plea, and Researcher.

## Confidence Rules

| Rule | Definition | Applies To |
|------|-----------|------------|
| **Confidence cap** | AI-only generation capped at confidence ≤ 0.50 | Cast (generation), Echo (usage), Plea (usage) |
| **Promotion condition** | `proto → active` requires at least 1 human research validation stream | Cast (registry), Researcher (validation) |
| **Expiry** | Synthetic personas without human validation require forced review at 60 days | Cast (decay rules) |

## Bias Audit

All synthetic personas must be checked for these 4 failure modes before distribution:

| Failure Mode | Description | Detection |
|-------------|-------------|-----------|
| **Mode collapse** | AI produces homogeneous personas clustered around stereotypical archetypes | Check diversity across trait dimensions |
| **Bias laundering** | Fluent empathetic language masks underrepresentation of marginalized perspectives | Compare demographic coverage against target population |
| **Over-sanitization** | AI avoids negative traits, producing unrealistically positive personas | Verify negative/frustration attributes are present |
| **People-pleasing** | AI generates what it thinks the team wants to hear | Compare against real Voice/Trace data when available |

## Tagging Rules

| Context | Required Tag | Applies To |
|---------|-------------|------------|
| All synthetic-derived findings | `[synthetic-hypothesis]` | Echo (reports), Plea (demand reports) |
| Downstream bias risk | Include bias caveat in DISTRIBUTE packet | Cast (distribution) |
| WEIRD population warning | Flag when target is non-Western, non-English | Cast, Echo, Researcher |

## Usage Constraints

| Constraint | Rule |
|-----------|------|
| **Go/No-Go decisions** | Synthetic-only findings must NOT be used for go/no-go decisions |
| **Demand forecasting** | Synthetic demands require real-data calibration (see `plea/references/calibration.md`) |
| **Research split** | 80% synthetic (rapid iterations, screening) / 20% human (depth, edge cases, cultural nuance) |
| **High-risk domains** | Regulated, novel markets, or culturally-sensitive contexts require human validation before any action |

## Feedback Loop

Synthetic persona findings should flow back to Cast to improve confidence:

```
Echo walkthrough result → Cast FUSE (confidence adjustment)
Plea demand calibration → Cast FUSE (coverage gap signal)
Trace behavioral validation → Cast EVOLVE (existing path)
Researcher interview validation → Cast promotion (proto → active)
```

## Reference

Full AI persona risk details: `_common/AI_PERSONA_RISKS.md`
