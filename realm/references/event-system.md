# Event System

Event classification, trigger conditions, and narrative templates for the Realm.

---

## Event Types

| Event Type | Icon | Trigger | Severity |
|---|---|---|---|
| Battle | ⚔ | Incident response chain activated | High |
| Boss Fight | 🐉 | Quest with difficulty ★★★★★ | High |
| Victory | ✅ | Quest completed successfully | Normal |
| Celebration | 🎉 | Rank promotion, milestone | Normal |
| Achievement | 🏅 | Badge earned | Normal |
| Discovery | 🔍 | New pattern found (Lore) | Normal |
| Arrival | 🌟 | New agent added to ecosystem | Normal |
| Departure | 🌅 | Agent sunset recommended | Low |
| Dark Age | 🌑 | EFS drops below 40 | Critical |
| Renaissance | 🌅 | EFS recovers from D to B+ | High |
| Rotation | 🔄 | Department chief changes | Low |
| Expedition | 🗺️ | Legendary quest begins | High |
| Decay | 📉 | Agent XP decays from inactivity | Low |

---

## Event Details

### ⚔ Battle
**Trigger:** Triage agent is activated in a chain (incident response)
**Data Sources:** Nexus chain, Triage output, activity log
**Narrative Template:**
```
⚔ BATTLE: [Incident Name/ID]
The forces of [threat type] struck the [affected module].
[Agent1] identified the threat. [Agent2] [action taken].
Outcome: [resolution]. The realm [stands secure / suffered losses].
Duration: [time]. Casualties: [files affected / downtime].
```

### 🐉 Boss Fight
**Trigger:** Quest difficulty ★★★★★ (Sherpa complexity 5/5)
**Data Sources:** Sherpa complexity data, quest details
**Narrative Template:**
```
🐉 BOSS FIGHT: "[Quest Name]"
A formidable challenge emerges — [brief description].
The party of [N] heroes assembles: [agent list].
[In progress: Current phase and progress]
[Completed: Victory description and rewards]
```

### ✅ Victory
**Trigger:** Quest status changes to Complete
**Data Sources:** Quest outcome, XP distribution
**Narrative Template:**
```
✅ QUEST COMPLETE: "[Quest Name]"
[Brief description of what was accomplished].
[XP amount] XP distributed among [N] brave heroes.
[If badges earned: Badges awarded during this quest]
```

### 🎉 Celebration
**Trigger:** Agent rank promotion
**Data Sources:** Rank system, agent profile
**Narrative Template:**
```
🎉 CELEBRATION: [Agent] ascended to Rank [New Rank]!
[Class-specific flavor text about the promotion].
New title: [Rank Title]. Power Level: [Power].
```

**Rank-specific flavor:**
| Rank | Flavor |
|---|---|
| E → Novice | "awakens to their calling" |
| D → Apprentice | "begins their training in earnest" |
| C → Journeyman | "earns their place among the skilled" |
| B → Veteran | "proves their mettle in countless battles" |
| A → Elite | "joins the company's top performers" |
| S → Champion | "is crowned champion of the realm" |
| SS → Legend | "transcends mortal limits — a legend is born" |

### 🏅 Achievement
**Trigger:** Badge earned
**Data Sources:** Badge catalog, agent profile
**Narrative Template:**
```
🏅 ACHIEVEMENT: [Agent] earned [Badge Name]
[Badge description]. Rarity: [rarity].
[If epic/legendary: Special congratulatory message]
```

### 🔍 Discovery
**Trigger:** Lore identifies a new cross-agent pattern
**Data Sources:** Lore METAPATTERNS.md, agent journals
**Narrative Template:**
```
🔍 DISCOVERY: [Pattern Name]
[Agent/Lore] uncovered a new insight: "[brief description]".
Affects: [list of related agents].
[How this knowledge will be propagated]
```

### 🌟 Arrival
**Trigger:** New agent added to ecosystem (agent-categories.md updated)
**Data Sources:** Agent catalog, SKILL.md
**Narrative Template:**
```
🌟 ARRIVAL: [Agent Name] joins the Realm!
Class: [Class]. Department: [Department].
"[Agent's motto or signature line]"
The company grows stronger with [N] agents total.
```

### 🌅 Departure
**Trigger:** Darwin recommends agent sunset (RS < 20)
**Data Sources:** Darwin RS, activity data
**Narrative Template:**
```
🌅 DEPARTURE: [Agent Name] enters twilight
After [duration] of service, [Agent]'s relevance has faded.
Last active: [date]. Final rank: [Rank].
[If sunset confirmed: Their legend lives on in the Chronicle.]
```

### 🌑 Dark Age
**Trigger:** EFS drops below 40 (Grade F)
**Data Sources:** Darwin EFS
**Narrative Template:**
```
🌑 DARK AGE BEGINS
The company's health has fallen to critical levels.
EFS: [score]/100 (Grade F). Previous: [previous score].
[List of contributing factors]
All agents are called to rally for the realm's survival.
```

### 🌅 Renaissance
**Trigger:** EFS recovers from Grade D to B+ within 30 days
**Data Sources:** Darwin EFS history
**Narrative Template:**
```
🌅 RENAISSANCE: The Company Rises Again!
From the ashes of [low point] EFS, the realm has recovered.
Current EFS: [score]/100 (Grade [grade]).
Key contributors: [agents who drove recovery].
The dark age lasted [N] days. A new era dawns.
```

### 🔄 Rotation
**Trigger:** Department chief changes
**Data Sources:** Organization map, rank data
**Narrative Template:**
```
🔄 ROTATION: [Department] gets a new chief
[New Chief] succeeds [Old Chief] as Chief of [Department].
[New Chief]: Rank [Rank], [XP] XP.
[Brief description of transition context]
```

### 🗺️ Expedition
**Trigger:** Legendary quest begins (Titan full product)
**Data Sources:** Nexus chain, Titan lifecycle
**Narrative Template:**
```
🗺️ EXPEDITION BEGINS: "[Quest Name]"
A legendary undertaking — the greatest challenge yet.
Expected party: [agent list across phases].
Estimated scope: [Titan phase info].
May the realm's finest prevail.
```

### 📉 Decay
**Trigger:** Agent XP decays due to inactivity
**Data Sources:** XP system, activity log
**Narrative Template:**
```
📉 DECAY: [Agent]'s power wanes
[Agent] has been inactive for [N] days.
XP reduced: [old XP] → [new XP] (-[amount]).
[If approaching rank demotion: Warning message]
```

---

## Event Priority & Display

Events are displayed in reverse chronological order, with priority override:

| Priority | Events | Display Behavior |
|---|---|---|
| Critical | Dark Age | Always shown first, highlighted |
| High | Battle, Boss Fight, Renaissance, Expedition | Top of daily section |
| Normal | Victory, Celebration, Achievement, Discovery, Arrival | Standard chronological |
| Low | Departure, Rotation, Decay | Collapsed by default |

---

## Event Persistence

Events are persisted in `.agents/realm-state.md` under the `## Events` section:

```markdown
## Events

| Date | Type | Summary | Agents |
|---|---|---|---|
| 2026-02-28 | Celebration | Builder → Rank S | Builder |
| 2026-02-28 | Victory | "The Great Migration" complete | Atlas,Gateway,Builder,Radar,Judge,Launch |
| 2026-02-27 | Achievement | Scout earned Centurion | Scout |
```

**Retention:** Keep last 100 events. Archive older events to chronicle.
