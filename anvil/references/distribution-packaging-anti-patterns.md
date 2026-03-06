# Distribution & Packaging Anti-Patterns

> CLIバイナリの配布、パッケージング、クロスプラットフォーム展開の失敗パターン

## 1. バイナリ配布 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **DP-01** | **Fat Package（肥大パッケージ）** | 全プラットフォームのバイナリを1パッケージに同梱 | npm installで100MB+ダウンロード、node_modulesが肥大化 | プラットフォーム別パッケージ + optionalDependencies で必要なバイナリのみ取得 |
| **DP-02** | **postinstall Reliance（postinstall依存）** | postinstallスクリプトでバイナリをダウンロード | セキュリティポリシーでpostinstallが無効化されると動作しない、サプライチェーン攻撃面 | optionalDependencies + postinstallのフォールバック二重構成 |
| **DP-03** | **No Integrity Check（整合性検証なし）** | ダウンロードしたバイナリのハッシュ検証を行わない | 中間者攻撃でバイナリが差し替えられるリスク | SHA256ハッシュ検証、署名付きバイナリ、SBOMの提供 |
| **DP-04** | **Permission Loss（実行権限喪失）** | CI/CDやGitHub Actionsでバイナリの実行ビットが消失 | `EACCES: permission denied` エラー、手動で `chmod +x` が必要 | パッケージング時に実行権限を明示的に設定、CI/CDでchmod適用 |
| **DP-05** | **Single Registry Dependency（単一レジストリ依存）** | npm/PyPIのみに配布、代替インストール手段がない | レジストリ障害時にインストール不能、企業プロキシ環境で取得不可 | 複数チャネル配布: レジストリ + GitHub Releases + Homebrew/Scoop |
| **DP-06** | **No Upgrade Path（アップグレード経路なし）** | 自動更新メカニズムがない | ユーザーが古いバージョンを使い続ける、手動アップデートの手間 | `app update` コマンド、バージョンチェック + 更新通知 |
| **DP-07** | **Platform Matrix Gap（プラットフォーム不足）** | 主要プラットフォーム/アーキテクチャの欠落 | Apple Silicon(arm64)未対応、Windows ARM未対応、musl libc未対応 | CI/CDマトリクスで主要6ターゲットをカバー: {linux,darwin,windows}×{amd64,arm64} |

---

## 2. パッケージマネージャ別の罠

```
npm 配布の罠:
  ❌ optionalDependencies の不安定性:
    → --ignore-optional で無効化可能
    → Docker環境でプラットフォーム検出ミス
    → 対策: optionalDependencies + postinstall フォールバック

  ❌ postinstall のセキュリティリスク:
    → 任意コードを実行可能 → サプライチェーン攻撃の標的
    → 「一般的に無効化が推奨されている」（Sentry Engineering）
    → 対策: 最小限のスクリプト、integrity検証、CSP的な制限

  ❌ node_modules 間のバイナリ移動:
    → VM/Docker間でnode_modulesをコピーするとアーキテクチャ不一致
    → 対策: 環境ごとに npm install を実行

pip/PyPI 配布の罠:
  ❌ wheel非提供:
    → ソースからのビルドが必要、C拡張のコンパイルエラー
    → 対策: manylinux/musllinux wheel を各プラットフォーム向けにビルド

  ❌ 再現性の低さ:
    → PyPIパッケージの再現可能ビルド率は12.2%（CMU研究）
    → 対策: pip freeze + ハッシュ検証、pip-tools/uv での依存ロック

Cargo 配布の罠:
  ❌ cargo install の遅さ:
    → ソースからの完全ビルド、dev-dependenciesも含む
    → 対策: cargo-binstall でプリビルドバイナリ取得、GitHub Releases配布

  ❌ バイナリ更新の困難:
    → cargo install --force で完全再ビルドが必要
    → 対策: cargo-update クレート、またはGitHub Releases + 自動更新

Go 配布の罠:
  ❌ go install のバージョン管理:
    → @latest で常に最新が入る、再現性の欠如
    → 対策: バージョン指定 go install pkg@v1.2.3、go.sum による検証

  ❌ ビルドフックの非存在:
    → ネイティブコード統合が困難（CGO依存）
    → 利点: サプライチェーン攻撃面が小さい
    → 対策: CGOクロスコンパイル戦略、静的リンク
```

---

## 3. セキュリティのアンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **SC-01** | **Dependency Confusion（依存関係混乱）** | プライベートパッケージ名と同名の公開パッケージが存在 | 意図しないパッケージがインストールされる | スコープ付きパッケージ (@org/pkg)、レジストリの明示的設定 |
| **SC-02** | **Unsigned Binaries（未署名バイナリ）** | コード署名なしでバイナリを配布 | macOS Gatekeeperの警告、Windows SmartScreenのブロック | Apple Developer ID / Windows Authenticode で署名 |
| **SC-03** | **No SBOM（SBOMなし）** | ソフトウェア部品表の未提供 | 依存関係の脆弱性を追跡不能 | CycloneDX/SPDX形式のSBOM生成、リリースに同梱 |
| **SC-04** | **Stale Dependencies（古い依存関係）** | セキュリティパッチ済みバージョンへの更新を怠る | CVEが既知なのに修正されない | Dependabot/Renovate による自動更新PR、定期的な監査 |

---

## 4. リリース・バージョニングのアンチパターン

```
バージョニングの罠:

  ❌ SemVer Lie（SemVer偽装）:
    → パッチバージョンでbreaking changeを含む
    → ユーザーの自動更新で既存スクリプトが壊れる
    → 対策: SemVerの厳守、API diffツールによる自動検出（Elm方式）

  ❌ No Changelog（変更履歴なし）:
    → ユーザーがアップデート内容を把握できない
    → バージョンアップを躊躇する原因
    → 対策: CHANGELOG.md の自動生成（conventional commits連携）

  ❌ Breaking Without Migration（マイグレーションなき破壊的変更）:
    → CLIの引数やフラグ名を予告なく変更
    → ユーザーのスクリプト・CI設定が壊れる
    → 対策: 廃止予定警告 → 移行期間 → 削除の3段階

  ❌ No Prerelease Channel（プレリリースチャネルなし）:
    → stableのみでベータテスト不可
    → ユーザーが新機能を事前検証できない
    → 対策: beta/canary チャネルの提供（npm tag, GitHub pre-release）

  ❌ Tag-Only Release（タグのみリリース）:
    → Gitタグだけでバイナリの配布なし
    → ユーザーがビルド環境を準備する必要
    → 対策: GitHub Actions でリリース時にバイナリ自動ビルド+アップロード
```

---

## 5. クロスプラットフォームビルドのアンチパターン

```
ビルドマトリクスの罠:

  ❌ CI-Only Build（CIのみビルド）:
    → ローカルでクロスプラットフォームビルドが不可能
    → デバッグがCI上でしかできない
    → 対策: Docker/cross-rs/zig cc でローカルクロスビルド環境を整備

  ❌ Dynamic Link Trap（動的リンクの罠）:
    → glibc等に動的リンクされたバイナリ
    → 古いLinuxディストリで `GLIBC_2.XX not found` エラー
    → 対策: musl静的リンク、または十分に古いベースイメージでビルド

  ❌ No Smoke Test（スモークテストなし）:
    → ビルドしたバイナリの動作確認をしない
    → リンクエラーや依存不足に気づかずリリース
    → 対策: 各プラットフォームで `app --version` + 基本操作のE2Eテスト

  ❌ Architecture Detection Failure（アーキテクチャ検出失敗）:
    → Rosetta 2環境でx86_64として検出
    → Apple Silicon最適化バイナリが使用されない
    → 対策: `uname -m` + `sysctl` による正確なアーキテクチャ判定
```

---

## 6. Anvil との連携

```
Anvil での活用:
  1. BLUEPRINT フェーズで DP-01〜07 の配布戦略レビュー
  2. HARDEN フェーズでセキュリティ・整合性検証の実装
  3. PRESENT フェーズでリリース・バージョニング戦略の提案
  4. 全フェーズでクロスプラットフォーム対応の確認

品質ゲート:
  - 全バイナリ同梱パッケージ → プラットフォーム別分割（DP-01 防止）
  - postinstallのみのバイナリ取得 → optionalDeps併用（DP-02 防止）
  - ダウンロードバイナリのハッシュ未検証 → SHA256検証追加（DP-03 防止）
  - 主要プラットフォーム未カバー → CIマトリクス拡張（DP-07 防止）
  - 未署名バイナリ → コード署名導入（SC-02 防止）
  - パッチバージョンでbreaking change → SemVer遵守+API diff（SemVer Lie 防止）
  - 動的リンクバイナリ → musl静的リンク検討（Dynamic Link Trap 防止）
```

**Source:** [Sentry Engineering: Publishing Binaries on npm](https://sentry.engineering/blog/publishing-binaries-on-npm) · [Andrew Nesbitt: Package Manager Design Tradeoffs](https://nesbitt.io/2025/12/05/package-manager-tradeoffs.html) · [Rust CLI: Packaging](https://rust-cli.github.io/book/tutorial/packaging.html) · [CMU: Reproducible Packaging Study](http://www.cs.cmu.edu/~ckaestne/pdf/icse25_rb.pdf) · [Orhun: Packaging Rust for npm](https://blog.orhun.dev/packaging-rust-for-npm/)
