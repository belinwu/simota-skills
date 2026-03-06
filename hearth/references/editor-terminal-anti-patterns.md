# Editor & Terminal Configuration Anti-Patterns

> Neovim/Vim設定、ターミナルエミュレータ、tmux設定、プラグイン管理の失敗パターン

## 1. Neovim設定 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **NV-01** | **Distro Dependency（ディストロ依存）** | NvChad/LunarVim/SpaceVimに全面依存 | カスタマイズ困難、ディストロ更新で設定崩壊 | kickstart.nvimベースで自前ビルド、理解してから採用 |
| **NV-02** | **Monolithic init.lua（モノリスinit.lua）** | 500行超のinit.luaに全設定を一括記述 | 変更影響が不明、プラグイン間の依存が見えない | `lua/config/`以下にモジュール分割（keymaps/options/plugins/lsp） |
| **NV-03** | **Eager Plugin Loading（全プラグイン即時読込）** | lazy.nvimの遅延ロード機能を未活用 | 起動時間300ms超、`:Lazy profile`で全プラグインがstart時読込 | `event`/`cmd`/`ft`/`keys`で適切に遅延、VeryLazyイベント活用 |
| **NV-04** | **Deprecated API Usage（非推奨API使用）** | vim.cmd()でVimscript依存、vim.api.nvim_set_keymap等の旧API | Neovim 0.10+の新機能が使えない、パフォーマンス低下 | `vim.keymap.set`/`vim.hl`/native snippet/built-in comment使用 |
| **NV-05** | **Excessive Keymaps（過剰キーマップ）** | 大量のカスタムキーマップがデフォルトと競合 | 標準操作が壊れる、学習コスト増大 | `<Plug>`マッピング活用、`which-key`で発見性確保 |
| **NV-06** | **No Health Check（ヘルスチェック未実施）** | 設定変更後に`:checkhealth`を実行しない | LSP/treesitter/provider問題が検出されない | `nvim --headless "+checkhealth" +qa`をVERIFYフェーズに統合 |
| **NV-07** | **Plugin setup() Ceremony（setup()儀式）** | 全プラグインに空の`setup({})`呼出を追加 | 不要な初期化コード、lazy.nvimのopts={}で自動呼出可能 | lazy.nvimの`opts`フィールド活用、setup不要なプラグインは省略 |

---

## 2. ターミナルエミュレータのアンチパターン

```
ターミナル設定の失敗:

  ❌ TERM Variable Mismatch（TERM変数不一致）:
    → GhosttyでTERM=xterm-ghosttyだがSSH先にterminfoなし
    → リモートで "Error opening terminal: xterm-ghostty"
    → 対策: infocmp -x xterm-ghostty | ssh remote 'tic -x -'

  ❌ Font Fallback Ignorance（フォントフォールバック無視）:
    → Nerd Fontのみ指定し、フォールバック未設定
    → アイコン・記号が豆腐（□）表示
    → 対策: font-family = "JetBrains Mono Nerd Font", "Symbols Nerd Font"

  ❌ Terminal Tabs as Persistence（タブ＝永続性の誤解）:
    → ターミナルタブでワークスペースを構築
    → 再起動で全レイアウト・コンテキスト消失
    → 対策: tmuxセッションで永続化、タブはUI便利機能のみ

  ❌ Ghostty+tmux Keyboard Protocol Conflict:
    → tmuxがkitty keyboardプロトコル未サポート
    → 修飾キー付きキーバインドが正しく伝達されない
    → 対策: tmux.confでextended-keysを有効化、制限を理解して設計

  ❌ No Shell Integration（シェル統合未設定）:
    → Ghosttyのシェル統合を未活用
    → プロンプトマーク、コマンドジャンプ機能が使えない
    → 対策: Ghostty 1.0+は自動検出するが、手動設定で確実に有効化

  ❌ Over-Configuration（過剰設定）:
    → ターミナルに100+行の設定を追加
    → デフォルトで十分な機能まで上書き、互換性問題
    → 対策: Ghosttyのミニマル設定哲学に従う（font + theme + 少数のkeybind）
```

---

## 3. tmux設定のアンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **TM-01** | **Default Prefix Key（デフォルトプレフィックス）** | C-bプレフィックスを変更しない | bキーが遠い、bash/zshのC-b（カーソル後退）と競合 | C-a or C-spaceに変更 |
| **TM-02** | **Zero-Based Indexing（ゼロ始まりインデックス）** | ウィンドウ/ペインが0始まり | 0キーがキーボード端、1-9の流れと不連続 | `set -g base-index 1` + `set -g pane-base-index 1` |
| **TM-03** | **Escape Delay（エスケープ遅延）** | escape-timeがデフォルト500ms | Vim/Neovimでモード切替が遅延 | `set -sg escape-time 0` |
| **TM-04** | **Deprecated Options（非推奨オプション）** | 旧オプション名を使用（例: window-status-current-bg） | tmux起動時にエラー/警告 | `-style`系オプションに移行（例: window-status-current-style） |
| **TM-05** | **Global tmux Auto-Start（グローバル自動起動）** | .zshrcで全シェルにtmux自動起動 | システムシェル・スクリプト実行にも干渉 | 特定ターミナル（Ghostty）でのみ自動起動、条件分岐 |
| **TM-06** | **No Session Naming（セッション名なし）** | `tmux new`で番号セッションのみ作成 | セッション一覧が `0, 1, 2...` で用途不明 | `tmux new -s project-name`で意味のある名前を付与 |
| **TM-07** | **TPM at Wrong Position（TPM位置エラー）** | tmux.confの途中でTPMを初期化 | プラグインが正しく読み込まれない | `run '~/.tmux/plugins/tpm/tpm'`はtmux.confの最後に配置 |

---

## 4. Neovim補完・LSP設定の罠

```
補完・LSP設定の失敗:

  ❌ nvim-cmp on New Setup（新規設定でnvim-cmp）:
    → 新規セットアップでnvim-cmp（冗長な設定）を採用
    → blink.cmp（Rust製、設定シンプル）の方が高速
    → 対策: 新規 → blink.cmp推奨、既存nvim-cmp → 移行不要

  ❌ Mason Without Lockfile（Masonロックファイルなし）:
    → mason.nvimでLSPサーバーをインストールするがバージョン未固定
    → マシン間でLSPバージョンが異なり挙動差異
    → 対策: mason-lock.nvimでロックファイル管理

  ❌ Treesitter Auto-Install All（Treesitter全言語自動インストール）:
    → ensure_installedに大量の言語パーサーを列挙
    → 初回起動が5分超、使わない言語のパーサーが蓄積
    → 対策: 実際に使う言語のみ列挙、auto_install = trueで必要時インストール

  ❌ Native Feature Ignorance（ネイティブ機能無視）:
    → Neovim 0.10+のビルトイン機能を知らずプラグインで代替
    → Comment.nvim不要（gcc/gcビルトイン）、clipboard不要（OSC 52）
    → 対策: `:help news`で新バージョンの機能確認、不要プラグイン削除

  ❌ No Lazy Event Optimization（遅延イベント未最適化）:
    → lazy.nvimのevent設定なしで全プラグインstartupロード
    → 起動時間がプラグイン数に比例して増加
    → 対策: UI系→VeryLazy、ファイル系→BufReadPre、言語系→ft指定
```

---

## 5. Hearth との連携

```
Hearth での活用:
  1. SCAN フェーズで NV-01〜07 のNeovim設定スクリーニング
  2. PLAN フェーズでターミナル設定の品質チェック
  3. CRAFT フェーズで TM-01〜07 のtmux設計確認
  4. VERIFY フェーズで :checkhealth と起動時間確認

品質ゲート:
  - NvChad/LunarVim検出 → kickstart.nvimベース移行提案（NV-01 防止）
  - init.lua 300行超 → モジュール分割提案（NV-02 防止）
  - :Lazy profile全プラグインstart → 遅延ロード設計（NV-03 防止）
  - tmux escape-time未設定 → 0ms設定追加（TM-03 防止）
  - tmux C-bプレフィックス → C-a/C-space提案（TM-01 防止）
  - TERM変数mismatch → terminfo転送手順提示（Terminal 防止）
  - Comment.nvimプラグイン+Neovim 0.10 → 削除提案（NV補完 防止）
```

**Source:** [nvim-best-practices: DOs and DON'Ts](https://github.com/lumen-oss/nvim-best-practices) · [DEV.to: Terminal Setup Anti-Patterns](https://dev.to/ssh_exe/a-lot-of-terminal-setups-look-productive-until-you-restart-your-machine-onh) · [sterba.dev: Replacing tmux with Ghostty](https://sterba.dev/posts/replacing-tmux/) · [darren.sh: Dev Terminal Setup](https://darren.sh/cli/dev-term-setup/) · [tmux.info: Configuration Guide](https://tmux.info/docs/configuration)
