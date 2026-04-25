# AITuber Latency Budget

## Purpose

An AITuber pipeline (chat ingest → LLM → TTS → avatar → OBS → RTMP) feels alive only when end-to-end response latency is below conversational threshold. Beyond ~2 seconds, viewers perceive the AITuber as broken. This reference defines the latency model, per-stage budgets, measurement methodology, and bottleneck-fix patterns.

## Scope Boundary

- IN scope: end-to-end latency targets, per-stage budgets, measurement instrumentation, bottleneck diagnosis, streaming-LLM and parallel-TTS strategies, network jitter handling.
- OUT of scope: avatar quality (delegate to `avatar`), TTS engine selection (`tts`), OBS scene wiring (`obs`), chat platform integration (`chat`), persona / prompt design (`stream` default), live-ops streaming infra (`scaffold` / `gear`).

## Core Concepts

### Total Budget Targets

| Tier | End-to-end latency | Viewer perception |
|------|-------------------|-------------------|
| World-class | ≤ 1.0 s | Indistinguishable from human reaction |
| Production | ≤ 2.0 s | Feels responsive |
| Acceptable | ≤ 3.5 s | Noticeable lag; viewers tolerant |
| Failing | > 3.5 s | Viewers leave; comments stack up unanswered |

End-to-end = from chat-message-arrival to first-audio-frame-emitted from RTMP. This is the **felt** latency, not server-internal latency.

### Stage-by-Stage Budget

A 2,000 ms total budget allocates roughly:

| Stage | Budget (ms) | Notes |
|-------|-------------|-------|
| Chat ingest + queue | 50–100 | YouTube/Twitch poll vs WS push |
| Pre-filter (NG, dedup) | 5–20 | Regex + bloom filter |
| LLM first token | 300–800 | Streaming-first matters |
| LLM full reply (until TTS-ready chunk) | 200–600 | Parallel TTS chunking helps |
| TTS first audio frame | 200–500 | Engine + model choice matters |
| Avatar lip-sync prep | 50–150 | Phoneme alignment |
| OBS audio routing | 30–80 | Hardware vs virtual cable |
| RTMP encoder | 50–200 | x264 ultrafast vs NVENC |
| Network last-mile | 200–500 | YouTube ingest 0.7-1.5s typically |

Total measured (server side, before RTMP): 1.0–1.5 s. With RTMP/network: 1.5–2.0 s.

### LLM Streaming-First

Naive: wait for full LLM reply, then send to TTS. Adds 800–1500 ms latency.

Streaming-first: stream LLM tokens, segment into TTS-ready chunks (sentence boundaries), send each chunk to TTS while LLM continues.

| Pattern | First-audio latency |
|---------|---------------------|
| Wait-full + serial TTS | 1.2–2.5 s |
| Stream + sentence chunk | 0.4–0.8 s |
| Stream + clause chunk | 0.3–0.6 s |
| Stream + adaptive chunk (filler-first) | 0.2–0.5 s |

Sentence-chunk strategy:

1. Buffer LLM tokens until punctuation (。 . ! ? ：).
2. Send chunk to TTS.
3. Continue buffering next chunk.
4. Concatenate audio frames in order.

Risks: TTS prosody breaks on chunk boundaries. Mitigation: keep chunks ≥ 1 sentence; inject a 100 ms silence between chunks; use TTS engines that support streaming input.

### Parallel TTS

When multiple TTS chunks arrive close together:

| Strategy | Throughput |
|----------|------------|
| Serial | 1 chunk at a time; total = sum |
| Parallel-bounded (2–3 workers) | up to 2–3× speedup; engine cost increases |
| Parallel + ordered emit | Workers in parallel; emit queue maintains order |

ElevenLabs and OpenAI TTS support concurrent requests; VOICEVOX local engine is GPU-bound; Style-Bert-VITS2 is CPU/GPU dependent.

### Network Last-Mile

| Path | Typical RTT |
|------|-------------|
| Streamer → YouTube ingest | 200–500 ms |
| Streamer → Twitch ingest | 100–300 ms |
| RTMP encoder buffer | 200–500 ms (default low-latency) |
| YouTube viewer-side lag | 2–5 s (HLS) |
| Twitch viewer-side lag | 3–10 s (low-latency mode 1–2 s) |

End-to-end **from-chat-to-viewer-hearing** includes viewer-side lag. The AITuber-side budget targets the **before-RTMP** latency only — viewer-side lag is platform-controlled.

### Measurement Instrumentation

Mandatory traces per request:

| Span | Start event | End event |
|------|-------------|-----------|
| chat_ingest | message API webhook | message in queue |
| pre_filter | dequeue | filter pass/fail |
| llm_first_token | LLM request sent | first token returned |
| llm_full | LLM request sent | last token returned |
| tts_first_audio | first chunk submitted | first audio frame returned |
| tts_full | last chunk submitted | last audio frame returned |
| avatar_prep | first audio frame received | first phoneme aligned |
| obs_route | audio frame to OBS | OBS confirms received |
| rtmp_encode | OBS encode start | encoder output frame |

Use OpenTelemetry traces; log per-span p50 / p95 / p99 over rolling 5-min windows. Without instrumentation, you cannot diagnose bottlenecks — guessing wastes streams.

### Bottleneck Diagnosis Flow

1. Pull p95 trace breakdown for last 1 hour.
2. Identify the stage with highest p95.
3. Apply the stage-specific fix table below.
4. Re-measure 24 hours later.

| Stage with high p95 | Fix |
|---------------------|-----|
| chat_ingest | Switch from poll to WebSocket; reduce poll interval; check API rate limit |
| llm_first_token | Switch to faster model (Haiku, gpt-4o-mini); reduce system prompt; KV cache; co-locate region |
| llm_full | Cap max_tokens; aggressive streaming; pre-emptive chunk dispatch |
| tts_first_audio | Faster TTS engine; smaller model; warm pool; co-locate region; streaming input |
| tts_full | Parallel chunk workers; ordered emit queue |
| avatar_prep | Faster phoneme aligner; cache phoneme dictionary; reduce expression complexity |
| obs_route | Hardware audio interface > virtual cable; check sample rate alignment |
| rtmp_encode | NVENC over x264; reduce keyframe interval; ABR off; lower b-frames |

### Filler-First Pattern

For high-latency stages (LLM thinking long), emit a **filler utterance** to keep the AITuber visibly engaged:

- "うん、" / "ええと…" / "let me think…" / "そうですね、"
- Filler is pre-recorded TTS, ≤200 ms.
- Trigger: LLM first-token > 600 ms.
- Effect: viewer perceives engagement; actual latency unchanged but felt as 0.

Risk: overuse becomes noticeable. Cap filler frequency at < 30% of replies.

### Persistent Connections

Cold-start penalty per stage:

| Stage | Cold start |
|-------|-----------|
| HTTPS handshake | 100–300 ms |
| TLS resume (session ID) | 30–80 ms |
| HTTP/2 multiplexing | shared connection; ~0 ms per request |
| WebSocket | persistent; ~0 ms per message after open |

Use HTTP/2 connection pools with keep-alive, or WebSocket where supported (OpenAI realtime API, ElevenLabs streaming, YouTube/Twitch chat).

### Region Co-Location

| Pair | Latency |
|------|---------|
| Tokyo streamer + Tokyo LLM | 30–80 ms RTT |
| Tokyo streamer + US-East LLM | 130–180 ms RTT |
| Tokyo streamer + US-West LLM | 100–130 ms RTT |
| EU streamer + US LLM | 80–120 ms RTT |

Co-locate streamer + LLM + TTS in same region. Cross-region adds ~100 ms per hop.

### Adaptive Latency

When system is overloaded:

| Pressure | Adaptive response |
|----------|-------------------|
| LLM queue depth > N | Drop to faster model (Haiku); reduce reply length |
| TTS queue depth > N | Use faster TTS engine; skip emotion/style flags |
| Chat queue depth > N | Skip low-priority messages; batch acknowledge |
| All overloaded | Emit emergency filler; resume normal when clear |

Document the policy in advance so the AITuber's "tired" mode is graceful, not broken.

### Anti-Patterns

| Anti-pattern | Impact |
|--------------|--------|
| Wait-full LLM before TTS | +800-1500 ms |
| Synchronous chat poll every 10 s | Misses fast turns; up to 10 s of dead air |
| Large system prompt > 2,000 tokens | LLM first token +200-400 ms |
| Cold connections per request | +100-300 ms × stage count |
| Cross-region LLM | +100 ms per hop |
| Generating long replies (>200 words) | Pipeline pressure; long tail |
| No tracing | Cannot diagnose; guesses cost streams |
| OBS browser source for audio routing | Adds 200-500 ms vs hardware |

## Workflow

1. **Set total budget** — pick tier (1.0 / 2.0 / 3.5 s).
2. **Allocate per-stage** — use the budget table.
3. **Instrument** — OpenTelemetry spans on every stage.
4. **Run baseline 30-min stream** — collect p50/p95/p99.
5. **Diagnose** — identify highest-p95 stage.
6. **Apply fix pattern** — from the bottleneck table.
7. **Re-measure 24h later** — confirm improvement.
8. **Iterate** until total p95 ≤ target tier.
9. **Document policy** — adaptive degradation, filler triggers, queue thresholds.
10. **Set monitoring alerts** — p95 > target × 1.5 for 5 min triggers PagerDuty / Discord.

## Output Template

```yaml
latency_budget:
  total_target_ms: 2000
  tier: production
  per_stage_ms:
    chat_ingest: 80
    pre_filter: 15
    llm_first_token: 600
    llm_full_to_tts_ready: 400
    tts_first_audio: 350
    avatar_prep: 100
    obs_route: 60
    rtmp_encode: 150
    network_last_mile: 245
  llm_streaming:
    enabled: yes
    chunk_strategy: sentence
    parallel_tts_workers: 3
  filler_first:
    enabled: yes
    threshold_first_token_ms: 600
    cap_pct: 30
  region:
    streamer: tokyo
    llm: tokyo
    tts: tokyo
  instrumentation: opentelemetry
  baseline:
    p50_ms: 1620
    p95_ms: 2380
    p99_ms: 3450
  bottleneck: tts_first_audio_p95_780ms
  fix_plan:
    - "Switch TTS engine to ElevenLabs streaming endpoint"
    - "Pre-warm 2-worker pool"
    - "Co-locate to ap-northeast-1"
  adaptive:
    pressure_high:
      llm_model: haiku
      tts_engine: voicevox_local
      reply_max_tokens: 60
  alerts:
    p95_above_3000_ms_for_5_min: true
```

## Anti-Patterns

- Setting a budget but never measuring — guesses are wrong.
- Optimizing the LLM stage when TTS is the bottleneck.
- Cross-region by default — adds 100 ms unnecessarily.
- Wait-full LLM before TTS — kills perceived latency.
- Chat poll every 10s — dead-air windows.
- No filler-first pattern — long thinks feel broken.
- Cold connections — re-handshake on every turn.
- OBS browser-source for audio routing — multi-hundred-ms penalty.
- Big system prompts — LLM first-token tax.
- No graceful degradation — overload becomes failure.
- No alerts — outages noticed by viewers, not ops.
- Counting only server-side latency, ignoring RTMP / viewer-side.
- Optimizing p50 only — p95 is the felt experience for engaged chatters.
- Generating > 200-word replies — pipeline pressure compounds.
- Letting filler exceed 30% — visible pattern, viewers notice.

## Deliverable Contract

A latency-budget design is complete when:

- Tier chosen (1.0 / 2.0 / 3.5 s).
- Per-stage budget allocated and sums to total.
- Instrumentation deployed (OpenTelemetry).
- Baseline measured at p50/p95/p99.
- Bottleneck identified and fix plan written.
- Streaming-first LLM enabled (or rationale documented).
- Filler-first policy specified.
- Region co-location planned.
- Adaptive degradation policy documented.
- Alert thresholds set.

## References

- OpenAI Realtime API documentation — streaming TTS / LLM patterns.
- ElevenLabs API documentation — streaming TTS chunking.
- VOICEVOX engine source — local TTS latency tuning.
- Style-Bert-VITS2 — open-source Japanese TTS reference.
- OBS Studio Plugin Reference — audio routing latency.
- YouTube Live encoding guide — RTMP recommended settings.
- Twitch Inspector — RTMP latency diagnostics.
- AWS / GCP / Azure region maps — co-location latency tables.
- OpenTelemetry — distributed-tracing spec.
- Robert Sapolsky, *Behave* — conversational reaction-time research (300-800 ms baseline).
- Designing Data-Intensive Applications (Kleppmann) — latency-budget framing.
