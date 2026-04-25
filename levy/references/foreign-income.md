# Foreign Income & Overseas Assets (国外所得・海外資産)

Reference for Levy's `foreign` recipe. Covers residency classification, taxation scope by status, foreign tax credit calculation, 国外財産調書 / 財産債務調書 obligations, CFC (タックスヘイブン対策税制) basics, and OECD CRS automatic exchange exposure.

> Disclaimer: General explanation only. International tax is highly fact-dependent — verify with a registered 税理士 specializing in international tax (国際税務).

---

## 1. Residency Classification

### Three categories

| Status | Definition | Taxation scope |
|---|---|---|
| **居住者** (Resident) | Domicile in Japan, OR continuous residence ≥ 1 year | Worldwide income |
| **非永住者** (Non-permanent resident) | Resident, no Japanese nationality, AND aggregate residence in Japan ≤ 5 years out of past 10 | Japan-source + foreign income paid in or remitted to Japan |
| **非居住者** (Non-resident) | Not 居住者 | Japan-source income only |

### 5-year rule (非永住者)
- Counts aggregate residence days within trailing 10-year window
- "Year" = 12 months count, not calendar year
- Once accumulated > 5 years → automatic shift to 永住者 (full worldwide taxation)
- Major life event: many expats face large tax shock at year 6

### Domicile (住所) judgment factors
- Family location (spouse, children)
- Economic center (income source, assets)
- Daily life base (home, utilities)
- Stay duration & frequency
- No single decisive factor — facts-and-circumstances test

### Tax treaty override
- Bilateral tax treaties may modify residency determination (tie-breaker rules)
- Common factor order: permanent home → center of vital interests → habitual abode → nationality → mutual agreement
- Treaty residency overrides domestic status for treaty-protected income types

---

## 2. Taxation Scope by Status

### 居住者 (Resident)
- All worldwide income subject to Japanese tax
- Foreign tax credit available for double-taxed income
- Major income types: 給与, 事業, 利子, 配当, 不動産, キャピタルゲイン

### 非永住者 (Non-permanent resident)
- Japan-source income: full taxation
- Foreign-source income: taxable only to extent **paid in Japan** OR **remitted to Japan** in the same year
- "Remittance" includes credit card payment in Japan funded from overseas account
- Tax planning opportunity — but documentation burden is heavy

### 非居住者 (Non-resident)
- Japan-source income only (rental of Japanese real estate, employment in Japan, etc.)
- Withholding rates apply at source
- Filing required only for certain categories

### Common Japan-source income examples
- Salary for work performed in Japan (regardless of payer)
- Rent from Japanese real estate
- Interest from Japanese bonds/deposits
- Dividends from Japanese companies
- Capital gain on Japanese real estate sale
- Royalties for use in Japan

---

## 3. Foreign Tax Credit (外国税額控除)

### Purpose
Eliminate double taxation when 居住者 owes Japanese tax on income already taxed abroad.

### Eligibility
- 居住者 only (非永住者: only on income taxed under Japanese rules)
- Foreign tax must be:
  - Income tax equivalent
  - Paid by the taxpayer (not entity)
  - Final and not refundable

### Calculation formula
```
Credit limit (per year) = Japanese tax × (国外所得 / 全世界所得)

Allowed credit = min(foreign tax paid, credit limit)
```

### Three credit categories
1. **Income tax credit limit**: against national income tax
2. **Resident tax credit limit**: 12% × national income tax credit limit
3. **Carryover**: 3-year unused credit carryforward + 3-year excess foreign tax carryforward

### Worked example
```
Japanese tax (worldwide): ¥3,000,000
World income: ¥10,000,000 (Japan ¥7M + Foreign ¥3M)
Foreign tax paid: ¥800,000

Credit limit = 3,000,000 × (3,000,000 / 10,000,000) = ¥900,000
Allowed credit = min(800,000, 900,000) = ¥800,000

Final Japanese tax = 3,000,000 - 800,000 = ¥2,200,000
```

### Source-rule mismatches
- Different countries may classify income differently (e.g., US treats stock options as compensation; Japan may differ)
- Treaty re-sourcing rules may apply
- Hybrid entities: complex — refer specialist

---

## 4. 国外財産調書 (Overseas Assets Report)

### Filing obligation
- 居住者 (excluding 非永住者) holding overseas assets with year-end (12/31) FMV total ≥ **¥50M**
- Filing deadline: **6/30** of following year (separate from 確定申告)

### Reportable assets
- Real estate (with appraised value)
- Bank accounts
- Securities (stocks, bonds, funds)
- Insurance with cash value
- Crypto on overseas exchanges
- Loans receivable
- Art, jewelry (if FMV identifiable)

### Valuation
- Year-end FMV in JPY (use 12/31 closing rate)
- Real estate: estimated market value (acquisition cost + improvements is acceptable if FMV not available)
- Securities: market price or recent transaction price

### Penalty for omission/false statement
- 5% reduction in normal penalty when properly filed and audit reveals understatement
- 5% increase in penalty when not filed and overseas asset income found
- **Up to ¥500K fine + 1 year imprisonment** for willful non-filing or false statement
- Adjustment surcharge does not apply if voluntary correction filed before audit notice

### Common pitfalls
- Forgetting overseas crypto exchange holdings
- Joint accounts: report your share
- Real estate held via foreign LLC: may need both 国外財産調書 and CFC consideration

---

## 5. 財産債務調書 (Asset & Liability Report)

### Filing obligation (令和5年度改正で要件追加)
File when ANY of the following:
- Income ≥ ¥20M AND year-end total assets ≥ ¥30M
- Income ≥ ¥20M AND year-end overseas assets ≥ ¥10M (lower threshold for overseas)
- Year-end total assets ≥ ¥1B (regardless of income)

### Reportable
- All major assets (Japan + overseas)
- Liabilities ≥ ¥10M
- Filed with 確定申告

### Penalty
- Same 5% adjustment mechanism as 国外財産調書

---

## 6. CFC (タックスヘイブン対策税制 / 外国子会社合算税制)

### Purpose
Prevent income shifting to low-tax foreign subsidiaries.

### Trigger
- Japanese resident holds **≥ 10%** (directly or via family/related) of a foreign corporation
- Foreign company effective tax rate < trigger threshold (varies: 20% for paper companies, 27% for some categories)

### Result
- Foreign company's passive income (or all income for paper companies) is included in Japanese shareholder's income annually, even without distribution

### Income categories (post-2017 reform)
- Paper company / cash box / black-list jurisdiction company → full inclusion regardless of effective tax rate
- Active business with sufficient substance → only passive income inclusion if passive income > de minimis
- Active business with substance and effective tax ≥ 20% → no inclusion

### Common situations
- Family holding company in Cayman / BVI
- Single-member LLC in low-tax US state (state tax may matter)
- Hong Kong / Singapore subsidiary with passive investment income
- Web business "registered" abroad while operated from Japan

### Recommendation
Any 10%+ ownership of foreign entity → **L3 escalation**, mandatory specialist consultation.

---

## 7. OECD CRS (Common Reporting Standard) — Automatic Exchange

### What
- 110+ jurisdictions automatically exchange financial account information with each other
- Banks/brokers report account balance, interest, dividends to local tax authority
- Local authority forwards to taxpayer's residence country tax authority

### Japan's participation
- NTA receives CRS data from partner jurisdictions annually since 2018
- Cross-references with declared income and 国外財産調書

### Detection mechanics
- Undeclared overseas account → CRS data → NTA mismatch detection → audit
- Past omissions: typical penalties **重加算税 35%** + **延滞税** (~14.6%/year)
- Willful evasion: criminal exposure

### What's covered
- Bank accounts, brokerage accounts, certain insurance contracts
- Crypto: covered under separate **CARF** framework (effective 2027-2028)
- Real estate: not directly covered, but financial flows often visible

### Recommendation
Any overseas account → declare promptly. Voluntary disclosure (修正申告 before audit notice) typically reduces penalty from 35% to 5% additional surcharge.

---

## 8. Common Pitfalls

| Pitfall | Impact | Avoidance |
|---|---|---|
| Treating self as 非居住者 while domiciled in Japan | Worldwide income unreported | Apply domicile test correctly |
| Forgetting overseas crypto in 国外財産調書 | ¥500K fine + 5% penalty | Track all overseas exchanges at year-end FMV |
| Missing 5-year non-permanent → permanent transition | Sudden full worldwide taxation shock | Track aggregate residence days |
| Claiming foreign tax credit for non-creditable taxes | Disallowed at audit | Verify foreign tax is income-tax equivalent + paid |
| Not splitting credit limit between 国 and 地方 | Underutilized credit | Apply both income tax and resident tax limits |
| Family LLC abroad ignored under CFC | Annual income inclusion + back tax | Specialist consult on any 10%+ foreign holding |
| Remittance trigger ignored for 非永住者 | Foreign income brought in is taxable | Track remittances carefully, including credit-card |
| Treaty residency tie-break ignored | Double taxation or wrong residency | Read applicable treaty Article 4 |

---

## 9. Decision Walkthrough Template

```
Tax year: ____ (令和__年分)
Nationality: ____
Domicile: Japan / abroad
Aggregate residence in Japan (last 10 years): ___ years
Residency: 居住者 / 非永住者 / 非居住者
Treaty applicable: Y / N (country: ____)

Income inventory:
  Japan-source income: ¥____
  Foreign-source income: ¥____ (paid/remitted in Japan: ¥____)
  Total taxable: ¥____

Foreign tax paid: ¥____
Credit limit (national): ¥____
Allowed credit: ¥____

Disclosure obligations:
  □ 国外財産調書 (overseas assets year-end ≥ ¥50M, due 6/30)
  □ 財産債務調書 (income ≥ ¥20M + assets ≥ ¥30M / overseas ≥ ¥10M)
  □ CFC inclusion (foreign company ≥ 10% holding)

Risk flags:
  □ Crossing 5-year non-permanent → permanent (planning needed)
  □ Foreign LLC / cash-box exposure
  □ Overseas crypto exchange holdings (CARF-detectable from 2027-2028)
  □ Past undeclared overseas account (voluntary disclosure recommended)
```

---

## 10. Legal Basis & References
- 所得税法 第2条 第1項 第3-5号 (居住者・非永住者・非居住者定義)
- 所得税法 第7条 (課税所得の範囲)
- 所得税法 第95条 (外国税額控除)
- 国外送金等調書法 第5条 (国外財産調書)
- 国外送金等調書法 第6条の2 (財産債務調書)
- 租税特別措置法 第40条の4 (タックスヘイブン対策税制)
- OECD「自動的情報交換 (CRS)」スタンダード
- OECD「Crypto-Asset Reporting Framework (CARF)」
- 各国との租税条約 (居住者性 tie-breaker)

## Disclaimer (Required in every output)
本資料は一般的な解説です。国際税務は事実関係に強く依存し、租税条約・各国制度の影響も大きいため、登録税理士 (国際税務専門) への相談が必須です (税理士法第52条)。CFC・国外財産調書・CRS関連の判断は税理士業務に該当する個別判断を含みます。OECD CRS により海外金融口座は税務当局に自動共有される時代であることに留意してください。
