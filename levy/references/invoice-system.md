# Invoice System (適格請求書等保存方式)

Reference for Levy's `invoice` recipe. Covers registration decision, transitional deduction schedule (revised by 令和8年度改正), 2割特例 / 3割特例 application, ¥100M per-supplier exclusion threshold, and simplified-taxation interaction.

> Disclaimer: General explanation only. Individual situations require a registered 税理士. AI-generated guidance does not substitute for professional advice (税理士法 compliance).

---

## 1. Registration Decision

### Who must register
- Taxable businesses (課税事業者) wanting to issue 適格請求書 to enable purchaser deduction
- Sole proprietors / corporations with prior-prior-year (基準期間) taxable sales > ¥10M (already 課税事業者 by default)

### Who chooses to register
- Tax-exempt small businesses (免税事業者) with B2B customers who require deduction
- Trade-off: gain customer retention vs lose tax exemption + new compliance burden

### Decision matrix

| Customer type | Customer's deduction need | Recommendation |
|---|---|---|
| B2C only (consumers) | None | Stay 免税 |
| B2B with small businesses | Customer uses 簡易課税 — deduction loss minimal | Likely stay 免税 |
| B2B with large businesses | Customer wants full deduction | Consider registration + 2割特例 |
| Mixed B2B/B2C | Depends on B2B share | Calculate breakeven |

### Registration application
- Form: 適格請求書発行事業者の登録申請書 (T-form)
- Submit to 所轄税務署
- Effective date: typically the 1st day of the next taxable period after acceptance, or chosen later date
- Cancellation: 適格請求書発行事業者の登録の取消しを求める旨の届出書 — effective from start of next taxable period

---

## 2. Transitional Deduction Schedule (令和8年度改正で延長)

Purchaser deduction rate when paying a 免税事業者 supplier (no 適格請求書):

| Period | Deduction rate | Note |
|---|---|---|
| 2023-10 to 2026-09 | 80% of input tax | Original schedule |
| **2026-10 to 2028-09** | **70%** | New tier (令和8年度改正 で追加) |
| **2028-10 to 2030-09** | **50%** | 2-year extension from original |
| **2030-10 to 2031-09** | **30%** | Final tier |
| 2031-10 onward | 0% | No deduction |

**Original schedule before 令和8年度改正:** 80% (3年) → 50% (3年) → 0%. The reform inserted 70% and 30% tiers, extending the transition by 2 years total to ease small-business migration.

### ¥100M Per-Supplier Exclusion (2024 改正で導入)
- If annual purchases from a single 免税 supplier > ¥100M (was ¥1B before 令和8年度改正), transitional deduction is **denied** for the excess.
- Threshold reduced to tighten loophole — large purchasers can no longer exempt by aggregation.
- Aggregation rule: per-supplier basis, taxable period.

### Invoice required line items (適格請求書記載事項)
1. 発行事業者の氏名・名称 + 登録番号 (T+13桁)
2. 取引年月日
3. 取引内容 (軽減税率対象は明示)
4. 税率ごとの取引金額 (税抜 or 税込) + 適用税率
5. 税率ごとの消費税額 (端数処理は税率ごとに1回)
6. 受領者の氏名・名称

### Simplified invoice (適格簡易請求書)
- Allowed for: 小売業, 飲食店業, 写真業, 旅行業, タクシー業, 駐車場業 (not reservation-based)
- Differences from full: receiver name optional, tax amount OR tax rate (not both required)

---

## 3. 2割特例 (令和5年度改正)

Inbound migration aid for businesses that became 課税事業者 only because of invoice registration.

### Eligibility
- Was 免税 in 基準期間 (prior-prior year)
- Became 課税 due to 適格請求書発行事業者 registration
- Period: **2023-10 to 2026-09** (only 3 years; not extended by 令和8年度改正)
- Both individuals and corporations eligible

### Calculation
- Consumption tax payable = sales 消費税額 × 20%
- No input deduction calculation needed
- No prior application required — choose at filing time

### Comparison example (annual sales ¥10M, 10% standard rate)
| Method | Sales tax | Input tax | Payable |
|---|---|---|---|
| 本則課税 | ¥1,000,000 | ¥600,000 | ¥400,000 |
| 簡易課税 (第3種 70%) | ¥1,000,000 | ¥700,000 | ¥300,000 |
| **2割特例** | ¥1,000,000 | ¥800,000 (みなし) | **¥200,000** |

**Switch flexibility:** can switch between 本則 / 簡易 / 2割特例 each filing year while eligible. Optimal strategy: re-evaluate annually.

---

## 4. 3割特例 (令和8年度改正で新設)

Post-2割特例 transitional aid. **Individuals only.**

### Eligibility
- Individual sole proprietors only (corporations excluded)
- Period: **2027 income (令和9年分) and 2028 income (令和10年分)** — 2 years
- Sales scale limit: TBD (likely tied to invoice-registration small-business definition; verify with NTA when finalized)

### Calculation
- Consumption tax payable = sales 消費税額 × 30%

### Comparison sequence for individual sole proprietor
| Year | Available | Likely best |
|---|---|---|
| 2023-2026 | 2割 / 簡易 / 本則 | 2割特例 |
| 2027-2028 | 3割 / 簡易 / 本則 | 3割特例 (slight tax increase from 2割) |
| 2029 onward | 簡易 / 本則 | 簡易課税 (if eligible) |

### Migration timeline guidance
- Plan cash-flow buffer for the 2割→3割→本則/簡易 step-up
- For corporations: directly transition from 2割→簡易 or 本則 in 2026-10

---

## 5. 簡易課税 (Simplified Taxation) Interaction

### Eligibility
- 基準期間 taxable sales ≤ ¥50M
- Prior application required: 消費税簡易課税制度選択届出書 by end of taxable period before application year

### Deemed input ratio (みなし仕入率)
| Category | Industry | Rate |
|---|---|---|
| 第1種 | 卸売業 | 90% |
| 第2種 | 小売業 | 80% |
| 第3種 | 製造業, 建設業, 農林漁業 | 70% |
| 第4種 | 飲食店業, その他事業 | 60% |
| 第5種 | サービス業, 金融業, 保険業, 運輸通信業 | 50% |
| 第6種 | 不動産業 | 40% |

### Switching constraints
- 2-year lock once selected
- Cannot switch to 本則 mid-period for refund

### Decision tree (per year while eligible for 2割/3割)
1. Estimate 本則 payable
2. Estimate 簡易 payable
3. Compare with 2割 / 3割 specials
4. Pick lowest — no prior election needed for 2割/3割

---

## 6. Common Pitfalls

| Pitfall | Impact | Avoidance |
|---|---|---|
| Applying 50% transitional rate from 2026-10 (instead of 70%) | Over-deducts input tax → 修正申告 + 過少申告加算税 | Verify revised schedule by date |
| Aggregating ¥100M threshold across periods | Wrong period basis | Apply per taxable period only |
| Corporation claiming 3割特例 | Disqualification, full back-tax | 3割特例 is individuals only |
| Skipping invoice 登録番号 verification | Customer deduction denied → relationship damage | Verify via 国税庁 適格請求書発行事業者公表サイト |
| Issuing invoices with wrong 端数処理 | Audit risk | Round per tax rate, once per invoice |
| Missing 軽減税率 (8%) split | Customer deduction denied | Separate 8% / 10% lines |
| Cancelling 課税 → losing eligibility for 棚卸資産 deduction | Lost ¥ on inventory | Plan cancellation timing carefully |

---

## 7. Decision Walkthrough Template

```
Year: ____ (令和__年分 / 20__ income)
Filing entity: 個人 / 法人
Prior-prior taxable sales: ¥____
Customer mix: B2C __% / B2B 簡易 __% / B2B 本則 __%
Annual purchases from 免税 suppliers: ¥____ (per supplier max ¥____)

Step 1 — Registration: Y / N
  Reason: ________________

Step 2 — Tax method this period:
  □ 2割特例 (eligible through 2026-09)
  □ 3割特例 (eligible 2027-2028, individuals only)
  □ 簡易課税 (種別 第__種, みなし率 __%)
  □ 本則課税

Step 3 — Estimated tax: ¥____

Step 4 — Transitional deduction applicable to purchases from 免税 suppliers:
  Period: ____ → rate __%
  ¥100M per-supplier check: _____
```

---

## 8. Legal Basis & References
- 消費税法 第30条 (仕入税額控除)
- 平成28年改正附則 (適格請求書等保存方式)
- 令和5年度税制改正 (2割特例新設)
- 令和8年度税制改正 (経過措置延長, 3割特例新設, ¥100M閾値)
- 国税庁「インボイス制度の概要」
- 国税庁 適格請求書発行事業者公表サイト

## Disclaimer (Required in every output)
本資料は一般的な解説であり、個別の税務判断には登録税理士への相談が必要です。AIによる助言は税理士業務に該当する個別判断を含みません (税理士法第52条)。最新の改正・経過措置適用日は国税庁公式情報で必ず確認してください。
