# Portraits

Drop Sketch-generated portrait PNGs here as `{slug}.png` (e.g. `flow.png`,
`vision.png`). Recommended size 720×720 (1:1). When a portrait arrives:

1. Add `assets/portraits/{slug}.png`.
2. In `assets/data/agents/{slug}.json`, change `portrait.status` from
   `"pending"` to `"generated"`.
3. Update the corresponding entry in `assets/data/agents.index.json`.
4. (One-time) Extend `portraitSvg()` in `assets/app.js` to render `<img>` when
   `status === "generated"` — see the README at the package root for the
   exact two-line patch.

Until then, the prototype shows a class-symbol SVG placeholder with a
"PENDING" badge in the top-right.
