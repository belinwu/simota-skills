# Tool Integration Anti-Patterns

> Linter/Formatter設定、ビルドツール統合、CI/CD連携の失敗パターン

## 1. Linter/Formatter設定 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **TI-01** | **Config Fragmentation（設定ファイル分散）** | 10+の依存関係と3+の設定ファイルが必要 | ESLint + Prettier + tsconfig + .editorconfig + lint-staged が必要、初期設定に30分+ | 統合ツール採用（Biome = lint+format）、プリセット設定の提供 |
| **TI-02** | **Rule Suppression Addiction（ルール無効化中毒）** | 理解せずに lint ルールを `// eslint-disable` で無効化 | ファイル先頭に大量の disable コメント、実質的にlintが機能していない | disable理由の必須記載、baselineファイルで既存違反を管理、新規コードは厳格に |
| **TI-03** | **Version Conflict Hell（バージョン競合地獄）** | Linter/Formatter/Plugin間のバージョン互換性問題 | `npm install` 時に peer dependency 警告、実行時エラー | ロックファイルの厳格管理、互換性テスト済みプリセットの使用 |
| **TI-04** | **Format-on-Save Only（保存時フォーマットのみ）** | エディタ設定に依存し、CI/CDでの検証がない | チームメンバーのエディタ設定差異で不整合、PRでフォーマット差分が大量発生 | CI/CDでフォーマットチェック必須化、pre-commit hookの導入 |
| **TI-05** | **Inconsistent Tool Chain（ツールチェーン不整合）** | ローカル開発とCI/CDで異なるツール/バージョンを使用 | ローカルではパスするがCIでは失敗、環境依存のバグ | mise/asdf でツールバージョンをピン留め、CI/CDでも同じツール使用 |
| **TI-06** | **Kitchen Sink Config（全部入り設定）** | 推奨ルールセットを全て有効化し、プロジェクトに不要なルールも適用 | 意味のない警告が大量発生、開発者がlintを無視する文化の醸成 | プロジェクトに必要なルールのみ選択、段階的にルール追加 |
| **TI-07** | **No Baseline Strategy（ベースライン戦略なし）** | 既存コードベースに新ルールを一括適用 | 数千の既存違反が発生、修正が不可能で結局ルールを無効化 | ベースライン設定で既存違反を凍結、新規コードのみ厳格適用 |

---

## 2. ビルドツール統合のアンチパターン

```
ビルド統合の罠:

  ❌ Slow Feedback Loop（遅いフィードバックループ）:
    → ファイル変更からlint/テスト結果まで10秒以上
    → 開発者がフィードバックを待たず先に進む、バグの見落とし
    → 対策: インクリメンタルビルド、ファイル変更のみ再チェック、キャッシュ活用

  ❌ Global Install Dependency（グローバルインストール依存）:
    → ツールのグローバルインストールを前提
    → チーム間のバージョン差異、新メンバーのセットアップ困難
    → 対策: npx/pipx/go run による実行、プロジェクトローカルインストール

  ❌ Implicit Tool Resolution（暗黙のツール解決）:
    → PATH上の最初に見つかったツールバージョンを使用
    → 環境によって異なるバージョンが実行、再現不能な結果
    → 対策: mise/asdf でプロジェクト単位のバージョン固定

  ❌ Monolithic Check Script（モノリシックチェックスクリプト）:
    → `npm run check` で lint+format+test+build を一括実行
    → 最初の失敗で停止、並列実行不可、個別実行不可
    → 対策: 個別コマンド化 + 集約コマンド提供、並列実行サポート

  ❌ No Cache Strategy（キャッシュ戦略なし）:
    → CI/CDで毎回フルビルド・フル lint
    → ビルド時間の増大、CI/CDコスト増加
    → 対策: ツール固有のキャッシュ（ESLint --cache, Biome --cached）活用

  ❌ Hook Bypass Culture（Hook バイパス文化）:
    → --no-verify でpre-commitフックを常にスキップ
    → フックの存在意義が消失、品質ゲートが機能しない
    → 対策: CIでの必須チェック、フックの実行時間短縮（5秒以内目標）
```

---

## 3. テストランナー統合のアンチパターン

```
テスト統合の罠:

  ❌ Inconsistent Test Commands（テストコマンド不整合）:
    → プロジェクトごとに異なるテスト実行方法
    → 新メンバーが実行方法を毎回調べる必要
    → 対策: package.json/Makefile/Taskfile に標準コマンドを定義

  ❌ No Watch Mode（ウォッチモード未提供）:
    → テストの手動再実行が必要
    → フィードバックループの断絶
    → 対策: --watch フラグでファイル変更監視+自動再実行

  ❌ All-or-Nothing Testing（全か無かテスト）:
    → 変更ファイルに関係なくフルテストスイート実行
    → テスト実行に数分、開発者がテスト実行を避ける
    → 対策: 影響テストのみ実行（--changed/--related-tests）

  ❌ Noisy Test Output（騒がしいテスト出力）:
    → 成功テストも含め全詳細を出力
    → 失敗箇所の特定が困難
    → 対策: デフォルトは失敗のみ表示、--verbose で全出力

  ❌ No Parallel Execution（並列実行なし）:
    → テストを逐次実行
    → テストスイート全体の実行時間が線形に増加
    → 対策: テストランナーの並列実行設定（--parallel, --workers）
```

---

## 4. Doctor/Healthcheck パターンのアンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **DH-01** | **No Doctor Command（Doctor未提供）** | 環境問題の診断手段がない | ユーザーが手動でバージョン確認・設定確認を実施 | `app doctor` コマンドで環境チェックを一括実行 |
| **DH-02** | **Diagnostic Without Fix（診断のみ修正なし）** | 問題を検出するが修復コマンドを提示しない | ユーザーが修正方法を自力で調べる必要 | 問題ごとに具体的な修正コマンドを提示 |
| **DH-03** | **Silent Dependency（暗黙の依存関係）** | 必要なツールが未インストール時に暗号的なエラー | `command not found` や `ENOENT` エラー | 起動時に依存チェック、未インストールならインストール手順を表示 |
| **DH-04** | **Version Ambiguity（バージョン曖昧性）** | 必要なバージョン範囲が不明確 | 古いバージョンで不可解なエラー | `doctor` で現在/必要バージョンを並べて表示 |

---

## 5. 設定管理のアンチパターン

```
設定管理の罠:

  ❌ Config Discovery Mystery（設定ファイル探索の謎）:
    → どの設定ファイルが実際に読み込まれているか不明
    → 設定が効かない原因が特定できない
    → 対策: --config-debug で読み込まれた設定ファイルのパスと優先順位を表示

  ❌ Schema-less Config（スキーマなし設定）:
    → 設定ファイルのバリデーションなし
    → タイプミスが無言で無視される（例: `colr: true` が `color: true` の代わり）
    → 対策: JSONスキーマ定義、起動時バリデーション、タイプミス候補の提示

  ❌ Breaking Config Changes（設定の破壊的変更）:
    → バージョンアップで設定フォーマットが変わり既存設定が動かない
    → アップデート後に突然動作しなくなる
    → 対策: 設定バージョニング、マイグレーションガイド/コマンドの提供

  ❌ No Default Config（デフォルト設定なし）:
    → 設定ファイルの作成がないと起動できない
    → 初回起動の障壁が高い
    → 対策: ゼロコンフィグで合理的なデフォルト動作、`app init` で設定生成
```

---

## 6. Anvil との連携

```
Anvil での活用:
  1. BLUEPRINT フェーズで TI-01〜07 のツール統合設計レビュー
  2. CAST フェーズでビルドスクリプト・コマンド構造の検証
  3. HARDEN フェーズでCI/CD連携・クロス環境動作の確認
  4. PRESENT フェーズで Doctor コマンド・設定管理の品質チェック

品質ゲート:
  - 設定ファイル3+種 → 統合ツール提案（TI-01 防止）
  - disable コメント5+個/ファイル → ベースライン戦略導入（TI-02 防止）
  - グローバルインストール前提 → npx/pipx 方式に変更（Global Install 防止）
  - フルビルドが10秒超 → キャッシュ/インクリメンタル対応（Slow Feedback 防止）
  - Doctor コマンド未提供 → 環境チェック実装提案（DH-01 防止）
  - 設定バリデーションなし → JSONスキーマ導入提案（Schema-less Config 防止）
```

**Source:** [Meta: Fixit 2 Linter](https://engineering.fb.com/2023/08/07/developer-tools/fixit-2-linter-meta/) · [Command Line Interface Guidelines](https://clig.dev/) · [Atlassian: 10 Design Principles for Delightful CLIs](https://www.atlassian.com/blog/it-teams/10-design-principles-for-delightful-clis) · [ESLint Documentation](https://eslint.org/)
