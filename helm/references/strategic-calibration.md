# Strategic Calibration System (FORESIGHT)

Prediction accuracy tracking, framework effectiveness scoring, assumption validation, and scenario quality measurement.
Helm gets better at strategic simulation by learning from outcomes.

---

## Overview

The FORESIGHT phase runs post-engagement (or periodically) to close the feedback loop between strategic simulations and actual business outcomes. Without FORESIGHT, framework selection stays static and scenario parameters remain uncalibrated. With it, Helm's simulations become progressively more accurate and actionable.

```
TRACK ──→ VALIDATE ──→ CALIBRATE ──→ PROPAGATE
  │            │            │            │
  │ Record    │ Check     │ Update    │ Share with
  │ simulations│ predictions│ framework │ Lore/Compass
  │ & predictions│ vs actual │ weights  │
```

---

## TRACK — Record Simulation Activities

After each simulation engagement, record:

```yaml
Simulation: [simulation-id]
Type: [SWOT | PESTLE | Porter | BCG | BSC | Ansoff | Full Strategy | KPI Forecast | M&A Evaluation | Crisis Response]
Horizon: [SHORT(0-1yr) | MID(1-3yr) | LONG(3-10yr)]
Frameworks_Applied: [list]
Scenarios_Generated: [count]
Key_Predictions:
  - prediction: [description]
    metric: [measurable KPI]
    baseline_value: [current]
    predicted_value: [target]
    confidence: [High/Medium/Low]
    timeframe: [validation date]
Assumptions_Used:
  - assumption: [description]
    source: [data/industry_default/estimate]
    sensitivity: [High/Medium/Low]
Data_Completeness: [Tier 1 only | Tier 1+2 | Tier 1+2+3 | Full]
Downstream_Handoff: [Magi/Scribe/Sherpa/Canvas/Compass/None]
```

### What to Track

| Data Point | Why | Used For |
|-----------|-----|----------|
| Prediction accuracy | Core calibration input | Scenario parameter adjustment |
| Framework effectiveness | Which frameworks yield best insights per context | Framework selection heuristic |
| Assumption accuracy | Were industry defaults/estimates valid? | Assumption library improvement |
| Scenario quality | Did the 3 scenarios bracket actual outcomes? | Scenario range calibration |
| Data completeness impact | Does more data actually improve accuracy? | Input requirement prioritization |
| Downstream utilization | Did Magi/Scribe/Sherpa use the output? | Output format improvement |

---

## VALIDATE — Check Predictions Against Outcomes

### Prediction Accuracy Tracking

```
Accuracy = Predictions Within ±15% of Actual / Total Validated Predictions

> 0.75  = Strong forecasting (maintain approach)
0.50-0.75 = Moderate accuracy (review assumptions, scenario parameters)
< 0.50  = Weak predictions (review methodology, data sources)
```

### Scenario Bracketing Quality

```
Bracket Rate = Actuals Falling Within Optimistic-Pessimistic Range / Total Scenarios

> 0.85  = Well-calibrated scenarios
0.70-0.85 = Good, some outliers
< 0.70  = Scenarios too narrow or biased (widen range or review drivers)
```

### Validation Triggers

| Trigger | Check |
|---------|-------|
| Quarterly KPI results available | Short-term prediction accuracy |
| Annual financial results | Mid-term prediction accuracy |
| Industry report published | Long-term trend prediction |
| Compass detects strategy drift | Assumption validity |
| M&A/Exit outcome known | Valuation accuracy |

### Per-Period Validation Summary

```markdown
### Strategic Validation

| Metric | Value | Trend |
|--------|-------|-------|
| Simulations completed | 8 | — |
| Predictions made | 15 | — |
| Predictions validated | 10 | — |
| Accuracy rate (±15%) | 70% (7/10) | ↑ |
| Scenario bracket rate | 80% (8/10) | — |
| Framework combinations used | 5 | — |
| Downstream utilization | 88% (7/8) | — |

**Strongest framework**: PESTLE→SWOT→Porter combo (highest insight yield)
**Weakest area**: Long-term pricing predictions (40% accuracy)
**Note**: Tier 2 data (KPI from Pulse) improved short-term accuracy by 25%.
```

---

## CALIBRATE — Update Strategic Heuristics

### Framework Effectiveness Scoring

Track which frameworks work best in which contexts:

```yaml
# Default framework effectiveness by context
swot_effectiveness:
  overall_assessment: 0.85
  startup_strategy: 0.80
  m_and_a: 0.75
pestle_effectiveness:
  market_entry: 0.90
  long_term_planning: 0.85
  crisis_response: 0.70
porter_effectiveness:
  industry_analysis: 0.90
  competitive_positioning: 0.85
  pricing_strategy: 0.75
bcg_effectiveness:
  portfolio_management: 0.90
  investment_allocation: 0.85
  product_strategy: 0.80

# Calibrated (from FORESIGHT data)
# Example: BSC unexpectedly effective for startup strategy
bsc_effectiveness:
  startup_strategy: 0.65 → 0.80  # KPI-driven approach resonated with founders
```

### Calibration Rules

1. **3+ simulations required** before adjusting framework effectiveness scores
2. **Max adjustment per cycle**: ±0.15 (prevent overcorrection)
3. **Decay**: Adjustments decay 10% per quarter toward defaults
4. **Override**: User explicit framework preferences always win

### Scenario Parameter Calibration

Track whether scenario ranges are well-calibrated:

| Parameter | Default Range | Calibrated Range | Adjustment Basis |
|-----------|--------------|-----------------|-----------------|
| Optimistic uplift | +20~40% | +25~35% | Actuals rarely exceeded +35% |
| Pessimistic downside | -20~40% | -25~45% | Severe downturns underestimated |
| Short-term confidence | ±10% | ±8% | Short-term more predictable |
| Long-term confidence | ±30% | ±35% | Long-term less predictable |

### Assumption Default Calibration

Track accuracy of industry default values used when data is missing:

| Assumption | Default Value | Actual Range Observed | Reliability |
|-----------|--------------|---------------------|-------------|
| SaaS churn rate | 1-2%/mo | 0.8-3.5%/mo | Medium |
| SaaS gross margin | 70-80% | 65-85% | High |
| Japan IT market growth | 3-5%/yr | 2-7%/yr | Medium |
| CAC Payback (B2B SaaS) | 12-18mo | 8-24mo | Medium |
| LTV/CAC target | 3:1+ | 2.5:1-5:1 | High |

---

## PROPAGATE — Share Validated Patterns

### Journal Entry Format

Record FORESIGHT insights in `.agents/helm.md`:

```markdown
## YYYY-MM-DD - FORESIGHT: [Simulation Type]

**Simulations assessed**: N
**Overall accuracy**: X%
**Key insight**: [description]
**Calibration adjustment**: [framework/parameter: old → new]
**Apply when**: [future scenario]
**reusable**: true

<!-- EVOLUTION_SIGNAL
type: PATTERN
source: Helm
date: YYYY-MM-DD
summary: [strategic insight]
affects: [Helm, Compass, Magi]
priority: MEDIUM
reusable: true
-->
```

### Pattern Library

Build a library of effective strategic approaches by context:

| Context | Best Framework Combo | Key Parameters | Accuracy |
|---------|---------------------|---------------|----------|
| Annual strategy | PESTLE→SWOT→Porter→Ansoff | Full Tier 1+2 data | High |
| M&A evaluation | Porter→SWOT→BCG→Financial | Tier 1+2+3C data | Medium-High |
| New market entry | PESTLE→Porter→Ansoff→Blue Ocean | Market research critical | Medium |
| Crisis response | SWOT→ST-3 pattern | Speed over depth | High |
| KPI forecasting | ST-1/ST-2 patterns | Tier 2A data essential | High |
| Long-term vision | Blue Ocean→PESTLE→BSC | Low certainty, wide scenarios | Medium |

### Quick Calibration (Small Engagements)

For engagements with < 3 predictions:

```markdown
## Quick FORESIGHT

**Simulations**: 1 completed
**Predictions**: 2 (too few to calibrate)
**Note**: PESTLE→SWOT combo provided clear strategic direction
**Action**: No weight change (insufficient data)
```

Rule: Do not adjust weights from a single small engagement. Accumulate data across engagements.

---

## Integration with Ecosystem

FORESIGHT data feeds into strategic simulation decisions:

| FORESIGHT Signal | Ecosystem Impact |
|-----------------|-----------------|
| Prediction accuracy improving | Confidence in strategic recommendations increases |
| Accuracy degrading | Re-examine frameworks, data sources, assumptions |
| Framework consistently underperforming | Deprioritize, try alternative combinations |
| Scenario brackets too narrow | Widen optimistic/pessimistic ranges |
| High downstream utilization | Output approach is working — continue |
| Low utilization by Magi | Adjust output format for decision-readiness |
| Validated strategic pattern | Share with Compass for monitoring, Lore for knowledge |

---

## Feedback to Ecosystem

When FORESIGHT discovers patterns valuable beyond a single engagement:

1. **Record in journal** with `reusable: true` tag
2. **Emit EVOLUTION_SIGNAL** for Lore to collect
3. **Feed to Compass** if prediction accuracy data improves monitoring thresholds
4. **Inform Magi** if framework effectiveness data improves decision quality
5. **Update assumption defaults** if industry benchmarks prove inaccurate
