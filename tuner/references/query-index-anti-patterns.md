# Query & Index Anti-Patterns

> クエリ最適化・インデックス設計で犯しやすい 12 の誤りと対策

## 1. クエリ 6 大アンチパターン

| # | アンチパターン | 問題 | 影響 | 対策 |
|---|-------------|------|------|------|
| **QA-01** | **SELECT *** | 不要カラムの取得 | ネットワーク転送増・カバリングインデックス無効化 | 必要カラムのみ明示指定 |
| **QA-02** | **関数ラップカラム** | `WHERE YEAR(created_at) = 2024` | インデックス使用不可（全行変換） | 範囲条件に書き換え `WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'` |
| **QA-03** | **暗黙の型変換** | `WHERE id = '123'`（id は INT） | インデックス使用不可、全行スキャン | 型を一致させる `WHERE id = 123` |
| **QA-04** | **OR 条件の多用** | `WHERE a = 1 OR b = 2` | 各インデックスが効かず Seq Scan | UNION ALL に分解 / 複合条件用インデックス |
| **QA-05** | **先頭 % の LIKE** | `WHERE name LIKE '%smith'` | B-tree インデックス使用不可 | Full-text search / pg_trgm（GIN） / 逆順インデックス |
| **QA-06** | **深いネストサブクエリ** | 3-4 層のサブクエリ | プランナーが最適化困難 | CTE / JOIN に書き換え・段階的に分解 |

---

## 2. インデックス 6 大アンチパターン

| # | アンチパターン | 問題 | 影響 | 対策 |
|---|-------------|------|------|------|
| **IA-01** | **過剰インデックス** | 全カラムにインデックス作成 | INSERT/UPDATE/DELETE 性能低下・ストレージ浪費 | クエリパターン分析→必要なものだけ作成 |
| **IA-02** | **冗長インデックス** | `(a)` と `(a, b)` の両方が存在 | `(a)` は `(a, b)` で代替可能 | 冗長インデックスを検出して削除 |
| **IA-03** | **複合インデックスのカラム順序誤り** | `(status, created_at)` だが `WHERE created_at = ?` で使う | 先頭カラムが WHERE にないとインデックス不使用 | クエリの WHERE/ORDER BY に合わせた順序 |
| **IA-04** | **低カーディナリティへの B-tree** | `boolean` や `status` (3値) にインデックス | 選択性が低くプランナーが Seq Scan を選択 | Partial Index (`WHERE status = 'active'`) |
| **IA-05** | **未使用インデックスの放置** | 作成後使われていないインデックス | 書き込みオーバーヘッドのみ発生 | `pg_stat_user_indexes` で `idx_scan = 0` を定期確認 |
| **IA-06** | **CONCURRENTLY なしの本番 CREATE INDEX** | 通常の `CREATE INDEX` | テーブルにロック → 書き込みブロック | `CREATE INDEX CONCURRENTLY` を必ず使用 |

---

## 3. 検出用 SQL

```
冗長インデックス検出（PostgreSQL）:
  SELECT
    a.indexrelid::regclass AS redundant_index,
    b.indexrelid::regclass AS covering_index,
    pg_size_pretty(pg_relation_size(a.indexrelid)) AS wasted_size
  FROM pg_index a
  JOIN pg_index b ON a.indrelid = b.indrelid
    AND a.indexrelid != b.indexrelid
    AND a.indkey::text = ANY(
      SELECT string_to_array(b2.indkey::text, ' ')::text[]
      FROM pg_index b2 WHERE b2.indexrelid = b.indexrelid
    )
  WHERE NOT a.indisprimary;

関数ラップ検出:
  pg_stat_statements で以下パターンを grep
  - WHERE YEAR(...), WHERE DATE(...), WHERE LOWER(...)
  - WHERE CAST(... AS ...), WHERE column::type
  → 範囲条件または Expression Index への書き換え候補

暗黙型変換検出（MySQL）:
  EXPLAIN FORMAT=JSON SELECT ...;
  → "attached_condition" に type conversion が表示
```

---

## 4. 最適化判定フローチャート

```
クエリが遅い？
  │
  ├─ EXPLAIN ANALYZE を実行した？
  │   └─ No → まず EXPLAIN ANALYZE を実行
  │
  ├─ Seq Scan が原因？
  │   ├─ インデックスが存在しない → CREATE INDEX CONCURRENTLY
  │   ├─ インデックスはあるが使われない
  │   │   ├─ 関数ラップ → QA-02 対策
  │   │   ├─ 型不一致 → QA-03 対策
  │   │   ├─ 低カーディナリティ → IA-04 対策
  │   │   └─ テーブルが小さい → 正常（Seq Scan が最適）
  │   └─ 統計情報が古い → ANALYZE テーブル名
  │
  ├─ Nested Loop が原因？
  │   ├─ 内側テーブルにインデックスなし → インデックス追加
  │   └─ 両側が大きい → Hash Join / Merge Join に誘導（enable_nestloop = off で検証）
  │
  ├─ Sort が原因？
  │   ├─ work_mem 不足でディスクソート → work_mem 増加
  │   └─ ORDER BY カラムにインデックスなし → ソート用インデックス追加
  │
  └─ N+1 クエリ？ → JOIN / IN 句 / eager loading に書き換え
```

---

## 5. Tuner との連携

```
Tuner での活用:
  1. Analyze フェーズで QA-01〜06 / IA-01〜06 のスクリーニング
  2. Diagnose フェーズで検出 SQL を実行して問題箇所を特定
  3. Optimize フェーズで対策パターンを適用
  4. Validate フェーズで EXPLAIN ANALYZE の before/after 比較

品質ゲート:
  - SELECT * 使用 → 必要カラム明示を要求（QA-01 防止）
  - WHERE に関数ラップ → 範囲条件への書き換えを推奨（QA-02 防止）
  - CREATE INDEX に CONCURRENTLY なし → 本番環境での必須化（IA-06 防止）
  - 冗長インデックス検出 → 削除候補として報告（IA-02 防止）
```

**Source:** [NumberAnalytics: Anti-Patterns in Database Systems](https://www.numberanalytics.com/blog/ultimate-guide-to-anti-patterns-in-database-systems) · [Medium: Query Optimization Patterns](https://medium.com/@artemkhrenov/query-optimization-patterns-writing-efficient-sql-for-high-performance-applications-8143e5028443) · [GitHub: SQL Anti-Patterns](https://github.com/boralp/sql-anti-patterns) · [InfoQ: Performance Anti-Patterns in Database-Driven Applications](https://www.infoq.com/articles/Anti-Patterns-Alois-Reitbauer/)
