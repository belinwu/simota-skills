# Prompt Engineering Reference

Prompt architecture, provider-specific tips, negative constraints, and example prompts for text-to-3D and image-to-3D generation.

## Prompt Architecture

Structure prompts in four layers:

```
[Subject] + [Style] + [Topology] + [Scale]
```

| Layer | Purpose | Example |
|-------|---------|---------|
| Subject | What to generate | "Medieval wooden treasure chest" |
| Style | Visual treatment | "low-poly stylized, hand-painted texture" |
| Topology | Mesh requirements | "clean quad topology, game-ready" |
| Scale | Size context | "prop scale, 1 meter wide" |

### Full Prompt Example

```
Medieval wooden treasure chest with iron bands and padlock,
low-poly stylized with hand-painted textures,
clean topology suitable for game engine,
prop scale approximately 1 meter wide
```

## Prompt Length Guidelines

| Length | Words | Recommendation |
|--------|-------|----------------|
| Optimal | 30-50 | Best balance of control and quality |
| Good | 50-100 | More detail, still reliable |
| Acceptable | 100-200 | May lose coherence on some providers |
| Avoid | > 200 | Diminishing returns, conflicting instructions |

Rules:
- Lead with the subject noun.
- Place style after subject.
- Keep topology/technical terms at the end.
- Use commas to separate clauses, not complex sentences.

## Provider-Specific Tips

### Meshy

- Supports `art_style` parameter: `realistic`, `sculpture`, `cartoon`, `low-poly`.
- Set style via parameter rather than prompt text when possible.
- Works well with detailed material descriptions ("weathered bronze", "polished marble").
- `topology: "quad"` parameter produces cleaner results for game assets.
- Preview mode is fast (~30s) but lower quality; Refine mode is slower (~2-5min) but production-viable.

### Tripo

- Excels at organic shapes (characters, creatures, plants).
- Shorter prompts (20-40 words) often produce better results than long ones.
- Supports multi-view input for image-to-3D; provide front + side views for best results.
- Model version significantly affects output; specify `model_version` explicitly.

### Hunyuan3D

- Open-source; behavior varies by checkpoint version.
- Benefits from explicit geometric terms ("smooth surface", "sharp edges").
- Self-hosted: adjust inference steps for quality vs speed tradeoff.
- For image-to-3D: single clean image with white background produces best results.

### Rodin

- Best for high-detail assets (characters, organic forms).
- Accepts multi-view condition images alongside text prompts.
- Higher cost but better topology quality.
- Responds well to artistic style references ("in the style of Pixar", "Ghibli aesthetic").

### Sloyd

- Parametric approach: works differently from pure AI generation.
- Best for architectural elements, furniture, simple props.
- Outputs pre-retopologized meshes (already game-ready).
- Prompt as a specification rather than a description.

### Stability (TripoSR)

- Single-image-to-3D specialist.
- Fast inference (~10s per model).
- Input image quality directly determines output quality.
- White or transparent background strongly recommended.

## Negative Constraints

Include these in prompts to avoid common AI generation artifacts:

| Issue | Negative Constraint Phrase |
|-------|--------------------------|
| Janus (multi-face) | "single continuous surface, no duplicate features" |
| Floating geometry | "no floating parts, all geometry connected" |
| Internal faces | "no internal faces, clean exterior surface only" |
| Excessive detail | "game-ready detail level, no micro-geometry" |
| Broken symmetry | "symmetrical design" (when appropriate) |
| Scale ambiguity | Include explicit size reference |

### Negative Prompt Example

```
A fantasy sword with ornate handle,
stylized game asset, clean topology,
no floating geometry, no internal faces,
single continuous mesh, symmetrical blade
```

## Image-to-3D Reference Preparation

### Optimal Input

1. **Multi-view images** (best): front, side, back, 3/4 angle.
2. **Single image** (acceptable): front or 3/4 view with clean background.

### Image Requirements

| Requirement | Specification |
|-------------|--------------|
| Background | White, solid color, or transparent |
| Lighting | Even, diffuse, no harsh shadows |
| Subject fill | 70-80% of frame |
| Resolution | 512x512 minimum, 1024x1024 recommended |
| Format | PNG (preferred) or JPEG |
| Ground shadows | Remove or minimize |
| Occlusion | Avoid heavy self-occlusion |

### Multi-View Consistency

For multi-view input (Tripo, Rodin):
- Use consistent lighting across all views.
- Maintain consistent color/exposure.
- Keep the same camera height and distance.
- Use turntable-style rotation (every 90 degrees).

## Multi-View Consistency and Janus Problem

The "Janus problem" occurs when SDS-based (Score Distillation Sampling) methods create models with duplicate features (e.g., two faces on a character). To mitigate:

1. **Use multi-view aware models**: Providers using MVDream, Zero123++, or similar multi-view diffusion avoid Janus artifacts.
2. **Specify view consistency**: "consistent appearance from all angles".
3. **Use FlexiCubes extraction**: Produces more coherent surfaces than naive marching cubes.
4. **Provide multi-view reference images**: Constrains generation to consistent geometry.

## Example Prompt Library

### Characters

```
# Stylized character
Chibi fantasy warrior character, large head proportions,
simple armor with sword and shield, stylized cartoon aesthetic,
clean topology for rigging, T-pose, game-ready

# Realistic character
Realistic medieval knight in full plate armor,
detailed surface with scratches and wear,
A-pose for rigging, high detail for hero asset,
approximately 180cm tall human proportions
```

### Props

```
# Simple prop
Wooden barrel with metal bands,
low-poly stylized, hand-painted texture look,
game-ready prop, approximately 1 meter tall

# Detailed prop
Ornate treasure chest with gold trim and gemstones,
semi-realistic style, clean quad topology,
openable lid (separate mesh), prop scale 80cm wide
```

### Environment

```
# Nature element
Stylized oak tree with thick trunk and full canopy,
low-poly foliage cards, game environment asset,
LOD-friendly silhouette, approximately 5 meters tall

# Structure
Medieval stone tower with spiral staircase visible through windows,
weathered stone texture, modular design for tiling,
game environment piece, 10 meters tall
```

### Vehicles

```
# Fantasy vehicle
Steampunk airship with propellers and wooden hull,
stylized game asset, clean topology,
approximately 15 meters long, no internal geometry

# Realistic vehicle
Military jeep with canvas top and mounted spotlight,
realistic proportions and surface detail,
game-ready vehicle asset, LOD-appropriate detail
```

## Prompt Iteration Strategy

1. **Start with a draft prompt** (30 words) and generate 1-3 previews.
2. **Evaluate results** against reference or requirements.
3. **Refine by adding specifics**: material, scale, topology constraints.
4. **Avoid over-specification**: if the result is good, stop adding terms.
5. **Document the final prompt** in metadata JSON for reproducibility.
