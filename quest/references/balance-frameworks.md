# Balance Frameworks

Mathematical foundations for game balance, difficulty tuning, matchmaking, and progression curves.

---

## Power Curves

### Exponential Growth (RPG Standard)

```
stat = base × (1 + rate)^level
```

| Parameter | Typical Range | Notes |
|-----------|---------------|-------|
| `base` | 10–100 | Starting stat value |
| `rate` | 0.05–0.15 | Growth per level (5–15%) |
| `level` | 1–100 | Player/enemy level |

**Example**: `HP = 100 × 1.08^level` → Level 50 HP ≈ 4,690

### Polynomial Growth (Gentler Scaling)

```
stat = base + (coefficient × level^exponent)
```

- Exponent 1.5–2.0 for moderate scaling
- Exponent 2.5–3.0 for steep late-game scaling
- Avoids the "number inflation" problem of pure exponential

### Fibonacci Difficulty Progression

Challenge rating follows a Fibonacci-like sequence where each encounter builds on the mastery of the previous two:

```
difficulty[n] = difficulty[n-1] + difficulty[n-2]
```

Practical variant: `difficulty[n] = difficulty[n-1] × 1.618` (golden ratio scaling)

### Sigmoid (S-Curve) Engagement

```
engagement = max_engagement / (1 + e^(-k × (time - midpoint)))
```

Models onboarding ramp-up → peak engagement → natural plateau. Useful for tutorial pacing and content gating.

---

## Combat Math

### DPS (Damage Per Second)

```
DPS = (base_damage × attack_speed) × (1 + crit_chance × (crit_multiplier - 1))
```

### TTK (Time To Kill)

```
TTK = target_HP / attacker_DPS
```

| Game Type | Target TTK | Notes |
|-----------|-----------|-------|
| Twitch shooter (CoD) | 0.2–0.5s | Positioning > reaction |
| Tactical shooter (Valorant) | 0.3–0.8s | Ability + aim |
| Hero shooter (Overwatch) | 1–3s | Team play > solo |
| MOBA (LoL) | 2–8s | Role-dependent |
| MMO PvP | 5–15s | Healer interaction |
| MMO PvE Boss | 180–600s | Raid coordination |

### EHP (Effective Hit Points)

```
EHP = HP / (1 - damage_reduction)
EHP = HP × (1 + armor / armor_constant)    # diminishing returns model
```

Armor constant determines diminishing returns curve. Common values: 50–200.

### Damage Reduction (Diminishing Returns)

```
reduction = armor / (armor + K)
```

Where K is the armor constant. At `armor = K`, reduction = 50%.

---

## Matchmaking

### Elo Rating

```
expected_score = 1 / (1 + 10^((opponent_rating - player_rating) / 400))
new_rating = old_rating + K × (actual_score - expected_score)
```

| K-Factor | Use Case |
|----------|----------|
| 32–40 | New players (high volatility) |
| 16–24 | Established players |
| 8–12 | Top-tier / ranked play |

### Glicko-2

Extends Elo with:
- **Rating Deviation (RD)**: Confidence interval. High RD = uncertain rating.
- **Volatility (σ)**: How erratic performance is.
- Rating adjustments scale with RD — uncertain players gain/lose more.

**When to use Glicko-2 over Elo**: Games with infrequent play sessions, team-based matchmaking, or where confidence intervals matter for queue fairness.

### SBMM (Skill-Based Matchmaking) Guidelines

- **Queue time vs match quality**: Target <60s queue, ±200 Elo spread maximum.
- **New player protection**: Separate pool for first 10–20 matches.
- **Smurf detection**: Flag accounts with >70% win rate in first 20 matches.
- **Team balancing**: Sum of team Elo within 2% of each other.

---

## Progression Math

### XP Curve (Level Requirements)

```
xp_required(level) = base_xp × level^exponent
```

| Exponent | Feel | Example |
|----------|------|---------|
| 1.5 | Gentle ramp | Casual mobile |
| 2.0 | Standard RPG | Most JRPGs |
| 2.5 | Hardcore grind | MMO endgame |

### Diminishing Returns (Soft Cap)

```
effective_stat = hard_cap × (1 - e^(-raw_stat / scale))
```

Prevents stat stacking. At `raw_stat = scale`, effective ≈ 63% of hard cap.

### Reward Scheduling

| Schedule | Pattern | Engagement Effect |
|----------|---------|-------------------|
| Fixed interval | Every N minutes | Predictable, lower excitement |
| Variable interval | Average N minutes | Sustained engagement |
| Fixed ratio | Every N actions | Grind-feeling |
| Variable ratio | Average N actions | Highest engagement (slot machine) |

**Ethical note**: Variable ratio is the most engaging but also the most potentially addictive. Use responsibly with transparent odds.

---

## Loot & Drop Math

### Expected Value (EV)

```
EV = Σ (probability_i × value_i)
```

### Pity System

```
effective_rate = base_rate + max(0, (attempts - pity_start) × escalation)
```

**Hard pity**: Guaranteed drop at attempt N. 2026-05 market references:
- *Genshin Impact*: 90 pulls (character banner), 80 pulls (weapon banner with Epitomized Path 1-fate guarantee)
- *Wuthering Waves*: 80 pulls (both character and weapon banner); no 50/50 on weapon banner; pity carries over between event banners

**Soft pity**: Increasing rate after threshold. Genshin: ramp begins around pull 73; Wuthering Waves: ramp begins from pull 50, so the felt pull cost is closer to 60 than 80.

When designing a new gacha system in 2026, Wuthering Waves' tighter pity + cross-banner carryover + no-weapon-50/50 is the **player-favourable reference**; Genshin Impact is the **conservative-but-tolerated** baseline. Anything looser than Genshin needs a clear ethical justification.

### Weighted Random with Rarity Tiers

| Rarity | Weight | Probability | 1-in-N |
|--------|--------|-------------|--------|
| Common | 60 | 60% | 1.7 |
| Uncommon | 25 | 25% | 4 |
| Rare | 10 | 10% | 10 |
| Epic | 4 | 4% | 25 |
| Legendary | 1 | 1% | 100 |

---

## Monte Carlo Methodology

When analytic solutions are impractical (complex interactions, emergent behavior):

1. **Define variables**: All stats, abilities, AI behaviors, RNG elements.
2. **Build simulation**: Run N combat/economy/session scenarios (N ≥ 10,000).
3. **Measure distributions**: Mean, median, std dev, percentiles (5th/95th).
4. **Identify outliers**: Scenarios where balance breaks (TTK < 0.1s, infinite loops, etc.).
5. **Iterate**: Adjust parameters, re-run until distributions meet design targets.

**Deliverable format**: Quest provides simulation specifications (parameters, scenarios, success criteria). Implementation runs in Forge/Builder.

---

## Spreadsheet Design Templates

### Balance Sheet Columns

| Column | Description |
|--------|-------------|
| Entity | Character/weapon/item name |
| Level/Tier | Power tier |
| Base Stat | Unmodified value |
| Formula | Growth function reference |
| Calculated | Result at target level |
| DPS | Damage output |
| TTK vs Tier | Time to kill same-tier target |
| Role | Tank/DPS/Support/Hybrid |
| Notes | Design intent, edge cases |

### Economy Sheet Columns

| Column | Description |
|--------|-------------|
| Source (Tap) | Where currency enters |
| Amount/hr | Rate of generation |
| Sink | Where currency exits |
| Cost | Price of sink |
| Time-to-earn | Hours to afford sink |
| Target ratio | Desired tap:sink balance |

---

## Quick Reference: Common Pitfalls

- **Number inflation**: Stats growing too fast makes differences meaningless. Use diminishing returns.
- **Linear scaling**: Feels boring after early game. Use polynomial or exponential.
- **No soft caps**: One stat dominates all builds. Add diminishing returns at 2× base.
- **Flat bonuses at high levels**: +5 damage matters at level 1, not at level 99. Use percentage bonuses.
- **Untested edge cases**: Always check min/max level, best/worst gear, 0-stat scenarios.

---

## Live-Service Balance Philosophy (2026 Reference: Riot Games)

For PvP and team-based live-service games, the 2026 reference patch philosophy from Riot:

- **Layered communication**: Riot ships **seasonal identity, accessibility features, and systemic balance changes** through regular live patches (LoL 26.x cadence), packaging gameplay and service content together via dev updates. Meta-break signals are cumulative — dev videos + patch notes + ranked-facing tests combine into a slower but still meaningful shift.
- **Lane / role agency**: The 2026 LoL season explicitly aimed to give laners more agency by reducing some automatic map protections — players should "enjoy the nuances of laning" without being pressured by early jungle intervention. Translation: when buffing one role, audit how it changes the moment-to-moment **decision space** for the role being buffed AND the roles around it.
- **Decision-space framing (Valorant)**: "All of our changes are aimed at supporting the different levels of decisions you make in VALORANT. The core game needs to support … different team compositions, a variety of attacker and defender strategies, and keep a mechanically deep combat system." When proposing a balance change, articulate which level of decision (team composition, strategy, mechanical execution) it primarily targets.
- **Ranked fairness as a balance vector**: 2026 Valorant communication framed ranked work as making the climb "feel fairer, more consistent, and more rewarding" — a player's rank should reflect real skill. Match-quality and rank-integrity belong in the balance frame, not separated as "matchmaking only".

Source: Sheep Esports / Esports Insider Riot dev-update coverage 2025-12 through 2026-04. Adopt these as default patterns for any live-service balance design unless the project explicitly diverges.
