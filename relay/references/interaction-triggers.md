# Interaction Trigger Templates

YAML templates for `AskUserQuestion` tool at each trigger point.

---

## ON_PLATFORM_SELECTION

```yaml
trigger: ON_PLATFORM_SELECTION
timing: BEFORE_START
questions:
  - question: "どのメッセージングプラットフォームを対象にしますか？優先順位を教えてください。"
    header: "Platform"
    multiSelect: true
    options:
      - label: "Slack"
        description: "Bolt.js / WebClient。企業内コミュニケーション向け"
      - label: "Discord"
        description: "discord.js。コミュニティ・ゲーミング向け"
      - label: "Telegram"
        description: "grammY / node-telegram-bot-api。グローバル・Bot向け"
      - label: "LINE"
        description: "LINE Bot SDK。日本市場向け"
```

---

## ON_SDK_CHOICE

```yaml
trigger: ON_SDK_CHOICE
timing: ON_DECISION
questions:
  - question: "対象プラットフォームのSDKを選択してください。"
    header: "SDK"
    options:
      - label: "公式SDK（推奨）"
        description: "安定性・サポート重視。Bolt.js, LINE SDK等"
      - label: "コミュニティSDK"
        description: "機能豊富・柔軟。discord.js, grammY等"
      - label: "低レベルAPI直接呼び出し"
        description: "最大の制御。REST API直接利用"
      - label: "プラットフォームごとに最適なSDKを選択"
        description: "各プラットフォームに最適なSDKを個別に選定"
```

---

## ON_TRANSPORT_STRATEGY

```yaml
trigger: ON_TRANSPORT_STRATEGY
timing: ON_DECISION
questions:
  - question: "リアルタイム通信のトランスポート戦略を選択してください。"
    header: "Transport"
    options:
      - label: "WebSocket（推奨）"
        description: "双方向リアルタイム通信。チャット、コラボレーション向け"
      - label: "SSE (Server-Sent Events)"
        description: "サーバー→クライアントのプッシュ通知。通知、ダッシュボード向け"
      - label: "WebSocket + SSEフォールバック"
        description: "WebSocket優先、SSEフォールバック。ブラウザ互換性重視"
      - label: "Long Polling"
        description: "レガシーブラウザ対応。シンプルだが高レイテンシ"
```

---

## ON_QUEUE_TECHNOLOGY

```yaml
trigger: ON_QUEUE_TECHNOLOGY
timing: ON_DECISION
questions:
  - question: "メッセージキュー技術を選択してください。信頼性のあるメッセージ配信に使用します。"
    header: "Queue"
    options:
      - label: "Redis (BullMQ)（推奨）"
        description: "シンプル・高速。既存Redisインフラ活用可能"
      - label: "RabbitMQ"
        description: "堅牢なルーティング・DLQ。複雑なルーティングが必要な場合"
      - label: "Amazon SQS"
        description: "マネージドサービス。AWS環境向け"
      - label: "キューなし（直接処理）"
        description: "低ボリューム・シンプル構成向け。メッセージ損失リスクあり"
```

---

## ON_SCHEMA_BREAKING_CHANGE

```yaml
trigger: ON_SCHEMA_BREAKING_CHANGE
timing: ON_RISK
questions:
  - question: "イベントスキーマの変更が既存コンシューマに影響を与える可能性があります。どう対応しますか？"
    header: "Schema"
    options:
      - label: "バージョニングで後方互換維持（推奨）"
        description: "新バージョンを追加し、旧バージョンも並行サポート"
      - label: "マイグレーション期間を設けて移行"
        description: "非推奨警告→マイグレーション→旧バージョン廃止"
      - label: "即時変更（影響範囲が限定的）"
        description: "影響を受けるコンシューマが少数の場合"
      - label: "変更を見送り、別の方法を検討"
        description: "スキーマ変更なしで要件を満たす代替案を探す"
```

---

## ON_SCALING_STRATEGY

```yaml
trigger: ON_SCALING_STRATEGY
timing: ON_DECISION
questions:
  - question: "WebSocket/リアルタイム接続の水平スケーリング戦略を選択してください。"
    header: "Scaling"
    options:
      - label: "Redis Pub/Sub（推奨）"
        description: "シンプルで実績あり。10K-100K接続向け"
      - label: "Sticky Sessions (IPハッシュ)"
        description: "最もシンプル。10K接続未満の小規模向け"
      - label: "専用メッセージブローカー (NATS/RabbitMQ)"
        description: "堅牢なメッセージルーティング。大規模・複雑なルーティング向け"
      - label: "Socket.io Adapter (Redis)"
        description: "Socket.io使用時のターンキーソリューション"
```
