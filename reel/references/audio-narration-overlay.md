# Audio Narration Overlay Reference

Purpose: Add TTS narration to terminal recordings. Cover TTS provider integration, ffmpeg audio overlay, sidechain ducking at keystroke events, LUFS match, subtitle-track sync for WCAG 1.2.2, and output to MP4 (not GIF — GIF can't hold audio).

## Scope Boundary

- **reel `narration`**: Audio narration overlay on terminal video (this document).
- **reel `vhs` / `terminalizer` / `asciinema` (elsewhere)**: Video capture.
- **reel `optimize` / `theme` (elsewhere)**: Size / appearance.
- **director `voiceover` (elsewhere)**: Narration for Playwright demos (UI, not terminal).
- **tone `lufs` / `voice` (elsewhere)**: Audio normalization + voice (referenced here).

## Why Narrate Terminal Demos

- Complex CLI flows: narration bridges "why, not what"
- Accessibility: some users process audio better than scrolling text
- Social feeds (LinkedIn / Twitter): autoplay with sound for higher retention
- Tutorial / course context: audio is table stakes

Note: **GIF format doesn't support audio**. Narrated output must be MP4 / WebM. For README GIF + audio, provide dual deliverable (silent GIF + MP4 below).

## TTS Pipeline

```bash
# OpenAI TTS (tts-1-hd)
curl -X POST https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-1-hd",
    "voice": "nova",
    "input": "First, install the package with npm install."
  }' \
  --output narration.mp3

# ElevenLabs v3 (higher quality, brand voice)
curl -X POST https://api.elevenlabs.io/v1/text-to-speech/VOICE_ID \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "First, install...", "model_id": "eleven_multilingual_v2"}' \
  --output narration.mp3

# Normalize to -16 LUFS (match typical video target)
ffmpeg -i narration.mp3 -af loudnorm=I=-16:TP=-1 narration_norm.wav
```

## Timeline Sync

Terminal recording has discrete events:
- Keystroke (typing)
- Enter (command execute)
- Command output (variable duration)
- Pause / Sleep

Build cue list with timestamps from VHS / terminalizer:

```yaml
# cues.yaml
- time: 0.0s
  text: "Let me show you how to install the package."
  event: intro
- time: 4.5s
  text: "First, run npm install."
  event: keystroke_command
- time: 8.0s
  text: "Wait for dependencies to resolve."
  event: command_output
- time: 15.2s
  text: "Now we can run the demo."
  event: next_command
```

Match narration cue duration to event gap. If narration runs 4s but gap is only 2.5s, either:
1. Add `Sleep 2s` to VHS tape
2. Shorten narration text (fewer words)
3. Speed up speech (SSML `<prosody rate="110%">`)

## FFmpeg Audio Overlay

```bash
# Basic: add narration on top of silent terminal recording
ffmpeg -i terminal.mp4 -i narration_norm.wav \
  -c:v copy \
  -c:a aac -b:a 192k \
  -map 0:v:0 -map 1:a:0 \
  -shortest \
  narrated.mp4
```

## Sidechain Ducking at Keystrokes

Problem: typing sound (mechanical keyboard effect) + narration = muddy audio.  
Solution: duck the typing sound when narration plays.

But terminal recordings typically have no audio track — just video. So there's nothing to duck.

However, if you layer in:
- A keystroke SFX (mechanical keyboard sound) for aesthetic
- Background music (BGM)

…then ducking matters:

```bash
# Mix: narration + BGM ducked + typing SFX ducked
ffmpeg -i terminal.mp4 \
       -i narration_norm.wav \
       -i bgm.mp3 \
       -i typing_sfx.wav \
  -filter_complex "
    [2:a]loudnorm=I=-30[bgm_norm];
    [3:a]loudnorm=I=-24[type_norm];
    [bgm_norm]volume=0.3[bgm_vol];
    [type_norm]volume=0.4[type_vol];
    [bgm_vol][1:a]sidechaincompress=threshold=0.05:ratio=8:attack=20:release=250[bgm_ducked];
    [type_vol][1:a]sidechaincompress=threshold=0.05:ratio=6:attack=10:release=200[type_ducked];
    [bgm_ducked][type_ducked][1:a]amix=inputs=3:duration=first:dropout_transition=0[aout]" \
  -map 0:v:0 -map "[aout]" \
  -c:v copy -c:a aac -b:a 192k \
  narrated_mixed.mp4
```

Sidechain `sidechaincompress`:
- `threshold=0.05`: duck when narration exceeds quiet floor
- `ratio=8`: aggressive ducking for BGM
- `attack=20ms`: quick duck-in (avoid attack artifacts)
- `release=250ms`: smooth return when narration pauses

## LUFS Match per Layer

| Layer | LUFS target |
|-------|-------------|
| Narration (voice) | -16 LUFS |
| BGM (music) | -30 LUFS (below voice) |
| Typing SFX | -24 LUFS |
| Overall master | -16 LUFS (web) / -14 (YouTube) |

Match prevents one layer dominating. Hand off deeper loudness work to **tone `lufs`**.

## WCAG 1.2.2 Caption Sync

Narration audio requires synchronized captions for accessibility.

```bash
# Generate caption track from narration text + timing
# Option 1: Manual .vtt from cues.yaml
cat > captions.vtt <<EOF
WEBVTT

00:00:00.000 --> 00:00:04.500
Let me show you how to install the package.

00:00:04.500 --> 00:00:08.000
First, run npm install.

00:00:08.000 --> 00:00:15.200
Wait for dependencies to resolve.

00:00:15.200 --> 00:00:19.000
Now we can run the demo.
EOF

# Option 2: Auto-transcribe with Whisper
whisper narration_norm.wav --output_format vtt --model base.en

# Option 3: Burn captions in (open)
ffmpeg -i narrated.mp4 -vf "subtitles=captions.vtt:force_style='FontSize=22'" \
  narrated_captioned.mp4

# Option 4: Soft subtitle track (toggleable)
ffmpeg -i narrated.mp4 -i captions.vtt \
  -c:v copy -c:a copy -c:s webvtt \
  narrated_softcap.mp4
```

Hand off captioning deeper work to **director `captions`**.

## Narration Script Guidelines

- **WPM target**: 150-160 for tutorials, 140-150 for onboarding
- **Breathing**: 400-600ms between sentences; 200ms between clauses
- **Brand / product names**: use SSML `<phoneme>` to control pronunciation
- **Commands**: "n-p-m install" (spell out) or "enpeam install" (phonetic)
- **Punctuation**: periods drive pauses; commas short pauses

Example SSML:

```xml
<speak>
  <p>
    <s>Let me show you <break time="200ms"/>
       how to install <phoneme alphabet="ipa" ph="ˈɑːkmi">Acme</phoneme>.</s>
    <break time="400ms"/>
    <s>First, run <prosody rate="90%">n p m install</prosody>.</s>
  </p>
</speak>
```

## Keystroke SFX Layer (optional aesthetic)

```bash
# Extract keystroke events from asciinema .cast or VHS log
# (or use a canned typing SFX loop)
# Apply typing sound on top of terminal video:
ffmpeg -i terminal.mp4 -i typing_sfx.wav -i narration.wav \
  -filter_complex "[1:a]atrim=0:$(ffprobe ...)[type]; [type][2:a]amix[out]" \
  -map 0:v -map "[out]" \
  narrated.mp4
```

Optional and stylistic. Some viewers find it charming (Wes Bos tutorials); others find it distracting. Default off.

## Workflow

```
INPUT        →  terminal recording (MP4 / WebM from VHS / asciinema export)
             →  narration script with timing cues
             →  optional: BGM + typing SFX

TTS          →  provider + voice selection (OpenAI / ElevenLabs)
             →  SSML with timing
             →  generate audio file

LUFS MATCH   →  narration → -16 LUFS
             →  BGM → -30 LUFS (if present)
             →  SFX → -24 LUFS

SYNC         →  align narration to cue timestamps
             →  adjust VHS Sleep or narration duration to match

MIX          →  ffmpeg overlay
             →  sidechain ducking for BGM (if present)
             →  master at -16 LUFS

CAPTIONS     →  generate .vtt from cues
             →  soft subtitle track (toggleable)
             →  or burn-in for autoplay platforms

DELIVER      →  MP4 (universal) + optional WebM
             →  silent GIF variant for README compat
             →  caption .vtt sidecar

VALIDATE     →  audio-video sync spot-check (3-5 cues)
             →  caption accuracy
             →  LUFS final check
             →  mobile + desktop playback

HANDOFF      →  reel `optimize`: file-size reduce
             →  reel `theme`: if theme misalignment
             →  director `captions` / `voiceover`: deeper a/v work
             →  tone `lufs`: final loudness QC
             →  Builder: CI integration
```

## Output Template

```markdown
## Narration Overlay: [Demo]

### Inputs
- Terminal video: [path, duration]
- Script: [path, WPM target]
- BGM: [path / none]
- Typing SFX: [path / none]

### TTS
- Provider: [OpenAI tts-1-hd / ElevenLabs v3]
- Voice: [nova / Rachel / ...]
- Language: [en-US / ja-JP]
- SSML used: [yes / no]

### Timeline Cues
| Time | Event | Narration |
|------|-------|-----------|
| 0.0s | intro | "Let me show you..." |
| 4.5s | keystroke_command | "First, run npm install." |
| 8.0s | command_output | "Wait for dependencies..." |

### Audio Layers (if present)
| Layer | LUFS | Volume adjust | Ducked? |
|-------|------|---------------|---------|
| Narration | -16 | 0 dB | N/A |
| BGM | -30 | -6 dB | sidechain |
| Typing SFX | -24 | -4 dB | sidechain |

### FFmpeg Pipeline
```bash
[ffmpeg command]
```

### Caption Track
- Source: [manual from cues / Whisper auto]
- Format: WebVTT
- Variant: [soft toggle / burned-in open]

### Deliverables
- narrated.mp4 (primary)
- narrated.webm (alt)
- captions.vtt (soft sub)
- silent.gif (README variant via reel `optimize`)

### Validation
- [ ] Audio sync spot-check at 3-5 cues
- [ ] LUFS master: [target hit]
- [ ] Caption reading speed ≤17 CPS
- [ ] Mobile playback OK
- [ ] Desktop playback OK
- [ ] WCAG 1.2.2 caption provided

### Handoffs
- reel `optimize`: file-size reduction
- reel `theme`: theme adjustments
- director `captions` / `voiceover`: deeper a/v work
- tone `lufs`: final loudness
- Builder: CI integration
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Trying to narrate a GIF | GIF has no audio; use MP4 |
| Narration without captions | WCAG 1.2.2 violation; always include .vtt |
| 180 WPM narration | Cap at 160 WPM for tutorials |
| BGM louder than narration | BGM -30 LUFS; narration -16 LUFS |
| No sidechain on BGM | Narration competes with BGM; duck via sidechain |
| Narration ends mid-command | Adjust VHS Sleep or shorten script |
| SFX on every keystroke (noisy) | Use sparse typing SFX or none |
| Narration script too technical for pace | Chunk; use SSML pauses |
| Product name mispronounced | SSML phoneme override |
| No LUFS match across layers | Master sounds unbalanced; match per-layer |
| Commands not spelled out ("npm install" → unclear) | "n-p-m install" or known pronunciation |
| One giant narration file without cues | Cue list in YAML; regenerable |
| Caption generated before final cut | Re-generate after timing locks |
| File too large (80MB with 10s demo) | Compress with H.264 / AAC; bitrate 96-192kbps |
| Stereo voice (sounds wide) | Mono voice + stereo BGM |
| Not committing source script | Commit cues.yaml + .vtt alongside video |

## Deliverable Contract

When `narration` completes, emit:

- **Inputs** (terminal video + script + optional BGM / SFX).
- **TTS choice** (provider + voice + SSML).
- **Timeline cues** YAML.
- **Audio layer LUFS matrix**.
- **FFmpeg pipeline** command.
- **Caption track** (WebVTT sidecar or burned-in).
- **Deliverables** (MP4 + WebM + GIF silent variant + .vtt).
- **Validation** (sync + LUFS + caption + platform).
- **Handoffs**: reel optimize, reel theme, director captions, tone lufs, Builder.

## References

- OpenAI TTS — platform.openai.com/docs/guides/text-to-speech
- ElevenLabs — elevenlabs.io
- Azure Neural TTS — learn.microsoft.com/azure/ai-services/speech-service
- ffmpeg sidechaincompress — ffmpeg.org/ffmpeg-filters.html
- ffmpeg loudnorm — ffmpeg.org/ffmpeg-filters.html#loudnorm
- WebVTT spec — w3.org/TR/webvtt1/
- WCAG 2.1 1.2.2 Captions — w3.org/TR/WCAG21
- OpenAI Whisper — github.com/openai/whisper
- VHS (charmbracelet) — github.com/charmbracelet/vhs
- Asciinema — asciinema.org
- SSML 1.1 — w3.org/TR/speech-synthesis11
- EBU R128 loudness — tech.ebu.ch/docs/r/r128.pdf
- "Mixing Narration + Music for Videos" — Transom.org radio tutorials
- Audacity — audacityteam.org (manual audio editing)
- Reaper DAW — reaper.fm (professional mixing)
- iZotope RX — izotope.com (audio cleanup)
- *Producing Great Sound for Films and Video* — Jay Rose
- pyloudnorm — github.com/csteinmetz1/pyloudnorm (pythonic LUFS)
