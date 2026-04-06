# Workflow Engine Selection Guide

**Purpose:** ワークフローエンジンの選定ガイド。
**Read when:** プロジェクトに適したワークフローエンジンを選定する時。

---

## Engine Comparison Matrix

| Engine | Type | Language | Hosting | Durability | Complexity | Cost Model |
|--------|------|----------|---------|------------|------------|------------|
| Temporal | General | Go/Java/TS/Python | Self/Cloud | High | Medium-High | Self: infra, Cloud: per-action |
| AWS Step Functions | Serverless | ASL (JSON) | AWS | High | Medium | Per transition |
| Inngest | Event-driven | TS/Go/Python | Cloud/Self | High | Low-Medium | Per run |
| XState | Client-side | TS/JS | N/A (in-process) | None (stateless) | Low-Medium | Free |
| Cadence | General | Go/Java | Self-hosted | High | High | Infra only |
| Apache Airflow | Data pipeline | Python | Self/Cloud | Medium | Medium | Infra only |
| Prefect | Data pipeline | Python | Self/Cloud | Medium | Low-Medium | Per task |

---

## Selection Decision Tree

```
ワークフローの種類は？
├── フロントエンド状態管理
│   └── XState
├── データパイプライン / ETL
│   ├── Python重視 → Airflow or Prefect
│   └── Stream連携 → Kafka Streams (→ Streamエージェント参照)
├── サーバーレス / イベント駆動
│   ├── AWS限定 → Step Functions
│   └── マルチクラウド → Inngest
└── 汎用ビジネスワークフロー
    ├── 既にAWS → Step Functions
    ├── マルチクラウド / 高可用性
    │   ├── マネージド希望 → Temporal Cloud
    │   └── セルフホスト可 → Temporal OSS or Cadence
    └── シンプルなイベント連鎖 → Inngest
```

---

## Temporal

### Strengths
- 言語ネイティブのワークフロー定義（コードがそのままワークフロー）
- 強力な耐久性保証（replay-safe execution）
- Signal/Query/Update でワークフロー状態の外部操作可能
- Child Workflow、Continue-as-new で長期ワークフロー対応

### Best For
- 長時間実行（日〜月単位）のビジネスプロセス
- 複雑な補償・リトライロジック
- マイクロサービス間オーケストレーション

### Template

```yaml
TEMPORAL_WORKFLOW:
  name: "[WorkflowName]"
  task_queue: "[queue-name]"
  workflow_execution_timeout: "30d"
  activities:
    - name: "[ActivityName]"
      start_to_close_timeout: "30s"
      retry_policy:
        initial_interval: "1s"
        backoff_coefficient: 2.0
        maximum_attempts: 5
        non_retryable_error_types: ["BusinessError"]
  signals:
    - name: "[SignalName]"
      description: "[External trigger]"
  queries:
    - name: "[QueryName]"
      description: "[State inspection]"
```

---

## AWS Step Functions

### Strengths
- AWSサービスとのネイティブ統合（Lambda, SQS, DynamoDB等）
- ASLによる宣言的ワークフロー定義
- Express/Standard の2つの実行モード
- Built-in error handling とリトライ

### Best For
- AWS中心のアーキテクチャ
- サーバーレスワークフロー
- Lambda関数のオーケストレーション

### Template

```json
{
  "Comment": "[WorkflowDescription]",
  "StartAt": "[FirstState]",
  "States": {
    "[StateName]": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...",
      "Retry": [{
        "ErrorEquals": ["States.TaskFailed"],
        "IntervalSeconds": 2,
        "MaxAttempts": 3,
        "BackoffRate": 2.0
      }],
      "Catch": [{
        "ErrorEquals": ["States.ALL"],
        "Next": "[ErrorHandler]"
      }],
      "Next": "[NextState]"
    }
  }
}
```

---

## Inngest

### Strengths
- イベント駆動でシンプルなAPI
- サーバーレスファースト（Vercel, Cloudflare等と統合）
- Step function / Sleep / Wait-for-event が組み込み
- ローカル開発体験が良い（Dev Server）

### Best For
- Next.js / Vercel ベースのプロジェクト
- イベント駆動ワークフロー
- バックグラウンドジョブ

### Template (TypeScript)

```typescript
// Inngest function definition
const workflow = inngest.createFunction(
  { id: "[function-id]", retries: 3 },
  { event: "[trigger/event]" },
  async ({ event, step }) => {
    const result1 = await step.run("[step-1]", async () => {
      // Step 1 logic
    });

    await step.sleep("wait-period", "1h");

    const result2 = await step.run("[step-2]", async () => {
      // Step 2 logic using result1
    });

    return { result1, result2 };
  }
);
```

---

## XState (v5)

### Strengths
- TypeScript型安全
- ブラウザ/Node.js両対応
- Stately Studio による視覚的エディタ
- Actor model ベースのスケーラブルな設計

### Best For
- フロントエンド状態管理
- フォームウィザード、UIフロー
- クライアントサイドのワークフロー

### Template

```typescript
import { createMachine } from 'xstate';

const machine = createMachine({
  id: '[machineName]',
  initial: '[initialState]',
  context: {
    // typed context
  },
  states: {
    // state definitions
  },
});
```

---

## Non-Functional Requirements Checklist

選定時に確認すべき非機能要件:

| Requirement | Question |
|-------------|----------|
| Durability | ワークフロー実行中にプロセスが落ちても再開できるか？ |
| Scalability | 同時実行数の上限は？スケールアウト可能か？ |
| Observability | 実行状態の可視化、ログ、メトリクスは十分か？ |
| Cost | 実行回数・遷移数に基づくコスト試算 |
| Latency | 各ステップ間のレイテンシ要件 |
| Vendor lock-in | クラウドベンダーへの依存度 |
| Team skill | チームの既存スキルセットとの親和性 |
| Community | コミュニティの活発さ、ドキュメントの充実度 |
