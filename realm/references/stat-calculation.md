# Stat Calculation

Algorithms for computing the 6 RPG stats for each agent character.

---

## Overview

Each agent has 6 stats scored 0–100. Stats are derived from observable ecosystem data — never fabricated.

```
╔══════════════════════════════════════════╗
║  STR [████████░░] 82  (Code Output)     ║
║  DEX [██████░░░░] 63  (Versatility)     ║
║  INT [███████░░░] 74  (Complexity)      ║
║  WIS [█████░░░░░] 55  (Learning Rate)   ║
║  CHA [██████░░░░] 68  (Collaboration)   ║
║  CON [█████████░] 91  (Reliability)     ║
╚══════════════════════════════════════════╝
```

---

## Stat Definitions & Formulas

### STR — Strength (Code Output Power)

**Meaning:** Volume and impact of the agent's direct output.

**Data Sources:**
- `PROJECT.md` activity log entries (action count)
- Commit contributions attributed to agent's work
- Artifact generation volume (files created/modified)

**Formula:**
```
activity_count = count of PROJECT.md entries for agent (last 90 days)
normalized = min(activity_count / median_activity_all_agents, 2.0)
STR = round(normalized * 50)  # 0-100 scale
```

**Adjustments:**
- Agents in non-code categories (Investigation, Strategy) use "report/analysis count" instead of commit count
- Newly created agents (<30 days) receive a 1.2x boost to avoid cold-start penalty

### DEX — Dexterity (Versatility)

**Meaning:** Diversity of task types the agent handles.

**Data Sources:**
- Distinct task type tags in activity log
- Different chain patterns participated in
- Cross-category collaboration count

**Formula:**
```
task_types = count of distinct task types handled (last 90 days)
max_types = max distinct types across all agents
DEX = round((task_types / max_types) * 100)
```

**Adjustments:**
- Specialist agents (Security, Testing) are normalized against their category peers, not globally
- Minimum DEX = 10 for any active agent (avoids zero for single-purpose agents)

### INT — Intelligence (Complexity Handling)

**Meaning:** Ability to handle complex, multi-faceted tasks.

**Data Sources:**
- Average Sherpa complexity rating of handled tasks
- Chain position (later positions in chain = more context to process)
- Nexus CES (Chain Efficiency Score) contribution

**Formula:**
```
avg_complexity = average complexity of tasks (1-5 scale, from Sherpa data)
chain_depth_bonus = average chain position * 5  # 0-25 bonus
INT = round(min((avg_complexity / 5) * 75 + chain_depth_bonus, 100))
```

**Adjustments:**
- If Sherpa data unavailable, estimate from chain length (longer chains = higher complexity assumed)
- Meta agents (Darwin, Realm, Sigil) receive inherent +15 INT bonus (ecosystem-level complexity)

### WIS — Wisdom (Learning Rate)

**Meaning:** How quickly the agent accumulates and applies knowledge.

**Data Sources:**
- Journal entry count growth (`.agents/{name}.md`)
- Pattern recognition rate (entries that reference previous entries)
- Lore METAPATTERNS.md mentions

**Formula:**
```
journal_entries_recent = entries added in last 30 days
journal_entries_prev = entries added in previous 30 days
growth_rate = journal_entries_recent / max(journal_entries_prev, 1)
base_wis = min(growth_rate * 30, 60)
lore_bonus = 5 * count of METAPATTERNS references  # up to 40
WIS = round(min(base_wis + lore_bonus, 100))
```

**Adjustments:**
- New agents (<60 days) with >5 journal entries get a learning acceleration bonus (+20)
- Stale journals (no entries >60 days) cap WIS at 30

### CHA — Charisma (Collaboration)

**Meaning:** How well the agent works with others in chains.

**Data Sources:**
- Chain co-occurrence frequency with other agents
- Unique collaboration partner count
- Nexus chain completion rate when participating

**Formula:**
```
collab_count = number of chain participations (last 90 days)
unique_partners = distinct agents collaborated with
partner_ratio = unique_partners / total_agents_in_ecosystem
CHA = round(min((collab_count * 2 + partner_ratio * 60), 100))
```

**Adjustments:**
- Orchestration agents (Commander class) receive a natural +15 CHA bonus
- Solo-specialist agents have a floor of CHA = 20 (they still exist in the ecosystem)

### CON — Constitution (Reliability)

**Meaning:** Consistency and dependability of the agent.

**Data Sources:**
- Task success rate (SUCCESS vs PARTIAL/BLOCKED/FAILED in AUTORUN markers)
- Error recovery instances
- Darwin RS (Relevance Score) component

**Formula:**
```
success_rate = SUCCESS_count / total_task_count  # 0.0-1.0
recovery_bonus = recovery_count * 5  # up to 20
rs_factor = Darwin_RS / 100 * 20  # 0-20 from RS
CON = round(min(success_rate * 60 + recovery_bonus + rs_factor, 100))
```

**Adjustments:**
- Agents with <5 total tasks use ecosystem average CON as baseline
- Perfect success rate (100%) over 20+ tasks earns CON bonus of +10

---

## Stat Bar Rendering

Stats are rendered as 10-segment bars:

```
segments = round(stat_value / 10)
filled = '█' × segments
empty = '░' × (10 - segments)
bar = '[' + filled + empty + ']'
```

**Example:** STR 82 → `[████████░░]`

---

## Stat Aggregation

### Power Level
Overall agent power = weighted average of all stats:
```
Power = (STR×20 + DEX×15 + INT×20 + WIS×15 + CHA×15 + CON×15) / 100
```

### Stat Profile Types

| Profile | Condition | Label |
|---|---|---|
| Balanced | All stats within 20 points of mean | "Well-Rounded" |
| Physical | STR + CON > 160 | "Powerhouse" |
| Mental | INT + WIS > 160 | "Intellectual" |
| Social | CHA + DEX > 160 | "Versatile" |
| Tank | CON > 85 | "Ironclad" |
| Glass Cannon | STR > 85, CON < 40 | "Glass Cannon" |

---

## Update Frequency

- Stats are recalculated on each `/Realm` or `/Realm agent` invocation
- Historical stats are stored in `.agents/realm-state.md` for trend tracking
- Stat deltas (vs last calculation) are shown as `↑`/`↓`/`→` indicators

---

## Cold Start Handling

For agents with insufficient data:
1. **No activity data:** All stats set to `??` (unknown), displayed as `[??????????]`
2. **Partial data (<5 tasks):** Calculate available stats, mark others as `??`
3. **New agent (<14 days):** Apply "Recruit" label, stats shown with `*` suffix to indicate provisional
