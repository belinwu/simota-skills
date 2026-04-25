# LUFS Normalization Reference

Purpose: Normalize game / web / broadcast audio to consistent loudness via LUFS (Loudness Units relative to Full Scale). Cover EBU R128, ITU-R BS.1770, integrated / momentary / short-term loudness, True Peak limiting, per-platform targets, and pyloudnorm / ffmpeg loudnorm tooling.

## Scope Boundary

- **tone `lufs`**: Loudness normalization (this document).
- **tone `sfx` / `bgm` / `voice` / `ambient` / `ui` (elsewhere)**: Asset generation.
- **tone `spatial` (elsewhere)**: 3D positional (orthogonal).
- **tone `adaptive` (elsewhere)**: Stem mix balance (loudness applied after).
- **Builder (elsewhere)**: Engine integration / runtime loudness control.
- **morph (elsewhere)**: Document conversion (different domain).

## Why LUFS, Not Peak / RMS

| Metric | Measures | Limitation |
|--------|----------|------------|
| **Peak (dBFS)** | Maximum sample value | Doesn't reflect perceived loudness |
| **RMS** | Average power | Frequency-flat (ignores hearing curve) |
| **LUFS** | Perceived loudness (K-weighted) | Standard since 2011 |

LUFS uses K-weighting (high-shelf + low-cut) approximating human hearing. ITU-R BS.1770 and EBU R128 standardized it for broadcast; streaming services adopted derived targets.

## Three LUFS Measurements

| Window | Use |
|--------|-----|
| **Momentary (M)** | 400ms sliding | Real-time meter |
| **Short-term (S)** | 3s sliding | Mix decisions |
| **Integrated (I)** | Whole program | Final delivery target |

Plus **LRA** (Loudness Range, in LU) and **True Peak** (dBTP, inter-sample peak).

## Per-Platform Targets

| Platform / context | Target | Tolerance | True Peak |
|-------------------|--------|-----------|-----------|
| **EBU R128 broadcast** | -23 LUFS | ±0.5 | -1 dBTP |
| **ATSC A/85 (US TV)** | -24 LKFS | ±2 | -2 dBTP |
| **Spotify** | -14 LUFS | ±1 | -1 dBTP |
| **Apple Music** | -16 LUFS | -- | -1 dBTP |
| **YouTube** | -14 LUFS | -- | -1 dBTP |
| **Tidal** | -14 LUFS | -- | -1 dBTP |
| **Amazon Music** | -14 LUFS | -- | -2 dBTP |
| **Podcast (most platforms)** | -16 LUFS | ±0.5 | -1 dBTP |
| **Mobile gameplay** | -18 LUFS | ±1 | -1 dBTP |
| **Console gameplay** | -23 to -27 LUFS | ±1 | -1 dBTP |
| **Cinematic in-game** | -27 LUFS | ±2 | -1 dBTP |
| **UI / interaction sounds** | -10 to -14 LUFS short-term | -- | -1 dBTP |
| **Voice / narration** | -16 LUFS (loud), -19 LUFS (default) | ±1 | -1 dBTP |
| **VR / spatial** | -16 to -18 LUFS | ±1 | -1 dBTP |

Streaming services apply playback normalization; over-loud masters get attenuated. Authoring at -14 LUFS is the de-facto modern target for distributed music.

## Per-Asset-Type Strategy

| Asset | Approach |
|-------|----------|
| BGM | Integrated LUFS to platform target; LRA preserved |
| SFX | Peak-normalize per family + momentary loudness budget |
| Voice / narration | Integrated LUFS with light compression for consistency |
| Ambient | Lower target (-24 to -30 LUFS); leave headroom for SFX |
| UI | Short-term loudness for transient impact; -10 to -14 LU |
| Cinematic | Wider LRA preserved; loudness anchor on dialogue |

## True Peak (dBTP)

Inter-sample peaks can exceed sample peaks after DAC reconstruction. Always limit True Peak to ≤ -1 dBTP (some platforms require -2 dBTP).

ffmpeg loudnorm and most tools apply true-peak limiter automatically with `tp=-1.0`.

## Two-Pass Loudnorm with FFmpeg

```bash
# Pass 1: measure
ffmpeg -i input.wav -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json \
  -f null - 2> measured.json

# Extract values from measured.json
# input_i, input_tp, input_lra, input_thresh, target_offset

# Pass 2: apply (linear normalization with exact values)
ffmpeg -i input.wav -af \
  "loudnorm=I=-14:TP=-1:LRA=11:measured_I=-23.4:measured_TP=-3.2:measured_LRA=8.4:measured_thresh=-34.0:offset=-0.1:linear=true" \
  output.wav
```

Single-pass is faster but uses dynamic loudnorm (compresses dynamics). Two-pass linear preserves dynamics — preferred for music.

## Python (pyloudnorm)

```python
import soundfile as sf
import pyloudnorm as pyln

data, rate = sf.read("input.wav")
meter = pyln.Meter(rate)               # ITU-R BS.1770-4
loudness = meter.integrated_loudness(data)
normalized = pyln.normalize.loudness(data, loudness, -14.0)
sf.write("output.wav", normalized, rate)
```

For peak limiting before/after:
```python
peak = pyln.normalize.peak(normalized, -1.0)
sf.write("output.wav", peak, rate)
```

## Per-Asset Pipeline

```python
# tone batch normalization scaffold
from pathlib import Path
import soundfile as sf, pyloudnorm as pyln

TARGETS = {
    "music":   -14.0,
    "sfx":     -18.0,
    "voice":   -16.0,
    "ambient": -24.0,
    "ui":      -12.0,
}

def normalize(path: Path, asset_type: str, true_peak: float = -1.0):
    data, rate = sf.read(path)
    meter = pyln.Meter(rate)
    li = meter.integrated_loudness(data)
    normalized = pyln.normalize.loudness(data, li, TARGETS[asset_type])
    limited = pyln.normalize.peak(normalized, true_peak)
    sf.write(path.with_suffix(".normalized.wav"), limited, rate)

for wav in Path("audio/").glob("*.wav"):
    asset_type = wav.parent.name  # by directory convention
    normalize(wav, asset_type)
```

## Game Engine Runtime Loudness

For games, normalize *assets at build time* and apply per-bus loudness control at *runtime*:

```
Build-time: each asset = -18 LUFS integrated
Runtime:
  master_bus      0 dB
  music_bus      -6 dB (relative)
  sfx_bus         0 dB
  voice_bus      +3 dB (above SFX for intelligibility)
  ui_bus         +6 dB (above gameplay for prominence)
  ambient_bus    -9 dB
```

This gives mixers the consistent baseline; real-time changes (ducking, mood) live on buses.

## Ducking (Sidechain)

When voice or critical SFX plays, automatically attenuate music + ambient.

```
sidechain_compressor:
  threshold: -24 dB (voice level)
  ratio: 4:1
  attack: 50ms
  release: 250ms
  target: music_bus (gain reduce)
```

Common in racing games (engine ducks for navigator), action games (music ducks for boss bark).

## Workflow

```
INVENTORY    →  list all audio assets by type (music / SFX / voice / ambient / UI)
             →  identify final delivery context (game / web / broadcast / mobile / VR)

TARGET       →  per asset-type LUFS target from platform table
             →  True Peak ceiling (-1 dBTP default)

MEASURE      →  pass 1 with ffmpeg loudnorm or pyloudnorm
             →  log integrated LUFS + LRA + TP

NORMALIZE    →  pass 2 linear normalization (preserves dynamics)
             →  apply true-peak limiter

VALIDATE     →  re-measure normalized output
             →  ±0.5 LU within target
             →  TP ≤ -1 dBTP

ASSET BUS    →  build-time consistent baseline
             →  runtime per-bus offsets

DUCKING      →  sidechain rules per priority
             →  threshold + ratio + attack + release

DELIVER      →  manifest with per-asset measured + target LUFS
             →  test on target devices (TV / phone / headphones)

HANDOFF      →  Builder: engine bus + ducking config
             →  tone `spatial`: 3D bus loudness
             →  tone `adaptive`: per-stem balance + final loudness
             →  Realm: in-game volume controls
```

## Output Template

```markdown
## Loudness Plan: [Project / Delivery]

### Delivery Context
- Platform: [game / Spotify / podcast / broadcast]
- Target context: [console / mobile / web / VR]

### Per-Asset-Type Targets
| Type | LUFS | TP | LRA |
|------|------|-----|-----|
| Music | -14 | -1 | 11 |
| SFX | -18 | -1 | -- |
| Voice | -16 | -1 | 8 |
| Ambient | -24 | -1 | -- |
| UI | -12 (short-term) | -1 | -- |

### Tooling
- Primary: [ffmpeg loudnorm / pyloudnorm]
- Pass: [two-pass linear]

### Runtime Bus Map
master   0 dB
  music    -6 dB
  sfx       0 dB
  voice    +3 dB
  ui       +6 dB
  ambient  -9 dB

### Ducking Rules
| Priority | Source | Target | Ratio | Attack/Release |
|----------|--------|--------|-------|----------------|
| voice | voice_bus | music + ambient | 4:1 | 50/250ms |
| crit_sfx | crit_sfx_bus | music | 3:1 | 30/200ms |

### Measurement Manifest
| Asset | Measured I | Target I | Measured TP | OK? |
|-------|-----------|----------|-------------|-----|
| bgm_main.wav | -16.2 | -14 | -2.1 | ✓ post-normalize |
| sfx_explosion.wav | -19.5 | -18 | -1.1 | ✓ |
| ... | ... | ... | ... | ... |

### Validation
- All assets within ±0.5 LU: [pass / N failed]
- All TP ≤ -1 dBTP: [pass / N failed]
- Device test (mobile): [pass]
- Device test (TV): [pass]
- Headphone test: [pass]

### Handoffs
- Builder: bus config + ducking
- tone `spatial`: 3D bus
- tone `adaptive`: stem balance
- Realm: volume controls
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Peak-normalize music to 0 dBFS | Use LUFS; peak-only ignores perceived loudness |
| Single-pass loudnorm for music | Two-pass linear preserves dynamics |
| Ignoring True Peak | Inter-sample peaks distort on consumer DACs |
| Same target for all asset types | Voice, music, SFX, ambient have distinct targets |
| Loudness war on game music (-9 LUFS) | Streaming + game playback both attenuate; preserve dynamics |
| Building with no LRA budget | LRA 8-14 keeps it musical; <6 sounds compressed |
| No platform calibration before delivery | Test on target hardware; mobile differs from TV |
| Voice quieter than SFX | +3 dB voice over SFX for intelligibility |
| Hard-clip true peak limit | Use TP limiter, not peak clipper |
| Manual gain riding instead of ducking | Sidechain compressor for predictable ducking |
| Per-asset LUFS without bus offsets | Build asset baseline, then apply runtime bus mix |
| Streaming-master at -8 LUFS | Spotify reduces to -14 anyway; you lose dynamics for nothing |
| Cinematic in-game = streaming target | Cinematic should be -27 LUFS for headroom |
| LRA collapsed to 4 LU | Listener fatigue; aim for 8-14 LU on music |
| Ducking with 5ms attack | 50ms attack avoids clicks; ear can't perceive faster |
| Mono assets summed with stereo at same LUFS | Mono is +3 dB louder when summed; account for this |

## Deliverable Contract

When `lufs` completes, emit:

- **Delivery context** + per-asset-type LUFS / TP / LRA targets.
- **Tooling** (ffmpeg / pyloudnorm) with two-pass linear procedure.
- **Runtime bus map** with offsets.
- **Ducking rules** with sidechain parameters.
- **Measurement manifest** with measured + target per asset.
- **Validation** (within tolerance + device tests).
- **Handoffs**: Builder, tone spatial, tone adaptive, Realm.

## References

- ITU-R BS.1770-4 — Algorithms to measure audio programme loudness
- EBU R128 — Loudness normalisation and permitted maximum level
- ATSC A/85 — Techniques for Establishing and Maintaining Audio Loudness
- AES TD1004 — Loudness guidelines for streaming
- ffmpeg loudnorm filter — ffmpeg.org/ffmpeg-filters.html#loudnorm
- pyloudnorm — github.com/csteinmetz1/pyloudnorm (Steinmetz)
- Spotify Loudness Normalization — newsroom.spotify.com / engineering.spotify.com
- Apple Music Sound Check — support.apple.com
- Tidal MQA / loudness specifications
- *Mastering Audio* — Bob Katz (loudness pioneer, K-system)
- *Audio Production and Critical Listening* — Jason Corey
- AES papers on perceptual loudness (Glasberg + Moore)
- Microsoft "Audio for Games" — docs.microsoft.com/gaming
- Sony PlayStation Audio Standards
- "Loudness in Game Audio" — GDC talks (Soundcrafter et al.)
- Dolby Atmos / Dolby Digital loudness recommendations
- ReplayGain (predecessor to LUFS for music) — replaygain.org
- *Sound Engineer's Pocket Book* — Michael Talbot-Smith
- "True Peak Detection" — McGill / iZotope white papers
