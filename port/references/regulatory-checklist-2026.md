# Regulatory Compliance Checklist (2026)

This file is the canonical regulatory checklist for any Web→Native porting blueprint. **Treat regulatory items as blueprint-time decisions, not pre-submission afterthoughts.** Late-stage rejection cycles cost 1-4 weeks per round.

The information here is a 2026-Q1 snapshot. Always verify against Apple/Google/EU primary sources before final submission.

---

## A. Apple — App Store / iOS

### A.1 Privacy Manifest (`PrivacyInfo.xcprivacy`)

**Status:** Mandatory for new apps and updates since **2024-05-01**. Third-party SDKs commonly used in apps must ship their own Privacy Manifest since **2025-02-12** (App Store Connect rejects submissions otherwise).

What goes in the manifest:

| Section | Required when |
|---------|---------------|
| `NSPrivacyAccessedAPITypes` | App or any linked SDK uses a "Required Reasons API" |
| `NSPrivacyTracking` | App tracks across apps/sites |
| `NSPrivacyCollectedDataTypes` | App collects PII or device data |
| `NSPrivacyTrackingDomains` | Tracking domains contacted by the app |

Required Reasons API categories (must declare reason codes per Apple):

- `UserDefaults` — `CA92.1` (app functionality), `1C8F.1` (analytics), `C56D.1` (advertising), `AC6B.1` (ads measurement)
- `FileTimestamp` — `C617.1` (app functionality), `0A2A.1` (timer/scheduler), `3B52.1` (display info)
- `SystemBootTime` — `35F9.1` (app functionality), `8FFB.1` (anti-fraud)
- `DiskSpace` — `85F4.1` (write files), `E174.1` (compute storage)
- `ActiveKeyboards` — `54BD.1` (custom keyboard apps), `3EC4.1` (browser extensions / parental controls)

Port deliverable: list every API call and the chosen reason code. Hand to `Cloak` for review.

**Note:** Keychain itself is currently *not* in the Required Reasons API list, but stored data classifications still go into `NSPrivacyCollectedDataTypes`.

### A.2 App Tracking Transparency (ATT)

- Required if the app tracks across third-party apps or websites.
- **Granular disclosure (2025+ trend):** name third-party recipients ("shared with Meta", "shared with Google") rather than generic "service providers".
- Germany Bundeskartellamt (2025-02 preliminary) flagged Apple's self-preferential ATT prompt — expect EU prompts to become uniform across Apple's own services and third-party apps during 2026.

### A.3 Sign in with Apple (SIWA)

- The "must offer SIWA when offering any third-party login" rule was **relaxed in 2024-01**.
- Replacement requirement: when offering third-party login, provide a "privacy-equivalent" option (limit to name+email, support private email relay, no cross-app tracking).
- **Practical guidance:** offering SIWA remains the safest path. Custom "privacy-equivalent" alternatives still trigger reviewer scrutiny.

### A.4 5.1.2(i) — Third-party AI disclosure (effective 2025-11)

If the app sends user data to a third-party AI (OpenAI, Anthropic, Google, etc.):

- Disclose the AI provider **by name** (no generic "service providers")
- Disclose the **purpose** of the data sharing
- Obtain **explicit consent** before transmission

**On-device AI** (Core ML, Foundation Models) is exempt from disclosure. Network-bound AI is in scope.

Port deliverable: a UI flow that names the provider, explains the purpose, and captures consent before any AI request — included in MVP, not retrofitted.

### A.5 IAP / external payment links

- US (since 2025-05): External payment links / CTAs are allowed in the app per court ruling — App Review Guidelines updated.
- Other regions: still subject to standard IAP requirements unless DMA / local law applies.
- Apple still requires that parallel IAP option be offered for "consumable" categories.

### A.6 DMA (EU)

- **2025-06-26:** Single entitlement + 3 fee models. IAP rate reduced 30%→20%; external payment also subject to 20% commission; **Core Technology Commission (CTC) 5%** on externally-announced IAP revenue.
- **2026-01-01:** Core Technology Fee (CTF) is fully retired; CTC is the consolidated model.
- iOS 18.6+: alternative marketplaces in EU; AltStore PAL etc. operating.
- **Port action:** decide whether the app distributes via App Store only, alternative marketplaces, or web-direct in EU. Note CTC implications in finance handoff.

### A.7 EU DSA Trader Status

- **Effective 2025-02-17:** All developers must declare trader status in App Store Connect — including non-EU developers and those not selling in EU. Non-compliant apps are removed from EU storefronts.

### A.8 Age Rating — 5-tier (Apple, 2026-01-31 deadline)

- New tiers: **4+, 9+, 13+, 16+, 18+** (replacing the older 4-tier scheme).
- All apps must answer the new questionnaire by **2026-01-31** to remain available in iOS 26+ devices.
- New API: **Declared Age Range** — apps receive only an age band (not birthday) for child-appropriate content gating.
- Restricted accounts: apps exceeding the rating are not surfaced in Today / Games / Apps tabs.

### A.9 Health, Children, Sensitive Categories

- HealthKit data: cannot be used for advertising; cannot be stored in iCloud Drive; cannot write fake data.
- Kids Category: stricter rules on data collection, advertising, and required parental gates.
- **Loan apps (2025-11):** APR cap 36%; cannot demand full repayment within 60 days.
- **Creator / UGC apps (2025-11):** must implement age-aware content restrictions.
- **Copycat apps (2025-11):** impersonating brand/icon/product is now an explicit rejection cause.

### A.10 Xcode / iOS SDK requirement

- **Xcode 26 + iOS 26 SDK required from 2026-04-28** for new submissions and updates.
- Roadmap should plan Liquid Glass adoption or document an explicit defer decision (with visual fallback verified).

---

## B. Google — Play Store / Android

### B.1 Target API Level

- **Effective 2025-08-31:** New apps and updates must target **API 35 (Android 15)** or higher (Wear OS / Auto / TV: API 34).
- Extension request was available via Play Console up to 2025-11-01.
- targetSdk 36 mandate is expected during 2026 — exact date is yet to be officially announced; plan for it during P1/P2.

### B.2 16KB Page Size

- **Effective 2025-11-01:** New releases on Google Play must support **16KB memory page size** (apps with NDK dependencies must be rebuilt against the 16KB-aligned NDK).
- Performance benefit: ~3-30% startup speedup, ~4.5% battery improvement.
- Extension available up to 2026-05-31 (request-based).
- Port action: audit all NDK-using SDKs (image processing, ML Kit, maps, crypto, gaming engines). Reject any that don't yet ship 16KB-aligned binaries.

### B.3 Edge-to-Edge enforcement (API 36)

- `R.attr#windowOptOutEdgeToEdgeEnforcement` is deprecated and disabled at targetSdk 36.
- Port action: design every screen with `Modifier.windowInsetsPadding()` / `WindowInsets.systemBars` from day 1.

### B.4 Predictive Back

- targetSdk 36: predictive back gesture animations are default ON for back-to-home, cross-task, and cross-activity.
- `onBackPressed()` is no longer dispatched. Use `OnBackPressedDispatcher` / `BackHandler`.

### B.5 Adaptive / Large screen forced resizability (API 36)

- For sw 600dp+ displays at targetSdk 36:
  - `screenOrientation`, `resizableActivity`, `minAspectRatio`, `maxAspectRatio` ignored
  - `setRequestedOrientation()` / `getRequestedOrientation()` ignored
- Exceptions: games (`appCategory="game"`), screens < sw 600dp, user override.
- Temporary opt-out: `PROPERTY_COMPAT_ALLOW_RESTRICTED_RESIZABILITY` (expires API 37).

### B.6 Photo & Video permission policy

- **Effective 2025-05-28:** Apps holding `READ_MEDIA_IMAGES` / `READ_MEDIA_VIDEO` for non-essential reasons are out of policy. Use **Photo Picker** instead for one-shot / limited media use.
- Declaration form via Play Console required if broad media access is essential.

### B.7 Data Safety form

- Mandatory for all apps including Internal Testing tracks.
- **2025-04-10 update:** `Settings.Secure.ANDROID_ID` is classified as "Device or other IDs" and must always be disclosed. SDK provider's own use counts as third-party transfer (Sharing).
- Google Play actively blocks data access of non-compliant apps; ~255k apps blocked and ~80k accounts suspended in 2025.

### B.8 Foreground Service Types (API 34+)

- Manifest must declare service type with matching permission.
- API 35+: `dataSync` and `mediaProcessing` capped at **6 hours per 24 hours**.
- Background-initiated foreground services restricted since API 31.

### B.9 Privacy Sandbox on Android (SDK Runtime)

- Android 14+ introduces SDK Runtime — ad/measurement SDKs run in an isolated process, IPC-bound to the host app.
- Latency impact on RE-enabled SDKs. Audit at blueprint when ad-revenue dependent.

### B.10 AI Content Policy

- **2025-01:** Google Play requires:
  - Visible labeling of AI-generated content (chat, image, music)
  - Listing description must indicate AI usage
  - **AI content moderation** mechanisms (against CSAM, deceptive content)
  - Stricter requirements for kid-targeted apps
- Penalties: warnings + 7-14 day blocks for minor; suspension for major violations.

### B.11 Google Play Billing / external

- Standard 15-30% commission still applies in most regions.
- DMA EU: third-party payment alternatives allowed; 27% commission on external payments (under separate Google rules) — verify current rates.

### B.12 Credential Manager (recommended path)

- 2025-09 official guidance: Credential Manager + Passkeys is the recommended sign-in surface, integrating Passkey, Password, and Sign-in-with-Google.
- Industry results: X 2× sign-in rate, KAYAK 50% sign-in time reduction.
- Passkey eligibility: API 28+.

---

## C. Cross-Cutting Regulations

### C.1 EU Accessibility Act (EAA)

- **In force since 2025-06-28** for all apps sold in the EU (regardless of company HQ location).
- Technical reference: **EN 301 549** (incorporates **WCAG 2.1 Level AA** plus mobile-specific extensions).
- Existing services have until **2028-06** for grandfathered compliance, but any major update during the grandfather window triggers immediate compliance.
- Exception: micro-enterprises (< 10 employees and < €2M turnover).
- Penalties: up to €3M + market exclusion + business suspension.
- Four obligations: comply / document / maintain / report.

### C.2 Children-targeted regulation

- US state laws (Utah, Texas, etc.): age-verification mandates.
- Apple/Google now provide age-band APIs to apps; verification largely OS-mediated.
- Kids-category apps face stricter ad / data / parental-consent rules across both stores.

### C.3 Fintech / Crypto

- App Store 3.1.5(b): per-country license proof required.
- Apple submission lead time: weeks-to-months for novel fintech/crypto.
- US loan apps (App Store, 2025-11): 36% APR cap, no 60-day balloon.
- Banking apps: biometric + Passkey is effectively required.
- Stablecoin / CBDC: emerging regulation in UK (FCA) and other jurisdictions during 2025-2026.

### C.4 Privacy laws (GDPR / CCPA / others)

- Hand off to `Cloak` for DPIA, consent flows, DSR endpoints, retention schedules.
- Mobile-specific concerns:
  - Default-opt-in tracking is not allowed in EU
  - Consent must be revocable in-app (Settings deep link to revoke)
  - Cross-border data transfer disclosure (esp. AI APIs hosted in US)

---

## D. Pre-Submission Gate Checklist

Run this before any TestFlight External / Play Closed Testing build.

### iOS

- [ ] `PrivacyInfo.xcprivacy` present and complete
- [ ] All linked third-party SDKs ship Privacy Manifests
- [ ] ATT prompt (if tracking) discloses recipients by name
- [ ] SIWA (or privacy-equivalent) offered alongside any social login
- [ ] AI disclosure UI flow per 5.1.2(i) (if third-party AI used)
- [ ] Age Rating questionnaire updated to new 5-tier (by 2026-01-31)
- [ ] DSA trader status declared
- [ ] DMA fee model confirmed (if EU distribution)
- [ ] Xcode 26 + iOS 26 SDK build (from 2026-04-28)
- [ ] If health / kids / fintech / loan / creator: domain-specific rules verified

### Android

- [ ] targetSdk = 35 (or 36 if mandated)
- [ ] 16KB-aligned native libraries
- [ ] Edge-to-edge layout (no opt-out at API 36)
- [ ] Predictive back wired via `BackHandler` / `OnBackPressedDispatcher`
- [ ] Foreground service types declared
- [ ] Photo Picker used (or media permission declaration filed)
- [ ] Data Safety form complete and accurate (incl. ANDROID_ID classification)
- [ ] Credential Manager wired for sign-in
- [ ] AI content labeled in app + listing (if applicable)
- [ ] Adaptive layout for sw 600dp+ (if API 36 expected)

### Cross

- [ ] EAA conformance (EN 301 549 / WCAG 2.1 AA) for any EU sale
- [ ] Per-country fintech license (if regulated)
- [ ] Privacy policy URL valid in both stores

---

## E. Output Skeleton

```markdown
# Regulatory & Privacy Compliance Plan: <App Name>

## Apple (iOS)
### Privacy Manifest
- Required Reasons API declarations: …
- 3rd-party SDKs Privacy Manifest status: …
- Tracking domains: …

### ATT
- Tracking? yes/no
- 3rd-party recipients: …

### SIWA / Auth
- Social logins offered: …
- SIWA included: yes/no (rationale)

### AI Disclosure (5.1.2(i))
- Third-party AI used: …
- Disclosure UI flow: …
- Consent capture: …

### IAP / Payment
- Standard IAP / external link / mixed
- DMA EU: …

### Age Rating
- Questionnaire completed (5-tier): yes/no
- Declared Age Range API: yes/no

### Domain-specific (if applicable)
- Health / Kids / Fintech / Crypto / Loan / Creator: …

## Google (Android)
### Target / 16KB
- targetSdk: 35 / 36
- 16KB native libs: yes/no (audit list)

### Edge-to-edge / Predictive Back
- Implementation: …

### Photo & Video
- Photo Picker / Permission declaration: …

### Data Safety
- Form completion: …
- ANDROID_ID classification: …
- 3rd-party Sharing classification: …

### Foreground Service Types
- Types declared: …

### Credential Manager / Passkey
- Implementation: …

### AI Content Labeling
- In-app: …
- Listing description: …

## Cross-cutting
- EAA conformance: …
- Per-country licenses: …
- Privacy law (GDPR/CCPA): handoff to Cloak

## Pre-submission gates
- iOS: [checklist results]
- Android: [checklist results]

## Open / Blocking items
- …

## Handoffs
- Cloak: privacy data flow + DPIA
- Crypt: token / Passkey storage architecture
- Comply: regulatory mapping (SOC2 / PCI-DSS / HIPAA)
- Launch: submission timeline & rollback
```

---

## F. Sources (2026 snapshot)

- Apple Developer Privacy Manifest docs / Required Reasons API (TN3183)
- Apple App Review Guidelines (5.1.2(i), DMA, IAP, Age Rating)
- Apple Developer Upcoming Requirements (Xcode/SDK schedule, Age Rating deadline)
- Google Play Target API Level Requirements
- Google Play 16KB page size policy
- Google Play Photo & Video permission policy
- Google Play Data Safety Section help articles
- Android Developers Blog (Credential Manager, Material 3 Expressive, edge-to-edge)
- EU Accessibility Act (EAA / EN 301 549)
- DMA — European Commission and Apple Developer DMA support page

When using this checklist, verify each rule against the latest Apple Developer / Google Play / EU portals — regulatory pages move and dates shift. Treat this file as a *starting* checklist, not an authoritative legal source.
