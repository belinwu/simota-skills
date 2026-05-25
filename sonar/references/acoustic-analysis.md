# Acoustic & Structural Analysis

Methods, library selection, and parameter guidance for BPM, key, time signature, beat tracking, spectral analysis, and structural segmentation.

## Library Selection Matrix

| Task | Primary library | Secondary | Notes |
|------|----------------|-----------|-------|
| BPM / tempo | `librosa.beat.tempo` | `madmom.features.tempo`, `essentia.RhythmExtractor2013` | madmom most accurate for popular music; essentia for batch |
| Beat tracking | `librosa.beat.beat_track` | `madmom.features.beats.RNNBeatProcessor` | madmom RNN model best on irregular meter |
| Downbeat / time signature | `madmom.features.downbeats.RNNDownBeatProcessor` | `essentia.BeatTrackerMultiFeature` | librosa alone cannot reliably infer downbeat |
| Key / scale | `librosa` chroma + Krumhansl profile | `essentia.KeyExtractor`, `madmom.features.key` | essentia KeyExtractor is the most accurate single call |
| Chord recognition | `madmom.features.chords.CNNChordFeatureProcessor` | `essentia.ChordsDetection` | CNN-based outperforms template-matching |
| Onset detection | `librosa.onset.onset_detect` | `madmom.features.onsets` | librosa default fine for most |
| Spectral features | `librosa.feature.*` | `essentia.SpectralCentroid`, `MFCC`, etc. | librosa is the lingua franca |
| Structural segmentation | `librosa.segment` + `msaf` | `essentia.SBic` | msaf wraps multiple algorithms |
| Tempo curve / variable BPM | `librosa.beat.plp` | `madmom.features.tempo` per-frame | PLP (Predominant Local Pulse) for tempo modulation |

## BPM / Tempo Detection

### Method choice
- **Static tempo (popular music, EDM, hip-hop)**: `librosa.beat.tempo(y=y, sr=sr)[0]` — single Python call, ~95% accuracy on 4/4 pop. (Note: keyword-only args since librosa 0.10; in 0.11+ the canonical path is `librosa.feature.rhythm.tempo`, with `librosa.beat.tempo` retained as a deprecation alias.)
- **Variable tempo (live recordings, classical)**: `librosa.beat.plp` for tempo curve.
- **Irregular meter (jazz, prog rock, world)**: madmom RNN models, slower but accurate.

### Octave error trap
Tempo detection often returns half or double the true BPM. Resolve with:
- Multiple-hypothesis check: compare `bpm`, `bpm/2`, `bpm*2` against perceptual range (40-200 BPM).
- Genre prior: hip-hop usually 80-100, drum-and-bass 160-180, house 120-130.
- Beat-period autocorrelation peak ratio.

### Parameter defaults
- `hop_length=512` (default at sr=22050 → 23 ms resolution).
- `aggregate=numpy.median` for robustness to outliers.
- For madmom: `RNNBeatProcessor()` + `DBNBeatTrackingProcessor(min_bpm=60, max_bpm=200, fps=100)`.

## Key Detection

### Krumhansl-Schmuckler profile (librosa baseline)
1. Compute chromagram (`librosa.feature.chroma_cqt`).
2. Average across time → 12-bin profile.
3. Correlate against 24 major/minor key templates.
4. Highest-correlation key wins.

### Essentia KeyExtractor (recommended for production)
```python
import essentia.standard as es
loader = es.MonoLoader(filename=path, sampleRate=44100)
audio = loader()
key_extractor = es.KeyExtractor()
key, scale, strength = key_extractor(audio)
```
Returns `key` (e.g., "A"), `scale` ("major"/"minor"), `strength` (0-1 confidence).

### Common failure modes
- **Modulation tracks**: report only the dominant key; flag if strength < 0.6.
- **Atonal / drum-only**: key meaningless; check chromagram entropy first.
- **Edrum/EDM samples**: percussive content dominates chroma; consider HPSS (`librosa.effects.hpss`) and key-analyze harmonic component only.

## Time Signature / Downbeat

`librosa` cannot reliably detect time signature alone. Use madmom:

```python
from madmom.features.downbeats import RNNDownBeatProcessor, DBNDownBeatTrackingProcessor
proc = DBNDownBeatTrackingProcessor(beats_per_bar=[3, 4], fps=100)
activations = RNNDownBeatProcessor()(audio_path)
downbeats = proc(activations)  # [(time, beat_position), ...]
```

Confidence indicators:
- Consistent `beats_per_bar` across the track → high confidence.
- Switching between bars → likely irregular meter or detection failure.
- Always sanity-check against detected BPM and onset density.

## Spectral Analysis

### Core features
| Feature | librosa call | What it tells you |
|---------|-------------|-------------------|
| Spectral centroid | `feature.spectral_centroid` | Brightness center of mass (Hz) |
| Spectral rolloff | `feature.spectral_rolloff` | Frequency below which N% energy lies (default 85%) |
| Spectral bandwidth | `feature.spectral_bandwidth` | Spread around centroid |
| Spectral flatness | `feature.spectral_flatness` | 0 = pure tone, 1 = white noise |
| Spectral contrast | `feature.spectral_contrast` | Peak-vs-valley energy per sub-band |
| MFCC | `feature.mfcc` | Timbral fingerprint (typically 13-20 coeffs) |
| Mel-spectrogram | `feature.melspectrogram` | Perceptual frequency representation |
| Chroma | `feature.chroma_cqt` | 12-bin pitch class energy |
| Tonnetz | `feature.tonnetz` | Harmonic network features |

### Tonal balance vs reference
1. Compute average spectrum (FFT-based or Mel-based) across the full track.
2. Compute the same for the reference.
3. Diff in dB per band → tonal-balance delta.
4. Flag bands with > ±3 dB deviation.

Typical pop master tonal balance (mastered reference):
- 20-60 Hz: -6 to -3 dB (sub low)
- 60-250 Hz: 0 to +2 dB (bass / kick)
- 250-2000 Hz: 0 dB (body / vocal)
- 2000-8000 Hz: -1 to +2 dB (presence)
- 8000-20000 Hz: -3 to 0 dB (air)

## Structural Segmentation

### Approach (librosa)
1. Compute MFCC + chroma + spectral features.
2. Compute self-similarity matrix (`librosa.segment.recurrence_matrix`).
3. Apply spectral clustering or laplacian segmentation (`librosa.segment.agglomerative` or `msaf`).
4. Output segment boundaries (in seconds).

### Section labeling
Boundaries alone don't tell you which section is verse vs chorus. Heuristics:
- **Loudness / energy peak** → chorus candidate.
- **Sparse arrangement, single-section recurrence** → intro / outro.
- **Tonal centroid shift** → bridge / breakdown.
- For automatic labeling, use `msaf` with `algo_id="scluster"` and `feature="cqt"`.

### msaf example
```python
import msaf
boundaries, labels = msaf.process(audio_path, boundaries_id="scluster", labels_id="scluster")
# boundaries: ndarray of times in seconds
# labels: cluster ID per segment
```

## Stem Separation

### Demucs v4 (recommended)
```bash
demucs --two-stems=vocals input.wav  # or --four-stems
# Output: separated/htdemucs/<track_name>/{vocals,drums,bass,other}.wav
```
- Best quality on modern music as of 2024-2026.
- ~real-time on CPU; ~5-10x faster on GPU.
- Memory: ~4 GB RAM for full quality.

### Spleeter (faster, lower quality)
```bash
spleeter separate -p spleeter:4stems -o output input.wav
```
- 100x faster than Demucs.
- Quality acceptable for QC, not production stem swap.

### Per-stem analysis
After separation:
- Per-stem LUFS → bass dominance ratio, vocal-in-mix balance.
- Per-stem spectral centroid → tonal-balance per element.
- Drum-stem onset density → groove feel.

## Confidence Reporting

Every measurement must include a confidence indicator:
- **High**: tool returns explicit confidence ≥ 0.8, or two independent tools agree within tolerance.
- **Medium**: single tool, no cross-check, but result within expected range.
- **Low**: tool reports low confidence, results out of expected range, or input is atypical (atonal, very short, very compressed).

Never report a single number without a confidence tag — measurement uncertainty is part of the result.
