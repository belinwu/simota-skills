# Shell Configuration Patterns

Reference for zsh, fish, and bash configuration best practices.

---

## Zsh Configuration

### Modular .zshrc Structure

```
~/.config/zsh/
├── .zshrc              # Entry point — sources modules in order
├── env.zsh             # Environment variables (PATH, XDG, LANG)
├── options.zsh         # setopt / unsetopt
├── aliases.zsh         # Aliases (safety, git, navigation)
├── functions.zsh       # Custom functions
├── plugins.zsh         # Plugin manager config (sheldon/zinit)
├── completions.zsh     # Completion setup
├── keybindings.zsh     # bindkey settings
└── local.zsh           # Machine-specific (gitignored)
```

**.zshrc entry point pattern:**
```zsh
# XDG Base Directory
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"
export ZDOTDIR="${XDG_CONFIG_HOME}/zsh"

# Source modules
for conf in "${ZDOTDIR}"/{env,options,aliases,functions,plugins,completions,keybindings}.zsh; do
  [[ -f "$conf" ]] && source "$conf"
done

# Machine-local overrides (not tracked in git)
[[ -f "${ZDOTDIR}/local.zsh" ]] && source "${ZDOTDIR}/local.zsh"
```

### Startup Performance

**Measurement:**
```bash
# Simple timing
time zsh -i -c exit

# Detailed profiling (add to top of .zshrc)
zmodload zsh/zprof
# ... (at bottom of .zshrc)
zprof
```

**Optimization techniques:**
```zsh
# Lazy compinit (only recompile once per day)
autoload -Uz compinit
if [[ -n ${ZDOTDIR}/.zcompdump(#qN.mh+24) ]]; then
  compinit
else
  compinit -C  # Skip security check
fi

# Compile zsh files for faster loading
zcompile "${ZDOTDIR}/.zshrc"

# Lazy load nvm (saves ~200ms)
lazy_nvm() {
  unset -f nvm node npm npx
  export NVM_DIR="$HOME/.nvm"
  [ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh"
}
nvm() { lazy_nvm; nvm "$@"; }
node() { lazy_nvm; node "$@"; }
npm() { lazy_nvm; npm "$@"; }
npx() { lazy_nvm; npx "$@"; }
```

**Target startup times:**
| Profile | Target | Acceptable |
|---------|--------|-----------|
| Minimal | <50ms | <100ms |
| Standard | <100ms | <200ms |
| Power | <200ms | <400ms |

### Plugin Managers

| Manager | Language | Config | Lazy Load | Speed |
|---------|----------|--------|-----------|-------|
| **sheldon** | Rust | TOML | Yes (defer) | Fast |
| **zinit** | Zsh | Zsh script | Yes (turbo) | Fast |
| **antidote** | Zsh | Text file | Yes | Medium |
| **oh-my-zsh** | Zsh | Zsh script | No | Slow |

**sheldon example (`~/.config/sheldon/plugins.toml`):**
```toml
shell = "zsh"

[plugins.zsh-defer]
github = "romkatv/zsh-defer"

[plugins.zsh-autosuggestions]
github = "zsh-users/zsh-autosuggestions"
apply = ["defer"]

[plugins.zsh-syntax-highlighting]
github = "zsh-users/zsh-syntax-highlighting"
apply = ["defer"]

[plugins.zsh-completions]
github = "zsh-users/zsh-completions"
apply = ["defer"]
```

**zinit example:**
```zsh
source "${XDG_DATA_HOME}/zinit/zinit.git/zinit.zsh"

# Turbo mode — load after prompt renders
zinit ice wait lucid
zinit light zsh-users/zsh-autosuggestions

zinit ice wait lucid atinit"zicompinit; zicdreplay"
zinit light zsh-users/zsh-syntax-highlighting

zinit ice wait lucid blockf
zinit light zsh-users/zsh-completions
```

### Essential Options

```zsh
# History
setopt HIST_EXPIRE_DUPS_FIRST  # Expire duplicates first
setopt HIST_IGNORE_DUPS        # Don't record duplicates
setopt HIST_IGNORE_SPACE       # Ignore commands starting with space
setopt SHARE_HISTORY           # Share history between sessions
HISTSIZE=50000
SAVEHIST=50000
HISTFILE="${XDG_DATA_HOME}/zsh/history"

# Directory navigation
setopt AUTO_CD                 # cd by typing directory name
setopt AUTO_PUSHD              # Push dirs to stack automatically
setopt PUSHD_IGNORE_DUPS       # No duplicate dirs in stack

# Globbing
setopt EXTENDED_GLOB           # Extended globbing (#, ~, ^)
setopt GLOB_DOTS               # Include dotfiles in globbing

# Correction
setopt CORRECT                 # Suggest corrections for commands
```

### Aliases Best Practices

```zsh
# Safety aliases
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Navigation
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

# ls (use eza if available)
if command -v eza &>/dev/null; then
  alias ls='eza --icons'
  alias ll='eza -la --icons --git'
  alias lt='eza --tree --level=2 --icons'
else
  alias ls='ls --color=auto'
  alias ll='ls -lah'
fi

# Git shortcuts
alias g='git'
alias ga='git add'
alias gc='git commit'
alias gco='git checkout'
alias gd='git diff'
alias gl='git log --oneline --graph'
alias gp='git push'
alias gs='git status'
alias gpl='git pull'
```

---

## Fish Configuration

### Structure
```
~/.config/fish/
├── config.fish          # Main config (like .zshrc)
├── fish_variables       # Universal variables (auto-managed)
├── conf.d/              # Auto-sourced config fragments
│   ├── aliases.fish
│   └── env.fish
├── functions/           # Autoloaded functions (one per file)
│   ├── fish_prompt.fish
│   └── mkcd.fish
└── completions/         # Custom completions
```

### Key Differences from Zsh
- No need for `export` — use `set -gx`
- Functions auto-load from `functions/` directory
- No plugin manager needed for basic use (Fisher for plugins)
- Built-in syntax highlighting and autosuggestions

```fish
# config.fish
if status is-interactive
  set -gx EDITOR nvim
  set -gx XDG_CONFIG_HOME $HOME/.config

  # Abbreviations (expand on space, unlike aliases)
  abbr -a g git
  abbr -a ga 'git add'
  abbr -a gc 'git commit'
end
```

---

## Bash Configuration

### Loading Order
```
Login shell:    /etc/profile → ~/.bash_profile → ~/.bash_login → ~/.profile
Interactive:    ~/.bashrc
Logout:         ~/.bash_logout
```

### Minimal .bashrc
```bash
# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# History
HISTCONTROL=ignoreboth
HISTSIZE=10000
HISTFILESIZE=20000
shopt -s histappend

# Navigation
shopt -s autocd cdspell dirspell

# Prompt (or use starship)
eval "$(starship init bash)"

# Aliases
[ -f ~/.bash_aliases ] && . ~/.bash_aliases
```

---

## Cross-Shell Patterns

### Environment Variables (shared)
```bash
# ~/.config/shell/env (sourced by all shells)
export EDITOR="nvim"
export VISUAL="nvim"
export PAGER="less"
export LANG="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"

# XDG Base Directory
export XDG_CONFIG_HOME="$HOME/.config"
export XDG_DATA_HOME="$HOME/.local/share"
export XDG_CACHE_HOME="$HOME/.cache"
export XDG_STATE_HOME="$HOME/.local/state"

# PATH additions
export PATH="$HOME/.local/bin:$PATH"
```

### Tool Version Management (mise)
```toml
# ~/.config/mise/config.toml
[tools]
node = "lts"
python = "3.12"
go = "latest"
```
