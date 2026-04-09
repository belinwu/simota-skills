# Ink Design Patterns

## SVG Icon Construction

### Basic Icon Template (24x24)

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
     fill="none" stroke="currentColor" stroke-width="2"
     stroke-linecap="round" stroke-linejoin="round"
     role="img" aria-label="Icon description">
  <title>Icon Name</title>
  <!-- paths here -->
</svg>
```

### Grid System

```
┌──────────────────────┐
│  ┌──────────────────┐ │ ← 2px padding
│  │                  │ │
│  │   Drawing Area   │ │ ← 20x20 active area
│  │                  │ │
│  └──────────────────┘ │
└──────────────────────┘
         24x24 total
```

Rules:
- Keep strokes within the padding boundary
- Align to whole pixels (no sub-pixel rendering)
- Optical center may differ from geometric center

## Icon Style Patterns

### Outline Style

```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
     stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <line x1="12" y1="8" x2="12" y2="16"/>
  <line x1="8" y1="12" x2="16" y2="12"/>
</svg>
```

### Filled Style

```svg
<svg viewBox="0 0 24 24" fill="currentColor">
  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 15v-4H7l5-7v4h4l-5 7z"/>
</svg>
```

### Duotone Style

```svg
<svg viewBox="0 0 24 24">
  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"
        fill="currentColor" opacity="0.2"/>
  <path d="M11 7v4H7l5 7v-4h4l-5-7z"
        fill="currentColor"/>
</svg>
```

## SVG Sprite System

### Symbol Definition

```svg
<svg xmlns="http://www.w3.org/2000/svg" style="display:none">
  <symbol id="icon-home" viewBox="0 0 24 24">
    <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0a1 1 0 01-1-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 01-1 1"/>
  </symbol>
  <symbol id="icon-search" viewBox="0 0 24 24">
    <circle cx="11" cy="11" r="8"/>
    <line x1="21" y1="21" x2="16.65" y2="16.65"/>
  </symbol>
</svg>
```

### Symbol Usage

```html
<svg class="icon" width="24" height="24">
  <use href="#icon-home"/>
</svg>
```

## Optimization Rules (SVGO)

| Rule | Description |
|------|-------------|
| Remove editor metadata | Strip Illustrator/Figma metadata |
| Normalize viewBox | Ensure viewBox matches content bounds |
| Merge paths | Combine compatible paths |
| Round coordinates | Round to 2 decimal places |
| Remove empty groups | Clean up `<g>` wrappers |
| Remove hidden elements | Strip `display:none` elements |
| Convert shapes to paths | Optionally for smaller output |

```bash
npx svgo input.svg -o output.svg --config='{"plugins":["preset-default",{"name":"removeViewBox","active":false}]}'
```

## Animated SVG Patterns

### CSS Animation

```svg
<svg viewBox="0 0 24 24">
  <style>
    .spin { animation: rotate 1s linear infinite; transform-origin: center; }
    @keyframes rotate { to { transform: rotate(360deg); } }
  </style>
  <circle class="spin" cx="12" cy="12" r="10" fill="none"
          stroke="currentColor" stroke-width="2"
          stroke-dasharray="50" stroke-dashoffset="10"/>
</svg>
```

### Hover Interaction

```css
.icon-button svg {
  transition: transform 0.2s ease, color 0.2s ease;
}
.icon-button:hover svg {
  transform: scale(1.1);
  color: var(--accent);
}
```

## Accessibility Checklist

| Requirement | Implementation |
|-------------|---------------|
| Screen reader label | `aria-label` or `<title>` element |
| Decorative icons | `aria-hidden="true"` |
| Focus indicators | Visible focus ring on interactive icons |
| Color contrast | 3:1 minimum against background |
| Touch target | 44x44px minimum for interactive icons |

## React Component Pattern

```tsx
interface IconProps extends React.SVGProps<SVGSVGElement> {
  size?: number;
  label?: string;
}

export const IconHome: React.FC<IconProps> = ({
  size = 24,
  label = "Home",
  ...props
}) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={2}
    strokeLinecap="round"
    strokeLinejoin="round"
    role="img"
    aria-label={label}
    {...props}
  >
    <title>{label}</title>
    <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0a1 1 0 01-1-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 01-1 1"/>
  </svg>
);
```
