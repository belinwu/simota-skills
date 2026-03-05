# BDD Anti-Patterns & Best Practices

> BDD シナリオ作成時の典型的なアンチパターンと回避策

## 1. プロセスのアンチパターン

### AP-001: Retrospective Scenarios（後付けシナリオ）

```
定義: 実装完了後に Gherkin シナリオを作成
症状: シナリオが「テストスクリプト」化し、要件としての機能を失う
影響: BDD の核心価値（共通理解の形成）が失われる

Attest の対策:
  - EXTRACT モードで事前にシナリオを生成し、実装前の合意形成を促進
  - Pre-Implementation Extraction チェーン（Accord → Attest → Builder/Radar）を活用
  - 「シナリオ先行」を推奨コメントとしてレポートに記載
```

### AP-002: Isolated Authoring（孤立した執筆）

```
定義: PO/BA が単独でシナリオを作成（Three Amigos 不実施）
症状: 技術的実現性の検証なし、テスト可能性が低い基準
影響: 実装時の認識齟齬、手戻り発生

Attest の対策:
  - AMBIGUOUS_FLAG で「Three Amigos レビュー推奨」を発行
  - テスタビリティが LOW の基準を自動検出し警告
  - Scribe/Accord への仕様改善ハンドオフで協議を促進
```

### AP-003: BDD as Testing Tool（テストツール誤認）

```
定義: BDD を QA テストツールとして扱い、仕様プロセスとして使わない
症状: QA チームが Gherkin を書く → テストスクリプト化
影響: ビジネス要件の共通理解が生まれない

Attest の対策:
  - 生成する BDD シナリオはビジネス言語で記述（技術用語を避ける）
  - シナリオの Given/When/Then がユーザー行動中心であることを検証
  - 実装詳細が混入したシナリオに警告を付与
```

---

## 2. シナリオ記述のアンチパターン

### AP-004: Incidental Details（付随的詳細）

```
定義: シナリオに本質と無関係な詳細を含める
症状: パスワード入力手順、UI 操作手順など不要な詳細が大量に記述
影響: ビジネスルールが埋もれる、メンテナンスコスト増大

Attest の対策:
  - シナリオ生成時に「行動の結果」にフォーカス
  - When ステップが 1 つの主要アクションに限定されることを検証
  - UI 操作ではなくユーザーゴールで記述
```

### AP-005: Multiple Rules per Scenario（複数ルール混在）

```
定義: 1 つのシナリオで複数のビジネスルールを検証
症状: Then が 5 つ以上、テスト失敗時にどのルールが原因か不明
影響: ドキュメント価値の低下、デバッグ困難

Attest の対策:
  - 1 シナリオ = 1 ビジネスルールを生成ルールとして厳守
  - 複合基準は自動分割（AC の「A かつ B」→ 別々のシナリオ）
  - criteria-extraction の compound requirement splitting と連携
```

### AP-006: Poor Scenario Titles（不明瞭なタイトル）

```
定義: シナリオタイトルが汎用的・コピペ・説明不足
症状: "Test Login" のような漠然としたタイトル
影響: シナリオの目的が不明、レビュー効率低下

Attest の対策:
  - タイトルに「the one where...」パターンを推奨
  - 基準 ID + ビジネスルールの要約を含むタイトル生成
  - 例: "SC-AC-LOGIN-001-HP-001: 有効な認証情報でダッシュボードにアクセスできる"
```

### AP-007: Given/When/Then Mixing（ステップ混同）

```
定義: 前提条件（Given）とアクション（When）を混同
症状: 複数の When ステップを And で連結、前提条件が When に記述
影響: テスト対象の行動が不明確、シナリオの意図が曖昧

Attest の対策:
  - Given: 状態の設定のみ（動詞は受動態・完了形）
  - When: 1 つの主要アクション（能動態）
  - Then: 検証可能な結果（観察可能な変化）
  - 生成時に構造検証を実施
```

---

## 3. カバレッジのアンチパターン

### AP-008: Over-Specification（過剰仕様化）

```
定義: 全コードパスをシナリオでカバーしようとする
症状: 数百のシナリオ、重複多数、メンテナンス不能
影響: 実行時間増大、メンテナンスコスト爆発

Attest の対策:
  - 優先度別の最小シナリオ数を遵守（CRITICAL:5, HIGH:3, MEDIUM:2, LOW:1）
  - 顧客が気にする正常系・異常系・境界値に絞る
  - bdd-generation.md の Coverage Matrix で適正量を管理
```

### AP-009: UI-Focused Testing（UI テスト偏重）

```
定義: すべてのシナリオを UI 操作ベースで記述
症状: ボタンクリック、フォーム入力の手順がシナリオの大半を占める
影響: UI 変更のたびに大量のシナリオが破壊、実行速度低下

Attest の対策:
  - シナリオはユーザージャーニー（意図）で記述
  - UI 詳細は実装レベル（Voyager/Radar）に委譲
  - "ユーザーがログインする" ≠ "メールフィールドに入力し、パスワードフィールドに入力し、ボタンをクリック"
```

### AP-010: Missing Negative Scenarios（ネガティブシナリオ欠落）

```
定義: ハッピーパスのみでネガティブ・エッジケースを無視
症状: エラー処理、異常系、境界値のシナリオがない
影響: 本番障害の主因（仕様外の入力・状態）を見逃す

Attest の対策:
  - 全 CRITICAL/HIGH 基準に最低 1 つのネガティブシナリオを必須化
  - adversarial-probing の 6 カテゴリと連動
  - Omission プローブで「仕様が忘れた失敗モード」を自動検出
```

---

## 4. ベストプラクティスチェックリスト

```
□ シナリオは実装前に作成されているか？
□ Three Amigos（PO + Dev + QA）で合意されているか？
□ 1 シナリオ = 1 ビジネスルールか？
□ ビジネス言語で記述されているか（技術用語なし）？
□ Given は前提条件、When は 1 アクション、Then は検証可能な結果か？
□ シナリオタイトルは目的を明確に表しているか？
□ ネガティブ・境界値シナリオが含まれているか？
□ UI 操作ではなくユーザーゴールで記述されているか？
□ 過剰なシナリオ数になっていないか（優先度別の上限を確認）？
□ シナリオはコードと同じリポジトリで管理されているか？
```

**Source:** [Cucumber Anti-Patterns (Part 1)](https://cucumber.io/blog/bdd/cucumber-antipatterns-part-one/) · [TestEvolve: BDD Best Practices](https://www.testevolve.com/blog/best-practices-and-anti-patterns-in-bdd-cucumber-automation-part-1) · [LinkedIn: BDD Pitfalls](https://www.linkedin.com/advice/1/how-do-you-deal-common-bdd-pitfalls) · [John Ferguson Smart: BDD Anti-Patterns](https://johnfergusonsmart.com/slidedecks/bdd-anti-patterns/) · [Thoughtworks: BDD Acceptance Criteria](https://www.thoughtworks.com/en-us/insights/blog/applying-bdd-acceptance-criteria-user-stories)
