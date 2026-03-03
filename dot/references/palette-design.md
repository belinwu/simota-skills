# Palette Design Reference

ピクセルアートのパレット設計に関する包括的リファレンス。色数制限理論、有名パレット定義、色彩理論、ジャンル別推奨。

---

## Color Count Theory

| Colors | Bits | Historical Platform | Modern Use |
|--------|------|-------------------|------------|
| 2 | 1-bit | Mac 128K, ZX Spectrum | Stamps, silhouettes, minimalist icons |
| 4 | 2-bit | GameBoy, CGA (mode 4) | Retro-style, monochrome themes |
| 8 | 3-bit | CGA (full), early MSX | Simplified sprites, low-res icons |
| 16 | 4-bit | NES, SNES per-tile, EGA | Standard game sprites, most common |
| 32 | 5-bit | Custom | Rich scenes, detailed backgrounds |
| 64 | 6-bit | Commodore 64 (nearby) | High-detail pixel art |
| 256 | 8-bit | SNES full, GBA, DOS VGA | Full-color pixel scenes |

### Platform Hardware Constraints

| Platform | Simultaneous Colors | Tile Size | Notes |
|----------|-------------------|-----------|-------|
| NES | 25 max (4 BG palettes × 4 + 4 sprite palettes × 3 + 1 shared) | 8×8 | 64-color system palette fixed |
| GameBoy (DMG) | 4 shades only | 8×8 | 160×144 screen |
| GameBoy Color | 56 simultaneous | 8×8 | 15-bit RGB (32,768 colors) |
| SNES | 256/scanline | 8×8 (OAM: 16×16) | 15-bit RGB |
| GBA | 512/32768 | Up to 64×64 sprites | 15-bit RGB |
| PICO-8 | 16 (+ 16 secret) | 8×8 | Virtual console |

## Palette Role System

Every palette needs at minimum 4 functional roles:

| Role | Purpose | Selection Rule |
|------|---------|---------------|
| **Base** | Primary fill color | Mid-tone, defines character identity |
| **Highlight** | Light-facing surfaces | 1-2 steps lighter + slight warm hue shift |
| **Shadow** | Dark-facing surfaces | 1-2 steps darker + slight cool hue shift |
| **Outline** | Edge definition | Darkest value, near-black or darkest hue |

### Extended roles (8+ color palettes)

| Role | Purpose |
|------|---------|
| **Mid-tone** | Transition between base and highlight/shadow |
| **Accent** | Eye-catching detail (eyes, gems, UI highlights) |
| **Background** | Scene fill, sky, ground base |
| **Secondary** | Supporting character/object colors |

## Famous Palettes

### DB16 (DawnBringer 16)

DawnBringer (Arne Niklas Jansson) が2012年に公開。暗色4色、中間色6色、明色4色、アクセント2色の構成。

```javascript
const DB16 = [
  "#140c1c", "#442434", "#30346d", "#4e4a4e",
  "#854c30", "#346524", "#d04648", "#757161",
  "#597dce", "#d27d2c", "#8595a1", "#6daa2c",
  "#d2aa99", "#6dc2ca", "#dad45e", "#deeed6"
];
```

**Best for:** General-purpose game sprites, balanced warm/cool

### DB32 (DawnBringer 32)

DB16の拡張版。各色域をより細かくカバー。スキントーン、グリーン系、ブルー系が充実。

```javascript
const DB32 = [
  "#000000", "#222034", "#45283c", "#663931",
  "#8f563b", "#df7126", "#d9a066", "#eec39a",
  "#fbf236", "#99e550", "#6abe30", "#37946e",
  "#4b692f", "#524b24", "#323c39", "#3f3f74",
  "#306082", "#5b6ee1", "#639bff", "#5fcde4",
  "#cbdbfc", "#ffffff", "#9badb7", "#847e87",
  "#696a6a", "#595652", "#76428a", "#ac3232",
  "#d95763", "#d77bba", "#8f974a", "#8a6f30"
];
```

**Best for:** Detailed scenes, rich environments

### Sweetie 16

GrafxKid作。明るく鮮やかで現代的なゲームに最適。

```javascript
const SWEETIE_16 = [
  "#1a1c2c", "#5d275d", "#b13e53", "#ef7d57",
  "#ffcd75", "#a7f070", "#38b764", "#257179",
  "#29366f", "#3b5dc9", "#41a6f6", "#73eff7",
  "#f4f4f4", "#94b0c2", "#566c86", "#333c57"
];
```

**Best for:** Modern pixel art, vibrant feel, UI/icons

### PICO-8

Lexaloffleの仮想ゲーム機パレット。高コントラストで視認性抜群。

```javascript
const PICO8 = [
  "#000000", "#1d2b53", "#7e2553", "#008751",
  "#ab5236", "#5f574f", "#c2c3c7", "#fff1e8",
  "#ff004d", "#ffa300", "#ffec27", "#00e436",
  "#29adff", "#83769c", "#ff77a8", "#ffccaa"
];
```

**Secret palette (index 128-143):**

```javascript
const PICO8_SECRET = [
  "#291814", "#111d35", "#422136", "#125359",
  "#742f29", "#49333b", "#a28879", "#f3ef7d",
  "#be1250", "#ff6c24", "#a8e72e", "#00b543",
  "#065ab5", "#754665", "#ff6e59", "#ff9d81"
];
```

**Best for:** Fantasy console style, retro games, game jams

### Endesga 32

Endesga作。ウォームトーン中心のファンタジー系パレット。

```javascript
const ENDESGA_32 = [
  "#be4a2f", "#d77643", "#ead4aa", "#e4a672",
  "#b86f50", "#733e39", "#3e2731", "#a22633",
  "#e43b44", "#f77622", "#feae34", "#fee761",
  "#63c74d", "#3e8948", "#265c42", "#193c3e",
  "#124e89", "#0099db", "#2ce8f5", "#ffffff",
  "#c0cbdc", "#8b9bb4", "#5a6988", "#3a4466",
  "#262b44", "#181425", "#ff0044", "#68386c",
  "#b55088", "#f6757a", "#e8b796", "#c28569"
];
```

**Best for:** Fantasy RPG, warm-toned games

### GameBoy (Original DMG)

```javascript
const GAMEBOY = [
  "#0f380f", // Darkest
  "#306230", // Dark
  "#8bac0f", // Light
  "#9bbc0f"  // Lightest
];
```

**Alternative interpretation:**

```javascript
const GAMEBOY_ALT = [
  "#081820", "#346856", "#88c070", "#e0f8d0"
];
```

### GameBoy Pocket (Greyscale)

```javascript
const GB_POCKET = [
  "#000000", "#555555", "#aaaaaa", "#ffffff"
];
```

### NES (Full 64-color system palette — Nestopia)

```javascript
// Row 0 (Dark)
const NES_ROW0 = [
  "#626262", "#001fb2", "#2404c8", "#5200b2",
  "#8a0070", "#ac0015", "#ac0500", "#7a1a00",
  "#423300", "#074800", "#005600", "#004f08",
  "#003c5c", "#000000"
];
// Row 1 (Normal)
const NES_ROW1 = [
  "#ababab", "#1e54f9", "#614eff", "#9946f2",
  "#c63fbe", "#d33a6b", "#d14014", "#b25e00",
  "#7d7b00", "#43a200", "#1ab500", "#0dab40",
  "#0d969b", "#2d2d2d"
];
// Row 2 (Light)
const NES_ROW2 = [
  "#ffffff", "#69a9ff", "#a29dff", "#d390ff",
  "#f77fff", "#ff7dbc", "#ff8469", "#ef9d34",
  "#d7ba00", "#94e01c", "#65f04e", "#48f597",
  "#4bd7ec", "#878787"
];
// Row 3 (Tints)
const NES_ROW3 = [
  "#ffffff", "#c5e0ff", "#d4dbff", "#e5d0ff",
  "#f7c7ff", "#ffc6e7", "#ffc9c1", "#ffd5a5",
  "#eee487", "#ceee94", "#bef4ac", "#c0fad1",
  "#bce0f0", "#d5d5d5"
];
```

### CGA (IBM PC)

```javascript
// 16-color mode
const CGA_16 = [
  "#000000", "#0000aa", "#00aa00", "#00aaaa",
  "#aa0000", "#aa00aa", "#aa5500", "#aaaaaa",
  "#555555", "#5555ff", "#55ff55", "#55ffff",
  "#ff5555", "#ff55ff", "#ffff55", "#ffffff"
];

// Mode 4 Palette 1 (High Intensity) — most famous
const CGA_P1 = [
  "#000000", "#55ffff", "#ff55ff", "#ffffff"
];

// Mode 4 Palette 0 (High Intensity)
const CGA_P0 = [
  "#000000", "#55ff55", "#ff5555", "#ffff55"
];
```

### Other Notable Palettes

**Nyx8 (Javier Guerrero) — 8 colors:**

```javascript
const NYX8 = [
  "#08141e", "#0f2a3f", "#20394f", "#f6d6bd",
  "#c3a38a", "#997577", "#816271", "#4e495f"
];
```

**Journey (Luis Zuno) — 11 colors:**

```javascript
const JOURNEY = [
  "#050914", "#1e1b26", "#493c2b", "#7b6d8d",
  "#a0938e", "#c9b99b", "#e8dccf", "#fffbf5",
  "#f4a720", "#ce6e27", "#682111"
];
```

## Color Theory for Pixel Art

### Hue Shifting

最も重要なピクセルアート技法の一つ。影・ハイライトを単純に暗くするのではなく、色相をシフトさせる。

**基本原則:**

```
Shadow direction:    Hue toward cool (blue/purple), Saturation +, Value -
Base:                Original hue
Highlight direction: Hue toward warm (yellow/orange), Saturation -, Value +
```

**Standard increment:** +20° shift per swatch step

**Practical shift range:** 20°–40° total

### Color Ramp Construction (9-swatch template)

```
Swatch 1 (darkest): H - 20°, S = 55%, V = 15%
Swatch 2:           H - 15°, S = 60%, V = 28%
Swatch 3:           H - 10°, S = 68%, V = 42%
Swatch 4:           H -  5°, S = 75%, V = 55%
Swatch 5 (mid):     H      , S = 80%, V = 65%  ← Saturation peak
Swatch 6:           H +  5°, S = 78%, V = 75%
Swatch 7:           H + 10°, S = 72%, V = 84%
Swatch 8:           H + 15°, S = 62%, V = 92%
Swatch 9 (lightest):H + 20°, S = 50%, V = 98%
```

### Hue Shifting Examples

**Red object:**

```
Deep shadow:  H=340°, S=60%, V=25%  (toward purple)
Shadow:       H=355°, S=70%, V=45%
Midtone:      H=5°,   S=80%, V=65%  (pure red)
Highlight:    H=20°,  S=75%, V=85%  (toward orange)
Bright HL:    H=35°,  S=65%, V=100% (toward yellow)
```

**Green foliage:**

```
Shadow:    #2d5a1e  (shift toward teal)
Base:      #4a8c3f  (green)
Highlight: #8cc63f  (shift toward yellow)
Bright:    #c8e66a  (more yellow)
```

| Base Hue | Shadow Shift | Highlight Shift |
|----------|-------------|-----------------|
| Red | → Purple | → Orange |
| Green | → Teal/Blue | → Yellow |
| Blue | → Purple | → Cyan |
| Yellow | → Green | → White/Cream |
| Brown | → Dark Purple | → Orange/Gold |

### Saturation Ramps

```
Shadow end:  Saturation 40-70%, Value 10-30%
Midtone:     Saturation 60-90%, Value 40-60%  ← Saturation peak
Highlight:   Saturation 20-50%, Value 70-90%
```

**Why:** Shadows mix with ambient light (reduce fixed color saturation). Midtones show pure local color under direct light. Highlights approach the white of the light source.

### Value Stepping

Value steps per hue by palette size:

| Palette Size | Steps per Hue |
|-------------|--------------|
| 2-color | 2 (shadow/light) |
| 8-color | 3-4 |
| 16-color | 4-5 |
| 32-color | 5-7 |
| 64-color | 7-10 |

**Perceptual spacing** (not linear):

```
Bad (linear):        V = 100, 80, 60, 40, 20
Good (perceptual):   V = 96, 82, 64, 44, 26, 12
```

### Color Temperature by Scene

| Scene | Shadow Color | Highlight Color |
|-------|-------------|----------------|
| Outdoor daylight | Cool blue-purple (sky reflection) | Warm yellow (sunlight) |
| Indoor lantern/fire | Deep blue/teal | Orange/yellow (flame) |
| Night | Deep blue-purple | Cool white/blue (moonlight) |
| Underwater | Dark teal | Bright cyan-green |

## Genre-Specific Recommendations

| Genre | Recommended Palette | Colors | Rationale |
|-------|-------------------|--------|-----------|
| RPG (Fantasy) | DB32, Endesga 32 | 16-32 | Wide range for characters, terrain, UI |
| Platformer | Sweetie 16, DB16 | 16 | Vibrant, readable at speed |
| Puzzle | PICO-8, Sweetie 16 | 16 | Clear color distinction for pieces |
| Horror | Custom dark | 8-16 | Low saturation, narrow value range |
| Sci-fi | Custom neon | 16 | High contrast, cyan/magenta accents |
| Mobile casual | Sweetie 16 | 16 | Friendly, modern feel |
| GameBoy homage | GAMEBOY | 4 | Authentic retro constraint |

### Fantasy RPG Palette Principles

- Natural colors (green/brown/blue) = 60-70% of base
- Magic colors (purple/gold) kept to 10-15% for accent impact
- Skin tones minimum 4 steps (deep shadow → bright highlight)
- Metallic colors (gray series 3-4) required for weapons/armor
- UI accent colors (gold, HP red, MP blue) reserved

### Puzzle Game Palette Principles

- Each piece/element must be distinguishable with certainty
- Minimum 30-45° hue separation between colors on color wheel
- Color vision deficiency consideration: don't rely only on red vs green (differentiate by shape and value too)
- Low saturation/dark background to make game pieces pop
- Use saturation levels for active/inactive state indication

### Horror Palette Principles

- 80%+ of palette is dark colors (V < 40%)
- Overall desaturated (muted tones), vivid colors for accent only
- Red reserved for "blood/danger" — limit frequency for impact
- Purple/blue-purple shadows for "supernatural" atmosphere
- Warm yellow lantern light creates isolated fear feeling

## Palette Construction Method

### Step-by-step for custom palette

1. **Choose color count** based on project scope
2. **Define value ramp** — perceptually even lightness from dark to light
3. **Assign hue families** — typically 3-5 hue groups
4. **Apply hue shifting** — warm highlights, cool shadows
5. **Test readability** — each color must be distinguishable at 1x scale
6. **Validate contrast** — outline vs. base must have >= 3:1 contrast ratio

### HSV Construction Flow

```
Step 1: Choose base hue (e.g., H=30° brown/orange)
Step 2: Set midtone (S=75%, V=65%)
Step 3: Create dark end (H=10°, S=60%, V=20%) — cool shift
Step 4: Create light end (H=50°, S=60%, V=95%) — warm shift
Step 5: Fill intermediate steps with even V increments, S peaking at midtone
Step 6: Verify: plot all swatches; adjacent values must not appear same brightness
Step 7: Add neutral shadow color (S=10-20%, V=match dark end)
```

### Harmony Methods

| Method | Description | Example Use |
|--------|------------|------------|
| **Analogous** | 30-60° range on color wheel | Sunset scenes (red-orange-yellow) |
| **Complementary** | 180° opposite colors | Fantasy (blue × orange) |
| **Triadic** | 120° interval, 3 hues | Vibrant games (red × blue × yellow) |
| **Split Complementary** | Main + 2 split opposites | Rich variety without clash |

## Palette Reduction Strategies

| Method | Description | Best For |
|--------|------------|---------|
| **Median Cut** | Recursively split RGB space | General purpose |
| **Octree Quantization** | Octree RGB space division | Fast processing |
| **k-means Clustering** | Iterative cluster optimization | Best quality |

**Manual reduction priority:**

1. Skin tones (if characters present) — highest priority
2. Background main colors (sky/ground) — multiple steps
3. Foreground objects — 3-4 colors each
4. UI/effect pure accent colors — last

### Dithering for Palette Expansion

```
2-color dithering creates visual intermediate:
Color A: #3a7840 (green)
Color B: #c8a850 (golden)
50% dither → eye perceives ~#839a48
```

## Design Checklist

```
Basic:
[ ] Darkest/lightest contrast ratio sufficient (WCAG AA: >= 4.5:1)
[ ] Value steps perceptually even per hue
[ ] Hue shifting properly set for shadow/highlight directions
[ ] Adjacent value steps visually distinguishable

Harmony:
[ ] Color temperature unified (matches scene lighting)
[ ] Accent colors limited to 15% of total
[ ] Maximum saturation restricted to 1-3 colors

Practical:
[ ] Skin tones have 3+ steps minimum
[ ] Neutral colors (gray series) reserved for UI
[ ] Color vision deficiency considered (shape/value differentiation)
[ ] Dithering use planned within limited palette
```

## Palette Templates

### JavaScript

```javascript
const PALETTE = {
  name: "my-palette",
  colors: {
    outline:   "#1a1c2c",
    shadow:    "#5d275d",
    base:      "#b13e53",
    highlight: "#ef7d57",
    accent:    "#ffcd75",
  },
  array: ["#1a1c2c", "#5d275d", "#b13e53", "#ef7d57", "#ffcd75"],
  count: 5,
  source: "custom",
};
```

### Python

```python
PALETTE = {
    "name": "my-palette",
    "colors": [
        (0x1a, 0x1c, 0x2c),  # outline
        (0x5d, 0x27, 0x5d),  # shadow
        (0xb1, 0x3e, 0x53),  # base
        (0xef, 0x7d, 0x57),  # highlight
        (0xff, 0xcd, 0x75),  # accent
    ],
}
```
