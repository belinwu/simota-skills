# Narrative Design

Story structures, branching patterns, quest design, world-building, and dialogue systems for game narrative.

---

## Story Structures

### Three-Act Structure

| Act | Purpose | Game Application |
|-----|---------|-----------------|
| Act 1 (Setup) | Introduce world, character, conflict | Tutorial + first area, establish core loop |
| Act 2 (Confrontation) | Rising stakes, complications, reversals | Mid-game, unlock new mechanics, deepen story |
| Act 3 (Resolution) | Climax, resolution, new equilibrium | Final boss/area, payoff of player choices |

**Pacing rule**: Act 1 ≈ 25%, Act 2 ≈ 50%, Act 3 ≈ 25% of total play time.

### Hero's Journey (Campbell/Vogler)

12 stages adapted for games:

1. **Ordinary World** → Hub/home area
2. **Call to Adventure** → Inciting incident / quest giver
3. **Refusal of the Call** → Tutorial friction / reluctant hero setup
4. **Meeting the Mentor** → First NPC companion or guide
5. **Crossing the Threshold** → Leave starting area, point of no return
6. **Tests, Allies, Enemies** → Mid-game quests, party building, enemy factions
7. **Approach to the Inmost Cave** → Pre-dungeon/pre-boss area
8. **Ordeal** → Major boss fight or pivotal decision
9. **Reward** → New ability, story revelation, loot
10. **The Road Back** → Consequences of Ordeal, new complications
11. **Resurrection** → Final boss / ultimate test
12. **Return with the Elixir** → Ending, new game+, epilogue

### Kishōtenketsu (Four-Act, No Conflict)

| Phase | Purpose | Notes |
|-------|---------|-------|
| Ki (Introduction) | Establish setting | Can substitute for traditional conflict-driven narrative |
| Shō (Development) | Deepen without conflict | Exploration, relationship building |
| Ten (Twist) | Unexpected element | Recontextualize what player knows |
| Ketsu (Conclusion) | Reconcile twist with setup | Resolution through understanding, not combat |

Ideal for: puzzle games, exploration games, narrative experiences, Japanese-inspired design.

### Dan Harmon's Story Circle

Simplified Hero's Journey in 8 beats: You → Need → Go → Search → Find → Take → Return → Change. Good for episodic content (quest chains, seasonal content).

---

## Branching Types

| Type | Complexity | Player Agency | Example |
|------|-----------|---------------|---------|
| **Linear** | Low | None | Call of Duty campaigns |
| **Gated Linear** | Low | Minimal (unlock order) | Metroidvania progression |
| **Branching** | Medium | High (exclusive paths) | The Witcher 2 Act 2 |
| **Parallel** | Medium | Moderate (order choice) | Mega Man stage select |
| **Hub-and-Spoke** | Medium | High (non-linear) | Mass Effect missions |
| **Emergent** | High | Maximum | Dwarf Fortress, Rimworld |

### Branching Complexity Guidelines

| Branches | Management Complexity | Recommendation |
|----------|----------------------|----------------|
| 1–5 nodes | Low | Solo developer feasible |
| 6–10 nodes | Medium | Requires tracking spreadsheet |
| 11–20 nodes | High | Needs dedicated narrative designer |
| 20+ nodes | Very high | Tool-assisted (Twine, Articy) required |

**Quest's ask-first threshold**: Branching narratives > 10 decision nodes.

---

## Quest Design Patterns

### Core Quest Types

| Type | Player Motivation | Design Notes |
|------|-------------------|--------------|
| **Fetch** | Completion, exploration | Disguise with narrative context; avoid "collect 10 bear asses" |
| **Escort** | Protection, empathy | AI pathfinding must be solid; escort must not feel like a burden |
| **Defense** | Territory, mastery | Wave-based; clear escalation; prep time between waves |
| **Puzzle** | Intellect, discovery | Difficulty curve; no pixel hunting; multiple solution paths preferred |
| **Boss** | Challenge, climax | Telegraph attacks; phase transitions; reward mastery |
| **Stealth** | Tension, agency | Multiple routes; clear detection rules; forgiving reset points |
| **Investigation** | Curiosity, narrative | Environmental clues; journal/log system; allow non-linear discovery |
| **Delivery/Timed** | Urgency, skill | Fair time limits; visible countdown; route optimization reward |

### Quest Chain Structure

```
Hook → Context → Travel → Challenge → Twist → Resolution → Reward → Setup Next
```

- **Hook**: First line should create curiosity ("My daughter hasn't come home in three days...")
- **Twist**: Subvert expectation at ~60% completion (the daughter left voluntarily)
- **Setup Next**: Every quest should seed the next quest or a future plot thread

### Side Quest Quality Checklist

- [ ] Connects to main theme or world-building
- [ ] Has its own mini-arc (not just task completion)
- [ ] Reveals something about the world, faction, or character
- [ ] Reward is proportional to effort + meaningful to progression
- [ ] Completable without blocking main story

---

## World-Building

### Iceberg Model

| Layer | Visible to Player | Example |
|-------|-------------------|---------|
| **Surface** (10%) | Directly experienced | Dialogue, environments, quests |
| **Implied** (30%) | Referenced or hinted | Lore books, NPC mentions, ruins |
| **Foundation** (60%) | Designer's internal docs | Full history, faction motivations, economic systems |

**Rule**: Build 3× what the player sees. The depth shows through consistency.

### Lore Hierarchy

1. **Cosmic lore**: Creation myths, magic systems, fundamental rules
2. **Historical lore**: Major events, wars, discoveries
3. **Faction lore**: Organizations, cultures, conflicts
4. **Personal lore**: Individual character backstories
5. **Environmental lore**: What the world looks like and why

### Environmental Storytelling Techniques

- **Architecture**: Building styles reveal culture and history
- **Wear and damage**: Scorch marks, cracks, repairs tell stories
- **Object placement**: A table set for two but one chair is overturned
- **Contrast**: A child's toy in a battlefield
- **Sequential discovery**: Clues revealed in exploration order tell a micro-story
- **Absence**: What's missing is as telling as what's present

---

## Dialogue Systems

### Types

| System | Implementation | Best For |
|--------|---------------|----------|
| **Linear** | Cutscene/text dump | Story-critical moments |
| **Branching tree** | Player selects from options | RPGs, adventure games |
| **Hub-and-spoke** | Topics to ask about, order-independent | NPC information gathering |
| **Keyword** | Player types/selects keywords | Investigation games |
| **Bark** | Contextual one-liners | Open world ambient dialogue |
| **Systemic** | Generated from game state | Simulation games |

### Dialogue Writing Guidelines

- **First line matters**: NPC's opening line must establish personality or conflict.
- **3 options rule**: 2 feels binary; 4+ causes decision fatigue; 3 is ideal.
- **Show personality through syntax**: Short sentences = urgent/military. Long = scholarly. Fragments = casual.
- **Avoid exposition dumps**: Break lore into multiple optional conversations.
- **Player voice**: Silent protagonist, voiced protagonist, or player-defined each require different dialogue structures.

---

## Narrative Design Tools (2026-05 Update)

| Tool | Type | Best For | 2026 Status |
|------|------|----------|-------------|
| **Twine** | Free, web-based | Prototyping branching narratives | 2.x line still standard for prototyping |
| **Ink (Inkle)** | Scripting language | Unity / Unreal integration, complex branching | **AAA credibility achieved 2025**: *Vampire: The Masquerade — Bloodlines 2* shipped using Ink. The Chinese Room (developer) released **Inkpot**, an open-source C++ port of the Ink runtime for Unreal Engine. Source: McvUK / Inkle |
| **Yarn Spinner** | Unity tool / engine-portable | C# integration, dialogue trees | **Version 3.1 shipped 2025-12** with async dialogue runner methods, option fallthrough, reworked typewriter system, and full Text Animator integration in the paid version. Notable shipped titles: *DREDGE*, *A Short Hike*, *Lost in Random* |
| **Arcweave** | Visual editor | Team collaboration, complex stories | |
| **Articy:Draft** | Professional suite | Large-scale production, localization | |
| **Chat Mapper** | Visual editor | Cinematic dialogue, voice acting pipelines | |

### AI NPC / Conversational AI Platforms (2026)

For dynamic dialogue beyond pre-authored branching, the 2026 landscape:

| Platform | Strength | Notable Adoption |
|----------|----------|------------------|
| **Inworld AI** | Voice AI platform + Agent Runtime for real-time apps. TTS ranked #1 on Artificial Analysis (sub-200ms latency). Clients: Google, NVIDIA, Meta, Ubisoft, Xbox. | Embedded in titles from Ubisoft, KRAFTON, NetEase via NVIDIA ACE collaboration |
| **Convai** | Real-time conversational AI built for Unity / Unreal; scene-aware NPCs. | Smaller-studio SDK option (alongside Inworld + NVIDIA ACE) |
| **NVIDIA ACE** | Stack-level integration for generative NPCs. | KRAFTON, Ubisoft, NetEase, Perfect World Games |

**2026 hybrid approach**: Strong human-authored foundations (Ink / Yarn Spinner for skeleton branches and key beats) **enhanced by** generative layers (Inworld / Convai for incidental dialogue, ambient NPC reactions, and emergent player-character chatter). Pure-AI dialogue still struggles with consistency, lore-faithfulness, and authorial voice; pure-authored dialogue still struggles with player-input volume at modern scale. The trade-offs are cloud dependency, authoring depth, and runtime maturity. Source: PowerUp Gaming / GladeCore / Naavik 2026 coverage.

Quest must include a curation gate on any AI-NPC integration spec: human-review window, safety-classifier layer, and fallback-to-authored-dialogue path.

---

## Narrative Anti-Patterns

- **Ludonarrative dissonance**: Story says "hurry" but gameplay rewards exploration. Align mechanics with narrative urgency.
- **Chosen One syndrome**: Player is special because the story says so, not because of player actions. Earn the status through gameplay.
- **Info dump**: Front-loading exposition. Distribute lore across optional discoveries.
- **False choice**: Dialogue options that lead to the same outcome. If choices don't matter, don't offer them.
- **Fridge logic**: Plot holes obvious on reflection. Playtest with narrative-focused testers.
- **Cutscene incompetence**: Player character is powerful in gameplay but helpless in cutscenes. Maintain consistency.
