# Cloud Infrastructure Anti-Patterns

> VPC/ネットワーク設計、IAM/セキュリティ、マルチクラウド、IaCセキュリティの失敗パターン

## 1. ネットワーク設計 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **NW-01** | **Flat Network（フラットネットワーク）** | 全リソースを1つのpublic subnetに配置 | DB/内部サービスがインターネットに露出 | public/private subnet分離、NAT Gateway経由のoutbound |
| **NW-02** | **IP Address Exhaustion（IPアドレス枯渇）** | /24 等の小さいCIDRでsubnetを作成 | Lambda/ECSのスケール時にENI枯渇、デプロイ失敗 | 将来を見越した十分なCIDR割当（/16 VPC、/20以上 subnet） |
| **NW-03** | **Security Group 0.0.0.0/0（全開放SG）** | inbound/outboundを0.0.0.0/0で許可 | ポートスキャンで内部サービス発見、攻撃面拡大 | 必要なCIDR/SGのみ許可、定期監査 |
| **NW-04** | **No VPC Endpoints（VPCエンドポイントなし）** | S3/DynamoDB等へのアクセスがNAT Gateway経由 | NAT Gateway課金増大（$0.045/GB）、帯域ボトルネック | Gateway/Interface VPC Endpoints活用 |
| **NW-05** | **Single AZ Deployment（単一AZデプロイ）** | 全リソースを1つのAZに配置 | AZ障害で全サービスダウン | Multi-AZ構成必須、subnetをAZごとに定義 |
| **NW-06** | **Overlapping CIDRs（重複CIDR）** | VPC間/オンプレミスとCIDRが重複 | VPC Peering/Transit Gateway接続不可 | CIDR計画表で重複チェック、RFC1918の範囲を計画的に割当 |
| **NW-07** | **No Network Segmentation（ネットワーク非分離）** | 同一VPCに全環境（dev/staging/prod）を配置 | dev環境からprod DBにアクセス可能、blast radius拡大 | 環境別VPC + Transit Gateway/Peering で必要な接続のみ |

---

## 2. IAM/セキュリティの罠

```
IAM設計の失敗:

  ❌ Wildcard Permissions（ワイルドカード権限）:
    → "Action": "*", "Resource": "*" のポリシー
    → 全サービスへのフルアクセス、横方向移動が容易
    → 対策: 最小権限原則、必要なAction/Resourceのみ指定

  ❌ Long-lived Credentials（長寿命認証情報）:
    → IAMユーザーの永続アクセスキー
    → Datadog調査: 依然として侵害の主要原因
    → 対策: IAM Roles + STS temporary credentials、Workload Identity Federation

  ❌ No MFA Enforcement（MFA未強制）:
    → 管理者アカウントにMFAなし
    → 認証情報漏洩時に即座にアカウント侵害
    → 対策: IAMポリシーでMFA強制、FIDO2/WebAuthn推奨

  ❌ Shared Service Accounts（共有サービスアカウント）:
    → 複数サービスが同一IAMロール/SAを共有
    → 権限の肥大化、監査ログの帰属不明
    → 対策: サービスごとに専用IAMロール/SA、ABAC活用

  ❌ No SCPs/Organization Policies（組織ポリシーなし）:
    → AWS Organizations SCPs / GCP Org Policies 未設定
    → 個別アカウントで危険な操作が可能
    → 対策: ガードレールSCPs（リージョン制限、ルートユーザー制限）

  ❌ IMDSv1 Reliance（IMDSv1依存）:
    → EC2でIMDSv1を許可したまま
    → SSRF攻撃でインスタンスメタデータ（認証情報）窃取
    → 対策: IMDSv2を強制（HttpTokens=required）
```

---

## 3. IaCセキュリティのアンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **IS-01** | **Console Drift（コンソールドリフト）** | 「緊急対応」でGUIから直接変更 | terraform planで予期しないdiff、IaCと実態の乖離 | drift detection定期実行 + コンソール変更禁止SCP |
| **IS-02** | **No Encryption Default（暗号化デフォルトなし）** | S3/RDS/EBSの暗号化を個別に設定 | 暗号化漏れ、監査で未暗号化リソース発見 | アカウントレベルでEBS/S3デフォルト暗号化有効化 |
| **IS-03** | **Public Storage Buckets（公開ストレージ）** | S3/GCSバケットのパブリックアクセスブロック未設定 | データ漏洩インシデント（医療記録・金融データ） | S3 Block Public Access有効化、BPA設定をIaCで強制 |
| **IS-04** | **No Audit Trail（監査証跡なし）** | CloudTrail/Audit Logs未有効化 | インシデント時に原因特定不能 | 全リージョンでCloudTrail有効化、S3に長期保存 |
| **IS-05** | **Unscanned IaC（未スキャンIaC）** | policy-as-codeツール未導入 | セキュリティ違反がデプロイされてから発覚 | CI/CDにtfsec/Checkov/Trivy統合、PR時にブロック |

---

## 4. マルチクラウド/マルチアカウントの罠

```
マルチクラウドの失敗:

  ❌ Lowest Common Denominator（最小公倍数設計）:
    → 全クラウドで共通のサービスのみ使用
    → 各クラウドの差別化機能（Aurora/Spanner等）を活用できない
    → 対策: クラウドごとの強みを活かす設計、abstraction layerは必要な部分のみ

  ❌ Multi-Account Chaos（マルチアカウント無秩序）:
    → アカウント/プロジェクトの命名・タグ付け規約なし
    → コスト帰属不明、セキュリティポリシーの不統一
    → 対策: Landing Zone設計（AWS Control Tower / GCP Organization）

  ❌ No Data Perimeter（データペリメーターなし）:
    → 信頼境界の定義なし
    → 認証情報漏洩時にクロスアカウントアクセスが可能
    → 対策: VPC Endpoints + S3 bucket policy + IAM条件キーでペリメーター構築

  ❌ Region Sprawl（リージョン拡散）:
    → 必要以上に多くのリージョンにリソース展開
    → 管理コスト増大、セキュリティ監視の盲点
    → 対策: SCPsでリージョン制限、使用リージョンを明示的に管理

  ❌ No Tagging Strategy（タグ戦略なし）:
    → リソースにタグがない、または不統一
    → コスト帰属不能、セキュリティグループ化不能
    → 対策: 必須タグ定義（Environment/Service/Owner/CostCenter）+ タグポリシー強制
```

---

## 5. 可用性/耐障害性のアンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **HA-01** | **No Backup Strategy（バックアップ戦略なし）** | RDS/EBSの自動スナップショット未設定 | データ損失時に復旧不能 | 自動スナップショット + クロスリージョンコピー |
| **HA-02** | **Single Point of Failure（単一障害点）** | 単一NAT Gateway / 単一DB / 単一ALB | 1リソース障害で全サービスダウン | Multi-AZ NAT Gateway、RDS Multi-AZ、ALB Cross-Zone |
| **HA-03** | **No Disaster Recovery Plan（DR計画なし）** | RPO/RTOの定義なし | 障害時の復旧に数日、SLA違反 | RPO/RTO定義 + DR構成（Pilot Light/Warm Standby） |
| **HA-04** | **Hardcoded Resource References（ハードコードリソース参照）** | 特定のAZ名/リソースIDを直書き | AZ障害時にフェイルオーバー不能 | data source + AZ動的取得 + 変数化 |

---

## 6. Scaffold との連携

```
Scaffold での活用:
  1. ASSESS フェーズで NW-01〜07 のネットワーク設計スクリーニング
  2. DESIGN フェーズで IAM/セキュリティの品質チェック
  3. IMPLEMENT フェーズで IS-01〜05 のIaCセキュリティ確認
  4. VERIFY フェーズで HA-01〜04 の可用性確認

品質ゲート:
  - 全リソースが1 subnet → public/private分離提案（NW-01 防止）
  - 0.0.0.0/0 inbound検出 → CIDR制限提案（NW-03 防止）
  - Action: "*" 検出 → 最小権限ポリシー提案（Wildcard Permissions 防止）
  - IAMアクセスキー使用 → IAM Roles移行提案（Long-lived Credentials 防止）
  - 暗号化未設定 → デフォルト暗号化有効化（IS-02 防止）
  - パブリックバケット → BPA有効化提案（IS-03 防止）
  - タグなしリソース → タグ戦略提案（No Tagging Strategy 防止）
  - 単一AZ構成 → Multi-AZ提案（NW-05 / HA-02 防止）
```

**Source:** [Datadog: 2025 State of Cloud Security](https://www.datadoghq.com/blog/cloud-security-study-learnings-2025/) · [Gomboc: IaC Security Best Practices 2026](https://www.gomboc.ai/blog/iac-security-best-practices-for-2026) · [AWS: VPC Security Best Practices](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-best-practices.html) · [Google Cloud: VPC Design Best Practices](https://cloud.google.com/architecture/best-practices-vpc-design)
