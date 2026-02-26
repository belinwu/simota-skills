# Cast SPEAK Engine

TTS エンジン仕様、ボイスマッピング、Auto-Derivation ルール、セリフ生成プロンプト設計。

---

## Overview

SPEAK モードは、Cast が管理するペルソナに「声」を与える。ペルソナの属性と speaking_style からセリフを AI 生成し、TTS エンジンで音声合成する。

```
┌─────────────────────────────────────────────────────────────┐
│                    SPEAK Pipeline                            │
│                                                              │
│  RESOLVE → GENERATE → VOICE → RENDER → OUTPUT               │
│  (ペルソナ)  (セリフ)   (エンジン)  (音声)    (再生/保存)         │
│                                                              │
│  voice_profile あり → 直接使用                                │
│  voice_profile なし → Auto-Derive → 動的生成                  │
└─────────────────────────────────────────────────────────────┘
```

**Canonical source for `voice_profile` schema:** `persona-model.md` (SPEAK Extension Fields section)

---

## TTS Engine Architecture

### Supported Engines

| Engine | Platform | Quality | Offline | Cost | Install |
|--------|----------|---------|---------|------|---------|
| **VOICEVOX** | Cross-platform | High (Deep Learning) | Yes | Free (OSS) | Binary download → localhost:50021 |
| **macOS `say`** | macOS only | Standard (concatenative) | Yes | Free | Pre-installed |
| **edge-tts** | Cross-platform | High (Neural TTS) | No (requires network) | Free | `npx --yes edge-tts` |
| **google_tts** | Cross-platform | Very High (Neural2/WaveNet) | No (requires network) | $16/1M chars (Neural2) | `pip3 install google-cloud-texttospeech` |

### Engine Selection Logic

```
engine_preference が明示指定されている場合:
  → そのエンジンを使用
  → unavailable なら ON_ENGINE_UNAVAILABLE トリガー発火
  → フォールバック順: voicevox → edge-tts → say

engine_preference: auto の場合:
  ※ google_tts は auto に含まない（課金保護 — 明示指定時のみ使用）
  1. VOICEVOX が利用可能か確認 (localhost:50021 接続確認)
     → 利用可能: VOICEVOX を使用（Deep Learning TTS で高品質日本語音声）
  2. edge-tts が利用可能か確認 (`which edge-tts` or npx availability)
     → 利用可能: edge-tts をフォールバックとして使用
  3. macOS say が利用可能か確認 (`which say`)
     → 利用可能: say をフォールバックとして使用
  4. すべて unavailable:
     → テキストのみ出力（警告メッセージ付き）
     → ON_ENGINE_UNAVAILABLE トリガー（AUTORUN: テキストのみ続行）

...
```

### Engine Availability Check

```bash
# VOICEVOX (localhost REST API)
curl -s -o /dev/null -w "%{http_code}" http://localhost:50021/version 2>/dev/null | grep -q "200"

# macOS say
which say && say -v '?' | head -1

# edge-tts (npm)
npx --yes edge-tts --list-voices 2>/dev/null | head -1
# または: which edge-tts

# google_tts (Python SDK + 認証)
python3 -c "from google.cloud import texttospeech; print('ok')" 2>/dev/null
test -n "$GOOGLE_APPLICATION_CREDENTIALS" && test -f "$GOOGLE_APPLICATION_CREDENTIALS"
```

---

## Voice Mapping

### Japanese Voices

| ペルソナ属性 | VOICEVOX (speaker_id) | say Voice | edge-tts Voice | google_tts Voice | Notes |
|-------------|----------------------|-----------|----------------|-----------------|-------|
| 女性・若年 (20s) | 四国めたん:ノーマル (2) | Kyoko | ja-JP-NanamiNeural | ja-JP-Neural2-B | デフォルト女性ボイス |
| 男性・若年 (20s) | 剣崎雌雄:ノーマル (46) | Eddy (ja_JP) | ja-JP-KeitaNeural | ja-JP-Neural2-C | デフォルト男性ボイス |
| 女性・中年 (30-50s) | 九州そら:ノーマル (16) | Flo (ja_JP) | ja-JP-NanamiNeural | ja-JP-Neural2-B | 幅広い年齢に対応 |
| 男性・中年 (30-50s) | 玄野武宏:ノーマル (11) | Reed (ja_JP) | ja-JP-KeitaNeural | ja-JP-Neural2-D | 幅広い年齢に対応 |
| 高齢 (60+) 女性 | 九州そら (16) + speed 0.85 | Grandma (ja_JP) | ja-JP-NanamiNeural | ja-JP-Neural2-B | + rate 減速 (-15%) / speaking_rate 0.85 |
| 高齢 (60+) 男性 | 玄野武宏 (11) + speed 0.85 | Grandpa (ja_JP) | ja-JP-KeitaNeural | ja-JP-Neural2-D | + rate 減速 (-15%) / speaking_rate 0.85 |

### VOICEVOX Speaker Styles Reference

VOICEVOX はキャラクター × スタイルで speaker_id が決まる。代表的な組み合わせ:

| Character | Style | speaker_id | Gender | Recommended For |
|-----------|-------|-----------|--------|-----------------|
| 四国めたん | ノーマル | 2 | F | デフォルト女性ボイス、若年ペルソナ |
| 四国めたん | あまあま | 0 | F | cheerful / enthusiastic 感情 |
| 四国めたん | セクシー | 4 | F | reserved / formal トーン |
| ずんだもん | ノーマル | 3 | F | カジュアル、親しみやすい |
| 春日部つむぎ | ノーマル | 8 | F | 明るい、元気な若年ペルソナ |
| 玄野武宏 | ノーマル | 11 | M | デフォルト男性ボイス、中年ペルソナ |
| 剣崎雌雄 | ノーマル | 46 | M | 若年男性ペルソナ |
| 九州そら | ノーマル | 16 | F | 落ち着いた女性、中年ペルソナ |
| 九州そら | セクシー | 19 | F | formal / reserved トーン |
| WhiteCUL | ノーマル | 23 | F | ニュートラル、ナレーション向け |

> **動的取得:** `curl -s http://localhost:50021/speakers | python3 -m json.tool` で全キャラクター×スタイルの一覧を取得可能。

### English Voices

| ペルソナ属性 | say Voice | edge-tts Voice | google_tts Voice | Notes |
|-------------|-----------|----------------|-----------------|-------|
| 女性・若年 | Samantha | en-US-JennyNeural | en-US-Neural2-F | |
| 男性・若年 | Alex | en-US-GuyNeural | en-US-Neural2-D | |
| 女性・中年 | Fiona | en-US-AriaNeural | en-US-Neural2-C | |
| 男性・中年 | Daniel | en-US-DavisNeural | en-US-Neural2-A | |

### Parameter Mapping (VOICEVOX ↔ say ↔ edge-tts ↔ google_tts)

```
Rate / Speed:
  VOICEVOX speedScale 1.0 ≈ say 180 WPM ≈ edge-tts "+0%" ≈ google_tts 1.0
  変換式:
    voicevox_speed = say_rate / 180
    voicevox_speed = 1.0 + (edge_rate_pct / 100)
    voicevox_speed = google_rate
    edge_rate% = ((say_rate - 180) / 180) × 100
    google_rate = say_rate / 180
  例: say 200 → voicevox 1.11 → edge "+11%" → google 1.11
      say 150 → voicevox 0.83 → edge "-17%" → google 0.83

Pitch:
  VOICEVOX pitchScale: -0.15〜+0.15（微細調整）
  say は直接制御不可（ボイス選択で間接制御）
  edge-tts は -50Hz〜+50Hz で直接制御
  google_tts は -20.0〜+20.0 半音 (semitones) で直接制御
  近似変換:
    voicevox_pitch ≈ edge Hz / 333  (e.g., edge "+5Hz" → voicevox 0.015)
    google semitones ≈ edge Hz / 10
  例: edge "+5Hz" → voicevox 0.015 → google 0.5st

Intonation (VOICEVOX 固有):
  VOICEVOX intonationScale: 0.0〜2.0（default: 1.0）
  emotional_tone からの推定:
    enthusiastic / cheerful → 1.3〜1.5
    neutral → 1.0
    reserved / frustrated → 0.7〜0.8
  他エンジンには直接対応パラメータなし

Volume:
  VOICEVOX volumeScale: 0.0〜2.0（default: 1.0）
  edge-tts: -50%〜+50%
  google_tts: -96.0〜+16.0 dB
  近似変換:
    voicevox_volume ≈ 1.0 + (edge_volume_pct / 100)
...
```

### TTS Command Templates

```bash
# VOICEVOX — audio_query → synthesis (2ステップ API)
curl -s -X POST "http://localhost:50021/audio_query?text={text}&speaker={speaker_id}" \
  | curl -s -X POST "http://localhost:50021/synthesis?speaker={speaker_id}" \
    -H "Content-Type: application/json" -d @- -o {output_path}

# VOICEVOX — パラメータ調整版（python3 で JSON 操作）
QUERY=$(curl -s -X POST "http://localhost:50021/audio_query?text={text}&speaker={speaker_id}")
QUERY=$(echo "$QUERY" | python3 -c "
import sys, json
q = json.load(sys.stdin)
q['speedScale'] = {speed}
q['pitchScale'] = {pitch}
q['intonationScale'] = {intonation}
q['volumeScale'] = {volume}
json.dump(q, sys.stdout)
")
echo "$QUERY" | curl -s -X POST "http://localhost:50021/synthesis?speaker={speaker_id}" \
  -H "Content-Type: application/json" -d @- -o {output_path}

# VOICEVOX — ワンライナー版
curl -s -X POST "http://localhost:50021/audio_query?text={text}&speaker={speaker_id}" \
  | python3 -c "import sys,json;q=json.load(sys.stdin);q.update(speedScale={speed},pitchScale={pitch},intonationScale={intonation},volumeScale={volume});json.dump(q,sys.stdout)" \
  | curl -s -X POST "http://localhost:50021/synthesis?speaker={speaker_id}" -H "Content-Type: application/json" -d @- -o {output_path}

# macOS say — 直接再生
say -v {voice} -r {rate} "{text}"

# macOS say — ファイル出力
say -v {voice} -r {rate} -o {output_path} "{text}"

# edge-tts — ファイル出力 + 再生
npx --yes edge-tts \
  --voice {voice} \
  --rate "{rate}" \
  --pitch "{pitch}" \
  --volume "{volume}" \
  --text "{text}" \
  --write-media {output_path}

# ...
```

---

## Auto-Derivation Rules

voice_profile が未定義の場合、既存ペルソナ属性から音声パラメータを自動推定する。

### speaking_style の自動推定

| 推定対象 | ソース属性 | ルール |
|---------|-----------|--------|
| `formality` | `category` + Profile.Tech Level | `developer`/`internal` → `technical`; Tech Level: Low → `casual`, High → `formal` |
| `vocabulary_level` | Profile.Tech Level | High → `advanced`, Medium → `moderate`, Low → `simple` |
| `sentence_length` | `echo_base_mapping` | Senior / Low-Literacy → `short`, Power User → `medium`, Custom → `mixed` |
| `emotional_tone` | Emotion Triggers セクション | negative dominant (合計 < 0) → `frustrated` or `anxious`; positive dominant → `cheerful`; balanced → `neutral` |
| `linguistic_markers` | Quote セクション | Quote から特徴的なパターンを抽出（疑問形、語尾、口癖） |

### TTS パラメータの自動推定

| 推定対象 | ソース属性 | ルール |
|---------|-----------|--------|
| `voicevox.speaker_id` | Demographics.age_group + 性別 + `language` | 年齢 × 性別 → VOICEVOX Speaker Styles マッピング参照（日本語のみ） |
| `voicevox.speed` / `say.rate` / `edge_tts.rate` / `google_tts.speaking_rate` | `echo_base_mapping` | Senior → 0.85 / 150 WPM / "-15%" / 0.85, Youth (Newbie) → 1.10 / 200 / "+10%" / 1.10, default → 1.0 / 180 / "+0%" / 1.0 |
| `voicevox.pitch` / `edge_tts.pitch` / `google_tts.pitch` | Emotion Triggers | anxious/enthusiastic → 0.05 / "+5Hz" / +2.0st, cheerful → 0.03 / "+3Hz" / +1.0st, reserved → -0.03 / "-5Hz" / -1.0st, default → 0.0 / "+0Hz" / 0.0st |
| `voicevox.intonation` | Emotion Triggers | enthusiastic/cheerful → 1.3–1.5, neutral → 1.0, reserved/frustrated → 0.7–0.8 |
| `say.voice` / `edge_tts.voice` / `google_tts.voice` | Demographics.age_group + `language` | 年齢 × 性別 × 言語 → ボイスマッピングテーブル参照 |
| `language` | Persona file content / Quote section | 日本語 Quote → `ja`, English Quote → `en`, mixed → `auto` |

### Demographics がない場合の年齢間接推定

`echo_base_mapping` から年齢層を推定:

| echo_base_mapping | 推定年齢層 | 推定 voicevox.speed | 推定 say.rate | 推定 edge_tts.rate |
|-------------------|-----------|-------------------|--------------|-------------------|
| The Newbie | 20s-30s | 1.10 | 200 | "+10%" |
| The Power User | 30s-40s | 1.05 | 190 | "+5%" |
| The Skeptic | 30s-50s | 1.00 | 180 | "+0%" |
| The Mobile User | 20s-30s | 1.10 | 200 | "+10%" |
| The Senior | 60+ | 0.85 | 150 | "-15%" |
| Accessibility User | — (default) | 0.90 | 160 | "-10%" |
| Low-Literacy User | — (default) | 0.90 | 160 | "-10%" |
| Competitor Migrant | 30s-40s | 1.05 | 190 | "+5%" |
| Distracted User | 20s-40s | 1.05 | 190 | "+5%" |
| Privacy Paranoid | 30s-50s | 1.00 | 180 | "+0%" |
| Custom Persona | — (default) | 1.00 | 180 | "+0%" |

### 性別推定

Demographics がない場合:
1. Quote セクションの語尾から推定（「〜わ」「〜かしら」→ 女性的、「〜だぜ」「〜だな」→ 男性的）
2. Name から推定可能な場合は使用
3. 推定不可能 → デフォルト: 女性ボイス（VOICEVOX: 四国めたん id:2 / Kyoko / ja-JP-NanamiNeural）

### Auto-Derivation Process

```
1. voice_profile が frontmatter に存在するか確認
   → 存在: そのまま使用
   → 不在: Auto-Derive 開始

2. speaking_style を推定
   a. category + Tech Level → formality
   b. Tech Level → vocabulary_level
   c. echo_base_mapping → sentence_length
   d. Emotion Triggers → emotional_tone
   e. Quote → linguistic_markers

3. TTS パラメータを推定
   a. Demographics (or echo_base_mapping fallback) → age_group
   b. 性別推定 → gender
   c. language 推定
   d. VOICEVOX: age_group × gender → speaker_id (VOICEVOX Speaker Styles マッピング)
   e. VOICEVOX: echo_base_mapping → speed, Emotion Triggers → pitch/intonation
   f. 他エンジン: 既存ルールに従い voice/rate/pitch を推定
...
```

---

## Text Generation — Prompt Design

Harvest の Loose Prompt パターンを応用。最小限の情報で自然な発話を引き出す。

### Base Prompt Template

```markdown
### Character Sketch
{name}。{role}。{emotional_tone}な気分。
口癖: "{quote}"

### Context
{topic_or_scenario}

### Instruction
このキャラクターになりきって、2-5文で語ってください。
口語体で、{formality}な口調で、{sentence_length}い文で。
{linguistic_markers があれば: 以下の口癖を自然に混ぜてください: {markers}}
```

### Anti-AI Rules (Harvest 応用)

自然な人間らしい発話を生成するための制約:

1. **完璧に整った文章にしない** — 実際のユーザーは文法を間違える
2. **感情が先、理由が後** — 人は感情的に反応してから合理化する
3. **語尾が統一されていない** — 「です」と「だよね」が混在してOK
4. **途中で話が逸れる** — 言いたいことが脱線するのが自然
5. **言い切らない** — 「〜かもしれないけど」「〜なのかな」で終わるのも自然

### Topic-Based Prompt (speak about)

```markdown
### Character Sketch
{name}。{role}。
{emotional_tone}な気分で{topic}について考えている。
口癖: "{quote}"

### Goals (for context)
- {goal_1}
- {goal_2}

### Frustrations (for authenticity)
- {frustration_1}
- {frustration_2}

### Instruction
このキャラクターとして、{topic}について2-5文で語ってください。
...
```

### Reaction Prompt (speak react to)

```markdown
### Character Sketch
{name}。{role}。
口癖: "{quote}"

### Emotion Triggers (reference)
{emotion_triggers_table}

### Situation
{context_description}

### Instruction
このキャラクターとして、この状況への最初のリアクションを2-4文で語ってください。
感情が先に来るように。理由は後から。
Emotion Triggers を参照して、適切な感情レベルで反応してください。
```

### Dialogue Prompt (speak dialogue)

```markdown
### Characters

#### {persona_1_name}
Role: {role_1}。{emotional_tone_1}。
口癖: "{quote_1}"
Goals: {goals_1}
Frustrations: {frustrations_1}

#### {persona_2_name}
Role: {role_2}。{emotional_tone_2}。
口癖: "{quote_2}"
Goals: {goals_2}
Frustrations: {frustrations_2}

### Topic
...
```

---

## Dialogue Sub-Mode Design

### Tension Design Rules

複数ペルソナの対話では、テンション（緊張感）を意図的に設計する:

1. **Goals の交差点を見つける** — 各ペルソナの Goals を比較し、競合・補完関係を特定
2. **Frustrations の衝突** — 片方の当然が他方の苛立ちになるポイントを活用
3. **全面同意の禁止** — 最低1回は噛み合わないターンを含める
4. **感情の揺れ** — 会話の中で感情レベルが変動する（最初は穏やか → 中盤で衝突 → 終盤は着地or未解決）

### Turn Count

| Participants | Default Turns | Range |
|-------------|---------------|-------|
| 2人 | 4 | 3-6 |
| 3人 | 6 | 4-8 |
| 4人+ | ON_DIALOGUE_COMPLEXITY trigger | 4-10 |

### Dialogue TTS Rendering

各ターンを対応ペルソナの voice_profile で音声化:

```
Turn 1: persona_1 → voice_profile_1 で TTS
Turn 2: persona_2 → voice_profile_2 で TTS
Turn 3: persona_1 → voice_profile_1 で TTS
...

Output: 個別ファイル (turn-1.wav, turn-2.wav, ...) + 連結再生
  ※ VOICEVOX は WAV 出力。MP3 変換: ffmpeg -i input.wav -codec:a libmp3lame output.mp3
```

---

## Output Modes

| Mode | Description | Default |
|------|-------------|---------|
| **play** | 音声を直接再生 | Yes (デフォルト) |
| **save** | ファイルに保存 | No |
| **both** | 再生 + 保存 | No |
| **text-only** | テキストのみ出力（TTS なし） | Fallback when no engine available |

### Output File Naming

```
.agents/personas/{service}/speak/
├── {persona-name}_{topic}_{timestamp}.wav     # 単一発話 (VOICEVOX: WAV, 他: MP3)
├── dialogue_{p1}_{p2}_{topic}_{timestamp}/     # 対話
│   ├── turn-1_{p1}.wav
│   ├── turn-2_{p2}.wav
│   ├── turn-3_{p1}.wav
│   └── turn-4_{p2}.wav
└── transcript_{timestamp}.md                   # テキスト記録
```

### Transcript Format

```markdown
## SPEAK Transcript

- **Date:** YYYY-MM-DD HH:MM
- **Mode:** speak / dialogue
- **Engine:** voicevox / say / edge-tts / google_tts
- **Persona(s):** {names}

### Generated Text

> {persona_name}: "{generated_text}"

### Voice Parameters Used

| Parameter | Value |
|-----------|-------|
...
```

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| VOICEVOX not running | `localhost:50021` 接続不可（VOICEVOX 未起動） | edge-tts フォールバック。VOICEVOX 起動手順を案内 |
| VOICEVOX speaker_id invalid | 指定 speaker_id が存在しない | `/speakers` API で確認案内 → デフォルト id:2 フォールバック |
| VOICEVOX synthesis timeout | 合成処理が 10 秒超過 | リトライ 1 回 → edge-tts フォールバック |
| VOICEVOX text encoding error | UTF-8 以外の文字混入 | UTF-8 確認 → 特殊文字除去リトライ |
| VOICEVOX large text | テキストが 500 文字超 | セグメント分割（500 文字単位）→ 順次合成 → 結合 |
| Engine unavailable | `say` not on macOS, `edge-tts` not installed/no network | ON_ENGINE_UNAVAILABLE → fallback or text-only |
| Voice not found | Specified voice name invalid | Fall back to default voice for language |
| Text too long | Generated text exceeds TTS limit | Split into segments (max ~500 chars per segment) |
| Persona not found | Registry lookup failed | Error message with suggestion to run `/Cast conjure` |
| No quote section | Quote missing in persona file | Use Goals[0] as fallback character sketch |
| Network timeout | edge-tts API timeout | Retry once, then fall back to `say` or text-only |
| `GOOGLE_APPLICATION_CREDENTIALS` 未設定 | google_tts 認証情報なし | edge-tts フォールバック推奨。認証設定手順を案内 |
| google-cloud-texttospeech SDK 未インストール | Python パッケージ未導入 | `pip3 install google-cloud-texttospeech` を提案。edge-tts フォールバック |
| Google Cloud quota exceeded | API 使用量が無料枠/上限を超過 | 警告表示 → edge-tts フォールバック |
| Google Cloud permission denied | サービスアカウント権限不足 | 認証設定の確認を案内（IAM ロール: `roles/texttospeech.user`） |

---

## Cost Management (google_tts)

google_tts は有料 API のため、意図しない課金を防止する設計を採用。

### Pricing

| Voice Type | Cost/1M chars | Free Tier |
|-----------|--------------|-----------|
| Neural2 | $16.00 | 1M chars/month |
| WaveNet | $16.00 | 1M chars/month |
| Standard | $4.00 | 4M chars/month |

### Cost Control Measures

1. **auto モード除外** — `engine_preference: auto` 時に google_tts は選択されない（明示指定のみ）
2. **長文事前確認** — 生成テキストが 1000 文字を超える場合、概算コストを表示して確認
3. **dialogue 個別合成** — 各ターンを個別に音声合成（部分再実行が可能、無駄な再合成を回避）
4. **Neural2 デフォルト** — Standard より高品質だが無料枠（1M chars/month）で十分な利用が可能

### Usage Estimation

```
1 発話 (50文字) ≈ $0.0008 (Neural2)
10 発話/日 × 30日 = 15,000文字/月 ≈ 無料枠内
dialogue 4ターン (200文字) ≈ $0.0032 (Neural2)
```

---

## Integration with Cast Ecosystem

### EVOLVE Integration

SPEAK で Auto-Derive された voice_profile は一時的。永続化するには:

```
/Cast evolve [persona]  →  voice_profile の Auto-Derive 結果を review → EVOLVE で frontmatter に追記
```

Evolution Log に記録: `"voice_profile added (auto-derived → persisted)"`

### DISTRIBUTE Integration

SPEAK データを下流エージェントに配信する場合:

| Consumer | SPEAK Data Included |
|----------|-------------------|
| Harvest | speaking_style (キャラクター表現の参考) |
| Prism | voice_profile 全体 (NotebookLM Audio ステアリング) |
| Aether | voicevox パラメータ (AITuber TTS 設定: speaker_id, speed, pitch, intonation) |
| Director | voicevox/say/edge_tts/google_tts パラメータ (ナレーション設定) |
| Echo | linguistic_markers (UI テキストのトーン参考) |

### Harvest Reference

Harvest の3ペルソナ声質定義パターン（Codex/Gemini/Claude）を参考に、speaking_style の設計を行った。Harvest はテキスト生成スタイルの設計、Cast SPEAK は音声合成パラメータまで含む統合ソリューション。
