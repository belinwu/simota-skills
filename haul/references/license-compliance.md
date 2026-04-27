# License & Compliance

**Purpose:** License classification, ToS rules, opt-out signal handling, regulatory context for product image acquisition.
**Read when:** You are in `INTAKE` (license scope), `SEARCH` (source ToS), `VERIFY` (license class assignment), or `audit` recipe.

## Contents

- License Classes
- Source ToS Verification
- Opt-Out Signal Surface
- Regulatory Context
- Use-Case → License Mapping
- Audit Workflow
- Take-Down Handling

---

## License Classes

Every delivered image is classified into one of these classes. The class determines permissible use.

| Class | Source signal | Permissible use | Restricted use |
|-------|---------------|------------------|-----------------|
| `canonical` | Manufacturer / brand canonical CDN; partner-licensed feed | Public commerce display, marketing, internal use | Resale of imagery itself, redistribution outside permitted contexts |
| `marketplace-licensed` | T1 marketplace API per its operating agreement | Commerce display tied to marketplace listing context | Standalone redistribution, training corpus without explicit grant |
| `partner-grant` | Documented partnership agreement with the rights holder | Per the grant's scope | Beyond the grant |
| `fair-use` | Permissible under fair use / fair dealing / quotation rights | Reference, criticism, education with attribution | Commercial display, training |
| `creative-commons` | CC license signal in source metadata | Per the specific CC variant (BY / SA / NC / ND) | Per the restriction |
| `unknown` | License could not be determined | Internal review and reference only | Public display, redistribution, training |
| `restricted` | Explicit prohibition (no-derivatives, no-AI, take-down) | None — do not retain | Any |

**Default class:** `unknown` until evidence establishes otherwise. Never upgrade classification without explicit evidence.

---

## Source ToS Verification

Run before adding a source to the allowlist.

| Check | Action |
|-------|--------|
| ToS text retrieval | Fetch the source's terms; record date and version |
| Automated access clause | Search for "automated", "scraping", "bot", "crawl", "API only" — record verbatim |
| AI training prohibition | Search for "AI training", "machine learning", "LLM", "model training" — record verbatim |
| Image redistribution clause | Search for "redistribution", "republish", "copy", "reproduction" — record verbatim |
| Per-jurisdiction notes | Note any geo-specific restrictions |
| Version & cache | Cache the ToS snapshot in `.haul/{batch-id}/tos/{source}.html`; record retrieval date |

If automated access is prohibited, refuse the source. If only API access is permitted, restrict to API; do not fall back to web scraping.

If terms are silent on automation, treat as ambiguous and ask the user before deployment.

---

## Opt-Out Signal Surface

Before any fetch from a non-API source, evaluate the opt-out signal surface.

| Signal | Source | Honor |
|--------|--------|-------|
| `robots.txt` | `/robots.txt` at origin | User-agent and path directives; `Crawl-Delay` |
| `ai.txt` | `/ai.txt` at origin (proposed standard) | AI training opt-out signals |
| TDM Reservation Protocol | HTTP header `tdm-reservation`, `tdm-policy` | EU-recognized opt-out for text and data mining |
| HTML meta tags | `<meta name="robots" content="noai, noimageai">`, `<meta name="ChatGPT-User" content="nofollow">` | Page-level signals |
| HTTP headers | `X-Robots-Tag: noai`, `X-Robots-Tag: noimageai` | Origin-level signals |
| W3C TDM Rep | TDM Reservation as a W3C Working Draft format | When present |

**Aggregation rule:** Honor any positive opt-out signal. If any of the above forbids the planned use, do not fetch. The most restrictive wins.

**Caching:** Cache opt-out signals per origin with a `24h` TTL. Re-fetch on TTL expiry. Record signal version in manifest.

---

## Regulatory Context

### EU AI Act (Regulation 2024/1689)

- Full enforcement of GPAI provisions: 2026-08-02.
- Article 53 requires GPAI providers to implement a copyright policy aligned with EU law and respect rights reservations expressed under the Copyright DSM Directive Article 4.
- Article 101 penalties for GPAI violations: up to €15M or 3% of global revenue.
- The EU Commission's GPAI Code of Practice (signatories include leading AI providers) explicitly commits to honoring `robots.txt`, IETF successor protocols, TDM Reservation Protocol, and other machine-readable opt-out signals.
- For Haul: when collecting product imagery for any AI training corpus or AI-feature use case (including embedding generation, retrieval-augmented systems with persistence, training data curation), opt-out compliance is structural. Refuse fetches from sources expressing reservation.

### EU Copyright DSM Directive (2019/790)

- Article 4 (Text and Data Mining exception for non-research) is conditional on the rights holder NOT having reserved rights in a machine-readable format.
- A reservation in any machine-readable format (robots.txt, ai.txt, TDM-rep, meta tags, HTTP headers) excludes the source from the TDM exception.

### German jurisprudence

- German courts have ruled that plain-text Terms of Service opt-outs constitute valid reservation of rights, not only machine-readable signals.
- Implication: when source ToS prohibits AI training even without machine-readable signals, the prohibition is enforceable. Always verify ToS text in addition to machine-readable signals.

### GDPR (Regulation 2016/679)

- Product images that incidentally contain identifiable persons (model imagery, user-uploaded review photos) may include personal data.
- Article 83 penalties: up to €20M or 4% of global revenue.
- For Haul: route images that contain identifiable persons (faces, identifying contexts) to Cloak for review; do not auto-deliver. Lifestyle imagery with models is the primary trigger.

### US copyright

- 17 U.S.C. § 107 (fair use) is a defense, not an authorization. Catalog imagery for commerce display is typically licensed under the marketplace operating agreement; it is not a fair-use case.
- DMCA Title II safe harbor applies only to hosting providers, not to crawlers / collectors.

### Japan copyright

- Article 30-4 of the Copyright Act of Japan permits use of copyrighted works for "non-enjoyment" purposes including data analysis and machine learning, with broad scope but with limits when the use unreasonably prejudices the interests of the rights holder.
- For commercial product display (the primary Haul use case), Article 30-4 does not authorize redistribution; treat as `marketplace-licensed` or `canonical` based on source.

### CFAA (Computer Fraud and Abuse Act, US)

- 18 U.S.C. § 1030. Bypassing technical access controls (CAPTCHA, paywall, rate-limit-with-block) may constitute unauthorized access.
- hiQ Labs v. LinkedIn (2022) clarified that ToS violation alone does not establish unauthorized access for public data, but bypassing technical controls remains in scope.
- For Haul: never bypass technical controls. Honor 429 / 403 / paywall / CAPTCHA signals as access denials.

---

## Use-Case → License Mapping

| Use case | Required license class | Rationale |
|----------|------------------------|-----------|
| Public LP / marketing | `canonical` or `partner-grant` | Manufacturer authorization required for public display |
| Internal catalog (pre-launch) | `canonical` or `marketplace-licensed` | Internal use generally permitted under marketplace agreements |
| Storybook / fixture | `canonical`, `marketplace-licensed`, or `creative-commons` | Internal development asset, but never `unknown` |
| Reference / training corpus | `canonical` (with explicit grant), `creative-commons (permissive)` | Most restrictive; opt-out compliance required |
| AI training / embedding | Explicit `partner-grant` or `creative-commons (permissive)` | Default-deny; collect only sources with explicit AI-use grant |
| Audit / spec verification | Any class with attribution | Internal verification with provenance is generally low-risk |
| Press / PR | `partner-grant` or `canonical (PR-permitted)` | Verify with rights holder before publication |

**If the class is below the required level, reject delivery and surface the gap to the user.**

---

## Audit Workflow

Run the `audit` Recipe to verify license compliance of an existing image set.

| Step | Action |
|------|--------|
| 1 | Read the existing manifest |
| 2 | For each image, recompute SHA-256 and pHash; verify match with manifest |
| 3 | Re-evaluate source URL: confirm it still resolves to the same canonical content |
| 4 | Re-fetch the source's current ToS and opt-out signals |
| 5 | Reclassify license per current evidence |
| 6 | Compare reclassified vs originally-declared classes; flag downgrades |
| 7 | Generate audit report with per-image verdict and any required remediation |

The audit does not refetch images. It verifies provenance and license assertions against current evidence.

---

## Take-Down Handling

When a manufacturer / rights holder issues a take-down request:

| Step | Action |
|------|--------|
| 1 | Record request: requester, date, scope, basis (DMCA / direct request / GDPR Article 17 erasure) |
| 2 | Identify all delivered images sourced from the requester within scope |
| 3 | Remove from delivery destinations (CDN / storage / search index) |
| 4 | Mark as `restricted` in manifest; record take-down evidence in `restricted/` folder |
| 5 | Add the requester's domain to a per-batch denylist for future runs |
| 6 | Notify downstream consumers (Showcase / Funnel / Pixel / etc.) to remove derivative uses |
| 7 | Acknowledge to the requester per the request's terms (DMCA counter-notice window if applicable) |

**Do not retain take-down-flagged images even for backup or audit purposes.** A `restricted/` placeholder records the take-down event without the image content.

---

## Provenance Requirements

Every delivered image must record:

| Field | Description |
|-------|-------------|
| `source_url` | Original fetched URL |
| `source_tier` | T0 / T1 / T2 / T3 / T4 / T5 |
| `fetch_timestamp` | ISO 8601 UTC |
| `tos_snapshot_path` | Path to cached ToS at fetch time |
| `optout_signals` | Object with `robots.txt`, `ai.txt`, TDM, meta-tag, HTTP-header values at fetch time |
| `license_class` | One of the License Classes |
| `license_evidence` | Free-text citing the basis (e.g., "Amazon PA-API Operating Agreement §X.Y") |
| `attribution_required` | Boolean |
| `attribution_text` | If required, the canonical attribution string |

Without these fields, the image cannot be delivered. Provenance is structural, not a footnote.
