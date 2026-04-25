# Responsive Derivation

Reference for Pixel's `responsive` recipe. Derive responsive breakpoints from a single-viewport mockup. All derived values are LOW confidence — designer review recommended.

> Derivation is inference, not extraction. Every breakpoint, fluid value, and reflow rule produced from a single mockup must be marked `/* LOW: derived from desktop, verify */`.

---

## 1. Standard Breakpoint Set

| Breakpoint | Min width | Typical device | Container max |
|---|---|---|---|
| Mobile (default) | 0 | Phones | 100% - 32px |
| Tablet | 768px | Tablets, large phones landscape | 720px |
| Laptop | 1024px | Laptops, small desktops | 960px |
| Desktop | 1440px | Standard desktops | 1280px |
| Wide | 1920px | Wide monitors (rare) | 1536px |

Use these unless the mockup explicitly demands custom breakpoints (e.g., dashboard with sidebar at 1280px).

---

## 2. Mobile-First Reflow Rules

### Section ordering
- Mobile: linear vertical stack
- Tablet: 2-column grids start (cards, features)
- Desktop: 3-4 column grids, sidebar layouts

### Common reflow patterns

| Desktop | Mobile reflow |
|---|---|
| Horizontal nav | Hamburger menu + drawer |
| 3-column hero (image + text + form) | Stack: text → image → form |
| Sidebar + content | Content full-width, sidebar collapsed/below |
| Multi-column footer | Stacked sections, accordion if dense |
| Inline form fields | Stacked fields, full-width inputs |
| Hover-revealed nav | Tap-toggle dropdown |

### Touch-first adjustments
- Buttons → ≥ 44px height
- Form inputs → ≥ 44px height + 16px font (prevents iOS zoom)
- Tap targets ≥ 8px spacing
- Hover-only effects → tap-or-focus equivalents

---

## 3. Fluid Typography (clamp)

### Formula
```css
font-size: clamp(MIN, BASE + VW-DELTA, MAX);
```

Where:
- MIN = mobile size (e.g., `1rem`)
- MAX = desktop size (e.g., `1.5rem`)
- VW-DELTA = `calc(MIN_REM + (MAX - MIN) * ((100vw - MIN_VW) / (MAX_VW - MIN_VW)))`

### Simple linear interpolation example
Desktop H1 = 48px, Mobile H1 = 32px, range 320-1440px:
```css
:root {
  --fs-h1: clamp(2rem, 1.71rem + 1.43vw, 3rem);
  /* min 32px @ 320px, max 48px @ 1440px */
}
```

### Quick scale (8-step type system)
```css
:root {
  --fs-xs:   clamp(0.75rem, 0.71rem + 0.18vw, 0.875rem);  /* 12-14 */
  --fs-sm:   clamp(0.875rem, 0.84rem + 0.18vw, 1rem);     /* 14-16 */
  --fs-base: clamp(1rem, 0.96rem + 0.18vw, 1.125rem);     /* 16-18 */
  --fs-lg:   clamp(1.125rem, 1.07rem + 0.27vw, 1.25rem);  /* 18-20 */
  --fs-xl:   clamp(1.25rem, 1.16rem + 0.45vw, 1.5rem);    /* 20-24 */
  --fs-2xl:  clamp(1.5rem, 1.34rem + 0.80vw, 2rem);       /* 24-32 */
  --fs-3xl:  clamp(2rem, 1.71rem + 1.43vw, 3rem);         /* 32-48 */
  --fs-4xl:  clamp(2.5rem, 2.05rem + 2.23vw, 4rem);       /* 40-64 */
}
```

### Fluid spacing
```css
:root {
  --space-section: clamp(3rem, 2.4rem + 3vw, 6rem);   /* 48-96 */
  --space-block:   clamp(1.5rem, 1.2rem + 1.5vw, 3rem); /* 24-48 */
  --gap-grid:      clamp(1rem, 0.8rem + 1vw, 2rem);     /* 16-32 */
}
```

---

## 4. Container Queries vs Media Queries

| Use case | Choose | Why |
|---|---|---|
| Page-level layout (header / sidebar / footer) | `@media` | Tied to viewport |
| Component used in multiple slots (card, sidebar widget) | `@container` | Responds to parent width |
| User preferences (`prefers-color-scheme`, `prefers-reduced-motion`) | `@media` | Only available there |
| Print | `@media print` | Only available there |
| Modal / dialog responsive content | `@container` | Modal width varies by trigger |

### Container query example
```css
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

.card {
  display: grid;
  grid-template-columns: 1fr;
}

@container card (min-width: 400px) {
  .card { grid-template-columns: 1fr 2fr; }
}

@container card (min-width: 600px) {
  .card { grid-template-columns: auto 1fr auto; }
}
```

### When NOT to use container queries
- Page-level layout that depends on viewport
- More than 3 levels of nested containers (browser overhead)
- When unnamed query would match wrong ancestor

---

## 5. Component Reflow Patterns

### Hero
```css
.hero {
  display: grid;
  gap: var(--space-block);
  grid-template-columns: 1fr;  /* mobile */
}

@media (min-width: 768px) {
  .hero {
    grid-template-columns: 1fr 1fr;  /* tablet+ */
    align-items: center;
  }
}
```

### Card grid (container-aware)
```css
.card-grid {
  container-type: inline-size;
  display: grid;
  gap: var(--gap-grid);
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 280px), 1fr));
}
/* Auto-reflows: 1col < 280, 2col < 580, 3col < 880, etc. */
```

### Navigation
```css
.nav-links {
  display: none;  /* mobile: hidden, drawer instead */
}
.nav-toggle {
  display: block;
}

@media (min-width: 768px) {
  .nav-links { display: flex; gap: var(--gap-grid); }
  .nav-toggle { display: none; }
}
```

---

## 6. Aspect Ratio & Image Handling

### Modern aspect-ratio
```css
.hero-image {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
}

@media (min-width: 768px) {
  .hero-image { aspect-ratio: 21 / 9; }  /* wider on desktop */
}
```

### Art-direction with `<picture>`
```html
<picture>
  <source media="(min-width: 1024px)" srcset="hero-wide.webp">
  <source media="(min-width: 768px)" srcset="hero-tablet.webp">
  <img src="hero-mobile.webp" alt="..." loading="eager">
</picture>
```

### Responsive images via srcset
```html
<img
  src="card-400.webp"
  srcset="card-400.webp 400w, card-800.webp 800w, card-1200.webp 1200w"
  sizes="(min-width: 1024px) 33vw, (min-width: 768px) 50vw, 100vw"
  alt="..."
  loading="lazy"
>
```

---

## 7. Common Pitfalls

| Pitfall | Avoidance |
|---|---|
| Designing only at desktop, scaling down | Mobile-first: start CSS without media queries |
| Fixed `px` font sizes | Use `rem` + `clamp` for fluid scaling |
| Single-breakpoint thinking (just `@media (min-width: 768px)`) | Test all standard breakpoints + intermediate widths |
| Hover-only interactions | Provide tap or focus alternative |
| `100vh` on iOS bounces with URL bar | Use `100dvh` |
| Sub-44px tap targets on touch devices | Enforce minimum size in mobile breakpoint |
| Container query without named container in nested layout | Always assign `container-name` |
| Hiding content via `display: none` instead of restructuring | Hidden content still loads but is unreachable to screen readers if `hidden` not used |
| Pixel values for fluid spacing | Use `clamp()` or `vw` units |
| Assuming 1440px is the widest viewport | Test 1920px+ for ultrawide users |

---

## 8. Decision Walkthrough Template

```
Mockup viewport: ___ x ___
Implied derived breakpoints (LOW confidence):
  Mobile:   0-767
  Tablet:   768-1023
  Laptop:   1024-1439
  Desktop:  1440+

Type scale strategy:
  □ 8-step fluid (xs/sm/base/lg/xl/2xl/3xl/4xl with clamp)
  □ Custom — list per-element clamps

Spacing strategy:
  □ Fluid section/block/gap tokens
  □ Static rem with @media overrides

Container queries (component-level):
  □ Cards
  □ Sidebar widgets
  □ Modal contents
  □ N/A

Per-component reflow:
  □ Hero (1-col → 2-col @ 768)
  □ Nav (hamburger ↔ inline @ 768)
  □ Card grid (auto-fill minmax)
  □ Sidebar (stacked → side @ 1024)
  □ Form (stacked → inline @ 768)

Image strategy:
  □ aspect-ratio + object-fit
  □ <picture> art direction
  □ srcset + sizes
  □ loading="lazy" below fold

Verification:
  □ Test at 320 / 375 / 768 / 1024 / 1280 / 1440 / 1920
  □ Touch target check at mobile widths
  □ All derived values marked LOW confidence
  □ Designer review for derived breakpoints
```

---

## 9. References
- MDN: CSS Container Queries, `clamp()`, `aspect-ratio`
- WCAG 2.5.5 Target Size (Level AAA)
- web.dev: Modern Responsive Design (Una Kravets)
- caniuse.com: container-type, dvh, aspect-ratio (all 95%+ baseline)
