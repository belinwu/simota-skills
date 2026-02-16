# Editor Configuration Patterns

Reference for neovim and vim configuration best practices.

---

## Neovim Configuration

### Directory Structure

```
~/.config/nvim/
├── init.lua                  # Entry point
├── lazy-lock.json            # Plugin lockfile (auto-generated)
└── lua/
    ├── config/
    │   ├── autocmds.lua      # Autocommands
    │   ├── keymaps.lua       # Key mappings
    │   ├── lazy.lua          # Plugin manager bootstrap
    │   └── options.lua       # vim.opt settings
    └── plugins/
        ├── colorscheme.lua   # Theme
        ├── completion.lua    # nvim-cmp / blink.cmp
        ├── editor.lua        # Editor enhancements (mini.pairs, surround)
        ├── lsp.lua           # LSP configuration
        ├── telescope.lua     # Fuzzy finder
        ├── treesitter.lua    # Syntax highlighting
        └── ui.lua            # UI elements (statusline, bufferline)
```

### init.lua Entry Point

```lua
-- Bootstrap lazy.nvim and load configuration
require("config.options")
require("config.lazy")

-- Load after plugins (via lazy.nvim event)
vim.api.nvim_create_autocmd("User", {
  pattern = "VeryLazy",
  callback = function()
    require("config.autocmds")
    require("config.keymaps")
  end,
})
```

### Core Options

```lua
-- lua/config/options.lua
local opt = vim.opt

-- Line numbers
opt.number = true
opt.relativenumber = true

-- Indentation
opt.tabstop = 2
opt.shiftwidth = 2
opt.expandtab = true
opt.smartindent = true

-- Search
opt.ignorecase = true
opt.smartcase = true
opt.hlsearch = false
opt.incsearch = true

-- UI
opt.termguicolors = true
opt.signcolumn = "yes"
opt.cursorline = true
opt.scrolloff = 8
opt.sidescrolloff = 8
opt.wrap = false

-- Files
opt.swapfile = false
opt.backup = false
opt.undofile = true
opt.undodir = vim.fn.stdpath("state") .. "/undo"

-- Split behavior
opt.splitright = true
opt.splitbelow = true

-- Misc
opt.updatetime = 250
opt.timeoutlen = 300
opt.clipboard = "unnamedplus"
opt.mouse = "a"
opt.completeopt = "menu,menuone,noselect"
```

### lazy.nvim Bootstrap

```lua
-- lua/config/lazy.lua
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git", "clone", "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable", lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup("plugins", {
  defaults = { lazy = true },
  install = { colorscheme = { "catppuccin" } },
  checker = { enabled = true, notify = false },
  change_detection = { notify = false },
  performance = {
    rtp = {
      disabled_plugins = {
        "gzip", "matchit", "matchparen",
        "netrwPlugin", "tarPlugin", "tohtml",
        "tutor", "zipPlugin",
      },
    },
  },
})
```

### Key Mapping Design

```lua
-- lua/config/keymaps.lua
local map = vim.keymap.set

-- Leader key
vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- Better window navigation
map("n", "<C-h>", "<C-w>h", { desc = "Go to left window" })
map("n", "<C-j>", "<C-w>j", { desc = "Go to lower window" })
map("n", "<C-k>", "<C-w>k", { desc = "Go to upper window" })
map("n", "<C-l>", "<C-w>l", { desc = "Go to right window" })

-- Buffer navigation
map("n", "<S-h>", "<cmd>bprevious<cr>", { desc = "Prev buffer" })
map("n", "<S-l>", "<cmd>bnext<cr>", { desc = "Next buffer" })

-- Move lines
map("v", "J", ":m '>+1<cr>gv=gv", { desc = "Move down" })
map("v", "K", ":m '<-2<cr>gv=gv", { desc = "Move up" })

-- Better indenting
map("v", "<", "<gv")
map("v", ">", ">gv")

-- Diagnostics
map("n", "[d", vim.diagnostic.goto_prev, { desc = "Prev diagnostic" })
map("n", "]d", vim.diagnostic.goto_next, { desc = "Next diagnostic" })

-- Search and replace (current word)
map("n", "<leader>sr", [[:%s/\<<C-r><C-w>\>/<C-r><C-w>/gI<Left><Left><Left>]], { desc = "Search and replace" })
```

### LSP Configuration

```lua
-- lua/plugins/lsp.lua
return {
  {
    "neovim/nvim-lspconfig",
    event = { "BufReadPre", "BufNewFile" },
    dependencies = {
      "mason.nvim",
      "mason-lspconfig.nvim",
    },
    config = function()
      -- Diagnostics
      vim.diagnostic.config({
        virtual_text = { spacing = 4, prefix = "●" },
        signs = true,
        underline = true,
        update_in_insert = false,
        severity_sort = true,
      })

      -- LSP keymaps (on attach)
      vim.api.nvim_create_autocmd("LspAttach", {
        callback = function(event)
          local map = function(keys, func, desc)
            vim.keymap.set("n", keys, func, { buffer = event.buf, desc = "LSP: " .. desc })
          end
          map("gd", vim.lsp.buf.definition, "Go to definition")
          map("gr", vim.lsp.buf.references, "Go to references")
          map("gI", vim.lsp.buf.implementation, "Go to implementation")
          map("K", vim.lsp.buf.hover, "Hover documentation")
          map("<leader>ca", vim.lsp.buf.code_action, "Code action")
          map("<leader>cr", vim.lsp.buf.rename, "Rename symbol")
        end,
      })
    end,
  },
  {
    "williamboman/mason.nvim",
    cmd = "Mason",
    opts = {},
  },
  {
    "williamboman/mason-lspconfig.nvim",
    opts = {
      ensure_installed = {
        "lua_ls",
        "ts_ls",
        "rust_analyzer",
      },
      automatic_installation = true,
    },
  },
}
```

### Essential Plugin Specs

```lua
-- lua/plugins/treesitter.lua
return {
  "nvim-treesitter/nvim-treesitter",
  build = ":TSUpdate",
  event = { "BufReadPost", "BufNewFile" },
  opts = {
    ensure_installed = {
      "lua", "vim", "vimdoc", "query",
      "typescript", "javascript", "tsx",
      "python", "rust", "go",
      "json", "yaml", "toml", "markdown",
      "bash", "html", "css",
    },
    highlight = { enable = true },
    indent = { enable = true },
    incremental_selection = {
      enable = true,
      keymaps = {
        init_selection = "<C-space>",
        node_incremental = "<C-space>",
        scope_incremental = false,
        node_decremental = "<bs>",
      },
    },
  },
}

-- lua/plugins/telescope.lua
return {
  "nvim-telescope/telescope.nvim",
  cmd = "Telescope",
  keys = {
    { "<leader>ff", "<cmd>Telescope find_files<cr>", desc = "Find files" },
    { "<leader>fg", "<cmd>Telescope live_grep<cr>", desc = "Live grep" },
    { "<leader>fb", "<cmd>Telescope buffers<cr>", desc = "Buffers" },
    { "<leader>fh", "<cmd>Telescope help_tags<cr>", desc = "Help" },
    { "<leader>fr", "<cmd>Telescope oldfiles<cr>", desc = "Recent files" },
  },
  dependencies = { "nvim-lua/plenary.nvim" },
  opts = {
    defaults = {
      prompt_prefix = "   ",
      selection_caret = " ",
    },
  },
}
```

---

## Vim Configuration

### Minimal .vimrc

```vim
" Sensible defaults
set nocompatible
filetype plugin indent on
syntax enable

" UI
set number relativenumber
set cursorline
set signcolumn=yes
set scrolloff=8
set nowrap
set termguicolors

" Indentation
set tabstop=2 shiftwidth=2 expandtab
set smartindent autoindent

" Search
set ignorecase smartcase
set incsearch nohlsearch

" Files
set noswapfile nobackup
set undofile undodir=~/.vim/undo

" Splits
set splitright splitbelow

" Misc
set updatetime=250
set clipboard=unnamedplus
set mouse=a
set wildmenu
set laststatus=2

" Leader key
let mapleader = " "
```

### vim-plug Setup

```vim
" Auto-install vim-plug
let data_dir = has('nvim') ? stdpath('data') . '/site' : '~/.vim'
if empty(glob(data_dir . '/autoload/plug.vim'))
  silent execute '!curl -fLo '.data_dir.'/autoload/plug.vim --create-dirs
    \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

call plug#begin()
Plug 'catppuccin/vim', { 'as': 'catppuccin' }
Plug 'tpope/vim-surround'
Plug 'tpope/vim-commentary'
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'
call plug#end()

colorscheme catppuccin_mocha
```

---

## Keymap Design Principles

1. **Mnemonic bindings**: `<leader>f` = find, `<leader>g` = git, `<leader>l` = LSP
2. **Consistency**: Same keys for same actions across plugins
3. **Discoverability**: Use which-key plugin to show available keymaps
4. **Avoid conflicts**: Check existing mappings with `:map <key>`
5. **Progressive disclosure**: Basic keys first, advanced behind leader

### Common Leader Key Namespace

| Prefix | Domain | Examples |
|--------|--------|---------|
| `<leader>f` | Find/Files | `ff` files, `fg` grep, `fb` buffers |
| `<leader>g` | Git | `gs` status, `gb` blame, `gd` diff |
| `<leader>l` | LSP | `lr` rename, `la` action, `ld` definition |
| `<leader>b` | Buffer | `bd` delete, `bp` prev, `bn` next |
| `<leader>w` | Window | `wv` vsplit, `ws` hsplit, `wq` close |
| `<leader>t` | Toggle | `tt` terminal, `te` explorer, `tz` zen |

---

## Minimal vs Full Configuration

| Aspect | Minimal | Standard | Full |
|--------|---------|----------|------|
| Plugin count | 0-5 | 10-20 | 30-50+ |
| LSP | None | Primary language | Multi-language |
| Completion | Built-in | nvim-cmp | nvim-cmp + AI |
| File finder | Built-in | telescope | telescope + extensions |
| Startup time | <50ms | <100ms | <200ms |
| Use case | Quick edits | Daily driver | IDE replacement |

---

## Neovim 0.10+ Features

### Native Snippets (`vim.snippet`)

```lua
-- Built-in snippet expansion (no plugin required for basic use)
vim.snippet.expand("function ${1:name}(${2:params})\n\t${0}\nend")

-- Jump between snippet placeholders
vim.keymap.set({ "i", "s" }, "<Tab>", function()
  if vim.snippet.active({ direction = 1 }) then
    return "<cmd>lua vim.snippet.jump(1)<cr>"
  end
  return "<Tab>"
end, { expr = true })

vim.keymap.set({ "i", "s" }, "<S-Tab>", function()
  if vim.snippet.active({ direction = -1 }) then
    return "<cmd>lua vim.snippet.jump(-1)<cr>"
  end
  return "<S-Tab>"
end, { expr = true })
```

### OSC 52 Clipboard

```lua
-- Native clipboard over SSH/tmux via OSC 52 (no xclip/pbcopy needed)
-- Enabled by default in 0.10+ when $SSH_TTY is set
-- Works with ghostty, kitty, wezterm, alacritty, tmux 3.3+
vim.opt.clipboard = "unnamedplus"
-- No additional configuration needed for remote sessions
```

### Built-in Comment Toggling (`gc`)

```lua
-- Native in Neovim 0.10+ (no vim-commentary or Comment.nvim needed)
-- gc{motion}  — toggle comment
-- gcc         — toggle comment on current line
-- gc          — toggle comment in visual mode
-- Respects commentstring from treesitter/filetype
```

### Default Colorscheme Improvements

Neovim 0.10+ ships with an improved default colorscheme and `vim.hl` namespace for highlight management. Treesitter highlighting is enabled by default for supported filetypes.

---

## blink.cmp (Alternative to nvim-cmp)

### Comparison with nvim-cmp

| Aspect | nvim-cmp | blink.cmp |
|--------|----------|-----------|
| Architecture | Lua-based, multi-source | Rust core, async-first |
| Performance | Good (can lag with many sources) | Faster (Rust fuzzy matching) |
| Configuration | Verbose, many plugins | Simpler, fewer dependencies |
| Source ecosystem | Large (30+ source plugins) | Growing (compatible adapter) |
| Maturity | Stable, widely adopted | Newer, rapidly evolving |
| Snippet support | Via cmp-luasnip/cmp-vsnip | Built-in vim.snippet |
| Ghost text | Via plugin | Built-in |

### Basic blink.cmp Configuration

```lua
-- lua/plugins/completion.lua
return {
  "saghen/blink.cmp",
  version = "*",
  event = "InsertEnter",
  dependencies = {
    "rafamadriz/friendly-snippets",
  },
  opts = {
    keymap = {
      preset = "default",
      ["<C-space>"] = { "show", "show_documentation", "hide_documentation" },
      ["<C-e>"] = { "cancel", "fallback" },
      ["<CR>"] = { "accept", "fallback" },
      ["<Tab>"] = { "snippet_forward", "select_next", "fallback" },
      ["<S-Tab>"] = { "snippet_backward", "select_prev", "fallback" },
    },
    appearance = {
      nerd_font_variant = "mono",
    },
    sources = {
      default = { "lsp", "path", "snippets", "buffer" },
    },
    signature = { enabled = true },
  },
}
```

### When to Choose blink.cmp

- Prefer **blink.cmp** for new setups (simpler config, better performance)
- Prefer **nvim-cmp** if you need specific source plugins not yet ported
- Both work well with mason.nvim and LSP

---

## Zed Editor Configuration

### Overview

Zed is a GPU-accelerated editor written in Rust. Hearth provides minimal support — Neovim remains the recommended editor for power users.

### Configuration (`~/.config/zed/settings.json`)

```jsonc
{
  // Theme
  "theme": {
    "mode": "dark",
    "dark": "Catppuccin Mocha",
    "light": "Catppuccin Latte"
  },

  // Font
  "buffer_font_family": "JetBrains Mono",
  "buffer_font_size": 14,
  "ui_font_size": 14,

  // Editor behavior
  "tab_size": 2,
  "hard_tabs": false,
  "format_on_save": "on",
  "autosave": { "after_delay": { "milliseconds": 1000 } },

  // Vim mode (optional)
  "vim_mode": true,
  "relative_line_numbers": true,

  // Terminal
  "terminal": {
    "font_family": "JetBrains Mono",
    "font_size": 14
  },

  // Telemetry
  "telemetry": {
    "diagnostics": false,
    "metrics": false
  }
}
```

### Zed Keymap (`~/.config/zed/keymap.json`)

```jsonc
[
  {
    "context": "Editor && VimNormal",
    "bindings": {
      "space f f": "file_finder::Toggle",
      "space f g": "search::SelectAllMatches",
      "space e": "workspace::ToggleLeftDock"
    }
  }
]
```

### LSP in Zed

Zed has built-in LSP support — no mason.nvim equivalent needed. Language servers are auto-installed on first use. Custom LSP configuration:

```jsonc
{
  "lsp": {
    "rust-analyzer": {
      "initialization_options": {
        "check": { "command": "clippy" }
      }
    }
  }
}
```
