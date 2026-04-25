# AITuber Monetization

## Purpose

An AITuber that streams without a monetization plan ships as a hobby. With a plan, it can become a sustainable creator business — Super Chat reactions, channel memberships, sponsor segments, merchandise, donations. This reference covers integration patterns, persona-consistent reactions, regulatory compliance, and revenue-mix design.

## Scope Boundary

- IN scope: Super Chat / Bits / Stars / Donation reaction integration, membership / subscription tiers, sponsor segment design, merchandise tie-ins, persona-consistent reactions, tax / disclosure compliance per region, YouTube Partner Program / Twitch Affiliate-Partner thresholds.
- OUT of scope: chat platform technical integration (`chat`), TTS reaction audio (`tts`), avatar reaction animation (`avatar`), payment processing code (delegate to `builder` / `gateway`), full business strategy (delegate to `helm`), legal contracts (`clause`).

## Core Concepts

### Revenue Mix

A mature AITuber channel mixes 4–6 streams. Single-source dependency (e.g., 100% Super Chat) is fragile.

| Source | Typical share | Volatility |
|--------|--------------|------------|
| YouTube Super Chat / Super Stickers | 25–40% | Spike-driven |
| YouTube Channel Membership | 15–25% | Stable monthly |
| Twitch Bits | 15–30% | Spike-driven |
| Twitch Subscriptions | 20–35% | Stable monthly |
| Sponsor segments | 10–25% | Lumpy |
| Merchandise | 5–15% | Long-tail |
| Direct donations (Streamlabs / Ko-fi) | 5–10% | Spike-driven |
| Patreon / Pixiv FANBOX / FANTIA | 10–20% | Stable monthly |
| YouTube Premium revenue | 1–3% | Trickle |
| Sponsorship-product placement | 5–20% | Per-deal |

Rule of thumb: no single source > 50% of monthly revenue.

### Per-Platform Mechanics (2026)

#### YouTube

| Feature | Threshold | Notes |
|---------|-----------|-------|
| Partner Program (monetization) | 1,000 subs + 4,000 watch hours OR 10M Shorts views | Required for ads / Super Chat / Memberships |
| Super Chat | After Partner | $1–500 per message; chat-pinned; revenue share ~70% (US) |
| Super Stickers | After Partner | Pre-set sticker amounts |
| Super Thanks (replays) | After Partner | Tip on uploaded video |
| Channel Membership | 1,000 subs minimum | Tiered ($0.99–$99.99); custom emoji + perks |
| Live shopping | Eligible after Partner | Product tags during stream |
| Member-only streams | After Membership | Reserve content for paid tier |

#### Twitch

| Feature | Threshold | Notes |
|---------|-----------|-------|
| Affiliate | 50 followers + 500 min in 7 days + 7 unique days | Subs + Bits unlocked |
| Partner | Higher bar (3 streams a week + 75 avg viewers + 12+ days) | Better revenue split, ads control |
| Bits | After Affiliate | Cheering currency |
| Subs | After Affiliate | $4.99 / $9.99 / $24.99 monthly |
| Hype Train | Auto | Group cheer/sub events |
| Brand sponsorships (Twitch ads) | Affiliate+ | Programmatic pre-roll / mid-roll |

#### Bilibili (China)

| Feature | Notes |
|---------|-------|
| Stream gifts (礼物) | Highly active in JP/Chinese-VTuber audience |
| Charge / 充电 | Tip-style support |
| Member 大会员 sub | Paid platform tier; not creator-controlled |
| China-strict ToS | Political / LGBTQ+ restrictions |

### Persona-Consistent Reactions

The most critical AITuber-specific design: reactions must stay in character.

| Donation event | Generic reaction | Persona-tuned reaction |
|----------------|------------------|------------------------|
| First Super Chat | "Thank you!" | (Persona-specific catchphrase + name + emote) |
| Tier 1 sub | "Thanks for subbing!" | Persona's specific gratitude voice line |
| Hype Train start | "Wow!" | Persona-themed escalation pattern |
| Member milestone (1 yr) | "Thanks!" | Persona-personal anniversary line |
| Top donor of month | Generic shoutout | Persona-themed nickname for "regular" |

Method:

1. Pre-record 20–40 voice lines per donation tier in persona voice.
2. Tag with mood (excited / grateful / shocked / playful).
3. Sample randomly within tag on event.
4. LLM generates name-personalized line if dynamic name needed.
5. Cap LLM dynamic at 5 sec to maintain pacing.

Risk: scripted reactions feel robotic. Mitigation: 20+ variants per tier; randomize.

### Membership Tier Design

| Tier | Monthly | What viewer gets |
|------|---------|------------------|
| T1 ("regular") | $0.99–$2.99 | Custom emoji + member badge |
| T2 ("super fan") | $4.99–$9.99 | T1 + member-only chat + member-only stream |
| T3 ("patron") | $24.99–$49.99 | T2 + monthly Q&A + name in credits |
| T4 ("inner circle") | $99 | T3 + 1-on-1 mention per quarter |

Custom emoji is the killer perk — ~70% of subs cite it. Design 5–10 emoji per tier.

### Sponsor Segment Design

Sponsor segments embedded in AITuber streams need:

| Element | Spec |
|---------|------|
| Length | 30–90 seconds |
| Placement | Mid-stream beat (not opening); after a high engagement moment |
| Disclosure | Verbal "this segment is sponsored by ___" + on-screen graphic |
| Persona alignment | Sponsor's product fits persona's interests |
| Segue | Smooth transition before and after; not a hard cut |
| Frequency | ≤ 1 sponsor segment per 60-min stream |
| Pre-record vs live | Prefer pre-recorded for tone consistency |
| Voice license | Confirm sponsor's right to AITuber voice for the segment |

Bad sponsor fit damages trust; rejecting sponsors is a brand-protection move.

### Donation Gating

| Pattern | Healthy | Predatory |
|---------|---------|-----------|
| "Donate to unlock my song" | OK as a one-time milestone | Predatory if every interaction gated |
| Member-only stream | OK; tier benefit | Predatory if main content moves member-only |
| Early access for subs | Healthy | Predatory if delay > 48h on main content |
| Sub-only chat during stream | OK in spam waves | Predatory as default |
| "Donate or I won't stream" | Predatory | Always |
| Paid persona unlocks | OK as cosmetic | Predatory if affects gameplay |

EU Digital Fairness Act draft (2026) targets predatory creator monetization patterns.

### Tax and Disclosure

| Region | Requirements |
|--------|-------------|
| US | 1099-K from platforms > $20K threshold; self-employment tax |
| JP | 確定申告 mandatory for >¥200K side income; 雑所得 / 事業所得 classification |
| EU | VAT MOSS for digital services; per-country VAT rates |
| UK | Self Assessment for >£1K trading income |
| AU | Goods and Services Tax registration > AU$75K |
| Sponsor disclosure | FTC US, ASA UK, JFTC JP all require clear sponsor disclosure |
| AI-disclosure | EU AI Act 2025 mandates chatbot disclosure (also affects monetized AITubers) |

A creator should consult a regional accountant; this reference flags awareness, not legal advice.

### KYC / Identity

For payouts:

- Platforms require government ID verification.
- Bank account verification (often microdeposit).
- Tax forms (W-9 / W-8BEN / マイナンバー / etc.).
- Some platforms (Patreon) require Stripe Connect onboarding.

For an AITuber operated as a corporation: payout to the corp's bank, not a personal account, to keep persona separate from operator identity.

### AI Disclosure Pattern

EU AI Act + emerging US state laws + platform ToS converging on:

- Channel description includes "This is an AI character" or equivalent.
- First message of every stream includes disclosure (or pinned chat).
- Donation acknowledgments include "you supported an AI-driven creator".
- Persona invariant documents disclosure language.

Hidden AI status risks platform suspension and regulatory fines.

### Brand Safety for Sponsors

Sponsors typically require:

- Platform monetization-eligible status.
- Content rated general audience.
- Persona invariants reviewed.
- AI-disclosure compliance.
- Insurance / corporate entity (for larger deals).
- Contract with usage rights, exclusivity, takedown clauses.
- Content moderation logs available for review.

Smaller sponsorships skip several; larger ($10K+) require all.

### Member Retention

| Lever | Effect |
|-------|--------|
| Monthly member-only stream | +20% retention vs no member content |
| Custom emoji refresh quarterly | +10% retention |
| Member milestone shoutout | +15% retention at 6 mo / 1 yr |
| Member name in credits | +5% retention |
| Member-only Discord / community | +25% retention vs no community |

Don't onboard members and ignore them — month 1 → month 2 churn is the highest single drop.

### Revenue Forecasting

Healthy ratios for an AITuber at 5K–20K subs:

| Metric | Healthy |
|--------|---------|
| Average concurrent viewers | 50–500 |
| Super Chat revenue per stream | $50–$500 |
| Active members | 0.5%–2% of subs |
| Average member duration | 4–10 months |
| Monthly revenue (5K subs) | $500–$3K |
| Monthly revenue (20K subs) | $2K–$15K |
| Monthly revenue (100K subs) | $10K–$80K |

Numbers vary 5×+ by audience demographics, persona archetype, and content cadence.

## Workflow

1. **Set revenue-mix target** — define 4+ sources with no single > 50%.
2. **Verify platform thresholds** — Partner / Affiliate eligibility on each platform.
3. **Design membership tiers** — 3–4 tiers with custom emoji per tier.
4. **Author persona reaction library** — 20–40 voice lines per donation tier; mood-tagged.
5. **Define sponsor-segment policy** — fit criteria, frequency cap, disclosure pattern.
6. **Decide donation-gating rules** — what's behind a paywall vs free.
7. **Verify tax / disclosure compliance** — region-specific accounting, FTC / ASA / JFTC, AI disclosure.
8. **Set up KYC / payout flow** — bank account, tax forms, corp entity if needed.
9. **Build sponsor brand-safety packet** — persona invariants, moderation logs, insurance.
10. **Plan member retention** — monthly member stream, quarterly emoji refresh, milestone shoutouts.
11. **Forecast revenue** — based on audience size + persona archetype.
12. **Set quarterly review** — revenue-mix audit, sponsor performance, tier health.

## Output Template

```yaml
aituber_monetization:
  revenue_mix_target:
    youtube_super_chat: 30
    youtube_membership: 25
    twitch_subs: 0
    sponsor_segments: 20
    merch: 10
    direct_donation: 5
    patreon: 10
    no_single_source_above_pct: 50
  platforms:
    primary: youtube
    secondary: [twitch, bilibili]
    youtube_partner_eligible: yes
    twitch_affiliate_eligible: yes
  membership_tiers:
    - tier: T1
      price_usd: 1.99
      perks: [custom_emoji_5, badge]
    - tier: T2
      price_usd: 4.99
      perks: [T1 + member_chat + monthly_member_stream + custom_emoji_3]
    - tier: T3
      price_usd: 24.99
      perks: [T2 + quarterly_qa + name_in_credits + custom_emoji_2]
  persona_reactions:
    voice_lines_per_tier: 30
    mood_tags: [excited, grateful, shocked, playful]
    dynamic_name_via_llm: yes
    dynamic_cap_sec: 5
  sponsor_policy:
    max_per_60min_stream: 1
    length_sec_range: [30, 90]
    placement: mid_stream_after_high_engagement
    disclosure_verbal: yes
    disclosure_graphic: yes
    pre_recorded_preferred: yes
    fit_criteria: aligns_with_persona_pillars
  donation_gating:
    member_only_streams_per_month: 1
    main_content_member_only: no
    early_access_hours: 24
  compliance:
    tax_region: jp
    sponsor_disclosure_authority: jftc
    ai_disclosure:
      channel_description: yes
      stream_pinned: yes
      ttf_acknowledgment: "AIキャラクターを応援していただきありがとうございます"
  kyc_payout:
    entity:合同会社_aether
    bank: separate_corp_account
    tax_forms_filed: yes
  member_retention:
    monthly_member_stream: yes
    emoji_refresh_quarterly: yes
    milestone_shoutout_at: [3mo, 6mo, 12mo]
    discord_community: yes
  forecast:
    audience_subs: 12_000
    monthly_revenue_usd_range: [1500, 6000]
  quarterly_review_date: 2026-07-25
```

## Anti-Patterns

- 100% Super Chat dependency — single spike-driven source; no floor.
- Member onboarded but no member-only content — month-2 churn cliff.
- Generic "thanks" reactions to donations — viewers feel transactional.
- Sponsor segment that contradicts persona — trust damage outweighs revenue.
- Sponsor segment with no disclosure — regulatory risk.
- "Donate or I won't stream" framing — predatory; suspension risk.
- Member-only main content — dilutes free audience growth.
- Custom emoji never refreshed — perk goes stale.
- No AI disclosure — EU AI Act / platform ToS violation.
- Personal bank account for AITuber payout — exposes operator identity.
- Paid voice license unverified — copyright + commercial-use risk.
- Sponsor segment > 90 sec — viewer flight.
- Sponsor segments > 1 / hour — perceived as ad-stuffed.
- Donation gating every interaction — predatory; community alienation.
- Tax not filed at threshold — back-tax + penalty.
- No KYC verification — payout failure during peak revenue moment.
- Disclosure language hidden in description footer — non-compliant.
- Sponsor brand-safety packet absent — losing higher-value deals.
- Treating chat-tip donations as monthly recurring — they're spike-driven; budget conservatively.
- Using projection rather than median when forecasting — overconfident.

## Deliverable Contract

A monetization design is complete when:

- Revenue-mix target documented with 4+ sources and no single > 50%.
- Platform thresholds verified.
- Membership tiers designed with custom emoji per tier.
- Persona reaction library defined (≥ 20 voice lines per tier).
- Sponsor-segment policy specified with frequency cap and disclosure pattern.
- Donation-gating rules stated.
- Tax / FTC / ASA / JFTC / AI-disclosure compliance per region.
- KYC / corp-entity / bank flow set up.
- Member-retention plan documented.
- Revenue forecast provided as range.
- Quarterly review scheduled.

## References

- YouTube Partner Program documentation (2026 thresholds).
- Twitch Affiliate / Partner program documentation.
- Patreon Creator Documentation.
- Stripe Connect onboarding for creators.
- US FTC Endorsement Guides (16 CFR Part 255) — sponsor disclosure.
- UK ASA CAP Code — influencer-marketing rules.
- JFTC ステマ規制 (2023) — Japanese influencer-marketing law.
- EU Digital Fairness Act draft (2026) — predatory monetization framing.
- EU AI Act Article 52 — AI disclosure obligations.
- ElevenLabs Voice License terms.
- VOICEVOX engine commercial-use terms.
- 国税庁 確定申告のしかた (個人事業主・副業).
- IRS Schedule C / Schedule SE — US self-employment.
- Streamlabs / Ko-fi creator FAQ — donation flow design.
- VTuber industry reports — Cover Corp / Anycolor financial filings (revenue-mix benchmarks).
- Kevin Allocca, *Videocracy* (2018) — creator-economy framing.
- Li Jin, *The Passion Economy* — Patreon / membership design.
