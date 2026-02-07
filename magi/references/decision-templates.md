# Decision Templates

Output format templates and sample deliberations for Magi's verdict delivery.

---

## Full Deliberation Report Template

```markdown
# MAGI Deliberation Report

## Decision Request
- **Type**: [Architecture / Trade-off / Go-No-Go / Strategy / Priority]
- **Subject**: [Decision subject]
- **Requestor**: [User / Agent name]
- **Urgency**: [Low / Medium / High / Critical]
- **Reversibility**: [Low / Medium / High]

---

## Context Summary
[2-3 sentences describing the decision context, constraints, and what's at stake]

---

## Three Perspectives

### Logos (Technical Analysis)
**Position**: APPROVE / REJECT / ABSTAIN
**Confidence**: [0-100]

[2-4 sentences of technical analysis]

**Key Evidence:**
- [Evidence point 1]
- [Evidence point 2]

**Technical Risks:**
- [Risk 1 with probability estimate]

---

### Pathos (Human Impact)
**Position**: APPROVE / REJECT / ABSTAIN
**Confidence**: [0-100]

[2-4 sentences of human impact analysis]

**Key Concerns:**
- [User/team impact 1]
- [User/team impact 2]

**Maintainability Assessment:**
- [Long-term human cost evaluation]

---

### Sophia (Strategic Assessment)
**Position**: APPROVE / REJECT / ABSTAIN
**Confidence**: [0-100]

[2-4 sentences of strategic analysis]

**Business Alignment:**
- [Business impact 1]
- [Business impact 2]

**ROI Assessment:**
- [Return on investment evaluation]

---

## Vote Summary

| Perspective | Position | Confidence | Key Rationale |
|-------------|----------|------------|---------------|
| Logos | [APPROVE/REJECT/ABSTAIN] | [0-100] | [One-line summary] |
| Pathos | [APPROVE/REJECT/ABSTAIN] | [0-100] | [One-line summary] |
| Sophia | [APPROVE/REJECT/ABSTAIN] | [0-100] | [One-line summary] |

**Consensus**: [3-0 / 2-1 / 1-1-1 / 0-3]
**Weighted Confidence**: [Score]

---

## Verdict

[VERDICT_DISPLAY - see Verdict Presentation section below]

**Decision**: [The decision in one clear sentence]
**Action**: [What to do next]

---

## Risk Register

| # | Risk | Source | Severity | Mitigation | Monitor |
|---|------|--------|----------|------------|---------|
| 1 | [Risk] | [Perspective] | [H/M/L] | [Mitigation] | [Indicator] |
| 2 | [Risk] | [Perspective] | [H/M/L] | [Mitigation] | [Indicator] |

---

## Dissent Record
[Only if 2-1 or overridden]

**Dissenting Perspective**: [Name]
**Position**: [APPROVE/REJECT]
**Concern**: [Key concern]
**Mitigation**: [How majority addresses this]
**Vindication Trigger**: [What would prove the dissenter right]

---

## Decision Audit Trail
- **Deliberation ID**: [MAGI-YYYY-MMDD-NNN]
- **Date**: [YYYY-MM-DD]
- **Domain**: [Architecture / Trade-off / Go-No-Go / Strategy / Priority]
- **Consensus Pattern**: [3-0 / 2-1 / 1-1-1 / 0-3]
- **Re-deliberations**: [0 / 1 / 2]
- **User Override**: [Yes/No]
```

---

## Verdict Presentation (Special Effects)

The verdict presentation changes based on the consensus pattern, using dramatic ASCII art.

### 3-0: Unanimous Approval

```
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                   M A G I   S Y S T E M                      ║
    ║                                                              ║
    ║           ┌─────────┐  ┌─────────┐  ┌─────────┐             ║
    ║           │  LOGOS  │  │ PATHOS  │  │ SOPHIA  │             ║
    ║           │  ██████ │  │  ██████ │  │  ██████ │             ║
    ║           │ APPROVE │  │ APPROVE │  │ APPROVE │             ║
    ║           └─────────┘  └─────────┘  └─────────┘             ║
    ║                                                              ║
    ║        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░             ║
    ║        ░  ALL SYSTEMS GREEN — UNANIMOUS APPROVAL ░           ║
    ║        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░             ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
```

### 2-1: Majority Decision

```
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                   M A G I   S Y S T E M                      ║
    ║                                                              ║
    ║           ┌─────────┐  ┌─────────┐  ┌─────────┐             ║
    ║           │  LOGOS  │  │ PATHOS  │  │ SOPHIA  │             ║
    ║           │  ██████ │  │  ░░░░░░ │  │  ██████ │             ║
    ║           │ APPROVE │  │ REJECT  │  │ APPROVE │             ║
    ║           └─────────┘  └─────────┘  └─────────┘             ║
    ║                                                              ║
    ║        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓             ║
    ║        ▓  MAJORITY RULE — 2:1 — DISSENT LOGGED  ▓           ║
    ║        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓             ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
```

### 1-1-1: Split Decision

```
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                   M A G I   S Y S T E M                      ║
    ║                                                              ║
    ║           ┌─────────┐  ┌─────────┐  ┌─────────┐             ║
    ║           │  LOGOS  │  │ PATHOS  │  │ SOPHIA  │             ║
    ║           │  ▒▒▒▒▒▒ │  │  ░░░░░░ │  │  ▓▓▓▓▓▓ │             ║
    ║           │ APPROVE │  │ REJECT  │  │ ABSTAIN │             ║
    ║           └─────────┘  └─────────┘  └─────────┘             ║
    ║                                                              ║
    ║        ░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓             ║
    ║        ░  DEADLOCK — HUMAN JUDGMENT REQUIRED    ▓           ║
    ║        ▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░             ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
```

### 0-3: Unanimous Rejection

```
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                   M A G I   S Y S T E M                      ║
    ║                                                              ║
    ║           ┌─────────┐  ┌─────────┐  ┌─────────┐             ║
    ║           │  LOGOS  │  │ PATHOS  │  │ SOPHIA  │             ║
    ║           │  ░░░░░░ │  │  ░░░░░░ │  │  ░░░░░░ │             ║
    ║           │ REJECT  │  │ REJECT  │  │ REJECT  │             ║
    ║           └─────────┘  └─────────┘  └─────────┘             ║
    ║                                                              ║
    ║        ████████████████████████████████████████████           ║
    ║        █  PROPOSAL DENIED — ALL SYSTEMS REJECT   █           ║
    ║        ████████████████████████████████████████████           ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
```

### Dynamic Elements

The verdict display should be customized per decision:
- Replace `APPROVE`/`REJECT` with each perspective's actual vote
- Replace the status bar text with a one-line summary of the decision
- Use `██████` (solid) for APPROVE, `░░░░░░` (light) for REJECT, `▒▒▒▒▒▒` (medium) for ABSTAIN, `▓▓▓▓▓▓` (dark) for CONDITIONAL

---

## Compact Report Template (AUTORUN Mode)

```markdown
## MAGI Verdict: [Subject]

| Perspective | Vote | Conf | Rationale |
|-------------|------|------|-----------|
| Logos | [A/R/AB] | [N] | [One line] |
| Pathos | [A/R/AB] | [N] | [One line] |
| Sophia | [A/R/AB] | [N] | [One line] |

**Consensus**: [Pattern] | **Confidence**: [Score] | **Decision**: [One sentence]

[VERDICT_DISPLAY ASCII art]

**Risks**: [Key risk] → [Mitigation]
**Next**: [Recommended action/agent]
```

---

## Sample Deliberations

### Sample 1: Architecture — Monolith vs Microservices

**Context:** 5-person team building an e-commerce platform. Current traffic: 1K DAU. Expected growth: 10K DAU in 12 months.

**Logos (Confidence: 78):** APPROVE monolith. Current scale doesn't justify distributed system complexity. Network latency, data consistency, and deployment overhead of microservices outweigh benefits. Monolith can handle 10K DAU easily. Extract services when specific bottlenecks are identified.

**Pathos (Confidence: 85):** APPROVE monolith. Team of 5 cannot effectively maintain service boundaries, separate deployments, and distributed debugging. Microservices would create cognitive overload and on-call burden. Monolith allows the team to focus on product value.

**Sophia (Confidence: 72):** APPROVE monolith. Time-to-market is 3 months faster. Microservices add operational cost (infrastructure, monitoring) without current business justification. Revisit at 50K DAU or when team grows to 15+.

**Verdict:** 3-0 UNANIMOUS APPROVAL — Monolith with future extraction plan

---

### Sample 2: Trade-off — Performance vs Readability

**Context:** API endpoint response time can be reduced from 200ms to 160ms with optimized code, but the optimized version uses bitwise operations and custom memory pooling.

**Logos (Confidence: 82):** REJECT optimization. 40ms improvement is within SLA. Optimized code has higher defect probability. Premature optimization. Benchmark when latency actually becomes a problem.

**Pathos (Confidence: 88):** REJECT optimization. Optimized code requires deep systems knowledge to maintain. Team has 2 junior developers. Bug rate will increase. Readable version enables faster feature development.

**Sophia (Confidence: 75):** REJECT optimization. 40ms doesn't impact conversion rates or user satisfaction metrics. Developer time is better spent on features. Optimize only when P99 latency exceeds SLA.

**Verdict:** 0-3 UNANIMOUS REJECTION — Keep readable implementation

---

### Sample 3: Go/No-Go — v2.0 Release

**Context:** Major version release with new payment system. 94% test pass rate, 2 medium bugs, no criticals. Migration guide 60% complete.

**Logos (Confidence: 80):** APPROVE (GO). Test coverage adequate, no critical issues. 2 medium bugs are edge cases with known workarounds. Payment system passed integration tests.

**Pathos (Confidence: 73):** CONDITIONAL (HOLD 2 days). Migration guide is incomplete — users will struggle. Support team hasn't been briefed on new payment flows. Launching without documentation creates frustration.

**Sophia (Confidence: 70):** APPROVE (GO WITH CONDITIONS). Competitor launches next week. 2-day delay acceptable, 1-week delay is not. Ship with conditions: complete migration guide and support briefing within 48 hours.

**Verdict:** 2-1 MAJORITY — GO WITH CONDITIONS (Pathos dissent recorded)

---

### Sample 4: Strategy — Build vs Buy (Auth System)

**Context:** Need authentication for SaaS product. Team has no security specialist. Budget: $500/month for SaaS tools.

**Logos (Confidence: 85):** APPROVE buy. Authentication is a solved problem with high security stakes. Building introduces CVE risk. Auth0/Clerk provide battle-tested implementations with compliance certifications.

**Pathos (Confidence: 80):** APPROVE buy. Team lacks security expertise — building auth creates anxiety and maintenance burden. Third-party auth lets the team focus on core product value. Better developer experience.

**Sophia (Confidence: 77):** APPROVE buy. Build cost: 3 developer-months (~$45K). Auth0 cost: $300/month ($3.6K/year). Break-even at 12+ years. Faster to market by 2 months. Clear ROI.

**Verdict:** 3-0 UNANIMOUS APPROVAL — Buy authentication service

---

### Sample 5: Priority — Security vs Feature vs Tech Debt

**Context:** Sprint planning with 3 competing items. Team capacity: 2 developers, 2 weeks.

**Security vulnerability (CVE-2024-XXXX):** Logos: 10, Pathos: 8, Sophia: 9
**Customer-requested feature:** Logos: 4, Pathos: 7, Sophia: 8
**Database migration (perf improvement):** Logos: 7, Pathos: 3, Sophia: 5

**Verdict:** UNANIMOUS — Priority: Security → Feature → Database migration

---

## Risk Register Template

```markdown
## Risk Register — [Decision ID]

| # | Risk | Source | Likelihood | Impact | Severity | Mitigation | Owner | Monitor | Status |
|---|------|--------|-----------|--------|----------|------------|-------|---------|--------|
| 1 | [Risk description] | [Logos/Pathos/Sophia] | [H/M/L] | [H/M/L] | [Critical/High/Med/Low] | [Action] | [Who] | [Metric] | [Open/Mitigated/Accepted] |

### Monitoring Schedule
- **Weekly**: [What to check weekly]
- **Monthly**: [What to check monthly]
- **Trigger-based**: [What triggers immediate review]
```

---

## Decision Log Template

For maintaining a record of all Magi decisions:

```markdown
## Decision Log

| ID | Date | Domain | Subject | Consensus | Confidence | Decision | Status |
|----|------|--------|---------|-----------|------------|----------|--------|
| MAGI-001 | YYYY-MM-DD | [Type] | [Subject] | [3-0/2-1/etc] | [Score] | [Brief] | [Active/Superseded/Revoked] |
```
