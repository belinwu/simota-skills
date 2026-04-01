# Modern CSS Animations

Purpose: Use this file when modern platform APIs can replace JavaScript or simplify animation architecture.

## Contents
- View Transitions API
- `@starting-style`
- Scroll-driven animations
- `@property`
- Progressive enhancement rules

## Feature Gates

| Feature | Use For | Support |
|---------|---------|---------|
| View Transitions API | SPA and page transitions, shared elements | Chrome `111+`, Safari `18+` |
| `@starting-style` | Entry from `display: none` or popover/dialog open state | Chrome `117+`, Safari `17.5+` |
| Scroll-driven animations | Progress bars, reveal-on-scroll, parallax-lite | Chrome `115+` |
| `@property` | Animating custom properties | Chrome `85+`, Safari `15.4+` |

## Progressive Enhancement Rules

- Use `@supports` to gate modern features.
- Provide a CSS-only baseline before adding advanced behavior.
- Prefer View Transitions for context-preserving route changes, not every navigation.
- Avoid scroll-driven animation for essential content visibility.

## Minimal Examples

```js
document.startViewTransition(() => {
  updateDOM();
});
```

```css
::view-transition-old(root) {
  animation: fade-out 200ms ease-in;
}
::view-transition-new(root) {
  animation: fade-in 200ms ease-out;
}

dialog[open] {
  opacity: 1;
  transform: scale(1);
  transition: opacity 200ms ease-out, transform 200ms ease-out;

  @starting-style {
    opacity: 0;
    transform: scale(0.95);
  }
}

.reveal {
  opacity: 1;
  transform: none;
}

@supports (animation-timeline: view()) {
  .reveal {
    animation: fadeIn linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 100%;
  }
}
```

## When Not To Use

- Do not require View Transitions on unsupported browsers.
- Do not use scroll-driven motion for key affordances.
- Do not use `@property` when a standard property animation is enough.

## View Transitions Level 2 (MPA Cross-Document)

Cross-document View Transitions enable page transitions without JavaScript in MPAs. Chrome 126+, Safari 18.2+. Firefox not yet supported.

### Basic MPA Transition

```css
/* Add to both source and destination pages */
@view-transition {
  navigation: auto;
}

/* Custom slide animation */
@keyframes slide-in-from-right {
  from { transform: translateX(100%); }
}
@keyframes slide-out-to-left {
  to { transform: translateX(-100%); }
}

::view-transition-new(root) {
  animation: slide-in-from-right 300ms ease-out;
}
::view-transition-old(root) {
  animation: slide-out-to-left 300ms ease-in;
}
```

### Shared Element Transition (MPA)

```css
/* Source page */
.hero-image {
  view-transition-name: hero-image;
}

/* Destination page — same view-transition-name */
.detail-image {
  view-transition-name: hero-image;
}
```

## @starting-style + transition-behavior

Pure CSS entry/exit animations for dialog and popover. Baseline achieved across all major browsers.

### Dialog Entry/Exit

```css
dialog {
  opacity: 0;
  transform: scale(0.95) translateY(8px);
  transition: opacity 200ms ease-out,
              transform 200ms ease-out,
              display 200ms allow-discrete,
              overlay 200ms allow-discrete;

  @starting-style {
    opacity: 0;
    transform: scale(0.95) translateY(8px);
  }
}

dialog[open] {
  opacity: 1;
  transform: scale(1) translateY(0);
}
```

### Popover Entry/Exit

```css
[popover] {
  opacity: 0;
  transform: translateY(4px);
  transition: opacity 150ms ease-out,
              transform 150ms ease-out,
              display 150ms allow-discrete,
              overlay 150ms allow-discrete;

  @starting-style {
    opacity: 0;
    transform: translateY(4px);
  }
}

[popover]:popover-open {
  opacity: 1;
  transform: translateY(0);
}
```

## Scroll-Driven Animations (Practical Examples)

Chrome 115+ only. Always wrap in `@supports` and provide reduced-motion fallback.

### ViewTimeline: Reveal on Scroll

```css
@media (prefers-reduced-motion: no-preference) {
  @supports (animation-timeline: view()) {
    .reveal {
      opacity: 0;
      animation: fadeUp linear both;
      animation-timeline: view();
      animation-range: entry 0% entry 60%;
    }
  }
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### ScrollTimeline: Progress Bar

```css
@supports (animation-timeline: scroll()) {
  .progress-bar {
    transform-origin: left;
    animation: progress linear;
    animation-timeline: scroll(root block);
  }

  @keyframes progress {
    from { transform: scaleX(0); }
    to { transform: scaleX(1); }
  }
}
```

### animation-range Keywords

| Keyword | Meaning |
|---------|---------|
| `entry 0% entry 100%` | Element entering the scroll area |
| `contain` | Element fully within the scroll area |
| `exit 0% exit 100%` | Element leaving the scroll area |

## @property for Gradient Animation

```css
@property --color-start {
  syntax: '<color>';
  initial-value: #6366f1;
  inherits: false;
}
@property --color-end {
  syntax: '<color>';
  initial-value: #8b5cf6;
  inherits: false;
}

.gradient-btn {
  background: linear-gradient(135deg, var(--color-start), var(--color-end));
  transition: --color-start 300ms ease-out, --color-end 300ms ease-out;
}

.gradient-btn:hover {
  --color-start: #4f46e5;
  --color-end: #7c3aed;
}
```

## Updated Feature Gate Table

| Feature | Use For | Support |
|---------|---------|---------|
| View Transitions Level 1 | SPA transitions, shared elements | Chrome 111+, Safari 18+, Firefox 133+ (**Baseline**) |
| View Transitions Level 2 | MPA/cross-document transitions | Chrome 126+, Safari 18.2+ (Firefox not supported) |
| `@starting-style` | Entry from display:none, popover/dialog | Chrome 117+, Safari 17.4+, Firefox 129+ (**Baseline**) |
| `transition-behavior: allow-discrete` | Bidirectional display:none animation | All major browsers (**Baseline**) |
| Scroll-driven animations | Progress bars, reveal-on-scroll | Chrome 115+ only (`@supports` required) |
| `@property` | Animating custom properties, gradients | Chrome 85+, Safari 15.4+ (Firefox not yet) |
