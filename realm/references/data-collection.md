# Data Collection

Data source specifications, collection flow, and state management schema for Realm.

---

## Data Sources

### Primary Sources

| Source | Path | Content | Used For |
|---|---|---|---|
| Activity Log | `.agents/PROJECT.md` | Agent task completions | STR, quest history, XP |
| Ecosystem State | `.agents/ECOSYSTEM.md` | EFS, RS, lifecycle phase | Stats, ranking, events |
| Agent Journals | `.agents/{name}.md` | Individual insights | WIS, learning rate |
| Git History | `git log` | Commit data | Activity trends, phases |
| Agent Catalog | `architect/references/agent-categories.md` | Agent list, categories | Class assignment, roster |

### Secondary Sources

| Source | Path | Content | Used For |
|---|---|---|---|
| Nexus Chains | AUTORUN markers in logs | Chain composition, outcomes | Quests, CHA, party data |
| Sherpa Tasks | Task decomposition data | Complexity ratings | INT, quest difficulty |
| Lore Patterns | `.agents/METAPATTERNS.md` | Cross-agent patterns | WIS, discovery events |
| Darwin Scores | `.agents/ECOSYSTEM.md` | EFS, RS per agent | CON, department health |
| Retain Templates | `retain/references/gamification.md` | Gamification patterns | Badge design reference |

---

## Collection Flow

```
SURVEY Phase Collection Order:
1. Read .agents/PROJECT.md → Extract activity counts per agent
2. Read .agents/ECOSYSTEM.md → Extract EFS, RS, lifecycle phase
3. Scan .agents/*.md → Count journal entries per agent
4. Run git log --oneline -100 → Extract recent commit patterns
5. Read agent-categories.md → Get current agent roster and categories
6. (Optional) Parse AUTORUN markers → Extract chain data
```

### Data Freshness

| Source | Refresh Frequency | Staleness Threshold |
|---|---|---|
| PROJECT.md | Every invocation | >7 days = stale warning |
| ECOSYSTEM.md | Every invocation | >14 days = stale warning |
| Agent journals | Every invocation | No staleness (historical) |
| Git history | Every invocation | Always fresh |
| Agent catalog | On `/Realm` or `/Realm map` | >30 days = roster drift warning |

---

## State Management Schema

All Realm state is persisted in `.agents/realm-state.md`.

### Schema Structure

```markdown
# Realm State
Last updated: YYYY-MM-DD HH:MM

## Agents

| Agent | Class | Rank | XP | Lv | STR | DEX | INT | WIS | CHA | CON | Badges |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Nexus | Commander | SS | 31200 | 99 | 98 | 82 | 91 | 74 | 99 | 95 | 18 |
| Builder | Artisan | S | 18500 | 96 | 98 | 63 | 74 | 55 | 68 | 95 | 15 |
| ...

## Active Quests

| ID | Name | Rarity | Party | Progress | Started |
|---|---|---|---|---|---|
| Q-127 | The API Redesign | Rare | Atlas,Gateway,Builder,Radar | 60% | 2026-02-28 |
| ...

## Completed Quests (last 50)

| ID | Name | Rarity | Party | XP | Completed |
|---|---|---|---|---|---|
| Q-126 | The Great Migration | Epic | Atlas,Gateway,Builder,Radar,Judge,Launch | 525 | 2026-02-28 |
| ...

## Badges Earned

| Agent | Badge ID | Badge Name | Earned Date |
|---|---|---|---|
| Nexus | quest_500 | Legendary Hero | 2026-01-15 |
| ...

## Events (last 100)

| Date | Type | Summary | Agents |
|---|---|---|---|
| 2026-02-28 | Celebration | Builder → Rank S | Builder |
| ...

## Department Health

| Department | Chief | Health | Status |
|---|---|---|---|
| Command Center | Nexus | 92 | 💚 Thriving |
| ...

## Ecosystem Badges

| Badge ID | Badge Name | Earned Date |
|---|---|---|
| eco_empire | Mighty Empire | 2026-02-15 |
| ...

## Chronicle

### Chapter XII: The Age of Expansion (2026-02 ~ present)
[Narrative content...]

### Chapter XI: The Stabilization (2026-01 ~ 2026-01)
[Narrative content...]
```

---

## State Initialization (Cold Start)

When `.agents/realm-state.md` does not exist:

1. **Create file** with header and empty tables
2. **Scan agent catalog** → Initialize all agents with:
   - Class from category mapping
   - Rank = F (0 XP)
   - All stats = `??` (unknown)
   - No badges
3. **Read PROJECT.md** → Backfill XP from historical activity (if available)
4. **Read ECOSYSTEM.md** → Import RS scores for CON calculation
5. **Generate first chronicle chapter**: "Chapter I: The Beginning"
6. **Persist** initial state

---

## Data Integrity Rules

1. **Never fabricate data** — if a source is unavailable, mark as `??` or `N/A`
2. **Preserve historical data** — never delete completed quests or earned badges
3. **Timestamp everything** — all state changes include the update timestamp
4. **Idempotent updates** — running SURVEY twice should produce identical results
5. **Graceful degradation** — if ECOSYSTEM.md is stale, use cached values with warning
6. **Source attribution** — each calculated value traces back to its data source

---

## Performance Considerations

- **File reads are the bottleneck** — minimize redundant reads by caching within a session
- **Git log limit** — cap at 100 entries per invocation to avoid long processing
- **Journal scanning** — only count entries, don't parse full content
- **State file size** — prune completed quests beyond 50, events beyond 100
- **Mermaid delegation** — offload complex graph rendering to Canvas to keep Realm focused
