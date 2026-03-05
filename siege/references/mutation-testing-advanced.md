# Mutation Testing Advanced Strategies

> 等価ミュータント問題（ML/LLM 検出）、パフォーマンス最適化、リスクベース閾値、段階的 CI 統合

## 1. 等価ミュータント問題

### 概要

```
等価ミュータント (Equivalent Mutant):
  コードを変更しても動作が変わらないミュータント
  → どんなテストを書いても kill できない
  → Mutation Score の分母を膨張させ、精度を低下させる

研究データ (ISSTA 2024):
  - 7 つの Java プロジェクトの中央値: 等価ミュータント率 2.97%
  - プロジェクトによっては 10% 超のケースもあり
  - 開発者の大半が等価ミュータントの正確な識別に苦労

修正 Mutation Score:
  Score = Killed / (Total - Equivalent) × 100
```

### 等価ミュータントの典型パターン

| パターン | 例 | 理由 |
|---------|---|------|
| **Dead Code Mutation** | 到達不能コードの変更 | パスが実行されない |
| **Redundant Operation** | `x = x + 0` → `x = x - 0` | 結果が同じ |
| **Overflow Guard** | `if (n > MAX)` → `if (n >= MAX)` | MAX+1 が入力にならない |
| **Boolean Tautology** | `if (a \|\| !a)` の変更 | 常に true |
| **String Constant** | ログメッセージの変更 | 動作に影響なし |
| **Idempotent Call** | 冪等メソッドの重複呼出し変更 | 結果が同じ |

---

## 2. 検出手法の進化

### 従来手法

| 手法 | 精度 | 速度 | 特徴 |
|------|------|------|------|
| **手動検査** | 高 | 極低 | 開発者依存、スケールしない |
| **コンパイラ最適化** | 中 | 高 | 同一バイナリを生成するかで判定 |
| **制約解析 (TCE)** | 中-高 | 中 | 数学的に等価性を証明 |
| **プログラム解析** | 中 | 中 | 制御フロー/データフロー分析 |

### ML/AI ベース手法（2024-2025）

| 手法 | 精度 | 研究 | 特徴 |
|------|------|------|------|
| **ML 分類器** | F1: 87-94% | Pugh 2025 | 複数の ML モデルで等価/非等価を分類 |
| **EMS (10 分析手法)** | 高 | ISSTA 2024 | 10 種の効率的な分析を組み合わせた抑制手法 |
| **LLM 検出** | P:79% R:47% | Meta 2024 | LLM で等価性を推論、前処理で P:95% R:96% |
| **LLM + テスト生成** | — | Meta 2025 | 等価判定 + kill テスト自動生成の統合 |

```
Meta のアプローチ (2025):
  1. LLM が等価ミュータントをフィルタリング
  2. 残った非等価ミュータントに対し LLM がテスト生成
  3. エンジニアがレビュー・マージ
  → コンプライアンスカバレッジの改善に活用
```

---

## 3. パフォーマンス最適化

### 実行時間削減戦略

| 戦略 | 削減率 | 適用方法 |
|------|--------|---------|
| **Incremental Mutation** | 60-90% | 変更ファイルのみミュータント生成 |
| **Parallel Execution** | 線形向上 | `--threads=N` で並列実行 |
| **Coverage-Based Filtering** | 30-50% | カバレッジ未到達コードを除外 |
| **Operator Selection** | 20-40% | 不要なオペレーター無効化 |
| **Early Termination** | 10-30% | 最初のテスト失敗で次のミュータントへ |
| **Caching** | 20-40% | テスト結果のキャッシュ（影響のないミュータントをスキップ） |

### 段階的 CI/CD 統合

```
Tier 1 — PR/Commit (高速、必須):
  対象: 変更ファイルのみ
  オペレーター: 主要なもののみ（条件/境界/戻り値）
  閾値: 警告のみ（ブロックしない）
  時間: < 5 分

Tier 2 — Merge/Nightly (中速、推奨):
  対象: 変更モジュール全体
  オペレーター: 全オペレーター
  閾値: モジュール別閾値（下記参照）
  時間: < 30 分

Tier 3 — Weekly/Release (完全、必須):
  対象: 全コードベース
  オペレーター: 全オペレーター
  閾値: 全体スコア閾値
  時間: 制限なし（夜間/週末実行）
```

---

## 4. リスクベース閾値

### モジュール別 Mutation Score 基準

| リスクレベル | 対象モジュール例 | 最低スコア | 推奨スコア |
|------------|----------------|----------|----------|
| **CRITICAL** | 決済処理、認証、暗号化 | 85% | 95%+ |
| **HIGH** | ビジネスロジック、データ検証 | 75% | 85%+ |
| **MEDIUM** | API ハンドラ、ミドルウェア | 65% | 75%+ |
| **LOW** | ユーティリティ、ログ、設定 | 50% | 65%+ |
| **MINIMAL** | UI コンポーネント、テスト | — | 50%+ |

### リスク分類の自動化

```
分類ヒューリスティック:
  CRITICAL:
    - payment, billing, auth, crypto, security を含むパス
    - @critical アノテーション付き
  HIGH:
    - service, domain, model を含むパス
    - 外部 API 呼出しを含む
  MEDIUM:
    - controller, handler, middleware を含むパス
  LOW:
    - util, helper, config, logger を含むパス
  MINIMAL:
    - component, view, test を含むパス
```

---

## 5. ミューテーションテスト・アンチパターン

| # | アンチパターン | 症状 | 対策 |
|---|-------------|------|------|
| **MA-01** | **Big Bang Mutation** | 全コードベースに一度に実行 → CI タイムアウト | Incremental + Tier 別実行 |
| **MA-02** | **Score Obsession** | 100% を目指して等価ミュータント対策に時間浪費 | 等価ミュータントを除外した現実的な目標設定 |
| **MA-03** | **Assertion Inflation** | スコア向上のためだけに弱いアサーション追加 | Property-based testing で根本的に改善 |
| **MA-04** | **Uniform Threshold** | 全モジュールに同一閾値 | リスクベース閾値を適用 |
| **MA-05** | **Mutation Without Coverage** | カバレッジ低い状態でミューテーション実行 | まず 80%+ のカバレッジを達成してから |
| **MA-06** | **Ignoring Survivors** | サバイバーレポートを見ない | 各サバイバーを分類（等価/デッドコード/テスト不足）して対処 |
| **MA-07** | **Test-Only Mutation** | ミューテーション対策でテストだけ修正 | テストで検出した設計課題 → コードの分解・簡素化も |

---

## 6. Property-Based Testing との相乗効果

```
従来のテスト:
  expect(add(2, 3)).toBe(5);
  → ミュータント add(a, b) => a * b は kill できるが
  → ミュータント add(a, b) => a + b + 0 は kill できない

Property-Based Testing:
  forAll(int, int, (a, b) => {
    expect(add(a, b)).toBe(a + b);
    expect(add(a, b) - a).toBe(b);       // 逆操作
    expect(add(a, 0)).toBe(a);            // 単位元
    expect(add(a, b)).toBe(add(b, a));    // 可換性
  });
  → 数学的性質で多くのミュータントを自動 kill

相乗効果:
  1. ミューテーションテストで弱いテストを発見
  2. Property-Based Testing で根本的にカバレッジ向上
  3. 等価ミュータントの影響を最小化
```

---

## 7. Siege との連携

```
Siege の MUTATE モードでの活用:
  1. リスクベース閾値をモジュール別に適用
  2. 段階的 CI 統合 (Tier 1-3) を推奨
  3. サバイバー分析時に等価ミュータント判定を支援
  4. Property-Based Testing の導入を Radar にハンドオフ

Radar へのハンドオフ:
  - サバイバーリスト → テスト追加タスク
  - Property-Based Testing 導入提案
  - 等価ミュータント除外設定の推奨
```

**Source:** [ISSTA 2024: Equivalent Mutants in the Wild](https://dl.acm.org/doi/10.1145/3650212.3680310) · [Pugh 2025: ML Models for Equivalent Mutant Identification](https://onlinelibrary.wiley.com/doi/10.1002/stvr.70004) · [Meta: LLM Mutation Testing](https://www.infoq.com/news/2026/01/meta-llm-mutation-testing/) · [Stryker: Equivalent Mutants](https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/) · [Master Software Testing: Mutation Testing Guide 2025](https://mastersoftwaretesting.com/testing-fundamentals/types-of-testing/mutation-testing)
