# Voice - Handoff Templates

## Voice → Retain (Risk Signal)

```markdown
## Voice → Retain Handoff

**Risk Level:** [High | Medium | Low]

**Signals Identified:**
- NPS score dropped from [X] to [Y]
- [N] detractors in the past [period]
- Common complaint: [issue]
- Churn mentions: [N] users said they're considering leaving

**User Segments at Risk:**
- [Segment 1]: [X%] negative sentiment
- [Segment 2]: [X%] negative sentiment

**Key Feedback Themes:**
1. [Theme 1] - [Sample quote]
2. [Theme 2] - [Sample quote]

**Recommended Retention Actions:**
1. [Specific action for at-risk segment]
2. [Specific action for at-risk segment]

Suggested command: `/Retain address churn risk`
```

## Voice → Spark (Feedback Insights)

```markdown
## SPARK_HANDOFF (from Voice)

### User Feedback Insights
- **Top feature requests:** [ranked list]
- **Pain points:** [ranked list]
- **Sentiment trend:** [improving/declining/stable]
- **Sample size:** [N responses]

Suggested command: `/Spark propose feature from feedback`
```

## Voice → Scout (Bug Report)

```
/Scout investigate reported bug
Bug: [description]
Reports: [N] users affected
Severity: [based on sentiment]
User quotes: [representative feedback]
```

## Voice → Roadmap (Feature Request)

```
/Roadmap evaluate feature request
Feature: [name]
Request count: [N]
User segments: [who is asking]
Business impact: [potential value]
```

## Voice → Retain (Churn Intervention)

```
/Retain address churn risk
Context: Voice identified [N] detractors with [common issue].
Risk: [X%] of users mention leaving.
Feedback: [Key themes]
```
