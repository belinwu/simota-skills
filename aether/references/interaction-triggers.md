# Interaction Triggers

AskUserQuestion ツール用 YAML テンプレート。`_common/INTERACTION.md` の標準フォーマットに準拠。

---

## BEFORE_START Triggers

### ON_TECH_STACK

```yaml
trigger: ON_TECH_STACK
timing: BEFORE_START
condition: "Runtime/language not specified for pipeline implementation"
question: "パイプラインのランタイムをどれにしますか？"
options:
  - label: "Node.js (TypeScript)"
    description: "OBS WebSocket、ブラウザベースアバターとの親和性が高い。エコシステム豊富。推奨"
  - label: "Python"
    description: "ML/AI ライブラリ豊富。SBV2 との統合が容易。TTS エンジンとの相性が良い"
  - label: "Hybrid (Node.js + Python)"
    description: "メインパイプラインは Node.js、TTS/ML 部分は Python。複雑だが最適化しやすい"
  - label: "Other (please specify)"
    description: "別のランタイムを指定"
recommended: "Node.js (TypeScript)"
```

### ON_TTS_ENGINE

```yaml
trigger: ON_TTS_ENGINE
timing: BEFORE_START
condition: "TTS engine not specified for voice synthesis"
question: "メインの TTS エンジンをどれにしますか？"
options:
  - label: "VOICEVOX"
    description: "セットアップ簡単、音素タイミング取得可能（リップシンク最適）、無料。推奨（v1）"
  - label: "Style-Bert-VITS2"
    description: "最高品質、カスタム音声学習可能。GPU推奨、セットアップ複雑"
  - label: "COEIROINK"
    description: "軽量・高速。リソース制約がある環境向け"
  - label: "NIJIVOICE (Cloud)"
    description: "クラウドAPI。GPUなし環境、安定したレイテンシ。従量課金"
recommended: "VOICEVOX"
```

### ON_AVATAR_FRAMEWORK

```yaml
trigger: ON_AVATAR_FRAMEWORK
timing: BEFORE_START
condition: "Avatar framework not specified"
question: "アバターフレームワークをどちらにしますか？"
options:
  - label: "Live2D Cubism SDK for Web"
    description: "2D VTuber標準。パラメータ制御が直感的。日本のVTuber文化で主流。推奨"
  - label: "VRM (@pixiv/three-vrm)"
    description: "3D VTuber。オープン標準。フルボディトラッキング対応。3Dモデル活用時"
  - label: "Both (adapter pattern)"
    description: "抽象レイヤーで両方対応。将来の切り替えを想定。初期コスト高"
recommended: "Live2D Cubism SDK for Web"
```

### ON_STREAMING_PLATFORM

```yaml
trigger: ON_STREAMING_PLATFORM
timing: BEFORE_START
condition: "Target streaming platform not specified"
question: "メインの配信プラットフォームはどれですか？"
options:
  - label: "YouTube Live"
    description: "日本の AITuber コミュニティの主流。Super Chat 対応。API クォータ制限あり"
  - label: "Twitch"
    description: "リアルタイム IRC チャット。EventSub で拡張イベント対応。海外コミュニティ向け"
  - label: "Both (YouTube + Twitch)"
    description: "同時配信。チャット統合が複雑化。視聴者ベース最大化"
  - label: "Other (please specify)"
    description: "ニコニコ生放送、SHOWROOM など"
recommended: "YouTube Live"
```

---

## ON_DECISION Triggers

### ON_LLM_PROVIDER

```yaml
trigger: ON_LLM_PROVIDER
timing: ON_DECISION
condition: "LLM provider not specified for response generation"
question: "応答生成に使う LLM をどれにしますか？"
options:
  - label: "Claude (Anthropic)"
    description: "日本語品質高、長文コンテキスト。API コスト中程度"
  - label: "GPT-4 (OpenAI)"
    description: "汎用性高、ストリーミング対応良好。API コスト高"
  - label: "Local LLM (llama.cpp etc.)"
    description: "コスト無料、レイテンシ制御可能。品質はモデル依存。GPU必要"
  - label: "Other (please specify)"
    description: "Gemini、Cohere など"
recommended: "Claude (Anthropic)"
```

### ON_LATENCY_TRADEOFF

```yaml
trigger: ON_LATENCY_TRADEOFF
timing: ON_DECISION
condition: "Latency target cannot be met with current quality settings"
question: "レイテンシ目標（3000ms）を達成するために品質を下げますか？"
options:
  - label: "レイテンシ優先（品質を下げる）"
    description: "LLM の max_tokens を減らし、TTS の品質設定を下げる。応答は短く速くなる"
  - label: "品質優先（レイテンシを緩和）"
    description: "3000ms 目標を 5000ms に緩和。自然な応答を維持"
  - label: "ハイブリッド（短い応答は高速、長い応答は高品質）"
    description: "応答の長さに応じて動的に切り替え。実装が複雑"
recommended: "ハイブリッド（短い応答は高速、長い応答は高品質）"
```

### ON_CHAT_MODERATION

```yaml
trigger: ON_CHAT_MODERATION
timing: ON_DECISION
condition: "Chat moderation level not specified"
question: "チャットモデレーションの厳しさをどのレベルにしますか？"
options:
  - label: "Strict（厳格）"
    description: "ブロックリスト + LLM判定。誤フィルタの可能性あり。安全重視"
  - label: "Standard（標準）"
    description: "キーワードフィルタ + 基本的な安全チェック。バランス型。推奨"
  - label: "Relaxed（緩め）"
    description: "明らかな違反のみフィルタ。コミュニティ成熟度が高い場合"
recommended: "Standard（標準）"
```

### ON_GPU_ALLOCATION

```yaml
trigger: ON_GPU_ALLOCATION
timing: ON_DECISION
condition: "GPU resources limited and multiple components need GPU"
question: "GPU リソースの配分をどうしますか？"
options:
  - label: "TTS 優先"
    description: "TTS に GPU を割り当て、アバターは CPU レンダリング。音声品質重視"
  - label: "Avatar 優先"
    description: "アバターに GPU を割り当て、TTS は CPU 推論。ビジュアル重視"
  - label: "Cloud TTS + Local Avatar"
    description: "TTS をクラウド API（NIJIVOICE）に逃がし、GPU はアバター専用。コスト増"
recommended: "Cloud TTS + Local Avatar"
```

---

## ON_RISK Triggers

### ON_LIVE_DEPLOYMENT

```yaml
trigger: ON_LIVE_DEPLOYMENT
timing: ON_RISK
condition: "First deployment to public live stream"
question: "初回ライブ配信デプロイを実行しますか？"
options:
  - label: "Dry-run first（ドライランから）"
    description: "非公開でフルパイプラインテスト → 問題なければ公開。推奨"
  - label: "限定公開で開始"
    description: "URLを知っている人のみ。小規模テスト後に公開へ移行"
  - label: "即座に公開配信"
    description: "テスト完了済みの場合のみ。リスク高"
recommended: "Dry-run first（ドライランから）"
```

### ON_PERSONA_CHANGE

```yaml
trigger: ON_PERSONA_CHANGE
timing: ON_RISK
condition: "Significant persona behavior change during active stream"
question: "配信中にペルソナの大幅な行動変更を適用しますか？"
options:
  - label: "次回配信から適用"
    description: "現在の配信には影響なし。安全。推奨"
  - label: "休憩後に適用"
    description: "BRBシーンに切り替え → 変更適用 → 配信再開"
  - label: "即座に適用"
    description: "視聴者に変化が見える。キャラクター一貫性のリスクあり"
recommended: "次回配信から適用"
```
