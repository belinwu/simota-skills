# Matching Precision

**Purpose:** Scoring formulas, identifier validation, fuzzy text matching, visual similarity thresholds for product image precision.
**Read when:** You are in `MATCH` phase and need to score / accept / reject candidates.

## Contents

- Match Score Formula
- Identifier Matching (Deterministic)
- Text Matching (Probabilistic)
- Visual Matching (Verification Layer)
- Confidence Bands & Actions
- Tie-Breaking
- Edge Cases

---

## Match Score Formula

A composite score in `[0.0, 1.0]`. Higher is better. Three layers, weighted:

```
score = w_id * identifier_score + w_text * text_score + w_visual * visual_score
```

Default weights:

| Layer | Weight | Rationale |
|-------|--------|-----------|
| `w_id` (identifier) | `0.50` | Deterministic; outweighs text and visual when present |
| `w_text` (text) | `0.30` | Probabilistic; high recall on names / brands / models |
| `w_visual` (visual) | `0.20` | Verification layer; resolves ambiguous matches |

**When identifier is unknown:** redistribute weight: `w_text = 0.60, w_visual = 0.40`. Visual cannot exceed `0.40` weight without identifier — it cannot anchor a match alone.

---

## Identifier Matching (Deterministic)

Before scoring, normalize and validate every identifier.

| Identifier | Format | Validation |
|------------|--------|------------|
| ASIN | 10 chars, alphanumeric, marketplace-scoped | Regex `^[A-Z0-9]{10}$`; verify against marketplace |
| JAN / EAN-13 | 13 digits | Check digit (mod-10 weighted); reject invalid |
| EAN-8 | 8 digits | Check digit (mod-10 weighted); reject invalid |
| UPC-A | 12 digits | Check digit (mod-10 weighted); reject invalid |
| GTIN-14 | 14 digits | Check digit (mod-10 weighted); reject invalid |
| ISBN-10 / 13 | 10 or 13 chars | Check digit (ISBN-10: mod-11; ISBN-13: mod-10) |
| MPN | Variable | No check digit; require manufacturer + MPN pair |
| SKU | Source-specific | No check digit; treat as marketplace-scoped |

### Identifier Score

```
identifier_score = 1.0 if validated_identifier_match
                  = 0.7 if check_digit_only_match (e.g., JAN matches but cross-source data differs)
                  = 0.0 if mismatch or absent
```

### Cross-Source Identifier Reconciliation

A product has multiple identifiers. Match across sources when at least one identifier maps:

```
JAN 4901234567894 (Rakuten)  ←→  ASIN B0XXXXXXX (Amazon, JAN field)  ←→  manufacturer SKU (T0)
```

When sources publish different identifiers (no shared key), fall back to text + visual.

### Check-Digit Algorithms

**JAN-13 / EAN-13 / UPC-A / GTIN-14 (mod-10 weighted):**

```
sum = 0
for i, digit in enumerate(digits[:-1]):
    weight = 3 if (length - 1 - i) % 2 == 1 else 1
    sum += digit * weight
check = (10 - sum % 10) % 10
valid = check == digits[-1]
```

**ISBN-10 (mod-11):** position-weighted sum mod 11 must equal the check digit (X = 10).

---

## Text Matching (Probabilistic)

Normalize and tokenize before comparison.

### Normalization

| Step | Action |
|------|--------|
| Unicode | NFKC normalize (Japanese full-width / half-width unification) |
| Case | Lowercase Latin characters |
| Whitespace | Collapse runs to single space; trim |
| Punctuation | Remove or replace with space (preserve `+`, `-`, `&` in product codes) |
| Brand alias | Apply alias map (e.g., `Apple` ↔ `Appuru` (katakana), `SONY` ↔ `Sonii` (katakana)) — store in alias dictionary keyed by canonical English form |
| Stop words | Remove generic terms (e.g., `product`, `official`, `New`, `2025`, and locale equivalents) when not part of model name |

### Tokenization

| Locale | Tokenizer | Notes |
|--------|-----------|-------|
| English / Latin | Whitespace + punctuation | Standard |
| Japanese | MeCab / Sudachi (morphological) | Mixed kana / kanji / katakana / latin in product names |
| Mixed (jp+en) | Japanese tokenizer + Latin word boundary | Common in Japan e-commerce |
| Number-heavy (model codes) | Preserve digit runs as tokens | `MX-Master-3S` → `MX`, `Master`, `3S` |

### Text Score

Combine three signals:

| Signal | Method | Weight |
|--------|--------|--------|
| Brand match | Exact / alias-mapped | `0.30` |
| Model name match | Token Jaccard or normalized Levenshtein | `0.40` |
| Attribute match | Color / size / capacity / variant token overlap | `0.30` |

```
text_score = 0.30 * brand_match + 0.40 * model_match + 0.30 * attribute_match
```

**Floor:** if brand mismatches, `text_score = 0.0` regardless of model / attribute match. Wrong brand is never a match.

### Locale-Specific Patterns

**Mixed-script product names (Japanese e-commerce typical)** often include: brand (English or katakana) + model (English) + size/color (locale terms) + bundle qualifiers (e.g., `set`, `single-unit`, `gift`).

Example (transliterated): `Sonii WH-1000XM5 wairesu noizukyanseringu heddohon burakku` (original mixes katakana + English).

Tokens: [`Sonii`/`SONY` brand], [`WH-1000XM5` model], [`wireless`, `noise-cancelling`, `headphones` category], [`black` color].

Match against schema: brand → SONY; model → WH-1000XM5; color → black. Bundle qualifiers (e.g., `single-unit`) are normalized away unless they distinguish a SKU.

---

## Visual Matching (Verification Layer)

Visual matching verifies — it does not anchor. Use to resolve ambiguous text matches and reject visually divergent candidates.

### Methods

| Method | Speed | Use case | Threshold (similar) |
|--------|-------|----------|---------------------|
| pHash (perceptual hash) | Fast | Near-duplicate detection across sources | Hamming distance `≤ 5` |
| dHash | Fast | Cropped / scaled variants | Hamming distance `≤ 8` |
| ORB feature matching | Medium | Different crops / angles of same product | `≥ 30` matched keypoints |
| CLIP embedding cosine | Slow | Semantic similarity (same product class, possibly different SKU) | `cosine ≥ 0.85` |
| Domain-specific reference | Variable | Compare to known canonical T0 image | Per-method threshold |

### Visual Score

```
visual_score = 1.0 if pHash_distance ≤ 3 OR (clip_cosine ≥ 0.92 AND orb_match ≥ 50)
              = 0.7 if pHash_distance ≤ 5 OR clip_cosine ≥ 0.85
              = 0.4 if clip_cosine ≥ 0.75
              = 0.0 otherwise
```

### Reference Anchor

When a T0 canonical image is available, treat it as the reference anchor. Score every other candidate's visual similarity to the anchor. A candidate that diverges visually from the canonical anchor is rejected even if text / identifier match — anchor mismatch indicates the listing has wrong imagery.

---

## Confidence Bands & Actions

| Score range | Band | Action |
|-------------|------|--------|
| `≥ 0.85` | Auto-accept | Deliver to manifest, mark `auto_accepted` |
| `0.70 – 0.85` | Review | Flag in manifest, include in `match-report.md` for human review |
| `< 0.70` | Reject | Do not deliver; record in `failures.md` with reason |

**Override rules:**
- Identifier-only match with `identifier_score = 1.0` and matched canonical-source URL → auto-accept regardless of composite (deterministic identifier on canonical is the strongest signal).
- Visual divergence from anchor (`visual_score < 0.4` against T0 anchor) → reject regardless of identifier / text score (suggests wrong imagery on the listing, not wrong product).

---

## Tie-Breaking

When multiple candidates score `≥ 0.85` for the same product:

1. Highest tier (T0 > T1 > T2 > T3 > T4 > T5).
2. Highest resolution (longest side).
3. Most-recent fetch / publication date if available.
4. Canonical source URL (manufacturer over marketplace).
5. Lower file size at equal resolution (better compression / less noise).

Keep all tied candidates as `alt-N` images in the manifest; only one wins `primary`.

---

## Edge Cases

### Multi-pack / Bundle Listings

Listing image shows a 3-pack while requested SKU is single. Detect via:
- Title tokens: `multi-pack`, `bundle`, `set of N`, `pack of N`, locale equivalents (e.g., `N-piece set`, `N-pack`).
- Image: visual analysis of count (if CLIP / OCR available); count shown in image text overlays often does NOT appear in title — run OCR on candidate image when title lacks bundle qualifier.
- Schema field: prefer explicit `pack_size` from product schema when available — record on manifest entry.

Action: lower text_score by 0.3 if bundle qualifier mismatches the requested SKU. Prefer single-unit listings. If neither title tokens nor OCR can resolve pack size, flag for review (do not auto-accept). [F07 mitigation]

### Color / Variant Mismatch

Listing shows black but requested SKU is red. Detect via:
- Variant attribute in product schema.
- Dominant color extraction from candidate image vs requested color.

Action: if color-token mismatch and dominant color diverges, lower attribute match to 0. Prefer correct-color listings or per-variant CDN URL.

### Stock Photo / Lifestyle Image vs Product Photo

Lifestyle image (model holding product) vs studio shot. Both can be valid but:
- For catalog `primary`, prefer studio shot on white / neutral background.
- For LP / marketing, lifestyle may be preferred — pass via Recipe / parameter.

Detect via background uniformity (variance of border pixels). Studio shots have low border variance.

### OEM / Generic / Counterfeit Listings

Marketplace listings may show generic product image while selling counterfeit / unrelated item.
- Compare visual_score against T0 anchor — divergence indicates listing imagery is wrong.
- If T0 is unavailable, require ≥ 2 T1 sources with mutually-similar images (visual_score between candidates ≥ 0.85).

### Sparse Identifier Coverage

Some products lack JAN / UPC. Fall back to manufacturer + MPN as composite identifier. If none available, text + visual only with explicit user acknowledgement of reduced precision.

---

## Calibration

Default thresholds work for general commerce. Calibrate per domain:

| Domain | Adjustment |
|--------|-----------|
| Apparel | Visual threshold `+0.05` (color / pattern variance high); attribute weight `+0.10` |
| Books / Media | Identifier weight `+0.10` (ISBN definitive); visual weight `-0.10` |
| Electronics | Default weights work |
| Cosmetics | Visual threshold `+0.05` (packaging variants); brand match floor strict |
| Food / Grocery | JAN coverage high → identifier weight `+0.10` |
| Furniture / Large items | Visual weight `+0.05` (lifestyle vs studio variance high) |

Record any threshold override in the manifest's `match_config` field.
