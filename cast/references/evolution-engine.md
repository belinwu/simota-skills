# Cast Evolution Engine

Evolution mechanism specification for data-driven persona updates.

---

## Overview

The evolution engine detects persona drift from new data, applies controlled updates, and maintains a full audit trail. Inspired by Harvest's chronicle system but adapted for structured persona data.

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  DETECT   │───→│  ASSESS   │───→│  APPLY    │───→│  LOG      │───→│ PROPAGATE│
│  Drift    │    │  Impact   │    │  Changes  │    │  History  │    │  Notify  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
```

---

## Drift Detection

### The 4 Drift Axes

Cast monitors persona drift across 4 axes:

| Axis | What Changes | Detection Signals | Threshold |
|------|-------------|-------------------|-----------|
| **Goals** | User objectives evolve | New JTBD patterns, changed priorities | ≥1 goal significantly shifted |
| **Pain Points** | Frustrations change | New complaints, resolved issues | ≥1 pain point added/removed |
| **Behavior** | Usage patterns shift | Session patterns, device mix, frequency | ≥2 behavioral attributes changed |
| **Segment** | User demographic shifts | New user types emerge, existing segments merge | Segment boundaries change |

### Detection Algorithm

```
FOR each active persona in registry:
  FOR each drift axis:
    compare(persona.current_state, new_data)
    IF difference > axis_threshold:
      flag_drift(persona, axis, difference)

  IF count(flagged_axes) >= 1:
    trigger_evolution(persona)
```

### Signal Sources

| Source Agent | Drift Signals Provided |
|-------------|----------------------|
| **Trace** | Session duration changes, navigation pattern shifts, device mix changes, drop-off point changes |
| **Voice** | New feedback themes, NPS score shifts, emerging complaints, resolved pain points |
| **Pulse** | Funnel metric changes, cohort behavior shifts, engagement pattern changes |
| **Researcher** | New interview findings, updated user segments, revised journey maps |

---

## Impact Assessment

### Severity Levels

| Severity | Criteria | Action |
|----------|----------|--------|
| **Minor** | 1 attribute changed within 1 axis | Auto-apply, minor version bump |
| **Moderate** | 2-3 attributes changed across 1-2 axes | Auto-apply with notification, minor version bump |
| **Significant** | 4+ attributes changed across 2+ axes | Require confirmation, minor version bump |
| **Identity** | Role or Category would change | Block — create new persona instead |

### Change Classification

```yaml
change_classification:
  minor_changes:
    - device_percentage_shift (< 20%)
    - session_duration_change (< 50%)
    - single_pain_point_update
    - single_behavior_update
    - emotion_trigger_refinement

  moderate_changes:
    - tech_level_shift
    - usage_frequency_change
    - multiple_pain_point_updates
    - goal_priority_reorder
    - context_scenario_addition

  significant_changes:
    - primary_goal_change
    - major_behavior_pattern_shift (3+ behaviors)
    - segment_boundary_change
    - echo_base_mapping_change

  identity_changes:
    - role_change
    - category_change
    - fundamental_user_type_shift
```

---

## Evolution Application

### Merge Rules

When applying new data to existing persona attributes:

| Rule | Description |
|------|-------------|
| **Newer wins** | When conflicting, more recent data takes precedence |
| **Higher confidence wins** | When timestamps are similar, higher confidence source wins |
| **Additive preferred** | Add new attributes rather than replacing existing ones |
| **Evidence required** | Every change must reference its data source |
| **Inferred preserved** | `[inferred]` markers stay until real data confirms/replaces |

### Section-Level Application

| Section | Evolution Behavior |
|---------|-------------------|
| **Profile** | Individual attribute updates (except Role — immutable) |
| **Quote** | Replace if new data provides more representative voice |
| **Goals** | Reorder, refine wording, add/remove (maintain 3) |
| **Frustrations** | Add new, resolve old, reword (maintain 3) |
| **Behaviors** | Update based on behavioral data (maintain 3) |
| **Emotion Triggers** | Refine triggers, adjust scores based on evidence |
| **Context Scenarios** | Add new scenarios, update existing environment details |
| **JTBD** | Refine jobs, rarely replace (fundamental needs are stable) |
| **Echo Testing Focus** | Update priority flows based on new friction data |
| **Extended Sections** | Update individual attributes with new evidence |

### Frontmatter Updates

On every evolution:
```yaml
version: "X.Y+1"           # Bump minor version
status: active              # Reset to active (from evolved)
updated: "YYYY-MM-DD"      # Current date
evolution_count: N+1        # Increment
confidence: recalculated    # Recalculate from all sources
```

---

## Evolution Log

### Entry Format

Each evolution adds a row to the persona's Evolution Log:

```markdown
## Evolution Log

| Version | Date | Source | Changes | Confidence Delta |
|---------|------|--------|---------|-----------------|
| 1.0 | 2026-02-01 | README, src/auth | Initial creation | 0.65 |
| 1.1 | 2026-02-08 | Trace session data | Behavior: device split 60/40→70/30 mobile. Context: added commute scenario | +0.10 |
| 1.2 | 2026-02-15 | Voice NPS feedback | Frustration: added "hidden shipping costs". Pain Points refined | +0.07 |
```

### Entry Fields

| Field | Description | Example |
|-------|-------------|---------|
| **Version** | New version after this evolution | `1.2` |
| **Date** | ISO 8601 date | `2026-02-15` |
| **Source** | Data source that triggered evolution | `Trace session data` |
| **Changes** | Concise description of what changed | `Behavior: device split updated` |
| **Confidence Delta** | Change in confidence score | `+0.07` or `-0.05` |

---

## Confidence Decay Algorithm

### Decay Schedule

```
current_date = today()
days_since_update = current_date - persona.updated

IF days_since_update < 30:
  decay = 0  # No decay within 30 days

ELIF days_since_update < 60:
  weeks_over = ceil((days_since_update - 30) / 7)
  decay = weeks_over * 0.05  # -0.05/week

ELIF days_since_update < 90:
  weeks_over = ceil((days_since_update - 30) / 7)
  decay_30_60 = 4 * 0.05  # First 4 weeks at -0.05
  weeks_60_plus = ceil((days_since_update - 60) / 7)
  decay = decay_30_60 + (weeks_60_plus * 0.10)  # -0.10/week after 60 days

ELSE:
  # Freeze at current value, recommend archival
  decay = frozen
  recommend_archival(persona)

new_confidence = max(0.0, persona.confidence - decay)
```

### Decay Notifications

| Days Since Update | Notification | Severity |
|-------------------|-------------|----------|
| 30 | "Persona {name} hasn't been updated in 30 days" | Info |
| 45 | "Persona {name} confidence decaying (-0.05/week)" | Warning |
| 60 | "Persona {name} confidence decaying faster (-0.10/week)" | Warning |
| 90 | "Persona {name} recommended for archival review" | Critical |

---

## Batch Evolution (EVOLVE ALL)

When scanning all personas for drift:

### Process

1. **Collect** new data from all source agents (Trace, Voice, Pulse)
2. **Compare** each active persona against new data
3. **Rank** evolutions by impact (significant first)
4. **Apply** based on severity rules (auto-apply minor, confirm significant)
5. **Report** summary of all changes

### Batch Report Format

```markdown
## Cast Evolution Report

**Scan date:** 2026-02-16
**Personas scanned:** 8
**Evolutions detected:** 3
**Auto-applied:** 2
**Requires confirmation:** 1

| Persona | Severity | Axes | Changes | New Confidence |
|---------|----------|------|---------|---------------|
| First-Time Buyer | Minor | Behavior | Device split updated | 0.82 → 0.85 |
| Power Shopper | Moderate | Goals, Pain | Goal priority shifted, new frustration | 0.75 → 0.80 |
| Enterprise Admin | Significant | Behavior, Segment | Usage pattern fundamentally changed | 0.70 (review needed) |
```

---

## Core Identity Protection

### Immutable Fields

The following fields cannot be changed through evolution:

| Field | Location | Why Immutable |
|-------|----------|---------------|
| `Role` | Profile section | Defines who the persona IS |
| `category` | Frontmatter | Fundamental classification |
| `service` | Frontmatter | Service binding |

### Identity Change Protocol

When data suggests Core Identity should change:

1. **Flag** the change as Identity-level severity
2. **Present** evidence to user with `ON_IDENTITY_CHANGE` trigger
3. **If approved** → Create new persona + archive old one
4. **Cross-reference** → New persona's Source Analysis references old persona
5. **Update registry** → Remove old, add new, update coverage

```markdown
## Source Analysis

| Source | Extracted Information |
|--------|----------------------|
| Evolved from Power Shopper v1.3 | Behavioral data showed role shift from "frequent buyer" to "marketplace seller". New persona created to reflect fundamentally different user type |
| Trace session data (2026-02-15) | Session patterns match seller behavior: listing creation, inventory management, pricing comparison |
```
