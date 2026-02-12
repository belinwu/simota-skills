# Tmux & Prompt Configuration Patterns

Reference for tmux, starship, and powerlevel10k configuration.

---

## Tmux Configuration

**Config path:** `~/.config/tmux/tmux.conf` (XDG) or `~/.tmux.conf` (legacy)

### Essential Configuration

```tmux
# ── Prefix ──────────────────────────────────
# Change prefix from C-b to C-a (more ergonomic)
unbind C-b
set -g prefix C-a
bind C-a send-prefix

# ── General ──────────────────────────────────
set -g default-terminal "tmux-256color"
set -ag terminal-overrides ",xterm-256color:RGB"
set -ag terminal-overrides ",xterm-ghostty:RGB"
set -g mouse on
set -g history-limit 50000
set -g base-index 1           # Start windows at 1
setw -g pane-base-index 1     # Start panes at 1
set -g renumber-windows on    # Renumber on close
set -sg escape-time 0         # No escape delay (important for vim)
set -g focus-events on        # Enable focus events
set -g set-clipboard on       # System clipboard

# ── Key Bindings ──────────────────────────────
# Reload config
bind r source-file ~/.config/tmux/tmux.conf \; display "Config reloaded"

# Split panes (intuitive keys)
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"
unbind '"'
unbind %

# New window in current path
bind c new-window -c "#{pane_current_path}"

# Pane navigation (vim-style)
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R

# Pane resizing
bind -r H resize-pane -L 5
bind -r J resize-pane -D 5
bind -r K resize-pane -U 5
bind -r L resize-pane -R 5

# Window navigation
bind -r C-h previous-window
bind -r C-l next-window

# Copy mode (vi keys)
setw -g mode-keys vi
bind -T copy-mode-vi v send-keys -X begin-selection
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "pbcopy"
bind -T copy-mode-vi C-v send-keys -X rectangle-toggle
```

### Status Bar

```tmux
# ── Status Bar ────────────────────────────────
set -g status-position top
set -g status-interval 5
set -g status-style "bg=default,fg=white"

# Left: session name
set -g status-left-length 30
set -g status-left "#[fg=blue,bold] #S "

# Center: window list
set -g window-status-format " #I:#W "
set -g window-status-current-format "#[fg=magenta,bold] #I:#W "
set -g window-status-separator ""

# Right: date/time
set -g status-right-length 50
set -g status-right "#[fg=white] %H:%M #[fg=blue] %Y-%m-%d "

# Pane borders
set -g pane-border-style "fg=brightblack"
set -g pane-active-border-style "fg=blue"
```

### TPM (Tmux Plugin Manager)

```tmux
# ── Plugins ───────────────────────────────────
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-resurrect'     # Session persistence
set -g @plugin 'tmux-plugins/tmux-continuum'      # Auto-save sessions
set -g @plugin 'christoomey/vim-tmux-navigator'   # Seamless vim/tmux nav

# Resurrect settings
set -g @resurrect-capture-pane-contents 'on'
set -g @continuum-restore 'on'

# Initialize TPM (keep at bottom)
run '~/.tmux/plugins/tpm/tpm'
```

**TPM installation:**
```bash
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
# Then in tmux: prefix + I (to install plugins)
```

### Session Management

```tmux
# Quick session switching
bind s choose-tree -sZ
bind S command-prompt -p "New session:" "new-session -s '%%'"

# Session layout presets (via shell script)
# ~/.local/bin/tmux-dev
# #!/bin/bash
# tmux new-session -d -s dev -c ~/projects
# tmux split-window -h -c ~/projects
# tmux select-pane -t 0
# tmux attach -t dev
```

---

## Starship Prompt

**Config path:** `~/.config/starship.toml`

### Minimal Configuration

```toml
# Timeout for commands (ms)
command_timeout = 500

# Prompt format
format = """
$directory\
$git_branch\
$git_status\
$character"""

# Newline before prompt
add_newline = false

[character]
success_symbol = "[❯](bold green)"
error_symbol = "[❯](bold red)"

[directory]
truncation_length = 3
truncation_symbol = "…/"

[git_branch]
format = "[$branch]($style) "
style = "bold purple"

[git_status]
format = '([$all_status$ahead_behind]($style) )'
style = "bold red"
```

### Standard Configuration

```toml
command_timeout = 500

format = """
$directory\
$git_branch\
$git_status\
$nodejs\
$python\
$rust\
$golang\
$docker_context\
$line_break\
$character"""

add_newline = true

[character]
success_symbol = "[❯](bold green)"
error_symbol = "[❯](bold red)"

[directory]
truncation_length = 4
truncation_symbol = "…/"
style = "bold cyan"

[git_branch]
format = "[$symbol$branch(:$remote_branch)]($style) "
symbol = " "
style = "bold purple"

[git_status]
format = '([$all_status$ahead_behind]($style) )'
conflicted = "="
ahead = "⇡${count}"
behind = "⇣${count}"
diverged = "⇕⇡${ahead_count}⇣${behind_count}"
untracked = "?${count}"
stashed = "*${count}"
modified = "!${count}"
staged = "+${count}"

[nodejs]
format = "[$symbol($version )]($style)"
symbol = " "
detect_files = ["package.json", ".node-version"]

[python]
format = '[${symbol}${pyenv_prefix}(${version} )(\($virtualenv\) )]($style)'
symbol = " "

[rust]
format = "[$symbol($version )]($style)"
symbol = " "

[golang]
format = "[$symbol($version )]($style)"
symbol = " "

[docker_context]
format = "[$symbol$context]($style) "
symbol = " "
only_with_files = true

[cmd_duration]
min_time = 2000
format = "[$duration]($style) "
style = "bold yellow"
```

### Power Configuration (Right Prompt)

```toml
# Add right prompt for less critical info
right_format = """$cmd_duration$time"""

[time]
disabled = false
format = "[$time]($style) "
style = "dimmed white"
time_format = "%H:%M"
```

---

## Powerlevel10k

**Config path:** `~/.p10k.zsh`

### Installation

```zsh
# With sheldon
[plugins.powerlevel10k]
github = "romkatv/powerlevel10k"

# Or direct clone
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git \
  ${XDG_DATA_HOME}/powerlevel10k
source ${XDG_DATA_HOME}/powerlevel10k/powerlevel10k.zsh-theme
```

### Configuration Wizard

```bash
# Run interactive configuration
p10k configure
```

### Key Settings (in .p10k.zsh)

```zsh
# Prompt elements (left)
typeset -g POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(
  dir                 # Current directory
  vcs                 # Git status
  prompt_char         # Prompt symbol
)

# Prompt elements (right)
typeset -g POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(
  status              # Exit code
  command_execution_time
  background_jobs
  node_version
  python_env
)

# Instant prompt (fast startup)
typeset -g POWERLEVEL9K_INSTANT_PROMPT=verbose

# Transient prompt (clean scrollback)
typeset -g POWERLEVEL9K_TRANSIENT_PROMPT=always
```

---

## Tmux + Neovim Integration

### True Color Pass-Through

```tmux
# tmux.conf — ensure true color works in neovim
set -g default-terminal "tmux-256color"
set -ag terminal-overrides ",*:Tc"
```

```lua
-- neovim init.lua — detect tmux
if vim.env.TMUX then
  vim.opt.termguicolors = true
end
```

### Seamless Navigation (vim-tmux-navigator)

```tmux
# tmux.conf
set -g @plugin 'christoomey/vim-tmux-navigator'
```

```lua
-- neovim plugin
return {
  "christoomey/vim-tmux-navigator",
  keys = {
    { "<C-h>", "<cmd>TmuxNavigateLeft<cr>" },
    { "<C-j>", "<cmd>TmuxNavigateDown<cr>" },
    { "<C-k>", "<cmd>TmuxNavigateUp<cr>" },
    { "<C-l>", "<cmd>TmuxNavigateRight<cr>" },
  },
}
```

### Clipboard Integration

```tmux
# tmux.conf — clipboard for macOS
set -g set-clipboard on
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "pbcopy"

# For Linux (xclip)
# bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "xclip -selection clipboard"
```

```lua
-- neovim — use system clipboard
vim.opt.clipboard = "unnamedplus"

-- OSC 52 clipboard (works over SSH/tmux)
-- Built-in since Neovim 0.10+
```

### Undercurl Support

```tmux
# tmux.conf — enable undercurl
set -as terminal-overrides ',*:Smulx=\E[4::%p1%dm'
set -as terminal-overrides ',*:Setulc=\E[58::2::%p1%{65536}%/%d::%p1%{256}%/%{255}%&%d::%p1%{255}%&%d%;m'
```
