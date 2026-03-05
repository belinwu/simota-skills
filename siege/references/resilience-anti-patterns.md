# Resilience Anti-Patterns & SLO-Based Testing

> レジリエンスアンチパターン（Retry Storm/Thundering Herd/Timeout Cascade）、Error Budget、SLO ベーステスト

## 1. レジリエンス 7 大アンチパターン

### AP-01: Retry Storm（リトライストーム）

```
定義: 失敗リクエストの過剰リトライがバックエンドに追加負荷を生む
症状: 障害時にトラフィックが 2-10 倍に急増、回復不能
原因: リトライ間隔なし、リトライ上限なし、バックオフなし

Bad:
  失敗 → 即リトライ → 即リトライ → 即リトライ ...
  (100 クライアント × 無制限リトライ = バックエンド崩壊)

Good:
  失敗 → 1s 待機 → 2s 待機 → 4s 待機 → Circuit Open
  (Exponential Backoff + Circuit Breaker 連携)

Retry Budget（リトライ予算）:
  - リトライによる追加負荷を通常トラフィックの 10-20% に制限
  - 例: 通常 1000 RPS → リトライ込みで最大 1200 RPS
  - 予算超過でリトライ停止 → Fallback 応答
```

### AP-02: Thundering Herd（雷鳴の群れ）

```
定義: 障害復旧時に全クライアントが一斉にリクエスト再開
症状: 復旧直後に再障害、回復-再障害の振動
原因: 全クライアントが同一タイミングでリトライ

対策:
  1. Jitter（ランダム遅延）: リトライ時間 ± 50% のランダム化
  2. Token Bucket: リトライレートを制限
  3. Staggered Recovery: 段階的なトラフィック復旧
  4. Client-side Circuit Breaker: 個別に回復判定

計算例:
  Base delay: 2s
  Full jitter: random(0, 2s)
  Equal jitter: 1s + random(0, 1s)
  Decorrelated jitter: min(cap, random(base, prev_delay * 3))
```

### AP-03: Timeout Cascade（タイムアウトカスケード）

```
定義: マイクロサービスチェーンでタイムアウトが連鎖
症状: 下流のタイムアウトが上流に伝播し全体がスローダウン
原因: 各サービスのタイムアウト値が不整合

Bad (全サービス 30s タイムアウト):
  Client → A(30s) → B(30s) → C(30s) → DB
  最悪: Client は 90s 待つ

Good (上流 > 下流の原則):
  Client → A(10s) → B(5s) → C(2s) → DB
  上流のタイムアウト > 下流のタイムアウト + 処理時間
  Client は最大 10s で応答を得る
```

### AP-04: Bulkhead Bypass（バルクヘッド迂回）

```
定義: 障害分離のバルクヘッドを共有リソースが無効化
症状: 1 つの依存障害が全サービスに波及
原因: 共有スレッドプール/接続プール/メモリ

Bad:
  全依存サービスが単一 HTTP クライアントプールを共有
  → 1 サービスの遅延で全プール枯渇

Good:
  依存サービスごとに独立したプール
  + 各プールにサイズ上限 + タイムアウト設定
```

### AP-05: Fallback Avalanche（フォールバック雪崩）

```
定義: フォールバック処理自体がリソースを消費し障害を悪化
症状: プライマリ障害 → フォールバック → フォールバックも障害
原因: フォールバックが本来パスと同じリソースに依存

対策:
  - フォールバックは独立リソースを使用
  - 静的フォールバック（キャッシュ済みデータ）を優先
  - フォールバックにも Circuit Breaker を設定
  - 最終手段: Graceful Degradation（機能制限で応答）
```

### AP-06: Health Check Lie（ヘルスチェックの嘘）

```
定義: ヘルスチェックが実際のサービス状態を反映しない
症状: ヘルスチェック OK なのにリクエスト処理できない
原因: 浅いヘルスチェック（プロセス alive のみ）

Good (Deep Health Check):
  /health/ready:
    - DB 接続プール: active < max × 80%
    - Redis 応答: < 100ms
    - ディスク空き: > 10%
    - 依存サービス: 主要エンドポイントに ping

  /health/live:
    - プロセス alive（簡易チェック、K8s liveness 用）
```

### AP-07: Configuration Drift（設定ドリフト）

```
定義: 環境間でレジリエンス設定が異なる
症状: テスト環境で動作するがプロダクションで障害
原因: タイムアウト/リトライ/プールサイズが環境ごとに異なる

対策:
  - レジリエンス設定を環境変数/Config Map で一元管理
  - 設定値のテスト（単体テストで設定検証）
  - 本番同等の設定でステージングテスト
```

---

## 2. Error Budget と SLO ベーステスト

### Error Budget の基本

```
Error Budget = 1 - SLO

例: SLO 99.9% → Error Budget 0.1%
  月間リクエスト 1,000,000 件 → 1,000 件のエラーまで許容
  月間 43,200 分 → 43.2 分のダウンタイムまで許容

Budget 消費率による行動:
  0-50% 消費: 通常リリース速度を維持
  50-75% 消費: インシデントレビュー、パフォーマンス調査
  75-100% 消費: リリース速度を低下、安定性に注力
  100% 超過: リリース凍結、全力で信頼性改善

単一インシデントで 20% 超消費:
  → 必須ポストモーテム + P0 アクションアイテム
```

### SLO ベーステスト戦略

| テストタイプ | SLO 連携 | 実施タイミング |
|------------|---------|--------------|
| **SLO Validation Test** | 目標 RPS で SLO 達成を検証 | リリース前ゲート |
| **Error Budget Stress** | Error Budget ギリギリまで負荷を増加 | 月次/四半期 |
| **Degradation Test** | SLO 違反時の Graceful Degradation 検証 | リリース前 |
| **Recovery Test** | SLO 違反からの回復時間（MTTR）測定 | Game Day |
| **Budget Burn Rate** | 障害シナリオでの Budget 消費速度を測定 | カオス実験 |

### SLI/SLO/SLA 階層

```
SLA (Service Level Agreement):
  → ビジネス契約（違反でペナルティ）
  → 例: 月間可用性 99.95%

SLO (Service Level Objective):
  → 内部目標（SLA より厳しく設定）
  → 例: 月間可用性 99.99%（SLA + 0.04% マージン）

SLI (Service Level Indicator):
  → 実測メトリクス
  → 例: 成功リクエスト数 / 総リクエスト数

Siege の検証対象:
  SLI の測定 → SLO 達成の検証 → Error Budget 消費の追跡
```

---

## 3. レジリエンスパターンの組み合わせ

### 推奨パターンチェーン

```
Client Request
  → Rate Limiter (過負荷保護)
    → Timeout (応答時間制限)
      → Retry + Backoff + Jitter (一時的障害回復)
        → Circuit Breaker (持続的障害検出)
          → Bulkhead (障害分離)
            → Fallback (代替応答)

組み合わせルール:
  1. Retry は Circuit Breaker の内側に配置
  2. Retry 回数は Circuit Breaker の閾値に加算
  3. Timeout は Retry 全体をカバー（個別 + 合計）
  4. Bulkhead は依存サービスごとに独立
  5. Fallback は最外側で最終防衛
```

### 検証マトリクス

| パターン | 正常時 | 一時障害 | 持続障害 | 復旧時 |
|---------|--------|---------|---------|--------|
| **Retry** | 不発動 | 成功まで再試行 | Budget 超過で停止 | 正常に戻る |
| **Circuit Breaker** | CLOSED | CLOSED (閾値以下) | OPEN → HALF-OPEN | CLOSED に戻る |
| **Bulkhead** | 通常プール使用 | 障害プールのみ影響 | 障害プール拒否 | プール回復 |
| **Timeout** | 設定時間内応答 | リトライ間に発動 | 即座にフォールバック | 正常応答 |
| **Fallback** | 不発動 | 不発動 | 代替応答 | 不発動 |

---

## 4. Siege との連携

```
Siege の RESILIENCE モードでの活用:
  1. 7 アンチパターンをチェックリストとして検証
  2. Error Budget 消費を負荷テスト結果に統合
  3. パターンチェーンの各コンポーネントを個別 + 統合テスト
  4. 障害注入 → 回復 → 再障害のサイクルを自動検証

Beacon へのハンドオフ:
  - SLO/SLI 定義の策定支援
  - Error Budget ポリシーの設計
  - ダッシュボード要件の提供
```

**Source:** [Azure: Retry Storm Antipattern](https://learn.microsoft.com/en-us/azure/architecture/antipatterns/retry-storm/) · [Temporal: Error Handling in Distributed Systems](https://temporal.io/blog/error-handling-in-distributed-systems) · [Backbase: Resilient Microservices](https://engineering.backbase.com/2024/06/28/resilient-microservices/) · [ThinhDA: Retries Without Thundering Herds](https://thinhdanggroup.github.io/retry-without-thundering-herds/) · [Google SRE: Error Budget Policy](https://sre.google/workbook/error-budget-policy/) · [Nobl9: Error Budgets Guide](https://www.nobl9.com/resources/a-complete-guide-to-error-budgets-setting-up-slos-slis-and-slas-to-maintain-reliability)
