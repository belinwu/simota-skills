# RTL / i18n Specification for Figma Make

Reference for Loom's `rtl` recipe. Document RTL-ready CSS using logical properties, locale-aware formatting via `Intl`, font-fallback chains for non-Latin scripts, and Make prompt recipes for bidirectional UI.

---

## 1. Logical CSS Properties (Mandatory)

Replace **all** physical properties with logical equivalents. Make follows the convention if Guidelines.md mandates it.

| Physical | Logical |
|---|---|
| `margin-left` / `margin-right` | `margin-inline-start` / `margin-inline-end` |
| `margin-top` / `margin-bottom` | `margin-block-start` / `margin-block-end` |
| `padding-left` / `padding-right` | `padding-inline-start` / `padding-inline-end` |
| `border-left` | `border-inline-start` |
| `left` / `right` | `inset-inline-start` / `inset-inline-end` |
| `text-align: left` | `text-align: start` |
| `float: left` | `float: inline-start` |
| `width` / `height` | `inline-size` / `block-size` |
| `min-width` | `min-inline-size` |
| `border-radius: 4px 0 0 4px` | `border-start-start-radius: 4px` (and `border-end-start-radius`) |

Shorthand variants:
- `margin-inline: 1rem` (both inline sides)
- `margin-block: 1rem` (both block sides)
- `padding-inline: 1rem 2rem` (start, end)

**Result**: when `dir="rtl"` is applied, the entire layout mirrors automatically — no separate stylesheet.

---

## 2. `dir` Attribute Strategy

### Document-level
```html
<html lang="ar" dir="rtl">
```

### Component-level override (mixed-direction content)
```html
<p dir="ltr">User input was: <span dir="auto">{userText}</span></p>
```

Use `dir="auto"` for **user-generated content** of unknown direction — browser infers from first strong directional character.

### React pattern
```tsx
const dir = isRTL(locale) ? 'rtl' : 'ltr';
<html lang={locale} dir={dir}>
```

Where `isRTL` checks against `['ar', 'he', 'fa', 'ur']` (and locale subtags).

---

## 3. Mirror-Exempt Elements

Some elements should **not** mirror in RTL:

| Element | Reason |
|---|---|
| Phone numbers | Always LTR |
| Email addresses | Always LTR |
| URLs | Always LTR |
| Credit card numbers | Always LTR |
| Code snippets | Always LTR |
| Progress bars (left → right time) | Mirroring confuses time perception |
| Media players (play / pause) | Convention is LTR for transport controls |
| Brand logos | Original orientation |

Use `dir="ltr"` or `unicode-bidi: isolate` to lock direction:

```css
.phone-number { direction: ltr; unicode-bidi: isolate; }
```

Document mirror-exempt list in Guidelines.md `## RTL Exceptions`.

---

## 4. Icon Mirroring Decisions

| Icon | Mirror in RTL? |
|---|---|
| Arrow (back / forward / next / prev) | ✓ Yes |
| Chevron (breadcrumb separator) | ✓ Yes |
| Send / paper plane | ✓ Yes |
| Reply | ✓ Yes |
| Search (magnifying glass) | ✗ No |
| Settings (gear) | ✗ No |
| Notifications (bell) | ✗ No |
| Trash / delete | ✗ No |
| Play / pause | ✗ No |
| Speech bubble | ✓ Yes (tail mirrors) |

CSS pattern for mirrorable icons:
```css
[dir="rtl"] .icon-arrow,
[dir="rtl"] .icon-chevron,
[dir="rtl"] .icon-send {
  transform: scaleX(-1);
}
```

Or use logical icons in the asset library (`icon-arrow-start` resolves to left in LTR, right in RTL).

---

## 5. `Intl` Locale-Aware Formatting

Mandatory for numbers, dates, currency, lists, plurals.

### Numbers
```ts
new Intl.NumberFormat('ar-EG').format(1234567.89);
// "١٬٢٣٤٬٥٦٧٫٨٩"
```

### Currency
```ts
new Intl.NumberFormat('ja-JP', { style: 'currency', currency: 'JPY' }).format(1500);
// "￥1,500"
```

### Date / time
```ts
new Intl.DateTimeFormat('he-IL', { dateStyle: 'long', timeStyle: 'short' })
  .format(new Date());
// "‎21 באפריל 2026 בשעה 14:30"
```

Use **dateStyle / timeStyle** instead of manual format strings.

### Relative time
```ts
new Intl.RelativeTimeFormat('ar', { numeric: 'auto' }).format(-1, 'day');
// "أمس"
```

### Lists
```ts
new Intl.ListFormat('ja', { style: 'long', type: 'conjunction' })
  .format(['りんご', 'ばなな', 'みかん']);
// "りんご、ばなな、みかん"
```

### Plurals
```ts
const pr = new Intl.PluralRules('ru');
pr.select(2); // "few"
pr.select(5); // "many"
```

Pair with i18n library (i18next, FormatJS, lingui) — never hardcode plural branches.

---

## 6. Font Fallback Chains

Non-Latin scripts require explicit fallback. Latin-only fonts cause `.notdef` glyph (□).

```css
:root {
  --font-sans-latin: 'Inter', system-ui, sans-serif;
  --font-sans-arabic: 'Noto Sans Arabic', 'IBM Plex Sans Arabic', sans-serif;
  --font-sans-cjk-jp: 'Noto Sans JP', 'Hiragino Sans', 'Yu Gothic', sans-serif;
  --font-sans-cjk-sc: 'Noto Sans SC', 'PingFang SC', sans-serif;
  --font-sans-hebrew: 'Noto Sans Hebrew', 'Arial Hebrew', sans-serif;
}

:lang(ar) { font-family: var(--font-sans-arabic), var(--font-sans-latin); }
:lang(ja) { font-family: var(--font-sans-cjk-jp), var(--font-sans-latin); }
:lang(zh-CN) { font-family: var(--font-sans-cjk-sc), var(--font-sans-latin); }
:lang(he) { font-family: var(--font-sans-hebrew), var(--font-sans-latin); }
```

### Font loading
- `font-display: swap` for non-blocking render
- Preload critical script: `<link rel="preload" as="font" type="font/woff2" crossorigin>`
- Subset CJK fonts (Noto Sans JP full = ~10MB; subset to current page glyphs)

### Line-height adjustments
CJK and Arabic typically need looser line-height than Latin:
```css
:lang(ja), :lang(zh) { line-height: 1.7; }
:lang(ar) { line-height: 1.8; }
:lang(en) { line-height: 1.5; }
```

---

## 7. Layout Considerations

### Text expansion
Translation grows / shrinks text. Plan for:
- German: ~30% longer than English
- Russian: ~20% longer
- CJK: ~30% shorter (but each glyph is wider)
- Arabic: ~25% longer with diacritics

Don't fix widths on text containers; use `min-width` + `max-width` + flex/grid.

### Bidirectional text within sentences
```html
<p>The order ID is <span dir="ltr">#A1B2-1234</span> for شحن البضائع</p>
```

Use `<span dir="ltr">` for LTR substrings inside RTL paragraphs (and vice versa).

### Form input alignment
```css
input[type="email"], input[type="tel"], input[type="url"] {
  direction: ltr;  /* Always LTR for these inputs */
  text-align: start;  /* But align according to document direction */
}
```

---

## 8. Make Prompt Recipes

### Recipe: enable RTL-ready layout
```
Use logical CSS properties throughout: margin-inline, padding-inline,
inset-inline, text-align: start. No physical left/right properties.
Test with dir="rtl" on the root container.
```

### Recipe: mirror navigation icons
```
Generate Breadcrumb component. Chevron separator must mirror in RTL:
add CSS rule [dir="rtl"] .breadcrumb-separator { transform: scaleX(-1); }
```

### Recipe: locale-aware formatting
```
Display price using new Intl.NumberFormat(locale, {
  style: 'currency', currency: 'JPY'
}).format(price). Pass locale as prop. Default locale: 'ja-JP'.
```

### Recipe: bidirectional text
```
For mixed Arabic + English text, wrap LTR substrings in <span dir="ltr">.
Use unicode-bidi: isolate for phone numbers, emails, codes.
```

---

## 9. Verification

After generation, verify in both LTR and RTL:

| Check | LTR | RTL |
|---|---|---|
| Layout mirrors completely | n/a | ✓ |
| Icons mirror correctly (arrows, chevrons) | n/a | ✓ |
| Mirror-exempt elements stay LTR (phone, code) | ✓ | ✓ |
| Numbers render in correct numeral system | ✓ | ✓ |
| Date format matches locale convention | ✓ | ✓ |
| Currency symbol position correct (¥1,000 vs 1.000 €) | ✓ | ✓ |
| Font fallback chain renders all glyphs (no □) | ✓ | ✓ |
| Text expansion doesn't overflow containers | ✓ | ✓ |
| Form inputs (email, tel) stay LTR | ✓ | ✓ |
| Focus order follows visual order | ✓ | ✓ |

Test with Arabic / Hebrew / Japanese / Russian locales minimum.

---

## 10. Common Pitfalls

| Pitfall | Avoidance |
|---|---|
| Hardcoded `margin-left` / `padding-right` | Use `margin-inline-start` / `padding-inline-end` |
| `text-align: left` instead of `start` | Always use logical alignment |
| Arrow icons not mirrored in RTL | Add `[dir="rtl"] transform: scaleX(-1)` rule |
| Phone numbers / codes mirrored | Wrap with `dir="ltr"` + `unicode-bidi: isolate` |
| Hardcoded date format (`MM/DD/YYYY`) | Use `Intl.DateTimeFormat` with locale |
| String concatenation for plurals | Use `Intl.PluralRules` + i18n library |
| Latin-only font causes `.notdef` for CJK | Per-language fallback chain via `:lang()` |
| Translated text overflows fixed-width container | Use min/max-width + flex/grid; allow text growth |
| `transform: translateX(20px)` doesn't flip in RTL | Use `transform: translateX(20px)` won't auto-flip; use logical equivalent or RTL override |
| Ignoring `lang` attribute | Set on `<html>`; use `:lang()` selectors |

---

## 11. Decision Walkthrough Template

```
Component: ____________

CSS audit:
  □ All margin/padding use logical properties
  □ All inset/positioning use logical properties
  □ text-align uses start/end (not left/right)
  □ float uses inline-start/inline-end (or replaced with flex/grid)
  □ border-radius uses logical corners

Icons:
  □ Listed mirror / no-mirror decision per icon
  □ [dir="rtl"] override or logical icon variant

Bidirectional content:
  □ Phone / email / URL wrapped with dir="ltr"
  □ User-generated content uses dir="auto"

Locale formatting:
  □ Numbers: Intl.NumberFormat
  □ Dates: Intl.DateTimeFormat with dateStyle/timeStyle
  □ Currency: Intl.NumberFormat with style: 'currency'
  □ Lists: Intl.ListFormat
  □ Plurals: Intl.PluralRules + i18n library

Fonts:
  □ Per-language fallback chain via :lang()
  □ font-display: swap
  □ Subset large fonts (CJK)
  □ Line-height adjusted per script

Verification:
  □ Tested in LTR (en, ja)
  □ Tested in RTL (ar, he)
  □ Text expansion (de, ru) doesn't overflow
  □ All glyphs render (no □)

Guidelines.md sections:
  □ ## RTL Strategy (logical properties mandate)
  □ ## RTL Exceptions (mirror-exempt list)
  □ ## Icon Mirroring (per-icon table)
  □ ## i18n Formatting (Intl usage)
  □ ## Font Fallback Chains
```

---

## 12. References
- MDN CSS Logical Properties and Values
- W3C International — Inline markup and bidirectional text
- ECMA-402 Internationalization API
- Google Noto fonts (universal script coverage)
- Material Design Bidirectionality
- Apple HIG Right-to-Left
