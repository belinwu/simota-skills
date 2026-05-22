# Texture Baking Reference

Purpose: Bake high-poly detail into low-poly PBR texture maps. Cover normal (tangent space + object space), AO, curvature, height, position, ID, metallic, roughness; cage-based projection; xNormal, Substance Painter, Marmoset Toolbag, Blender, and Substance Automation Toolkit.

## Scope Boundary

- **clay `baking`**: PBR texture baking high → low poly (this document).
- **clay `text` / `image` (elsewhere)**: Mesh generation.
- **clay `retopo` (elsewhere)**: Low-poly creation before baking.
- **clay `uv` (elsewhere)**: UV layout before baking.
- **clay `rigging` / `retarget` (elsewhere)**: Skeleton / animation (orthogonal).
- **Builder (elsewhere)**: Engine integration code.

## Why Bake

Modern PBR pipelines: high-poly sculpt has all detail → bake into texture maps that drive shaders on a low-poly game-ready mesh. Result: cinematic-looking models that render fast.

## PBR Map Inventory

| Map | Purpose | Channel | Bit depth |
|-----|---------|---------|-----------|
| **Normal (tangent)** | Surface detail (bumps / wrinkles) | RGB | 8-bit / 16-bit |
| **Normal (object)** | World-space normals | RGB | 8-bit / 16-bit |
| **AO (ambient occlusion)** | Shadows in crevices | R (single channel) | 8-bit |
| **Curvature** | Edge wear / sharpness | R | 8-bit |
| **Height / Displacement** | Tessellation / parallax | R | 16-bit / 32-bit |
| **Position (world)** | Per-pixel world-space | RGB | 16-bit / 32-bit |
| **ID / Color** | Region masking | RGB | 8-bit |
| **Albedo / Base Color** | Diffuse color | RGB | 8-bit (sRGB) |
| **Metallic** | Metal vs dielectric | R | 8-bit |
| **Roughness** | Microsurface | R | 8-bit |
| **Emissive** | Self-illumination | RGB | 8-bit / 16-bit |
| **Thickness** | SSS depth | R | 8-bit |

Game engines typically pack: `Roughness + Metallic + AO` into a single RGB texture (channel pack) to save memory.

## Tangent vs Object Space Normal

| | Tangent Space | Object Space |
|---|--------------|--------------|
| **Use** | Most game characters / props | Vehicles / static rigid models |
| **UV requirement** | Standard UV with tangents | UV (tangents not required) |
| **Mirror UV** | Works | Breaks (requires per-shell flip) |
| **Animation** | Works (deforms with mesh) | Requires custom shader |

Default to tangent space. Object space for static rigid (cars, walls).

## Cage-Based Projection

Cage = expanded version of low-poly used to define the search volume for ray-casting from low → high.

```
LOW POLY (target UV)  →  CAGE (expanded)  →  raycast outward to HIGH POLY
                                              capture detail at hit point
```

Without cage: ray distance estimated → artifacts at curved areas.
With cage: ray distance defined per-vertex → clean projection.

Major bakers (xNormal, Substance, Marmoset, Blender) all support cages.

## xNormal (free Windows; gold standard)

```
Workflow:
1. Load low-poly OBJ (with UVs + tangents)
2. Load high-poly OBJ
3. Optional: load cage OBJ
4. Configure maps + bit depth
5. Bake
```

Supports: Normal (tangent + object), AO, Cavity, Convexity, Heightmap, Vertex Color, Wireframe + Ray distance, Bent Normal.

## Substance Painter (commercial; texture authoring)

Latest: **Substance 3D Painter 12.0** (unveiled at GDC 2026, Mar 2026). 2025 added an experimental fully-automatic cage generation option for high-poly bake. 12.1 Beta adds Mesh-Map Bakers sync across Texture Sets (link icon), copy/paste baker settings across Texture Sets, in-context "jump to setting" error messages from the Baking Log, and split of Mesh Map vs Common Baking settings.

```
1. New project: bake mesh maps from high-poly
2. Mesh Maps panel: Normal, AO, Curvature, Position, Thickness, ID
3. Apply smart materials that use mesh maps for procedural detail
4. Export channel-packed PBR textures per engine preset (Unity / UE / glTF)
```

## Marmoset Toolbag

Highest-quality tangent normals; real-time interactive bake preview. Standard for AAA character pipelines.

Latest releases:
- **Toolbag 5.0** (official release 2024-10) — introduced interactive baking with real-time preview of bake output, plus UDIM workflow support for create / bake / render of UDIM-laid materials.
- **Toolbag 5.01** (2024-12-16) and **Toolbag 5.02** (2025-08-14) — Toolbag 5.02 added **low-to-low baking** (bake textures directly from a low-poly mesh — useful for baking down bevel-shader data without duplicating the low mesh into the High slot).

```
1. New Baker
2. Load High + Low + Cage
3. Configure maps + skew adjustment
4. Bake with real-time preview
```

## Blender (free; Cycles + Eevee bake)

```python
import bpy

def bake_normal_map(low_obj, high_obj, output_path, resolution=2048):
    # Select high-poly first, then low-poly active
    bpy.ops.object.select_all(action='DESELECT')
    high_obj.select_set(True)
    low_obj.select_set(True)
    bpy.context.view_layer.objects.active = low_obj

    # Setup image to bake into
    img = bpy.data.images.new(
        "normal_bake", width=resolution, height=resolution,
        alpha=False, float_buffer=True
    )

    # Add Image Texture node to low-poly material, link to bake
    mat = low_obj.active_material
    nodes = mat.node_tree.nodes
    img_node = nodes.new("ShaderNodeTexImage")
    img_node.image = img
    nodes.active = img_node

    # Bake settings
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.bake_type = 'NORMAL'
    scene.render.bake.use_selected_to_active = True
    scene.render.bake.use_cage = True
    scene.render.bake.cage_extrusion = 0.05
    scene.render.bake.normal_space = 'TANGENT'

    bpy.ops.object.bake(type='NORMAL')
    img.save_render(filepath=output_path)

# Usage
high = bpy.data.objects["high_poly"]
low = bpy.data.objects["low_poly"]
bake_normal_map(low, high, "/tmp/normal.exr", resolution=2048)
```

Other map types: change `bake_type` to `AO`, `DIFFUSE`, `EMIT`, etc.

## Substance Automation Toolkit (SAT) — pipeline scripting

```python
# pysbs: Substance Designer / Painter automation
from pysbs.batchtools import sbsbaker

sbsbaker.bake(
    input_mesh="low.fbx",
    high_def_mesh="high.fbx",
    output_path="textures/",
    output_size=2048,
    map_types=["normal_world_space", "ambient_occlusion", "curvature"]
)
```

For batch / CI / large asset libraries.

## Bake Settings Discipline

| Setting | Default | Notes |
|---------|---------|-------|
| Resolution | 2048 (mid), 4096 (hero) | Power of 2 |
| Anti-aliasing | 4× samples for AO; 1× for normal | AO benefits more |
| Edge padding | 16 px | Prevents seam visibility on mip-maps |
| Tangent basis | MikkTSpace | Standard for engine-compat |
| Bit depth (normal) | 8-bit OK; 16-bit if banding | Storage doubles |
| Cage extrusion | 0.05–0.5 (model-specific) | Test both extremes |
| Ray distance | Auto with cage | Cage replaces it |
| Sub-mesh isolation | "Match by Name" | Prevents cross-mesh bleed |

## Channel Packing per Engine

| Engine | Pack |
|--------|------|
| Unity URP | R=Metallic, G=Occlusion, B=(unused), A=Smoothness |
| Unity HDRP | R=Metallic, G=Occlusion, B=Detail, A=Smoothness |
| Unreal Engine | R=AO, G=Roughness, B=Metallic (ORM convention) |
| glTF 2.0 | G=Roughness, B=Metallic (single texture) |
| Godot 4 | Roughness, Metallic separate textures |

Always validate channel packing against the target engine's standard.

## MikkTSpace (Tangent Basis)

The standard tangent calculation algorithm. All major bakers + engines use it (Unity, UE, glTF, Blender, Substance, xNormal). If your bake source and target engine use different tangent algorithms, normal maps look wrong.

Always verify "MikkTSpace" or "Tangent Space: same as engine" in baker.

## Workflow

```
PREP         →  high-poly (sculpt or AI generate)
             →  low-poly (clay `retopo` output)
             →  UV layout (clay `uv` output)
             →  optional cage (low-poly extruded)

PIPELINE     →  pick: xNormal (free) / Substance Painter (auth) / Marmoset (AAA) / Blender (free)
             →  per asset budget

MAP LIST     →  required: Normal, AO, Curvature, ID
             →  optional: Position, Height, Thickness
             →  PBR: Albedo, Metallic, Roughness from authoring after bake

BAKE         →  resolution per asset tier (1K UI, 2K mid, 4K hero)
             →  4× AA on AO
             →  16 px edge padding
             →  MikkTSpace tangents

VALIDATE     →  no seam visibility at mip-maps
             →  no normal-map flipped (engine sees same handedness)
             →  AO not over-darkening crevices
             →  curvature usable for edge-wear masks

CHANNEL PACK →  per engine convention
             →  Unity: Metal_AO_Smoothness or Mask Map
             →  UE: ORM
             →  glTF: G=Rough B=Metal

AUTHORING    →  Substance Painter / Mari / 3D Coat over baked maps
             →  produces final Albedo + Roughness + Metallic + Emissive

EXPORT       →  per-engine textures (channel-packed)
             →  per-engine material defs (.mat / .uasset)

VALIDATE     →  in-engine render preview matches sculpt look
             →  performance: texture memory footprint

HANDOFF      →  Builder: shader / material integration
             →  clay `game`: pipeline integration
             →  clay `rigging`: rig now that mesh is final
             →  Realm: in-game asset integration
```

## Output Template

```markdown
## Bake Plan: [Asset]

### Inputs
- High-poly: [path] [polycount]
- Low-poly: [path] [polycount]
- UV: [path] [layout summary]
- Cage: [path / N/A]

### Tooling
- Primary baker: [xNormal / Substance Painter / Marmoset / Blender / SAT]
- Tangent basis: MikkTSpace

### Bake Map Inventory
| Map | Resolution | Bit | Anti-alias | Pack |
|-----|-----------|-----|-----------|------|
| Normal (tangent) | 2048 | 8-bit | 1× | individual |
| AO | 2048 | 8-bit | 4× | G of Mask Map |
| Curvature | 2048 | 8-bit | 4× | masks for edge wear |
| ID | 2048 | 8-bit | 1× | regions |
| Position | 1024 | 16-bit | 1× | gradient masks |
| Thickness | 1024 | 8-bit | 4× | SSS |

### Channel Pack (Engine: [Unity / UE / glTF])
| Texture | R | G | B | A |
|---------|---|---|---|---|
| Mask Map | Metallic | Occlusion | Detail | Smoothness |

### Baker Code
[Python / xNormal / Substance script]

### Validation
- [ ] No seam visibility at mip-3
- [ ] Normal direction matches engine (Y+ vs Y-)
- [ ] AO crevices not over-darkened
- [ ] Curvature usable as edge mask
- [ ] Mip-maps clean (16 px padding effective)
- [ ] Texture memory: [N MB] within budget

### Handoffs
- Builder: shader / material integration
- clay `game`: pipeline integration
- clay `rigging`: rig now that geo is final
- Realm: in-game integration
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| No cage on curved surfaces | Use cage; ray-distance alone fails on corners |
| Mismatched tangent basis (MikkTSpace vs custom) | Use MikkTSpace everywhere |
| Mirror UV on tangent-space normal | Move mirrored shells to UV V > 1 island |
| Single normal-map for all LODs | Bake per-LOD; LOD3 needs softer normal |
| 4K everywhere by default | 1K UI, 2K mid, 4K hero only |
| AO in albedo (legacy) | Separate AO map; PBR convention |
| 8-bit normal with banding | Bake 16-bit, store 8-bit only if confirmed clean |
| Edge padding < 8 px | 16 px standard; visible seams at mip-3 otherwise |
| Bake all maps every iteration | Bake quick (Normal + AO) for early; full set at final |
| Triangulate after bake | Triangulate before bake; tris differ from quads in tangent space |
| Cross-mesh bleed (eyes pick up shirt) | Match-by-name or per-mesh isolation |
| Object-space normal for skinned mesh | Tangent-space mandatory for deformation |
| Channel pack ignored (loose textures) | Always pack per engine convention |
| Roughness baked from sculpt micro-surface | Roughness is authored, not baked |
| Skipping in-engine preview | Bake looks different in Painter vs game; verify in target engine |

## Deliverable Contract

When `baking` completes, emit:

- **Inputs** (high / low / UV / cage paths + counts).
- **Tooling** + tangent basis.
- **Bake map inventory** with resolution / bit depth / AA.
- **Channel pack** per target engine.
- **Baker code** (xNormal / Substance / Marmoset / Blender / SAT).
- **Validation** checklist (seams / direction / mips / budget).
- **Handoffs**: Builder, clay game, clay rigging, Realm.

## References

- xNormal — xnormal.net (Santiago Orgaz; free)
- Substance Painter — adobe.com/products/substance3d-painter (12.0 unveiled GDC 2026; 2025 added experimental auto cage; 12.1 Beta added Mesh-Map Bakers sync across Texture Sets)
- Marmoset Toolbag — marmoset.co/toolbag (5.0 official Oct 2024 — interactive baking + UDIM; 5.02 Aug 2025 — low-to-low baking)
- Polycam 2D Texture Generator — poly.cam (Stable-Diffusion-driven seamless tileable PBR — albedo/displacement/normal/roughness — royalty-free commercial license, 768/1024/1536 px)
- Blender Cycles bake — docs.blender.org/manual (Blender 4.5 LTS supported until July 2027; Blender 5.0 released 2025-11-18 with ACES, HDR, Volumes + SDF Geometry Nodes)
- Substance Automation Toolkit (SAT) — adobe.com/products/substance3d-sat
- MaterialX 1.39.4 (Sep 2025) — materialx.org (OpenPBR support; WebGPU Shading Language; hex-tiled + lat-long images; NanoColor; animated materials). Maya 2025.3+ ships OpenPBR by default; 3ds Max 2026 makes OpenPBR the default surface shader.
- MikkTSpace — github.com/mmikk/MikkTSpace (Morten Mikkelsen)
- "Mikkelsen Tangent Space" — original paper
- *Real-Time Rendering* (4th ed.) — Akenine-Möller, Haines, Hoffman
- *Physically Based Rendering: From Theory to Implementation* — Pharr, Jakob, Humphreys
- glTF 2.0 specification — github.com/KhronosGroup/glTF
- Unity HDRP / URP material spec — docs.unity3d.com
- Unreal Engine ORM convention — docs.unrealengine.com
- "Toolbag Baker Documentation" — Marmoset
- "PBR Guide" — Allegorithmic / Substance (legacy archive)
- "Crafting a Next-Gen Material Pipeline for The Order: 1886" — Ready at Dawn (GDC)
- Polycount wiki — polycount.com (community knowledge)
- 3D Coat — 3dcoat.com (alternative authoring)
- Mari (Foundry) — foundry.com/products/mari
- "Filament" — Google PBR rendering engine (open source reference for PBR math)
