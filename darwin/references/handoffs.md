# Handoff Templates

All-direction handoff templates for Darwin's collaboration with other agents.

---

## Darwin → Architect

### Improvement Proposal

```markdown
## NEXUS_HANDOFF

**Step**: [N]
**Agent**: Darwin
**Summary**: Ecosystem analysis identified improvement opportunities for agent design.

**Findings**:
- EFS: [XX]/100 (Grade: [X])
- Lifecycle phase: [PHASE] (confidence: [X.XX])
- Agents needing improvement: [list with RS scores]
- Coverage gaps identified: [list]

**Improvement proposals**:
1. [Proposal with rationale]
2. [Proposal with rationale]

**Artifacts**: `.agents/ECOSYSTEM.md` (updated)
**Risks**: [potential risks of proposed changes]
**Suggested next agent**: Architect
**Next action**: Review proposals, update agent designs as needed
```

### Sunset Candidate

```markdown
## NEXUS_HANDOFF

**Step**: [N]
**Agent**: Darwin
**Summary**: Staleness detection identified sunset candidates requiring Architect review.

**Sunset candidates**:
| Agent | RS | Status | Last Used | Reason |
|-------|----|--------|-----------|--------|
| [name] | [XX] | Sunset | [date] | [reason] |

**Void verification**: [status — should be confirmed before Architect acts]
**Artifacts**: `.agents/ECOSYSTEM.md` Staleness Report
**Risks**: Premature retirement may leave coverage gaps
**Suggested next agent**: Architect (after Void verification)
**Next action**: Review sunset candidates, plan retirement or revival
```

---

## Darwin → Nexus

### Dynamic AFFINITY Override

```markdown
## NEXUS_HANDOFF

**Step**: [N]
**Agent**: Darwin
**Summary**: Lifecycle analysis generated Dynamic AFFINITY overrides for improved routing.

**Phase transition**: [FROM] → [TO] (confidence: [X.XX])

**AFFINITY overrides**:
| Agent | Base | Override | Reason |
|-------|------|---------|--------|
| [name] | [H/M/—] | [H/M/—] | [reason] |

**Application**: Read `.agents/ECOSYSTEM.md` Dynamic Affinity Override section during routing.
**Expiry**: 90 days from date (auto-expire if not refreshed)
**Artifacts**: `.agents/ECOSYSTEM.md` (updated)
**Risks**: Override may not match all task types; monitor chain success rate
**Suggested next agent**: DONE (Nexus applies overrides automatically)
**Next action**: Apply overrides in subsequent routing decisions
```

---

## Darwin → Void

### Sunset Verification Request

```markdown
## NEXUS_HANDOFF

**Step**: [N]
**Agent**: Darwin
**Summary**: Requesting YAGNI verification for potential sunset candidates.

**Candidates**:
| Agent | RS | Days Unused | Phase Affinity | Evidence |
|-------|----|-------------|---------------|----------|
| [name] | [XX] | [NN] | [low/neutral] | [evidence summary] |

**Question**: Are these agents still needed, or are they YAGNI?
**Context**: Current phase is [PHASE], EFS is [XX]/100
**Artifacts**: `.agents/ECOSYSTEM.md` Staleness Report
**Risks**: False positive — agent may be needed in upcoming phase transition
**Suggested next agent**: Void
**Next action**: YAGNI assessment for each candidate
```

---

## Darwin → Canvas

### EFS Dashboard Request

```markdown
## NEXUS_HANDOFF

**Step**: [N]
**Agent**: Darwin
**Summary**: Requesting visualization of Ecosystem Fitness Score dashboard.

**Data**:
```
EFS Trend: [time-series data]
Dimension Breakdown: [5 dimensions with scores]
Agent RS Distribution: [status counts]
Lifecycle Phase: [current phase]
Evolution History: [recent actions]
```

**Visualization needs**:
1. EFS time-series line chart (last 10 checks)
2. 5-dimension radar chart (current state)
3. Agent RS distribution bar chart (by status)
4. Lifecycle phase timeline

**Artifacts**: `.agents/ECOSYSTEM.md`
**Format**: Mermaid diagrams preferred
**Suggested next agent**: Canvas
**Next action**: Generate ecosystem health dashboard
```

---

## Darwin → Latch

### SessionStart Hook Recommendation

```markdown
## NEXUS_HANDOFF

**Step**: [N]
**Agent**: Darwin
**Summary**: Recommending SessionStart hook configuration for evolution-aware sessions.

**Recommendation**:
- Display EFS summary on session start (if ECOSYSTEM.md exists)
- Alert on pending evolution proposals
- Show lifecycle phase context

**Hook format**:
```
On SessionStart:
  If .agents/ECOSYSTEM.md exists:
    Read EFS, Phase, Pending Proposals
    Display: "🧬 Ecosystem: EFS [XX]/100 ([Grade]) | Phase: [PHASE] | [N] proposals"
```

**Artifacts**: `.agents/ECOSYSTEM.md`
**Risks**: Minimal — read-only hook
**Suggested next agent**: Latch
**Next action**: Configure SessionStart hook
```

---

## Architect → Darwin

### Health Score Input

```markdown
## NEXUS_HANDOFF

**Step**: [N]
**Agent**: Architect
**Summary**: Providing ecosystem health assessment for Darwin integration.

**Health Score**: [XX]/100
**Agent count**: [NN]
**Coverage gaps**: [list]
**Overlap warnings**: [list]
**Recent changes**: [list of agent additions/modifications]

**Artifacts**: Latest Architect review output
**Suggested next agent**: Darwin
**Next action**: Integrate into EFS Quality dimension
```

---

## Hone → Darwin

### UQS History Input

```markdown
## NEXUS_HANDOFF

**Step**: [N]
**Agent**: Hone
**Summary**: Providing UQS history for Darwin quality trend analysis.

**UQS History** (last 5 cycles):
| Cycle | UQS | Delta | Focus Area |
|-------|-----|-------|------------|
| [N] | [XX] | [±X] | [area] |

**Plateau detected**: [yes/no]
**Quality trend**: [improving/stable/declining]

**Artifacts**: `.agents/hone.md` journal
**Suggested next agent**: Darwin
**Next action**: Integrate into EFS Quality dimension, check ET-02 trigger
```

---

## Compass → Darwin

### Strategy Drift Alert

```markdown
## NEXUS_HANDOFF

**Step**: [N]
**Agent**: Compass
**Summary**: Strategy drift detected, providing data for ecosystem alignment.

**Drift summary**: [description]
**Affected areas**: [list]
**Strategic priority shift**: [from → to]

**Artifacts**: `.agents/compass.md` journal
**Suggested next agent**: Darwin
**Next action**: Re-evaluate AFFINITY overrides for strategy alignment
```

---

## Totem → Darwin

### Culture DNA Update

```markdown
## NEXUS_HANDOFF

**Step**: [N]
**Agent**: Totem
**Summary**: Culture profile updated, providing DNA scores for Darwin integration.

**DNA scores**:
| Dimension | Score | Change |
|-----------|-------|--------|
| [dim] | [X.XX] | [±X.XX] |

**Significant shifts**: [list of dimensions with >0.5 change]

**Artifacts**: `.agents/totem.md` journal
**Suggested next agent**: Darwin
**Next action**: Check ET-08 trigger, update cultural alignment in AFFINITY
```

---

## DARWIN_COMPLETE Format

Used when Darwin finishes a complete evolution check:

```markdown
## DARWIN_COMPLETE

**Evolution check**: YYYY-MM-DD
**Lifecycle phase**: [PHASE] (confidence: [X.XX])
**EFS**: [XX]/100 (Grade: [X], trend: [↑↓→])
**Triggers fired**: [list or "none"]
**Actions taken**: [list or "none"]
**Proposals pending**: [count]
**Next recommended check**: [date or trigger condition]
```
