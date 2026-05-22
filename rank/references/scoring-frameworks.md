# Scoring Frameworks

**Purpose:** Detailed procedures for each prioritization framework.
**Read when:** Executing CRITERIA or SCORE phases.

> **2026 framing.** The 2026 product-management literature continues to put **RICE** and **WSJF** at the top of "frameworks teams actually use" alongside MoSCoW, Kano, and Value-vs-Effort matrices — the toolkit itself has not changed in 2026, but two operating shifts have:
>
> 1. **AI assistance accelerates *scoring*, not the decision.** Tools like ProductBoard / Productboard AI, Roadmunk, Linear's "AI insights", and ChatGPT / Claude can summarise tickets, surface reach data, and propose ICE / RICE values — but the inputs (impact, confidence) remain a human judgement call. Treat AI-suggested scores as *anchors* in a calibration discussion, not as the score.
> 2. **AI feature work needs an explicit "Confidence ≤ X" guardrail.** Empirical 2026 data on AI features shows higher post-ship variance: only ~`1/3` of shipped features hit their target metric (Kohavi et al., Microsoft), and AI-authored implementations carry the additional risk surface documented in `void/references/over-engineering-anti-patterns.md`. Treat any feature whose `Impact` argument relies on "AI will figure it out" as `Confidence ≤ 50%` until validated.

---

## 1. ICE (Impact × Confidence × Ease)

**Formula:** `ICE Score = Impact × Confidence × Ease`

Each factor scored 1-10:
- **Impact**: How much will this move the target metric? (1=negligible, 10=massive)
- **Confidence**: How sure are we about the impact estimate? (1=guess, 10=data-backed)
- **Ease**: How easy is implementation? (1=months of effort, 10=hours)

**When to use:** Quick triage, early-stage evaluation, limited data available.
**Strengths:** Simple, fast, good for large lists.
**Weaknesses:** Subjective without calibration, no reach component.

---

## 2. RICE (Reach × Impact × Confidence / Effort)

**Formula:** `RICE Score = (Reach × Impact × Confidence) / Effort`

- **Reach**: How many users/events affected per time period? (absolute number)
- **Impact**: How much does it affect each user? (3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal)
- **Confidence**: How sure are we? (100%=high, 80%=medium, 50%=low)
- **Effort**: Person-months of work (absolute estimate)

**When to use:** Product feature prioritization with user data.
**Strengths:** Includes reach, penalizes high-effort items.
**Weaknesses:** Requires user reach data, effort estimation is hard.

---

## 3. WSJF (Weighted Shortest Job First)

**Formula:** `WSJF = Cost of Delay / Job Duration`

**Cost of Delay** = User-Business Value + Time Criticality + Risk Reduction/Opportunity Enablement

Each component scored using modified Fibonacci (1, 2, 3, 5, 8, 13, 20):
- **User-Business Value**: Revenue/satisfaction impact
- **Time Criticality**: How much value decays with delay?
- **Risk Reduction**: Does this reduce future risk or enable other work?
- **Job Duration**: Relative size of the work (same Fibonacci scale)

**When to use:** SAFe/Lean environments, PI planning, time-sensitive decisions.
**Strengths:** Explicitly values time, balances multiple value dimensions.
**Weaknesses:** Requires team calibration on Fibonacci scales.

---

## 4. MoSCoW

**Categories:**
- **Must have**: Non-negotiable for this release. Without it, the release fails.
- **Should have**: Important but not critical. Workaround exists.
- **Could have**: Nice to have. Only if time/resources allow.
- **Won't have (this time)**: Explicitly excluded from this scope.

**Rule of thumb:** Must ≤ 60% of effort, Should ≤ 20%, Could ≤ 20%.

**When to use:** Stakeholder alignment, scope definition, release planning.
**Strengths:** Simple, inclusive, good for non-technical stakeholders.
**Weaknesses:** Binary-ish (no ordering within categories), "Must" inflation.

---

## 5. Cost of Delay (CoD)

**Three profiles:**
- **Standard**: Linear value loss over time. CoD = $/week of delay.
- **Urgent (Fixed Date)**: Deadline-driven. Value drops to zero after date. CoD spikes near deadline.
- **Peak (Time-Sensitive)**: Seasonal or market-window driven. CoD peaks at optimal launch window.

**Calculation:**
```
Weekly CoD = (Expected revenue per week) × (probability of achieving if on time) 
           - (Expected revenue per week) × (probability of achieving if delayed)
```

**When to use:** Economic decision-making, ROI-driven organizations.
**Strengths:** Connects priorities to money, hard to argue against.
**Weaknesses:** Requires revenue/cost data, hard to estimate for infrastructure work.

---

## 6. Kano Model

**Categories:**
- **Must-be (Basic)**: Expected. Absence causes dissatisfaction. Presence doesn't increase satisfaction.
- **One-dimensional (Performance)**: More = better. Linear relationship with satisfaction.
- **Attractive (Delighter)**: Unexpected. Absence doesn't cause dissatisfaction. Presence delights.
- **Indifferent**: Users don't care either way.
- **Reverse**: Presence causes dissatisfaction for some users.

**Classification method:** Pair of questions per feature:
1. "How do you feel if this feature IS present?" (functional)
2. "How do you feel if this feature is NOT present?" (dysfunctional)

Cross-reference answers to classify.

**When to use:** UX-driven prioritization, user satisfaction optimization.
**Strengths:** User-centric, reveals hidden delighters.
**Weaknesses:** Requires user research data, categories shift over time.

---

## 7. Value vs Effort Matrix

**Axes:**
- X: Effort (Low → High)
- Y: Value (Low → High)

**Quadrants:**
| Quadrant | Value | Effort | Action |
|----------|-------|--------|--------|
| Quick Wins | High | Low | Do first |
| Major Projects | High | High | Plan carefully |
| Fill-ins | Low | Low | Do if time allows |
| Thankless Tasks | Low | High | Avoid or defer |

**When to use:** Team workshops, visual alignment, quick consensus.
**Strengths:** Intuitive, collaborative, good for teams.
**Weaknesses:** Low precision, groupthink risk in workshops.
