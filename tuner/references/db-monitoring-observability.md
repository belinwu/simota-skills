# Database Monitoring & Observability

> プロアクティブ DB 監視、pg_stat_statements 活用、アラート戦略、ダッシュボード設計

## 1. DB モニタリング 5 つの柱

| # | 柱 | 主要メトリクス | 監視ツール |
|---|---|-------------|---------|
| **MO-01** | **クエリパフォーマンス** | p50/p95/p99 レイテンシ、スロークエリ数、実行回数 | pg_stat_statements / Performance Schema |
| **MO-02** | **リソース使用率** | CPU、メモリ（heapUsed/shared_buffers）、ディスク I/O | Prometheus + node_exporter / pg_exporter |
| **MO-03** | **コネクション管理** | アクティブ/アイドル接続数、プール使用率、待機数 | pg_stat_activity / pgBouncer metrics |
| **MO-04** | **ロック・競合** | ロック待ち時間、デッドロック数、ロック競合率 | pg_stat_activity / pg_locks |
| **MO-05** | **メンテナンス状態** | Autovacuum 実行状況、テーブルブロート率、インデックスブロート | pg_stat_user_tables / pgstattuple |

---

## 2. pg_stat_statements vs pg_stat_monitor

| 機能 | pg_stat_statements | pg_stat_monitor |
|------|-------------------|-----------------|
| **データ収集** | 累積カウンター | 時間ベースバケット |
| **グルーピング** | 3 次元（user/db/query） | 5 次元（+ client IP, plan ID） |
| **クエリプラン** | 手動 EXPLAIN が必要 | 自動キャプチャ |
| **ヒストグラム** | 非サポート | ビルトイン分布分析 |
| **パラメータ** | 正規化（プレースホルダー） | 実パラメータ値を記録可能 |
| **CPU オーバーヘッド** | < 5% | < 5% |
| **推奨用途** | 長期トレンド分析 | 詳細デバッグ・リアルタイム分析 |

```
pg_stat_statements 推奨設定:
  shared_preload_libraries = 'pg_stat_statements'
  pg_stat_statements.max = 5000         # メモリ制約時は 1000-2000
  pg_stat_statements.track = 'top'      # ネストされた SQL 除外でオーバーヘッド削減
  track_activity_query_size = 4096      # 長いクエリの完全キャプチャ

定期メンテナンス:
  - 週次/月次で統計リセット: SELECT pg_stat_statements_reset();
  - track_utility = off でユーティリティコマンド除外
```

---

## 3. アラート閾値設計

| メトリクス | 警告 | クリティカル | アクション |
|-----------|------|------------|---------|
| **クエリ実行時間 p95** | > 500ms | > 2000ms | スロークエリ調査 |
| **コネクション使用率** | > 80% | > 95% | プールサイズ拡大 / リーク調査 |
| **CPU 使用率** | > 75% | > 90% | クエリ最適化 / スケールアップ |
| **メモリ使用率** | > 80% | > 95% | work_mem 調整 / キャッシュ見直し |
| **ディスク I/O レイテンシ** | > 10ms | > 50ms | インデックス追加 / ストレージ改善 |
| **デッドロック数** | > 0/hr | > 5/hr | トランザクション設計見直し |
| **レプリケーションラグ** | > 1s | > 10s | ネットワーク / レプリカ負荷確認 |
| **テーブルブロート率** | > 20% | > 50% | VACUUM FULL / pg_repack |
| **Autovacuum 遅延** | > 1hr | > 24hr | Autovacuum 設定チューニング |
| **未使用インデックス数** | > 5 | > 20 | 不要インデックス削除検討 |

---

## 4. プロアクティブ監視パターン

```
パターン 1: トップ N クエリ監視
  SELECT
    queryid,
    calls,
    round(total_exec_time::numeric, 2) AS total_ms,
    round(mean_exec_time::numeric, 2) AS mean_ms,
    round((100 * total_exec_time / sum(total_exec_time) OVER())::numeric, 2) AS pct,
    rows
  FROM pg_stat_statements
  ORDER BY total_exec_time DESC
  LIMIT 20;
  → 全体実行時間の上位 20 クエリを定期確認

パターン 2: I/O ボトルネック検出
  SELECT
    queryid,
    shared_blks_read,
    shared_blks_hit,
    round(100.0 * shared_blks_hit / NULLIF(shared_blks_hit + shared_blks_read, 0), 2) AS hit_ratio,
    temp_blks_written
  FROM pg_stat_statements
  WHERE shared_blks_read > 1000
  ORDER BY shared_blks_read DESC
  LIMIT 10;
  → キャッシュヒット率が低いクエリを特定

パターン 3: コネクションリーク検出
  SELECT
    state,
    count(*),
    max(now() - state_change) AS max_duration
  FROM pg_stat_activity
  WHERE datname = current_database()
  GROUP BY state
  ORDER BY count DESC;
  → idle 接続の数と最大持続時間を監視

パターン 4: テーブルブロート推定
  SELECT
    schemaname || '.' || relname AS table,
    pg_size_pretty(pg_total_relation_size(relid)) AS total_size,
    n_live_tup,
    n_dead_tup,
    round(100.0 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_pct,
    last_autovacuum
  FROM pg_stat_user_tables
  WHERE n_dead_tup > 10000
  ORDER BY n_dead_tup DESC
  LIMIT 20;
  → デッドタプル率の高いテーブルを特定

パターン 5: インデックス使用効率
  SELECT
    schemaname || '.' || relname AS table,
    indexrelname AS index,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size,
    idx_scan AS scans,
    idx_tup_read AS tuples_read,
    idx_tup_fetch AS tuples_fetched
  FROM pg_stat_user_indexes
  ORDER BY idx_scan ASC
  LIMIT 20;
  → 使用頻度の低いインデックスを特定
```

---

## 5. ダッシュボード設計

```
推奨ダッシュボード構成（Grafana）:

  Row 1: 概要パネル
    - クエリ実行レート（QPS）
    - アクティブコネクション数
    - キャッシュヒット率
    - レプリケーションラグ

  Row 2: クエリパフォーマンス
    - トップ 10 スロークエリ（テーブル）
    - クエリレイテンシ分布（ヒストグラム）
    - 時系列: p50/p95/p99 レイテンシ

  Row 3: リソース
    - CPU 使用率
    - メモリ使用率（shared_buffers ヒット率）
    - ディスク I/O（読み取り/書き込み IOPS）
    - WAL 生成量

  Row 4: メンテナンス
    - テーブル別ブロート率
    - Autovacuum 実行頻度
    - デッドロック発生数
    - 長時間トランザクション

ツールスタック:
  - メトリクス収集: Prometheus + pg_exporter
  - 可視化: Grafana 12.0
  - アラート: Grafana Alerting / PagerDuty
  - 計装: OpenTelemetry v1.27.0
```

---

## 6. Tuner との連携

```
Tuner での活用:
  1. Analyze フェーズで pg_stat_statements のトップ N クエリ確認
  2. Diagnose フェーズで I/O ボトルネック・ブロート検出
  3. Optimize フェーズで改善後のメトリクス監視設定
  4. Validate フェーズでダッシュボードでの before/after 追跡

品質ゲート:
  - pg_stat_statements 未有効化 → 有効化を推奨（MO-01）
  - アラート閾値未設定 → 基本アラートの設定を推奨
  - キャッシュヒット率 < 95% → shared_buffers / インデックス見直し
  - デッドタプル率 > 20% → Autovacuum 設定チューニング
  - 未使用インデックス > 5 → 削除検討リストとして報告
```

**Source:** [DasRoot: Database Observability Monitoring](https://dasroot.net/posts/2025/12/database-observability-monitoring/) · [Severalnines: pg_stat_monitor and pg_stat_statements](https://severalnines.com/blog/query-observability-and-performance-tuning-with-pg_stat_monitor-and-pg_stat_statements/) · [DrDroid: PostgreSQL Monitoring & Alerting Best Practices](https://drdroid.io/engineering-tools/postgresql-monitoring-alerting-best-practices) · [Sematext: PostgreSQL Monitoring Tools & Metrics](https://sematext.com/blog/postgresql-monitoring/)
