# DNA Dimensions Reference — Totem

8次元の詳細分析ガイド、スコアリング基準、言語別バリエーション、サブカルチャー。

---

## Dimension N: Naming

### What to Measure

- **Variable naming**: camelCase / snake_case / PascalCase 使用率
- **Function naming**: 動詞パターン（get/set/is/has/create/update/delete/handle）
- **File naming**: kebab-case / PascalCase / flat / dot-separated
- **Constant naming**: SCREAMING_SNAKE_CASE 使用率
- **Abbreviation patterns**: 省略形の一貫性（msg vs message, btn vs button, req vs request）
- **Boolean naming**: is/has/can/should プレフィクス使用率
- **Type/Interface naming**: I-prefix, T-prefix, -able suffix パターン

### Scoring Rubric (0-3)

| Score | Criteria |
|-------|----------|
| **0** | パターンなし。ケース混在、動詞規約なし、省略形が不統一 |
| **1** | 主要ケース規約は存在するが30%以上の例外あり |
| **2** | 一貫したケース使用、動詞パターン確立、例外 < 10%（すべて説明可能） |
| **3** | 名前が自己文書化。コード読解にコメント不要 |

### Language-Specific Notes

| Language | Default Case | Function Pattern | Notes |
|----------|-------------|-----------------|-------|
| **JavaScript/TypeScript** | camelCase | verb + noun | React: handleClick, useState, useMemo |
| **Python** | snake_case | verb_noun | クラスは PascalCase、定数は SCREAMING |
| **Go** | exported: PascalCase, unexported: camelCase | verb + noun | 短い名前を好む文化（r, w, ctx） |
| **Rust** | snake_case | verb_noun | 型は PascalCase、定数は SCREAMING_SNAKE |
| **Ruby** | snake_case | verb_noun? | クラスは PascalCase、述語は ? suffix |
| **Java** | camelCase | verbNoun | クラスは PascalCase、定数は SCREAMING |
| **C#** | PascalCase (public), camelCase (private) | VerbNoun | Interface は I-prefix |

### Evidence Collection

```yaml
evidence_methods:
  - method: "grep for naming patterns"
    command: "count camelCase vs snake_case occurrences in variable declarations"
  - method: "function name analysis"
    command: "extract all function/method names, classify verb patterns"
  - method: "file name analysis"
    command: "glob all source files, classify naming convention"
  - method: "percentage calculation"
    formula: "dominant_pattern_count / total_count × 100"
```

### Subculture Awareness

- **Test files**: describe/it ブロック、テスト固有の命名（mockXxx, stubXxx）
- **Config files**: 固有の規約（kebab-case keys, dot.separated.keys）
- **Generated code**: 自動生成ファイルは除外対象
- **Framework-mandated**: React hooks（use-prefix）、Go exported（PascalCase）

---

## Dimension A: Abstraction

### What to Measure

- **DRY threshold**: 何回繰り返しで抽出するか（2回？3回？）
- **Helper extraction patterns**: ユーティリティ関数の作成傾向
- **Inheritance vs Composition**: 継承の深さ、コンポジション使用率
- **Abstraction depth**: 平均呼び出し階層の深さ
- **Generic/Template usage**: ジェネリクスの使用頻度と複雑度
- **Interface count**: インターフェース定義数 vs 実装数の比率

### Scoring Rubric (0-3)

| Score | Criteria |
|-------|----------|
| **0** | 抽象化の哲学なし。一部は過剰抽象化、他はコピペ |
| **1** | 傾向は見えるが適用が不統一 |
| **2** | 明確な暗黙の閾値あり。チーム全体で似たタイミングで抽出 |
| **3** | 抽象化レベルが複雑度に完全一致。早すぎず遅すぎない |

### Indicators

| Indicator | How to Measure | Healthy Range |
|-----------|---------------|---------------|
| Abstract class count | grep for abstract/ABC | 全クラスの < 15% |
| Interface-to-class ratio | count interfaces vs implementations | 0.3 - 1.0 |
| Average function length | LOC per function distribution | 5-25 lines (median) |
| Utility file patterns | count files named util/helper/common | < 5% of total files |
| Max inheritance depth | AST analysis | <= 3 levels |
| Code duplication rate | similar block detection | < 5% |

### Abstraction Philosophy Spectrum

```
MINIMAL ←─────────────────────────→ MAXIMAL
"Repeat 3x    "Extract at 2x     "Abstract
 before         repetition"        everything
 extracting"                       upfront"
```

---

## Dimension E: Error Handling

### What to Measure

- **Error message tone**: 技術的 / ユーザーフレンドリー / 混在
- **Error handling patterns**: try-catch / Result type / error codes / panic
- **Error propagation strategy**: wrap & rethrow / transform / swallow / bubble up
- **Logging level conventions**: error/warn/info/debug の使い分け基準
- **Custom error types**: 独自エラー型の定義頻度と構造
- **Recovery patterns**: retry / fallback / circuit breaker の使用

### Scoring Rubric (0-3)

| Score | Criteria |
|-------|----------|
| **0** | 混沌。catch-all、空の catch、console.log 混在、エラー握りつぶし |
| **1** | 主要パターンは存在するが、エラーの伝播方法が不統一 |
| **2** | 一貫したパターン。エラー型定義、伝播方法、ログレベルが統一 |
| **3** | エラーが文書として機能。エラーメッセージだけで原因・対処法がわかる |

### Language-Specific Patterns

| Language | Idiomatic Pattern | Anti-Pattern |
|----------|-------------------|-------------|
| **TypeScript** | Custom Error classes + type guards | any in catch, untyped throws |
| **Python** | Custom exceptions hierarchy + context managers | bare except, pass in except |
| **Go** | errors.Is/As, fmt.Errorf wrapping | _ = err, panic for non-fatal |
| **Rust** | Result<T,E>, ? operator, thiserror/anyhow | unwrap() in library code |
| **Java** | Checked vs Unchecked hierarchy | catch(Exception e) everywhere |

---

## Dimension C: Comments

### What to Measure

- **Comment density**: コメント行数 / 総コード行数（比率）
- **Style**: "why" vs "what" vs 両方
- **JSDoc/docstring usage**: public API へのドキュメント付与率
- **TODO/FIXME conventions**: フォーマット統一度（TODO(name): vs TODO: vs FIXME）
- **Inline vs block**: インラインコメントとブロックコメントの比率
- **Language**: コメント言語（英語 / 日本語 / 混在）

### Scoring Rubric (0-3)

| Score | Criteria |
|-------|----------|
| **0** | 混沌。コメントアウトされたコード、"what" コメントの氾濫、古いコメント放置 |
| **1** | Public API にはドキュメントあり。内部コメントは不統一 |
| **2** | 統一された "why" コメント方針。TODO フォーマット統一。古いコメント少数 |
| **3** | 精密な "why-only" 哲学。コメントは非自明な制約・根拠のみ。コード自体が文書 |

### Comment Density Benchmarks

| Density | Interpretation |
|---------|---------------|
| < 5% | ミニマリスト（コード自体が語る or ドキュメント不足） |
| 5-15% | 健全な範囲 |
| 15-25% | やや多め（"what" コメントが多い可能性） |
| > 25% | 過剰（コメントアウトされたコード含む可能性） |

---

## Dimension T: Testing

### What to Measure

- **Test naming conventions**: should.../describe-it/test_verb_noun/given-when-then
- **Test structure**: AAA (Arrange-Act-Assert) / GWT (Given-When-Then) / 混在
- **Fixture patterns**: factory / builder / fixture files / inline
- **Mock philosophy**: minimal mocking / heavy mocking / test doubles分類
- **Coverage expectations**: 暗黙的なカバレッジ目標
- **Test file organization**: co-located / separate __tests__ / test/ directory

### Scoring Rubric (0-3)

| Score | Criteria |
|-------|----------|
| **0** | テスト不統一。命名バラバラ、構造不明、スキップ多数 |
| **1** | テスト存在するが構造がチーム内で異なる |
| **2** | 統一された命名・構造。モック方針が明確。カバレッジ目標あり |
| **3** | テストが仕様として機能。テストを読めば仕様書不要 |

### Test Organization Patterns

| Pattern | Structure | Common In |
|---------|----------|-----------|
| **Co-located** | src/foo.ts + src/foo.test.ts | React, modern JS/TS |
| **Mirror tree** | src/foo.ts + test/foo_test.go | Go, Java |
| **__tests__ dir** | src/foo.ts + src/__tests__/foo.test.ts | Jest default |
| **Spec dir** | lib/foo.rb + spec/foo_spec.rb | Ruby/RSpec |

---

## Dimension R: Architecture

### What to Measure

- **Module boundary patterns**: 明確な境界線の有無
- **Dependency direction rules**: Clean Architecture / Hexagonal / ad-hoc
- **Layer naming**: controllers/services/repositories vs handlers/usecases/adapters
- **Import patterns**: 相対 vs 絶対、barrel exports、circular dependency
- **Entry point patterns**: index.ts re-exports, __init__.py, mod.rs

### Scoring Rubric (0-3)

| Score | Criteria |
|-------|----------|
| **0** | 混沌。循環依存、レイヤー境界なし、god objects/files |
| **1** | ディレクトリ構造はあるが、依存方向が一貫しない |
| **2** | 明確なレイヤー構造、依存方向ルール、境界違反 < 10% |
| **3** | 自明な構造。新しいファイルの配置先が構造から自動的にわかる |

### Architecture Pattern Detection

| Pattern | Indicators |
|---------|-----------|
| **Clean Architecture** | domain/ + application/ + infrastructure/ + presentation/ |
| **Hexagonal** | ports/ + adapters/ + core/ |
| **MVC** | models/ + views/ + controllers/ |
| **Feature-based** | features/auth/ + features/billing/ (各内部にlayer) |
| **Flat** | すべてがルートまたは1層のディレクトリ |

---

## Dimension G: Git

### What to Measure

- **Commit message format**: conventional commits / free-form / prefix-based / Jira ID
- **PR title conventions**: format, length, language
- **Branch naming**: feature/xxx, fix/xxx, chore/xxx vs free-form
- **Squash vs merge strategy**: squash merge / merge commit / rebase
- **Commit granularity**: atomic (1 logical change) / batch / WIP commits

### Scoring Rubric (0-3)

| Score | Criteria |
|-------|----------|
| **0** | 混沌。"fix", "update", "wip" のみ。ブランチ名不統一 |
| **1** | 主要フォーマットは存在するが50%以上が非準拠 |
| **2** | 統一されたフォーマット。ブランチ命名規約あり。PR テンプレート使用 |
| **3** | コミット履歴がストーリーを語る。git log だけで変更の経緯がわかる |

### Commit Message Analysis

```yaml
analysis_method:
  sample: "直近 100 commits"
  classify:
    - conventional: "^(feat|fix|docs|style|refactor|test|chore|ci|perf|build)(\\(.+\\))?: .+"
    - prefix_based: "^\\[.+\\] .+"
    - jira_id: "^[A-Z]+-\\d+ .+"
    - free_form: "上記いずれにも該当しない"
  calculate:
    - dominant_format: "最多パターン"
    - adherence_rate: "dominant_count / total × 100"
```

---

## Dimension D: Dependencies

### What to Measure

- **Dependency minimalism vs maximalism**: 外部ライブラリへの依存度
- **Version pinning strategy**: exact / caret / tilde / range
- **Vendoring patterns**: vendor/ 使用有無
- **Upgrade frequency**: 依存関係の更新頻度（Renovate/Dependabot 設定）
- **Internal vs external preference**: 自前実装 vs ライブラリ使用の判断基準

### Scoring Rubric (0-3)

| Score | Criteria |
|-------|----------|
| **0** | ポリシーなし。無計画な依存追加、ピン留めなし、セキュリティ更新放置 |
| **1** | 暗黙のポリシーあり。主要依存は管理されているが周辺は野放し |
| **2** | 明確なバージョン戦略。自動更新設定あり。追加時のレビュー基準あり |
| **3** | 意図的かつ文書化済み。各依存の選定理由が明確。最小限かつ最新 |

### Dependency Philosophy Spectrum

```
MINIMAL ←──────────────────────→ MAXIMAL
"stdlib only,    "pragmatic:      "if there's a
 vendor           use popular      lib for it,
 everything"      battle-tested    use it"
                  libraries"
```

### Version Strategy Analysis

| Strategy | Example | Risk Level |
|----------|---------|-----------|
| **Exact** | "1.2.3" | LOW — 再現性高、更新手動 |
| **Caret** | "^1.2.3" | MEDIUM — minor/patch auto |
| **Tilde** | "~1.2.3" | MEDIUM-LOW — patch auto |
| **Range** | ">=1.0.0 <2.0.0" | HIGH — 広範囲許容 |
| **Latest** | "*" or "latest" | CRITICAL — 非推奨 |

---

## Cross-Dimension Correlations

よく見られる次元間の相関パターン。

| Correlation | Pattern | Implication |
|-------------|---------|-------------|
| **N↔C** | 高 Naming → 低 Comment density | 名前が自己文書化するため、コメントが不要になる |
| **A↔R** | 高 Abstraction → 高 Architecture | 抽象化の意識が構造にも反映される |
| **T↔E** | 高 Testing → 高 Error Handling | テストがエラーケースを強制する |
| **G↔T** | 高 Git → 高 Testing | 規律あるワークフローが全体の品質意識を示す |
| **D↔E** | 低 Dependencies → 高 Error Handling | 自前実装が多いとエラー処理も自前で丁寧になる |
| **N↔T** | 高 Naming → 高 Test naming | 命名への意識がテスト名にも波及する |
| **C↔G** | 高 Comments → 高 Git messages | 文書化意識が高いとコミットメッセージも丁寧 |

---

## Module Subcultures

モジュールごとに正当に異なる規約を持つケースの取り扱い。

### Legitimate Subcultures

| Module | Expected Differences | Rationale |
|--------|---------------------|-----------|
| **test/** | 異なる命名（describe/it）、ヘルパー関数、fixture パターン | テストフレームワークが規約を決定 |
| **scripts/** | 簡略化された命名、エラー処理の簡素化 | 一回限りの使用、保守性より実行速度 |
| **generated/** | 機械生成の命名、非人間的構造 | 自動生成のため人間の規約と異なるのは正常 |
| **vendor/** | 外部プロジェクトの規約 | サードパーティコードをそのまま取り込み |
| **migrations/** | シーケンシャルな命名、SQL 直書き | スキーマ管理ツールの要件 |
| **config/** | 固有のフォーマット（YAML/TOML/JSON）| ツール要件に従う |

### Subculture Handling Rules

```yaml
subculture_rules:
  - rule: "サブカルチャーは DNA Profile のメインスコアから除外"
    action: "Module Subcultures セクションに別途記載"
  - rule: "サブカルチャー内でも内部一貫性は評価"
    action: "モジュール内のスコアを別途算出"
  - rule: "サブカルチャーの境界が曖昧な場合は ON_MODULE_SUBCULTURE トリガー"
    action: "ユーザーに境界確認を依頼"
```

### Subculture Detection

```yaml
detection_signals:
  - signal: "ディレクトリ名が明確な役割を示す"
    examples: ["test/", "scripts/", "__generated__/"]
  - signal: "Naming dimension のスコアがメインと 1.5+ 乖離"
    action: "サブカルチャー候補としてフラグ"
  - signal: "独自の linter/formatter 設定が存在"
    examples: [".eslintrc in subdirectory", "rustfmt.toml override"]
  - signal: ".gitattributes で linguist-generated マーク"
    action: "generated code として除外"
```
