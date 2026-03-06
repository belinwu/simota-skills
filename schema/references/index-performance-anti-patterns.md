# Index Performance Anti-Patterns

> インデックス設計の失敗パターン、パフォーマンス劣化の原因、過剰/不足インデックスの罠

## 1. インデックス 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **IP-01** | **Over-Indexing（過剰インデックス）** | 全カラムにインデックスを作成 | INSERT/UPDATE 速度劣化、ストレージ肥大、gaming: 20+インデックスで1万同時ユーザー処理不能 | クエリパターン分析→必要最小限、`pg_stat_user_indexes` で未使用検出 |
| **IP-02** | **Composite Order Mistake（複合インデックス順序ミス）** | 複合インデックスのカラム順序が不適切 | インデックスがあるのに Seq Scan、WHERE 句の最左カラム不一致 | 左端一致ルール: 高選択性カラム → 低選択性カラムの順、WHERE 句の使用パターンに合致 |
| **IP-03** | **Low Cardinality Index（低カーディナリティ）** | `status` ('active'/'inactive') や `gender` ('M'/'F') にB-treeインデックス | インデックスサイズ大、効果なし（フルスキャンと同等）、プランナーが無視 | 部分インデックス（`WHERE status = 'active'`）、BRIN インデックス、またはインデックス不要 |
| **IP-04** | **Missing FK Index（FK インデックス不在）** | 外部キーカラムにインデックスなし | JOIN 時にフルテーブルスキャン、CASCADE DELETE が極端に遅い | FK カラムには自動でインデックス追加（PostgreSQL は自動作成しない） |
| **IP-05** | **Index Bloat（インデックス膨張）** | UPDATE/DELETE 後の dead tuple でインデックスが肥大 | インデックスサイズがテーブルサイズを超過、VACUUM 不足、クエリ速度の段階的劣化 | 定期的 REINDEX、VACUUM 設定の調整、pg_repack 活用 |
| **IP-06** | **Expression Index Neglect（式インデックス未活用）** | WHERE LOWER(email) でインデックスが効かない | 関数適用でインデックスが使われない、Seq Scan が発生 | 式インデックス（`CREATE INDEX ON t (LOWER(email))`）、PostgreSQL の COLLATE 設定 |
| **IP-07** | **Covering Index Miss（カバリングインデックス未活用）** | インデックスで検索後にテーブルアクセスが必要 | Index Scan 後に大量の Heap Fetch、ランダム I/O 多発 | INCLUDE 句でカバリングインデックス（Index-Only Scan を実現） |

---

## 2. 複合インデックス設計の原則

```
左端一致ルール（Leftmost Prefix Rule）:

  CREATE INDEX idx_example ON orders (status, created_at, customer_id);

  ✅ 使用される:
    WHERE status = 'active'
    WHERE status = 'active' AND created_at > '2024-01-01'
    WHERE status = 'active' AND created_at > '2024-01-01' AND customer_id = 5

  ❌ 使用されない:
    WHERE created_at > '2024-01-01'  ← status をスキップ
    WHERE customer_id = 5            ← status, created_at をスキップ

カラム順序の決定基準:

  1. 等値条件のカラムを先に:
     WHERE status = 'active' AND created_at > '2024-01-01'
     → (status, created_at) ✅
     → (created_at, status) ❌

  2. 選択性の高いカラムを先に:
     status: 3値（低選択性） vs customer_id: 10万値（高選択性）
     → 等値条件が同じなら customer_id を先に

  3. 範囲条件は最後:
     WHERE status = 'active' AND customer_id = 5 AND created_at > '2024-01-01'
     → (status, customer_id, created_at) ✅

  4. ORDER BY / GROUP BY を考慮:
     WHERE status = 'active' ORDER BY created_at
     → (status, created_at) でソートもインデックスで処理
```

---

## 3. インデックス種別の適切な使い分け

```
PostgreSQL インデックス種別:

  B-tree（デフォルト）:
    ✅ 等値検索、範囲検索、ソート、LIKE 'prefix%'
    ❌ 全文検索、配列検索、低カーディナリティ

  GIN（Generalized Inverted Index）:
    ✅ JSONB 検索、全文検索（tsvector）、配列 contains
    ❌ 範囲検索、更新頻度が高いカラム（更新コスト高）

  GiST（Generalized Search Tree）:
    ✅ 地理空間データ、範囲型、全文検索（近傍）
    ❌ 単純な等値/範囲検索（B-tree が優位）

  BRIN（Block Range Index）:
    ✅ 物理的にソートされた大テーブル（時系列データ、ログ）
    ❌ ランダムに分布するデータ、小テーブル
    → インデックスサイズが B-tree の 1/100 以下

  Hash:
    ✅ 等値検索のみ（= 演算子のみ）
    ❌ 範囲検索、ソート、部分一致
    → PG 10+ でクラッシュセーフ、用途限定的

  部分インデックス（Partial Index）:
    CREATE INDEX idx_active_users ON users (email) WHERE is_active = true;
    → インデックスサイズ削減、特定条件のクエリ高速化
    → 低カーディナリティの IP-03 対策として有効
```

---

## 4. インデックス健全性モニタリング

```
未使用インデックスの検出:

  -- PostgreSQL: 未使用インデックス
  SELECT schemaname, relname, indexrelname, idx_scan,
         pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
  FROM pg_stat_user_indexes
  WHERE idx_scan = 0
    AND indexrelid NOT IN (
      SELECT conindid FROM pg_constraint
      WHERE contype IN ('p', 'u')  -- PK/UNIQUE は除外
    )
  ORDER BY pg_relation_size(indexrelid) DESC;

重複インデックスの検出:

  -- 左端が重複するインデックスペア
  -- (a, b) と (a, b, c) → (a, b) は冗長な可能性
  SELECT a.indexrelid::regclass AS index_a,
         b.indexrelid::regclass AS index_b,
         a.indkey AS cols_a, b.indkey AS cols_b
  FROM pg_index a
  JOIN pg_index b ON a.indrelid = b.indrelid
    AND a.indexrelid != b.indexrelid
    AND a.indkey <@ b.indkey  -- a のカラムが b に含まれる
    AND a.indkey != b.indkey;

インデックス膨張の確認:

  -- pgstattuple 拡張
  SELECT * FROM pgstattuple('index_name');
  -- dead_tuple_percent が高い → REINDEX 検討

  -- テーブルサイズ vs インデックスサイズ
  SELECT relname,
         pg_size_pretty(pg_table_size(oid)) AS table_size,
         pg_size_pretty(pg_indexes_size(oid)) AS indexes_size
  FROM pg_class
  WHERE relkind = 'r'
  ORDER BY pg_indexes_size(oid) DESC;
  -- インデックスサイズ > テーブルサイズ → 過剰インデックスの疑い
```

---

## 5. インデックス設計チェックリスト

```
新規インデックス追加前:
  □ EXPLAIN ANALYZE でインデックスなしのクエリプランを確認
  □ 対象カラムのカーディナリティを確認
  □ 既存インデックスとの重複チェック
  □ INSERT/UPDATE への影響見積もり
  □ テーブルサイズと行数の確認

作成時:
  □ CREATE INDEX CONCURRENTLY を使用（本番環境）
  □ 適切なインデックス種別を選択
  □ 複合インデックスのカラム順序を最適化
  □ 部分インデックスの適用可否を検討
  □ INCLUDE 句でカバリングインデックスを検討

作成後:
  □ EXPLAIN ANALYZE で効果を検証
  □ pg_stat_user_indexes で利用状況を追跡
  □ ストレージ増加量の確認

定期メンテナンス:
  □ 未使用インデックスの定期検出（月次）
  □ 重複インデックスの定期検出（月次）
  □ インデックス膨張の監視（VACUUM 状況）
  □ 新しいクエリパターンに対するインデックス追加検討
```

---

## 6. Schema との連携

```
Schema での活用:
  1. Index Design フェーズで IP-01〜07 のスクリーニング
  2. 新規テーブル設計時に FK インデックスの自動提案
  3. 既存スキーマレビュー時にインデックス健全性チェック
  4. Tuner への連携時にインデックス品質情報を提供

品質ゲート:
  - テーブルにインデックス 10+ → 過剰インデックス検出（IP-01 防止）
  - 複合インデックスの順序 → 左端一致ルール検証（IP-02 防止）
  - BOOLEAN/ENUM カラムに B-tree → 部分インデックス提案（IP-03 防止）
  - FK カラムにインデックスなし → 追加提案（IP-04 防止）
  - インデックスサイズ > テーブルサイズ → 膨張チェック（IP-05 防止）
  - WHERE LOWER/UPPER 使用 → 式インデックス提案（IP-06 防止）
  - 頻繁な Index Scan + Heap Fetch → カバリングインデックス提案（IP-07 防止）
```

**Source:** [Levitation: Database Schema Design Anti-Patterns](https://levitation.in/blog/database-schema-design-anti-patterns/) · [DBSchema: Database Indexing Anti-Patterns](https://dbschema.com/2024/12/11/data-modeling-anti-patterns/) · [Furkan Baytekin: Indexing Strategies](https://furkanbaytekin.dev/database-migration-anti-patterns/)
