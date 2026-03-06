# Terraform / IaC Anti-Patterns

> Terraformモジュール設計、状態管理、HCLパターン、バージョニングの失敗パターン

## 1. モジュール設計 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **TF-01** | **Monolithic State（モノリシック状態）** | 全リソースを1つのstateファイルで管理 | `terraform plan`が遅い、blast radiusが巨大、apply恐怖 | サービス×環境ごとにstate分割、remote backend+locking |
| **TF-02** | **God Module（神モジュール）** | 1モジュールがVPC+Compute+DB+IAMを全て管理 | 再利用不能、変更のたびに全体が壊れる、50行超/module | Single Responsibility: networking/compute/storage/iam各モジュールに分割 |
| **TF-03** | **Hardcoded Values（ハードコード値）** | リージョン名、ARN、CIDR、AMI IDを直書き | 環境切替不能、別リージョンデプロイ失敗 | 全値をvariable化、defaultsは明確にドキュメント化 |
| **TF-04** | **Version Drift（バージョン漂流）** | Terraform本体・provider・moduleのバージョン未固定 | CI/CDとローカルで挙動が異なる、state互換エラー | `required_version`+`required_providers`でpin、tfenvで管理 |
| **TF-05** | **Reinventing Modules（車輪の再発明）** | 標準的なVPC/ECS/RDSモジュールを毎回自作 | メンテナンス負荷増大、セキュリティパッチ漏れ | Terraform Registry活用、カスタムは差分のみ |
| **TF-06** | **Resource-Type Organization（リソース型組織化）** | ディレクトリをDNS/IAM/CloudFront等のリソース型で構成 | サービス横断の変更が複数ディレクトリにまたがる | サービス境界・チームオーナーシップに沿った構成に変更 |
| **TF-07** | **Copy-Paste Environments（コピペ環境）** | dev/staging/prodを別ディレクトリに丸コピー | 環境間のドリフト、修正の3重適用、設定の乖離 | workspacesまたはtfvars分離+共通module構成 |

---

## 2. 状態管理の罠

```
State管理の失敗:

  ❌ Local State（ローカル状態）:
    → terraform.tfstateをローカルで管理
    → チーム間で同期不能、同時実行で状態破壊
    → 対策: S3+DynamoDB / GCS / Azure Blob の remote backend + locking

  ❌ State in VCS（状態のバージョン管理）:
    → .tfstateファイルをGitにコミット
    → シークレット漏洩（state内のDB password等）、マージコンフリクト
    → 対策: .gitignoreに追加、remote backend使用、sensitive属性活用

  ❌ Oversized State（巨大状態）:
    → 1stateに100+リソース
    → plan/apply遅延（30秒→5分）、API rate limit、blast radius拡大
    → 対策: サービス境界で分割、data sourceで参照

  ❌ Undersized State（過度な分割）:
    → リソース単位で state を分割
    → 依存関理の複雑化、terraform_remote_state の連鎖
    → 対策: サービス×環境の粒度で適切なバランス

  ❌ No State Locking（状態ロックなし）:
    → 同時 apply で状態ファイル破損
    → リソースの二重作成、孤立リソース
    → 対策: DynamoDB/GCS locking を必ず有効化

  ❌ Manual State Surgery（手動状態操作）:
    → terraform state mv/rm を計画なしで実行
    → リソースの孤立、再作成、本番障害
    → 対策: moved block活用、import block活用、操作前にbackup
```

---

## 3. HCLコード品質のアンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **HC-01** | **Secrets in Plaintext（平文シークレット）** | .tfvars / .tf にパスワード・APIキーを直書き | GitにDB passwordがコミットされている | Vault/Secrets Manager + sensitive変数 + .gitignore |
| **HC-02** | **No Validation（検証なし）** | variable に validation block がない | 不正値（空文字CIDR、無効リージョン）が通過 | validation + precondition + postcondition 活用 |
| **HC-03** | **No Formatting（フォーマットなし）** | terraform fmt を実行しない | コードスタイルが不統一、Git blameが汚染 | pre-commit hookで terraform fmt -check 自動化 |
| **HC-04** | **No Documentation（ドキュメントなし）** | variable/output に description がない | モジュール利用者が用途を理解できない | 全variable/outputにdescription必須、terraform-docs自動生成 |
| **HC-05** | **Deep Nesting（深いネスト）** | for_each + dynamic + conditional の3重ネスト | 可読性崩壊、デバッグ困難 | ローカル変数で中間変換、複雑なロジックはmoduleに抽出 |

---

## 4. Provider・ワークスペースの罠

```
Provider設計の失敗:

  ❌ Provider Lock-in（プロバイダーロックイン）:
    → AWS固有リソースをモジュール内にハードコード
    → マルチクラウド移行時にモジュール全書き直し
    → 対策: 抽象化レイヤーを設計、プロバイダー固有部分を分離

  ❌ Workspace Abuse（ワークスペース乱用）:
    → workspace名でdev/staging/prodを切替え、1設定で全環境管理
    → 環境間の差異表現が困難、条件分岐の増殖
    → 対策: ディレクトリ分離+tfvars方式、workspaceはライトユースのみ

  ❌ Unpinned Providers（プロバイダー未固定）:
    → required_providers にバージョン制約なし
    → minor updateで破壊的変更、CI/CDの不安定化
    → 対策: ~> 制約でマイナーバージョンまでpin

  ❌ Multiple Provider Configs（複数プロバイダー設定混在）:
    → 1モジュール内に複数リージョン/アカウントのprovider設定
    → モジュールの再利用性低下、暗黙的な依存
    → 対策: provider設定はroot moduleで定義し、aliasで渡す
```

---

## 5. CI/CD統合のアンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **CI-01** | **No Plan Review（plan未レビュー）** | applyを直接実行しplan出力を確認しない | 意図しないリソース削除・再作成 | plan→PRコメント→承認→applyのゲートフロー |
| **CI-02** | **Console Drift（コンソールドリフト）** | GUIから「ちょっとした修正」を手動実施 | IaCと実態の乖離、次のapplyで上書き | drift detection定期実行、コンソール変更禁止ポリシー |
| **CI-03** | **No Policy Gates（ポリシーゲートなし）** | tfsec/Checkov/OPA無しでapply | セキュリティ違反（0.0.0.0/0許可等）がデプロイされる | CI pipelineにpolicy-as-code gate必須 |
| **CI-04** | **apply -auto-approve in Prod（本番自動承認）** | 本番環境でも-auto-approve使用 | 破壊的変更が即座に適用、ロールバック不能 | 本番は手動承認必須、staging以下のみ自動化 |

---

## 6. Scaffold との連携

```
Scaffold での活用:
  1. ASSESS フェーズで TF-01〜07 のモジュール設計スクリーニング
  2. DESIGN フェーズで状態管理戦略の品質チェック
  3. IMPLEMENT フェーズで HC-01〜05 のHCLコード品質確認
  4. VERIFY フェーズで CI-01〜04 のパイプライン品質確認

品質ゲート:
  - 1stateに100+リソース → state分割提案（TF-01 防止）
  - module 50行超 → 分割提案（TF-02 防止）
  - ハードコード値検出 → variable化提案（TF-03 防止）
  - バージョン制約なし → pinning追加（TF-04 防止）
  - .tfvarsにシークレット → Vault/SM移行提案（HC-01 防止）
  - コンソール変更検出 → drift detection導入（CI-02 防止）
  - policy gate未設定 → tfsec/Checkov導入（CI-03 防止）
```

**Source:** [pipetail: 10 Most Common Terraform Mistakes](https://blog.pipetail.io/posts/2020-10-29-most-common-mistakes-terraform/) · [HashiCorp: Opinionated Terraform Best Practices](https://www.hashicorp.com/en/resources/opinionated-terraform-best-practices-and-anti-patterns) · [Gomboc: IaC Security Best Practices 2026](https://www.gomboc.ai/blog/iac-security-best-practices-for-2026) · [Ricky Smith: Terraform Module Design Pitfalls](https://www.ricky-dev.com/coding/2025/09/terraform-pitfalls/)
