# Voiceover Design Reference

Purpose: Design TTS narration for product demo videos. Cover voice selection (ElevenLabs / OpenAI TTS / Azure Neural / Google Cloud TTS), SSML pacing markup, breathing pauses, LUFS normalization for video, Playwright timeline sync via ffmpeg, and accessibility (Audio Description per WCAG 1.2.5).

## Scope Boundary

- **director `voiceover`**: TTS narration for demo videos (this document).
- **director `demo` / `record` / `scenario` / `onboard` (elsewhere)**: Scenario + recording orchestration.
- **director `captions` (elsewhere)**: On-screen captions (complements voiceover).
- **tone `voice` / `lufs` (elsewhere)**: Game / non-video voice generation + loudness normalization.
- **Cue (elsewhere)**: Video script narrative authoring (pre-voiceover).
- **Builder (elsewhere)**: Rendering pipeline code beyond ffmpeg stubs.

## When to Voice Over

- Product feature demos requiring narration
- Onboarding videos (step-by-step guidance)
- Tutorials / how-to content
- Conference talk recordings (pre-recorded variant)
- YouTube / LinkedIn product announcements
- Internal training materials

## Provider Comparison (2025-current)

| Provider | Voices | Latency | Quality | Cost | Best for |
|----------|--------|---------|---------|------|----------|
| **ElevenLabs v3** | 10+ base + clones | 200-800ms | Highest (cloning + multilingual) | $5-$330/mo | Brand voice, multilingual |
| **OpenAI TTS (tts-1-hd)** | 6 voices | 300ms | High | $30/1M chars | Quick iteration |
| **Azure Neural TTS** | 400+ multilingual | 200ms | High (enterprise) | $16/1M chars | Enterprise / accessibility |
| **Google Cloud TTS (Studio)** | 220+ voices | 300ms | High | $16/1M chars | Global locales |
| **Amazon Polly Neural** | 60+ voices | 200ms | High | $16/1M chars | AWS pipelines |
| **Coqui / local XTTS** | Open-source clone | varies | Mid | Free (compute) | Offline / privacy |
| **Descript Overdub** | Clone-based | interactive | High | Subscription | Podcast workflows |

Default: **OpenAI TTS tts-1-hd** for iteration speed, **ElevenLabs** for brand / multilingual / cloning.

## Voice Selection Matrix

| Demo type | Voice character | Pace |
|-----------|-----------------|------|
| Product announcement | Energetic, confident | 160-170 WPM |
| Onboarding | Friendly, measured | 140-150 WPM |
| Technical tutorial | Clear, authoritative | 150-160 WPM |
| Investor demo | Professional, trust | 150-160 WPM |
| Fun / casual | Conversational, warm | 160-180 WPM |
| Accessibility / AD | Neutral, clear | 140-150 WPM |

## SSML Pacing

Speech Synthesis Markup Language is the cross-provider spec for pacing. Core tags:

```xml
<speak>
  <p>
    <s>Welcome to Acme.<break time="400ms"/></s>
    <s>Let me show you how it works.</s>
  </p>
  <p>
    Click <emphasis level="moderate">here</emphasis> to create
    <prosody rate="90%">your first project.</prosody>
    <break time="800ms"/>
    <phoneme alphabet="ipa" ph="əˈkmi">Acme</phoneme>
  </p>
</speak>
```

Key tags:
- `<break time="500ms"/>` — pause
- `<prosody rate="90%" pitch="+2st">` — rate / pitch adjustment
- `<emphasis level="moderate">` — stress
- `<phoneme alphabet="ipa" ph="...">` — custom pronunciation
- `<say-as interpret-as="ordinal">3</say-as>` — "third"
- `<audio src="sfx.wav"/>` — insert audio

Not all providers support all tags. Test per provider.

## Pacing Guidelines

Target WPM = (total words) / (total duration in minutes).

Natural speech: 130-160 WPM.  
Demo narration: 150-160 WPM (brisk, engaging).  
Onboarding: 140-150 WPM (clearer, easier to follow).  
Tutorials: 150-160 WPM.  
Audio Description (AD) per WCAG 1.2.5: 140-170 WPM, gaps between visual events.

### Breathing & Pauses

```
Sentence end:    400-600ms pause
Comma / clause:  200-300ms
Section break:   800-1200ms
Post-CTA:        1000ms (let viewer see result)
Before emphasis: 200ms (anticipation)
```

Real humans breathe every 10-15 seconds. TTS sounds unnatural without these.

## Playwright Timeline Sync

Demo video timeline = Playwright action timestamps. Sync narration to action cues.

```typescript
// Playwright: emit timestamps to a sidecar JSON
await test.step('open settings', async () => {
  timeline.push({ time: performance.now(), event: 'open_settings' });
  await page.click('[data-test=settings]');
});

await test.step('toggle dark mode', async () => {
  timeline.push({ time: performance.now(), event: 'toggle_dark' });
  await page.click('[data-test=dark-toggle]');
});
```

Narration script (annotated with cues):
```yaml
narration:
  - cue: open_settings
    text: "Open settings from the top-right."
    duration_ms: 1500
  - cue: toggle_dark
    text: "Now enable dark mode."
    duration_ms: 1200
```

## FFmpeg Audio Sync

```bash
# Generate TTS audio
curl -X POST https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{"model":"tts-1-hd","voice":"nova","input":"Welcome..."}' \
  --output narration.mp3

# LUFS normalize to -16 LUFS (YouTube target)
ffmpeg -i narration.mp3 -af \
  "loudnorm=I=-16:TP=-1:LRA=7" \
  narration_normalized.wav

# Overlay on video (Playwright .webm)
ffmpeg -i demo.webm -i narration_normalized.wav \
  -c:v copy -c:a aac -b:a 192k \
  -map 0:v -map 1:a \
  demo_with_voiceover.mp4
```

## LUFS for Video

| Platform | Target LUFS | True Peak |
|----------|-------------|-----------|
| YouTube | -14 | -1 dBTP |
| Vimeo | -16 to -23 | -1 dBTP |
| LinkedIn | -16 | -1 dBTP |
| Broadcast TV (EBU R128) | -23 | -1 dBTP |
| Podcast | -16 | -1 dBTP |

Default: -16 LUFS for web demo videos. Hand off to **tone `lufs`** for deeper loudness analysis.

## De-essing

TTS voices often produce harsh sibilance ("s", "sh", "t"). Apply de-esser:

```bash
ffmpeg -i narration.wav -af \
  "deesser=i=0.05:m=0.5:f=0.5:s=o" \
  narration_deessed.wav
```

Or use Fabfilter Pro-DS / iZotope RX for professional output.

## Accessibility (WCAG 1.2.5 Audio Description)

If video has visual content that narration doesn't cover, AD track required.

- Primary track: main narration
- Extended AD: separate audio track describing visuals for sight-impaired users
- Pauses in main narration synced to visual-only moments
- AD voice distinct from narration

Use `<track kind="descriptions">` in HTML5 video or `<audiodescription>` in IMSC/TTML.

## Workflow

```
SCRIPT       →  receive scenario (from director `scenario`)
             →  extract timeline cues

VOICE        →  provider + voice selection per demo type
             →  clone / register if brand voice

SSML         →  insert pacing (sentence / section / CTA)
             →  phoneme for product names
             →  emphasis at key moments

SYNTHESIZE   →  TTS API call
             →  iterate on pronunciation / pace per take

CLEANUP      →  de-esser
             →  breathing pauses if TTS lacks
             →  remove click artifacts

LUFS         →  normalize to platform target (-16 default)
             →  True Peak ≤ -1 dBTP

SYNC         →  align to Playwright timeline cues
             →  adjust silence / trim to match action timing

MIX          →  ffmpeg overlay + encode
             →  BGM mix if applicable (-18 dB vs narration)

ACCESS       →  generate caption track (hand off to director `captions`)
             →  AD track if visual-only content exists
             →  WCAG 1.2.5 compliance

DELIVER      →  MP4 (H.264 + AAC 192kbps) per platform

HANDOFF      →  director `captions`: caption generation
             →  director `thumbnail`: thumbnail design
             →  tone `lufs`: final loudness QC
             →  Builder: build-pipeline integration
```

## Output Template

```markdown
## Voiceover Plan: [Demo]

### Scenario Summary
- Duration: [N seconds]
- Cue count: [N]
- Total words: [N]
- Target WPM: [150-160]

### Voice
- Provider: [ElevenLabs / OpenAI TTS / Azure Neural]
- Voice ID: [nova / Rachel / en-US-JennyNeural]
- Language: [en-US / ja-JP / ...]
- Gender / character: [friendly female / authoritative male]

### Script with SSML
```xml
<speak>
  <p>
    <s>Welcome to Acme.<break time="400ms"/></s>
    ...
  </p>
</speak>
```

### Cue-to-Text Map
| Cue | Playwright action | Text | Duration (ms) |
|-----|-------------------|------|---------------|
| open_settings | click settings | "Open settings from the top-right." | 1500 |
| toggle_dark | click toggle | "Now enable dark mode." | 1200 |

### Audio Pipeline
1. TTS generation: [provider API call]
2. De-esser: [ffmpeg or tool]
3. LUFS: [-16 LUFS, TP -1 dBTP]
4. Overlay: [ffmpeg command]

### Accessibility
- Captions: [auto / manual; hand off to director `captions`]
- Audio Description: [yes / no]
- WCAG 1.2.5 compliance: [pass / needs work]

### Handoffs
- director `captions`: SRT / WebVTT
- director `thumbnail`: thumbnail
- tone `lufs`: loudness QC
- Builder: build-pipeline integration
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Monotonic TTS with no pacing marks | Add SSML breaks, prosody, emphasis |
| Pronunciation of product name wrong | `<phoneme ph="...">` override |
| WPM too fast (180+) | Cap at 160-170 for narration |
| No breathing pauses | 400-600ms at sentence boundaries |
| Peak-normalize instead of LUFS | -16 LUFS with TP limit |
| Harsh sibilance | De-esser pass required |
| Audio out of sync with video action | Align to timeline cues; trim silence |
| Skipping captions | WCAG 1.2.2 requires; cheap insurance |
| Voice change mid-demo | Consistent voice per demo |
| Brand voice cloned without consent | Legal + ethical check; ElevenLabs / Descript have clone consent rules |
| Generating 100 variants; no iteration | 3-5 takes at key cues; refine best |
| No test on target device (mobile / TV) | Test playback on actual devices |
| Ignoring locale (EN only for global product) | Multilingual voices; test each language |
| BGM -6 dB under narration (drowns) | BGM -18 dB; duck further during narration |
| SSML that only one provider understands | Test across OpenAI + ElevenLabs; fallback plain text |
| No source control on script | Commit SSML + cue map alongside Playwright script |

## Deliverable Contract

When `voiceover` completes, emit:

- **Scenario summary** with duration + cues + WPM.
- **Voice choice** (provider / ID / language / character).
- **SSML script** with pacing markup.
- **Cue-to-text map** aligned to Playwright timeline.
- **Audio pipeline** (TTS → de-esser → LUFS → overlay).
- **Accessibility plan** (captions + AD + WCAG).
- **Handoffs**: director captions, director thumbnail, tone lufs, Builder.

## References

- ElevenLabs — elevenlabs.io (v3 models)
- OpenAI TTS — platform.openai.com/docs/guides/text-to-speech
- Azure Neural TTS — learn.microsoft.com/azure/ai-services/speech-service
- Google Cloud TTS — cloud.google.com/text-to-speech
- Amazon Polly — docs.aws.amazon.com/polly
- Descript — descript.com (Overdub)
- Coqui TTS — github.com/coqui-ai/TTS
- SSML 1.1 specification — w3.org/TR/speech-synthesis11/
- WCAG 2.1 Guideline 1.2 Time-based Media — w3.org/TR/WCAG21
- EBU R128 loudness — tech.ebu.ch/docs/r/r128.pdf
- ffmpeg loudnorm — ffmpeg.org/ffmpeg-filters.html#loudnorm
- *Sound for Film and Television* — Tomlinson Holman
- Fabfilter Pro-DS — fabfilter.com (professional de-esser)
- iZotope RX — izotope.com (audio restoration)
- Audio Description style guide — fcc.gov, DCMP Clearinghouse
- IMSC / TTML2 spec — w3.org/TR/ttml2/
- Descript + ElevenLabs voice-clone consent frameworks
- "Narration Pacing for Explainer Videos" — Vidyard / Wistia whitepapers
- "OpenAI TTS vs ElevenLabs benchmark" — community comparisons
