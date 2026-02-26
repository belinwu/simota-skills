# Mediation Calibration System (MEDIATE)

Translation quality tracking, decision persistence analysis, scope creep detection rate, and alignment success measurement.
Bridge gets better at mediating between business and technical stakeholders by learning from outcomes.

---

## Overview

The MEDIATE phase runs post-engagement (or periodically) to close the feedback loop between mediation activities and actual project outcomes. Without MEDIATE, translation patterns stay static. With it, Bridge's mediation becomes progressively more effective at preventing costly misalignments.

```
RECORD ──→ EVALUATE ──→ CALIBRATE ──→ PROPAGATE
  │            │            │            │
  │ Log       │ Measure    │ Update    │ Share with
  │ sessions  │ persistence│ patterns  │ Lore/Scribe
  │ & decisions│ & success  │ & heuristics│
```

---

## RECORD — Log Mediation Activities

After each mediation engagement, record:

```yaml
Engagement: [engagement-id]
Type: [Requirement Clarification | Scope Guard | Trade-off Mediation | Stakeholder Alignment | Feasibility Assessment | Decision Facilitation]
Stakeholders: [list with roles]
Assumptions_Surfaced: [count]
Scope_Changes_Detected: [count]
Decisions_Logged: [count]
Translation_Challenges:
  - concept: [technical concept]
    difficulty: [High/Medium/Low]
    analogy_used: [description]
    understood: [yes/no/partial]
Alignment_Achieved: [full/partial/none]
Downstream_Handoff: [Scribe/Sherpa/Atlas/Canvas/Builder/None]
```

### What to Track

| Data Point | Why | Used For |
|-----------|-----|----------|
| Translation quality | Which analogies and framings work best | Translation pattern improvement |
| Decision persistence | Do decisions stick or get re-opened? | Decision documentation quality |
| Scope creep detection rate | How much creep is caught vs slipping through? | Detection heuristic tuning |
| Alignment success | Are misalignments resolved before becoming costly? | Process improvement |
| Assumption accuracy | Were surfaced assumptions validated correctly? | Assumption library building |
| Handoff completeness | Did downstream agents have all needed context? | Handoff quality improvement |

---

## EVALUATE — Measure Mediation Impact

### Decision Persistence Tracking

```
Persistence Rate = Decisions Still Standing / Total Decisions Made

> 0.85  = Strong mediation (decisions well-documented and understood)
0.65-0.85 = Good, some decisions being revisited
< 0.65  = Weak persistence (review documentation quality, stakeholder buy-in)
```

### Evaluation Triggers

| Trigger | Check |
|---------|-------|
| Decision revisited by stakeholder | Decision persistence, documentation quality |
| Scope creep detected late | Detection heuristic effectiveness |
| Requirement misunderstanding discovered | Translation quality |
| Handoff agent requests clarification | Handoff completeness |
| Quarterly review | Overall mediation effectiveness |

### Per-Period Evaluation Summary

```markdown
### Mediation Evaluation

| Metric | Value | Trend |
|--------|-------|-------|
| Engagements completed | 10 | — |
| Assumptions surfaced | 32 | — |
| Scope changes caught | 8 | — |
| Decisions logged | 15 | — |
| Decision persistence rate | 87% (13/15) | ↑ |
| Translation success rate | 90% | — |
| Alignment success rate | 80% (8/10) | — |

**Strongest area**: Scope creep detection (all major changes caught)
**Weakest area**: Feasibility translation (technical constraints hard to convey)
**Note**: Using concrete business analogies improved translation success by 20%.
```

---

## CALIBRATE — Update Mediation Patterns

### Translation Effectiveness Scoring

Track which translation approaches work best in which contexts:

```yaml
# Default translation effectiveness by audience
analogy_effectiveness:
  executive_audience: 0.90
  pm_audience: 0.85
  sales_audience: 0.80
quantitative_framing:
  executive_audience: 0.85
  pm_audience: 0.75
  sales_audience: 0.90
before_after_comparison:
  all_audiences: 0.85

# Calibrated (from MEDIATE data)
# Example: Quantitative framing more effective with PMs than expected
quantitative_framing:
  pm_audience: 0.75 → 0.85  # PMs responded well to metric-based explanations
```

### Calibration Rules

1. **3+ engagements required** before adjusting effectiveness scores
2. **Max adjustment per cycle**: ±0.15 (prevent overcorrection)
3. **Decay**: Adjustments decay 10% per quarter toward defaults
4. **Override**: User explicit communication preferences always win

### Scope Detection Calibration

Track which signals predict actual scope creep:

| Signal | Detection Rate | False Positive Rate | Reliability |
|--------|---------------|---------------------|-------------|
| "While we're at it..." | 75% | 20% | Medium |
| "Can we also add..." | 90% | 10% | High |
| "This should include..." (post-agreement) | 95% | 5% | Very High |
| Implicit feature expansion | 60% | 30% | Medium |
| "Users will expect..." (no data) | 70% | 25% | Medium |

---

## PROPAGATE — Share Validated Patterns

### Journal Entry Format

Record MEDIATE insights in `.agents/bridge.md`:

```markdown
## YYYY-MM-DD - MEDIATE: [Engagement Type]

**Engagements assessed**: N
**Decision persistence**: X%
**Key insight**: [description]
**Calibration adjustment**: [pattern/signal: old → new]
**Apply when**: [future scenario]
**reusable**: true

<!-- EVOLUTION_SIGNAL
type: PATTERN
source: Bridge
date: YYYY-MM-DD
summary: [mediation insight]
affects: [Bridge, Scribe, Sherpa]
priority: MEDIUM
reusable: true
-->
```

### Pattern Library

Build a library of effective mediation approaches by context:

| Context | Best Approach | Key Technique | Success Rate |
|---------|--------------|---------------|-------------|
| Vague requirements | Decomposition Pattern | Assumption Ladder + Open Questions | High |
| Priority conflicts | Priority Stack | Forced ranking, no ties | High |
| Timeline disagreements | Phased Release | MVP definition + Phase gates | High |
| Technical constraint explanation | Business Analogy | Concrete analogies + Before/After | Medium-High |
| Scope creep in progress | Scope Fence | Impact Ripple + Change control | High |
| Feasibility mismatch | Bronze/Silver/Gold levels | Graduated options with clear trade-offs | Medium |

### Quick Calibration (Small Engagements)

For engagements with < 3 decisions:

```markdown
## Quick MEDIATE

**Engagements**: 1 completed
**Decisions**: 2 (too few to calibrate)
**Note**: Trade-off Triangle was immediately effective with PM
**Action**: No weight change (insufficient data)
```

Rule: Do not adjust weights from a single small engagement. Accumulate data across engagements.

---

## Integration with Ecosystem

MEDIATE data feeds into mediation decisions:

| MEDIATE Signal | Ecosystem Impact |
|---------------|-----------------|
| Translation quality improving | Confidence in stakeholder alignment increases |
| Quality degrading | Re-examine analogies, framing approaches |
| Decisions frequently revisited | Improve documentation quality, strengthen buy-in process |
| High scope detection rate | Detection approach is working — continue |
| Low handoff completeness | Adjust handoff format, add more context |
| Validated mediation pattern | Share with Lore, update Scribe templates |

---

## Feedback to Ecosystem

When MEDIATE discovers patterns valuable beyond a single engagement:

1. **Record in journal** with `reusable: true` tag
2. **Emit EVOLUTION_SIGNAL** for Lore to collect
3. **Feed to Scribe** if pattern affects specification quality
4. **Inform Sherpa** if scope detection patterns improve decomposition
5. **Update anti-patterns** if new communication failure modes are identified
