# Pixel Art Techniques Reference

ディザリング、アウトライン、シェーディング、アンチエイリアス回避、よくあるミスなど、ピクセルアート固有の技法。

---

## Dithering Patterns

### Ordered Dithering (Bayer Matrix)

2×2 Bayer matrix:

```
┌───┬───┐
│ 0 │ 2 │
├───┼───┤
│ 3 │ 1 │
└───┴───┘
```

4×4 Bayer matrix:

```
┌────┬────┬────┬────┐
│  0 │  8 │  2 │ 10 │
├────┼────┼────┼────┤
│ 12 │  4 │ 14 │  6 │
├────┼────┼────┼────┤
│  3 │ 11 │  1 │  9 │
├────┼────┼────┼────┤
│ 15 │  7 │ 13 │  5 │
└────┴────┴────┴────┘
```

8×8 matrix: 0-63 values. Generated recursively:

```
M(2n) = [ 4·M(n)    4·M(n)+2 ]
         [ 4·M(n)+3  4·M(n)+1 ]
```

### Dithering Implementation

```javascript
// 2x2 ordered dither between two colors
const BAYER_2x2 = [[0, 2], [3, 1]];

function ditherPixel(x, y, ratio, colorA, colorB) {
  const threshold = BAYER_2x2[y % 2][x % 2] / 4;
  return ratio > threshold ? colorB : colorA;
}
```

```python
# 4x4 Bayer dither with Pillow
BAYER_4x4 = [
    [0,  8,  2, 10],
    [12, 4, 14,  6],
    [3, 11,  1,  9],
    [15, 7, 13,  5],
]

def dither_region(img, x0, y0, w, h, color_a, color_b, ratio=0.5):
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            threshold = BAYER_4x4[y % 4][x % 4] / 16
            color = color_b if ratio > threshold else color_a
            img.putpixel((x, y), color)
```

### Floyd-Steinberg Error Diffusion

誤差拡散法。現在ピクセルの量子化誤差を隣接ピクセルに分配。Bayerよりも自然なグラデーションを生む。

```
Error distribution kernel:
         [current]   7/16
   3/16    5/16      1/16
```

```python
def floyd_steinberg_dither(img, palette):
    """Apply Floyd-Steinberg dithering to reduce to palette."""
    pixels = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            old_val = pixels[x, y]
            new_val = nearest_palette_color(old_val, palette)
            pixels[x, y] = new_val
            error = tuple(o - n for o, n in zip(old_val, new_val))
            if x + 1 < w:
                distribute(pixels, x+1, y, error, 7/16)
            if y + 1 < h:
                if x - 1 >= 0:
                    distribute(pixels, x-1, y+1, error, 3/16)
                distribute(pixels, x, y+1, error, 5/16)
                if x + 1 < w:
                    distribute(pixels, x+1, y+1, error, 1/16)
```

**Note:** Floyd-Steinberg is NOT recommended for animation sprites — causes flicker between frames.

### Dithering Pattern Types

| Pattern | Visual | Best For |
|---------|--------|----------|
| 50% checker | `XOXOXO` | Sharp color transitions |
| 25% sparse | `X...X.` | Subtle gradients |
| 75% dense | `XXXOXX` | Near-solid with texture |
| Vertical lines | `XOXOXO` rows | Fabric, rain |
| Horizontal lines | `XXXXXX` / `......` | Wood grain, horizon |
| Diagonal | Staggered | Soft shadows |
| Cross-hatch | 2 diagonal directions | Pencil-like texture |

### Dithering Selection Guide

| Situation | Recommended |
|-----------|------------|
| Retro hardware emulation | Bayer (match hardware size) |
| Photo palette reduction | Floyd-Steinberg |
| Simple gradient expression | Checkerboard or Bayer 2×2 |
| Hand-crafted artistic | Stylized (artist-directed) |
| Animated sprites | Bayer only (no error diffusion) |
| Metal/stone texture | Sparse dithering |
| Fabric/cloth | Directional dithering |

## Outline Techniques

### Standard Outline (1px solid)

```
. . X X X . .
. X ■ ■ ■ X .
X ■ ■ ■ ■ ■ X
X ■ ■ ■ ■ ■ X
X ■ ■ ■ ■ ■ X
. X ■ ■ ■ X .
. . X X X . .

X = outline color (darkest)
■ = fill color
. = transparent
```

**Pros:** Clear separation from any background. Simple to implement.
**Cons:** Can look heavy on bright/pastel sprites.

### Selective Outline (Sel-out)

Outline color varies based on adjacent fill color and light direction:

```
Rules:
- Light-facing edge: lighter outline or omit entirely
- Shadow-facing edge: darkest outline
- Side edges: mid-dark outline
- Outline color = darkened version of adjacent fill (NOT pure black)
```

```javascript
// Sel-out color examples
// Red area:   base #cc2200 → outline #660011
// Yellow area: base #ffdd00 → outline #886600
// Skin area:   base #ffaa88 → outline #884422
```

**Light-sourced sel-out:** Remove or lighten outline on light-facing edge (e.g., top-left). Keep darkest outline on shadow side (bottom-right). Creates embossed/3D feel.

### Double Outline

Two layers of outline for emphasis:
- Inner: darkest fill color or standard outline
- Outer: pure black or darkest palette color

**Use for:** UI icons, boss characters, important objects, chibi emphasis.
**Warning:** Consumes 2px of sprite area — not suitable for small sprites.

### No Outline (Outlineless)

Used for:
- Background elements (clouds, terrain details)
- Very small sprites (4×4, 8×8)
- Soft/organic shapes
- High-resolution pixel art (64×64+)

Rules when going outlineless:
- Increase color contrast between adjacent surfaces
- Use darker base colors to maintain readability
- Add 1px inner shadow for shape definition

### Inner Outline vs Outer Outline

| Type | Position | Use Case |
|------|----------|----------|
| Outer outline | On transparent pixels adjacent to sprite | Separation from background |
| Inner outline | Darken outermost filled pixels | Form emphasis, glass/gem thickness |

## Shading and Lighting

### Pillow Shading — ANTI-PATTERN

The most common pixel art mistake. Center is brightest, edges darken uniformly in all directions.

```
         Dark
      Dark  Light  Dark
   Dark  Light Brightest Light  Dark
      Dark  Light  Dark
         Dark
```

**Problems:**
- Ignores actual light source
- Looks like internal self-illumination
- Destroys shape information — all surfaces look identical
- Creates "pillow" or "balloon" appearance

**Fix:** Choose a single directional light source (e.g., top-left 45°) and shade accordingly.

### Cel Shading for Pixel Art

Flat color planes with sharp shading boundaries. 3-5 color steps:

1. **Highlight** — closest to light source, brightest color
2. **Base** — primary sprite color
3. **Shadow** — 1-2 steps darker
4. **Deep Shadow** — darkest area where no bounce light reaches
5. **(Optional) Rim Light** — backlit edge highlight

**Shading boundary rules:**
- Boundaries are 1px sharp lines (no gradient — use dithering if needed)
- Boundaries follow sprite form contours (form shadows)
- Keep 1px gap between boundary and outline

### Light Source Convention

Standard light source: **top-left** (10 o'clock position).

```
  ↘ Light direction
┌─────────┐
│ H H H . │  H = highlight
│ H B B S │  B = base
│ . B B S │  S = shadow
│ . S S S │  . = mid-tone
└─────────┘
```

**Light source consistency:** Keep the same direction across ALL sprites and UI icons in the game.

**Multiple light sources:**
- Primary + weak ambient (bounce light) = 2 max for most sprites
- Rim light = 3rd light from opposite side (backlit edge)
- 3+ light sources → sprite becomes hard to read

### Form Rendering by Sprite Size

| Size | Steps | Recommended Approach |
|------|-------|---------------------|
| 8×8 | 2-3 colors | Silhouette only. Minimal or no shading |
| 16×16 | 3-4 colors | 1-level shadow + highlight. Sharp boundaries |
| 32×32 | 4-6 colors | Full cel-shading. Dithering for mid-tones |
| 64×64+ | 6-12 colors | Fine details, rim light, subsurface effects |

### Highlight Placement

| Surface | Highlight Position | Notes |
|---------|-------------------|-------|
| Flat top | Top 1-2 rows | Horizontal surface |
| Curved | Top-left quadrant | Sphere-like |
| Cylindrical | Left 1-2 columns | Vertical tube |
| Metallic | Concentrated point | Small bright spot |
| Matte | Diffused area | Spread across surface |

## Hue Shifting in Practice

### Temperature Shift

```
Shadow:    Hue -15°, Sat +10%, Val -25%
Base:      Original
Highlight: Hue +15°, Sat -10%, Val +25%
```

### Example: Green Foliage

```
Shadow:    #2d5a1e  (shift toward teal)
Base:      #4a8c3f  (green)
Highlight: #8cc63f  (shift toward yellow)
Bright:    #c8e66a  (more yellow)
```

### Example: Red Character

```
Deep shadow: H=340°, S=60%, V=25%  (toward purple)
Shadow:      H=355°, S=70%, V=45%
Midtone:     H=5°,   S=80%, V=65%  (pure red)
Highlight:   H=20°,  S=75%, V=85%  (toward orange)
Bright HL:   H=35°,  S=65%, V=100% (toward yellow)
```

## Common Mistakes and Anti-Patterns

### Orphan Pixels

Isolated single pixels without same-color neighbors.

```
. . . . .
. . X . .    ← X is orphaned (no adjacent same-color)
. . . . .
```

**Problems:** Noisy silhouette, flickers in animation.
**Fix:** Merge with adjacent pixels (make 2+ pixel clusters) or remove.
**Exception:** Intentional sparkle/eye highlights.

### Jaggies

Staircase artifacts on diagonal lines, especially at shallow angles.

```
Bad (inconsistent steps):    Good (consistent 2:1):
. . X X                      . . X X
. X . .                      . X X .
X X . .                      X X . .
```

**Fix:** Keep line segment lengths consistent. For smooth curves, vary progressively: 3-2-1-1-2-3.

### Banding

Shading colors form parallel bands instead of following the form.

```
Bad (horizontal bands):      Good (form-following):
H H H H H H                 . H H H . .
B B B B B B                  H H B B H .
S S S S S S                  . B B S S .
                             . . S S S .
```

**Fix:** Make shading boundaries follow the shape's internal contour. Interlock clusters.
**Exception:** Intentional banding for water/metal reflections.

### Noise

Too much unnecessary pixel variation making the sprite look "busy."

**Causes:** Excessive dithering, over-detailed textures, too many colors.
**Fix:** Ensure clusters are 2-3px minimum. Prioritize silhouette over internal detail. Step back and squint.

### Too Many Colors

Using unique colors for subtle differences instead of reusing.

**Fix:** Consolidate — reuse colors across different parts. A limited palette forces cohesion.

## Manual Anti-Aliasing

Unlike automated AA (which is forbidden), **manual AA** places intermediate-value pixels intentionally on specific edges.

### When to Use Manual AA

- Curves on sprites 32px+ in size
- Silhouette outer edges for polish
- NOT on internal shading boundaries

### When NOT to Use

- 45° lines, horizontal/vertical lines (already crisp)
- Small sprites (8×8, 16×16) — not enough resolution
- Intentionally hard/pixel-crunchy style

### Technique

```
Before AA:           After manual AA:
. . . X X            . . m X X
. . X X .            . m X X .
. X X . .            m X X . .
X X . . .            X X . . .

m = mid-tone pixel (between outline and background)
```

Place 1-3 intermediate pixels at staircase segment ends.

## Anti-Aliasing Avoidance (Automated)

### Why Avoid Automated AA in Pixel Art

| Problem | Consequence |
|---------|------------|
| Blurry at 1x scale | Loses pixel crispness |
| Halo artifacts at Nx scale | Grey fringe around shapes |
| Palette violation | Introduces uncontrolled mid-tones |
| Inconsistent upscaling | Different interpolation per browser/engine |

### CSS/HTML Anti-AA Prevention

```css
image-rendering: pixelated;
image-rendering: crisp-edges;
```

```javascript
ctx.imageSmoothingEnabled = false;
```

### SVG Anti-AA Prevention

```xml
<svg shape-rendering="crispEdges">
```

### Engine Settings

| Engine | Setting |
|--------|---------|
| Phaser 3 | `pixelArt: true` in config + `this.cameras.main.roundPixels = true` |
| Godot | Import → Filter: Off, Snap 2D: On |
| Unity | Sprite → Filter Mode: Point, Compression: None |
| CSS | `image-rendering: pixelated` |

## Pixel Cluster Rules

### Minimum Cluster Size

- **2×1 minimum** — avoid "orphan" single pixels (except intentional detail like eyes)
- **Staircase rule** — when drawing diagonal lines, keep consistent step width

### Staircase Patterns

```
Good (consistent 2:1):     Bad (inconsistent):
. . X X                    . . X X
. X X .                    . X . .
X X . .                    X X . .

Good (consistent 1:1):     Bad (double):
. . . X                    . . X X
. . X .                    . X X .
. X . .                    X X . .
X . . .
```

## Sub-Pixel Animation

Movement smaller than 1 pixel without actually moving. Creates smooth illusion on tiny sprites.

### Techniques

- **Value cycling:** Brighten/darken highlight pixel 1 palette step per frame (shimmer/breathing)
- **Color substitution:** Swap single pixel between two palette colors (micro-movement)
- **Outline shifting:** Change 1-2 outline pixels from dark to slightly lighter (light angle change)
- **Edge addition/removal:** Add 1px on advancing side, remove on trailing side

```
Frame 1: X X X .    (object 3px wide)
Frame 2: X X X X    (add 1px right)
Frame 3: . X X X X  (remove 1px left, keep right)
Frame 4: . X X X .  (remove right — back to 3px)
→ Apparent movement = 0.5px/frame
```

**Use for:** Idle breathing, floating effects, hovering, fire/water ripples, HP bar pulsing.

## Readability at Small Sizes

### Silhouette Test

1. Fill sprite with single color (black)
2. Can you identify what it is from shape alone?
3. If not → redesign from silhouette first

**Good silhouette:** Unique outline shape, pose/action readable from form, clean perimeter.
**Bad silhouette:** Too symmetrical, noisy contour, rectangular/boxy.

### 8×8 Design Rules

- 2-3 colors + transparent only
- Shape recognition depends entirely on silhouette
- Every pixel = one design decision (no wasted pixels)
- Draw silhouette first, then add 1 level of shading

### 16×16 Design Rules

- 4-6 colors + transparent
- 1 level of shading only (base + shadow OR highlight)
- Face = eyes (2-4px) + mouth (2px) minimum
- Outline required for background separation
- Action must be readable from silhouette

### Contrast Requirements

| Comparison | Minimum Ratio |
|-----------|--------------|
| Sprite body vs background | 4.5:1 (WCAG AA reference) |
| Outline vs background | 7:1 ideal |
| Highlight vs shadow (internal) | 3:1 |

**Verification methods:**
- Convert to greyscale to check value contrast (also color blindness test)
- Place sprite on actual game background
- Squint test from 1-2m distance

## Common Pixel Art Dimensions

| Asset Type | Common Sizes | Notes |
|-----------|-------------|-------|
| Character (small) | 16×16, 16×24 | RPG overworld |
| Character (medium) | 32×32, 32×48 | Platformer, detail |
| Character (large) | 64×64, 64×96 | Boss, portrait |
| Icon | 8×8, 16×16 | UI, items |
| Tile | 16×16, 32×32 | Terrain, walls |
| Portrait | 48×48, 64×64 | Dialog box |
| Background | 320×180, 480×270 | Full scene (16:9) |

### Character Proportions by Size

| Size | Head Width | Proportion | Practical Colors |
|------|-----------|------------|-----------------|
| 8×8 | 4px max | Stick figure abstraction | 3 + transparent |
| 16×16 | 5-7px | Chibi 2:1 to 3:1 | 4-8 |
| 32×32 | 8-10px | Chibi 3:1 to semi-real 6:1 | 8-16 |
| 64×64 | 16-20px | Realistic 7:1 possible | 16-64 |

**Rule:** Realistic proportions below 48×48 don't work. Use chibi for small sprites.
