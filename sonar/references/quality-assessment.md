# Quality Assessment Checks

Issue detection logic, severity rubrics, and remediation hints for audio file quality assessment.

## Issue Catalog

| Issue | Severity rubric | Detection |
|-------|----------------|-----------|
| Sample-peak clipping | FAIL if any sample = ±1.0 | `np.abs(y).max() >= 1.0` |
| True-peak overshoot | FAIL if TP > platform ceiling | 4x oversampling + peak detect (manual — pyloudnorm 0.1.x has no built-in TP method) |
| Inter-sample peak | WARN if ISP > -1.0 dBTP and sample peak < 0 dBFS | True-peak minus sample peak comparison |
| DC offset | WARN if mean ≠ 0 ±0.01 | `np.mean(y)` per channel |
| Phase inversion | FAIL if L/R correlation < -0.3 | `np.corrcoef(L, R)` |
| Mono incompatibility | WARN if mono sum loss > 3 dB | Compare stereo LUFS vs L+R mono-sum LUFS |
| Frequency masking | WARN if bands > 10 dB above adjacent | Spectral analysis + band comparison |
| Excessive limiting | WARN if PLR < 6 dB | True Peak − Integrated LUFS |
| Dead air / silence | WARN if start/end > 2 s silence | RMS < -60 dBFS for > 2 s |
| Sample-rate mismatch | WARN if SR ≠ delivery target | ffprobe vs target |
| Bit depth degradation | WARN if int16 master expected int24 | ffprobe codec info |
| Encoder artifacts | INFO if lossy source | ffprobe codec name |
| Aliasing | WARN if HF energy above Nyquist/2 with rolloff | Spectral analysis at top 10% of Nyquist |
| Pre-ringing | INFO if linear-phase mastering EQ used | Impulse response analysis (rarely needed) |

## Clipping Detection

### Sample-peak clipping
```python
import soundfile as sf
import numpy as np

y, sr = sf.read(path, always_2d=True)
clipped_samples = np.sum(np.abs(y) >= 0.9999)
clip_ratio = clipped_samples / y.size
# FAIL if clip_ratio > 0 (even one clipped sample is a finding)
# Severity escalates with ratio:
#   >0 and ≤1e-6: WARN (incidental)
#   >1e-6 and ≤1e-3: FAIL (audible)
#   >1e-3: FAIL (mastering error)
```

### True-peak clipping (inter-sample peaks)
Sample-peak measurement misses peaks that occur **between** samples after DAC reconstruction. Streaming codecs (AAC, Opus, MP3) make this worse.

```python
import pyloudnorm as pyln

meter = pyln.Meter(sr)  # BS.1770-4
y_int = y[:, 0] if y.ndim == 2 else y  # one channel example
# True peak via 4x oversampling
from scipy.signal import resample_poly
y_4x = resample_poly(y_int, 4, 1)
true_peak_db = 20 * np.log10(np.abs(y_4x).max() + 1e-12)
# FAIL if true_peak_db > -1.0 (Spotify/Apple ceiling)
```

## Phase Issues

### L/R correlation
```python
L, R = y[:, 0], y[:, 1]
corr = np.corrcoef(L, R)[0, 1]
# +1.0 = identical (mono)
# 0.0 = independent
# -1.0 = fully inverted (cancellation on mono sum)
# Canonical thresholds (use these consistently — sample-peak code at tool-stack.md Template 8 matches):
#   corr >  0.3 → PASS (healthy stereo)
#   corr in [-0.3, 0.3] → WARN (wide / loose stereo, common in production but check intent)
#   corr < -0.3 → FAIL (likely phase issue, mono-sum cancellation)
```

### Mono sum loss
```python
stereo_lufs = meter.integrated_loudness(np.stack([L, R], axis=1))
mono_sum_lufs = meter.integrated_loudness(0.5 * (L + R))
loss = stereo_lufs - mono_sum_lufs
# 0-2 dB: normal
# 2-3 dB: WARN (significant phase content)
# >3 dB: FAIL (mono-incompatible; check for inverted side material)
```

## DC Offset

```python
dc_per_channel = np.mean(y, axis=0)
# WARN if any |dc| > 0.005 (-46 dBFS); FAIL if > 0.01
# Remediation: high-pass filter at 20 Hz before delivery
```

## Frequency Masking

Inter-band masking analysis — identifies frequency bands so loud they mask adjacent content.

```python
import librosa
import numpy as np

S = np.abs(librosa.stft(y_mono)) ** 2
mel = librosa.feature.melspectrogram(S=S, sr=sr, n_mels=32)
mel_db = librosa.power_to_db(mel)
band_means = mel_db.mean(axis=1)  # per-band average dB

# Check for >10 dB jumps between adjacent bands
for i in range(1, len(band_means) - 1):
    if band_means[i] > band_means[i-1] + 10 and band_means[i] > band_means[i+1] + 10:
        flag(f"Band {i} masking adjacent content")
```

## Excessive Limiting

```python
true_peak_db = ...  # see above
integrated_lufs = meter.integrated_loudness(y_mono)
plr = true_peak_db - integrated_lufs
# PLR ≥ 12 dB: dynamic master (good for streaming)
# PLR 9-12 dB: typical pop master
# PLR 6-9 dB: aggressive limiting (WARN for streaming, normal for radio/TikTok)
# PLR < 6 dB: over-limited (FAIL — streaming will turn it down anyway; you lost dynamics for nothing)
```

## Silence Detection

```python
import librosa

# Trim silence
y_trimmed, idx = librosa.effects.trim(y_mono, top_db=60)
leading_silence = idx[0] / sr
trailing_silence = (len(y_mono) - idx[1]) / sr
# WARN if leading > 0.5 s (most platforms allow ≤500ms)
# WARN if trailing > 2.0 s (fade-out tail OK; pure silence wastes bandwidth)
```

## Sample-Rate / Bit-Depth Consistency

```bash
ffprobe -v error -select_streams a:0 \
  -show_entries stream=sample_rate,bits_per_raw_sample,bits_per_sample,codec_name,channel_layout \
  -of json input.wav
```

Verdict matrix:
| Source | Target | Action |
|--------|--------|--------|
| 96 kHz / 24-bit master | 44.1 kHz / 16-bit (CD) | SRC + dither (FAIL if dither absent) |
| 48 kHz / 24-bit master | 44.1 kHz / 16-bit | SRC + dither |
| 44.1 kHz / 24-bit master | 44.1 kHz / 16-bit | Dither only |
| 44.1 kHz / 16-bit | 44.1 kHz / 16-bit | Pass-through |
| 44.1 kHz / 24-bit | Streaming (lossy) | Streaming transcodes; deliver 44.1/24 |
| Any | Streaming hi-res (Tidal Master / Apple Lossless) | 96 kHz / 24-bit max |

## Aliasing Detection

```python
nyquist = sr / 2
S = np.abs(librosa.stft(y_mono))
freqs = librosa.fft_frequencies(sr=sr)
top_band_energy = S[(freqs > 0.95 * nyquist)].mean()
total_energy = S.mean()
# WARN if top_band_energy / total_energy > 0.05 (likely aliasing from upstream SRC)
```

## Severity Tagging

Use three-level severity in every QC report:

- **PASS**: measurement within target / no issue detected.
- **WARN**: out of ideal range but acceptable; cite the threshold.
- **FAIL**: violates a hard requirement (platform ceiling, distribution standard, audible degradation); requires remediation before delivery.

Always include:
1. The measured value.
2. The threshold and source standard.
3. The remediation hint (re-master / re-encode / accept-with-rationale).

## Remediation Hint Catalog

| Issue | Standard fix |
|-------|-------------|
| Sample-peak clipping | Reduce master gain; re-render; or apply true-peak limiter at -1.0 dBTP |
| True-peak overshoot | True-peak limiter (Sonnox Limiter v3, Fabfilter Pro-L 2, izotope Maximizer) with TP detection on |
| DC offset | High-pass at 20 Hz, 12 dB/oct |
| Phase inversion | Check polarity per channel; flip the inverted one |
| Mono incompatibility | Reduce side-channel content (mid/side EQ low-cut on side) |
| Excessive limiting | Reduce limiter ceiling input; re-master with more headroom |
| Frequency masking | Spectral EQ cut on the masking band |
| SR mismatch | High-quality SRC (SoX, izotope RX, Weiss Saracon) + dither for bit-depth reduction |
| Dead air | Trim to ≤500 ms leading silence, ≤2 s trailing |
