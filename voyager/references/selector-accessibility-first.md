# Modern Selector Strategy & Accessibility-First Testing

> セレクタ優先度階層、getByRole ベストプラクティス、ARIA スナップショット、アクセシビリティファーストテスト

## 1. セレクタ優先度階層（2026年推奨）

### Playwright 公式推奨順位

| 優先度 | セレクタ | 根拠 | 例 |
|--------|---------|------|-----|
| **1** | `getByRole()` | ユーザー視点 + a11y 保証 | `getByRole('button', { name: 'Submit' })` |
| **2** | `getByLabel()` | フォーム要素に最適 | `getByLabel('Email')` |
| **3** | `getByPlaceholder()` | ラベルなしフォーム | `getByPlaceholder('Search...')` |
| **4** | `getByText()` | 可視テキストベース | `getByText('Welcome back')` |
| **5** | `getByTestId()` | 意図的なエスケープハッチ | `getByTestId('checkout-form')` |
| **6** | CSS / XPath | **最終手段のみ** | `page.locator('.btn')` |

### セレクタ選択フローチャート

```
Q: 要素にアクセシブルなロールがあるか?
  → Yes → getByRole() を使用
  → No ↓
Q: フォーム要素にラベルがあるか?
  → Yes → getByLabel() を使用
  → No ↓
Q: プレースホルダーテキストがあるか?
  → Yes → getByPlaceholder() を使用
  → No ↓
Q: ユニークな可視テキストがあるか?
  → Yes → getByText() を使用
  → No ↓
Q: data-testid を追加できるか?
  → Yes → getByTestId() を使用（推奨）
  → No → CSS/XPath（最終手段、要コメント）
```

---

## 2. getByRole() ベストプラクティス

### 基本パターン

```typescript
// ボタン
await page.getByRole('button', { name: 'Save changes' }).click();

// リンク
await page.getByRole('link', { name: 'Sign up' }).click();

// テキストボックス
await page.getByRole('textbox', { name: 'Email' }).fill('user@example.com');

// チェックボックス
await page.getByRole('checkbox', { name: 'Agree to terms' }).check();

// 見出し
await expect(page.getByRole('heading', { level: 1 })).toHaveText('Dashboard');

// ナビゲーション
await page.getByRole('navigation').getByRole('link', { name: 'Home' }).click();
```

### 高度なフィルタリング

```typescript
// 状態フィルタ
await page.getByRole('checkbox', { name: 'Newsletter', checked: true });
await page.getByRole('tab', { name: 'Settings', selected: true });
await page.getByRole('treeitem', { expanded: true });

// スコープの絞り込み
const dialog = page.getByRole('dialog');
await dialog.getByRole('button', { name: 'Confirm' }).click();

// 隠し要素の操作（通常は避ける）
await page.getByRole('button', { name: 'Menu', includeHidden: true });
```

### getByRole() の限界と対策

| 限界 | 症状 | 対策 |
|------|------|------|
| **同名同ロール** | 複数ボタンが同じ name | スコープ絞り込み or `getByTestId` |
| **動的コンテンツ** | ロール/名前が頻繁に変化 | `getByTestId` をフォールバック |
| **Shadow DOM** | アクセシビリティツリーに現れない | `locator()` + pierce or `getByTestId` |
| **カスタムコンポーネント** | ARIA ロールが未設定 | コンポーネント側で ARIA を追加 |
| **複雑な表/グリッド** | セル特定が困難 | `getByRole('cell')` + フィルタ |

---

## 3. ARIA スナップショットテスト

### 概念

アクセシビリティツリーのスナップショットを保存し、変更を検出するテスト手法。DOM 構造ではなく**セマンティクス**をテスト。

### 実装パターン

```typescript
// ARIA スナップショットの生成とアサーション
await expect(page.getByRole('navigation')).toMatchAriaSnapshot(`
  - navigation:
    - link "Home"
    - link "Products"
    - link "About"
    - link "Contact"
`);

// 部分マッチ（属性やアクセシブル名を省略可能）
await expect(page.getByRole('form')).toMatchAriaSnapshot(`
  - form:
    - textbox
    - textbox
    - button "Submit"
`);
```

### ARIA スナップショット vs DOM スナップショット

| 観点 | ARIA スナップショット | DOM スナップショット |
|------|-------------------|-------------------|
| **安定性** | 高（セマンティクスベース） | 低（構造変更で壊れる） |
| **可読性** | 高（人間が理解しやすい） | 低（HTML ノイズ多い） |
| **a11y 保証** | 同時にアクセシビリティも検証 | a11y 検証なし |
| **適用範囲** | ナビゲーション、フォーム、ダイアログ | 詳細な HTML 構造の検証 |

---

## 4. アクセシビリティファーストテスト

### 原則

```
テストをアクセシビリティファーストで書く
  = ユーザーがスクリーンリーダーで操作する方法でテストする
  = テストが壊れる ≈ アクセシビリティが壊れた（早期検出）
```

### 実践パターン

```typescript
// ❌ 実装ベース
await page.locator('#submit-btn').click();
await page.locator('.error-msg').isVisible();

// ✅ アクセシビリティファースト
await page.getByRole('button', { name: 'Submit order' }).click();
await expect(page.getByRole('alert')).toContainText('Invalid email');
```

### フォームテストのアクセシビリティファーストパターン

```typescript
test('should submit registration form', async ({ page }) => {
  // ラベルでフォーム要素を操作
  await page.getByLabel('Full name').fill('John Doe');
  await page.getByLabel('Email address').fill('john@example.com');
  await page.getByLabel('Password').fill('SecurePass123');

  // チェックボックスをロールで操作
  await page.getByRole('checkbox', { name: 'I agree to terms' }).check();

  // ボタンをロールで操作
  await page.getByRole('button', { name: 'Create account' }).click();

  // 成功メッセージをロールで検証
  await expect(page.getByRole('status')).toContainText('Account created');
});
```

### ARIA ロール一覧（テストでよく使うもの）

| ロール | HTML 要素 | 用途 |
|--------|----------|------|
| `button` | `<button>`, `<input type="submit">` | クリック操作 |
| `link` | `<a href>` | ナビゲーション |
| `textbox` | `<input type="text">`, `<textarea>` | テキスト入力 |
| `checkbox` | `<input type="checkbox">` | トグル |
| `heading` | `<h1>`-`<h6>` | ページ構造 |
| `navigation` | `<nav>` | ナビゲーション領域 |
| `dialog` | `<dialog>` | モーダル |
| `alert` | `role="alert"` | エラー/成功メッセージ |
| `status` | `role="status"` | ステータス更新 |
| `form` | `<form>` | フォーム領域 |
| `list` / `listitem` | `<ul>/<li>` | リスト |
| `table` / `row` / `cell` | `<table>/<tr>/<td>` | テーブル |

---

## 5. 自動 a11y テストとの統合

### axe-core + アクセシビリティファーストの組み合わせ

```typescript
import AxeBuilder from '@axe-core/playwright';

test('checkout page is accessible', async ({ page }) => {
  await page.goto('/checkout');

  // 1. アクセシビリティファーストなインタラクション
  await page.getByLabel('Card number').fill('4111111111111111');
  await page.getByRole('button', { name: 'Pay now' }).click();

  // 2. axe-core で自動 a11y チェック
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .analyze();

  expect(results.violations).toEqual([]);
});
```

### テストで検出できる a11y 問題

| 問題 | 検出方法 |
|------|---------|
| ラベルなしフォーム | `getByLabel()` が失敗 → a11y 問題 |
| ロールなしボタン | `getByRole('button')` が失敗 → a11y 問題 |
| キーボード操作不可 | `Tab` + `Enter` でテスト |
| コントラスト不足 | axe-core の自動チェック |
| 重複 ID | axe-core の自動チェック |

**Source:** [Playwright: Locators](https://playwright.dev/docs/locators) · [Playwright: Accessibility Testing](https://playwright.dev/docs/accessibility-testing) · [Playwright: ARIA Snapshots](https://playwright.dev/docs/aria-snapshots) · [Components.Guide: Accessibility-First Playwright](https://components.guide/accessibility-first/playwright) · [Cam McHenry: Accessible Playwright Tests](https://camchenry.com/blog/how-i-write-accessible-playwright-tests) · [Momentic: Limits of getByRole](https://momentic.ai/resources/the-limits-of-playwright-getbyrole-when-semantic-locators-arent-enough)
