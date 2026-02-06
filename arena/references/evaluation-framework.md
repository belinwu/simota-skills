# Evaluation Framework

Quality metrics, scoring methodology, and comparison report templates for variant evaluation.

---

## Variant Scoring Matrix

| Criterion | Weight | Score (1-5) | Weighted | Description |
|-----------|--------|-------------|----------|-------------|
| Correctness | 40% | | | Meets specification requirements completely |
| Code Quality | 25% | | | Readability, maintainability, idiomatic patterns |
| Performance | 15% | | | Efficiency, resource usage, scalability |
| Safety | 15% | | | Error handling, input validation, security |
| Simplicity | 5% | | | Avoids over-engineering, minimal complexity |
| **Total** | 100% | | | |

### Score Definitions

| Score | Label | Meaning |
|-------|-------|---------|
| 5 | Excellent | Exceeds requirements, best-in-class |
| 4 | Good | Meets all requirements with minor room for improvement |
| 3 | Adequate | Meets core requirements, some gaps |
| 2 | Below Average | Partial implementation, notable issues |
| 1 | Poor | Fails to meet requirements |

### Weight Adjustment Guidelines

Default weights work for most scenarios. Adjust when:

| Scenario | Adjustment |
|----------|------------|
| Security-critical code | Safety: 30%, Code Quality: 20% |
| Performance-sensitive path | Performance: 30%, Simplicity: 0% |
| Prototype / exploration | Simplicity: 15%, Performance: 5% |
| Legacy codebase integration | Code Quality: 35%, Correctness: 30% |

---

## Comparison Report Template

```markdown
## Arena Comparison Report

### Run Information
- Run ID: [ID]
- Spec: [Spec file/description]
- Engines: [List of engines used]
- Variants Generated: [N]
- Date: [YYYY-MM-DD]

### Variant Summaries

#### Variant A (Engine: [engine])
- Approach: [Brief description of implementation strategy]
- Strengths: [Key advantages]
- Weaknesses: [Key disadvantages]
- Score: [X.XX/5.00]

#### Variant B (Engine: [engine])
- Approach: [Brief description of implementation strategy]
- Strengths: [Key advantages]
- Weaknesses: [Key disadvantages]
- Score: [X.XX/5.00]

### Head-to-Head Comparison

| Aspect | Variant A | Variant B | Winner |
|--------|-----------|-----------|--------|
| Correctness | [score] | [score] | [A/B/Tie] |
| Code Quality | [score] | [score] | [A/B/Tie] |
| Performance | [score] | [score] | [A/B/Tie] |
| Safety | [score] | [score] | [A/B/Tie] |
| Simplicity | [score] | [score] | [A/B/Tie] |
| **Weighted Total** | **[total]** | **[total]** | **[Winner]** |

### Selection Decision
- **Selected:** Variant [X]
- **Rationale:** [Why this variant won - focus on decisive factors]
- **Trade-offs Accepted:** [What was sacrificed and why it's acceptable]
- **Dissenting Strengths:** [What the losing variant did better - preserve for future reference]

### Cost Report
- Total Cost: [Amount]
- Cost per Variant: [Breakdown by variant]
- Cost per Engine: [Breakdown by engine if multi-engine]
- Cost Efficiency: [Value assessment - was the comparison worth the cost?]
```

---

## Quick Evaluation (for AUTORUN mode)

When time is constrained, use this abbreviated format:

```markdown
## Quick Eval: [Run ID]
| Variant | Correct | Quality | Perf | Safety | Simple | Total |
|---------|---------|---------|------|--------|--------|-------|
| A | [1-5] | [1-5] | [1-5] | [1-5] | [1-5] | [X.XX] |
| B | [1-5] | [1-5] | [1-5] | [1-5] | [1-5] | [X.XX] |

**Winner:** Variant [X] ([one-line rationale])
**Cost:** [Total]
```

---

## Evaluation Anti-Patterns

Avoid these common evaluation mistakes:

| Anti-Pattern | Problem | Correction |
|--------------|---------|------------|
| **Recency bias** | Favoring the last variant reviewed | Score each criterion independently, then compare |
| **Halo effect** | One strong criterion overshadowing weaknesses | Apply weighted scoring strictly |
| **Complexity worship** | Preferring "clever" over "clear" | Simplicity criterion exists for a reason |
| **Sunk cost** | Favoring variant from expensive engine | Judge output, not input cost |
| **Feature creep** | Rewarding variants that add unrequested features | Score against spec, not beyond it |

---

## Tie-Breaking Rules

When variants score within 0.2 points of each other:

1. **Correctness wins** - If one is more correct, it wins regardless of total
2. **Simplicity wins** - Among equally correct variants, prefer simpler
3. **Safety wins** - If security is relevant, prefer safer
4. **Cost wins** - If all else equal, prefer cheaper engine
5. **Escalate** - If truly indistinguishable, present both to user with trade-offs
