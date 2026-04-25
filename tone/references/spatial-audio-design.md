# Spatial Audio Design Reference

Purpose: Design 3D positional audio for games and immersive web. Cover HRTF binaural rendering, ambisonics, occlusion / reverb zones, middleware (Steam Audio, Resonance Audio, Wwise Spatial Audio, Web Audio API PannerNode), and engine integration (Unity / Unreal / Phaser / Three.js).

## Scope Boundary

- **tone `spatial`**: 3D positional audio design (this document).
- **tone `sfx` / `bgm` / `ambient` (elsewhere)**: Asset generation.
- **tone `adaptive` (elsewhere)**: Music transitions (different concern).
- **tone `lufs` (elsewhere)**: Loudness normalization.
- **Builder (elsewhere)**: Engine integration code beyond stubs.
- **Realm (elsewhere)**: Phaser-specific 2D scenes (this doc covers 3D).

## When Spatial Audio Matters

- 3D games (FPS, action, immersive sim)
- VR / AR (HRTF mandatory; positional cues = presence)
- 360° video / cinematic audio
- Multiplayer voice chat (positional)
- Audio-driven gameplay (Echo Wakefield-class, audio-only games)

For 2D platformers / puzzle games, simple stereo panning is enough — don't over-engineer.

## Three Layers

| Layer | Question | Mechanism |
|-------|----------|-----------|
| **Direction** | Where is the source? | HRTF / pan / VBAP |
| **Distance** | How far? | Attenuation curves, low-pass per distance |
| **Environment** | What space am I in? | Reverb zones, occlusion, propagation |

## HRTF (Head-Related Transfer Function)

Per-ear filtering that emulates how human anatomy shapes incoming sound. Required for binaural / headphone-out delivery.

| Library / engine | HRTF source |
|------------------|-------------|
| Steam Audio | Custom HRTF + per-user calibration |
| Resonance Audio (Google) | Open dataset |
| Wwise Spatial Audio | Auro-3D / Microsoft Spatial Sound |
| Web Audio PannerNode | Default IRCAM HRTF |
| FMOD Studio Resonance Audio plugin | Resonance |
| Unity Audio Spatializer | Per-platform default |
| Unreal MetaSounds + Steam Audio | Steam Audio |

For VR: HRTF mandatory. Distance + environment alone don't sell head movement.

## Ambisonics

3D audio encoded into spherical harmonics — independent of speaker layout.

| Order | Channels | Use |
|-------|----------|-----|
| 1st (B-format) | 4 (W X Y Z) | YouTube 360, basic VR |
| 2nd | 9 | Higher quality VR |
| 3rd | 16 | Cinema, professional VR |

Ambisonics + binaural decoder = headphone-friendly 3D audio. Major game engines support 1st / 3rd order.

## Distance Attenuation

```
Linear:        gain = 1 - clamp(d / max_d, 0, 1)
Inverse:       gain = ref / max(d, ref)        (physically accurate, "quiet far away")
Inverse-square: gain = (ref / max(d, ref))²
Logarithmic:   gain = -20 * log10(max(d, ref) / ref) [in dB]
Exponential:   gain = e^(-rolloff * d)
```

Game-genre defaults:
- Realistic shooter: inverse-square
- Stylized action: linear or curve-shaped
- Web (PannerNode): `inverse` default; reduce `rolloffFactor` for shorter range

Pair with low-pass filter that closes as distance increases (air absorption).

## Occlusion / Obstruction / Exclusion

| Concept | Meaning |
|---------|---------|
| **Occlusion** | Listener and source separated by geometry; both direct + reverb attenuated |
| **Obstruction** | Direct path blocked but reverb path open |
| **Exclusion** | Direct path open but reverb attenuated |

Compute via raycast (cheap) or geometric propagation (Steam Audio probes, expensive but accurate).

## Reverb Zones

```
ZONES:
  cathedral: long tail (3-6s), high diffuse, wet 60%
  cave: med tail (1.5-3s), mid diffuse, wet 50%
  outdoor: short tail (0.3-0.8s), low diffuse, wet 15%
  small_room: short tail (0.3-0.6s), high early reflection, wet 25%
```

Crossfade between zones on listener move. FMOD reverb sends, Wwise reverb buses, Unity AudioReverbZone.

## Per-Engine Integration

### Web Audio PannerNode

```javascript
const ctx = new AudioContext();
const panner = ctx.createPanner();
panner.panningModel = 'HRTF';
panner.distanceModel = 'inverse';
panner.refDistance = 1;
panner.maxDistance = 50;
panner.rolloffFactor = 1;
panner.coneInnerAngle = 360;  // omnidirectional source
source.connect(panner).connect(ctx.destination);
panner.positionX.value = x; panner.positionY.value = y; panner.positionZ.value = z;
ctx.listener.positionX.value = lx; // and orientation
```

Browser support: Chromium / Safari / Firefox via `panningModel: 'HRTF'`.

### Three.js + PositionalAudio

```javascript
import { AudioListener, PositionalAudio, AudioLoader } from 'three';
const listener = new AudioListener();
camera.add(listener);
const sound = new PositionalAudio(listener);
new AudioLoader().load('explosion.mp3', (buffer) => {
  sound.setBuffer(buffer);
  sound.setRefDistance(5);
  sound.setRolloffFactor(2);
  sound.setDistanceModel('inverse');
  enemy.add(sound);
});
```

### Unity (Unity 6)

- AudioSource + AudioListener
- SpatialBlend = 1.0 (full 3D)
- Spatializer Plugin: Microsoft Spatial Sound / Steam Audio / Resonance Audio
- AudioMixer + AudioReverbZone

### Unreal (UE5)

- MetaSounds for procedural audio
- Steam Audio plugin (Valve) — best free HRTF + occlusion
- Sound Submix + Reverb Effects

### FMOD Studio

- 3D Spatializer effect on event tracks
- Geometry occlusion via FMOD Geometry API
- Resonance Audio plugin

### Wwise

- Spatial Audio: Acoustic Portals, Geometric Diffraction
- 3D Bus + Auro-3D / Microsoft Spatial Sound binaural

## Performance Budget

| Concern | Budget |
|---------|--------|
| Voice limit | ≤ 32 simultaneous 3D voices (mobile), ≤ 256 (PC) |
| HRTF cost | ~0.1ms per voice (PC), ~0.3ms (mobile) |
| Occlusion raycast | Cache results 100-200ms |
| Reverb tails | Single global late reverb, multiple early-reflection sends |

Use voice priority + virtualization (sounds that don't render but track gain).

## Workflow

```
INVENTORY    →  list audio sources by 2D vs 3D
             →  per-source: distance range, attenuation curve, directionality

ENGINE       →  pick engine + spatializer (Steam / Resonance / Wwise / Web Audio)
             →  HRTF source (default or custom)

DISTANCE     →  per-source attenuation curve + ref/max distance
             →  air absorption (low-pass per distance)

OCCLUSION    →  raycast cheap path, geometric for high-fidelity
             →  occlusion / obstruction / exclusion mapping per zone

REVERB       →  reverb zone definitions (cathedral / cave / outdoor / room)
             →  early-reflection vs late-reverb send levels
             →  zone-crossfade duration

VOICE BUDGET →  max simultaneous 3D voices
             →  priority + virtualization rules
             →  culling distance

PROFILE      →  measure spatializer cost per voice
             →  fall back to 2D pan if budget exceeded

INTEGRATION  →  emit engine-specific code stubs
             →  test on headphones (HRTF correctness) + speakers (downmix)

HANDOFF      →  Builder: full engine integration
             →  tone `lufs`: loudness post-spatial
             →  Realm: 2D scene fallback if applicable
```

## Output Template

```markdown
## Spatial Audio Plan: [Project / Scene]

### Engine + Spatializer
- Engine: [Unity 6 / Unreal 5 / Three.js / Web Audio / FMOD / Wwise]
- Spatializer: [Steam Audio / Resonance / Microsoft Spatial / IRCAM HRTF]
- Format: [stereo binaural / 5.1 / 7.1.4 / Ambisonic 1st]

### Source Inventory
| Source | 3D? | Ref | Max | Curve | Cone |
|--------|-----|-----|-----|-------|------|
| Footstep | yes | 1m | 15m | inverse-sq | omni |
| NPC voice | yes | 2m | 20m | inverse | 60° |
| BGM | no | — | — | — | — |
| Explosion | yes | 1m | 60m | inverse-sq | omni |

### Reverb Zones
| Zone | RT60 | Diffuse | Wet |
|------|------|---------|-----|
| Cathedral | 4s | 0.8 | 60% |
| Cave | 2s | 0.6 | 50% |
| Outdoor | 0.5s | 0.2 | 15% |

### Occlusion Strategy
- Method: [raycast / Steam Audio probes / portals]
- Update rate: [100ms cached]
- Filter: [low-pass at -6dB through walls]

### Voice Budget
- Max 3D voices: [32 mobile / 128 PC]
- Priority: [proximity → action-tier → ambient]
- Virtualization at: [-30dB or out of range]

### Code Stubs
[Web Audio / Three.js / Unity / Unreal / FMOD / Wwise per target]

### Validation
- Headphone HRTF check: [pass / fail]
- Speaker downmix: [pass / fail]
- Voice budget under load: [profiled]
- Occlusion correctness: [test scene]

### Handoffs
- Builder: full engine integration
- tone `lufs`: post-spatial loudness
- Realm: 2D fallback if needed
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| HRTF on speakers (not headphones) | Detect output; use stereo crossfeed for speakers |
| Linear attenuation for realistic shooter | Inverse-square for physical accuracy |
| No air absorption with distance | Add distance-coupled low-pass |
| Reverb on dialogue (lost intelligibility) | Dry dialogue bus; reverb on FX bus |
| Occlusion raycast every frame per voice | Cache 100-200ms; budget update count |
| Overlapping reverb zones (double-wet) | Crossfade between zones; never sum |
| 3D pan on UI sounds | UI is 2D non-positional |
| Voice limit ignored (mobile crash) | Hard cap + virtualization |
| Same HRTF for all listeners | Default HRTF works; custom calibration optional |
| Ignoring loudness across distance | Spatial gain ≠ loudness target; pair with `lufs` |
| Stereo source forced into PannerNode | Mono required for HRTF; downmix first |
| BGM through 3D bus | BGM is 2D non-positional; route separately |
| No fallback when spatializer absent | Graceful 2D pan fallback |
| Hard cutoff at max distance | Use smooth roll-off; voice virtualization |
| Reverb tail longer than gameplay sound itself | Tune RT60 to gameplay pace |

## Deliverable Contract

When `spatial` completes, emit:

- **Engine + spatializer choice** with format target.
- **Source inventory** with 3D flag + curve + cone.
- **Reverb zones** with RT60 + wet levels.
- **Occlusion strategy** with method + update rate.
- **Voice budget** with priority + virtualization rules.
- **Code stubs** per target engine.
- **Validation** (headphone / speaker / load / occlusion).
- **Handoffs**: Builder, tone lufs, Realm.

## References

- Steam Audio — valvesoftware.github.io/steam-audio
- Resonance Audio — resonance-audio.github.io (Google)
- Wwise Spatial Audio — audiokinetic.com
- FMOD Spatial Audio — fmod.com
- Web Audio API PannerNode — developer.mozilla.org
- Three.js PositionalAudio — threejs.org/docs
- Unity Audio Spatializer SDK — docs.unity3d.com
- Unreal Steam Audio plugin — steam-audio for UE
- Microsoft Spatial Sound — docs.microsoft.com
- *Game Audio Implementation* — Richard Stevens, Dave Raybould
- *Designing Sound* — Andy Farnell (procedural audio)
- AES (Audio Engineering Society) papers on HRTF
- *3D Audio Programming* — Mat Buckland
- ITU-R BS.2076 — Audio Definition Model (ADM)
- IRCAM Listen HRTF database — recherche.ircam.fr/equipes/salles/listen
- "Binaural Audio for Headphone-Based Spatial Sound" — AES tutorial
- Auro-3D format documentation
- AmbiX 1st/3rd order ambisonics convention (Auro-3D, AmbiX)
- Microsoft Project Triton (precomputed propagation, Halo: Reach onward)
- "Audio for VR" — Oculus Audio SDK guides (legacy)
