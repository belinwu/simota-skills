# Auto-Rigging Reference

Purpose: Generate rig (skeleton + skin weights) for 3D models automatically. Cover Mixamo, Rodin auto-rig, Meshy 5 rigging, Anything-World (game-genre rigs), skeleton standards (Mixamo / Unity Humanoid / UE Mannequin), skin weight smoothing, and Blender bpy automation.

## Scope Boundary

- **clay `rigging`**: Auto-rigging (this document).
- **clay `text` / `image` (elsewhere)**: Mesh generation.
- **clay `retopo` / `uv` (elsewhere)**: Mesh prep before rig.
- **clay `retarget` (elsewhere)**: Animation onto rigged mesh.
- **Builder (elsewhere)**: Engine integration code beyond stubs.

## When to Auto-Rig

- AI-generated character meshes (Meshy / Tripo / TRELLIS) need rigs to animate
- Asset library characters needing standard humanoid skeleton
- Crowd / NPC models in volume
- Prototyping where manual rig isn't ROI-positive

## Provider Comparison

| Provider | Rig type | Best for | Cost |
|----------|----------|----------|------|
| **Mixamo (Adobe)** | Humanoid (65 bones) | Bipeds; standard skeleton | Free with Adobe ID — **backend SSL/auth broke 2025-06-16, intermittent "Too many requests" errors, no official ETA from Adobe as of 2026-05; community-maintained Mixanimo Blender addon (Mixamo Rig 2025) is the working fallback** |
| **Autodesk Flow Studio AI Rigging** (formerly Wonder Studio, rebrand 2025-03; AI Rigging launched 2026-04-28) | Humanoid + neural | AI-driven character rigging in cloud, free + paid tiers | Free tier preview / paid tiers for Live Action + export |
| **Meshy 6 Rigging API** | Humanoid | Quick humanoid via API endpoint | Subscription credits |
| **Tripo Studio AI Rigging** | Humanoid (enterprise) | Production game characters | Enterprise plan |
| **Hunyuan3D Studio Auto-Rig** | Humanoid (T/A-pose) | Joints for arms/legs/spine, exported to Mixamo/UE/Unity | Hunyuan3D 3.0+ |
| **Rodin Auto-Rig** | Humanoid + custom | Stylized + realistic humanoids | Per-rig credit |
| **Anything-World** | Game-genre (humanoid + quadruped + bird + reptile) | Diverse creatures | Per-rig |
| **DeepMotion Animate 3D** | Humanoid + auto-anim | Mocap-style anim from video | Per-second |
| **Maya HumanIK** | Humanoid | Pro studio pipelines | Maya license |
| **Blender Rigify** | Humanoid + meta-rig | Open-source artists | Free |
| **AccuRig (Reallusion)** | Humanoid | Game characters | Free |
| **Cascadeur Quick Rigging** (2025.3+) | Humanoid + Quadruped (Alpha 2025.3) | Physics-aware char animation | Subscription |

For most AI-generated characters, default to **Hunyuan3D Studio Auto-Rig** or **Autodesk Flow Studio AI Rigging** for AI-pipeline integration, fall back to **Tripo Studio / Meshy API / Rodin** for hosted service, escalate to **Anything-World** for non-human or stylized. **Mixamo is currently unreliable for production due to the 2025-06 backend break** — use the community-maintained Mixanimo Blender plugin if you need the classic Mixamo skeleton.

## Skeleton Standards

Standardize on a known skeleton so retargeting works downstream.

| Standard | Bones | Notes |
|----------|-------|-------|
| Mixamo | 65 | Industry-broad; most AAA pipelines accept |
| Unity Humanoid | ~60 | Maps via Avatar; auto-bone-mapping |
| Unreal Mannequin (UE5) | 75 | UE5 default; Quinn / Manny meta |
| MetaHuman | 700+ | Facial-rich; massive |
| Maya HumanIK | 30 effector | Full-body IK |
| OpenMotion / SMPL | 24 | Research / mocap |

If multi-engine (Unity + UE), use Mixamo rig + Avatar mapping per engine.

## Skin Weights

Skin weight = how much each vertex follows each bone.

```
vertex_v = sum(weight_i * bone_i.transform * v.rest_pose)
```

| Quality knob | Effect |
|--------------|--------|
| Max bones per vertex | Usually 4 (mobile) - 8 (PC) |
| Weight smoothing iterations | Reduce harsh boundaries |
| Bone-length-based capture | Works for organic; fails on long thin |
| Heat / geodesic capture | Slow but accurate |
| Voxel / volume binding | Best for armor / rigid + soft mix |
| Manual paint per joint | Final pass for hands / face |

Auto-rig services typically apply default voxel + heat. Manual touch-up for shoulders, hips, elbows is common.

## Mixamo Workflow

```
1. Mesh prep:
   - T-pose or A-pose (Mixamo prefers T-pose)
   - Single mesh (no separate eyes/teeth attached)
   - <100K triangles for fast process
   - Clean, watertight (no holes)

2. Upload to mixamo.com:
   - FBX / OBJ / DAE
   - Auto-rigger places markers (chin, wrists, elbows, knees, groin)
   - Manual marker adjustment as needed

3. Result:
   - 65-bone Mixamo skeleton
   - Auto skin weights
   - 3000+ animation library available

4. Download:
   - With skin (T-pose) — for asset library
   - Or with animation — pre-applied (FBX)

5. Import to engine:
   - Unity: Avatar setup auto-detects Mixamo
   - Unreal: IK Retargeter to UE5 Mannequin
```

CLI / API: Mixamo has never had a public API. Workflow is web-based — **and as of 2025-06-16 the backend auto-rig + animation download flow has been broken for many users with "Too many requests" or auth errors and no Adobe ETA** (Adobe community thread "Mixamo Is Not End of Life — It's Broken, and Fixable"). For production pipelines today prefer Hunyuan3D Studio Auto-Rig, Tripo Studio AI Rigging, or Autodesk Flow Studio AI Rigging (cloud); fall back to the community-maintained **Mixanimo** Blender addon (Mixamo Rig 2025, originally Adobe-open-sourced GPL auto-rig now maintained on Gumroad) for offline.

## Rodin Auto-Rig

```python
# Rodin Auto-Rig API (sketch)
import requests, time

def auto_rig(mesh_url, rig_type="humanoid"):
    job = requests.post(
        "https://api.rodin.com/v1/rigging",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"input_mesh_url": mesh_url, "skeleton": rig_type}
    ).json()
    while True:
        status = requests.get(f"https://api.rodin.com/v1/jobs/{job['id']}").json()
        if status["state"] == "completed":
            return status["result_url"]
        time.sleep(5)
```

Rodin handles humanoid + custom skeleton specs via JSON.

## Anything-World

For diverse creature rigs (humanoid, quadruped, bird, reptile, insect, fish):

```python
# Anything-World API (sketch)
res = requests.post(
    "https://api.anything.world/animate",
    files={"model": open("creature.fbx", "rb")},
    data={"category": "quadruped", "auto_animate": "true"}
)
```

Returns rigged + auto-animated FBX with locomotion cycles.

## Blender Rigify (Local / Free)

```python
import bpy
# Add meta-rig
bpy.ops.object.armature_human_metarig_add()
metarig = bpy.context.object
# Adjust meta-rig to mesh proportions (scale bones to match)
# Generate rig
bpy.ops.pose.rigify_generate()
# Result: full IK/FK humanoid rig with controls
```

Rigify gives a control rig with IK / FK / face controls. Heavier than Mixamo but offline + free.

## Skin Weight Painting (Blender)

```python
import bpy

def auto_weight(mesh, armature):
    bpy.ops.object.select_all(action='DESELECT')
    mesh.select_set(True)
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')

def smooth_weights(mesh, iterations=5, factor=0.5):
    bpy.context.view_layer.objects.active = mesh
    bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
    for _ in range(iterations):
        bpy.ops.object.vertex_group_smooth(factor=factor)

def limit_total(mesh, max_bones=4):
    bpy.ops.object.vertex_group_limit_total(limit=max_bones)
    bpy.ops.object.vertex_group_normalize_all(lock_active=False)
```

Always run `limit_total` (4 for mobile, 8 for PC) and `normalize_all` to ensure weights sum to 1.0.

## Validation

| Check | Target |
|-------|--------|
| Bone count | Within target standard (Mixamo: 65, UE5: 75) |
| Max influences per vertex | ≤ 4 (mobile) / ≤ 8 (PC) |
| Weight sum per vertex | 1.0 (normalized) |
| Pose test | T-pose, A-pose, contrapposto, fetal — no blowouts |
| Range-of-motion test | Shoulders 180°, hips 90°, elbows 150° — no stretch / clip |
| Animation test | Walk cycle from Mixamo applied — looks natural |
| Engine import | Unity Avatar configured / UE Skeleton mapped |

## Workflow

```
PREP         →  ensure mesh is T-pose, single mesh, watertight, ≤100K tris
             →  clay `retopo` if needed for retopo before rig
             →  clay `uv` for UV before rig (saves time)

PROVIDER     →  pick: Mixamo / Rodin / Meshy / Anything-World / Rigify / AccuRig
             →  per character: provider may differ (humanoid vs creature)

UPLOAD       →  per provider API or manual upload
             →  marker placement (Mixamo) or skeleton spec (custom)

GENERATE     →  wait for rig
             →  download with skin (no animation)

VALIDATE     →  bone count, weight count, normalized
             →  pose tests (T / A / contrapposto / fetal)
             →  range of motion

CLEANUP      →  smooth weights at problem joints (shoulder / hip)
             →  limit total influences (4 mobile / 8 PC)
             →  rename bones to engine standard

ENGINE       →  Unity: Avatar config + Humanoid mapping
             →  UE5: IK Retargeter to Mannequin
             →  Godot: Skeleton3D + skin profile

ANIMATION    →  hand off to clay `retarget` for mocap
             →  or apply Mixamo library directly

HANDOFF      →  Builder: integration code
             →  clay `retarget`: mocap retargeting
             →  Realm: in-game integration
```

## Output Template

```markdown
## Auto-Rigging Plan: [Character / Asset]

### Mesh Pre-check
- Pose: [T / A]
- Triangles: [N]
- Watertight: [yes/no]
- Single mesh: [yes/no]

### Provider
- Service: [Mixamo / Rodin / Meshy 5 / Anything-World / Rigify / AccuRig]
- Skeleton standard: [Mixamo 65 / UE5 75 / Unity Humanoid]
- Cost: [free / N credits / $X]

### Rigging Code
[Python / API call snippet]

### Skin Weight Settings
- Max influences per vertex: [4 / 8]
- Smoothing iterations: [N]
- Special joints (manual touch-up): [shoulders, hips, hands, jaw]

### Validation Plan
- [ ] Bone count: [target ± 0]
- [ ] Per-vertex influence count ≤ [4/8]
- [ ] Normalized weights (sum=1.0)
- [ ] T-pose, A-pose look correct
- [ ] Walk cycle from Mixamo plays naturally
- [ ] Engine Avatar configured

### Engine Targets
- [ ] Unity Humanoid Avatar
- [ ] Unreal IK Retargeter to UE5 Mannequin
- [ ] Godot Skeleton3D + skin profile
- [ ] Three.js / Babylon.js skinning

### Handoffs
- Builder: integration code
- clay `retarget`: mocap retargeting
- Realm: in-game asset integration
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Auto-rig before retopo | Retopo first; auto-rig assumes clean topology |
| A-pose into Mixamo (expects T) | Convert to T-pose; or use provider that supports A |
| Multi-mesh single FBX (eyes / teeth) | Merge to single mesh, or rig eyes separately |
| 8-influence on mobile target | Limit to 4 max; mobile GPUs have hard cap |
| Skip weight smoothing on shoulders | Manual smooth pass mandatory at major joints |
| Rigify without scale-fixing meta-rig | Bone proportions must match mesh |
| Mixamo rig direct to UE5 without IK Retargeter | Use IK Retargeter; bone names differ |
| No range-of-motion test | Pose-test all extreme positions before declaring done |
| Per-mesh different skeleton standard | Standardize one skeleton (Mixamo) for retarget compatibility |
| Heavy manual edit on auto-rig | If you're touching 100+ verts, manual rig might be faster |
| Skin weights without normalize | Sum > 1 → over-deformation; sum < 1 → vertex floats off |
| Quadruped through humanoid auto-rigger | Use Anything-World or per-leg manual chain |
| No validation pose tests | Bugs surface during animation; fix at rig stage |
| Bones named arbitrarily | Engine bone-name conventions must match (Mixamo prefix, UE skeleton) |
| Skip face rig assumption (just body) | If face anim needed, add ARKit-blendshape OR jaw + eyes bones |
| Auto-anim accepted without review | Mixamo / Anything-World auto-anim is starting point, not final |

## Deliverable Contract

When `rigging` completes, emit:

- **Mesh pre-check** (pose / triangles / watertight / single).
- **Provider choice** + skeleton standard + cost.
- **Rigging code** / API call.
- **Skin weight settings** (max influences / smoothing / manual joints).
- **Validation plan** with pose + ROM tests.
- **Engine targets** (Unity / UE5 / Godot / web).
- **Handoffs**: Builder, clay retarget, Realm.

## References

- Mixamo — mixamo.com (Adobe; auto-rig + animation library; **backend broken since 2025-06-16**, no official Adobe ETA)
- Mixanimo (Mixamo Rig 2025) — mixanimo.gumroad.com/l/mixamorig (community-maintained Blender 3.x/4.x port of Adobe's GPL Mixamo auto-rig add-on)
- Autodesk Flow Studio (formerly Wonder Studio) — autodesk.com/products/flow-studio (AI Rigging + Neural Layer launched 2026-04-28, available on free + paid tiers)
- Hunyuan3D Studio — github.com/Tencent-Hunyuan/Hunyuan3D-2.1 (3.0+ auto-rig system, T/A-pose joints arms/legs/spine, export to Mixamo/UE/Unity)
- Tripo Studio AI Rigging — tripo3d.ai (enterprise plan; integrated with text-to-3D + image-to-3D + AI retopology)
- Meshy 6 Rigging API — meshy.ai/api (asynchronous task endpoint)
- Rodin Auto-Rig — hyper3d.ai (Deemos Tech; Rodin Gen-2 Oct 2025)
- Cascadeur Quick Rigging — cascadeur.com (humanoid + quadruped Alpha as of 2025.3, Nov 2025)
- Anything-World — anything.world
- DeepMotion Animate 3D — deepmotion.com
- AccuRig (Reallusion) — reallusion.com/auto-rig
- Blender Rigify — docs.blender.org/manual/en/latest/addons/rigging/rigify
- Maya HumanIK — autodesk.com
- Unity Humanoid Avatar — docs.unity3d.com (Animation > Avatar; Unity 6 LTS Oct 2024, Unity 6.3 LTS Dec 2025)
- Unreal IK Retargeter — docs.unrealengine.com (UE 5.5 added Nanite Skeletal Mesh)
- MetaHuman Creator — unrealengine.com/metahuman
- SMPL body model — smpl.is.tue.mpg.de
- *3D Modeling and Animation* — Lammers, Wallinger
- *Game Character Development* — Antony Ward
- "Skinning a Character" — Pixar / Disney technical papers
- "Voxelized Skinning" — Eurographics papers
- "Bounded Biharmonic Weights" — Jacobson et al. (state-of-the-art skinning)
- glTF skinning specification — github.com/KhronosGroup/glTF
- Blender Python API (bpy) — docs.blender.org/api
