# Quest Mapping

Rules for transforming Nexus chain executions and tasks into RPG quests.

---

## Quest Rarity Classification

| Chain Complexity | Rarity | Color | Quest Theme | XP Multiplier |
|---|---|---|---|---|
| Single agent | Common | White (⚪) | Daily quest | ×1.0 |
| 2-3 agents | Uncommon | Green (🟢) | Investigation quest | ×2.0 |
| 4+ agents | Rare | Blue (🔵) | Adventure quest | ×4.0 |
| Parallel branches | Epic | Purple (🟣) | Expedition quest | ×7.5 |
| Titan full product | Legendary | Orange (🟠) | Grand expedition | ×15.0 |

---

## Quest Structure

Each quest has:

```
╔═══════════════════════════════════════════════╗
║  🟢 UNCOMMON QUEST: "The Authentication Fix"  ║
╠═══════════════════════════════════════════════╣
║  Objective: Investigate and fix auth bug       ║
║  Party: Scout → Builder → Radar               ║
║  Difficulty: ★★★☆☆                            ║
║  Status: ✅ COMPLETE                           ║
║  Reward: 120 XP (40 base × 3 party members)   ║
║  Duration: ~45 min                             ║
║  Badges earned: [Bug Slayer]                   ║
╚═══════════════════════════════════════════════╝
```

### Quest Fields

| Field | Source | Description |
|---|---|---|
| Name | Auto-generated from task description | Human-readable quest title |
| Rarity | Chain agent count + branching | Quest rarity classification |
| Objective | Original user request / Nexus task | What needs to be accomplished |
| Party | Nexus chain agents | Quest participants (ordered) |
| Difficulty | Sherpa complexity rating (1-5) | ★ per complexity point |
| Status | AUTORUN markers | Active / Complete / Failed / Abandoned |
| Reward | Base XP × modifiers | Total XP distributed to party |
| Duration | Timestamps from activity log | Estimated quest duration |
| Badges | Badge catalog match | Any badges earned during quest |

---

## Quest Name Generation

Auto-generate quest names from task context:

| Task Pattern | Quest Name Template |
|---|---|
| Bug investigation | "The [Component] Mystery" |
| Bug fix | "Vanquishing the [Component] Bug" |
| New feature | "Forging the [Feature]" |
| Refactoring | "Purifying the [Module]" |
| Security audit | "The Sentinel's Vigil: [Target]" |
| Performance optimization | "Accelerating the [Component]" |
| Documentation | "Chronicling the [Subject]" |
| Architecture design | "Blueprint of [System]" |
| Testing | "Fortifying [Component] Defenses" |
| Deployment | "The Great [Version] Launch" |
| Migration | "The [Technology] Exodus" |
| Review | "The Council Reviews [Subject]" |

---

## Party Composition

### Party Roles

| Chain Position | Party Role | Description |
|---|---|---|
| First agent | Leader | Initiates the quest |
| Middle agents | Support | Provides specialized skills |
| Final agent | Finisher | Delivers the final artifact |
| Parallel agents | Flankers | Execute simultaneously |

### Party Size Bonuses

| Party Size | Bonus | Narrative |
|---|---|---|
| 1 (Solo) | None | Lone wolf mission |
| 2-3 | +10% XP | Small party synergy |
| 4-5 | +20% XP | Full party advantage |
| 6+ | +30% XP | Raid bonus |

### Class Composition Bonuses

When the party includes specific class combinations:

| Composition | Bonus | Condition |
|---|---|---|
| Balanced Party | +15% XP | 3+ different classes in party |
| Specialist Team | +10% XP | All same class |
| Full Stack | +25% XP | Commander + Artisan + Guardian + Sage |

---

## Quest Outcomes

### Status Mapping

| AUTORUN Status | Quest Status | Display |
|---|---|---|
| All SUCCESS | ✅ Complete | Green |
| Mix of SUCCESS/PARTIAL | ⚠️ Partial | Yellow |
| Any BLOCKED | 🔒 Blocked | Gray |
| Any FAILED | ❌ Failed | Red |
| Abandoned (no completion) | 💀 Abandoned | Dark gray |

### Outcome XP Distribution

| Quest Status | XP Awarded | Distribution |
|---|---|---|
| Complete | 100% of reward | Equal split among all party members |
| Partial | 50% of reward | Only to agents with SUCCESS status |
| Blocked | 20% of reward | Participation credit only |
| Failed | 0% of reward | No XP (but recorded in history) |
| Abandoned | 0% of reward | Negative event in chronicle |

---

## Quest Board Layout

### Active Quests

```
╔═══════════════════════ QUEST BOARD ═══════════════════════╗
║                                                           ║
║  ACTIVE QUESTS (3)                                        ║
║  ─────────────────────────────────────────────────────     ║
║  🔵 [Rare] "The API Redesign"                             ║
║     Party: Atlas → Gateway → Builder → Radar              ║
║     Progress: ██████░░░░ 60% · In: Builder phase          ║
║                                                           ║
║  🟢 [Uncommon] "Vanquishing the Login Bug"                ║
║     Party: Scout → Builder                                ║
║     Progress: ████████░░ 80% · In: Builder phase          ║
║                                                           ║
║  ⚪ [Common] "Chronicling the Auth Module"                 ║
║     Party: Quill                                          ║
║     Progress: ██████████ 100% · Wrapping up               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

### Completed Quests (Recent)

```
║  COMPLETED (last 7 days: 12)                              ║
║  ─────────────────────────────────────────────────────     ║
║  ✅ 🟣 "The Great Migration" — 2026-02-28                  ║
║     Party: Horizon → Builder → Radar · Reward: 525 XP     ║
║  ✅ 🟢 "Purifying the Utils" — 2026-02-27                  ║
║     Party: Zen → Judge · Reward: 88 XP                    ║
║  ...                                                       ║
```

---

## Quest History & Statistics

Track lifetime quest statistics per agent:

```
Quest Stats:
  Total: 47 quests
  ✅ Complete: 42 (89%)
  ⚠️ Partial: 3 (6%)
  ❌ Failed: 1 (2%)
  💀 Abandoned: 1 (2%)

  By Rarity:
  ⚪ Common: 20 · 🟢 Uncommon: 15 · 🔵 Rare: 8 · 🟣 Epic: 3 · 🟠 Legendary: 1
```
