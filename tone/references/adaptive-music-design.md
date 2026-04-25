# Adaptive Music Design Reference

Purpose: Design interactive / adaptive music systems where music responds to gameplay state. Cover vertical layering (stem combinations), horizontal re-sequencing (segment switching), transition matrices, stingers, FMOD Studio, Wwise Interactive Music, and engine integration.

## Scope Boundary

- **tone `adaptive`**: Adaptive music architecture (this document).
- **tone `bgm` (elsewhere)**: Static BGM asset generation.
- **tone `sfx` / `voice` / `ui` (elsewhere)**: Non-music audio.
- **tone `spatial` (elsewhere)**: 3D positional (orthogonal concern).
- **tone `lufs` (elsewhere)**: Loudness normalization across stems.
- **Quest (elsewhere)**: Game state taxonomy that drives music.
- **Builder (elsewhere)**: Engine integration code beyond stubs.

## Two Core Techniques

### Vertical (Layering)

Multiple stems play *simultaneously*; each stem's volume is controlled by gameplay parameters.

```
TIME →
─────────────────────────────────
[drums]    ████████████████████
[bass]     ████████████████████
[harmony]      ████████████████   (fades in at tension=0.5)
[melody]              ██████████   (fades in at tension=0.8)
─────────────────────────────────
```

- Strength: smooth gradient between calm ↔ intense
- Cost: stems must be musically compatible at all combinations
- Use: open-world, exploration, gradual tension (Skyrim, Red Dead, Journey)

### Horizontal (Re-sequencing)

A library of *segments* (musical phrases) plays sequentially; gameplay state picks which segment is next.

```
TIME →
[exploration_A] → [exploration_B] → [combat_intro] → [combat_loop_1] →
                                                      [combat_loop_2] → [combat_outro] → [exploration_A]
```

- Strength: clean phrase-based transitions; distinct moods
- Cost: precomposed transitions; segment count grows with state count
- Use: turn-based RPG, action games with discrete states (Final Fantasy, Halo)

### Hybrid

Real systems combine both: horizontal segments with vertical stems within each.

## Transition Matrix

For horizontal: define what plays *between* segments per source/target pair.

```
                    To: explore  combat   boss     death
From: explore       loop         intro    long     stinger_d
From: combat        outro        loop     escalate stinger_d
From: boss          outro        downgrade loop    stinger_d
From: death         intro        intro    intro    -
```

Each cell = a transition rule:
- **At time**: bar / beat / cue / immediate
- **Source action**: continue / fadeout / cut
- **Bridge**: transition segment / stinger / nothing
- **Target action**: from start / from cue / sync to source position

FMOD calls these "transition timelines"; Wwise calls them "music transitions".

## Stingers

Short musical hits triggered by events (level up, item pickup, boss defeat). Play *over* the current music without changing state.

```
EVENT             STINGER         DURATION    FOLLOW
victory_level     fanfare_major   2s          fade-in current
item_legendary    chime_high      1s          continue
boss_defeated     coda_grand      4s          go to victory state
death             dirge_short     2s          go to silence/menu
```

Stingers must be in the same key as the underlying music or they clash. Pre-render in multiple keys, or compose key-agnostic stingers (rhythmic / atonal).

## State Taxonomy

The game state model that drives music:

```
EXPLORATION_LOW    (calm, atmospheric)
EXPLORATION_MED    (tension building)
COMBAT_LOW         (skirmish, 1-2 enemies)
COMBAT_HIGH        (overwhelmed)
BOSS_PHASE_1       (signature theme)
BOSS_PHASE_2       (escalated variation)
VICTORY            (resolution)
DEFEAT             (downbeat resolution)
MENU               (separate music)
LOADING            (suspended state)
```

Plus continuous parameters:
- `tension` (0.0–1.0): drives layer volumes
- `health` (0.0–1.0): subtle filter sweep
- `proximity_to_objective`: melody intensity

## FMOD Studio

```
1. Create Event "music_main"
2. Add Tracks for stems (drums / bass / harmony / melody)
3. Add Parameter "tension" (0–1)
4. Volume automation per track on parameter
5. Add Logic Markers (loop region per state)
6. Transition timelines between markers
7. Stinger events triggered via API
```

API:
```cpp
event->setParameterByName("tension", 0.6f);
event->setParameterByName("state", 2);  // boss
fmodSystem->loadBank("music.bank");
```

## Wwise Interactive Music

```
1. Music Hierarchy: Music Switch Container with sub-Music Segments
2. State Group "GameState" {Explore, Combat, Boss, Victory}
3. Per state: Music Segment with stems on tracks
4. Transition rules: at next bar, with bridge segment
5. Music Stingers triggered via Trigger objects
```

API:
```cpp
AK::SoundEngine::SetState("GameState", "Combat");
AK::SoundEngine::PostTrigger("Stinger_Victory", gameObjectID);
```

## Web Audio (Custom Implementation)

```javascript
class AdaptiveMusic {
  constructor(ctx) {
    this.ctx = ctx;
    this.stems = {};       // {name: GainNode + Source}
    this.tension = 0;
  }
  loadStem(name, url) { /* fetch + decode + connect via gain */ }
  setTension(value) {
    this.tension = value;
    // Linear ramp gain on stems based on tension thresholds
    this.stems.harmony.gain.linearRampToValueAtTime(
      value > 0.4 ? 1 : 0, this.ctx.currentTime + 0.5
    );
    this.stems.melody.gain.linearRampToValueAtTime(
      value > 0.7 ? 1 : 0, this.ctx.currentTime + 0.5
    );
  }
  transitionTo(segment, atBar = true) {
    const targetTime = atBar ? this.nextBarTime() : this.ctx.currentTime;
    this.crossfade(this.currentSegment, segment, targetTime, 0.5);
  }
}
```

## Tempo + Key Discipline

All stems / segments must share:
- **Tempo**: same BPM, or tempo-mapped transitions
- **Time signature**: 4/4 or compatible
- **Key**: same key, or use pivot chords for transitions
- **Loop length**: integer bars (typically 8 / 16 / 32 bars)

Mismatched tempo or key = unmusical transitions. Production discipline: lock these in pre-production.

## Workflow

```
STATE TAXONOMY    →  enumerate game states from Quest / design
                  →  identify continuous parameters

TECHNIQUE         →  vertical / horizontal / hybrid per state group
                  →  rule of thumb: hybrid for AAA, vertical for indie open-world

ASSET PLAN        →  stem list per state (vertical)
                  →  segment list per state (horizontal)
                  →  transitions + stingers
                  →  same tempo / key discipline

COMPOSE           →  produce stems / segments
                  →  pre-export at 24-bit 48kHz
                  →  loop boundaries on integer bars

TRANSITION MATRIX →  per source-target pair: timing + bridge + behavior
                  →  per stinger: trigger event + key compatibility

MIDDLEWARE        →  FMOD / Wwise / custom (Web Audio / Howler)
                  →  parameter design (tension / state)
                  →  bank organization

VOLUME / LUFS     →  per-stem peak normalization (-6 dBFS)
                  →  hand off to tone `lufs` for final loudness

INTEGRATE         →  engine API stubs
                  →  game state → music API mapping
                  →  test all transitions

VALIDATE          →  every transition is musical (no clipping, no clash)
                  →  no awkward silence between segments
                  →  stingers don't clash with key
                  →  test under rapid state changes (combat in/out repeatedly)

HANDOFF           →  Builder: full integration
                  →  Quest: state taxonomy alignment
                  →  tone `lufs`: loudness pass
                  →  tone `bgm`: stem / segment authoring
                  →  Realm: 2D game integration
```

## Output Template

```markdown
## Adaptive Music Plan: [Project / Scene]

### Technique
- Primary: [vertical / horizontal / hybrid]
- Justification: [game state count, transition smoothness need]

### State Taxonomy
| State | Description | Music intent |
|-------|-------------|--------------|
| EXPLORE_LOW | calm overworld | quiet, atmospheric |
| COMBAT_HIGH | overwhelmed | heavy, layered, fast |
| BOSS_P1 | boss intro | signature theme |
| ... | ... | ... |

### Continuous Parameters
| Param | Range | Drives |
|-------|-------|--------|
| tension | 0–1 | layer volumes |
| health | 0–1 | filter sweep |

### Stem / Segment Inventory
**Vertical stems** (per state):
- explore: drums(quiet), bass(quiet), pad
- combat: drums(driving), bass(driving), harmony, melody, percussion

**Horizontal segments**:
- explore_loop_A (16 bars), explore_loop_B (16 bars)
- combat_intro (8 bars), combat_loop_1 (16), combat_loop_2 (16), combat_outro (4)
- boss_p1 (32), boss_p2 (32)

### Transition Matrix
[source × target table with timing / bridge / behavior]

### Stingers
| Event | Stinger | Duration | Key |
|-------|---------|----------|-----|
| level_up | fanfare_major | 2s | C maj |
| boss_defeated | coda_grand | 4s | tonic |

### Tempo + Key
- Tempo: 110 BPM
- Time sig: 4/4
- Key: D minor (modulates to D major in victory)

### Middleware
- Tool: [FMOD / Wwise / Web Audio custom]
- Parameter setup: [list]
- Bank organization: [list]

### Engine Integration
[code stubs for state changes + parameter ramps]

### Validation
- All transitions tested: [pass/fail]
- Rapid state changes: [pass/fail]
- Stinger key clash: [pass/fail]
- LUFS handoff: [pending]

### Handoffs
- Builder: full integration
- Quest: state alignment
- tone `lufs`: loudness
- tone `bgm`: stem / segment authoring
- Realm: 2D integration
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Stems with different tempos | Lock tempo in pre-production |
| Hard cuts on state change without transition | Use transition matrix; bridge segments |
| Stingers in random keys | Pre-render per-key OR compose key-agnostic |
| 100+ states with full transition matrix | Reduce to 5-10 states; use parameters for variation |
| Music never resolves on state exit | Outro segments per state |
| Layering produces dissonance at certain combos | Composer must verify all layer combinations |
| Engine API call per frame | Set parameters at state change only |
| Loop point not on integer bar | Always loop on bar boundaries |
| BGM bank loaded per scene change | Streaming / persistent bank for music |
| Adaptive music tested only in calm | Test under rapid combat in/out |
| Stinger volume = music volume (drowns out) | Stinger -3 to -6 dB above music |
| Death state with same theme as combat | Distinct "defeat" theme; players need closure |
| Vertical stems unmastered as a sum | Mix the full sum, not individual stems |
| Continuous parameter steps not smoothed | Linear ramp 0.5-2s on parameter change |
| Boss music doesn't loop seamlessly | Test 5-min loop without seam click |
| No silence between bars allowed | Sometimes silence is the right beat |

## Deliverable Contract

When `adaptive` completes, emit:

- **Technique choice** (vertical / horizontal / hybrid) with rationale.
- **State taxonomy** + continuous parameters.
- **Stem / segment inventory** per state.
- **Transition matrix** with timing / bridge / behavior.
- **Stinger** definitions with key compatibility.
- **Tempo + key** discipline statement.
- **Middleware** (FMOD / Wwise / custom) configuration.
- **Engine integration** code stubs.
- **Validation** plan + results.
- **Handoffs**: Builder, Quest, tone lufs, tone bgm, Realm.

## References

- *A Composer's Guide to Game Music* — Winifred Phillips
- *The Cambridge Companion to Video Game Music* — Fritsch + Summers
- *The Art of Game Audio* — Phillips
- FMOD Studio User Manual — fmod.com/docs
- Wwise Interactive Music — audiokinetic.com/learn
- "Adaptive Music in Halo" — Marty O'Donnell GDC talks
- "Music for Skyrim" — Jeremy Soule interviews
- "Red Dead Redemption 2 Adaptive Audio" — Rockstar audio team
- "Journey Music" — Austin Wintory GDC postmortem
- "Inside Outside Adaptive Music" — Martin Stig Andersen (Limbo, Inside)
- *Game Audio Implementation* — Stevens + Raybould
- *Designing Sound* — Andy Farnell (procedural audio + sequencing)
- Microsoft Project Acoustics — for music spatial integration
- AES — Audio Engineering Society game audio papers
- "Vertical Remixing" — early Lucasarts iMUSE system
- iMUSE (LucasArts) — origin of horizontal re-sequencing
- "Crash Bandicoot Music Mixing" — Mark Mothersbaugh interview
- Howler.js, Tone.js — JavaScript adaptive music libraries
