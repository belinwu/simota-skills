# Code Review Anti-Patterns

> レビュープロセスのアンチパターン、行動的アンチパターン、改善策

## 1. プロセスアンチパターン（AWS Well-Architected）

| # | パターン | 症状 | 影響 | 対策 |
|---|---------|------|------|------|
| 1 | **Infrequent Reviews** | レビューを飛ばす/まれにしか行わない | エラー検出機会の喪失、孤立した開発 | レビューをマージ前の必須ステップに |
| 2 | **Excessive Reviewers** | レビュアーが多すぎる | ボトルネック、不要な遅延 | コード複雑度に応じた実用的な人数設定 |
| 3 | **No Automated Feedback** | 自動ツールを使わない | レビュー時間の延長、些細な問題に集中 | SAST/Linter を事前実行、人間は高次の問題に |
| 4 | **Large Batch Reviews** | 複数変更を一括レビュー | 問題の特定困難、長いレビューサイクル | 小さく焦点の絞られた PR を提出 |
| 5 | **Unconstructive Reviews** | 厳しいトーン、曖昧なフィードバック | 開発者の士気低下、対話の阻害 | 具体的・建設的なフィードバック研修 |
| 6 | **No Action on Findings** | 指摘事項が放置される | 同じ問題の繰り返し、レビューの形骸化 | フィードバック追跡システムの導入 |

---

## 2. 行動的アンチパターン

### 8大行動パターン

| パターン | 説明 | Judge での対策 |
|---------|------|-------------|
| **Rubber Stamping** | 内容を読まずに承認 | 自動レビューで最低限の品質保証を確保 |
| **Nit-Picking** | スタイル/フォーマットの些事に執着 | スタイルは Linter/Zen に委譲、ロジックに集中 |
| **Long-Running PRs** | PR がレビュー待ちで長期間滞留 | レビューターンアラウンドの計測・アラート |
| **Self-Merging** | 自分のコードを自分で承認・マージ | 最低1名の他者レビューを必須化 |
| **Heroing** | 1人が全レビューを担当 | レビュー負荷の分散、ローテーション |
| **Over-Helping** | レビュアーがコードを書き直してしまう | 提案に留め、修正は著者に任せる |
| **"Just One More Thing"** | 承認直前に追加要求を繰り返す | スコープを明確化、追加はフォローアップ Issue に |
| **Knowledge Silos** | 特定領域を特定者のみがレビュー | クロスレビューの促進、ドキュメント化 |

---

## 3. 認知バイアスとレビュー品質

### レビューに影響するバイアス

| バイアス | 影響 | 対策 |
|---------|------|------|
| **確認バイアス** | 既存の信念に一致する問題のみ検出 | チェックリストベースのレビュー |
| **決定疲労** | レビュー後半で品質が低下 | 1回 60分以内、休憩を挟む |
| **アンカリング** | 最初に見た問題に引きずられる | 構造化レビュー（セキュリティ→ロジック→パフォーマンス） |
| **バンドワゴン** | 他のレビュアーの意見に追従 | 独立レビュー後にディスカッション |
| **ハロー効果** | 著者の能力でレビュー深度が変わる | コードのみを評価、著者名を意識しない |

### Judge での認知バイアス対策

```
Judge の自動レビューは認知バイアスに影響されない:
  ✅ 一貫した深度で全ファイルをレビュー
  ✅ 疲労なく大量のコードを処理
  ✅ チェックリストベースで漏れを防止
  ✅ 著者に関係なく同じ基準を適用

ただし AI レビューの限界:
  ❌ ビジネスコンテキストの理解が不完全
  ❌ アーキテクチャ判断は人間が必要
  ❌ 暗黙知に基づく判断は困難
```

---

## 4. レビュースコープのアンチパターン

### "Everything Everywhere All at Once" パターン

```
❌ 1回のレビューで全観点をチェック:
   正確性 + セキュリティ + パフォーマンス + スタイル + テスト + ドキュメント

✅ 観点を分離してレビュー（Specialist-Agent パターン）:
   Pass 1: 正確性・ロジック（Judge）
   Pass 2: セキュリティ（Sentinel）
   Pass 3: パフォーマンス（Bolt）
   Pass 4: テスト品質（Radar）
```

### 一貫性のないフィードバック

```
❌ 前回承認したパターンを今回は拒否
❌ レビュアーによって基準が異なる
❌ 明文化されていない暗黙ルール

✅ レビューガイドラインの明文化
✅ Living Rules（チーム基準の継続的更新）
✅ AI レビューによる基準の一貫性確保
```

---

## 5. Judge のアンチパターン回避策

| アンチパターン | Judge の対策 |
|-------------|------------|
| スタイル指摘 | severity=INFO、Zen に委譲 |
| 大量指摘で埋もれ | CRITICAL/HIGH を最上位表示 |
| フォローアップなし | remediation agent を明示 |
| コンテキスト不足 | PR description + commit message を intent check |
| false positive 多発 | codex-integration.md のフィルタリング適用 |

**Source:** [AWS: Anti-patterns for Code Review](https://docs.aws.amazon.com/wellarchitected/latest/devops-guidance/anti-patterns-for-code-review.html) · [CodeRabbit: 5 Code Review Anti-Patterns](https://www.coderabbit.ai/blog/5-code-review-anti-patterns-you-can-eliminate-with-ai) · [IEEE: Anti-patterns in Modern Code Review](https://ieeexplore.ieee.org/document/9425884/) · [Arxiv: Towards Debiasing Code Review](https://arxiv.org/abs/2407.01407)
