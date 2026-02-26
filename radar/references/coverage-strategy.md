# Coverage Strategy

カバレッジの種類・目標設定・PR監視・マルチモジュール集約・アンチパターン。

---

## Coverage Types Decision Matrix

### Type Definitions

| Type | What It Measures | Blind Spots |
|------|-----------------|-------------|
| **Line** | 各行が実行されたか | 分岐網羅せず（`if(a && b)` で `a=true, b=false` のみでも100%） |
| **Branch** | 各分岐（if/else, switch, ternary）が実行されたか | 条件式内の組み合わせ不足 |
| **Function** | 各関数が呼ばれたか | 関数内のパス未検証 |
| **Statement** | 各文が実行されたか | Line とほぼ同等（1行複数文で差が出る） |
| **Condition** | 各条件式の true/false が両方テストされたか | ツールサポートが限定的 |

### Recommended Metrics by Code Type

| Code Type | Primary Metric | Secondary | Target | Rationale |
|-----------|---------------|-----------|--------|-----------|
| Business Logic | Branch | Line | 85%+ | 分岐が品質の核心 |
| API Handlers | Line | Function | 80%+ | エンドポイント網羅が重要 |
| Utility / Helpers | Branch | Line | 90%+ | 再利用コードは高品質必須 |
| UI Components | Function | Line | 70%+ | レンダリング検証が主目的 |
| Generated Code | — | — | Exclude | テスト不要 |
| Config / Constants | — | — | Exclude | ロジック無し |

### Judge Integration

Judge の UQS (Universal Quality Score) では以下の複合式でカバレッジスコアを算出:

```
radar_score = (line × 0.4) + (branch × 0.4) + (function × 0.2)
```

この配分は line と branch を同等重視し、function を補助指標とする設計。
カバレッジ戦略はこの配分を考慮し、branch カバレッジの改善が radar_score 向上に最も効果的であることを意識する。

---

## Coverage Decline Detection

### Diff Coverage (New/Changed Lines)

変更されたコードのカバレッジを個別に測定し、新規コードの品質低下を防止。

```bash
# diff-cover: measure coverage of changed lines only
pip install diff-cover

# Generate coverage, then check diff
npx vitest run --coverage
diff-cover coverage/lcov.info --compare-branch=main --fail-under=80
```

### Vitest Coverage Configuration

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8', // or 'istanbul'
      reporter: ['text', 'lcov', 'json-summary'],
      reportsDirectory: './coverage',

      // Thresholds - CI fails if below these
      thresholds: {
        lines: 80,
        branches: 80,
        functions: 75,
        statements: 80,
      },
// ...
```

### Jest Coverage Configuration

```javascript
// jest.config.js
module.exports = {
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'json-summary'],

  coverageThreshold: {
    global: {
      branches: 80,
      functions: 75,
      lines: 80,
      statements: 80,
    },
    // Per-path thresholds
    './src/core/': {
// ...
```

### pytest-cov Configuration

```ini
# pyproject.toml
[tool.pytest.ini_options]
addopts = "--cov=src --cov-report=term-missing --cov-report=lcov:coverage/lcov.info"

[tool.coverage.run]
branch = true
source = ["src"]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "*/__generated__/*",
]

[tool.coverage.report]
fail_under = 80
// ...
```

### Go Coverage

```bash
# Run with coverage
go test ./... -coverprofile=coverage.out -covermode=atomic

# Check coverage threshold
go tool cover -func=coverage.out | grep total | awk '{print $3}' | \
  awk -F'%' '{if ($1 < 80) exit 1}'

# HTML report
go tool cover -html=coverage.out -o coverage.html
```

### JaCoCo (Java/Kotlin)

```xml
<!-- pom.xml -->
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <configuration>
    <rules>
      <rule>
        <element>BUNDLE</element>
        <limits>
          <limit>
            <counter>LINE</counter>
            <value>COVEREDRATIO</value>
            <minimum>0.80</minimum>
          </limit>
          <limit>
<!-- ... -->
```

---

## Coverage Ratchet Strategy

カバレッジを「下げない」制約で段階的に品質を引き上げる。

### Principle

```
Current coverage = 75%
  → New code must have ≥ 80% (diff coverage)
  → Overall cannot drop below 75% (ratchet)
  → Gradually rises as new code is higher quality
```

### Implementation

```yaml
# .github/workflows/coverage-ratchet.yml
- name: Check coverage ratchet
  run: |
    # Get current coverage from main branch
    MAIN_COV=$(curl -s "$CODECOV_API/repos/$REPO/commits/main" | jq '.totals.coverage')

    # Get PR coverage
    PR_COV=$(jq '.total.lines.pct' coverage/coverage-summary.json)

    # Ratchet: PR coverage must be >= main coverage
    if (( $(echo "$PR_COV < $MAIN_COV" | bc -l) )); then
      echo "::error::Coverage decreased from ${MAIN_COV}% to ${PR_COV}%"
      exit 1
    fi
```

### Per-Module Ratchet

| Module | Current | Min (Ratchet) | New Code Target |
|--------|---------|---------------|-----------------|
| core | 88% | 88% | 90% |
| api | 75% | 75% | 80% |
| utils | 92% | 92% | 90% |
| legacy | 45% | 45% | 60% |

## Dead Code vs Untested Code

### Distinction

| Category | Description | Action |
|----------|------------|--------|
| **Dead Code** | Code that is never reachable at runtime | Delete safely |
| **Untested Code** | Reachable code without test coverage | Add tests or accept risk |
| **Test-Only Code** | Code reachable only from tests | Review: may indicate over-testing |

### Static Analysis Tools

```bash
# TypeScript: find unused exports
npx ts-prune

# TypeScript: find dead code
npx knip

# Python: find unused code
pip install vulture
vulture src/ --min-confidence 80

# Go: find unused code
go install golang.org/x/tools/cmd/deadcode@latest
deadcode ./...
```

### Triage Workflow

```
Low coverage file detected
        │
        ▼
  ┌─────────────────┐
  │ Static analysis: │
  │ Is code used?    │
  └────────┬────────┘
     ┌─────┴─────┐
     │           │
  Used ▼     Unused ▼
  ┌──────────┐  ┌──────────────┐
  │ Priority │  │ Delete or    │
  │ for tests│  │ deprecate    │
  └────┬─────┘  └──────────────┘
       │
...
```

---

## Multi-Module Coverage Aggregation

### lcov Merge

```bash
# Merge multiple lcov files
npx lcov-result-merger 'packages/*/coverage/lcov.info' merged-coverage.info

# Generate combined HTML report
genhtml merged-coverage.info --output-directory combined-coverage
```

### Codecov Flags

```yaml
# codecov.yml
coverage:
  status:
    project:
      default:
        target: 80%
      core:
        target: 90%
        flags: [core]
      api:
        target: 80%
        flags: [api]

flags:
  core:
# ...
```

```yaml
# .github/workflows/coverage.yml
- name: Upload coverage (core)
  uses: codecov/codecov-action@v4
  with:
    files: packages/core/coverage/lcov.info
    flags: core
    token: ${{ secrets.CODECOV_TOKEN }}

- name: Upload coverage (api)
  uses: codecov/codecov-action@v4
  with:
    files: packages/api/coverage/lcov.info
    flags: api
    token: ${{ secrets.CODECOV_TOKEN }}
```

### Turborepo Coverage Integration

```json
// turbo.json
{
  "pipeline": {
    "test:coverage": {
      "dependsOn": ["^build"],
      "outputs": ["coverage/**"],
      "cache": false
    }
  }
}
```

```bash
# Run coverage across all packages
npx turbo run test:coverage

# Merge results
npx lcov-result-merger 'packages/*/coverage/lcov.info' merged.lcov
```

---

## CI Coverage Reporting

### PR Comment with Coverage

```yaml
# .github/workflows/coverage-report.yml
- name: Coverage Report
  uses: davelosert/vitest-coverage-report-action@v2
  with:
    json-summary-path: coverage/coverage-summary.json
    json-final-path: coverage/coverage-final.json
    vite-config-path: vitest.config.ts
```

### Coverage Badge

```yaml
# Generate coverage badge
- name: Coverage Badge
  uses: jaywcjlove/coverage-badges-cli@main
  with:
    source: coverage/coverage-summary.json
    output: coverage/badge.svg
```

---

## Anti-Patterns

### Coverage Anti-Pattern Catalog

| Anti-Pattern | Problem | Better Approach |
|-------------|---------|-----------------|
| **100% Target** | Diminishing returns、テスト保守コスト増大 | 80-90% + mutation testing |
| **Assertion-Free Tests** | 行は実行されるが何も検証しない | テスト品質監視（Judge TQ-002） |
| **Generated Code Coverage** | 自動生成コードを含めると目標が歪む | exclude 設定で除外 |
| **Coverage Gaming** | テストを通すだけのコード追加 | Code review + mutation score |
| **Global-Only Threshold** | モジュール間の品質格差が隠れる | Per-module thresholds |
| **Ignoring Branch Coverage** | Line 100% でも分岐未テスト | Branch を primary metric に |
| **Coverage Without Review** | 数値だけ見てテスト品質を無視 | Judge と連携してTQ評価 |

### Detection: Assertion-Free Tests

```typescript
// Custom ESLint rule concept
// Detect test blocks without expect() calls
// → Flag as TQ-002 (Assertion Quality) issue

// Better: Use vitest-plugin-no-only with custom rule
// or integrate with Judge for test quality review
```

### Coverage vs Quality Matrix

```
                High Coverage
                     │
         ┌───────────┼───────────┐
         │  False     │  Ideal    │
   Low   │  Security  │  Quality  │
 Quality │ (gaming)   │           │
         │           │           │
─────────┼───────────┼───────────┤
         │           │           │
   High  │  Risk     │  Tested   │
 Quality │  Zone     │  but      │
         │           │  Incomplete│
         └───────────┼───────────┘
                     │
                Low Coverage
```

---

## Quick Reference

| Metric | Target (New Code) | Target (Legacy) | Tool |
|--------|-------------------|-----------------|------|
| Line | 80%+ | Ratchet | v8 / istanbul |
| Branch | 80%+ | Ratchet | v8 / istanbul |
| Function | 75%+ | Ratchet | v8 / istanbul |
| Diff | 80%+ | 60%+ | diff-cover |
| Mutation Score | 75%+ | — | Stryker |

| Tool | Language | Command |
|------|----------|---------|
| Vitest v8 | TypeScript | `vitest --coverage` |
| Jest istanbul | TypeScript | `jest --coverage` |
| pytest-cov | Python | `pytest --cov=src` |
| go cover | Go | `go test -coverprofile=c.out` |
| JaCoCo | Java | Maven plugin |
| tarpaulin | Rust | `cargo tarpaulin` |
