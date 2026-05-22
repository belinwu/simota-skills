# Level Design

## Purpose

A level is a problem the player solves with the verbs the game gave them. Designing levels means designing the **shape of the problem**: pacing, signposting, encounter density, branching, and the felt arc from entry to exit.

## Scope Boundary

- IN scope: pacing curves, signposting / wayfinding, critical-path vs branching, encounter density, set-piece placement, environmental storytelling beats, beat-sheet authoring, 8-shape progression.
- OUT of scope: art direction (delegate to `vision`), specific environment art (`dot` / `clay`), exact balance numbers (`balance`), economy / loot (`economy`), narrative dialogue (`narrative`), code (`builder` / `forge`).

## Core Concepts

### Level Types and Their Shapes

| Type | Examples | Shape |
|------|----------|-------|
| Linear corridor | *Half-Life 2*, *The Last of Us*, *Uncharted* | One thread; high authorial control |
| Hub-and-spoke | *Hollow Knight* (Dirtmouth), *Dark Souls* (Firelink), most MMO zones | Central rest, radial branches |
| Branching | *Bioshock 2* level layouts, Metroidvania zones | Multiple critical paths; backtrackable |
| Open-world chunk | Witcher 3 region, GTA district | Player-defined order; many micro-objectives |
| Arena | Souls boss arenas, fighting-game stages | Single space, focused fight |
| Procedural | *Spelunky*, *Hades*, *Diablo* dungeons | Generation rules + handcrafted modules |
| Puzzle room | *Portal* test chambers, escape rooms | Single problem, single solution space |
| Sandbox plot | *Hitman* missions, *Deus Ex* levels | Multiple verbs to reach one goal |

Choose level type from genre + the question "what kind of agency does the player have here?"

### Pacing Curves

Pacing = the rhythm of intensity over time. Two canonical models:

| Model | Source | Pattern |
|-------|--------|---------|
| Calm-Tense-Calm | Mark Brown, *Game Maker's Toolkit* | Open with low intensity → build → climax → release |
| Lazzaro 4 Keys | Nicole Lazzaro | Easy Fun → Hard Fun → Serious Fun → People Fun, layered through the level |
| Two-peak | *Resident Evil 4*, *Half-Life 2* | Mid-level mini-climax + final-level climax |
| Three-act | *Last of Us* chapters | Setup → Confrontation → Resolution within one level |
| Crescendo | *DOOM 2016* corridor of arenas | Continuous escalation |
| Wave | Tower defense, horde shooters | Pulses of intensity with cooldown |

Map intensity to a beat-sheet (below). Without a curve, levels feel flat or exhausting.

### Signposting and Wayfinding

Players must know **where to go** without explicit pointers. Tools:

| Cue | Example |
|-----|---------|
| Lighting | Bright spot pulls eye through dark space (*Half-Life 2*) |
| Color contrast | Yellow paint on climbable ledges (*Uncharted*) |
| Silhouette | Distinct landmark visible from spawn (*BOTW* tower) |
| Audio cue | NPC voice / music swell pulls toward objective |
| Affordance | Climbable surface reads as climbable (*Mirror's Edge* red) |
| Sightline | Composed framing — player sees the goal early |
| Negative space | Empty corridor leads forward; cluttered space reads as side area |
| Verticality | Higher ground = goal in many games |

Anti-pattern: relying on map waypoints alone. Players who turn waypoints off must still find their way.

### Critical Path vs Branching

| Choice | When | Risk |
|--------|------|------|
| Pure linear | Heavy narrative / scripted moments | Loses replay; no player agency |
| Critical path + side rooms | Most action / adventure | Side rooms must offer real reward |
| Multiple critical paths | Metroidvania, immersive sims | Production cost multiplies |
| Open + soft-gated | Open world | Difficulty calibration is hard |

Production rule: every branching path is multiplicative content cost. Cap branches at 2–3 per major junction unless content reuse is planned.

### Encounter Density and Spacing

Encounters per minute is a tunable. Approximate ranges:

| Genre | Encounters/10 min |
|-------|-------------------|
| Tactical / horror | 1–3 |
| Action / shooter | 5–10 |
| Hack-and-slash | 10–20 |
| Roguelite | 6–12 |
| Stealth | 2–5 (with patrols counted differently) |

Add **breath beats** between encounters — exploration / dialogue / vista — to prevent fatigue. Without breath, even good combat becomes monotonous.

### Set-Pieces

A set-piece is a high-investment moment: scripted spectacle, mini-boss, scripted environmental event, story beat. Rules:

- 1–3 set-pieces per level.
- Set-piece announces itself visually before triggering (the train arrives 30 seconds before it explodes).
- Set-piece does NOT replace the verb — players use existing skills in elevated context.
- Cost-aware — set-pieces are 5–10× the cost of standard content.

### Environmental Storytelling

Show, don't tell. Environmental beats convey lore without dialogue:

| Pattern | Example |
|---------|---------|
| Aftermath | Bloody handprint on wall, body posed mid-action |
| Trace | Notes / journals / audio logs left in context |
| Skeleton | Diorama of failure — show the prior victim's last move |
| Architecture | Building purpose readable from layout |
| Population | Inhabitants behaving in-character (animations on loop) |
| Decay | Visible time passing — overgrowth, rust, dust |

Anti-pattern: stuffing every room with text logs. Environmental beats work when sparse and earned.

### The 8-Shape (Lazzaro)

A lap that returns to start, layered with new context. *Hollow Knight*'s zones, *Souls* shortcuts, and *Dark Souls*' return-to-Firelink-via-shortcut all use this.

Beat sequence:

1. Setup at hub.
2. Exploration outward.
3. Mid-level revelation / shortcut found.
4. Loop back to hub from new direction.
5. Hub feels different because of new knowledge.

The 8-shape is **the** pattern for memorable level design. Pure linear paths are forgotten; loops are remembered.

### Beat-Sheet Authoring

Levels are designed at the beat level, not the moment-to-moment. A beat sheet:

| Beat | Time | Player verb | Intensity | Note |
|------|------|-------------|-----------|------|
| 1 | 0:00 | walk | 1 | Spawn; vista; signpost goal |
| 2 | 0:30 | combat | 4 | First skirmish; teaches enemy A |
| 3 | 2:00 | explore | 2 | Hidden room; lore note + minor item |
| 4 | 3:30 | combat | 6 | Multi-enemy; combine A + B |
| 5 | 5:00 | puzzle | 3 | Environmental; teaches mechanic X |
| 6 | 7:00 | combat | 8 | Mini-boss using mechanic X |
| 7 | 9:00 | walk | 2 | Cooldown vista; story beat |
| 8 | 11:00 | climax | 10 | Boss; uses A, B, X |
| 9 | 13:00 | resolution | 1 | Reward; preview next level |

Beat sheet is the level's spine. Build art and detail around it; never the reverse.

### Procedural Levels

Procgen ≠ random. Good procgen uses:

- **Authored modules** (rooms, sub-graphs, tile sets) shuffled by rules.
- **Distribution constraints** (rare = once per level, common = 1 per 3 rooms).
- **Critical-path guarantees** (always at least one solvable path).
- **Pacing budget** (ensure encounter density and rest beats balance).
- **Fail-state handling** (dead ends, loops, soft-locks must be detected).

References: *Spelunky* (Yu), *Hades* (Supergiant), *Slay the Spire* node-graph generator, *Diablo* dungeon BSP.

**Generative-AI level generation (2026 caveat)**: 52% of GDC 2026 State of the Game Industry respondents view generative AI as having a negative industry impact (up from 30% in 2025, 18% in 2024); only 7% positive. Treat any AI-generated layout as an unqualified candidate that must pass the same beat-sheet, signposting, encounter-density, soft-lock, and pacing-budget audits as a handcrafted level. AI-assisted modulation of authored modules (parameter sweep, decorator pass, distribution sampling) is healthier than full-stack AI generation. Always pair AI-assisted level pipelines with explicit human curation gates and aesthetic-coherence checks to avoid the "gameslop" reputational pattern.

### Tutorial Integration

Levels teach. Implicit tutorials beat tutorials-as-text:

| Pattern | Example |
|---------|---------|
| Safe sandbox | First room has the verb's affordance with no consequence (*Mario* world 1-1's first goomba) |
| Learn → test → twist | Introduce → use → recombine in 3 beats |
| Optional master class | Side room rewards mastery without requiring it |
| In-context prompt | Button hint shows once on first relevant moment |
| Progressive complexity | Each level adds 1 new mechanic; sticks to it for 5+ encounters |

Anti-pattern: tutorial sequence dumped in a single tutorial level. Players forget by mission 3.

### Soft-Lock Detection

Every level should pass:

- Can the player reach the exit from any pocket? (no soft-locks)
- Can the player die without resources to restart efficiently?
- Do all branches yield a path forward (no dead ends)?
- Are checkpoints placed at boss / set-piece entries?

## Workflow

1. **Choose level type** — linear / hub / branching / arena / etc.
2. **Articulate the level question** — what problem are we asking the player to solve?
3. **Pick a pacing curve** — calm-tense-calm / two-peak / three-act / etc.
4. **Sketch a beat sheet** — 6–12 beats with time, verb, intensity.
5. **Plot signposting** — what guides the player at each transition?
6. **Decide critical path / branches** — count branches; verify content cost.
7. **Set encounter density** — encounters / 10 min within genre range.
8. **Place set-pieces** — 1–3, announced before they fire.
9. **Drop environmental storytelling beats** — sparse, earned.
10. **Apply 8-shape if applicable** — return-to-hub with new perspective.
11. **Plan tutorial integration** — implicit, contextual.
12. **Soft-lock audit** — exits reachable, checkpoints placed.
13. **Hand off** — beat sheet to `builder` for blockout; art briefs to `vision` / `dot` / `clay`.

## Output Template

```yaml
level_design:
  level_id: A1-2
  level_type: branching
  question: "Can the player choose stealth or combat to reach the lab?"
  pacing_curve: two_peak
  target_minutes: 14
  beat_sheet:
    - beat: 1
      time_min: 0
      verb: walk
      intensity: 1
      note: "spawn balcony with vista of objective"
    - beat: 2
      time_min: 1
      verb: stealth_or_fight
      intensity: 4
      note: "first patrol; player chooses approach"
    - beat: 3
      time_min: 3
      verb: explore
      intensity: 2
      note: "side room: lore log + medkit"
    - beat: 4
      time_min: 5
      verb: combat
      intensity: 7
      note: "first peak; arena fight"
    - beat: 5
      time_min: 7
      verb: walk
      intensity: 2
      note: "calm vista corridor; story beat"
    - beat: 6
      time_min: 8
      verb: puzzle
      intensity: 3
      note: "environmental puzzle teaches mechanic X"
    - beat: 7
      time_min: 11
      verb: combat
      intensity: 9
      note: "second peak; boss using X"
    - beat: 8
      time_min: 13
      verb: resolution
      intensity: 1
      note: "reward + preview A1-3"
  signposting:
    - cue: lighting
      placement: corridor_to_first_arena
    - cue: silhouette
      placement: tower_visible_from_spawn
    - cue: audio_cue
      placement: boss_chamber_entry
  critical_path: stealth_route + combat_route + sneak_combo
  branches:
    - junction: catwalk_split
      paths: [stealth, combat]
      content_cost_multiplier: 1.6
  encounter_density:
    encounters: 5
    breath_beats: 3
    encounters_per_10min: 4
  set_pieces:
    - id: SP-1
      beat: 7
      type: boss_fight
      announced_at_beat: 6
  environmental_storytelling:
    - beat: 3
      pattern: trace
      content: "scientist's audio log mid-experiment"
    - beat: 5
      pattern: aftermath
      content: "abandoned lab equipment + body"
  shape: 8_shape
  hub_return: yes_after_boss
  tutorial:
    new_mechanic_introduced: mechanic_X
    learn: beat_6
    test: beat_7
  soft_lock_audit:
    exits_reachable_from_all_pockets: yes
    checkpoints: [beat_4_entry, beat_7_entry]
    branch_dead_ends: 0
  handoff:
    builder: blockout_request
    vision: art_direction_brief
    balance: encounter_difficulty_targets
```

## Anti-Patterns

- Building art before the beat sheet — production drift, no rhythm.
- Pure linear paths with no exploration — flat memory, low replay.
- Branching without budget — content cost balloons, levels ship unfinished.
- Encounter-dense corridors with no breath beats — fatigue.
- Set-piece without announce — feels like ambush, not spectacle.
- Tutorial dumped in level 1, forgotten by level 4.
- Wayfinding via map waypoints alone — fails when waypoints off.
- 8-shape attempted in linear genre — confusing without the genre's expectation of return.
- Procgen with no critical-path guarantee — soft-locks ship.
- Environmental storytelling stuffed into every room — noise, no signal.
- Set-pieces driving the critical path so hard players cannot fail — feels rail-roaded.
- Level question unspecified — design becomes "more rooms".
- Boss arena with no architectural readability — players don't understand spatial constraints.
- Branches that converge to identical outcomes — wasted player choice.
- Levels designed without a verb — "what does the player do here?" must be the first answer, not the last.

## Deliverable Contract

A level design is complete when:

- Level type chosen with rationale.
- Level question articulated.
- Pacing curve named.
- Beat sheet documented with 6–12 beats (time / verb / intensity / note).
- Signposting cues specified.
- Critical path / branches counted with content-cost multiplier.
- Encounter density within genre range.
- Set-pieces identified with announce-beats.
- Environmental storytelling beats placed sparsely.
- 8-shape considered.
- Tutorial integration mapped.
- Soft-lock audit passes.
- Handoff briefs prepared for builder / vision / balance.

## References

- Henry Smith / Mark Brown, *Game Maker's Toolkit* — Boss Keys / Level Design videos.
- Sander van der Vegte, *Worlds Beyond* GDC talks.
- *Hollow Knight* zone analyses (Team Cherry GDC).
- Jaime Griesemer, *The 30 seconds of fun* (Halo) — micro-loop level design.
- Iain Bull, *Designing levels for Hitman* (GDC).
- Cliff Bleszinski, *The Art of Level Design* lectures.
- *Half-Life 2* commentary tracks — wayfinding lighting masterclass.
- Steve Lee, *Level Design Workshop* (YouTube).
- Dan Cook, *Lostgarden* — skill atom / level granularity.
- *Spelunky* by Derek Yu (book) — handcrafted-modular procgen.
- *Boss Keys* (Mark Brown) — Metroidvania graph-design analysis.
- Christopher Totten, *An Architectural Approach to Level Design* (2nd ed., 2019).
- Robert Yang, *Radiator Blog* — environmental storytelling theory.
- Nicole Lazzaro, *Why We Play Games: Four Keys to More Emotion Without Story*.
