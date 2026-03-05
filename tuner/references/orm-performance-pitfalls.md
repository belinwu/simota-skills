# ORM Performance Pitfalls

> N+1 以外の ORM 固有パフォーマンス問題、ORM 選定基準、Raw SQL の使い分け

## 1. ORM 8 大パフォーマンス落とし穴

| # | 落とし穴 | ORM | 影響 | 対策 |
|---|---------|-----|------|------|
| **OP-01** | **Object Hydration コスト** | TypeORM / Sequelize | 大量行をクラスインスタンス化 → CPU 飽和 | 大量データは raw SQL + 軽量マッピング |
| **OP-02** | **Cold Start 遅延** | Prisma | Rust エンジンバイナリ起動 ~300ms | サーバーレスでは Drizzle / raw SQL 検討 |
| **OP-03** | **シリアライゼーションオーバーヘッド** | Prisma | Node.js ↔ Rust エンジン間のデータ変換 | 高スループット時は Drizzle / raw SQL |
| **OP-04** | **Lazy Loading の罠** | 全 ORM | 未設定で N+1 発生、設定ミスでメモリ膨張 | 明示的な eager loading（include/relations/with） |
| **OP-05** | **Synchronize モードの本番使用** | TypeORM | `synchronize: true` でスキーマ自動変更 → データ損失リスク | 本番は必ず明示的マイグレーション |
| **OP-06** | **Over-fetching** | 全 ORM | `findMany()` で全カラム取得 | select で必要カラムのみ指定 |
| **OP-07** | **Transaction スコープの広がりすぎ** | 全 ORM | 長時間トランザクション → ロック競合・コネクション枯渇 | トランザクションは最小範囲に限定 |
| **OP-08** | **型安全の偽り** | TypeORM | relation 未 include 時に undefined 返却、型は non-nullable | runtime 検証 / strict mode 有効化 |

---

## 2. ORM 別パフォーマンス特性（2025-2026）

```
ORM 選定マトリクス:

  Drizzle ORM:
    ✅ 軽量（バンドルサイズ最小）
    ✅ SQL ライクな構文 → 生成 SQL が予測可能
    ✅ サーバーレス Cold Start 最速
    ⚠️ 複雑な TypeScript 推論 → IDE ラグ（大規模スキーマ）
    ⚠️ N+1 保護なし → 開発者のSQL知識が必要

  Prisma:
    ✅ 型安全性最高 → DX 優秀
    ✅ エコシステム充実（Prisma Studio, Accelerate）
    ⚠️ Rust エンジンの Cold Start ~300ms
    ⚠️ 高スループットでのシリアライゼーションコスト
    ⚠️ 生成 SQL が非最適な場合あり

  TypeORM:
    ✅ Active Record + Data Mapper 両方サポート
    ⚠️ Object Hydration が重い（高スループットで顕著）
    ⚠️ 型安全性に穴（relation 未 include 問題）
    ❌ メンテナンス頻度低下（2025 時点）

  Sequelize:
    ⚠️ レガシー感（callback ベースの名残り）
    ❌ Object Hydration が最重量
    ❌ TypeScript サポートが限定的

パフォーマンス順（一般的なCRUD）:
  Drizzle ≈ raw SQL > Prisma > TypeORM > Sequelize
```

---

## 3. Raw SQL に切り替えるべき場面

```
ORM を超えるべきシグナル:

  1. 分析クエリ（複数 JOIN + GROUP BY + HAVING + Window Functions）
     → ORM の抽象化が邪魔になる
     → 例: 月次売上レポート、コホート分析

  2. バルク操作（10,000+ 行の INSERT/UPDATE/DELETE）
     → ORM のインスタンス化コストが支配的
     → 例: CSV インポート、バッチ更新

  3. DB 固有機能（PostgreSQL: LATERAL JOIN, JSONB 操作, CTE 再帰）
     → ORM がサポートしていない構文
     → 例: ツリー構造走査、JSONB パス操作

  4. サーバーレス環境（Cold Start が重要）
     → Prisma の ~300ms オーバーヘッド回避
     → Drizzle または kysely + raw SQL

  5. 高スループット API（1000+ RPS）
     → Object Hydration のコストが蓄積
     → 軽量マッピング（手動 or pgTyped）

ハイブリッドアプローチ（推奨）:
  - CRUD 操作: ORM（型安全性・DX のメリット）
  - レポート/分析: raw SQL（パフォーマンス優先）
  - バルク操作: COPY コマンド / raw SQL
  - マイグレーション: ORM のマイグレーション機能を維持
```

---

## 4. ORM パフォーマンスチェックリスト

```
レビュー時のチェック項目:

  □ findMany() に select が指定されているか（Over-fetching 防止）
  □ 関連テーブルは include/with で eager loading されているか（N+1 防止）
  □ ループ内で DB クエリを実行していないか
  □ Transaction スコープは最小限か
  □ 1000+ 行の操作に ORM の create/update を使っていないか（バルク操作）
  □ TypeORM の synchronize は false か（本番環境）
  □ Prisma の Cold Start が許容範囲内か（サーバーレス）
  □ 生成 SQL が EXPLAIN ANALYZE で確認されているか
```

---

## 5. Tuner との連携

```
Tuner での活用:
  1. Analyze フェーズで ORM 生成 SQL の EXPLAIN ANALYZE 確認
  2. Diagnose フェーズで OP-01〜08 のスクリーニング
  3. Optimize フェーズで raw SQL 切り替え判断
  4. Validate フェーズで ORM vs raw SQL の before/after 比較

品質ゲート:
  - findMany() に select なし → Over-fetching として警告（OP-06）
  - ループ内 DB クエリ → N+1 として検出（OP-04）
  - 10,000+ 行の ORM 操作 → バルク操作への切り替えを推奨（OP-01）
  - TypeORM synchronize: true → 本番禁止（OP-05）
  - サーバーレス + Prisma → Cold Start 計測を要求（OP-02）
```

**Source:** [TheDataGuy: Node.js ORMs in 2025](https://thedataguy.pro/blog/2025/12/nodejs-orm-comparison-2025/) · [Bytebase: Prisma vs TypeORM 2025](https://www.bytebase.com/blog/prisma-vs-typeorm/) · [UrhobA: Prisma ORM Performance Optimization Tips](https://www.urhoba.net/2025/11/prisma-orm-performance-optimization-tips.html) · [Silversky: TypeORM vs Prisma Deep Dive](https://medium.com/@silverskytechnology/battle-of-the-data-layers-a-deep-dive-into-typeorm-vs-prisma-for-node-js-developers-bee08a88f347)
