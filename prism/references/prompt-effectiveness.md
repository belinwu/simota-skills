# Prompt Effectiveness System (SPECTRUM)

Prompt pattern tracking, format-audience fit analysis, template performance measurement, and steering strategy improvement.
Prism gets better at designing steering prompts by learning from outcomes.

---

## Overview

The SPECTRUM phase runs post-task (or periodically) to close the feedback loop between prompt design activities and actual output quality. Without SPECTRUM, prompt recommendations stay static and format-audience fit remains uncalibrated. With it, Prism's prompt designs become progressively more effective and audience-aligned.

```
RECORD ──→ EVALUATE ──→ CALIBRATE ──→ PROPAGATE
  │            │            │            │
  │ Log       │ Measure    │ Update    │ Share with
  │ prompts   │ quality &  │ pattern   │ Lore
  │ & scores  │ trends     │ weights   │
```

---

## RECORD — Log Prompt Design Activities

After each prompt design task, record:

```yaml
Task: [task-id]
Format: [Audio Deep Dive | Audio Brief | Audio Critique | Audio Debate | Audio Lecture | Video Explainer | Video Brief | Slide Presenter | Slide Detailed | Infographic | Mind Map | Deep Research]
Audience_Type: [C-suite | PM | Senior Engineer | Junior Dev | Researcher | General Public | Student | Sales]
Source_Pattern: [Single Deep | Multi-Perspective | Hierarchical | Comparative | Chronological]
Source_Count: [number]
Prompt_Layers_Used:
  L1_audience: [yes/no]
  L2_focus: [yes/no]
  L3_tone: [yes/no]
Patterns_Applied:
  - pattern: [Audience Anchor | Negative Space | Focus Laser | Tone Dial | Duration Target | Structural Blueprint]
    effectiveness: [High/Medium/Low/Unknown]
Quality_Score:
  accuracy: [1-5]
  audience_fit: [1-5]
  engagement: [1-5]
  completeness: [1-5]
  actionability: [1-5]
  overall: [1.0-5.0]
Iterations_Required: [count]
Downstream_Handoff: [Morph/Growth/Canvas/Lore/None]
```

### What to Track

| Data Point | Why | Used For |
|-----------|-----|----------|
| Format × audience quality | Core calibration input | Format recommendation improvement |
| Prompt pattern effectiveness | Which patterns produce highest quality per context | Pattern selection heuristic |
| Source composition impact | Which notebook patterns work best for which formats | Source advice improvement |
| Iteration count | How many rounds needed to reach quality target | Prompt template refinement |
| Three-layer completeness | Which layers are most impactful per format | Layer guidance tuning |
| Downstream utilization | Did Morph/Growth/Canvas use the output? | Output format improvement |

---

## EVALUATE — Measure Prompt Design Impact

### Quality Trend Tracking

```
Average Quality Score = Sum of Overall Scores / Total Tasks

> 4.2  = Excellent prompt design (pattern is working)
3.5-4.2 = Good quality (maintain approach, minor tuning)
2.5-3.5 = Moderate quality (review pattern selection, source advice)
< 2.5  = Low quality (investigate root causes)
```

### Format-Audience Fit Tracking

```
Fit Score = Tasks Scoring ≥ 4.0 on Audience Fit / Total Tasks for Format × Audience

> 0.85  = Highly effective combination
0.70-0.85 = Good, some contexts need tuning
< 0.70  = Underperforming (review template, audience guidance)
```

### Evaluation Triggers

| Trigger | Check |
|---------|-------|
| Quality score < 3.0 | Source quality, prompt pattern selection, format match |
| User requests major revision | Audience mismatch, tone calibration, scope issue |
| 3+ iterations required | Template completeness, pattern guidance |
| New NotebookLM feature released | Format capability updates, constraint changes |
| Quarterly review | Overall prompt design health |

### Per-Period Evaluation Summary

```markdown
### Prompt Design Evaluation

| Metric | Value | Trend |
|--------|-------|-------|
| Prompt designs completed | 15 | — |
| Average quality score | 4.1/5.0 | ↑ |
| Score ≥ 4.0 rate | 73% (11/15) | ↑ |
| Average iterations | 1.8 | ↓ |
| Most used format | Audio Deep Dive (40%) | — |
| Most used pattern | Audience Anchor (87%) | — |
| Downstream utilization | 80% (12/15) | — |

**Strongest combination**: Audio Deep Dive × Senior Engineer (4.5 avg)
**Weakest area**: Video Brief × General Public (3.2 avg — tone calibration needed)
**Note**: Negative Space pattern improved focus scores by 25%.
```

---

## CALIBRATE — Update Prompt Design Heuristics

### Pattern Effectiveness Scoring

Track which patterns work best in which contexts:

```yaml
# Default pattern effectiveness by format
audio_patterns:
  audience_anchor: 0.95
  negative_space: 0.90
  focus_laser: 0.85
  tone_dial: 0.85
  duration_target: 0.80
  structural_blueprint: 0.75
video_patterns:
  audience_anchor: 0.90
  focus_laser: 0.90
  tone_dial: 0.80
  structural_blueprint: 0.85
  duration_target: 0.75
  negative_space: 0.70
slide_patterns:
  structural_blueprint: 0.95
  focus_laser: 0.90
  audience_anchor: 0.85
  negative_space: 0.80
  tone_dial: 0.70
  duration_target: 0.65

# Calibrated (from SPECTRUM data)
# Example: Negative Space more effective than expected for Audio
audio_patterns:
  negative_space: 0.90 → 0.95  # Explicit skip lists dramatically improved focus
```

### Calibration Rules

1. **3+ tasks required** before adjusting pattern effectiveness scores
2. **Max adjustment per cycle**: ±0.15 (prevent overcorrection)
3. **Decay**: Adjustments decay 10% per quarter toward defaults
4. **Override**: User explicit prompt preferences always win

### Format-Audience Fit Calibration

Track optimal format-audience combinations:

| Audience | Best Audio | Best Video | Best Slides | Notes |
|----------|-----------|-----------|------------|-------|
| C-suite | Brief: Executive Summary | Brief: Corporate | Presenter: Internal | Short, actionable |
| Senior Engineers | Deep Dive: Technical | Explainer: Whiteboard | Detailed: Handout | Depth over breadth |
| General Public | Deep Dive: General | Brief: Casual | Presenter: TED-style | Engagement first |
| Students | Lecture: Tutorial | Explainer: Classroom | Detailed: Educational | Building-block structure |
| Researchers | Critique: Research | Explainer: Academic | Detailed: Handout | Evidence-focused |

### Source Composition Calibration

Track which notebook composition patterns produce best results:

| Source Pattern | Best For | Quality Score | Notes |
|---------------|----------|--------------|-------|
| Single Deep | Lecture Mode, Deep Research | High | Focus single topic deeply |
| Multi-Perspective | Debate, Critique | Very High | Tension drives engagement |
| Hierarchical | Lecture, Detailed Deck | High | Natural learning flow |
| Comparative | Infographic, Critique | High | Clear structure for comparison |
| Chronological | Deep Dive, Presenter | Medium-High | Narrative arc strength |

---

## PROPAGATE — Share Validated Patterns

### Journal Entry Format

Record SPECTRUM insights in `.agents/prism.md`:

```markdown
## YYYY-MM-DD - SPECTRUM: [Format × Audience]

**Tasks assessed**: N
**Average quality**: X/5.0
**Key insight**: [description]
**Calibration adjustment**: [pattern/fit: old → new]
**Apply when**: [future scenario]
**reusable**: true

<!-- EVOLUTION_SIGNAL
type: PATTERN
source: Prism
date: YYYY-MM-DD
summary: [prompt design insight]
affects: [Prism, Lore]
priority: MEDIUM
reusable: true
-->
```

### Pattern Library

Build a library of effective prompt design approaches by context:

| Context | Best Format | Key Patterns | Effectiveness |
|---------|-----------|-------------|---------------|
| Technical knowledge sharing | Audio Deep Dive | Audience Anchor + Focus Laser + Negative Space | Very High |
| Executive briefing | Audio Brief | Duration Target + Focus Laser | High |
| Product comparison | Infographic | Structural Blueprint + Focus Laser | High |
| Educational content | Audio Lecture + Detailed Deck | Structural Blueprint + Audience Anchor | High |
| Social media content | Video Brief + Audio Brief | Tone Dial + Duration Target | Medium-High |
| Research analysis | Audio Critique + Deep Research | Audience Anchor + Negative Space | High |

### Quick Calibration (Small Tasks)

For tasks with < 3 prompt designs:

```markdown
## Quick SPECTRUM

**Tasks**: 1 completed
**Quality**: 4.2/5.0
**Note**: Negative Space pattern with explicit skip list improved Audio Deep Dive focus
**Action**: No weight change (insufficient data)
```

Rule: Do not adjust weights from a single small task. Accumulate data across tasks.

---

## Integration with Ecosystem

SPECTRUM data feeds into prompt design decisions:

| SPECTRUM Signal | Ecosystem Impact |
|----------------|-------------------|
| Quality improving steadily | Prompt design approach is working — continue |
| Quality degrading | Re-examine source advice, template selection, format-audience fit |
| Pattern consistently effective | Standardize for similar contexts |
| Format-audience mismatch detected | Update recommendation heuristics |
| Low downstream utilization | Adjust output format, improve handoff quality |
| Validated prompt pattern | Share with Lore, update prompt catalog |

---

## Feedback to Ecosystem

When SPECTRUM discovers patterns valuable beyond a single task:

1. **Record in journal** with `reusable: true` tag
2. **Emit EVOLUTION_SIGNAL** for Lore to collect
3. **Feed to Growth** if content strategy patterns improve engagement
4. **Inform Cast** if audience-format fit data improves persona design
5. **Update prompt catalog** if new template approaches prove more effective
