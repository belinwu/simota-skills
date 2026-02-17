# Data Inputs Reference — Helm

入力データ種別・フォーマット仕様・不足時の対処法を定義する。

---

## Input Tier 定義

| Tier | 種別 | 説明 | 精度への影響 |
|------|------|------|------------|
| **Tier 1** | 必須入力 | これがないとシミュレーション不可 | 不可欠 |
| **Tier 2** | 推奨入力 | あると精度が大幅向上 | 高 |
| **Tier 3** | オプション入力 | 特定分析に必要 | 中〜低 |
| **Tier 4** | 外部データ | 公開情報・業界標準値で代替可能 | 代替可 |

---

## Tier 1: 最小入力セット

口頭説明でも可。数値があれば尚良し。

```yaml
# === 1A. 財務概況 ===
financial_overview:
  current_mrr: "¥Xm"                # または年間売上
  revenue_type: "SaaS|Product|Service|Mixed"
  growth_rate_ytd: "X%"             # 年初来成長率（任意）
  gross_margin: "X%"                # 粗利率
  operating_profit: "¥Xm or X%"    # 営業利益（額または率）
  cash_position: "¥Xm"             # 現金残高
  monthly_burn: "¥Xm"              # 月次バーン（スタートアップの場合）
  primary_model: "SaaS|Transaction|Project|Product|Hybrid"
  customer_type: "B2B|B2C|Both"
  avg_contract_value: "¥X"         # 平均契約単価

# === 1B. 市場・業界 ===
market_context:
  industry: "SaaS/HR|EC|FinTech|Healthcare|Manufacturing|..."
  target_market: "SMB|Mid-market|Enterprise|Consumer"
  geographic_scope: "Japan|APAC|Global"
  tam: "¥Xbn"                      # 口頭でも可
  market_growth_rate: "X%/year"    # 業界標準値での代替可
  competitive_position: "リーダー|チャレンジャー|ニッチャー|フォロワー"

# === 1C. 時間軸指定 ===
simulation_config:
  horizon: "SHORT|MID|LONG|ALL"    # 短期0-1年/中期1-3年/長期3-10年/全部
  priority_question: "string"      # 「何を知りたいか」を明示
```

**口頭説明で可能な例:**
> 「MRRは500万円で、月次成長率は約10%です。粗利は70%ほどで、キャッシュは3000万円あります」

→ Helmはこれをパースして仮定セットを構築する。

---

## Tier 2: 推奨入力（精度向上）

### 2A. KPIデータ

```yaml
kpi_data:
  total_customers: X               # 顧客数
  new_customers_per_month: X       # 新規獲得/月
  churn_rate_mrr: "X%"             # MRRベースチャーン率
  churn_rate_logo: "X%"            # ロゴチャーン率
  nps: XX                          # NPS
  cac: "¥X"                        # 顧客獲得コスト
  ltv: "¥X"                        # ライフタイムバリュー
  ltv_cac_ratio: "X.X"            # LTV/CAC比率
  payback_period: "Xヶ月"          # CAC回収期間
  magic_number: "X.X"             # SaaSグロース効率
  arpu: "¥X"                       # 平均月額単価
  expansion_revenue_rate: "X%"     # アップセル/クロスセル率
```

### 2B. 競合情報

```yaml
competitive_intel:
  direct_competitors:
    - name: "競合A"
      estimated_revenue: "¥Xm"    # 推定売上
      market_share: "X%"          # 市場シェア
      key_differentiators: ["差別化1", "差別化2"]
      recent_moves: "直近の動き"
  our_differentiation: "string"    # 自社の差別化ポイント
  win_rate: "X%"                   # 商談勝率
```

### 2C. 組織・人材情報

```yaml
organization:
  headcount_total: X               # 総人数
  headcount_by_function:           # 機能別: eng/sales/mkt/cs/ga
    engineering: X
    sales: X
    marketing: X
    cs: X
    ga: X
  personnel_cost: "¥Xm/月"        # 人件費
  personnel_ratio: "X%"           # 売上比人件費率
  planned_hires_next_12m: X        # 採用計画人数
  key_roles: ["役割1", "役割2"]    # 重要ポジション
```

---

## Tier 3: オプション入力（特定分析向け）

### 3A. ESGデータ（長期シミュレーション向け）

```yaml
esg_data:
  carbon_footprint: "tCO2e/年"     # CO2排出量
  reduction_target: "X% by YYYY"   # 削減目標
  supply_chain_risk: "高/中/低"    # サプライチェーンリスク
  employee_satisfaction: "X/5"     # 従業員満足度
  diversity_ratio: "X%"            # ダイバーシティ比率
  board_composition: "string"      # 取締役構成
  esg_rating: "A+|A|B+|B|..."     # ESGレーティング
```

### 3B. 製品情報（製品ポートフォリオ分析向け）

```yaml
product_portfolio:
  products:
    - name: "製品A"
      revenue_share: "X%"         # 売上構成比
      growth_rate: "X%"           # 成長率
      margin: "X%"                # 利益率
      stage: "Intro|Growth|Maturity|Decline"
  rd_budget: "¥Xm/年"             # R&D予算
  pipeline: ["開発中製品1", "開発中製品2"]
  time_to_market: "Xヶ月"          # 市場投入期間
```

### 3C. M&A / Exit関連（長期・Exit戦略向け）

```yaml
ma_exit_context:
  valuation_method: "Revenue Multiple|EBITDA Multiple|DCF"
  valuation_value: "¥Xm"          # 現在評価額
  revenue_multiple: "X.X"         # 売上倍率
  exit_timeline: "X年以内"         # Exit目標時期
  exit_preference: "IPO|Strategic M&A|PE|継続"
  investor_return_target: "X% IRR"
  existing_investors:
    - name: "VC/PE名"
      ownership: "X%"             # 持分比率
      invested_at: "YYYY"         # 投資年
      target_return: "X倍"        # 目標リターン
```

---

## Tier 4: 外部データ（Helmが標準値を適用）

データが提供されない場合、以下の標準値を使用し、前提として明示する:

| データ項目 | Helmが適用するデフォルト | 出典 |
|-----------|----------------------|------|
| SaaS中央値チャーン率 | MRRベース: 1-2%/月 | Bessemer / OpenView |
| SaaS粗利率 | 70-80% | SaaS業界標準 |
| 日本IT市場成長率 | 3-5%/年 | IDC Japan |
| CAC Payback期間 (B2B SaaS) | 12-18ヶ月 | Bessemer |
| LTV/CAC目標比率 | 3:1以上 | 業界標準 |
| SaaS Magic Number 健全値 | 0.75以上 | Salesforce創業者基準 |
| M&A SaaS Revenue Multiple | 5-8× ARR（成長率依存） | 市場標準 |
| 組織人件費比率（スタートアップ） | 60-70% | 一般的なスタートアップ |

---

## Input不足時の対処フロー

### Step 1: 不足データの識別

```
CRITICAL GAP（シミュレーション不可）:
□ 収益規模が全く不明
□ 時間軸指定がない
□ 業界・市場が不明

SIGNIFICANT GAP（精度低下）:
□ チャーン率不明 → 業界標準値を使用（明示）
□ 競合情報なし → 定性的評価のみ
□ 組織コスト不明 → P&L精度が低下

MINOR GAP（代替可能）:
□ ESGデータなし → 長期分析から除外
□ M&A詳細なし → オプション評価のみ
```

### Step 2-3: 対処と前提仮定の記載

- **CRITICAL** → `ON_DATA_INSUFFICIENT` トリガー発火 → AskUserQuestion で最小限の情報を取得
- **SIGNIFICANT** → 業界標準値を適用して続行 → 前提仮定セクションで明示
- **MINOR** → スコープを調整して続行 → 出力の制約事項として記載

前提仮定の記載例:

| 項目 | 使用値 | 根拠 | 実際値に置換を推奨 |
|------|--------|------|-----------------|
| チャーン率 | 1.5%/月 | B2B SaaS中央値 | ✅ |
| 粗利率 | 75% | SaaS業界標準 | ✅ |
| 市場成長率 | 8%/年 | 日本SaaS市場 (IDC 2024) | ✅ |

---

## Compete / Pulse からのハンドオフ形式

→ ハンドオフスキーマは references/handoffs.md を参照
