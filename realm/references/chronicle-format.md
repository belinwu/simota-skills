# Chronicle Format

Rules for generating the Realm's long-term narrative chronicle.

---

## Chronicle Structure

The chronicle is a serialized narrative of the ecosystem's history, organized into chapters.

### Chapter Format

```markdown
## Chapter [N]: [Era Title]
**Period:** YYYY-MM ~ YYYY-MM
**EFS Range:** [start] → [end]
**Phase:** [Lifecycle phase]

[2-4 paragraph narrative summary of the era]

### Key Events
- [Event 1]
- [Event 2]
- [Event 3]

### Heroes of the Era
- [Agent]: [Notable achievement]

### Statistics
- Quests completed: [N]
- Agents active: [N]
- Badges earned: [N]
- XP distributed: [N]
```

---

## Era Detection

A new chapter/era begins when any of these triggers fire:

| Trigger | New Era Title Pattern |
|---|---|
| Lifecycle phase transition | "The Age of [Phase Name]" |
| EFS grade change (2+ grades) | "The [Rise/Fall] of [Grade]" |
| 10+ new agents added in 30 days | "The Great Expansion" |
| Agent sunset wave (3+ in 30 days) | "The Consolidation" |
| First Legendary quest completed | "The [Quest Name] Saga" |
| 90 days of stable EFS A+ | "The Golden Age" |
| EFS drops to D or below | "The Dark Times" |
| Manual user trigger | "The [User-specified] Era" |

---

## Narrative Style Guide

### Voice
- **Third person omniscient** narrator perspective
- **Past tense** for completed events, **present tense** for ongoing situations
- **Formal but warm** — like a company's official historian
- Weave data into narrative naturally (avoid raw number dumps)

### Tone Examples

**Good:**
> "The Frontline saw unprecedented activity as Builder, newly crowned Champion, led a series of ambitious construction projects. In the span of a single moon, 47 quests were completed — more than any previous month."

**Bad:**
> "Builder completed 47 quests this month. Their XP went from 12,000 to 18,500."

### Vocabulary Guide

| Technical Term | Chronicle Equivalent |
|---|---|
| Agent | Hero, champion, warrior, scholar (class-dependent) |
| Task/Chain | Quest, mission, expedition |
| Bug fix | Battle, defense, vanquishing |
| Feature | Construction, creation, forging |
| Refactoring | Purification, renewal, restoration |
| Deployment | Launch, expedition departure |
| EFS increase | Prosperity, growth, strengthening |
| EFS decrease | Decline, shadow, weakening |
| Agent inactive | Slumber, withdrawal, retreat |
| New agent | Arrival, emergence, awakening |
| Rank promotion | Ascension, crowning, advancement |
| Incident | Invasion, assault, crisis |
| Recovery | Healing, restoration, renaissance |

### Class-Specific Titles

| Class | Title |
|---|---|
| Commander | General, Marshal, Grand Commander |
| Ranger | Scout Master, Chief Tracker |
| Artisan | Master Craftsman, Grand Artisan |
| Guardian | Shield Captain, Warden |
| Paladin | Holy Knight, Grand Paladin |
| Sage | Elder, Chief Sage |
| Alchemist | Grand Alchemist, Transmuter |
| Scribe | Grand Chronicler, Lorekeeper |
| Architect | Grand Architect, Master Planner |
| Enchanter | Court Enchanter, Spell Weaver |
| Engineer | Chief Engineer, Grand Mechanic |
| Merchant | Guild Master, Trade Prince |
| Oracle | High Oracle, Chief Seer |
| Herald | Royal Herald, Grand Messenger |
| Demiurge | World Shaper, Grand Demiurge |
| Strategist | Grand Strategist, War Sage |

---

## Story Arcs

The chronicle tracks narrative arcs that span multiple chapters:

### Arc Types

| Arc Type | Duration | Narrative Pattern |
|---|---|---|
| Rise | 1-3 chapters | Agent/department grows from weakness to strength |
| Fall | 1-2 chapters | Decline from a high point |
| Redemption | 2-4 chapters | Fall followed by recovery |
| Rivalry | Ongoing | Two agents/departments competing for dominance |
| Journey | 3+ chapters | Agent progresses from Rank F to Rank S+ |
| Alliance | 1-2 chapters | Two departments form a strong collaboration |
| Crisis | 1-2 chapters | Ecosystem faces and overcomes a threat |

### Arc Detection Rules

1. **Rise Arc:** Agent XP increases >200% in 60 days
2. **Fall Arc:** Agent RS drops from Active to Dormant
3. **Redemption Arc:** Fall followed by Rise within 90 days
4. **Rivalry Arc:** Two agents consistently rank #1 and #2, alternating
5. **Journey Arc:** Agent crosses 3+ rank thresholds
6. **Alliance Arc:** Two departments' collaboration frequency doubles
7. **Crisis Arc:** EFS drops below 55, then recovers above 70

---

## Chronicle Commands

### `/Realm chronicle` Output

Display the last 3 chapters in full, with a table of contents for older chapters.

### Chronicle Length Limits

| Section | Max Length |
|---|---|
| Chapter narrative | 200 words |
| Key events list | 10 items |
| Heroes list | 5 agents |
| Arc summary | 50 words |

---

## Persistence

Chronicles are stored in `.agents/realm-state.md` under `## Chronicle`:

```markdown
## Chronicle

### Chapter XII: The Age of Expansion (2026-02 ~ present)
[Content...]

### Chapter XI: The Stabilization (2026-01 ~ 2026-01)
[Content...]
```

**Retention:** All chapters are retained permanently (the chronicle is the ecosystem's permanent history).
