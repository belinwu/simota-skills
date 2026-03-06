# Data Modeling Anti-Patterns

> データモデリングの失敗パターン、EAV・ポリモーフィック・正規化の罠

## 1. データモデリング 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **DM-01** | **EAV Abuse（EAV 濫用）** | Entity-Attribute-Value パターンの不適切な使用 | メタデータ検索に数分、型安全性なし、JOIN 地獄 | 専用カラム + JSONB for truly dynamic attributes、EAV は最終手段 |
| **DM-02** | **Polymorphic Association（ポリモーフィック関連の罠）** | `commentable_type` + `commentable_id` で複数テーブル参照 | FK 制約不可、孤児レコード（ゴースト）発生、型安全性なし | 専用 FK テーブル or STI（Single Table Inheritance）、UNION ALL ビュー |
| **DM-03** | **Over-Normalization（過剰正規化）** | 正規化を極限まで追求し JOIN 爆発 | 12テーブル JOIN の単純クエリ、レスポンス秒単位、fintech で $100K 損失事例 | 戦略的デノーマライゼーション、マテリアライズドビュー、読み取り専用レプリカ |
| **DM-04** | **Under-Normalization（正規化不足）** | 冗長データを複数テーブルに散在 | 顧客住所が orders/invoices/shipments に重複、更新漏れで不整合 | 3NF まで正規化、参照で共有、更新は単一箇所 |
| **DM-05** | **JSONB Everything（JSONB 万能薬）** | 構造化可能なデータを全て JSONB に格納 | スキーマレスで開発速度は速いが、クエリ最適化不能、型チェック不在 | 構造が安定したら専用カラムに昇格、JSONB は truly dynamic data のみ |
| **DM-06** | **Multi-Purpose Table（多目的テーブル）** | 1テーブルで複数エンティティを表現 | `type` カラムで分岐、NULL カラム多数、ビジネスロジックが type 依存 | テーブル分割 or STI（共通カラム+type 固有テーブル） |
| **DM-07** | **Temporal Blindness（時制盲目）** | 履歴データの設計を考慮しない | 現在値のみ保持、「先月の価格」が取得不能、監査要件に対応不可 | 履歴テーブル（*_history）、有効期間（valid_from/valid_to）、SCD Type 2 |

---

## 2. EAV パターンの判断基準

```
EAV（Entity-Attribute-Value）:

  構造:
    entity_id | attribute_name | attribute_value
    ---------|--------------|-----------------
    1        | color         | red
    1        | size          | large
    2        | weight        | 5.2

  適切な使用場面:
    ✅ 属性が動的で事前に定義不可能（ユーザー定義フィールド）
    ✅ 属性数がエンティティごとに大きく異なる（100+ 属性、使用率 < 10%）
    ✅ CMS のメタデータ、商品のカスタム属性
    ✅ 設定値の柔軟な管理

  不適切な使用場面:
    ❌ 属性が事前に定義可能（→ 専用カラム）
    ❌ 型安全性が必要（→ 専用カラム + CHECK）
    ❌ 属性間の関係性がある（→ 正規化テーブル）
    ❌ 頻繁な集計・ソート・フィルタ（→ パフォーマンス劣化）

  EAV → JSONB 移行の検討:
    → PostgreSQL JSONB は EAV の多くのユースケースを代替
    → GIN インデックスでクエリ高速化可能
    → JSON Schema バリデーション（CHECK 制約）で型安全性確保
    → ただし JSONB も万能ではない（DM-05 参照）

  JSONB の適切な使用:
    ✅ スキーマレスな属性（商品のカスタムフィールド）
    ✅ 外部 API レスポンスの一時保存
    ✅ 設定値・メタデータ
    ❌ 頻繁に JOIN/GROUP BY する構造化データ
    ❌ FK 参照が必要なデータ
    ❌ レポーティング対象のコアビジネスデータ
```

---

## 3. ポリモーフィック関連の代替パターン

```
問題の構造:

  -- ❌ ポリモーフィック（FK 制約不可）
  comments:
    id | commentable_type | commentable_id | body
    ---|-----------------|----------------|-----
    1  | Post            | 42             | ...
    2  | Photo           | 17             | ...

代替パターン:

  パターン A — 専用 FK テーブル:
    post_comments:
      id | post_id (FK) | body
    photo_comments:
      id | photo_id (FK) | body
    → FK 制約可能、型安全、ただしテーブル増加

  パターン B — 共通テーブル + Nullable FK:
    comments:
      id | post_id (FK, NULL) | photo_id (FK, NULL) | body
    + CHECK (num_nonnulls(post_id, photo_id) = 1)
    → FK 制約可能、参照先が少数の場合に有効

  パターン C — 中間テーブル:
    comments:
      id | body
    commentable_posts:
      comment_id (FK) | post_id (FK)
    commentable_photos:
      comment_id (FK) | photo_id (FK)
    → 完全な参照整合性、拡張性高い

  選択基準:
    参照先 2-3 種 → パターン B（シンプル）
    参照先 4+ 種 → パターン A or C
    Rails/Django 既存コード → 段階的にパターン B へ移行
```

---

## 4. 正規化 vs デノーマライゼーションの判断

```
バランスの取り方:

  正規化を進めるべき場面:
    → 更新頻度が高いデータ（顧客情報、在庫数）
    → データ整合性がビジネスクリティカル（金融、医療）
    → 複数箇所から参照されるマスタデータ

  デノーマライゼーションが有効な場面:
    → 読み取りが圧倒的に多い（99% 読み取り）
    → JOIN コストがボトルネック（5+ テーブル JOIN）
    → リアルタイム要件（ダッシュボード、検索）
    → 履歴スナップショット（注文時の商品名・価格）

  デノーマライゼーション戦略:
    1. マテリアライズドビュー: 集計結果のキャッシュ
    2. 計算カラム: 頻繁に計算する値の事前格納
    3. スナップショットカラム: 注文時の価格等の時点保存
    4. サマリーテーブル: 日次/月次集計の事前計算
    5. 読み取りレプリカ: 読み取り専用の非正規化コピー

  ⚠️ デノーマライゼーション時の必須事項:
    □ 更新戦略の明文化（トリガー/バッチ/イベント）
    □ 整合性チェックの自動化
    □ ソース・オブ・トゥルースの明示
    □ ADR（Architecture Decision Record）への記録
```

---

## 5. 時制データの設計パターン

```
Slowly Changing Dimension (SCD):

  Type 1 — 上書き（履歴なし）:
    users: name = 'New Name'  -- 旧値は消失
    → 履歴不要のマスタデータ向け

  Type 2 — 履歴行追加:
    user_history:
      id | user_id | name | valid_from | valid_to | is_current
    → 完全な履歴追跡、「あの時点の値」が取得可能
    → 行数増加、クエリに valid_to IS NULL 条件が必要

  Type 3 — 前回値カラム:
    users: name | previous_name | name_changed_at
    → 直前の値のみ必要な場合（限定的）

  イベントソーシング:
    user_events:
      id | user_id | event_type | payload (JSONB) | created_at
    → 全変更をイベントとして記録
    → 任意の時点のステートを再構築可能
    → 複雑だが監査要件が厳しい場合に有効

  選択基準:
    履歴不要          → Type 1
    直前値のみ        → Type 3
    完全履歴（期間別） → Type 2
    完全履歴（イベント）→ イベントソーシング
    監査要件（金融等） → Type 2 + イベントソーシング
```

---

## 6. Schema との連携

```
Schema での活用:
  1. Model フェーズで DM-01〜07 のスクリーニング
  2. EAV/JSONB の使用判断時に判断基準を適用
  3. ポリモーフィック関連の検出と代替パターン提案
  4. デノーマライゼーション決定時に ADR 記録を強制

品質ゲート:
  - EAV テーブル検出 → 代替手段（JSONB/専用カラム）提案（DM-01 防止）
  - *_type + *_id ペア → ポリモーフィック代替提案（DM-02 防止）
  - 5+ テーブル JOIN → デノーマライゼーション検討（DM-03 防止）
  - 同一データ 3+ テーブルに重複 → 正規化提案（DM-04 防止）
  - JSONB カラム 5+ → 構造化検討（DM-05 防止）
  - NULL 50%+ のテーブル → テーブル分割提案（DM-06 防止）
  - 履歴要件に *_history テーブルなし → SCD 提案（DM-07 防止）
```

**Source:** [Levitation: Database Schema Design Anti-Patterns](https://levitation.in/blog/database-schema-design-anti-patterns/) · [DBSchema: Data Modeling Anti-Patterns](https://dbschema.com/2024/12/11/data-modeling-anti-patterns/) · [NumberAnalytics: Database Design Anti-Patterns](https://www.numberanalytics.com/blog/database-design-anti-patterns-to-avoid)
