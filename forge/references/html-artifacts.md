# HTML Artifacts

Purpose: Use this reference when a prototype needs higher information density, visual comparison, or interactive feedback than Markdown can provide. Especially useful for multi-approach exploration, slider/drag-driven parameter tuning, and self-contained artifacts that can be opened directly in a browser without a build step.

## Contents

- When to Use HTML Artifacts
- Four Core Patterns
- Closed-Loop Design
- Single-File Constraints
- Anti-Patterns
- Source

---

## When to Use HTML Artifacts

Use HTML when:
- 3+ alternative approaches need side-by-side visual comparison
- The prototype's hypothesis requires user-driven parameter exploration (sliders, drag, toggles, animation timing)
- The artifact needs to render natively in a browser without a dev server or build step
- Information density exceeds what a Markdown table or code block can carry (mixed diagrams + interactive controls + linked sub-views)
- The output will be shared with non-developers who cannot run `npm run dev`

Use Markdown when:
- The artifact is purely textual specification or proposal copy
- Token efficiency matters more than visual density (e.g., long-context handoff payloads)
- The recipient is another agent, not a human reviewer

Use JSON when:
- The output is structured data consumed by another tool, not a human

---

## Four Core Patterns

### 1. Multi-Approach Grid

A single HTML file that lays out N candidate designs/approaches in a responsive grid. Each cell is self-contained (own styles, own state) and can be evaluated independently.

Use when:
- Forge is producing `moodboard`-style variants
- Spark `multi` Recipe produced 3-7 proposals that need visual comparison
- Vision needs to evaluate alternative directions before committing

Prompt pattern:
```
Generate 6 different approaches to <X>. Lay them out in a single
HTML file as a responsive grid (3 columns desktop, 1 column mobile).
Each cell should be self-contained and labeled with approach name +
one-line rationale.
```

Inline structure:
- `<style>` scoped to the grid via CSS Grid or Flexbox
- Each cell renders independently — no shared mutable state
- Approach metadata (name, rationale, trade-off) above each preview
- Optional: per-cell "Copy as spec" button (see Closed-Loop Design)

### 2. Interactive Prototype

A self-contained HTML page where the user adjusts parameters via sliders, drag handles, dropdowns, or animation scrubbers. Used to validate a hypothesis that depends on a parameter the team has not yet committed to.

Use when:
- The prototype's value question is "what value of X feels right?"
- Animation timing, spacing density, color saturation, or motion-curve choices need user-driven exploration
- A static screenshot or single frame cannot capture the design intent

Prompt pattern:
```
Build an HTML prototype for <component>. Include sliders for
<parameter list> (e.g., spacing, animation duration, opacity).
Render the result live as the user drags. Show current parameter
values as text below the preview.
```

Required hygiene:
- All parameters initialized to a reasonable default
- Current values displayed numerically alongside controls
- "Reset to defaults" button
- No persistence required (throwaway-first per Forge lifecycle)

### 3. Annotated Review Artifact

Out of scope for Forge (belongs to Judge / Scout / Lens), but Forge prototypes occasionally need to ship with reviewer notes inline. Use a sidebar or margin-note pattern: main column shows the prototype, side column shows reviewer questions and call-outs anchored to specific elements.

Reference: see `judge/` for code-review HTML artifact patterns.

### 4. Dashboard / Report Artifact

A single HTML file combining SVG diagrams, tables, and inline charts (no external library needed for simple cases — hand-authored SVG suffices). Used when the prototype's deliverable is information synthesis, not behavior.

Use when:
- The prototype is a dashboard mock validating layout + data shape, not real-time data
- The hypothesis is "does this report communicate the right insight?"
- The audience is reviewing the artifact, not interacting with it

Reference: see `showcase/` for design-system catalog patterns and `dashboard-prototyping.md` for charting-library-based dashboard prototypes (which are not single-file but offer richer interactivity).

---

## Closed-Loop Design

The Anthropic Claude Code blog post (see Source) emphasizes that HTML artifacts become most valuable when they can feed their output back into the next prompt — closing the loop between human exploration and agent iteration.

Pattern:
- Add a "Copy as JSON" or "Copy as Markdown spec" button to interactive prototypes
- The button serializes the current parameter state (or selected approach) to clipboard
- The user pastes the result into the next agent prompt — Forge → Builder, Forge → Muse, etc.

Implementation sketch:
```html
<button onclick="
  const spec = {
    approach: currentApproach,
    parameters: { spacing: spacingValue, duration: durationValue },
    timestamp: new Date().toISOString()
  };
  navigator.clipboard.writeText(JSON.stringify(spec, null, 2));
  this.textContent = 'Copied!';
">Copy as spec</button>
```

Closed-loop artifacts shorten the Forge → Builder handoff because the spec the user committed to is captured exactly, not paraphrased.

---

## Single-File Constraints

HTML artifacts in Forge must be **single-file by default** unless the user explicitly requests otherwise:

- All CSS inline in `<style>` (no external stylesheets)
- All JS inline in `<script>` (no module imports, no bundlers)
- No external image dependencies — use SVG inline or data-URIs
- No CDN dependencies for hypothesis-stage prototypes — they break offline and create build/version drift

Exception: lightweight CDN libraries (e.g., a single `<script src="https://unpkg.com/...">` for D3 / Chart.js) are acceptable when the prototype hypothesis depends on charting capability the team cannot reasonably hand-author. Document the dependency in the BUILDER FRICTION pointer so production migration accounts for it.

---

## Anti-Patterns

- **Single-page-app prototype**: Spinning up Vite + React just to render a prototype that could be a single HTML file. Adds 5-30 minutes of scaffolding overhead per prototype and breaks the ≤ 4h time-box.
- **Hidden state across cells**: In a grid of N approaches, allowing one cell to mutate state observed by another cell. Each cell must be evaluable independently — shared state defeats the comparison purpose.
- **Pixel-perfect HTML prototypes**: Treating the HTML artifact as the final deliverable. HTML prototypes are still subject to the 80% rule (`prototyping-anti-patterns.md`) — 20% time budget for styling.
- **Persistent server-side state**: Adding localStorage / sessionStorage / IndexedDB for "stateful" prototypes. Throwaway-first lifecycle forbids this; if the prototype needs persistence to demonstrate its hypothesis, the hypothesis itself probably needs splitting.
- **Markdown-with-HTML embedding**: Authoring a Markdown file with `<div style="...">` blocks instead of a clean HTML file. Loses the browser-native rendering benefit and creates the worst of both formats.
- **Skipping the closed-loop button**: Producing an interactive prototype with no way to capture the user's chosen parameters. Forces the human to re-describe the chosen state verbally to the next agent.

---

## Source

- Anthropic, "Using Claude Code: The unreasonable effectiveness of HTML" (2026-05-20). Author: Thariq Shihipar. The article catalogues five categories — specs/plans/exploration, code review, design/prototypes, reports/research, custom edit interfaces — and argues that HTML's combination of information density, browser-native rendering, and interactive bidirectionality outweighs Markdown's token-efficiency advantage in the Opus 4.7 / 1M-context-window regime. The closed-loop pattern (HTML artifact → JSON/Markdown export → next prompt) is the article's most actionable contribution and applies directly to Forge's prototype-to-builder handoff.
