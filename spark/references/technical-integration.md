# Spark Technical Integration Patterns Reference

Builder/Sherpaとの密接な連携パターンガイド。

---

## SPARK_TO_BUILDER_HANDOFF (Sherpa bypass版)

シンプルな機能で直接Builderに渡す場合のフォーマット。

### When to Use Direct Builder Handoff

| Condition | Sherpa経由 | Builder直接 |
|-----------|------------|-------------|
| 複雑度 | 複数ステップ、依存関係あり | 単一機能、独立 |
| リスク | 高リスク、不確実性あり | 低リスク、明確な要件 |
| 既存パターン | 新パターン | 既存パターンの拡張 |
| 見積もり | 1日以上 | 数時間以内 |
| チーム調整 | 必要 | 不要 |

### Direct Builder Handoff Format

```markdown
## SPARK_TO_BUILDER_HANDOFF

**Feature**: [Feature name]
**Proposal Doc**: [Link to proposal file]
**Bypass Sherpa**: Yes (Reason: [Simple feature / Pattern exists / Low risk])

### Technical Specification

**Core Requirement**:
[One-sentence description of what to build]

**User Story**:
As a [persona], I want to [action] so that [benefit].

### Domain Model Requirements
...
```

---

## DDD Pattern Requirements

提案に含めるべきDDDパターン要件の指定方法。

### Pattern Selection Guide

```markdown
## DDD Pattern Recommendation

When specifying requirements, indicate the expected DDD pattern:

| Scenario | Recommended Pattern | Rationale |
|----------|---------------------|-----------|
| 一意のIDで識別される概念 | Entity | 状態変化しても同一性を維持 |
| IDなし、値で比較される概念 | Value Object | イミュータブル、交換可能 |
| 複数エンティティの整合性境界 | Aggregate Root | トランザクション境界を定義 |
| エンティティに属さないビジネスロジック | Domain Service | 複数集約を跨ぐ操作 |
| 外部システムとのインタラクション | Infrastructure Service | API、DB、メッセージング |
```

### Entity Requirements Template

```markdown
### Entity: [EntityName]

**Identity**:
- ID Type: [UUID / Sequential / Natural key]
- ID Generation: [Client / Server / External system]

**Properties**:
| Property | Type | Mutable? | Business Rule |
|----------|------|----------|---------------|
| [prop1] | [type] | [Yes/No] | [Rule if any] |
| [prop2] | [type] | [Yes/No] | [Rule if any] |

**State Transitions** (if applicable):
```
[Initial] → [State A] → [State B] → [Final]
     ↑          │
     └──────────┘ (rollback conditions)
```

**Invariants**:
- [Business rule that must always be true]
- [Business rule that must always be true]

**Methods Expected**:
| Method | Purpose | Side Effects |
|--------|---------|--------------|
| [method()] | [What it does] | [State change / Event] |
```

### Value Object Requirements Template

```markdown
### Value Object: [VOName]

**Purpose**: [Why this is a Value Object, not just a primitive]

**Properties**:
| Property | Type | Validation |
|----------|------|------------|
| [prop1] | [type] | [Pattern / Range / Enum] |

**Creation Validation**:
- [Validation rule 1]
- [Validation rule 2]

**Equality**:
- Compare by: [All properties / Specific subset]
...
```typescript
// Expected signature
static create(raw: RawInput): Result<[VOName], ValidationError>
```

**Use Cases**:
- Used in: [Entity A], [Entity B]
- Represents: [Business concept]
```

### Aggregate Root Requirements Template

```markdown
### Aggregate Root: [AggregateName]

**Root Entity**: [Entity name]

**Child Entities**:
| Entity | Relationship | Cascade |
|--------|--------------|---------|
| [Child A] | [1:N / 1:1] | [Create/Update/Delete rules] |
| [Child B] | [1:N / 1:1] | [Create/Update/Delete rules] |

**Aggregate Invariants**:
- [Cross-entity business rule]
- [Cross-entity business rule]

**Transaction Boundary**:
...
```

---

## API統合提案時の技術要件

外部API連携を含む機能提案での要件定義。

### API Integration Requirements Template

```markdown
## API Integration Requirements

**External API**: [API Name / Service]
**Purpose**: [Why we need this integration]

### Connection Requirements

**Authentication**:
- Type: [API Key / OAuth2 / Basic / JWT]
- Credential storage: [Environment variable / Secrets manager]
- Rotation: [Frequency if applicable]

**Base Configuration**:
```yaml
base_url: [https://api.example.com/v1]
timeout: [30s]
rate_limit: [100 requests/minute]
```

### Retry Strategy

| Error Type | Retry? | Strategy | Max Attempts |
|------------|--------|----------|--------------|
| 5xx (Server) | Yes | Exponential backoff | 3 |
| 429 (Rate limit) | Yes | Wait for Retry-After | 3 |
| 4xx (Client) | No | Fail immediately | 1 |
| Network timeout | Yes | Exponential backoff | 3 |
| Connection refused | Yes | Linear backoff | 2 |

**Backoff Configuration**:
```yaml
initial_delay: 1s
max_delay: 30s
multiplier: 2
jitter: 0.1
```

### Rate Limiting

**External API Limits**:
- Requests per second: [N]
- Requests per minute: [N]
- Requests per day: [N]

**Our Implementation**:
- Rate limiter type: [Token bucket / Sliding window]
- Queue behavior: [Wait / Reject]
- Burst capacity: [N]

### Error Handling

...
```yaml
failure_threshold: 5
reset_timeout: 60s
half_open_requests: 3
```

### Data Validation

**Request Validation**:
- Validate before sending: [Yes/No]
- Schema: [Zod schema name or link]

**Response Validation**:
- Validate on receive: [Yes/No]
- Handle unknown fields: [Ignore / Fail]
- Type coercion: [Allowed for dates, numbers]

### Fallback Strategy

| Scenario | Fallback |
...
```

---

## SHERPA_TO_SPARK_FEEDBACK

Sherpaからのフィードバックを受けて提案を調整するフォーマット。

### Feedback Trigger Conditions

| Feedback Type | Trigger | Spark Action |
|---------------|---------|--------------|
| Feasibility Concern | 技術的に困難 | スコープ調整または代替案 |
| Scope Too Large | 分解後も15分超えるステップ多数 | MVPに絞り込み |
| Dependency Issue | 外部依存がブロッカー | フェーズ分けまたは代替案 |
| Risk Escalation | 高リスクステップが多い | リスク軽減策を追加 |
| Resource Concern | 想定以上の工数 | 優先度再評価 |

### Sherpa → Spark Feedback Format

```markdown
## SHERPA_TO_SPARK_FEEDBACK

**Feature**: [Feature name from Spark proposal]
**Proposal Doc**: [Link]
**Feedback Type**: [Feasibility / Scope / Dependency / Risk / Resource]

### Breakdown Attempt Summary

**Total Steps Identified**: [N]
**Estimated Total Time**: [X hours]
**High Risk Steps**: [N] (threshold: 0-1 acceptable)

### Feasibility Concerns

| Concern | Affected Steps | Severity | Suggestion |
...
```

### Spark Response to Feedback

```markdown
## SPARK_ITERATION_ON_SHERPA_FEEDBACK

**Original Proposal**: [Link]
**Sherpa Feedback**: [Link or summary]
**Iteration**: v2

### Accepted Adjustments

| Sherpa Suggestion | Spark Decision | Rationale |
|-------------------|----------------|-----------|
| [Suggestion 1] | [Accept/Reject/Modify] | [Why] |
| [Suggestion 2] | [Accept/Reject/Modify] | [Why] |

### Revised Scope

...
```

---

## Feasibility Concerns → Scope Adjustment

実現可能性の懸念に基づくスコープ調整パターン。

### Adjustment Decision Matrix

| Concern Type | Impact | Preferred Adjustment |
|--------------|--------|---------------------|
| 技術的に不可能 | Critical | 機能削除 or 代替アプローチ |
| 工数が予算超過 | High | Phase分割 or MVP縮小 |
| 外部依存がブロック | High | Mock化 or 非同期対応 |
| 品質リスク | Medium | 追加テスト要件 or 段階リリース |
| パフォーマンス懸念 | Medium | 最適化要件追加 or 制限追加 |

### Scope Adjustment Template

```markdown
## SCOPE_ADJUSTMENT

**Original Feature**: [Feature name]
**Adjustment Reason**: [Feasibility concern from Sherpa]

### Impact Analysis

**Original Scope Impact**:
| Metric | Original | Adjusted | Change |
|--------|----------|----------|--------|
| User value | [High/Med/Low] | [High/Med/Low] | [+/-/=] |
| Effort | [X hours] | [Y hours] | [-Z%] |
| Risk | [High/Med/Low] | [High/Med/Low] | [Reduced/Same] |

### Adjustment Options
...
```

---

## Integration Workflow

### Full Flow: Spark → Sherpa → Builder

```
Spark Proposal Created
        │
        ├── Complex? ───────────────────────────────┐
        │      │                                     │
        │      ↓                                     │
        │   SPARK_TO_SHERPA_HANDOFF                  │
        │      │                                     │
        │      ↓                                     │
        │   Sherpa Breakdown                         │
        │      │                                     │
        │      ├── OK ────────→ SHERPA_TO_BUILDER   │
        │      │                      │              │
        │      │                      ↓              │
        │      │                   Builder           │
        │      │                      │              │
...
```

### Handoff Checklists

**Before Sherpa Handoff**:
- [ ] User story is complete and clear
- [ ] Acceptance criteria are testable
- [ ] DDD patterns are suggested (not mandated)
- [ ] API requirements are specified if applicable
- [ ] Priority is clear

**Before Builder Direct Handoff**:
- [ ] Feature is simple (< 4 hours estimate)
- [ ] Existing patterns can be followed
- [ ] No external dependencies pending
- [ ] Low risk
- [ ] All technical requirements specified

**After Sherpa Feedback**:
- [ ] Review all concerns
- [ ] Decide on adjustment approach
- [ ] Update proposal document
- [ ] Communicate scope changes to stakeholders
- [ ] Re-submit for breakdown
