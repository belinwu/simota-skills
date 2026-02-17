# TTS Engines

AITuber 向けリアルタイム TTS エンジン比較、TTSAdapter パターン、音声キュー管理。

---

## Engine Comparison

| Engine | Type | Latency | Quality | Japanese | GPU Required | Cost | API |
|--------|------|---------|---------|----------|-------------|------|-----|
| **VOICEVOX** | Local | 200-800ms | High | ✅ Native | Optional | Free (OSS) | REST (localhost:50021) |
| **Style-Bert-VITS2** | Local | 500-1500ms | Very High | ✅ Native | Recommended | Free (OSS) | REST |
| **COEIROINK** | Local | 200-600ms | High | ✅ Native | Optional | Free | REST (localhost:50032) |
| **NIJIVOICE** | Cloud | 300-1000ms | Very High | ✅ Native | No | Pay-per-use | REST (API key) |
| **VOICEVOX Nemo** | Local | 200-800ms | High | ✅ Native | Optional | Free (OSS) | REST (localhost:50021) |

### Detailed Comparison

| Feature | VOICEVOX | SBV2 | COEIROINK | NIJIVOICE | VOICEVOX Nemo |
|---------|----------|------|-----------|-----------|---------------|
| **Speaker count** | 60+ | Custom trained | 80+ | 100+ | 20+ |
| **Voice cloning** | ❌ | ✅ (fine-tune) | ❌ | ❌ | ❌ |
| **Emotion control** | Speed/Pitch/Intonation | Style mixing | Speed/Pitch | Limited | Speed/Pitch/Intonation |
| **Streaming output** | ❌ (full synthesis) | ❌ (full synthesis) | ❌ (full synthesis) | ✅ (chunked) | ❌ (full synthesis) |
| **Phoneme timing** | ✅ (query API) | Partial | ❌ | ❌ | ✅ (query API) |
| **Lip sync support** | ✅ Excellent | ⚠️ Manual | ❌ | ❌ | ✅ Excellent |
| **Setup complexity** | Low (binary) | High (Python env) | Low (binary) | Low (API key) | Low (binary) |
| **Offline** | ✅ | ✅ | ✅ | ❌ | ✅ |
| **Commercial use** | Per-character license | Model-dependent | Per-character license | License required | Per-character license |

### Recommendation by Use Case

| Use Case | Recommended | Reason |
|----------|-------------|--------|
| **v1 / Quick start** | VOICEVOX | Low setup, good quality, phoneme data for lip sync |
| **Highest quality** | Style-Bert-VITS2 | Best naturalness, custom voice training |
| **Low resource** | COEIROINK | Lightweight, fast synthesis |
| **No GPU available** | NIJIVOICE (cloud) | Offload computation, consistent latency |
| **Custom voice** | Style-Bert-VITS2 | Fine-tuning with custom dataset |

---

## TTSAdapter Pattern

共通インターフェースで TTS エンジンを抽象化し、パイプライン変更なしでエンジン切り替えを実現。

```typescript
interface TTSAdapter {
  /** エンジン名 */
  readonly name: string;

  /** 利用可能か確認 */
  isAvailable(): Promise<boolean>;

  /** 音声合成 */
  synthesize(params: TTSSynthesizeParams): Promise<TTSResult>;

  /** 音素タイミング取得（リップシンク用、対応エンジンのみ） */
  getPhonemeTimings?(text: string, speakerId: number): Promise<PhonemeTiming[]>;

  /** 話者一覧取得 */
  getSpeakers(): Promise<TTSSpeaker[]>;

  /** エンジン停止 */
  dispose(): Promise<void>;
}

interface TTSSynthesizeParams {
  text: string;
  speakerId: number;
  speed?: number;       // 0.5 - 2.0 (default: 1.0)
  pitch?: number;       // -0.15 - 0.15 (default: 0.0)
  intonation?: number;  // 0.0 - 2.0 (default: 1.0)
  volume?: number;      // 0.0 - 2.0 (default: 1.0)
}

interface TTSResult {
  audio: Buffer;           // WAV audio data
  format: 'wav' | 'mp3';
  duration: number;        // ms
  phonemes?: PhonemeTiming[];
  synthesisTime: number;   // ms (for latency tracking)
}

interface PhonemeTiming {
  phoneme: string;    // 'a', 'i', 'u', 'e', 'o', 'N', 'cl', 'pau'
  startTime: number;  // ms
  endTime: number;    // ms
}

interface TTSSpeaker {
  id: number;
  name: string;
  styles: { id: number; name: string }[];
}
```

### VOICEVOX Adapter Example

```typescript
class VOICEVOXAdapter implements TTSAdapter {
  readonly name = 'voicevox';
  private baseUrl: string;

  constructor(baseUrl = 'http://localhost:50021') {
    this.baseUrl = baseUrl;
  }

  async isAvailable(): Promise<boolean> {
    try {
      const res = await fetch(`${this.baseUrl}/version`);
      return res.ok;
    } catch {
      return false;
    }
  }

  async synthesize(params: TTSSynthesizeParams): Promise<TTSResult> {
    const start = Date.now();

    // Step 1: Generate audio query (includes phoneme timing)
    const query = await fetch(
      `${this.baseUrl}/audio_query?text=${encodeURIComponent(params.text)}&speaker=${params.speakerId}`,
      { method: 'POST' }
    ).then(r => r.json());

    // Apply parameters
    if (params.speed) query.speedScale = params.speed;
    if (params.pitch) query.pitchScale = params.pitch;
    if (params.intonation) query.intonationScale = params.intonation;
    if (params.volume) query.volumeScale = params.volume;

    // Step 2: Synthesize audio
    const audioRes = await fetch(
      `${this.baseUrl}/synthesis?speaker=${params.speakerId}`,
      { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(query) }
    );
    const audio = Buffer.from(await audioRes.arrayBuffer());

    // Step 3: Extract phoneme timings from query
    const phonemes = this.extractPhonemes(query);

    return {
      audio,
      format: 'wav',
      duration: this.calculateDuration(query),
      phonemes,
      synthesisTime: Date.now() - start,
    };
  }

  async getPhonemeTimings(text: string, speakerId: number): Promise<PhonemeTiming[]> {
    const query = await fetch(
      `${this.baseUrl}/audio_query?text=${encodeURIComponent(text)}&speaker=${speakerId}`,
      { method: 'POST' }
    ).then(r => r.json());
    return this.extractPhonemes(query);
  }

  private extractPhonemes(query: any): PhonemeTiming[] {
    // VOICEVOX audio_query returns accent_phrases with moras
    // Each mora has: text, consonant, consonant_length, vowel, vowel_length, pitch
    const phonemes: PhonemeTiming[] = [];
    let currentTime = 0;

    for (const phrase of query.accent_phrases) {
      for (const mora of phrase.moras) {
        if (mora.consonant) {
          const duration = mora.consonant_length * 1000;
          phonemes.push({ phoneme: mora.consonant, startTime: currentTime, endTime: currentTime + duration });
          currentTime += duration;
        }
        if (mora.vowel) {
          const duration = mora.vowel_length * 1000;
          phonemes.push({ phoneme: mora.vowel, startTime: currentTime, endTime: currentTime + duration });
          currentTime += duration;
        }
      }
      if (phrase.pause_mora) {
        const duration = phrase.pause_mora.vowel_length * 1000;
        phonemes.push({ phoneme: 'pau', startTime: currentTime, endTime: currentTime + duration });
        currentTime += duration;
      }
    }
    return phonemes;
  }

  private calculateDuration(query: any): number {
    let total = 0;
    for (const phrase of query.accent_phrases) {
      for (const mora of phrase.moras) {
        total += (mora.consonant_length ?? 0) + mora.vowel_length;
      }
      if (phrase.pause_mora) total += phrase.pause_mora.vowel_length;
    }
    return total * 1000;
  }

  async getSpeakers(): Promise<TTSSpeaker[]> {
    return fetch(`${this.baseUrl}/speakers`).then(r => r.json());
  }

  async dispose(): Promise<void> {
    // VOICEVOX runs as separate process — no cleanup needed
  }
}
```

---

## Audio Queue Management

リアルタイム配信では複数のチャットメッセージが連続して到着するため、音声合成・再生の管理が重要。

### Priority Queue

```typescript
interface AudioQueueItem {
  id: string;
  text: string;
  priority: number;     // 1=highest (superchat), 4=lowest (regular)
  timestamp: number;
  speakerId: number;
  emotion?: string;
}

class AudioQueue {
  private queue: AudioQueueItem[] = [];
  private maxSize = 10;
  private processing = false;

  enqueue(item: AudioQueueItem): boolean {
    // Dedup: skip if same text within 5s
    if (this.queue.some(q => q.text === item.text && Date.now() - q.timestamp < 5000)) {
      return false;
    }

    // Queue full: drop lowest priority
    if (this.queue.length >= this.maxSize) {
      const lowestPriority = Math.max(...this.queue.map(q => q.priority));
      if (item.priority >= lowestPriority) return false; // New item is also low priority
      const dropIndex = this.queue.findLastIndex(q => q.priority === lowestPriority);
      this.queue.splice(dropIndex, 1);
    }

    // Insert by priority (stable sort)
    const insertIndex = this.queue.findIndex(q => q.priority > item.priority);
    if (insertIndex === -1) {
      this.queue.push(item);
    } else {
      this.queue.splice(insertIndex, 0, item);
    }
    return true;
  }

  dequeue(): AudioQueueItem | null {
    return this.queue.shift() ?? null;
  }

  get depth(): number {
    return this.queue.length;
  }

  clear(): void {
    this.queue = [];
  }
}
```

### Double-Buffered Audio Playback

```
Buffer A: [Playing current sentence audio]
Buffer B: [Synthesizing next sentence] ← ready before A finishes

Timeline:
  A plays ──────────────┐
  B synthesizing ────┐  │
                     ▼  ▼
  B plays ──────────────┐  (seamless transition)
  C synthesizing ────┐  │
                     ▼  ▼
  C plays ──────────────┐
  ...
```

---

## TTS Parameter Tuning

### Voice Character Profiles

| Character Type | Speed | Pitch | Intonation | Volume |
|---------------|-------|-------|------------|--------|
| 元気系 (Energetic) | 1.1-1.2 | +0.05 | 1.3-1.5 | 1.1 |
| おっとり系 (Gentle) | 0.85-0.95 | -0.03 | 0.8-1.0 | 0.9 |
| クール系 (Cool) | 0.95-1.0 | -0.05 | 0.7-0.9 | 1.0 |
| ツンデレ系 (Tsundere) | 1.0-1.1 | +0.03 | 1.2-1.5 | 1.0-1.2 |
| 落ち着き系 (Calm) | 0.9-1.0 | -0.02 | 0.9-1.1 | 0.95 |

### Emotion-Based Parameter Adjustment

| Emotion | Speed Δ | Pitch Δ | Intonation Δ | Volume Δ |
|---------|---------|---------|-------------|----------|
| Joy / Excited | +0.1 | +0.05 | +0.3 | +0.1 |
| Sad | -0.15 | -0.05 | -0.2 | -0.1 |
| Angry | +0.05 | +0.03 | +0.4 | +0.2 |
| Surprised | +0.15 | +0.08 | +0.5 | +0.15 |
| Thinking | -0.1 | 0 | -0.1 | -0.05 |
| Neutral | 0 | 0 | 0 | 0 |
