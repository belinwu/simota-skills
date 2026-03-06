# Cost Management / FinOps Anti-Patterns

> クラウドコスト管理、FinOps実践、リソース最適化、コミットメント戦略の失敗パターン

## 1. コスト管理 7 大アンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **CO-01** | **Over-Provisioning（過剰プロビジョニング）** | 必要以上のインスタンスサイズ/数を常時稼働 | CPU使用率<20%、メモリ使用率<30%のインスタンス群 | 右サイズ化: CloudWatch/Compute Optimizer分析→1サイズダウン |
| **CO-02** | **Zombie Resources（ゾンビリソース）** | 停止/未接続リソースが課金され続ける | 未アタッチEBS、停止EIP、空ALB、古いスナップショット | 定期棚卸し: idle resource検出→削除/archive自動化 |
| **CO-03** | **No Tagging Strategy（タグ戦略なし）** | リソースにタグがない/不統一 | コスト帰属不能、chargeback/showback不可 | 必須タグ（Environment/Service/Owner/CostCenter）+ ポリシー強制 |
| **CO-04** | **Commitment Misalignment（コミットメント不整合）** | インフラロードマップと無関係にRI/SP購入 | $300K 3年RI購入後にコンテナ移行、65%が無駄に | 購入前にインフラロードマップと整合、Flexibleタイプ優先 |
| **CO-05** | **NAT Gateway Cost Explosion（NAT Gateway課金爆発）** | 全outbound通信がNAT Gateway経由 | NAT Gatewayが月額コスト上位、$0.045/GB課金 | VPC Endpoints活用、S3/DynamoDB Gateway Endpoint無料 |
| **CO-06** | **Data Transfer Blindness（データ転送コスト盲目）** | クロスAZ/リージョン/インターネット転送量を無視 | 月末に予期せぬ転送費、マルチAZ通信で$数千 | 転送パターン可視化、同一AZ配置、CloudFront/CDN活用 |
| **CO-07** | **Environment Always-On（環境常時稼働）** | dev/staging環境が24/7稼働 | 週末・夜間も非本番環境が課金、全体の20-30%を占有 | スケジュール停止（夜間/週末）、Instance Scheduler/Lambda |

---

## 2. FinOps実践の罠

```
FinOps組織の失敗:

  ❌ Siloed Teams（サイロ化チーム）:
    → 財務・開発・運用が別々にコスト管理
    → コミットメントを財務が購入、開発がコンテナ移行を計画→不整合
    → 対策: FinOpsチーム横断、購入決定にエンジニアリング参加

  ❌ Reactive Cost Management（事後対応型コスト管理）:
    → 月末の請求書で初めて問題を認識
    → 異常支出が30日間放置、対応が後手に
    → 対策: 日次/週次のコスト異常検知アラート（AWS Cost Anomaly Detection）

  ❌ Manual Optimization（手動最適化）:
    → スプレッドシートでコスト分析、手動でリサイズ
    → スケールしない、頻度が月次/四半期で遅い
    → 対策: 自動右サイズ化ツール、自動スケジュール停止

  ❌ Cost Visibility Gap（コスト可視性ギャップ）:
    → 一部のアカウント/サービスのみ追跡
    → シャドウIT的に利用されるサービスが盲点
    → 対策: 全アカウント統合ダッシュボード、CUR (Cost and Usage Report) 分析

  ❌ Aggressive Cost Cutting（過度なコスト削減）:
    → ビジネス影響を無視してリソース縮小
    → トラフィックスパイク時にautoscalingが追いつかず、収益損失
    → 対策: コスト最適化はビジネスKPIと連動、バッファを確保
```

---

## 3. コミットメント戦略のアンチパターン

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **CM-01** | **All-or-Nothing Commitment（全額コミット）** | 使用量の100%をRI/SPでカバー | ワークロード変動時に余剰、柔軟性喪失 | 60-70%をSP/RI、残りをOn-Demand/Spotで柔軟性確保 |
| **CM-02** | **Long-Term Lock Without Roadmap（ロードマップなし長期固定）** | 3年RIを購入後にアーキテクチャ変更 | コンテナ/サーバーレス移行でRIが無駄 | 1年Convertibleから開始、アーキテクチャ安定後に3年検討 |
| **CM-03** | **Instance Family Lock-in（インスタンスファミリー固定）** | 特定のm5.xlargeでRI購入 | Graviton(m7g)移行時に割引適用不可 | Compute Savings Plans（ファミリー/リージョン柔軟） |
| **CM-04** | **No Coverage Tracking（カバレッジ追跡なし）** | SP/RI購入後に利用率を確認しない | 購入額の30%が未使用、節約効果が実感できない | 週次利用率モニタリング + 未使用SP/RIの是正 |

---

## 4. リソース最適化の罠

```
最適化の失敗:

  ❌ CPU-Only Right-Sizing（CPU単一軸の右サイズ化）:
    → CPU使用率だけでリサイズ判断
    → メモリ/ネットワーク/IOのボトルネックを見逃す
    → 対策: CPU + メモリ + ネットワーク + ディスクIOの4軸分析

  ❌ Spot Without Fallback（Spot無保険運用）:
    → Spot Instanceのみで構成、中断時のフォールバックなし
    → Spot回収で一時的にキャパシティゼロ
    → 対策: Spot + On-Demand混在、Spot Fleet多様化、中断ハンドリング

  ❌ Storage Class Ignorance（ストレージクラス無視）:
    → 全データをS3 Standard / gp3に配置
    → アクセスされないデータに高いストレージ単価
    → 対策: Lifecycle Policy（Standard→IA→Glacier）、Intelligent-Tiering

  ❌ Log Retention Unlimited（ログ無制限保持）:
    → CloudWatch Logs / Cloud Loggingの保持期間を設定しない
    → ログストレージが際限なく増大
    → 対策: 環境別保持期間（dev:7日/staging:30日/prod:90日）+ S3エクスポート

  ❌ Uncompressed Data Transfer（非圧縮データ転送）:
    → API/Lambda/ECS間で非圧縮JSONを転送
    → データ転送量増大、NAT/インターネットゲートウェイ課金増
    → 対策: gzip圧縮、Protocol Buffers、VPC内通信活用
```

---

## 5. コスト見積もり・予算管理の罠

| # | アンチパターン | 問題 | 兆候 | 対策 |
|---|-------------|------|------|------|
| **BU-01** | **No Budget Alerts（予算アラートなし）** | AWS Budgets/GCP Billing Budgets未設定 | 月末に驚きの請求書、クレジット枯渇に気づかない | 50%/80%/100%/120%の段階的アラート |
| **BU-02** | **Single Global Budget（単一グローバル予算）** | アカウント全体で1つの予算のみ | どのサービス/チームが超過しているか不明 | チーム×環境×サービスの粒度で予算設定 |
| **BU-03** | **No Cost Estimation Before Deploy（デプロイ前見積もりなし）** | terraform applyしてから月末にコスト判明 | 想定外のサービス費用、予算超過 | Infracost統合: PR時にコスト差分表示 |
| **BU-04** | **Historical-Only Forecasting（過去ベースのみ予測）** | 過去の使用量だけで予算策定 | 新機能リリース/キャンペーン時に大幅超過 | ビジネスイベントカレンダーと予算連動 |

---

## 6. 2025年 クラウドコスト統計

```
業界データ:

  💰 クラウド廃棄物: $44.5B（2025年予測）
  📊 企業のクラウド支出のうち28-35%が無駄
  📈 67%の組織が予想以上のクラウドコストを経験
  🏢 82%のグローバル組織でクラウド支出の10%以上が浪費
  💻 35-45%のVM/コンテナが過剰プロビジョニング（8-12%の超過コスト）
  🏚️ 停止/未使用リソースが月次請求の10-15%
  🚀 スタートアップ/SMBは25-32%のクラウド支出を浪費
  🏷️ タグコンプライアンス90%以上で10-15%の無駄削減
```

---

## 7. Scaffold との連携

```
Scaffold での活用:
  1. ASSESS フェーズで CO-01〜07 のコスト設計スクリーニング
  2. DESIGN フェーズで CM-01〜04 のコミットメント戦略確認
  3. IMPLEMENT フェーズで BU-01〜04 の予算管理設定
  4. VERIFY フェーズで Infracost によるコスト見積もり確認

品質ゲート:
  - CPU使用率<20%のインスタンス → 右サイズ化提案（CO-01 防止）
  - 未アタッチEBS/未使用EIP検出 → 削除提案（CO-02 防止）
  - タグなしリソース → タグ追加提案（CO-03 防止）
  - NAT Gateway課金上位 → VPC Endpoints導入（CO-05 防止）
  - 非本番環境24/7稼働 → スケジュール停止提案（CO-07 防止）
  - 予算アラート未設定 → Budgets設定提案（BU-01 防止）
  - terraform planにコスト差分なし → Infracost統合（BU-03 防止）
```

**Source:** [ProsperOps: Cloud Cost Optimization Strategies](https://www.prosperops.com/blog/cloud-cost-optimization-strategies/) · [DataStackHub: Cloud Wastage Statistics 2025-2026](https://www.datastackhub.com/insights/cloud-wastage-statistics/) · [Quinnox: 10 FinOps Best Practices 2025](https://www.quinnox.com/blogs/finops-best-practices/) · [Cloudaware: FinOps Framework Top 10 Mistakes](https://cloudaware.com/blog/finops-framework/)
