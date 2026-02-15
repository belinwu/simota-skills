# Mutation Testing Guide

Stryker/mutmut/cargo-mutants、サバイバル分析のリファレンス。

---

## Mutation Testing Overview

### How It Works

```
1. Parse source code
2. Apply mutations (small code changes)
3. Run test suite against each mutant
4. Analyze results:
   - Killed mutant: Tests detected the change ✅
   - Survived mutant: Tests missed the change ❌
   - Timed out: Infinite loop mutation (usually killed) ✅
   - No coverage: No tests cover this code ⚠️

Mutation Score = Killed / (Total - No Coverage) × 100
```

### Common Mutation Operators

| Category | Mutation | Example |
|----------|----------|---------|
| **Arithmetic** | Replace operator | `a + b` → `a - b` |
| **Conditional** | Negate condition | `if (a > b)` → `if (a <= b)` |
| **Boundary** | Off-by-one | `a > 0` → `a >= 0` |
| **Return value** | Change return | `return true` → `return false` |
| **Remove call** | Delete function call | `validate(input)` → (removed) |
| **String** | Empty string | `"error"` → `""` |
| **Assignment** | Change value | `x = 1` → `x = 0` |

---

## Tool Configuration

### Stryker (JavaScript/TypeScript)

```json
{
  "$schema": "https://raw.githubusercontent.com/stryker-mutator/stryker/master/packages/core/schema/stryker-schema.json",
  "mutate": ["src/**/*.ts", "!src/**/*.test.ts", "!src/**/*.d.ts"],
  "testRunner": "jest",
  "reporters": ["html", "clear-text", "progress"],
  "coverageAnalysis": "perTest",
  "thresholds": {
    "high": 80,
    "low": 60,
    "break": 50
  },
  "timeoutMS": 10000,
  "concurrency": 4
}
```

```bash
# Run
npx stryker run

# Run on specific files
npx stryker run --mutate "src/utils/validation.ts"
```

### mutmut (Python)

```ini
# setup.cfg
[mutmut]
paths_to_mutate=src/
tests_dir=tests/
runner=pytest -x --tb=no -q
```

```bash
# Run all mutations
mutmut run

# Run on specific file
mutmut run --paths-to-mutate src/validation.py

# View results
mutmut results

# Show specific surviving mutant
mutmut show 42
```

### cargo-mutants (Rust)

```bash
# Run all mutations
cargo mutants

# Run on specific file
cargo mutants --file src/validation.rs

# Parallel execution
cargo mutants -j 4

# Skip long-running tests
cargo mutants --timeout 30
```

---

## Survival Analysis

### Interpreting Results

| Result | Meaning | Action |
|--------|---------|--------|
| **Score > 80%** | Strong test suite | Maintain, focus on survivors |
| **Score 60-80%** | Decent, gaps exist | Investigate top survived mutants |
| **Score < 60%** | Significant gaps | Prioritize test improvements |

### Common Survival Patterns

| Pattern | Why It Survives | Fix |
|---------|----------------|-----|
| **Missing boundary test** | `>` vs `>=` not tested | Add boundary value tests |
| **Missing negative test** | Only happy path tested | Add error/edge case tests |
| **Weak assertion** | Test checks existence, not value | Assert exact expected values |
| **Dead code** | Code path unreachable | Remove dead code |
| **Equivalent mutant** | Mutation doesn't change behavior | Skip (false positive) |

### Survival Analysis Workflow

```markdown
1. Run mutation testing
2. Sort survivors by file/module
3. For each survivor:
   a. Is it an equivalent mutant? → Mark as ignored
   b. Is it dead code? → Remove the code
   c. Is it a missing test? → Write the test
4. Re-run to verify improvement
5. Track mutation score over time
```

---

## CI Integration

### Stryker in GitHub Actions

```yaml
mutation-test:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
    - run: npm ci
    - run: npx stryker run
    - name: Check mutation score
      run: |
        score=$(cat reports/mutation/mutation.json | jq '.schemaVersion' -r)
        if [ "$score" -lt "60" ]; then
          echo "Mutation score below threshold"
          exit 1
        fi
```

### Incremental Mutation Testing

```bash
# Only mutate changed files (CI optimization)
CHANGED_FILES=$(git diff --name-only HEAD~1 -- 'src/**/*.ts' | tr '\n' ',')
npx stryker run --mutate "$CHANGED_FILES"
```

---

## Mutation Testing Thresholds

| Context | Minimum Score | Recommended |
|---------|--------------|-------------|
| **Critical business logic** | 80% | 90%+ |
| **Utility functions** | 70% | 80%+ |
| **API handlers** | 60% | 70%+ |
| **UI components** | 50% | 60%+ |
| **Overall project** | 60% | 75%+ |
