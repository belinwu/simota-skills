# SVG Optimization

## Purpose

Hand-authored or design-tool-exported SVG often weighs 10–50× more than necessary. SVGO and disciplined path simplification compress without visual loss. This reference defines the optimization config, rules, and the sprite-vs-inline trade-off.

## Scope Boundary

- IN scope: SVGO config, decimal precision, path simplification, transform flatten, ID minification, sprite-vs-inline trade-off, build-time pipeline integration.
- OUT of scope: a11y annotation (`a11y`), animation (`animate`), theming via `currentColor` (`theme`), icon system grid (`system`), pictogram standards (`pictogram`).

## Core Concepts

### SVGO Default Plugins (2026)

SVGO 4+ ships with a "preset-default" that runs ~30 plugins. Useful overrides:

| Plugin | Default | Recommended override |
|--------|---------|---------------------|
| removeViewBox | enabled | **disable** — viewBox needed for responsive sizing |
| cleanupIds | enabled | enable for inline; minify only when sprite |
| inlineStyles | enabled | enable for icons (style → attributes) |
| convertColors | enabled | enable; converts to shorter form |
| convertPathData | enabled | enable with floatPrecision: 2 |
| mergePaths | enabled | enable; combines compatible paths |
| removeUnknownsAndDefaults | enabled | enable |
| sortAttrs | enabled | enable for diff-friendly output |
| removeAttrs | disabled | enable for stripping editor metadata (`data-*`, `inkscape:*`) |

### Recommended svgo.config.js

```js
export default {
  multipass: true,
  floatPrecision: 2,
  plugins: [
    {
      name: 'preset-default',
      params: {
        overrides: {
          removeViewBox: false,
          cleanupIds: { minify: true, prefix: 'ink-' },
        },
      },
    },
    {
      name: 'removeAttrs',
      params: {
        attrs: ['data-name', 'inkscape:.*', 'sodipodi:.*'],
      },
    },
    'removeDimensions', // strip width/height; viewBox handles sizing
  ],
};
```

### Decimal Precision

| Precision | File-size impact | Visual impact |
|-----------|------------------|---------------|
| 5+ digits | baseline | no impact (overspec) |
| 3 digits | -20% | none on icons / illustrations |
| 2 digits | -35% | none for icons up to 64 px; subtle on illustrations |
| 1 digit | -50% | visible jaggedness on curves |
| 0 digits | -65% | broken paths |

Default: `floatPrecision: 2` for icons / system icons. Use 3 for illustrations with smooth curves.

### Path Simplification

| Source | Optimization |
|--------|-------------|
| Adobe Illustrator export | Strip `<defs>` if not used; flatten transforms |
| Figma export | Remove duplicate nodes; merge identical paths |
| Inkscape SVG | Strip `inkscape:*` namespace; remove guides / grids |
| Sketch SVG | Convert text to outlines if used as decoration |
| Hand-coded | Use relative coords; chain commands with M/L/C/Z |

A 2 KB hand-optimized icon can be 200 B after SVGO.

### Transform Flattening

Nested `<g transform="...">` adds bytes and prevents some plugins from running. SVGO's `convertTransform` and `applyTransforms` flatten when safe.

Manual rule: avoid groups whose only purpose is `transform="translate(...)"` — bake the transform into the path data.

### Sprite vs Inline

Decision matrix:

| Count of icons | Reuse pattern | Recommendation |
|----------------|---------------|----------------|
| 1–5 unique | Used once each | Inline `<svg>` |
| 6–20 unique | Mixed reuse | Inline if part of components; sprite for global icons |
| 20+ unique | High reuse | Sprite (`<symbol>` + `<use>`) |
| Per-app system | All used everywhere | Sprite + Component-wrapped `<Icon>` |

Sprite trade-offs:

| Pro | Con |
|-----|-----|
| Single network request | currentColor inheritance harder across `<use>` shadow boundary |
| Browser-cacheable | Per-icon SEO image-search loss |
| Smaller total payload for 20+ icons | Tooling required to build sprite |
| Easy to hash-version cache | Smaller projects don't justify infra |

For React / Vue / Svelte component-based apps with a build step, the inline + bundler-treeshake pattern (e.g., `lucide-react`, `react-feather`) often beats sprites in DX without losing perf.

### Inline Strategy

- Component wraps `<svg viewBox>` and accepts `size` / `color` / `class` props.
- `currentColor` everywhere; no hard-coded `fill`.
- Tree-shaken: only imported icons land in the bundle.
- Output: per-icon ~200–600 B before gzip.

### Sprite Strategy

```html
<!-- Single sprite file, loaded once -->
<svg style="display:none">
  <symbol id="icon-check" viewBox="0 0 24 24">
    <path d="..." fill="currentColor"/>
  </symbol>
  <symbol id="icon-x" viewBox="0 0 24 24">
    <path d="..." fill="currentColor"/>
  </symbol>
</svg>

<!-- Usage -->
<svg class="icon" aria-hidden="true">
  <use href="#icon-check" />
</svg>
```

Caveats:

- `<use>` reaches into shadow DOM; CSS targeting via `:hover .icon-check path` may fail.
- Cross-origin sprites (CDN) need CORS headers + `<use href="https://...">`.
- IE11 dead in 2026; modern browsers OK with external `<use>`.

### Build Pipeline Integration

| Tool | Approach |
|------|----------|
| Vite + svgo | `vite-plugin-svgo` or pre-build script |
| Webpack | `svgo-loader` |
| Rollup | `rollup-plugin-svgo` |
| Astro | Built-in SVG handling + svgo plugin |
| esbuild | Custom plugin |
| Make/Justfile | `svgo --config svgo.config.js src/icons/**.svg --output dist/` |

CI: run SVGO in `pnpm lint` so unoptimized SVG never lands in main.

### Lossless vs Lossy Optimizations

Lossless (always safe):

- Strip XML namespaces / metadata.
- Remove empty groups / defs.
- Convert hex to short hex (`#rrggbb` → `#rgb`).
- Convert RGB → hex.
- Strip default attributes.
- Sort attributes.
- Minify IDs.
- Merge identical paths.

Lossy (visually imperceptible at most sizes):

- Decimal precision reduction.
- Convert `<line>` to `<path>` or vice versa.
- Path data concatenation (relative vs absolute coord choice).

Always avoid:

- Removing viewBox (breaks responsive sizing).
- Stripping `<title>` (a11y impact).
- Stripping `<desc>` if used.
- Removing `aria-*` attributes.

### Measurement

Pre / post commit checklist per icon:

| Metric | Target |
|--------|--------|
| File size | ≤ 2 KB (icon) / ≤ 8 KB (illustration) / ≤ 200 B per symbol in sprite |
| Path count | Minimum needed |
| Decimal precision | 2 (icons) / 3 (illustrations) |
| viewBox preserved | yes |
| currentColor used | yes (themed icons) |
| `<title>` if standalone | a11y requirement |

### Sprite Build Script

```sh
npx svgstore --inline -o dist/icons.svg src/icons/*.svg \
  && npx svgo --multipass --config svgo.config.js dist/icons.svg
```

Outputs single file with `<symbol>` per icon, optimized.

### Common Failure Patterns

| Problem | Fix |
|---------|-----|
| File 30 KB after SVGO | Likely embedded raster `<image>`; remove or split |
| Visible jaggedness | Decimal precision too low; bump to 3 |
| Theme color doesn't apply | Hard-coded `fill` instead of `currentColor` |
| Broken on dark mode | currentColor in CSS, but path overrides with `fill="black"` |
| CORS errors on sprite | Add CORS headers to sprite host or move to same-origin |
| `<use>` doesn't render | Old browser; or sprite path 404; verify with DevTools |
| Sprite gets re-downloaded | Missing cache headers; or no version-hash |
| Bloated JSX bundle | Treeshaking broken; configure tree-shake or use icon-CDN approach |

### Icon CDN vs Self-Hosted

| Source | Pro | Con |
|--------|-----|-----|
| Self-hosted SVGO'd | Full control; no external dep | Requires build pipeline |
| Lucide / Feather (treeshake) | Small per-icon; large library | Per-icon import bloat if not treeshaken |
| Iconify | 100+ libraries via API | External dep; runtime loading |
| Heroicons | Tailwind-aligned | Not tree-shaken in some setups |
| Font-icons (FontAwesome) | Single network request | Larger overall; a11y issues |

## Workflow

1. **Measure baseline** — record original file sizes for the icon set.
2. **Configure SVGO** — start from the recommended config; tune for your library.
3. **Decide sprite vs inline** — count + reuse pattern.
4. **Run SVGO** — verify visual diff.
5. **Inspect each icon** — sample 10% for visual fidelity at 16 / 24 / 48 px.
6. **Set decimal precision** — 2 for icons; 3 for illustrations.
7. **Strip metadata** — `data-name`, `inkscape:*`, comments.
8. **Convert hard-coded colors to currentColor** — for themed icons.
9. **Build sprite (if chosen)** — one file with `<symbol>` per icon.
10. **Set up CI** — fail builds on > target file size.
11. **Add cache headers** — sprite cached aggressively with hash version.
12. **Document the config** — commit `svgo.config.js` to repo.

## Output Template

```yaml
svg_optimization:
  baseline_kb_total: 320
  optimized_kb_total: 38
  reduction_pct: 88
  config:
    multipass: true
    float_precision: 2
    preserve_view_box: yes
    cleanup_ids: minify_with_prefix
    remove_attrs: [data-name, inkscape:.*, sodipodi:.*]
  delivery: sprite + inline_fallback
  per_icon_target_bytes: 200_to_600
  build_pipeline:
    tool: vite_plugin_svgo
    ci_check: file_size_under_2kb_per_icon
  cache:
    hash_versioned: yes
    cache_control: max-age=31536000
  visual_qa:
    sampled_pct: 10
    sizes_tested: [16, 24, 48]
    fidelity: PASS
```

## Anti-Patterns

- Removing `viewBox` — breaks responsive sizing.
- Stripping `<title>` — a11y degradation.
- Decimal precision 0 or 1 — visible jaggedness.
- Hard-coded `fill="#000"` blocking theme switching.
- Embedded `<image>` (raster) inside SVG — defeats vector benefit.
- Sprite without cache headers — re-downloaded every page load.
- Sprite without version hash — stale icons in production.
- 100 inline icons in one component — bundle bloat.
- Font-icons in 2026 — outdated; a11y issues; use SVG.
- No CI check on file size — regressions slip in.
- Editor metadata not stripped (`inkscape:*`, `sodipodi:*`).
- No multipass — partial optimizations missed.
- Mixed sprite + inline without strategy — duplicated icons.
- Treeshaking broken — full library shipped per import.
- Sprite served from cross-origin CDN without CORS — `<use>` fails silently.
- Optimizing animated SVG with `removeUselessDefs` — animation breaks.
- Optimizing without visual diff verification — regressions ship.

## Deliverable Contract

An SVG optimization plan is complete when:

- Baseline + post-optimization sizes recorded.
- SVGO config committed to repo.
- Decimal precision set per asset class.
- viewBox preserved on all assets.
- Sprite-vs-inline decision made.
- Build pipeline integrates SVGO.
- CI check enforces per-icon size cap.
- Cache headers + version hash for sprite.
- Visual QA sampled at multiple sizes.
- Common-failure-pattern audit run.

## References

- SVGO documentation — github.com/svg/svgo (4.0+ in 2026).
- Sara Soueidan, *Practical SVG* (2016) and updated blog series.
- Jake Archibald, *SVG icons FTW* — sprite vs inline trade-off classic.
- Chris Coyier, *CSS-Tricks* — SVG optimization series.
- Lucide / Feather / Heroicons — modern icon library implementations.
- web.dev *Image Performance* — image-format guidance.
- Smashing Magazine, *SVG Best Practices* (2023–2024).
- W3C SVG 2 Recommendation.
- svgstore + vite-plugin-svgo / rollup-plugin-svgo / svgo-loader documentation.
- Iconify documentation — runtime icon loading.
- web.dev *Variable fonts* — analogous tree-shake / subset strategy.
