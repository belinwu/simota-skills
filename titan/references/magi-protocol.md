# Magi Consultation Protocol

Defines the formal interface between Titan and Magi for structured decision-making.

---

## When to Consult Magi

Per the Decision Matrix:

| Condition | Action |
|-----------|--------|
| Medium impact + Semi-reversible | Decide + consult Magi |
| Medium impact + Irreversible | Decide + Magi + risk log |
| High impact + Reversible | Decide + consult Magi |
| High impact + Semi-reversible | Decide + Magi + risk log |
| High impact + Irreversible | Check Risk Budget (Magi mandatory) |
| Risk budget ≥76 (HIGH state) | Magi mandatory for all decisions |

---

## MAGI_REQUEST Format

When Titan needs Magi consultation, issue:

```markdown
## MAGI_REQUEST
Decision: [What needs to be decided — concise statement]
Phase: [Current lifecycle phase]
Options:
  A: [Description] — Pros: [...] Cons: [...]
  B: [Description] — Pros: [...] Cons: [...]
  C: [Description] — Pros: [...] Cons: [...]
Criteria:
  - [Primary evaluation criterion]
  - [Secondary criterion]
  - [Tertiary criterion]
Risk:
  scope: [1-3]
  reversibility: [1-3]
  external_dep: [0-2]
  security: [0-3]
  calculated_score: [N]
  cumulative_before: [N]
Context: [Phase state, blocking issues, prior decisions, constraints]
```

### Request Rules

1. Always provide **3 options minimum** (A/B/C)
2. Include quantified risk scores, not just labels
3. Specify criteria in priority order (most important first)
4. Include relevant context from prior phases/decisions

---

## MAGI_VERDICT Format

Magi returns:

```markdown
## MAGI_VERDICT
Verdict: [Selected option: A/B/C]
Consensus: [3-0 / 2-1 / 1-1-1]
Perspectives:
  Logic: [Technical merit analysis — which option and why]
  Empathy: [User/team impact analysis — which option and why]
  Pragmatism: [Delivery speed/cost analysis — which option and why]
Dissent: [Minority perspective rationale, if not unanimous]
Conditions: [Any conditions or caveats for the chosen option]
Confidence: [HIGH / MEDIUM / LOW]
```

---

## Consensus-Based Actions

| Consensus | Meaning | Titan Action |
|-----------|---------|-------------|
| **3-0** | Unanimous agreement | Log decision → proceed immediately |
| **2-1** | Majority with dissent | Log decision + dissent → proceed |
| **1-1-1** | No agreement | Present to user for selection (ON_AMBIGUOUS_GOAL pattern) |
| **0-3** against all | All options rejected | L3 Strategic reconsideration |

### Confidence Modifiers

| Confidence | Action |
|-----------|--------|
| HIGH | Proceed without delay |
| MEDIUM | Proceed + add to monitoring list |
| LOW | Add risk buffer; consider user check at next phase gate |

---

## Decision Log Integration

After receiving MAGI_VERDICT, Titan records in the Decision Log:

```markdown
## Decision: [Title]
- **ID**: DEC-[NNN]
- **Phase**: [Phase]
- **Date**: [YYYY-MM-DD]
- **Impact**: [Low/Medium/High]
- **Reversibility**: [Reversible/Semi/Irreversible]
- **Risk Score**: [N] (cumulative: [N])
- **Choice**: [Selected option]
- **Rationale**: [Why — from MAGI_VERDICT]
- **Magi Consensus**: [3-0/2-1/1-1-1]
  - Logic: [Summary]
  - Empathy: [Summary]
  - Pragmatism: [Summary]
- **Dissent**: [If any]
- **Conditions**: [If any]
- **Rollback Plan**: [How to undo]
```

### Decision Log Location

Decisions are recorded in `.agents/titan-state.md` under `## Decision Log` section.

---

## Magi Interaction Patterns

### Architecture Decision (ARCHITECT phase)

```markdown
## MAGI_REQUEST
Decision: Monolith vs Microservices for user management
Phase: ARCHITECT
Options:
  A: Monolith — Pros: Simple, fast delivery Cons: Scaling limits
  B: Microservices — Pros: Independent scaling Cons: Complexity, latency
  C: Modular monolith — Pros: Balanced Cons: Requires discipline
Criteria:
  - Team size and skill (small team → simpler)
  - Expected scale (>10K users → scalable)
  - Time to market (tight → simpler)
Risk:
  scope: 3
  reversibility: 2
  external_dep: 0
  security: 0
  calculated_score: 6
  cumulative_before: 12
Context: 2-person team, MVP target, enterprise SaaS
```

### Technology Selection (BUILD phase)

```markdown
## MAGI_REQUEST
Decision: State management library selection
Phase: BUILD
Options:
  A: Redux Toolkit — Pros: Mature, devtools Cons: Boilerplate
  B: Zustand — Pros: Minimal, simple Cons: Less ecosystem
  C: Jotai — Pros: Atomic, React-native Cons: Learning curve
Criteria:
  - Bundle size impact
  - Developer experience
  - Ecosystem maturity
Risk:
  scope: 2
  reversibility: 1
  external_dep: 1
  security: 0
  calculated_score: 3
  cumulative_before: 18
Context: React 18 app, 15 components need shared state
```
