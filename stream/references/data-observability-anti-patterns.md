# Data Observability Anti-Patterns

> データ品質監視の失敗パターン、可観測性の罠、アラート疲れと検出漏れ

## 1. データ可観測性 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **DO-01** | **Test-Only Quality（テストのみ品質管理）** | 事前定義テストだけに依存 | 予期しない問題が検出不能、テスト数が無限増殖、スケールしない | テスト + 統計的異常検出の併用、ML ベース自動モニタリング |
| **DO-02** | **Alert Fatigue（アラート疲れ）** | 閾値が狭すぎて大量のアラート | チームがアラートを無視、重要な問題の見逃し、信頼喪失 | 動的閾値（統計ベース）、重要度分類、アラートのグルーピング |
| **DO-03** | **Freshness Blindness（鮮度盲目）** | パイプライン成功 = データ最新と誤認 | パイプラインは成功だがデータは昨日のまま、ソース障害の検出遅延 | max event timestamp 監視、ソース鮮度チェック（dbt source freshness） |
| **DO-04** | **Schema Drift Ignorance（スキーマ漂流無視）** | ソーススキーマ変更の検出なし | カラム追加/削除/型変更でパイプライン破損、サイレントなデータ損失 | スキーマ変更自動検出、Data Contract（スキーマ契約）、アラート |
| **DO-05** | **Volume Anomaly Gap（ボリューム異常の見逃し）** | 行カウントの監視なし | 0行ロード/10倍ロードに気づかない、重複/欠落の検出遅延 | 行カウントの統計的モニタリング、前日/前週比較、異常検出 |
| **DO-06** | **No Lineage（リネージ不在）** | データの流れが追跡不能 | 障害時の影響範囲が不明、根本原因分析に数時間、変更の影響予測不能 | カラムレベルリネージ、自動生成（dbt docs）、可視化ダッシュボード |
| **DO-07** | **Siloed Observability（サイロ化された可観測性）** | パイプライン/DWH/BI が個別に監視 | 端から端の品質が不明、問題の責任があいまい、修復に複数チーム必要 | 統合可観測性プラットフォーム、ソースから消費までの一貫した監視 |

---

## 2. データ品質管理の進化

```
3 つのアプローチと限界:

  Level 1 — Data Testing（テスト）:
    手法: 事前定義ルール（unique, not_null, range）
    ツール: dbt tests, Great Expectations
    限界:
      ❌ 知っている問題しか検出できない
      ❌ テーブル数が増えるとスケールしない
      ❌ 障害 vs データ問題の区別不能
    適用: 既知のビジネスルール、PK/FK 制約

  Level 2 — Data Monitoring（モニタリング）:
    手法: 閾値ベース or ML ベースの異常検出
    ツール: Monte Carlo, Elementary, Soda
    限界:
      ❌ 高コンピュートコスト（全データスキャン）
      ❌ 閾値設定に時間がかかる
      ❌ コンテキストなしのアラート → Alert Fatigue
    適用: ボリューム監視、分布シフト検出

  Level 3 — Data Observability（可観測性）:
    手法: テスト + モニタリング + リネージ + 根本原因分析
    ツール: Monte Carlo, Atlan, SYNQ, Dagster+
    強み:
      ✅ 予期しない問題も検出
      ✅ 根本原因まで自動追跡
      ✅ 影響範囲の即座把握
      ✅ 修復アクションの提案
    適用: 成熟したデータチーム、50+ パイプライン

  推奨:
    → Level 1 は全チーム必須（dbt tests）
    → Level 2 はパイプライン 10+ で導入
    → Level 3 はパイプライン 50+ or チーム 5+ で導入
```

---

## 3. 5 つの柱（Five Pillars）の実装

```
Pillar 1 — Freshness（鮮度）:
  監視対象: max(event_timestamp), max(loaded_at)
  閾値: 期待される更新間隔の 2-3 倍
  ツール: dbt source freshness, カスタムクエリ
  例: 日次パイプライン → 36h 以上古いとアラート

Pillar 2 — Volume（ボリューム）:
  監視対象: row_count, byte_size
  閾値: 過去 7 日の平均 ± 3σ（標準偏差）
  ツール: カスタム SQL + メトリクスストア
  例: 通常 10K 行/日 → 0 行 or 100K 行でアラート

Pillar 3 — Distribution（分布）:
  監視対象: NULL 率, 値の分布, 統計量
  閾値: ベースラインからの偏差
  ツール: Great Expectations, Monte Carlo
  例: NULL 率が 0.1% → 5% に急増でアラート

Pillar 4 — Schema（スキーマ）:
  監視対象: カラム名, データ型, カラム数
  検出: カラム追加/削除/型変更
  ツール: dbt schema tests, カスタムマクロ
  例: 予期しないカラム削除を即座に検出

Pillar 5 — Lineage（リネージ）:
  監視対象: 上流→下流の依存関係
  活用: 障害影響範囲の特定、変更の影響分析
  ツール: dbt docs, Atlan, DataHub
  例: ソーステーブル変更 → 影響を受ける全モデルを特定
```

---

## 4. Data Contract パターン

```
データ契約の概念:

  問題:
    → プロデューサー（ソースシステム）が勝手にスキーマ変更
    → コンシューマー（パイプライン）が予告なしに破損
    → 「誰が何を保証するか」が不明確

  Data Contract の構成要素:
    □ スキーマ定義（カラム、型、NULL 許可）
    □ 品質保証（鮮度 SLA、ボリューム範囲）
    □ セマンティクス（カラムの意味、ビジネス定義）
    □ オーナーシップ（プロデューサー/コンシューマーの責務）
    □ 変更管理（後方互換ルール、通知プロセス）

  実装パターン:

    パターン A — Schema Registry:
      → Avro/Protobuf スキーマの中央管理
      → 後方互換チェックの自動化
      → ストリーミング（Kafka）に最適

    パターン B — dbt Contract:
      → dbt の contract 機能でカラム型を強制
      → CI/CD でスキーマ違反を検出
      → バッチ（dbt プロジェクト）に最適

    パターン C — API Contract:
      → OpenAPI / JSON Schema でデータ構造定義
      → API 経由のデータ取り込みに最適
      → Gateway エージェントと連携

  導入判断:
    チーム間データ共有あり → Data Contract 必須
    ソースが外部 API → API Contract
    ストリーミング → Schema Registry
    バッチ DWH → dbt Contract
```

---

## 5. 可観測性チェックリスト

```
最小限の可観測性（全パイプライン必須）:
  □ パイプライン成功/失敗のアラート
  □ 実行時間のトレンド監視
  □ ソース鮮度チェック
  □ 行カウントの前日比較
  □ PK の unique + not_null テスト

中級の可観測性（パイプライン 10+ ）:
  □ 統計的異常検出（ボリューム、NULL率）
  □ スキーマ変更検出
  □ カラムレベルリネージ
  □ SLA モニタリング（鮮度、遅延）
  □ ダッシュボード（メトリクス可視化）

高度な可観測性（パイプライン 50+ ）:
  □ ML ベース自動モニタリング
  □ 根本原因分析の自動化
  □ 影響範囲の自動特定
  □ Data Contract の強制
  □ 統合プラットフォーム（Monte Carlo 等）
  □ AI/LLM パイプラインの出力品質監視
```

---

## 6. Stream との連携

```
Stream での活用:
  1. Quality Checks 設計で DO-01〜07 のスクリーニング
  2. パイプライン設計時に 5 Pillars の実装計画
  3. Data Contract の設計支援
  4. Beacon への可観測性ハンドオフ時にチェックリスト提供

品質ゲート:
  - テストのみの品質管理 → 統計的モニタリング追加（DO-01 防止）
  - アラート 50+/週 → 動的閾値・重要度分類（DO-02 防止）
  - パイプライン成功だけ監視 → 鮮度チェック追加（DO-03 防止）
  - スキーマ変更検出なし → Data Contract 導入（DO-04 防止）
  - 行カウント監視なし → ボリューム異常検出追加（DO-05 防止）
  - dbt docs 未生成 → リネージ可視化（DO-06 防止）
  - パイプライン/DWH/BI 個別監視 → 統合プラットフォーム検討（DO-07 防止）
```

**Source:** [Dagster: Data Observability 2025](https://dagster.io/guides/data-observability-in-2025-pillars-pros-cons-best-practices) · [Monte Carlo: Data Quality Management Past Present Future](https://www.montecarlodata.com/blog-the-past-present-and-future-of-data-quality-management/) · [Prefect: Data Pipeline Monitoring Best Practices](https://www.prefect.io/blog/data-pipeline-monitoring-best-practices) · [DQLabs: Multi-Layered Data Observability](https://www.dqlabs.ai/blog/multi-layered-data-observability-complete-guide-for-2025/)
