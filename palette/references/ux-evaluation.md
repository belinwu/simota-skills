# UX Evaluation Reference

## Heuristic Evaluation Output Format

```markdown
### UX Heuristic Evaluation: [Component/Flow Name]

| # | Heuristic | Score | Issues | Priority |
|---|-----------|-------|--------|----------|
| 1 | Visibility of System Status | X/5 | [specific issue] | High/Med/Low |
| 2 | Match User's Mental Model | X/5 | [specific issue] | High/Med/Low |
| 3 | User Control & Freedom | X/5 | [specific issue] | High/Med/Low |
| 4 | Consistency & Standards | X/5 | [specific issue] | High/Med/Low |
| 5 | Error Prevention | X/5 | [specific issue] | High/Med/Low |
| 6 | Recognition over Recall | X/5 | [specific issue] | High/Med/Low |
| 7 | Flexibility & Efficiency | X/5 | [specific issue] | High/Med/Low |
| 8 | Minimalist Design | X/5 | [specific issue] | High/Med/Low |
| 9 | Error Recovery | X/5 | [specific issue] | High/Med/Low |
| 10 | Contextual Help | X/5 | [specific issue] | High/Med/Low |

**Overall Score**: X.X/5
**Critical Areas**: #X, #X (scores ≤ 2)
**Quick Wins**: [low-effort, high-impact improvements]
```

---

## Score Definitions

| Score | Rating | Description |
|-------|--------|-------------|
| 5 | Excellent | Best practices fully implemented, delightful experience |
| 4 | Good | Mostly appropriate, minor room for improvement |
| 3 | Acceptable | Meets basics but improvement recommended |
| 2 | Poor | Clear problems exist, improvement needed |
| 1 | Critical | Severe issues, immediate action required |

### Priority Guidelines

```
High Priority: Score 1-2, affects critical user flows
Medium Priority: Score 3, noticeable friction but workaround exists
Low Priority: Score 4, polish improvements
```

---

## UX Metrics

### Core Metrics

| Metric | Definition | Target | How to Measure |
|--------|------------|--------|----------------|
| Task Success Rate | % of users completing target task | >95% critical flows | Analytics / User testing |
| Time on Task | Time from start to completion | Varies by complexity | Timestamp tracking |
| Error Rate | % of tasks with errors encountered | <5% common flows | Error event tracking |
| Abandonment Rate | % of users leaving mid-task | <10% critical flows | Funnel analysis |

### System Usability Scale (SUS) - Quick Version

Rate each statement 1-5 (1=Strongly Disagree, 5=Strongly Agree):

1. I can complete my task without help
2. The interface feels consistent
3. Error messages help me fix problems
4. I always know what's happening
5. I can undo mistakes easily

**SUS Score**: (sum × 4) = ___/100

| Range | Interpretation |
|-------|---------------|
| 80+ | Excellent |
| 68-79 | Good |
| 51-67 | Needs improvement |
| <51 | Poor |

### Measurement Guidelines

**Before implementing:** Identify applicable metrics → Establish baseline → Define expected improvement

**After implementing:** Describe expected metric impact in PR → Suggest validation method (manual test / analytics)

---

## Before/After Template

```markdown
### UX Improvement: [Title]

#### Before
**Problem**: [Describe user friction in plain language]
**Evidence**: [Where this happens - file:line or user flow]
\`\`\`tsx
// Current problematic code
\`\`\`

#### After
**Solution**: [What changes and why it helps]
**Benefit**: [Expected user experience improvement]
\`\`\`tsx
// Improved code
\`\`\`

#### Impact Assessment

| Metric | Before | After (Expected) |
|--------|--------|------------------|
| Task completion | X% | Y% |
| Error rate | X% | <Y% |
| User confidence | Low/Med/High | Low/Med/High |

#### Heuristics Improved
- [#X: Heuristic name] - from X/5 to Y/5

#### Implementation
- **Files**: [list of files to change]
- **Effort**: S / M / L
- **Risk**: Low / Medium / High
```
