# Git Hooks & Automation

> Hook マネージャー比較、lint-staged、シークレット検出、auto-merge、Monorepo CI パターン

## 1. Hook マネージャー比較

| 観点 | Husky | Lefthook | pre-commit |
|------|:-----:|:--------:|:----------:|
| 言語 | Node.js | Go | Python |
| 実行速度 | 普通（逐次） | **高速（並列）** | 遅め |
| ベンチマーク | — | 1.0s | 5.1s |
| 設定形式 | `.husky/` シェルスクリプト | YAML | YAML |
| 言語依存 | Node.js 必須 | **言語非依存** | Python 必須 |
| 適したPJ | Node.js/JS | ポリグロット/高速 | Python/多言語 |

### Lefthook 設定例

```yaml
# lefthook.yml
pre-commit:
  parallel: true
  commands:
    lint:
      glob: "*.{ts,tsx}"
      run: npx eslint {staged_files}
    format:
      glob: "*.{ts,tsx,json,md}"
      run: npx prettier --check {staged_files}
    typecheck:
      glob: "*.{ts,tsx}"
      run: npx tsc --noEmit

commit-msg:
  commands:
    commitlint:
      run: npx commitlint --edit {1}
```

### Husky + lint-staged

```bash
# .husky/pre-commit
npx lint-staged
```

```json
// package.json
{
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md,yml}": ["prettier --write"]
  }
}
```

---

## 2. シークレット検出

| ツール | 特徴 |
|--------|------|
| **gitleaks** | Go製、高速、CI統合容易 |
| **detect-secrets** | Yelp製、Python、ベースライン管理 |
| **trufflehog** | 広範なパターン検出 |

pre-commit hook に組み込むことで、シークレットのコミットを事前防止。

---

## 3. GitHub Actions Auto-Merge

```yaml
name: Auto Merge
on:
  pull_request:
    types: [labeled, synchronize]

jobs:
  auto-merge:
    if: contains(github.event.pull_request.labels.*.name, 'auto-merge')
    runs-on: ubuntu-latest
    steps:
      - uses: pascalgn/automerge-action@v0.16.4
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          MERGE_LABELS: "auto-merge,!wip,!do-not-merge"
          MERGE_METHOD: squash
          MERGE_DELETE_BRANCH: true
```

**適用対象:** 依存関係更新、ドキュメント変更等の低リスクPR。ブランチ保護ルールとの組み合わせ必須。

---

## 4. Monorepo CI パターン

### Affected パッケージ検出

```bash
# Turborepo
turbo run build --affected

# Nx
nx affected -t build
```

**必須:** CI で `fetch-depth: 0` を指定（shallow clone では affected 検出が失敗）。

```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0
```

### パスベース選択的 CI

```yaml
on:
  push:
    paths:
      - 'packages/frontend/**'
      - 'packages/shared/**'
```

### dorny/paths-filter による動的検出

```yaml
- uses: dorny/paths-filter@v3
  id: filter
  with:
    filters: |
      frontend:
        - 'packages/frontend/**'
      backend:
        - 'packages/api/**'
```

### Changesets (Monorepo バージョニング)

```bash
npx changeset          # 変更インパクトを宣言
npx changeset version  # バージョン更新 + CHANGELOG 生成
npx changeset publish  # npm 公開
```

---

## 5. 推奨スタック (2025)

| 用途 | 推奨 |
|------|------|
| パッケージ管理 | pnpm |
| タスク実行 | Turborepo or Nx |
| Hook管理 | Lefthook (ポリグロット) / Husky (JS) |
| コミット検証 | commitlint |
| バージョニング | Changesets |
| CI/CD | GitHub Actions |

**Source:** [Git Hooks Guide 2025](https://dev.to/arasosman/git-hooks-for-automated-code-quality-checks-guide-2025-372f) · [Lefthook vs Husky](https://dev.to/quave/lefthook-benefits-vs-husky-and-how-to-use-30je) · [Auto-Merge Actions](https://oneuptime.com/blog/post/2025-12-20-github-actions-auto-merge/view) · [Monorepo CI Best Practices (Buildkite)](https://buildkite.com/resources/blog/monorepo-ci-best-practices/)
