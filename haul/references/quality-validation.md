# Quality Validation

**Purpose:** Resolution / blur / watermark checks, perceptual hashing, deduplication logic for product image quality assurance.
**Read when:** You are in `VERIFY` phase or designing the quality gate for a Recipe.

## Contents

- Quality Gates
- Resolution Validation
- Blur Detection
- Watermark Detection
- Aspect-Ratio Sanity
- Format Integrity
- Perceptual Hashing
- Cross-Source Deduplication
- Quality Failure Recovery

---

## Quality Gates

Apply gates in this order. Fail-fast: stop at the first failed gate and record reason.

| Gate | Check | Default threshold | On failure |
|------|-------|-------------------|------------|
| G1 | Format integrity | File parses as valid JPEG / PNG / WebP / AVIF | Reject |
| G2 | Resolution floor | Longest side `≥ 800px` (catalog) | Reject or flag |
| G3 | Blur | Laplacian variance `≥ 100` | Reject or flag |
| G4 | Watermark presence | No detected watermark | Flag (do not auto-reject) |
| G5 | Aspect-ratio sanity | `0.25 ≤ width/height ≤ 4.0` | Flag |
| G6 | Border / padding | Non-trivial product area `≥ 60%` of frame | Flag |
| G7 | Color profile | sRGB or convertible | Convert and proceed |
| G8 | Perceptual dedup (cross-source) | Hamming distance `> 5` from accepted set | Dedupe (keep best) |

---

## Resolution Validation

| Use case | Longest side floor | Notes |
|----------|---------------------|-------|
| Catalog (default) | `800px` | Sufficient for grid views and product cards |
| Hero / LP imagery | `1200px` | Required for above-the-fold display |
| Print / PR | `2000px` | Required for print at 300dpi up to ~6 inches |
| Thumbnail-only | `400px` | Acceptable when only listing thumbnails are needed |
| Storybook / fixture | `600px` | Sufficient for component preview |

Compute longest side from the actual decoded image dimensions, not declared metadata. Some sources misreport dimensions in EXIF.

### Upscaling Refusal

Never upscale to meet the floor. Upscaled images carry the source resolution as metadata and should fail. Re-fetch from a higher-resolution source URL pattern (many CDNs accept size suffixes like `_800x800` → `_2000x2000`).

---

## Blur Detection

Laplacian variance is the standard metric. Higher variance = sharper image.

| Variance range | Verdict | Action |
|----------------|---------|--------|
| `≥ 200` | Sharp | Accept |
| `100 - 200` | Acceptable | Accept |
| `60 - 100` | Borderline | Flag for review |
| `< 60` | Blurry | Reject |

```
gray = grayscale(image)
laplacian = cv2.Laplacian(gray, cv2.CV_64F)
variance = laplacian.var()
```

### Domain-Specific Calibration

| Domain | Adjustment | Reason |
|--------|-----------|--------|
| Apparel (textured fabric) | Lower floor to `80` | Fabric texture appears low-variance but is sharp |
| Glossy / metallic | Higher floor to `150` | Reflective surfaces require high sharpness for product detail |
| Soft-focus product photography | Lower floor to `70` | Intentional shallow depth of field |

Record any per-domain calibration in the manifest's `quality_config` field.

---

## Watermark Detection

Watermarks indicate the image is licensed by a third party (stock photo agency, marketplace overlay, brand-protection service).

### Detection Methods

| Method | Detects | Notes |
|--------|---------|-------|
| OCR text presence | `Getty Images`, `Shutterstock`, `Adobe Stock`, `© [name]`, marketplace logos | Run OCR on full image and on edges separately |
| Repeating pattern | Tiled / diagonal watermark patterns | FFT-based periodicity detection |
| Edge-band content | Logo or text in a uniform band along an edge | Horizontal / vertical strip analysis |
| Alpha-channel watermark | Semi-transparent overlays | PNG alpha analysis |
| Known agency hash | Match against Getty / Shutterstock fingerprint set | Curated list, low recall but high precision |

### Action on Watermark

| Watermark class | Action |
|-----------------|--------|
| Stock-photo agency (Getty / Shutterstock / Adobe) | Reject — license required, not redistributable |
| Marketplace overlay (`Sold on Amazon` etc.) | Flag — listing image but may have alternate from canonical |
| Brand watermark (manufacturer-applied) | Accept if canonical T0 source — manufacturer-applied watermarks are part of the canonical asset |
| Anti-counterfeit watermark | Accept if T0 / T1 — typical on luxury / regulated products |
| User-applied watermark (review photos) | Reject |

**Never strip watermarks.** Removal is a copyright violation and a Boundaries Never rule.

---

## Aspect-Ratio Sanity

| Aspect | Range | Notes |
|--------|-------|-------|
| Standard product | `0.5 ≤ ratio ≤ 2.0` | Most catalog imagery falls here |
| Tall (apparel, bottles) | `0.4 ≤ ratio < 0.5` | Acceptable for known categories |
| Wide (panoramic, group shots) | `2.0 < ratio ≤ 4.0` | Acceptable for known categories |
| Outside `[0.25, 4.0]` | — | Reject — likely not a product image (banner / lifestyle / cropped) |

Aspect-ratio sanity is a heuristic, not a hard rule. Pair with category context.

---

## Format Integrity

| Check | Method |
|-------|--------|
| Parseable | Decode header + first scan; reject on parse error |
| Truncation | Decode full image; reject on truncation error |
| Color depth | `≥ 8 bits/channel` for delivery; convert if 1-bit / 4-bit |
| Color profile | Convert non-sRGB to sRGB for catalog use; record original profile in manifest |
| Animated formats | Animated GIF / WebP: extract canonical frame (frame 0 or longest-displayed); record |
| Progressive JPEG | Accept; many marketplaces use progressive |

---

## Perceptual Hashing

Perceptual hash fingerprints are stable under format conversion, resizing, and minor color shifts.

### pHash (DCT-based)

| Property | Value |
|----------|-------|
| Hash length | 64 bits |
| Hamming distance threshold (duplicate) | `≤ 5` |
| Hamming distance threshold (similar) | `≤ 10` |
| Resilient to | JPEG re-encoding, mild scaling, color profile swap |
| Sensitive to | Crop, rotation, mirroring |

```
gray = grayscale(image_resized_to_32x32)
dct = dct2(gray)
top8x8 = dct[:8, :8]
median = median(top8x8 except DC)
hash = bits where top8x8 > median
```

### dHash (difference hash)

| Property | Value |
|----------|-------|
| Hash length | 64 bits |
| Threshold (duplicate) | `≤ 8` |
| Resilient to | Slight crop / scaling |
| Sensitive to | Brightness shifts, gamma changes |

### When to Use Which

| Scenario | Recommended hash |
|----------|------------------|
| Cross-source dedup | pHash |
| Cropped variant detection | ORB / CLIP (pHash unreliable) |
| Same source, different size | pHash |
| Different angle / lighting | CLIP embedding |

---

## Cross-Source Deduplication

Run dedup pass after all candidates per product are downloaded.

### Algorithm

```
1. Compute pHash for every candidate.
2. Group candidates by pHash hamming distance ≤ 5 (union-find).
3. Within each group, select the keeper:
   a. Highest source tier (T0 > T1 > T2 > T3 > T4 > T5).
   b. Highest resolution.
   c. Lowest file size at equal resolution.
4. Mark non-keepers as duplicates; record alternate-source URLs in keeper's manifest entry.
5. Recompute manifest entries.
```

### Group Reporting

For every dedup group with size > 1, record:

```json
{
  "primary_url": "...",
  "primary_phash": "...",
  "duplicates": [
    {
      "url": "...",
      "phash": "...",
      "hamming_distance": 3,
      "source_tier": "T1",
      "reason_skipped": "lower tier than T0 keeper"
    }
  ]
}
```

### Identical-Bytes Detection

Before pHash dedup, run SHA-256 dedup. Many sources mirror the exact same file (e.g., Amazon → manufacturer CDN). Identical-bytes are deduped without computing pHash.

---

## Quality Failure Recovery

| Failure | Recovery |
|---------|----------|
| Resolution too low | Try higher-resolution URL pattern from same source (e.g., `_500x500` → `_2000x2000`); else try alternate source |
| Blur | Try alternate source; if all sources blurry, flag for review (may be a low-quality SKU) |
| Watermark (stock-photo class) | Reject; remove this URL from candidate set; try alternate source |
| Watermark (marketplace overlay) | Try canonical T0 source; if unavailable, accept with `marketplace_overlay` flag |
| Aspect-ratio outside range | Flag; check whether this is a banner / lifestyle and try alternate source |
| Format parse error | Retry download (transient); if persistent, route to alternate source |
| Persistent failure across all sources | Mark in `failures.md` with reason; surface to user for manual handling |

### Resumable Recovery

`failures.md` contains a structured per-product entry with the list of attempted sources and failure reasons. On `refresh` recipe, Haul reads this file, re-attempts only the failed entries, and updates the manifest.

---

## Quality Report Aggregation

End-of-batch summary:

```yaml
quality_summary:
  total_images: 248
  passed_all_gates: 231
  flagged: 12
    - reason: "blur borderline (variance 80-100)"  # count: 5
    - reason: "watermark marketplace overlay"      # count: 4
    - reason: "aspect-ratio outside standard"      # count: 3
  rejected: 5
    - reason: "resolution below floor"             # count: 2
    - reason: "stock-photo watermark"              # count: 2
    - reason: "format parse error after retry"     # count: 1
  dedup_collisions: 47  # cross-source duplicates resolved
  longest_side_distribution:
    "< 800": 0
    "800-1200": 89
    "1200-2000": 102
    ">= 2000": 40
```

This summary is written to `.haul/{batch-id}/reports/quality-report.md`.
