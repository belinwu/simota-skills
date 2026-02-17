# Pipeline Architecture

AITuber リアルタイムパイプラインの全体設計、コンポーネント間通信、レイテンシバジェット、エラーハンドリング。

---

## Pipeline Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                     AITuber Real-time Pipeline                          │
│                                                                         │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐            │
│  │  Chat     │   │ Message  │   │   LLM    │   │   TTS    │            │
│  │ Listener  │──▶│  Queue   │──▶│  Engine  │──▶│  Engine  │──┐        │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘  │        │
│                                                               │        │
│                                     ┌────────────────────────┘        │
│                                     ▼                                  │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐                          │
│  │   OBS    │◀──│  Avatar   │◀──│ Lip Sync │                          │
│  │  Output  │   │ Renderer │   │  Engine  │                          │
│  └──────────┘   └──────────┘   └──────────┘                          │
│                                                                         │
│  ────── Data Flow ──────▶                                              │
│  Total: Chat Message → Audible Speech < 3000ms                         │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Component Communication

| From → To | Protocol | Pattern | Notes |
|-----------|----------|---------|-------|
| Chat Listener → Message Queue | EventEmitter / In-process | Pub/Sub | Single-process: EventEmitter. Multi-process: Redis Pub/Sub |
| Message Queue → LLM Engine | Async function call | Request/Response (streaming) | Pull-based: queue consumer pulls next message |
| LLM Engine → TTS Engine | EventEmitter / Stream pipe | Streaming chunks | Sentence-boundary detection triggers TTS per sentence |
| TTS Engine → Lip Sync | Direct call + data pass | Synchronous | Phoneme timing extracted from TTS query data |
| Lip Sync → Avatar Renderer | WebSocket / IPC | Push | Viseme timeline sent to avatar process |
| Avatar Renderer → OBS | Virtual camera / NDI | Video stream | Browser source or virtual camera capture |
| TTS Engine → OBS | Virtual audio / pipe | Audio stream | Audio routed to OBS audio source |

### Inter-Process Communication Options

| Method | Latency | Complexity | Use When |
|--------|---------|------------|----------|
| In-process EventEmitter | < 1ms | Low | Single Node.js process (recommended for v1) |
| IPC (child_process) | 1-5ms | Medium | Separate processes on same machine |
| Redis Pub/Sub | 1-10ms | Medium | Multi-machine or process isolation needed |
| WebSocket (local) | 5-20ms | Medium | Cross-language components (Python TTS + Node.js) |
| gRPC | 1-5ms | High | High-throughput, type-safe inter-service |
| Message Queue (BullMQ) | 10-50ms | High | Persistence, retry, monitoring needed |

---

## Latency Budget Detail

### Target: Chat → Speech < 3000ms

```
Stage                    Target    Max     Optimization Strategy
─────────────────────────────────────────────────────────────────
Chat Listener            200ms     500ms   WebSocket > Polling
Message Queue            50ms      100ms   In-memory priority queue
LLM (first token)        500ms     800ms   Streaming API, prompt cache
LLM (sentence complete)  1000ms    1500ms  Sentence boundary detection
TTS Synthesis            800ms     1200ms  Chunked synthesis, warm cache
Lip Sync Computation     50ms      100ms   Pre-computed from TTS data
Avatar Frame Update      100ms     200ms   60fps render loop
OBS Encoding + Output    250ms     400ms   Hardware encoding (NVENC/QSV)
─────────────────────────────────────────────────────────────────
Pipeline Total           ~2950ms   ~4800ms
```

### Streaming Optimization (Overlap Strategy)

```
Time ──────────────────────────────────────────────────▶

Chat msg received
 ├─ Queue processing (50ms)
 ├─ LLM streaming starts ─────────────────────┐
 │   ├─ Sentence 1 complete (800ms) ──────┐   │
 │   │   ├─ TTS synthesis S1 (600ms) ─┐   │   │
 │   │   │   ├─ Lip sync compute ─┐   │   │   │
 │   │   │   │   └─ Avatar + Audio play starts (S1)
 │   │   │   │                     ▲
 │   │   │   │              ~1650ms from chat msg
 │   ├─ Sentence 2 complete ───┐   │
 │   │   ├─ TTS synthesis S2 ──┤   │ (parallel with S1 playback)
 │   │   │   └─ Seamless transition to S2 playback
 │   └─ LLM complete ─────────┘
```

**Key insight:** By streaming LLM output and detecting sentence boundaries, TTS can begin synthesizing the first sentence while the LLM is still generating subsequent sentences. This reduces perceived latency to ~1650ms for the first audible word.

---

## Synchronous vs Asynchronous vs Streaming

| Approach | Latency | Complexity | Use Case |
|----------|---------|------------|----------|
| **Synchronous** | High (sequential) | Low | Debug/testing only |
| **Async (full response)** | Medium (parallel stages) | Medium | Short responses only |
| **Streaming (sentence-level)** | **Low (overlapped)** | **High** | **Production (recommended)** |

### Sentence Boundary Detection

```typescript
// Japanese sentence boundary patterns
const SENTENCE_BOUNDARIES = /[。！？\n]/;

// Streaming accumulator
class SentenceAccumulator {
  private buffer = '';

  push(chunk: string): string[] {
    this.buffer += chunk;
    const sentences: string[] = [];

    let match: RegExpExecArray | null;
    while ((match = SENTENCE_BOUNDARIES.exec(this.buffer)) !== null) {
      const sentence = this.buffer.slice(0, match.index + 1).trim();
      if (sentence.length > 0) {
        sentences.push(sentence);
      }
      this.buffer = this.buffer.slice(match.index + 1);
    }
    return sentences;
  }

  flush(): string | null {
    const remaining = this.buffer.trim();
    this.buffer = '';
    return remaining.length > 0 ? remaining : null;
  }
}
```

---

## Pipeline Orchestrator

```typescript
interface PipelineConfig {
  chatListener: ChatListenerAdapter;
  messageQueue: MessageQueue;
  llmEngine: LLMAdapter;
  ttsEngine: TTSAdapter;
  lipSync: LipSyncEngine;
  avatarController: AvatarController;
  obsController: OBSController;
}

interface PipelineMetrics {
  chatToSpeechLatency: number;   // ms
  ttsQueueDepth: number;
  droppedFrames: number;
  messagesProcessed: number;
  messagesSkipped: number;
}
```

### Message Priority

| Priority | Type | Max Queue | Processing |
|----------|------|-----------|------------|
| 1 (highest) | Superchat / Donation | Unlimited | Always process |
| 2 | Command (!command) | 20 | Process in order |
| 3 | Mentioned (@AITuber) | 10 | Process in order |
| 4 | Regular chat | 5 | Newest first, skip old |

---

## Error Handling & Fallback

| Component | Failure Mode | Detection | Fallback | Recovery |
|-----------|-------------|-----------|----------|----------|
| Chat Listener | API rate limit | HTTP 429 | Increase poll interval | Exponential backoff |
| Chat Listener | Auth expired | HTTP 401 | Pause chat | Token refresh |
| Message Queue | Queue full | Depth > max | Drop lowest priority | Auto-drain |
| LLM Engine | Timeout | No response 5s | Canned response | Retry with shorter prompt |
| LLM Engine | API error | HTTP 5xx | Switch to fallback LLM | Retry after 30s |
| TTS Engine | Synthesis failure | Error/timeout | Switch to fallback TTS | Restart TTS process |
| TTS Engine | All engines down | All adapters fail | Text overlay on screen | Alert + manual intervention |
| Lip Sync | Timing mismatch | Audio/visual desync | Reset to neutral mouth | Re-sync on next sentence |
| Avatar | Render crash | Process exit | Static image scene | Restart renderer |
| Avatar | Low FPS | < 20fps sustained | Reduce expression complexity | Scale down model |
| OBS | Connection lost | WebSocket close | Auto-reconnect | Exponential backoff |
| OBS | Encoding overload | Dropped frames > 1% | Reduce bitrate/resolution | Alert |

### Circuit Breaker Pattern

```
For each component:
  CLOSED (normal) → error count > threshold → OPEN (bypass)
  OPEN → after cooldown period → HALF_OPEN (test one request)
  HALF_OPEN → success → CLOSED / failure → OPEN

Thresholds:
  LLM: 3 consecutive failures → 30s cooldown
  TTS: 2 consecutive failures → 15s cooldown
  Avatar: 1 crash → 10s cooldown (restart)
```

---

## Resource Requirements

| Component | CPU | Memory | GPU | Notes |
|-----------|-----|--------|-----|-------|
| Chat Listener | Low | 100MB | - | I/O bound |
| Message Queue | Low | 200MB | - | In-memory queue |
| LLM Engine | Low (API) | 200MB | - | External API call |
| TTS (VOICEVOX) | Medium | 500MB | Optional | CPU inference, GPU accelerates |
| TTS (SBV2) | High | 1GB | Recommended | GPU strongly recommended |
| Lip Sync | Low | 100MB | - | Lightweight computation |
| Avatar (Live2D) | Medium | 500MB | Recommended | WebGL rendering |
| Avatar (VRM) | Medium | 800MB | Recommended | Three.js + WebGL |
| OBS | Medium | 500MB | Recommended | Hardware encoding preferred |
| **Total (v1)** | **Medium** | **~3GB** | **Optional** | Single machine feasible |
