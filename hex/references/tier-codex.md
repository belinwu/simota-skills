# Tier Codex

Canonical silhouette, palette, and motif for each of the 5 tiers. Use during the `ANTHROPOMORPHIZE` and `PROMPT` phases. The tier governs the base form; trait surfaces from `trait-mapping.md` overlay it without replacing it.

## T1 — Veil

- **Score**: < 1.0
- **Silhouette**: Small child-like figure, half a head shorter than a real human, faint translucent edges
- **Posture**: Hesitant, looking down, hands hidden
- **Palette**: Pale ivory, faint grey-blue mist, soft moonlight backlight
- **Motif**: A single floating ribbon or thread; the spirit barely interacts with the world
- **Aura**: None or barely-there shimmer
- **Environment**: Empty soft-lit space, hint of dawn
- **Tone keywords**: nascent, fragile, hopeful, unfinished

> Read: a healthy young codebase. The image should reassure, not threaten.

## T2 — Shade

- **Score**: 1.0–2.5
- **Silhouette**: Full-height humanoid, partial features formed; cloak or robe partially solid
- **Posture**: Upright but stiff; one shoulder lower than the other
- **Palette**: Cool greys, dusk indigo, charcoal cloak with faint silver thread
- **Motif**: A simple staff, broken talisman, or single bandage; the curse is starting to take form
- **Aura**: Thin smoke or vapor pooling at the feet
- **Environment**: Twilight, indistinct ruins in the background
- **Tone keywords**: emerging, watchful, weary

> Read: an aging product with manageable debt. The image is a polite warning.

## T3 — Wraith

- **Score**: 2.5–5.0
- **Silhouette**: Armored revenant, fully formed, ~1.1× human height, visible weapon or relic
- **Posture**: Combat-ready, rooted stance, one hand on weapon
- **Palette**: Charcoal armor with verdigris, deep oxblood inner cloth, bone accents
- **Motif**: A cracked sword, sealed prayer scrolls, lantern or eye-shaped relic; battle-scarred bearing
- **Aura**: Visible heat-shimmer or low embers, smoke trailing from wounds
- **Environment**: Battlefield ruin, twilight or eclipse
- **Tone keywords**: vigilant, scarred, dignified

> Read: a working production system carrying real debt. The image earns respect — neither cute nor catastrophic.

## T4 — Revenant

- **Score**: 5.0–8.0
- **Silhouette**: Hulking cursed body, ~1.5× human height, asymmetric build, multiple wounds
- **Posture**: Slouched but powerful, weight uneven; one limb visibly larger than the others
- **Palette**: Iron black, smoldering crimson cracks across the skin, sickly bile-yellow highlights
- **Motif**: Broken multiple weapons strapped to the body; chains; multiple seals trying and failing to contain it
- **Aura**: Heavy aura distorting nearby air; visible miasma; the ground around the figure is cracked or burning
- **Environment**: Storm-lit ruin, heavy ash falling, the architecture itself failing in the background
- **Tone keywords**: dangerous, accumulated, restraint-failing

> Read: a system where debt has begun to bleed into product reliability. The image should make the team feel an urgency to act, not despair.

## T5 — Calamity

- **Score**: > 8.0
- **Silhouette**: Deity-class composite curse, ~2–3× human height, often multiple heads or limbs, terrain-warping presence
- **Posture**: Either enthroned or rising; the figure is the center of gravity in the image
- **Palette**: Void black, molten core glow, ichor green or bone white accents, environmental color drained around the figure
- **Motif**: Crowns of broken seals, coiled chains being torn, multiple weapons fused into one weapon, eyes too many to count
- **Aura**: A localized weather pattern — eternal storm, frozen sun, ash spiral; the world bends around it
- **Environment**: The figure *is* the environment; landscape is a husk, distance falls into the figure
- **Tone keywords**: civilization-scale, mythic, dread, irreversible-without-coordinated-action

> Read: a system whose debt is now an existential business risk. **Confirm with the user before publishing.** The image is a deliberately unsettling diagnostic — useful for budget conversations, harmful as a meme.

## Cross-Tier Visual Continuity

The same character archetype evolves across tiers — same silhouette family, same garment vocabulary, same color anchors that darken and amplify with each tier. When using `evolve` Recipe, hold the silhouette's identity (shoulder line, mask shape, weapon type) constant and let the deformation, palette, and aura tell the change story.

## Style Anchors (Image Generation)

These keywords go into every prompt regardless of tier:

- `mythic dark fantasy`
- `painterly`, `dramatic chiaroscuro lighting`
- `single character, full body, three-quarter view`
- `painted concept art`; for T1–T2 lean on `ethereal negative space` and `classical fantasy painting tradition`; for T3+ lean on `dense detailed linework` and `dark heroic fantasy illustration tradition`
- `centered composition, neutral environment`, `clean background`

Avoid:

- modern brand cues, photographs, generic anime moe styling, cartoon comedy
- gore-for-gore-sake; never sexualized
- text or letters on the character (keeps the image localizable)

## Aspect Ratio and Resolution

- Default: `2:3` portrait (suits a single-character full-body shot)
- For dashboards / banners: `16:9` may be requested by the user; pad with environmental haze rather than upscaling the figure
- Resolution: 1024×1536 baseline, 2048×3072 if downstream Sketch invocation supports it

## Tier Confirmation Checklist

Before composing the prompt, verify:

- [ ] Tier matches the formula in `severity-rubric.md` (no gut-feel override)
- [ ] Silhouette family fits the tier
- [ ] Palette anchors taken from the tier (not arbitrary)
- [ ] Motif inventory drawn from this codex
- [ ] Trait surfaces from `trait-mapping.md` overlay without contradicting the tier
