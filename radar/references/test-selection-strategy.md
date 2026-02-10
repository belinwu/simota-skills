# Test Selection & Prioritization Strategy

CI高速化の核心：変更に基づくテスト選択と優先順位付け。

---

## Changed-File Based Selection

### Vitest

```bash
# Run tests related to changed files (vs main)
npx vitest --changed HEAD~1

# Run tests related to specific files
npx vitest --related src/utils/auth.ts

# Run tests affected by staged changes
npx vitest --changed
```

```typescript
// vitest.config.ts - Workspace-aware changed detection
export default defineConfig({
  test: {
    // Only in CI: run related tests for changed files
    ...(process.env.CI && {
      // Uses git to find changed files
      changed: 'HEAD~1',
    }),
  },
});
```

### Jest

```bash
# Find tests related to changed files
npx jest --findRelatedTests src/utils/auth.ts src/services/user.ts

# Run tests changed since a branch point
npx jest --changedSince=main

# Only re-run failed tests from last run
npx jest --onlyFailures

# Combine: changed files + only failures
npx jest --changedSince=main --onlyFailures
```

```json
// package.json - CI script
{
  "scripts": {
    "test:changed": "jest --changedSince=main --passWithNoTests",
    "test:related": "jest --findRelatedTests $(git diff --name-only main -- '*.ts' '*.tsx')"
  }
}
```

### pytest

```bash
# Install testmon for change-based selection
pip install pytest-testmon

# First run: build dependency database
pytest --testmon

# Subsequent runs: only affected tests
pytest --testmon

# Combine with coverage
pytest --testmon --cov=src

# Manual: run tests in changed directories
pytest $(git diff --name-only main -- '*.py' | xargs -I{} dirname {} | sort -u)
```

```ini
# pytest.ini - testmon configuration
[pytest]
addopts = --testmon
testmon_datadir = .testmondata
```

```yaml
# .github/workflows/test.yml - Cache testmon data
- name: Cache testmon data
  uses: actions/cache@v4
  with:
    path: .testmondata
    key: testmon-${{ runner.os }}-${{ hashFiles('src/**/*.py') }}
    restore-keys: testmon-${{ runner.os }}-
```

### Go

```bash
# Run tests for changed packages only
CHANGED_PKGS=$(git diff --name-only main -- '*.go' | xargs -I{} dirname {} | sort -u | sed 's|^|./|')
go test $CHANGED_PKGS

# Run tests for package and its dependents
go test ./pkg/auth/...

# List packages that depend on changed package
go list -f '{{.ImportPath}}' ./... | xargs -I{} go list -f '{{if (index .Deps "mymodule/pkg/auth")}}{{.ImportPath}}{{end}}' {}
```

```bash
# go-affected: find all packages affected by changes
# Script: scripts/go-affected-tests.sh
#!/bin/bash
set -euo pipefail

BASE_BRANCH=${1:-main}
CHANGED_FILES=$(git diff --name-only "$BASE_BRANCH" -- '*.go')
CHANGED_PKGS=$(echo "$CHANGED_FILES" | xargs -I{} dirname {} | sort -u)

# Find reverse dependencies
ALL_PKGS=""
for pkg in $CHANGED_PKGS; do
  DEPS=$(go list -f '{{ join .Deps "\n" }}' "./..." 2>/dev/null | grep "$pkg" | sort -u)
  ALL_PKGS="$ALL_PKGS $DEPS ./$pkg/..."
done

echo "$ALL_PKGS" | tr ' ' '\n' | sort -u | tr '\n' ' '
```

### Rust

```bash
# cargo-nextest: modern test runner with better selection
cargo install cargo-nextest

# Run tests for changed crates in workspace
cargo nextest run -p my-crate

# Run with partitioning (for CI sharding)
cargo nextest run --partition count:1/4

# Filter by test name pattern
cargo nextest run -E 'test(auth::)'

# Run only tests that previously failed
cargo nextest run --run-ignored=only
```

```toml
# .config/nextest.toml
[profile.ci]
retries = 2
fail-fast = false
status-level = "slow"
slow-timeout = { period = "60s", terminate-after = 2 }

[profile.ci.junit]
path = "target/nextest/ci/junit.xml"
```

---

## Fail-Likely-First Prioritization

### Priority Levels

| Priority | Category | Description | Selection Criteria |
|----------|----------|-------------|-------------------|
| **P0** | Last-Failed | 直前CIで失敗したテスト | `--onlyFailures` / retry list |
| **P1** | Direct | 変更ファイルの直接テスト | `--findRelatedTests` / `--changed` |
| **P2** | Dependent | 変更ファイルの依存先テスト | Import graph analysis |
| **P3** | Proximate | 同ディレクトリ・同モジュールのテスト | Directory-based selection |
| **P4** | Full | 全テストスイート | Full run |

### Implementation: Priority-Based Runner

```typescript
// scripts/prioritized-test-runner.ts
import { execSync } from 'child_process';

interface TestTier {
  name: string;
  command: string;
  timeout: number; // minutes
  required: boolean;
}

const tiers: TestTier[] = [
  {
    name: 'P0: Last-Failed',
    command: 'npx vitest --reporter=verbose run --bail 5 2>/dev/null || true',
    timeout: 2,
    required: false,
  },
  {
    name: 'P1: Direct Changes',
    command: 'npx vitest --changed HEAD~1 --reporter=verbose',
    timeout: 3,
    required: true,
  },
  {
    name: 'P2: Dependent Tests',
    command: `npx vitest --related ${getChangedFiles().join(' ')}`,
    timeout: 5,
    required: true,
  },
  {
    name: 'P3: Same Module',
    command: `npx vitest ${getChangedDirectories().join(' ')}`,
    timeout: 5,
    required: false,
  },
  {
    name: 'P4: Full Suite',
    command: 'npx vitest run',
    timeout: 15,
    required: false,  // Only on main branch
  },
];

function getChangedFiles(): string[] {
  return execSync('git diff --name-only HEAD~1 -- "*.ts" "*.tsx"')
    .toString().trim().split('\n').filter(Boolean);
}

function getChangedDirectories(): string[] {
  const files = getChangedFiles();
  const dirs = [...new Set(files.map(f => f.replace(/\/[^/]+$/, '')))];
  return dirs;
}
```

### CI Priority Matrix

```yaml
# .github/workflows/prioritized-tests.yml
jobs:
  determine-scope:
    runs-on: ubuntu-latest
    outputs:
      changed-files: ${{ steps.changes.outputs.files }}
      run-full: ${{ steps.scope.outputs.full }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - id: changes
        run: |
          FILES=$(git diff --name-only origin/main -- '*.ts' '*.tsx' | tr '\n' ' ')
          echo "files=$FILES" >> $GITHUB_OUTPUT

      - id: scope
        run: |
          if [[ "${{ github.ref }}" == "refs/heads/main" ]]; then
            echo "full=true" >> $GITHUB_OUTPUT
          else
            echo "full=false" >> $GITHUB_OUTPUT
          fi

  p0-last-failed:
    needs: determine-scope
    runs-on: ubuntu-latest
    continue-on-error: true
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - name: Restore failure cache
        uses: actions/cache@v4
        with:
          path: .vitest-failures
          key: test-failures-${{ github.ref }}
      - run: npx vitest run --reporter=verbose --bail 3
        timeout-minutes: 2

  p1-direct:
    needs: determine-scope
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - run: npm ci
      - run: npx vitest --changed HEAD~1
        timeout-minutes: 3

  p4-full:
    needs: [p0-last-failed, p1-direct]
    if: needs.determine-scope.outputs.run-full == 'true'
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx vitest run --shard=${{ matrix.shard }}/4
        timeout-minutes: 15
```

---

## Incremental Execution Pipeline

### 3-Gate Strategy

```
┌──────────────┐    ┌──────────────────┐    ┌────────────────┐
│  Fast Gate   │───▶│ Integration Gate  │───▶│  Full Suite     │
│  ≤ 2 min     │    │  ≤ 5 min          │    │  ≤ 15 min       │
│              │    │                    │    │                 │
│ • Lint       │    │ • Changed-related  │    │ • All tests     │
│ • Type check │    │ • Integration      │    │ • Mutation (opt) │
│ • Unit (P0+P1)│   │ • Contract         │    │ • Performance   │
└──────────────┘    └──────────────────┘    └────────────────┘
  PR required         PR required              main only
```

### Gate Configuration

```yaml
# .github/workflows/gates.yml
name: Test Gates

on:
  pull_request:
    branches: [main, develop]

jobs:
  # Gate 1: Fast (always runs, blocks PR)
  fast-gate:
    runs-on: ubuntu-latest
    timeout-minutes: 2
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npx vitest run --changed HEAD~1 --bail 1

  # Gate 2: Integration (runs after fast gate, blocks PR)
  integration-gate:
    needs: fast-gate
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - run: npm ci
      - run: npx vitest run --project=integration
      - run: npx vitest run --related $(git diff --name-only origin/main -- '*.ts' '*.tsx' | tr '\n' ' ')

  # Gate 3: Full (main branch only, non-blocking for PRs)
  full-suite:
    if: github.ref == 'refs/heads/main'
    needs: integration-gate
    runs-on: ubuntu-latest
    timeout-minutes: 15
    strategy:
      fail-fast: false
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx vitest run --shard=${{ matrix.shard }}/4
```

---

## CI-Specific Patterns

### Test Result Caching

```yaml
# Cache test results for faster re-runs
- name: Cache Vitest
  uses: actions/cache@v4
  with:
    path: |
      node_modules/.vitest
      .vitest-failures
    key: vitest-${{ runner.os }}-${{ hashFiles('src/**/*.ts', 'tests/**/*.ts') }}
    restore-keys: |
      vitest-${{ runner.os }}-
```

### Failed Test Auto Re-run

```yaml
# Retry failed tests up to 2 times
- name: Run tests with retry
  uses: nick-fields/retry@v3
  with:
    timeout_minutes: 10
    max_attempts: 3
    retry_on: error
    command: npx vitest run --reporter=junit --outputFile=test-results.xml

# Or use built-in retry
- name: Run tests
  run: npx vitest run --retry 2
```

### Matrix Strategy for Multi-Environment

```yaml
strategy:
  fail-fast: false
  matrix:
    node-version: [18, 20, 22]
    os: [ubuntu-latest, windows-latest]
    exclude:
      - node-version: 18
        os: windows-latest
```

---

## Monorepo Strategy

### Turborepo

```bash
# Run tests only for affected packages
npx turbo run test --filter=...[origin/main]

# Run tests for specific package and dependents
npx turbo run test --filter=@myorg/auth...

# Dry run to see what would execute
npx turbo run test --filter=...[origin/main] --dry-run
```

```json
// turbo.json
{
  "pipeline": {
    "test": {
      "dependsOn": ["^build"],
      "outputs": ["coverage/**"],
      "cache": true,
      "inputs": ["src/**/*.ts", "tests/**/*.ts", "vitest.config.ts"]
    },
    "test:ci": {
      "dependsOn": ["^build"],
      "outputs": ["coverage/**", "test-results/**"],
      "cache": false
    }
  }
}
```

### pnpm Workspace

```bash
# Run tests in changed packages only
pnpm --filter "...[origin/main]" run test

# Run tests in specific package
pnpm --filter @myorg/auth run test

# Run tests in all packages matching pattern
pnpm --filter "./packages/core-*" run test

# Parallel execution across packages
pnpm -r --parallel run test
```

### Nx

```bash
# Run affected tests
npx nx affected --target=test --base=main

# Run tests for specific project graph
npx nx run-many --target=test --projects=auth,users

# Visualize affected graph
npx nx affected:graph --base=main
```

```json
// nx.json
{
  "targetDefaults": {
    "test": {
      "inputs": ["default", "^default", "{workspaceRoot}/jest.preset.js"],
      "cache": true,
      "dependsOn": ["^build"]
    }
  },
  "namedInputs": {
    "default": ["{projectRoot}/**/*", "!{projectRoot}/**/*.md"]
  }
}
```

---

## Decision Tree: Test Selection Strategy

```
PR opened / Push event
        │
        ▼
  ┌─────────────────┐
  │ Changed files?   │
  │ (git diff)       │
  └────────┬────────┘
           │
     ┌─────┴─────┐
     │           │
  Yes ▼        No ▼
  ┌──────┐   ┌──────────┐
  │Select│   │Skip tests│
  │scope │   │(docs only)│
  └──┬───┘   └──────────┘
     │
     ▼
  ┌────────────────────┐
  │ Config files changed│
  │ (CI, tsconfig, etc)│
  └────────┬───────────┘
     ┌─────┴─────┐
     │           │
  Yes ▼        No ▼
  ┌──────┐   ┌─────────────┐
  │ Full │   │ Related only │
  │ suite│   │ (--changed)  │
  └──────┘   └──────┬──────┘
                     │
                     ▼
              ┌────────────┐
              │ main branch?│
              └──────┬─────┘
                ┌────┴────┐
                │        │
             Yes ▼     No ▼
           ┌──────┐  ┌──────────┐
           │ Full │  │ PR scope │
           │+shard│  │ (P0-P3)  │
           └──────┘  └──────────┘
```

### Skip Conditions

```yaml
# Skip tests when only docs/config changed
- name: Check for skippable changes
  id: skip-check
  run: |
    CHANGED=$(git diff --name-only origin/main)
    # Skip if only markdown, docs, or non-code files changed
    if echo "$CHANGED" | grep -qvE '\.(md|txt|png|jpg|svg|yml|yaml)$'; then
      echo "skip=false" >> $GITHUB_OUTPUT
    else
      echo "skip=true" >> $GITHUB_OUTPUT
    fi

- name: Run tests
  if: steps.skip-check.outputs.skip != 'true'
  run: npx vitest run
```

---

## Quick Reference

| Strategy | Tool/Flag | Use Case |
|----------|-----------|----------|
| Changed files | `vitest --changed` | PR テスト高速化 |
| Related files | `jest --findRelatedTests` | 依存先テスト |
| Failed first | `jest --onlyFailures` | リグレッション優先 |
| Monorepo scope | `turbo --filter=...[main]` | 影響パッケージのみ |
| Shard | `vitest --shard=1/4` | CI 並列化 |
| Retry | `vitest --retry 2` | Flaky 対策 |
| Skip | Path filter in CI | Docs-only 変更スキップ |
| Priority | P0→P4 tier | 段階的実行 |
