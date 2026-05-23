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
| T1 — Marketplace API | Authenticated marketplace API with documented terms | High | `marketplace-licensed` | Amazon Creators API (PA-API 5.0 deprecates 2026-04-30, retired 2026-05-15 — see Migration notes), Rakuten Ichiba API (openapi.rakuten.co.jp from 2026-02-10), Shopify Storefront 2026-04+, eBay Browse, Walmart Open API |
| T2 — Marketplace Web | Marketplace public HTML with documented scraping policy | Medium | `marketplace-licensed` (verify ToS) | Public Amazon / Rakuten / Yahoo Shopping pages |
| T3 — Image Search | General image search engines | Medium-Low | `unknown` (per-image) | Google Custom Search (closed to new customers; sunset 2027-01-01), Brave Search Image (independent index, default Bing successor), SerpAPI, Azure AI Agents Grounding with Bing Search (replaces retired Bing Search API EOL 2025-08-11) |
| T4 — Reverse Image | Reverse image search to resolve canonical | Medium | `unknown` until canonical resolved | Google Lens, TinEye, Brave Search Visual (Bing Visual Search retired 2025-08-11) |
| T5 — Aggregator | Third-party catalog aggregators | Low | Verify per-aggregator | UPCDatabase, OpenFoodFacts, Barcode Lookup |

**Rule:** Prefer T0 → T1 → T2 → T3 → T4 → T5. A T0 match alone satisfies the 2-source minimum. T3 / T4 / T5 alone never satisfy delivery; always pair with at least one T0-T2 source.

---

## Per-Source Patterns

### T1 — Amazon PA-API 5.0 → Creators API (2026 migration)

| Aspect | Value |
|--------|-------|
| Status | **PA-API 5.0 deprecates 2026-04-30; endpoint retires 2026-05-15.** Amazon Offers V1 inside PA-API removed 2026-01-31 — live pricing / Prime status only available via Creators API Offers V2. [Source: dev.to/th3nate, blog.freshstore.com] |
| Successor | Amazon Creators API (different auth scheme, request shape, and token lifecycle — not a config swap). Docs: `affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction` |
| Auth | PA-API 5.0: Access Key + Secret Key + Associate Tag (deprecated path). Creators API: OAuth-style bearer tokens scoped to Associate account. |
| Endpoint | PA-API 5.0 (legacy until 2026-05-15): `webservices.amazon.{tld}/paapi5/getitems`. Creators API: per docs site. |
| Identifier | ASIN (10-char alphanumeric) |
| Image fields | `Images.Primary.Large.URL`, `Images.Variants[].Large.URL` (Creators API preserves Large/Medium/Small dimensions but field paths differ) |
| Rate limit | Driven by shipped-item revenue: 1 TPD per $0.05 / 1 TPS per $4,320 of attributed revenue in the trailing 30 days, capped at 10 TPS. Starter accounts: 1 req/s. [Source: webservices.amazon.com api-rates docs] |
| Quirks | `Marketplace` differs per region (US: `webservices.amazon.com`, JP: `webservices.amazon.co.jp`); image URLs are CloudFront-signed and stable. After 2026-05-15, all Haul recipes must target Creators API. |
| License class | `marketplace-licensed` — usage governed by Amazon Associates Operating Agreement (PA-API 5.0) or Creators API Operating Agreement (post-migration) |

### T1 — Rakuten Ichiba API (2026 infrastructure migration)

| Aspect | Value |
|--------|-------|
| Status | **Domain migrating from `app.rakuten.co.jp` → `openapi.rakuten.co.jp`.** Dual-run window: 2026-02-10 → 2026-05-13. Legacy domain and numeric `applicationId` permanently shut down **2026-05-14** (1 day after `2026-05-13` cutoff). Re-register the app to obtain a UUID `applicationId` plus an API Access Key. [Source: webservice.rakuten.co.jp, 8091.info] |
| Current API version | `IchibaItem/Search/2026-04-01` — verify in webservice.rakuten.co.jp/documentation before each batch. |
| Auth | New scheme: UUID `applicationId` (e.g., `2fc160ec-26f2-4a04-888f-4b6eb504b0e6`) + API Access Key header. Old numeric `applicationId` rejected after 2026-05-14. |
| Endpoint | New: `openapi.rakuten.co.jp/services/api/IchibaItem/Search/20260401`. Legacy `app.rakuten.co.jp` decommissioned 2026-05-14. |
| Identifier | `itemCode` (shop:item) or JAN |
| Image fields | `mediumImageUrls[]`, `smallImageUrls[]` (`128x128` / `64x64` thumbnails — request larger via shop CDN URL pattern) |
| Rate limit | 1 req/s default; daily quota by application |
| Quirks | Default image sizes are small; many shops host higher-res at predictable URL patterns (`_ex=500x500`). Haul `INTAKE` must check the source allowlist for any pre-2026-05-14 endpoint string and surface a migration warning. |
| License class | `marketplace-licensed` |

### T1 — Shopify Storefront API

| Aspect | Value |
|--------|-------|
| Auth | Storefront Access Token |
| Endpoint | `{shop}.myshopify.com/api/2026-04/graphql.json` (current stable as of 2026-05). New stable release every quarter; 12-month minimum support window per version. [Source: shopify.dev/docs/api/usage/versioning] |
| Identifier | Product handle / SKU / variant ID |
| Image fields | `images.edges[].node.url` (request `transform: { maxWidth: 2048 }`) |
| Rate limit | Cost-based, 50 points/sec default. Cost budget is **per Storefront Access Token** — parallel Haul subagents sharing one token must serialize or partition. [F06 mitigation] |
| 2026 breaking changes | Checkout `metafields` deprecated in 2026-04 (migrate to cart metafields). 2026-07 will remove deprecated `PRIVATE` / `PUBLIC_READ` enums on metaobject definitions and drop the `grams` field on `DraftOrderLineItem`. Cart emits `unavailable in buyer's location` warnings from 2026-07. [Source: shopify.dev/changelog, weaverse.io/blogs/shopify-developer-breaking-changes-april-2026] |
| Quirks | Per-merchant; usage varies with merchant ToS — confirm if not the merchant |

### T1 — eBay Browse API

| Aspect | Value |
|--------|-------|
| Auth | OAuth 2.0 application token |
| Endpoint | `api.ebay.com/buy/browse/v1/item/{item_id}` |
| Identifier | eBay item ID, GTIN, MPN |
| Image fields | `image.imageUrl`, `additionalImages[].imageUrl` (Note: `Image.height` and `Image.width` are reserved fields — only `imageUrl` is populated as of 2026) |
| Rate limit | 5,000 calls/day default; higher limits require Application Growth Check approval via developer.ebay.com |
| 2025 migration note | **eBay Finding API and Shopping API were decommissioned 2025-02-05** (deprecated 2024-01-04). Any Haul source allowlist entry targeting `api.ebay.com/services/search/FindingService/v1` or `open.api.ebay.com/shopping` is broken and must be removed. Successor: Browse API for product search; `searchByImage` endpoint available for reverse-image product matching. [Source: developer.ebay.com/develop/get-started/api-deprecation-status] |

### T1 — Walmart Open API

| Aspect | Value |
|--------|-------|
| Auth | API key |
| Endpoint | `developer.api.walmart.com/api-proxy/service/affil/product/v2/items` |
| Identifier | Item ID, UPC |
| Image fields | `largeImage`, `mediumImage`, `imageEntities[]` |

### T3 — Google Custom Search (Image) — sunset path

| Aspect | Value |
|--------|-------|
| Status | **Closed to new customers (since 2025).** Existing keys keep working until **2027-01-01**, then mandatory migration to Vertex AI Search (semantic search over your own corpus, ~$2 / 1,000 queries base tier). [Source: developers.google.com/custom-search, dev.to/nexgendata] |
| Auth | API key + CSE ID |
| Endpoint | `customsearch.googleapis.com/customsearch/v1?searchType=image` |
| Rate limit | 100 free queries/day; paid tier $5 / 1,000 queries, hard cap 10K queries/day (~$1,500/month at max) |
| Quirks | Returns external URLs; license unknown per result; pair with T0/T1 verification. Treat as legacy — do not build new pipelines on Google CSE without an explicit Vertex AI Search migration plan. |

### T3 — Brave Search Image API (primary Bing successor)

| Aspect | Value |
|--------|-------|
| Auth | API key (Brave Search API, Search plan) |
| Endpoint | `api.search.brave.com/res/v1/images/search` |
| Index | Independent Brave web index — not a Bing reseller. Brave launched independent image/video search in 2025 after removing its Bing API dependency. [Source: brave.com/blog/image-video-search/] |
| 2026 Plans | Brave Search API split into **Search** (data substrate: Web, Image, Video, News, LLM Context, Place) and **Answers** (AI-generated synthesis) since 2026-02. |
| License class | `unknown` (per-image) — same constraint as any general image search |

### T3 — Azure AI Agents Grounding with Bing Search (Microsoft successor)

| Aspect | Value |
|--------|-------|
| Status | **Bing Search APIs retired 2025-08-11.** Microsoft's official successor is **Grounding with Bing Search** inside the Azure AI Agents Service. Migration cost is 40–483% higher than legacy Bing Search API at equivalent volume. [Source: learn.microsoft.com/en-us/lifecycle/announcements/bing-search-api-retirement, ppc.land] |
| Auth | Azure AD / Azure AI Project key |
| Endpoint | Azure AI Agents Service grounding tool (no direct REST passthrough — agent-mediated) |
| Quirks | Agent-mediated; raw image URL extraction requires the Azure AI Agent to surface citations. For batch image acquisition, **Brave Search Image API is the lower-friction Bing successor**; reserve Azure AI Agents for cases that need LLM-mediated grounding. |
| Migration deadline | Any code still calling `api.bing.microsoft.com/v7.0/images/search` is broken since 2025-08-11 — remove from source allowlist. |

### T4 — Reverse Image (Google Lens / TinEye / Brave)

Use only in `reverse` recipe. Submit a sample image, retrieve candidate canonical URLs, then route candidates through normal MATCH path.

| Source | Strength | Caveats |
|--------|----------|---------|
| Google Lens | Highest recall on consumer products | No official API for general use; respect ToS |
| TinEye | Earliest-occurrence detection | Smaller index than Google; better for source-attribution |
| Brave Search Visual | Independent index; API accessible | Smaller index than Google; replaces Bing Visual Search after Bing Search API EOL 2025-08-11 |
| ~~Bing Visual Search~~ | — | **Retired 2025-08-11. Remove from allowlist.** |

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
| Amazon PA-API 5.0 (legacy → 2026-05-15) | 1 req/s, scales to ≤ 10 TPS by attributed revenue | 1 | HTTP 503 / `Throttled` | API-quota driven |
| Amazon Creators API (post-2026-05-15) | Per OAuth token bucket — verify per the Creators API Operating Agreement | 1 | HTTP 429 | API-quota driven |
| Rakuten API (`openapi.rakuten.co.jp`) | 1 req/s | 1 | HTTP 429 | Quota-driven; cost budget is per-token, parallel batches sharing token must serialize or partition [F06] |
| Shopify | 50 pts/s cost | Cost-based | GraphQL throttle field | n/a |
| Google CSE | 1 req/s | 1 | HTTP 429 | n/a |
| Brave Search Image | Per Search plan (commercial tiers) | Per plan | HTTP 429 | n/a |
| Azure AI Agents (Grounding with Bing) | Per Azure AI Agents tier | Per tier | HTTP 429 / 503 | n/a |
| ~~Bing Image (`api.bing.microsoft.com`)~~ | **Retired 2025-08-11** | — | — | — |
| ~~eBay Finding API~~ | **Decommissioned 2025-02-05** | — | — | — |
| ~~eBay Shopping API~~ | **Decommissioned 2025-02-05** | — | — | — |
| Brand canonical (T0) | 1 req/s + jitter | 1 | HTTP 429 / 5xx | Honor robots.txt `Crawl-Delay` |
| Marketplace web (T2) | 0.5 req/s + jitter | 1 | HTTP 429 / 5xx | Honor robots.txt `Crawl-Delay` |

**Adaptive backoff:** On HTTP 429 / 503 / 504, exponential backoff base = 2s, cap = 60s, max retries = 5. Honor `Retry-After` header when present (overrides exponential).

**Per-origin concurrency cap:** `≤ 4` concurrent connections per host. This is fleet-wide, not per-IP.

---

## Source Allowlist Composition

For a typical catalog batch, compose the allowlist as:

| Use case | Recommended allowlist (2026-05 baseline) |
|----------|----------------------|
| Internal catalog (own products) | T0 (own CDN) + T1 (own Shopify 2026-04+ / marketplace listings) |
| External marketplace catalog | T1 marketplace API (Amazon Creators API post-2026-05-15, Rakuten `openapi.rakuten.co.jp`, Shopify 2026-04+) + T0 manufacturer canonical |
| Reference imagery (research / training) | T0 + T1 + T3 (Brave Search Image preferred over legacy Google CSE) verification, license: `unknown` declared upfront; **EU AI Act enforcement live from 2026-08-02 — opt-out compliance is structural for training corpora** |
| LP / marketing imagery | T0 only (canonical license required for display). For Japan-targeted LPs, preserve attribution per AUPMR (stealth marketing prohibition since 2023-10) |
| Storybook / design fixture | T0 + T1, accept `marketplace-licensed` for non-public fixtures |

**Decision rule:** If the use case is public commerce display, require T0 canonical or explicit T1 license grant. T3 alone is never sufficient for public display.

---

## Cross-Source Deduplication

Many sources mirror each other (Amazon → manufacturer CDN, Rakuten → manufacturer CDN). Deduplicate by:

1. Final URL after redirect resolution (canonicalize CDN parameters).
2. SHA-256 of file bytes.
3. pHash for visually identical with different encoding.

Keep the highest-tier source's copy (T0 over T1 over T2). Record alternate-source URLs in manifest for provenance.

---

## 2026–2027 Migration Calendar (verify at INTAKE)

| Date | Event | Action |
|------|-------|--------|
| 2025-02-05 | eBay Finding API & Shopping API decommissioned | Remove from allowlist; replace with eBay Browse API (`/buy/browse/v1/`) [Source: developer.ebay.com/develop/get-started/api-deprecation-status] |
| 2026-01-31 | Amazon PA-API Offers V1 removed | Switch live-pricing reads to Amazon Creators API Offers V2 |
| 2026-01 | GS1 Digital Link Resolver standard v1.2.0 released | Validate GTIN-embedded GS1 Digital Link URIs using updated conformant resolver spec (ref.gs1.org/standards/resolver/) |
| 2026-02-10 | Rakuten `openapi.rakuten.co.jp` opens | Re-register apps; obtain UUID `applicationId` + API Access Key |
| 2026-04-30 | Amazon PA-API 5.0 deprecation | Complete Creators API migration before retirement window |
| 2026-05-13 | Rakuten dual-run window ends | Cut over Rakuten clients to new domain |
| 2026-05-14 | Rakuten legacy `app.rakuten.co.jp` shutdown | Any remaining `app.rakuten.co.jp` calls fail |
| 2026-05-15 | Amazon PA-API 5.0 endpoint retired | `webservices.amazon.*.com/paapi5/*` returns errors |
| 2026-07 | Shopify 2026-07 release | Drop deprecated `PRIVATE`/`PUBLIC_READ` metaobject enums; remove `grams` field |
| 2026-08-02 | EU AI Act enforcement powers + Art. 50 AI-content disclosure activate | Opt-out compliance enforceable (€15M / 3% revenue); C2PA-signed AI-generated images require machine-detectable marking |
| 2027-12-31 | GS1 Sunrise 2027 — retailer POS 2D-readiness deadline | Retail POS systems must read GTIN from GS1 Digital Link QR / DataMatrix. New packaging from 2025–2026 should carry 2D code alongside 1D EAN/UPC. Haul INTAKE must parse GS1 Digital Link URIs in product identifiers from this point. [Source: gs1us.org/industries-and-insights/by-topic/sunrise-2027, trackvision.ai GS1 Sunrise 2027 compliance deadlines] |

Sources: webservices.amazon.com api-rates, blog.freshstore.com, webservice.rakuten.co.jp, 8091.info, shopify.dev/changelog, artificialintelligenceact.eu, developer.ebay.com, gs1us.org/industries-and-insights/by-topic/sunrise-2027, ref.gs1.org/standards/resolver/.

`INTAKE` MUST verify that every entry in `sources_allowlist` is not on a retired endpoint as of the batch start date. Any legacy endpoint triggers an Ask First with migration plan.
