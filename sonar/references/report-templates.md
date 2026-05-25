# Report Templates & Pipeline Structures

QC report formats (Markdown / JSON), batch pipeline structure, and CI-gate exit-code convention.

## Markdown QC Report Template

```markdown
# Audio Analysis Report

**File:** `path/to/track.wav`
**Target Platform:** Spotify (Integrated -14 LUFS, True Peak -1.0 dBTP)
**Measured:** 2026-05-25T10:00:00Z
**Tools:** ffprobe 6.0, pyloudnorm 0.1.1, librosa 0.10.1
**Standards:** ITU-R BS.1770-4, EBU R128

## Format

| Property | Value |
|----------|-------|
| Codec | PCM s24le |
| Sample rate | 48000 Hz |
| Channels | 2 (stereo) |
| Bit depth | 24-bit |
| Duration | 3:42 (222.0 s) |
| Bitrate | 2304 kbps |

## Loudness (BS.1770-4)

| Measurement | Value | Target | Verdict |
|-------------|-------|--------|---------|
| Integrated | -13.2 LUFS | -14 LUFS | WARN (+0.8 LU over) |
| True Peak | -0.6 dBTP | -1.0 dBTP | FAIL (+0.4 dB over ceiling) |
| LRA | 6.4 LU | — | INFO (compressed) |
| PLR | 12.6 dB | ≥9 dB | PASS |

**Predicted normalization:** Spotify will reduce by −0.8 LU; True Peak after platform shift = −1.4 dBTP (safe post-normalization).
**Remediation:** The post-normalization TP is safe, but the **master itself** ships above the −1.0 dBTP ceiling and may transcode-distort before normalization is applied. Re-render with a true-peak limiter at −1.0 dBTP regardless — the FAIL is a master-side issue, not a normalization-side issue.

## Acoustic

| Measurement | Value | Confidence |
|-------------|-------|-----------|
| BPM | 128.0 | High |
| Key | A minor | High (0.84) |
| Time signature | 4/4 | High |

## Spectral Balance

| Band | Energy (dB rel mid) | Notes |
|------|---------------------|-------|
| 20–60 Hz (sub low) | -4.0 | PASS |
| 60–250 Hz (bass) | +1.0 | PASS |
| 250–2000 Hz (mids) | 0.0 | PASS (reference) |
| 2000–8000 Hz (presence) | +1.5 | PASS |
| 8000–20000 Hz (air) | -1.0 | PASS |

## Quality Issues

| Check | Severity | Value | Notes |
|-------|----------|-------|-------|
| Sample-peak clipping | PASS | 0 samples | — |
| True-peak overshoot | FAIL | -0.6 dBTP | Exceeds -1.0 ceiling |
| DC offset | PASS | L:0.001 R:0.001 | — |
| Phase correlation | PASS | 0.62 | Healthy stereo image |
| Mono compatibility | PASS | 1.8 dB sum loss | — |
| Excessive limiting | PASS | PLR 12.6 dB | Dynamic master |

## Findings Summary

- **1 FAIL** — True Peak overshoot. Block release until fixed.
- **1 WARN** — Integrated LUFS 0.8 LU above Spotify target. Acceptable (platform will normalize), but consider re-master if you want unprocessed delivery.

## Recommended Next Action

1. Apply true-peak limiter at -1.0 dBTP, re-render.
2. Re-run Sonar `qc` to confirm PASS.
3. Route to Judge for release-gate sign-off.

## Reproducibility

Pipeline: `analyze.py` (see attached). Pinned versions: librosa>=0.10.1,<0.11, pyloudnorm>=0.1.1, ffmpeg>=6.0.
```

## JSON Report Schema

```json
{
  "schema_version": "1.0",
  "file": {
    "path": "path/to/track.wav",
    "size_bytes": 64012800,
    "sha256": "..."
  },
  "measured_at": "2026-05-25T10:00:00Z",
  "tools": {
    "ffprobe": "6.0",
    "pyloudnorm": "0.1.1",
    "librosa": "0.10.1"
  },
  "standards": ["ITU-R BS.1770-4", "EBU R128"],
  "target": {
    "platform": "spotify",
    "integrated_lufs": -14.0,
    "true_peak_dbtp": -1.0,
    "lra_max": null
  },
  "format": {
    "codec": "pcm_s24le",
    "sample_rate": 48000,
    "channels": 2,
    "channel_layout": "stereo",
    "bit_depth": 24,
    "duration_sec": 222.0,
    "bitrate_bps": 2304000
  },
  "loudness": {
    "integrated_lufs": -13.2,
    "true_peak_dbtp": -0.6,
    "lra": 6.4,
    "plr_db": 12.6,
    "predicted_normalization": {
      "gain_shift_db": -0.8,
      "true_peak_after_shift_dbtp": -1.4
    }
  },
  "acoustic": {
    "bpm": 128.0,
    "bpm_confidence": "high",
    "key": "A minor",
    "key_confidence": 0.84,
    "time_signature": "4/4"
  },
  "spectral": {
    "bands_db_rel_mid": {
      "20_60": -4.0,
      "60_250": 1.0,
      "250_2000": 0.0,
      "2000_8000": 1.5,
      "8000_20000": -1.0
    }
  },
  "quality_findings": [
    {
      "check": "true_peak_overshoot",
      "severity": "FAIL",
      "value_db": -0.6,
      "threshold_db": -1.0,
      "remediation": "Apply true-peak limiter at -1.0 dBTP, re-render"
    }
  ],
  "summary": {
    "fail_count": 1,
    "warn_count": 1,
    "pass_count": 5,
    "verdict": "FAIL",
    "next_action": "Re-render with TP limiter; re-run sonar qc"
  }
}
```

## Batch Pipeline Structure

```python
# batch.py — analyze every audio file in a directory in parallel
import sys, json
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

AUDIO_EXT = {".wav", ".flac", ".aiff", ".mp3", ".m4a", ".aac", ".ogg", ".opus"}

def analyze_one(path: str) -> dict:
    # Combine: format, loudness, acoustic, quality.
    # IMPORTANT: import from `format_inspect`, NOT `inspect` — Python's stdlib has an
    # `inspect` module that would shadow a user module of the same name.
    from format_inspect import ffprobe_inspect
    from loudness import measure_loudness
    from acoustic import detect_bpm_and_key
    from quality import quality_scan
    return {
        "path": path,
        "format": ffprobe_inspect(path),
        "loudness": measure_loudness(path),
        "acoustic": detect_bpm_and_key(path),
        "quality": quality_scan(path),
    }

def main(root: str, out_json: str):
    files = [str(p) for p in Path(root).rglob("*") if p.suffix.lower() in AUDIO_EXT]
    results = []
    with ProcessPoolExecutor() as pool:
        futures = {pool.submit(analyze_one, f): f for f in files}
        for fut in as_completed(futures):
            try:
                results.append(fut.result())
            except Exception as e:
                results.append({"path": futures[fut], "error": str(e)})
    Path(out_json).write_text(json.dumps(results, indent=2))
    print(f"Analyzed {len(results)} files → {out_json}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "batch_report.json")
```

## CI-Gate Convention

A QC pipeline used in CI should exit nonzero on FAIL so the pipeline blocks merge / release.

```python
# ci_gate.py
import sys, json
from pathlib import Path

# Exit codes:
#   0 = all PASS
#   1 = one or more WARN, zero FAIL (advisory)
#   2 = one or more FAIL (blocks release)

def evaluate(report: dict) -> int:
    summary = report.get("summary", {})
    fail = summary.get("fail_count", 0)
    warn = summary.get("warn_count", 0)
    if fail > 0:
        print(f"FAIL: {fail} hard finding(s) — release blocked")
        return 2
    if warn > 0:
        print(f"WARN: {warn} advisory finding(s)")
        return 1
    print("PASS")
    return 0

if __name__ == "__main__":
    report = json.loads(Path(sys.argv[1]).read_text())
    sys.exit(evaluate(report))
```

GitHub Actions example:

```yaml
- name: Audio QC gate
  run: |
    python analyze.py "release/master.wav" --target spotify --output report.json
    python ci_gate.py report.json
```

## Reference Comparison Report

```markdown
# Reference Comparison

**Target:** path/to/master.wav
**Reference:** path/to/reference.wav

## Loudness Delta

| Measurement | Target | Reference | Delta | Verdict |
|-------------|--------|-----------|-------|---------|
| Integrated LUFS | -13.2 | -14.0 | +0.8 | Target louder |
| True Peak (dBTP) | -0.6 | -1.0 | +0.4 | Target peakier |
| LRA | 6.4 | 8.1 | -1.7 | Target more compressed |

## Spectral Delta (dB per band, target − reference)

| Band | Delta | Notes |
|------|-------|-------|
| 20–60 Hz | -1.5 | Target lighter on sub |
| 60–250 Hz | +0.8 | Slightly bassier |
| 250–2000 Hz | 0.0 | Aligned |
| 2000–8000 Hz | +2.1 | Brighter |
| 8000–20000 Hz | -0.5 | Slightly less air |

## Recommendation

Target is louder and brighter than reference. To match:
- Reduce master gain by ~0.8 LU.
- Cut 2–8 kHz by ~2 dB.
- Slight low-shelf cut at 60–250 Hz (-0.8 dB).
- Re-render and re-compare.
```

## Output File Naming Convention

| Artifact | Default name |
|----------|-------------|
| Markdown report | `{stem}_sonar_report.md` |
| JSON report | `{stem}_sonar_report.json` |
| Spectrogram | `{stem}_spectrogram.png` |
| Waveform | `{stem}_waveform.png` |
| Loudness history | `{stem}_loudness.png` |
| Batch aggregate | `batch_report.json` + `batch_summary.csv` |
| Pipeline script | `analyze.py`, `qc.py`, `compare.py`, `batch.py` |
