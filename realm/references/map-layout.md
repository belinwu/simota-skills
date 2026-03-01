# Map Layout

Spatial layout definition for the HTML Company HQ Map (`templates/realm-map.html`).

---

## Visual Concept

The map renders the Realm as a **modern company headquarters floor plan**. Each department is an office room/area arranged on a 4×6 CSS Grid. RPG mechanics (stats, XP, ranks, classes) overlay on the corporate structure.

| Element | Fantasy → Corporate |
|---|---|
| Castle | Executive Suite |
| Tower | Lab / Office |
| Temple | Training Center |
| Forge | Development Floor |
| Fortress | Security Center |
| Sanctum | CTO Office |

---

## Grid Layout (4 rows × 6 columns)

```
     Col1            Col2           Col3          Col4           Col5           Col6
R1   ⚔ Command      (empty)        🏛 Council    (empty)        📯 Herald      📊 Observatory
     Exec Suite                     Strategy                     Comms          Analytics Lab

R2   (empty)         🔨 Frontline   (empty)       📚 Academy    (empty)        🛡 Defense
                     Dev Floor                     Training                     Security

R3   ⚙ Workshop     (empty)        ✨ Enchant    (empty)        🌍 Outlands   (empty)
     Infra Lab                      Design Studio                Innovation Hub

R4   🌟 Pantheon    (empty)        🔍 Intel      (empty)        (empty)       (empty)
     CTO Office                     Research Lab
```

---

## Department Grid Coordinates

| Department | Key | Grid Position | Office Type | Floor Tag |
|---|---|---|---|---|
| Command Center | `command` | R1C1 | Executive Suite | Exec |
| Council | `council` | R1C3 | Strategy Office | Strategy |
| Herald's Tower | `herald` | R1C5 | Communications | Comms |
| Observatory | `observatory` | R1C6 | Analytics Lab | Analytics |
| Frontline | `frontline` | R2C2 | Development Floor | Dev |
| Academy | `academy` | R2C4 | Training Center | Training |
| Defense | `defense` | R2C6 | Security Center | Security |
| Workshop | `workshop` | R3C1 | Infrastructure Lab | Infra |
| Enchantment Hall | `enchant` | R3C3 | Design Studio | Design |
| Outlands | `outlands` | R3C5 | Innovation Hub | R&D |
| Pantheon | `pantheon` | R4C1 | CTO Office | Meta |
| Intelligence Corps | `intel` | R4C3 | Research Lab | Research |

---

## Road Connections (Inter-Department Lines)

SVG lines drawn between department centers representing collaboration relationships.

| From | To | Relation | Line Style |
|---|---|---|---|
| Command | Frontline | Allied | Solid, blue, 2px |
| Command | Intel | Allied | Solid, blue, 2px |
| Intel | Defense | Allied | Solid, blue, 2px |
| Academy | Frontline | Cooperative | Dashed, gray, 1.5px |
| Council | Command | Advisory | Dashed, gray, 1.5px |
| Enchant | Frontline | Cooperative | Dashed, gray, 1.5px |
| Workshop | Frontline | Support | Dashed, gray, 1.5px |
| Pantheon | Command | Oversight | Dashed, gray, 1.5px |
| Workshop | Defense | Support | Dashed, gray, 1.5px |
| Observatory | Intel | Cooperative | Dashed, gray, 1.5px |
| Herald | Command | Cooperative | Dashed, gray, 1.5px |
| Outlands | Intel | Cooperative | Dashed, gray, 1.5px |

---

## Template Variables

### Status Bar Variables

| Variable | Description | Example |
|---|---|---|
| `{{COMPANY_ICON}}` | Company emoji icon | `🏰` |
| `{{EFS_SCORE}}` | Ecosystem Fitness Score | `87` |
| `{{EFS_GRADE}}` | EFS letter grade | `A` |
| `{{EFS_PERCENT}}` | EFS as percentage for bar fill | `87` |
| `{{EFS_LEVEL}}` | Bar fill class: `high`/`mid`/`low` | `high` |
| `{{PHASE}}` | Lifecycle phase | `ACTIVE_BUILD` |
| `{{AGENT_TOTAL}}` | Total agent count | `63` |
| `{{QUEST_ACTIVE}}` | Active quest count | `5` |
| `{{LAST_UPDATED}}` | Timestamp | `2026-03-01 12:00` |

### Per-Department Variables

For each department `{DEPT}` (COMMAND, FRONTLINE, INTEL, DEFENSE, ACADEMY, COUNCIL, ENCHANT, WORKSHOP, OBSERVATORY, HERALD, PANTHEON, OUTLANDS):

| Variable | Description | Example |
|---|---|---|
| `{{DEPT_{DEPT}_ICON}}` | Department emoji | `⚔` |
| `{{DEPT_{DEPT}_CHIEF}}` | Chief agent name | `Nexus` |
| `{{DEPT_{DEPT}_CHIEF_RANK}}` | Chief rank display | `SS` |
| `{{DEPT_{DEPT}_CHIEF_RANK_LC}}` | Chief rank lowercase (CSS class) | `ss` |
| `{{DEPT_{DEPT}_HEALTH}}` | Health score (0-100) | `92` |
| `{{DEPT_{DEPT}_HEALTH_STATUS}}` | CSS class: `thriving`/`stable`/`strained`/`critical` | `thriving` |
| `{{DEPT_{DEPT}_HEALTH_LABEL}}` | Status label | `Thriving` |
| `{{DEPT_{DEPT}_HEALTH_ICON}}` | Status emoji | `💚` |
| `{{DEPT_{DEPT}_AGENTS}}` | HTML agent dots markup | `<span class="agent-dot" ...>` |

### Event Ticker Variable

| Variable | Description |
|---|---|
| `{{EVENT_TICKER_ITEMS}}` | HTML markup for ticker items |

Event ticker item format:
```html
<div class="event-ticker__item">
  <span class="event-ticker__item-icon">🎉</span>
  <span class="event-ticker__item-text">Builder ascended to Rank S!</span>
  <span class="event-ticker__item-date">2026-02-28</span>
</div>
```

### Agent Dot Markup

Per-agent dot inside `{{DEPT_*_AGENTS}}`:

```html
<span class="agent-dot agent-dot--{rank_lc} agent-dot--chief"
      style="background: var(--class-{class_lc});"
      title="{name} [{rank}] {class}"
      onmouseenter="showAgentTooltip(event, {json})"
      onmouseleave="hideTooltip()">
</span>
```

- `agent-dot--chief` class only for department chiefs
- `agent-dot--{rank_lc}`: rank-based size (ss/s/a/b/c/d/e/f)
- `--class-{class_lc}`: class-based color variable

### REALM_DATA_JSON

The `{{REALM_DATA_JSON}}` variable contains the full data object for JS interactivity:

```json
{
  "company": {
    "name": "The Realm",
    "efs": 87,
    "efsGrade": "A",
    "phase": "ACTIVE_BUILD",
    "totalAgents": 63,
    "activeQuests": 5,
    "lastUpdated": "2026-03-01 12:00"
  },
  "departments": {
    "command": {
      "name": "Command Center",
      "icon": "⚔",
      "type": "Executive Suite",
      "chief": "Nexus",
      "chiefRank": "SS",
      "health": 92,
      "healthStatus": "thriving",
      "healthLabel": "Thriving",
      "healthIcon": "💚",
      "ability": { "name": "Grand Strategy", "description": "Can initiate multi-department operations" },
      "members": [
        {
          "name": "Nexus",
          "class": "Commander",
          "rank": "SS",
          "xp": 31200,
          "isChief": true,
          "classColor": "var(--class-commander)",
          "stats": { "str": 98, "dex": 82, "int": 91, "wis": 74, "cha": 99, "con": 95 }
        }
      ]
    }
  },
  "roads": [
    { "from": "command", "to": "frontline", "type": "allied" }
  ],
  "events": [
    { "icon": "🎉", "text": "Builder ascended to Rank S!", "date": "2026-02-28" }
  ],
  "quests": [
    { "name": "The Great API Overhaul", "rarity": "epic", "progress": 60, "party": ["Atlas", "Gateway", "Builder"] }
  ],
  "conversations": [
    { "agent": "Nexus", "message": "Chain #42 complete", "dept": "command" },
    { "agent": "Builder", "message": "Deploying v2.1", "dept": "frontline" },
    { "agent": "Scout", "message": "Found root cause", "dept": "intel" }
  ]
}
```

---

## Interaction Behavior

| Action | Result |
|---|---|
| Hover on department card | Tooltip with chief name, health, member count |
| Click on department card | Opens right detail panel with team stats, members, quests |
| Click same card again | Closes detail panel |
| Hover on agent dot | Tooltip with name, class, rank, XP; pauses wander animation |
| Click agent in panel | Shows agent details in panel |
| Hover on ticker | Pauses auto-scroll |

### Ambient Animations (Automatic)

| Animation | Behavior | Timing |
|---|---|---|
| Agent Wandering | Agent dots subtly drift within department cards (3 motion patterns) | 4–10s per cycle, random delay |
| Working Glow | ~20% of agents pulse with blue glow indicating active work | 2s pulse cycle |
| Speech Bubbles | Pop-up speech bubbles over random agents showing conversations | Every 2–6.5s, max 3 simultaneous |
| Traveling Dots | Colored dots travel along road lines between departments | Every 3–8s, ease-in-out motion |
| Building Breathing | Thriving departments have a subtle shadow pulse | 4s breath cycle |

### Conversations Data

The `conversations` array in REALM_DATA provides custom speech bubble content. When available, these are mixed with built-in office chatter phrases. Format:

```json
{ "agent": "Nexus", "message": "Chain #42 complete", "dept": "command" }
```

If `conversations` is empty or absent, the speech bubble system falls back to 24 built-in office chatter phrases and event data.

---

## CSS Class Color Mapping

Agent dots use CSS custom properties mapped from the class system:

| Class | CSS Variable | Color |
|---|---|---|
| Commander | `--class-commander` | #ef4444 |
| Ranger | `--class-ranger` | #22c55e |
| Artisan | `--class-artisan` | #f97316 |
| Guardian | `--class-guardian` | #06b6d4 |
| Paladin | `--class-paladin` | #eab308 |
| Sage | `--class-sage` | #a855f7 |
| Alchemist | `--class-alchemist` | #14b8a6 |
| Scribe | `--class-scribe` | #8b5cf6 |
| Architect | `--class-architect` | #6366f1 |
| Enchanter | `--class-enchanter` | #ec4899 |
| Engineer | `--class-engineer` | #84cc16 |
| Merchant | `--class-merchant` | #f59e0b |
| Oracle | `--class-oracle` | #06b6d4 |
| Herald | `--class-herald` | #f97316 |
| Demiurge | `--class-demiurge` | #c026d3 |
| Strategist | `--class-strategist` | #4f46e5 |
| Diplomat | `--class-diplomat` | #10b981 |
| Pioneer | `--class-pioneer` | #f43f5e |
| Navigator | `--class-navigator` | #34d399 |
| Transmuter | `--class-transmuter` | #facc15 |
| Watcher | `--class-watcher` | #6b7280 |
