# Resilience & Cost Optimization

> 3層レジリエンス戦略、Circuit Breaker、Saga パターン、モデルティアリング、トークンコスト最適化

## 1. 3層レジリエンス戦略

### 層1: Retry（短期回復）

| 戦略 | アプローチ | 推奨場面 |
|------|----------|---------|
| 即時リトライ | 即座に再試行 | ほぼ非推奨 |
| 固定インターバル | 一定待機 | 回復時間が既知の場合 |
| Exponential Backoff | 待機時間を倍増 (1s→2s→4s) | 大半のネットワーク呼び出し |
| **Exponential + Jitter** | **バックオフにランダム性追加** | **本番環境のゴールドスタンダード** |

**重要ルール**: 冪等でない操作はリトライしない。

### 層2: Fallback（プランB）

- プライマリ過負荷時にセカンダリへ切り替え
- キャッシュデータ提供、機能簡略化、非本質機能の無効化
- **注意**: フォールバックロジックは置き換える操作より単純で信頼性が高くなければならない

### 層3: Circuit Breaker（予防的防止）

```
Closed（正常）→ Open（遮断: 閾値超過）→ Half-Open（回復テスト中）
```

**チューニングパラメータ:**

| パラメータ | 説明 | 推奨値 |
|-----------|------|--------|
| 失敗閾値 | Open に遷移する条件 | 10秒間で50%エラー |
| リセットタイムアウト | 次のプローブまでの時間 | 30-60秒 |
| 最小リクエスト数 | 孤立した失敗での誤トリップ防止 | 5-10 |

---

## 2. AIエージェント向けレジリエンス拡張

### エージェント特有の失敗カテゴリ

| カテゴリ | 説明 | 従来のサービスとの違い |
|---------|------|---------------------|
| ネットワーク/HTTPエラー | 4xx, 5xx | 同じ |
| タイムアウト | 応答遅延 | LLM は応答時間が長い |
| レート制限 | API制限 | 並列エージェントで急増 |
| **セマンティック失敗** | ハルシネーション（200 OK） | **AIエージェント固有** |
| ツール実行失敗 | ツール呼び出しエラー | エージェント固有 |

### DEGRADED状態の導入

```
Closed → Degraded（部分的能力）→ Open（全停止）
```

従来の Closed → Open の二値ではなく、中間状態で部分的な処理を継続。

### Rally への適用

| 状態 | Rally での挙動 |
|------|---------------|
| Closed | 通常のチーム実行 |
| Degraded | チームサイズ縮小、高リスクタスクのみ人間承認 |
| Open | チーム実行停止、単一セッションにフォールバック |

---

## 3. Saga パターン（分散トランザクション）

マルチエージェント実行で途中失敗した場合の補償アクション:

```
Step 1: Teammate A 実行 → 補償: A の成果物をリバート
Step 2: Teammate B 実行 → 補償: B の成果物をリバート
Step 3: Teammate C 実行 → 補償: C の成果物をリバート

失敗時: 逆順で補償アクションを実行
```

### Rally での Saga 適用

| フェーズ | 正常フロー | 補償アクション |
|---------|-----------|---------------|
| SPAWN | TeamCreate + Task | shutdown_request + TeamDelete |
| ASSIGN | TaskCreate | TaskUpdate (deleted) |
| MONITOR | TaskList check | stalled → replacement spawn |
| SYNTHESIZE | 結果統合 | conflict → 手動マージエスカレーション |

---

## 4. Bulkhead 分離

異なるアクティビティタイプを別々のタスクキューと専用ワーカープールに割り当て。一方の失敗が他に伝播しない。

```
┌─ Pool A: Frontend tasks ─┐
│  Teammate 1, Teammate 2  │
└──────────────────────────┘
┌─ Pool B: Backend tasks ──┐    ← 独立した障害ドメイン
│  Teammate 3, Teammate 4  │
└──────────────────────────┘
```

---

## 5. コスト構造と最適化

### トークンコスト構造

| コスト要素 | 単価（フラッグシップ） | 影響 |
|-----------|---------------------|------|
| 入力トークン | $2-3 / 100万 | 中 |
| 出力トークン | $10-15 / 100万 | **高（入力の4-5倍）** |
| 出力遅延 | 1トークンあたり数ms | 累積的 |

**実務的含意**: 出力トークンの削減がレイテンシとコストの両方に最も影響。

### モデルティアリング（最高ROI施策）

| タスク複雑度 | 推奨モデル | コスト | Rally での適用 |
|------------|----------|-------|---------------|
| 単純（分類・抽出） | haiku | 最低 | 調査タスク |
| 中程度 | sonnet | 中 | 一般実装（デフォルト） |
| 複雑（推論・設計） | opus | 最高 | 設計タスク |

**コスト差: haiku vs opus で 15-50倍**（平均16倍）

### ROIが高いコスト削減手法

| # | 手法 | 削減効果 | Rally での適用 |
|---|------|---------|---------------|
| 1 | **モデルティアリング** | 15-50倍 | タスク複雑度別モデル選択 |
| 2 | **コンテキスト最適化** | 20-40% | スポーンプロンプトの最適化 |
| 3 | **チームサイズ最小化** | 線形削減 | 2-4人を厳守 |
| 4 | **早期終了** | 可変 | stall 検出 → 早期 shutdown |
| 5 | **shared_read 活用** | 重複排除 | 共通ファイルの読み込み統合 |

---

## 6. 並列実行のコスト管理

### コスト見積もり

| 項目 | 計算式 |
|------|--------|
| 1チームメイトあたりのコスト | `(input_tokens × input_rate + output_tokens × output_rate) × turns` |
| チーム総コスト | `Σ teammate_costs + lead_cost` |
| **安全マージン** | **初期見積もりの 1.5倍を予算確保** |

### コスト上限の設定

```
Team Budget = max_teammates × estimated_cost_per_teammate × safety_margin

例: 4 teammates × $2.00 × 1.5 = $12.00 上限
```

### コスト監視ポイント

| チェックポイント | アクション |
|---------------|----------|
| チーム開始時 | 予算上限を設定 |
| 50% 消費時 | 進捗率を確認、乖離なら調整 |
| 80% 消費時 | 残タスクの優先度を再評価 |
| 100% 到達時 | 強制 shutdown + 残タスクを報告 |

---

## 7. Work Stealing パターン

「プル型」分散パターン: ワーカーが容量の余裕ができたときにキューからタスクを取得。

### Rally での適用可能性

```
Central Task Queue ← Teammates pull tasks when idle
                   ← Idle teammate "steals" from busy teammate's queue
```

**適用条件:**
- 実行時間が長いタスク（短いタスクには向かない）
- スループット優先（レイテンシ優先ではない）

**注意**: 現在の Rally は中央割り当て方式（push型）。Work Stealing への移行は HARMONIZE データで適性を判断。

---

## 8. エラーリカバリ判断マトリクス

| エラータイプ | 初回対応 | 2回目 | 3回目 | 最終手段 |
|------------|---------|-------|-------|---------|
| Teammate hang | DM nudge | scope-reduced retry | replacement spawn | shutdown + report |
| Task failure | context-augmented retry | scope-reduced retry | skip + report | manual escalation |
| Ownership conflict | re-partition | sequentialize | interface separation | manual merge |
| All teammates fail | TeamDelete | single-session fallback | — | report alternatives |

**Source:** [Portkey - Retries, Fallbacks, Circuit Breakers in LLM Apps](https://portkey.ai/blog/retries-fallbacks-and-circuit-breakers-in-llm-apps/) · [Temporal - Error Handling in Distributed Systems](https://temporal.io/blog/error-handling-in-distributed-systems) · [Circuit Breaker Pattern 2025 (Shadecoder)](https://www.shadecoder.com/topics/the-circuit-breaker-pattern-a-comprehensive-guide-for-2025) · [Redis - LLM Token Optimization](https://redis.io/blog/llm-token-optimization-speed-up-apps/) · [Convex - Work Stealing](https://stack.convex.dev/work-stealing)
