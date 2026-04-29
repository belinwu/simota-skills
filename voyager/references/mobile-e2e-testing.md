# Mobile E2E Testing Reference

Purpose: Build an E2E test harness around a **shipped mobile application** (an app the team is releasing to users). Validate critical journeys on real or emulated devices, in a CI-scalable way, with device-farm execution for matrix coverage. **Start here for native mobile E2E.**

## Cross-Reference

| You need | Read |
|----------|------|
| Concrete WebdriverIO + Appium config snippets, real-device session capabilities, Playwright mobile emulation, mobile-specific test patterns (rotation, push, airplane mode) | `mobile-native-testing.md` |
| Cloud session control (tunnels, parallel session caps, credential management, cost-tier strategy), provider integration tables for App Automate / Real Device Cloud / AWS Device Farm / Firebase Test Lab | `cloud-testing.md` |

## Scope Boundary

- **Voyager `mobile`**: E2E harness around a production-bound mobile app. Owns test design, Page Object for mobile, device matrix, device-farm integration.
- **Forge `mobile`**: throwaway mobile PoC (Expo / RN / Flutter), native capabilities stubbed, ≤4h time-box. Not released, not tested at matrix scale.
- **Native**: builds and ships the mobile app — navigation architecture, offline strategy, store review. Owns the app under test.
- **Voyager `playwright`**: mobile-browser emulation of a web app. If the product is a PWA, that recipe is the right tool. `mobile` is for native / React Native binaries.

If the artifact is an `.ipa` / `.apk` / `.aab` being shipped, → `mobile`. If it is Chromium mobile-viewport tests, → `playwright` with emulation.

## Framework Selection

| Framework | Pick when | Skip when |
|-----------|-----------|-----------|
| **Detox** | React Native app, fastest feedback (grey-box, syncs with RN bridge), deterministic | Non-RN native app; true black-box required |
| **Maestro** | Cross-platform YAML DSL, lowest authoring cost, excellent for smoke flows, CI-simple | Deep programmatic logic, complex fixtures |
| **Appium** | Cross-platform native + hybrid, widest device matrix, WebDriver-compatible | Team wants minimal YAML DSL; speed over breadth |
| **XCUITest / Espresso** | Platform-native only (iOS-only or Android-only product); tight integration with native build pipeline | Cross-platform suite, shared test authoring |

Default matrix strategy: **Detox for RN smoke** + **Maestro for cross-platform critical paths** + **Appium on device farm** for the release-gate matrix.

## Workflow

```
PLAN       → list critical journeys (login, purchase, onboarding, push-notif handling)
           → pick frameworks per journey (smoke vs matrix vs platform-specific)
           → decide device matrix tier (local sim/emu → device farm → real-device release gate)
           → define real-device flake budget (quarantine bucket separate from logic flake)

AUTOMATE   → Page Object per screen (mobile POM — design around user intent, not view hierarchy)
           → use accessibility IDs (iOS accessibilityIdentifier, Android contentDescription)
           → never use text-based locators for localized strings unless the test is locale-specific
           → stub network at the app boundary (mock server / MSW native / WireMock)

STABILIZE  → retry only transient device noise (ADB disconnect, sim crash); never retry logic failures
           → separate device-specific quarantine from logic quarantine
           → collect video + device logs on failure; wire to CI artifacts

SCALE      → route matrix runs to BrowserStack / Sauce Labs / AWS Device Farm
           → shard by device, not by test
           → release-gate tier = real devices on 3+ OS versions; PR tier = 1 sim + 1 emu
```

## Device Farm Integration

| Farm | Strength | Watch for |
|------|----------|-----------|
| **BrowserStack App Automate** | Broadest real-device matrix, Appium + Detox + XCUITest, parallel sessions | Per-minute cost scales fast; prune matrix before enabling |
| **Sauce Labs Real Device Cloud** | Strong Appium support, enterprise SSO, detailed logs | iOS pool capacity fluctuates at release time |
| **AWS Device Farm** | Pay-per-minute, integrates with CodeBuild/CodePipeline | Slower session acquisition than BS/SL |
| **Firebase Test Lab** | Android-only, cheap, Robo-crawler included | No iOS — pair with BS/SL for full coverage |

Rule of thumb: local simulators/emulators for the dev loop; one farm for the PR-blocking smoke; a second farm / real-device lab for release gate. Never run the PR gate on real devices — flake budget and cost both explode.

## Locator Strategy

Mobile has no DOM. Use accessibility trees:

```ts
// Detox (React Native)
await element(by.id('login-submit')).tap();  // testID prop on the component

// Appium (cross-platform)
await driver.$('~login-submit').click();     // ~ prefix = accessibility id

// Maestro (YAML)
- tapOn:
    id: "login-submit"
```

Priority: `accessibilityIdentifier` / `testID` > accessibility label > text. Text locators break on localization and A/B copy tests.

## Flake Management

Mobile E2E has **two independent flake sources**:

1. **Logic flake**: race conditions, missing waits, state bleed. Same remediation as web E2E — replace sleeps with condition-based waits.
2. **Device flake**: simulator crashes, ADB disconnects, farm session timeout, network flap. Quarantine separately; retry budget applies only here.

Do not mix the two. A logic flake hidden in a device-flake retry policy ships a bug to production. Tag quarantined tests with `@flaky-device` vs `@flaky-logic`.

## Anti-Patterns

- Running the full device matrix on every PR — 45+ min wait, cost explosion, noise. Keep PR gate on 2 devices, push matrix to nightly + release.
- Text-based locators on localized screens — translation changes break the suite.
- Real push notifications in tests — permission dialog races, APNs/FCM deliverability noise. Stub the push payload at the app boundary.
- Testing with the production backend — rate limits, real charges, real user data. Always route to a staging or mock API.
- One giant `beforeAll` that logs in via UI — slow, flaky, and couples every test to the login screen. Use `storageState` equivalents (Detox: launch-args with auth token; Appium: pre-set keychain/SharedPrefs).
- Skipping biometric / camera / permission tests "because they are hard" — at least stub them; route real-hardware validation to Native.

## CI Shape

- PR tier: 1 iOS sim + 1 Android emu, smoke tag only, < 10 min.
- Nightly tier: 3-5 device classes on a farm, regression + smoke.
- Release gate: real devices on the oldest and newest supported OS versions per platform.
- Never block a PR on the full matrix — cost and flake budget both collapse.

## Handoff

- To **Native**: a failure that reproduces as a bug in the app (not the test).
- To **Voyager `playwright`**: PWA or responsive web in a mobile viewport.
- To **Siege**: load / background-kill / low-memory verification.
- To **Probe**: mobile DAST (reverse-engineering protection, cert pinning bypass checks).

---

## 2025-2026 Trend Update (as of 2026-04)

### Framework lifecycle status

| Framework | Status | Source |
|-----------|--------|--------|
| **Appium 3.x** | GA since **2025-08-07**. JSONWP fully removed (W3C-only). `appium:` capability prefix is mandatory. Driver/plugin decoupling is now the default; install only what you need (`--use-drivers`, `--use-plugins`). Node 20.19+ / npm 10+. Express 5 internally. New `X-Appium-Is-Sensitive` HTTP header masks secrets in logs. Inspector hostable in-process (`appium plugin install inspector`). Migration impact is smaller than 2.x; treat 3.x as a cleanup release. Source: <https://appium.io/docs/en/3.1/blog/2025/08/07/-appium-3/> · <https://appium.io/docs/en/3.1/guides/migrating-2-to-3/> | Official |
| **Detox** | New Architecture officially supported on **RN 0.77.x – 0.84.x** (covers RN 0.79+). Practical friction reported on RN 0.81+ in some CI setups — pin Detox to a tested combo before upgrading. Source: <https://github.com/wix/Detox/issues/4799> · <https://github.com/wix/Detox/issues/4832> | GitHub Issues |
| **Maestro** | Maestro Studio (visual flow recorder), **Maestro Cloud** (binary upload + scheduled runs + PR-trigger), and **MaestroGPT** / AI test analysis (LLM-powered failure summaries beyond pass/fail) shipped through 2025. Lowest authoring cost remains the differentiator. Source: <https://docs.maestro.dev/maestro-flows/workspace-management/ai-test-analysis> · <https://docs.maestro.dev/maestro-studio/run-cloud-tests-from-maestro-studio> | Official |
| **XCUITest / Swift Testing** | Xcode 26 / Swift 6.2 introduced Swift Testing macros (`@Test`, `#expect`, parameterized arguments, exit tests, ranged confirmations, test scoping traits). Swift Testing has **no UI automation story yet** — XCUITest remains the only native UI driver as of 2026-04. XCTest stays fully supported for legacy + UI suites. Source: <https://developer.apple.com/xcode/swift-testing/> · <https://forums.swift.org/t/whats-new-in-testing-swift-6-2-xcode-26/80688> | Official |
| **Espresso + Compose UI Test** | `Modifier.testTag` + `testTagsAsResourceId` semantic remains the Espresso ↔ Compose interop bridge (Compose 1.2.0-alpha08+). **Robolectric 4.16** (released 2025-Q3) adds Android 16 / SDK 36 / Baklava support and requires JDK 21; introduces `ResourcesMode.NATIVE` for SDK 36 only. Robolectric 4.14/4.15 do **not** support Baklava — upgrade to 4.16 before targeting SDK 36 in JVM tests. Source: <https://github.com/robolectric/robolectric/releases/tag/robolectric-4.16> · <https://developer.android.com/develop/ui/compose/testing/interoperability> | Official |
| **WebDriver BiDi** | W3C Editor's Draft, living standard, continuously evolving. Appium 3.2 docs expose a BiDi reference, and Selenium / WebdriverIO surface BiDi via the `webSocketUrl` session field. A formal **mobile profile** has not landed at W3C as of 2026-04 — treat BiDi-on-mobile as exploratory and stay on classic WebDriver for production gates. Source: <https://w3c.github.io/webdriver-bidi/> · <https://appium.io/docs/en/3.2/reference/api/bidi/> | W3C / Appium |

### Adaptive / foldable testing

- Compose Material 3 `WindowSizeClass` exposes **compact / medium / expanded** breakpoints (plus large / extra-large in newer adaptive libraries). Test layouts at every breakpoint AND at fold/unfold posture transitions. Source: <https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes>
- Concrete devices to cover at release-gate tier as of 2026-04: Galaxy Z Fold 7 (and the leaked **Wide-form** Z Fold 8 expected ~2026-07), Pixel 10 Pro Fold (first IP68 foldable), iPad Pro with Stage Manager / Split View. Source: <https://9to5google.com/2026/04/26/samsung-galaxy-z-fold-8-wide-leak/>
- Add at least one **fold ↔ unfold posture transition** smoke test — state preservation across hinge events is the foldable-specific bug class web E2E never sees.

### Privacy Manifest impact on the test harness

- Apple's Privacy Manifest enforcement: **2024-05-01** for new App Store submissions, **2025-02-12** for new privacy-impacting third-party SDKs. Required-reason API categories include disk space, active keyboard, user defaults, file timestamp, and system boot time. Source: <https://developer.apple.com/documentation/bundleresources/privacy-manifest-files> · <https://developer.apple.com/news/?id=3d8a9yyh>
- **Test-side implication**: any XCUITest helper, Appium driver, mock SDK, or analytics-stub bundled into the test target must declare its own `PrivacyInfo.xcprivacy`. App Store Connect aggregates app + SDK manifests; a missing test SDK reason can block a TestFlight build. Add a CI step that diffs the merged manifest before release.
