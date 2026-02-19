# Spark Experiment Lifecycle Reference

A/Bテスト結果に基づく提案イテレーションのガイド。

---

## Result → Decision Matrix

テスト結果に基づく意思決定フレームワーク。

### Decision Matrix

| Verdict | Primary Metric | Guardrail | Decision | Next Action |
|---------|----------------|-----------|----------|-------------|
| **VALIDATED** | Significant positive | No regression | **Ship** | Proceed to implementation |
| **INVALIDATED** | Significant negative OR No effect | - | **Kill or Pivot** | Archive or pivot hypothesis |
| **INCONCLUSIVE** | Not significant | - | **Extend or Iterate** | More data or modified test |
| **GUARDRAIL_VIOLATED** | Positive | Significant negative | **Kill** | Cannot ship, analyze tradeoffs |

### Detailed Verdict Definitions

```markdown
## VALIDATED
- Primary metric shows statistically significant improvement (p < 0.05)
- Effect size meets or exceeds MDE (Minimum Detectable Effect)
- No guardrail metrics significantly regressed
- Decision: SHIP

## INVALIDATED
- Primary metric shows significant negative effect, OR
- Primary metric shows no meaningful change after adequate sample
- Decision: KILL (archive learnings) or PIVOT (new hypothesis)

## INCONCLUSIVE
- Statistical significance not reached
- Sample size may be insufficient
- Test duration may be too short
...
```

---

## EXPERIMENT_RESULT_TO_SPARK_ITERATION

実験結果を受けてSparkが次のアクションを決定するためのフォーマット。

### Experiment → Spark Result Handoff

```markdown
## EXPERIMENT_TO_SPARK_ITERATION

**Hypothesis ID**: H-[XXX]
**Test Name**: [Test name]
**Duration**: [Start] → [End]
**Sample Size**: Control: [N], Treatment: [N]

**Results Summary**:
| Metric | Control | Treatment | Δ | P-value | Significant? |
|--------|---------|-----------|---|---------|--------------|
| [Primary] | [Val] | [Val] | [±X%] | [p] | [Yes/No] |
| [Secondary] | [Val] | [Val] | [±X%] | [p] | [Yes/No] |
| [Guardrail] | [Val] | [Val] | [±X%] | [p] | [Regressed?] |

**Statistical Confidence**: [90% / 95% / 99%]
...
```

### Spark Iteration Response

```markdown
## SPARK_ITERATION_RESPONSE

**Hypothesis ID**: H-[XXX]
**Original Proposal**: [Link to original proposal]
**Experiment Verdict**: [VALIDATED/INVALIDATED/INCONCLUSIVE/GUARDRAIL_VIOLATED]

**Decision**: [SHIP / ITERATE / PIVOT / KILL / EXTEND]

**Rationale**:
[Explanation based on results]

**Next Steps**:
[ ] [Specific action based on decision]
[ ] [Specific action based on decision]

...
```

---

## Inconclusive結果の対応フロー

統計的有意性に達しなかった場合の対応ガイド。

### Inconclusive Analysis Checklist

```markdown
## Inconclusive Result Analysis

**Test Details**:
- Actual sample size: [N] vs Required: [N]
- Actual duration: [X days] vs Planned: [Y days]
- Traffic allocation: [X%]

**Possible Causes**:
- [ ] Insufficient sample size
- [ ] Test duration too short
- [ ] Effect size smaller than expected
- [ ] High variance in data
- [ ] Implementation issues
- [ ] Seasonal/external factors

...
```

### Inconclusive Decision Tree

```
Inconclusive Result
        │
        ├── Trend matches hypothesis?
        │   │
        │   ├── Yes → Calculate required sample size
        │   │          │
        │   │          ├── Achievable in 2 weeks? → EXTEND
        │   │          │
        │   │          └── Not achievable? → Evaluate:
        │   │                    │
        │   │                    ├── Effect too small to matter → KILL
        │   │                    │
        │   │                    └── Strategic importance high → ITERATE (amplify effect)
        │   │
        │   └── No clear trend →
...
```

---

## Hypothesis Pivot Patterns

仮説を軌道修正するパターン。

### Pivot Type Matrix

| Pivot Type | When to Use | Example |
|------------|-------------|---------|
| **Scope Pivot** | Feature too broad/narrow | "All users" → "Power users only" |
| **Mechanism Pivot** | Right problem, wrong solution | Modal → Inline notification |
| **Metric Pivot** | Wrong success measure | Clicks → Time on page |
| **Timing Pivot** | Wrong moment in journey | Homepage → Post-signup |
| **Channel Pivot** | Wrong touchpoint | In-app → Email |

### Pivot Documentation Template

```markdown
## HYPOTHESIS_PIVOT

**Original Hypothesis**: H-[XXX]
**New Hypothesis**: H-[XXX]-pivot or H-[YYY]

**Pivot Type**: [Scope/Mechanism/Metric/Timing/Channel]

**Original Statement**:
- We believed: [Original assumption]
- For: [Original target]
- Would achieve: [Original outcome]
- Measured by: [Original metric]

**Learnings from Test**:
- What worked: [Positive findings]
...
```

---

## Sample Size Recalculation

テスト延長・再設計時のサンプルサイズ再計算ガイド。

### When to Recalculate

- Observed effect smaller than expected MDE
- Variance higher than anticipated
- Confidence level requirements changed
- Test showed inconclusive results

### Recalculation Inputs

```markdown
## Sample Size Recalculation

**Original Assumptions**:
- Baseline conversion: [X%]
- Expected MDE: [Y%]
- Confidence level: [90%/95%/99%]
- Power: [80%/90%]
- Original sample needed: [N]

**Observed Reality**:
- Actual baseline: [X%] (vs expected [Y%])
- Observed effect: [Z%] (vs expected MDE [Y%])
- Observed variance: [Higher/Lower/Same]

**Recalculated Requirements**:
...
```

### Quick Reference: Sample Size Formula

```
n = (Zα/2 + Zβ)² × 2 × p × (1-p) / δ²

Where:
- n = sample size per group
- Zα/2 = Z-score for confidence (1.96 for 95%)
- Zβ = Z-score for power (0.84 for 80%)
- p = baseline conversion rate
- δ = minimum detectable effect (absolute)
```

---

## Guardrail Metric Violations対応

ガードレールメトリクス違反時の対応ガイド。

### Guardrail Violation Severity

| Guardrail Type | Violation Severity | Typical Action |
|----------------|-------------------|----------------|
| Revenue | Critical | Always kill |
| User Experience (NPS, CSAT) | High | Kill unless strategic |
| Performance (latency, errors) | High | Kill or fix before ship |
| Engagement (secondary) | Medium | Evaluate tradeoff |
| Operational (cost, support tickets) | Medium | Evaluate tradeoff |

### Violation Analysis Template

```markdown
## GUARDRAIL_VIOLATION_ANALYSIS

**Hypothesis**: H-[XXX]
**Violated Guardrail**: [Metric name]
**Primary Metric Result**: [+X% improvement, p=Y]

**Violation Details**:
- Guardrail metric: [Name]
- Control value: [X]
- Treatment value: [Y]
- Change: [±Z%]
- P-value: [p]
- Threshold: [Acceptable regression limit]

**Impact Assessment**:
...
```

---

## Iteration Tracking

複数イテレーションを追跡するテンプレート。

### Hypothesis Evolution Log

```markdown
## Hypothesis Evolution: [Feature Area]

### H-001 (Original)
- Statement: [Original hypothesis]
- Test dates: [Start - End]
- Result: INCONCLUSIVE
- Learning: [Key insight]

### H-001-v2 (Iteration)
- Changes: [What changed from v1]
- Statement: [Updated hypothesis]
- Test dates: [Start - End]
- Result: INVALIDATED
- Learning: [Key insight]

...
```

### Iteration Velocity Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| Iterations to validation | Number of test cycles | < 3 |
| Time to decision | Days from first test to final decision | < 30 days |
| Learning quality | Actionable insights per iteration | > 2 |
| Pivot success rate | % of pivots that lead to validation | > 30% |

---

## Integration with Other Patterns

### Experiment Lifecycle × Other Patterns

| Result | Related Pattern | Integration |
|--------|-----------------|-------------|
| VALIDATED | Pattern F: Implementation Handoff | Proceed to Sherpa |
| INVALIDATED | Pattern D: Competitive | Check if competitors have solution |
| INCONCLUSIVE | Pattern A: Echo Validation | Get qualitative user feedback |
| GUARDRAIL_VIOLATED | Pattern H: Security Review | Check if security concern caused it |

### Post-Experiment Handoff

```markdown
## POST_EXPERIMENT_HANDOFF

**Hypothesis**: H-[XXX]
**Final Verdict**: [SHIP / KILL / PIVOT]

**If SHIP → Pattern F Handoff**:
- Use SPARK_TO_SHERPA_HANDOFF format
- Include: Test results as evidence
- Priority: [Based on effect size]

**If KILL → Documentation**:
- Archive in: `.agents/spark-experiments.md`
- Key learnings: [List]
- Related hypotheses affected: [List]

...
```
