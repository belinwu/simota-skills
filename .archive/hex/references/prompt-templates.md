# Prompt Templates

How Hex composes the Sketch handoff packet during the `PROMPT` phase. Sketch will turn this into Gemini API code; Hex's job is to compose a high-quality, evidence-grounded prompt.

## Master Prompt Skeleton

```
[Subject + tier silhouette]: <one-line description>
[Form details]: <silhouette family from tier-codex.md, posture, size>
[Trait inventory]: <comma-separated trait surfaces with body region tags>
[Aura and atmosphere]: <aura intensity from tier, environmental notes>
[Palette]: <tier palette anchors>
[Style anchors]: mythic dark fantasy, painterly, dramatic chiaroscuro, single character full body, three-quarter view, painted concept art, clean neutral background
[Composition]: 2:3 portrait, centered, full body
[Mood]: <three tone keywords from tier-codex.md>
[Negative prompt]: text, letters, modern brand, photograph, anime moe, gore, sexualization, multiple characters, watermark, signature
```

## Worked Example — T3 Wraith, security-dominant

```yaml
sketch_handoff:
  positive_prompt: |
    A T3 Wraith — armored revenant, 1.1× human height, full body, three-quarter view.
    Combat-ready stance, one hand on a cracked sword, lantern relic at the hip.
    Trait surfaces:
      - toxic green aura pooling around the legs (security debt, dominant)
      - rusted shoulder pauldron and cracked greaves (outdated dependencies)
      - third arm branching from the right shoulder holding a second blade (cyclomatic complexity)
      - translucent left hand, fingers half-fading (test coverage gap)
      - parchment seals tied around the right forearm (TODO/FIXME)
      - faceless mouth, lower face wrapped in cloth (documentation gap)
    Palette: charcoal armor with verdigris, deep oxblood inner cloth, bone-white seals, sickly green aura.
    Atmosphere: battlefield ruin at twilight, low embers, smoke trailing from old wounds.
    Style: mythic dark fantasy, painterly, dramatic chiaroscuro, painted concept art, single character full body, three-quarter view, clean neutral background.
    Mood: vigilant, scarred, dignified.
  negative_prompt: |
    text, letters, modern brand, photograph, anime moe styling, cartoon comedy,
    gore, sexualization, multiple characters, watermark, signature, ui chrome
  style_anchors:
    - mythic dark fantasy
    - painterly
    - dramatic chiaroscuro lighting
    - painted concept art
    - single character full body
    - three-quarter view
  aspect_ratio: "2:3"
  resolution: "1024x1536"
  suggested_model: "gemini-3-pro-image-preview (Nano Banana Pro) for final renders; gemini-3.1-flash-image-preview (Nano Banana 2) for fast iterations"
  seed_strategy: "deterministic per-repo (hash of repo+date) for reproducible evolution snapshots"
```

## PII Scrub Pass

Before handing off, run a final scan over the prompt:

| Pattern | Action |
|---------|--------|
| File paths longer than the module name | Redact to module name only |
| Function or class names verbatim | Replace with abstract role ("the order processor") |
| Customer / company / employee names | Drop entirely |
| Internal URLs | Drop entirely |
| Proprietary product names | Replace with category label |
| Secrets, tokens, hashes (even partial) | Drop entirely; flag in report |

The image prompt should be readable as a piece of dark fantasy art with no clear connection to a specific company's source code.

## Composition Variants

| Use case | Composition tweak |
|----------|-------------------|
| Retro slide deck | Default 2:3 portrait |
| README banner | Request 16:9 from Sketch; pad with environmental haze; figure on left third |
| Onboarding doc inline | 1:1 square; tighten crop to mid-thigh up |

## Sketch Handoff Packet

The full packet handed to Sketch (or Nexus when in hub mode):

```yaml
HEX_TO_SKETCH_PROMPT:
  hex_run_id: <uuid>
  tier: T3
  total_score: 4.7
  positive_prompt: <string>
  negative_prompt: <string>
  style_anchors: [<list>]
  aspect_ratio: "2:3"
  resolution: "1024x1536"
  suggested_model: "gemini-3-pro-image-preview"
  seed: <int>
  pii_scrub_result: passed
  notes: <optional, e.g. "T5 — confirm with user before publishing">
```

## Model Selection (2026-05)

Google's image-generation family expanded in early 2026. Pick by tier and use-case:

| Model | Identifier | When to use |
|-------|------------|-------------|
| Nano Banana Pro | `gemini-3-pro-image-preview` | Final renders for T3–T5 characters, dashboard banners, anything published outside the dev team. Supports 4K, accurate text avoidance, 14-image style references. |
| Nano Banana 2 | `gemini-3.1-flash-image-preview` | Iteration loop while tuning the prompt; launched 2026-02-26 alongside Nano Banana Pro. Combines Pro's quality cues with Flash speed. |
| Nano Banana (legacy) | `gemini-2.5-flash-image` | Cheap snapshots for CI evolution timelines; superseded for end-deliverable use. |
| Imagen 4 Standard | `imagen-4.0-generate-preview` | Alternative when DeepMind painterly bias is preferred; tiered pricing Fast $0.02 / Standard $0.04 / Ultra $0.06 per image. |

Sources: <https://deepmind.google/models/gemini-image/>, <https://blog.google/innovation-and-ai/technology/ai/nano-banana-2/>, <https://ai.google.dev/gemini-api/docs/image-generation>.
