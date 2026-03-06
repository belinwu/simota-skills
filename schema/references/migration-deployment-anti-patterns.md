# Migration & Deployment Anti-Patterns

> マイグレーション・デプロイメントの失敗パターン、ゼロダウンタイム移行の課題

## 1. マイグレーション 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **MD-01** | **Big Bang Migration（ビッグバン移行）** | 全スキーマ変更を1回のマイグレーションで実行 | ロールバック不能、失敗時の復旧に数時間、ダウンタイム長大 | 段階的マイグレーション（Expand-Contract）、小さな変更の連続 |
| **MD-02** | **Table Lock Blindness（テーブルロック盲目）** | ALTER TABLE がロックを取得することを考慮しない | 本番で ALTER TABLE 実行時にクエリタイムアウト多発、502 エラー | NOT NULL 追加は DEFAULT 付き、カラム追加は末尾、大テーブルは pt-osc/gh-ost |
| **MD-03** | **No Rollback Plan（ロールバック不在）** | DOWN マイグレーションを書かない | 問題発生時に手動修正、データ復旧不能、深夜の緊急対応 | 全マイグレーションに UP/DOWN を必須化、不可逆操作はバックアップ必須 |
| **MD-04** | **Data Migration in Schema Migration（スキーマ内データ移行）** | スキーマ変更とデータ変換を同じマイグレーションで実行 | マイグレーション時間の長大化、失敗時の状態不明、ロック時間増大 | スキーマ変更とデータ移行を分離（別マイグレーション） |
| **MD-05** | **Inadequate Planning（計画不足）** | マイグレーション前のインパクト分析なし | レガシーマイグレーションの60%が計画不足で失敗（業界統計） | 依存関係マッピング、影響分析、テスト環境での事前検証 |
| **MD-06** | **CDC Ignorance（CDC 無視）** | バルクロード中の差分データを捕捉しない | 移行完了後にデータ不整合、ソースとターゲットの乖離 | Change Data Capture（CDC）パイプライン、Debezium/DMS 活用 |
| **MD-07** | **Observability Gap（可観測性の欠如）** | マイグレーション中のモニタリングなし | 乖離の検出が遅延、サイレントなデータ損失、移行の成功/失敗が不明 | リアルタイムメトリクス、行カウント比較、チェックサム検証 |

---

## 2. ゼロダウンタイムマイグレーション戦略

```
5 フェーズアプローチ:

  Phase 1 — Preparation（準備）:
    □ 現行スキーマの完全なドキュメント化
    □ 依存関係マッピング（アプリ、ジョブ、レポート）
    □ ターゲットスキーマ設計 + レビュー
    □ テスト環境での事前検証
    □ ロールバック手順書の作成
    □ 影響を受けるチームへの事前通知

  Phase 2 — Bulk Load（初期データ移行）:
    □ スナップショット取得 + バルクコピー
    □ 大量データの効率的転送（COPY コマンド, pg_dump）
    □ インデックスは後で構築（バルクロード高速化）
    □ 外部キー制約は一時無効化

  Phase 3 — Change Data Capture（差分同期）:
    □ CDC パイプライン起動（Debezium, AWS DMS）
    □ ソース→ターゲットのリアルタイム同期
    □ 差分の遅延モニタリング
    □ データ整合性の継続チェック

  Phase 4 — Dual Writes（二重書き込み）:
    □ アプリが新旧両方に書き込み
    □ 新スキーマからの読み取りテスト
    □ パフォーマンス比較
    □ 整合性の最終検証

  Phase 5 — Traffic Cutover（切り替え）:
    □ 読み取りを新スキーマに切り替え
    □ 書き込みを新スキーマに切り替え
    □ 旧スキーマへの書き込み停止
    □ モニタリング強化（24-48h）
    □ 旧スキーマのアーカイブ/削除
```

---

## 3. 危険な ALTER TABLE 操作

```
PostgreSQL でのロックレベル:

  ACCESS EXCLUSIVE LOCK（全操作ブロック）:
    ❌ ALTER TABLE ... ALTER COLUMN TYPE ...（型変更）
    ❌ ALTER TABLE ... ADD COLUMN ... DEFAULT ...（PG < 11）
    ❌ ALTER TABLE ... SET NOT NULL（制約追加）
    ❌ DROP TABLE / DROP COLUMN

  安全な操作（ロック最小限）:
    ✅ ADD COLUMN（NULL 許可、DEFAULT なし）
    ✅ ADD COLUMN ... DEFAULT ...（PG 11+, メタデータのみ変更）
    ✅ CREATE INDEX CONCURRENTLY（非ブロッキング）
    ✅ DROP INDEX CONCURRENTLY
    ✅ COMMENT ON（メタデータ更新のみ）

  安全な NOT NULL 追加手順:
    Step 1: CHECK 制約追加（NOT VALID — ロック短い）
      ALTER TABLE t ADD CONSTRAINT chk_col_nn
        CHECK (col IS NOT NULL) NOT VALID;
    Step 2: CHECK 制約の VALIDATE（ShareUpdateExclusiveLock）
      ALTER TABLE t VALIDATE CONSTRAINT chk_col_nn;
    Step 3: NOT NULL 追加（PG 12+ は CHECK から推論、即座）
      ALTER TABLE t ALTER COLUMN col SET NOT NULL;
    Step 4: CHECK 制約の削除
      ALTER TABLE t DROP CONSTRAINT chk_col_nn;

  MySQL での注意:
    → InnoDB Online DDL は多くの操作をインプレースで実行可能
    → ただし大テーブルでの ALTER は pt-online-schema-change が安全
    → gh-ost: GitHub 製、トリガーレスのオンラインスキーマ変更
```

---

## 4. Expand-Contract パターン詳細

```
カラムリネーム例（ゼロダウンタイム）:

  ❌ 危険な方法:
    ALTER TABLE users RENAME COLUMN name TO full_name;
    → アプリが即座に壊れる

  ✅ Expand-Contract:

    Step 1 — Expand（拡張）:
      ALTER TABLE users ADD COLUMN full_name VARCHAR(255);
      -- アプリ: name を読み書き + full_name にも書き込み
      -- トリガー: name 更新時に full_name も更新

    Step 2 — Migrate（移行）:
      UPDATE users SET full_name = name WHERE full_name IS NULL;
      -- バッチ処理（大テーブルは chunk 単位）
      ALTER TABLE users ALTER COLUMN full_name SET NOT NULL;
      -- アプリ: full_name を読み書き（name は読み取りのみ）

    Step 3 — Contract（縮小）:
      -- 全アプリが full_name を使用していることを確認
      ALTER TABLE users DROP COLUMN name;
      -- トリガー削除

  時間軸:
    Step 1 → デプロイ A（新カラム追加 + 二重書き込み）
    Step 2 → バッチジョブ（データ移行）→ デプロイ B（読み取り切り替え）
    Step 3 → デプロイ C（旧カラム削除）— 数日〜数週間後
```

---

## 5. マイグレーション前チェックリスト

```
実行前:
  □ テスト環境で全マイグレーションを実行済み
  □ ロールバック手順をテスト済み
  □ 影響を受けるテーブルのサイズを確認
  □ ロック時間の見積もり（大テーブルは要注意）
  □ 依存するアプリ/ジョブ/レポートの確認
  □ 実行タイミングの決定（低トラフィック時間帯）
  □ モニタリング/アラートの準備
  □ バックアップの取得と検証

実行中:
  □ 各ステップの実行時間を記録
  □ エラー発生時の即時中断判断基準
  □ ロック待機のモニタリング
  □ アプリケーションのヘルスチェック

実行後:
  □ データ整合性の検証（行カウント、チェックサム）
  □ アプリケーション動作確認
  □ パフォーマンス確認（クエリ実行計画）
  □ 24h モニタリング強化
  □ ロールバック手順書の保管（一定期間）
```

---

## 6. Schema との連携

```
Schema での活用:
  1. Migrate フェーズで MD-01〜07 のスクリーニング
  2. ゼロダウンタイム要件時に 5 フェーズ戦略を適用
  3. ALTER TABLE 実行前にロック影響分析
  4. Expand-Contract パターンの自動提案

品質ゲート:
  - 1マイグレーション 100+ 行 → 分割提案（MD-01 防止）
  - ALTER TABLE ... SET NOT NULL → 安全手順提案（MD-02 防止）
  - DOWN マイグレーション未定義 → 追加要求（MD-03 防止）
  - スキーマ変更 + データ変換が同一ファイル → 分離提案（MD-04 防止）
  - 大テーブル（100万+ 行）への ALTER → オンラインツール提案（MD-02 防止）
  - モニタリング計画なし → 可観測性追加（MD-07 防止）
```

**Source:** [Furkan Baytekin: Database Migration Anti-Patterns](https://furkanbaytekin.dev/database-migration-anti-patterns/) · [Red-Gate: Zero-Downtime Database Migration](https://www.red-gate.com/blog/database-devops/zero-downtime-database-migration) · [DEV.to: Common Database Anti-Patterns](https://dev.to/kanani_nirav/common-database-anti-patterns-and-how-to-avoid-them-2kib)
