# Code Review Guide

> レビューチェックリスト、CODEOWNERS、レビュアー割り当て、ターンアラウンド最適化、AI活用、アンチパターン

## 1. レビューの焦点分離

| 人間がフォーカス | 自動化に委ねる |
|:---------------:|:-------------:|
| 正確性・ロジック | スタイル/フォーマット (Prettier, Biome) |
| 設計・アーキテクチャ | 静的解析 (ESLint, TypeScript) |
| セキュリティ | 依存関係脆弱性スキャン |
| パフォーマンス | テスト実行 |
| 可読性・保守性 | — |

---

## 2. CODEOWNERS

```
# .github/CODEOWNERS
/src/compiler/    @my-org/compiler-team
/src/frontend/    @my-org/frontend-team
/src/api/         @my-org/backend-team
*.sql             @my-org/dba-team
package.json      @my-org/platform-team
pnpm-lock.yaml    @my-org/platform-team
```

- **last-match-wins**: ファイル末尾のパターンが優先
- チーム単位での割り当てが推奨
- 依存関係変更にはプラットフォームレビュアー必須

### GitHub 自動割り当て

Round-robin または Load Balance でチーム内のレビュアーを自動選択。

---

## 3. ターンアラウンド目標

| メトリクス | エリートチーム | 目標 |
|-----------|:------------:|:----:|
| 最初のレビューまで | < 4時間 | **4時間以内** |
| マージまで | < 6時間 | **24時間以内** |

**最も効果的な施策:** PRサイズを200-400行に制限。acceptance → merge 時間短縮だけで code velocity 最大63%向上。

---

## 4. AI アシストレビュー (2025)

| ツール | 特徴 |
|--------|------|
| **CodeRabbit** | PR自動レビュー、コンテキスト理解、修正提案 |
| **GitHub Copilot** | インラインでのレビュー支援 |
| **Cursor Bugbot** | レビュー時間40%削減 |
| **Claude Code** | 包括的コードレビュー・解析 |

**推奨:** AIを初回パスとして使用 → 人間がアーキテクチャ・設計・ビジネスロジックの最終判断（ハイブリッドアプローチ）。

最先端ツールは実世界のランタイムバグの42-48%を検出（従来の静的解析 <20% から大幅向上）。

---

## 5. アンチパターン

| # | パターン | 問題 | 修正 |
|---|---------|------|------|
| 1 | **Rubber Stamping** | 読まずに "LGTM" で承認 | レビューコメント必須化 |
| 2 | **Bike Shedding** | 些末な問題に時間を費やす | スタイル議論は linter に委ねる |
| 3 | **Knowledge Silos** | 特定の人だけがレビュー | CODEOWNERS + ローテーション |
| 4 | **Over-helping** | コードを書き直す | 方向性を示し、著者に修正させる |
| 5 | **"Just One More Thing"** | 追加修正要求が際限なく続く | スコープを定め、follow-up Issue を作る |
| 6 | **Self-merging** | 自分のPRを承認してマージ | ブランチ保護で最低1承認必須 |

**Bike Shedding 対策:** 一部チームは Slack に「自転車置き場」絵文字を追加してこのパターンを可視化。

**Source:** [Code Review Best Practices (mev.com)](https://mev.com/blog/code-review-best-practices-for-software-engineers) · [Code Review Anti-Patterns (DZone)](https://dzone.com/refcardz/code-review-patterns-and-anti-patterns) · [AI Code Review 2025 (Addy Osmani)](https://addyo.substack.com/p/code-review-in-the-age-of-ai) · [Review Turnaround (Graphite)](https://graphite.com/guides/tracking-improving-code-review-turnaround)
