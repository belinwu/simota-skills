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

---

## TTS Engine Architecture

### Supported Engines

| Engine | Platform | Quality | Offline | Cost | Install |
|--------|----------|---------|---------|------|---------|
| **macOS `say`** | macOS only | Standard (concatenative) | Yes | Free | Pre-installed |
| **edge-tts** | Cross-platform | High (Neural TTS) | No (requires network) | Free | `npx --yes edge-tts` |
| **google_tts** | Cross-platform | Very High (Neural2/WaveNet) | No (requires network) | $16/1M chars (Neural2) | `pip3 install google-cloud-texttospeech` |

### Engine Selection Logic

```
engine_preference が明示指定されている場合:
  → そのエンジンを使用
  → unavailable なら ON_ENGINE_UNAVAILABLE トリガー発火
  → フォールバック順: google_tts → edge-tts → say

engine_preference: auto の場合:
  ※ google_tts は auto に含まない（課金保護 — 明示指定時のみ使用）
  1. edge-tts が利用可能か確認 (`which edge-tts` or npx availability)
     → 利用可能: edge-tts を使用（Neural TTS で高品質）
  2. macOS say が利用可能か確認 (`which say`)
     → 利用可能: say をフォールバックとして使用
  3. 両方 unavailable:
     → テキストのみ出力（警告メッセージ付き）
     → ON_ENGINE_UNAVAILABLE トリガー（AUTORUN: テキストのみ続行）

engine_preference: google_tts の場合:
  1. 認証チェック ($GOOGLE_APPLICATION_CREDENTIALS が設定済み & ファイル存在)
  2. SDK チェック (google-cloud-texttospeech インストール済み)
  3. 両方 OK → google_tts で実行
  4. 失敗時 → edge-tts フォールバック → say フォールバック
```

### Engine Availability Check

```bash
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

| ペルソナ属性 | say Voice | edge-tts Voice | google_tts Voice | Notes |
|-------------|-----------|----------------|-----------------|-------|
| 女性・若年 (20s) | Kyoko | ja-JP-NanamiNeural | ja-JP-Neural2-B | デフォルト女性ボイス |
| 男性・若年 (20s) | Eddy (ja_JP) | ja-JP-KeitaNeural | ja-JP-Neural2-C | デフォルト男性ボイス |
| 女性・中年 (30-50s) | Flo (ja_JP) | ja-JP-NanamiNeural | ja-JP-Neural2-B | Nanami / Neural2-B は幅広い年齢に対応 |
| 男性・中年 (30-50s) | Reed (ja_JP) | ja-JP-KeitaNeural | ja-JP-Neural2-D | Keita / Neural2-D は幅広い年齢に対応 |
| 高齢 (60+) 女性 | Grandma (ja_JP) | ja-JP-NanamiNeural | ja-JP-Neural2-B | + rate 減速 (-15%) / speaking_rate 0.85 |
| 高齢 (60+) 男性 | Grandpa (ja_JP) | ja-JP-KeitaNeural | ja-JP-Neural2-D | + rate 減速 (-15%) / speaking_rate 0.85 |

### English Voices

| ペルソナ属性 | say Voice | edge-tts Voice | google_tts Voice | Notes |
|-------------|-----------|----------------|-----------------|-------|
| 女性・若年 | Samantha | en-US-JennyNeural | en-US-Neural2-F | |
| 男性・若年 | Alex | en-US-GuyNeural | en-US-Neural2-D | |
| 女性・中年 | Fiona | en-US-AriaNeural | en-US-Neural2-C | |
| 男性・中年 | Daniel | en-US-DavisNeural | en-US-Neural2-A | |

### Parameter Mapping (say ↔ edge-tts ↔ google_tts)

```
Rate:
  say 180 WPM ≈ edge-tts "+0%" ≈ google_tts 1.0
  変換式:
    edge_rate% = ((say_rate - 180) / 180) × 100
    google_rate = say_rate / 180
    google_rate = 1.0 + (edge_rate_pct / 100)
  例: say 200 → edge "+11%" → google 1.11
      say 150 → edge "-17%" → google 0.83

Pitch:
  say は直接制御不可（ボイス選択で間接制御）
  edge-tts は -50Hz〜+50Hz で直接制御
  google_tts は -20.0〜+20.0 半音 (semitones) で直接制御
  近似変換: google semitones ≈ edge Hz / 10
  例: edge "+5Hz" → google 0.5st, edge "-10Hz" → google -1.0st

Volume:
  say は直接制御不可（システムボリューム依存）
  edge-tts は -50%〜+50% で直接制御
  google_tts は -96.0〜+16.0 dB で直接制御
  近似変換: google volume_gain_db ≈ (edge_volume_pct / 50) × 16
  例: edge "+25%" → google +8.0dB, edge "-50%" → google -16.0dB

Output Format:
  say → .aiff (default) or .m4a (with --file-format)
  edge-tts → .mp3
  google_tts → .mp3 (default) or .wav (LINEAR16 encoding)
```

### TTS Command Templates

```bash
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

# edge-tts 出力ファイルの再生 (macOS)
afplay {output_path}

# google_tts — Python SDK でファイル出力
python3 -c "
from google.cloud import texttospeech
client = texttospeech.TextToSpeechClient()
synthesis_input = texttospeech.SynthesisInput(text=\"{text}\")
voice = texttospeech.VoiceSelectionParams(
    language_code=\"{lang}\", name=\"{voice_name}\")
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
    speaking_rate={rate}, pitch={pitch}, volume_gain_db={vol})
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config)
with open(\"{output_path}\", \"wb\") as f:
    f.write(response.audio_content)
"

# google_tts 出力ファイルの再生 (macOS)
afplay {output_path}
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
| `say.voice` / `edge_tts.voice` / `google_tts.voice` | Demographics.age_group + `language` | 年齢 × 性別 × 言語 → ボイスマッピングテーブル参照 |
| `say.rate` / `edge_tts.rate` / `google_tts.speaking_rate` | `echo_base_mapping` | Senior → 150 WPM / "-15%" / 0.85, Youth (Newbie) → 200 / "+10%" / 1.10, default → 180 / "+0%" / 1.0 |
| `edge_tts.pitch` / `google_tts.pitch` | Emotion Triggers | anxious/enthusiastic → "+5Hz" / +2.0st, cheerful → "+3Hz" / +1.0st, reserved → "-5Hz" / -1.0st, default → "+0Hz" / 0.0st |
| `language` | Persona file content / Quote section | 日本語 Quote → `ja`, English Quote → `en`, mixed → `auto` |

### Demographics がない場合の年齢間接推定

`echo_base_mapping` から年齢層を推定:

| echo_base_mapping | 推定年齢層 | 推定 say.rate | 推定 edge_tts.rate |
|-------------------|-----------|--------------|-------------------|
| The Newbie | 20s-30s | 200 | "+10%" |
| The Power User | 30s-40s | 190 | "+5%" |
| The Skeptic | 30s-50s | 180 | "+0%" |
| The Mobile User | 20s-30s | 200 | "+10%" |
| The Senior | 60+ | 150 | "-15%" |
| Accessibility User | — (default) | 160 | "-10%" |
| Low-Literacy User | — (default) | 160 | "-10%" |
| Competitor Migrant | 30s-40s | 190 | "+5%" |
| Distracted User | 20s-40s | 190 | "+5%" |
| Privacy Paranoid | 30s-50s | 180 | "+0%" |
| Custom Persona | — (default) | 180 | "+0%" |

### 性別推定

Demographics がない場合:
1. Quote セクションの語尾から推定（「〜わ」「〜かしら」→ 女性的、「〜だぜ」「〜だな」→ 男性的）
2. Name から推定可能な場合は使用
3. 推定不可能 → デフォルト: 女性ボイス（Kyoko / ja-JP-NanamiNeural）

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
   d. age × gender × language → voice selection
   e. age_group → rate
   f. emotional_tone → pitch (edge-tts only)

4. 推定結果を一時的な voice_profile として使用（ファイルには書き込まない）
   → ユーザーが EVOLVE で永続化を選択可能
```

---

## Text Generation — Prompt Design

Bard の Loose Prompt パターンを応用。最小限の情報で自然な発話を引き出す。

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

### Anti-AI Rules (Bard 応用)

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
{formality}な口調で、自分の経験に基づいて。
Goals や Frustrations の観点が自然に出るようにしてください。
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
{topic}

### Tension Design
- {persona_1_name} の Goals と {persona_2_name} の Frustrations が交差するポイント
- 全面同意にせず、噛み合わない部分を作る

### Instruction
この2人のキャラクターが{topic}について{turn_count}ターン会話してください。
各ターンは1-3文。
口語体で、各キャラクターの口調・語彙レベルを維持してください。
相手の言葉にちゃんと反応しつつ、完全同意にはならないようにしてください。

### Format
{persona_1_name}: (セリフ)
{persona_2_name}: (セリフ)
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

Output: 個別ファイル (turn-1.mp3, turn-2.mp3, ...) + 連結再生
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
├── {persona-name}_{topic}_{timestamp}.mp3     # 単一発話
├── dialogue_{p1}_{p2}_{topic}_{timestamp}/     # 対話
│   ├── turn-1_{p1}.mp3
│   ├── turn-2_{p2}.mp3
│   ├── turn-3_{p1}.mp3
│   └── turn-4_{p2}.mp3
└── transcript_{timestamp}.md                   # テキスト記録
```

### Transcript Format

```markdown
## SPEAK Transcript

- **Date:** YYYY-MM-DD HH:MM
- **Mode:** speak / dialogue
- **Engine:** say / edge-tts / google_tts
- **Persona(s):** {names}

### Generated Text

> {persona_name}: "{generated_text}"

### Voice Parameters Used

| Parameter | Value |
|-----------|-------|
| Engine | edge-tts |
| Voice | ja-JP-NanamiNeural |
| Rate | +0% |
| Pitch | +0Hz |

### Source
- Auto-derived: {yes/no}
- voice_profile version: {version or "N/A (auto-derived)"}
```

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
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
| Bard | speaking_style (キャラクター表現の参考) |
| Prism | voice_profile 全体 (NotebookLM Audio ステアリング) |
| Director | say/edge_tts/google_tts パラメータ (ナレーション設定) |
| Echo | linguistic_markers (UI テキストのトーン参考) |

### Bard Reference

Bard の3ペルソナ声質定義パターン（Codex/Gemini/Claude）を参考に、speaking_style の設計を行った。Bard はテキスト生成スタイルの設計、Cast SPEAK は音声合成パラメータまで含む統合ソリューション。
