# Coverage Measurement & Adequacy

> カバレッジ計測手法、妥当性基準、実行後分析、継続的改善プロセス

## 1. カバレッジ測定の階層

### 3層カバレッジモデル

```
Layer 1: Pair Coverage（ペアカバレッジ）
  = カバーされた t-way ペア数 / 全 t-way ペア数 × 100%
  → Matrix の OPTIMIZE フェーズで保証する基本メトリクス

Layer 2: Configuration Coverage（構成カバレッジ）
  = テストセットがカバーする入力空間の割合
  → 全直積に対する最適化セットのカバー率

Layer 3: Fault Detection Effectiveness（欠陥検出効果）
  = テストセットで検出された欠陥数 / 全欠陥数
  → 実行後に遡及的に計測
```

---

## 2. カバレッジ不足の検出パターン

### 6つの警告サイン

| # | 警告サイン | 示唆する問題 | 対策 |
|---|----------|-----------|------|
| **CM-01** | **本番バグが Pairwise でカバー済みの組み合わせで発生** | パラメータモデリングの不備 · 値の粒度が粗い | 値の細分化 · パラメータ追加 |
| **CM-02** | **本番バグが未カバーの組み合わせで発生** | パラメータ漏れ · 制約による過剰除外 | パラメータモデルの拡張 · 制約の見直し |
| **CM-03** | **特定パラメータが過小テスト** | 制約やアルゴリズムの偏り | 分布検証 · パラメータ別カバレッジ率の確認 |
| **CM-04** | **3-way テストで大量の追加欠陥が発見** | 2-way では不十分な相互作用パターン | 高リスク領域を 3-way にエスカレーション |
| **CM-05** | **同一軸の値が偏って出現** | 生成アルゴリズムの偏り | バランス検証 · 直交配列の併用 |
| **CM-06** | **制約による除外が急増** | モデルと実システムの乖離 | 制約の棚卸し · 不要制約の削除 |

---

## 3. パラメータ別カバレッジ分析

### 分布均一性の検証

```
各パラメータの値が均等にテストされているか検証する。

検証方法:
  1. テストセット内の各値の出現回数をカウント
  2. 期待出現回数（テスト数 / 値数）との偏差を計算
  3. 偏差が 30% 以上の値を警告

例（9テストケース、browser 軸に 3値）:
  期待: 各値 3回
  実績: Chrome=5, Firefox=3, Safari=1
  → Safari が期待の 33%（偏差 67%）→ 警告

対策:
  - require 制約で過小テスト値を強制包含
  - 直交配列に切り替えてバランス保証
  - priority: high を設定して均等カバレッジを要求
```

---

## 4. 実行後分析（Post-Execution Analysis）

### 結果マッピングプロセス

```
実行後の 4 ステップ分析:

Step 1: 結果の回収
  - 各テストケースの Pass/Fail/Skip を収集
  - 失敗ケースの発見された欠陥を記録

Step 2: カバレッジ影響分析
  - 失敗ケースが担っていたペアカバレッジを特定
  - 失敗によって未検証となったペアをリストアップ
  - Skip ケースの影響も同様に分析

Step 3: 補完テストの提案
  - 未検証ペアをカバーする追加テストケースを生成
  - 最小追加数で未検証ペアをカバーする最適セットを計算

Step 4: モデル改善フィードバック
  - 発見された欠陥の相互作用次数を分析
  - 3-way 以上の欠陥が発見された場合 → 強度エスカレーション検討
  - パラメータモデルへの追加軸・値の候補を特定
```

### カバレッジ回復率

```
Coverage_Recovery = (回復済みペア数) / (失敗で未検証となったペア数) × 100%

目標:
  Critical ドメイン: 100%（全未検証ペアの補完テスト実施）
  Standard ドメイン: 80%（高リスクペアの補完のみ）
  Low-risk ドメイン: 50%（Critical ペアのみ補完）
```

---

## 5. 継続的カバレッジ改善

### イテレーション間のカバレッジトレンド

```
追跡すべきメトリクス:
  1. Pair Coverage 率のトレンド（イテレーションごと）
  2. 本番バグの Pairwise カバレッジ率（遡及分析）
  3. 補完テスト必要数のトレンド（減少していれば改善）
  4. パラメータモデルの変更頻度（安定していれば成熟）
  5. 欠陥の相互作用次数分布（2-way → 3-way シフトの兆候）

改善サイクル:
  Sprint N: テスト実行 → 結果回収
  Sprint N+1: 遡及分析 → モデル改善 → 再生成
  Sprint N+2: 改善モデルでテスト → 効果測定
```

### Escape Rate（検出漏れ率）

```
Escape_Rate = (本番で発見された欠陥のうちテストで検出すべきだったもの)
              / (全テスト対象欠陥) × 100%

目標:
  Escape_Rate < 5% → 良好（モデルが適切）
  Escape_Rate 5-15% → 要改善（パラメータ追加 or 強度引き上げ）
  Escape_Rate > 15% → モデル再設計（パラメータ特定からやり直し）
```

---

## 6. Matrix との連携

```
Matrix での活用:
  1. OPTIMIZE フェーズで Pair Coverage 100% を検証（既存）
  2. PLAN フェーズでパラメータ別分布均一性チェックを追加
  3. 実行後の Coverage Report（Template 6）に CM-01〜06 チェックを統合
  4. 結果マッピング時に未検証ペアの補完テスト案を自動生成
  5. イテレーション間のカバレッジトレンドを記録（journal に蓄積）

品質ゲート:
  - パラメータ値の出現偏差 > 30% で警告（CM-05 防止）
  - 失敗ケースによる未検証ペアがある場合は補完テストを必須提案
  - Escape_Rate > 5% でモデル改善を推奨
```

**Source:** [NIST: Measuring and Specifying Combinatorial Coverage](https://pmc.ncbi.nlm.nih.gov/articles/PMC5267492/) · [NIST: Combinatorial Coverage Measurement Concepts](https://csrc.nist.gov/CSRC/media/Presentations/Combinatorial-Coverage-Measurement-Concepts-and-Ap/images-media/kuhn-et-al-iwct13.pdf) · [Master Software Testing: Pairwise Testing Guide](https://mastersoftwaretesting.com/testing-fundamentals/types-of-testing/specialized-testing/pairwise-testing) · [TestSigma: Combinatorial Testing Guide](https://testsigma.com/blog/combinatorial-testing/)
