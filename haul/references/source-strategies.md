# Source Strategies

**Purpose:** Source-specific query patterns, API quirks, fallback chains, and login-protected source handling for product image acquisition.
**Read when:** You are in `INTAKE`, `SEARCH`, or `DOWNLOAD` phase and need to choose / configure a source.

## Contents

- Source Tiers
- Per-Source Patterns
- Fallback Chain
- Login-Protected Sources (Navigator Handoff)
- Politeness Defaults per Source
- Source Allowlist Composition

---

## Source Tiers

Classify every source before query. Tier determines trust, license posture, and rate-limit policy.

| Tier | Description | Trust | License Class | Examples |
|------|-------------|-------|---------------|----------|
| T0 — Canonical | Manufacturer / brand canonical site or partner-provided feed | Highest | `canonical` | Sony product page, Nike CDN, partner asset feed |
| T1 — Marketplace API | Authenticated marketplace API with documented terms | High | `marketplace-licensed` | Amazon PA-API, Rakuten Ichiba API, Shopify Storefront, eBay Browse, Walmart Open API |
| T2 — Marketplace Web | Marketplace public HTML with documented scraping policy | Medium | `marketplace-licensed` (verify ToS) | Public Amazon / Rakuten / Yahoo Shopping pages |
| T3 — Image Search | General image search engines | Medium-Low | `unknown` (per-image) | Google CSE Image, Bing Image Search, SerpAPI |
| T4 — Reverse Image | Reverse image search to resolve canonical | Medium | `unknown` until canonical resolved | Google Lens, TinEye, Bing Visual Search |
| T5 — Aggregator | Third-party catalog aggregators | Low | Verify per-aggregator | UPCDatabase, OpenFoodFacts, Barcode Lookup |

**Rule:** Prefer T0 → T1 → T2 → T3 → T4 → T5. A T0 match alone satisfies the 2-source minimum. T3 / T4 / T5 alone never satisfy delivery; always pair with at least one T0-T2 source.

---

## Per-Source Patterns

### T1 — Amazon PA-API (Product Advertising API)

| Aspect | Value |
|--------|-------|
| Auth | Access Key + Secret Key + Associate Tag |
| Endpoint | `webservices.amazon.{tld}/paapi5/getitems` |
| Identifier | ASIN (10-char alphanumeric) |
| Image fields | `Images.Primary.Large.URL`, `Images.Variants[].Large.URL` |
| Rate limit | 1 req/s default; throughput scales with sales-driven shopping fees |
| Quirks | `Marketplace` differs per region (US: `webservices.amazon.com`, JP: `webservices.amazon.co.jp`); image URLs are CloudFront-signed and stable |
| License class | `marketplace-licensed` — usage governed by PA-API Operating Agreement |

### T1 — Rakuten Ichiba API

| Aspect | Value |
|--------|-------|
| Auth | Application ID |
| Endpoint | `app.rakuten.co.jp/services/api/IchibaItem/Search/20220601` |
| Identifier | `itemCode` (shop:item) or JAN |
| Image fields | `mediumImageUrls[]`, `smallImageUrls[]` (`128x128` / `64x64` thumbnails — request larger via shop CDN URL pattern) |
| Rate limit | 1 req/s default; daily quota by application |
| Quirks | Default image sizes are small; many shops host higher-res at predictable URL patterns (`_ex=500x500`) |
| License class | `marketplace-licensed` |

### T1 — Shopify Storefront API

| Aspect | Value |
|--------|-------|
| Auth | Storefront Access Token |
| Endpoint | `{shop}.myshopify.com/api/2025-01/graphql.json` |
| Identifier | Product handle / SKU / variant ID |
| Image fields | `images.edges[].node.url` (request `transform: { maxWidth: 2048 }`) |
| Rate limit | Cost-based, 50 points/sec default |
| Quirks | Per-merchant; usage varies with merchant ToS — confirm if not the merchant |

### T1 — eBay Browse API

| Aspect | Value |
|--------|-------|
| Auth | OAuth 2.0 application token |
| Endpoint | `api.ebay.com/buy/browse/v1/item/{item_id}` |
| Identifier | eBay item ID, GTIN, MPN |
| Image fields | `image.imageUrl`, `additionalImages[].imageUrl` |
| Rate limit | 5,000 calls/day default |

### T1 — Walmart Open API

| Aspect | Value |
|--------|-------|
| Auth | API key |
| Endpoint | `developer.api.walmart.com/api-proxy/service/affil/product/v2/items` |
| Identifier | Item ID, UPC |
| Image fields | `largeImage`, `mediumImage`, `imageEntities[]` |

### T3 — Google Custom Search (Image)

| Aspect | Value |
|--------|-------|
| Auth | API key + CSE ID |
| Endpoint | `customsearch.googleapis.com/customsearch/v1?searchType=image` |
| Rate limit | 100 free queries/day; paid tier 10K/day max |
| Quirks | Returns external URLs; license unknown per result; pair with T0/T1 verification |

### T3 — Bing Image Search (Azure)

| Aspect | Value |
|--------|-------|
| Auth | Subscription key |
| Endpoint | `api.bing.microsoft.com/v7.0/images/search` |
| Rate limit | Per Azure tier |
| Quirks | `imageInsights` token enables visual-similarity filtering — use to verify candidates |

### T4 — Reverse Image (Google Lens / TinEye / Bing Visual)

Use only in `reverse` recipe. Submit a sample image, retrieve candidate canonical URLs, then route candidates through normal MATCH path.

| Source | Strength | Caveats |
|--------|----------|---------|
| Google Lens | Highest recall on consumer products | No official API for general use; respect ToS |
| TinEye | Earliest-occurrence detection | Smaller index than Google; better for source-attribution |
| Bing Visual Search | API access via Bing Image Search | Lower precision on niche products |

### T0 — Manufacturer / Brand Canonical Site

| Aspect | Value |
|--------|-------|
| Pattern | Direct fetch of product page; parse JSON-LD (`Product` schema) for `image` field, OpenGraph `og:image`, microdata, or rendered HTML |
| Rate limit | 1 req/s with jitter unless robots.txt specifies `Crawl-Delay` |
| Quirks | Many brand sites use CDN with size-suffix patterns (e.g., `image.jpg?wid=2000`); request larger size variants explicitly |
| License class | `canonical` — typically permits product display in commerce contexts; verify ToS for training / redistribution |

---

## Fallback Chain

For each product, run sources in this order. Stop when 2 independent sources produce auto-accept matches, or when the chain is exhausted.

```
1. Manufacturer canonical URL (T0)        — if known
2. Tier-1 marketplace API by identifier   — ASIN / SKU / JAN match
3. Tier-1 marketplace API by name         — fuzzy match
4. Tier-2 marketplace web by URL          — public listing
5. Tier-3 image search by name + brand    — verification candidate
6. Tier-5 aggregator (UPC/EAN lookup)     — last resort
```

**Termination conditions:**
- 2 sources with score ≥ 0.85 → accept and stop.
- 1 T0 source with verified identifier match → accept and stop.
- Chain exhausted with no auto-accept → flag for review or reject (per threshold table in SKILL.md).

---

## Login-Protected Sources (Navigator Handoff)

When a source requires authentication and no API path exists:

1. Confirm with user that automated access is permitted under the source's ToS.
2. Request Navigator session: pass auth flow spec, target URL pattern, expected DOM signals.
3. Navigator returns `storageState.json` + signed download URLs (or downloaded files).
4. Haul resumes MATCH / VERIFY / CURATE on the returned files.

```yaml
HAUL_TO_NAVIGATOR_HANDOFF:
  task_type: authenticated_image_collection
  target: "{source_domain}"
  auth_method: "session_cookie | oauth | basic | form_login"
  product_keys: [list of identifiers]
  expected_outputs:
    - storageState.json
    - downloaded_files: ".haul/{batch-id}/raw-{source}/"
    - per_product_index.json
  constraints:
    rate_limit: "{req_per_sec}"
    politeness_floor: "{seconds}"
    tos_ref: "{ToS URL or attestation}"
```

---

## Politeness Defaults per Source

| Source | Default rate | Burst | Backoff trigger | Crawl-Delay honored |
|--------|--------------|-------|-----------------|----------------------|
| Amazon PA-API | 1 req/s | 1 | HTTP 503 / `Throttled` | API-quota driven |
| Rakuten API | 1 req/s | 1 | HTTP 429 | Quota-driven |
| Shopify | 50 pts/s cost | Cost-based | GraphQL throttle field | n/a |
| Google CSE | 1 req/s | 1 | HTTP 429 | n/a |
| Bing Image | 3 req/s | 5 | HTTP 429 | n/a |
| Brand canonical (T0) | 1 req/s + jitter | 1 | HTTP 429 / 5xx | Honor robots.txt `Crawl-Delay` |
| Marketplace web (T2) | 0.5 req/s + jitter | 1 | HTTP 429 / 5xx | Honor robots.txt `Crawl-Delay` |

**Adaptive backoff:** On HTTP 429 / 503 / 504, exponential backoff base = 2s, cap = 60s, max retries = 5. Honor `Retry-After` header when present (overrides exponential).

**Per-origin concurrency cap:** `≤ 4` concurrent connections per host. This is fleet-wide, not per-IP.

---

## Source Allowlist Composition

For a typical catalog batch, compose the allowlist as:

| Use case | Recommended allowlist |
|----------|----------------------|
| Internal catalog (own products) | T0 (own CDN) + T1 (own Shopify / marketplace listings) |
| External marketplace catalog | T1 marketplace API (ASIN/SKU match) + T0 manufacturer canonical |
| Reference imagery (research / training) | T0 + T1 + T3 verification, license: `unknown` declared upfront |
| LP / marketing imagery | T0 only (canonical license required for display) |
| Storybook / design fixture | T0 + T1, accept `marketplace-licensed` for non-public fixtures |

**Decision rule:** If the use case is public commerce display, require T0 canonical or explicit T1 license grant. T3 alone is never sufficient for public display.

---

## Cross-Source Deduplication

Many sources mirror each other (Amazon → manufacturer CDN, Rakuten → manufacturer CDN). Deduplicate by:

1. Final URL after redirect resolution (canonicalize CDN parameters).
2. SHA-256 of file bytes.
3. pHash for visually identical with different encoding.

Keep the highest-tier source's copy (T0 over T1 over T2). Record alternate-source URLs in manifest for provenance.
