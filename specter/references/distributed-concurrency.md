# Distributed Concurrency Patterns

分散システム固有の並行性問題パターンカタログ。

## 1. Distributed Lock Issues

### Pattern: Lock Contention Cascade
- 症状: レイテンシスパイク、タイムアウト増加
- 原因: Redis/ZooKeeper 分散ロックの競合がカスケード
- 検出: ロック待機時間メトリクス、ロック取得失敗率の急増
- Risk Score 調整: Impact +2 (cascading), Recovery +1 (requires coordination)

### Pattern: Split-Brain Lock
- 症状: 同一リソースへの重複書き込み
- 原因: ネットワーク分断でロックマネージャーが分裂
- 検出: データ不整合、重複処理ログ
- Risk Score 調整: DataRisk +3 (data corruption)

### Pattern: Lock Expiry Race
- 症状: 間欠的なデータ破損
- 原因: 処理時間がロック TTL を超過し、他プロセスがロック取得
- 検出: ロック TTL vs 処理時間のヒストグラム比較

## 2. Eventual Consistency Conflicts

### Pattern: Read-Your-Write Violation
- 症状: ユーザーが更新後に古いデータを見る
- 原因: リードレプリカの同期遅延
- 検出: write timestamp vs read result timestamp の差異

### Pattern: Conflict Resolution Failure
- 症状: データ消失（last-write-wins で先行書き込みが消える）
- 原因: CRDT や vector clock なしの楽観的並行制御
- 検出: バージョン履歴での「消失」パターン
- Risk Score 調整: DataRisk +3

### Pattern: Saga Compensation Failure
- 症状: 部分的にコミットされたトランザクション
- 原因: 補償処理の失敗（冪等性不足、順序依存）
- 検出: Saga 状態マシンの COMPENSATING 状態の長期滞留
- Risk Score 調整: Impact +2, Recovery +2

## 3. Microservice Race Conditions

### Pattern: Event Ordering Violation
- 症状: 処理結果が実行順序に依存して不正
- 原因: メッセージキュー内のパーティション間順序保証なし
- 検出: イベント timestamp とローカルクロックの不整合

### Pattern: Thundering Herd
- 症状: キャッシュ失効時のバックエンド過負荷
- 原因: TTL 同時失効で全リクエストがオリジンに殺到
- 検出: キャッシュミス率の周期的スパイク

### Pattern: Retry Storm
- 症状: 障害時のトラフィック増幅
- 原因: 指数バックオフなし/ジッターなしのリトライ
- 検出: 4xx/5xx エラー率 × リクエスト数の相関

## 4. Container/Kubernetes Resource Issues

### Pattern: OOMKill Loop
- 症状: Pod の繰り返し再起動
- 原因: メモリ制限設定ミス or メモリリーク
- 検出: `kubectl get events --field-selector reason=OOMKilling`
- 調査: `kubectl top pod` の時系列 + Rewind での変更特定

### Pattern: CPU Throttling Latency
- 症状: P99 レイテンシの定期的スパイク
- 原因: CPU limit によるスロットリング
- 検出: `container_cpu_cfs_throttled_periods_total` メトリクス

### Pattern: Ephemeral Storage Exhaustion
- 症状: Pod eviction
- 原因: ログ/tmp ファイルの累積
- 検出: `ephemeral-storage` usage trending

## 5. WebAssembly/Edge Computing Concurrency

### Pattern: SharedArrayBuffer Race
- 症状: Worker 間の共有メモリで不正値
- 原因: Atomics API 未使用のまま SharedArrayBuffer にアクセス
- 検出: 非決定的な計算結果のバラつき

### Pattern: Edge Worker Connection Limit
- 症状: 間欠的なタイムアウト
- 原因: Edge runtime の同時接続数制限（通常 6-10）
- 検出: 429 レスポンスのスパイク、接続プール枯渇ログ

## Rewind Escalation Criteria

以下に該当する場合、`SPECTER_TO_REWIND_HANDOFF` (`_common/INVESTIGATION_ESCALATION.md`):

- リーク/レース発見だが開始時期が不明
- 特定のデプロイ以降に問題が顕在化した形跡
- 設定変更（環境変数、feature flag）との相関が疑われる
