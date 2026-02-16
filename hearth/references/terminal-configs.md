# Terminal Emulator Configuration Patterns

Reference for ghostty, alacritty, kitty, and wezterm configuration.

---

## Ghostty

**Config path:** `~/.config/ghostty/config`
**Format:** Key-value pairs (no TOML/YAML, custom format)

### Basic Configuration

```
# Font
font-family = "JetBrains Mono"
font-size = 14
font-thicken = true
adjust-cell-height = 20%

# Theme
theme = catppuccin-mocha

# Window
window-padding-x = 8
window-padding-y = 4
window-decoration = true
macos-titlebar-style = transparent
background-opacity = 0.95

# Cursor
cursor-style = block
cursor-style-blink = false
shell-integration-features = no-cursor

# Mouse
mouse-hide-while-typing = true
copy-on-select = clipboard

# Behavior
confirm-close-surface = false
quit-after-last-window-closed = true
```

### Keybindings

```
# Splits
keybind = super+d=new_split:right
keybind = super+shift+d=new_split:down
keybind = super+w=close_surface

# Split navigation
keybind = super+alt+left=goto_split:left
keybind = super+alt+right=goto_split:right
keybind = super+alt+up=goto_split:top
keybind = super+alt+down=goto_split:bottom

# Tab navigation
keybind = super+t=new_tab
keybind = super+shift+left_bracket=previous_tab
keybind = super+shift+right_bracket=next_tab

# Font size
keybind = super+equal=increase_font_size:1
keybind = super+minus=decrease_font_size:1
keybind = super+0=reset_font_size
```

---

## Alacritty

**Config path:** `~/.config/alacritty/alacritty.toml`
**Format:** TOML

### Basic Configuration

```toml
# General
live_config_reload = true

[env]
TERM = "xterm-256color"

[window]
padding = { x = 8, y = 4 }
decorations = "Buttonless"
opacity = 0.95
option_as_alt = "Both"

[font]
size = 14.0
normal = { family = "JetBrains Mono", style = "Regular" }
bold = { family = "JetBrains Mono", style = "Bold" }
italic = { family = "JetBrains Mono", style = "Italic" }

[cursor]
style = { shape = "Block", blinking = "Off" }

[mouse]
hide_when_typing = true

[selection]
save_to_clipboard = true
```

### Theme Import

```toml
# alacritty.toml
import = ["~/.config/alacritty/catppuccin-mocha.toml"]
```

### Keybindings

```toml
[[keyboard.bindings]]
key = "N"
mods = "Command"
action = "SpawnNewInstance"

[[keyboard.bindings]]
key = "Return"
mods = "Command"
action = "ToggleFullscreen"
```

---

## Kitty

**Config path:** `~/.config/kitty/kitty.conf`
**Format:** Key-value pairs

### Basic Configuration

```
# Font
font_family      JetBrains Mono
bold_font        auto
italic_font      auto
bold_italic_font auto
font_size        14.0

# Window
window_padding_width 4
hide_window_decorations titlebar-only
background_opacity 0.95
macos_option_as_alt yes

# Cursor
cursor_shape block
cursor_blink_interval 0

# Mouse
mouse_hide_wait 3.0
copy_on_select clipboard

# Theme
include themes/catppuccin-mocha.conf

# Tab bar
tab_bar_style powerline
tab_bar_min_tabs 2
tab_title_template "{index}: {title}"

# Keybindings
map cmd+d       new_window_with_cwd
map cmd+shift+d new_window_with_cwd
map cmd+t       new_tab_with_cwd
map cmd+w       close_window
```

### Kittens (Extensions)

```bash
# Image viewer
kitty +kitten icat image.png

# Diff viewer
kitty +kitten diff file1 file2

# SSH (with terminal features forwarded)
kitty +kitten ssh user@host
```

---

## WezTerm

**Config path:** `~/.config/wezterm/wezterm.lua`
**Format:** Lua

### Basic Configuration

```lua
local wezterm = require 'wezterm'
local config = wezterm.config_builder()

-- Font
config.font = wezterm.font('JetBrains Mono')
config.font_size = 14.0

-- Window
config.window_padding = { left = 8, right = 8, top = 4, bottom = 4 }
config.window_decorations = "RESIZE"
config.window_background_opacity = 0.95
config.macos_window_background_blur = 20

-- Tab bar
config.hide_tab_bar_if_only_one_tab = true
config.tab_bar_at_bottom = true

-- Cursor
config.default_cursor_style = "SteadyBlock"

-- Color scheme
config.color_scheme = 'Catppuccin Mocha'

-- Keybindings
config.keys = {
  { key = 'd', mods = 'CMD', action = wezterm.action.SplitHorizontal { domain = 'CurrentPaneDomain' } },
  { key = 'd', mods = 'CMD|SHIFT', action = wezterm.action.SplitVertical { domain = 'CurrentPaneDomain' } },
  { key = 'w', mods = 'CMD', action = wezterm.action.CloseCurrentPane { confirm = false } },
}

return config
```

---

## Cross-Terminal Topics

### True Color Support

**Detection:**
```bash
# Test true color support
printf "\x1b[38;2;255;100;0mTRUECOLOR\x1b[0m\n"
echo $COLORTERM  # Should be "truecolor" or "24bit"
```

**Terminal-specific TERM values:**
| Terminal | Recommended TERM |
|----------|-----------------|
| ghostty | `xterm-ghostty` (auto) |
| alacritty | `xterm-256color` |
| kitty | `xterm-kitty` (auto) |
| wezterm | `xterm-256color` |
| tmux | `tmux-256color` |

**tmux true color pass-through:**
```tmux
set -g default-terminal "tmux-256color"
set -ag terminal-overrides ",xterm-256color:RGB"
set -ag terminal-overrides ",xterm-ghostty:RGB"
```

### Nerd Font Setup

**Recommended fonts (with Nerd Font patches):**
| Font | Style | Best For |
|------|-------|----------|
| JetBrains Mono | Modern, balanced | General coding |
| FiraCode | Ligatures | Symbol-heavy code |
| Hack | Clean, no-nonsense | Terminal focus |
| CascadiaCode | Microsoft design | Windows/cross-platform |

**Installation (macOS):**
```bash
brew install --cask font-jetbrains-mono-nerd-font
```

**Installation (Linux):**
```bash
# Manual
mkdir -p ~/.local/share/fonts
cd ~/.local/share/fonts
curl -fLO "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/JetBrainsMono.zip"
unzip JetBrainsMono.zip
fc-cache -fv
```

### Terminal Selection Guide

| Feature | Ghostty | Alacritty | Kitty | WezTerm |
|---------|---------|-----------|-------|---------|
| GPU rendering | Yes | Yes | Yes | Yes |
| Config format | Custom | TOML | Custom | Lua |
| Built-in splits | Yes | No | Yes | Yes |
| Image protocol | Kitty | No | Kitty | Kitty+iTerm2 |
| Ligatures | Yes | No | Yes | Yes |
| Platform | macOS/Linux | All | All | All |
| Resource usage | Low | Low | Medium | Medium |
| Customizability | Medium | Low | High | Very High |

---

## Ghostty 1.0+ Advanced Features

### Native Split Panes

Ghostty's built-in splits can replace tmux for simple workflows:

```
# Split management (no tmux required)
keybind = super+d=new_split:right
keybind = super+shift+d=new_split:down
keybind = super+alt+left=goto_split:left
keybind = super+alt+right=goto_split:right
keybind = super+shift+enter=toggle_split_zoom

# Equalize split sizes
keybind = super+shift+e=equalize_splits
```

**When to still use tmux:** Session persistence (SSH/remote), complex layouts, scripted pane management, shared sessions.

### Theme Discovery

```bash
# List all built-in themes
ghostty +list-themes

# Preview a theme (applies temporarily)
ghostty +list-themes --preview

# Popular themes: catppuccin-mocha, tokyonight, rose-pine, gruvbox-dark
```

### Shell Integration

```
# Enable shell integration features (auto-detected for zsh/bash/fish)
shell-integration = detect

# Features controlled by shell-integration-features:
# - cursor: Change cursor shape based on vi mode
# - sudo: Preserve shell integration through sudo
# - title: Set window title from shell
shell-integration-features = no-cursor,sudo,title
```

### terminfo Handling

```bash
# Ghostty sets TERM=xterm-ghostty by default
# If remote host lacks xterm-ghostty terminfo:
#   Option 1: Install terminfo on remote
infocmp -x xterm-ghostty | ssh remote 'tic -x -'

#   Option 2: Override TERM for SSH sessions
# In ~/.ssh/config or shell alias:
alias ssh='TERM=xterm-256color ssh'

# Verify terminfo
infocmp xterm-ghostty  # Should show capabilities
```
