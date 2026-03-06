# Performance & Testing

> Core Web Vitals、画像最適化、バンドル削減、レンダリング最適化、Testing Trophy、Vitest + Testing Library、E2E パターン

## 1. Core Web Vitals ターゲット

| メトリクス | 目標 | 測定対象 |
|-----------|------|---------|
| **LCP** (Largest Contentful Paint) | < 2.5s | メインコンテンツの表示速度 |
| **INP** (Interaction to Next Paint) | < 200ms | インタラクション応答性 (2024年3月にFIDを置換) |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 視覚的安定性 |

---

## 2. 画像最適化

```tsx
import Image from 'next/image';

// LCP画像: priority で即座にロード（lazy loading は使わない）
<Image src="/hero.jpg" alt="Hero" width={1200} height={600} priority />

// 通常画像: 自動 lazy loading
<Image src="/product.jpg" alt="Product" width={400} height={300} />

// 外部画像
<Image src={user.avatar} alt={user.name} width={48} height={48}
  sizes="48px" quality={75} />
```

| ルール | 理由 |
|--------|------|
| LCP要素に `loading="lazy"` を使わない | LCP が悪化する |
| LCP画像に `fetchpriority="high"` | 優先的にロード |
| `width`/`height` を必ず指定 | CLS 防止 |
| WebP/AVIF 使用 | JPEG比 25-35% 圧縮改善 |
| `sizes` で適切なサイズ配信 | 不要な大画像を防止 |

---

## 3. バンドルサイズ削減

### コード分割

```tsx
import { lazy, Suspense } from 'react';

// ルートベース分割（最も効果的: 初期ロード 40-60% 削減）
const AdminDashboard = lazy(() => import('./AdminDashboard'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/admin" element={<AdminDashboard />} />
      </Routes>
    </Suspense>
  );
}
```

### ChunkLoadError 対応

```tsx
class ChunkErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false };
  static getDerivedStateFromError(error: Error) {
    if (error.name === 'ChunkLoadError') return { hasError: true };
    throw error;
  }
  render() {
    if (this.state.hasError) {
      return <button onClick={() => window.location.reload()}>Reload</button>;
    }
    return this.props.children;
  }
}
```

### バンドル分析チェックリスト

- [ ] `bundle-analyzer` で定期的に構成を確認
- [ ] Tree Shaking が有効 (`sideEffects: false`)
- [ ] 大きなライブラリの部分インポート (`import { debounce } from 'lodash-es'`)
- [ ] `next/dynamic` でクライアント専用コンポーネントを遅延ロード
- [ ] サードパーティスクリプトに `strategy="lazyOnload"` 適用

---

## 4. レンダリング最適化

| 手法 | 効果 | 適用場面 |
|------|------|---------|
| Server Components をデフォルトに | JSバンドルに含まれない | 全てのデータ表示コンポーネント |
| Suspense ストリーミング | 段階的コンテンツ表示 | 遅いデータフェッチ |
| React Compiler (React 19) | 自動メモ化 | 新規コード全般 |
| `@tanstack/react-virtual` | 長リストの仮想化 | 100+アイテムのリスト |

### リソースヒント

```html
<!-- クリティカルリソース -->
<link rel="preload" href="/fonts/inter.woff2" as="font" crossorigin />

<!-- 次のナビゲーション先 -->
<link rel="prefetch" href="/dashboard" />

<!-- DNS 事前解決 -->
<link rel="dns-prefetch" href="https://api.example.com" />
```

---

## 5. パフォーマンスバジェット

| 項目 | 推奨上限 |
|------|---------|
| 総ページ重量 | < 1.5MB |
| JavaScript バンドル | < 300KB |
| Time to Interactive | < 3.5s |
| HTTP リクエスト数 | < 50 |

---

## 6. Testing Trophy

"Write tests. Not too many. Mostly integration." — Kent C. Dodds

| 層 | ツール | 量 | 対象 |
|----|-------|:---:|------|
| **Static Analysis** | ESLint, TypeScript | 常時 | 型エラー、リントルール |
| **Unit Test** | Vitest | 少 | 純粋関数、ビジネスロジック |
| **Component Test** | Vitest + Testing Library | **多** | コンポーネントの振る舞い |
| **Integration Test** | Vitest + Testing Library | **最多** | 複数コンポーネント連携 |
| **Visual Test** | Chromatic / Percy | 中 | 外観のリグレッション |
| **E2E Test** | Playwright | **少** | クリティカルなユーザーフロー |

---

## 7. Vitest セットアップ (Next.js)

```ts
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './vitest.setup.ts',
    css: true,
  },
  resolve: { alias: { '@': './src' } },
});
```

```ts
// vitest.setup.ts
import '@testing-library/jest-dom/vitest';
```

---

## 8. テストパターン

### コンポーネントテスト

```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';

describe('Counter', () => {
  it('increments count on click', () => {
    render(<Counter initialCount={0} />);
    fireEvent.click(screen.getByRole('button', { name: /increment/i }));
    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });

  it('calls onCountChange callback', () => {
    const onChange = vi.fn();
    render(<Counter initialCount={0} onCountChange={onChange} />);
    fireEvent.click(screen.getByRole('button', { name: /increment/i }));
    expect(onChange).toHaveBeenCalledWith(1);
  });
});
```

### Server Actions のテスト

```tsx
import { describe, it, expect } from 'vitest';
import { createTodo } from './actions';

describe('createTodo', () => {
  it('validates input and creates todo', async () => {
    const fd = new FormData();
    fd.set('title', 'Test Todo');
    const result = await createTodo({}, fd);
    expect(result.success).toBe(true);
  });

  it('returns errors for invalid input', async () => {
    const fd = new FormData();
    fd.set('title', '');
    const result = await createTodo({}, fd);
    expect(result.errors).toBeDefined();
  });
});
```

### 非同期 Server Components

**現状:** Vitest は非同期 Server Components を直接サポートしない。

| Component タイプ | テスト方法 |
|-----------------|----------|
| 同期 Server/Client Component | Vitest + Testing Library |
| 非同期 Server Component | **Playwright E2E** |
| Server Actions | Vitest ユニットテスト |

---

## 9. Testing Library クエリ優先順位

```
1. getByRole       ← 最優先（a11y も改善される）
2. getByLabelText  ← フォーム要素
3. getByText       ← 非インタラクティブ要素
4. getByTestId     ← 最終手段のみ
```

**原則:** 実装詳細ではなくユーザーに見える振る舞いをテストする。

---

## 10. E2E テスト (Playwright)

```ts
// e2e/checkout.spec.ts
import { test, expect } from '@playwright/test';

test('complete checkout flow', async ({ page }) => {
  await page.goto('/products');
  await page.click('[data-testid="product-1"] button');
  await expect(page.locator('[data-testid="cart-count"]')).toHaveText('1');

  await page.click('[data-testid="checkout-button"]');
  await page.fill('[name="email"]', 'test@example.com');
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL(/\/order-confirmation/);
});
```

**E2E は収益直結パスのみ:** サインアップ → 購入 → 決済確認

---

## 11. アンチパターン

### パフォーマンス

| # | アンチパターン | 問題 | 修正 |
|---|------------|------|------|
| 1 | LCP要素に `loading="lazy"` | LCP スコア悪化 | `priority` / `fetchpriority="high"` |
| 2 | 画像に width/height 未指定 | CLS 発生 | 明示的にサイズ指定 |
| 3 | 過剰なプリフェッチ | コード分割の利点を相殺 | 重要パスのみ |
| 4 | Lab テストのみ依存 | 実ユーザー環境と乖離 | RUM で計測 |
| 5 | サードパーティスクリプト野放し | CWV の最大脅威 | `lazyOnload` + 影響監視 |
| 6 | モバイル最適化の軽視 | Google はモバイルで CWV 評価 | モバイルファースト |

### テスト

| # | アンチパターン | 問題 | 修正 |
|---|------------|------|------|
| 1 | スナップショットテスト過剰依存 | 意味なし更新が蓄積 | 振る舞いテストに切替 |
| 2 | 実装詳細のテスト (内部state等) | リファクタで壊れる | ユーザー視点のアサーション |
| 3 | E2E テスト過剰 | 遅い、フレーキー | Integration テスト中心に |
| 4 | モック過剰使用 | 本当の統合テストにならない | 必要最小限にモック |
| 5 | `getByTestId` 多用 | a11y 改善機会の喪失 | `getByRole` 優先 |

**Source:** [Frontend Performance 2026](https://vofoxsolutions.com/front-end-performance-in-2026) · [Top CWV Improvements (web.dev)](https://web.dev/articles/top-cwv) · [Frontend Testing Guide (Chromatic)](https://www.chromatic.com/frontend-testing-guide) · [Next.js Vitest Guide](https://nextjs.org/docs/app/guides/testing/vitest)
