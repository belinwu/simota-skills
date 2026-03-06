# dbt & Data Warehouse Anti-Patterns

> dbt モデリング・データウェアハウス設計の失敗パターン、セマンティックレイヤーの課題

## 1. dbt モデリング 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **DW-01** | **Staging Skip（ステージング省略）** | raw → mart 直接変換 | ソース変更が mart に直撃、テスト困難、リネージ不明 | 必ず stg_ レイヤーを経由、1:1 のソーステーブルマッピング |
| **DW-02** | **God Model（神モデル）** | 1つの SQL に全ビジネスロジックを詰め込み | 500+ 行の SQL、理解不能、テスト困難、再利用不能 | int_ レイヤーで分割、単一責務（1モデル = 1変換） |
| **DW-03** | **Hardcoded References（ハードコード参照）** | `ref()` を使わず直接テーブル名指定 | リネージ切断、環境切替不能、DAG 依存関係不明 | 全参照を `ref()` / `source()` マクロ経由 |
| **DW-04** | **Test Desert（テスト砂漠）** | dbt tests ゼロのプロジェクト | データ品質問題の検出遅延、回帰バグ、信頼性低下 | unique/not_null 必須、relationships テスト、カスタム SQL テスト |
| **DW-05** | **View Everything（全ビュー化）** | 全モデルを `materialized='view'` で構成 | クエリ時間の線形増大、大規模テーブルでタイムアウト | stg=view, int=ephemeral or table, mart=table/incremental |
| **DW-06** | **Metric Inconsistency（指標不一致）** | 同じ KPI が複数モデルで異なる定義 | 「売上」の定義がチームごとに異なる、レポート間の数値不一致 | セマンティックレイヤー（dbt Metrics / Semantic Layer）で一元定義 |
| **DW-07** | **Documentation Void（ドキュメント不在）** | モデル・カラムの description 未記載 | 新メンバーが理解不能、データカタログ空、発見性ゼロ | schema.yml に全モデル・カラムの description 必須 |

---

## 2. レイヤー設計のベストプラクティス

```
4 層アーキテクチャ:

  Source Layer（ソース宣言）:
    → sources.yml でソーステーブルを宣言
    → freshness チェックで鮮度監視
    → 直接参照は staging からのみ

  Staging Layer（stg_*）:
    materialized: view
    命名: stg_{source}__{entity}（例: stg_stripe__payments）
    役割:
      □ カラムリネーム（スネークケース統一）
      □ 型キャスト
      □ 基本フィルタ（deleted = false 等）
      □ ソースと 1:1 対応
    禁止: JOIN、ビジネスロジック

  Intermediate Layer（int_*）:
    materialized: ephemeral or table
    命名: int_{entity}_{verb}（例: int_orders_enriched）
    役割:
      □ JOIN（エンリッチメント）
      □ ビジネスロジックの適用
      □ 計算カラムの追加
      □ 再利用可能な中間成果物
    原則: 単一責務、分割して小さく保つ

  Mart Layer（dim_* / fct_* / rpt_*）:
    materialized: table or incremental
    命名:
      dim_{entity}（ディメンション: dim_customers）
      fct_{event}（ファクト: fct_orders）
      rpt_{report}（レポート: rpt_daily_sales）
    役割:
      □ BI ツール/API が直接参照
      □ ビジネスユーザーが理解できる粒度
      □ パフォーマンス最適化済み

  依存ルール:
    source → stg → int → mart（一方向のみ）
    mart → mart は避ける（循環依存の元）
    int → int は許可（段階的変換）
```

---

## 3. Materialization 戦略

```
選択基準:

  view:
    ✅ ステージングモデル（軽量、ソース追従）
    ✅ シンプルな変換（型キャスト、リネーム）
    ❌ 大量データの集計（クエリ時間増大）

  table:
    ✅ マートモデル（BI ツールから直接クエリ）
    ✅ 中間モデル（頻繁に参照される場合）
    ❌ ソースが頻繁に変わるモデル（毎回フルリビルド）

  incremental:
    ✅ 大規模ファクトテーブル（イベントログ等）
    ✅ 追記型データ（ログ、トランザクション）
    ⚠️ 注意: is_incremental() の条件設計が重要
    ⚠️ 定期的な full-refresh も計画に含める

  ephemeral:
    ✅ 中間 CTE として使い捨て
    ✅ 単独では参照されないヘルパーモデル
    ❌ デバッグ困難（実テーブルが存在しない）

  一般的な構成:
    stg_ → view
    int_ → ephemeral（小規模） or table（大規模/頻繁参照）
    dim_ → table
    fct_ → table or incremental（データ量による）
    rpt_ → table
```

---

## 4. セマンティックレイヤーの課題

```
指標定義の一貫性問題:

  問題の構造:
    → 「月間売上」の定義がチームごとに異なる
    → 返品を含む/含まない、税込/税抜、通貨換算の違い
    → BI ツールごとに独自計算 → 数値不一致 → 信頼喪失

  解決策 — セマンティックレイヤー:
    → 指標（Metrics）を一元的に定義
    → 全BI ツール/API が同一定義を参照
    → dbt Semantic Layer / MetricFlow が標準的な実装

  セマンティックレイヤー設計原則:
    □ 1つの指標 = 1つの定義（Single Source of Truth）
    □ ディメンション（切り口）を明示的に定義
    □ フィルタ条件を指標定義に含める
    □ バージョン管理で定義変更を追跡

  導入判断:
    チーム 1-3人 → dbt mart で直接定義で十分
    チーム 4-10人 → セマンティックレイヤー検討
    チーム 10人+ → セマンティックレイヤー必須
```

---

## 5. dbt プロジェクトチェックリスト

```
新規 dbt プロジェクト:
  □ sources.yml で全ソース宣言 + freshness 設定
  □ stg_ モデルで全ソースをラップ（1:1）
  □ schema.yml で全モデル・カラムに description
  □ unique + not_null テストを PK カラムに必須
  □ relationships テストを FK カラムに設定
  □ CI/CD で dbt build（run + test）を自動実行

既存プロジェクトの健全性チェック:
  □ ref() 未使用のハードコード参照がないか
  □ 500+ 行の巨大モデルがないか
  □ テストカバレッジ（全 PK に unique + not_null）
  □ description カバレッジ（全モデル + 主要カラム）
  □ materialization が適切か（大規模 view の検出）
  □ 循環参照がないか（mart → mart 等）
  □ 命名規約（stg_/int_/dim_/fct_/rpt_）統一

  dbt コマンド:
    dbt source freshness   — ソース鮮度チェック
    dbt build              — run + test を一括実行
    dbt docs generate      — ドキュメント生成
    dbt docs serve         — ドキュメントサーバー起動
```

---

## 6. Stream との連携

```
Stream での活用:
  1. dbt Modeling で DW-01〜07 のスクリーニング
  2. 新規 dbt プロジェクトでレイヤー設計ガイド適用
  3. 既存プロジェクトの健全性チェック
  4. Scribe へのドキュメントハンドオフ時に指標定義を提供

品質ゲート:
  - stg_ レイヤー不在 → ステージング追加提案（DW-01 防止）
  - 500+ 行モデル → int_ 分割提案（DW-02 防止）
  - ref() 未使用 → マクロ移行提案（DW-03 防止）
  - テスト 0 件 → unique/not_null 追加（DW-04 防止）
  - 大規模 view → table/incremental 移行（DW-05 防止）
  - 同一指標の複数定義 → セマンティックレイヤー提案（DW-06 防止）
  - description 0% → ドキュメント追加（DW-07 防止）
```

**Source:** [HevoData: dbt Data Modeling Pitfalls](https://hevodata.com/data-transformation/dbt-data-modeling/) · [dbt Labs: Modular Data Modeling Techniques](https://www.getdbt.com/blog/modular-data-modeling-techniques) · [dbt Labs: Data Modeling Techniques](https://www.getdbt.com/blog/data-modeling-techniques) · [Integrate.io: Mastering Data Warehouse Modeling](https://www.integrate.io/blog/mastering-data-warehouse-modeling/)
