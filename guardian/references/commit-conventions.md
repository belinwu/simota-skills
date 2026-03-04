# Commit Conventions & Best Practices

> Conventional Commits 仕様、Atomic Commits、コミット署名、commitlint、アンチパターン

## 1. Conventional Commits 仕様 (v1.0.0)

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

| Type | 用途 | SemVer |
|------|------|--------|
| `feat` | 新機能 | MINOR |
| `fix` | バグ修正 | PATCH |
| `docs` | ドキュメントのみ | — |
| `style` | フォーマット（意味変更なし） | — |
| `refactor` | リファクタリング | — |
| `perf` | パフォーマンス改善 | — |
| `test` | テストの追加・修正 | — |
| `build` | ビルドシステム・外部依存 | — |
| `ci` | CI設定変更 | — |
| `chore` | その他雑務 | — |

### Breaking Change

```
feat(api)!: remove deprecated endpoints

BREAKING CHANGE: The /v1/users endpoint has been removed.
Use /v2/users instead.
```

- `!` を type/scope 直後に置く → SemVer MAJOR
- footer に `BREAKING CHANGE:` でも可

---

## 2. Atomic Commits

| 原則 | 説明 |
|------|------|
| 1コミット = 1論理的変更 | 独立して適用・revert 可能 |
| 常に動作状態 | 各コミット後もテストがパス |
| 関心の分離 | フォーマット変更とロジック変更を混ぜない |
| subject は50文字以内 | Git ツールでの可読性確保 |
| 命令形で記述 | "Add feature" (O) / "Added feature" (X) |
| body で "why" を説明 | "what" は diff で分かる |

---

## 3. コミット署名

| 観点 | GPG | SSH |
|------|-----|-----|
| プラットフォーム | GitHub, GitLab, Bitbucket 全て | GitHub, GitLab のみ |
| セットアップ | やや複雑 | 既存SSH鍵を流用でき簡単 |
| 最小Git版 | 制限なし | Git 2.34+ |

```bash
# SSH 署名の設定
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
```

---

## 4. commitlint 設定

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 'refactor',
      'perf', 'test', 'build', 'ci', 'chore', 'revert'
    ]],
    'subject-max-length': [2, 'always', 72],
    'body-max-line-length': [2, 'always', 100],
  }
};
```

---

## 5. アンチパターン

| # | パターン | 問題 | 修正 |
|---|---------|------|------|
| 1 | "Update file.rb" | ファイル名はdiffで分かる | 意味的な変更内容を記述 |
| 2 | "Bugfix" / "fix stuff" | 何のバグか不明 | 修正対象と方法を明記 |
| 3 | `-m` フラグ多用 | マルチライン記述不可 | エディタでコミットメッセージ作成 |
| 4 | 巨大コミット | bisect・revert 困難 | Atomic commits に分割 |
| 5 | フォーマット + ロジック混在 | revert が困難 | 別コミットに分離 |
| 6 | WIP コミットの放置 | 履歴が不透明 | interactive rebase で整理 |

**Source:** [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) · [Atomic Commits (PHP Architect)](https://www.phparch.com/2025/06/atomic-commits-explained-stop-writing-useless-git-messages/) · [Commit Message Best Practices 2025](https://blog.pullnotifier.com/blog/8-git-commit-message-best-practices-for-2025)
