# Legal Compliance Architecture

## Compliance as Infrastructure

Legal compliance is not an afterthought — it is a structural subsystem designed alongside the crawler. Every crawl architecture must include these components.

## robots.txt Parser Service

### Architecture

```
┌──────────────┐     ┌───────────────────┐
│  Worker N     │────▶│  robots.txt Cache │
│  (fetch URL)  │     │  Service          │
└──────────────┘     └────────┬──────────┘
                              │ Cache miss
                              ▼
                       ┌──────────────┐
                       │  Fetch       │
                       │  robots.txt  │
                       └──────┬───────┘
                              │
                              ▼
                       ┌──────────────┐
                       │  Parse +     │
                       │  Store       │
                       └──────────────┘
```

### Design Specifications

| Component | Specification |
|-----------|---------------|
| Cache TTL | 24 hours (default), configurable per domain |
| Cache backend | Redis with domain key, serialized parsed rules |
| Fetch failure | Fall back to conservative policy (1 req/10s, allow only root) |
| Parser | RFC 9309 compliant (2022 standard), handle wildcards, Crawl-delay |
| Versioning | Store fetch timestamp + ETag for change detection |
| User-agent matching | Match specific UA first, then `*` wildcard |

### Crawl-Delay Enforcement

```
Decision flow:
1. Check robots.txt for Crawl-delay directive for our User-Agent
2. If specified: use as minimum inter-request interval for that domain
3. If not specified: use default (1 second)
4. Apply token bucket rate limiter: burst = 1, refill = 1/crawl_delay
5. Floor: never faster than 1 request per second per domain

Edge cases:
- Crawl-delay = 0: treat as 1 second (defensive)
- Crawl-delay > 60: flag for review (may indicate "don't crawl")
- Missing robots.txt (404): no restrictions, use default rate
- Fetch error (5xx): retry 3x with backoff, then conservative policy
```

## EU AI Act Compliance (Full Enforcement August 2026)

### Opt-Out Signal Taxonomy

| Signal Type | Source | Detection Method | Action |
|-------------|--------|-----------------|--------|
| Machine-readable | `robots.txt` Disallow | robots.txt parser | Block URL/path |
| Machine-readable | `X-Robots-Tag: noai` | HTTP header inspection | Skip content |
| Machine-readable | `<meta name="robots" content="noai">` | HTML meta parse | Skip content |
| Machine-readable | `ai.txt` (proposed standard) | Dedicated parser | Follow directives |
| Plain-text | ToS "no scraping" clause | Manual review → domain blocklist | Block domain |
| Plain-text | ToS "no AI training" clause | Manual review → domain blocklist | Block domain |

### Implementation Pattern

```
Opt-out check pipeline (per URL):
1. robots.txt check (cached) → blocked? → skip
2. HTTP response headers → X-Robots-Tag check → noai? → skip content, keep metadata
3. HTML <meta> tags → noai? → skip content, keep metadata
4. Domain blocklist check (manually curated from ToS review) → blocked? → skip
5. Pass → proceed with extraction

Log every opt-out decision for audit trail.
```

### Penalty Framework

| Violation | Penalty (EU AI Act) |
|-----------|---------------------|
| GPAI data obligations (Art. 53) | Up to €15M or 3% global revenue (Art. 101) |
| Copyright opt-out violation | National copyright law + EU AI Act overlay |
| Data minimization failure (GDPR) | Up to €20M or 4% global turnover (Art. 83) |

## Jurisdiction Risk Table

| Jurisdiction | Key Law | Risk Level | Key Requirement |
|-------------|---------|------------|-----------------|
| EU | AI Act + GDPR + Copyright Directive | High | Respect all opt-out signals, data minimization, DPIA for PII |
| US | CFAA + State laws + Fair Use doctrine | Medium | No unauthorized access, respect ToS, fair use analysis |
| UK | UK GDPR + ICO guidance | Medium-High | Similar to EU, ICO enforcement actions |
| Japan | Copyright Act Art. 30-4 (informational analysis exception) | Low-Medium | Broad research exception, but respect opt-out |
| China | Personal Information Protection Law | High | Strict consent requirements for PII |
| Australia | Privacy Act + Copyright Act | Medium | Fair dealing defense, privacy obligations |

## Sitemaps Integration

### Design Pattern

```
Sitemap as priority signal, NOT exhaustive URL source:
1. Fetch /sitemap.xml (or sitemap index)
2. Parse lastmod, changefreq, priority attributes
3. Inject URLs into frontier with priority boost
4. Do NOT rely solely on sitemap — many sites have incomplete sitemaps
5. Sitemap URLs get priority level 2 (below seeds, above discovered links)

Cache: Same TTL as robots.txt (24h)
Formats: XML sitemap, sitemap index, RSS/Atom feed
```

## Audit Trail Design

### What to Log

| Event | Fields | Retention |
|-------|--------|-----------|
| robots.txt fetch | domain, timestamp, status, rules_hash | 90 days |
| Opt-out detection | url, signal_type, action_taken | 1 year |
| Domain block | domain, reason, blocked_by, timestamp | Indefinite |
| Crawl-delay override | domain, requested_delay, applied_delay | 90 days |
| PII detection | url, pii_type, action_taken | 1 year (or per policy) |

### Storage

```
Audit log format: JSON-Lines, append-only
Storage: S3/GCS with lifecycle policy
Indexing: Date-partitioned for efficient querying
Access: Read-only for audit, write-only for crawler
```
