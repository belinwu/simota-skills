# Decay Detection — Knowledge Freshness Management

How Lore monitors knowledge freshness, detects staleness, and manages the lifecycle of patterns.

---

## Freshness States

| State | Age Since Last Evidence | Indicator | Action |
|-------|----------------------|-----------|--------|
| **FRESH** | < 30 days | Recently validated or reinforced | None — healthy |
| **CURRENT** | 30-90 days | Still relevant, not recently reinforced | Monitor |
| **AGING** | 90-180 days | Risk of becoming stale | Flag for review |
| **STALE** | > 180 days | Likely outdated, no recent evidence | Review + Archive or Revalidate |

### State Transitions

```
FRESH ──(30 days)──→ CURRENT ──(90 days)──→ AGING ──(180 days)──→ STALE
  ↑                      ↑                     ↑                    │
  └── new evidence ───────┴── new evidence ─────┘                    │
                                                              ┌──────┴──────┐
                                                          ARCHIVED      REVALIDATED
                                                          (removed)     (→ FRESH)
```

---

## Decay Signals

### Primary Signals (Automatic Detection)

| Signal | Detection Method | Severity |
|--------|-----------------|----------|
| **Time-based decay** | `now - last_validated > threshold` | Proportional to age |
| **Source agent deprecated** | Agent removed from BOUNDARIES.md | High |
| **Technology obsolescence** | Referenced tech no longer in project | Medium |
| **Contradicted by newer evidence** | Newer journal entries conflict | High |
| **Zero consumer references** | No consuming agent has referenced pattern | Medium |

### Secondary Signals (Requires Analysis)

| Signal | Detection Method | Severity |
|--------|-----------------|----------|
| **Domain shift** | Project types in ecosystem have changed | Low |
| **Ecosystem restructuring** | Agent boundaries or routing changed significantly | Medium |
| **Confidence deflation** | Modifiers have reduced confidence below registration threshold | Medium |

---

## Audit Protocol

### Scheduled Audit (Monthly)

1. **Scan all patterns** for freshness state
2. **Identify AGING patterns** — add to review queue
3. **Identify STALE patterns** — flag for immediate review
4. **Check for orphaned patterns** — source agents no longer exist
5. **Generate Decay Report**

### Decay Report Format

```markdown
## Knowledge Decay Report — [YYYY-MM-DD]

### Summary
- Total patterns: [N]
- FRESH: [N] ([%])
- CURRENT: [N] ([%])
- AGING: [N] ([%]) — review recommended
- STALE: [N] ([%]) — action required

### STALE Patterns (Action Required)
| Pattern ID | Title | Days Since Evidence | Source Agents | Recommended |
|------------|-------|--------------------|----|---|
| [ID] | [Title] | [N] | [Agents] | Archive / Revalidate / Remove |

### AGING Patterns (Review Recommended)
| Pattern ID | Title | Days Since Evidence | Consumer Activity |
|------------|-------|--------------------|----|
| [ID] | [Title] | [N] | [Last referenced by consumer] |

### Orphaned Patterns
| Pattern ID | Missing Source Agent | Recommended |
|------------|---------------------|-------------|
| [ID] | [Agent name] | Archive with note |
```

---

## Revalidation Protocol

When a STALE or AGING pattern needs revalidation:

### Steps

1. **Check source journals** — has new relevant evidence appeared but was missed?
2. **Check consumer behavior** — are consumers still acting on this pattern?
3. **Check domain relevance** — is the technology/context still in active use?
4. **Decision matrix:**

| Still relevant? | New evidence? | Action |
|----------------|---------------|--------|
| Yes | Yes | Revalidate → FRESH |
| Yes | No | Keep at AGING, note "awaiting evidence" |
| No | — | Archive with reason |
| Uncertain | — | Flag for domain expert review |

### Revalidation Sources

| Approach | Method |
|----------|--------|
| **Active probing** | Ask relevant agents "is this pattern still observed?" via propagation |
| **Passive monitoring** | Watch for new journal entries that reinforce or contradict |
| **Context check** | Verify referenced technologies/tools still in use |

---

## Archive Management

### Archive Criteria

A pattern is archived (not deleted) when:
- STALE for > 180 days AND no consumer references in that period
- Source agent has been removed from ecosystem
- Superseded by a newer, broader pattern
- Technology context no longer exists

### Archive Format

Archived patterns move to an `## Archive` section at the bottom of METAPATTERNS.md:

```markdown
## Archive

### [PATTERN_ID]: [Title] (Archived: [YYYY-MM-DD])
**Reason:** [Why archived]
**Original confidence:** [Level]
**Last evidence:** [YYYY-MM-DD]
**Superseded by:** [New pattern ID, if applicable]
```

### Resurrection

Archived patterns can be restored if:
1. New evidence emerges that revalidates the pattern
2. Technology/context becomes relevant again
3. Consumer explicitly requests restoration

Restore to EMERGING confidence, regardless of original level — must re-earn confidence.

---

## Health Score Contribution

Lore's decay management contributes to Darwin's Ecosystem Fitness Score:

| Metric | Weight | Calculation |
|--------|--------|-------------|
| **Freshness ratio** | 40% | (FRESH + CURRENT) / total_patterns |
| **Contradiction ratio** | 30% | 1 - (contested / total_patterns) |
| **Coverage ratio** | 20% | domains_with_patterns / total_domains |
| **Uptake ratio** | 10% | patterns_referenced_by_consumers / patterns_propagated |

**Knowledge Health Score** = Σ(metric × weight) × 100

| Score | Grade | Interpretation |
|-------|-------|---------------|
| 90-100 | A | Excellent — knowledge is fresh and well-propagated |
| 80-89 | B | Good — minor staleness or gaps |
| 70-79 | C | Fair — significant staleness, review needed |
| 60-69 | D | Poor — many stale patterns, active curation required |
| < 60 | F | Critical — knowledge base is unreliable, major refresh needed |
