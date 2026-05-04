# Portrait Prompts

Build Sketch-ready AI portrait prompts for an agent character. The `portrait` Recipe takes a Realm character sheet (class, stat tier, rank, badges, department, active quest), selects a **style variant**, and emits a positive/negative prompt pair, style anchors, trait citations, and a `REALM_TO_SKETCH_PORTRAIT` handoff packet.

Realm produces the prompt and citations only. Image rendering is Sketch's responsibility.

## Inputs and Visual Surface

Each visible trait in the prompt MUST cite at least one input attribute. No invented elements.

| Attribute | Source ref | Visual surface |
|-----------|-----------|----------------|
| `class` | `class-system.md` | Job archetype — silhouette, gear, profession cues |
| `stat tier` (`STR`/`DEX`/`INT`/`WIS`/`CHA`/`CON`) | `stat-calculation.md` | Build, posture, gear emphasis (NOT raw numerical display) |
| `rank` | `rank-xp-system.md` | Costume grade, insignia, ornamentation density |
| `badges` | `badge-catalog.md` | Emblems, accessories, flair (density per rarity) |
| `department` | `organization-map.md` | Background motif, allegiance markers |
| `active quest` | `quest-mapping.md` | Pose, held tool / weapon, environmental cue |

## Mapping Rules

1. **1 trait = 1 citation.** Every armor piece, badge, accessory, pose detail, or background element traces back to a Realm-tracked attribute. Citations are listed alongside the prompt in the handoff packet.
2. **Stat tier governs body/posture, not numerical display.** Use the tier thresholds in `stat-calculation.md`; do not write "STR 12" into the prompt. Tier-1 STR ≠ "weak"; calibrate against the rubric.
3. **Rank governs costume density and ornamentation, not pose dominance.** Avoid implying superiority through aggressive postures across ranks — keep all agents in dignified, character-sheet posture.
4. **Badge density follows rarity tier, not visual real estate.** Common badges = subtle pin / brooch. Rare = visible emblem. Legendary = central focal element. Never fill the canvas with badges to "look impressive."
5. **Class wins ties.** When two attributes suggest conflicting visual cues (e.g., heavy-armor class + low STR tier), class anchors the silhouette; stat tier modulates posture and weight inside that silhouette.

## Style Variants

Default variant: **`personality-archetype-chibi-paper-poly`**. Override via the `style_variant` field in the handoff packet, or whenever the user requests a specific aesthetic.

| Variant key | Tone | Aspect | When to use |
|------------|------|--------|-------------|
| `personality-archetype-chibi-paper-poly` ⭐ default | 2.5-head chibi, fully-flat 2D base + light polygon facets on hair tips / ribbon edges / ornaments | `1:1` | Default ecosystem portrait — friendly, sticker-like, with paper-craft geometric depth |
| `personality-archetype-chibi-flat` | 2.5-head chibi, fully-flat 2D, no faceting | `1:1` | Pure sticker / pictogram register |
| `personality-archetype-flat` | Stylized elongated proportions, flat illustration | `3:4` | Personality-test app register, modern editorial |
| `personality-archetype-low-poly` | Flat-shaded base + heavier faceted geometry across silhouette | `3:4` | Game-leaning register, more structured |
| `heroic-fantasy` | Painterly oil-style RPG portrait | `2:3` | Fantasy / event art, tier-S agents, chronicle highlights |

### Shared style rules (all variants)

- Soft inner glow, gentle approachable mood. Realm portraits are dignified hero shots, never menacing.
- Centered composition, character-sheet framing.
- No heavy outlines unless the variant explicitly calls for them.
- Class anchors silhouette; stat tier / rank / badge density layered on top.
- Cold-start attributes (`??`) are explicitly omitted from the visible surface — declare them in `cold_start_attributes`, never invent.

### Variant snippets

Each snippet provides a positive-prompt skeleton (fill `[ATTRS]` with attribute-derived traits) and a variant-specific style-anchor / negative-addition set. Combine with the **shared negative base** below.

#### `personality-archetype-chibi-paper-poly` (default)

Positive skeleton:

```
modern personality-archetype chibi illustration of [CLASS] character,
super-deformed proportions at roughly 2.5 head height, fully flat 2D
vector style with subtle low-poly accents, single-tone color fills,
paper-cut layered shapes, light angular polygon faceting on hair tips,
ribbon edges, and background ornaments giving paper-craft geometric
depth without 3D rendering, [DEPT_PALETTE] pastel palette, minimal
cute facial features with simple dot eyes and gentle approachable
expression, [CLASS_SILHOUETTE] with faceted-tip accents,
[SPECIALTY_ITEM], [RANK_ORNAMENT_DENSITY], [BADGE_EMBLEMS],
[QUEST_POSE_OR_NEUTRAL], soft inner glow, clean vector edges, no heavy
outlines, sticker-like silhouette, caption block at bottom-center on a
soft pastel band with one paper-cut polygon accent: large friendly
rounded sans-serif lowercase agent name "[AGENT_NAME]" on the upper
line, smaller "[ROLE] · [CATEGORY]" on the lower line in a soft mid-tone
color, centered composition, 1:1 portrait
```

- style_anchors: `["personality-archetype illustration", "chibi 2.5-head proportions", "fully flat 2D base", "subtle low-poly accents", "paper-cut layered shapes", "angular polygon faceting on edges", "soft pastel palette", "single-tone fills", "sticker-like silhouette", "no heavy outlines"]`
- variant negative additions: `dense low-poly mesh, wireframe, exposed mesh edges, gradient noise, full 3D rendering, hyperreal subsurface scattering`
- suggested_model_anchor: `stylized-flat-vector-with-poly-accents`

#### `personality-archetype-chibi-flat`

Replace polygon-faceting language with `clean flat shapes, no faceting, smooth silhouette edges`. Same chibi proportions and palette philosophy as the default variant.

- style_anchors: `["personality-archetype illustration", "chibi 2.5-head proportions", "fully flat 2D", "single-tone fills", "sticker-like silhouette", "no heavy outlines"]`
- variant negative additions: `polygon faceting, low-poly mesh, faceted geometry`
- suggested_model_anchor: `stylized-flat-vector`

#### `personality-archetype-flat`

Replace chibi proportions with `stylized elongated proportions, modern editorial body`. Aspect `3:4`.

- style_anchors: `["personality-archetype illustration", "stylized elongated proportions", "fully flat 2D", "modern editorial style", "soft pastel palette"]`
- variant negative additions: `chibi proportions, super-deformed, polygon faceting, low-poly mesh`
- suggested_model_anchor: `stylized-flat-illustration`

#### `personality-archetype-low-poly`

Stronger faceting language: `flat-shaded geometric planes throughout silhouette, polygonal forms with smooth gradient fills, faceted paper-craft surfaces`. Adult proportions. Aspect `3:4`.

- style_anchors: `["personality-archetype illustration", "stylized elongated proportions", "flat-shaded geometric planes", "low-poly faceting", "paper-craft surfaces", "soft pastel palette"]`
- variant negative additions: `chibi proportions, super-deformed, painterly oil, photoreal 3D`
- suggested_model_anchor: `stylized-low-poly-illustration`

#### `heroic-fantasy`

Painterly RPG portrait register. Aspect `2:3`.

- style_anchors: `["heroic-fantasy RPG portrait", "painterly", "character-sheet framing", "medium shot", "centered composition"]`
- variant negative additions: `chibi proportions, super-deformed, flat illustration, sticker style, low-poly mesh`
- suggested_model_anchor: `stylized-painterly`

## Nameplate (caption block in image)

Every portrait MUST include a small **caption block** rendered as typography inside the image. The caption block is part of the visible surface and follows the chosen `style_variant`.

### Rules

- **Text content**: a caption block with three short tokens, **and nothing else**:
  - `name` (primary, larger): agent name verbatim, lowercase one word (e.g. `flow`)
  - `role` (secondary, smaller): the agent's archetype from `class-system.md` **Archetype** column (e.g. `Illusionist`, `Strategic leader`, `Master crafter`). Class is kept in the handoff packet for silhouette mapping but is **not** rendered in the caption.
  - `category` (secondary, smaller): the agent's category from `class-system.md` Category column (e.g. `UX/Design`, `Implementation`, `Architecture`)
  - No rank, no badges, no decorative subtitles, no other text.
- **Layout**: `name` on the upper line; `role` and `category` on a smaller second line below, separated by a middle-dot `·` (e.g. `Enchanter · UX/Design`).
- **Position**: default `bottom-center` on a subtle band or directly on background. Override via `nameplate.position` only when the user requests it.
- **Size**: total caption-block height roughly 8–14% of canvas. `name` line ~60% of that height, secondary line ~40%. Must not cover face / silhouette / dominant trait.
- **Color**: chosen for high readability against the department palette; never bright primary against pastel base. Secondary line in a soft mid-tone derivative of the same palette. Allow soft shadow / subtle outline only when the variant supports outlines.
- **Typography**: variant-defined (see table below). `name` and secondary line share a font family but differ in size/weight.
- **Spelling**: emit each token (`name`, `role`, `category`) verbatim to Sketch. Diffusion models can mis-render text — keep tokens short. If `name` exceeds 8 characters, recommend `nameplate.position: top` and slightly smaller size. If `role` (archetype) exceeds 16 characters, fall back to the `class` value (always ≤ 11 characters in `class-system.md`). If `category` exceeds 12 characters, abbreviate via department short-form or drop it. If both `role` and `category` remain problematic after fallback, drop the secondary line and keep `name` only.
- **No trademark fonts**. Describe typography by category, not by foundry brand (e.g. `friendly rounded sans-serif`, not `Comic Sans` / `SF Pro` / specific brand names).

### Per-variant typography defaults

| Variant | Typography style |
|---------|------------------|
| `personality-archetype-chibi-paper-poly` (default) | `name`: friendly rounded sans-serif lowercase, slight letter-spacing. Secondary: same family at smaller size, soft mid-tone color. Caption block on a soft pastel band with one paper-cut polygon accent. |
| `personality-archetype-chibi-flat` | `name`: friendly rounded sans-serif lowercase. Secondary: same family at smaller size. Plain pastel band, no facets. |
| `personality-archetype-flat` | `name`: clean modern editorial sans-serif. Secondary: same family in lighter weight. No band — text directly on background. |
| `personality-archetype-low-poly` | `name`: geometric sans-serif with slight angular cut. Secondary: same family condensed. Faceted polygonal banner. |
| `heroic-fantasy` | `name`: classic fantasy serif with subtle gilded touches. Secondary: same family italic, smaller. Small scroll or stone tablet motif. |

### Optional caption supplements

Beyond the core caption block (`name` / `role · category`), three optional elements MAY enrich the portrait when source data is available. All supplements are independent — include or omit each per portrait. The portrait remains valid with only the core caption block.

| Supplement | Source | Include when | Visualization |
|-----------|--------|-------------|---------------|
| `tagline` | `class-system.md` Flavor column (e.g. "Enchanters make complexity feel effortless.") | Always available; include when ≤ 60 chars | Single italic line, smaller than secondary caption, placed directly under the caption block |
| `rank_pill` | `rank-xp-system.md` Title column (e.g. `Apprentice`, `Veteran`, `Champion`) | Rank is **not** cold-start | Small color-coded pill/badge tucked below or beside the caption block; pill color = rank `Badge Color` from `rank-xp-system.md` (Veteran=Purple, Elite=Gold, Champion=Orange, Legend=Red, etc.) |
| `affinity_icons` | Agent's `PROJECT_AFFINITY` from its SKILL.md frontmatter | Always available; show only entries marked `(H)` High; max 3 icons | Small abstract icon strip in a corner (no text labels). Standard symbols: SaaS=stacked cards, E-commerce=shopping bag, Mobile=smartphone, Dashboard=gauge, Marketing=megaphone, Game=controller |

#### Supplement rules

- **No text bloat.** Never write `PROJECT_AFFINITY: SaaS(H) E-commerce(H)` as text — render as icons only. `tagline` is the only additional text element.
- **Tagline**: short single-line italic. Never use the agent's full SKILL.md description, marketing copy, or invented quotes. Use `class-system.md` Flavor column verbatim; if it exceeds 60 chars, drop the leading subject (e.g. "Enchanters make complexity feel effortless." → "Make complexity feel effortless.") or omit.
- **Rank pill**: title only (no XP numbers, no level numbers, no `??`). Omit entirely under cold-start rather than rendering `??`.
- **Affinity icons**: abstract symbols only — never product logos, never company brands. Max 3 icons; if more than 3 entries are `(H)`, pick the 3 most thematically aligned with the agent's class.
- **Cold-start handling**: `rank_pill` is omitted. `tagline` and `affinity_icons` remain available because they trace to static SKILL.md / class-system.md data, not to runtime activity.
- **Negative prompt addition** (when supplements are used): add `extra paragraphs, full descriptions, marketing copy, brand logos, version numbers, statistics text` to the variant negative additions to prevent diffusion overflow.

## Shared Negative Base

Always include in the negative prompt, in addition to the variant negative additions:

```
mythic curse, eldritch horror, grotesque distortion, exorcism imagery,
photorealistic, real personality-test brand logos, named individuals,
modern clothing brand, source code text, secret identifiers, repo paths,
customer names, NSFW, gore, weapon brandishing, aggressive posture,
heavy outlines, gritty texture, additional captions or paragraphs,
extra text labels, watermarks, signature, misspelled nameplate,
duplicated nameplate, multiple text blocks
```

## Forbidden Tones (all variants)

- **Mythic-curse, exorcism, eldritch horror, grotesque body distortion** — Hex's domain. Never blend.
- **Photorealistic / real-person likeness / specific celebrity styling** — agents are abstract roles.
- **Direct trademark names** (e.g., MBTI, 16Personalities, specific game / studio brands) — describe generically via `personality-archetype illustration` style anchors instead.
- **NSFW, gore, violence-glorification.**

## Sketch Handoff Packet

```yaml
REALM_TO_SKETCH_PORTRAIT:
  agent: "<agent name>"
  class: "<class>"
  rank: "<rank or '??' for cold-start>"
  style_variant: "<variant key from table above; default: personality-archetype-chibi-paper-poly>"
  positive_prompt: "<≤ 200 words; must embed nameplate phrase>"
  negative_prompt: "<≤ 100 words; shared base + variant additions>"
  style_anchors: [<variant style_anchors>]
  aspect_ratio: "<variant default or override>"
  suggested_model_anchor: "<variant suggested_model_anchor>"
  nameplate:
    name: "<agent name verbatim, e.g., flow>"
    role: "<archetype from class-system.md Archetype column, e.g., Illusionist; falls back to class when archetype > 16 chars>"
    category: "<category name from class-system.md, e.g., UX/Design>"
    position: "bottom-center | top-center | top-left | bottom-left"
    typography:
      primary: "<font style for the name line, per variant default>"
      secondary: "<font style for the role · category line, per variant default>"
    background: "<soft pastel band | scroll motif | none | low-poly banner>"
    supplements:
      tagline:
        text: "<class flavor verbatim or shortened, ≤ 60 chars; null to omit>"
        source: "class-system.md Flavor column"
      rank_pill:
        title: "<rank title from rank-xp-system.md; null under cold-start>"
        color: "<rank Badge Color, e.g., Purple, Gold, Orange>"
      affinity_icons:
        items: ["<abstract symbol descriptor>", "..."]   # max 3, e.g. ["stacked cards (SaaS)", "shopping bag (E-commerce)", "smartphone (Mobile)"]
        position: "top-right | bottom-right | top-left | bottom-left"
  trait_citations:
    - trait: "<visible trait>"
      source: "<attribute citation>"
  cold_start_attributes: [<list of attributes not yet sourced>]
  pii_scrub:
    status: "passed | flagged"
    flagged_terms: []
    notes: "<e.g., 'Trademark names not embedded; <variant> described generically.'>"
```

## Validation Checklist

Before emitting the handoff packet, verify:

- [ ] `style_variant` is set explicitly.
- [ ] All visible traits in the prompt cite a Realm-tracked attribute (class / stat tier / rank / badge / department / active quest).
- [ ] Cold-start attributes listed in `cold_start_attributes` are not visualized — declared, not invented.
- [ ] No mythic-curse, eldritch, or grotesque-distortion imagery is present in any variant.
- [ ] No PII, customer / competitor / partner names, internal URLs, repo paths, secrets, or source code identifiers appear in the prompt.
- [ ] No real-person or named-individual references; no direct trademark brand names.
- [ ] Stat-tier → body / posture mapping calibrated per `stat-calculation.md` (not gut feel; not numerical display).
- [ ] Rank ornamentation density matches rank tier; pose dominance does NOT scale with rank.
- [ ] Badge density follows rarity tier, not canvas real estate.
- [ ] Class anchors the silhouette when attributes conflict.
- [ ] Sketch handoff packet is complete: positive, negative, `style_variant`, `style_anchors`, `aspect_ratio`, `suggested_model_anchor`, `nameplate`, `trait_citations`, `cold_start_attributes`, `pii_scrub`.
- [ ] Caption block embeds exactly three tokens: `name` (verbatim agent name), `role` (archetype from `class-system.md` Archetype column, with class fallback), `category` (category from `class-system.md`). No rank, no badges, no extra text.
- [ ] Layout: `name` on upper line (larger), `role · category` on lower line (smaller, middle-dot separator). Typography matches the variant default; position does not cover face or dominant trait.
- [ ] Long-token fallback applied: `name` > 8 → `position: top` + smaller size; `role` (archetype) > 16 → fall back to class; `category` > 12 → abbreviate or drop; both problematic → drop secondary line, keep `name` only.
- [ ] `class` value retained in handoff packet for silhouette mapping even when the displayed `role` is the archetype.
- [ ] Optional supplements respected: `tagline` ≤ 60 chars (or null); `rank_pill` set only when rank is not cold-start (otherwise null, never `??`); `affinity_icons` are abstract symbols only (no brand logos), max 3.
- [ ] No supplement contains: SKILL.md description, marketing copy, XP numbers, levels, version strings, or product brand references.
- [ ] Tone matches the selected variant; no cross-variant bleed (e.g., heroic-fantasy painterly mixed into chibi-flat).

## Boundary Notes

- **Realm vs Hex.** Realm portraits visualize agent identity as a positive job-class character (any variant). Hex anthropomorphizes codebase debt as a curse (mythic-grotesque only). They never blend. If a request mixes "agent + debt curse," produce two separate artifacts — Realm portrait for the agent, Hex character for the debt.
- **Realm vs Dot.** Dot generates pixel-art sprites for the Phaser map (in-game tiles, low-res, palette-locked). Realm portraits are AI-painted hero shots rendered by Sketch. Both can coexist for the same agent.
- **Image rendering is Sketch's responsibility.** Realm produces prompt + citations + variant declaration only. If Sketch is unavailable, report the dependency gap rather than degrading to a non-image artifact.
- **Variant evolution.** New style variants may be proposed per user request, but each must keep the Forbidden Tones and Shared Negative Base intact, and must declare its own `style_anchors`, `variant negative additions`, and `suggested_model_anchor`.
