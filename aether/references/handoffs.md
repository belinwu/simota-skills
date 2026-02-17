# Handoff Templates

Aether エージェントのコラボレーション用ハンドオフフォーマット。

---

## Inbound Handoffs (→ Aether)

### CAST_TO_AETHER

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Cast → Aether
- **Summary**: Persona data for AITuber pipeline integration

### Persona Specification
- **Name**: [AITuber character name]
- **Registry ID**: [persona registry ID]
- **Version**: [persona version]

### Voice Profile
- **TTS Engine**: [VOICEVOX / SBV2 / COEIROINK / NIJIVOICE]
- **Speaker ID**: [engine-specific speaker ID]
- **Speed**: [0.5-2.0]
- **Pitch**: [-0.15 to 0.15]
- **Intonation**: [0.0-2.0]

### Speaking Style
- **Formality**: [casual / formal / technical]
- **Vocabulary**: [simple / moderate / advanced]
- **Emotional tone**: [default emotion]
- **Linguistic markers**: [catchphrases, speech patterns]
- **Sentence length**: [short / medium / long]

### Emotion Triggers
| Trigger | Emotion | Intensity |
|---------|---------|-----------|
| [positive chat] | joy | 0.7 |
| [superchat] | surprised + joy | 0.9 |
| [question] | thinking | 0.5 |
| [criticism] | [character-appropriate] | [0.3-0.6] |

### Aether Actions Required
- [ ] Map voice_profile to TTS adapter parameters
- [ ] Create expression map from emotion triggers
- [ ] Define interaction rules (superchat reactions, command responses)
- [ ] Configure streaming personality traits (reaction speed, catchphrase frequency)
```

### FORGE_TO_AETHER

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Forge → Aether
- **Summary**: AITuber prototype for production pipeline design

### Prototype Overview
- **Architecture**: [prototype architecture description]
- **Components implemented**: [list of PoC components]
- **Known limitations**: [list of prototype shortcuts]
- **Performance**: [observed latency, resource usage]
- **Prototype files**: [path to prototype code]

### Production Requirements
- [ ] Design fault-tolerant pipeline architecture
- [ ] Implement adapter pattern for swappable components
- [ ] Add latency monitoring and optimization
- [ ] Design error recovery and fallback mechanisms
- [ ] Scale for concurrent viewer chat load
```

### VOICE_TO_AETHER

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Voice → Aether
- **Summary**: Viewer feedback for stream improvement

### Feedback Summary
- **Period**: [date range]
- **Viewer count**: [average/peak]
- **Sentiment**: [overall positive/mixed/negative]

### Key Findings
| Category | Feedback | Frequency | Priority |
|----------|----------|-----------|----------|
| Voice quality | [specific feedback] | [count] | [H/M/L] |
| Response speed | [specific feedback] | [count] | [H/M/L] |
| Character personality | [specific feedback] | [count] | [H/M/L] |
| Avatar expression | [specific feedback] | [count] | [H/M/L] |
| Stream quality | [specific feedback] | [count] | [H/M/L] |

### Aether Actions Required
- [ ] Analyze latency data against feedback
- [ ] Identify TTS parameter adjustments
- [ ] Review expression mapping accuracy
- [ ] Propose pipeline optimizations
- [ ] Feed persona improvements to Cast[EVOLVE]
```

---

## Outbound Handoffs (Aether →)

### AETHER_TO_BUILDER

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Aether → Builder
- **Summary**: AITuber pipeline implementation specification

### Architecture
- **Pipeline diagram**: [reference to pipeline-architecture.md or inline]
- **Runtime**: [Node.js / Python / Hybrid]
- **Key interfaces**: [TTSAdapter, ChatListenerAdapter, AvatarController]

### Implementation Requirements

#### Chat Listener
- **Platform**: [YouTube / Twitch / both]
- **Polling interval**: [ms] (YouTube) or WebSocket (Twitch)
- **Message normalization**: UnifiedChatMessage interface
- **Filtering**: [safety filter, command parser, rate limiter]

#### LLM Integration
- **Provider**: [Claude / GPT / local]
- **Streaming**: Required (sentence-level chunking)
- **System prompt**: [persona-based prompt template]
- **Max tokens**: [token limit for latency budget]

#### TTS Integration
- **Engine**: [VOICEVOX / SBV2 / etc.]
- **Adapter interface**: TTSAdapter (see tts-engines.md)
- **Audio queue**: Priority queue with dedup
- **Fallback chain**: [primary → secondary → text overlay]

#### Avatar Integration
- **Framework**: [Live2D / VRM]
- **Lip sync**: Viseme timeline from TTS phonemes
- **Expression**: Emotion → expression parameter mapping
- **Idle motion**: Auto-blink, breathing, head sway

### Type Definitions
[Include key TypeScript interfaces inline]

### Artifacts
- **Pipeline architecture**: `references/pipeline-architecture.md`
- **TTS adapter spec**: `references/tts-engines.md`
- **Avatar control spec**: `references/avatar-control.md`
- **Lip sync spec**: `references/lip-sync-expression.md`

### Builder Actions Required
- [ ] Implement ChatListenerAdapter for target platform(s)
- [ ] Implement TTSAdapter for selected engine
- [ ] Implement LLM integration with streaming
- [ ] Implement pipeline orchestrator with message queue
- [ ] Implement audio playback with double buffering
- [ ] Add health monitoring and metrics
- [ ] Write integration tests for end-to-end pipeline
```

### AETHER_TO_ARTISAN

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Aether → Artisan
- **Summary**: Avatar frontend implementation specification

### Avatar Specification
- **Framework**: [Live2D Cubism SDK for Web / VRM three-vrm]
- **Model**: [model file path or source]
- **Rendering target**: Browser (OBS Browser Source)

### Control Interface
- **Lip sync input**: WebSocket receiving VisemeKeyframe[] timeline
- **Expression input**: WebSocket receiving emotion state updates
- **Idle animation**: Built-in (auto-blink, breathing, head sway)

### Requirements
- [ ] Load and render avatar model in browser
- [ ] Implement lip sync playback from viseme timeline
- [ ] Implement emotion expression transitions
- [ ] Implement idle animation system
- [ ] Transparent background (CSS: `background: transparent`)
- [ ] WebSocket client for receiving control data
- [ ] 30fps minimum render performance
- [ ] Graceful error handling (model load failure → fallback image)

### Artifacts
- **Avatar control spec**: `references/avatar-control.md`
- **Lip sync spec**: `references/lip-sync-expression.md`
- **Expression mapping**: [emotion → parameter table]
```

### AETHER_TO_SCAFFOLD

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Aether → Scaffold
- **Summary**: Streaming infrastructure requirements

### Infrastructure Requirements
- **OBS**: OBS Studio with WebSocket plugin (v5)
- **TTS Engine**: [VOICEVOX server / SBV2 server / NIJIVOICE API]
- **Streaming**: [RTMP / SRT to YouTube / Twitch]
- **Process management**: PM2 or systemd for pipeline process

### Environment Variables
```env
# LLM
LLM_API_KEY=
LLM_MODEL=

# TTS
VOICEVOX_URL=http://localhost:50021
# or: NIJIVOICE_API_KEY=

# Streaming Platform
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=
YOUTUBE_REFRESH_TOKEN=
# or: TWITCH_CLIENT_ID= / TWITCH_CLIENT_SECRET= / TWITCH_BOT_TOKEN=

# OBS
OBS_WS_URL=ws://localhost:4455
OBS_WS_PASSWORD=

# Monitoring (optional)
METRICS_PORT=9090
```

### Resource Requirements
- **CPU**: 4+ cores recommended
- **Memory**: 4GB+ (pipeline + TTS + avatar rendering)
- **GPU**: Optional but recommended (TTS acceleration, avatar rendering)
- **Network**: Stable upload 10Mbps+ for streaming
- **Storage**: 50GB+ (TTS models, avatar models, recording archive)

### Scaffold Actions Required
- [ ] Configure TTS engine server (startup, health check)
- [ ] Configure OBS with scene definitions
- [ ] Set up process manager for pipeline
- [ ] Configure streaming output (RTMP/SRT)
- [ ] Set up monitoring endpoint
- [ ] Create deployment scripts
```

### AETHER_TO_RADAR

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Aether → Radar
- **Summary**: Test specifications for AITuber pipeline

### Test Requirements

#### Pipeline Integration Tests
- [ ] End-to-end: chat message → TTS audio output (< 3000ms)
- [ ] Message priority: superchat processed before regular messages
- [ ] Queue management: queue full → lowest priority dropped
- [ ] Deduplication: identical messages within 5s window filtered

#### TTS Adapter Tests
- [ ] VOICEVOX adapter: synthesize returns valid WAV
- [ ] Phoneme timing extraction matches audio duration
- [ ] Fallback: primary engine fail → secondary engine used
- [ ] Parameter application: speed/pitch/intonation affect output

#### Chat Listener Tests
- [ ] YouTube: polling retrieves messages correctly
- [ ] Twitch: IRC connection and message parsing
- [ ] Message normalization: platform → UnifiedChatMessage
- [ ] Command recognition: !command parsing
- [ ] Safety filter: toxic content blocked

#### Avatar Control Tests
- [ ] Lip sync: viseme timeline aligned with audio
- [ ] Expression transition: smooth blend between emotions
- [ ] Idle animation: continuous when not speaking

### Test Data
- **Sample chat messages**: [path or inline]
- **Sample VOICEVOX responses**: [path or inline]
```

### AETHER_TO_BEACON

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Aether → Beacon
- **Summary**: Stream monitoring and metrics specification

### Metrics to Track
| Metric | Type | Source | Alert Threshold |
|--------|------|--------|-----------------|
| chat_to_speech_latency_ms | Histogram | Pipeline | p95 > 4000ms |
| tts_queue_depth | Gauge | Audio queue | > 10 |
| tts_synthesis_time_ms | Histogram | TTS adapter | p95 > 1200ms |
| obs_dropped_frames | Counter | OBS WebSocket | > 1% in 5min |
| avatar_fps | Gauge | Avatar renderer | < 20 |
| memory_usage_mb | Gauge | Process | > 3072 |
| chat_messages_per_minute | Gauge | Chat listener | > 200 (flood) |
| active_viewers | Gauge | Platform API | — (info only) |

### Dashboard Requirements
- [ ] Real-time latency graph (per pipeline stage)
- [ ] TTS queue depth visualization
- [ ] OBS stream health indicators
- [ ] Chat activity timeline
- [ ] Alert history
```

### AETHER_TO_CAST_EVOLVE

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Aether → Cast[EVOLVE]
- **Summary**: Streaming behavior data for persona evolution

### Stream Session Data
- **Stream date**: [YYYY-MM-DD]
- **Duration**: [hours]
- **Peak viewers**: [count]
- **Chat messages**: [total count]

### Behavioral Observations
| Observation | Data | Suggested Change |
|-------------|------|-----------------|
| [Viewer engagement pattern] | [metric] | [persona adjustment] |
| [Popular topic/reaction] | [metric] | [knowledge expansion] |
| [Latency feedback] | [metric] | [TTS parameter tweak] |

### Cast Actions Required
- [ ] Review persona attributes against streaming data
- [ ] Evaluate voice_profile parameter effectiveness
- [ ] Update emotion triggers based on viewer reactions
- [ ] Version bump persona with evolution log entry
```
