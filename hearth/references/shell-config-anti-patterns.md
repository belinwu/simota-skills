# Shell Configuration Anti-Patterns

> zsh/bash/fishの設定ミス、起動時間の劣化要因、プラグイン管理、パフォーマンス最適化の失敗パターン

## 1. シェル起動パフォーマンス 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **SH-01** | **Eager Version Manager Loading（バージョンマネージャ即時読込）** | nvm/pyenv/rbenv/condaを.zshrcで即座に`eval`実行 | nvm単体で300-500ms追加、全体で1秒超 | 遅延ロード: ラッパー関数で初回使用時に初期化、またはmiseに統合 |
| **SH-02** | **Multiple compinit Calls（複数compinit呼出）** | 複数ファイルから`compinit`を重複呼出 | 補完システム初期化が毎回200ms+消費 | `compinit`は全`$fpath`設定後に1回のみ、日次キャッシュで再ビルド抑制 |
| **SH-03** | **Oh-My-Zsh Full Framework（フルフレームワーク依存）** | oh-my-zshを全機能有効で使用 | 起動時間の55%がフレームワーク読込、30%が補完 | 必要プラグインのみ有効化、またはsheldon/zimに移行 |
| **SH-04** | **Synchronous Plugin Loading（同期プラグイン読込）** | 全プラグインを起動時に同期的にsource | プラグイン数に比例して起動時間が線形増加 | `zsh-defer`/sheldon deferred loading/zinit turbo modeで非同期化 |
| **SH-05** | **Heavy Theme Rendering（重いテーマ）** | gitステータス等をプロンプトで毎回サブプロセス実行 | 大規模リポジトリでプロンプト表示に数秒 | Powerlevel10k（Instant Prompt）またはstarship（Rust製高速描画） |
| **SH-06** | **eval "$(tool init zsh)" Pattern（eval initパターン）** | 毎回ツール初期化を`eval`で実行 | starship/zoxide/fzf等のinit実行が毎起動で発生 | 出力をファイルにキャッシュ: `tool init zsh > ~/.cache/tool.zsh` + `source` |
| **SH-07** | **Auto-Update on Every Launch（毎起動自動更新）** | oh-my-zsh/プラグインマネージャの自動更新チェック | 起動のたびにネットワークチェック発生 | `DISABLE_AUTO_UPDATE="true"`、手動更新に切替 |

---

## 2. 設定構造のアンチパターン

```
構造の失敗:

  ❌ Monolithic .zshrc（モノリス設定ファイル）:
    → 500行超の.zshrcに全設定を一括記述
    → 変更時の影響範囲が不明、デバッグ困難
    → 対策: モジュール分割（env.zsh/aliases.zsh/plugins.zsh/local.zsh）

  ❌ No local.zsh Separation（ローカル設定未分離）:
    → マシン固有設定（パス、トークン参照）を共通ファイルに混在
    → dotfileリポジトリに秘密情報が混入するリスク
    → 対策: local.zshをgitignoreし、マシン固有設定を分離

  ❌ Hardcoded Paths（ハードコードパス）:
    → `/opt/homebrew/bin`等をOS判定なしに記述
    → macOS/Linux間でdotfile共有不能
    → 対策: `[[ -d /opt/homebrew ]] && eval "$(/opt/homebrew/bin/brew shellenv)"`

  ❌ No XDG Compliance（XDG非準拠）:
    → zsh設定を~/直下に散在（.zshrc, .zprofile, .zshenv等）
    → ホームディレクトリ汚染、管理困難
    → 対策: ZDOTDIR=$XDG_CONFIG_HOME/zsh を ~/.zshenv で設定

  ❌ Source Order Ignorance（読込順序無視）:
    → 環境変数設定よりプラグイン読込を先に実行
    → PATHが未設定のままツールが見つからないエラー
    → 対策: env → path → plugins → completions → aliases → local の順序厳守
```

---

## 3. プラグイン管理のアンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **PM-01** | **Plugin Hoarding（プラグイン肥大）** | 使わないプラグインが大量に残留 | `zprof`で未使用プラグインが上位に表示 | 月次棚卸し: 2週間使わないプラグインは削除 |
| **PM-02** | **Framework Lock-in（フレームワークロックイン）** | oh-my-zsh/preztoに全面依存 | フレームワーク外のプラグイン追加が困難 | sheldon/zimで個別プラグイン管理 |
| **PM-03** | **Compilation Overhead（コンパイルオーバーヘッド）** | zinit compile等のコンパイル処理が起動時に実行 | 初回起動が異常に遅い、キャッシュ不整合 | TOMLベースのsheldon（コンパイル不要）推奨 |
| **PM-04** | **No Plugin Pinning（プラグインバージョン未固定）** | プラグインを常にHEAD参照 | 更新で突然壊れる、再現不能な環境差異 | sheldon/zimでタグ/コミットSHA固定 |

---

## 4. パフォーマンス計測と目標

```
計測方法:

  プロファイリング:
    1. zmodload zsh/zprof      # .zshrc先頭
    2. zprof                   # .zshrc末尾 or シェル起動後に実行
    → "self"列が最大の項目から優先対処

  壁時計計測:
    /usr/bin/time zsh -i -c exit     # 実際の起動時間
    hyperfine 'zsh -i -c exit'       # 統計的計測（推奨）

  起動時間目標:
    | Profile  | 目標      | 許容上限  |
    |----------|-----------|-----------|
    | Minimal  | < 50ms    | < 100ms   |
    | Standard | < 150ms   | < 250ms   |
    | Power    | < 250ms   | < 400ms   |

  最適化優先順位:
    1. バージョンマネージャ遅延ロード（効果: 300-500ms削減）
    2. compinit単一化+キャッシュ（効果: 100-200ms削減）
    3. 未使用プラグイン除去（効果: 50-150ms削減）
    4. テーマ軽量化（効果: 50-100ms削減）
    5. eval initキャッシュ化（効果: 30-80ms削減）
```

---

## 5. Hearth との連携

```
Hearth での活用:
  1. SCAN フェーズで SH-01〜07 の起動時間スクリーニング
  2. PLAN フェーズで設定構造の品質チェック
  3. CRAFT フェーズで PM-01〜04 のプラグイン管理設計
  4. VERIFY フェーズでパフォーマンス計測と目標達成確認

品質ゲート:
  - 起動時間 > 250ms → zprof分析+ボトルネック特定（SH-01〜07 防止）
  - .zshrc 200行超 → モジュール分割提案（構造 防止）
  - eval "$(tool init)" 検出 → キャッシュ化提案（SH-06 防止）
  - oh-my-zshフル使用 → 軽量代替提案（SH-03 防止）
  - nvm/pyenv直接eval → 遅延ロード or mise提案（SH-01 防止）
  - XDG非準拠設定 → ZDOTDIR移行提案（構造 防止）
```

**Source:** [OpenReplay: Why zsh Is Slow to Start](https://blog.openreplay.com/zsh-slow-startup-fix/) · [Mike Kasberg: Optimizing Zsh Init with ZProf](https://www.mikekasberg.com/blog/2025/05/29/optimizing-zsh-init-with-zprof.html) · [Santacloud: Optimizing ZSH Startup to Under 70ms](http://santacloud.dev/posts/optimizing-zsh-startup-performance/) · [DEV.to: Achieving 30ms Zsh Startup](https://dev.to/tmlr/achieving-30ms-zsh-startup-40n1) · [Kian's Blog: Profiling ZSH](https://kasad.com/blog/zsh-profiling/)
