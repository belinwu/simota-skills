# Trait Mapping

How findings become character traits. Used during the `ANTHROPOMORPHIZE` phase. The constraint that gives Hex its diagnostic value: **every visible trait on the character must trace 1:1 back to a detected, evidenced finding.** No decorative flourishes.

## Mapping Rule (1:1)

For each `CategoryScore ≥ 0.3` (the salience floor from `severity-rubric.md`), pick one trait surface from the table below and pair it with the strongest finding from that category.

```yaml
trait:
  surface: "rusted_armor"
  category: outdated_dependencies
  intensity: 0.7        # = CategoryScore
  source_finding: F-014  # references the finding id
  citation: "package-lock.json:1024 (react@16, current major @19)"
  visual_note: "rust concentrated on chest plate (the package's heaviest call site)"
```

## Trait Surface Catalog

### 1. Code Smells → Body Distortion

| Intensity | Visual |
|-----------|--------|
| 0.3–0.5 | Slight hunch, asymmetric shoulders |
| 0.5–0.7 | Twisted limbs, swollen joints |
| 0.7–1.0 | Severely deformed silhouette, unnatural curvature |

### 2. Duplication → Doppelgängers

| Intensity | Visual |
|-----------|--------|
| 0.3–0.5 | Faint mirrored shadow trailing the figure |
| 0.5–0.7 | Visible second self emerging from the back/shoulder |
| 0.7–1.0 | Multiple conjoined twins, hydra-like multiplication |

### 3. Cyclomatic Complexity → Branching Limbs

| Intensity | Visual |
|-----------|--------|
| 0.3–0.5 | Extra finger or two, slightly tendril-like hair |
| 0.5–0.7 | Third arm or branching forearm |
| 0.7–1.0 | Multi-armed silhouette, tentacular tendrils replacing legs |

### 4. Outdated Dependencies → Rusted Equipment

| Intensity | Visual |
|-----------|--------|
| 0.3–0.5 | Patina on a single armor plate |
| 0.5–0.7 | Rust streaks, cracked weapon edge |
| 0.7–1.0 | Corroded armor, weapon snapped, moss creeping in |

### 5. Test Coverage Gap → Translucent Body

| Intensity | Visual |
|-----------|--------|
| 0.3–0.5 | Hands faintly transparent |
| 0.5–0.7 | Forearms or torso half-translucent |
| 0.7–1.0 | Major body region missing or ghostly, organs partially visible |

### 6. TODO/FIXME/HACK → Bindings and Bandages

| Intensity | Visual |
|-----------|--------|
| 0.3–0.5 | A few cloth wraps around the wrist |
| 0.5–0.7 | Chains around limbs, sealed parchment talismans |
| 0.7–1.0 | Heavy iron chains, mouth gagged, multiple manacles |

### 7. Architectural Violations → Tumors and Conjoined Growth

| Intensity | Visual |
|-----------|--------|
| 0.3–0.5 | Small protrusion on shoulder |
| 0.5–0.7 | Visible growth, second head emerging |
| 0.7–1.0 | Massive tumorous mass, conjoined torso, twisted spine |

### 8. Security Debt → Toxic Aura

| Intensity | Visual |
|-----------|--------|
| 0.3–0.5 | Faint green vapor at the feet |
| 0.5–0.7 | Glowing sigil dripping liquid, vapor surrounds limbs |
| 0.7–1.0 | Full-body toxic aura, environment corroding around the figure |

### 9. Performance Hotspots → Burning / Freezing Regions

| Intensity | Visual |
|-----------|--------|
| 0.3–0.5 | Hot embers along one limb, or frost on knuckles |
| 0.5–0.7 | Open flames or ice crystals on a body region |
| 0.7–1.0 | Whole limb engulfed in fire or ice, scorch/crack damage |

### 10. Documentation Gap → Faceless Features

| Intensity | Visual |
|-----------|--------|
| 0.3–0.5 | Eyes covered by veil |
| 0.5–0.7 | Face featureless from the eyes up |
| 0.7–1.0 | No face at all, or sewn-shut mouth and blank slate where eyes belong |

## Composition Rules

1. **Cap the trait count at 8.** If more than 8 categories exceed the salience floor, render only the top 8 by intensity. Listed in the report; not visualized.
2. **Dominant category gets primary silhouette weight.** If security debt dominates, the toxic aura is the first thing the eye sees.
3. **Keep readability.** A character that is rusted *and* burning *and* translucent on the same arm becomes incoherent — when conflicts arise on the same body region, split traits across regions per the table below.
4. **Tier governs base form.** Trait surfaces overlay the tier silhouette from `tier-codex.md`; never replace it.

## Body Region Allocation (Conflict Resolution)

When multiple categories want the same region, use this default allocation order:

| Region | Default category |
|--------|------------------|
| Head/face | Documentation Gap |
| Mouth | TODO/FIXME (gag), Documentation Gap (sewn) |
| Chest/torso | Architectural Violations |
| Arms | Cyclomatic Complexity, Performance Hotspots |
| Hands | Test Coverage Gap (translucency) |
| Legs/feet | Outdated Dependencies (corroded boots), Security Debt (aura pooling) |
| Shadow/aura | Duplication (doppelgängers), Security Debt (aura) |
| Skin/surface | Code Smells (distortion) |

If a region is already taken by the dominant category, push the secondary trait to the next-best region and note the override in the spec.

## Citation Discipline

Each trait entry in the character spec must list:

- `category`
- `intensity` (= CategoryScore)
- `source_finding` (id)
- `citation` (`path:line`)
- `visual_note` (one-line description)

If you cannot produce all five fields for a trait, drop the trait. Hex never renders unevidenced visuals — that is the line that separates a diagnostic from decorative AI art.

## Retrospective Use (2026 facilitator notes)

When the rendered character is shown in a retrospective, surface the evidence list inline with the image — do not let the visual stand alone as decoration. The current generation of retro tooling (Miro AI retrospective templates, Parabol's grouping/AI summary, Reetro/Retrium) can cluster sticky notes and surface action items, but they do not enforce evidence linkage; Hex does. Pair every trait the team reacts to with its `path:line` citation in the discussion. References: <https://miro.com/miroverse/ai-retrospective-template/>, <https://www.parabol.co/comparison/miro-alternative/>.

If the codebase exhibits AI-generated-code symptoms (high Duplication, churn-within-2-weeks, low refactor ratio per GitClear 2025: copy-pasted lines 12.3% in 2024 vs 8.3% in 2021, refactored "moved" lines 9.5% vs 24.1%), call this out as a "Brood" sub-motif overlay on the dominant trait rather than introducing a new category. Source: <https://www.gitclear.com/ai_assistant_code_quality_2025_research>.
