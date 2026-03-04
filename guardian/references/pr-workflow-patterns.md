# PR Workflow Patterns

> PRサイズガイドライン、Stacked PRs、Draft PR、テンプレート、アンチパターン

## 1. PR サイズガイドライン

| サイズ | 行数 | 評価 |
|--------|------|------|
| Small | < 200行 | 承認速度3倍、理想的 |
| Medium | 200-400行 | **推奨範囲**、欠陥率40%低下 |
| Large | 400-1000行 | レビュー品質が低下し始める |
| Mega | > 1000行 | アンチパターン、分割必須 |

**原則:** 1 PR = 1タスク / 1関心事。大きいPRほどピックアップ時間が長く、レビュー中の修正も増加。

---

## 2. Stacked PRs（積み重ねPR）

大きな機能を複数の依存PRに分割し、レビュー待ちでブロックされずに開発を続ける手法。

**ワークフロー:**
1. `feature/step-1` → `main` へPR作成
2. `feature/step-2` → `feature/step-1` へPR作成
3. 各PRにラベル: `[1/3] Setup Schema`, `[2/3] Add API`

**主要ツール:**

| ツール | 特徴 |
|--------|------|
| **Graphite** | CLI + Web UI、`gt stack submit` で一括PR作成 |
| ghstack | Meta発、Git上のスタック管理 |
| Git Town | 軽量、Git native に近い |

```bash
# Graphite の主要コマンド
gt branch create feat-step-1
gt commit create -m "feat: add schema"
gt branch create feat-step-2
gt stack submit  # スタック全体をPRとして提出
```

---

## 3. Draft PR パターン

| 用途 | 効果 |
|------|------|
| 方向性の確認 | アーキテクチャ判断の早期フィードバック |
| WIP の共有 | CIは実行されるため早期問題検出 |
| レビュアー負担の明示 | 完成前であることが明確 |

---

## 4. PR Description テンプレート

```markdown
## Summary
<!-- What changed and why -->

## Changes
- [ ] Change 1
- [ ] Change 2

## Related Issues
<!-- Closes #123, Refs #456 -->

## Screenshots / Recordings
<!-- UI変更がある場合 -->

## Test Plan
- [ ] Unit tests added/updated
- [ ] Manual testing steps

## Checklist
- [ ] Self-review completed
- [ ] Documentation updated (if needed)
- [ ] No breaking changes (or documented)
```

**ベストプラクティス:** テンプレートはシンプルに保ち、HTML コメントで記入ガイドを提供。

---

## 5. アンチパターン

| # | パターン | 問題 | 修正 |
|---|---------|------|------|
| 1 | Mega PR (1000行超) | レビュー品質著しく低下 | 200-400行に分割 |
| 2 | 空の description | コンテキスト不明 | テンプレート必須化 |
| 3 | 複数関心事の混在 | リファクタ+機能+修正を1PRに | 1PR = 1関心事 |
| 4 | セルフマージ | 品質ゲートバイパス | 最低1人のレビュー必須 |
| 5 | 長期放置PR | コンフリクト蓄積、コンテキスト喪失 | SLA設定（24h以内レビュー） |
| 6 | レビュー前のセルフレビュー欠如 | 容易に防げるミスが混入 | チェックリストでセルフレビュー |

**Source:** [PR Size Best Practices (Graphite)](https://graphite.com/guides/best-practices-managing-pr-size) · [Stacked PRs Guide (PullNotifier)](https://pullnotifier.com/tools/stacked-prs) · [PR Best Practices 2025 (Sopa)](https://www.heysopa.com/post/pull-request-best-practices)
