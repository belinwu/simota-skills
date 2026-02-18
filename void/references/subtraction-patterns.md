# Subtraction Patterns Reference — Void

6削減パターン定義・適用条件・Before/After事例。

---

## Pattern Overview

| # | Pattern | Target Category | Typical CoK Range | Description |
|---|---------|----------------|-------------------|-------------|
| 1 | **Feature Sunset** | Feature | 6-10 | 機能全体の段階的廃止 |
| 2 | **Abstraction Collapse** | Abstraction | 5-10 | 不要な抽象化層の除去・平坦化 |
| 3 | **Scope Cut** | Scope | 4-8 | 機能の対応範囲を縮小 |
| 4 | **Pattern Simplification** | Abstraction | 4-8 | 過剰な設計パターンの簡素化 |
| 5 | **Dependency Elimination** | Dependency | 3-10 | 外部依存の除去・内製化 |
| 6 | **Configuration Reduction** | Configuration | 3-7 | 設定項目の削減・デフォルト化 |

---

## 1. Feature Sunset

**定義:** ユーザーが直接操作する機能を段階的に廃止する。

**適用条件:**
- 使用率が低い（DAUの5%未満）
- 代替手段が存在する
- メンテナンスコストが提供価値を超えている

**段階:**
```
1. ANNOUNCE  — 廃止予告。代替手段を提示
2. DEPRECATE — 非推奨マーク。新規利用を停止
3. MIGRATE   — 既存ユーザーの移行支援
4. REMOVE    — コード削除
```

**Before/After:**
```
Before: 5種類のエクスポート形式（CSV, JSON, XML, YAML, PDF）
  → XML使用率0.3%, YAML使用率0.1%, PDF使用率1.2%

After: 2種類のエクスポート形式（CSV, JSON）
  → 3フォーマットのパーサー/テスト/ドキュメント削除
  → テスト実行時間 -15%, メンテナンス工数 -40%
```

---

## 2. Abstraction Collapse

**定義:** 具象クラスが1-2個しかない抽象化層を除去し、直接実装に置き換える。

**適用条件:**
- インターフェース/基底クラスの実装が1-2個のみ
- 「将来の拡張性のため」に作られたが拡張されていない
- 抽象化が理解を妨げている

**判定ルール:**
```
実装数 = 1  → ほぼ確実にCollapse対象
実装数 = 2  → 両方が常にペアで使われるならCollapse候補
実装数 >= 3 → Collapseは不適切（正当な抽象化の可能性高い）
```

**Before/After:**
```
Before:
  INotificationService (interface)
    └── EmailNotificationService (唯一の実装)
    └── NotificationServiceFactory
    └── NotificationServiceConfig

After:
  sendEmailNotification(to, subject, body) (単一関数)
  → 3ファイル削除、テスト簡素化、DI設定不要に
```

---

## 3. Scope Cut

**定義:** 機能の対応範囲（バリエーション・オプション）を絞り込む。

**適用条件:**
- 80/20ルール: 全バリエーションの20%が使用の80%を占める
- 稀にしか使われないオプションのメンテナンスコストが高い
- エッジケース対応が本体より複雑になっている

**分析テンプレート:**
```yaml
scope_analysis:
  total_variations: X
  usage_distribution:
    - { variation: "A", usage_percent: 65, maintenance_cost: LOW }
    - { variation: "B", usage_percent: 25, maintenance_cost: LOW }
    - { variation: "C", usage_percent: 7, maintenance_cost: HIGH }
    - { variation: "D", usage_percent: 3, maintenance_cost: CRITICAL }
  cut_candidates: ["C", "D"]
  kept_coverage: "90%"
  maintenance_reduction: "60%"
```

**Before/After:**
```
Before: 12種類の日付フォーマット対応
After:  4種類（ISO 8601, locale default, relative, custom format string）
  → 8パターンのパーサー/バリデーション削除
  → バグ報告 -70%（エッジケース起因のバグが大半だった）
```

---

## 4. Pattern Simplification

**定義:** 過剰な設計パターン（over-engineering）を簡素な実装に置き換える。

**適用条件:**
- パターン適用のコンテキストが小規模（数百行以下）
- パターンの複雑さが問題の複雑さを超えている
- 「教科書通り」のパターン適用が可読性を損なっている

**典型的なSimplification対象:**

| Over-engineering | Simplification |
|-----------------|---------------|
| Strategy Pattern（実装2個） | if/else or switch |
| Observer Pattern（リスナー1個） | 直接呼び出し |
| Builder Pattern（パラメータ3個） | コンストラクタ引数 |
| Event-driven（同期処理） | 関数呼び出し |
| Microservice（月間100リクエスト） | モジュール/ライブラリ |

**Before/After:**
```
Before: 
  Command Pattern with CommandHandler, CommandDispatcher, 
  CommandValidator, CommandResult (4 classes, 200 lines)
  → 実際のコマンドは3種類のみ

After:
  3つの関数: createUser(), updateUser(), deleteUser() (60 lines)
  → 140行削減、テスト数 -50%、理解時間 -80%
```

---

## 5. Dependency Elimination

**定義:** 外部ライブラリ/サービスへの依存を除去する。

**適用条件:**
- ライブラリの使用機能が全体の10%未満
- ネイティブAPI/標準ライブラリで代替可能
- セキュリティ脆弱性が頻繁に報告される
- メンテナンスが停止/不活発

**判定マトリクス:**

| 使用率 | 代替容易性 | 推奨 |
|--------|----------|------|
| < 10% | 高い | ELIMINATE（即時） |
| < 10% | 低い | ELIMINATE（段階的） |
| 10-50% | 高い | ELIMINATE候補（コスト対効果検討） |
| 10-50% | 低い | KEEP-WITH-WARNING |
| > 50% | — | KEEP（正当な依存） |

**Before/After:**
```
Before: lodash（使用: _.get, _.debounce, _.cloneDeep のみ）
After: 
  - optional chaining (?.) で _.get を代替
  - 自前debounce関数（10行）
  - structuredClone() で _.cloneDeep を代替
  → node_modules -2MB, バンドルサイズ -70KB
```

---

## 6. Configuration Reduction

**定義:** 設定項目を削減し、合理的なデフォルト値で固定する。

**適用条件:**
- 設定項目の80%がデフォルト値のまま使用されている
- 設定の組み合わせが予測不能な動作を生む
- 設定ドキュメントの維持コストが高い

**分析アプローチ:**
```yaml
config_analysis:
  total_options: X
  default_usage_rate:
    - { option: "timeout", default_rate: "98%", action: "HARDCODE" }
    - { option: "retries", default_rate: "95%", action: "HARDCODE" }
    - { option: "theme", default_rate: "60%", action: "KEEP" }
    - { option: "language", default_rate: "40%", action: "KEEP" }
  candidates_for_removal: ["timeout", "retries"]
  remaining_options: ["theme", "language"]
```

**Before/After:**
```
Before: 24の環境変数、15のconfig.yamlオプション
After:  8の環境変数、5のconfig.yamlオプション
  → 設定ドキュメント -60%, 設定起因のバグ -80%
  → デフォルト値で98%のユースケースをカバー
```

---

## Pattern Selection Guide

```
CoK Score算出後の削減パターン選択フロー:

1. 対象カテゴリを確認（evaluation-criteria.md の分類）
2. カテゴリ → パターンマッピング:
   Feature       → Feature Sunset
   Abstraction   → Abstraction Collapse or Pattern Simplification
   Scope         → Scope Cut
   Dependency    → Dependency Elimination
   Configuration → Configuration Reduction
3. 適用条件を確認
4. blast radius を評価
5. 段階的アプローチを設計
```
