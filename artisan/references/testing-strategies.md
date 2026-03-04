# Frontend Testing Strategies

> Testing Trophy、Vitest + Testing Library、Server Components テスト、E2E パターン

## 1. Testing Trophy

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

## 2. Vitest セットアップ (Next.js)

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

## 3. テストパターン

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

## 4. Testing Library クエリ優先順位

```
1. getByRole       ← 最優先（a11y も改善される）
2. getByLabelText  ← フォーム要素
3. getByText       ← 非インタラクティブ要素
4. getByTestId     ← 最終手段のみ
```

**原則:** 実装詳細ではなくユーザーに見える振る舞いをテストする。

---

## 5. E2E テスト (Playwright)

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

## 6. アンチパターン

| # | アンチパターン | 問題 | 修正 |
|---|------------|------|------|
| 1 | スナップショットテスト過剰依存 | 意味なし更新が蓄積 | 振る舞いテストに切替 |
| 2 | 実装詳細のテスト (内部state等) | リファクタで壊れる | ユーザー視点のアサーション |
| 3 | E2E テスト過剰 | 遅い、フレーキー | Integration テスト中心に |
| 4 | モック過剰使用 | 本当の統合テストにならない | 必要最小限にモック |
| 5 | `getByTestId` 多用 | a11y 改善機会の喪失 | `getByRole` 優先 |

**Source:** [Frontend Testing Guide (Chromatic)](https://www.chromatic.com/frontend-testing-guide) · [Next.js Vitest Guide](https://nextjs.org/docs/app/guides/testing/vitest) · [Testing async RSC](https://howtotestfrontend.com/resources/testing-async-react-rsc-components) · [Vitest Component Testing](https://vitest.dev/guide/browser/component-testing)
