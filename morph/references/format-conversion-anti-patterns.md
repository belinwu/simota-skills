# Format Conversion Anti-Patterns

> フォーマット変換の失敗パターン、ツール選択ミス、忠実度損失、パイプライン設計の罠

## 1. フォーマット変換 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **FC-01** | **双方向 PDF 変換の誤解** | PDF を入力フォーマットとして扱う | 構造情報の喪失、テキスト抽出の失敗、レイアウト崩壊 | PDF は出力専用フォーマットとして扱う |
| **FC-02** | **中間表現の過信** | Pandoc AST で全フォーマット情報が保持されると仮定 | マージンサイズ、複雑テーブル、カスタムスタイルの消失 | 変換前に非互換要素を特定・ドキュメント化 |
| **FC-03** | **ツール不一致** | 変換ペアに対して不適切なツールを選択 | 品質劣化、機能欠損、不要な依存関係 | conversion-matrix.md のツール選定ガイドに従う |
| **FC-04** | **依存関係の暗黙化** | 必要なフォント・パッケージ・エンジンが未確認 | 「pdflatex not found」「font not installed」エラー | 変換前に全依存関係を明示的に検証 |
| **FC-05** | **品質検証スキップ** | 変換後の出力を検証せずに配布 | 構造崩壊、リンク切れ、画像欠落の見逃し | VERIFY フェーズ必須（構造/視覚/コンテンツ/メタデータ） |
| **FC-06** | **ロスレス変換の幻想** | 全変換がロスレスで行えると仮定 | フォーマット間の表現力差による情報損失 | ロスレス（JSON）vs ロッシー（Markdown/HTML）を明示的に選択 |
| **FC-07** | **単一ツール万能主義** | 全変換に Pandoc だけ / wkhtmltopdf だけを使用 | 特定変換ペアでの品質低下、機能不足 | 変換ペアごとに最適ツールを選定 |

---

## 2. LaTeX/Pandoc 変換の具体的落とし穴

```
LaTeX → Word 変換の既知問題:

  1. 引用文献:
     → Pandoc は .bib ファイルを自動検出しない
     → --citeproc --bibliography=refs.bib を明示必須
     → 解決なしだと引用が [?] になる

  2. 図表:
     → \begin{figure*} が正しく変換されない
     → \begin{figure} への置換が必要
     → キャプションの欠落、参照の未解決

  3. 数式:
     → \Bigl( 等の一部 LaTeX コマンドがエラーを引き起こす
     → \newcommand{\Bigl}{} でノーオップとして再定義
     → 数式番号は pandoc-crossref で補完

  4. カスタムカウンター:
     → Lua フィルターで手動対応が必要
     → 補足資料の図番号等は自動変換不可

  重要な認識:
    「任意の LaTeX ドキュメントをエラーなしで Word に変換する
     ことはおそらく不可能」— ドキュメントの複雑性に依存

  デバッグ手法:
    → 変換失敗時はセクションをコメントアウトして切り分け
    → 問題の原因ブロックを特定してから対処
```

---

## 3. Markdown 変換の制限事項

```
Markdown の表現力制限:

  ❌ 細かいスタイリング制御が不可能
    → フォントサイズ、色、余白の直接指定不可
    → 対策: HTML パススルーで補完

  ❌ 複雑なテーブル:
    → セル結合、ネストテーブルは標準 Markdown 非対応
    → 対策: HTML テーブルを埋め込み

  ❌ ページレイアウト:
    → 改ページ、ヘッダー/フッター、段組は Markdown の範囲外
    → 対策: テンプレート + PDF エンジンで制御

  ❌ フロントマター不一致:
    → YAML フロントマターの変数名がテンプレートと不一致
    → サイレントに失敗（エラーなし）
    → 対策: テンプレートの期待変数を文書化

  Pandoc の中間表現（AST）の限界:
    → フォーマット固有の機能はASTに含まれない
    → 変換は構造要素を保持するが、書式の詳細は保持しない
    → 完全な往復変換（round-trip）は不可能
```

---

## 4. PDF エンジン選択の判断基準

```
PDF エンジンの比較と選定:

  LaTeX (pdflatex/xelatex/lualatex):
    ✅ 高品質な組版、数式サポート
    ❌ インストールサイズ大、学習コスト高、依存関係複雑
    適用: 学術論文、数式を含むドキュメント

  Typst (2023年〜):
    ✅ 軽量、高速、CSS 的な直感的構文
    ❌ バージョン互換性の問題（v0.11 テンプレートが v0.12 で非互換）
    ❌ カスタム変数の Markdown ヘッダー経由渡しが困難
    適用: モダンなドキュメント、軽量パイプライン

  Chrome/Puppeteer (HTML → PDF):
    ✅ Web 技術で完全制御、CSS 活用
    ❌ @page ルールのサポートが限定的
    ❌ ページ余白ルールが非サポート
    適用: Web コンテンツのPDF化、動的ドキュメント

  Prince:
    ✅ CSS Paged Media の最高サポート、20年の実績
    ❌ 商用ライセンス、大規模ドキュメントでメモリ消費大
    適用: 書籍、高品質商用ドキュメント

  WeasyPrint:
    ✅ OSS、CSS Paged Media サポート
    ❌ モダン CSS（padding-inline 等）の部分的非サポート
    ❌ border-radius のクリッピング問題
    適用: OSS プロジェクト、中品質 PDF

  ❌ アンチパターン: エンジン特性を無視した選定
  ✅ 推奨: 品質要件×コスト×依存関係で判断
```

---

## 5. Morph との連携

```
Morph での活用:
  1. ANALYZE フェーズで FC-01〜07 のスクリーニング
  2. conversion-matrix.md と連携した FC-03/FC-07（ツール不一致）防止
  3. CONFIGURE フェーズでエンジン選択判断基準を適用
  4. pandoc-recipes.md と連携した LaTeX/Markdown 変換の既知問題対応

品質ゲート:
  - PDF 入力変換 → 出力専用フォーマットとして拒否（FC-01 防止）
  - 非互換要素の事前特定なし → 変換前リスク評価必須（FC-02 防止）
  - 依存関係未検証 → 変換前の環境チェック必須（FC-04 防止）
  - VERIFY フェーズスキップ → 品質チェック必須（FC-05 防止）
  - ロスレス/ロッシー未区別 → 明示的選択必須（FC-06 防止）
```

**Source:** [Pandoc User's Guide](https://pandoc.org/MANUAL.html) · [LaTeX to Word conversion with Pandoc](https://const-ae.name/post/2024-08-02-latex-to-word-conversion-with-pandoc/) · [Pandoc and Typst for PDF](https://neilzone.co.uk/2025/01/using-pandoc-and-typst-to-convert-markdown-into-custom-formatted-pdfs-with-a-sample-template/) · [Creating Beautiful PDFs](https://michaelnthiessen.com/create-beautiful-pdfs-with-html-css-and-markdown)
