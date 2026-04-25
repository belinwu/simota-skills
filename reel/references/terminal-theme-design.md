# Terminal Theme Design Reference

Purpose: Design terminal themes optimized for demo readability. Cover font selection (JetBrains Mono / FiraCode / Cascadia / SF Mono), size scaling, WCAG contrast, palette choice (Dracula / Solarized / One Dark / Gruvbox / brand-custom), Nerd Font icons, transparent BG handling, and VHS / terminalizer theme config.

## Scope Boundary

- **reel `theme`**: Terminal appearance design for demos (this document).
- **reel `vhs` / `terminalizer` / `asciinema` (elsewhere)**: Recording tools.
- **reel `optimize` / `narration` (elsewhere)**: Size / audio.
- **hearth (elsewhere)**: Personal dev-env dotfile themes (different scope).
- **Muse (elsewhere)**: Modern design tokens (color theory reference).

## Why Demo-Specific Theme

- **Readability at compressed GIF**: Text legibility drops 30-40% after optimization; theme must compensate
- **Mobile viewing**: 70% of GitHub README reads happen on desktop, but 30% on mobile — theme must work both
- **Brand alignment**: Product demo should not scream "default Terminal"
- **Contrast for a11y**: WCAG AA 4.5:1 minimum, AAA 7:1 preferred
- **Thumbnail-worthy**: A theme-styled terminal doubles social media CTR vs bland default

## Font Selection

| Font | License | Ligatures | Nerd Font | Best for |
|------|---------|-----------|-----------|----------|
| **JetBrains Mono** | OFL Free | ✓ | ✓ (via Nerd Font bundle) | General dev; JetBrains-style |
| **FiraCode** | OFL Free | ✓ | ✓ | Popular dev standard |
| **Cascadia Code** | OFL Free | ✓ | ✓ (Cascadia Code NF) | Microsoft stacks |
| **SF Mono** | Apple | ✗ | ✗ | macOS-native feel |
| **Menlo** | Apple | ✗ | ✗ | Fallback, macOS Terminal.app default |
| **Source Code Pro** | OFL Free | ✗ | ✓ | Adobe ecosystem |
| **IBM Plex Mono** | OFL Free | ✗ | ✓ | Modern, IBM-branded |
| **Hack** | Apache 2 | ✗ | ✓ | Lightweight, clean |
| **Monaspace** | OFL Free | ✓ | ✗ | GitHub new standard 2024+ |
| **Berkeley Mono** | Paid | ✓ | ✓ | Premium, unique aesthetic |
| **Iosevka** | OFL Free | ✓ | ✓ | Highly customizable |

Default: **JetBrains Mono Nerd Font** or **FiraCode Nerd Font**. For corporate stacks that have their own brand font, use it.

## Nerd Font Icons

Nerd Fonts add glyphs for Git, file types, Unicode symbols used by modern CLI tools (starship, oh-my-zsh, lazygit).

Install:
```bash
brew install --cask font-jetbrains-mono-nerd-font
# Or download from nerdfonts.com
```

VHS tape:
```
Set FontFamily "JetBrains Mono Nerd Font"
```

If Nerd Font glyphs are missing, `` (folder),  (Git branch) etc render as tofu boxes. Test on rendered output.

## Font Size Guidelines

| Resolution | Font size | Notes |
|-----------|-----------|-------|
| 1920×1080 (4K source) | 18-22pt | Comfortable reading |
| 1280×720 (720p) | 16-18pt | README default |
| 1024×576 (compact) | 14-16pt | Tight |
| Mobile-first (scaled to 480p) | 20-24pt at source | Upscale for small screens |

Terminal columns: **80-120 col** for demo. Too-narrow truncates commands; too-wide wastes space. 100 col is the sweet spot.

## Contrast

WCAG standards:
| Level | Normal text | Large text (18pt+) |
|-------|-------------|--------------------|
| AA (minimum) | 4.5:1 | 3:1 |
| AAA (enhanced) | 7:1 | 4.5:1 |

Check each palette color vs background:
```bash
# Tools:
# - https://webaim.org/resources/contrastchecker/
# - https://www.oddbird.net/tools/color-contrast-grid/
```

Dark backgrounds: ensure brightest accent (usually yellow/green) has ≥ 7:1 vs BG.  
Light backgrounds: ensure darkest (usually blue/purple) has ≥ 7:1 vs BG.

## Canonical Palettes

| Palette | Vibe | URL |
|---------|------|-----|
| **Dracula** | Dark, vibrant, high contrast | draculatheme.com |
| **Solarized Dark/Light** | Muted, science-backed contrast | ethanschoonover.com/solarized |
| **One Dark** | Atom editor style | atom-one-dark |
| **Gruvbox** | Retro, earthy | github.com/morhetz/gruvbox |
| **Tokyo Night** | Modern, vibrant | github.com/enkia/tokyo-night-vscode-theme |
| **Catppuccin** | Pastel, four variants | catppuccin.com |
| **Nord** | Arctic, cool | nordtheme.com |
| **Monokai Pro** | Classic, high-contrast | monokai.pro |
| **Ayu** | Balanced, three variants | ayu.pub |
| **Rosé Pine** | Warm, soft | rosepinetheme.com |
| **GitHub Dark/Light** | GitHub match | github.com/theme |

For demos: **Dracula** or **Tokyo Night** photograph best; **Solarized Dark** for muted / professional.

## 16-Color ANSI Palette

Every theme defines 16 colors (8 normal + 8 bright):

```
Black         : #282a36  (dark BG)
Red           : #ff5555  (error, diff-minus)
Green         : #50fa7b  (success, diff-plus)
Yellow        : #f1fa8c  (warning)
Blue          : #6272a4  (dim, comment)
Magenta       : #bd93f9  (keyword, function)
Cyan          : #8be9fd  (string, link)
White         : #f8f8f2  (foreground)

Bright Black  : #44475a  (selection BG)
Bright Red    : #ff6e6e
Bright Green  : #69ff94
Bright Yellow : #ffffa5
Bright Blue   : #d6acff
Bright Magenta: #ff92df
Bright Cyan   : #a4ffff
Bright White  : #ffffff
```

Above is Dracula. Reassign bright-blue to something readable (not gray) — default `blue` is often too dim against dark bg.

## VHS Theme Configuration

```
# demo.tape
Output demo.gif

Set FontFamily "JetBrains Mono Nerd Font"
Set FontSize 18
Set Width 1280
Set Height 720
Set Padding 20
Set Theme {
  "name": "Dracula",
  "background": "#282a36",
  "foreground": "#f8f8f2",
  "black":   "#21222c",
  "red":     "#ff5555",
  "green":   "#50fa7b",
  "yellow":  "#f1fa8c",
  "blue":    "#bd93f9",
  "magenta": "#ff79c6",
  "cyan":    "#8be9fd",
  "white":   "#f8f8f2",
  "cursor":  "#f8f8f2",
  "selection": "#44475a"
}

Type "npm install"
Enter
Sleep 2s
```

Or use built-in theme:
```
Set Theme "Dracula"
```

VHS built-in themes: Dracula, Solarized Dark/Light, Tokyo Night, Gruvbox, Nord, Catppuccin Mocha.

## Terminalizer Theme

```yaml
# config.yml
theme:
  background: "#282a36"
  foreground: "#f8f8f2"
  cursor: "#f8f8f2"
  black: "#21222c"
  red: "#ff5555"
  # ... full 16-color palette

cols: 100
rows: 28
fontFamily: "JetBrains Mono Nerd Font, monospace"
fontSize: 16
lineHeight: 1.4
letterSpacing: 0
```

## Asciinema Theme

Asciinema uses CSS on the player side:

```html
<asciinema-player src="demo.cast" theme="solarized-dark"></asciinema-player>
```

Built-in: asciinema, tango, solarized-dark, solarized-light, monokai. Custom via CSS override.

## Transparent Background

For overlay on slides / videos, transparent BG:

```
# VHS
Set BackgroundColor "transparent"

# ffmpeg post
ffmpeg -i demo.mp4 -vf "colorkey=0x282a36:0.1:0.1" demo_transparent.mov
```

Note: GIF doesn't support alpha well; APNG / WebP / MP4 with chroma-key needed.

## Prompt Styling

The shell prompt matters as much as the theme:

```
# bash .bashrc
PS1='%F{cyan}→%f %F{green}%~%f $ '

# zsh .zshrc (oh-my-zsh)
ZSH_THEME="agnoster"
# Or Starship prompt
eval "$(starship init zsh)"

# Fish
set -g fish_prompt_pwd_dir_length 1
```

Keep prompt short (1-2 chars) for demo — long prompts waste horizontal space.

## Brand Custom Theme

For branded demos, inject brand palette:

```json
{
  "name": "AcmeBrand",
  "background": "#0F172A",
  "foreground": "#F8FAFC",
  "blue":    "#3B82F6",  // brand primary
  "green":   "#10B981",  // brand secondary
  "magenta": "#A855F7",  // accent
  "yellow":  "#FBBF24",
  "red":     "#EF4444",
  "cyan":    "#06B6D4"
}
```

Rule: at least 3 brand colors (primary, secondary, accent) should land on ANSI slots. Others can be standard to preserve legibility.

## Dark vs Light Variants

Most dev audiences: dark. But many blog contexts expect light. Provide both:

```bash
# Dark variant (default)
vhs demo.tape -o demo-dark.gif

# Light variant
Set Theme "Solarized Light"
vhs demo.tape -o demo-light.gif
```

README picks via prefers-color-scheme:

```markdown
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="demo-dark.gif">
  <source media="(prefers-color-scheme: light)" srcset="demo-light.gif">
  <img alt="demo" src="demo-dark.gif">
</picture>
```

## Workflow

```
CONTEXT      →  identify demo placement (README hero / blog / slide)
             →  dark / light / both
             →  brand alignment required?

FONT         →  Nerd Font variant of JetBrains Mono / FiraCode / Cascadia default
             →  verify Nerd Font glyphs render (no tofu)

SIZE         →  resolution target (1280×720 README default)
             →  font size 16-18pt
             →  columns 100 default

PALETTE      →  built-in (Dracula / Tokyo Night) OR brand-custom
             →  WCAG AA 4.5:1 per ANSI vs BG

PROMPT       →  short (1-2 char) for demo
             →  starship / custom PS1

VHS CONFIG   →  full .tape theme block
             →  or Set Theme "Dracula"

VARIANTS     →  dark + light if blog / docs context
             →  separate .tape files or parameterized

RENDER       →  VHS / terminalizer / asciinema capture
             →  visual QC: contrast, legibility, icon render

MOBILE CHECK →  scale to 480px width
             →  text still legible, colors distinct

HANDOFF      →  reel `optimize`: size-reduce
             →  reel `narration`: if audio layer
             →  Builder: CI integration
```

## Output Template

```markdown
## Terminal Theme: [Demo / Project]

### Context
- Placement: [README hero / docs / blog / slide overlay]
- Mode: [dark / light / both]
- Brand alignment: [yes / no]

### Font
- Family: [JetBrains Mono Nerd Font / FiraCode Nerd Font / ...]
- Size: [18pt]
- Nerd Font glyphs: [yes]
- Ligatures: [on / off]

### Resolution
- Width × Height: [1280×720]
- Columns × Rows: [100 × 28]
- Padding: [20px]

### Palette
- Name: [Dracula / Tokyo Night / Custom AcmeBrand]
- Background: [#282a36]
- Foreground: [#f8f8f2]
- 16 ANSI colors: [list or link to JSON]
- WCAG AA contrast verified: [pass]

### Prompt
- Shell: [zsh + starship / bash PS1]
- Characters: [→ ]
- Visible info: [cwd only]

### VHS Config
```
Set FontFamily "JetBrains Mono Nerd Font"
Set FontSize 18
Set Theme "Dracula"
# ...
```

### Variants
- Dark: demo-dark.gif
- Light: demo-light.gif

### Validation
- [ ] WCAG AA contrast verified
- [ ] Nerd Font glyphs render
- [ ] Mobile preview legible at 480px
- [ ] Brand palette represented (if applicable)
- [ ] Prompt not too long

### Handoffs
- reel `optimize`: size optimization
- reel `narration`: audio overlay
- Builder: CI integration
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Default black Terminal theme | Styled theme doubles CTR |
| 12pt font at 720p | 16-18pt minimum |
| Non-Nerd Font + modern CLI (lazygit, starship) | Use Nerd Font variant |
| Blue on dark (too dim) | Use bright-blue or custom lighter blue |
| White on yellow | Contrast test fails; use dark-text on yellow |
| 120+ column terminal | Truncate at 100 col max |
| Long prompt (`user@host:/long/path$ `) | Shorten to 1-2 chars |
| Only dark variant for docs-site with light mode | Provide light variant with `<picture>` |
| Custom theme ignoring ANSI standard | Keep 16-slot convention; custom brand colors on primary/secondary/accent |
| Terminal too narrow (60 col) | Commands wrap ugly; use 100 col |
| No mobile preview check | Scale to 480px; verify still legible |
| Brand color replaces `red` (error color) | Keep error = red convention; brand to blue/green/magenta |
| Testing with local Nerd Font, missing on CI | CI must install Nerd Font or VHS fails to render glyphs |
| Mixing fonts mid-demo | Consistent font throughout |
| Ligatures causing confusion (`===` → weird glyph) | Disable ligatures for teaching demos |
| Extreme transparency (alpha 0.3) | BG must be solid enough for contrast; transparent for overlay only |

## Deliverable Contract

When `theme` completes, emit:

- **Context** (placement + mode + brand alignment).
- **Font** choice + size + Nerd Font + ligature.
- **Resolution** + columns + padding.
- **Palette** (name + 16 ANSI + WCAG check).
- **Prompt** style + shell.
- **VHS / terminalizer / asciinema config** block.
- **Variants** (dark + light if applicable).
- **Validation** checklist.
- **Handoffs**: reel optimize, reel narration, Builder.

## References

- Nerd Fonts — nerdfonts.com
- JetBrains Mono — jetbrains.com/lp/mono
- FiraCode — github.com/tonsky/FiraCode
- Cascadia Code — github.com/microsoft/cascadia-code
- Monaspace — monaspace.githubnext.com
- Iosevka — typeof.net/Iosevka
- Dracula — draculatheme.com
- Solarized — ethanschoonover.com/solarized
- Tokyo Night — github.com/enkia/tokyo-night-vscode-theme
- Catppuccin — catppuccin.com
- Nord — nordtheme.com
- Gruvbox — github.com/morhetz/gruvbox
- Ayu — ayu.pub
- VHS (charmbracelet) — github.com/charmbracelet/vhs
- Terminalizer — terminalizer.com
- Asciinema — asciinema.org
- WCAG 2.1 Contrast — w3.org/TR/WCAG21
- WebAIM Contrast Checker — webaim.org/resources/contrastchecker
- Starship prompt — starship.rs
- Oh-My-Zsh — ohmyz.sh
- Ghostty terminal — ghostty.org (modern; good for demos)
- iTerm2 — iterm2.com
- Alacritty — alacritty.org
- WezTerm — wezfurlong.org/wezterm
- Kitty — sw.kovidgoyal.net/kitty
- Warp — warp.dev (modern with command completion)
- `<picture>` HTML element — developer.mozilla.org
- prefers-color-scheme — web.dev/prefers-color-scheme
