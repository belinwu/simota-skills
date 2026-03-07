# Code Patterns Reference

Templates and conventions for 3D modeling code across Blender Python, Three.js, Babylon.js, OpenSCAD, and SDF.

## Blender Python (bpy)

### Scene Setup

```python
import bpy
import math

def clear_scene():
    """Remove all objects from the current scene."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    # Clear orphan data
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)

def setup_scene(camera_distance: float = 5.0):
    """Set up a clean scene with camera and light."""
    clear_scene()

    # Camera
    bpy.ops.object.camera_add(location=(camera_distance, -camera_distance, camera_distance))
    cam = bpy.context.object
    cam.rotation_euler = (math.radians(55), 0, math.radians(45))
    bpy.context.scene.camera = cam

    # Sun light
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    light = bpy.context.object
    light.data.energy = 3.0

    # Render settings
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 128
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
```

### Mesh Creation

```python
import bpy
import bmesh

def create_mesh_from_data(name: str, vertices: list, faces: list) -> bpy.types.Object:
    """Create a mesh object from vertex and face data."""
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()
    verts = [bm.verts.new(v) for v in vertices]
    bm.verts.ensure_lookup_table()
    for face_indices in faces:
        bm.faces.new([verts[i] for i in face_indices])
    bm.to_mesh(mesh)
    bm.free()

    mesh.update()
    return obj
```

### Modifier Stack

```python
def add_subdivision(obj: bpy.types.Object, levels: int = 2, render_levels: int = 3):
    """Add subdivision surface modifier."""
    mod = obj.modifiers.new("Subdivision", 'SUBSURF')
    mod.levels = levels
    mod.render_levels = render_levels

def add_decimate(obj: bpy.types.Object, ratio: float = 0.5):
    """Add decimate modifier for poly reduction."""
    mod = obj.modifiers.new("Decimate", 'DECIMATE')
    mod.ratio = ratio
    return mod

def apply_all_modifiers(obj: bpy.types.Object):
    """Apply all modifiers on an object."""
    bpy.context.view_layer.objects.active = obj
    for mod in obj.modifiers:
        bpy.ops.object.modifier_apply(modifier=mod.name)
```

### Material Assignment

```python
def create_pbr_material(name: str, base_color: tuple = (0.8, 0.8, 0.8, 1.0),
                         metallic: float = 0.0, roughness: float = 0.5) -> bpy.types.Material:
    """Create a PBR material with Principled BSDF."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = base_color
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    return mat

def assign_material(obj: bpy.types.Object, material: bpy.types.Material):
    """Assign a material to an object."""
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)
```

### Batch Export

```python
import bpy
from pathlib import Path

def batch_export_fbx(output_dir: str, apply_modifiers: bool = True):
    """Export each selected object as a separate FBX file."""
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)

    selected = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
    for obj in selected:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        filepath = str(path / f"{obj.name}.fbx")
        bpy.ops.export_scene.fbx(
            filepath=filepath,
            use_selection=True,
            apply_unit_scale=True,
            use_mesh_modifiers=apply_modifiers,
            mesh_smooth_type='FACE',
            path_mode='COPY',
            embed_textures=True,
        )
        print(f"Exported: {filepath}")

def export_gltf(obj_name: str, output_path: str, draco: bool = True):
    """Export a single object as glTF with optional Draco compression."""
    obj = bpy.data.objects.get(obj_name)
    if not obj:
        raise ValueError(f"Object '{obj_name}' not found")
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        use_selection=True,
        export_format='GLB',
        export_draco_mesh_compression_enable=draco,
        export_draco_mesh_compression_level=6,
        export_apply=True,
    )
```

## Three.js

### Scene Setup

```javascript
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';

function createScene(container) {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0xf0f0f0);

  // Camera
  const camera = new THREE.PerspectiveCamera(
    45, container.clientWidth / container.clientHeight, 0.1, 1000
  );
  camera.position.set(5, 3, 5);

  // Renderer
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;
  container.appendChild(renderer.domElement);

  // Controls
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;

  // Lighting
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
  scene.add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0xffffff, 1.0);
  directionalLight.position.set(5, 10, 7);
  directionalLight.castShadow = true;
  scene.add(directionalLight);

  // Ground plane
  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(20, 20),
    new THREE.MeshStandardMaterial({ color: 0xcccccc })
  );
  ground.rotation.x = -Math.PI / 2;
  ground.receiveShadow = true;
  scene.add(ground);

  return { scene, camera, renderer, controls };
}
```

### GLTFLoader with Draco

```javascript
function loadModel(scene, url, options = {}) {
  const { position = [0, 0, 0], scale = 1.0, onLoad } = options;

  const dracoLoader = new DRACOLoader();
  dracoLoader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.7/');

  const loader = new GLTFLoader();
  loader.setDRACOLoader(dracoLoader);

  return new Promise((resolve, reject) => {
    loader.load(
      url,
      (gltf) => {
        const model = gltf.scene;
        model.position.set(...position);
        model.scale.setScalar(scale);
        model.traverse((child) => {
          if (child.isMesh) {
            child.castShadow = true;
            child.receiveShadow = true;
          }
        });
        scene.add(model);
        onLoad?.(model);
        resolve(model);
      },
      (progress) => {
        const pct = (progress.loaded / progress.total * 100).toFixed(1);
        console.log(`Loading: ${pct}%`);
      },
      reject
    );
  });
}
```

### PBR Material

```javascript
function createPBRMaterial(options = {}) {
  const {
    color = 0x888888,
    metalness = 0.0,
    roughness = 0.5,
    map = null,
    normalMap = null,
    roughnessMap = null,
    metalnessMap = null,
  } = options;

  return new THREE.MeshStandardMaterial({
    color,
    metalness,
    roughness,
    map,
    normalMap,
    roughnessMap,
    metalnessMap,
  });
}
```

## Babylon.js

### Engine Setup

```javascript
const canvas = document.getElementById('renderCanvas');
const engine = new BABYLON.Engine(canvas, true);

const createScene = () => {
  const scene = new BABYLON.Scene(engine);
  scene.clearColor = new BABYLON.Color4(0.9, 0.9, 0.9, 1);

  // Camera
  const camera = new BABYLON.ArcRotateCamera(
    'camera', Math.PI / 4, Math.PI / 3, 10,
    BABYLON.Vector3.Zero(), scene
  );
  camera.attachControl(canvas, true);

  // Lighting
  const hemiLight = new BABYLON.HemisphericLight(
    'hemiLight', new BABYLON.Vector3(0, 1, 0), scene
  );
  hemiLight.intensity = 0.6;

  const dirLight = new BABYLON.DirectionalLight(
    'dirLight', new BABYLON.Vector3(-1, -2, -1), scene
  );
  dirLight.intensity = 0.8;

  // Shadows
  const shadowGen = new BABYLON.ShadowGenerator(1024, dirLight);
  shadowGen.useBlurExponentialShadowMap = true;

  return { scene, camera, shadowGen };
};
```

### PBR Material (Babylon.js)

```javascript
function createPBRMaterial(scene, name, options = {}) {
  const {
    albedoColor = new BABYLON.Color3(0.5, 0.5, 0.5),
    metallic = 0.0,
    roughness = 0.5,
  } = options;

  const mat = new BABYLON.PBRMaterial(name, scene);
  mat.albedoColor = albedoColor;
  mat.metallic = metallic;
  mat.roughness = roughness;
  return mat;
}
```

## OpenSCAD

OpenSCAD is the most LLM-compatible 3D modeling language due to its declarative, text-based nature.

### Parametric Primitives

```openscad
// Parametric box with rounded edges
module rounded_box(size, radius=2) {
    minkowski() {
        cube([size[0]-2*radius, size[1]-2*radius, size[2]-2*radius], center=true);
        sphere(r=radius, $fn=20);
    }
}

// Parametric cylinder with chamfer
module chamfered_cylinder(h, r, chamfer=1) {
    union() {
        cylinder(h=h-chamfer, r=r, $fn=32);
        translate([0, 0, h-chamfer])
            cylinder(h=chamfer, r1=r, r2=r-chamfer, $fn=32);
    }
}
```

### Boolean Operations

```openscad
// CSG operations for complex shapes
module game_prop_crate(size=20, wall=2) {
    difference() {
        // Outer shell
        cube(size, center=true);
        // Hollow interior
        cube(size - 2*wall, center=true);
        // Cross planks (decorative cuts)
        for (angle = [45, -45]) {
            rotate([0, 0, angle])
                cube([size*1.5, wall/2, size+1], center=true);
        }
    }
    // Corner reinforcements
    for (x = [-1, 1], y = [-1, 1]) {
        translate([x*(size/2 - wall), y*(size/2 - wall), 0])
            cube([wall*2, wall*2, size], center=true);
    }
}

game_prop_crate(size=30, wall=3);
```

### STL Export

```openscad
// Design for STL export
// Run: openscad -o output.stl model.scad

// Set resolution for export
$fn = 48;

module final_model() {
    // Model definition here
    rounded_box([40, 20, 10], radius=2);
}

final_model();
```

## SDF (Signed Distance Functions)

### SDF Primitives

```python
import numpy as np

def sdf_sphere(p: np.ndarray, center: np.ndarray, radius: float) -> np.ndarray:
    """Signed distance to a sphere."""
    return np.linalg.norm(p - center, axis=-1) - radius

def sdf_box(p: np.ndarray, center: np.ndarray, half_extents: np.ndarray) -> np.ndarray:
    """Signed distance to an axis-aligned box."""
    q = np.abs(p - center) - half_extents
    return (np.linalg.norm(np.maximum(q, 0), axis=-1)
            + np.minimum(np.max(q, axis=-1), 0))

def sdf_cylinder(p: np.ndarray, center: np.ndarray,
                  radius: float, height: float) -> np.ndarray:
    """Signed distance to a cylinder along Y axis."""
    q = p - center
    d_xz = np.sqrt(q[..., 0]**2 + q[..., 2]**2) - radius
    d_y = np.abs(q[..., 1]) - height / 2
    return (np.maximum(d_xz, d_y) +
            np.linalg.norm(np.stack([np.maximum(d_xz, 0), np.maximum(d_y, 0)], axis=-1), axis=-1) -
            np.maximum(np.maximum(d_xz, d_y), 0))
```

### CSG Operations

```python
def sdf_union(d1: np.ndarray, d2: np.ndarray) -> np.ndarray:
    return np.minimum(d1, d2)

def sdf_intersection(d1: np.ndarray, d2: np.ndarray) -> np.ndarray:
    return np.maximum(d1, d2)

def sdf_difference(d1: np.ndarray, d2: np.ndarray) -> np.ndarray:
    return np.maximum(d1, -d2)

def sdf_smooth_union(d1: np.ndarray, d2: np.ndarray, k: float = 0.1) -> np.ndarray:
    """Smooth union for organic blending."""
    h = np.clip(0.5 + 0.5 * (d2 - d1) / k, 0, 1)
    return d2 * (1 - h) + d1 * h - k * h * (1 - h)
```

### Marching Cubes Extraction

```python
from skimage.measure import marching_cubes

def extract_mesh_from_sdf(sdf_fn, bounds, resolution=64):
    """Extract a triangle mesh from an SDF using marching cubes."""
    # Create grid
    x = np.linspace(bounds[0][0], bounds[1][0], resolution)
    y = np.linspace(bounds[0][1], bounds[1][1], resolution)
    z = np.linspace(bounds[0][2], bounds[1][2], resolution)
    grid = np.stack(np.meshgrid(x, y, z, indexing='ij'), axis=-1)

    # Evaluate SDF
    values = sdf_fn(grid)

    # Extract surface
    verts, faces, normals, _ = marching_cubes(values, level=0.0,
                                               spacing=(x[1]-x[0], y[1]-y[0], z[1]-z[0]))
    # Offset to world coordinates
    verts += np.array(bounds[0])
    return verts, faces, normals
```

## Common Conventions

### Asset Naming

```
{project}_{category}_{name}_{variant}_{lod}.{ext}

Examples:
  rpg_prop_crate_wood_lod0.fbx
  rpg_prop_crate_wood_lod1.fbx
  rpg_char_knight_base_lod0.glb
  rpg_env_tree_oak_lod2.glb
```

### Directory Structure

```
assets/
  models/
    characters/
    props/
    environment/
    vehicles/
  textures/
    characters/
    props/
  materials/
  animations/
metadata/
  {asset_name}.json
```

### Metadata JSON

```json
{
  "name": "rpg_prop_crate_wood",
  "provider": "meshy",
  "task_id": "task_abc123",
  "created": "2025-01-15T10:30:00Z",
  "prompt": "Medieval wooden crate with iron reinforcements",
  "quality_tier": "game-ready",
  "target_engine": "unity",
  "lod_levels": [
    {"level": 0, "tris": 2400, "file": "crate_wood_lod0.fbx"},
    {"level": 1, "tris": 800, "file": "crate_wood_lod1.fbx"},
    {"level": 2, "tris": 200, "file": "crate_wood_lod2.fbx"}
  ],
  "textures": {
    "albedo": "crate_wood_albedo.png",
    "normal": "crate_wood_normal.png",
    "roughness_metallic": "crate_wood_rm.png"
  },
  "validation": {
    "manifold": true,
    "max_tris": 2400,
    "uv_coverage": 0.85,
    "texel_density_variance": 0.12
  }
}
```
