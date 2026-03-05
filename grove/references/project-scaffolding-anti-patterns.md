# Project Scaffolding Anti-Patterns

> プロジェクト初期構造設計の失敗パターン、テンプレートの罠、設定管理の課題

## 1. プロジェクトスキャフォールディング 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **PS-01** | **Template Cargo Cult（テンプレートカーゴカルト）** | FAANG企業のリポジトリ構造をそのまま複製 | 使わないディレクトリが大量に存在、複雑な設定が理解されていない | プロジェクト規模・チームスキルに合った最小構造から開始 |
| **PS-02** | **Skeleton Overload（スケルトン過積載）** | スキャフォールディングで過剰な初期構造を生成 | 空の src/features/auth/, docs/adr/ 等が初日から存在、実コードなし | 必要になった時点で追加（YAGNI）、初期は最小限の構造 |
| **PS-03** | **Config Proliferation（設定ファイル増殖）** | プロジェクト初期から設定ファイルが乱立 | ルートに15+の設定ファイル、重複する設定（.eslintrc.js + .eslintrc.json） | フラットコンフィグ統合、config/ ディレクトリへの集約、設定ツール統合 |
| **PS-04** | **Framework Lock-in Structure（フレームワーク固定構造）** | フレームワーク固有の構造に過度に依存 | Express→Fastify 移行でディレクトリ全体の再設計が必要 | フレームワーク非依存のドメイン中心設計、アダプターパターン |
| **PS-05** | **AI-Generated Chaos（AI生成の混乱）** | AI ツールが独自の構造を発明 | 要求していないディレクトリ構造が生成される、一貫性のないパターン | AI 使用前にスキャフォールディングを完了、CLAUDE.md/rules で構造を指定 |
| **PS-06** | **Monorepo Premature（早すぎるモノレポ化）** | 単一アプリをモノレポ構造で開始 | apps/web/ に1アプリのみ、packages/ に1パッケージのみ、turbo.json の無駄 | 単一リポジトリで開始、パッケージ分割の実際のニーズが発生してから移行 |
| **PS-07** | **Convention Blindness（規約無視）** | 言語/フレームワークの標準規約を無視した構造 | Go で src/ 使用、Next.js で独自ルーティング構造、Django でアプリ構造無視 | 言語検出 → 標準規約テンプレート適用、フレームワーク公式ドキュメント参照 |

---

## 2. 段階的スキャフォールディング戦略

```
Minimal Viable Structure（最小実行可能構造）:

  Phase 0（プロトタイプ）:
    /
    ├── src/           ← ソースコード
    ├── README.md      ← プロジェクト概要
    ├── .gitignore     ← Git 除外設定
    └── (言語設定)     ← package.json / pyproject.toml / go.mod 等

  Phase 1（初期開発 ~20ファイル）:
    /
    ├── src/
    │   └── (フラット構造)
    ├── tests/         ← テスト追加時に作成
    ├── docs/          ← 最初の仕様書作成時に作成
    │   └── README.md
    ├── scripts/       ← 最初のスクリプト作成時に作成
    └── .github/       ← CI/CD 設定時に作成

  Phase 2（成長期 20-100ファイル）:
    src/
    ├── features/      ← 機能別グルーピング開始
    │   ├── auth/
    │   └── user/
    └── shared/        ← 共有コード抽出
    tests/
    ├── unit/
    └── integration/
    docs/
    ├── design/        ← 設計書追加時に作成
    └── adr/           ← 最初の ADR 作成時に作成

  Phase 3（成熟期 100+ファイル）:
    → Feature-Sliced Design or DDD への移行検討
    → モジュール境界の強制（ESLint rules, internal/ 等）
    → パッケージ分割の検討

  原則:
    → 空ディレクトリは作らない（必要になったら作る）
    → 構造はコードの成長に合わせて進化させる
    → 一度に全体を設計しない（段階的リファクタ）
```

---

## 3. 設定ファイル管理戦略

```
Config Hygiene（設定衛生）:

  ルートに必須の設定（移動不可）:
    → package.json / pyproject.toml / go.mod
    → tsconfig.json
    → turbo.json / nx.json（モノレポ）
    → .gitignore

  ルートに推奨の設定:
    → eslint.config.js（フラットコンフィグ）
    → prettier.config.js
    → vitest.config.ts / jest.config.ts

  config/ に移動可能:
    → webpack.config.js
    → postcss.config.js
    → docker-compose.yml

  設定統合のベストプラクティス:
    □ ESLint: .eslintrc.* → eslint.config.js（フラットコンフィグ）
    □ TypeScript: 複数 tsconfig → extends で継承
    □ テストランナー: Jest OR Vitest（両方入れない）
    □ フォーマッター: Prettier OR Biome（両方入れない）
    □ バンドラー: 1つだけ選択（webpack OR vite OR rspack）

  設定ファイル数の目安:
    → 10以下: 健全
    → 10-15: 注意（統合検討）
    → 15+: Config Soup（AP-003）、即時対応
```

---

## 4. テンプレートリポジトリの設計

```
良いテンプレートの条件:

  必須要素:
    □ README.md（プロジェクト概要テンプレート）
    □ .gitignore（言語/フレームワーク適切）
    □ 言語設定ファイル（package.json 等）
    □ CI/CD ワークフロー（.github/workflows/）
    □ .editorconfig（エディタ設定統一）

  任意要素（プロジェクト規模に応じて）:
    □ docs/ 骨格（大規模プロジェクト向け）
    □ tests/ 骨格 + 最初のテスト例
    □ .agents/ ディレクトリ（エージェント活用プロジェクト）
    □ CLAUDE.md / .cursor/rules（AI ツール連携）

  アンチパターン:
    ❌ 使わないツールの設定を含む
    ❌ 空の feature ディレクトリを大量に含む
    ❌ 特定プロジェクトのビジネスロジックを含む
    ❌ ハードコードされたプロジェクト名・URL
    ❌ 古いバージョンのツール/ライブラリ

  テンプレート更新サイクル:
    → 四半期ごとに依存関係更新
    → 新しいベストプラクティス反映（ESLint flat config 等）
    → 実際のプロジェクト経験からのフィードバック反映
```

---

## 5. AI 時代のスキャフォールディング

```
AI ツール連携の考慮事項:

  AI の構造理解を助ける:
    □ CLAUDE.md / .cursor/rules でディレクトリ規約を明示
    □ 命名規約の文書化
    □ barrel export（index.ts）で公開 API を明確化
    □ ディレクトリの README.md で各ディレクトリの責務を記述

  AI 生成の制御:
    □ スキャフォールディングは AI 使用前に完了する
    □ AI が生成するファイルの配置先を明示的に指定
    □ 生成後にディレクトリ構造の一貫性をチェック

  モノレポでの AI 活用:
    → AI アシスタントにリポジトリ全体のコンテキストを提供
    → パッケージ境界を AI が理解できるよう exports フィールドを設定
    → .gitignore で node_modules 等を除外し AI のノイズを削減

  ⚠️ 注意: AI ツールは便利だが、構造の「正解」は
  チーム・規模・ドメインによって異なる
  → AI の提案を無批判に受け入れない（PS-05 防止）
```

---

## 6. 初期構造チェックリスト

```
新規プロジェクト開始時:

  □ 言語/フレームワーク検出
  □ 言語標準の構造規約を確認
  □ 最小実行可能構造で開始（Phase 0）
  □ README.md + .gitignore + 言語設定
  □ CI/CD ワークフロー（基本的なもの）
  □ .editorconfig（チーム統一）

  成長に応じて追加:
  □ tests/ ディレクトリ（最初のテスト作成時）
  □ docs/ ディレクトリ（最初の仕様書作成時）
  □ scripts/ ディレクトリ（最初のスクリプト作成時）
  □ features/ グルーピング（ファイル 20+ 時）
  □ shared/ 抽出（コード重複検出時）
  □ モジュール境界強制（ファイル 100+ 時）

  避けるべきこと:
  ❌ 初日からフル構造を設計
  ❌ 他プロジェクトの構造をそのままコピー
  ❌ 空ディレクトリの大量作成
  ❌ 必要のないツールの設定追加
```

---

## 7. Grove との連携

```
Grove での活用:
  1. DETECT フェーズで PS-01〜07 のスクリーニング
  2. 新規プロジェクトでは段階的スキャフォールディング戦略を適用
  3. 既存プロジェクトでは Config Hygiene チェック
  4. テンプレートリポジトリの定期監査

品質ゲート:
  - FAANG 構造コピー → 規模適合性チェック（PS-01 防止）
  - 空ディレクトリ多数 → 最小構造提案（PS-02 防止）
  - ルート設定 15+ → 統合・移動提案（PS-03 防止）
  - 言語規約違反 → 標準テンプレート提案（PS-07 防止）
  - モノレポ構造に1アプリ → 単一リポジトリ提案（PS-06 防止）
```

**Source:** [Iterators: Project Codebase Organization](https://www.iteratorshq.com/blog/a-comprehensive-guide-on-project-folder-organization/) · [GitHub Well-Architected: Anti-Patterns](https://wellarchitected.github.com/library/scenarios/anti-patterns/) · [FnJoin: Code Your Own Scaffolding First](https://fnjoin.com/post/2025-12-21-code-your-own-scaffolding-first/)
