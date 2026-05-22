# Gameplay Loop Design

## Purpose

Games are loops nested in loops. The 5-second loop hooks the hands; the 5-minute loop hooks the session; the 5-hour loop hooks the campaign. Designing only one fails; aligning all three is what produces "I'll just play one more turn."

## Scope Boundary

- IN scope: micro / mid / macro loop architecture, reward cadence, compulsion vs healthy engagement boundary, session-length design, pacing of novelty vs mastery, retention validation against benchmarks.
- OUT of scope: balance numbers (`balance`), narrative structure (`narrative`), monetization (`monetization`), visual / UX polish (delegate to `vision` / `palette`), code (`builder` / `forge`).

## Core Concepts

### The Three-Loop Hierarchy

| Tier | Duration | Question | Example |
|------|----------|----------|---------|
| Core (micro) | 5–30 seconds | "What does it feel like to do the verb?" | Aim → shoot → kill in *DOOM Eternal*; tap → match → pop in *Candy Crush* |
| Session (mid) | 5–30 minutes | "Why did this session feel complete?" | One mission run in *Hades*; one match in *League of Legends*; one expedition in *Hollow Knight* |
| Meta (macro) | 5–50 hours | "Why come back tomorrow?" | Build a settlement in *Stardew Valley*; complete the campaign in *Slay the Spire*; rank climb in *Apex* |

A player's loyalty progresses inward-out: the moment-to-moment must feel good before the long arc matters. If the 5-second loop is mediocre, the 5-hour loop cannot save it.

### The Core Loop Anatomy

Core loop = `Action → Feedback → Reward → New tension`.

| Element | Question | Failure Mode |
|---------|----------|--------------|
| Action | What does the player input? | Floaty controls; unclear affordance |
| Feedback | How does the system respond? | Slow; muffled; no juice |
| Reward | What does the player get? | Always the same; predictable |
| New tension | What pulls them in again? | Resolved too cleanly; no forward momentum |

**Juice** (game-feel) lives in feedback: screen shake, hit-stop, particle bursts, sound layering, controller rumble, color flashes. *Vlambeer's "The art of screenshake"* (2013) and Jan Willem Nijman's GDC talks remain the canonical references.

### Session Loop Anatomy

The 5-minute loop is the **completion satisfaction unit**. It must produce a felt sense of "that was a thing" within one session.

| Element | Pattern |
|---------|---------|
| Setup | Establish goal in 30 seconds (mission brief / wave start / hand dealt) |
| Build | Series of core-loop iterations with rising stakes |
| Climax | Spike of tension (boss / final wave / showdown) |
| Resolution | Reward + recap (XP gained / item earned / stats screen) |
| Hook | Next-session preview (preview next mission / unlock condition / item glimmer) |

Mobile and short-session games (puzzlers, roguelikes) demand tight 3–7 minute session loops. AAA single-player can stretch to 30–60 minute "epic" sessions but still benefits from sub-loops within.

### Meta Loop Anatomy

The 5-hour+ loop = persistent progression. Players come back because something accumulates.

| Pattern | Examples |
|---------|----------|
| Vertical (power up) | Levels, gear, stats — *Diablo*, *MMOs* |
| Horizontal (collect) | Decks, cards, characters, costumes — *Genshin*, *Pokémon* |
| Construct | Build a base / settlement / deck — *Factorio*, *Stardew* |
| Master (skill) | Visible skill ceiling — *Souls*, fighting games, *StarCraft* |
| Status (social) | Rank, prestige, leaderboard — *League*, *Apex*, *MMOs* |
| Narrative | Story revelations across hours — *Disco Elysium*, *Outer Wilds* |
| Habit | Daily / weekly cadence — *Animal Crossing*, gachas |

Strong meta loops mix 2–3 of these. Pure single-axis progression hits ceiling fast.

### Reward Cadence

Variable-ratio reinforcement (Skinner) is the most addictive schedule, but ethics demand restraint. Healthy reward cadence:

| Tier | Frequency | Examples |
|------|-----------|----------|
| Micro reward | Every action | Hit feedback, particle, sound |
| Mini reward | Every 30s–2min | Coin drop, level-up sparkle, combo |
| Major reward | Every 5–15 min | Boss kill, level cleared, item unlock |
| Pinnacle reward | Every 1–5 hours | Major story beat, prestige unlock, character ascended |

Skipping a tier produces "dead air"; over-rewarding any tier dulls all of them.

### The Compulsion-Loop Boundary

The line between **engagement** and **exploitation**:

| Healthy | Predatory |
|---------|-----------|
| Players choose when to play | Notifications + FOMO drive sessions |
| Sessions have natural endpoints | "Just one more" loops with no satisfying off-ramp |
| Reward unpredictability serves variety | Reward unpredictability serves payment leverage |
| Time investment compounds visibly | Time pressure punishes absence |
| Players can articulate why they enjoy it | Players express regret about play time |

Quest **must** flag designs that cross into predatory territory. The Pegg & Wood (2014) and CYP (2025) academic literature — and EU Digital Fairness Act draft — establishes that compulsive-loop design is now a regulatory issue, not just an ethical one.

### Pacing: Novelty vs Mastery

Within a session and across the campaign, balance:

| Tension | Ratio (rule of thumb) |
|---------|----------------------|
| New mechanics introduced | 1 per 30–60 min in early game; 1 per 2–3 hours in late game |
| Mastery moments (using known skills well) | 60–70% of total session time |
| Novelty surge (genuinely new) | 30–40% of total session time |
| Difficulty spike | Every 30–60 min (boss / wave / puzzle) |
| Calm beat | Every 15–25 min (resource gather / dialogue / cinematic) |

Too much novelty → cognitive overload, churn. Too much mastery → boredom, churn. The 60/40 ratio shifts as the player levels up.

### Loop Tightness

A loop is **tight** when each iteration ends with the next iteration's setup baked in.

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| Players quit after the level cleared | Loop ends, doesn't seed | Show next level's reward / preview before victory screen exits |
| Players quit after boss | Big resolution, no setup | Drop a new question (cliffhanger / NPC text / open door) |
| Players quit after gacha pull | Reward is the end | Show the next pull's possibility space (rate-up info, banner countdown) |

The mantra: **end every loop with a question, not an answer**.

### Retention Validation

Tie loop design to retention benchmarks (see Quest's Core Contract):

| Metric | Diagnosis |
|--------|-----------|
| D1 < 22% | Core loop weak; players don't see value in first session |
| D7 < 4% | Session loop weak; sessions don't feel complete |
| D28 < 3% | 75% of 2026 mobile games sit here; meta loop weak |
| DAU/MAU < 10% | Session-trigger weak; players don't form habit |
| DAU/MAU > 20% | Healthy engagement |
| DAU/MAU > 30% | World-class (or potentially predatory — investigate) |

These are global medians. Compare against **genre + platform + region** targets.

#### 2026 GameAnalytics Mobile Benchmarks (16,000+ live games tracked)

| Tier | D1 | D7 | D28-D30 |
|------|----|----|---------|
| Top quartile (excellence target) | 40%+ | 20%+ | 10%+ |
| Top 25% D7 | — | 7-8% | — |
| Median | ~22% | 3.4-3.9% | <3% (for 75% of games) |

**Genre-specific D30 (2026)**: Match games 7.15%, casino/tabletop 4-5.5%, puzzle 5.35%, RPG 3.48%, strategy 2-4%.

**Genre-specific D1 targets (2026)**: Casual / puzzle 40%+, mid-core 35%+, hardcore / RPG 30%+.

**Regional (2026)**: North America D1 ~30.26%; Japan D30 ~6.4% (≈2× the US rate of 3.72%).

Source: GameAnalytics *2026 Mobile & PC Gaming Benchmarks* / InvestGame summary 2026-01. Always cite the specific genre + platform + region rather than the global median when proposing a target.

### 5-Second / 5-Minute / 5-Hour Test

A canonical Quest exercise:

1. Pick a single verb (the core action).
2. Describe what makes it feel good in 5 seconds.
3. Describe what makes one session feel complete in 5 minutes.
4. Describe what makes a player return for 5 hours.
5. Confirm the three answers reinforce — not contradict — each other.

If the 5-second answer is "satisfying combo", but the 5-hour answer is "narrative arc", the design is at risk: the verb-driven hook may not survive the slow story.

## Workflow

1. **Articulate the verb** — single noun + single action.
2. **Design the core loop** — action / feedback / reward / new-tension.
3. **Audit juice** — each step has felt feedback (visual / audio / haptic).
4. **Design the session loop** — setup / build / climax / resolution / hook.
5. **Choose 2–3 meta-loop patterns** — vertical / horizontal / construct / master / status / narrative / habit.
6. **Cadence the rewards** — micro / mini / major / pinnacle frequency.
7. **Run the compulsion-boundary audit** — healthy vs predatory checklist.
8. **Pace novelty vs mastery** — 60/40 default; adjust per genre.
9. **Tighten loops** — end every loop with a question.
10. **Tie to retention benchmarks** — predict D1/D7/D30 and DAU/MAU.

## Output Template

```yaml
gameplay_loop_design:
  game: "Working title: BOLT"
  genre: roguelite_deckbuilder
  target_platform: pc + switch
  verb: "build a deck that solves a fight"
  core_loop:
    action: "play a card"
    feedback: "screen shake on hit; coin sound on cost paid; trail VFX"
    reward: "damage numbers + status icon + combo meter"
    new_tension: "next card draw revealed; opponent next intent shown"
    juice_audit:
      hit_stop_ms: 80
      screen_shake_intensity_px: 3
      sound_layers: 4
  session_loop:
    setup: "act start, deck shown, map node selected"
    build: "3-4 fights of rising difficulty; relics tempt"
    climax: "act boss with telegraphed wind-up"
    resolution: "deck post-mortem screen; runs stats"
    hook: "next-act preview reveals new biome enemy art"
    target_minutes: 25
  meta_loop:
    primary_pattern: collect    # unlock new cards / characters
    secondary_pattern: master   # ascension levels
    tertiary_pattern: narrative # story unlocks per character
  reward_cadence:
    micro_freq_sec: per_action
    mini_freq_sec: 30_to_120
    major_freq_min: 5_to_15
    pinnacle_freq_hour: 2_to_4
  compulsion_audit:
    natural_session_endpoints: yes
    notifications_drive_sessions: no
    fomo_pressure: low
    healthy: yes
  pacing:
    new_mechanic_per_run: 1
    mastery_ratio_pct: 65
    novelty_ratio_pct: 35
    difficulty_spike_min: 8
  loop_tightness:
    ends_with_question: yes
    next_unlock_visible_at_resolution: yes
  retention_targets:
    genre: roguelite
    platform: pc
    region: global
    d1_target: 35
    d7_target: 18
    d30_target: 8
    dau_mau_target: 22
  five_test:
    five_sec: "playing a card with a satisfying impact"
    five_min: "winning a fight by piecing together synergies"
    five_hour: "unlocking a new character whose deck plays differently"
    consistency_check: PASS
```

## Anti-Patterns

- Designing the meta loop first while the core loop is unspecified — long-term value with no moment-to-moment feel.
- Skipping the juice audit — mechanically correct but feels limp.
- Loops that end at the resolution with no hook — players leave at the natural off-ramp.
- Reward cadence skipping a tier (e.g., mini → pinnacle with no major) — dead-air zones.
- 5-second answer and 5-hour answer contradict — verb hook doesn't survive the campaign.
- Compulsion-loop design without examining the healthy / predatory boundary.
- Pure mastery loop with no novelty injection — boredom plateau.
- Pure novelty loop with no mastery — overwhelmed players.
- Daily-login bonus as the meta loop — weak; punishes absence rather than rewarding return.
- Notification-driven session triggers — predatory; flag immediately.
- "More content" as the meta-loop answer — content is fuel, not the engine.
- Loop diagrams without measurable rewards — feedback rituals without payoff.
- Retention targets pulled from global medians — under-investment; benchmark genre + platform + region.
- Sessions designed to be infinite — destroys completion satisfaction; players can't reach the "done for now" feeling.

## Deliverable Contract

A gameplay-loop design is complete when:

- Verb articulated as one action.
- Core loop has all four parts with juice audit.
- Session loop has 5 parts with target minutes.
- Meta loop names 2–3 patterns.
- Reward cadence specified across all 4 tiers.
- Compulsion audit passes (or predatory pattern flagged for explicit decision).
- Novelty/mastery ratio set.
- Loop tightness verified — every loop ends with a question.
- Retention targets cited per genre + platform + region (not global).
- 5-sec / 5-min / 5-hour test passes consistency.

## References

- Mihaly Csikszentmihalyi, *Flow: The Psychology of Optimal Experience* (1990).
- Daniel Cook, *The Chemistry of Game Design* (Lostgarden, 2007) — skill atom / loop framing.
- Jesse Schell, *The Art of Game Design* (3rd ed., 2019) — loop and lens taxonomy.
- Raph Koster, *A Theory of Fun for Game Design* (2nd ed., 2013) — pattern recognition / mastery.
- Jan Willem Nijman, *The art of screenshake* (Vlambeer, 2013) — juice canonical.
- Mark Brown, *Game Maker's Toolkit* (YouTube) — loop teardown series.
- Dan Cook & Steve Swink, *Game Feel* (2008) — micro-feedback theory.
- Nick Yee, *The Daedalus Project* / Quantic Foundry — motivation profiling.
- Amy Jo Kim, *Game Thinking* (2018) — habit/onboarding loops.
- Brendan Sinclair, *GamesIndustry.biz* — retention benchmarks.
- GameAnalytics annual *State of the Industry* — D1/D7/D30 by genre/platform.
- Adams, Pegg & Wood, *Compulsive video game playing*, *Cyberpsychology, Behavior, and Social Networking* (2014).
- Centre for Youth Policy / EU Digital Fairness Act draft (2026) — predatory-loop regulation.
- Yu-kai Chou, *Octalysis Framework* — eight motivational drives.
