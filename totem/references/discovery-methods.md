# Discovery Methods Reference — Totem

サンプリング戦略、ファイルタイプ別分析、設定ファイルからの規約抽出、信頼度算出。

---

## Sampling Strategy

### Minimum Sample Size

- **最小サンプル**: 30 ファイル、または コードベースの 20%（いずれか小さい方）
- **推奨サンプル**: 50 ファイル以上（信頼度 HIGH を確保するため）

### Stratified Sampling

各主要ディレクトリからの比例配分サンプリング:

```yaml
stratified_sampling:
  method: "proportional allocation"
  steps:
    - step: "主要ディレクトリを列挙"
      action: "src/, lib/, app/, pkg/ 等のトップレベル分類"
    - step: "各ディレクトリのファイル数を計数"
      action: "比例配分でサンプル数を決定"
    - step: "各ディレクトリからランダムサンプリング"
      action: "recency weighting 適用"
  example:
    total_files: 500
    sample_target: 50
    allocation:
      - { dir: "src/api/", files: 150, sample: 15 }
      - { dir: "src/core/", files: 200, sample: 20 }
      - { dir: "src/ui/", files: 100, sample: 10 }
      - { dir: "src/utils/", files: 50, sample: 5 }
```

### Recency Weighting

- **直近6ヶ月のファイル**: 1.5x の重み（現在のチーム文化をより反映）
- **6-18ヶ月のファイル**: 1.0x（標準）
- **18ヶ月以上前のファイル**: 0.7x（レガシーの可能性あり）

```yaml
recency_weighting:
  rationale: "直近のコードが現在の文化をより正確に反映"
  method: "git log --diff-filter=AM で最終更新日を取得"
  weights:
    recent: { age: "< 6 months", weight: 1.5 }
    standard: { age: "6-18 months", weight: 1.0 }
    legacy: { age: "> 18 months", weight: 0.7 }
  note: "レガシーファイルも完全除外はしない（文化の歴史を示す）"
```

### Exclusions

以下のファイル/ディレクトリはサンプリングから除外:

| Exclusion | Reason | Detection Method |
|-----------|--------|-----------------|
| generated files | 機械生成のため文化を反映しない | ファイルヘッダの生成マーカー、.gitattributes |
| vendor/ | サードパーティコード | ディレクトリ名 |
| node_modules/ | 依存関係 | ディレクトリ名 |
| build/ / dist/ | ビルド成果物 | ディレクトリ名、.gitignore |
| .min.js / .min.css | minified files | ファイル拡張子パターン |
| lock files | 自動生成 | package-lock.json, yarn.lock, go.sum 等 |
| binary files | テキスト分析不可 | ファイルタイプ判定 |

---

## File Type Analysis

| File Type | Dimensions Analyzed | Primary Method | Priority |
|-----------|-------------------|---------------|----------|
| **Source code** (.ts, .py, .go, etc.) | N, A, E, C, T, R | パターン頻度分析 | HIGH |
| **Test files** (*_test.*, *.spec.*) | T, N, C | テスト構造分析 | HIGH |
| **Config files** (.eslintrc, tsconfig) | N, A, D | 明示的ルール抽出 | HIGH |
| **Package manifests** (package.json, go.mod) | D | 依存哲学分析 | MEDIUM |
| **Git history** (git log) | G | コミットメッセージパターン分析 | MEDIUM |
| **CI config** (.github/workflows) | G, R | パイプラインパターン分析 | MEDIUM |
| **Documentation** (*.md, JSDoc) | C | ドキュメント哲学分析 | LOW |
| **Build config** (Makefile, Dockerfile) | R, D | ビルドパターン分析 | LOW |

### Source Code Analysis Detail

```yaml
source_analysis:
  naming:
    - extract: "variable declarations"
      classify: "camelCase | snake_case | PascalCase"
    - extract: "function/method names"
      classify: "verb pattern (get/set/is/has/create/update/delete)"
    - extract: "constant declarations"
      classify: "SCREAMING_SNAKE | other"
  abstraction:
    - measure: "function length distribution (LOC per function)"
    - measure: "class/interface count and ratio"
    - measure: "inheritance depth"
    - measure: "code duplication indicators"
  error_handling:
    - detect: "try-catch/except patterns"
    - detect: "custom error type definitions"
    - detect: "error propagation patterns (wrap/rethrow/swallow)"
    - detect: "logging patterns and levels"
  comments:
    - calculate: "comment-to-code ratio"
    - classify: "why vs what comments"
    - detect: "TODO/FIXME patterns and format"
    - detect: "JSDoc/docstring coverage on public APIs"
```

### Test File Analysis Detail

```yaml
test_analysis:
  naming:
    - detect: "test function naming pattern"
      patterns:
        - "should_verb_when_condition"
        - "test_verb_noun"
        - "describe/it blocks"
        - "given_when_then"
    - calculate: "naming consistency rate"
  structure:
    - detect: "test body structure"
      patterns:
        - "AAA (Arrange-Act-Assert)"
        - "GWT (Given-When-Then)"
        - "setup/teardown usage"
    - detect: "fixture patterns"
      patterns:
        - "factory functions"
        - "builder pattern"
        - "fixture files (JSON/YAML)"
        - "inline data"
  philosophy:
    - detect: "mock usage density"
    - detect: "test helper/utility patterns"
    - detect: "snapshot testing usage"
    - detect: "integration vs unit ratio"
```

### Git History Analysis Detail

```yaml
git_analysis:
  sample: "直近 100 commits (git log -100 --oneline)"
  commit_messages:
    - classify: "conventional commits | prefix | jira_id | free_form"
    - calculate: "format adherence rate"
    - analyze: "average message length"
    - detect: "co-author patterns"
  branch_names:
    - sample: "直近 20 branches (git branch -r --sort=-committerdate)"
    - classify: "feature/fix/chore prefix | free_form | jira_id"
    - calculate: "naming consistency rate"
  merge_strategy:
    - detect: "squash merges vs merge commits vs rebase"
    - method: "git log --merges analysis"
```

---

## Config-Derived Conventions

設定ファイルから暗黙的な規約を抽出する方法。

### ESLint / Prettier / Biome → Naming, Comments

```yaml
eslint_extraction:
  naming_rules:
    - "camelcase" → Naming convention confirmation
    - "@typescript-eslint/naming-convention" → detailed naming rules
    - "id-length" → abbreviation policy
  comment_rules:
    - "spaced-comment" → comment style
    - "capitalized-comments" → comment formatting
    - "jsdoc/*" → documentation requirements
  error_rules:
    - "no-throw-literal" → error handling discipline
    - "no-empty-catch" → catch block requirements

prettier_extraction:
  implications:
    - "printWidth" → code style density preference
    - "singleQuote vs doubleQuote" → string style
    - "trailingComma" → modernness indicator
```

### tsconfig / pyproject.toml → Error Handling Philosophy

```yaml
tsconfig_extraction:
  strict_mode:
    - "strict: true" → high Error Handling score likely
    - "noImplicitAny: true" → type discipline
    - "strictNullChecks: true" → null handling awareness
  module_settings:
    - "paths" → import alias patterns (Architecture indicator)
    - "moduleResolution" → module system preference

pyproject_extraction:
  mypy_settings:
    - "strict = true" → type discipline
    - "disallow_untyped_defs" → function typing requirement
  ruff_settings:
    - selected rules → naming/style enforcement
```

### Test Config → Testing Philosophy

```yaml
jest_config:
  - "coverageThreshold" → coverage expectations (Testing score)
  - "testMatch" → test file organization pattern
  - "setupFilesAfterSetup" → shared test infrastructure
  - "moduleNameMapper" → test isolation approach

vitest_config:
  - "coverage.thresholds" → coverage expectations
  - "globals: true" → describe/it availability without import

pytest_config:
  - "addopts: --strict-markers" → test discipline
  - "filterwarnings" → error awareness
```

### Package Scripts → Development Workflow

```yaml
package_scripts_analysis:
  indicators:
    - "lint" script exists → linting is enforced
    - "test:coverage" → coverage monitoring
    - "typecheck" → type safety valued
    - "format:check" → formatting in CI
    - "prepare" with husky → git hooks enforced (Git score)
    - "commitlint" → commit message enforcement (Git score)
```

---

## Confidence Calculation

### Confidence Levels

| Sample Size (per dimension) | Confidence Level | Action |
|----------------------------|-----------------|--------|
| >= 30 files | **HIGH** | 完全プロファイリング実行 |
| 15-29 files | **MEDIUM** | キャビート付きプロファイリング |
| < 15 files | **LOW** | ON_LOW_CONFIDENCE トリガー発火 |

### Per-Dimension Confidence

各次元に独立した信頼度を算出:

```yaml
confidence_calculation:
  per_dimension:
    naming:
      required_evidence: "30+ variable/function declarations"
      high_threshold: 30
      medium_threshold: 15
    abstraction:
      required_evidence: "20+ functions/classes"
      high_threshold: 20
      medium_threshold: 10
    error_handling:
      required_evidence: "15+ error handling blocks"
      high_threshold: 15
      medium_threshold: 8
    comments:
      required_evidence: "30+ files with comment analysis"
      high_threshold: 30
      medium_threshold: 15
    testing:
      required_evidence: "10+ test files"
      high_threshold: 10
      medium_threshold: 5
    architecture:
      required_evidence: "3+ distinct directory layers"
      high_threshold: 20
      medium_threshold: 10
    git:
      required_evidence: "50+ commits"
      high_threshold: 50
      medium_threshold: 25
    dependencies:
      required_evidence: "package manifest + lockfile"
      high_threshold: 1
      medium_threshold: 1
```

### Confidence Adjustments

```yaml
adjustments:
  - condition: "config file provides explicit rules"
    effect: "+1 confidence level (e.g., MEDIUM → HIGH)"
    rationale: "明示的ルールはサンプルサイズ不足を補う"
  - condition: "all samples from single contributor"
    effect: "-1 confidence level"
    rationale: "個人スタイル vs チーム文化の判別不能"
  - condition: "codebase age < 3 months"
    effect: "-1 confidence level"
    rationale: "文化が確立されていない可能性"
  - condition: "strong linter/formatter enforcement"
    effect: "+1 for Naming dimension"
    rationale: "自動化されたルールは信頼度が高い"
```

---

## Analysis Techniques

### 1. Pattern Frequency Analysis

```yaml
frequency_analysis:
  method: "occurrences counting + percentage calculation"
  steps:
    - "対象パターンを列挙"
    - "各パターンの出現回数をカウント"
    - "割合を算出"
    - "dominant pattern（最多）を特定"
  thresholds:
    dominant: ">= 60% → adopted convention"
    secondary: "20-59% → competing convention"
    outlier: "< 20% → exception/legacy"
```

### 2. Outlier Detection

```yaml
outlier_detection:
  definition: "パターン出現率 < 5% または > 95% のもの"
  categories:
    - rare_pattern: "< 5% → 逸脱候補"
    - near_universal: "> 95% → 確立された規約"
  action:
    rare: "逸脱として Deviation Report に記録"
    near_universal: "規約としてスコアリングに反映"
```

### 3. Temporal Analysis

```yaml
temporal_analysis:
  method: "git blame による時系列分析"
  purpose: "規約の変化を検出（文化ドリフト）"
  steps:
    - "各ファイルの最終更新日を取得"
    - "時系列でパターン変化を追跡"
    - "新しいコードと古いコードで規約が異なるか比較"
  output:
    - "規約変化のタイムライン"
    - "変化ポイント（いつ、どの次元で変わったか）"
```

### 4. Cluster Analysis

```yaml
cluster_analysis:
  method: "モジュール/ディレクトリ単位でのパターンクラスタリング"
  purpose: "モジュールサブカルチャーの検出"
  steps:
    - "各ディレクトリの次元スコアを個別算出"
    - "メインスコアとの乖離度を計算"
    - "乖離度 > 1.5 のモジュールをサブカルチャー候補に"
  threshold:
    subculture: "2+ dimensions with > 1.0 score difference"
    outlier_module: "1 dimension with > 1.5 score difference"
```
