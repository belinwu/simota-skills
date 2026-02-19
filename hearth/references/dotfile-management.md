# Dotfile Management Strategies

Reference for dotfile management tools, Brewfile management, and XDG Base Directory compliance.

---

## GNU Stow (Recommended for Single Machine)

### Overview

GNU Stow is a symlink farm manager that creates symlinks from a central directory to `$HOME`. Simple, transparent, and requires no special tooling beyond `stow` itself.

### Directory Structure Convention

```
~/dotfiles/
├── zsh/
│   ├── .zshrc                    # → ~/.zshrc
│   └── .config/
│       └── zsh/
│           ├── aliases.zsh       # → ~/.config/zsh/aliases.zsh
│           └── functions.zsh     # → ~/.config/zsh/functions.zsh
├── nvim/
│   └── .config/
│       └── nvim/
│           ├── init.lua          # → ~/.config/nvim/init.lua
│           └── lua/              # → ~/.config/nvim/lua/
├── ghostty/
│   └── .config/
│       └── ghostty/
...
```

**Key Rule:** The directory structure inside each package mirrors `$HOME` exactly.

### Commands

```bash
# Install (create symlinks for a package)
stow -d ~/dotfiles -t ~ zsh

# Install all packages
cd ~/dotfiles && stow */

# Uninstall (remove symlinks)
stow -d ~/dotfiles -t ~ -D zsh

# Restow (unlink then relink — use after restructuring)
stow -d ~/dotfiles -t ~ -R zsh

# Dry run (preview what would happen)
stow -d ~/dotfiles -t ~ -n -v zsh

# ...
```

### .stow-local-ignore

```
# ~/dotfiles/.stow-local-ignore
\.git
\.gitignore
\.gitmodules
README\.md
LICENSE
^\.DS_Store
```

### Multi-Machine with Stow

```
~/dotfiles/
├── zsh/              # Shared across all machines
├── nvim/             # Shared
├── zsh-work/         # Work machine only
├── zsh-personal/     # Personal machine only
└── linux-specific/   # Linux only
```

```bash
# On work machine:
cd ~/dotfiles && stow zsh nvim zsh-work

# On personal machine:
cd ~/dotfiles && stow zsh nvim zsh-personal
```

---

## chezmoi (Recommended for Multi-Machine)

### Overview

chezmoi manages dotfiles across multiple machines with templates, secrets integration, and automatic encryption. Best when configs differ between machines (OS, hostname, work/personal).

### Initialization Workflow

```bash
# Initialize (creates ~/.local/share/chezmoi/)
chezmoi init

# Add a file to management
chezmoi add ~/.zshrc

# Edit managed file
chezmoi edit ~/.zshrc

# Preview changes
chezmoi diff

# Apply changes to $HOME
chezmoi apply

# ...
```

### Go Template Syntax

```
# ~/.local/share/chezmoi/dot_zshrc.tmpl

# Shared configuration
export EDITOR="nvim"
export LANG="en_US.UTF-8"

{{ if eq .chezmoi.os "darwin" -}}
# macOS specific
export HOMEBREW_PREFIX="/opt/homebrew"
eval "$($HOMEBREW_PREFIX/bin/brew shellenv)"
{{ else if eq .chezmoi.os "linux" -}}
# Linux specific
export HOMEBREW_PREFIX="/home/linuxbrew/.linuxbrew"
{{ end -}}

...
```

### chezmoi Config (`.chezmoi.toml.tmpl`)

```toml
[data]
    name = "Your Name"
    email = "{{ if eq .chezmoi.hostname "work-laptop" }}work@company.com{{ else }}personal@email.com{{ end }}"
    personal = {{ not (eq .chezmoi.hostname "work-laptop") }}
```

### Secret Management

```
# 1Password integration
{{ onepasswordRead "op://vault/item/field" }}

# Bitwarden integration
{{ (bitwarden "item" "My SSH Key").notes }}

# Age encryption
chezmoi add --encrypt ~/.ssh/id_rsa

# Keychain (macOS)
{{ (keyring "service-name" "username") }}
```

### File Naming Conventions

| Prefix | Meaning | Example |
|--------|---------|---------|
| `dot_` | Leading dot | `dot_zshrc` → `.zshrc` |
| `private_` | Permission 0600 | `private_dot_ssh/` |
| `executable_` | Permission +x | `executable_dot_local/bin/script` |
| `modify_` | Modify existing | `modify_dot_zshrc` |
| `create_` | Create if missing | `create_dot_gitconfig` |
| `symlink_` | Create symlink | `symlink_dot_config/nvim` |
| `.tmpl` suffix | Template file | `dot_zshrc.tmpl` |

---

## yadm

### Overview

yadm (Yet Another Dotfiles Manager) wraps Git to manage dotfiles directly in `$HOME`. Feels like regular Git — no symlinks, no separate directory.

### Basic Workflow

```bash
# Initialize
yadm init
yadm add ~/.zshrc ~/.config/nvim/init.lua
yadm commit -m "initial dotfiles"
yadm remote add origin <repo-url>
yadm push -u origin main

# Clone on new machine
yadm clone <repo-url>
```

### Alt Files (Machine-Specific)

```
# Files are selected based on OS, hostname, user
~/.config/zsh/aliases.zsh##os.Darwin     # macOS
~/.config/zsh/aliases.zsh##os.Linux      # Linux
~/.config/zsh/aliases.zsh##h.work-laptop # Specific host
~/.config/zsh/aliases.zsh##default       # Fallback
```

### Bootstrap Script

```bash
# ~/.config/yadm/bootstrap (auto-runs on clone)
#!/bin/bash

# Install Homebrew if missing
if ! command -v brew &>/dev/null; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install packages
brew bundle --file="$HOME/Brewfile"

# Set up Neovim
nvim --headless "+Lazy! sync" +qa
```

---

## Bare Git Repo

### Overview

Minimal approach using a bare Git repository. No extra tools needed — just Git.

### Setup

```bash
# Initialize bare repo
git init --bare $HOME/.dotfiles

# Add alias to shell config
alias dotfiles='git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'

# Hide untracked files (critical — prevents $HOME listing)
dotfiles config --local status.showUntrackedFiles no
```

### Basic Workflow

```bash
# Add and commit
dotfiles add ~/.zshrc
dotfiles commit -m "add zshrc"
dotfiles push

# Clone on new machine
git clone --bare <repo-url> $HOME/.dotfiles
alias dotfiles='git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
dotfiles checkout
```

**Limitation:** No templates, no secrets management, no machine-specific files. Best for simple, single-machine setups.

---

## Brewfile Management

### Structure

```ruby
# ~/Brewfile

# Taps (third-party repositories)
tap "homebrew/bundle"
tap "homebrew/cask-fonts"

# CLI tools (formulae)
brew "git"
brew "neovim"
brew "tmux"
brew "starship"
brew "sheldon"
brew "mise"
brew "ripgrep"
brew "fd"
# ...
```

### Commands

```bash
# Install everything from Brewfile
brew bundle

# Install from specific file
brew bundle --file=~/dotfiles/Brewfile

# Dump current state to Brewfile
brew bundle dump --force

# Check what would be installed
brew bundle check

# Clean up (remove unlisted packages)
brew bundle cleanup          # Dry run
brew bundle cleanup --force  # Actually remove
# ...
```

### Tips

- Keep `Brewfile` in dotfiles repo for reproducibility
- Use `brew bundle dump --describe` to add comments
- Split into `Brewfile` (core) + `Brewfile.work` (work-specific) if needed
- Run `brew bundle check` in CI/bootstrap scripts

---

## XDG Base Directory Specification

### Variables and Defaults

| Variable | Default | Purpose |
|----------|---------|---------|
| `XDG_CONFIG_HOME` | `~/.config` | User-specific config files |
| `XDG_DATA_HOME` | `~/.local/share` | User-specific data files |
| `XDG_STATE_HOME` | `~/.local/state` | User-specific state (logs, history) |
| `XDG_CACHE_HOME` | `~/.cache` | User-specific non-essential cache |
| `XDG_RUNTIME_DIR` | `/run/user/$UID` | Runtime files (sockets, pipes) |

### Tool XDG Compliance

| Tool | XDG Support | Config Location |
|------|------------|-----------------|
| neovim | Native | `$XDG_CONFIG_HOME/nvim/` |
| ghostty | Native | `$XDG_CONFIG_HOME/ghostty/` |
| alacritty | Native | `$XDG_CONFIG_HOME/alacritty/` |
| kitty | Native | `$XDG_CONFIG_HOME/kitty/` |
| wezterm | Native | `$XDG_CONFIG_HOME/wezterm/` |
| tmux | Since 3.1 | `$XDG_CONFIG_HOME/tmux/tmux.conf` |
| starship | Native | `$XDG_CONFIG_HOME/starship.toml` |
| git | Partial | `$XDG_CONFIG_HOME/git/config` (but `~/.gitconfig` takes precedence) |
| zsh | Manual | Set `ZDOTDIR=$XDG_CONFIG_HOME/zsh` in `~/.zshenv` |
| mise | Native | `$XDG_CONFIG_HOME/mise/` |
| sheldon | Native | `$XDG_CONFIG_HOME/sheldon/` |
| bash | No | `~/.bashrc`, `~/.bash_profile` only |

### Migration Steps

```bash
# 1. Set XDG variables in ~/.zshenv (loaded before .zshrc)
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
export XDG_STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"

# 2. Move zsh config to XDG
export ZDOTDIR="$XDG_CONFIG_HOME/zsh"
# Then move .zshrc → $ZDOTDIR/.zshrc

# 3. Create required directories
mkdir -p "$XDG_CONFIG_HOME" "$XDG_DATA_HOME" "$XDG_STATE_HOME" "$XDG_CACHE_HOME"

# 4. Move tool configs as needed
# Most modern tools already use ~/.config/ by default
```

---

## Selection Guide

| Scenario | Recommended | Reason |
|----------|-------------|--------|
| Single machine, simple setup | **GNU Stow** | Transparent symlinks, zero learning curve |
| Multiple machines, different configs | **chezmoi** | Templates, secrets, conditional logic |
| Git power user, minimal tooling | **Bare git repo** | No extra dependencies |
| Already using yadm | **yadm** | Familiar Git workflow with alt files |
| Team/shared dotfiles | **chezmoi** | Template variables per person/machine |
| Quick start, no manager | **Manual symlinks** | `ln -sf` for a few files |

### Decision Flow

```
Need machine-specific configs?
├── Yes → Need secrets management?
│   ├── Yes → chezmoi
│   └── No → chezmoi or yadm
└── No → Need more than ~10 config files?
    ├── Yes → GNU Stow
    └── No → Manual symlinks or bare git
```
