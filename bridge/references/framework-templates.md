# Bridge Framework Templates

Templates for each phase of the Clarify → Align → Guard → Document framework.

---

## Requirement Clarification Template

```markdown
## Requirement Clarification

### Original Request
> [Quote the original requirement as stated]

### My Understanding
[Translate into concrete, testable statements]

### Hidden Assumptions
| # | Assumption | Risk if Wrong | Validation Needed |
|---|------------|---------------|-------------------|
| 1 | [Assumption] | [Impact] | [How to validate] |

### Open Questions
| # | Question | Stakeholder | Priority |
|---|----------|-------------|----------|
| 1 | [Question] | [Who can answer] | High/Med/Low |

### Technical Implications
| Aspect | Impact | Trade-off |
|--------|--------|-----------|
| Performance | [Description] | [Options] |
| Security | [Description] | [Options] |
| UX | [Description] | [Options] |

### Acceptance Criteria (Draft)
- [ ] [Concrete, testable criterion 1]
- [ ] [Concrete, testable criterion 2]
- [ ] [Concrete, testable criterion 3]

### Recommended Next Steps
1. [Action item with owner]
2. [Action item with owner]
```

---

## Scope Change Assessment Template

```markdown
## Scope Change Assessment

### Change Request
> [What is being requested]

### Original Scope
> [What was originally agreed]

### Gap Analysis
| Aspect | Original | Requested | Delta |
|--------|----------|-----------|-------|
| Features | [Count] | [Count] | +[N] |
| Effort estimate | [Time] | [Time] | +[Time] |
| Risk level | [Level] | [Level] | [Change] |

### Impact Assessment
- **Schedule:** [Impact description]
- **Resources:** [Impact description]
- **Quality:** [Impact description]
- **Dependencies:** [Impact description]

### Recommendation
- [ ] Approve as-is (if impact is acceptable)
- [ ] Approve with conditions: [conditions]
- [ ] Defer to next phase
- [ ] Reject (reason: [reason])

### Required Approvals
- [ ] Product Owner
- [ ] Tech Lead
- [ ] [Other stakeholder]
```

---

## Trade-off Presentation Template

```markdown
## Trade-off Analysis: [Decision Title]

### Context
[Why this trade-off is necessary]

### Options

| Option | Pros | Cons | Effort | Risk |
|--------|------|------|--------|------|
| A: [Name] | [Benefits] | [Drawbacks] | [Est.] | [Level] |
| B: [Name] | [Benefits] | [Drawbacks] | [Est.] | [Level] |
| C: [Name] | [Benefits] | [Drawbacks] | [Est.] | [Level] |

### Business Impact Matrix

| Factor | Option A | Option B | Option C |
|--------|----------|----------|----------|
| Time to market | [Fast/Med/Slow] | | |
| User experience | [Better/Same/Worse] | | |
| Maintenance cost | [Low/Med/High] | | |
| Future flexibility | [High/Med/Low] | | |

### Recommendation
**Option [X]** because [clear business reasoning]

### What we're accepting
- [Explicit acknowledgment of trade-off 1]
- [Explicit acknowledgment of trade-off 2]
```

---

## Decision Narrative Structure

For major technical decisions, present as a story. See also `references/decision-narratives.md` for comprehensive examples.

```markdown
## [Decision Title]

### Before (The Problem)
[Opening: "We had X problem..."]
- What pain exists today
- Who is affected and how

### Decision (The Solution)
[Decision: "So we decided to..."]
- What we're doing
- Why this approach

### After (The Outcome)
[Outcome: "This enables..."]
- Expected business benefits
- Measurable improvements

### Risks & Mitigations
[Risk: "However, X risk exists, addressed by..."]
- What could go wrong
- How we're protecting against it
```

**Japanese phrase patterns:**
- Before: 「〜という課題がありました」
- Decision: 「そこで〜することにしました」
- After: 「これにより〜が実現できます」
- Risks: 「ただし〜のリスクがありますが、〜で対応します」

---

## Alignment Meeting Facilitation Template

```markdown
## Alignment Session Agenda

### 1. Current State (5 min)
- What do we have today?
- What works? What doesn't?

### 2. Desired State (10 min)
- What does success look like?
- For business? For users? For engineering?

### 3. Gap Analysis (10 min)
- Where are we misaligned?
- What assumptions differ?

### 4. Trade-off Discussion (15 min)
- What can we have? What must we sacrifice?
- Present options, not ultimatums

### 5. Agreement (5 min)
- What exactly are we committing to?
- What is explicitly OUT of scope?

### 6. Next Steps (5 min)
- Who does what by when?
- When do we check in again?
```

---

## Decision Log Entry Template

```markdown
## Decision: [Title]

**Date:** YYYY-MM-DD
**Stakeholders:** [Who was involved]
**Status:** Decided | Pending | Revisited

### Context
[Why this decision was needed]

### Options Considered
1. **[Option A]:** [Brief description]
2. **[Option B]:** [Brief description]
3. **[Option C]:** [Brief description]

### Decision
**Chose: [Option X]**

### Rationale
[Why this option was selected over others]

### Consequences
- **Accepted:** [What we're explicitly accepting]
- **Deferred:** [What we're pushing to later]
- **Rejected:** [What we're explicitly not doing]

### Review Trigger
[When should this decision be revisited?]
```
