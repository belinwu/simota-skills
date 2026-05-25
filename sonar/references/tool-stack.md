# Tool Stack & Code Templates

Pinned library versions, install commands, and runnable code templates for the standard Sonar pipeline.

## Library Selection

| Library | Pin | Purpose | Notes |
|---------|-----|---------|-------|
| `librosa` | `>=0.10.1,<0.13` | Acoustic features, beat, spectral | De facto standard. `librosa.beat.tempo` is deprecated in 0.11+ in favor of `librosa.feature.rhythm.tempo`; both work in 0.10-0.12 |
| `pyloudnorm` | `>=0.1.1` | BS.1770-4 LUFS / True Peak | Minimal deps; recommended for LUFS |
| `soundfile` | `>=0.12.1` | WAV/FLAC/OGG read/write | Wraps libsndfile |
| `mutagen` | `>=1.47.0` | ID3, Vorbis, MP4 metadata | Pure Python |
| `numpy` | `>=1.26,<3` | Array math | Foundation |
| `scipy` | `>=1.11` | Signal processing (resample, filter) | For true-peak oversampling |
| `matplotlib` | `>=3.8` | Visualization | Spectrograms, loudness plots |
| `madmom` | `>=0.16.1` | RNN-based beat / downbeat / chord | Slower but accurate; install via git for Python 3.11+ |
| `essentia` | `>=2.1b6` | Optimized C++ MIR | Best for batch / key detection |
| `msaf` | `>=0.1.80` | Structural segmentation | Wraps multiple algorithms |
| `demucs` | `>=4.0.1` | Stem separation (recommended) | PyTorch-based |
| `spleeter` | `>=2.4.0` | Fast stem separation | TF-based; lower quality than Demucs |
| `ffmpeg` (binary) | `>=6.0` | Format read, ebur128 filter, oversampling | System install |
| `sox` (binary) | `>=14.4.2` | SRC, dither, batch utility | System install |

## Install Commands

```bash
# System binaries (macOS)
brew install ffmpeg sox

# System binaries (Debian/Ubuntu)
sudo apt-get install -y ffmpeg sox

# Core Python stack
pip install 'librosa>=0.10.1,<0.13' 'pyloudnorm>=0.1.1' 'soundfile>=0.12.1' \
            'mutagen>=1.47.0' 'numpy>=1.26' 'scipy>=1.11' 'matplotlib>=3.8'

# Optional advanced
pip install cython numpy  # madmom requires both pre-installed for source build
pip install 'madmom @ git+https://github.com/CPJKU/madmom.git'  # Py3.11+ compat from git
pip install 'essentia>=2.1b6'
pip install 'msaf>=0.1.80'

# Stem separation (heavy)
pip install 'demucs>=4.0.1'
pip install 'spleeter>=2.4.0'
```

## Reusable Code Templates

### Template 1: Format inspection (INGEST phase)

> **File-naming note**: name this file `format_inspect.py` — do NOT name it `inspect.py`. Python's stdlib has an `inspect` module; a user module of the same name shadows it and breaks `from format_inspect import ...` resolution in batch.py.

```python
# format_inspect.py — pin versions: see tool-stack.md
import subprocess, json, sys

def ffprobe_inspect(path: str) -> dict:
    cmd = [
        "ffprobe", "-v", "error", "-print_format", "json",
        "-show_format", "-show_streams", "-select_streams", "a:0", path,
    ]
    out = subprocess.check_output(cmd).decode()
    return json.loads(out)

if __name__ == "__main__":
    info = ffprobe_inspect(sys.argv[1])
    stream = info["streams"][0]
    fmt = info["format"]
    print(f"Codec:      {stream['codec_name']}")
    print(f"Sample rate:{stream['sample_rate']} Hz")
    print(f"Channels:   {stream.get('channels')}")
    print(f"Layout:     {stream.get('channel_layout', 'unknown')}")
    print(f"Bit depth:  {stream.get('bits_per_raw_sample', stream.get('bits_per_sample', 'n/a'))}")
    print(f"Duration:   {float(fmt['duration']):.2f} s")
    print(f"Bitrate:    {int(fmt.get('bit_rate', 0)) // 1000} kbps")
```

### Template 2: LUFS / True Peak measurement (MEASURE — loudness)

```python
# loudness.py
import sys
import numpy as np
import soundfile as sf
import pyloudnorm as pyln
from scipy.signal import resample_poly

def measure_loudness(path: str) -> dict:
    y, sr = sf.read(path, always_2d=True)  # shape: (samples, channels)
    # BS.1770-4 momentary block is 400 ms; shorter clips cannot be measured.
    if len(y) / sr < 0.4:
        return {"error": "audio too short for BS.1770-4 (min 400 ms required)"}
    meter = pyln.Meter(sr)  # BS.1770-4
    if y.shape[1] == 1:
        y_for_lufs = y[:, 0]
    elif y.shape[1] <= 5:
        y_for_lufs = y  # pyloudnorm supports up to 5 channels (L,R,C,Ls,Rs); LFE is NOT handled
    else:
        return {"error": f"pyloudnorm caps at 5 channels (got {y.shape[1]}); pre-downmix via ITU-R BS.775 or use ffmpeg ebur128"}
    integrated = meter.integrated_loudness(y_for_lufs)
    if integrated == float("-inf"):
        return {"error": "audio is silent (no gated blocks above -70 LUFS absolute gate)"}
    # True peak via 4x oversampling per channel.
    # NOTE: scipy.signal.resample_poly uses a Kaiser-windowed FIR by default, NOT the
    # BS.1770-4 Annex 2 reference filter. Expect ±0.1-0.5 dB drift vs ffmpeg ebur128.
    # Cross-check with Template 3 when reporting standards-grade verdicts.
    tp_db_per_channel = []
    for ch in range(y.shape[1]):
        y_4x = resample_poly(y[:, ch], 4, 1)
        peak = np.abs(y_4x).max()
        tp_db_per_channel.append(20 * np.log10(peak + 1e-12))
    true_peak = max(tp_db_per_channel)
    # PLR
    plr = true_peak - integrated
    return {
        "standard": "ITU-R BS.1770-4 / EBU R128",
        "sample_rate": sr,
        "channels": y.shape[1],
        "integrated_lufs": round(integrated, 2),
        "true_peak_dbtp": round(true_peak, 2),
        "plr_db": round(plr, 2),
    }

if __name__ == "__main__":
    result = measure_loudness(sys.argv[1])
    for k, v in result.items():
        print(f"{k:20s}: {v}")
```

### Template 3: Cross-check with ffmpeg ebur128

```bash
# loudness_ffmpeg.sh — reference implementation cross-check
ffmpeg -nostats -i "$1" -af ebur128=peak=true -f null - 2>&1 | \
  grep -E "(Integrated|True peak|Loudness range)" | tail -10
```

### Template 4: BPM / Key (MEASURE — acoustic)

```python
# acoustic.py
import sys
import librosa
import numpy as np

KRUMHANSL_MAJOR = np.array([6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88])
KRUMHANSL_MINOR = np.array([6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17])
PITCHES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

def detect_bpm_and_key(path: str) -> dict:
    # Load at native sample rate. Do NOT downsample silently — that contradicts
    # SKILL.md "Never silently resample" and degrades chroma accuracy. BPM/key
    # analysis is sample-rate-invariant; pass through whatever the file uses.
    y, sr = librosa.load(path, sr=None, mono=True)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    # librosa 0.10+ returns scalar float by default; older versions returned ndarray.
    bpm = float(np.atleast_1d(tempo)[0])
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr).mean(axis=1)
    scores = []
    for i in range(12):
        rot_major = np.roll(KRUMHANSL_MAJOR, i)
        rot_minor = np.roll(KRUMHANSL_MINOR, i)
        scores.append((np.corrcoef(chroma, rot_major)[0, 1], f"{PITCHES[i]} major"))
        scores.append((np.corrcoef(chroma, rot_minor)[0, 1], f"{PITCHES[i]} minor"))
    scores.sort(reverse=True)
    return {
        "library": "librosa>=0.10",
        "bpm": round(bpm, 2),
        "key": scores[0][1],
        "key_confidence": round(float(scores[0][0]), 3),
    }

if __name__ == "__main__":
    print(detect_bpm_and_key(sys.argv[1]))
```

### Template 5: Metadata extraction

```python
# metadata.py
import sys
from mutagen import File

def extract_metadata(path: str) -> dict:
    f = File(path)
    if f is None:
        return {"error": "unsupported format or unreadable"}
    return {
        "format": f.mime[0] if f.mime else "unknown",
        "length_sec": round(f.info.length, 2),
        "bitrate_bps": getattr(f.info, "bitrate", None),
        "sample_rate": getattr(f.info, "sample_rate", None),
        "channels": getattr(f.info, "channels", None),
        "tags": dict(f.tags) if f.tags else {},
    }

if __name__ == "__main__":
    print(extract_metadata(sys.argv[1]))
```

### Template 6: Visualization (waveform + spectrogram + loudness history)

```python
# visualize.py
import sys
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def visualize(path: str, out: str = "analysis.png") -> None:
    y, sr = librosa.load(path, sr=None, mono=True)
    fig, axes = plt.subplots(3, 1, figsize=(12, 8))
    # Waveform
    librosa.display.waveshow(y, sr=sr, ax=axes[0])
    axes[0].set_title("Waveform")
    # Mel spectrogram
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    S_db = librosa.power_to_db(S, ref=np.max)
    img = librosa.display.specshow(S_db, sr=sr, x_axis="time", y_axis="mel", ax=axes[1])
    axes[1].set_title("Mel Spectrogram (dB)")
    fig.colorbar(img, ax=axes[1], format="%+2.0f dB")
    # RMS energy over time
    rms = librosa.feature.rms(y=y)[0]
    times = librosa.times_like(rms, sr=sr)
    axes[2].plot(times, 20 * np.log10(rms + 1e-9))
    axes[2].set_title("RMS Energy (dBFS)")
    axes[2].set_xlabel("Time (s)")
    plt.tight_layout()
    plt.savefig(out, dpi=120)
    print(f"Saved: {out}")

if __name__ == "__main__":
    visualize(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "analysis.png")
```

### Template 7: Stem separation (Demucs)

```bash
# stems.sh
# Demucs v4 — htdemucs is the default high-quality model
demucs --two-stems=vocals -o ./stems "$1"
# Output: ./stems/htdemucs/<track>/vocals.wav and no_vocals.wav

# Per-stem LUFS measurement
for stem in ./stems/htdemucs/*/*.wav; do
  echo "=== $stem ==="
  python loudness.py "$stem"
done
```

### Template 8: Quality checks (clipping, phase, DC)

```python
# quality.py
import sys
import numpy as np
import soundfile as sf

def quality_scan(path: str) -> list[dict]:
    y, sr = sf.read(path, always_2d=True)
    findings = []
    # Clipping
    clipped = int(np.sum(np.abs(y) >= 0.9999))
    if clipped > 0:
        sev = "FAIL" if clipped > 1e-6 * y.size else "WARN"
        findings.append({"check": "sample_peak_clipping", "severity": sev,
                         "value": clipped, "threshold": "0 samples"})
    # DC offset
    dc = np.mean(y, axis=0)
    for ch, v in enumerate(dc):
        if abs(v) > 0.005:
            findings.append({"check": "dc_offset", "severity": "WARN" if abs(v) < 0.01 else "FAIL",
                             "channel": ch, "value": round(float(v), 4), "threshold": "±0.005"})
    # Phase (stereo only)
    if y.shape[1] == 2:
        corr = float(np.corrcoef(y[:, 0], y[:, 1])[0, 1])
        if corr < -0.3:
            findings.append({"check": "phase_inversion", "severity": "FAIL",
                             "value": round(corr, 3), "threshold": ">= -0.3"})
        elif corr < 0.3:
            findings.append({"check": "wide_stereo_image", "severity": "INFO",
                             "value": round(corr, 3)})
    if not findings:
        findings.append({"check": "all", "severity": "PASS"})
    return findings

if __name__ == "__main__":
    for f in quality_scan(sys.argv[1]):
        print(f)
```

## Sample-Rate / Channel Policy

- Always read at original sample rate first (`sr=None` or `soundfile.read` without explicit SR).
- Resample only when an algorithm requires it (most librosa defaults are 22050; you can override).
- For LUFS measurement, keep original SR — pyloudnorm handles 44.1 / 48 / 96 / 192 kHz natively.
- **pyloudnorm channel cap: 5 channels max** (L, R, C, Ls, Rs). LFE is NOT handled. 5.1 / 7.1 / Atmos sources must be pre-downmixed (ITU-R BS.775 to stereo, or LFE-stripped to 5.0) or measured via `ffmpeg -af ebur128` which handles arbitrary channel layouts. Passing 6+ channels raises `ValueError: Audio must have five channels or less.`
- For multi-channel (>2 ch), confirm downmix policy at INGEST:
  - **ITU-R BS.775 downmix** to stereo for LUFS, OR
  - per-channel / stem-wise measurement and report all channels.
