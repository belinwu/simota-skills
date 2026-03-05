# Conversion Pipeline Anti-Patterns

> 変換パイプラインの設計ミス、CI/CD 統合の落とし穴、バッチ処理の罠、品質保証の盲点

## 1. 変換パイプライン 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **PP-01** | **環境依存の暗黙化** | ローカルで動くがCI/CDで失敗 | 「フォントが見つからない」「ツール不在」エラー | Docker コンテナで全依存関係をパッケージ化 |
| **PP-02** | **生成物のリポジトリコミット** | 生成PDF/Wordをgitにコミット | リポジトリ肥大化、マージコンフリクト、バイナリ差分不能 | CI/CDアーティファクトとして保存、リポジトリには含めない |
| **PP-03** | **全変更での再ビルド** | ドキュメント以外の変更でも変換を実行 | CI/CDパイプラインの遅延、リソース浪費 | docs/ ブランチ・パス変更時のみトリガー |
| **PP-04** | **品質検証の欠如** | 変換後の出力を自動検証しない | 構造崩壊・画像欠落・リンク切れの見逃し | 自動品質チェックをパイプラインに組み込み |
| **PP-05** | **エラーハンドリングの欠如** | 変換エラーを無視して続行 | 不完全な出力の配布、サイレント失敗 | エラー時の明示的失敗 + 通知 + ロールバック |
| **PP-06** | **シンタックスの不整合** | Markdown の方言差によるフォーマット崩壊 | ツールごとに異なる出力、予期しないレンダリング | Markdown リンター + 標準方言の統一（CommonMark 等） |
| **PP-07** | **テンプレートのハードコード** | スタイルを変換スクリプトに直接埋め込み | スタイル変更のたびにスクリプト修正、再利用性ゼロ | テンプレート/スタイルシートの外部化 + 変数化 |

---

## 2. Docker コンテナ化のベストプラクティス

```
変換パイプラインの Docker 化:

  推奨 Dockerfile 構成:
    FROM pandoc/extra:latest
    # LaTeX、フォント、追加ツールを含む

    # 日本語フォントの追加
    RUN apt-get update && apt-get install -y \
        fonts-noto-cjk fonts-noto-cjk-extra

    # 追加ツール
    RUN apt-get install -y \
        librsvg2-bin \  # SVG 処理
        mermaid-cli     # Mermaid 図レンダリング

  利点:
    → ローカル/CI/CD 環境の完全一致
    → 依存関係の明示的管理
    → バージョン固定による再現性

  ❌ アンチパターン: ベースイメージの latest タグ
    → バージョンアップで突然の破綻
  ✅ 推奨: 特定バージョンをピン留め
    → pandoc/extra:3.1.12
```

---

## 3. CI/CD パイプライン設計パターン

```
GitHub Actions 推奨構成:

  トリガー設計:
    on:
      push:
        paths: ['docs/**', 'templates/**']
        branches: [main]
    → ドキュメント変更時のみ実行
    → 不要なビルドを回避（PP-03 防止）

  アーティファクト管理:
    → 生成物は actions/upload-artifact で保存
    → リリース時は GitHub Release にアタッチ
    → リポジトリには PDF/Word をコミットしない（PP-02 防止）

  品質ゲート:
    → 変換成功の検証（exit code チェック）
    → 出力ファイルの存在確認
    → ファイルサイズの妥当性チェック（0 バイト防止）
    → 構造検証（見出し数、ページ数等）

  エラー通知:
    → 変換失敗時の Slack/Email 通知
    → エラーログのアーティファクト保存
    → 前回成功出力へのフォールバック

  バッチ処理:
    → 複数ドキュメントの並列変換
    → 変更されたファイルのみの差分変換
    → マトリクスビルドでの複数フォーマット同時生成
```

---

## 4. 品質保証の自動化

```
変換品質の自動検証:

  Level 1: 基本検証（全変換で必須）
    □ 出力ファイルの存在
    □ ファイルサイズ > 0
    □ MIME タイプの正確性
    □ 変換エラー/警告なし

  Level 2: 構造検証（重要ドキュメントで推奨）
    □ 見出し構造の保持（H1→H2→H3 の階層）
    □ 画像の全数存在確認
    □ ハイパーリンクの有効性
    □ テーブル構造の保持

  Level 3: 忠実度検証（配布ドキュメントで必須）
    □ フォントの正確な埋め込み
    □ ページ番号の正確性
    □ TOC のページ番号一致
    □ クロスリファレンスの解決

  Level 4: アクセシビリティ検証（公開ドキュメントで必須）
    □ PDF/UA 準拠
    □ タグ構造の適切性
    □ 代替テキストの存在
    □ コントラスト比の充足

  ❌ アンチパターン: Level 1 のみで出荷
  ❌ アンチパターン: 手動検証のみに依存
  ✅ 推奨: Level 1-2 は全自動、Level 3-4 は配布時に自動+手動
```

---

## 5. バージョン互換性管理

```
ツールバージョンの互換性問題:

  Pandoc:
    → メジャーバージョン間でテンプレート構文が変更
    → Lua フィルター API の破壊的変更
    → 対策: バージョン固定 + 変更ログ確認

  Typst:
    → 急速な進化（v0.11 テンプレートが v0.12 で非互換）
    → テンプレートのバージョン依存が高い
    → 対策: Typst バージョンとテンプレートをセットで管理

  LaTeX:
    → パッケージの非互換性（年次更新で破綻のリスク）
    → 対策: TeX Live のバージョン固定（Docker で管理）

  Mermaid CLI:
    → 構文の進化でレンダリング結果が変化
    → 対策: バージョン固定 + レンダリング結果の差分確認

  ✅ 推奨: 全ツールのバージョンを lockfile で管理
  ✅ 推奨: 変換結果のスナップショットテスト導入
```

---

## 6. Morph との連携

```
Morph での活用:
  1. CONFIGURE フェーズで PP-01〜07 のスクリーニング
  2. conversion-workflow.md と連携したパイプライン設計
  3. VERIFY フェーズで品質検証の自動化レベルを選定
  4. conversion-calibration.md と連携した品質追跡

品質ゲート:
  - 環境依存の暗黙化 → Docker コンテナ化必須（PP-01 防止）
  - 生成物リポジトリコミット → アーティファクト管理（PP-02 防止）
  - 全変更再ビルド → パストリガー設定（PP-03 防止）
  - 品質検証なし → 自動検証パイプライン必須（PP-04 防止）
  - エラー無視 → 明示的失敗+通知（PP-05 防止）
  - テンプレート埋め込み → 外部テンプレート管理（PP-07 防止）
  - バージョン未固定 → lockfile + スナップショットテスト（互換性管理）
```

**Source:** [freeCodeCamp: Automate Documentation Conversion with Pandoc](https://www.freecodecamp.org/news/how-to-automate-documentation-conversion-with-pandoc-in-cicd-pipelines) · [BladeDocs: Automating Documentation Conversion](https://bladedocs.com/dev-tools/automating-documentation-conversion-with-pandoc-in-your-ci-cd-pipeline/) · [Generating PDFs with Pandoc](https://lornajane.net/posts/2023/generating-a-nice-looking-pdf-with-pandoc)
