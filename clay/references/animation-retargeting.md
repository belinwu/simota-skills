# Animation Retargeting Reference

Purpose: Apply animations from one rig to another. Cover Mixamo → custom skeleton, BVH/FBX/glTF anim conversion, bone-name mapping, T-pose / A-pose alignment, root motion vs in-place, foot IK locking, and engine retargeters (Unity Humanoid, Unreal IK Retargeter, Blender, Maya HumanIK).

## Scope Boundary

- **clay `retarget`**: Animation retargeting (this document).
- **clay `rigging` (elsewhere)**: Source rig generation.
- **clay `text` / `image` (elsewhere)**: Mesh generation.
- **Builder (elsewhere)**: Engine integration code beyond stubs.
- **Realm (elsewhere)**: In-game animation playback.

## When to Retarget

- Mixamo animation library → custom-skeleton character
- Mocap data (BVH / FBX) → game character rig
- Cross-engine: Unity character → Unreal project
- Multi-character: shared animation set across diverse rigs

## Core Components

| Component | Purpose |
|-----------|---------|
| **Source rig** | Where animation lives (Mixamo, mocap actor) |
| **Target rig** | Where you want it to play (your character) |
| **Bone map** | Which source bone drives which target bone |
| **Pose alignment** | T-pose vs A-pose calibration |
| **Root motion handling** | World-space movement vs in-place |
| **IK / FK** | Per-target rig: Foot lock, hand reach |
| **Curve filtering** | Smooth keyframe noise from mocap |

## Bone Name Mapping

```
Mixamo prefix:  mixamorig:Hips, mixamorig:Spine, mixamorig:LeftArm
Unity Humanoid: Hips, Spine, LeftUpperArm
UE5 Mannequin:  pelvis, spine_01, upperarm_l
Custom:         (your naming)
```

Engines + tools have built-in maps for common standards. Custom rigs need a manual JSON / XML map.

```yaml
bone_map:
  - source: mixamorig:Hips
    target: pelvis
  - source: mixamorig:Spine
    target: spine_01
  - source: mixamorig:LeftArm
    target: upperarm_l
  # ... 65 entries for full Mixamo
```

## T-Pose vs A-Pose Alignment

If source = T-pose and target = A-pose (or vice versa), naive copy makes arms 30° off.

Solution: rest-pose alignment. Capture both rest poses, compute per-bone delta rotation, apply to animation as offset.

```
delta_q = target_rest_q * inverse(source_rest_q)
animation_q' = delta_q * animation_q
```

Engines that handle this automatically:
- Unity Humanoid: Avatar config defines rest pose
- Unreal IK Retargeter: Source + Target IKRig with rest pose
- Maya HumanIK: characterization step
- Blender: Auto Rig Pro / Rigify retarget

## Root Motion vs In-Place

| Mode | Description | Use case |
|------|-------------|----------|
| **In-place** | Anim is on hips locally; player code drives world position | Most action games (run blends, locomotion) |
| **Root motion** | Anim has actual translation on root bone; engine moves character | Cinematic moves, melee dashes, interactions |
| **Hybrid** | Root motion for specific anims (attacks), in-place for locomotion | Modern AAA |

Mixamo offers both versions for download. Match the version to the engine integration:
- Unity: in-place + Animator drives motion, OR root motion via Animator setting
- UE5: Root Motion mode per Animation Sequence

## IK / Foot Locking

Mocap or generic anim doesn't know your character's foot length / leg length. Foot can:
- Float above ground
- Penetrate ground
- Slide ("ice skating")

Solution: IK foot lock at runtime. The animation provides the *intent*; engine constrains feet to ground + lower-leg IK.

| Engine | Foot IK |
|--------|---------|
| Unity | Avatar IK Pass + AnimatorIK script |
| UE5 | Control Rig + IK Rig + Foot Placement |
| Godot 4 | SkeletonModification3DLookAt + custom IK |

Also useful: hand IK (drinking, weapons), look-at IK (head/eyes follow target).

## BVH / FBX / glTF Conversion

| Format | Origin | Notes |
|--------|--------|-------|
| BVH | Biovision (mocap) | Bone hierarchy + euler keyframes; common mocap export |
| FBX | Autodesk | De-facto exchange; supports skinned mesh + anim + materials |
| glTF 2.0 | Khronos | Modern web/game; quaternion keyframes |
| Alembic | Sony | Baked geometry caching (cinematic) |
| USD | Pixar | Modern Hollywood + AAA; complex |
| ABC (Alembic) | Sony | Cinematic |

Conversion tools:
- Blender (free; reads/writes all)
- Autodesk FBX Converter (FBX-only; legacy)
- Cascadeur (animation polish + conversion)
- Reallusion iClone (mocap workflow)

## Mixamo → UE5 Workflow

```
1. Export Mixamo anim as FBX with skin (or just animation)
2. Import to UE5 — it imports as a separate skeleton
3. Open IK Retargeter:
   - Source IKRig: Mixamo skeleton
   - Target IKRig: UE5 Mannequin skeleton (or your skeleton)
   - Configure chain mappings (spine, arms, legs, head)
   - Auto-map bones; manual fix gaps
4. Retarget Animation Sequence
5. Resulting anim plays on UE5 Mannequin / your character
```

## Mixamo → Unity Workflow

```
1. Import Mixamo character + anim FBX
2. Configure as Humanoid in Animation tab
3. Unity creates Avatar from Mixamo skeleton
4. Apply same Avatar to your character (if also Humanoid)
5. Animations play across all characters with Humanoid Avatar
```

## Custom-Skeleton Retargeting (Blender)

```python
import bpy

def retarget_animation(source_armature, target_armature, bone_map):
    """
    bone_map: dict {source_bone_name: target_bone_name}
    """
    # Compute rest-pose delta per bone pair
    deltas = {}
    for src, tgt in bone_map.items():
        src_bone = source_armature.pose.bones[src]
        tgt_bone = target_armature.pose.bones[tgt]
        deltas[(src, tgt)] = tgt_bone.rest_matrix.to_quaternion() @ \
                              src_bone.rest_matrix.to_quaternion().inverted()

    # Iterate keyframes
    fcurves = source_armature.animation_data.action.fcurves
    for src, tgt in bone_map.items():
        # Copy + apply delta to target bone f-curves
        # ...
```

In practice, use Auto Rig Pro / Rokoko Studio Live / Mixamo Auto-Map plugins.

## Mocap Cleanup

Raw mocap has:
- Foot floating / sliding
- Hand jitter
- Spine flicker
- Knee popping

Cleanup passes:
- **Filter**: Butterworth low-pass on quaternion curves (3-5 Hz cutoff)
- **Foot lock**: Detect contact frames, lock world-space pos
- **Pose constraints**: Knee must stay between hip + ankle
- **Hand constraints**: Wrist follows arm chain

Cascadeur, Maya AnimLayer, Blender Graph Editor for manual cleanup.

## Workflow

```
INVENTORY    →  list source animations + target rigs
             →  identify root motion vs in-place needs

BONE MAP     →  pick standard or define custom
             →  validate full chain (spine + arms + legs + head)

POSE ALIGN   →  T-pose vs A-pose check
             →  per-bone delta rotation if needed

CONVERT      →  source format → engine-compatible format
             →  BVH ↔ FBX ↔ glTF as needed

RETARGET     →  per-engine: Unity Humanoid / UE5 IK Retargeter / Blender / Maya HumanIK / Cascadeur
             →  auto-map + manual gap fix

CLEANUP      →  filter mocap noise (Butterworth low-pass)
             →  fix foot sliding (IK foot lock + contact detection)
             →  fix knee / spine popping (constraint pass)

ROOT MOTION  →  decide per-anim: in-place vs root motion
             →  bake root motion if hybrid

ENGINE       →  Unity: Animator State Machine + Avatar
             →  UE5: Animation Blueprint + Control Rig
             →  Godot: AnimationTree + SkeletonModification3D
             →  Web (Three.js): SkinnedMesh + AnimationMixer

VALIDATE     →  side-by-side source vs retargeted
             →  no joint rotation extreme
             →  no foot slide visible
             →  performance: animation events fire on time

HANDOFF      →  Builder: in-engine integration
             →  Realm: in-game playback
             →  clay `rigging`: rig if not already done
```

## Output Template

```markdown
## Retarget Plan: [Source → Target]

### Inputs
- Source rig: [Mixamo / mocap / Unity Humanoid / UE5 Mannequin]
- Source animations: [list with file + duration]
- Target rig: [your skeleton]
- Target rest pose: [T-pose / A-pose]

### Bone Map
| Source bone | Target bone |
|-------------|-------------|
| mixamorig:Hips | pelvis |
| mixamorig:Spine | spine_01 |
| mixamorig:LeftArm | upperarm_l |
| ... (full chain) | ... |

### Pose Alignment
- Source rest: [T / A]
- Target rest: [T / A]
- Delta required: [yes / no]
- Per-bone delta computed: [yes — file path]

### Root Motion Plan
| Animation | Mode | Notes |
|-----------|------|-------|
| walk | in-place | Animator drives world pos |
| dash | root motion | Engine moves character |
| attack_lunge | root motion | melee step-forward |

### Tooling
- Primary: [UE5 IK Retargeter / Unity Humanoid / Blender Auto Rig Pro / Cascadeur]
- Cleanup: [filter cutoff + foot lock + constraints]

### Cleanup Pass
- Butterworth low-pass cutoff: [4 Hz]
- Foot lock: [contact threshold + lock duration]
- Knee constraint: [hinge with limit]
- Hand jitter: [filter cutoff]

### Engine Integration
[Unity Animator / UE5 Animation Blueprint / Godot AnimationTree / Three.js mixer]

### Validation
- [ ] Source vs target side-by-side check
- [ ] No joint rotation > limit
- [ ] Foot lock works at all gait speeds
- [ ] Spine doesn't flicker
- [ ] Hand chain follows naturally
- [ ] Root motion ≠ in-place mismatch
- [ ] Performance: keyframe count + memory acceptable

### Handoffs
- Builder: in-engine integration
- Realm: in-game playback
- clay `rigging`: rig confirm if not yet done
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Mixamo straight to UE5 without IK Retargeter | Use IK Retargeter; bones differ |
| T-pose source on A-pose target without alignment | Rest-pose delta required |
| In-place anim with engine expecting root motion | Match mode per anim |
| Filtering all keyframes uniformly | Filter only mocap (high noise); preserve hand-keyed anim |
| No foot IK on character with varying ground | IK lock mandatory for varied terrain |
| Skipping rest-pose validation | T-pose must be canonical (arms straight, palms down) |
| Skeleton with twist bones unmapped | Twist bones (forearm, thigh) need explicit map or auto-derive |
| Custom skeleton without standard pivot orientation | Use industry-standard (Y-up, Z-forward) for tooling compatibility |
| Per-anim retarget instead of per-rig (shared map) | Once retarget map is good, reuse across all anims |
| Mocap raw without cleanup | Always filter + foot-lock; raw mocap looks janky |
| Root motion baked into in-place anim | Hips floats around; clearly assign mode |
| 60fps anim → 30fps without resampling | Resample on import; some engines auto, some don't |
| Skipping engine validation | Looks fine in DCC, broken in engine; verify in target |
| Multiple Mixamo anims with different export settings | Standardize export (frame rate, scale, skin) |
| Hand IK ignored on weapons / props | Hand attaches to weapon; IK ensures grip pose |
| Eyes / head don't track | Add look-at IK for camera or target |

## Deliverable Contract

When `retarget` completes, emit:

- **Source / target rig** identification.
- **Bone map** with full chain.
- **Pose alignment** plan (T/A delta).
- **Root motion plan** per animation.
- **Tooling choice** + cleanup pass parameters.
- **Engine integration** stubs.
- **Validation** checklist (side-by-side / IK / mode / performance).
- **Handoffs**: Builder, Realm, clay rigging.

## References

- Mixamo — mixamo.com
- Unreal IK Retargeter — docs.unrealengine.com
- Unity Humanoid Animation Retargeting — docs.unity3d.com
- Blender Auto Rig Pro — blendermarket.com
- Maya HumanIK — autodesk.com
- Cascadeur — cascadeur.com (physics-based polish + retarget)
- Rokoko Studio — rokoko.com (mocap + retarget)
- iClone (Reallusion) — reallusion.com
- BVH format — research.cs.wisc.edu (origin: Biovision)
- FBX format — autodesk.com/products/fbx
- glTF 2.0 spec — github.com/KhronosGroup/glTF
- USD (Pixar) — graphics.pixar.com/usd
- *Computer Animation* — Rick Parent
- *Game Anim: Video Game Animation Explained* — Jonathan Cooper
- "Motion Matching" — Naughty Dog / Ubisoft GDC talks
- "Procedural Animation" — Inverse Kinematics literature
- ART (Animation Rigging Toolset) — Unreal community
- "FK to IK conversion" — Maya animation papers
- SteamVR Skeleton Input — for VR hand pose retargeting
- DeepMotion — AI-based mocap from video
- Move.AI — markerless mocap to FBX
