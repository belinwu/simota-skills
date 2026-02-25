# Execution Learning System (CALIBRATE)

Estimation calibration, pattern recognition, adaptive complexity multipliers, and velocity prediction.
Sherpa gets better at planning over time by learning from actual execution data.

---

## Overview

The CALIBRATE phase runs post-session (or post-Epic) to close the feedback loop between planning and execution. Without calibration, estimates remain static guesses. With it, Sherpa's guidance becomes progressively more accurate.

```
RECORD ──→ COMPARE ──→ ADJUST ──→ PERSIST
  │            │           │          │
  │ Capture    │ Actual    │ Update   │ Store in
  │ actual     │ vs Est    │ factors  │ journal
  │ times      │ analysis  │          │
```

---

## RECORD — Capture Execution Data

After each step completion, record:

```yaml
Step: [name]
Estimated: [minutes]
Actual: [minutes]
Size: [XS/S/M/L]
Complexity_Factors: [list applied]
Risk_Level: [Low/Medium/High]
Agent: [who executed]
Domain: [frontend/backend/infra/test/docs]
Outcome: [clean/rework/blocked]
Notes: [any observations]
```

### What to Track

| Data Point | Why | Used For |
|-----------|-----|----------|
| Estimated vs Actual time | Core calibration input | Multiplier adjustment |
| Step size accuracy | T-shirt sizing calibration | Better initial estimates |
| Complexity factor hits | Which factors actually applied | Factor weight tuning |
| Domain patterns | Recurring effort by area | Pattern library |
| Blocker frequency | Common blockers by type | Risk prediction |
| Agent effectiveness | Which agents complete steps fastest | Better agent suggestions |

---

## COMPARE — Analyze Accuracy

### Per-Step Accuracy

```
Accuracy Ratio = Estimated / Actual

> 1.2  = Overestimated (padded too much)
0.8-1.2 = Good estimate (within 20%)
< 0.8  = Underestimated (missed complexity)
```

### Session-Level Metrics

```markdown
### Calibration Report

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Steps completed | 8 | - |
| Avg accuracy ratio | 0.85 | Slight underestimation |
| Overestimates | 2/8 (25%) | Padding on simple tasks |
| Underestimates | 3/8 (38%) | Missing complexity in API tasks |
| Good estimates | 3/8 (38%) | Baseline accuracy |

**Pattern**: API integration steps consistently underestimated by 30%.
**Action**: Add 1.3x multiplier for API steps in this project.
```

### Trend Detection

Track accuracy over multiple sessions:

| Session | Avg Ratio | Trend | Notes |
|---------|-----------|-------|-------|
| Session 1 | 0.72 | - | First time, many unknowns |
| Session 2 | 0.85 | Improving | Applied calibration |
| Session 3 | 0.95 | Good | Stabilizing |
| Session 4 | 0.92 | Stable | Within target range |

**Target**: Maintain average accuracy ratio between 0.85-1.15 across sessions.

---

## ADJUST — Update Factors

### Adaptive Complexity Multipliers

Base multipliers (from `task-breakdown.md`) can be adjusted per-project:

```yaml
# Default multipliers
new_technology: 1.5x
unclear_requirements: 1.5x
external_dependency: 2.0x
high_risk: 1.5x
multiple_files: 1.3x

# Project-specific adjustments (from calibration)
# Format: factor: base → adjusted (reason)
api_integration: 1.0x → 1.3x  # consistently underestimated
css_styling: 1.0x → 0.8x      # team is fast at styling
test_writing: 1.0x → 1.2x     # testing standards are strict
```

### Adjustment Rules

1. **3+ data points required** before adjusting a multiplier
2. **Max adjustment per session**: ±0.3x (prevent overcorrection)
3. **Decay**: Adjustments decay 10% per month toward default (prevents stale calibration)
4. **Override**: User can explicitly set multipliers (overrides calibration)

---

## PERSIST — Store Calibration Data

### Journal Entry Format

Record calibration insights in `.agents/sherpa.md`:

```markdown
## YYYY-MM-DD - Calibration: [Project/Epic Name]

**Sessions analyzed**: N
**Overall accuracy**: X.XX
**Key adjustments**:
- [factor]: [old] → [new] (reason)

**Pattern discovered**: [description]
**Apply when**: [future scenario]
**reusable**: true

<!-- EVOLUTION_SIGNAL
type: PATTERN
source: Sherpa
date: YYYY-MM-DD
summary: [calibration insight]
affects: [Sherpa, relevant agents]
priority: MEDIUM
reusable: true
-->
```

### Pattern Library

Build a library of recurring task patterns with calibrated estimates:

| Pattern | Typical Steps | Typical Duration | Common Risks | Calibration Notes |
|---------|--------------|------------------|-------------|-------------------|
| New API endpoint | 5-7 | 60-90 min | External deps | Add 1.3x for first endpoint |
| UI component | 4-6 | 45-75 min | Design drift | Stable after 2nd iteration |
| Bug fix | 3-5 | 30-60 min | Root cause clarity | Scout first saves 40% time |
| Refactor | 4-8 | 60-120 min | Scope creep | Strict scope prevents 2x blowup |
| Test suite | 3-6 | 40-80 min | Flaky dependencies | Mock early saves rework |
| Config/infra | 2-4 | 20-40 min | Environment diffs | Add 1.5x for new environments |

### Pattern Matching

When decomposing a new Epic, check the pattern library:

```
1. Identify task type (API endpoint, UI component, etc.)
2. Look up pattern in library
3. Apply calibrated estimates (not default)
4. Note confidence level:
   - High: 5+ matching data points
   - Medium: 3-4 matching data points
   - Low: 1-2 matching data points (use with caution)
```

---

## Velocity Prediction

Use calibrated data to predict completion:

```
Predicted Remaining = Σ(remaining steps × calibrated estimate)
Confidence Band = Predicted × [0.8, 1.3] (narrower with more data)

Example:
- 4 steps remaining
- Calibrated estimates: 10m + 15m + 20m + 10m = 55m
- Confidence: 44m - 72m (medium confidence, 8 data points)
```

### Velocity-Based Re-planning

| Current Velocity | Action |
|-----------------|--------|
| > 1.2x estimate | Consider combining small steps, maintain momentum |
| 0.8-1.2x | On track, no adjustment needed |
| 0.5-0.8x | Break remaining steps smaller, add buffer |
| < 0.5x | Stop and re-plan — something fundamental is wrong |

---

## Integration with Weather System

Calibration data feeds into weather assessment:

| Calibration Signal | Weather Impact |
|-------------------|----------------|
| Accuracy improving | Weather stabilizes (Clear tendency) |
| Accuracy degrading | Weather worsens (Cloudy tendency) |
| New pattern discovered | Short-term uncertainty, long-term improvement |
| Insufficient data | Wider confidence bands, conservative estimates |

---

## Quick Calibration (Short Sessions)

For sessions < 1 hour or < 5 steps:

```markdown
## Quick Calibration

**Steps**: 3 completed
**Avg accuracy**: 0.90 (slightly under)
**Note**: Frontend steps faster than expected
**Action**: No multiplier change (insufficient data)
```

Rule: Do not adjust multipliers from a single short session. Accumulate data across sessions.
