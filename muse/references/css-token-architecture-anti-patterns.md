# CSS Token Architecture Anti-Patterns

> CSS 変数の設計ミス、トークン配置・スコープの落とし穴、詳細度問題、モダン CSS アーキテクチャ

## 1. CSS トークン実装 7 大アンチパターン

| # | アンチパターン | 問題 | 対策 |
|---|-------------|------|------|
| **CT-01** | **過剰ネスト** | `var(--theme)` → `var(--light)` → `var(--colors)` → `var(--primary)` の連鎖 | 参照は最大 2 段階、直接的な値解決を優先 |
| **CT-02** | **Raw 値混在** | コンポーネント内で `#2563eb` と `var(--color-primary)` が混在 | 全スタイルで Semantic トークン使用を徹底 |
| **CT-03** | **グローバル汚染** | 全コンポーネントトークンを `:root` に定義 | グローバルは Primitive/Semantic のみ、Component はスコープ内 |
| **CT-04** | **カテゴリ未整理** | 色・余白・シャドウが無秩序に混在 | カテゴリごとにグループ化 + コメントで区切り |
| **CT-05** | **詳細度戦争** | トークンオーバーライドに `!important` 使用 | Cascade Layers (`@layer`) で詳細度を制御 |
| **CT-06** | **未使用トークン蓄積** | 削除されたコンポーネントのトークンが残存 | 定期的なトークン監査 + 未使用検出ツール |
| **CT-07** | **フォールバック欠如** | `var(--color-primary)` のフォールバックなし | `var(--color-primary, #3b82f6)` でフォールバック提供 |

---

## 2. トークン配置のベストプラクティス

```
✅ 推奨: スコープに応じた配置

  /* グローバルトークン（Primitive + Semantic） */
  :root {
    /* Colors */
    --color-primary: #4f46e5;
    --color-secondary: #f59e0b;
    --color-bg-primary: #ffffff;
    --color-text-primary: #111827;

    /* Spacing */
    --space-2: 0.5rem;
    --space-4: 1rem;
    --space-6: 1.5rem;

    /* Shadows */
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  /* コンポーネントスコープトークン */
  .card {
    --card-padding: var(--space-4);
    --card-radius: var(--radius-lg);
    --card-shadow: var(--shadow-md);

    padding: var(--card-padding);
    border-radius: var(--card-radius);
    box-shadow: var(--card-shadow);
  }

❌ アンチパターン: 全てを :root に定義

  :root {
    --card-padding: 1rem;
    --card-radius: 0.75rem;
    --card-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    --modal-padding: 1.5rem;
    --modal-radius: 1rem;
    --button-height: 2.5rem;
    /* ... 数百のコンポーネントトークンが :root に... */
  }
```

---

## 3. Cascade Layers によるスタイル制御

```
@layer を使った詳細度管理（CSS 2025 ベストプラクティス）:

  @layer tokens, base, components, utilities, overrides;

  @layer tokens {
    :root {
      --color-primary: #4f46e5;
      --space-4: 1rem;
    }
  }

  @layer base {
    body {
      color: var(--color-text-primary);
      background: var(--color-bg-primary);
    }
  }

  @layer components {
    .button {
      padding: var(--space-2) var(--space-4);
      background: var(--color-primary);
    }
  }

  @layer utilities {
    .mt-4 { margin-top: var(--space-4); }
  }

メリット:
  - !important 不要で優先度制御
  - 詳細度の衝突を構造的に解決
  - フレームワークとカスタムスタイルの共存が容易
```

---

## 4. テーマ切替のパターンと落とし穴

```
推奨: data 属性によるテーマ切替

  :root {
    --color-bg: #ffffff;
    --color-text: #111827;
  }

  [data-theme="dark"] {
    --color-bg: #0f172a;
    --color-text: #f1f5f9;
  }

よくある失敗:

  ❌ クラスベースの大量オーバーライド:
    .dark .card { background: #1e1e1e; }
    .dark .card .title { color: #fff; }
    .dark .card .description { color: #ccc; }
    → 全コンポーネント × 全要素のオーバーライドが必要

  ✅ トークンベースのテーマ切替:
    .card {
      background: var(--color-bg-surface);
      color: var(--color-text-primary);
    }
    → テーマ変更はトークン値の変更のみ

  ❌ @media と data 属性の混在:
    問題: prefers-color-scheme と [data-theme] が競合
    対策: 一方を真実の源とし、もう一方はフォールバック

マルチテーマ対応:
  [data-theme="light"] { ... }
  [data-theme="dark"] { ... }
  [data-theme="high-contrast"] { ... }
  → Semantic トークン層があれば追加テーマは容易
```

---

## 5. CSS Custom Properties の高度なパターン

```
@property による型付きカスタムプロパティ（2025 新機能）:

  @property --color-primary {
    syntax: "<color>";
    inherits: true;
    initial-value: #4f46e5;
  }

  メリット:
  - transition/animation でカスタムプロパティをアニメーション可能
  - 型安全: 無効な値の検出
  - initial-value でフォールバック保証

Container Queries とトークンの組み合わせ:

  .card-container {
    container-type: inline-size;
  }

  @container (min-width: 400px) {
    .card {
      --card-padding: var(--space-6);  /* 広いコンテナでは大きめ余白 */
      --card-layout: row;
    }
  }

  @container (max-width: 399px) {
    .card {
      --card-padding: var(--space-3);  /* 狭いコンテナでは小さめ余白 */
      --card-layout: column;
    }
  }
```

---

## 6. フレームワーク別トークン連携の注意点

```
Tailwind v4 + CSS トークン:
  ✅ @theme でトークン定義 → ユーティリティクラス自動生成
  ❌ tailwind.config.js と @theme の二重定義
  → v4 では CSS-first、config ファイルは非推奨

Panda CSS:
  ✅ semanticTokens で dark/light 自動切替
  ❌ 通常の tokens と semanticTokens の混同
  → テーマ依存は semanticTokens、テーマ非依存は tokens

CSS Modules:
  ✅ var(--token) でグローバルトークンを参照
  ❌ :root トークンを .module.css 内で再定義
  → モジュール内はコンポーネントスコープのみ

CSS-in-JS (styled-components / emotion):
  ✅ CSS 変数を theme オブジェクト経由で参照
  ❌ JS 内でハードコード値を使用
  → theme.colors.primary = 'var(--color-primary)' で一元化
```

---

## 7. Muse との連携

```
Muse での活用:
  1. SCAN フェーズで CT-01〜07 のスクリーニング
  2. トークン監査で :root 汚染度を測定
  3. !important 使用箇所の検出と Cascade Layers への移行提案
  4. フレームワーク移行時のトークン互換性チェック

品質ゲート:
  - var() の 3+ 段階ネスト → 参照チェーン簡素化（CT-01 防止）
  - コンポーネント内の HEX/RGB 値 → トークン置換（CT-02 防止）
  - :root のトークン数 > 100 → コンポーネントスコープへ移動（CT-03 防止）
  - !important 使用 → @layer 導入を提案（CT-05 防止）
  - フォールバックなし var() → フォールバック追加（CT-07 防止）
```

**Source:** [FrontendTools: CSS Variables Guide 2025](https://www.frontendtools.tech/blog/css-variables-guide-design-tokens-theming-2025) · [Martin Fowler: Design Token-Based UI Architecture](https://martinfowler.com/articles/design-token-based-ui-architecture.html) · [Feature-Sliced Design: Design Tokens Architecture](https://feature-sliced.design/blog/design-tokens-architecture)
