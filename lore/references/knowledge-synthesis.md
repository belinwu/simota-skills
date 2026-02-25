# Knowledge Synthesis — Pattern Extraction Methodology

How Lore harvests, clusters, deduplicates, and scores patterns from agent journals.

---

## Harvest Protocol

### Source Priority

| Source | Priority | Frequency | Content Type |
|--------|----------|-----------|--------------|
| `.agents/triage.md` | High | After every incident | Incident patterns, detection gaps, mitigation insights |
| `.agents/mend.md` | High | After every remediation | Fix patterns, rollback incidents, verification insights |
| `.agents/builder.md` | High | Weekly | Implementation patterns, API pitfalls, DDD insights |
| `.agents/scout.md` | Medium | Weekly | Bug root cause patterns, investigation techniques |
| `.agents/beacon.md` | Medium | Weekly | Observability insights, SLO patterns |
| `.agents/architect.md` | Medium | Monthly | Design patterns, overlap discoveries |
| `.agents/darwin.md` | Medium | Monthly | Evolution insights, ecosystem health patterns |
| `.agents/PROJECT.md` | Low | Weekly | Activity trends, agent utilization |
| Other agent journals | Low | Monthly | Domain-specific insights |

### Extraction Rules

1. **Read the full journal entry** — never extract from partial context
2. **Identify the core insight** — what was learned that is generalizable?
3. **Extract supporting evidence** — dates, metrics, outcomes
4. **Note the context** — project type, technology stack, scale
5. **Check for prior art** — does this reinforce or contradict existing patterns?

---

## Clustering Algorithm

### Step 1: Semantic Grouping

Group extracted insights by similarity:

```
For each new insight:
  1. Compare against existing METAPATTERNS entries
  2. Calculate semantic similarity (topic + domain + outcome)
  3. If similarity ≥ 80%: cluster with existing pattern
  4. If similarity 50-79%: flag as potential variant
  5. If similarity < 50%: mark as new candidate
```

### Step 2: Cross-Agent Correlation

Look for the same insight appearing across multiple agents:

| Correlation | Significance |
|-------------|-------------|
| Same insight from 2+ agents in same domain | Reinforced domain pattern |
| Same insight from 2+ agents across domains | Cross-cutting pattern (high value) |
| Contradictory insights from different agents | Conflict requiring resolution |
| Agent A's problem = Agent B's solution | Handoff optimization opportunity |

### Step 3: Temporal Analysis

Track pattern evolution over time:

- **Emerging**: First appeared recently, limited evidence
- **Growing**: Evidence increasing, appearing in more contexts
- **Stable**: Consistent evidence over extended period
- **Declining**: Evidence frequency dropping, may be becoming obsolete

---

## Deduplication Protocol

Before registering a new pattern, check:

| Check | If True | Action |
|-------|---------|--------|
| Exact match in catalog | Already registered | Update evidence count + last_validated |
| Partial match (same root cause, different symptoms) | Variant exists | Add as variant to existing pattern |
| Same symptoms, different root cause | Different pattern | Register separately, link as related |
| Superseded by broader pattern | Subsumed | Archive and reference from parent pattern |

### Merge Rules

When merging insights into an existing pattern:
1. Preserve all unique evidence instances
2. Update confidence level based on new evidence count
3. Expand consumer list if new agents are relevant
4. Update last_validated timestamp
5. Note any new context (project type, scale, etc.)

---

## Confidence Scoring

### Evidence-Based Scoring

| Level | Evidence Count | Label | Trust |
|-------|---------------|-------|-------|
| 1 | 1 instance | **Anecdote** | Low — single observation, may be coincidence |
| 2 | 2 instances | **Emerging** | Low-Medium — possible pattern, needs validation |
| 3-5 | 3-5 instances | **Pattern** | Medium — reliable enough to propagate |
| 6-10 | 6-10 instances | **Established** | High — proven across multiple contexts |
| 11+ | 11+ instances | **Foundational** | Very High — core ecosystem knowledge |

### Confidence Modifiers

| Factor | Effect | Example |
|--------|--------|---------|
| Cross-agent corroboration | +1 level | Builder and Artisan both report same API pattern |
| Diverse project types | +1 level | Pattern holds across SaaS, CLI, and E-commerce |
| Contradiction exists | -1 level | Conflicting evidence from another agent |
| Single project context | -1 level | Only observed in one project |
| Recent evidence (< 30 days) | +0 (no modifier) | Freshness is tracked separately |
| Stale evidence (> 180 days) | -1 level | Pattern may be outdated |

### Promotion Criteria

A pattern is promoted to the next confidence level when:
1. New evidence instance from a different context (not just same project repeated)
2. No active contradictions at time of promotion
3. Last evidence instance is within 90 days (freshness requirement)

---

## Contradiction Resolution

When conflicting insights are discovered:

### Resolution Protocol

1. **Document both sides** — preserve both perspectives with full evidence
2. **Identify the variable** — what differs between contexts? (scale, domain, tech stack)
3. **Classify the contradiction**:
   - **Context-dependent**: Both are correct in their respective contexts → Create conditional pattern
   - **Temporal**: Older insight superseded by newer knowledge → Archive old, promote new
   - **Genuine conflict**: Fundamentally incompatible → Escalate to relevant domain agents
4. **Register resolution** with reasoning in pattern entry

### Conditional Pattern Format

```markdown
**Pattern:** [Description]
**When [context A]:** [Approach A] — Evidence: [sources]
**When [context B]:** [Approach B] — Evidence: [sources]
**Deciding factor:** [What determines which context applies]
```

---

## Output: Synthesis Report

After each synthesis cycle, produce:

```markdown
## Lore Synthesis Report — [YYYY-MM-DD]

### Journals Scanned
| Agent | Entries Processed | New Insights | Updated Patterns |
|-------|-------------------|-------------|------------------|

### New Patterns Registered
| Pattern ID | Title | Confidence | Consumers |
|------------|-------|------------|-----------|

### Patterns Reinforced
| Pattern ID | Previous Confidence | New Confidence | New Evidence |
|------------|--------------------|----|------|

### Contradictions Detected
| Pattern ID | Conflicting Source | Resolution Status |
|------------|-------------------|-------------------|

### Decay Alerts
| Pattern ID | State | Days Since Last Evidence | Recommended Action |
|------------|-------|------------------------|-------------------|
```
