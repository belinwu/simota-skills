# Risk-Based Prioritization

How Drill assigns P0-P3 to every test case, aligned with **ISO/IEC/IEEE 29119-2:2021** Risk-Based Testing.

---

## Risk Score

```
Risk = Likelihood × Impact × Frequency-of-use
```

Score each factor 1-5, then sum the **product weights**:

| Factor | 1 | 2 | 3 | 4 | 5 |
|--------|---|---|---|---|---|
| **Likelihood** (defect probability) | Trivial logic | Simple | Moderate | Complex | High-complexity / new module |
| **Impact** (consequence if it fails) | Cosmetic | Minor inconvenience | Workflow blocked, workaround exists | Data loss / revenue blocked / single-user | Outage / breach / data corruption / many users |
| **Frequency** (usage rate) | <1% of sessions | 1-10% | 10-30% | 30-70% | >70% / every session |

| Risk Score | Priority | SLA |
|------------|----------|-----|
| ≥48 | **P0** | Smoke + Sanity + Regression; blocks release if failing |
| 24-47 | **P1** | Sanity + Regression |
| 8-23 | **P2** | Regression only |
| <8 | **P3** | Spot-check; smoke-only if covered at all |

The thresholds are gauges, not absolutes. Override with documented rationale.

---

## Priority Definitions

### P0 — Release Blocker

- Critical business function (payment, auth, data write).
- Compliance-required (privacy, accessibility, regulatory).
- Affects all users or >50% of sessions.
- Failure has no workaround.

**Must include**: positive case, negative case, boundary case, recovery case.
**Tier membership**: Smoke + Sanity + Regression.

### P1 — Important

- Major feature path, secondary business function.
- Affects 10-50% of users.
- Workaround exists but is awkward.

**Must include**: positive case, negative case.
**Tier membership**: Sanity + Regression.

### P2 — Standard

- Edge feature or rarely-used path.
- Affects <10% of users or specific personas.
- Failure is recoverable without intervention.

**Must include**: at least one happy-path case.
**Tier membership**: Regression only.

### P3 — Low

- Cosmetic, nice-to-have, deprecated path.
- Workarounds trivial.

**Tier membership**: Spot-check only; may be excluded from default regression.

---

## Worked Example

**Feature**: "Apply gift card during checkout".

| Test Case | Likelihood | Impact | Frequency | Score | Priority |
|-----------|------------|--------|-----------|-------|----------|
| Apply valid gift card → discount applied | 2 | 4 | 3 | 24 | P1 |
| Apply expired gift card → reject with reason | 3 | 4 | 2 | 24 | P1 |
| Apply gift card during inventory race → no double-spend | 4 | 5 | 2 | 40 | P1 |
| Apply gift card with currency mismatch → reject or convert | 4 | 4 | 1 | 16 | P2 |
| Gift card UI shows hint text in correct color | 1 | 1 | 4 | 4 | P3 |
| Apply gift card → audit log entry written | 2 | 5 | 3 | 30 | P1 |
| Apply gift card across two tabs → no double-redeem | 5 | 5 | 1 | 25 | P1 |
| Apply gift card → email confirmation includes balance | 2 | 3 | 2 | 12 | P2 |

---

## Domain-Specific Risk Modifiers

Apply on top of the base score.

| Modifier | Multiplier | When |
|----------|------------|------|
| Money / Payments | +50% | Any cash-affecting flow |
| Auth / Identity | +50% | Login, password reset, session, MFA |
| Data Write | +30% | Any persistent state change |
| Compliance | +30% | Regulated data (PII, PHI, PCI), accessibility legal floor |
| Public API consumer | +20% | Any externally-contracted endpoint |
| First-time user path | +20% | Onboarding, signup |
| Reversible | -20% | Action that can be undone within 5 min |
| Internal-only | -30% | Admin / staff feature, no end-user exposure |
| EU market exposure | **+1 tier** | Product is offered to EU end-users; accessibility (WCAG 2.2 ISO + EAA effective 2025-06-28) and DSA/GDPR scenarios escalate one priority tier (P2→P1, P1→P0). [Source: https://adaquickscan.com/blog/wcag-2-2-iso-standard-2025] |
| High-risk AI component (EU AI Act Annex III) | **+1 tier** | Case targets a high-risk AI subsystem (biometric ID, employment, essential services, law enforcement, etc.); Article 18 logging and dataset-lineage obligations apply, phased application from 2027-12. [Source: https://artificialintelligenceact.eu/article/43/] |

Apply multiplicative modifiers first, then re-tier with the same thresholds, then apply tier-shift modifiers last.

---

## Risk Heatmap (Output Artifact)

For releases, Drill emits a heatmap:

```markdown
## Risk Heatmap

|                | Impact 1 | Impact 2 | Impact 3 | Impact 4 | Impact 5 |
|----------------|----------|----------|----------|----------|----------|
| Likelihood × Freq high | — | TC-008 | TC-001, TC-003 | TC-005 | **TC-002, TC-007** |
| Likelihood × Freq med  | TC-012 | TC-009 | TC-004 | TC-006 | TC-010 |
| Likelihood × Freq low  | TC-013 | — | TC-011 | — | — |

P0 cells: top-right corner (bolded).
```

---

## When the Spec Doesn't Tell You Risk

If the source artifact provides no risk signal, fall back to:
1. Recent defect density per module (route to Trail for git-log query).
2. Production usage analytics (route to Pulse for KPI lookup).
3. Customer-facing exposure (public / authenticated / internal-only).
4. Cost of failure modeling (revenue per minute of outage × estimated MTTR).

Document the inferred risk basis in the test case's `Notes:` field so reviewers can challenge it.

---

## Anti-Patterns

| Anti-pattern | Why it's bad | Fix |
|--------------|--------------|-----|
| Everything is P0 | The suite cannot be tiered; smoke runs 3 hours | Re-score; force a distribution close to P0 15% / P1 35% / P2 35% / P3 15% as a sanity check |
| Priority by author preference | Bias toward author's recent work | Use the scoring rubric verbatim; show the scores in the case body |
| Priority once, never re-scored | Risk shifts as the product matures | Re-score quarterly; trigger re-score after major architecture change |
| Severity confused with Priority | "Severity" describes a defect's impact when found; "Priority" describes urgency to test | Keep them separate: defect severity in the defect template, test priority in the test case |
| **Over-coverage / under-specification (AI-generation failure mode)** | LLM-drafted suites pile up many redundant valid-input variants ("Login with Alice", "Login with Bob", …) while leaving expected results vague ("should work", "looks correct") | Require each Expected Result to contain a verb + observable object; consolidate redundant positive variants into one parameterized case + boundary deltas. Enforced by the SKILL.md AI-authoring self-check. [Source: https://techdebt.guru/ai-testing-gaps/] |
