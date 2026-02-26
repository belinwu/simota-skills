# Intelligence Calibration System (SHARPEN)

Intelligence accuracy tracking, source reliability scoring, prediction validation, and strategic impact measurement.
Compete gets better at competitive analysis by learning from outcomes.

---

## Overview

The SHARPEN phase runs post-analysis (or periodically) to close the feedback loop between competitive intelligence and actual market outcomes. Without SHARPEN, intelligence quality stagnates. With it, Compete's analyses become progressively more accurate and actionable.

```
TRACK ──→ VALIDATE ──→ CALIBRATE ──→ PROPAGATE
  │            │            │            │
  │ Record    │ Check     │ Update    │ Share with
  │ analyses  │ predictions│ source   │ Lore/Helm
  │ & sources │ vs actual  │ weights  │
```

---

## TRACK — Record Intelligence Activities

After each analysis, record:

```yaml
Analysis: [analysis-id]
Type: [SWOT | Feature Matrix | Positioning | Battle Card | Alert Response | Market Trends]
Competitors_Analyzed: [list]
Sources_Used: [list with reliability tier]
Key_Predictions:
  - prediction: [description]
    confidence: [High/Medium/Low]
    timeframe: [when should this be validated]
Actionability: [immediately_actionable | needs_further_research | monitoring_only]
Downstream_Handoff: [Spark/Growth/Helm/None]
```

### What to Track

| Data Point | Why | Used For |
|-----------|-----|----------|
| Prediction accuracy | Core calibration input | Confidence adjustment |
| Source reliability | Which sources produce useful data | Source prioritization |
| Actionability rate | What % of analyses led to action | Focus improvement |
| Handoff effectiveness | Did downstream agents use the output? | Collaboration tuning |
| Alert hit rate | How often alerts were meaningful | Alert threshold tuning |

---

## VALIDATE — Check Predictions

### Prediction Outcome Tracking

```
Accuracy = Correct Predictions / Total Predictions

> 0.80  = Strong analyst (maintain approach)
0.60-0.80 = Good, room for improvement
< 0.60  = Weak predictions (review methodology)
```

### Validation Triggers

| Trigger | Check |
|---------|-------|
| Competitor launches feature we predicted | Prediction accuracy |
| Competitor pricing changes | Price intel accuracy |
| Market trend materializes | Trend prediction accuracy |
| Win/Loss data available | Battle card effectiveness |
| Quarterly review | Overall intelligence quality |

### Per-Period Validation Summary

```markdown
### Validation Report

| Metric | Value | Trend |
|--------|-------|-------|
| Analyses produced | 12 | — |
| Predictions made | 8 | — |
| Predictions validated | 5 | — |
| Accuracy rate | 80% (4/5) | ↑ |
| Actionability rate | 67% (8/12) | — |
| Downstream utilization | 75% (6/8) | — |

**Strongest area**: Feature gap prediction (90% accuracy)
**Weakest area**: Pricing predictions (50% accuracy)
**Note**: More financial data sources needed for pricing analysis.
```

---

## CALIBRATE — Update Intelligence Weights

### Source Reliability Scoring

Track which sources consistently provide accurate and useful intelligence:

```yaml
# Default reliability weights
official_sources: 0.90   # Company website, docs, changelog
review_platforms: 0.75   # G2, Capterra, TrustRadius
financial_data: 0.85     # SEC filings, funding announcements
job_postings: 0.65       # Hiring patterns
community_signals: 0.60  # Reddit, forums, social media

# Calibrated weights (from SHARPEN data)
# Example: Community signals consistently predict features
community_signals: 0.60 → 0.75  # Reddit discussions predicted 3 features
job_postings: 0.65 → 0.70       # Hiring accurately predicted tech stack changes
```

### Calibration Rules

1. **3+ data points required** before adjusting reliability weights
2. **Max adjustment per cycle**: ±0.15 (prevent overcorrection)
3. **Decay**: Adjustments decay 10% per quarter toward defaults
4. **Override**: User explicit source preferences always win

### Confidence Factor Calibration

Track which analysis types have highest/lowest accuracy:

| Analysis Type | Avg Accuracy | Default Confidence |
|--------------|-------------|-------------------|
| Feature Matrix | 85% | High |
| Tech Stack | 90% | High |
| SWOT | 70% | Medium |
| Market Trends | 60% | Medium (wider timeframes) |
| Pricing | 55% | Low (mark speculative) |

---

## PROPAGATE — Share Validated Patterns

### Journal Entry Format

Record SHARPEN insights in `.agents/compete.md`:

```markdown
## YYYY-MM-DD - SHARPEN: [Analysis Type]

**Analyses validated**: N
**Overall accuracy**: X%
**Key insight**: [description]
**Calibration adjustment**: [source/type: old → new]
**Apply when**: [future scenario]
**reusable**: true

<!-- EVOLUTION_SIGNAL
type: PATTERN
source: Compete
date: YYYY-MM-DD
summary: [intelligence insight]
affects: [Compete, Helm, Growth]
priority: MEDIUM
reusable: true
-->
```

### Pattern Library

Build a library of recurring competitive patterns:

| Pattern | Indicators | Typical Timeframe | Reliability |
|---------|-----------|-------------------|-------------|
| Pricing undercut | Price reduction 10%+ | 1-3 months to impact | High |
| Feature convergence | 3+ competitors ship same feature | 6-12 months | Medium |
| Market consolidation | 2+ acquisitions in segment | 12-24 months | Medium |
| Niche expansion | Leader enters adjacent market | 3-6 months to respond | High |
| Talent drain | Key hires moving to competitor | 6-12 months delayed | Low |

### Quick Calibration (Small Analyses)

For analyses with < 3 predictions:

```markdown
## Quick SHARPEN

**Analyses**: 2 completed
**Predictions**: 1 (too few to calibrate)
**Note**: Feature matrix was immediately used by Spark
**Action**: No weight change (insufficient data)
```

Rule: Do not adjust weights from a single small analysis. Accumulate data across analyses.

---

## Integration with Ecosystem

SHARPEN data feeds into strategic decisions:

| SHARPEN Signal | Ecosystem Impact |
|---------------|------------------|
| Intelligence accuracy improving | Confidence in strategic recommendations increases |
| Accuracy degrading | Re-examine sources, methodology |
| Source consistently unreliable | Deprioritize, find alternatives |
| High actionability rate | Intelligence approach is working — continue |
| Low downstream utilization | Adjust output format, improve handoff quality |
| Validated competitive pattern | Share with Helm for strategy simulation |

---

## Feedback to Ecosystem

When SHARPEN discovers patterns valuable beyond a single analysis:

1. **Record in journal** with `reusable: true` tag
2. **Emit EVOLUTION_SIGNAL** for Lore to collect
3. **Feed to Helm** if pattern affects strategic planning
4. **Update alert thresholds** if alert hit rate data suggests adjustment
