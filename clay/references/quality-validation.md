# Quality Validation Reference

Topology checks, geometric metrics, game-readiness scoring, and pass/fail thresholds for AI-generated 3D models.

## Geometric Metrics

### Hausdorff Distance

Measures the maximum deviation between two surfaces. Used to compare AI output against reference or between LOD levels.

```python
import trimesh
import numpy as np

def hausdorff_distance(mesh_a: trimesh.Trimesh, mesh_b: trimesh.Trimesh,
                        sample_count: int = 10000) -> float:
    """Compute one-sided Hausdorff distance from mesh_a to mesh_b."""
    points_a = mesh_a.sample(sample_count)
    _, distances, _ = mesh_b.nearest.on_surface(points_a)
    return float(np.max(distances))


def symmetric_hausdorff(mesh_a: trimesh.Trimesh, mesh_b: trimesh.Trimesh,
                         sample_count: int = 10000) -> float:
    """Symmetric Hausdorff distance (max of both directions)."""
    d_ab = hausdorff_distance(mesh_a, mesh_b, sample_count)
    d_ba = hausdorff_distance(mesh_b, mesh_a, sample_count)
    return max(d_ab, d_ba)
```

### Chamfer Distance

Average bidirectional nearest-neighbor distance. More robust than Hausdorff for overall shape similarity.

```python
import trimesh
import numpy as np

def chamfer_distance(mesh_a: trimesh.Trimesh, mesh_b: trimesh.Trimesh,
                      sample_count: int = 10000) -> float:
    """Compute Chamfer distance between two meshes."""
    points_a = mesh_a.sample(sample_count)
    points_b = mesh_b.sample(sample_count)

    _, dist_a_to_b, _ = mesh_b.nearest.on_surface(points_a)
    _, dist_b_to_a, _ = mesh_a.nearest.on_surface(points_b)

    return float(np.mean(dist_a_to_b**2) + np.mean(dist_b_to_a**2))
```

### Normal Consistency

Measures alignment of surface normals between meshes.

```python
import trimesh
import numpy as np

def normal_consistency(mesh_a: trimesh.Trimesh, mesh_b: trimesh.Trimesh,
                        sample_count: int = 10000) -> float:
    """Normal consistency score (0-1, higher is better)."""
    points_a = mesh_a.sample(sample_count)
    _, _, face_indices = mesh_b.nearest.on_surface(points_a)

    normals_a_at_points = mesh_a.face_normals[
        mesh_a.nearest.on_surface(points_a)[2]
    ]
    normals_b_at_nearest = mesh_b.face_normals[face_indices]

    dot_products = np.sum(normals_a_at_points * normals_b_at_nearest, axis=1)
    return float(np.mean(np.clip(dot_products, 0, 1)))
```

### F1 Score (Surface Reconstruction)

Precision/recall metric for surface reconstruction quality at a given distance threshold.

```python
import trimesh
import numpy as np

def f1_score(mesh_pred: trimesh.Trimesh, mesh_gt: trimesh.Trimesh,
              threshold: float = 0.01, sample_count: int = 10000) -> dict:
    """F1 score for surface reconstruction quality."""
    points_pred = mesh_pred.sample(sample_count)
    points_gt = mesh_gt.sample(sample_count)

    _, dist_pred_to_gt, _ = mesh_gt.nearest.on_surface(points_pred)
    _, dist_gt_to_pred, _ = mesh_pred.nearest.on_surface(points_gt)

    precision = float(np.mean(dist_pred_to_gt < threshold))
    recall = float(np.mean(dist_gt_to_pred < threshold))

    f1 = 2 * precision * recall / (precision + recall + 1e-8)
    return {"precision": precision, "recall": recall, "f1": f1}
```

## Topology Checks

### Non-Manifold Detection

```python
import trimesh

def check_topology(mesh: trimesh.Trimesh) -> dict:
    """Comprehensive topology check for game readiness."""
    results = {
        "is_watertight": mesh.is_watertight,
        "is_winding_consistent": mesh.is_winding_consistent,
        "euler_number": mesh.euler_number,
        "face_count": len(mesh.faces),
        "vertex_count": len(mesh.vertices),
        "edge_count": len(mesh.edges),
    }

    # Non-manifold edges (edges shared by more than 2 faces)
    edge_face_count = {}
    for i, face in enumerate(mesh.faces):
        edges = [
            tuple(sorted([face[0], face[1]])),
            tuple(sorted([face[1], face[2]])),
            tuple(sorted([face[2], face[0]])),
        ]
        for edge in edges:
            edge_face_count.setdefault(edge, []).append(i)

    non_manifold_edges = [e for e, faces in edge_face_count.items() if len(faces) > 2]
    boundary_edges = [e for e, faces in edge_face_count.items() if len(faces) == 1]

    results["non_manifold_edges"] = len(non_manifold_edges)
    results["boundary_edges"] = len(boundary_edges)

    # Degenerate triangles (zero area)
    areas = mesh.area_faces
    degenerate = int(np.sum(areas < 1e-10))
    results["degenerate_faces"] = degenerate

    return results
```

### Trimesh Validation Script

```python
import trimesh
import numpy as np
import json
from pathlib import Path

def validate_model(filepath: str, poly_budget: int = 50000) -> dict:
    """Full validation of a 3D model file for game readiness."""
    mesh = trimesh.load(filepath, force='mesh')

    topo = check_topology(mesh)

    # Bounding box
    extents = mesh.extents.tolist()
    center = mesh.centroid.tolist()

    # Face type analysis
    face_sizes = np.array([len(f) for f in mesh.faces]) if hasattr(mesh.faces[0], '__len__') else np.full(len(mesh.faces), 3)
    tris = int(np.sum(face_sizes == 3))
    quads = int(np.sum(face_sizes == 4))
    ngons = int(np.sum(face_sizes > 4))

    report = {
        "file": filepath,
        "topology": topo,
        "geometry": {
            "extents": extents,
            "center": center,
            "surface_area": float(mesh.area),
            "volume": float(mesh.volume) if mesh.is_watertight else None,
        },
        "face_types": {"triangles": tris, "quads": quads, "ngons": ngons},
        "budget": {
            "poly_budget": poly_budget,
            "actual_tris": topo["face_count"],
            "within_budget": topo["face_count"] <= poly_budget,
            "utilization": topo["face_count"] / poly_budget,
        },
        "issues": [],
    }

    # Flag issues
    if topo["non_manifold_edges"] > 0:
        report["issues"].append(f"Non-manifold edges: {topo['non_manifold_edges']}")
    if topo["degenerate_faces"] > 0:
        report["issues"].append(f"Degenerate faces: {topo['degenerate_faces']}")
    if not topo["is_watertight"]:
        report["issues"].append("Mesh is not watertight")
    if not topo["is_winding_consistent"]:
        report["issues"].append("Inconsistent face winding")
    if ngons > 0:
        report["issues"].append(f"N-gons detected: {ngons} (triangulate before engine import)")
    if topo["face_count"] > poly_budget:
        report["issues"].append(f"Over poly budget: {topo['face_count']} > {poly_budget}")

    report["pass"] = len(report["issues"]) == 0
    return report
```

## UV Analysis

```python
import trimesh
import numpy as np

def analyze_uv(mesh: trimesh.Trimesh) -> dict:
    """Analyze UV quality metrics."""
    if not hasattr(mesh.visual, 'uv') or mesh.visual.uv is None:
        return {"has_uv": False, "issues": ["No UV coordinates found"]}

    uv = mesh.visual.uv

    # Basic checks
    out_of_range = int(np.sum((uv < 0) | (uv > 1)))

    # Texel density variance (lower is more uniform)
    # Compare 3D face area to UV face area
    face_areas_3d = mesh.area_faces
    uv_areas = []
    for face in mesh.faces:
        uvs = uv[face]
        # Shoelace formula
        area = abs(
            (uvs[1][0] - uvs[0][0]) * (uvs[2][1] - uvs[0][1]) -
            (uvs[2][0] - uvs[0][0]) * (uvs[1][1] - uvs[0][1])
        ) / 2.0
        uv_areas.append(area)

    uv_areas = np.array(uv_areas)
    valid = (face_areas_3d > 1e-10) & (uv_areas > 1e-10)

    if np.sum(valid) > 0:
        texel_densities = uv_areas[valid] / face_areas_3d[valid]
        density_variance = float(np.std(texel_densities) / (np.mean(texel_densities) + 1e-10))
    else:
        density_variance = float('inf')

    # UV coverage (total UV area used)
    total_uv_area = float(np.sum(uv_areas))

    return {
        "has_uv": True,
        "uv_coverage": min(total_uv_area, 1.0),
        "out_of_range_coords": out_of_range,
        "texel_density_variance": density_variance,
        "issues": [
            *(["Low UV coverage (< 80%)"] if total_uv_area < 0.80 else []),
            *(["High texel density variance (> 0.3)"] if density_variance > 0.3 else []),
            *(["UV coords out of 0-1 range"] if out_of_range > 0 else []),
        ],
    }
```

## PBR Material Validation

```python
def validate_pbr_textures(albedo_path: str = None, normal_path: str = None,
                           roughness_path: str = None, metallic_path: str = None) -> dict:
    """Validate PBR texture maps for common issues."""
    from PIL import Image
    import numpy as np

    issues = []
    report = {}

    if albedo_path:
        img = np.array(Image.open(albedo_path))
        report["albedo"] = {
            "resolution": img.shape[:2],
            "is_power_of_two": all(s & (s - 1) == 0 for s in img.shape[:2]),
        }
        if not report["albedo"]["is_power_of_two"]:
            issues.append("Albedo: non-power-of-two resolution")

    if normal_path:
        img = np.array(Image.open(normal_path).convert('RGB')).astype(float) / 255.0
        # Normal maps should have blue channel ~0.5-1.0 (Z pointing outward)
        avg_blue = float(np.mean(img[:, :, 2]))
        report["normal"] = {"avg_blue_channel": avg_blue}
        if avg_blue < 0.4:
            issues.append(f"Normal map: low blue channel ({avg_blue:.2f}), may be inverted")

    if roughness_path:
        img = np.array(Image.open(roughness_path).convert('L')).astype(float) / 255.0
        report["roughness"] = {
            "min": float(np.min(img)),
            "max": float(np.max(img)),
            "mean": float(np.mean(img)),
        }
        if np.min(img) == 0 and np.max(img) == 1:
            issues.append("Roughness: full range 0-1 detected, may cause visual artifacts")

    report["issues"] = issues
    report["pass"] = len(issues) == 0
    return report
```

## Game-Readiness Scoring

### Pass/Fail Thresholds by Quality Tier

| Check | Draft | Game-ready | Production |
|-------|-------|------------|------------|
| Manifold | Warn | Required | Required |
| Watertight | Skip | Warn | Required |
| Within poly budget | Skip | Required | Required |
| No degenerate faces | Warn | Required | Required |
| UV coverage > 80% | Skip | Required | Required |
| Texel density variance < 0.3 | Skip | Warn | Required |
| No n-gons | Skip | Required | Required |
| LOD chain present | Skip | Required | Required |
| PBR textures valid | Skip | Warn | Required |
| Consistent winding | Warn | Required | Required |

### Scoring Function

```python
def game_readiness_score(validation_report: dict, quality_tier: str = "game-ready") -> dict:
    """Compute game-readiness score from validation report."""
    checks = {
        "manifold": validation_report["topology"]["non_manifold_edges"] == 0,
        "watertight": validation_report["topology"]["is_watertight"],
        "within_budget": validation_report["budget"]["within_budget"],
        "no_degenerate": validation_report["topology"]["degenerate_faces"] == 0,
        "consistent_winding": validation_report["topology"]["is_winding_consistent"],
        "no_ngons": validation_report["face_types"]["ngons"] == 0,
    }

    weights = {
        "draft":      {"manifold": 0.1, "watertight": 0, "within_budget": 0,
                       "no_degenerate": 0.1, "consistent_winding": 0.1, "no_ngons": 0},
        "game-ready": {"manifold": 0.2, "watertight": 0.1, "within_budget": 0.25,
                       "no_degenerate": 0.15, "consistent_winding": 0.15, "no_ngons": 0.15},
        "production": {"manifold": 0.2, "watertight": 0.15, "within_budget": 0.2,
                       "no_degenerate": 0.15, "consistent_winding": 0.15, "no_ngons": 0.15},
    }

    tier_weights = weights.get(quality_tier, weights["game-ready"])
    score = sum(tier_weights[k] * (1.0 if checks[k] else 0.0) for k in checks)

    return {
        "quality_tier": quality_tier,
        "score": round(score, 2),
        "max_score": 1.0,
        "pass": score >= 0.8,
        "checks": checks,
        "weights": tier_weights,
    }
```
