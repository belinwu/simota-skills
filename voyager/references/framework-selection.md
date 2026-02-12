# Framework Selection Guide

## Framework Comparison

| Criteria | Playwright | Cypress | WebdriverIO | TestCafe |
|----------|------------|---------|-------------|----------|
| **Best for** | Cross-browser, complex flows | DX, component testing | Selenium compat, mobile | Zero-dependency |
| **Browser support** | All + mobile emulation | Chrome, Firefox, Edge | All + real mobile (Appium) | All |
| **Parallel** | Free, built-in | Paid (Cypress Cloud) | Free, built-in | Free, built-in |
| **Multi-tab/iframe** | Full support | Limited | Full support | Limited |
| **Network stubbing** | `page.route` | `cy.intercept` (excellent) | `mock` | `RequestMock` |
| **Architecture** | Out-of-process | In-browser, same-origin | WebDriver protocol | Proxy-based |
| **Learning curve** | Moderate | Low | Moderate | Low |
| **Component testing** | Experimental | Mature | Experimental | None |

## Decision Guide

```
Need cross-browser + mobile emulation? → Playwright
Need real mobile device testing (Appium)? → WebdriverIO
Team already uses Cypress? → Cypress
Need zero-dependency simplicity? → TestCafe
Starting fresh? → Playwright (recommended default)
```

See `playwright-patterns.md` for Playwright details.
See `cypress-guide.md` for Cypress details.

---

## Advanced Scenario Support

| Feature | Playwright | Cypress | WebdriverIO |
|---------|------------|---------|-------------|
| Multi-tab | ✅ Full | ❌ Limited | ✅ Full |
| WebSocket | ✅ Native | ⚠️ Plugin | ✅ Native |
| File download | ✅ Native | ⚠️ Workaround | ✅ Native |
| Offline mode | ✅ Native | ⚠️ Plugin | ⚠️ Limited |
| Performance | ✅ CDP | ❌ N/A | ⚠️ Limited |
| Shadow DOM | ✅ Native | ✅ Native | ⚠️ Plugin |
| iframes | ✅ Full | ⚠️ Same-origin | ✅ Full |

---

## Playwright 1.49+ Modern Features

| Feature | API | Use Case |
|---------|-----|----------|
| **Clock API** | `page.clock.install()` / `.fastForward()` / `.setFixedTime()` | Fake timers, animation control, date-dependent UI |
| **Soft Assertions** | `expect.configure({ soft: true })` | Collect all failures in one test run |
| **Viewport Assertions** | `expect(el).toBeInViewport()` | Lazy loading, infinite scroll verification |
| **API Testing** | `request.get()` / `request.post()` in test | Mix UI + API tests, setup via API |
| **Component Testing** | `@playwright/experimental-ct-react` | React/Vue/Svelte component tests in real browser |

See `playwright-patterns.md` → "Playwright 1.49+ Modern Features" for code examples.

---

## Quick Reference

### Playwright Config Essentials

```typescript
export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 4 : undefined,
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'on-first-retry',
  },
});
```

### Wait Strategy

| Need | Method |
|------|--------|
| Element visible | `await expect(locator).toBeVisible()` |
| Text content | `await expect(locator).toContainText('...')` |
| URL change | `await page.waitForURL('**/path')` |
| Network idle | `await page.waitForLoadState('networkidle')` |
| API response | `await page.waitForResponse(resp => ...)` |
| Element enabled | `await expect(locator).toBeEnabled()` |
| In viewport | `await expect(locator).toBeInViewport()` |
| ❌ Avoid | `await page.waitForTimeout(N)` |

### Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| **LCP** | ≤ 2.5s | web-vitals + `page.evaluate()` |
| **CLS** | ≤ 0.1 | web-vitals + `page.evaluate()` |
| **INP** | ≤ 200ms | web-vitals + `page.evaluate()` |
| **TTFB** | ≤ 800ms | Navigation Timing API |
| **Bundle Size** | Per budget | `page.on('response')` |

### Page Object Template

```typescript
export class ExamplePage extends BasePage {
  readonly element: Locator;

  constructor(page: Page) {
    super(page);
    this.element = this.getByTestId('element-id');
  }

  async goto() { await super.goto('/path'); }
  async doAction() { await this.element.click(); }
  async expectResult() { await expect(this.element).toBeVisible(); }
}
```

See `playwright-patterns.md` for full Page Object patterns.
