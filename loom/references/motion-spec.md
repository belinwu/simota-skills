# Motion Specification for Figma Make

Reference for Loom's `motion` recipe. Document animation intent, Make's animation limitations, Framer Motion handoff strategy, and `prefers-reduced-motion` compliance.

---

## 1. Make's Animation Reality

Figma Make generates **CSS transitions** reliably but struggles with:
- Keyframe animations (`@keyframes`) — often dropped or simplified
- JS-driven animations (Framer Motion, GSAP) — Make won't generate; must be hand-stitched post-generation
- SVG morph / path animations — unsupported
- Scroll-linked animations (`animation-timeline: scroll()`) — unsupported

What Make does well:
- `transition: <property> <duration> <easing>` on hover / focus / active
- `:has()` and group-state transitions
- `@starting-style` for entrance transitions (modern browsers only)

Plan for **2-tier delivery**: (1) Make-generated CSS transitions for the base UI, (2) Framer Motion overlays for choreographed sequences.

---

## 2. Motion Token Schema

Document tokens in Guidelines.md `## Motion Tokens`:

```markdown
## Motion Tokens

### Duration
| Token | Value | Use case |
|---|---|---|
| --duration-instant | 0ms | State sync (no perceptible motion) |
| --duration-fast | 120ms | Micro-interactions (hover, focus ring) |
| --duration-base | 200ms | Standard UI transitions |
| --duration-moderate | 320ms | Panel slide, modal entrance |
| --duration-slow | 480ms | Page transition, choreographed sequence |

### Easing
| Token | Value | Use case |
|---|---|---|
| --ease-linear | linear | Progress bar, opacity fade |
| --ease-out | cubic-bezier(0.0, 0.0, 0.2, 1) | Entrance (decelerate) |
| --ease-in | cubic-bezier(0.4, 0.0, 1.0, 1) | Exit (accelerate) |
| --ease-in-out | cubic-bezier(0.4, 0.0, 0.2, 1) | State change |
| --ease-spring | cubic-bezier(0.34, 1.56, 0.64, 1) | Playful overshoot |
```

Make consumes these as CSS variables.

---

## 3. Tiered Specification

### Tier 1: CSS-only (Make-generated)
Document each element's CSS transition spec:

```markdown
### Button — hover transition
- property: background-color, transform
- duration: var(--duration-fast)
- easing: var(--ease-out)
- delay: 0ms
- transform: translateY(-1px) on hover

CSS:
```css
.button {
  transition: background-color var(--duration-fast) var(--ease-out),
              transform var(--duration-fast) var(--ease-out);
}
.button:hover { transform: translateY(-1px); }
```
```

### Tier 2: Framer Motion (post-Make handoff)
Document intent + variants only — leave implementation to engineering:

```markdown
### Card stack — staggered entrance (Framer Motion)
- intent: cards slide in from below + fade in, staggered by 60ms
- variants:
  - hidden: { opacity: 0, y: 20 }
  - visible: { opacity: 1, y: 0 }
- transition: { duration: 0.32, ease: 'easeOut' }
- stagger: 0.06s per child via `staggerChildren`
- reduced-motion fallback: opacity only, no Y translation
```

---

## 4. Micro-interactions Catalog

Document common micro-interactions in Guidelines.md `## Micro-interactions`:

| Element | Trigger | Property | Duration | Easing |
|---|---|---|---|---|
| Button | hover | bg-color, translateY | fast (120ms) | ease-out |
| Button | active | scale(0.98) | instant | linear |
| Input | focus | border-color, ring | fast | ease-out |
| Toggle | toggle | translateX, bg | base (200ms) | ease-spring |
| Modal | open | opacity, scale(0.96→1) | moderate | ease-out |
| Modal | close | opacity, scale(1→0.96) | fast | ease-in |
| Toast | enter | translateY(20px→0), opacity | base | ease-out |
| Accordion | expand | grid-template-rows (0fr→1fr) | moderate | ease-in-out |

Modern accordion expand uses `grid-template-rows` (works without `height: auto` hack).

---

## 5. `prefers-reduced-motion` Compliance

**Mandatory** for WCAG 2.3.3 (Animation from Interactions, AAA).

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

Per-component opt-in (preferred over global blanket):

```css
.modal {
  transition: opacity var(--duration-fast) var(--ease-out),
              transform var(--duration-fast) var(--ease-out);
}
@media (prefers-reduced-motion: reduce) {
  .modal {
    transition: opacity var(--duration-fast) linear;
    transform: none;
  }
}
```

Document fallback strategy in Guidelines.md `## Reduced-motion Fallbacks`:

| Original animation | Reduced fallback |
|---|---|
| Slide in + fade | Fade only |
| Scale + opacity | Opacity only |
| Spring overshoot | Linear ease |
| Stagger sequence | Simultaneous (no stagger) |
| Parallax scroll | Static |
| Auto-playing carousel | Pause; user-controlled only |

---

## 6. Make Prompt Recipes

### Recipe: hover transition
```
Add hover transition to Button:
background-color from var(--color-brand) to var(--color-brand-hover),
duration 120ms, ease cubic-bezier(0,0,0.2,1).
Add transform translateY(-1px) on hover.
```

### Recipe: modal entrance
```
Modal opens with: opacity 0→1, scale 0.96→1.
Duration 320ms, ease-out.
Use @starting-style for entrance transition.
Wrap in @media (prefers-reduced-motion: reduce) → transition opacity only, no scale.
```

### Recipe: toggle (state change)
```
Toggle switch: thumb translateX(0 → 20px) on checked,
background-color transition 200ms ease cubic-bezier(0.34,1.56,0.64,1).
Add :focus-visible ring with --duration-fast transition.
```

---

## 7. Performance Budget

| Property | Budget | Notes |
|---|---|---|
| Compositor-only properties | unlimited | `transform`, `opacity`, `filter` (with caveats) |
| Layout properties | avoid | `width`, `height`, `top`, `left` trigger reflow |
| Paint properties | minimize | `background-color` is cheap; `box-shadow` is expensive |
| Concurrent animations | ≤ 3 | More than 3 simultaneous transforms degrade on mid-tier mobile |
| FPS target | 60fps | Use Chrome DevTools Performance tab to verify |

Prefer `transform` / `opacity` for any animation > 200ms.

---

## 8. Choreography Patterns

### Stagger entrance
```
Container: visible variant triggers staggerChildren: 0.06
Children: hidden { opacity: 0, y: 20 } → visible { opacity: 1, y: 0 }
Result: cards cascade in from top to bottom
```

### FLIP animation (for layout transitions)
- Use `getBoundingClientRect()` to capture First/Last positions
- Apply Inverse transform, then animate to identity
- Use Framer Motion's `layout` prop or `react-flip-toolkit`
- Make cannot generate this; document as engineering handoff

### Shared element transition
- Modern: View Transitions API (`view-transition-name`)
- Document in Guidelines.md as "Tier 2 / engineering implementation"

---

## 9. Common Pitfalls

| Pitfall | Avoidance |
|---|---|
| Animating `height` triggers reflow → janky | Use `grid-template-rows` (0fr → 1fr) or `max-height` with known max |
| `transition: all` over-animates everything | Specify properties explicitly |
| No `prefers-reduced-motion` fallback | Mandatory; WCAG 2.3.3 |
| Spring easing on exit feels wrong | Spring for entrances/playful; linear/ease-in for exits |
| Stagger > 100ms feels sluggish | Cap at 80ms per item; use 40-60ms for tight sequences |
| Auto-playing video/carousel without pause | Provide controls; respect reduced-motion |
| `animation-iteration-count: infinite` without opt-out | Stop on hover/focus; respect reduced-motion |
| Make-generated keyframes silently dropped | Verify post-generation; fall back to transitions |

---

## 10. Decision Walkthrough Template

```
Element: ____________
Trigger: hover / focus / active / click / mount / scroll / route-change

Animation tier:
  □ Tier 1 — CSS-only (Make can generate)
  □ Tier 2 — Framer Motion (engineering handoff)

Tokens:
  duration: ____ (--duration-_____)
  easing:   ____ (--ease-_____)
  delay:    ____

Properties animated:
  □ transform (compositor-cheap)
  □ opacity   (compositor-cheap)
  □ background-color (paint)
  □ box-shadow (expensive — verify)
  □ other: ____

Reduced-motion fallback:
  ____________________________________

Performance check:
  □ Properties are compositor-friendly
  □ Concurrent animations ≤ 3
  □ Tested at 60fps on mid-tier mobile
  □ Tested with prefers-reduced-motion: reduce

Guidelines.md sections:
  □ ## Motion Tokens
  □ ## Micro-interactions (this element)
  □ ## Reduced-motion Fallbacks
  □ ## Engineering Handoff (if Tier 2)
```

---

## 11. References
- WCAG 2.3.3 Animation from Interactions
- MDN `prefers-reduced-motion`
- Framer Motion variants documentation
- View Transitions API (W3C CSS WG)
- Material Design Motion guidelines
