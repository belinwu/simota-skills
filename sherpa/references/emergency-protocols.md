# Emergency Protocols & Base Camp

Emergency response levels, evacuation procedures, recovery checkpoints, and multi-epic management.

---

## Emergency Levels

| Level | Condition | Response |
|-------|-----------|----------|
| **Yellow Alert** | 1-2 major blockers, falling behind | Reassess plan, consider scope cut |
| **Red Alert** | Critical path blocked, deadline at risk | Stop, invoke Triage, escalate |
| **Evacuation** | Multiple cascading failures | Full stop, damage control only |

---

## Yellow Alert Protocol

```markdown
## Yellow Alert

**Triggered by**: Velocity 40% below estimate, 2 blockers identified

### Situation Assessment
- Original estimate: 4 hours
- Current progress: 30% in 2.5 hours
- Projected completion: 8+ hours (2x over)

### Options

1. **Scope Cut** (Recommended)
   - Remove Steps 7-9 (nice-to-have features)
   - Deliver MVP by deadline
   - Defer extras to v1.1

2. **Request Reinforcements**
   - Parallel work with another developer
   - Delegate Steps 5-6 to specialist

3. **Extend Timeline**
   - Negotiate deadline extension
   - Communicate revised estimate

4. **Push Through**
   - Accept overtime
   - Risk: Quality may suffer

### Immediate Actions
1. Commit current progress (save point)
2. Document blockers
3. Choose response strategy
```

---

## Red Alert Protocol

```markdown
## Red Alert

**Triggered by**: Critical blocker, cannot proceed

### Situation
- **Blocker**: External API is down, no ETA
- **Impact**: Steps 4-8 are blocked
- **Deadline**: Tomorrow

### Invoking Triage

This situation requires **Triage** agent intervention.

/Triage assess current situation
Context: [Epic] blocked by [blocker]
Impact: [N] steps blocked, deadline [when]
Need: Prioritized recovery options

### Emergency Actions
1. STOP all dependent work
2. DOCUMENT current state thoroughly
3. COMMIT all progress with clear message
4. COMMUNICATE to stakeholders
5. PIVOT to unblocked work if available
```

---

## Evacuation Protocol (Project Fire)

```markdown
## Evacuation Protocol

**Triggered by**: Multiple cascading failures, project integrity at risk

### Immediate Actions

1. **STOP ALL WORK**
   - Do not make any more changes
   - Do not try to "quick fix"

2. **SECURE CURRENT STATE**
   git stash        # Save uncommitted work
   git status       # Document state
   git log -5       # Record recent commits

3. **DOCUMENT EVERYTHING**
   - What was working before
   - What triggered the cascade
   - Current error states

4. **INVOKE TRIAGE**
   /Triage EMERGENCY
   Context: [Brief description]
   Last known good state: [commit hash]
   Current symptoms: [list]

5. **COMMUNICATE**
   - Alert stakeholders immediately
   - Set expectation: "Investigating, will update in X"

### Do NOT:
- Make hasty fixes
- Delete anything
- Hide the problem
- Continue other work until stabilized
```

---

## Recovery Checkpoint

After emergency resolution:

```markdown
## Recovery Checkpoint

**Emergency**: [Description]
**Resolution**: [What fixed it]
**Duration**: [How long it took]

### Post-Mortem Notes
- **Root cause**: [What actually went wrong]
- **Warning signs missed**: [What could have predicted this]
- **Prevention**: [How to avoid next time]

### Plan Adjustments
- [ ] Re-estimate remaining steps
- [ ] Update risk assessments
- [ ] Add new monitoring/checks
- [ ] Document in project journal
```

---

## Base Camp (Multi-Epic Management)

Manage multiple expeditions (Epics) from a central base camp.

### Base Camp Dashboard

```markdown
## Base Camp

**Date**: YYYY-MM-DD
**Session Duration**: Xh Ym
**Total Steps Today**: N completed

### Active Expeditions

| Epic | Progress | Status | Priority | Last Touch |
|------|----------|--------|----------|------------|
| Payment Flow | 40% | Active | P0 | Now |
| User Settings | 25% | Paused | P1 | 2h ago |
| Bug #123 | 0% | Queued | P2 | - |

### Today's Summit Target
- [ ] Payment Flow: Complete Steps 4-6
- [ ] User Settings: Resume if time permits
```

### Epic Priority Matrix

| Priority | Criteria | Examples |
|----------|----------|----------|
| **P0 - Summit** | Blocking others, deadline today | Critical bug, release blocker |
| **P1 - High Camp** | Important, deadline this week | Main feature work |
| **P2 - Base Camp** | Should do, flexible timing | Improvements, tech debt |
| **P3 - Queue** | Nice to have | Ideas, explorations |

### Context Switch Protocol

When user wants to switch Epics:

```markdown
## Context Switch Request

**Current**: [Epic A] (Step X/Y, Z% complete)
**Target**: [Epic B]

### Switch Assessment

| Factor | Value |
|--------|-------|
| Current step completion | 60% (not at good stopping point) |
| Context switch cost | ~8 minutes |
| Priority comparison | P0 -> P1 (lower priority) |
| Momentum loss | High (in flow state) |

### Recommendation: Delay Switch

Complete current step first (est. 8 min remaining).
This creates a clean save point and reduces switch cost.

**Options**:
1. **Finish current step, then switch** (Recommended)
2. **Switch now** (Note: will need to re-do partial work)
3. **Stay on current Epic** (Reconsider switch)
```

### Context Switch Cost Reference

| From -> To | Estimated Cost | Reason |
|-----------|---------------|--------|
| Same domain | ~3 min | Quick pivot, context is fresh |
| Different domain | ~8 min | Need to re-read context |
| After long break | ~12 min | Need to review completed work |
