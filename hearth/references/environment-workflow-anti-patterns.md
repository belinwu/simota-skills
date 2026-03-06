# Environment & Workflow Anti-Patterns

> 開発環境の再現性、ツール選定、macOS設定、パッケージ管理、ワークフロー統合の失敗パターン

## 1. 環境再現性 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **EN-01** | **Non-Reproducible Environment（再現不能環境）** | 設定がコード化されず手動構築 | 新マシンセットアップに1日、「前のマシンと違う」 | dotfileリポジトリ + Brewfile + install.sh で全自動化 |
| **EN-02** | **Version Manager Sprawl（バージョンマネージャ散在）** | nvm + pyenv + rbenv + goenv を個別インストール | 各ツールのinit処理で起動500ms超、管理コスト増 | mise（旧rtx）に統合: 1ツールで全言語管理、Rust製高速 |
| **EN-03** | **Brewfile Unmanaged（Brewfile未管理）** | Homebrewパッケージをbrew installで個別追加 | 新マシンで何をインストールすべきか不明 | `brew bundle dump --describe`で定期同期、dotfileリポジトリに含める |
| **EN-04** | **No OS Detection（OS検出なし）** | macOS/Linux差異を無視してパスをハードコード | dotfile共有時にエラー、パスが見つからない | `uname -s`/`$OSTYPE`で分岐、chezmoi templateでOS条件 |
| **EN-05** | **Tool Version Drift（ツールバージョン乖離）** | プロジェクト要求のNode/Python/Rubyバージョンがグローバルと不一致 | ローカルでは動くがCIで失敗 | `.tool-versions`/`.mise.toml`でプロジェクト別バージョン固定 |
| **EN-06** | **Manual Font Installation（手動フォントインストール）** | Nerd Fontを手動ダウンロード+インストール | 新マシンでアイコンが豆腐表示 | Brewfileに`cask "font-jetbrains-mono-nerd-font"`で自動化 |
| **EN-07** | **No Environment Validation（環境検証なし）** | セットアップ後に動作確認をしない | 設定ミスが数日後に発覚 | 検証スクリプト: 各ツールのバージョン確認+構文チェック+接続テスト |

---

## 2. macOS設定のアンチパターン

```
macOS設定の失敗:

  ❌ Undocumented defaults write（文書化なしdefaults write）:
    → defaults writeコマンドを理解せずにコピペ実行
    → 意図しないシステム動作変更、復元方法不明
    → 対策: 全defaults writeにコメントで目的記述、defaults readで事前確認

  ❌ No Restart Warning（再起動警告なし）:
    → defaults write後にFinder/Dock再起動が必要なことを伝えない
    → 設定が反映されず「効かない」と混乱
    → 対策: `killall Finder`/`killall Dock`を必要に応じて案内

  ❌ Aggressive System Modification（過激なシステム変更）:
    → セキュリティ系設定（SIP/Gatekeeper）を無効化
    → セキュリティリスク増大、macOSアップデートで問題
    → 対策: セキュリティ設定変更は明確な理由+確認必須

  ❌ Karabiner Over-Complexity（Karabiner過剰複雑化）:
    → 50+ルールのkarabiner.jsonでキーリマップ
    → デバッグ困難、他のアプリとの競合多発
    → 対策: 最小限のルール（Caps→Hyper、基本的なVim arrows）のみ

  ❌ No macOS Version Compatibility（macOSバージョン互換性なし）:
    → defaults writeが特定macOSバージョンでのみ有効
    → OSアップグレード後に設定スクリプトがエラー
    → 対策: sw_versでバージョンチェック、非互換設定はスキップ
```

---

## 3. ツール選定のアンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **TS-01** | **Hype-Driven Adoption（ハイプ駆動採用）** | 流行だけでツールを次々変更 | 毎月ターミナル/エディタが変わる、設定が常に不完全 | 最低1ヶ月の試用期間、既存ワークフローとの統合確認後に移行 |
| **TS-02** | **Config Copy-Paste（設定コピペ）** | インターネットの設定を理解せずにコピペ | 何が何をしているか説明できない、トラブル時に対応不能 | 1行ずつ理解してから追加、全行にコメントで目的記述 |
| **TS-03** | **Deprecated Tool Retention（非推奨ツール保持）** | asdf/nvm等のレガシーツールを惰性で使用 | Rust製代替（mise/fnm）の方が5-10倍高速 | 定期的なツール棚卸し、Rust製代替の評価 |
| **TS-04** | **Kitchen Sink Approach（全部入りアプローチ）** | 使うかもしれないツールを全部インストール | Brewfileが100+パッケージ、ディスク浪費、更新時間増大 | 必要になってからインストール、Brewfileを定期的にプルーニング |

---

## 4. ワークフロー統合の罠

```
ワークフロー統合の失敗:

  ❌ Inconsistent Theme（テーマ不統一）:
    → ターミナル/エディタ/tmuxで異なるカラーテーマ
    → 視覚的不統一、コンテキストスイッチの認知負荷
    → 対策: Catppuccin等の統一テーマを全ツールに適用

  ❌ Clipboard Chain Broken（クリップボードチェーン断裂）:
    → tmux→Neovim→システムクリップボードの連携が途切れる
    → Neovimでyankしたテキストがシステムに届かない
    → 対策: Neovim OSC 52 + tmux set-clipboard on + ターミナルOSC 52有効化

  ❌ SSH Remote Incompatibility（SSHリモート非互換）:
    → ローカル設定がSSH先で動作しない
    → terminfo不在、クリップボード不通、テーマ崩壊
    → 対策: TERM=xterm-256color フォールバック、terminfo転送スクリプト

  ❌ No Alias Documentation（エイリアス文書化なし）:
    → 大量のエイリアスを定義するが一覧/説明なし
    → 覚えられない、衝突に気づかない
    → 対策: aliases.zshにセクション分けとコメント、`alias`コマンドで一覧確認

  ❌ PATH Pollution（PATH汚染）:
    → PATH追加を.zshrcの複数箇所で実行
    → PATHが重複エントリだらけ、起動のたびに追加
    → 対策: env.zshで一元管理、typeset -U pathで重複排除
```

---

## 5. 2025年 モダンツールスタック推奨

| カテゴリ | レガシー | モダン推奨 | 理由 |
|---------|----------|-----------|------|
| シェルフレームワーク | oh-my-zsh | sheldon/zim | 起動速度5-10倍改善 |
| バージョンマネージャ | nvm + pyenv + rbenv | mise | 単一ツール、Rust製高速 |
| ファイルリスト | ls | eza | Git統合、カラー、ツリー表示 |
| ファイル検索 | find | fd | Rust製、gitignore自動適用 |
| テキスト検索 | grep | ripgrep | Rust製、10倍高速 |
| ディレクトリ移動 | cd | zoxide | 学習型ジャンプ |
| diff | diff | delta | Git統合、シンタックスハイライト |
| cat | cat | bat | シンタックスハイライト、ページャ |
| Nodeマネージャ | nvm | fnm | Rust製、起動時間ほぼゼロ |

---

## 6. Hearth との連携

```
Hearth での活用:
  1. SCAN フェーズで EN-01〜07 の環境再現性スクリーニング
  2. PLAN フェーズでツール選定の品質チェック
  3. CRAFT フェーズでワークフロー統合の設計確認
  4. VERIFY フェーズで環境検証スクリプト実行

品質ゲート:
  - install.sh/Makefile不在 → 自動セットアップスクリプト作成（EN-01 防止）
  - nvm + pyenv 併用検出 → mise統合提案（EN-02 防止）
  - Brewfile不在 → `brew bundle dump`実行提案（EN-03 防止）
  - ハードコードパス検出 → OS検出分岐追加（EN-04 防止）
  - テーマ不統一検出 → 統一テーマ設定提案（Workflow 防止）
  - defaults writeコメントなし → 目的コメント追加（macOS 防止）
  - PATH重複検出 → typeset -U path追加（Workflow 防止）
```

**Source:** [GBergatto: Tools for Managing Dotfiles](https://gbergatto.github.io/posts/tools-managing-dotfiles/) · [Michael Tinsley: Taming Dotfiles with GNU Stow](https://michaeltinsley.github.io/2025/09/09/taming-my-dotfiles-with-gnu-stow/) · [Samuel Lawrentz: Minimal Ghostty Config](https://samuellawrentz.com/blog/minimal-ghostty-config/) · [DEV.to: Terminal Setup Anti-Patterns](https://dev.to/ssh_exe/a-lot-of-terminal-setups-look-productive-until-you-restart-your-machine-onh) · [Chris Arderne: Neovim Config 2025](https://rdrn.me/neovim-2025/) · [Bitdoze: Ghostty Terminal Setup](https://www.bitdoze.com/ghostty-terminal/)
