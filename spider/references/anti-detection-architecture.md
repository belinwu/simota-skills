# Anti-Detection Architecture

## Ethical Framework

**Anti-detection measures are infrastructure design decisions, not adversarial tools.** Before designing any anti-detection layer, document:

1. **Authorization:** Written permission, ToS compliance, or legal basis for crawling
2. **Purpose:** Legitimate use case (research, market analysis, compliance monitoring)
3. **Proportionality:** Measures are proportional to the access need
4. **Transparency:** User-Agent identifies the crawler and provides contact info

**When NOT to design anti-detection:**
- Public data with permissive robots.txt → standard crawling is sufficient
- Sitemap-only crawls → no detection risk
- API-based data collection → use the API
- No clear legal basis for access → do not proceed

## IP Rotation Strategies

### Proxy Pool Architecture

```
┌────────────┐     ┌──────────────────┐     ┌─────────────┐
│  Worker     │────▶│  Proxy Gateway   │────▶│  Target     │
│  (Fetcher)  │     │  (IP Selection)  │     │  Website    │
└────────────┘     └──────┬───────────┘     └─────────────┘
                          │
              ┌───────────┼───────────┐
              │           │           │
        ┌─────▼─────┐ ┌──▼──────┐ ┌──▼──────┐
        │Residential │ │Datacenter│ │Egress   │
        │Proxy Pool  │ │Proxy Pool│ │Gateway  │
        └───────────┘ └─────────┘ └─────────┘
```

### Proxy Type Comparison

| Type | Cost/GB | Block Rate | Speed | Best For |
|------|---------|------------|-------|----------|
| Datacenter | $0.5-2 | High (20-40%) | Fast | Low-protection targets, high volume |
| Residential | $5-15 | Low (2-5%) | Medium | High-protection targets, critical data |
| Mobile | $15-30 | Very low (< 1%) | Variable | Maximum stealth, limited volume |
| ISP (static residential) | $3-8 | Low (5-10%) | Fast | Session persistence needed |
| Egress gateway rotation | Infra cost | Medium | Fast | Own infrastructure, predictable cost |

### IP Rotation Strategies

| Strategy | Implementation | Suitable For |
|----------|---------------|-------------|
| Per-request rotation | New IP every request | High-volume, no session |
| Per-session rotation | New IP every N requests or T minutes | Session-based crawling |
| Per-domain rotation | Sticky IP per domain, rotate on block | Domain affinity crawling |
| Geo-targeted | Match proxy location to target locale | Region-specific content |
| Reputation-based | Track IP success rate, retire low performers | Long-running crawls |

## User-Agent Management

### Pool Design

```
Requirements:
- 50-200 realistic User-Agent strings
- Weighted by actual browser market share
- Updated quarterly (browser versions change)
- Rotation: per-session (not per-request — consistent UA within a session)

Example distribution (Q1 2025 approximation):
  Chrome 120-124 (Windows 10/11): 45%
  Chrome 120-124 (macOS): 15%
  Safari 17.x (macOS): 12%
  Firefox 120-124 (Windows/Linux): 10%
  Edge 120-124 (Windows): 8%
  Chrome Mobile (Android): 7%
  Safari Mobile (iOS): 3%

Anti-pattern: DO NOT use bot-like UAs (e.g., "Python-urllib/3.11")
Best practice: Include realistic Accept, Accept-Language, Accept-Encoding headers
```

## TLS Fingerprint Diversification

### JA3/JA4 Fingerprinting

```
What it detects:
  TLS Client Hello → cipher suites, extensions, supported groups, signature algorithms
  Each TLS library has a distinctive fingerprint:
  - Python requests (urllib3): distinct JA3 hash
  - Go net/http: distinct JA3 hash
  - Chrome browser: distinct JA3 hash

Mitigation strategies:
1. curl-impersonate: Mimics Chrome/Firefox TLS fingerprints
2. Playwright/Puppeteer: Real browser TLS stack
3. utls (Go): Customizable TLS fingerprint
4. Custom cipher suite ordering: Match target browser profile

Decision: If target uses JA3 fingerprinting (Cloudflare, Akamai), use
curl-impersonate or browser-based fetching. Otherwise, standard TLS is fine.
```

## Timing Models

### Inter-Request Delay Design

| Model | Formula | Realism | Complexity |
|-------|---------|---------|------------|
| Fixed delay | delay = constant | Poor (detectable) | Low |
| Uniform random | delay = uniform(min, max) | Fair | Low |
| Gaussian jitter | delay = max(floor, N(μ, σ)) where μ = crawl_delay, σ = 0.3μ | Good | Medium |
| Pareto distribution | delay = pareto(α=1.5, x_m=crawl_delay) | Excellent (human-like) | Medium |
| Session-aware | Short bursts (2-5 pages) + longer pauses (10-30s) | Excellent | High |

**Recommended default:** Gaussian jitter with μ = Crawl-Delay (or 1s), σ = 30% of μ, floor = 0.5s.

### Behavioral Pattern Avoidance

```
Anti-patterns (detectable by sophisticated systems):
✗ Alphabetical URL crawling within a domain
✗ Perfectly sequential page numbers
✗ Constant request interval
✗ No referrer headers
✗ Unrealistic session depth (1000 pages without pause)

Best practices:
✓ Randomize URL order within domain queue
✓ Vary session depth (5-50 pages per "session")
✓ Include realistic referrer chains
✓ Simulate "reading time" (longer delay for content pages)
✓ Occasionally re-visit previously seen pages (human browsing pattern)
```

## CAPTCHA Escalation Path

```
CAPTCHA encounter decision flow:

1. CAPTCHA detected?
   ├── No → Continue crawling
   └── Yes → Classify type
        ├── Simple (image text) → Flag for review, DO NOT auto-solve
        ├── reCAPTCHA v2/v3 → Pause domain, rotate proxy, retry after cooldown
        ├── hCaptcha → Pause domain, reduce crawl rate, retry in 1 hour
        └── Custom/unknown → Block domain, log, escalate to human

IMPORTANT: Never design automated CAPTCHA solving as a primary path.
Acceptable responses:
- Reduce crawl rate for that domain
- Rotate to different proxy
- Pause and retry after cooldown period
- Escalate to human operator for decision
- Accept data loss for that domain
```

## Detection Risk Assessment

| Indicator | Risk Level | Mitigation |
|-----------|-----------|------------|
| High request rate from single IP | High | IP rotation, rate limiting |
| Bot-like User-Agent | High | Realistic UA pool |
| Missing browser headers | Medium | Full header simulation |
| TLS fingerprint mismatch | Medium | curl-impersonate / browser |
| Sequential URL patterns | Medium | Randomized crawl order |
| No JavaScript execution | Low-Medium | Browser-based fetching for JS-heavy sites |
| Unusual access times | Low | Schedule during business hours |
| Missing cookie handling | Low | Session-aware cookie jar |
