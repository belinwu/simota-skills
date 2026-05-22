# Economy Design

Currency systems, monetization models, inflation control, and ethical guidelines for game economies.

---

## Taps & Sinks Model

Every game economy is a flow system:

- **Taps** (sources): Where currency/resources enter the economy
- **Sinks** (drains): Where currency/resources leave the economy
- **Equilibrium**: Taps ≈ Sinks over time → stable economy

### Common Taps

| Tap | Type | Notes |
|-----|------|-------|
| Quest rewards | Finite | One-time; depletes over content lifecycle |
| Monster drops | Infinite | Must be rate-limited |
| Daily login | Infinite | Predictable income floor |
| Crafting/selling | Infinite | Player-driven; harder to control |
| Real-money purchase | Infinite | External injection; inflationary risk |
| Achievement rewards | Finite | Milestone-based |

### Common Sinks

| Sink | Type | Effectiveness |
|------|------|---------------|
| Consumables | Recurring | High — constant drain |
| Repair costs | Recurring | Medium — tied to activity |
| Fast travel fees | Recurring | Low — convenience tax |
| Auction house tax | Recurring | High — removes currency per transaction |
| Cosmetic purchases | One-time | Medium — voluntary but desirable |
| Upgrade costs (exponential) | Recurring | High — exponential scaling absorbs inflation |
| Crafting materials | Recurring | Medium — resource transformation |
| Guild/clan fees | Recurring | Low-medium — social pressure to pay |
| Prestige reset | One-time | High — voluntarily resetting progress for status |

---

## Castronova's Three Pillars

Edward Castronova's framework for virtual economies:

1. **Production**: How goods/currency are created (taps, crafting, drops)
2. **Distribution**: How goods move between players (trade, auction, gifts)
3. **Consumption**: How goods are destroyed/used (sinks, durability, consumables)

A healthy economy needs all three pillars balanced. Most economy failures come from weak consumption (insufficient sinks).

---

## Inflation Control Strategies

| # | Strategy | Mechanism | Example |
|---|----------|-----------|---------|
| 1 | **Transaction tax** | Remove % of currency per trade | 5% auction house fee (WoW) |
| 2 | **Repair costs** | Currency drain tied to activity | Equipment degradation (Dark Souls) |
| 3 | **Exponential upgrade costs** | Absorb accumulated wealth | Upgrade costs doubling per tier |
| 4 | **Limited inventory** | Cap hoarding | Bank slot limits, weight systems |
| 5 | **Seasonal resets** | Periodic economy wipe | Ladder seasons (Path of Exile) |
| 6 | **Bind-on-pickup** | Remove items from trade | Soulbound gear (WoW) |
| 7 | **Consumable meta** | Ensure constant resource drain | Potion/buff requirements for endgame |
| 8 | **Currency caps** | Hard limit on holdings | Maximum gold per character |
| 9 | **NPC price scaling** | Prices rise with server wealth | Dynamic vendor pricing |
| 10 | **Prestige systems** | Convert wealth to status | Spending currency for titles/cosmetics |

### Inflation Detection Metrics

- **CPI equivalent**: Track price of a basket of common items over time
- **Velocity of money**: How quickly currency changes hands
- **Gini coefficient**: Wealth distribution inequality (>0.6 = problematic)
- **New player purchasing power**: Can a new player afford basic gear?

---

## Dual Currency Design

Most F2P games use two currencies:

| Currency | Earned By | Spent On | Design Purpose |
|----------|-----------|----------|----------------|
| **Soft** (gold, coins) | Gameplay | Progression, consumables | Core loop reward |
| **Hard** (gems, crystals) | Real money (+ small gameplay) | Cosmetics, convenience, gacha | Monetization |

### Design Rules

- Soft currency should always be sufficient for core progression
- Hard currency should never be required for completing content
- Exchange rate (hard → soft) should be one-directional to prevent arbitrage
- Small hard currency trickle from gameplay (5-10% of what purchasers get) maintains F2P player engagement

---

## Gacha & Pity Systems

### Gacha Models

| Model | Description | Player Feel |
|-------|-------------|-------------|
| **Standard** | Fixed probability per pull | Unpredictable, can feel unfair |
| **Soft pity** | Rate increases after threshold | Building excitement |
| **Hard pity** | Guaranteed at N pulls | Safety net, budget planning |
| **Spark** | Choose any item after N pulls | Full control after investment |
| **Step-up** | Increasing value per sequential pull | Encourages multi-pull |

### Pity Math

```
P(getting item by pull N) = 1 - (1 - base_rate)^N        # without pity
P(getting item by pull N) = 1 - Π(1 - rate_i) for i=1..N  # with escalating pity
```

**Hard pity guarantee**: At pull N, rate = 100%.
**Soft pity example**: Base 0.6%, +6% per pull after pull 73, hard pity at 90. Expected pulls ≈ 62.

### Ethical Gacha Guidelines

- [ ] Display exact probabilities for all outcomes (mandatory under South Korea GIPA 2024 + December 2025 immediate-surcharge amendment; recommended by Japan METI / CESA self-regulation; required for PEGI 16 transparency from 2026-06)
- [ ] Implement pity/spark system (hard pity ≤ 200 pulls recommended; 2026 market norms: Genshin Impact 90 / Wuthering Waves 80 for character banner)
- [ ] Show pull history and pity counter
- [ ] No "bait and switch" — featured items must have stated rates (50/50 mechanic must be documented; Wuthering Waves' "no 50/50 on weapon banner + cross-banner pity carryover" is the 2026 player-favourable reference)
- [ ] Allow earning gacha currency through gameplay (not just purchase)
- [ ] Age-gate and spending limits for minors. **Brazil ECA Digital (Lei 15.211/25) effective 2026-03-17 bans loot-box sale to under-18s; penalties up to R$ 50 M / 10% of Brazilian revenue**
- [ ] No limited-time-only items that create FOMO pressure
- [ ] Apply PEGI 2026-06 reform impact: any gacha mechanic forces minimum PEGI 16, which excludes the under-16 EU audience entirely. Confirm publisher acceptance before locking the model

---

## Monetization Models

### Comparison

| Model | Revenue Source | Player Trust | Design Constraint |
|-------|---------------|-------------|-------------------|
| **Premium (B2P)** | Upfront purchase | High | Content must justify price |
| **Subscription** | Monthly fee | High | Constant content updates needed |
| **F2P + Cosmetics** | Optional cosmetics | Medium-high | Core game must be fully free |
| **F2P + Convenience** | Time-savers, boosts | Medium | Must not feel required |
| **F2P + Gacha** | Random reward pulls | Low-medium | Requires ethical safeguards |
| **F2P + P2W** | Power advantages | Low | Destroys competitive integrity |
| **Hybrid** | B2P + cosmetic MTX | Medium-high | No pay-for-power post-purchase |

### Ethical Monetization Principles

1. **No pay-to-win**: Purchased items must not provide competitive advantage
2. **Transparency**: All odds, rates, and contents clearly disclosed
3. **Respect time**: Paying accelerates, never gates core content
4. **No predatory FOMO**: Limited-time offers must not exploit urgency
5. **Child protection**: Age verification, spending caps, parental controls
6. **Earned, not rented**: Purchased items persist; no expiring purchases
7. **Value clarity**: Players understand exactly what they're buying

---

## Real-World Economy Failures

### Diablo II (2000s)
- **Problem**: Rampant duplication exploits flooded economy with gold and items
- **Result**: Gold became worthless; Stone of Jordan (SoJ) became de facto currency
- **Lesson**: Economy security is as important as economy design

### Diablo III Auction House (2012–2014)
- **Problem**: Real Money Auction House (RMAH) made playing for loot less satisfying than buying it
- **Result**: Core gameplay loop undermined; RMAH removed in 2014
- **Lesson**: Monetization must not shortcut the core game loop

### Venezuela's RuneScape Gold Farming (2017+)
- **Problem**: Real-world economic crisis drove mass gold farming
- **Result**: Hyperinflation in-game; legitimate players priced out
- **Lesson**: Virtual economies are not isolated from real-world pressures

### Star Wars Battlefront II (2017)
- **Problem**: Loot boxes provided gameplay advantages (P2W)
- **Result**: Massive backlash, government investigations, legislation changes
- **Lesson**: P2W + loot boxes = regulatory and reputational risk

### Belgium Loot-Box Ban Enforcement Gap (2018–2025)
- **Problem**: Belgium banned paid loot boxes in 2018, but 82% of top-100 iPhone games in Belgium still generated revenue via randomised monetisation (TheGamer / GameRant 2024-2025 studies). The Belgian Gaming Commission admitted in December 2024 that "this generalized ban proved difficult to enforce".
- **Result**: The Antwerp Enterprise Court ruled in **LS v Apple** on 2025-01-16, opening platform-operator (Apple) liability for distributing loot-box games into a Belgian market. Flemish Parliament committee discussions followed in January and March 2025.
- **Lesson**: Even where enforcement has historically been weak, court rulings can pivot platform-level liability suddenly. Don't bet a launch on lax enforcement of an existing ban — model the platform-operator-liability scenario.

### Roblox 2026 Adult Pivot
- **Problem (opportunity)**: Roblox identified the over-18 cohort as its largest untapped growth segment; only 26% of age-checked users were over 18 in early 2026, but U.S. over-18 users monetised >50% higher than under-18 users, and the 18-34 cohort grew >50% YoY.
- **Result**: 2026-04 announcement; effective 2026-06-08, Roblox raised the Developer Exchange (DevEx) rate by **42%** for in-game spend from age-checked U.S. 18+ players (effective creator earnings 26.6% → **37.8%**). Requires R15 avatars and supports a new recurring-subscription model. In 2025 Roblox creators earned over USD 1.5 B via DevEx.
- **Lesson**: Age-segmented monetisation can unlock significant developer revenue, but only when paired with platform-enforced age verification. Don't design adult-targeted economies without verifiable age gating.

---

## Economy Design Checklist

- [ ] All taps and sinks identified and documented
- [ ] Tap:sink ratio modeled for 30/90/365 day horizons
- [ ] New player purchasing power calculated
- [ ] Inflation detection metrics defined
- [ ] Currency cap or overflow handling designed
- [ ] Dual currency exchange rules specified (if applicable)
- [ ] Monetization model selected with ethical review
- [ ] Gacha probabilities disclosed and pity system designed (if applicable)
- [ ] Economy simulation spec prepared for Monte Carlo validation
