# GIF Optimization Reference

Purpose: Reduce terminal-recording output size without unacceptable quality loss. Cover gifsicle palette quantization, Bayer / Floyd-Steinberg dithering, lossy mode, frame-drop analysis, ffmpeg 2-pass VP9 / AV1 for MP4, WebP alternatives, and GitHub README embed budgets.

## Scope Boundary

- **reel `optimize`**: GIF / video size optimization (this document).
- **reel `vhs` / `terminalizer` / `asciinema` / `readme` (elsewhere)**: Capture + baseline encoding.
- **reel `theme` / `narration` (elsewhere)**: Appearance + audio (orthogonal).
- **morph `batch` (elsewhere)**: Document batch pipelines.
- **tone `lufs` (elsewhere)**: Audio loudness.

## Why Optimize

GitHub README / docs has practical file-size ceilings: 5MB hard, 500KB-1MB comfortable. Unoptimized VHS / terminalizer output often clocks 5-15MB. Optimization recovers 80-95% without visible quality loss.

Plus: faster page load, better mobile experience, lower bandwidth cost.

## Decision: GIF vs Video

| Format | Size | Autoplay | Sound | Loop | Use |
|--------|------|----------|-------|------|-----|
| **GIF** | Large (relative) | Yes (inline) | No | Yes | README, docs, Slack |
| **WebP** | Smaller than GIF | Yes (most browsers) | No | Yes | Modern web |
| **APNG** | Comparable to WebP | Yes | No | Yes | Firefox-friendly |
| **MP4 (H.264)** | Smallest | Hover / click (GitHub Camo) | Yes | Yes (HTML video) | Full demos |
| **WebM / VP9** | Very small | Partial | Yes | Yes | Open-source pipelines |
| **MP4 / AV1** | Smallest (new) | Modern only | Yes | Yes | Cutting-edge |

**GitHub README default: GIF** (autoplay works). For docs / longer demos: **MP4** embedded via `<video>` (Camo proxy).

## Size Targets

| Context | Target |
|---------|--------|
| README hero GIF | ≤ 500 KB (fast load, mobile) |
| README section GIF | ≤ 2 MB |
| Docs page GIF | ≤ 3 MB |
| GitHub issue / PR | ≤ 10 MB hard limit |
| Slack / Discord | ≤ 8 MB |
| Twitter / X | ≤ 15 MB |
| Mobile-first blog | ≤ 300 KB |

## GIF Optimization with gifsicle

```bash
# Install
brew install gifsicle

# Basic optimize (≤256 colors, default)
gifsicle -O3 input.gif -o output.gif

# Palette reduction
gifsicle -O3 --colors 128 input.gif -o output.gif
gifsicle -O3 --colors 64 input.gif -o output.gif

# Lossy mode (quality 35-80; 80 typical)
gifsicle -O3 --lossy=80 input.gif -o output.gif
gifsicle -O3 --colors 128 --lossy=80 input.gif -o output.gif

# Dithering control
gifsicle --colors 64 --dither input.gif -o output.gif
# bayer: better for terminal (sharp edges)
gifsicle --colors 64 --dither=bayer input.gif -o output.gif

# Frame drop (halve frame count)
gifsicle -O3 --every 2 input.gif -o output.gif

# Resize
gifsicle -O3 --resize 960x540 input.gif -o output.gif
gifsicle -O3 --scale 0.5 input.gif -o output.gif
```

### Recommended combo for terminal recordings

```bash
gifsicle -O3 \
  --colors 64 \
  --lossy=80 \
  --dither=bayer \
  --resize 960x_ \
  input.gif -o output.gif
```

Typical result: 15MB → 1.5MB (10×) without terminal-text legibility loss.

## FFmpeg GIF Pipeline (alternative to gifsicle)

For more control, use ffmpeg 2-pass palette:

```bash
# Pass 1: generate palette
ffmpeg -y -i input.mp4 \
  -vf "fps=15,scale=960:-1:flags=lanczos,palettegen=max_colors=128:stats_mode=diff" \
  palette.png

# Pass 2: apply palette with Bayer dither
ffmpeg -y -i input.mp4 -i palette.png \
  -lavfi "fps=15,scale=960:-1:flags=lanczos [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" \
  output.gif
```

Tuning:
- `fps=15` vs 30: halves size (typing doesn't need 30fps)
- `scale=960`: downscale if source > 1080p
- `max_colors=64-128`: palette size trade-off
- `dither=bayer:bayer_scale=3-5`: less banding, sharper
- `diff_mode=rectangle`: frame-delta encoding

## WebP (smaller than GIF)

```bash
# Convert GIF to WebP
gif2webp -q 75 -m 6 input.gif -o output.webp

# Or from MP4
ffmpeg -i input.mp4 \
  -vcodec libwebp \
  -filter:v "fps=15,scale=960:-1" \
  -lossless 0 -compression_level 6 -q:v 70 -loop 0 -preset picture \
  output.webp
```

Browser support as of 2025: ~97% (Safari 14+, Chrome, Firefox, Edge). Fallback to GIF for older browsers.

## MP4 / VP9 / AV1 (for videos, not GIFs)

```bash
# H.264 MP4 (universal)
ffmpeg -i input.mov \
  -c:v libx264 -crf 23 -preset slow \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  output.mp4

# VP9 WebM (smaller, good browser support)
ffmpeg -i input.mov \
  -c:v libvpx-vp9 -crf 32 -b:v 0 \
  -c:a libopus -b:a 96k \
  -pass 1 -an -f null /dev/null && \
ffmpeg -i input.mov \
  -c:v libvpx-vp9 -crf 32 -b:v 0 \
  -c:a libopus -b:a 96k \
  -pass 2 \
  output.webm

# AV1 MP4 (cutting-edge, smallest)
ffmpeg -i input.mov \
  -c:v libaom-av1 -crf 30 -b:v 0 \
  -c:a libopus -b:a 96k \
  output.av1.mp4
```

AV1 gives 30-50% smaller files than H.264 at equivalent quality, but encode is 10-100× slower. Browser support improving (Chrome, Firefox full; Safari iOS 18+).

## Frame Drop Analysis

Typing demos rarely need 30fps. 15fps is indistinguishable from 30fps for text-only output. 12fps saves further; 8fps looks choppy.

```bash
# Measure source fps
ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate input.mp4

# Halve fps
ffmpeg -i input.mp4 -filter:v "fps=15" output.mp4
```

For animations / graphics: stay at 24-30fps. For terminal typing: 12-15fps fine.

## Quality A/B Check

Always spot-check output against original:

```bash
# Side-by-side preview
ffmpeg -i input.mp4 -i optimized.gif \
  -filter_complex "[0:v]scale=480:-1[orig];[1:v]scale=480:-1[opt];[orig][opt]hstack" \
  -frames:v 1 compare.png
```

Check:
- Text legibility (especially 10pt+ terminals)
- Color accuracy (syntax highlighting, brand colors)
- Smoothness (no stutter at reduced fps)
- Artifact-free (no banding, no dither pattern on flat areas)

## GitHub / README Embed

```markdown
<!-- GIF (autoplay, inline) -->
![demo](docs/demo.gif)

<!-- MP4 via HTML (GitHub auto-proxies) -->
<video src="docs/demo.mp4" autoplay loop muted playsinline></video>

<!-- asciinema embed (interactive) -->
[![asciicast](https://asciinema.org/a/XXXX.svg)](https://asciinema.org/a/XXXX)
```

GitHub renders `<video>` via Camo proxy. Silent + autoplay works. Use `poster="frame.png"` for first-frame thumbnail.

## Workflow

```
BUDGET       →  identify target size (README hero: 500KB, section: 2MB)
             →  pick format (GIF / WebP / MP4)

CAPTURE      →  from reel `vhs` / `terminalizer` / `asciinema`
             →  at 30fps default; downsample later

BASELINE     →  unoptimized output size
             →  source fps / resolution / color depth

REDUCE       →  decision tree:
                1. fps: 30 → 15 (halves size)
                2. resize: if > 960px wide, downscale
                3. palette: colors 256 → 128 → 64
                4. dither: Bayer for terminals
                5. lossy: 80 (visible quality trade-off)

VALIDATE     →  side-by-side vs original
                text legibility + color + smoothness
                artifacts check

DELIVER      →  write optimized file
                commit alongside source (both in repo)
                update README embed

HANDOFF      →  reel `theme`: if colors look wrong, re-theme
             →  reel `narration`: audio handoff for video
             →  Builder: CI integration (vhs-action + gifsicle)
```

## Output Template

```markdown
## GIF Optimization Report: [Demo]

### Inputs
- Source: [path] (format, size, fps, resolution)
- Baseline: [N MB]
- Target budget: [≤ N KB / MB]
- Context: [README hero / section / docs / Slack]

### Decisions
- Format: [GIF / WebP / MP4]
- FPS: [30 → 15]
- Resolution: [1920×1080 → 960×540]
- Palette: [256 → 64 colors]
- Dithering: [Bayer scale 5]
- Lossy: [80]

### Pipeline
```bash
[ffmpeg or gifsicle command]
```

### Result
- Optimized: [N KB]
- Reduction: [%]
- Quality check: [text legible / colors accurate / smooth]
- A/B sample: [compare.png path]

### Artifact Inventory
- Source: demo.mp4
- Optimized GIF: demo.gif ([N KB])
- WebP alt: demo.webp ([N KB])
- MP4 alt: demo.mp4 ([N KB])
- Compare PNG: compare.png

### README Embed
```markdown
![demo](docs/demo.gif)
<!-- or -->
<video src="docs/demo.mp4" autoplay loop muted playsinline></video>
```

### Handoffs
- reel `theme`: if palette artifacts
- reel `narration`: audio for video
- Builder: CI integration
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| 15 MB GIF on README | Optimize to ≤500 KB hero / ≤2 MB section |
| 30 fps terminal typing | 15 fps indistinguishable; save 50% |
| 256 colors on terminal GIF | 64-128 covers any terminal palette |
| No dithering (hard palette transitions) | Bayer scale 3-5 for terminals |
| 4K source retained at output | Downscale to 960-1280px wide |
| Lossy at quality 100 | Try 80; spot-check; rarely see difference |
| GIF for hours-long demo | Switch to MP4 / WebM for > 30s |
| Same GIF for dark + light mode README | Separate variants or use MP4 with color adaption |
| No compare.png A/B | Always spot-check; catches color / legibility bugs |
| Optimized with Floyd-Steinberg on terminal | Bayer produces sharper text edges |
| Forgetting `-movflags +faststart` for web MP4 | Enables streaming / early playback |
| Lossy 100+ (extreme) | Creates "digital noise"; cap at 80 |
| Ignoring WebP (smaller alternative) | Modern browsers support; fall back to GIF |
| No CI re-optimization | Set up GitHub Actions to re-run gifsicle on new VHS output |
| Checking only desktop view | Test on mobile; color banding more visible on small |
| Source GIF lost; only optimized retained | Commit source too; can re-optimize differently later |

## Deliverable Contract

When `optimize` completes, emit:

- **Baseline + target budget**.
- **Decision rationale** per axis (fps / resolution / palette / dither / lossy).
- **Pipeline command**.
- **Result** (size + reduction + quality check).
- **Artifact inventory** (source + all variants).
- **README embed snippet**.
- **Handoffs**: reel theme, reel narration, Builder.

## References

- gifsicle — github.com/kohler/gifsicle (Eddie Kohler)
- gif2webp — developers.google.com/speed/webp
- ffmpeg — ffmpeg.org
- VHS (charmbracelet) — github.com/charmbracelet/vhs
- asciinema — asciinema.org
- WebP browser support — caniuse.com/webp
- AV1 browser support — caniuse.com/av1
- "How to Make Small GIF Files" — Giphy engineering blog
- "Encoding Settings for Instagram / TikTok" — various social guides
- Mathias Bynens — "Smaller GIFs with lossy compression"
- "Vertical Video Encoding Best Practices" — Meta
- H.264 AVC spec — ITU-T H.264
- VP9 — webmproject.org
- AV1 — aomedia.org
- GitHub Camo proxy docs — docs.github.com
- "Image and video compression in the browser" — web.dev/compress-images
- imageoptim — imageoptim.com (Mac batch optimizer)
- ezgif — ezgif.com (web-based GIF tools)
- GifReducer, CompressPNG — alternative web tools
- "Bayer Dithering Algorithm" — Bryce Bayer (1971)
- "Floyd-Steinberg Dithering" — academic paper (1976)
