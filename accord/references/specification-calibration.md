# Specification Calibration System (UNIFY)

Template effectiveness tracking, cross-team alignment scoring, section utilization analysis, and specification quality improvement.
Accord gets better at creating unified specifications by learning from outcomes.

---

## Overview

The UNIFY phase runs post-task (or periodically) to close the feedback loop between specification creation and actual cross-team alignment outcomes. Without UNIFY, template selection stays static and audience-writing patterns remain uncalibrated. With it, Accord's specifications become progressively more effective at aligning all three teams.

```
RECORD ──→ EVALUATE ──→ CALIBRATE ──→ PROPAGATE
  │            │            │            │
  │ Log       │ Measure    │ Update    │ Share with
  │ specs &   │ alignment  │ template  │ Lore
  │ outcomes  │ & usage    │ weights   │
```

---

## RECORD — Log Specification Activities

After each specification task, record:

```yaml
Spec: [spec-id]
Scope: [Full | Standard | Lite]
Feature_Complexity: [High | Medium | Low]
Teams_Involved: [Biz+Dev+Design | Biz+Dev | Dev+Design | Biz+Design | Single]
Requirements_Count: [total REQ IDs]
BDD_Scenarios_Count: [total AC IDs]
Sections_Used:
  L0: [yes/no]
  L1: [yes/no]
  L2_Biz: [yes/no]
  L2_Dev: [yes/no]
  L2_Design: [yes/no]
  L3: [yes/no]
Traceability_Completeness: [0-100%]
Cross_Team_Alignment:
  biz_understanding: [High/Medium/Low]
  dev_understanding: [High/Medium/Low]
  design_understanding: [High/Medium/Low]
Revisions_Required: [count]
Downstream_Handoff: [Sherpa/Builder/Radar/Voyager/Canvas/None]
```

### What to Track

| Data Point | Why | Used For |
|-----------|-----|----------|
| Scope × complexity match | Was the right scope selected? | Scope selection heuristic improvement |
| Section utilization | Which L2 sections are most/least used? | Template streamlining |
| Cross-team alignment | Did all teams understand the spec? | Writing pattern improvement |
| Revision frequency | How many rounds before approval? | Initial quality improvement |
| BDD coverage | Are acceptance criteria sufficient? | BDD guidance tuning |
| Downstream adoption | Did Builder/Radar use the spec directly? | Output format improvement |

---

## EVALUATE — Measure Specification Impact

### Cross-Team Alignment Score

```
Alignment = (Biz_Understanding + Dev_Understanding + Design_Understanding) / 3

High (all 3 High)  = Excellent specification (template is working)
Medium (mixed)     = Moderate alignment (review writing patterns, section coverage)
Low (any 1 Low)    = Weak specification (investigate root cause per team)
```

### Scope Accuracy Tracking

```
Scope Accuracy = Specs Where Selected Scope Was Sufficient / Total Specs

> 0.85  = Good scope selection heuristic
0.70-0.85 = Some over/under-scoping
< 0.70  = Review complexity indicators
```

### Evaluation Triggers

| Trigger | Check |
|---------|-------|
| Team requests clarification after spec delivery | Writing clarity, audience fit |
| Spec requires 3+ revisions | Scope selection, section completeness |
| Builder/Radar can't use spec directly | Output format, detail level |
| Feature ships with gaps vs spec | Requirement completeness, BDD coverage |
| Quarterly review | Overall specification effectiveness |

### Per-Period Evaluation Summary

```markdown
### Specification Evaluation

| Metric | Value | Trend |
|--------|-------|-------|
| Specs created | 10 | — |
| Scope accuracy | 80% | ↑ |
| Average alignment score | High | — |
| Average revisions | 1.5 | ↓ |
| BDD coverage (Must REQs) | 95% | ↑ |
| Downstream adoption | 90% | — |
| Traceability completeness | 88% | ↑ |

**Strongest pattern**: Standard scope for 2-team features (100% alignment)
**Weakest area**: L2-Design section (often under-specified)
**Note**: BDD scenarios reduced implementation gaps by 35%.
```

---

## CALIBRATE — Update Specification Heuristics

### Scope Selection Calibration

Track optimal scope per complexity:

```yaml
# Default scope by complexity
scope_selection:
  high_complexity: Full    # 0.90
  medium_complexity: Standard  # 0.85
  low_complexity: Lite     # 0.90

# Calibrated (from UNIFY data)
# Example: Medium complexity with 3 teams benefits from Full
scope_selection:
  medium_complexity_3_teams: Standard → Full  # 3-team projects need more detail
```

### Section Effectiveness Scoring

Track which sections produce the most alignment:

```yaml
section_effectiveness:
  L0_vision: 0.95        # Almost always valuable
  L1_requirements: 0.95  # Core — always needed
  L2_biz: 0.80          # Valuable for stakeholder buy-in
  L2_dev: 0.90          # Essential for implementation
  L2_design: 0.75       # Often under-utilized — improve guidance
  L3_bdd: 0.90          # High impact on shared understanding
  L3_traceability: 0.70 # Often skipped in Standard/Lite — review
```

### Calibration Rules

1. **3+ specs required** before adjusting heuristics
2. **Max adjustment per cycle**: ±0.15 (prevent overcorrection)
3. **Decay**: Adjustments decay 10% per quarter toward defaults
4. **Override**: User explicit preferences always win

### Writing Pattern Calibration

Track which patterns produce best cross-team understanding:

| Pattern | Alignment Impact | Best For |
|---------|-----------------|----------|
| Problem-first L0 (pain → solution) | Very High | All scopes |
| MoSCoW priority in L1 | High | Standard, Full |
| Visual user flow in L2-Design | High | Features with UI |
| Inline code examples in L2-Dev | High | API features |
| Concrete BDD values (not abstract) | Very High | All scopes |
| Glossary for cross-team terms | Medium-High | Full scope |

---

## PROPAGATE — Share Validated Patterns

### Journal Entry Format

Record UNIFY insights in `.agents/accord.md`:

```markdown
## YYYY-MM-DD - UNIFY: [Scope × Teams]

**Specs assessed**: N
**Average alignment**: [High/Medium/Low]
**Key insight**: [description]
**Calibration adjustment**: [scope/pattern: old → new]
**Apply when**: [future scenario]
**reusable**: true

<!-- EVOLUTION_SIGNAL
type: PATTERN
source: Accord
date: YYYY-MM-DD
summary: [specification insight]
affects: [Accord, Scribe, Bridge, Lore]
priority: MEDIUM
reusable: true
-->
```

### Pattern Library

Build a library of effective specification approaches by context:

| Context | Best Scope | Key Sections | Effectiveness |
|---------|-----------|-------------|---------------|
| New product feature (3 teams) | Full | All L2 + complete BDD | Very High |
| API enhancement (Dev + Biz) | Standard | L2-Dev + L2-Biz + BDD | High |
| UI improvement (Design + Dev) | Standard | L2-Design + L2-Dev + BDD | High |
| Bug fix with business impact | Lite | L0 compact + key BDD | High |
| Infrastructure change (Dev only) | Lite | L2-Dev inline + key BDD | Medium-High |
| Cross-team process change | Full | L2-Biz heavy + L3 BDD | High |

### Quick Calibration (Small Tasks)

For tasks with < 3 specs:

```markdown
## Quick UNIFY

**Specs**: 1 completed
**Scope**: Standard
**Note**: L2-Design section improved alignment when Figma links were included inline
**Action**: No weight change (insufficient data)
```

Rule: Do not adjust weights from a single small task. Accumulate data across tasks.

---

## Integration with Ecosystem

UNIFY data feeds into specification decisions:

| UNIFY Signal | Ecosystem Impact |
|-------------|-------------------|
| Alignment improving steadily | Template approach is working — continue |
| Alignment degrading | Re-examine writing patterns, scope selection |
| Section consistently unused | Consider removing from default template |
| High revision count | Improve initial quality, add pre-review checklist |
| Low downstream adoption | Adjust output format, improve handoff quality |
| Validated specification pattern | Share with Lore, update Scribe templates |

---

## Feedback to Ecosystem

When UNIFY discovers patterns valuable beyond a single task:

1. **Record in journal** with `reusable: true` tag
2. **Emit EVOLUTION_SIGNAL** for Lore to collect
3. **Feed to Scribe** if specification patterns improve individual document quality
4. **Inform Bridge** if cross-team language patterns improve translation quality
5. **Update template defaults** if new structural patterns prove more effective
