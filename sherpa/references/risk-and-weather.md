# Risk Assessment & Weather System

Risk categories, severity levels, mitigation strategies, project health monitoring, and fatigue detection.

---

## Risk Categories

| Category | Description |
|----------|-------------|
| Technical | New technology, complex logic, unfamiliar patterns |
| Blocker | External dependencies, approvals, third-party APIs |
| Scope | Unclear requirements, potential scope creep |
| Time | Underestimated complexity, unknown unknowns |

---

## Risk Levels

| Level | Action |
|-------|--------|
| Low | Proceed normally |
| Medium | Monitor closely, have fallback ready |
| High | Investigate first, consider alternatives |

---

## Risk Assessment Template

```markdown
### Risk Assessment: [Epic Name]

| Step | Risk Level | Category | Risk | Mitigation |
|------|------------|----------|------|------------|
| 1 | Low | - | Standard task | - |
| 2 | Medium | Technical | New API pattern | Review docs first |
| 3 | Low | - | Standard UI | - |
| 4 | High | Blocker | External API unstable | Mock fallback ready |
| 5 | Medium | Scope | Error cases unclear | Scout investigation |

**Overall Risk**: Medium
**High Risk Steps**: Step 4 - prepare mock fallback
**Recommended**: Scout investigation before Step 5
```

---

## Risk Mitigation Strategies

### Technical Risk
- Spike/prototype first
- Pair with expert (suggest specialist agent)
- Time-box investigation

### Blocker Risk
- Identify early in planning
- Prepare mock/stub fallback
- Communicate dependencies to stakeholders

### Scope Risk
- Request Scout investigation
- Define MVP scope explicitly
- Get written confirmation before starting

### Time Risk
- Break down further (smaller atoms)
- Add buffer to estimates
- Identify cut points if running late

---

## Weather System (Project Health)

Monitor project conditions continuously, like a mountain guide reading the weather.

### Weather Indicators

| Indicator | Clear | Cloudy | Stormy | Dangerous |
|-----------|-------|--------|--------|-----------|
| **Velocity** | On/ahead of estimate | 10-20% slower | 20-50% slower | >50% slower |
| **Risk accumulation** | 0-1 high-risk steps | 2 high-risk steps | 3+ high-risk | Cascading risks |
| **Blockers** | None | 1 manageable | Multiple | Critical path blocked |
| **Scope changes** | None | Minor additions | Significant growth | Uncontrolled |
| **User energy** | Focused | Normal | Fatigued signals | Frustrated/stuck |

### Weather Report Template

```markdown
## Weather Report

**Current Conditions**: Clear / Cloudy / Stormy / Dangerous
**Trend**: Improving / Stable / Degrading

| Indicator | Status | Notes |
|-----------|--------|-------|
| Velocity | On track, 12 min/step (est: 15) | Ahead of schedule |
| Risk level | 2 high-risk pending | Step 4 & 7 |
| Blockers | None | - |
| Scope | Stable | No changes |
| Energy | 3h into session | Consider break soon |

**Forecast**: Clear conditions for next 2 steps. Expect turbulence at Step 4.

**Recommendations**:
- Complete Steps 2-3 while conditions are good
- Prepare API mock before reaching Step 4
- Schedule break after Step 3
```

### Weather-Based Decisions

| Condition | Guidance |
|-----------|----------|
| **Clear** | Proceed at full speed; can take on slightly larger steps; good time for challenging work |
| **Cloudy** | Proceed with monitoring; stick to estimated step sizes; address warnings early |
| **Stormy** | Slow down, smaller steps only; focus on stabilizing; frequent commits |
| **Dangerous** | STOP new feature work; assess continue or retreat; invoke Triage if needed |

---

## Fatigue Detection

Watch for signs of user fatigue:

| Signal | Pattern | Response |
|--------|---------|----------|
| Increasing errors | Same mistake 2+ times | Suggest break |
| Slowing velocity | Steps taking 2x longer | Acknowledge, adjust |
| Drift frequency | 3+ drift alerts in 30 min | Focus check |
| Frustration language | "This is annoying", "Why won't..." | Empathize, simplify |
| Long silences | No progress for 15+ min | Check in gently |

### Rest Stop Suggestion Template

```markdown
## Rest Stop Suggestion

You've been climbing for 2.5 hours and completed 6 steps. Great progress!

I notice the pace is slowing - this is normal. Options:

1. **Quick break** (5 min) - Step away, return refreshed
2. **Commit checkpoint** - Save progress, continue tomorrow
3. **Switch to easier terrain** - Move to a simpler parallel task
4. **Push through** - If deadline requires it

Your current step is 80% done. Good stopping point after completion.
```
