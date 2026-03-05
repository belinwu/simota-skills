# Refactoring Anti-Patterns

> リファクタリング時に陥りやすいアンチパターン、回避策、Zen での対策

## 1. プロセスアンチパターン

### ANTI-001: Big Bang Refactoring

```
定義: 大規模な一括書き換えを試みるパターン
症状: 「全部きれいにしよう」で数百〜数千行を一度に変更
影響: デバッグ困難、リグレッションリスク激増、レビュー不能

Zen の対策:
  - Scope tier 制限（Focused: 1-3 files, ≤50 lines）
  - 1 PR = 1 リファクタリング
  - Module/Project-wide は計画のみ（実行は Focused 単位で分割）
```

### ANTI-002: Refactoring Without Tests

```
定義: テストカバレッジなしにリファクタリングを実行
症状: 「動いてるから大丈夫」でテストを省略
影響: 動作変更に気づけない、サイレントバグ混入

Zen の対策:
  - BEFORE+AFTER テスト実行を必須化
  - カバレッジ < 80% の場合は Radar に先にテスト追加を委譲
  - Pre-Refactor Verification パターン（Zen → Radar → Zen）
```

### ANTI-003: Mixing Refactoring with Features

```
定義: 機能追加とリファクタリングを同一コミットに混在
症状: PR に「あ、ついでにここも整理しました」が混入
影響: レビュー困難、リグレッション原因の特定不能

Zen の対策:
  - リファクタリングコミットと機能コミットを厳密に分離
  - Guardian 連携: PR Noise Separation（Guardian → Zen → Guardian）
  - 動作変更は NEVER（Zen の絶対境界）
```

### ANTI-004: Perfectionism Over Progress

```
定義: 完璧なリファクタリングを追求し、本来の目的を見失う
症状: 「もうちょっとだけ」が無限に続く
影響: 機能デリバリー遅延、スコープクリープ

Zen の対策:
  - Boy Scout Rule: 「来た時より少しきれいに」（完璧ではない）
  - Scope tier による上限制限
  - 1 回 1 つの意味あるリファクタリングに集中
```

### ANTI-005: Underestimating Effort

```
定義: リファクタリングの工数を過小見積もり
症状: 「変数名変えるだけだから5分」→ 実際は影響範囲調査に数時間
影響: スケジュール遅延、中途半端な変更の放置

Zen の対策:
  - 必ず影響範囲を事前調査（Ripple 連携）
  - public API / exports の変更は「Ask first」に分類
  - Before/After レポートで変更範囲を可視化
```

---

## 2. 技術的アンチパターン

### ANTI-006: Golden Hammer

```
定義: 馴染みのあるパターンを全ての問題に適用
症状: 「とりあえず Strategy パターンで」「全部 Extract Method で」
影響: 過度な抽象化、不必要な複雑性の導入

Zen の対策:
  - レシピ選択は問題パターンに基づく（code-smells-metrics.md）
  - 「そのリファクタリングは本当に必要か？」を常に問う
  - 複雑性が増す場合はリファクタリングを中止
```

### ANTI-007: Premature Abstraction

```
定義: 再利用の可能性が不明なうちに共通化・抽象化
症状: 2回しか使われていないのに共通関数を作成
影響: 不要なインダイレクション、理解困難

判断基準:
  Rule of Three: 3回以上の重複を確認してから共通化
  Wrong Abstraction > No Abstraction: 間違った抽象化は重複より悪い

Zen の対策:
  - 「Small is beautiful」原則に基づき最小限の変更
  - 3行の類似コード × 2箇所 = まだ共通化しない
  - 3行の類似コード × 3箇所 = 共通化を検討
```

### ANTI-008: Speculative Generality (Boat Anchor)

```
定義: 将来必要になるかもしれないコードを先行して追加
症状: 「いつか使うかもしれないから残しておこう」
影響: デッドコード増加、メンテナンスコスト増大

Zen の対策:
  - YAGNI 原則の適用（Void エージェントと連携）
  - dead-code-detection.md のツールで検出
  - 未使用コードは積極的に削除
```

### ANTI-009: Shotgun Refactoring

```
定義: 1つのスメル修正が多数のファイルに波及する変更
症状: 変数名変更が 20 ファイルに影響
影響: レビュー困難、リグレッションリスク

Zen の対策:
  - Scope tier で変更範囲を制限
  - Module scope（4-10 files）は mechanical only
  - Project-wide（10+ files）は plan only → 段階実行
```

### ANTI-010: Copy-Paste Refactoring

```
定義: 他プロジェクトの「良いコード」をそのままコピー
症状: Stack Overflow のベストアンサーをそのまま適用
影響: コンテキスト不一致、既存パターンとの不整合

Zen の対策:
  - consistency-audit.md で既存パターンとの整合性チェック
  - プロジェクト固有の命名規則・パターンを優先
  - 「Follow project naming」原則
```

---

## 3. 認知バイアスとリファクタリング

| バイアス | 影響 | 対策 |
|---------|------|------|
| **確証バイアス** | 自分のリファクタリングが正しいと思い込む | Before/After メトリクスで客観評価 |
| **サンクコスト** | 時間をかけたリファクタリングを中止できない | 複雑性が増したら即座に revert |
| **計画の錯誤** | リファクタリング工数を楽観視 | Scope tier で上限制限 |
| **ハンマーの法則** | 得意なパターンを全てに適用 | 問題→レシピのマッピングを遵守 |

---

## 4. チェックリスト: リファクタリング前の確認

```
□ テストカバレッジは十分か？（< 80% なら Radar へ）
□ リファクタリングの目的は明確か？
□ Scope tier に収まるか？
□ 機能変更と混在していないか？
□ public API への影響はないか？
□ Before メトリクスを記録したか？
□ 既存パターンとの整合性は取れるか？
```

**Source:** [Tembo: Code Refactoring Mistakes](https://www.tembo.io/blog/code-refactoring) · [GeeksforGeeks: Anti-Patterns to Avoid](https://www.geeksforgeeks.org/blogs/types-of-anti-patterns-to-avoid-in-software-development/) · [BairesDev: Software Anti-Patterns](https://www.bairesdev.com/blog/software-anti-patterns/) · [Sahand Saba: 9 Anti-Patterns](https://sahandsaba.com/nine-anti-patterns-every-programmer-should-be-aware-of-with-examples.html)
