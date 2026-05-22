# Output Manifest

**Purpose:** Manifest schema, directory layout, report templates, audit format for Haul deliverables.
**Read when:** You are in `INTAKE` (set up batch dir), `CURATE` (write manifest and reports), or `audit` recipe.

## Contents

- Directory Layout
- Manifest Schema (`manifest.json`)
- Match Report Template
- Quality Report Template
- License Report Template
- Failures Report Template
- Audit Report Template

---

## Directory Layout

```
.haul/
└── {batch-id}/                          # e.g., haul-20260522-1432
    ├── manifest.json                    # Primary deliverable: per-image metadata
    ├── batch-config.json                # Run parameters (sources, thresholds, recipe)
    ├── images/                          # Final delivered images
    │   └── {product-key}/               # product-key = SKU / JAN / ASIN / slug
    │       ├── primary.{ext}
    │       ├── alt-1.{ext}
    │       ├── alt-2.{ext}
    │       └── ...
    ├── tos/                             # ToS snapshots at fetch time
    │   ├── {source-domain}.html
    │   └── {source-domain}.meta.json    # Retrieved-at, version
    ├── raw-{source}/                    # Per-source raw downloads (skill-internal subagents)
    │   └── {product-key}/
    │       └── candidate-{n}.{ext}
    ├── restricted/                      # Take-down placeholders (no image content)
    │   └── {product-key}.json
    └── reports/
        ├── match-report.md
        ├── quality-report.md
        ├── license-report.md
        ├── failures.md
        └── audit-report.md              # Only when `audit` recipe is run
```

`product-key` precedence: SKU (if unique within batch) > JAN / EAN / UPC > ASIN > sanitized product name slug.

---

## Manifest Schema (`manifest.json`)

```json
{
  "$schema": "https://example.com/haul/manifest-v1.json",
  "batch_id": "haul-20260522-1432",
  "recipe": "catalog",
  "started_at": "2026-05-22T05:32:00Z",
  "finished_at": "2026-05-22T05:48:12Z",
  "config": {
    "sources_allowlist": ["amazon-creators-api", "rakuten-ichiba-openapi", "manufacturer-canonical", "brave-search-image"],
    "resolution_floor": 800,
    "blur_threshold": 100,
    "match_floor_auto_accept": 0.85,
    "match_floor_review": 0.70,
    "phash_dedup_distance": 5,
    "embedding_model": "siglip2",
    "license_scope": "marketplace-licensed",
    "use_case": "internal_catalog",
    "regulatory_baseline": "eu-ai-act-pre-enforcement-2026-05"
  },
  "summary": {
    "products_requested": 120,
    "products_delivered": 117,
    "products_flagged": 8,
    "products_rejected": 3,
    "images_total": 348,
    "auto_accepted": 312,
    "review_band": 26,
    "rejected_low_confidence": 10,
    "dedup_collisions": 47,
    "license_breakdown": {
      "canonical": 89,
      "marketplace-licensed": 251,
      "fair-use": 0,
      "creative-commons": 0,
      "unknown": 8,
      "restricted": 0
    }
  },
  "products": [
    {
      "product_key": "B0XXXXXXX",
      "input": {
        "name": "Sony WH-1000XM5 Wireless Headphones — Black",
        "identifiers": {
          "asin": "B0XXXXXXX",
          "jan": "4548736134256",
          "mpn": "WH-1000XM5/B"
        },
        "schema_attributes": {
          "brand": "Sony",
          "model": "WH-1000XM5",
          "color": "Black"
        }
      },
      "delivered": [
        {
          "role": "primary",
          "file_path": "images/B0XXXXXXX/primary.jpg",
          "source_url": "https://m.media-amazon.com/images/I/61abcdef.jpg",
          "source_tier": "T1",
          "source_id": "amazon-creators-api",
          "fetch_timestamp": "2026-05-22T05:33:14Z",
          "dimensions": { "width": 2000, "height": 2000 },
          "file_size_bytes": 412338,
          "format": "jpeg",
          "color_profile": "sRGB",
          "sha256": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
          "phash": "ffb4c3a1d9e6f2b8",
          "dhash": "8a9d3c6f2b1e4a7d",
          "match": {
            "score": 0.94,
            "basis": "identifier+text",
            "identifier_score": 1.0,
            "text_score": 0.91,
            "visual_score": 0.85,
            "verdict": "auto_accepted"
          },
          "quality": {
            "longest_side": 2000,
            "blur_variance": 215,
            "watermark_class": "none",
            "aspect_ratio": 1.0,
            "border_uniformity": 0.92,
            "verdict": "passed"
          },
          "license": {
            "class": "marketplace-licensed",
            "evidence": "Amazon Creators API Operating Agreement (PA-API 5.0 retired 2026-05-15)",
            "tos_snapshot_path": "tos/amazon.com.html",
            "optout_signals": {
              "robots_txt": null,
              "ai_txt": null,
              "tdm_reservation": null,
              "meta_robots": null,
              "x_robots_tag": null
            },
            "attribution_required": true,
            "attribution_text": "Image courtesy of Amazon.com"
          },
          "alternates": [
            {
              "source_url": "https://www.sony.jp/products/.../primary.jpg",
              "source_tier": "T0",
              "phash": "ffb4c3a1d9e6f2b8",
              "hamming_distance": 0,
              "skipped_reason": "byte-identical to primary; T0 tier ranked equal but T1 had higher resolution metadata"
            }
          ]
        },
        {
          "role": "alt-1",
          "file_path": "images/B0XXXXXXX/alt-1.jpg",
          "source_url": "https://m.media-amazon.com/images/I/61abcdef-side.jpg",
          "source_tier": "T1",
          "source_id": "amazon-creators-api",
          "fetch_timestamp": "2026-05-22T05:33:18Z",
          "dimensions": { "width": 2000, "height": 2000 },
          "match": { "score": 0.89, "basis": "visual+text", "verdict": "auto_accepted" },
          "quality": { "verdict": "passed" },
          "license": { "class": "marketplace-licensed", "evidence": "Amazon Creators API Operating Agreement" }
        }
      ],
      "status": "delivered",
      "notes": "Primary and 2 alternates from Creators API (post-PA-API-retirement). Sony canonical CDN serves byte-identical primary."
    }
  ]
}
```

### Required Fields per Image

Per the Core Contract, every image entry must include:

- `source_url`, `source_tier`, `source_id`
- `fetch_timestamp` (ISO 8601 UTC)
- `dimensions`, `file_size_bytes`, `format`, `color_profile`
- `sha256`, `phash`
- `match.score`, `match.basis`, `match.verdict`
- `quality.verdict`
- `license.class`, `license.evidence`, `license.tos_snapshot_path`, `license.optout_signals`

Missing any required field blocks delivery.

---

## Match Report Template (`reports/match-report.md`)

```markdown
# Match Report — {batch-id}

**Run:** {start} → {finish}
**Recipe:** {recipe}

## Summary

| Verdict | Count | % of total |
|---------|-------|-----------|
| auto_accepted (score ≥ 0.85) | 312 | 89.7% |
| review_band (0.70-0.85) | 26 | 7.5% |
| rejected (< 0.70) | 10 | 2.9% |
| total | 348 | 100% |

## Score Distribution

| Score range | Count |
|-------------|-------|
| ≥ 0.95 | 198 |
| 0.85-0.95 | 114 |
| 0.70-0.85 | 26 |
| 0.50-0.70 | 7 |
| < 0.50 | 3 |

## Match Basis Breakdown

| Basis | Count |
|-------|-------|
| identifier-only (1.0 deterministic) | 211 |
| identifier + text | 87 |
| identifier + visual | 14 |
| text + visual | 26 |
| visual-only fallback | 0 |

## Review Band Items (manual review required)

| Product Key | Score | Basis | Source | Note |
|-------------|-------|-------|--------|------|
| B0YYYYYYY | 0.78 | text+visual | rakuten-ichiba | Bundle qualifier mismatch (listing was `3-piece set`, requested single-unit) |
| B0ZZZZZZZ | 0.74 | text+visual | google-cse | Color attribute ambiguity |
| ... | ... | ... | ... | ... |

## Rejected Items

| Product Key | Top Score | Reason |
|-------------|-----------|--------|
| B0AAAAAAA | 0.62 | All sources returned generic stock imagery; no anchor verification |
| ... | ... | ... |
```

---

## Quality Report Template (`reports/quality-report.md`)

See `quality-validation.md` for the full schema. Summary template:

```markdown
# Quality Report — {batch-id}

## Summary

| Metric | Value |
|--------|-------|
| Total images evaluated | 348 |
| Passed all gates | 331 |
| Flagged | 12 |
| Rejected | 5 |
| Cross-source dedup collisions | 47 |

## Gate Failure Breakdown

| Gate | Failures | Notes |
|------|----------|-------|
| G1 Format integrity | 1 | Truncated JPEG; alternate source used |
| G2 Resolution | 2 | Below 800px; rejected |
| G3 Blur | 5 | Borderline 80-100; flagged |
| G4 Watermark | 4 | Marketplace overlay; flagged |
| G5 Aspect ratio | 3 | Outside [0.5, 2.0]; flagged |
| G6 Border / padding | 0 | — |
| G7 Color profile | 12 | Non-sRGB converted |
| G8 Cross-source dedup | 47 | Resolved by tier preference |

## Resolution Distribution

| Longest side | Count |
|---|---|
| < 800 | 0 |
| 800-1199 | 89 |
| 1200-1999 | 102 |
| ≥ 2000 | 140 |
```

---

## License Report Template (`reports/license-report.md`)

```markdown
# License Report — {batch-id}

## Class Breakdown

| Class | Count | Permissible Use Verified? |
|-------|-------|---------------------------|
| canonical | 89 | yes |
| marketplace-licensed | 251 | yes |
| partner-grant | 0 | n/a |
| fair-use | 0 | n/a |
| creative-commons | 0 | n/a |
| unknown | 8 | flagged |
| restricted | 0 | n/a |

## Per-Source ToS Snapshots

| Source | ToS retrieved at | Path |
|--------|------------------|------|
| amazon.com | 2026-05-22T05:32Z | tos/amazon.com.html |
| rakuten.co.jp | 2026-05-22T05:32Z | tos/rakuten.co.jp.html |
| sony.jp | 2026-05-22T05:32Z | tos/sony.jp.html |

## Opt-Out Signal Surface

Re-evaluated at every batch start (6h cache TTL; aligns with EU AI Act 2026-08-02 enforcement readiness).

| Source | robots.txt | ai.txt | TDM-rep | meta-robots | X-Robots-Tag |
|--------|------------|--------|---------|-------------|--------------|
| amazon.com | allow | n/a | n/a | n/a | n/a |
| rakuten.co.jp | allow | n/a | n/a | n/a | n/a |
| sony.jp | allow `/products/`; disallow `/news/` | n/a | n/a | n/a | n/a |

## Unknown-Class Items (require user decision)

| Product Key | Source | Reason class is unknown |
|-------------|--------|--------------------------|
| B0AAAAAAA | google-cse | Source attribution chain incomplete |
| ... | ... | ... |
```

---

## Failures Report Template (`reports/failures.md`)

```markdown
# Failures Report — {batch-id}

This file is structured for resumable recovery. Re-running with the `refresh` recipe
will retry only items listed here.

## Per-Product Failures

### B0AAAAAAA — Sony XYZ Speaker

- **Status:** rejected
- **Attempts:**
  - amazon-paapi: 200 OK, score 0.62 (text+visual only, identifier mismatch)
  - rakuten-ichiba: 404 Not Found
  - sony.jp: robots.txt disallows `/discontinued/` path
  - google-cse: returned generic stock imagery, no anchor verification
- **Recovery hint:** Item appears discontinued. Verify whether to source archived imagery from Wayback Machine (license unclear) or accept exclusion.

### B0BBBBBBB — Acme Widget

- **Status:** flagged
- **Attempts:**
  - shopify-storefront: 429 Throttled, retried with backoff, succeeded; score 0.79 (review band)
- **Recovery hint:** Single source in review band. Add manufacturer canonical to allowlist or accept manual review.
```

---

## Audit Report Template (`reports/audit-report.md`)

Generated only when the `audit` recipe runs.

```markdown
# Audit Report — {batch-id} (audited at {audit-timestamp})

## Manifest Integrity

| Check | Result |
|-------|--------|
| Total images in manifest | 348 |
| Files present on disk | 348 |
| SHA-256 matches | 346 |
| SHA-256 mismatches | 2 |
| pHash recomputed and matches | 348 |

## License Re-classification

| Original class | Re-classified | Count | Action |
|----------------|---------------|-------|--------|
| canonical | canonical | 87 | none |
| canonical | marketplace-licensed | 2 | downgrade — note in report |
| marketplace-licensed | marketplace-licensed | 251 | none |
| unknown | restricted | 1 | take-down detected; remove from delivery |

## SHA-256 Mismatches (require investigation)

| Product Key | Role | Original SHA | Current SHA | Likely cause |
|-------------|------|--------------|-------------|--------------|
| B0CCCCCCC | primary | abc... | def... | File replaced after delivery; verify provenance |
| ... | ... | ... | ... | ... |

## Take-Down Detections

| Product Key | Source | Detected at | Action |
|-------------|--------|-------------|--------|
| B0DDDDDDD | sony.jp | 2026-04-27T05:32Z | Source returns 410 Gone; mark restricted |

## Recommended Actions

- Re-run `refresh` recipe for items with downgraded license classification.
- Remove `restricted` items from all downstream consumers (Showcase, Funnel, ...).
- Verify SHA-256 mismatch root cause; re-fetch if accidental modification.
```

---

## Manifest Versioning

`manifest.json` includes `$schema` referencing the version. On schema migration:

| Version | Change |
|---------|--------|
| `v1` | Initial schema |
| Future: `v2` | Backwards-compatible additions only; breaking changes warrant new schema version |

Tooling reading manifests should branch on `$schema` URL to support multiple versions.
