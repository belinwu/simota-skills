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
  suggested_model: "gemini-2.5-flash-image (Nano Banana 2)"
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
| Evolution diptych (`evolve` Recipe) | Two 2:3 portraits side-by-side, same lighting and seed family |

## ASCII Fallback

If Sketch is unavailable or the user requests text-only output, render the same character as ASCII art with a structured trait list. Keep the silhouette family and tone — the textual character should still feel mythic.

```
       .--""--.
      /  ___   \
     | / · _\ · |    ← faceless: documentation gap
     |  \_____/  |
     |  /     \  |    ← third arm: cyclomatic complexity
     |~~~~~~~~~~~|
     |  RUSTED   |    ← outdated dependencies
     |   ARMOR   |
     |~~~~~~~~~~~|
     |  >toxic<  |    ← security debt
     |   ~aura~  |
     '-_______-'

Tier:        T3 — Wraith   (Score 4.7)
Dominant:    Security debt
Traits:      Toxic aura · Rusted armor · Third arm · Translucent hand
             · Parchment seals · Faceless mouth
```

## Reproducibility (`evolve` Recipe)

For evolution snapshots:

1. Compute a stable seed hash: `hash(repo_url + ISO_date)`.
2. Use the same seed family across the diptych (left = old, right = new).
3. Hold style anchors and silhouette family identical; only let trait surfaces and tier change.
4. Note the seed in the report so future runs can reproduce the comparison.

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
  suggested_model: "gemini-2.5-flash-image"
  seed: <int>
  pii_scrub_result: passed
  notes: <optional, e.g. "T5 — confirm with user before publishing">
```
