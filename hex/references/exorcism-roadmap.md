# Exorcism Roadmap

How Hex turns the character spec into an actionable refactor roadmap. Used during the `ROADMAP` phase. Without the roadmap, Hex is just AI art — the roadmap is what makes it diagnostic.

## Core Principle: Trait → Refactor (1:1)

For every visible trait on the character, the roadmap names exactly one refactor task that, when shipped, will banish that trait from the next snapshot. This is what gives users a feedback loop: "we untied the chain on the right arm" should be a literal sentence after the next run.

## Roadmap Item Schema

```yaml
- id: R-001
  banishes_trait: "rusted shoulder pauldron"
  category: outdated_dependencies
  intensity_addressed: 0.7
  task: "Upgrade react 16 → 19 in the checkout package"
  evidence_anchor: "package-lock.json:1024"
  effort: M           # XS | S | M | L | XL  (≈ <2h | <1d | 1-3d | 1w | >1w)
  risk: medium        # low | medium | high   (likelihood of regression)
  prerequisites: []
  expected_visual_change: "shoulder pauldron returns to clean steel"
```

## Prioritization

Roadmap items are sorted by:

```
priority = intensity_addressed × category_weight × (1 / effort_cost)
                              − risk_penalty
```

Where:

- `category_weight` reuses the weights from `severity-rubric.md`
- `effort_cost`: XS=1, S=2, M=4, L=8, XL=16
- `risk_penalty`: low=0, medium=0.2, high=0.5

Top of the list = "biggest visual change for the cheapest, safest fix."

## Phasing

Group roadmap items into 3 phases. The user (or Atlas) executes them in order:

| Phase | Theme | Typical content |
|-------|-------|-----------------|
| `Phase 1 — Banish` | Quick wins, top severity | Critical CVE patches, top TODOs older than 180 days, easiest dep bumps |
| `Phase 2 — Bind` | Structural fixes | Test coverage backfill on the dominant module, breaking up god classes, reducing duplication |
| `Phase 3 — Restore` | Long-term form | Architectural refactor, full dep modernization, documentation rewrite |

Each phase ends with a re-run of Hex (default `summon`) to verify the silhouette changed. Visualizing progress is the point.

## Output Format

```markdown
## Exorcism Roadmap — Tier T3 Wraith (Score 4.7)

### Phase 1 — Banish (target: drop to T2 in ~2 weeks)

1. **Patch CVE-2024-XXXX in `lib/auth`** — banishes the toxic green aura
   - Effort: S | Risk: low
   - Evidence: `package-lock.json:1024`
   - Expected: aura clears

2. **Untie 8 TODOs older than 180 days in `src/checkout`** — removes parchment seals
   - Effort: M | Risk: low
   - Evidence: `src/checkout/process.ts:142, 198, 240, …`
   - Expected: forearm bindings fall away

…

### Phase 2 — Bind (target: drop to T2 confirmed)

…

### Phase 3 — Restore (target: T1 by next quarter)

…

### Re-run cadence

- After each phase, run `hex summon` to update the character.
- Compare the new character against the original snapshot to confirm trait removal.
```

## Effort Calibration

Hex does not estimate effort from thin air — calibrate against:

- The size of the affected module (LOC, file count)
- The historical Atlas / Builder / Sweep handoff effort estimates if available
- The blast radius from `Ripple` if that handoff exists
- If no calibration is available, mark the effort as `M ?` (best-guess medium with explicit uncertainty)

## Risk Assessment

| Risk Level | Trigger |
|------------|---------|
| `low` | Pure removal (TODOs, dead code, lint fixes); deps with no breaking changes |
| `medium` | Refactor of business logic; minor framework upgrade; dep with deprecations |
| `high` | Major framework upgrade; god-class breakup; data model change; architectural shift |

If a single roadmap item is `high` risk, attach a "see Atlas / Magi" note — Hex stops short of architectural decision authority.

## What the Roadmap Is Not

- It is **not** an ADR. Hex names *what* would banish the trait; Atlas names *how* and *why*.
- It is **not** a sprint plan. The phasing is logical-order, not capacity-aware. A sprint planner consumes this list, doesn't replace it.
- It is **not** a guarantee. A team could ship every Phase-1 item and still see T3 if new debt accumulates faster than it's banished. Hex measures, doesn't prescribe how to allocate engineering time.

## Handoff Hooks

The roadmap is shaped to be consumable by:

- **Atlas**: Phase 3 architectural items become ADR/RFC inputs
- **Builder**: Phase 1–2 concrete tasks become implementation tickets
- **Sweep**: Dead-code-related items can be batched into a single removal PR
- **Sentinel**: Security items can flow back as verification targets
- **Sherpa**: The whole roadmap can be decomposed into <15-min Atomic Steps

When emitting the roadmap, list which downstream agents are relevant. The user decides who executes.

## Empty Roadmap (T1 Veil)

If the codebase is `T1`, the roadmap is intentionally short:

```markdown
## Exorcism Roadmap — Tier T1 Veil (Score 0.6)

The codebase carries minimal debt. The Veil is faint.

Recommended cadence:
- Re-run `hex audit` monthly to catch drift early.
- No active refactor required. The character is a healthy snapshot, not a call to action.
```

Resist the urge to invent work. T1 means the character is doing its job by being unalarming.
