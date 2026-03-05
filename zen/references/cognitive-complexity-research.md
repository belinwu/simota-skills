# Cognitive Complexity Research & Metrics

> 認知的複雑度の最新研究、メトリクス比較、計測ツール、テスト対応メトリクス、実践的改善手法

## 1. 認知的複雑度 vs 循環的複雑度

| 観点 | 認知的複雑度 | 循環的複雑度 |
|------|------------|------------|
| **焦点** | コードの読みやすさ・理解のしやすさ | 実行パスの数・テスタビリティ |
| **測定対象** | 人間の認知的努力 | 分岐点の数 |
| **ネスト感度** | あり（深いネスト = 高スコア） | なし（ネスト深度を考慮しない） |
| **用途** | リーダビリティ改善の優先順位 | テストケース数の見積もり |
| **研究知見** | 理解しやすさの「中程度の」予測因子 | テストの複雑さの指標 |

### 研究結果: 216 人のジュニア開発者による実証研究

```
ScienceDirect (2023):
  - 認知的複雑度はコード理解しやすさの「中程度に許容できる精度」の予測因子
  - 循環的複雑度より人間の理解困難度をよく反映
  - ただし完全な予測因子ではない（ドメイン知識、個人差の影響大）
```

---

## 2. 複雑度メトリクス一覧

### 主要メトリクス

| メトリクス | 説明 | しきい値 | ツール |
|-----------|------|---------|--------|
| **Cognitive Complexity** | ネスト・制御フローの理解困難度 | 0-5: 低 / 6-10: 中 / 11-15: 高 / 16+: 危険 | SonarQube, ESLint |
| **Cyclomatic Complexity** | 分岐点の数 | 1-10: 低 / 11-20: 中 / 21-50: 高 / 50+: 危険 | SonarQube, ESLint, PMD |
| **Halstead Measures** | 演算子・被演算子から計算する Volume/Effort/Time | context 依存 | Radon, CodeMR |
| **Maintainability Index** | 複合指標（CC + Halstead + LOC） | 0-9: 高リスク / 10-19: 中 / 20-100: 良好 | VS Code Analysis, SonarQube |
| **Nesting Depth** | 最大ネスト深度 | 1-2: 低 / 3: 中 / 4: 高 / 5+: 危険 | ESLint (max-depth) |

### 補助メトリクス

| メトリクス | 説明 | 目標値 |
|-----------|------|--------|
| **Code Churn Rate** | コミット直後の頻繁な書き換え回数 | 3回以下 |
| **PR Size** | 変更行数 | 200-400 LOC |
| **Change Failure Rate** | 変更後の障害率 | < 15%（エリートチーム） |
| **Time to Review** | レビュー完了までの時間 | < 24-48 時間 |

---

## 3. テスト対応認知的複雑度 (CCTR)

### 2025年の最新研究

```
問題:
  - PMD の Cognitive Complexity は LLM 生成テストの 99%+ にゼロスコア付与
  - EvoSuite 出力にも控えめなスコアのみ
  - 実際のテストスイートは非自明なアサーションを含むのにゼロ評価

CCTR (Test-Aware Cognitive Complexity):
  新メトリクスの特徴:
    - 構造的特徴 + 意味的特徴を統合
    - アサーション密度を考慮
    - アノテーション役割を評価
    - テスト構成パターンを分析
    - 構造化 vs 断片化テストスイートを効果的に識別
```

### Zen での活用

```
テストリファクタリング時の補助指標として:
  - 構造的複雑度（従来 CC）+ テスト特有複雑度（CCTR）
  - test-refactoring.md のスメル検出を補完
  - テストコードの「読みやすさ」をより正確に評価
```

---

## 4. 認知的複雑度の原因と改善

### 8 大原因

| # | 原因 | 説明 | 対策 |
|---|------|------|------|
| 1 | **過剰な条件分岐** | if/else/switch の多用 | Guard Clauses, Strategy Pattern |
| 2 | **深いネスト** | 4 段以上のネスト | Early Return, Extract Method |
| 3 | **不明瞭な命名** | 曖昧な変数名・関数名 | Explaining Variable, Rename |
| 4 | **密結合** | コンポーネント間の過度な依存 | Interface 分離, DI |
| 5 | **巨大関数/クラス** | 数百行の関数 | Extract Method, SRP |
| 6 | **不整合な規約** | 混在する命名スタイル | consistency-audit.md |
| 7 | **本質的複雑性** | 問題自体が複雑 | 適切な抽象化（過度でなく） |
| 8 | **不慣れなコードベース** | 94% の開発者が影響 | ドキュメント、命名改善 |

### 改善手法の研究知見

```
287,813 リファクタリング操作の分析:
  - 57.8% がコードの簡素化に焦点
  - 意味のある名前が理解度を有意に改善（25 コード特徴の研究）
  - セルフドキュメンティングコードが過剰コメントより効果的

58% の開発者が可読性の高いコードの書き方について
正式な教育を受けていない
```

---

## 5. Zen の複雑度改善ワークフロー

```
Step 1: 計測（Before）
  → SonarQube / ESLint で CC + Cognitive 計測
  → ベースラインを Before/After レポートに記録

Step 2: 原因特定
  → 上記 8 大原因のどれに該当するか分類
  → code-smells-metrics.md のスメルカテゴリと照合

Step 3: レシピ選択
  → refactoring-recipes.md から適切なレシピを選択
  → 1 回 1 つのレシピに集中

Step 4: 適用
  → Scope tier 内で変更
  → テスト実行で動作不変を確認

Step 5: 計測（After）
  → 同一メトリクスで再計測
  → 改善を定量的に確認（目標: CC 15-25% 削減）
```

---

## 6. ツール設定リファレンス

### ESLint

```json
{
  "rules": {
    "complexity": ["warn", 15],
    "max-depth": ["warn", 4],
    "max-lines-per-function": ["warn", 50],
    "max-params": ["warn", 5]
  }
}
```

### SonarQube

```
sonar.cognitive_complexity.threshold=15
sonar.complexity.threshold=20
```

### Python (Radon)

```bash
radon cc src/ -a -nc    # 循環的複雑度
radon mi src/ -s        # メンテナンス性インデックス
radon hal src/          # Halstead メトリクス
```

**Source:** [ScienceDirect: Cognitive Complexity as Predictor](https://www.sciencedirect.com/science/article/abs/pii/S0164121222002370) · [Arxiv: Rethinking Cognitive Complexity for Unit Tests (CCTR)](https://www.arxiv.org/abs/2506.06764) · [Axify: Cognitive Complexity Explained](https://axify.io/blog/cognitive-complexity) · [DX: Cognitive Complexity in Engineering](https://getdx.com/blog/cognitive-complexity/) · [Arxiv: How Developers Improve Code Readability](https://arxiv.org/pdf/2309.02594)
