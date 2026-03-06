# Dotfile Management & Security Anti-Patterns

> dotfile管理戦略、シークレット漏洩、リポジトリ構造、マルチマシン対応、セキュリティの失敗パターン

## 1. dotfile管理 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **DF-01** | **Secrets in Dotfiles（dotfile内シークレット）** | APIキー/トークン/パスワードを設定ファイルに直接記述 | GitGuardianスキャンで検出、git historyにシークレット残留 | `local.zsh`（gitignored）分離 + 1Password CLI/direnv/.envrc |
| **DF-02** | **No .gitignore Strategy（gitignore戦略なし）** | dotfileリポジトリに`.gitignore`未設定 or 不十分 | `.ssh/`, `.gnupg/`, `.env`がcommit候補に表示 | 明示的allowlist方式: 必要ファイルのみ`git add`、デフォルト除外 |
| **DF-03** | **Git History Secret Residue（Git履歴のシークレット残留）** | シークレットをcommit後に行削除で対応 | `git log -p`で過去コミットにシークレットが残存 | git filter-repo/BFG Repo-Cleanerで履歴書き換え、即座にキー失効 |
| **DF-04** | **No Backup Before Change（変更前バックアップなし）** | 設定ファイルをバックアップなしに上書き | 設定破壊時に復元不能 | `cp file file.bak.$(date +%Y%m%d)` を全変更前に実行 |
| **DF-05** | **Wrong Tool for Scale（スケール不一致のツール選択）** | 単一マシンでchezmoiの複雑さ、マルチマシンでstowの制限 | テンプレート不要なのにGo templateを学習、マシン間差異を手動管理 | 単一マシン→GNU Stow、マルチマシン→chezmoi、ミニマル→yadm |
| **DF-06** | **Stow Symlink Conflicts（Stowシンボリックリンク競合）** | stow実行時に既存ファイルとの競合未解決 | `CONFLICT: ... already exists`エラー | `stow --adopt`で既存ファイルをリポジトリに取込 or 手動移動 |
| **DF-07** | **No Bootstrap Script（ブートストラップスクリプトなし）** | dotfileリポジトリはあるが新マシンセットアップ手順が未定義 | 新マシンで1時間+の手動セットアップ | `install.sh`/`Makefile`でワンコマンドセットアップ（stow + brew bundle + mise install） |

---

## 2. シークレット管理のアンチパターン

```
シークレット漏洩の失敗:

  ❌ Hardcoded API Keys（ハードコードAPIキー）:
    → .zshrcに export GITHUB_TOKEN="ghp_xxxx" を直接記述
    → 73.6%のdotfileリポジトリが何らかの機密情報を漏洩（MSR 2023研究）
    → 対策: .localファイルに分離、direnvの.envrc、1Password CLI

  ❌ SSH Keys in Repo（リポジトリ内SSH鍵）:
    → ~/.ssh/をdotfileリポジトリに含める
    → RSA秘密鍵がパブリックに公開
    → 対策: .ssh/は絶対にdotfileリポジトリに含めない、chezmoi encrypt

  ❌ Shell History Exposure（シェル履歴の露出）:
    → .zsh_history/.bash_historyをdotfileリポジトリに含める
    → パスワード付きコマンド、内部URLが露出
    → 対策: history系ファイルを.gitignoreに追加

  ❌ No Pre-Commit Hook（プリコミットフックなし）:
    → シークレットスキャンなしにcommit
    → レビューなしでシークレットがpush
    → 対策: gitleaks/detect-secretsをpre-commit hookに統合

  ❌ Delete-Only Remediation（削除のみの修復）:
    → シークレットcommit後に行を削除してcommit
    → git historyにシークレットが永続的に残存
    → 対策: 即座にキー失効→git filter-repo→force push→全履歴確認

  ❌ Credentials in Git Config（Gitコンフィグ内認証情報）:
    → .gitconfigにgithub tokenや社内プロキシ認証を記述
    → git configがdotfileリポジトリ経由で公開
    → 対策: credential helper使用、[include] pathでlocal分離
```

---

## 3. よく漏洩するシークレットの種類

| カテゴリ | 具体例 | リスク | 検出パターン |
|---------|--------|--------|-------------|
| **クラウドキー** | AWS_ACCESS_KEY_ID, GCP_SERVICE_ACCOUNT_JSON | クリプトマイニング、5桁ドル請求 | `AKIA[0-9A-Z]{16}` |
| **APIトークン** | GITHUB_TOKEN, SLACK_TOKEN, STRIPE_KEY | リポジトリ改ざん、通知スパム、決済不正 | `ghp_`, `xoxb-`, `sk_live_` |
| **SSH鍵** | id_rsa, id_ed25519 | サーバー直接アクセス | `-----BEGIN.*PRIVATE KEY-----` |
| **DB接続** | DATABASE_URL, MONGODB_URI | データ窃取、ランサムウェア | `://.*:.*@` |
| **個人情報** | メールアドレス、内部ホスト名 | フィッシング、内部構造推測 | email regex, hostname patterns |

---

## 4. リポジトリ構造のアンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **RS-01** | **Flat Structure（フラット構造）** | dotfileリポジトリ直下に全ファイルを配置 | stowが使えない、ツール別の管理不能 | パッケージ別ディレクトリ: `zsh/`, `nvim/`, `ghostty/` |
| **RS-02** | **Missing README（README欠如）** | リポジトリの利用手順が未記載 | 半年後の自分がセットアップ方法を忘れる | README.mdにセットアップ手順、依存ツール、構成図を記載 |
| **RS-03** | **No XDG Directory Mapping（XDGマッピングなし）** | stowパッケージが$HOMEフラットでXDGパスを反映しない | `stow nvim`で~/.config/nvim/にリンクされない | `nvim/.config/nvim/` 構造でXDGパスをミラー |
| **RS-04** | **Brewfile Drift（Brewfile乖離）** | Brewfileが実際のインストール状況と乖離 | `brew bundle check`で差分多数 | 定期的に`brew bundle dump --describe --force`で同期 |

---

## 5. マルチマシン管理の罠

```
マルチマシンの失敗:

  ❌ Manual Sync（手動同期）:
    → マシン間の設定差分を手動でコピー
    → 同期漏れ、設定の乖離が蓄積
    → 対策: chezmoi + GitリポジトリでCD的同期

  ❌ No Template Strategy（テンプレート戦略なし）:
    → macOS/Linuxの差異をif文で.zshrcに埋め込み
    → 条件分岐が複雑化、可読性低下
    → 対策: chezmoi template (.tmpl) でOS/hostname条件分岐

  ❌ Work/Personal Config Collision（仕事/個人設定衝突）:
    → 仕事用gitconfig（社内email）が個人リポジトリに混入
    → 社内メールアドレスがパブリックに露出
    → 対策: .gitconfig [includeIf "gitdir:~/work/"] で条件別設定

  ❌ No Idempotent Setup（冪等セットアップなし）:
    → install.shが2回実行すると設定が重複/壊れる
    → 安全な再実行不能
    → 対策: 冪等なスクリプト設計（存在チェック→スキップパターン）
```

---

## 6. Hearth との連携

```
Hearth での活用:
  1. SCAN フェーズで DF-01〜07 のdotfileリポジトリスクリーニング
  2. PLAN フェーズでシークレット管理の品質チェック
  3. CRAFT フェーズで RS-01〜04 のリポジトリ構造設計
  4. VERIFY フェーズでgitleaksスキャン+Brewfile整合性確認

品質ゲート:
  - dotfileリポジトリにシークレットパターン検出 → 即座に警告+失効手順（DF-01 防止）
  - .gitignore未設定 → テンプレート生成（DF-02 防止）
  - install.sh/Makefile不在 → ブートストラップスクリプト作成（DF-07 防止）
  - stowパッケージがフラット → XDGマッピング構造に移行（RS-03 防止）
  - Brewfile乖離 → `brew bundle dump`実行提案（RS-04 防止）
  - .gitconfigに認証情報 → includeIf分離提案（Secret 防止）
```

**Source:** [InstaTunnel: Dotfiles Security Minefield](https://instatunnel.my/blog/why-your-public-dotfiles-are-a-security-minefield) · [MSR 2023: Connecting the .dotfiles](https://pure.mpg.de/rest/items/item_3505626/component/file_3505627/content) · [OpenReplay: Dotfiles Commit or Ignore](https://blog.openreplay.com/dotfiles-commit-ignore/) · [GitGuardian: Protecting Developer Secrets](https://blog.gitguardian.com/protecting-developers-secrets/) · [Spondicious: Stow or Chezmoi](https://spondicious.com/blog/stoworchezmoi/) · [chezmoi: Comparison Table](https://www.chezmoi.io/comparison-table/)
