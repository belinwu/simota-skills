# CSS Print & Paged Media Anti-Patterns

> CSS 印刷スタイルの落とし穴、ページ制御の罠、ツール間互換性問題、タイポグラフィ課題

## 1. CSS 印刷スタイル 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **CP-01** | **ページ分割の無制御** | break-before/break-after/break-inside 未設定 | コードブロック・画像・テーブルがページ境界で分断 | `break-inside: avoid` + 要素種別ごとの分割制御 |
| **CP-02** | **ウィドウ/オーファン放置** | 段落の最初/最後の行が孤立 | 1行だけ次/前ページに残る | `widows: 3; orphans: 3;` で最小行数を設定 |
| **CP-03** | **ダークテーマのそのまま印刷** | コードブロックのダークテーマを印刷に適用 | インク浪費、可読性低下、印刷コスト増大 | `@media print` でライトテーマに切り替え + ボーダー追加 |
| **CP-04** | **モダン CSS の過信** | PDF ツールがモダン CSS をサポートすると仮定 | `padding-inline`、`overflow-wrap: anywhere` 等が無視される | レガシーフォールバック（`padding-left/right`、`word-break: break-all`） |
| **CP-05** | **ブラウザ印刷プレビューの過信** | ブラウザ DevTools でのプレビューを最終出力と同一視 | `@page` ルール非表示、ページ余白ルール非サポート | ブラウザは初期確認用、最終検証は実際の PDF 生成で |
| **CP-06** | **長い文字列の未処理** | URL・メールアドレス・コード変数の折り返し未設定 | コンテナからのオーバーフロー、レイアウト崩壊 | `word-break: break-all !important` + `overflow-wrap` |
| **CP-07** | **@page ルールのスコープ問題** | CSS Modules 内に `@page` を記述 | ページ設定が無視される（CSS Modules 外に配置必須） | `@page` ルールはグローバルスタイルシートに配置 |

---

## 2. ブラウザ vs PDF ツール互換性マトリクス

```
CSS 機能のサポート状況:

  機能               | ブラウザ | Prince | WeasyPrint | Chrome PDF
  -------------------|---------|--------|------------|----------
  @page              | ❌      | ✅     | ✅         | △（限定）
  @page :first       | ❌      | ✅     | ✅         | ❌
  @top-left 等余白   | ❌      | ✅     | ✅         | ❌
  break-before/after | ✅      | ✅     | ✅         | ✅
  break-inside       | ✅      | ✅     | ✅         | ✅
  widows/orphans     | ✅      | ✅     | ✅         | ✅
  counter(page)      | ❌      | ✅     | ✅         | ❌
  padding-inline     | ✅      | △      | ❌         | ✅
  overflow-wrap      | ✅      | △      | ❌         | ✅
  CSS Grid/Flexbox   | ✅      | ✅     | △          | ✅
  border-radius clip | ✅      | ✅     | ❌         | ✅

  ❌ アンチパターン: 全ツール共通 CSS を書く
  ✅ 推奨: ターゲットツール別のスタイルシートを管理

  CSS Paged Media コンバーターの特性:
    → 印刷固有のスタイリングはブラウザより良いサポート
    → しかしモダン CSS 構文のサポートは劣る
    → 「古い CSS + 印刷固有機能」が最も安全な組み合わせ
```

---

## 3. ページレイアウト制御のベストプラクティス

```
ページ設定:

  1. ページサイズ・マージン:
     @page { size: a4; margin: 2cm 2.5cm; }
     → 日本語ドキュメント: A4 が標準

  2. ページ番号:
     @page { @bottom-center { content: "Page " counter(page); } }
     → ブラウザ非サポート、Prince/WeasyPrint のみ

  3. 最初のページの差別化:
     @page :first { margin-top: 0; }
     counter-set: page 0; で番号リセット

  4. 改ページ制御:
     h1 { break-before: page; }              // 章ごとに改ページ
     figure { break-inside: avoid; }          // 図を分割しない
     .chapter { break-before: right; }        // 書籍: 右ページ開始

  5. リンク URL の表示:
     @media print {
       a[href]:not([href^="#"])::after {
         content: " (" attr(href) ")";
       }
     }
     → アンカーリンクは除外（#始まり）

  6. 非表示要素:
     .no-print { display: none !important; }
     → Tailwind: print:hidden ユーティリティ
```

---

## 4. 印刷スタイル開発ワークフロー

```
効率的な開発フロー:

  Phase 1: ブラウザ DevTools（高速イテレーション）
    → @media print のシミュレーション
    → DOM・CSS のインスペクション
    → 制限: ページ分割は表示されない

  Phase 2: ブラウザ印刷プレビュー（ページ確認）
    → 実際のページ分割位置の確認
    → break-before/after の動作検証
    → 制限: @page 余白ルールは反映されない

  Phase 3: 実 PDF 生成（最終検証）
    → Prince/WeasyPrint/Chrome でPDF出力
    → 全 CSS Paged Media 機能の動作確認
    → ページ番号・ヘッダー/フッターの検証

  ❌ アンチパターン: Phase 3 のみで開発
    → イテレーション速度が極端に低下
  ❌ アンチパターン: Phase 1 のみで完了と判断
    → 印刷固有機能が未検証

  ✅ 推奨: Phase 1 → Phase 2 → Phase 3 の段階的検証

  重要な注意点:
    → 印刷スタイルの CSS 標準化は遅い（権威的リソースは 2011-2018 年）
    → 既存技術スタックへの統合は「少し面倒」になりがち
    → 古い CSS 構文と新しい構文の混在が必要
```

---

## 5. Morph との連携

```
Morph での活用:
  1. CONFIGURE フェーズで CP-01〜07 のスクリーニング
  2. template-library.md と連携した CSS テンプレートの品質管理
  3. conversion-matrix.md と連携したツール互換性確認
  4. VERIFY フェーズでページレイアウト検証を適用

品質ゲート:
  - ページ分割制御なし → break-inside/before/after 設定必須（CP-01 防止）
  - ダークテーマコード → @media print でライト切り替え（CP-03 防止）
  - モダン CSS のみ → レガシーフォールバック追加（CP-04 防止）
  - ブラウザプレビューのみ → 実 PDF 生成での最終検証必須（CP-05 防止）
  - @page ルール → グローバルスタイルシート配置確認（CP-07 防止）
```

**Source:** [DiDoesDigital: CSS Print Styles for PDFs](https://didoesdigital.com/blog/print-styles/) · [Michael Thiessen: Create Beautiful PDFs with HTML, CSS, and Markdown](https://michaelnthiessen.com/create-beautiful-pdfs-with-html-css-and-markdown)
