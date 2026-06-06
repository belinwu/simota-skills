# Character Progression

Purpose: Define Realm's character progression mechanics — the six stats and their formulas, the derived Power level, and the XP / rank / level system that drives long-term agent growth.

Contents:
- Stat formulas and data sources
- Power level (derived from stats)
- Bar rendering and profile types
- Update frequency and cold-start handling
- Rank thresholds and titles
- Level math
- XP sources (task / activity / collaboration)
- XP decay rules
- Promotion behavior and rank benefits
- XP display format

## Overview

Each agent has six stats scored `0-100`. Realm derives them from observable ecosystem data only. The stats combine into a single **Power** level, while accumulated **XP** drives **Rank** and **Level** progression independently. Together these form the agent's character progression model: stats describe *what the agent is capable of right now*, while XP/rank describe *how far the agent has come*.

## Stats

### Stat Formulas

| Stat | Meaning | Data sources | Formula | Key adjustments |
|---|---|---|---|---|
| `STR` | Output power | `PROJECT.md`, commit contributions, artifact volume | `activity_count = entries in last 90d` → `normalized = min(activity_count / median_activity_all_agents, 2.0)` → `STR = round(normalized * 50)` | Non-code categories use report or analysis counts. Agents younger than 30 days get `×1.2` to reduce cold-start penalty. |
| `DEX` | Versatility | Distinct task types, chain patterns, cross-category work | `DEX = round((task_types / max_types) * 100)` | Specialists normalize against category peers. Minimum `DEX = 10` for any active agent. |
| `INT` | Complexity handling | Sherpa complexity, chain depth, Nexus contribution | `avg_complexity = avg complexity (1-5)`; `chain_depth_bonus = avg chain position * 5`; `INT = round(min((avg_complexity / 5) * 75 + chain_depth_bonus, 100))` | If Sherpa data is missing, estimate complexity from chain length. Meta agents (`Darwin`, `Realm`, `Sigil`) gain `+15 INT`. |
| `WIS` | Learning rate | Journal growth, pattern reuse, Lore references | `growth_rate = recent_30d_entries / max(previous_30d_entries, 1)`; `base_wis = min(growth_rate * 30, 60)`; `lore_bonus = 5 * metapattern_refs` capped by total `100` | Agents younger than 60 days with more than 5 entries get `+20`. Stale journals (`>60 days`) cap `WIS` at `30`. |
| `CHA` | Collaboration | Chain participation, unique partners, completion with others | `partner_ratio = unique_partners / total_agents`; `CHA = round(min(collab_count * 2 + partner_ratio * 60, 100))` | Commander-class agents gain `+15 CHA`. Solo specialists have a floor of `20`. |
| `CON` | Reliability | AUTORUN outcomes, recovery count, Darwin RS | `success_rate = SUCCESS / total_tasks`; `recovery_bonus = recovery_count * 5` up to `20`; `rs_factor = Darwin_RS / 100 * 20`; `CON = round(min(success_rate * 60 + recovery_bonus + rs_factor, 100))` | Agents with fewer than 5 tasks use the ecosystem average as a baseline. Perfect success over 20+ tasks gains `+10`. |

### Power Level

Power is a weighted aggregate over the six stats — the single headline number for an agent's current capability.

```
Power = (STR*20 + DEX*15 + INT*20 + WIS*15 + CHA*15 + CON*15) / 100
```

STR and INT carry the heaviest weight (`20` each); DEX, WIS, CHA, CON each weight `15`. Power therefore moves whenever any stat moves, but never decouples from the underlying six.

### Bar Rendering

```
segments = round(stat_value / 10)
filled = '█' * segments
empty = '░' * (10 - segments)
bar = '[' + filled + empty + ']'
```

Example: `82 -> [████████░░]`

### Profile Types

| Profile | Condition | Label |
|---|---|---|
| Balanced | All stats within 20 points of mean | Well-Rounded |
| Physical | `STR + CON > 160` | Powerhouse |
| Mental | `INT + WIS > 160` | Intellectual |
| Social | `CHA + DEX > 160` | Versatile |
| Tank | `CON > 85` | Ironclad |
| Glass Cannon | `STR > 85` and `CON < 40` | Glass Cannon |

### Update Frequency

- Recalculate stats on each `/Realm` or `/Realm agent` invocation.
- Persist historical stat snapshots in `.agents/realm-state.md`.
- Show deltas as `↑`, `↓`, or `→` compared with the previous stored state.

### Cold-Start Handling

| Situation | Behavior |
|---|---|
| No activity data | Show all stats as `??` and bars as `[??????????]`. |
| Partial data (`<5` tasks) | Calculate only supported stats; leave missing stats as `??`. |
| New agent (`<14 days`) | Mark stats as provisional with a `*` suffix. |

## Rank & XP

Stats reflect current capability. Rank and XP track long-term progression — they only grow (or decay) over time, never recalculated from scratch.

### Rank Thresholds

| Rank | XP Required | Title | Badge Color | Description |
|---|---|---|---|---|
| F | 0 | Recruit | Gray | Newly registered, minimal activity |
| E | 100 | Novice | White | Beginning to contribute |
| D | 500 | Apprentice | Green | Regular contributor |
| C | 1,500 | Journeyman | Blue | Reliable, consistent performer |
| B | 4,000 | Veteran | Purple | Experienced, proven track record |
| A | 8,000 | Elite | Gold | Top-tier performer |
| S | 15,000 | Champion | Orange | Ecosystem pillar |
| SS | 30,000 | Legend | Red | Defining presence in the ecosystem |

### Level Calculation

Levels provide finer-grained progress within ranks.

```
level = floor(sqrt(total_xp / 2))
```

Maximum display level is `99`. Agents above `19,602 XP` display `Lv.99+` until Rank `SS`.

### XP Sources

#### Task Completion XP

| Task Type | Base XP | Condition |
|---|---|---|
| Single-agent task | 20 | Common quest completed |
| Multi-agent chain participant | 40 | Uncommon chain completed |
| Complex chain participant | 80 | Rare chain with 4+ agents completed |
| Parallel branch chain | 150 | Epic parallel chain completed |
| Titan product lifecycle | 300 | Legendary lifecycle delivered |

#### Outcome Modifiers

| Outcome | Modifier | Condition |
|---|---|---|
| `SUCCESS` | ×1.0 | Standard completion |
| `PARTIAL` | ×0.5 | Some deliverables produced |
| `BLOCKED` | ×0.2 | Attempted but blocked |
| `FAILED` | ×0.0 | No usable output |
| First-time task type | ×1.5 | Agent's first time handling that task type |
| Streak bonus | ×1.2 | `3+` consecutive `SUCCESS` outcomes |

#### Activity XP

| Activity | XP | Cap |
|---|---|---|
| Journal entry added | 10 | `5/day` |
| Pattern discovered | 25 | No cap |
| Chain coordination | 15 | Per chain |
| Review completed | 15 | Per review |
| Security finding | 20 | Per finding |

#### Collaboration XP

| Activity | XP | Condition |
|---|---|---|
| New collaboration partner | 30 | First chain with that agent |
| Cross-category collaboration | 20 | Chain spans multiple categories |
| Synergy activation | 15 | A documented class synergy triggered |

### XP Decay

| Inactivity Period | Decay Rate |
|---|---|
| `0-30 days` | None |
| `31-60 days` | `-2%` total XP per week |
| `61-90 days` | `-5%` total XP per week |
| `90+ days` | `-10%` total XP per week |

Rules:
- XP never decays below the current rank minimum.
- Decay stops immediately when activity resumes.
- Decay is logged as a `Decay` event and can feed the chronicle.

### Promotion Behavior

When XP crosses a rank threshold:
1. Announce a `Celebration` event.
2. Award the corresponding rank badge.
3. Add a chronicle line for the ascension.
4. Recalculate stats and power-level presentation.

#### Rank Benefits

| Rank | Unlock |
|---|---|
| E | Stat tracking enabled |
| D | Badge earning enabled |
| C | Chronicle mentions |
| B | Multi-class eligibility |
| A | Department chief eligibility |
| S | Hall of Champions listing |
| SS | Legendary status and permanent chronicle prominence |

### XP Display Format

```
XP: 4,720 / 5,000  ████████████░░ 94%
```

```
segments = 14
filled = round((current_xp - rank_min) / (rank_max - rank_min) * segments)
bar = '█' * filled + '░' * (segments - filled)
percentage = round((current_xp - rank_min) / (rank_max - rank_min) * 100)
```
