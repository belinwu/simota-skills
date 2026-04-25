# Monetization Design

## Purpose

Monetization is a design system, not a billing decision. The model chosen — premium, F2P, hybrid, subscription, battle pass — shapes the core loop, the economy, and the player relationship. This reference catalogs models, gacha math, ethical and regulatory boundaries, and the audit protocol every monetization design must pass.

## Scope Boundary

- IN scope: model selection, price-point design, battle-pass structure, gacha math (pity systems, probability disclosure), regulatory audit (EU Digital Fairness Act, EU age-rating uplift, Brazil under-18 ban, Belgium prohibition), predatory-pattern audit.
- OUT of scope: payment-system code (delegate to `builder`), tax / GAAP revenue recognition (out of domain), App Store / Play Store policy specifics (review platform docs separately), retention strategy (`retain`), pricing-experiment statistical design (`experiment`).

## Core Concepts

### Model Selection

| Model | Best For | Risk |
|-------|----------|------|
| Premium (one-time) | Single-player, narrative, indie | Limited LTV; 1× transaction |
| Premium + DLC | Single-player + post-launch content | DLC fatigue; cannibalization |
| Subscription | Service games, MMOs, online single-player | Churn-driven |
| F2P + IAP | Mobile, social, live-service | Whales; predatory risk |
| F2P + Battle Pass | Live-service, GaaS | Treadmill fatigue |
| F2P + Cosmetics only | PVP / multiplayer with strong identity | Lower ARPU, defensible |
| Hybrid (premium + IAP) | AAA single-player + season pass | Player perception of double-charge |
| Ad-supported | Casual mobile | Low ARPU; cap at clear floor |

Pick the model based on:

1. Genre conventions (players know what to expect).
2. Engagement loop length (short sessions favor IAP; long campaigns favor premium).
3. Audience age & region (regulatory + cultural).
4. Production scale (live ops needs the live-service model).
5. Studio values (defensible cosmetic model vs whale-driven gacha).

### F2P Architecture

A F2P game is three economies in one:

| Layer | Currency | Role |
|-------|----------|------|
| Soft currency | Gold / coins | Earned by play; spent on common items |
| Hard currency | Gems / crystals | Earned slowly + bought; spent on premium |
| Time | Energy / cooldowns | Limits free play; bypass via hard currency |

Healthy F2P design:

- Soft currency caps grind; hard currency caps wallet dependency.
- Premium-only cosmetics; gameplay accessible without payment.
- Pity / mercy mechanics on randomness.
- Probability disclosure on every randomized reward.
- Daily / weekly missions reward time, not wallet.

Predatory F2P flags:

- Pay-to-win in PVP.
- Energy systems that gate progression behind hard currency.
- Time-limited offers with no cooldown.
- Push notifications driving session start.
- Wallet abstraction (display in points, not local currency).
- Random rewards without probability disclosure.

### Battle Pass Design

| Element | Best Practice |
|---------|--------------|
| Duration | 6–12 weeks |
| Tiers | 50–100 |
| Free track | Always present, includes meaningful rewards |
| Premium track | Pay once, earn over duration |
| Premium+ tier | Optional accelerator; should not skip earned content |
| Tier skip | Optional, priced to feel like a luxury not a necessity |
| Catch-up | Bonus XP or weekly challenges so latecomers can complete |
| Rewards | Mix cosmetics, currency, gameplay extras |
| Carryover | Unused XP / progress for next pass (Player-positive) |

Antipattern: pass tiers gated behind grind that requires daily play. Healthy passes complete with 4–6 hours / week.

### Gacha Math

Gacha = randomized reward purchase. Math:

| Concept | Definition |
|---------|------------|
| Base rate | Probability per pull of drawing a target rarity |
| Pity (hard) | Guaranteed target after N pulls without one |
| Pity (soft) | Increasing rate after threshold |
| Spark / mileage | Currency earned per pull, redeemable for direct purchase |
| Banner | Time-limited featured pool with rate-up |
| Rate-up | Higher chance for specific items within banner |
| Off-banner / off-rate | Drawing a target that isn't the featured one |

Standard gacha rates (2026 market norms):

| Rarity | Base Rate |
|--------|-----------|
| Top tier (5★) | 0.6%–1.6% |
| Rate-up specific | ~50% of top-tier draws |
| Hard pity | 90 / 180 / 200 pulls |
| Soft pity ramp | Starts at pull ~75, increases per pull |

Probability disclosure is **mandatory** in 2026 — both for player trust and regulatory compliance (EU age-rating, Apple / Google policy, Japan METI guidelines, China NPPA disclosure rule).

### Regulatory Map (2026)

| Region | Status |
|--------|--------|
| EU | Digital Fairness Act draft expected Q3 2026; enforcement ~2029. May classify aggressive F2P loops as deceptive design. Existing: PEGI age-rating uplift for loot boxes (2025). |
| Belgium | Full prohibition on paid loot boxes since 2018. |
| Brazil | Under-18 loot box ban effective March 2026. |
| Netherlands | Loot boxes with marketable items = gambling. |
| China | NPPA disclosure rules; minor playtime caps; IP-tied identity. |
| Japan | METI guidelines on probability disclosure; complete-gacha banned since 2012. |
| US (federal) | No federal loot box law as of 2026; FTC investigations active. |
| US (states) | Various; NY, MN consider age-gating. |
| UK | DCMS calling for industry self-regulation; ongoing review. |
| South Korea | Probability disclosure mandatory (Game Industry Promotion Act, 2024). |

Quest **must** flag regional risk in every monetization design.

### Predatory Pattern Audit

Run on every model:

| Pattern | Audit Question |
|---------|---------------|
| Pay-to-win | Does spending give competitive advantage in PVP / shared leaderboards? |
| FOMO pressure | Are time-limited offers paired with countdown anxiety? |
| Notification grind | Do push notifications drive sessions? |
| Sunk cost | Does the game punish absence (decay, missed dailies)? |
| Wallet abstraction | Is hard-currency price disconnected from local fiat display? |
| Random reward without disclosure | Are loot boxes / gacha rates hidden? |
| Soft pity hidden | Is the soft pity ramp documented to players? |
| Limited-time exclusive | Are key gameplay items time-locked? |
| Targeted pricing | Are higher prices shown to identified high-spenders ("whale targeting")? |
| Loss-aversion design | Does the UI emphasize what the player loses by not paying? |

Each "yes" requires either a design change or an explicit ethical-flag note.

### Ethical Whales

A "whale" = top 1% of spenders. Healthy F2P serves whales without exploitation:

- Whale spending is bounded — no unlimited rolls; pity caps a value.
- Whale rewards are cosmetic / collection — not pay-to-win.
- Whale community is acknowledged (collectors, completionists), not extracted.
- Spending limits tools available (self-imposed wallet cap, monthly cap, parental control).

Predatory whales: design rewards spending up to 1000 USD / month with no safeguards.

### Pricing Tactics

| Tactic | Healthy Use | Predatory Misuse |
|--------|-------------|------------------|
| Anchor pricing | "Was 1200, now 800" with real prior price | Fake "was" price |
| Bundle discount | Bundle saves 15–30% over individual | Bundle includes filler the player doesn't want |
| Limited-time offer | Genuine seasonal cadence (new year, summer) | Daily 30-min countdown timers |
| Whale tier | Premium currency packs scale with bonus | "Tycoon pack" 100 USD with marginal value bonus |
| First purchase doubler | One-time onboarding bonus | "Triple offer" repeating |
| Subscription value | Monthly value > monthly cost via guaranteed content | Subscription required to access bought content |

### LTV and ARPDAU Targets

Healthy model targets (2026 market):

| Metric | Mobile F2P (Top 25%) | Console / PC GaaS |
|--------|---------------------|-------------------|
| Day-1 conversion | 1.5–4% | 5–15% |
| Day-30 conversion | 3–8% | 10–25% |
| ARPDAU | 0.10–0.40 USD | 0.30–1.50 USD |
| ARPPU (paying users) | 25–80 USD | 15–60 USD |
| Paying player share | 1–4% | 8–18% |
| LTV / CAC ratio | > 3 | > 2 |

Pure cosmetic models compress ARPPU to 5–25 USD but spread paying-player share to 5–10%.

### Ethical Probability Disclosure Format

Required for every randomized reward in 2026:

```
SR (3★) ........ 75.00%
SSR (4★) ....... 22.00%
UR (5★) ........  3.00%
  └ rate-up: 1.50%   (50% of UR drawn = featured)
  └ off-rate: 1.50%

Soft pity begins at pull 75; rate increases by 0.32% per pull.
Hard pity: pull 90 guarantees UR.

50/50 banner: First UR may be off-rate; next UR guaranteed featured.

Disclosure version: 2026-04-15  (effective from this banner forward)
```

Display in-game in 2 taps from any banner. Never bury in EULA.

## Workflow

1. **Choose model** — premium / F2P / hybrid / subscription / battle pass / ad / cosmetic-only.
2. **Justify with audience + genre + region**.
3. **Map currencies** — soft / hard / time, with caps.
4. **If F2P + gacha** — set base rates, pity, banner cadence, disclosure spec.
5. **If battle pass** — duration, tiers, free vs premium track, catch-up rules.
6. **Run regulatory map** — flag risk per target region.
7. **Run predatory-pattern audit** — 10-question checklist.
8. **Set whale boundaries** — wallet caps, parental controls, tools.
9. **Specify pricing tactics** — anchor / bundle / limited-time / first-purchase.
10. **Project LTV / ARPPU / ARPDAU** — with 25th / 50th / 75th percentile targets per genre.
11. **Author the disclosure** — explicit text, in-game placement.
12. **Hand off** — implementation to `builder`; user-facing copy to `prose`; A/B testing to `experiment`; dashboard to `pulse`.

## Output Template

```yaml
monetization_design:
  game: "BOLT"
  genre: roguelite_deckbuilder
  platform: pc + mobile
  model: hybrid
  premium_tier:
    price_usd: 19.99
    includes: full_campaign + cosmetic_starter_pack
  f2p_tier:
    available: yes
    limits: 3_runs_per_day; access_to_2_of_5_characters
    upgrade_path: one_time_payment_to_premium
  cosmetic_shop:
    primary_currency: gems
    avg_price_usd: 4.99
    rotation: weekly
  battle_pass:
    enabled: yes
    duration_weeks: 8
    tiers: 60
    free_track_meaningful_rewards: yes
    premium_price_usd: 9.99
    plus_tier_price_usd: 19.99
    plus_tier_skips_content: no
    catchup_xp: yes
  gacha:
    enabled: no
  currencies:
    soft:
      name: gold
      cap: 999_999
      faucets: [run_completion, dailies]
      sinks: [character_unlocks, card_upgrades]
    hard:
      name: gems
      cap: 99_999
      faucets: [pass_tier_rewards, daily_login_low_amount]
      sinks: [cosmetics, optional_continue_token]
    time:
      energy_system: no
  predatory_audit:
    pay_to_win: no
    fomo_pressure: low
    notification_grind: no
    wallet_abstraction: no       # gem prices show local fiat equivalent
    random_disclosure_required: no  # no gacha
    limited_time_exclusive: only_seasonal_cosmetics
    targeted_pricing: no
    audit_pass: yes
  regulatory:
    eu_age_rating_uplift: not_applicable    # no loot boxes
    eu_digital_fairness_act: monitor_2026   # no current trigger
    brazil_under_18_lootbox_ban: not_applicable
    belgium_paid_lootbox_ban: not_applicable
    south_korea_disclosure: not_applicable
    overall_risk: low
  whale_safeguards:
    wallet_cap_monthly_usd: 200
    parental_controls: yes
    self_imposed_limit_tool: yes
  ltv_targets:
    arppu_usd: 28
    paying_player_share_pct: 6
    ltv_cac_ratio: 2.4
  handoff:
    builder: storefront_implementation
    prose: storefront_copy + disclosure_copy
    experiment: pricing_tier_ab_test
    pulse: monetization_dashboard
    cloak: pii_review_for_purchase_flow
```

## Anti-Patterns

- Pay-to-win in PVP — instant predatory flag; reject.
- Energy systems that gate progression behind hard currency — predatory.
- Loot boxes without probability disclosure — regulatory non-compliance + trust loss.
- Random rewards with marketable / trade-able outputs — gambling classification in NL, BE.
- Wallet abstraction (game points, no fiat shown) — predatory; forbidden in many regions.
- Limited-time offer with countdown timer < 1 hour — FOMO-engineered; predatory.
- Push notifications driving session start — predatory; flag.
- Battle pass that requires 6+ hours / day to complete — fatigue; high churn.
- Battle pass premium+ tier that skips earned content — feels like double-charge.
- Subscription required to access previously bought content — trust-destroyer.
- Targeted pricing showing higher prices to whales — predatory; legal risk.
- Probability rates buried in EULA, not in-game.
- Hidden soft-pity ramps — players sense them, lose trust when not disclosed.
- Pay-to-skip-grind without offering grind-skip via play — pure pay-gate.
- Ignoring regional regulation — Brazil, Belgium, NL classifications kill launches.
- Marketing the game as "free" while gating progression — UK CMA enforcement risk.

## Deliverable Contract

A monetization design is complete when:

- Model chosen with rationale tied to audience + genre + region.
- Currencies mapped with caps + faucets + sinks.
- If F2P + gacha: base rates, pity, banner cadence, disclosure spec authored.
- If battle pass: duration, tiers, free track, catch-up rules specified.
- Regulatory map applied per target region.
- Predatory-pattern audit run with 10 questions; each "yes" addressed.
- Whale safeguards documented (cap, parental, self-limit).
- LTV / ARPPU / paying-share targets stated.
- Pricing tactics specified.
- Probability disclosure format authored if applicable.
- Handoff briefs prepared for builder, prose, experiment, pulse.

## References

- Ramin Shokrizade, *The Top F2P Monetization Tricks* (Gamasutra, 2013) — predatory pattern catalogue.
- Daniel Cook, *Lostgarden* — F2P design ethics.
- Adams, Pegg & Wood, *Compulsive video game playing*, Cyberpsychology (2014).
- Drachen, Sifa, Bauckhage, Canossa, *Game Data Mining* (2013) — LTV / ARPPU methodology.
- Will Luton, *Free-to-Play: Making Money From Games You Give Away* (2013).
- Ben Cousins, *The Future of F2P* (Casual Connect talks).
- DeltaDNA / GameAnalytics annual *State of the Industry* — ARPDAU / ARPPU / paying-share benchmarks.
- EU Commission, *Digital Fairness Fitness Check* (2024–2026) — Digital Fairness Act prep.
- Belgian Gaming Commission, *Research report on loot boxes* (2018).
- UK CMA, *Online consumer protection* — F2P misleading practices.
- METI (Japan), *Self-regulation guidelines on online games* — gacha disclosure norms.
- South Korea *Game Industry Promotion Act* (2024 amendment) — probability disclosure.
- Apple App Store Review Guidelines § 3.1.1 — IAP and loot box disclosure.
- Google Play Developer Program Policy — Real-money gambling rules.
- Yu-kai Chou, *Octalysis Framework* — distinguishing healthy and predatory drives.
- ESRB, PEGI 2025 update — loot box age-rating uplift.
- Mihaly Csikszentmihalyi, *Flow* — distinguishing engagement from compulsion.
