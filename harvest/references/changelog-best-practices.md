# Changelog & Release Notes Best Practices

> Keep a Changelog 原則、Conventional Commits 連携、オーディエンス別ライティング、アンチパターン

## 1. Keep a Changelog 原則

### 基本原則

```
1. チェンジログは人間のためのもの — マシンのためではない
2. すべてのバージョンにエントリを記載する
3. 同じ種類の変更はグループ化する
4. バージョンとセクションはリンク可能にする
5. 最新バージョンを先頭に表示する
6. 各リリースの日付を表示する
7. Semantic Versioning に従っているか明記する
```

### 変更カテゴリ（6分類）

| カテゴリ | 用途 | 日本語対応 |
|---------|------|-----------|
| **Added** | 新機能の追加 | 追加 |
| **Changed** | 既存機能の変更 | 変更 |
| **Deprecated** | 将来削除予定の機能 | 非推奨 |
| **Removed** | 削除された機能 | 削除 |
| **Fixed** | バグ修正 | 修正 |
| **Security** | セキュリティ脆弱性のパッチ | セキュリティ |

### Unreleased セクション

```
## [Unreleased]
- 次回リリースに含まれる変更を随時追記
- リリース時に [Unreleased] → [X.Y.Z] - YYYY-MM-DD に変更
- ユーザーが今後の変更を事前確認できる
```

---

## 2. Conventional Commits との連携

### マッピングルール

| Commit Type | Changelog カテゴリ | SemVer |
|-------------|-------------------|--------|
| `feat` | Added | MINOR |
| `fix` | Fixed | PATCH |
| `feat!` / `BREAKING CHANGE` | Changed (破壊的変更) | MAJOR |
| `perf` | Changed | PATCH |
| `refactor` | — (通常は記載不要) | — |
| `docs` | — (通常は記載不要) | — |
| `test` | — (通常は記載不要) | — |
| `chore` | — (通常は記載不要) | — |
| `ci` | — (通常は記載不要) | — |
| `build` | — (通常は記載不要) | — |
| `style` | — (通常は記載不要) | — |
| `deprecate` | Deprecated | — |
| `security` | Security | PATCH |

### Harvest 用カテゴリ検出ルール

```
既存ルール（report-templates.md）との統合:
  PR タイトルから Conventional Commits プレフィックスを検出:
    feat:     → Added
    fix:      → Fixed
    perf:     → Changed (パフォーマンス)
    security: → Security
    deprecate:→ Deprecated

  フォールバック（プレフィックスなし）:
    キーワード検出で分類（既存ロジックを維持）

  除外対象（changelog 不要）:
    refactor, docs, test, chore, ci, build, style
    → Internal Changes として折りたたみ可能
```

---

## 3. オーディエンス別ライティング

### 2 バージョン戦略

| 項目 | Customer-facing | Developer-facing |
|------|----------------|-----------------|
| **対象** | エンドユーザー · PM · ステークホルダー | 開発者 · SRE · QA |
| **言語** | ビジネス用語 · ユーザー視点 | 技術用語 · 実装視点 |
| **詳細度** | 影響と改善点のみ | PR番号 · 技術的変更点 |
| **例** | 「検索結果の表示速度が改善されました」 | 「検索クエリのN+1問題を修正 (#1234)」 |
| **Breaking Changes** | 「○○の操作方法が変わります」 | 「API v2 の /users エンドポイントの応答形式変更」 |
| **形式** | 箇条書き · カテゴリ別 | PR リンク付き · コミットハッシュ参照 |

### ライティングガイドライン

```
Good（ユーザー視点）:
  ✓ "ダッシュボードの読み込みが 40% 高速化されました"
  ✓ "CSVエクスポートで日本語の文字化けが解消されました"
  ✓ "チーム招待メールにプレビュー画像が追加されました"

Bad（実装視点 — changelog に書くべきでない）:
  ✗ "React.memo を追加してリレンダリングを最適化"
  ✗ "user_exports テーブルに encoding カラムを追加"
  ✗ "SendGrid テンプレートを更新"
```

---

## 4. Changelog 8 大アンチパターン

| # | アンチパターン | 問題 | 対策 |
|---|-------------|------|------|
| **CL-01** | **git log のコピペ** | マージコミット · 内部リファクタ · WIP コミットがノイズ | PR タイトル + 手動キュレーション |
| **CL-02** | **変更の省略** | 重要な変更が記載漏れ → ユーザーの信頼低下 | PR マージ時にchangelog要否を判定するチェックリスト |
| **CL-03** | **非推奨の未記載** | deprecation を記載しない → 突然の削除でユーザー混乱 | Deprecated カテゴリを必ず使用 |
| **CL-04** | **日付フォーマット不統一** | 地域依存の日付形式 → 国際チームで混乱 | ISO 8601 (YYYY-MM-DD) を強制 |
| **CL-05** | **バージョン番号なし** | タイムスタンプのみ → どのリリースかの追跡が困難 | SemVer + 日付の併記 |
| **CL-06** | **全部 "Fixed"** | あらゆる変更を Fixed に分類 → カテゴリの意味が消失 | 6 カテゴリの正確な使い分けを徹底 |
| **CL-07** | **内部変更の露出** | リファクタリング・CI変更を記載 → ユーザーにとってノイズ | ユーザー影響のある変更のみ記載 |
| **CL-08** | **破壊的変更の埋没** | Breaking change が通常の変更に紛れる → 見落としで障害 | 破壊的変更は専用セクション or 先頭に配置 · `!` マーク |

---

## 5. リリースノート品質チェックリスト

```
生成前チェック:
  □ PR が Conventional Commits プレフィックスで分類済みか
  □ 期間内の全 PR が取得されているか（漏れなし）
  □ Breaking changes が明示的に識別されているか

内容チェック:
  □ ユーザー視点の記述になっているか（CL-07 防止）
  □ 6 カテゴリが正確に使い分けられているか（CL-06 防止）
  □ Deprecated がある場合、移行ガイドが記載されているか
  □ 日付が ISO 8601 形式か（CL-04 防止）
  □ 破壊的変更が目立つ位置にあるか（CL-08 防止）

形式チェック:
  □ 最新バージョンが先頭か
  □ PR 番号のリンクが含まれているか（Developer 版）
  □ Unreleased セクションが維持されているか
```

---

## 6. Yanked リリースの記載

```
撤回されたリリースの記載方法:

## [0.3.0] - 2024-03-15 [YANKED]
> ⚠️ このリリースは重大な問題により撤回されました。0.3.1 をご利用ください。

用途:
  - セキュリティ脆弱性が発見された場合
  - データ破損リスクがある場合
  - 重大なリグレッションが含まれていた場合
```

---

## 7. Harvest との連携

```
Harvest での活用:
  1. Release Notes レポートで 6 カテゴリ分類を標準適用
  2. PR タイトルから Conventional Commits プレフィックスを自動検出
  3. CL-01〜08 のアンチパターンチェックを生成時に適用
  4. Customer-facing / Developer-facing の 2 バージョン生成オプション
  5. Breaking changes を自動ハイライト

品質ゲート:
  - git log のコピペ検出 → 警告（CL-01 防止）
  - 全 PR が同一カテゴリ → 再分類を提案（CL-06 防止）
  - 破壊的変更が通常セクションに混在 → 分離を提案（CL-08 防止）
  - 日付形式が ISO 8601 でない → 自動変換
```

**Source:** [Keep a Changelog v1.1.0](https://keepachangelog.com/en/1.1.0/) · [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) · [GitLab: Writing Changelogs](https://docs.gitlab.com/ee/development/changelog.html) · [GitHub: Automatically Generated Release Notes](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes)
