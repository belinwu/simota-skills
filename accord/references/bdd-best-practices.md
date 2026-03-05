# BDD Acceptance Criteria Best Practices

> BDD シナリオの品質向上、12 の落とし穴、Three Amigos プラクティス、品質ゲート

## 1. BDD 12 の落とし穴

### シナリオ記述の落とし穴

| # | 落とし穴 | 問題 | 対策 |
|---|---------|------|------|
| **BDD-01** | **テストツール扱い** | BDD を QA ツールと誤解 → PO が書かず QA が書く | BDD はコラボレーションツール · PO が主導して記述 |
| **BDD-02** | **抽象的シナリオ** | 具体値なし → 検証不能（例: 「適切に表示される」） | Given/When/Then に具体的な値・数値を必須化 |
| **BDD-03** | **過剰詳細** | テストスクリプト化 → ビジネス文脈が消失 | 高レベルのユーザー行動に焦点 · 実装詳細は避ける |
| **BDD-04** | **DOM 依存シナリオ** | UI 要素（ボタン名、フォーム ID）を含む → 実装変更で壊れる | ビジネスドメイン言語で記述 · UI 抽象化 |
| **BDD-05** | **複数 When** | 1 シナリオに複数の When/And → テスト対象が不明確 | 1 シナリオ = 1 ユーザー行動 · 分割が必要 |
| **BDD-06** | **ビジネス価値欠如** | 技術検証のみ → 機能がビジネス成果を実現するか不明 | 各シナリオにビジネス価値を紐付け |

### プロセスの落とし穴

| # | 落とし穴 | 問題 | 対策 |
|---|---------|------|------|
| **BDD-07** | **Three Amigos 未実施** | 開発・テスト・ビジネスの協調的リファインメントなし | 3 チーム合同でシナリオ定義セッションを実施 |
| **BDD-08** | **仕様の陳腐化** | コード進化に伴いシナリオが未更新 → 不整合 | 仕様をソースコードと同リポジトリで管理 · CI ゲート |
| **BDD-09** | **事後記述** | 実装後にシナリオを書く → BDD の設計としての価値がゼロ | 実装前にシナリオを完成 · シナリオが設計の青写真 |
| **BDD-10** | **一律適用** | 全機能に同じ BDD フォーマットを強制 → 形式主義 | コンテキストに応じて柔軟に適用 · 原則を理解して進化 |
| **BDD-11** | **カバレッジ未計測** | シナリオ品質・カバレッジを測定しない | カバレッジ要件を CI ゲートに統合 |
| **BDD-12** | **AC と DoD の混同** | 全ユーザーストーリーに共通する品質基準を AC に記述 | AC = 機能固有の基準 · DoD = チーム共通の品質基準 |

---

## 2. Three Amigos プラクティス

### 概要

```
Three Amigos（3人の友人）:
  ビジネス（PO/BA）× 開発 × テスト が協働でシナリオを定義するプラクティス

目的:
  - 要件の共通理解を形成
  - 見落としやすいエッジケースを早期発見
  - 「誰かが後で決める」を排除

セッション構造:
  1. PO がユーザーストーリーの背景を説明（2分）
  2. 全員で Given/When/Then を協働記述（10-15分）
  3. テスト担当がエッジケースを提起（5分）
  4. 開発担当が技術的制約を共有（3分）
  5. 合意確認 → AC 確定
```

### Accord での適用

| Three Amigos の役割 | Accord のチーム | 責任 |
|-------------------|-------------|------|
| **ビジネス** | L2-Biz 担当 | Why の明確化 · ビジネスルール定義 |
| **開発** | L2-Dev 担当 | 技術的制約 · 実現可能性評価 |
| **テスト** | L3 BDD 担当 | エッジケース発見 · テスト可能性確認 |

---

## 3. BDD シナリオ品質チェックリスト

```
記述品質:
  □ Given は「状態」を記述しているか（動作ではなく）
  □ When は「1つの」ユーザーアクションか
  □ Then は「検証可能な」結果か（具体値あり）
  □ ビジネスドメイン言語で書かれているか（技術用語なし）
  □ 非技術者が読んで理解できるか

構造品質:
  □ 1 シナリオ = 1 ユーザー行動か
  □ 正常系と異常系の両方がカバーされているか
  □ 境界値・エッジケースが含まれているか
  □ REQ-XXX への紐付け（Linked）があるか

プロセス品質:
  □ 実装前に記述されたか（事後ではなく）
  □ 3 チーム（または Three Amigos）で合意されたか
  □ AC（機能固有）と DoD（共通品質）が分離されているか
```

---

## 4. BDD シナリオの良い例 / 悪い例

### 悪い例（アンチパターン）

```gherkin
# BDD-02: 抽象的すぎる
Given ユーザーがログインしている
When 検索する
Then 結果が適切に表示される    ← 「適切に」は検証不能

# BDD-04: DOM 依存
Given ユーザーが /login ページにいる
When #email-input に "test@example.com" を入力する    ← DOM 要素名
And #submit-btn をクリックする                        ← DOM 要素名
Then .dashboard-container が表示される                 ← DOM 要素名

# BDD-05: 複数 When
Given ユーザーが商品一覧にいる
When 商品Aをカートに追加する
And 商品Bをカートに追加する        ← 2つ目の When
And 注文確定ボタンを押す          ← 3つ目の When
Then 注文が完了する
```

### 良い例

```gherkin
# 具体的 + ビジネスドメイン + 1アクション
Scenario: AC-001 — 在庫切れ商品の注文を防止する — Linked: REQ-003
  Given 商品 "Premium Widget" の在庫が 0 個である
  When ユーザーが "Premium Widget" をカートに追加しようとする
  Then "在庫切れです" というメッセージが表示される
  And カートの商品数は変わらない

Scenario: AC-002 — 割引クーポン適用 — Linked: REQ-005
  Given ユーザーのカートに合計 10,000 円の商品がある
  And クーポン "SAVE20" が有効である
  When ユーザーがクーポン "SAVE20" を適用する
  Then 合計金額が 8,000 円に更新される
  And "20% 割引が適用されました" と表示される
```

---

## 5. Accord との連携

```
Accord での活用:
  1. L3 セクション記述時に品質チェックリストを自動適用
  2. BDD-01〜12 のアンチパターン検出を VERIFY フェーズに統合
  3. Three Amigos の原則を ALIGN フェーズのステークホルダー特定に適用
  4. UNIFY で BDD カバレッジ率と下流採用率（Radar/Voyager）を追跡
  5. 良い例/悪い例のパターンを ELABORATE 時のガイダンスとして提示

品質ゲート:
  - 具体値なしの Then は警告（BDD-02 防止）
  - 複数 When を検出したら分割提案（BDD-05 防止）
  - REQ-XXX リンクなしの AC は不完全とマーク（トレーサビリティ）
```

**Source:** [LinkedIn: BDD Pitfalls and Anti-Patterns](https://www.linkedin.com/advice/1/how-do-you-deal-common-bdd-pitfalls) · [Thoughtworks: BDD Acceptance Criteria](https://www.thoughtworks.com/en-us/insights/blog/applying-bdd-acceptance-criteria-user-stories) · [Parallel: Given-When-Then Best Practices](https://www.parallelhq.com/blog/given-when-then-acceptance-criteria) · [Kaizenko: 9 User Story Smells](https://www.kaizenko.com/9-user-story-smells-and-anti-patterns/) · [Dojo Consortium: BDD](https://dojoconsortium.org/docs/work-decomposition/behavior-driven-development/)
