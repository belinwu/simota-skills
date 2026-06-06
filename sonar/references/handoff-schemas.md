# Handoff Schemas

Detailed inter-agent handoffs, AUTORUN `_STEP_COMPLETE` YAML, and Nexus `## NEXUS_HANDOFF` templates for Sonar.

## Collaboration Handoff Table

| Direction | Handoff | Purpose |
|-----------|---------|---------|
| Tone → Sonar | `TONE_TO_SONAR_QC` | Generated audio LUFS / True Peak / spectral QC |
| Aether → Sonar | `AETHER_TO_SONAR_TTS_QC` | AITuber TTS output loudness verification |
| Cue → Sonar | `CUE_TO_SONAR_NARRATION_QC` | Narration broadcast EBU R128 compliance |
| Director → Sonar | `DIRECTOR_TO_SONAR_DEMO_QC` | Demo video audio track loudness check |
| Lyric → Sonar | `LYRIC_TO_SONAR_MASTERING_QC` | Generated song mastering verification |
| Sonar → Tone | `SONAR_TO_TONE_MASTERING_FEEDBACK` | Re-normalize / re-render with adjusted parameters |
| Sonar → Lyric | `SONAR_TO_LYRIC_VOCAL_FEEDBACK` | Vocal alignment / pronunciation issues for re-generation |
| Sonar → Cue | `SONAR_TO_CUE_NARRATION_FEEDBACK` | Narration pacing / loudness drift for script revision |
| Sonar → Aether | `SONAR_TO_AETHER_TTS_ALERT` | Real-time TTS latency or loudness anomaly during streaming |
| Sonar → Judge | `SONAR_TO_JUDGE_RELEASE_GATE` | QC report for release-gate review |
| Sonar → Canvas | `SONAR_TO_CANVAS_VISUALIZATION` | Spectrogram / loudness-history plot handoff |
| Sonar → Scribe | `SONAR_TO_SCRIBE_REPORT` | Audio analysis report formatting |
| Sonar → Spark | `SONAR_TO_SPARK_VARIATION_SEED` | Creative variation proposal as feature/track-concept seed |
| Sonar → Compete | `SONAR_TO_COMPETE_SIMILAR_ARTIST` | Similar-artist surface for competitive/market-positioning context |
| Sonar → Lyric (rewrite) | `SONAR_TO_LYRIC_REWRITE_BRIEF` | Variation-derived re-write brief (genre/mood shift) |
| Researcher → Sonar | `RESEARCHER_TO_SONAR_METADATA_GAP` | Metadata gap-fill request for emerging-artist tracks |

## Overlap Boundaries

| Agent | Sonar owns | They own |
|-------|------------|----------|
| Tone | Measurement of audio files (existing) | Generation of audio (new) |
| Lyric | Measurement of rendered Suno output | Lyric text + style prompts |
| Cue | Narration audio loudness measurement | Narration script / storyboard |
| Aether | Stream-time TTS output verification | TTS pipeline orchestration |
| Director | Demo video audio track measurement | Playwright-based video production |
| Canvas | Producing visualization data (loudness curve, spectrogram array) | Rendering as diagrams/charts |
| Judge | Audio quality evidence collection | Release-gate verdict integration |
| Spark | Variation proposals as raw seeds (one-shot, measurement-grounded) | Feature-spec elaboration, prioritization, product framing |
| Compete | Similar-artist data surface (raw similarity list) | Competitive analysis, positioning, market sizing |
| Researcher | Fingerprint + metadata retrieval (audio-anchored) | General web research, interview design, qual analysis |
| Lyric (rewrite path) | Re-write brief derived from variation axis (genre/mood) | Lyric authoring, Suno style prompts |

## AUTORUN `_STEP_COMPLETE` Schema

```yaml
_STEP_COMPLETE:
  Agent: Sonar
  Task_Type: analyze | qc | loudness | compare | batch | stems | explore | variation
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [pipeline script + report]
    artifact_type: "python_pipeline | shell_pipeline | qc_report | comparison_report | batch_pipeline"
    parameters:
      input_files: ["path/to/track.wav"]
      target_platform: "spotify | apple_music | youtube | tidal | amazon | soundcloud | ebu_r128 | atsc_a85 | custom"
      reference_track: "path/to/reference.wav | none"
      measurement_standards: ["BS.1770-4", "EBU R128"]
      network_consent: "allow | ask | deny | n/a"
      lookup_apis: ["acoustid", "musicbrainz", "lastfm", "discogs", "genius"]
      inference_models: ["laion-clap", "yamnet", "ast", "openl3", "demucs"]
      variation_axes: ["genre", "tempo-key", "arrangement", "instrument", "effector"]
    measurements:
      integrated_lufs: -13.2
      true_peak_dbtp: -0.8
      lra: 7.4
      bpm: 128.0
      key: "A minor"
    inferences:
      instruments: [{name: "drums", confidence: 0.94, method: "laion-clap-zero-shot"}]
      effectors: [{family: "reverb", subtype: "plate", rt60_s: 1.4, confidence: 0.71, method: "schroeder-decay"}]
      similar_tracks: [{title: "...", artist: "...", similarity: 0.83, method: "clap-knn"}]
      fingerprint_match: {mbid: "...", title: "...", artist: "...", confidence: 0.99}
  Validations:
    format_inspected: "passed"
    standards_cited: "passed"
    target_declared: "passed | n/a"
    verdict: "PASS | WARN | FAIL"
    inference_confidence_tagged: "passed | failed"
    network_consent_recorded: "passed | n/a"
    source_api_cited: "passed | n/a"
  Next: Tone | Judge | Canvas | Scribe | DONE
  Reason: [Why this next step — e.g., "FAIL on True Peak; route to Tone for re-render with -1.0 dBTP ceiling"]
```

## Nexus `## NEXUS_HANDOFF` Template

```text
## NEXUS_HANDOFF
- Step: [X/Y]
- Agent: Sonar
- Summary: [1-3 lines — file inspected, target platform, verdict]
- Key findings / decisions:
  - Integrated LUFS: [value] (BS.1770-4) vs target [value]
  - True Peak: [value] dBTP vs ceiling [value]
  - LRA: [value] LU
  - Acoustic: BPM [value], Key [value], Time Sig [value]
  - Quality issues: [clipping / phase / masking / none]
- Artifacts: [pipeline script path], [report path]
- Risks: [codec drift, downmix loss, measurement-tool disagreement]
- Open questions (blocking/non-blocking):
  - [blocking: yes/no] [question]
- Pending Confirmations:
  - Trigger: [INTERACTION_TRIGGER name if any]
  - Question: [Question for user]
  - Options: [Available options]
  - Recommended: [Recommended option]
- User Confirmations:
  - Q: [Previous question] → A: [User's answer]
- Suggested next agent: [Tone | Judge | Canvas | Scribe] (reason)
- Next action: CONTINUE | VERIFY | DONE
```

## Supported Formats & Tooling

| Format | Container | Codec | Best Tool | Notes |
|--------|-----------|-------|-----------|-------|
| WAV / BWF | WAV / RF64 | PCM 16/24/32, IEEE float | `librosa`, `soundfile`, `ffmpeg` | Reference format for measurement |
| FLAC | FLAC | FLAC (lossless) | `soundfile`, `librosa` | Lossless; mastering-grade |
| AIFF | AIFF / AIFC | PCM | `soundfile` | Apple lossless container |
| MP3 | MP3 | MPEG-1/2 Layer 3 | `librosa` (via audioread/ffmpeg) | Lossy; flag measurement drift |
| AAC / M4A | MP4 | AAC-LC / HE-AAC | `librosa` (via ffmpeg) | Lossy; Apple/YouTube default |
| OGG | OGG | Vorbis | `librosa` | Lossy |
| Opus | OGG / WebM | Opus | `librosa` (via ffmpeg) | Lossy; streaming-favored |
| DSD | DSF / DFF | DSD | `ffmpeg` decode → PCM | Decode to PCM 24/96 first |
| Multi-channel | WAV / MP4 | PCM / AAC 5.1/7.1 | `soundfile` + manual downmix | Confirm downmix policy first |

## Canonical Loudness Targets (inline summary)

Full table in `loudness-standards.md`. Defaults:

| Platform | Integrated LUFS | True Peak (dBTP) | LRA | Notes |
|----------|----------------|------------------|-----|-------|
| Spotify | -14 | -1.0 | — | Normalize on/off both honored; quiet masters get +gain |
| Apple Music | -16 | -1.0 | — | Sound Check; gain reduction stricter |
| YouTube | -14 | -1.0 | — | Per-track normalize |
| Tidal | -14 | -1.0 | — | Aligns with Spotify |
| Amazon Music | -14 | -2.0 | — | Slightly tighter TP |
| SoundCloud | -14 to -8 | -1.0 | — | Loose; let mastering breathe |
| Broadcast (EBU R128) | -23 ±0.5 | -1.0 | ≤20 | Hard compliance for TV / radio |
| Broadcast (ATSC A/85) | -24 ±2 | -2.0 | — | US broadcast |
| Cinema (Dolby) | Dialnorm -27 | — | — | Theatrical mix |
