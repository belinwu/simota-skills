# Fault Interaction Statistics & Coverage Adequacy

> NIST 実証データに基づく欠陥相互作用率、t-way カバレッジ効果、強度選択ガイド

## 1. 欠陥相互作用の実証データ

### NIST 研究の基本知見

```
ソフトウェア欠陥の大部分は1〜2つのパラメータの相互作用で発生し、
3つ以上の相互作用による欠陥は漸進的に減少する。
実際に観測された最大相互作用次数は 6。
```

### ドメイン別の相互作用分布

| ドメイン | 1-way | ≤2-way | ≤3-way | ≤4-way | ≤5-way | ≤6-way |
|---------|:-----:|:------:|:------:|:------:|:------:|:------:|
| 医療機器 | 66% | 97% | 99% | 100% | — | — |
| ブラウザ | — | 70% | 90% | 95% | 99% | 100% |
| サーバー | — | 76% | 95% | 99% | 100% | — |
| 一般ソフトウェア | — | 70-95% | 90-99% | 97-100% | — | — |

### 削減効果

```
研究結果サマリー:
  - 網羅テストと同等の欠陥検出率で 20X〜700X のテストセット削減
  - 10パラメータ×4値の 3-way: 全組み合わせ約100万 → 151テストでカバー
  - ランダム生成では 900+ テストが必要な同等カバレッジを 151 で達成
  - 一般的な Pairwise 適用で 85-95% のテストケース削減
  - 5-10% のテストケースで 80-90% の欠陥を検出（TestSigma調査）
```

---

## 2. t-way 強度の選択ガイド

### 強度別の特性

| 強度 | カバレッジ | テスト数増加率 | 典型的な欠陥検出率 | 適用場面 |
|------|----------|-------------|-----------------|---------|
| **2-way** (Pairwise) | 全2軸ペア | 基準 | 70-95% | 一般的なアプリケーション |
| **3-way** | 全3軸トリプル | 2-3倍 | 90-99% | 高品質要件 · 複雑な相互作用 |
| **4-way** | 全4軸クアッド | 3-5倍 | 97-100% | 安全クリティカル |
| **5-way+** | 全5軸以上 | 指数的増加 | 99-100% | 規制要件（DO-178C 等） |

### 強度選択フロー

```
強度選択の判断基準:
  ① 規制要件があるか？
     Yes → 規制が求める強度を適用（通常 4-way 以上）
     No → ②へ

  ② 安全クリティカルか（人命・金融・インフラ）？
     Yes → 3-way 以上（推奨: 4-way）
     No → ③へ

  ③ 過去の欠陥データで 3-way 以上の相互作用バグがあるか？
     Yes → 3-way（該当パラメータ群に適用）
     No → ④へ

  ④ テスト予算に余裕があるか？
     Yes → 2-way で開始し、欠陥が減るまで強度を上げる
     No → 2-way (Pairwise)
```

### 動的強度調整（推奨プロセス）

```
段階的強度エスカレーション:
  Step 1: 2-way (Pairwise) でテスト実行
  Step 2: 欠陥が検出される場合 → 3-way に引き上げ
  Step 3: 3-way で追加欠陥が検出される場合 → 4-way に引き上げ
  Step 4: t-way で追加欠陥がゼロ → t+1 で確認テスト → 確定

  停止条件: t-way テストで新規欠陥ゼロ かつ t+1 でも追加ゼロ
```

---

## 3. 混合強度テスト（Mixed-Strength）

### 概念

```
全パラメータに同一強度を適用するのではなく、
リスクレベルに応じて異なる強度を割り当てる戦略。

例:
  高リスクパラメータ群（認証 × 権限 × データ感度）→ 3-way
  中リスクパラメータ群（ブラウザ × OS）→ 2-way
  低リスクパラメータ群（言語 × テーマ）→ 1-way（各値最低1回）
```

### 効果

| 戦略 | テスト数 | カバレッジ | コスト効率 |
|------|---------|----------|----------|
| 全体 2-way | 基準 | 均一（中） | 良好 |
| 全体 3-way | 2-3倍 | 均一（高） | 中 |
| 混合強度（3+2+1） | 1.5-2倍 | 高リスク部は高 | 最良 |

---

## 4. カバレッジメトリクス

### 基本メトリクス

```
Variable-Value Configuration Coverage:
  Coverage(t) = (カバーされた t-way 組み合わせ数) / (全 t-way 組み合わせ数) × 100%

Tuple Density:
  TD = t + (カバーされた (t+1)-tuple 数) / (全 (t+1)-tuple 数)
  → t-way 100% 達成後の追加カバレッジを測定

Simple t-way Coverage:
  全 t-way 軸組み合わせで Configuration Coverage = 100% かを検証
```

### カバレッジ目標

| ドメイン | 最低 2-way | 推奨 | 備考 |
|---------|:--------:|:----:|------|
| 一般 Web アプリ | 100% | 2-way 100% | 標準 |
| 金融システム | 100% | 3-way 100% | 取引処理は 3-way 必須 |
| 医療機器 | 100% | 4-way 100% | 規制要件 |
| IoT/組込み | 100% | 3-way 100% | 環境変数が多い |
| セキュリティテスト | 100% | 混合強度 | 脅威関連パラメータは 3-way |

---

## 5. Matrix との連携

```
Matrix での活用:
  1. OPTIMIZE フェーズで欠陥データに基づく強度選択を適用
  2. domain パターンごとにデフォルト強度を推奨
     - test: 2-way（デフォルト）
     - risk: 2-way + 高リスク部 3-way
     - load: 2-way（パラメータ数が少ないため十分）
     - deploy: full（パラメータ数が少ないため全組み合わせ推奨）
     - compat: 2-way（LTS バージョンは require で強制）
  3. カバレッジレポートに t-way Coverage 率を必ず記載
  4. 混合強度テストの priority 軸を活用して強度を自動分類

品質ゲート:
  - 2-way Coverage < 100% の場合は警告
  - 安全クリティカルドメインで 2-way のみの場合は 3-way 以上を提案
  - 混合強度の場合、高リスクパラメータ群の Coverage を個別表示
```

**Source:** [NIST: Combinatorial Methods in Testing](https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software) · [NIST: Interactions Involved in Software Failures](https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software/combinatorial-methods-in-testing/interactions-involved-in-software-failures) · [NIST SP 800-142: Practical Combinatorial Testing](https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-142.pdf) · [NIST: Measuring Combinatorial Coverage](https://pmc.ncbi.nlm.nih.gov/articles/PMC5267492/) · [ISSTA 2024: Beyond Pairwise Testing](https://2024.issta.org/details/issta-2024-papers/52/Beyond-Pairwise-Testing-Advancing-3-wise-Combinatorial-Interaction-Testing-for-Highl)
