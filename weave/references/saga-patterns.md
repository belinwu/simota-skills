# Saga Patterns

**Purpose:** Sagaパターン（Orchestration / Choreography）の設計ガイド。
**Read when:** 分散トランザクション・長時間ワークフロー設計が必要な時。

---

## Orchestration Pattern

中央のオーケストレーター（Saga Coordinator）が各ステップを制御する。

### Structure

```
┌──────────────────────────────────┐
│        Saga Orchestrator         │
│                                  │
│  Step 1 → Step 2 → Step 3       │
│    ↓         ↓         ↓        │
│  Comp 3 ← Comp 2 ← Comp 1      │
│  (rollback on failure)           │
└──────────────────────────────────┘
     ↕         ↕         ↕
  Service A  Service B  Service C
```

### Template

```yaml
SAGA_ORCHESTRATION:
  name: "[SagaName]"
  timeout: "[TotalTimeout]"
  steps:
    - name: "[Step1]"
      service: "[ServiceA]"
      action:
        command: "[ForwardCommand]"
        timeout: "[StepTimeout]"
        retry:
          max_attempts: 3
          backoff: exponential
          base_delay: "1s"
      compensation:
        command: "[CompensationCommand]"
        timeout: "[CompTimeout]"
        retry:
          max_attempts: 5
          backoff: exponential
      on_success: "[Step2]"
      on_failure: "COMPENSATE"
    - name: "[Step2]"
      service: "[ServiceB]"
      action:
        command: "[ForwardCommand]"
      compensation:
        command: "[CompensationCommand]"
      on_success: "[Step3]"
      on_failure: "COMPENSATE"
  compensation_order: "reverse"  # reverse | custom
  idempotency:
    strategy: "idempotency_key"
    key_format: "saga:{saga_id}:step:{step_name}:{attempt}"
```

### Use Cases

- EC注文処理（在庫確保 → 決済 → 出荷指示）
- ユーザー登録（アカウント作成 → メール送信 → 初期設定）
- 旅行予約（フライト → ホテル → レンタカー）

---

## Choreography Pattern

各サービスがイベントを発行・購読し、自律的に連携する。

### Structure

```
Service A ──event──→ Service B ──event──→ Service C
    ↑                    ↑                    │
    └────comp event──────┴────comp event──────┘
```

### Template

```yaml
SAGA_CHOREOGRAPHY:
  name: "[SagaName]"
  services:
    - name: "[ServiceA]"
      listens_to:
        - event: "[TriggerEvent]"
          action: "[Process]"
          emits: "[SuccessEvent]"
          on_failure:
            emits: "[FailureEvent]"
      compensates_on:
        - event: "[CompensationTrigger]"
          action: "[RollbackAction]"
    - name: "[ServiceB]"
      listens_to:
        - event: "[ServiceA.SuccessEvent]"
          action: "[Process]"
          emits: "[SuccessEvent]"
  correlation:
    key: "saga_id"
    timeout: "30m"
    dead_letter:
      destination: "[DLQ]"
      alert: true
```

---

## Compensation Design Rules

### 1. Semantic Undo, Not Technical Undo

```yaml
# Good: ビジネス意味での取消
compensation:
  action: "cancel_reservation"  # 予約キャンセル
  side_effects:
    - "send_cancellation_email"
    - "release_inventory"

# Bad: DB操作の逆転
compensation:
  action: "DELETE FROM reservations WHERE id = ?"
```

### 2. Idempotent Compensations

```yaml
compensation:
  command: "cancel_payment"
  idempotency:
    check: "SELECT status FROM payments WHERE idempotency_key = ?"
    skip_if: "status IN ('cancelled', 'refunded')"
```

### 3. Timeout and Escalation

```yaml
compensation:
  command: "refund_payment"
  timeout: "30s"
  on_timeout:
    retry: 3
    escalate_to: "manual_intervention_queue"
    alert:
      channel: "#ops-alerts"
      severity: "high"
```

---

## Pattern Selection Decision Tree

```
分散トランザクションが必要？
├── No → 単一DBトランザクションで十分
└── Yes
    ├── 参加サービス数 <= 3？
    │   ├── Yes
    │   │   ├── サービス間の結合度を低く保ちたい？
    │   │   │   ├── Yes → Choreography
    │   │   │   └── No → Orchestration (シンプル)
    │   │   └──
    │   └── No (4+サービス)
    │       └── Orchestration を推奨
    ├── 全体の可視性が重要？
    │   ├── Yes → Orchestration
    │   └── No → Choreography
    ├── デバッグ容易性が重要？
    │   ├── Yes → Orchestration
    │   └── No → どちらでも可
    └── 単一障害点を避けたい？
        ├── Yes → Choreography
        └── No → Orchestration
```

---

## Error Handling Strategies

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| Retry | 一時的障害を再試行で解消 | Network timeout, 429 |
| Compensate | 成功済みステップを巻き戻し | Business logic failure |
| Pivot | 代替フローに切り替え | Primary path unavailable |
| Park | 保留して人手介入を待つ | Unrecoverable, needs decision |
| Ignore | 影響が軽微なため無視 | Non-critical side effects |

---

## Observability

```yaml
SAGA_OBSERVABILITY:
  tracing:
    correlation_id: "saga:{saga_id}"
    span_per_step: true
    propagation: "W3C Trace Context"
  metrics:
    - name: "saga_duration_seconds"
      type: histogram
      labels: [saga_name, status]
    - name: "saga_step_failures_total"
      type: counter
      labels: [saga_name, step_name, error_type]
    - name: "saga_compensations_total"
      type: counter
      labels: [saga_name, trigger_step]
  logging:
    level: "INFO"
    structured: true
    fields: [saga_id, step, status, duration]
```
