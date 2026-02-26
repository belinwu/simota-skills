# Research Calibration System (DISTILL)

Research method effectiveness tracking, recommendation adoption analysis, insight accuracy validation, and question type evaluation.
Researcher gets better at designing studies and extracting insights by learning from outcomes.

---

## Overview

The DISTILL phase runs post-study (or periodically) to close the feedback loop between research design and actual product impact. Without DISTILL, method selection stays static. With it, Researcher's study designs become progressively more effective and insight-rich.

```
TRACK ──→ ASSESS ──→ REFINE ──→ SHARE
  │           │          │         │
  │ Record   │ Measure  │ Update  │ Share with
  │ study    │ adoption │ method  │ Lore/Echo
  │ designs  │ & accuracy│ weights │
```

---

## TRACK — Record Research Activities

After each study, record:

```yaml
Study: [study-id]
Type: [Interview | Usability Test | Diary Study | Focus Group | Survey Design | Mixed Methods]
Research_Questions: [list]
Methods_Used: [list]
Participants: [count by segment]
Key_Insights:
  - insight: [description]
    confidence: [High/Medium/Low]
    evidence_strength: [strong/moderate/weak]
    actionability: [immediately_actionable | needs_further_research | monitoring_only]
Questions_That_Yielded_Rich_Data: [list]
Questions_That_Fell_Flat: [list]
Bias_Checks_Performed: [list]
Downstream_Handoff: [Echo/Spark/Voice/Canvas/None]
```

### What to Track

| Data Point | Why | Used For |
|-----------|-----|----------|
| Method effectiveness | Which methods yield richest insights per context | Method selection heuristic |
| Question quality | Which question types generate deepest responses | Interview guide improvement |
| Recommendation adoption | What % of recommendations were acted upon | Actionability improvement |
| Insight accuracy | Did identified needs prove real in product? | Confidence calibration |
| Participant segment value | Which segments provide most useful data | Recruitment prioritization |
| Bias detection rate | How often biases were caught and corrected | Protocol improvement |

---

## ASSESS — Measure Research Impact

### Recommendation Adoption Tracking

```
Adoption Rate = Acted Recommendations / Total Recommendations

> 0.70  = High-impact research (maintain approach)
0.40-0.70 = Moderate impact (review actionability framing)
< 0.40  = Low adoption (review recommendation quality, stakeholder alignment)
```

### Assessment Triggers

| Trigger | Check |
|---------|-------|
| Feature shipped based on insight | Insight accuracy |
| Recommendation ignored by team | Actionability, framing quality |
| Persona used by Echo/designers | Persona utility |
| Journey map referenced in planning | Synthesis value |
| Quarterly review | Overall research effectiveness |

### Per-Period Assessment Summary

```markdown
### Research Assessment

| Metric | Value | Trend |
|--------|-------|-------|
| Studies completed | 6 | — |
| Insights generated | 24 | — |
| Recommendations made | 15 | — |
| Adoption rate | 67% (10/15) | ↑ |
| Insight accuracy (validated) | 80% (8/10) | — |
| Persona utilization by Echo | 3/4 active | — |

**Strongest method**: Semi-structured interviews (richest data per session)
**Weakest area**: Survey design recommendations (low adoption)
**Note**: Stakeholder involvement in DEFINE phase improved adoption rate.
```

---

## REFINE — Update Method Selection Heuristics

### Method Effectiveness Scoring

Track which methods work best in which contexts:

```yaml
# Default method effectiveness by context
interview_effectiveness:
  feature_discovery: 0.90
  pain_point_identification: 0.85
  workflow_understanding: 0.80
usability_test_effectiveness:
  interaction_issues: 0.95
  navigation_problems: 0.90
  task_completion_barriers: 0.85
diary_study_effectiveness:
  habitual_behavior: 0.85
  longitudinal_change: 0.80
  context_of_use: 0.75

# Calibrated (from DISTILL data)
# Example: Diary studies unexpectedly effective for feature discovery
diary_study_effectiveness:
  feature_discovery: 0.60 → 0.75  # Participants revealed unmet needs over time
```

### Refinement Rules

1. **3+ studies required** before adjusting method effectiveness scores
2. **Max adjustment per cycle**: ±0.15 (prevent overcorrection)
3. **Decay**: Adjustments decay 10% per quarter toward defaults
4. **Override**: User explicit method preferences always win

### Question Type Calibration

Track which question types produce richest data:

| Question Type | Avg Data Richness | Best For |
|--------------|------------------|----------|
| Descriptive ("Walk me through...") | High | Behavior understanding |
| Contrast ("How does A differ...") | High | Value discovery |
| Evaluative ("How did that feel?") | Medium | Emotion mapping |
| Hypothetical ("If you could...") | Low-Medium | Latent needs (use sparingly) |
| Structural ("What's most important?") | Medium | Priority mapping |

---

## SHARE — Propagate Validated Patterns

### Journal Entry Format

Record DISTILL insights in `.agents/researcher.md`:

```markdown
## YYYY-MM-DD - DISTILL: [Study Type]

**Studies assessed**: N
**Overall adoption rate**: X%
**Key insight**: [description]
**Calibration adjustment**: [method/question: old → new]
**Apply when**: [future scenario]
**reusable**: true

<!-- EVOLUTION_SIGNAL
type: PATTERN
source: Researcher
date: YYYY-MM-DD
summary: [research methodology insight]
affects: [Researcher, Echo, Spark, Voice]
priority: MEDIUM
reusable: true
-->
```

### Pattern Library

Build a library of effective research approaches by context:

| Context | Best Method | Sample Size | Key Questions | Reliability |
|---------|------------|-------------|---------------|-------------|
| New feature validation | Interview + Usability | 5-8 + 5 | Behavior-based + Task scenarios | High |
| Pain point discovery | Interview | 8-12 | Descriptive + Evaluative | High |
| Workflow optimization | Contextual inquiry | 5-8 | Observation + Probing | High |
| Market fit assessment | Mixed (Interview + Survey) | 8 + 100+ | Contrast + Structural | Medium |
| Onboarding friction | Usability test | 5-6 | Task scenarios + Think-aloud | High |
| Long-term behavior | Diary study | 10-15 | Daily prompts + Reflective | Medium |

### Quick Calibration (Small Studies)

For studies with < 3 insights:

```markdown
## Quick DISTILL

**Studies**: 1 completed
**Insights**: 2 (too few to calibrate)
**Note**: Persona was immediately adopted by Echo
**Action**: No weight change (insufficient data)
```

Rule: Do not adjust weights from a single small study. Accumulate data across studies.

---

## Integration with Ecosystem

DISTILL data feeds into research design decisions:

| DISTILL Signal | Ecosystem Impact |
|---------------|-----------------|
| Research accuracy improving | Confidence in user insights increases |
| Accuracy degrading | Re-examine methods, recruitment, bias checks |
| Method consistently underperforming | Deprioritize, try alternatives |
| High adoption rate | Research approach is working — continue |
| Low downstream utilization | Adjust output format, improve handoff quality |
| Validated user pattern | Share with Echo for persona updates, Spark for ideation |

---

## Feedback to Ecosystem

When DISTILL discovers patterns valuable beyond a single study:

1. **Record in journal** with `reusable: true` tag
2. **Emit EVOLUTION_SIGNAL** for Lore to collect
3. **Feed to Echo** if pattern affects persona models
4. **Inform Spark** if recurring unmet needs are discovered
5. **Update bias checklists** if new bias patterns are identified
