# Cookie Consent / Cookie Policy Review Reference

Purpose: Structured review methodology for cookie consent banners and cookie policy documents under EU ePrivacy Directive 2002/58/EC (Art. 5(3)), GDPR consent integration (Art. 4(11), 7), IAB TCF v2.2 framework alignment, cookie categorization (strictly necessary / functional / analytics / marketing), and jurisdictional opt-in vs opt-out divergence (EU / UK / California / Japan). Surfaces banner-design and policy-text gaps that trigger DPA enforcement (CNIL, Garante, ICO) without empirical user testing.

## Scope Boundary

- **clause `cookie`**: cookie consent banner UX/copy review and cookie policy document review — categorization correctness, consent legality, IAB TCF v2.2 alignment, jurisdictional logic. Output is a banner-and-policy findings report with regulator-decision citations.
- **clause `privacy` (sibling)**: full privacy policy review. Cookie policy is a sub-document; a standalone cookie page is common but its terms must align with the master privacy policy.
- **clause `dpa` (sibling)**: B2B data processing contract. Cookies often involve processors (analytics vendors, ad networks) — the cookie list and the DPA sub-processor list must match.
- **clause `gap` (sibling)**: cross-document consistency. Use `gap` to verify cookie list ↔ privacy policy ↔ DPA sub-processor list ↔ vendor list match.
- **Cloak (elsewhere)**: privacy implementation. Clause `cookie` reviews the banner copy and policy text; Cloak implements the CMP (consent management platform), cookie scanning, and conditional-loading logic. Hand banner spec to Cloak for implementation.
- **Canon `gdpr` (elsewhere)**: codebase compliance. Canon checks the runtime — does the site actually block analytics until consent is granted? Clause checks the contract and copy.
- **Comply (elsewhere)**: SOC2 / ISO 27001 mapping. Cookie consent typically maps to privacy and consent control families.

## Workflow

```
SCOPE     →  identify jurisdictions targeted (EU / UK / CH / CA / JP / US-states)
          →  inventory cookies and similar tech (localStorage, fingerprinting, pixels, SDKs)
          →  identify CMP in use (OneTrust / Cookiebot / Usercentrics / TrustArc / custom)
          →  identify TCF participation (IAB TCF v2.2 yes/no; CMP ID)

SCAN      →  walk banner UX checklist (equal prominence, no dark pattern,
              reject-all parity, granular toggle, withdraw-consent path)
          →  walk cookie categorization (each cookie tagged: strictly necessary / functional /
              analytics / marketing; purpose, retention, vendor)
          →  walk policy-document checklist (categories, vendors, retention,
              cross-border transfer, opt-out mechanism, contact)
          →  walk TCF v2.2 alignment if used (purposes 1-11, special features, vendor list)

ASSESS    →  per-jurisdiction legality (EU/UK opt-in pre-load; CA opt-out via GPC;
              JP changing-law analysis under amended APPI 2022 cookie-like rules)
          →  banner dark-pattern test (CNIL guidelines, EDPB 03/2022, ICO opinion)
          →  scanner-vs-policy diff (cookies on site not in policy; policy lists cookies not on site)

REPORT    →  per-finding risk level, regulator-decision/guideline citation, proposed wording

SUGGEST   →  banner copy redlines, missing categories, vendor disclosures, opt-out flow
```

## Cookie Categorization Decision Tree

```
Is the cookie strictly necessary for a service the user explicitly requested?
├─ YES → Strictly Necessary (no consent required under ePrivacy Art. 5(3) exemption)
│         Examples: session ID for logged-in user, CSRF token, load balancer affinity,
│                   shopping-cart contents during checkout
└─ NO → Consent required (EU/UK/CH); notice + opt-out may suffice (US states, JP)
        ├─ Improves UX without being essential? → Functional / Preferences
        │   Examples: language preference, font-size choice, region selection
        ├─ Measures site usage in aggregate? → Analytics / Performance
        │   Examples: GA4, Plausible, Matomo, Hotjar, Clarity
        │   Note: even first-party analytics needs consent in EU (CNIL exempts only
        │   strict-config Matomo / AT Internet meeting tight criteria)
        └─ Targets advertising or cross-site tracking? → Marketing / Advertising
            Examples: Meta Pixel, Google Ads, LinkedIn Insight, retargeting,
                      affiliate cookies, fingerprinting, server-side conversion APIs
```

## Clause / Banner Checklist

| Item | Source | Common gap | Risk |
|------|--------|------------|------|
| Banner appears before non-necessary cookies set | ePrivacy Art. 5(3); CNIL 2020 guidelines | GA4 fires on first paint before consent | High |
| Reject All as easy as Accept All | EDPB 03/2022; CNIL Cookie sanctions | "Reject" hidden in 2nd layer; only "Manage" visible | High |
| Granular consent per purpose | GDPR Art. 7; TCF v2.2 purposes | Single "I agree" toggle | High |
| No pre-ticked boxes for non-necessary | Planet49 (CJEU C-673/17); ePrivacy | Analytics pre-ticked | High |
| Withdraw consent as easy as give | GDPR Art. 7(3) | "Cookie settings" link buried in footer only | Medium |
| Cookie list with purpose, retention, vendor | ePrivacy Art. 5(3) + GDPR Art. 13 | Generic "we use cookies" without enumeration | High |
| Third-country transfer disclosure | GDPR Art. 13(1)(f), 44 | US analytics vendor — no SCC reference | High |
| Consent record retention | GDPR Art. 7(1) accountability | No proof-of-consent log | Medium |
| Banner does not block essential content (UX dark pattern) | EDPB 03/2022 | "Wall" forces accept to read content | Medium-High |
| Consistent text across languages | GDPR Art. 12 transparency | EN strict; localized versions weaker | Medium |
| Children's cookie special handling | GDPR Art. 8; UK Children's Code | No age-gate for marketing cookies | High |
| Do Not Track / GPC honoring (CA, CO) | CCPA/CPRA + 2024 GPC enforcement | GPC signal ignored | High |
| Cookie scanner result matches policy | Accountability | Scanner finds 40 cookies; policy lists 12 | Medium |

## IAB TCF v2.2 Notes

TCF v2.2 (effective Nov 2023, mandatory replacement for v2.1 since 2024) changes:

- Purpose 1 (Store/access info on device) — separated from "legitimate interest" path; consent only.
- Legitimate interest removed for advertising-related purposes (3, 4, 5, 6) — must rely on consent.
- Standardized illustrations and language (no custom rewording of purpose names).
- "Reject All" button required at first layer.
- Withdraw / re-open consent UI required.

If using TCF v2.2: register CMP with IAB; expose `tcfapi`/`__tcfapiLocator` correctly; pass TC string downstream to vendors; respect Global Vendor List (GVL) updates.

If not using TCF: cannot rely on TCF signals to demonstrate consent to ad-tech vendors. Either join TCF or use direct contractual consent flows.

## Jurisdictional Differences

| Jurisdiction | Model | Key rule | Enforcer |
|--------------|-------|----------|----------|
| EU (GDPR + ePrivacy) | Opt-in (prior consent) | Banner before non-necessary cookies; equal Accept/Reject | National DPAs (CNIL, Garante, AEPD, BfDI) |
| UK | Opt-in (UK GDPR + PECR) | Same as EU; ICO opinion on banner design | ICO |
| Switzerland | Opt-in (revFADP, since Sep 2023) | Aligned with EU; transparency-first | FDPIC |
| California (CCPA/CPRA) | Opt-out for "sale/sharing" | "Do Not Sell or Share My Personal Information" link; honor GPC | CPPA, AG |
| Colorado / Connecticut / Virginia | Opt-out | UOOM (Universal Opt-Out Mechanism) honoring required (CO from Jul 2024) | State AG |
| Japan (APPI 2022 amendments) | Notice + cooperation request | "Personally referable info" rule for cookie-like data sent to third parties able to identify; notice/consent depending on scenario | PPC |
| Brazil (LGPD) | Opt-in for sensitive; legitimate interest possible for non-sensitive | Aligned with GDPR direction; ANPD guidance evolving | ANPD |

## Implementation Pattern: CMP / Banner UX

| Pattern | Description | When to use |
|---------|-------------|-------------|
| Two-layer banner | Layer 1: Accept All / Reject All / Manage. Layer 2: per-purpose toggles | Default for EU/UK |
| One-layer with toggles | All purposes visible upfront with toggles | High-trust B2B; low cookie count |
| Geo-routed banner | EU users see opt-in; US users see opt-out link | Multi-jurisdiction sites |
| Server-side gating | Cookies only set after server confirms consent record | High-risk verticals (health, finance) |
| TCF integrated | CMP emits TC string; vendors read before firing | Programmatic ad-tech sites |

UX rules: equal-weight buttons (color, size, position); no "Reject All" requiring more clicks than "Accept All"; no auto-dismissing banner that infers consent from inaction; persistent re-open control (footer link, floating icon).

## Anti-Patterns

- **Loading analytics before consent banner shows** — most common ePrivacy violation. GA4, Hotjar, Meta Pixel must be conditionally loaded after explicit consent. CNIL has fined repeatedly (Google EUR 150M, Facebook EUR 60M, Jan 2022).
- **"Reject All" hidden in second layer while "Accept All" is one click** — EDPB 03/2022 dark-pattern guidance plus CNIL sanctions explicitly target this asymmetry. Reject must be at first layer with equal prominence.
- **Pre-ticked consent boxes** — Planet49 (CJEU C-673/17, Oct 2019) settled this: pre-ticked boxes do not constitute consent. Any default-on toggle for non-necessary purposes is a clear violation.
- **Treating "continued browsing = consent"** — implicit consent from scrolling or navigating is invalid under GDPR Art. 4(11) (unambiguous, affirmative action required). CNIL specifically rejected this.
- **Cookie wall blocking content unless Accept** — EDPB 05/2020 cookie guidelines: a wall forcing accept to access content vitiates freely-given consent. Limited exceptions for value-equivalent paid alternatives ("pay or okay") remain contested (Garante, AustrianDPA decisions).
- **No granular purpose toggle** — bundling analytics + marketing + functional under one switch fails GDPR specificity. Each purpose needs its own toggle.
- **Stale or inaccurate cookie list** — running a scanner finds cookies absent from the policy. Accountability principle (GDPR Art. 5(2)) requires the policy to match reality. Re-scan on every deploy.
- **Ignoring GPC / Global Privacy Control signal in California / Colorado** — CCPA/CPRA AG opinions and CO UOOM rules require honoring GPC as opt-out of sale/sharing. Custom CMPs that drop the signal are non-compliant.
- **Same opt-in flow for EU and US-states** — wasteful at minimum, legally risky if it forces opt-in where opt-out is correct (US-states consumers expect to use site without banner) or skips opt-in for EU. Geo-route or use a CMP that handles per-region logic.

## Handoff

- **To Cloak**: implementation — CMP integration, conditional script loading, consent record store, GPC signal honoring, server-side gating. Send banner spec, cookie categorization, and per-jurisdiction logic.
- **To Comply**: framework mapping — cookie controls ↔ ISO 27701 / NIST Privacy Framework / SOC2 P-series. Send cookie policy and request control gap analysis.
- **To Canon `gdpr`**: codebase audit. Send banner spec and request runtime verification — does no analytics fire before consent? Are cookies in code matched to policy?
- **To Builder**: implementation tasks (banner component, settings center, withdraw flow, geo-routing, TCF API integration). Spec acceptance criteria from policy.
- **To Prose**: banner copy and policy plain-language rewrite. Microcopy must be unambiguous, jargon-free, and consistent across languages. Send draft text and target reading level.
- **To Scribe**: cookie inventory documentation and per-vendor data sheets for accountability records.
