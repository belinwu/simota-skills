# Branching Strategies

> Trunk-Based vs GitHub Flow vs Git Flow、Feature Flags、選定ガイド

## 1. 戦略比較

| 観点 | Trunk-Based | GitHub Flow | Git Flow |
|------|:-----------:|:-----------:|:--------:|
| ブランチ寿命 | 数時間〜1-2日 | 数日 | 数日〜数週間 |
| ブランチ数 | 最小 | 少 | 多 |
| リリースモデル | 継続的デプロイ | main マージ = デプロイ | リリースブランチ管理 |
| チーム規模 | 小〜大 (経験豊富) | 小〜中 | 中〜大 |
| 複雑さ | 低 | 低〜中 | 高 |
| 適したプロダクト | SaaS, Web | SaaS, Web | バージョン管理ソフト |

---

## 2. 選定ガイド

```
プロダクト種別？
├── SaaS / Web アプリ
│   ├── CI/CD成熟 + 経験豊富チーム → Trunk-Based
│   └── シンプルさ重視 / 小中規模 → GitHub Flow
└── パッケージ / バージョン管理ソフト
    └── 複数バージョン同時サポート → Git Flow
```

### Trunk-Based Development の前提条件

- CI/CD パイプラインが成熟
- Feature flag インフラが整備
- チームにコードレビューの文化がある
- 自動テストカバレッジが十分

### Git Flow が必要な場面

- 予測可能な長期リリースサイクル
- 複数バージョンの同時サポート
- ホットフィックスの明確な分離が必要

---

## 3. Feature Flags vs Feature Branches

| 観点 | Feature Branches | Feature Flags |
|------|:----------------:|:-------------:|
| 隔離方法 | Gitブランチ | ランタイム制御 |
| デプロイ可能性 | マージ後のみ | フラグ OFF でデプロイ可 |
| A/Bテスト | 困難 | 容易 |
| マージコンフリクト | 長寿命で増加 | 発生しない |
| 技術的負債 | ブランチ削除で解消 | 古いフラグの掃除が必要 |

**2025年の推奨:** 両方を組み合わせる。短寿命 feature branch で開発 → feature flag で本番ロールアウトを制御。

**主要サービス:** LaunchDarkly · Statsig · Unleash · Flagsmith

---

## 4. ブランチ命名規則

```
feature/<issue-id>-<short-description>
fix/<issue-id>-<short-description>
hotfix/<version>-<description>
release/<version>
chore/<description>
```

---

## 5. アンチパターン

| # | パターン | 問題 | 修正 |
|---|---------|------|------|
| 1 | 長寿命ブランチ | マージコンフリクト蓄積 ("merge hell") | 1-2日以内にマージ |
| 2 | main 直接コミット (大規模チーム) | レビューなしのコード混入 | ブランチ保護ルール |
| 3 | 命名不統一 | `feature/`, `feat/`, `f/` 混在 | 命名規則を統一・自動化 |
| 4 | 古いブランチ放置 | リポジトリ汚染 | マージ後に自動削除 |
| 5 | リリースブランチ乱立 | 管理コスト指数的増大 | 必要最小限に制限 |

**Source:** [Trunk-Based vs Git Flow (Assembla)](https://get.assembla.com/blog/trunk-based-development-vs-git-flow/) · [Trunk-Based Development (Atlassian)](https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development) · [Feature Flags vs Branches (Statsig)](https://www.statsig.com/perspectives/feature-flags-vs-feature-branches)
