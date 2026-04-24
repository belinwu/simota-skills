# SVG Animation Reference

Purpose: Author animated SVG assets (loaders, status transitions, microinteractions) using SMIL, CSS, or a hybrid of both. Pick the technique that matches the browser target, file-size budget, and interactivity needs — and ship a reduced-motion fallback by default.

## Scope Boundary

- **ink `animate`**: SMIL `<animate>` / `<animateTransform>` / `<animateMotion>` inside the SVG, CSS `@keyframes` driving SVG shapes, path morphing, reduced-motion variants shipped alongside the asset.
- **Flow (elsewhere)**: DOM-level CSS/JS animation of HTML elements, scroll-driven animations, View Transitions API, orchestration across an entire page.
- **Artisan (elsewhere)**: React/Vue component wiring that toggles SVG animation classes or mounts/unmounts animated icons.
- **Palette (elsewhere)**: interaction quality review and motion-accessibility audits.

If the hypothesis is "does this icon itself animate?" → `animate`. If it is "does this page transition feel right?" → Flow.

## SMIL vs CSS Decision Matrix

| Concern | SMIL | CSS | Hybrid |
|---------|------|-----|--------|
| Browser support | All modern evergreen; deprecated-then-unimplemented in Chrome history — now stable | Universal | Pick CSS for transforms, SMIL for path data |
| Path morphing (`d` attr) | Native (`<animate attributeName="d">`) | Not possible without JS | SMIL for `d`, CSS for color |
| Interactivity (`:hover`, class toggle) | Possible via `begin="mouseover"` but awkward | Natural via `:hover` / class | CSS for state, SMIL for shape |
| External standalone `.svg` (no host CSS) | Self-contained — works in `<img src>` | Requires inline `<svg>` or `<style>` inside | SMIL wins for portable loaders |
| File-size cost | +50-200 B per animation element | +100-400 B per keyframe block | Additive |
| Reduced-motion | Must be gated manually | `@media (prefers-reduced-motion)` works | CSS gate controls both |

Default: **CSS** for inline SVG inside an app. **SMIL** for portable standalone `.svg` (loader shipped as a single file, email-friendly, used in `<img>`).

## Workflow

1. **Declare intent**: loader / status transition / hover feedback / path morph. Decide loop count and total duration up front.
2. **Pick technique** from the matrix above.
3. **Constrain to transform + opacity** wherever possible (GPU-composited, no layout/paint).
4. **Author** — write the animation on the smallest element necessary.
5. **Gate on `prefers-reduced-motion`** before shipping.
6. **Measure** — confirm total file size delta is within the 4 KB per-icon budget.

## SMIL Patterns

```xml
<!-- Rotating spinner (portable, works in <img src>) -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" role="img" aria-label="Loading">
  <circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"
          stroke-dasharray="40 20" stroke-linecap="round">
    <animateTransform attributeName="transform" type="rotate"
                      from="0 12 12" to="360 12 12"
                      dur="1s" repeatCount="indefinite"/>
  </circle>
</svg>
```

```xml
<!-- Path morph: hamburger -> close -->
<path d="M3 6h18M3 12h18M3 18h18" stroke="currentColor" stroke-width="2">
  <animate attributeName="d"
           to="M6 6L18 18M6 18L18 6M12 12h0"
           begin="indefinite" dur="0.25s" fill="freeze"/>
</path>
```

Key knobs: `begin` (`0s`, `click`, `mouseover`, `indefinite`), `dur`, `repeatCount` (`indefinite` or integer), `fill="freeze"` (hold final state).

## CSS Patterns

```xml
<svg viewBox="0 0 24 24" class="icon-pulse" role="img" aria-label="Recording">
  <circle cx="12" cy="12" r="4" fill="currentColor"/>
</svg>
<style>
  .icon-pulse circle {
    transform-origin: center;
    animation: pulse 1.2s ease-in-out infinite;
  }
  @keyframes pulse {
    0%, 100% { transform: scale(1);   opacity: 1; }
    50%      { transform: scale(1.3); opacity: 0.5; }
  }
  @media (prefers-reduced-motion: reduce) {
    .icon-pulse circle { animation: none; }
  }
</style>
```

Prefer `transform` and `opacity` over `width`, `height`, `cx`, `cy`, `r` — the former two are GPU-composited; the latter trigger layout or paint per frame.

## Reduced-Motion Handling

Every animated icon ships a reduced-motion variant. Two acceptable strategies:

```css
/* Strategy A: disable */
@media (prefers-reduced-motion: reduce) {
  .icon-spin { animation: none; }
}

/* Strategy B: substitute a non-motion cue (opacity fade) */
@media (prefers-reduced-motion: reduce) {
  .icon-spin { animation: fade 2s ease-in-out infinite; }
  @keyframes fade { 0%, 100% { opacity: 1 } 50% { opacity: 0.5 } }
}
```

For SMIL (no media query), inline a `<script>` guard or author two asset variants and let the consumer pick. Flow owns page-level orchestration; `animate` owns the asset-level guard.

## Performance Checklist

- Animate `transform` / `opacity` only. Avoid `stroke-dashoffset` fast loops (paint cost adds up on many concurrent icons).
- Use `will-change: transform` sparingly — only on icons known to animate continuously.
- Keep `repeatCount="indefinite"` loops to one or two per viewport.
- For spinners in a list (table rows, toast stacks), share a single `<symbol>` via sprite and reference with `<use>` — one animation, N references.
- Total added bytes per animated icon should stay under 600 B (gzipped) — more means the animation is over-specified.

## Anti-Patterns

- No `prefers-reduced-motion` fallback — WCAG 2.3.3 / vestibular accessibility failure.
- Animating `cx` / `cy` / `r` / `width` at 60 fps — paint-bound and janky on mobile.
- Using SMIL inside inline SVG that already has CSS available — mixes paradigms without reason.
- Running SVGO with default config on SMIL markup — default plugins strip `<animate>` elements. Use safe-only plugins and visually verify.
- Stacking 20+ animated spinners on one screen — GPU memory and compositor pressure.
- Embedding motion in a decorative icon marked `aria-hidden="true"` without considering that assistive-tech users still see it flicker visually if they disable AT temporarily.

## Handoff

**To Artisan:** animation class names, state-trigger contract (`data-state="loading"` → CSS applies), reduced-motion behavior expected, whether the icon is in a sprite or inline.
**To Flow:** if the animation is part of a larger page transition, hand off total duration, easing, and the shape boundaries so Flow can orchestrate surrounding DOM.
**To Showcase:** story variants for `default`, `animating`, and `prefers-reduced-motion: reduce` so the catalog captures all three states.
