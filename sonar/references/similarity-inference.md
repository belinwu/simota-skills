# Similarity Inference: Similar Tracks, Instruments, Effectors

Methods, ML models, and heuristics for **inference** outputs (vs measurements). Every output here is INFERENCE and MUST carry a confidence interval (`confidence: 0.0-1.0`) and method/model name. Never report an inference as a measurement.

## Measurement vs Inference (Core Rule)

| Type | Examples | Reporting requirement |
|------|----------|----------------------|
| **Measurement** | LUFS, dBTP, BPM, key, spectral centroid | Cite the standard (BS.1770-4, etc.) |
| **Inference** | Instrument labels, effector family, similar tracks, fingerprint match | Cite the model + confidence interval |

**Never** emit an instrument or effector label without `confidence` and `method`. **Never** assert "this track uses [specific plugin name or hardware model]" — sonar can infer **effect family** (e.g., "plate-style reverb, RT60 ≈ 1.4s, confidence: 0.71") but not plugin identity.

## A. Similar-Track Recommendation

### Approach Matrix

| Approach | Source | Cost | Privacy | When to use |
|----------|--------|------|---------|-------------|
| **Last.fm `track.getSimilar`** | Last.fm API | Free | No audio upload | Popular tracks with prior plays |
| **ListenBrainz CF** | MetaBrainz | Free | No audio upload | MBID-anchored; pairs with AcoustID identification |
| **Local CLAP embedding k-NN** | LAION-CLAP local | Compute only | **All local — best privacy** | Indie, unreleased, sensitive audio; primary recommended path |
| **OpenL3 embedding k-NN** | openl3 local | Compute only | Local | Alternative to CLAP; larger 6144-dim vectors |
| **MusicBrainz tag overlap** | MusicBrainz | Free | No audio upload | Crude fallback; tag-based co-occurrence |
| **MSAF structural distance** | msaf local | Compute only | Local | "Structurally similar" niche queries |
| **Spotify `/v1/recommendations`** | Spotify API | — | — | **DEPRECATED 2024-11-27 for new apps. Do not target.** |

### CLAP Embedding k-NN (recommended default)

LAION-CLAP (Contrastive Language-Audio Pretraining) — Apache 2.0 license, joint audio+text embeddings, 512-dim, supports zero-shot queries.

```python
# pip install transformers librosa torch scikit-learn faiss-cpu
from transformers import ClapModel, ClapProcessor
from sklearn.neighbors import NearestNeighbors
import librosa, numpy as np, glob, torch

proc = ClapProcessor.from_pretrained("laion/clap-htsat-unfused")
model = ClapModel.from_pretrained("laion/clap-htsat-unfused").eval()

def embed(path: str) -> np.ndarray:
    y, _ = librosa.load(path, sr=48000, mono=True)
    with torch.no_grad():
        inp = proc(audios=y, sampling_rate=48000, return_tensors="pt")
        return model.get_audio_features(**inp).squeeze().numpy()

# Build local corpus index (one-time)
corpus = {p: embed(p) for p in glob.glob("library/*.wav")}
mat = np.stack(list(corpus.values()))
knn = NearestNeighbors(n_neighbors=5, metric="cosine").fit(mat)

# Query
query = embed("unknown.wav")
dist, idx = knn.kneighbors(query.reshape(1, -1))
paths = list(corpus)
results = [
    {
        "path": paths[i],
        "similarity": float(1 - d),  # cosine sim from cosine dist
        "method": "LAION-CLAP htsat-unfused k-NN",
        "confidence": float(1 - d),  # similarity == confidence for k-NN
    }
    for d, i in zip(dist[0], idx[0])
]
```

### Last.fm Path (popular tracks, metadata-mode)

```python
# pip install requests
import os, requests
LASTFM_KEY = os.environ["LASTFM_API_KEY"]

def lastfm_similar(artist: str, track: str, limit: int = 20) -> list[dict]:
    r = requests.get("http://ws.audioscrobbler.com/2.0/", params={
        "method": "track.getsimilar", "artist": artist, "track": track,
        "api_key": LASTFM_KEY, "format": "json", "limit": limit,
    })
    return [
        {
            "title": t["name"], "artist": t["artist"]["name"],
            "similarity": float(t.get("match", 0)),  # 0-1
            "method": "lastfm.track.getSimilar",
            "confidence": float(t.get("match", 0)),
        }
        for t in r.json().get("similartracks", {}).get("track", [])
    ]
```

### Industry Reference

Spotify's Discover Weekly historically combines collaborative filtering, NLP over playlist/blog text, and raw audio CNN features (Sander Dieleman 2014). Apple Music's similarity layer is undocumented; Shazam-backed track ID feeds it. No fully open replication exists — local CLAP-embedding k-NN is the closest open-source equivalent.

## B. Instrument Detection (Multi-Label)

### Model Matrix

| Model | License | Training data | Output | Speed | Recommended? |
|-------|---------|--------------|--------|-------|--------------|
| **LAION-CLAP htsat-unfused** | **Apache 2.0** | LAION-Audio-630K (633k audio-text pairs) | Zero-shot label confidence per arbitrary candidate label | Medium | **Primary — Apache, zero-shot, flexible** |
| **AST (Audio Spectrogram Transformer)** | BSD-3 (code) / MIT (weights) | AudioSet | 527 AudioSet tags (incl. instruments) | Medium | Secondary; AudioSet-tagged baseline |
| **YAMNet** | Apache 2.0 | AudioSet (Google) | 521 AudioSet tags | Fast | Fallback; Keras 2 only — needs `tf-keras` shim for TF 2.16+ |
| **OpenL3** | MIT (code) / CC BY 4.0 (weights) | AudioSet | Embeddings (512/6144-dim) — not a classifier itself | Medium | Use as feature extractor + sklearn head |
| **PaSST** | MIT | AudioSet | AudioSet tags, transformer | Slow | Higher accuracy alternative to AST |
| **Essentia MTG-Jamendo instrument (`mtg-jamendo-instrument-discogs-effnet`)** | AGPLv3 (lib) + **CC BY-NC-ND 4.0 (weights)** | MTG-Jamendo | 40 instrument classes | Medium | **NON-COMMERCIAL ONLY** — blocks commercial sonar use without UPF license |
| **Essentia Discogs-EffNet** | AGPLv3 + **CC BY-NC-SA 4.0** | Discogs styles | Embeddings + 400/519 style logits | Medium | NON-COMMERCIAL |
| **OpenMIC-2018** | CC-BY | OpenMIC-2018 | 20 instruments (music-specific) | Medium | Music-domain-tuned; good for ensemble |
| **demucs v4 (HT-Demucs)** | MIT | MUSDB18 + extras | **Separation** (drums/bass/vocals/other) — not classification | Slow | Use stem RMS as instrument-presence proxy |
| **spleeter** | MIT | Deezer internal | 2/4/5-stem separation | Fast | Lower quality than demucs but faster |
| **Whisper** | MIT | Multilingual speech | Speech transcription + lang ID | Medium | Vocal-detection proxy (high-confidence transcription → vocals present) |
| **openSMILE (eGeMAPS / ComParE)** | **Dual — research only / commercial requires audEERING contract** | — | 88 / 6k-dim acoustic feature vectors | Fast | Best for paralinguistic / voice; complement to MIR features |

### CLAP Zero-Shot Instrument Check (recommended default, Apache 2.0)

```python
# pip install transformers librosa torch
from transformers import pipeline
import librosa

audio, sr = librosa.load("track.wav", sr=48000, mono=True)
clf = pipeline("zero-shot-audio-classification", model="laion/clap-htsat-unfused")

INSTRUMENT_LABELS = [
    "electric guitar", "acoustic guitar", "bass guitar",
    "piano", "synthesizer", "organ",
    "drum kit", "percussion", "cymbals",
    "vocals", "choir", "rap vocals",
    "violin", "cello", "strings",
    "trumpet", "saxophone", "brass section",
]
raw = clf(audio, candidate_labels=INSTRUMENT_LABELS)

# Honesty: surface confidence + model on every label
results = [
    {"instrument": r["label"], "confidence": float(r["score"]),
     "method": "LAION-CLAP htsat-unfused (zero-shot)"}
    for r in raw if r["score"] > 0.1  # filter very low confidence
]
```

### Demucs Per-Stem Presence Proxy

For more robust drum / bass / vocals / other detection (when full-band classification is uncertain), use demucs separation + per-stem RMS:

```python
# CLI: python -m demucs --two-stems=vocals track.wav  (or default 4-stem)
import librosa, numpy as np, glob

def stem_presence(stems_dir: str) -> list[dict]:
    out = []
    for stem_path in glob.glob(f"{stems_dir}/*.wav"):
        y, sr = librosa.load(stem_path, sr=None, mono=True)
        rms = float(np.sqrt((y**2).mean()))
        rms_db = 20 * np.log10(rms + 1e-9)
        present = rms_db > -40  # threshold: -40 dBFS RMS = audible
        out.append({
            "stem": stem_path.split("/")[-1].replace(".wav", ""),
            "rms_dbfs": round(rms_db, 1),
            "present": present,
            "confidence": min(1.0, max(0.0, (rms_db + 60) / 30)),  # crude confidence
            "method": "demucs v4 + RMS threshold (-40 dBFS)",
        })
    return out
```

### Ensemble Recommendation

For high-stakes instrument detection:
1. Run **CLAP zero-shot** with full label set → primary confidence.
2. Run **demucs separation** → stem-RMS proxy → confirms drums/bass/vocals presence.
3. If CLAP confidence ≥ 0.5 AND stem-RMS confirms → report with combined confidence.
4. If they disagree → report both methods' verdicts separately; never silently pick one.

## C. Effector Inference

**Soft territory**: no canonical libraries. All effector outputs are **heuristic inferences** from spectral, dynamic, and stereo analysis. Confidence is generally lower (0.3-0.8 range). **Never claim plugin or hardware brand identity** — only effect-family inference.

### Effect Catalog

| Effect family | Method | Library / approach | Confidence ceiling |
|---------------|--------|-------------------|--------------------|
| **Reverb (RT60)** | Schroeder backward integration of squared impulse response; blind estimation from non-overlapping decays in music | `pyroomacoustics.experimental.measure_rt60` (MIT, Python ≥3.9), `python-acoustics`, `blind-rt60` PyPI | High (with IR), Low-Medium (blind) |
| **Reverb (type: plate / spring / hall / room)** | Early-reflection density + frequency response of tail | DIY heuristic | Low-Medium (family hint only) |
| **Compression / limiting** | PLR (true_peak_dBTP − integrated_LUFS) + crest factor + short-term LRA | `pyloudnorm` + numpy | High |
| **Delay / slapback** | Autocorrelation peaks in 50-2000 ms range, excluding BPM-aligned subdivisions | `librosa.autocorrelate` on mid-channel | Medium |
| **Chorus / phaser / flanger (modulation)** | Pitch wobble in sustained tones (4-8 Hz vibrato); sideband detection in spectrogram | `librosa.pyin` for f0 + periodic-deviation analysis | Low-Medium |
| **Distortion / saturation** | THD via spectral peaks at integer harmonics of f0; harmonic ratio | `librosa.stft` + peak-picking at 2f₀, 3f₀, … | Medium |
| **Stereo width / Haas** | Side energy ratio (side = (L−R)/2, mid = (L+R)/2, width = ‖side‖/‖mid‖); Haas via cross-correlation peak position | numpy | High |
| **EQ profile** | Long-term average spectrum (LTAS) vs genre baseline | `librosa.stft` averaged over track | Medium |

### Code: Compression + Stereo Width

```python
# pip install pyloudnorm librosa numpy soundfile
import numpy as np, librosa, soundfile as sf, pyloudnorm as pyln

def infer_compression_and_width(path: str) -> dict:
    y, sr = sf.read(path, always_2d=True)  # shape (samples, channels)
    if y.shape[1] < 2:
        y_stereo = np.repeat(y, 2, axis=1)  # mono → fake stereo for width=0
    else:
        y_stereo = y[:, :2]
    L, R = y_stereo[:, 0], y_stereo[:, 1]
    mono = (L + R) / 2

    meter = pyln.Meter(sr)
    if len(mono) / sr < 0.4:
        return {"error": "too short for inference"}
    lufs_i = meter.integrated_loudness(mono)
    true_peak_dbfs = 20 * np.log10(np.max(np.abs(y_stereo)) + 1e-9)
    plr = true_peak_dbfs - lufs_i

    rms = np.sqrt((mono ** 2).mean())
    crest_db = 20 * np.log10((np.max(np.abs(mono)) + 1e-9) / (rms + 1e-9))

    side = (L - R) / 2
    mid = (L + R) / 2
    width = float(np.sqrt((side ** 2).mean()) / (np.sqrt((mid ** 2).mean()) + 1e-9))

    # Compression family heuristic
    if plr < 6:
        compression = {"family": "heavy limiting", "confidence": 0.85}
    elif plr < 9:
        compression = {"family": "moderate compression", "confidence": 0.75}
    elif plr < 13:
        compression = {"family": "light compression", "confidence": 0.65}
    else:
        compression = {"family": "minimal / dynamic master", "confidence": 0.7}

    return {
        "compression": {**compression, "method": "PLR (BS.1770-4 LUFS + true peak)",
                        "plr_db": round(plr, 1), "crest_db": round(crest_db, 1)},
        "stereo_width": {"value": round(width, 3),
                         "label": "narrow" if width < 0.2 else "wide" if width > 0.6 else "moderate",
                         "method": "side/mid energy ratio",
                         "confidence": 0.9},
    }
```

### Code: Reverb (RT60 from impulse)

```python
# pip install pyroomacoustics soundfile
import soundfile as sf
from pyroomacoustics.experimental.rt60 import measure_rt60

def measure_reverb_rt60(impulse_path: str) -> dict:
    ir, sr = sf.read(impulse_path)
    # T30 measured, extrapolated to RT60
    rt60_s = measure_rt60(ir, fs=sr, decay_db=30, plot=False)
    return {
        "rt60_seconds": round(float(rt60_s), 3),
        "method": "pyroomacoustics Schroeder integration (T30 → RT60)",
        "confidence": 0.9,  # high when an impulse is available
        "note": "Blind RT60 on full music mix is lower-confidence (0.4-0.6)",
    }
```

### Code: Delay Detection

```python
import numpy as np, librosa

def detect_delay(audio_path: str) -> dict:
    y, sr = librosa.load(audio_path, sr=None, mono=True)
    # Autocorrelation
    ac = librosa.autocorrelate(y, max_size=int(2 * sr))  # up to 2 seconds
    # Detect peaks excluding the trivial lag=0
    ac = ac / ac.max()
    peaks = []
    for lag in range(int(0.05 * sr), len(ac)):  # 50ms minimum
        if ac[lag] > 0.3 and ac[lag] > ac[lag - 1] and ac[lag] > ac[lag + 1] if lag + 1 < len(ac) else False:
            peaks.append((lag / sr * 1000, float(ac[lag])))  # (ms, strength)
    peaks.sort(key=lambda p: -p[1])
    if not peaks:
        return {"delay_detected": False, "method": "autocorrelation", "confidence": 0.7}
    return {
        "delay_detected": True,
        "candidates_ms": [{"delay_ms": round(p[0], 1), "strength": round(p[1], 3)} for p in peaks[:5]],
        "method": "librosa.autocorrelate peak-picking (50ms-2000ms range)",
        "confidence": 0.6,
        "note": "BPM-aligned peaks are likely rhythm, not delay — cross-check with detected BPM",
    }
```

## D. Confidence Reporting Schema

Every inference output must follow this schema:

```python
{
    # Required fields
    "value": <any>,                  # the inferred label / number
    "confidence": <float 0.0-1.0>,   # how sure the model/method is
    "method": <string>,              # model name + version OR heuristic name
    # Optional
    "method_version": <string>,
    "alternatives": [...],           # other candidates with their confidences (esp. for fingerprint match)
    "anchor": <string>,              # which measured feature grounded this inference
    "note": <string>,                # caveats, e.g. "blind estimation lower confidence"
}
```

**Disallowed**: emitting an inference label without `confidence` and `method`. This is a Core Contract violation.

## E. Library Pins

```python
# Embedding + classification
transformers>=4.40       # LAION-CLAP, AST, PaSST via HF
tensorflow-hub>=0.16     # YAMNet (note: needs tf-keras shim for TF 2.16+)
tf-keras                 # YAMNet compatibility shim
openl3>=0.4.2            # OpenL3 embeddings
laion-clap>=1.1.6        # Alternative to transformers-based CLAP
panns-inference>=0.1.1   # PANNs audio tagging
scikit-learn>=1.4        # k-NN, classifiers
faiss-cpu>=1.8           # Large embedding indexes
torch>=2.1               # PyTorch backend

# Separation
demucs>=4.0.1            # MIT, recommended
spleeter>=2.4.0          # MIT, fast alternative

# Speech / vocal proxy
openai-whisper           # MIT, Whisper

# Effector heuristics
pyroomacoustics>=0.10.1  # MIT, RT60 measurement
pyloudnorm>=0.1.1        # BS.1770-4 LUFS for PLR
librosa>=0.10.1,<0.13    # Spectral / autocorrelation

# Caveats
# openSMILE: dual-license, commercial requires audEERING contract
# Essentia models (MTG-Jamendo, Discogs-EffNet, MAEST): CC BY-NC — non-commercial only
```

## F. Decision Matrix

| Goal | Primary path | Fallback / alternative |
|------|--------------|----------------------|
| Multi-label instrument detection (Apache OK) | LAION-CLAP zero-shot | AST AudioSet tagger |
| Verify drum/bass/vocals presence | demucs v4 stems + RMS | spleeter (faster, lower quality) |
| Vocal-only detection | Whisper (high-confidence transcription) | CLAP zero-shot "vocals" label |
| Similar tracks (popular catalog) | Last.fm `track.getSimilar` | ListenBrainz CF |
| Similar tracks (privacy / indie) | Local CLAP-embedding k-NN | OpenL3 k-NN |
| Reverb RT60 (with IR) | pyroomacoustics Schroeder | python-acoustics |
| Reverb RT60 (blind, mix) | Use lower-confidence label; flag method | Skip; report "RT60 requires impulse" |
| Compression intensity | PLR + crest factor (pyloudnorm) | Short-term LRA |
| Delay / slapback | librosa.autocorrelate (50-2000ms, ex-BPM peaks) | DIY |
| Stereo width | side/mid energy ratio (numpy) | — |
| Distortion / THD | librosa.stft + harmonic peak-picking | — |
