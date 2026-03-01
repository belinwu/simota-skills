# Rank & XP System

Progression system for agent characters with rank thresholds, XP earning rules, and level calculation.

---

## Rank Thresholds

| Rank | XP Required | Title | Badge Color | Description |
|---|---|---|---|---|
| F | 0 | Recruit | Gray | Newly registered, minimal activity |
| E | 100 | Novice | White | Beginning to contribute |
| D | 500 | Apprentice | Green | Regular contributor |
| C | 1,500 | Journeyman | Blue | Reliable, consistent performer |
| B | 4,000 | Veteran | Purple | Experienced, proven track record |
| A | 8,000 | Elite | Gold | Top-tier performer |
| S | 15,000 | Champion | Orange | Exceptional, ecosystem pillar |
| SS | 30,000 | Legend | Red | Legendary status, defining the ecosystem |

**Rank Display Format:**
```
Rank: A · Lv.47
XP: 8,720 / 15,000  ████████████░░░░ 58%
```

---

## Level Calculation

Levels provide finer granularity within ranks.

**Formula:**
```
level = floor(sqrt(total_xp / 2))
```

**Level → XP Table (sample):**

| Level | XP Required | Level | XP Required |
|---|---|---|---|
| 1 | 2 | 30 | 1,800 |
| 5 | 50 | 40 | 3,200 |
| 10 | 200 | 50 | 5,000 |
| 15 | 450 | 60 | 7,200 |
| 20 | 800 | 70 | 9,800 |
| 25 | 1,250 | 80+ | 12,800+ |

Maximum display level: 99 (at 19,602 XP). Agents above this show "Lv.99+" until rank SS.

---

## XP Earning Rules

### Task Completion XP

| Task Type | Base XP | Conditions |
|---|---|---|
| Single-agent task (Common quest) | 20 | Completed successfully |
| Multi-agent chain participant (Uncommon) | 40 | Chain completed successfully |
| Complex chain participant (Rare) | 80 | 4+ agents, completed |
| Parallel branch chain (Epic) | 150 | Parallel execution, completed |
| Titan product lifecycle (Legendary) | 300 | Full product delivered |

### Outcome Modifiers

| Outcome | Modifier | Condition |
|---|---|---|
| SUCCESS | ×1.0 | Standard completion |
| PARTIAL | ×0.5 | Some deliverables produced |
| BLOCKED | ×0.2 | Attempted but blocked |
| FAILED | ×0.0 | No usable output |
| First-time task type | ×1.5 | Agent's first time handling this type |
| Streak bonus (3+ consecutive SUCCESS) | ×1.2 | Sustained performance |

### Activity XP

| Activity | XP | Frequency Cap |
|---|---|---|
| Journal entry added | 10 | 5/day |
| Pattern discovered (Lore reference) | 25 | No cap |
| Chain coordination (Commander class) | 15 | Per chain |
| Review completed (Sage class) | 15 | Per review |
| Security finding (Paladin class) | 20 | Per finding |

### Collaboration XP

| Activity | XP | Conditions |
|---|---|---|
| New collaboration partner | 30 | First chain with a specific agent |
| Cross-category collaboration | 20 | Chain includes agents from different categories |
| Synergy activation | 15 | Class synergy bonus triggered |

---

## XP Decay (Inactivity)

To prevent stale agents from holding high ranks:

| Inactivity Period | Decay Rate |
|---|---|
| 0-30 days | None |
| 31-60 days | -2% total XP per week |
| 61-90 days | -5% total XP per week |
| 90+ days | -10% total XP per week |

**Rules:**
- XP never decays below the current rank's minimum threshold (prevents rank loss from inactivity alone)
- Decay stops immediately when activity resumes
- Decay is logged as an event in the chronicle

---

## Rank Promotion

When XP crosses a rank threshold:
1. **Announce:** Generate a rank-up event in the event system
2. **Badge:** Award the corresponding rank badge
3. **Narrative:** Chronicle entry: "[Agent] ascends to [Rank] rank!"
4. **Stat Recalculation:** Trigger stat recalculation (potential bonuses at higher ranks)

**Rank Benefits:**

| Rank | Unlocks |
|---|---|
| E | Stat tracking enabled |
| D | Badge earning enabled |
| C | Chronicle mentions |
| B | Multi-class eligibility |
| A | Department chief eligibility |
| S | Hall of Champions listing |
| SS | Legendary status, permanent chronicle chapter |

---

## XP Display Format

```
XP: 4,720 / 5,000  ████████████░░ 94%
     current / next_rank_threshold
```

**Progress bar:** 14 segments, filled proportional to progress within current rank.

```
segments = 14
filled = round((current_xp - rank_min) / (rank_max - rank_min) * segments)
bar = '█' × filled + '░' × (segments - filled)
percentage = round((current_xp - rank_min) / (rank_max - rank_min) * 100)
```
