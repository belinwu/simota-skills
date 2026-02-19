# Decision Narratives: Technical Decisions as Business Stories

This document provides templates for presenting technical decisions as compelling narratives that business stakeholders can understand and support.

---

## Why Narratives Work

> **"People don't remember facts. They remember stories."**

Technical decisions are often presented as feature lists or architecture diagrams. But stakeholders remember and support decisions when they understand the journey:
- What problem existed
- Why we chose this solution
- What we expect to achieve
- How we'll handle risks

---

## The Core Narrative Structure

Every technical decision narrative follows this arc:

```
┌─────────────────────────────────────────────────────────┐
│  BEFORE          DECISION         AFTER                 │
│                                                         │
│  "We had a       "So we          "This enables         │
│   problem"   →    decided"    →   the benefit"         │
│       │             │             │                     │
│       ↓             ↓             ↓                     │
│   Pain Point    Solution     Benefit                    │
│   + Risk        + Rationale  + Measurement             │
└─────────────────────────────────────────────────────────┘
```

**Japanese phrase patterns:**
- Before: 「〜という課題がありました」
- Decision: 「そこで〜することにしました」
- After: 「これにより〜が実現できます」

---

## Part 1: Main Narrative Template

### Complete Decision Narrative

```markdown
# [Decision Title]: [One-line summary]

## Before (Background)
### Problem Statement
[Opening phrase, e.g., "We had X problem..."]

**Specific problems:**
- [Problem 1]: [Business impact]
- [Problem 2]: [Business impact]
- [Problem 3]: [Business impact]

**Affected stakeholders:**
- [Stakeholder 1]: [How they are affected]
- [Stakeholder 2]: [How they are affected]

...
```

---

## Part 2: Narrative Variations

### Quick Decision Narrative (1 page)

For smaller decisions or busy stakeholders.

```markdown
## [Decision Title]

### Summary
[1-2 sentences explaining the decision]

### Before → After
| Aspect | Before | After |
|--------|--------|-------|
| [Aspect 1] | [Current state] | [Improved state] |
| [Aspect 2] | [Current state] | [Improved state] |

### Why this decision
[3 points or fewer explaining rationale]

### Risk and mitigation
...
```

---

### Problem-Focused Narrative

When the problem needs emphasis.

```markdown
## [Problem Statement]

### Current situation
[Specific problem description]

### Business impact
- **Revenue**: [Impact]
- **Customer satisfaction**: [Impact]
- **Operating cost**: [Impact]
- **Risk**: [Impact]

### If left unaddressed
[Projection for 3 months, 6 months, 1 year]

### Proposed solution
...
```

---

### Solution-Focused Narrative

When the solution is innovative or exciting.

```markdown
## [Solution Name]: A New Approach

### What becomes possible
[Business outcomes first]

### Background problem
[Brief problem description]

### How the solution works
[Visual explanation]

### Success stories from others
[Similar success cases if available]

### Application to our company
...
```

---

### Risk-Focused Narrative

When risk mitigation is the primary driver.

```markdown
## Risk Response: [Risk Name]

### Current risk situation
**Identified risk:**
[Specific risk description]

**Scope of impact:**
- Affected systems: [List]
- Affected operations: [List]
- Potential loss: [Amount or impact]

### If risk materializes
[Worst-case scenario]

### Proposed countermeasure
...
```

---

## Part 3: Narrative Elements Library

### Opening Hooks

| Type | English Pattern | Japanese Sample |
|------|-----------------|-----------------|
| Problem-driven | "X problem causes Y loss monthly" | 「〇〇という問題で、毎月△△万円のロスが発生しています」 |
| Opportunity-driven | "Achieving X would improve Y by Z%" | 「〇〇を実現できれば、△△%の効率改善が見込めます」 |
| Risk-driven | "Without action, X risk is increasing" | 「現状のままでは、〇〇のリスクが高まっています」 |
| Competition-driven | "Competitors have already adopted X" | 「競合他社は既に〇〇を導入しています」 |
| Customer-driven | "Customer requests for X are increasing" | 「お客様から〇〇の要望が増えています」 |
| Regulation-driven | "X regulation compliance is required" | 「〇〇の法規制対応が必要になりました」 |

---

### Problem Description Patterns

| Pattern | English Pattern | Japanese Sample |
|---------|-----------------|-----------------|
| Frequency | "X problem occurs Y times per week" | 「週に〇回、△△という問題が発生しています」 |
| Cost | "This problem costs X per month" | 「この問題により、月間〇〇万円のコストがかかっています」 |
| Time waste | "Staff spend X hours daily on Y" | 「担当者が毎日〇時間を△△に費やしています」 |
| Customer impact | "X% of customers are affected by Y" | 「お客様の〇〇%が△△で困っています」 |
| Risk exposure | "If X occurs, Y loss is expected" | 「〇〇が発生した場合、△△の損失が見込まれます」 |
| Opportunity cost | "Inability to do X causes Y missed opportunity" | 「〇〇ができないことで、△△の機会を逃しています」 |

---

### Decision Rationale Patterns

| Reason Type | English Pattern | Japanese Sample |
|-------------|-----------------|-----------------|
| Cost-benefit | "Investment X yields Y benefit" | 「投資〇〇に対し、〇〇の効果が見込めます」 |
| Risk reduction | "Reduces X risk by Y%" | 「〇〇のリスクを△△%低減できます」 |
| Speed improvement | "Reduces X time from Y to Z" | 「〇〇の時間を△△から□□に短縮できます」 |
| Quality improvement | "Improves error rate from X% to Y%" | 「エラー率を〇〇%から△△%に改善できます」 |
| Scalability | "Enables support for up to X" | 「将来〇〇まで対応可能になります」 |
| Competitive advantage | "Gains advantage over competitors in X" | 「競合他社より△△で優位に立てます」 |
| Compliance | "Ensures compliance with X regulation" | 「〇〇規制への準拠を確保できます」 |

---

### Trade-off Acknowledgment Patterns

| Pattern | English Pattern | Japanese Sample |
|---------|-----------------|-----------------|
| Cost trade-off | "Initial investment X required, but recovered by Y" | 「初期投資は〇〇必要ですが、△△で回収できます」 |
| Time trade-off | "Takes X months to implement, but then Y benefit" | 「導入に〇ヶ月かかりますが、その後は△△の効果があります」 |
| Complexity trade-off | "Operations become complex, but X benefit" | 「運用は複雑になりますが、△△のメリットがあります」 |
| Flexibility trade-off | "Creates dependency on X, but gains Y benefit" | 「〇〇に依存しますが、△△の恩恵を受けられます」 |
| Short vs Long term | "Short-term X, but long-term Y" | 「短期的には〇〇ですが、長期的には△△です」 |

---

### Risk Mitigation Patterns

| Pattern | English Pattern | Japanese Sample |
|---------|-----------------|-----------------|
| Rollback plan | "If problems occur, can revert with X" | 「問題が発生した場合、〇〇で元に戻せます」 |
| Phased approach | "Phased rollout with validation at each phase" | 「段階的に導入し、各フェーズで検証します」 |
| Pilot testing | "Pilot test in X first, then validate" | 「まず〇〇で試験導入し、効果を確認します」 |
| Fallback option | "Worst case, respond with X" | 「最悪の場合は〇〇で対応します」 |
| Monitoring | "Monitor X to detect problems early" | 「〇〇を監視し、問題を早期発見します」 |

---

### Closing Call-to-Action Patterns

| Type | English Pattern | Japanese Sample |
|------|-----------------|-----------------|
| Approval request | "May we proceed with the above?" | 「以上の内容で進めてよろしいでしょうか」 |
| Resource request | "X is required. Please approve." | 「実施には〇〇が必要です。ご承認をお願いします」 |
| Priority request | "Please prioritize X" | 「〇〇を優先課題として取り組ませてください」 |
| Timeline request | "Decision by X enables start by Y" | 「〇月までに判断をいただければ、△月に開始できます」 |
| Feedback request | "Please share your thoughts on this direction" | 「この方向性についてご意見をお聞かせください」 |

---

## Part 4: Real-World Examples

### Example 1: Infrastructure Migration

```markdown
# Cloud Migration: Infrastructure Modernization

## Before (Background)
### Problem Statement
"Aging on-premise servers were increasing failure risk and operating costs."

**Specific problems:**
- 3 unplanned downtimes per year (average 4 hours each)
- Hardware maintenance costs increasing annually (20% YoY)
- New environment setup takes 2 weeks

**Affected stakeholders:**
- Customers: Lost opportunities due to service outages
- Development team: Wait time for environment preparation
- Operations team: Late-night and weekend emergency response
...
```

---

### Example 2: Security Enhancement

```markdown
# Security Enhancement: Authentication System Refresh

## Before (Background)
### Problem Statement
"Password-only authentication was increasing unauthorized access risk."

**Specific problems:**
- Industry-wide password breach incidents increasing
- Regulatory bodies recommending multi-factor authentication
- Competitors have already implemented

**Risk if left unaddressed:**
- Data breach damages: Estimated hundreds of millions of yen
- Brand damage: Customer churn

...
```

---

## Part 5: Presentation Tips

### The 3-30-3 Rule

- **3 seconds**: Title and one-line summary must hook attention
- **30 seconds**: Executive summary must convey the essence
- **3 minutes**: Full story for those who want details

### Emotional vs Logical Balance

| Audience | Lead With | Support With |
|----------|-----------|--------------|
| Executive | Business impact | Technical feasibility |
| Finance | ROI & cost | Risk mitigation |
| Operations | Stability & reliability | Implementation details |
| Engineering | Technical merit | Business justification |

### Visual Aids

Always include:
- Before/After comparison (table or diagram)
- Timeline with milestones
- Risk matrix (if applicable)
- One simple diagram of the solution

### Anticipate Questions

Prepare answers for:
1. "Why now?"
2. "What if we don't do this?"
3. "What's the worst case?"
4. "Who else has done this?"
5. "What do you need from us?"
