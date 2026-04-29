# Mobile Native Testing

Purpose: Use this file for **concrete WebdriverIO + Appium configuration patterns**, real-device session capabilities, Playwright mobile-emulation alternatives, and mobile-specific test recipes (rotation, push notification, airplane mode).

Contents:
- Agent boundary and emulation-vs-native decision rules
- Playwright mobile emulation patterns
- WebdriverIO/Appium configuration and real-device execution (BrowserStack / Sauce Labs)
- Mobile-specific test patterns (orientation, push, network condition)

## Cross-Reference

| You need | Read |
|----------|------|
| Framework selection across Detox / Maestro / Appium / XCUITest / Espresso, mobile Page Object design, two-axis flake taxonomy (logic vs device), device-farm tier matrix (PR / nightly / release gate) | `mobile-e2e-testing.md` (start there for shipped-app E2E) |
| Cloud session control (tunnels, parallel session caps, credential management, cost-tier strategy) and provider integration tables | `cloud-testing.md` |
| Concrete WebdriverIO/Appium config snippets, Playwright mobile emulation, mobile-specific test recipes | this file |

> When the artifact is a shipping `.ipa`/`.apk`/`.aab` (or RN bundle), start at `mobile-e2e-testing.md` — it routes you back here once framework selection lands on Appium.

---

## Agent Boundary

| Responsibility | Voyager | Navigator | Artisan |
|----------------|---------|-----------|---------|
| **Mobile E2E tests** | ✅ Primary | | |
| **Mobile browser tasks** | | ✅ Primary | |
| **Mobile UI components** | | | ✅ Primary |

**Rule of thumb**: Voyager owns mobile E2E test design and execution. Navigator handles one-off mobile browser tasks. Artisan implements responsive mobile components.

---

## Playwright Mobile Emulation

### Capabilities & Limits

| Feature | Playwright Emulation | Real Device |
|---------|---------------------|-------------|
| **Viewport / user-agent** | ✅ Accurate | ✅ Native |
| **Touch events** | ✅ Simulated | ✅ Native |
| **Device rotation** | ⚠️ Viewport resize only | ✅ Accelerometer |
| **Push notifications** | ❌ Not supported | ✅ Native |
| **Camera / GPS** | ⚠️ Permission grants only | ✅ Native |
| **App install / deep links** | ❌ Browser only | ✅ Native |
| **Performance (real)** | ❌ Desktop CPU/GPU | ✅ Device constraints |
| **Gestures (swipe/pinch)** | ⚠️ Basic via touchscreen | ✅ Native |

**Decision**: Use Playwright emulation for responsive layout + basic mobile UX. Use real devices (Appium) for native features + real performance testing.

### Playwright Device Emulation

```typescript
// playwright.config.ts
import { devices } from '@playwright/test';

export default defineConfig({
  projects: [
    { name: 'mobile-chrome', use: { ...devices['Pixel 7'] } },
    { name: 'mobile-safari', use: { ...devices['iPhone 14'] } },
    { name: 'tablet', use: { ...devices['iPad Pro 11'] } },
  ],
});
```

### Touch & Gesture Simulation

```typescript
test('swipe to delete item', async ({ page }) => {
  await page.goto('/todo');

  const item = page.getByTestId('todo-item-1');
  const box = await item.boundingBox();

  // Simulate swipe left
  await page.touchscreen.tap(box!.x + box!.width - 10, box!.y + box!.height / 2);
  await page.mouse.move(box!.x + box!.width - 10, box!.y + box!.height / 2);
  await page.mouse.down();
  await page.mouse.move(box!.x + 10, box!.y + box!.height / 2, { steps: 10 });
  await page.mouse.up();

  await expect(page.getByTestId('delete-confirm')).toBeVisible();
});

test('pinch to zoom on map', async ({ page }) => {
  await page.goto('/map');

  // Dispatch touch events for pinch gesture
  await page.evaluate(() => {
    const map = document.querySelector('[data-testid="map-container"]')!;
    const rect = map.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;

    const touch1 = new Touch({ identifier: 0, target: map, clientX: cx - 50, clientY: cy });
    const touch2 = new Touch({ identifier: 1, target: map, clientX: cx + 50, clientY: cy });
    map.dispatchEvent(new TouchEvent('touchstart', { touches: [touch1, touch2] }));

    const touch1End = new Touch({ identifier: 0, target: map, clientX: cx - 100, clientY: cy });
    const touch2End = new Touch({ identifier: 1, target: map, clientX: cx + 100, clientY: cy });
    map.dispatchEvent(new TouchEvent('touchmove', { touches: [touch1End, touch2End] }));
    map.dispatchEvent(new TouchEvent('touchend', { touches: [] }));
  });
});
```

---

## WebdriverIO + Appium (Native Apps)

### Setup

```bash
# Install dependencies
npm install -D webdriverio @wdio/cli @wdio/appium-service @wdio/mocha-framework

# Install Appium
npm install -g appium
appium driver install uiautomator2  # Android
appium driver install xcuitest       # iOS
```

### Configuration

```typescript
// wdio.conf.ts
export const config: WebdriverIO.Config = {
  runner: 'local',
  specs: ['./e2e/mobile/**/*.spec.ts'],
  capabilities: [{
    platformName: 'Android',
    'appium:deviceName': 'Pixel 7',
    'appium:platformVersion': '14',
    'appium:automationName': 'UiAutomator2',
    'appium:app': './app/build/outputs/apk/debug/app-debug.apk',
  }],
  services: ['appium'],
  framework: 'mocha',
};
```

### Native App Test Example

```typescript
describe('Login Flow (Native)', () => {
  it('should login with valid credentials', async () => {
    const emailInput = await $('~email-input');  // accessibility id
    await emailInput.setValue('test@example.com');

    const passwordInput = await $('~password-input');
    await passwordInput.setValue('Test1234!');

    const loginButton = await $('~login-button');
    await loginButton.click();

    const dashboard = await $('~dashboard-screen');
    await expect(dashboard).toBeDisplayed();
  });
});
```

---

## Real Device Testing (Cloud)

### BrowserStack App Automate

```typescript
// wdio.conf.browserstack.ts
export const config: WebdriverIO.Config = {
  user: process.env.BROWSERSTACK_USERNAME,
  key: process.env.BROWSERSTACK_ACCESS_KEY,
  hostname: 'hub.browserstack.com',
  capabilities: [{
    platformName: 'Android',
    'appium:deviceName': 'Google Pixel 7',
    'appium:platformVersion': '14.0',
    'appium:app': process.env.BROWSERSTACK_APP_URL,
    'bstack:options': {
      projectName: 'Mobile E2E',
      buildName: process.env.GITHUB_SHA || 'local',
      sessionName: 'Login Flow',
    },
  }],
};
```

### Sauce Labs Real Devices

```typescript
// wdio.conf.saucelabs.ts
export const config: WebdriverIO.Config = {
  user: process.env.SAUCE_USERNAME,
  key: process.env.SAUCE_ACCESS_KEY,
  hostname: 'ondemand.us-west-1.saucelabs.com',
  capabilities: [{
    platformName: 'iOS',
    'appium:deviceName': 'iPhone 15',
    'appium:platformVersion': '17',
    'appium:app': 'storage:filename=app.ipa',
    'sauce:options': {
      appiumVersion: '2.0',
      name: 'iOS E2E Tests',
    },
  }],
};
```

---

## Mobile-Specific Patterns

### Device Rotation

```typescript
it('handles orientation change', async () => {
  await driver.setOrientation('PORTRAIT');
  const portraitNav = await $('~mobile-nav');
  await expect(portraitNav).toBeDisplayed();

  await driver.setOrientation('LANDSCAPE');
  const landscapeNav = await $('~desktop-nav');
  await expect(landscapeNav).toBeDisplayed();
});
```

### Push Notification Testing

```typescript
it('receives push notification', async () => {
  // Trigger notification via API
  await fetch(`${API_URL}/test/send-push`, {
    method: 'POST',
    body: JSON.stringify({ userId: 'test-user', message: 'New order received' }),
  });

  // Wait for notification (Android)
  await driver.openNotifications();
  const notification = await $('android=new UiSelector().textContains("New order")');
  await expect(notification).toBeDisplayed();

  await notification.click();

  const orderScreen = await $('~order-detail-screen');
  await expect(orderScreen).toBeDisplayed();
});
```

### Network Condition Testing (Mobile)

```typescript
it('handles offline mode gracefully', async () => {
  await driver.toggleAirplaneMode();

  const offlineMsg = await $('~offline-message');
  await expect(offlineMsg).toBeDisplayed();

  await driver.toggleAirplaneMode();

  const syncComplete = await $('~sync-complete');
  await expect(syncComplete).toBeDisplayed();
});
```

---

## CI Configuration for Mobile

### GitHub Actions + Appium

```yaml
# .github/workflows/mobile-e2e.yml
name: Mobile E2E Tests

on:
  push:
    branches: [main]

jobs:
  android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci

      - name: Start Android Emulator
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 34
          target: google_apis
          arch: x86_64
          script: npx wdio run wdio.conf.ts

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: mobile-e2e-report
          path: allure-results/

  ios-cloud:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - name: Run iOS tests on BrowserStack
        run: npx wdio run wdio.conf.browserstack.ts
        env:
          BROWSERSTACK_USERNAME: ${{ secrets.BROWSERSTACK_USERNAME }}
          BROWSERSTACK_ACCESS_KEY: ${{ secrets.BROWSERSTACK_ACCESS_KEY }}
          BROWSERSTACK_APP_URL: ${{ secrets.BROWSERSTACK_APP_URL }}
```

---

## 2025-2026 Spec Update

### Appium 3.x capability handling (released 2025-08-07)

Appium 3.x makes the `appium:` capability prefix mandatory and drops JSONWP entirely (W3C-only). Existing 2.x configs will fail at session creation if non-standard caps are not prefixed. Decoupled drivers/plugins mean the CI runner only installs what is needed; Inspector can now be hosted in-process via `appium plugin install inspector`. Sensitive headers are masked with `X-Appium-Is-Sensitive`. Source: <https://appium.io/docs/en/3.1/blog/2025/08/07/-appium-3/> · <https://appium.io/docs/en/3.1/guides/migrating-2-to-3/>

```typescript
// Appium 3.x: every non-W3C cap MUST carry the appium: prefix
capabilities: [{
  // W3C standard caps (no prefix)
  platformName: 'Android',
  // Appium-specific (prefix mandatory)
  'appium:deviceName': 'Pixel 7',
  'appium:platformVersion': '14',
  'appium:automationName': 'UiAutomator2',
  'appium:app': './app/build/outputs/apk/debug/app-debug.apk',
}]
```

CI prerequisites for Appium 3.x: Node.js >= 20.19.0, npm >= 10. Install only the drivers and plugins you need:

```bash
appium driver install uiautomator2
appium driver install xcuitest
appium plugin install images          # only if used
appium --use-drivers=uiautomator2,xcuitest --use-plugins=images
```

### Swift Testing (Xcode 26 / Swift 6.2) vs XCUITest

Swift Testing (`@Test`, `#expect`, parameterized arguments, exit tests, ranged confirmations, scoping traits) is the modern unit-test framework for new code. **It does not yet have a UI automation story** — XCUITest is still the only native iOS UI driver as of 2026-04, and XCTest remains fully supported for legacy and UI tests. Mix Swift Testing for logic tests with XCUITest for UI flows in the same target. Source: <https://developer.apple.com/xcode/swift-testing/> · <https://forums.swift.org/t/whats-new-in-testing-swift-6-2-xcode-26/80688>

### Compose UI Test ↔ Espresso interop & Robolectric 4.16

Espresso reaches Compose nodes through the Compose semantics tree by enabling `testTagsAsResourceId = true` on a composable subtree (Compose 1.2.0-alpha08+). For JVM tests targeting Android 16 / SDK 36 (Baklava), upgrade to **Robolectric 4.16** (released 2025-Q3) on **JDK 21**; older 4.14/4.15 do not support Baklava. Robolectric 4.16 introduces `ResourcesMode.NATIVE` (SDK 36 only). Source: <https://github.com/robolectric/robolectric/releases/tag/robolectric-4.16> · <https://developer.android.com/develop/ui/compose/testing/interoperability>

```kotlin
// Compose composable: opt the subtree into resource-id semantics for Espresso
Box(
  Modifier.semantics { testTagsAsResourceId = true }.testTag("checkout-submit")
) { /* ... */ }
```

### Foldable / window-size-class testing patterns

```kotlin
// Drive layout under each WindowSizeClass breakpoint and verify the right pane appears.
@RunWith(AndroidJUnit4::class)
class AdaptiveLayoutTest {
  @Test fun showsListDetailOnExpanded() {
    composeTestRule.setContent {
      val widthSize = WindowWidthSizeClass.Expanded
      // ...assert dual-pane visible
    }
  }
}
```

For real-device fold/unfold posture coverage, target Galaxy Z Fold (incl. expected wide-form Z Fold 8 in 2026-07), Pixel 10 Pro Fold (IP68), and large-screen iPad Pro with Stage Manager. Add at least one fold ↔ unfold posture transition test to the release-gate tier — state-loss bugs across hinge events are foldable-specific. Source: <https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes> · <https://9to5google.com/2026/04/26/samsung-galaxy-z-fold-8-wide-leak/>

### WebDriver BiDi for mobile (status as of 2026-04)

WebDriver BiDi remains a W3C **Editor's Draft** — a living standard with continuous additions. Appium 3.2 docs include a BiDi reference, and Selenium 4 / WebdriverIO surface BiDi via the `webSocketUrl` session field. A formal **mobile profile** has not been ratified as of 2026-04. Treat BiDi-on-mobile as exploratory; keep production gates on classic WebDriver until a stable mobile profile lands. Source: <https://w3c.github.io/webdriver-bidi/> · <https://appium.io/docs/en/3.2/reference/api/bidi/>

### Privacy Manifest awareness in tests

Apple enforces Privacy Manifest declarations for new submissions since 2024-05-01, and for new privacy-impacting third-party SDKs since 2025-02-12. Required-reason API categories include disk space, active keyboard, user defaults, file timestamp, and system boot time. Test scaffolding (XCUITest helpers, mock SDKs, Appium helper apps) must declare `PrivacyInfo.xcprivacy` independently — App Store Connect aggregates app + SDK manifests. Add a CI step that diffs the merged manifest before TestFlight. Source: <https://developer.apple.com/documentation/bundleresources/privacy-manifest-files> · <https://developer.apple.com/news/?id=3d8a9yyh>
