# Mobile E2E Testing Reference

Purpose: Build an E2E test harness around a **shipped mobile application** (an app the team is releasing to users). Validate critical journeys on real or emulated devices, in a CI-scalable way, with device-farm execution for matrix coverage.

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
