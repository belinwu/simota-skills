# WCAG 2.2 & Inclusive Design Evolution

> WCAG 2.2 新基準、よくある違反パターン、インクルーシブデザインのベストプラクティス

## 1. WCAG 2.2 新基準（2.1 からの追加）

| レベル | 基準 | 概要 | 影響範囲 |
|--------|------|------|---------|
| **A** | 2.4.11 Focus Not Obscured (Minimum) | フォーカス要素がスティッキーヘッダー等で完全に隠れない | フォーム、ナビゲーション |
| **A** | 3.2.6 Consistent Help | ヘルプ機能の配置が全ページで一貫 | サイト全体 |
| **A** | 3.3.7 Redundant Entry | 同一セッション内で同じ情報の再入力を求めない | フォーム、チェックアウト |
| **AA** | 2.4.12 Focus Not Obscured (Enhanced) | フォーカス要素が一部分でも隠れない | フォーム、ナビゲーション |
| **AA** | 2.4.13 Focus Appearance | フォーカスインジケータが十分なサイズ・コントラスト | 全インタラクティブ要素 |
| **AA** | 2.5.7 Dragging Movements | D&D に単一ポインタ代替操作を提供 | D&D、スライダー、ソート |
| **AA** | 2.5.8 Target Size (Minimum) | タッチターゲット最小 24×24 CSS px | 全タップ可能要素 |
| **AA** | 3.3.8 Accessible Authentication (Minimum) | 認証に認知テスト（CAPTCHA 等）不要 | ログイン、認証 |
| **AA** | 3.3.9 Accessible Authentication (Enhanced) | パスワードマネージャー対応必須 | ログイン、認証 |

---

## 2. よくある a11y 違反 8 パターン

| # | 違反パターン | WCAG 基準 | 検出手段 | 修正策 |
|---|------------|----------|---------|--------|
| **AV-01** | **Div ボタン** | 4.1.2 | 手動/axe | `<div onclick>` → `<button>` に変更 |
| **AV-02** | **プレースホルダのみラベル** | 3.3.2 | axe/手動 | 常時表示 `<label>` を追加 |
| **AV-03** | **色のみのエラー表示** | 1.4.1 | 手動 | アイコン + テキストを併用 |
| **AV-04** | **スティッキー要素によるフォーカス隠蔽** | 2.4.11 | キーボードテスト | `scroll-padding-top` で余白確保 |
| **AV-05** | **D&D のみの操作** | 2.5.7 | キーボードテスト | ボタン/Arrow key での代替操作提供 |
| **AV-06** | **ARIA 過剰使用** | 4.1.2 | axe | セマンティック HTML 優先、ARIA は補助のみ |
| **AV-07** | **小さなタッチターゲット** | 2.5.8 | 自動計測 | 最小 24×24px、推奨 44×44px |
| **AV-08** | **オーバーレイウィジェット依存** | 全般 | レビュー | コード自体を修正、ウィジェットは不十分 |

---

## 3. セマンティック HTML 優先ガイド

```
HTML 要素の選択フレームワーク:

  Step 1: ネイティブ HTML 要素で実現可能か？
    <button>  → クリック操作（keyboard/focus/role 自動付与）
    <a href>  → ナビゲーション
    <input>   → データ入力
    <select>  → 選択肢（限定的）
    <dialog>  → モーダル（showModal() でフォーカストラップ自動）
    <details> → 折りたたみ/展開
    <nav>     → ナビゲーション領域
    <main>    → 主要コンテンツ
    → YES: ネイティブ要素を使用（ARIA 不要）

  Step 2: カスタムウィジェットが必要な場合
    → アクセシブルコンポーネントライブラリを使用:
      - Radix UI Primitives（unstyled、完全 a11y）
      - React Aria（Adobe、30+ 言語対応）
      - shadcn/ui（Radix ベース + Tailwind）
      - Headless UI（軽量、Tailwind フォーカス）

  Step 3: 手動 ARIA が必要な場合（最終手段）
    - アイコンボタン: aria-label on <button>
    - 動的コンテンツ: aria-live regions
    - 複合ウィジェット: role + aria-expanded + aria-controls
    - 複数ランドマーク: aria-label で区別
```

---

## 4. フォーカス管理パターン（WCAG 2.2 対応）

```
フォーカス隠蔽の防止（2.4.11/2.4.12）:

  CSS 対策:
    html {
      scroll-padding-top: 80px;  /* スティッキーヘッダーの高さ */
      scroll-padding-bottom: 60px;  /* スティッキーフッターの高さ */
    }

  JavaScript 対策:
    // フォーカス時にスティッキー要素との重なりを検出
    element.addEventListener('focus', () => {
      const rect = element.getBoundingClientRect();
      const headerHeight = stickyHeader.offsetHeight;
      if (rect.top < headerHeight) {
        window.scrollBy(0, rect.top - headerHeight - 16);
      }
    });

フォーカスインジケータ（2.4.13）:
  要件:
    - 最小面積: 要素の全周 2px 以上、または同等面積
    - コントラスト: 隣接色に対して 3:1 以上
    - フォーカス/非フォーカスの差: 3:1 以上

  推奨実装:
    :focus-visible {
      outline: 2px solid var(--focus-color, #2563eb);
      outline-offset: 2px;
    }

D&D 代替操作（2.5.7）:
  ❌ ドラッグのみでソート可能なリスト
  ✅ ドラッグ + 上下ボタン + キーボード Arrow key
  ✅ ドラッグ + 「移動先を選択」ドロップダウン

冗長入力の防止（3.3.7）:
  ❌ 配送先住所と請求先住所の二重入力
  ✅ 「請求先と同じ」チェックボックス
  ✅ 前回入力のオートフィル
  ✅ セッション内の値を自動保持
```

---

## 5. 認証アクセシビリティ（3.3.8/3.3.9）

```
禁止パターン:
  ❌ テキスト CAPTCHA（手動書き写し）
  ❌ パズル CAPTCHA（画像認識タスク）
  ❌ パスワードのコピーペースト禁止
  ❌ パスワードマネージャーのブロック
  ❌ 二要素認証でのコード手動入力のみ

推奨パターン:
  ✅ reCAPTCHA v3（ユーザー操作不要）
  ✅ パスワードマネージャー対応（autocomplete 属性）
  ✅ WebAuthn/パスキー認証
  ✅ マジックリンク認証
  ✅ OTP 自動入力（autocomplete="one-time-code"）

フォーム autocomplete 属性:
  <input type="email" autocomplete="email" />
  <input type="password" autocomplete="current-password" />
  <input type="text" autocomplete="one-time-code" inputmode="numeric" />
  <input type="text" autocomplete="name" />
  <input type="tel" autocomplete="tel" />
```

---

## 6. Reduced Motion とインクルーシブ設計

```
前庭障害への配慮:
  - 40 歳以上の成人の約 35% が前庭機能障害を経験
  - アニメーションは吐き気、めまい、不快感を引き起こしうる

実装アプローチ（Progressive Enhancement）:
  /* ベース: アニメーションなし */
  .card { opacity: 1; transform: none; }

  /* モーション許可時のみアニメーション */
  @media (prefers-reduced-motion: no-preference) {
    .card {
      transition: opacity 300ms ease, transform 300ms ease;
    }
  }

テーマとカスタマイズ:
  - high-contrast: コントラスト比強化モード
  - large-text: ベースフォントサイズ拡大
  - reduced-motion: アニメーション抑制
  - forced-colors: Windows ハイコントラスト対応

SVG アイコンのアクセシビリティ:
  装飾的アイコン（テキストあり）:
    <svg aria-hidden="true" focusable="false">...</svg>

  アイコンのみボタン:
    <button aria-label="保存">
      <svg aria-hidden="true">...</svg>
    </button>

  情報を持つ SVG（チャート等）:
    <svg role="img" aria-labelledby="title desc">
      <title id="title">月次売上</title>
      <desc id="desc">1月100万円から6月150万円へ増加</desc>
    </svg>
```

---

## 7. 法的コンプライアンス状況（2025-2026）

```
規制タイムライン:
  2025-06-28: European Accessibility Act（EAA）施行
    - 違反時: 最大 €80,000 の罰金
    - 対象: EU 市場向けデジタル製品・サービス

  2026-04: ADA Title II デジタルアクセシビリティ期限
    - 対象: 米国政府機関、公的サービス

  継続: Section 508（米国連邦要件）
  継続: 障害者差別解消法（日本）

コスト比較:
  初期設計時のアクセシビリティ組み込み: 1x
  リリース後のアクセシビリティ修正: 10x
  → 「設計制約」として最初から組み込む方が圧倒的に効率的
```

---

## 8. Palette との連携

```
Palette での活用:
  1. OBSERVE フェーズで AV-01〜08 の自動/手動スクリーニング
  2. WCAG 2.2 新基準のチェックリストを評価に組み込み
  3. IMPLEMENT フェーズでセマンティック HTML 優先ガイドを適用
  4. VERIFY フェーズで axe-core + 手動テストの実施

品質ゲート:
  - <div> + onclick → <button> への変更を要求（AV-01 防止）
  - placeholder のみのフォーム → <label> 追加を要求（AV-02 防止）
  - D&D のみの操作 → キーボード代替を要求（AV-05 防止）
  - タッチターゲット < 24px → サイズ拡大を要求（AV-07 防止）
  - CAPTCHA テキスト入力 → reCAPTCHA v3 or パスキーへ変更
  - スティッキー要素 → scroll-padding 設定を確認（AV-04 防止）

テストワークフロー:
  自動（30-40% の問題を検出）:
    - eslint-plugin-jsx-a11y（開発時）
    - axe DevTools（ブラウザ拡張）
    - jest-axe（テストコード内）

  手動（60-70% の問題を検出）:
    - VoiceOver (macOS: Cmd+F5)
    - NVDA (Windows)
    - キーボードのみナビゲーション
    - ズーム 200% テスト
```

**Source:** [AllAccessible: WCAG 2.2 Complete Guide 2025](https://www.allaccessible.org/blog/wcag-22-complete-guide-2025) · [inhaq: Accessibility for Design Engineers](https://inhaq.com/blog/accessibility-for-design-engineers-building-inclusive-uis) · [Level Access: WCAG 2.2 Checklist](https://www.levelaccess.com/blog/wcag-2-2-aa-summary-and-checklist-for-website-owners/) · [Usercentrics: WCAG 2.2 and Inclusive Design](https://usercentrics.com/knowledge-hub/mastering-web-app-accessibility-wcag2-2-and-inclusive-design/)
