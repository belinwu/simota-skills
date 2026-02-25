# Propagation Protocol — Knowledge Distribution

How Lore distributes insights to consuming agents effectively.

---

## Propagation Triggers

| Trigger | Action | Urgency |
|---------|--------|---------|
| New pattern registered (Confidence ≥ Pattern) | Notify relevant consumers | Normal |
| Pattern promoted to Established/Foundational | Broadcast to all consumers | Normal |
| Contradiction detected | Alert affected agents | High |
| Decay alert (pattern going STALE) | Notify consumers + source agents | Low |
| Anti-pattern discovered | Immediately notify affected agents | High |
| Cross-agent pattern discovered | Notify Architect + Darwin | Normal |

---

## Consumer Relevance Matrix

### Primary Consumers (Always notify)

| Consumer | Relevant Patterns | Why |
|----------|------------------|-----|
| **Architect** | META-*, DESIGN-*, any ECOSYSTEM scope | Informs new agent design and existing agent improvement |
| **Darwin** | META-*, usage trends, staleness signals | Informs ecosystem evolution proposals |
| **Nexus** | PROCESS-*, chain effectiveness patterns | Informs routing matrix optimization |

### Domain Consumers (Notify when domain matches)

| Consumer | Relevant Domains | Example |
|----------|-----------------|---------|
| **Builder** | APP-SUCCESS, APP-ANTI, APP-HEURISTIC | "Validate API responses at integration boundary" |
| **Artisan** | UX-SUCCESS, UX-ANTI, APP-TRADEOFF | "Server Components reduce hydration bugs" |
| **Mend** | INFRA-SUCCESS, INFRA-FAILURE, APP-FAILURE | New remediation pattern candidates |
| **Triage** | INFRA-FAILURE, APP-FAILURE, PROCESS-* | Recurring incident patterns |
| **Sentinel** | SECURITY-* | Security anti-patterns, vulnerability patterns |
| **Radar** | TEST-* | Testing best practices, coverage patterns |
| **Beacon** | PERF-*, INFRA-HEURISTIC | Observability insights, SLO patterns |
| **Gear** | INFRA-SUCCESS, INFRA-ANTI | CI/CD and infrastructure patterns |

### Meta Consumers (Notify for ecosystem patterns)

| Consumer | Relevant Patterns | Why |
|----------|------------------|-----|
| **Sigil** | CROSS scope patterns, PROJECT_AFFINITY matches | Project-specific skill optimization |
| **Hone** | PROCESS-*, quality-related patterns | PDCA cycle improvements |
| **Totem** | DESIGN-*, naming/convention patterns | Cultural drift detection input |

---

## Insight Delivery Format

### Standard Insight Notification

```markdown
## LORE_INSIGHT: [Pattern ID]

**To:** [Consumer Agent]
**Relevance:** [1-2 sentences on why this matters to the consumer]
**Pattern:** [Clear description]
**Confidence:** [Level] ([N] evidence instances)
**Evidence highlights:**
- [Most relevant evidence for this consumer]
- [Second most relevant]
**Recommended action:** [Specific, actionable suggestion for the consumer]
**Full details:** METAPATTERNS.md → [Pattern ID]
```

### Anti-Pattern Alert (Urgent)

```markdown
## LORE_ALERT: [Pattern ID]

**To:** [Consumer Agent]
**Type:** Anti-pattern / Contradiction
**Impact:** [What could go wrong if ignored]
**Pattern:** [Description of what to avoid]
**Evidence:** [Key evidence]
**Instead:** [What to do instead]
**Confidence:** [Level]
```

---

## Feedback Loop

After propagation, Lore tracks effectiveness:

### Feedback Collection

| Signal | Meaning | Action |
|--------|---------|--------|
| Consumer references pattern in journal | Pattern was useful | +1 reinforcement |
| Consumer contradicts pattern in journal | Pattern may be wrong | Flag as CONTESTED |
| Consumer ignores pattern (no reference in 90 days) | Pattern may be irrelevant | Review consumer relevance |
| Consumer requests more detail | Pattern description insufficient | Expand evidence/context |

### Propagation Effectiveness Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Uptake rate** | ≥ 60% | Patterns referenced by consumers / patterns propagated |
| **Relevance accuracy** | ≥ 80% | Useful patterns / total propagated (per consumer) |
| **Contradiction rate** | < 10% | Contested patterns / total patterns |
| **Decay prevention** | ≥ 70% | Patterns kept FRESH or CURRENT / total patterns |

---

## Propagation Schedule

| Frequency | Activity |
|-----------|----------|
| **Per-event** | Anti-pattern alerts, contradiction alerts |
| **Weekly** | Digest of new patterns + reinforced patterns to primary consumers |
| **Monthly** | Full synthesis report to Architect + Darwin |
| **Quarterly** | Ecosystem knowledge health report (coverage, freshness, gaps) |

---

## Knowledge Gaps Report

When Lore detects areas with sparse pattern coverage:

```markdown
## Knowledge Gap Report — [YYYY-MM-DD]

### Under-documented Domains
| Domain | Pattern Count | Last New Pattern | Assessment |
|--------|--------------|-----------------|------------|
| [Domain] | [N] | [date] | Sparse — needs attention |

### Under-sourced Agents
| Agent | Journal Entries | Insights Extracted | Assessment |
|-------|----------------|-------------------|------------|
| [Agent] | [N] | [M] | Low yield — journal may need enrichment |

### Recommended Actions
1. [Action to address gap 1]
2. [Action to address gap 2]
```
