# Responsive Strategies

**Purpose:** Mobile-first conversion patterns and breakpoint estimation for mockup reproduction.
**Read when:** You need to convert a static (typically desktop) mockup into responsive HTML/CSS.

## Contents
- Mobile-First Philosophy
- Breakpoint Estimation
- Section Conversion Patterns
- Responsive Typography
- Common Responsive Patterns

---

## Mobile-First Philosophy

When a mockup shows only a desktop viewport:
1. **Build mobile layout first** — single column, stacked elements.
2. **Add complexity at breakpoints** — multi-column, larger spacing, bigger type.
3. **Document assumptions** — since mobile view is not in the mockup, all mobile decisions are MEDIUM confidence at best.

```css
/* Mobile first: default styles are mobile */
.features__grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

/* Tablet: 2 columns */
@media (min-width: 48rem) {
  .features__grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop: match mockup */
@media (min-width: 64rem) {
  .features__grid {
    grid-template-columns: repeat(3, 1fr); /* HIGH: matches mockup */
  }
}
```

---

## Breakpoint Estimation

### Standard Breakpoints

When the mockup doesn't specify breakpoints, use these defaults:

| Name | Width | CSS | Confidence |
|------|-------|-----|------------|
| Mobile (base) | 0-639px | Default styles | HIGH (convention) |
| Tablet | 640px+ | `@media (min-width: 40rem)` | MEDIUM |
| Laptop | 1024px+ | `@media (min-width: 64rem)` | MEDIUM |
| Desktop | 1280px+ | `@media (min-width: 80rem)` | HIGH (if mockup is ~1440px) |

### Tailwind Breakpoint Mapping

| Pixel Breakpoint | Tailwind Prefix |
|-----------------|----------------|
| 640px | `sm:` |
| 768px | `md:` |
| 1024px | `lg:` |
| 1280px | `xl:` |
| 1536px | `2xl:` |

### Breakpoint Estimation from Content

| Content Pattern | Likely Break | Reason |
|----------------|-------------|--------|
| 3-column grid | ~768px → 1 col, ~1024px → 3 col | 3 cols too narrow below 1024px |
| 4-column grid | ~640px → 1 col, ~768px → 2 col, ~1024px → 4 col | Needs progressive build-up |
| Side-by-side text+image | ~768px → stack | Text becomes too narrow below |
| Pricing cards (3) | ~768px → stack, ~1024px → 3 | Cards need ~300px minimum |
| Navigation | ~768px → hamburger | Standard mobile nav pattern |

---

## Section Conversion Patterns

### Hero: Desktop → Mobile

```css
/* Mobile */
.hero {
  min-height: 100vh; /* Full screen on mobile */
  min-height: 100svh; /* Safe area viewport */
  padding: 4rem 1.5rem;
  text-align: center;
}

.hero__headline {
  font-size: 2rem; /* Smaller on mobile */
}

.hero__subline {
  font-size: 1rem;
}

.hero__actions {
  flex-direction: column;
  gap: 0.75rem;
}

/* Desktop */
@media (min-width: 64rem) {
  .hero {
    min-height: 80vh;
    padding: 6rem 1.5rem;
  }

  .hero__headline {
    font-size: 3rem; /* MEDIUM: match mockup */
  }

  .hero__subline {
    font-size: 1.25rem;
  }

  .hero__actions {
    flex-direction: row;
  }
}
```

### Navigation: Desktop → Mobile

```css
/* Mobile: hamburger (hide links) */
.nav__links {
  display: none;
}

.nav__hamburger {
  display: block;
}

/* Desktop: show links */
@media (min-width: 48rem) {
  .nav__links {
    display: flex;
  }

  .nav__hamburger {
    display: none;
  }
}
```

### Grid Sections: Desktop → Mobile

```css
/* Mobile: single column */
.pricing__grid {
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

/* Featured card: no scale on mobile */
.pricing__card--featured {
  transform: none;
}

/* Desktop: match mockup */
@media (min-width: 64rem) {
  .pricing__grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .pricing__card--featured {
    transform: scale(1.05);
  }
}
```

### Footer: Desktop → Mobile

```css
/* Mobile: stacked */
.footer__grid {
  grid-template-columns: 1fr;
  gap: 2rem;
}

.footer__bottom {
  flex-direction: column;
  gap: 1rem;
  text-align: center;
}

/* Desktop: multi-column */
@media (min-width: 48rem) {
  .footer__grid {
    grid-template-columns: 2fr repeat(3, 1fr);
  }

  .footer__bottom {
    flex-direction: row;
    text-align: left;
  }
}
```

---

## Responsive Typography

### Fluid Type Scale

When the mockup shows large desktop text, scale down proportionally for mobile:

| Element | Mobile | Tablet | Desktop | Method |
|---------|--------|--------|---------|--------|
| Hero h1 | 2rem | 2.5rem | 3rem+ | Breakpoint steps |
| Section h2 | 1.5rem | 1.75rem | 2.25rem | Breakpoint steps |
| Body | 1rem | 1rem | 1rem | Fixed |
| Small | 0.875rem | 0.875rem | 0.875rem | Fixed |

### CSS Clamp Alternative

For smoother scaling without breakpoints:

```css
/* Fluid hero headline: 2rem at 375px → 3.5rem at 1440px */
.hero__headline {
  font-size: clamp(2rem, 1.25rem + 2.5vw, 3.5rem);
}

/* Fluid section heading: 1.5rem → 2.25rem */
.section__heading {
  font-size: clamp(1.5rem, 1rem + 1.5vw, 2.25rem);
}
```

**Note**: Clamp is MEDIUM confidence when derived from a single-viewport mockup. Document the assumed mobile minimum.

---

## Common Responsive Patterns

### Image Handling

```css
/* Responsive images by default */
img {
  max-width: 100%;
  height: auto;
}

/* Hero background: cover at all sizes */
.hero__bg-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Side-by-side: stack on mobile */
.split__image {
  width: 100%;
  aspect-ratio: 4/3;
  object-fit: cover;
}

@media (min-width: 48rem) {
  .split__image {
    aspect-ratio: auto;
  }
}
```

### Spacing Reduction on Mobile

```css
/* Section padding: reduced on mobile */
.section {
  padding: 3rem 1rem;
}

@media (min-width: 48rem) {
  .section {
    padding: 4rem 1.5rem;
  }
}

@media (min-width: 64rem) {
  .section {
    padding: 5rem 1.5rem; /* Match mockup */
  }
}
```

### Hidden/Shown Elements

```css
/* Show simplified mobile version, hide desktop version */
.desktop-only { display: none; }
.mobile-only { display: block; }

@media (min-width: 48rem) {
  .desktop-only { display: block; }
  .mobile-only { display: none; }
}
```

### Touch Targets (WCAG 2.2 — 2.5.8 Target Size)

WCAG 2.2 AA requires minimum 24x24 CSS px; 44x44px is recommended for mobile:

```css
/* WCAG 2.2 AA minimum: 24x24px. Recommended: 44x44px */
.nav__link,
.faq__question,
.footer__link {
  min-height: 2.75rem; /* 44px */
  display: flex;
  align-items: center;
}

.cta-button {
  min-height: 2.75rem;
  min-width: 2.75rem;
  padding: 0.75rem 1.5rem;
}
```

---

## Modern CSS for Faithful Reproduction (2025–2026)

Browser-support summary (as of 2026-05):

| Feature | Baseline | Ship to production? |
|---------|----------|---------------------|
| `subgrid` | Baseline Widely Available (2026-03-15, all stable engines) | Yes — first-class tool, no `@supports` needed |
| `:has()` parent selector | Baseline Widely Available | Yes |
| Container Queries (`@container`, `cqw/cqh`) | Baseline Widely Available, ~78% of production sites adopt it | Yes |
| Dynamic Viewport Units (`dvh/svh/lvh`) | Baseline Widely Available | Yes |
| Cascade Layers (`@layer`) | Baseline Widely Available | Yes |
| Native Nesting | Baseline Widely Available | Yes |
| `text-wrap: balance` / `pretty` | Baseline Widely Available | Yes |
| Anchor Positioning (`anchor-name`, `position-anchor`, `position-try-fallbacks`) | Baseline Newly Available — Chrome/Edge stable; Safari TP and Firefox shipping behind partial support | Progressive enhancement only; require JS fallback for popover/tooltip placement |
| `@scope` | Baseline Newly Available — Chrome/Edge stable; Safari/Firefox catching up | Progressive enhancement; treat as a nice-to-have, not a load-bearing rule |
| Native CSS Masonry / Grid Lanes (`grid-template-rows: masonry`) | NOT Baseline — Safari TP only; Chrome team has proposed a separate `display: masonry` spec; Firefox keeps it behind a flag | Do not ship without a JS or Grid fallback |
| `@starting-style` + `interpolate-size` (entry/exit transitions) | Baseline Newly Available — Chrome/Edge stable | Progressive enhancement for entrance animations |

### CSS Subgrid — Card Content Alignment

Subgrid is now Baseline Widely Available. Use it as the default for any mockup that shows horizontally-aligned card content (title row / description row / CTA row across all cards).

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}
.card {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: span 3; /* title + description + CTA */
}
```

**Rule**: Eliminates fixed-height hacks and the legacy "auto-flow + min-content" workarounds. No `@supports` gate required as of 2026-05.

### Anchor Positioning — Tooltip / Dropdown Reproduction

```css
.tooltip-trigger { anchor-name: --tip; }
.tooltip {
  position: fixed;
  position-anchor: --tip;
  position-area: top;
  position-try-fallbacks: bottom, right, left;
}
```

**Rule**: Use for mockups showing positioned overlays. Browser support is still uneven (Chrome/Edge stable, Safari/Firefox partial), so pair with a JS positioning fallback (Floating UI or a manual `position: absolute` strategy) when shipping cross-browser.

### `@scope` — Section Style Isolation

```css
@scope (.hero-section) {
  h1 { font-size: 3rem; }
  p { font-size: 1.25rem; }
}
@scope (.features-section) {
  h2 { font-size: 2rem; }
  p { font-size: 1rem; }
}
```

**Rule**: Use when mockup sections have different typography scales. Prevents style bleed. Still progressive enhancement in 2026-05 — pair with explicit class selectors so the layout still works on engines without `@scope` support.

### Native CSS Masonry — Pinterest Layout

```css
.masonry {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  grid-template-rows: masonry;
}
```

**Rule**: As of 2026-05, native Masonry is NOT Baseline. Safari Technology Preview has the most complete implementation; Chrome has tabled a competing `display: masonry` proposal; Firefox keeps it behind a flag. Ship with `@supports (grid-template-rows: masonry)` and a Grid- or JS-based fallback (e.g., CSS multi-column or Masonry.js). Do not promise native masonry to designers as a faithful reproduction tool yet.

---

## Modern CSS for Responsive Design (2025–2026)

### Container Queries

Respond to component container size rather than viewport — ideal for reusable LP sections:

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card { flex-direction: row; }
}

@container card (min-width: 700px) {
  .card { grid-template-columns: 1fr 2fr; }
}
```

### Dynamic Viewport Units

Use `dvh` for mobile-accurate full-screen hero sections (accounts for address bar):

```css
.hero {
  min-height: 100dvh; /* Dynamic viewport height — adjusts with mobile chrome */
}
```

| Unit | Behavior |
|------|----------|
| `svh` | Small viewport (address bar visible) |
| `lvh` | Large viewport (address bar hidden) |
| `dvh` | Dynamic — changes with browser chrome |

### CSS Nesting (Native)

No preprocessor needed — all major browsers support native nesting:

```css
.pricing__card {
  border: 1px solid #e5e7eb;
  border-radius: 1rem;
  padding: 2rem;

  &--featured {
    border-color: transparent;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);
    transform: scale(1.05);
  }

  @media (max-width: 64rem) {
    &--featured {
      transform: none;
    }
  }
}
```

### :has() Selector

Parent selection based on child state — useful for form validation styling:

```css
/* Highlight form group when input is invalid */
.form-group:has(:invalid) {
  border-color: #ef4444;
}

/* Show label differently when input has value */
.form-group:has(input:not(:placeholder-shown)) .label {
  transform: translateY(-1.5rem);
  font-size: 0.75rem;
}
```

### text-wrap: balance

Avoid orphaned words in headings:

```css
h1, h2, h3 {
  text-wrap: balance;
}

p {
  text-wrap: pretty; /* Prevents orphans in body text */
}
```

### Cascade Layers

Organize CSS specificity for generated code to avoid conflicts:

```css
@layer reset, base, components, utilities;

@layer reset {
  *, *::before, *::after { box-sizing: border-box; margin: 0; }
}

@layer base {
  body { font-family: system-ui, sans-serif; line-height: 1.6; }
}

@layer components {
  .hero { /* ... */ }
  .pricing { /* ... */ }
}
```

### Subpixel Rendering Best Practices

```css
/* Consistent font rendering */
body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* 0.5px border alternative (cross-browser) */
.thin-border {
  box-shadow: inset 0 0 0 0.5px rgba(0, 0, 0, 0.1);
}

/* GPU layer promotion for precise positioning */
.precise-element {
  transform: translateZ(0);
}
```
