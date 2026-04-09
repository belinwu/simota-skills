# Ink Handoff Templates

## Receiving Handoffs

### From Vision (Art Direction)

```yaml
VISION_TO_INK_HANDOFF:
  source: Vision
  content:
    style_direction: "[modern | playful | corporate | minimal]"
    mood: "[description]"
    color_palette: ["#hex1", "#hex2"]
    reference_libraries: ["[Lucide | Heroicons | Phosphor | custom]"]
  request: "Create icon set matching this direction"
```

### From Muse (Design Tokens)

```yaml
MUSE_TO_INK_HANDOFF:
  source: Muse
  content:
    tokens:
      color_primary: "[hex]"
      color_secondary: "[hex]"
      spacing_unit: "[px]"
      border_radius: "[px]"
    icon_context: "[where icons will be used]"
  request: "Align icon design with token system"
```

### From Frame (Figma Context)

```yaml
FRAME_TO_INK_HANDOFF:
  source: Frame
  content:
    figma_icons: ["[icon specs from Figma]"]
    grid_size: "[px]"
    style_notes: "[Figma design notes]"
  request: "Implement icons matching Figma specifications"
```

## Sending Handoffs

### To Artisan (Component Integration)

```yaml
INK_TO_ARTISAN_HANDOFF:
  source: Ink
  destination: Artisan
  content:
    icons:
      - name: "[icon-name]"
        svg: "[SVG code or path]"
        props: ["size", "color", "label"]
    component_pattern: "[inline | sprite | component]"
    framework: "[React | Vue | Svelte]"
  request: "Integrate SVG icons as framework components"
```

### To Showcase (Storybook Catalog)

```yaml
INK_TO_SHOWCASE_HANDOFF:
  source: Ink
  destination: Showcase
  content:
    icon_set:
      name: "[icon set name]"
      icons: ["[icon name list]"]
      grid: "[size]"
      styles: ["[outline | filled | duotone]"]
    design_spec:
      stroke_width: "[px]"
      corner_radius: "[px]"
  request: "Create Storybook stories for icon catalog"
```
