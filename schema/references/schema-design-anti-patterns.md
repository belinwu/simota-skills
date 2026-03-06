# Schema Design Anti-Patterns

> スキーマ設計の失敗パターン、構造的欠陥、制約不足の課題

## 1. スキーマ設計 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **SD-01** | **God Table（神テーブル）** | 1テーブルに200+カラムを詰め込む | クエリ時間の80%がフルスキャン、ALTER TABLE に数時間、NULL だらけのカラム | ドメイン分割（users→users+user_profiles+user_settings）、正規化 |
| **SD-02** | **Missing Primary Key（PK不在）** | テーブルにPKを定義しない | レプリケーション不能、UPDATE/DELETE の一意特定不可、ORM が動作しない | UUID or BIGSERIAL PK 必須化、既存テーブルには surrogate key 追加 |
| **SD-03** | **FK Orphan（外部キー孤児）** | FK制約なしでID参照カラムを作成 | 参照先が削除されても参照元が残る「ゴーストレコード」、データ不整合 | FK制約 + ON DELETE CASCADE/SET NULL、定期的な孤児レコード検出 |
| **SD-04** | **Wrong Data Type（誤ったデータ型）** | VARCHAR で日付・金額・真偽値を格納 | 日付ソートが文字列順、金額計算の丸め誤差、型変換コスト | DATE/TIMESTAMP 型、NUMERIC(precision,scale) for money、BOOLEAN 型を使用 |
| **SD-05** | **Wide Table（幅広テーブル）** | 150+カラムの水平肥大テーブル | INSERT 速度劣化、ページ分割多発、キャッシュ効率低下 | 垂直分割（頻度別テーブル分離）、JSONB for sparse attributes |
| **SD-06** | **Constraint Desert（制約砂漠）** | CHECK/NOT NULL/UNIQUE 制約なし | アプリ側でのみバリデーション、DB直接操作で不正データ混入 | DB レベルで制約定義（defense in depth）、CHECK 制約で値域制限 |
| **SD-07** | **Reserved Word Collision（予約語衝突）** | `user`, `order`, `group` 等をテーブル名に使用 | クエリでクォート必須、フレームワーク互換性問題、DB移行時のエラー | 複数形 or プレフィックス使用（`users`, `orders`, `app_groups`） |

---

## 2. データ型選択の判断基準

```
正しい型選択マトリクス:

  データ種別        | ❌ 誤った選択           | ✅ 正しい選択
  ----------------|----------------------|-------------------
  金額             | FLOAT, DOUBLE         | NUMERIC(12,2) / DECIMAL
  日付             | VARCHAR('2024-01-01') | DATE / TIMESTAMP WITH TIME ZONE
  真偽値           | INT(0/1), CHAR('Y/N')| BOOLEAN
  UUID             | VARCHAR(36)           | UUID 型（PostgreSQL native）
  メールアドレス     | TEXT（無制約）          | VARCHAR(254) + CHECK
  ステータス        | VARCHAR（自由文字列）    | ENUM 型 or CHECK 制約
  IPアドレス        | VARCHAR               | INET 型（PostgreSQL）
  JSON データ      | TEXT                  | JSONB（PostgreSQL）/ JSON

  原則:
    → セマンティクスに最も近い型を選択
    → DB エンジン固有の最適化を活用
    → 型によるバリデーションをDBレベルで保証
    → ストレージ効率も考慮（VARCHAR(36) vs UUID = 36B vs 16B）
```

---

## 3. 制約設計のベストプラクティス

```
制約のレイヤー戦略:

  Layer 1（DB 制約 — 最終防御線）:
    □ NOT NULL: 必須カラムに例外なく適用
    □ UNIQUE: ビジネスキー（email, slug 等）に適用
    □ FK: 参照整合性を DB レベルで保証
    □ CHECK: 値域制限（status IN ('active','inactive'), age > 0）
    □ DEFAULT: 合理的なデフォルト値の設定

  Layer 2（アプリ制約 — UX 向上）:
    □ バリデーション: ユーザーフレンドリーなエラーメッセージ
    □ フォーマット検証: メール、電話番号、URL
    □ ビジネスルール: 複雑な条件検証

  原則:
    → DB 制約 = データの整合性保証（絶対に破れない）
    → アプリ制約 = ユーザー体験の向上（エラーメッセージ等）
    → 両方必要（defense in depth）
    → DB 直接操作や別アプリからのアクセスでも制約が効く

  アンチパターン:
    ❌ アプリ側だけでバリデーション（DB 直接操作で破壊）
    ❌ 全カラム NOT NULL（nullable に意味がある場合もある）
    ❌ ON DELETE CASCADE の連鎖が深すぎる（予期しない大量削除）
    ❌ 制約名を自動生成のまま放置（デバッグ困難）
```

---

## 4. 命名規約

```
テーブル/カラム命名:

  テーブル名:
    ✅ 複数形 snake_case: users, order_items, user_profiles
    ❌ 単数形: user, order_item
    ❌ CamelCase: UserProfile, OrderItem
    ❌ 予約語: user, order, group, table, column
    ❌ 略語: usr, ord_itm, usr_prof

  カラム名:
    ✅ snake_case: created_at, first_name, is_active
    ✅ FK 命名: {参照テーブル単数}_id → user_id, order_id
    ✅ Boolean: is_* or has_* → is_active, has_verified
    ✅ 日時: *_at → created_at, updated_at, deleted_at
    ❌ 曖昧名: data, info, value, type, status2
    ❌ 冗長: user_user_name → user_name で十分

  インデックス命名:
    ✅ idx_{table}_{columns}: idx_users_email
    ✅ uniq_{table}_{columns}: uniq_users_email
    ✅ fk_{table}_{ref_table}: fk_orders_users

  制約命名:
    ✅ chk_{table}_{rule}: chk_users_age_positive
    ✅ pk_{table}: pk_users
```

---

## 5. テーブル設計チェックリスト

```
新規テーブル作成時:

  構造:
    □ PK 定義済み（UUID or BIGSERIAL）
    □ 全 FK に制約定義済み
    □ NOT NULL が適切に設定済み
    □ UNIQUE がビジネスキーに設定済み
    □ CHECK 制約で値域制限済み
    □ DEFAULT 値が適切に設定済み

  命名:
    □ テーブル名が複数形 snake_case
    □ カラム名が明確で自己文書化
    □ FK カラムが {ref_table}_id 形式
    □ 予約語を回避

  データ型:
    □ 日付は DATE/TIMESTAMP 型
    □ 金額は NUMERIC 型
    □ Boolean は BOOLEAN 型
    □ UUID は UUID 型
    □ JSONB は構造化できないデータにのみ使用

  運用:
    □ created_at / updated_at カラム存在
    □ soft delete が必要なら deleted_at カラム
    □ COMMENT ON で各テーブル・カラムの説明
    □ インデックス設計済み（別途 index-strategies.md 参照）
```

---

## 6. Schema との連携

```
Schema での活用:
  1. Model フェーズで SD-01〜07 のスクリーニング
  2. 新規テーブル設計時にチェックリスト適用
  3. 既存スキーマレビュー時にアンチパターン検出
  4. Tuner へのハンドオフ時にデータ型・制約の品質保証

品質ゲート:
  - カラム 50+ → 垂直分割提案（SD-01/SD-05 防止）
  - PK 未定義 → 即時修正（SD-02 防止）
  - FK 制約なしの *_id カラム → FK 追加提案（SD-03 防止）
  - VARCHAR で日付/金額格納 → 型変更提案（SD-04 防止）
  - CHECK/NOT NULL ゼロ → 制約追加提案（SD-06 防止）
  - 予約語テーブル名 → リネーム提案（SD-07 防止）
```

**Source:** [Levitation: Database Schema Design Anti-Patterns](https://levitation.in/blog/database-schema-design-anti-patterns/) · [DEV.to: Common Database Anti-Patterns](https://dev.to/kanani_nirav/common-database-anti-patterns-and-how-to-avoid-them-2kib) · [NumberAnalytics: Database Design Anti-Patterns](https://www.numberanalytics.com/blog/database-design-anti-patterns-to-avoid)
