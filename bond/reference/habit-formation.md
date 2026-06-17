# Bond Habit Formation Design

Purpose: Hook Model design, behavior-design foundation, streak rules, and habit-loop safeguards.
Contents: Fogg Behavior Model (foundation), Hook Model template, reward taxonomy, investment choices, streak logic.

## Fogg Behavior Model (B=MAP) — the foundation under the Hook

The Hook Model's **Action** step rests on BJ Fogg's behavior model: a behavior occurs only
when **Motivation**, **Ability**, and a **Prompt** converge at the same moment.

```
B = M · A · P     (behavior happens iff all three are present together)
```

| Factor | Meaning | Design lever |
|--------|---------|--------------|
| `Motivation` | desire to act (pleasure/pain, hope/fear, acceptance/rejection) | usually expensive to raise — do not rely on it |
| `Ability` | how easy the action is (time, money, effort, routine fit) | **cheapest lever — make the behavior smaller/easier first** |
| `Prompt` | the cue to act now (= the Hook's Trigger) | only fires behavior when M and A are already sufficient |

**Action line:** plot a behavior on the Motivation (y) × Ability (x) plane. A prompt above
the curve → behavior fires; below → it fails. Three prompt types: `spark` (raises motivation),
`facilitator` (raises ability), `signal` (when M and A are both already high — a pure reminder).

Design rules that flow into the Hook:
- **Increase Ability before Motivation.** Shrink the target behavior until it fits the user's
  lowest-motivation moment. This is why the Hook's `Action` block specifies the *smallest*
  useful action.
- **Match prompt type to the M×A state.** A `signal` prompt sent to a low-ability user is the
  #1 cause of dead notifications — diagnose before adding triggers.
- **Behavior fizzles below the action line** — if a habit isn't forming, the failure is M, A, or
  prompt-timing, not "not enough reminders." Map which factor is missing before iterating.

The Hook Model below operationalizes B=MAP into a repeating loop (Trigger=Prompt, Action=B,
Variable Reward + Investment = motivation/ability reinforcement for the *next* cycle).

## Hook Model Template

```markdown
## Hook Model: [Feature/Behavior]

### 1. Trigger
**External triggers**
- Push notification at [time]
- Email digest on [day]
- Calendar reminder

**Internal triggers**
- Emotion: [situation] -> Product
- Routine: [existing routine] -> Product

### 2. Action
**Target behavior:** [smallest useful action]
**Motivation:** [why the user wants it]
**Ability:** [how easy it is]

### 3. Variable Reward
| Type | Example |
|------|---------|
| Tribe | Social response from others |
| Hunt | Discovery of something new |
| Self | Visible progress or skill gain |

### 4. Investment
Users invest one or more of:
- time
- data
- social graph
- learning effort
```

## Streak System Rules

| Situation | Rule |
|-----------|------|
| Same-day activity | No streak change |
| `daysDiff === 1` | Increment streak |
| `daysDiff === 2` and protection available | Consume 1 protection and continue |
| `daysDiff > 2` or no protection | Reset to `1` |
| Milestone reached | Award at `7`, `30`, `100`, `365` days |

## Streak UI Cues

- Show current streak.
- Show remaining streak protections when available.
- Show longest streak as a recovery anchor after a streak break.
