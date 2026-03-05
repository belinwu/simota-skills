# PostgreSQL 17 Performance Features

> PG 17 のクエリ最適化改善、インデックス強化、Vacuum 改善、バルクロード高速化

## 1. クエリ最適化の主要改善

| 改善項目 | PG 16 | PG 17 | 改善率 | 詳細 |
|---------|-------|-------|--------|------|
| **Streaming I/O** | 単一バッファ読み込み | ベクタ I/O（複数バッファ一括） | ~27% 高速化 | Seq Scan: 6.6s → 4.8s |
| **B-tree IN 句最適化** | 値ごとに個別インデックススキャン | 同一リーフページから複数値取得 | ~10% 高速化 | 2 回 → 1 回のスキャン |
| **相関サブクエリ → JOIN 変換** | 相関 IN サブクエリを繰り返し実行 | 自動的に JOIN に変換 | ~14,000x 高速化 | 100s → 7ms |
| **UNION 最適化** | ソート後マージ | Merge Append でソートストリーム結合 | ~15% 高速化 | 1.3s → 1.1s |
| **CTE 統計伝播** | Materialized CTE の統計が外部クエリに不可視 | カラム統計を外部クエリに伝播 | ~2x 高速化 | 不要ソートの排除 |
| **IS NULL 最適化** | NOT NULL カラムでも IS NULL チェック実行 | NOT NULL 制約を認識して省略 | ~150,000x | 2,151ms → 0.014ms |

---

## 2. Vacuum 改善

```
PG 17 の Vacuum 最適化:

  メモリ管理の刷新:
    - Vacuum プロセスのメモリフットプリントを最大 20 倍削減
    - 大規模テーブルの Vacuum が安定化
    - 高並行性環境での Vacuum パフォーマンス向上

  実務への影響:
    - Autovacuum のリソース消費が大幅減少
    - テーブルブロートの蓄積が抑制されやすく
    - shared_buffers への影響が軽減

  推奨設定（PG 17）:
    autovacuum_vacuum_cost_delay = 2ms  (デフォルト: 2ms, 以前: 20ms)
    autovacuum_vacuum_cost_limit = 200
    maintenance_work_mem = 256MB - 1GB  (テーブルサイズに応じて)
```

---

## 3. バルクロード・エクスポート

```
COPY コマンドの高速化:
  - 大きな行の COPY で最大 2x 高速化
  - ソース/宛先のエンコーディング一致時に最適化
  - バルク INSERT のパフォーマンスも改善

実務への活用:
  - CSV インポート: COPY FROM で 2 倍速
  - データエクスポート: COPY TO で大幅高速化
  - ETL パイプラインのスループット向上
```

---

## 4. インデックス関連の改善

```
B-tree インデックス:
  - IN リスト / ANY 条件での効率的なスキャン
  - 同一リーフページ内の複数値を 1 回のスキャンで取得
  - CPU とバッファページの競合を軽減

並列クエリ:
  - Sequential Scan の並列化が効率化
  - テーブルブロックを範囲に分割し、ワーカープロセス間で共有
  - ワーカーが割り当て範囲完了後に追加ブロックをリクエスト

JSON サポート:
  - 新規 JSON_TABLE 関数: JSON → リレーショナルテーブル直接変換
  - SQL/JSON 標準準拠の SQL_JSON_ITEM_CANNOT_BE_CAST エラー処理
```

---

## 5. PG 17 活用のための推奨設定

| パラメータ | 推奨値 | 理由 |
|-----------|--------|------|
| `shared_buffers` | RAM の 25% | 変更なし（従来通り） |
| `effective_cache_size` | RAM の 75% | 変更なし |
| `work_mem` | 64MB-256MB | CTE 統計伝播の恩恵を受けやすく |
| `maintenance_work_mem` | 256MB-1GB | Vacuum 改善を最大化 |
| `random_page_cost` | 1.1 (SSD) | 変更なし |
| `jit` | on | 複雑クエリで JIT コンパイル有効化 |
| `max_parallel_workers_per_gather` | 2-4 | 並列スキャン改善の恩恵 |
| `huge_pages` | try | 大規模 shared_buffers で TLB ミス削減 |

---

## 6. PG 17 アップグレード時の注意点

```
互換性:
  - pg_upgrade でインプレースアップグレード可能
  - 一部の実行計画が変わる可能性（プランナー改善のため）
  - PG 16 → 17 で相関サブクエリの自動 JOIN 変換により
    一部クエリの実行計画が劇的に変化する可能性

テスト推奨事項:
  1. 主要クエリの EXPLAIN ANALYZE を PG 16/17 で比較
  2. pg_stat_statements でトップ 20 クエリの実行時間比較
  3. Vacuum のメモリ使用量モニタリング
  4. COPY 操作のスループット比較

移行後のチェック:
  - ANALYZE を全テーブルに実行（統計情報の更新）
  - pg_stat_statements をリセット（ベースライン再設定）
  - Autovacuum パラメータの見直し（メモリ効率改善のため）
```

---

## 7. Tuner との連携

```
Tuner での活用:
  1. Analyze フェーズで PG 17 の新プランナー動作を確認
  2. Diagnose フェーズで相関サブクエリの自動 JOIN 変換を検証
  3. Optimize フェーズで IN 句最適化・CTE 改善を活用
  4. Validate フェーズで PG 16 → 17 の before/after 比較

品質ゲート:
  - 相関 IN サブクエリ → PG 17 で自動最適化されるか確認
  - COPY 操作 → PG 17 の高速化を計測
  - Vacuum → メモリ使用量の削減を確認
  - IS NULL on NOT NULL カラム → PG 17 で自動最適化
```

**Source:** [Microsoft: Postgres 17 Query Performance Improvements](https://techcommunity.microsoft.com/blog/adforpostgresql/postgres-17-query-performance-improvements/4284693) · [pgEdge: PostgreSQL 17 Performance](https://www.pgedge.com/blog/postgresql-17-a-major-step-forward-in-performance-logical-replication-and-more) · [PostgreSQL.org: Release Notes 17](https://www.postgresql.org/docs/release/17.0/) · [ScaleGrid: PostgreSQL 17 New Features](https://scalegrid.io/blog/postgresql-17-new-features/)
