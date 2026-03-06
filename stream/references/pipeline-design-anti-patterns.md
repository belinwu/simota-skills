# Pipeline Design Anti-Patterns

> ETL/ELT パイプライン設計の失敗パターン、オーケストレーションの罠、スケーラビリティ課題

## 1. パイプライン設計 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **PD-01** | **Append-Only Trap（追記のみの罠）** | パイプライン再実行でデータが重複 | 午前2時の手動クリーンアップ、重複行の頻発、行カウント不一致 | べき等設計: パーティション単位の DELETE→INSERT（トランザクション内）、UPSERT |
| **PD-02** | **Silent Failure（サイレント障害）** | パイプラインは成功するがデータは古いまま | ユーザー苦情で初めて発覚、ダッシュボードの鮮度不明、信頼喪失 | データ鮮度監視（max event timestamp）、成功≠最新のアラート分離 |
| **PD-03** | **SELECT * Fragility（SELECT * の脆弱性）** | ソースカラム追加でパイプライン破損 | スキーマ変更のたびに障害、型不一致エラー、予期しないNULL | カラム明示指定 + 型キャスト + 欠落カラムの明示的エラー |
| **PD-04** | **Cron Job Orchestration（cron ジョブ依存）** | 依存関係・リトライなしの定期実行 | 3パイプライン超で破綻、手動リトライ、障害の連鎖 | 専用オーケストレーター（Airflow/Dagster/Prefect）、DAG 依存管理 |
| **PD-05** | **Hardcoded Time（時間のハードコード）** | `today()` や `now()` を直接使用 | バックフィル不能、テスト困難、再実行で異なる結果 | 実行日パラメータ化（Airflow `{{ ds }}`）、決定論的な時間参照 |
| **PD-06** | **No Validation Gate（バリデーション不在）** | 品質チェックなしでデータをロード | 不正データが下流に伝播、ダッシュボード汚染、指標の信頼喪失 | 3層バリデーション（Source/Transform/Sink）、失敗時のパイプライン停止 |
| **PD-07** | **Full Reload Addiction（フルリロード中毒）** | 毎回全データを再処理 | 処理時間の線形増大、コスト爆発、SLA 未達 | 増分ロード（CDC/timestamp ベース）、変更データのみ処理 |

---

## 2. ETL vs ELT 選択の判断ミス

```
よくある判断ミス:

  ❌ クラウド DWH なのに ETL を採用:
    → Snowflake/BigQuery は変換処理に最適化されている
    → Python で変換するより SQL（dbt）が効率的
    → 推奨: ELT（dbt + クラウド DWH）

  ❌ レガシー DB なのに ELT を採用:
    → オンプレ DB に変換処理を押し付ける
    → DB リソースがトランザクション処理と競合
    → 推奨: ETL（Airflow + Python/Spark）

  ❌ リアルタイム要件にバッチを採用:
    → レイテンシ < 1分 の要件にバッチは不適
    → 推奨: Kafka + ストリーム処理（Flink/Spark Streaming）

  ❌ バッチで十分なのにストリーミングを採用:
    → 日次レポートに Kafka クラスタは過剰
    → 運用コスト・複雑性が不必要に増大
    → 推奨: Airflow + dbt のシンプル構成

判断マトリクス:
  レイテンシ要件    | データ量      | 推奨アーキテクチャ
  --------------|------------|---------------------
  日次/週次       | 任意        | Batch（Airflow + dbt）
  1時間以内       | 中量        | Micro-batch（Spark Structured Streaming）
  1分以内        | 大量        | Streaming（Kafka + Flink）
  サブ秒         | 任意        | Streaming + CDC（Debezium + Kafka）
```

---

## 3. オーケストレーションのアンチパターン

```
DAG 設計の罠:

  ❌ God DAG（神 DAG）:
    → 1つの DAG に全パイプラインを詰め込む
    → 問題: 1つの失敗で全体が停止、再実行コスト大
    → 対策: ドメイン別 DAG 分割、DAG 間依存は ExternalTaskSensor

  ❌ Deep DAG（深い DAG）:
    → タスクが直列に 20+ ステップ連鎖
    → 問題: 1つの失敗で長い再実行、並列化不能
    → 対策: 独立タスクの並列化、ステージ単位のグルーピング

  ❌ Fat Task（太ったタスク）:
    → 1つのタスクに Extract/Transform/Load を全部詰める
    → 問題: 部分リトライ不能、デバッグ困難
    → 対策: E → T → L を個別タスクに分割

  ❌ Missing Retry Strategy（リトライ戦略不在）:
    → リトライなし or 無限リトライ
    → 問題: 一時的エラーで永久停止 or リソース枯渇
    → 対策: exponential backoff + jitter、transient/permanent エラー分離

  ❌ No Dead Letter Queue（DLQ 不在）:
    → 処理失敗レコードを破棄 or パイプライン全体停止
    → 問題: データ損失 or 全体停止の二択
    → 対策: 失敗レコードを DLQ に退避、後で再処理

  ✅ 健全な DAG 設計原則:
    → 1 DAG = 1 ドメイン（orders, users, payments）
    → タスクは単一責務（Extract, Validate, Transform, Load）
    → べき等性: 何回実行しても同じ結果
    → パラメータ化: 実行日を引数で受け取る
    → アラート: 失敗時 + SLA 超過時の通知
```

---

## 4. スケーラビリティの落とし穴

```
パイプライン成長に伴う問題:

  Stage 1（初期 ~10 パイプライン）:
    → cron + Python スクリプトで十分
    → 問題は少ないが技術的負債が蓄積

  Stage 2（成長期 10-50 パイプライン）:
    → オーケストレーター必須（Airflow/Dagster）
    → DAG 設計の品質が運用負荷を決める
    → PD-04（cron 依存）がここで顕在化

  Stage 3（成熟期 50-200 パイプライン）:
    → フルリロードのコスト問題（PD-07）
    → 増分ロード + CDC への移行必須
    → データカタログ・リネージの需要増大

  Stage 4（大規模 200+ パイプライン）:
    → チーム横断のガバナンス問題
    → Data Mesh / Domain Ownership の検討
    → SLA 管理・優先度制御の仕組み必須

  予防策:
    → Stage 1 からオーケストレーター採用
    → Stage 2 でべき等性 + バリデーション標準化
    → Stage 3 で増分ロード + リネージ導入
    → Stage 4 でドメイン分割 + セルフサービス化
```

---

## 5. パイプラインテスト戦略

```
テストレベル:

  Level 1 — Unit Tests（変換ロジック）:
    □ 既知の入力→期待出力のアサーション
    □ エッジケース: ゼロ値、負数、NULL、空文字列
    □ 型変換の正確性

  Level 2 — Integration Tests（E2E）:
    □ テスト DB でのパイプライン全体実行
    □ サンプルデータでのソース→シンク検証
    □ スキーマ変更の影響テスト

  Level 3 — Data Contract Tests:
    □ ソース/シンク間のスキーマ合意
    □ カラム型、NULL 許可、値域の契約
    □ 契約違反時のアラート

  Level 4 — Canary Tests（本番）:
    □ 本番データの統計的異常検出
    □ 行カウント、NULL 率、分布の監視
    □ SLA（鮮度、レイテンシ）の検証
```

---

## 6. Stream との連携

```
Stream での活用:
  1. FLOW Framework の Frame フェーズで PD-01〜07 スクリーニング
  2. パイプライン設計時に ETL/ELT 判断マトリクス適用
  3. DAG 設計レビュー時にオーケストレーションアンチパターン検出
  4. Gear への CI/CD ハンドオフ時にテスト戦略を提供

品質ゲート:
  - パイプライン再実行で行カウント変化 → べき等性修正（PD-01 防止）
  - データ鮮度アラートなし → 鮮度監視追加（PD-02 防止）
  - SELECT * 使用 → カラム明示指定（PD-03 防止）
  - cron 直接実行 → オーケストレーター移行（PD-04 防止）
  - バリデーション 0 件 → 3 層バリデーション追加（PD-06 防止）
  - フルリロード + データ量増大 → 増分ロード提案（PD-07 防止）
```

**Source:** [OneUpTime: ETL Best Practices](https://oneuptime.com/blog/post/2026-02-13-etl-best-practices/view) · [Celigo: 7 ETL Best Practices](https://www.celigo.com/blog/7-etl-best-practices-for-building-data-pipelines-that-scale/) · [dbt Labs: Modern Data Engineering Best Practices](https://www.getdbt.com/blog/modern-data-engineering-best-practices)
