# Crypto Asset Taxation (暗号資産税制)

Reference for Levy's `crypto` recipe. Covers current comprehensive taxation regime, future separate taxation regime (令和8年度改正), event-type classification, cost basis methods, NFT/DeFi gray zones, and overseas exchange disclosure.

> Disclaimer: General explanation only. Crypto tax treatment is rapidly evolving — verify the latest NTA FAQ before filing. Individual situations require a registered 税理士.

---

## 1. Current Regime (through enactment of 金商法 amendment)

### Classification
- Crypto profits: **雑所得 (miscellaneous income)** by default
- Comprehensive taxation: combined with other income, taxed at progressive rates
- Effective max rate: **55%** (45% income tax + 10% resident tax + reconstruction)
- **Loss treatment: cannot offset against other income; cannot carry forward**

### Exception: business income classification
- If crypto trading is business-scale (規模, continuity, 反復継続性) → 事業所得
- Loss can offset other income (損益通算可) and carry forward 3 years (青色 only)
- Bar is high — NTA scrutinizes: separate office, employees, accounting books, primary income source

---

## 2. Future Regime (令和8年度改正で大綱決定)

### Effective date
- Application from year following 金融商品取引法 amendment enforcement
- 金商法 amendment bill planned for 2026 通常国会
- Earliest application: **2028 income (令和10年分)** — verify with NTA when bill passes

### New rules
- **申告分離課税**: rate **20.315%** (income 15% + resident 5% + reconstruction 0.315%)
- **3-year loss carryforward** (similar to 上場株式)
- Scope: only **金商法-registered crypto assets** (not all crypto)
- Likely excluded initially: NFTs, governance tokens with utility, native chain tokens not registered

### Likely transition risks
- Mid-year transactions split across regimes
- Taxpayers holding mix of registered and unregistered assets must classify
- DeFi yield, staking rewards, airdrops may stay 雑所得 even after reform

---

## 3. Event-Type Classification

| Event | Tax timing | Tax base | Income type |
|---|---|---|---|
| Sale (crypto → JPY) | At sale | Sale - cost | Misc / 事業 / 譲渡 (rare) |
| Exchange (crypto → crypto) | At exchange | FMV at exchange - cost of source | Misc |
| Use (crypto → goods/services) | At use | FMV used - cost | Misc |
| Mining receipt | At receipt | FMV at receipt | Misc / 事業 |
| Staking reward | At receipt | FMV at receipt | Misc |
| Airdrop receipt | At receipt | FMV at receipt | Misc (usually) |
| Lending interest | At accrual or receipt | Interest received | Misc |
| Lending repayment (crypto returned) | No event if same coin returned | — | — |
| Hard fork (new coin received) | NTA: at sale of new coin (cost basis = 0) | Sale price | Misc |
| Loan-borrowed crypto sold | At sale | Sale - cost (cost = repayment FMV est.) | Complex — refer 税理士 |

### Cost not recognized at exchange
Even crypto-to-crypto swaps trigger taxable events at full FMV — common pitfall.

---

## 4. Cost Basis Methods

### Default: 移動平均法 (moving average)
- Updated each acquisition: weighted average of all holdings
- Required unless 総平均法 election filed
- Election: 所得税の暗号資産の評価方法の届出書 — by filing deadline of first acquisition year

### Alternative: 総平均法 (annual average)
- Once per year, full-year weighted average
- Simpler but may diverge from real economic profit
- Lock-in: cannot switch back without 3-year minimum

### Calculation example (移動平均)
```
2026-01: Buy 1 BTC at ¥5,000,000 → avg cost ¥5,000,000
2026-03: Buy 1 BTC at ¥7,000,000 → avg cost (5M + 7M) / 2 = ¥6,000,000
2026-06: Sell 0.5 BTC at ¥4,500,000
  Proceeds: ¥4,500,000
  Cost: 0.5 × ¥6,000,000 = ¥3,000,000
  Gain: ¥1,500,000 (taxable as 雑所得)
  Remaining: 1.5 BTC at ¥6,000,000 avg
```

### Multiple exchanges
Aggregate across all exchanges and wallets — single cost-basis pool per coin per taxpayer.

---

## 5. NFT / DeFi Gray Zones

### NFTs
- Creator sale: 事業所得 if business / 雑所得 if hobby
- Buyer resale: 雑所得 (gain) typically; 譲渡所得 if used as personal collectible (rare)
- Royalty receipt: 事業 / 雑所得
- Cost basis: purchase price + gas

### DeFi
- LP token deposit: NTA position unclear — treat conservatively as taxable swap
- LP token withdrawal: same — treat as swap back
- Yield farming rewards: 雑所得 at receipt FMV
- Impermanent loss: not deductible until realized via withdrawal

### Wrapping / bridging
- WBTC ↔ BTC, ETH bridge: treat conservatively as swap (taxable)
- Aggressive position: same-asset wrapping is non-taxable — unsupported by NTA

### Staking lockup periods
- Reward at receipt timing, not unlock — but valuation may differ

### Recommendation
DeFi-heavy users → **L3 escalation** (registered 税理士 with crypto specialty).

---

## 6. Overseas Exchanges & Disclosure

### Exchange location does not affect taxation
Japanese tax residents owe tax on global crypto income regardless of exchange location.

### 国外財産調書 obligation
- Year-end overseas asset value ≥ ¥50M → file by 6/30
- Crypto on overseas exchange = 国外財産
- Penalty for omission: up to ¥500K + 5% surcharge increase

### 財産債務調書 obligation
- Income ≥ ¥20M AND assets ≥ ¥30M (or overseas assets ≥ ¥10M including crypto) → file with 確定申告
- Crypto holdings included in asset total

### OECD CARF (Crypto-Asset Reporting Framework)
- 2027-2028 onward: automatic exchange of crypto holdings between tax authorities
- Japan participating
- Undisclosed overseas crypto increasingly detectable
- Past omissions carry **重加算税 35%** + criminal exposure for willful evasion

### Recommendation
Hold overseas crypto → declare proactively. Voluntary disclosure mitigates penalties significantly vs detection.

---

## 7. Common Pitfalls

| Pitfall | Impact | Avoidance |
|---|---|---|
| Treating crypto-to-crypto swap as non-taxable | Multi-year underpayment | Every swap = taxable at FMV |
| Applying separate 20% taxation before 金商法 amendment | Major underpayment | Stay on comprehensive 雑所得 until enacted |
| Mixing exchanges without aggregating cost basis | Incorrect gain/loss | Aggregate per coin globally |
| Missing 国外財産調書 for overseas exchange holdings | ¥500K + 5% penalty | Track year-end FMV across all exchanges |
| Treating NFT sale as 譲渡所得 (favorable rates) | Reclassification at audit | Default to 雑所得 unless personal collectible test met |
| Losing crypto via hack — claiming as loss | Currently no loss treatment in 雑所得 | Document, but cannot offset (until reform) |
| Mining at small scale claimed as 事業所得 | 雑所得 reclassification | Need scale + continuity + books |
| 総平均法 → 移動平均法 mid-year switch | Disallowed; 3-year lock | Plan election carefully |

---

## 8. Decision Walkthrough Template

```
Tax year: ____ (令和__年分)
Resident status: 居住者 / 非永住者 / 非居住者
Crypto activity scale: hobby / part-time / business
Number of exchanges (incl. overseas): ____
Year-end overseas exchange FMV total: ¥____ (国外財産調書 ≥ ¥50M check)

For each event:
  Date: ____  Type: sale / exchange / use / mining / staking / airdrop / lending
  Coin: ____ amount: ____
  Cost basis (移動平均): ¥____
  FMV at event: ¥____
  Gain/Loss: ¥____

Annual aggregate:
  Net 雑所得 (crypto): ¥____
  Comprehensive taxation rate (combined with other income): __%
  Tax payable: ¥____

Disclosure obligations:
  □ 国外財産調書 (overseas ≥ ¥50M)
  □ 財産債務調書 (income ≥ ¥20M + assets ≥ ¥30M / overseas ≥ ¥10M)
```

---

## 9. Legal Basis & References
- 所得税法 第35条 (雑所得)
- 国税庁「暗号資産に関する税務上の取扱いについて(FAQ)」(latest revision)
- 令和8年度税制改正大綱 (separate taxation transition)
- 金融商品取引法改正案 (status: 2026 通常国会 予定)
- OECD CARF (Crypto-Asset Reporting Framework)
- 国送法 第5条 (国外財産調書)

## Disclaimer (Required in every output)
本資料は一般的な解説です。暗号資産税制は急速に変化しており、最新の国税庁FAQと改正情報を必ず確認してください。DeFi・NFT・海外取引所利用の個別判断は登録税理士への相談が必須です (税理士法第52条)。分離課税 20.315% 適用は金融商品取引法改正の施行後の年分のみ — 施行前年分への適用は重大な過少申告となります。
