# Game Pipeline Reference

Full pipeline from AI generation to engine-ready assets: LOD, retopology, UV packing, texture baking, and engine import.

## Full Pipeline Overview

```
AI Generation -> QC Check -> Retopology -> UV Unwrap -> Texture Bake -> LOD Generation -> Rig (optional) -> Engine Import
```

Each step produces code (Blender Python or pipeline scripts), not manual instructions.

## LOD (Level of Detail) Generation

### Blender Decimate LOD Script

```python
import bpy
from pathlib import Path

def generate_lod_chain(obj_name: str, output_dir: str,
                       lod_ratios: list = None, export_format: str = "fbx"):
    """Generate LOD chain using Blender's decimate modifier.

    Args:
        obj_name: Name of the source mesh object.
        lod_ratios: Reduction ratios per LOD level (e.g., [1.0, 0.5, 0.25, 0.1, 0.05]).
        export_format: "fbx" or "gltf".
    """
    if lod_ratios is None:
        lod_ratios = [1.0, 0.5, 0.25, 0.1, 0.05]

    src = bpy.data.objects[obj_name]
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    for i, ratio in enumerate(lod_ratios):
        # Duplicate
        bpy.ops.object.select_all(action='DESELECT')
        src.select_set(True)
        bpy.context.view_layer.objects.active = src
        bpy.ops.object.duplicate()
        lod_obj = bpy.context.active_object
        lod_obj.name = f"{obj_name}_lod{i}"

        if ratio < 1.0:
            mod = lod_obj.modifiers.new(f"Decimate_LOD{i}", 'DECIMATE')
            mod.ratio = ratio
            bpy.ops.object.modifier_apply(modifier=mod.name)

        # Report
        tri_count = sum(len(p.vertices) - 2 for p in lod_obj.data.polygons)
        print(f"LOD{i}: ratio={ratio}, tris={tri_count}")

        # Export
        bpy.ops.object.select_all(action='DESELECT')
        lod_obj.select_set(True)
        bpy.context.view_layer.objects.active = lod_obj

        filepath = str(out / f"{obj_name}_lod{i}")
        if export_format == "fbx":
            bpy.ops.export_scene.fbx(
                filepath=filepath + ".fbx",
                use_selection=True, use_mesh_modifiers=True,
                mesh_smooth_type='FACE', path_mode='COPY', embed_textures=True,
            )
        else:
            bpy.ops.export_scene.gltf(
                filepath=filepath + ".glb",
                use_selection=True, export_format='GLB',
                export_draco_mesh_compression_enable=True,
            )

        # Remove duplicate
        bpy.ops.object.delete(use_global=False)
```

### LOD Distance Thresholds

| LOD Level | Typical Ratio | Screen Coverage | Use Case |
|-----------|--------------|-----------------|----------|
| LOD0 | 100% | > 50% screen | Close-up, hero view |
| LOD1 | 50% | 25-50% screen | Mid-range |
| LOD2 | 25% | 10-25% screen | Background |
| LOD3 | 10% | 5-10% screen | Far distance |
| LOD4 | 5% | < 5% screen | Extreme distance / impostor candidate |

### Unity LOD Group Script

```csharp
// C# reference for Unity LOD Group setup
// Clay generates this as a code template, not executed directly
/*
LODGroup lodGroup = gameObject.AddComponent<LODGroup>();
LOD[] lods = new LOD[4];
lods[0] = new LOD(0.6f, new Renderer[] { lod0Renderer });
lods[1] = new LOD(0.3f, new Renderer[] { lod1Renderer });
lods[2] = new LOD(0.1f, new Renderer[] { lod2Renderer });
lods[3] = new LOD(0.01f, new Renderer[] { lod3Renderer });
lodGroup.SetLODs(lods);
lodGroup.RecalculateBounds();
*/
```

## Retopology

### Blender Auto-Retopo (Voxel Remesh + QuadriFlow)

```python
import bpy

def auto_retopo(obj_name: str, target_faces: int = 5000, method: str = "voxel"):
    """Automatic retopology using Blender's built-in tools.

    Args:
        method: "voxel" for voxel remesh, "quadriflow" for quad-based.
    """
    obj = bpy.data.objects[obj_name]
    bpy.context.view_layer.objects.active = obj

    if method == "voxel":
        # Voxel remesh - good for organic shapes
        mod = obj.modifiers.new("Remesh", 'REMESH')
        mod.mode = 'VOXEL'
        # Estimate voxel size from target face count
        bbox = obj.dimensions
        volume = bbox.x * bbox.y * bbox.z
        mod.voxel_size = (volume / target_faces) ** (1/3) * 2
        bpy.ops.object.modifier_apply(modifier=mod.name)

    elif method == "quadriflow":
        # QuadriFlow - produces clean quad topology
        bpy.ops.object.quadriflow_remesh(
            target_faces=target_faces,
            use_preserve_sharp=True,
            use_preserve_boundary=True,
        )

    tri_count = sum(len(p.vertices) - 2 for p in obj.data.polygons)
    print(f"Retopo complete: {tri_count} tris (target: {target_faces})")
```

## UV Unwrapping and Packing

### Blender UV Unwrap Script

```python
import bpy

def auto_uv_unwrap(obj_name: str, method: str = "smart", margin: float = 0.005):
    """Automatic UV unwrapping.

    Args:
        method: "smart" for Smart UV Project, "angle" for angle-based.
        margin: Island margin (target >80% UV space utilization).
    """
    obj = bpy.data.objects[obj_name]
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')

    if method == "smart":
        bpy.ops.uv.smart_project(
            angle_limit=66.0,
            margin_method='SCALED',
            island_margin=margin,
            scale_to_bounds=True,
        )
    elif method == "angle":
        bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=margin)

    bpy.ops.object.mode_set(mode='OBJECT')

    # Report UV coverage
    uv_layer = obj.data.uv_layers.active
    if uv_layer:
        coverage = estimate_uv_coverage(obj)
        print(f"UV coverage: {coverage:.1%}")
        if coverage < 0.80:
            print("WARNING: UV coverage below 80% target. Consider repacking.")


def estimate_uv_coverage(obj: bpy.types.Object) -> float:
    """Estimate UV space utilization (0.0-1.0)."""
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    uv_layer = bm.loops.layers.uv.active
    if not uv_layer:
        bm.free()
        return 0.0

    total_uv_area = 0.0
    for face in bm.faces:
        uvs = [loop[uv_layer].uv for loop in face.loops]
        # Shoelace formula for polygon area
        n = len(uvs)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += uvs[i].x * uvs[j].y - uvs[j].x * uvs[i].y
        total_uv_area += abs(area) / 2.0

    bm.free()
    return min(total_uv_area, 1.0)
```

## Texture Baking

### Texture Atlas Generation

```python
import bpy

def bake_texture_maps(obj_name: str, output_dir: str, resolution: int = 2048):
    """Bake PBR texture maps (albedo, normal, roughness/metallic)."""
    from pathlib import Path
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    obj = bpy.data.objects[obj_name]
    bpy.context.view_layer.objects.active = obj
    bpy.context.scene.render.engine = 'CYCLES'

    maps_to_bake = [
        ("DIFFUSE", f"{obj_name}_albedo.png"),
        ("NORMAL", f"{obj_name}_normal.png"),
        ("ROUGHNESS", f"{obj_name}_roughness.png"),
    ]

    for bake_type, filename in maps_to_bake:
        # Create bake target image
        img = bpy.data.images.new(filename, resolution, resolution)

        # Create image texture node in material
        for mat_slot in obj.material_slots:
            mat = mat_slot.material
            if not mat or not mat.use_nodes:
                continue
            nodes = mat.node_tree.nodes
            tex_node = nodes.new('ShaderNodeTexImage')
            tex_node.image = img
            tex_node.select = True
            nodes.active = tex_node

        # Bake
        bpy.ops.object.bake(type=bake_type)
        img.filepath_raw = str(out / filename)
        img.file_format = 'PNG'
        img.save()
        print(f"Baked: {filename} ({resolution}x{resolution})")
```

### Draw Call Reduction via Atlasing

Combine multiple small textures into a single atlas to reduce draw calls:

| Scenario | Without Atlas | With Atlas | Improvement |
|----------|--------------|------------|-------------|
| 20 unique props | 20 draw calls | 1-2 draw calls | ~10-20x |
| 50 environment objects | 50 draw calls | 3-5 draw calls | ~10-17x |

Target: keep total draw calls under 200 for mobile, under 2000 for PC.

## Engine Export Settings

### FBX (Unity / Unreal Engine)

```python
def export_for_unity(obj_name: str, output_path: str):
    """Export with Unity-optimized FBX settings."""
    obj = bpy.data.objects[obj_name]
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    bpy.ops.export_scene.fbx(
        filepath=output_path,
        use_selection=True,
        apply_scale_options='FBX_SCALE_ALL',
        axis_forward='-Z',
        axis_up='Y',
        use_mesh_modifiers=True,
        mesh_smooth_type='FACE',
        path_mode='COPY',
        embed_textures=True,
        bake_anim=False,
    )
```

### glTF (Web / Mobile)

```python
def export_for_web(obj_name: str, output_path: str, draco: bool = True):
    """Export with web-optimized glTF settings."""
    obj = bpy.data.objects[obj_name]
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    bpy.ops.export_scene.gltf(
        filepath=output_path,
        use_selection=True,
        export_format='GLB',
        export_draco_mesh_compression_enable=draco,
        export_draco_mesh_compression_level=6,
        export_image_format='WEBP',
        export_apply=True,
    )
```

## FlexiCubes (NVIDIA)

FlexiCubes is the current recommended approach for differentiable mesh extraction from neural fields. It produces significantly better topology than naive marching cubes.

Key advantages over marching cubes:
- Adaptive resolution at surface boundaries.
- Flexible vertex positioning (not grid-locked).
- Differentiable, so it integrates into training pipelines.
- Produces cleaner quad-dominant topology.

When generating code that involves mesh extraction from neural representations (NeRF, SDF networks), prefer FlexiCubes over marching cubes when the user's pipeline supports it.

```python
# FlexiCubes is available via NVIDIA Kaolin or standalone
# pip install kaolin

# Conceptual usage pattern:
# 1. Train neural field (SDF or occupancy)
# 2. Extract mesh with FlexiCubes
# 3. Fine-tune mesh with differentiable rendering
# 4. Export final mesh

# For detailed FlexiCubes implementation, refer to:
# https://github.com/nv-tlabs/FlexiCubes
```

## MaterialX / OpenPBR

For interchange between DCC tools, use MaterialX with OpenPBR shading model:

```xml
<?xml version="1.0"?>
<materialx version="1.39">
  <open_pbr_surface name="game_material" type="surfaceshader">
    <input name="base_color" type="color3" value="0.8, 0.6, 0.4" />
    <input name="base_metalness" type="float" value="0.0" />
    <input name="specular_roughness" type="float" value="0.5" />
  </open_pbr_surface>
</materialx>
```

## Platform Budgets

| Platform | Verts/Scene | Tris/Model (avg) | Texture Memory | Draw Calls |
|----------|------------|-------------------|----------------|------------|
| Mobile | < 100K | < 5K | < 128MB VRAM | < 200 |
| Web (mid-range) | < 500K | < 20K | < 256MB | < 500 |
| PC (mid-range) | < 3M | < 100K | < 2GB VRAM | < 2000 |
| PC (high-end) | < 10M | < 500K | < 4GB VRAM | < 5000 |
| Console (current gen) | < 5M | < 200K | < 4GB VRAM | < 3000 |

Rules:
- Always validate total scene budget, not just per-model.
- LOD0 uses the per-model budget; subsequent LODs reduce by 50-75% each level.
- Texture resolution scales with model importance: hero=2048, standard=1024, background=512.
