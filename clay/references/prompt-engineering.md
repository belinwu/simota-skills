# Prompt Engineering Reference

Prompt architecture, provider-specific tips, negative constraints, style transfer, multi-view strategies, and example prompts for text-to-3D and image-to-3D generation.

## Prompt Architecture

Structure prompts in five layers:

```
[Subject] + [Style] + [Material] + [Topology] + [Scale]
```

| Layer | Purpose | Example |
|-------|---------|---------|
| Subject | What to generate | "Medieval wooden treasure chest" |
| Style | Visual treatment | "low-poly stylized, hand-painted texture" |
| Material | Surface properties | "weathered oak wood with tarnished iron bands" |
| Topology | Mesh requirements | "clean quad topology, game-ready, no internal faces" |
| Scale | Size context | "prop scale, 1 meter wide, fits on a table" |

### Full Prompt Example

```
Medieval wooden treasure chest with iron bands and padlock,
low-poly stylized with hand-painted textures,
weathered oak wood with tarnished iron fittings,
clean topology suitable for game engine, no floating geometry,
prop scale approximately 1 meter wide
```

## Prompt Length Guidelines

| Length | Words | Recommendation |
|--------|-------|----------------|
| Optimal | 30-60 | Best balance of control and quality |
| Good | 60-100 | More detail, still reliable |
| Acceptable | 100-150 | May lose coherence on some providers |
| Avoid | > 150 | Diminishing returns, conflicting instructions |

Rules:
- Lead with the subject noun.
- Place style after subject, material next.
- Keep topology/technical terms at the end.
- Use commas to separate clauses, not complex sentences.
- Be specific but not contradictory.

## Provider-Specific Tips

### Meshy (Meshy 6, GA 2026-01-18)

- Supports `art_style` parameter: `realistic`, `sculpture`, `cartoon`, `low-poly`, `pbr`.
- Set style via parameter rather than prompt text when possible.
- Prompts accept up to **800 characters** in any language.
- Works well with detailed material descriptions ("weathered bronze", "polished marble").
- `topology: "quad"` parameter produces cleaner results for game assets.
- Dedicated **Low Poly Mode** generates game-ready wireframes; Standard Mode for high-detail PBR.
- Preview mode (~30s): use for iteration. Refine mode (~60s typical for full Model+Texture): production quality.
- Text-to-texture: can re-skin existing models with new prompts.
- Newer models support negative prompts via `negative_prompt` parameter.
- API exposes Text-to-3D, Image-to-3D, Multi-Image-to-3D, AI Texturing, Remesh, and Rigging endpoints; Python + Node.js SDKs available.
- Full Text/Image-to-3D = 20 credits (Model + Texture); 100 credits/month free tier; $20-60/mo paid plans unlock API + private assets.
- Meshy Creative Lab (CES 2026) and Form Now integration (2026-04-08) close the loop from text/image → 3D → physical print/manufacture.

### Tripo (P1.0 + H3.1, 2026)

- Excels at organic shapes (characters, creatures, plants).
- Shorter prompts (20-40 words) often outperform long ones.
- Supports multi-view input for image-to-3D; provide front + side views.
- Model version significantly affects output; always specify `model_version`.
- **Tripo P1.0 Smart Mesh** (GDC 2026) — production-grade native 3D diffusion: vertices/edges/polygon faces modeled in a unified spatial probabilistic field rather than sequential token prediction → engine-ready quad-dominant low-poly in ~2s.
- **Tripo H3.1** (Mar 2026, "high-fidelity") — improved input alignment, geometry accuracy, texture quality, and generation speed for production hero assets.
- Tripo Studio enterprise edition integrates text-to-3D + image-to-3D + AI retopology + AI Rigging.
- Tripo Game Hub: experimental layer for turning generated assets into interactive projects.
- Supports style transfer via reference images.

### Hunyuan3D (3.0 / 3.1, intl. launch 2025-11)

- Open-source via `Tencent-Hunyuan/Hunyuan3D-2.1` (commercial-friendly Tencent license).
- Generates PBR textures natively: **Albedo, Metallic, Roughness, Normal, AO at up to 4K** out-of-the-box.
- 3D-DiT architecture; mesh at **1536³ resolution** (Hunyuan3D 3.0), **3.4× the geometric density** of v2.5 (which capped at 1024³).
- Hunyuan3D 3.1 international API available in Pro + Rapid editions.
- **Auto-Rig** option in Hunyuan3D Studio: skeletal rig with joints for arms/legs/spine, optimized for T/A-pose input, exportable to Mixamo / UE / Unity.
- Benefits from explicit geometric terms ("smooth surface", "sharp edges", "beveled corners").
- Self-hosted: adjust inference steps for quality vs speed (30 steps=fast, 75 steps=quality).
- For image-to-3D: single clean image with white background produces best results.
- Supports both text-to-3D and image-to-3D in a single model.
- Uses multi-view diffusion internally, largely immune to Janus problem.

### Rodin (Gen-2, Oct 2025 by Deemos Tech)

- Best for high-detail assets (characters, organic forms, complex props).
- **10B parameters, BANG architecture, recursive part-based generation** that divides and subdivides complex objects for intricate models with high fidelity.
- Generates **clean quad-based meshes** with fine surface details, **baked normals** to display high-poly detail on low-poly, **HD textures** ready for production pipelines.
- **Partial-redo** lets you regenerate only a specific part while keeping the rest untouched — strong for iterative refinement.
- Accepts multi-view condition images alongside text prompts.
- Higher cost but consistently better topology quality (4× improvement claimed over Gen-1).
- Responds well to artistic style references ("in the style of Pixar", "Ghibli aesthetic").
- Subscription from $12/mo (Creator) on hyper3d.ai.

### Sloyd (2.0, Apr 2026)

- Hybrid AI + parametric approach: slider/toggle customization of templates + AI workflows.
- Best for: architectural elements, furniture, simple props, modular pieces.
- Outputs pre-retopologized meshes (already game-ready topology).
- **Sloyd 2.0** added image-to-3D upload, the Visual WACK widget for identifying parametric components, render images + lighting/background controls, and unlimited generation on paid plans.
- Prompt as a specification rather than a description.
- Supports parameter-based variation (adjust dimensions, style).
- Fastest generation time (~5-15s) among all providers.
- Future roadmap: text-to-3D via G-splatting, watertightness QC, print-topology optimization.

### Stability (SPAR3D — Stable Point Aware 3D, CES 2025)

- Single-image-to-3D specialist (no text-to-3D).
- **0.7 s inference**; succeeds the earlier Stable Fast 3D.
- Two-stage architecture: lightweight point-cloud diffusion → regressive mesh prediction using both the sampled point cloud and the input image.
- **Real-time point-cloud editing**: delete, duplicate, stretch, add features, or recolor points before mesh extraction.
- Predicts complete 360° structure including hidden back faces.
- Input image quality directly determines output quality; white/transparent background recommended.
- Released under **Stability AI Community License — free for commercial + non-commercial use**; weights on Hugging Face, code on GitHub, API on Stability AI Developer Platform.

### TRELLIS.2 (Microsoft, Dec 2025)

- Open-source MIT, self-hosted, **4B parameters**.
- Image-to-3D only (no text-to-3D).
- O-Voxel "field-free" sparse voxel architecture for arbitrary topology / sharp features / non-manifold geometry; native 3D VAE with 16× spatial compression.
- Dual output: 3D Gaussian Splatting **+** extracted mesh.
- Models PBR: Base Color, Roughness, Metallic, **and Opacity/Alpha** — but exported `.glb` defaults to OPAQUE; you must connect the texture's alpha to material opacity manually in the target DCC.
- Generation: ~3 s at 512³ / ~17 s at 1024³ / ~60 s at 1536³ on NVIDIA H100.
- Best for: photorealistic reconstructions, objects with complex materials or transparency.

### PartCrafter (NeurIPS 2025, open-source)

- First **structured** 3D generative model: jointly synthesizes multiple semantically meaningful + geometrically distinct meshes from a single RGB image.
- Built on a pretrained 3D mesh diffusion transformer (DiT) — adds compositional latent space (per-part disentangled tokens) + hierarchical attention (within-part + cross-part).
- Generates parts that are not directly visible in the input image (e.g., back of an object, occluded internals).
- Ideal for assets needing per-part editing, animation, 3D printing with separate components, or scene-level multi-object reconstruction.

### Meta AssetGen 2.0 (announced May 2025)

- Meta's text + image → 3D foundation model with **3D diffusion** for geometry estimation, plus PBR materials.
- Currently used internally for Meta Horizon worlds; rolling out to Horizon creators 2025+.
- Not a general public API as of 2026-05.

### Luma Genie

- Supports text-to-3D, image-to-3D, and video-to-3D.
- Video-to-3D: excellent for capturing real objects from phone video.
- Text prompts respond well to descriptive language about shape and form.
- 3D Gaussian Splatting output for photorealistic rendering.
- Requires conversion to mesh for game engine use.

## Negative Constraints

Include these to avoid common AI generation artifacts:

| Issue | Negative Constraint Phrase |
|-------|--------------------------|
| Janus (multi-face) | "single continuous surface, no duplicate features, consistent from all angles" |
| Floating geometry | "no floating parts, all geometry connected, single solid mesh" |
| Internal faces | "no internal faces, clean exterior surface only, no hidden geometry" |
| Excessive detail | "game-ready detail level, no micro-geometry, clean silhouette" |
| Broken symmetry | "symmetrical design, mirror symmetry on central axis" |
| Scale ambiguity | Include explicit size reference and context |
| Z-fighting | "no coplanar faces, no overlapping surfaces" |
| Self-intersection | "no self-intersecting geometry, clean mesh" |
| Disconnected parts | "single connected mesh, no separate floating pieces" |

### Negative Prompt Template

```
[Positive prompt],
no floating geometry, no internal faces,
single continuous mesh, consistent appearance from all angles,
game-ready topology, no micro-detail noise
```

## Style Transfer Techniques

### Style Vocabulary

| Style | Keywords | Best Provider | Use Case |
|-------|----------|---------------|----------|
| Stylized/Cartoon | "stylized, cartoon, cel-shaded, bold colors" | Meshy, Tripo | Mobile games, casual |
| Low-poly | "low-poly, flat shaded, geometric, faceted" | Meshy (low-poly mode), Sloyd | Retro games, minimalist |
| Realistic/PBR | "photorealistic, PBR materials, detailed surface" | Rodin, Hunyuan3D 2.0 | AAA games, archviz |
| Hand-painted | "hand-painted textures, painterly, diffuse-only" | Meshy, Tripo | World of Warcraft style |
| Voxel | "voxelized, blocky, minecraft-style, cubic" | Meshy | Voxel games |
| Pixel art 3D | "pixel art style, low resolution textures, retro" | Meshy | Retro-3D, indie |
| Anime/Manga | "anime style, cel-shaded, Japanese animation" | Rodin, Tripo | Anime games, VTuber |
| Sci-fi | "futuristic, sci-fi, metallic, holographic" | Rodin, Meshy | Sci-fi games |
| Fantasy | "fantasy, magical, enchanted, mystical" | Meshy, Rodin | RPG games |

### Style Consistency Across Assets

For consistent style across multiple assets in a project:

```
# Define a style template
STYLE_TEMPLATE = """
{subject},
stylized hand-painted textures with warm color palette,
slightly exaggerated proportions, rounded edges,
game-ready for Unity, clean topology,
consistent with medieval fantasy art direction
"""

# Generate variants
prompts = [
    STYLE_TEMPLATE.format(subject="Wooden barrel with metal bands"),
    STYLE_TEMPLATE.format(subject="Stone well with wooden roof"),
    STYLE_TEMPLATE.format(subject="Market stall with canvas awning"),
]
```

## Image-to-3D Reference Preparation

### Optimal Input

1. **Multi-view images** (best): front, side, back, 3/4 angle.
2. **Single image** (acceptable): front or 3/4 view with clean background.
3. **Turntable video** (for Luma): smooth rotation around object.

### Image Requirements

| Requirement | Specification |
|-------------|--------------|
| Background | White, solid color, or transparent |
| Lighting | Even, diffuse, no harsh shadows |
| Subject fill | 70-80% of frame |
| Resolution | 512x512 minimum, 1024x1024 recommended |
| Format | PNG (preferred) or JPEG (quality 95+) |
| Ground shadows | Remove or minimize |
| Occlusion | Avoid heavy self-occlusion |
| Color consistency | Same white balance across views |
| Orientation | Subject upright, facing camera |

### AI Image-to-3D Pipeline (Sketch -> Clay)

When receiving images from Sketch agent (Gemini API):

```python
def prepare_sketch_output_for_3d(image_path: str, output_path: str):
    """Prepare Sketch-generated image for image-to-3D.

    Sketch generates images that may need preprocessing:
    1. Background removal
    2. Centering and scaling
    3. Resolution adjustment
    """
    from PIL import Image
    import numpy as np

    img = Image.open(image_path).convert("RGBA")

    # Simple background removal (white background)
    data = np.array(img)
    white_threshold = 240
    mask = np.all(data[:, :, :3] > white_threshold, axis=2)
    data[mask, 3] = 0  # Make white pixels transparent

    # Center and crop to subject
    alpha = data[:, :, 3]
    rows = np.any(alpha > 0, axis=1)
    cols = np.any(alpha > 0, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]

    # Add padding (15% of larger dimension)
    h, w = rmax - rmin, cmax - cmin
    pad = int(max(h, w) * 0.15)
    rmin = max(0, rmin - pad)
    rmax = min(data.shape[0], rmax + pad)
    cmin = max(0, cmin - pad)
    cmax = min(data.shape[1], cmax + pad)

    cropped = data[rmin:rmax, cmin:cmax]

    # Resize to 1024x1024
    result = Image.fromarray(cropped)
    result = result.resize((1024, 1024), Image.Resampling.LANCZOS)
    result.save(output_path, "PNG")
```

### Multi-View Consistency

For multi-view input (Tripo, Rodin):
- Use consistent lighting across all views.
- Maintain consistent color/exposure.
- Keep the same camera height and distance.
- Use turntable-style rotation (every 90 degrees for 4 views, every 45 for 8).
- Ensure the object is centered in frame across all views.
- Use the same focal length/FOV for all views.

## Multi-View Consistency and Janus Problem

The "Janus problem" occurs when SDS-based (Score Distillation Sampling) methods create models with duplicate features (e.g., two faces on a character). Mitigation strategies:

1. **Use multi-view aware providers**: Hunyuan3D 2.0, Trellis, and newer Tripo/Meshy models use multi-view diffusion (MVDream, Zero123++) which largely eliminates Janus artifacts.
2. **Specify view consistency**: "consistent appearance from all angles, single face only".
3. **Use FlexiCubes extraction**: Produces more coherent surfaces than naive marching cubes.
4. **Provide multi-view reference images**: Constrains generation to consistent geometry.
5. **Validate with multi-view render**: Always render 4+ views before accepting the model.
6. **Prefer newer providers**: 2025+ generation models have largely solved this issue.

## Prompt Chaining for Complex Assets

For complex assets that need multiple generation passes:

```python
# Step 1: Generate base shape
base_prompt = """
Medieval stone tower, cylindrical shape,
3 stories with arched windows,
clean exterior surface, solid geometry,
game environment piece, 10 meters tall
"""

# Step 2: Generate decorative elements separately
details = [
    "Stone gargoyle perched on a ledge, small prop, 30cm tall",
    "Wooden door with iron studs, flat prop, 2m x 1m",
    "Banner flag on a pole, cloth simulation ready, 1m long",
]

# Step 3: Combine in Blender (code generated by Clay)
# - Import base tower
# - Import detail pieces
# - Position and attach
# - Merge or keep as hierarchy
# - Export as single asset or LOD-friendly group
```

## Example Prompt Library

### Characters

```
# Stylized character (casual/mobile game)
Chibi fantasy warrior character, large head proportions,
simple armor with sword and shield, stylized cartoon aesthetic,
bright saturated colors, clean topology for rigging,
T-pose, game-ready, approximately 1000 triangles

# Realistic character (AAA/mid-core)
Realistic medieval knight in full plate armor,
detailed surface with scratches and wear, PBR materials,
A-pose for rigging, high detail for hero asset,
approximately 180cm tall, 30000 triangle budget

# NPC / background character
Simple villager NPC, medieval clothing,
low-poly with hand-painted textures,
game-ready background character, 2000 triangle budget,
no complex accessories, clean silhouette

# Creature
Fantasy dragon with spread wings,
stylized proportions, scales texture,
game-ready with clean topology,
wingspan approximately 3 meters, idle pose
```

### Props

```
# Simple prop
Wooden barrel with metal bands,
low-poly stylized, hand-painted texture look,
game-ready prop, approximately 1 meter tall,
no internal geometry, single mesh

# Interactive prop
Ornate treasure chest with gold trim and gemstones,
semi-realistic style, clean quad topology,
openable lid as separate mesh, hinge point clearly defined,
prop scale 80cm wide, 2000 triangle budget

# Weapon
Fantasy sword with ornate handle and glowing runes,
stylized game asset, clean topology,
no floating geometry, symmetrical blade,
120cm total length, held in one hand

# Food / consumable
Roasted chicken on a wooden plate,
stylized hand-painted look, warm colors,
simple prop for inventory UI or table decoration,
30cm wide, under 500 triangles
```

### Environment

```
# Nature element
Stylized oak tree with thick trunk and full canopy,
low-poly foliage cards arranged in clusters,
game environment asset, LOD-friendly silhouette,
approximately 5 meters tall, no internal geometry

# Building
Medieval stone cottage with thatched roof,
modular walls and roof as separate pieces,
stylized game environment, hand-painted textures,
approximately 4 meters wide, tileable wall sections

# Terrain feature
Rocky cliff face with moss and vines,
stylized game terrain piece, tileable edges,
approximately 5 meters wide, flat back for placement,
LOD chain friendly, no floating rocks

# Interior
Wooden bookshelf filled with colorful books,
stylized fantasy library style, warm lighting bake,
game prop for indoor scenes, 2 meters tall,
books as texture, not individual geometry
```

### Vehicles

```
# Fantasy vehicle
Steampunk airship with propellers and wooden hull,
stylized game asset, clean topology,
approximately 15 meters long, no internal geometry,
visible deck with simple details, floating orientation

# Realistic vehicle
Military jeep with canvas top and mounted spotlight,
realistic proportions and PBR surface detail,
game-ready vehicle, LOD-appropriate detail,
4 meters long, separate wheel meshes for animation

# Mount / rideable
Fantasy horse with ornate saddle and armor,
stylized medieval game mount,
rigging-ready with clean joint areas,
1.6 meters at shoulder height, walk/run animation ready
```

## Prompt Iteration Strategy

1. **Start with a draft prompt** (30 words) and generate 1-3 previews.
2. **Evaluate results** using multi-view renders (front, side, back, 3/4).
3. **Identify issues**: check for Janus, floating geometry, scale, style match.
4. **Refine by category**:
   - Shape wrong -> adjust subject description
   - Style wrong -> adjust style/material terms
   - Topology wrong -> adjust topology constraints
   - Scale wrong -> add explicit dimensions
5. **Lock the prompt** when results are acceptable.
6. **Generate full quality** using refine/high mode.
7. **Document the final prompt** in metadata JSON for reproducibility.

### Iteration Decision Tree

```
Result OK? -> Accept and proceed to pipeline
  |
  No -> What's wrong?
  |
  Shape/Form -> Rewrite subject layer, try different angle words
  Style/Look -> Change art_style parameter or style keywords
  Artifacts -> Add negative constraints, try different provider
  Too complex -> Simplify prompt, remove conflicting terms
  Janus issue -> Add "consistent from all angles", use multi-view provider
  Scale wrong -> Add explicit dimensions in meters/cm
```

## Provider Prompt Compatibility Matrix (2026)

| Prompt Feature | Meshy 6 | Tripo P1/H3.1 | Hunyuan3D 3.0/3.1 | Rodin Gen-2 | Sloyd 2.0 | SPAR3D / TRELLIS.2 |
|---------------|---------|---------------|-------------------|-------------|-----------|--------------------|
| Detailed descriptions | Good (≤800 chars) | Medium | Good | Excellent | Poor | N/A (image-only) |
| Style keywords | Excellent | Good | Good | Excellent | Medium | N/A |
| Material descriptions | Excellent | Good | Good (4K PBR) | Good | Poor | N/A |
| Topology instructions | Good (Low Poly Mode) | Medium (P1.0 quad-dom.) | Medium | Medium (quad) | Excellent | N/A |
| Size/scale in prompt | Medium | Medium | Medium | Good | Good | N/A |
| Negative prompts | Good | Poor | Medium | Medium | Poor | N/A |
| Reference style | Medium | Good | Medium | Excellent | Poor | N/A |
| Short prompts (<30w) | Good | Excellent | Good | Good | Excellent | N/A |
| Long prompts (>100w) | Good | Poor | Medium | Good | Poor | N/A |
