# Progress Tracking

Epic dashboard, stalled detection, task tool integration, dependency graphs, velocity tracking, and session retrospectives.

---

## Epic Dashboard Template

```markdown
## Epic Dashboard: [Name]

**Started**: YYYY-MM-DD HH:MM
**Elapsed**: X hours Y minutes
**Status**: On Track | Behind | Blocked

### Progress
[========....................] 40% (4/10 steps)

### Velocity
- Completed: 4 steps in 45 min
- Average: 11 min/step
- Projected completion: 1h 15min remaining

### Steps
| # | Step | Size | Est | Actual | Status |
|---|------|------|-----|--------|--------|
| 1 | Define types | S | 10m | 8m | Done |
| 2 | API mock | M | 20m | 25m | Done |
| 3 | UI skeleton | M | 20m | 12m | Done |
| 4 | Form logic | S | 15m | - | In Progress |
| 5 | Validation | S | 10m | - | Pending |

### Commits
- `abc123` feat(payment): add payment types
- `def456` feat(payment): add api mock

### Blockers
- None currently

### Drift Log
- 14:23 - "Also fix footer" -> Added to backlog
```

---

## Stalled Progress Detection

| Condition | Threshold | Action |
|-----------|-----------|--------|
| No progress | > 30 min on one step | Prompt: "Need help?" |
| Repeated attempts | Same step 3x | Suggest: Scout investigation |
| Blocked | External dependency | Suggest: Switch to parallel task |
| Overwhelmed | User reports stuck | Offer: Break down further |

### Stalled Response Template

```markdown
## Progress Check

**Current Step**: [Step Name]
**Time on Step**: 35 minutes (threshold: 30 min)

It looks like this step is taking longer than expected.

**What might help?**
1. **Break down further** - This step might be too big
2. **Scout investigation** - Need more information?
3. **Pair with specialist** - Request Builder/Artisan help
4. **Take a break** - Fresh eyes in 10 minutes
5. **Skip for now** - Move to parallel task, return later
```

---

## Task Tool Integration

Sherpa uses Claude Code's native task management tools to persist progress.

### Automatic Task Creation

When breaking down an Epic, automatically create tasks using `TaskCreate`:

```yaml
On Epic Breakdown:
  1. Create parent task for Epic (if not exists)
  2. Create child tasks for each Atomic Step
  3. Set up dependencies using TaskUpdate (addBlockedBy)
  4. Mark current step as in_progress
```

### Task Lifecycle

```
TaskCreate (pending) -> TaskUpdate (in_progress) -> TaskUpdate (completed)
                              |
                    User works on step
                              |
                    Sherpa monitors progress
```

### Task Metadata

Store Sherpa-specific data in task metadata:

```typescript
TaskCreate({
  subject: "Define PaymentProps interface",
  description: "Create TypeScript interface for payment form props",
  activeForm: "Defining PaymentProps interface",
  metadata: {
    epicId: "payment-flow",
    stepNumber: 1,
    riskLevel: "green",
    estimatedMinutes: 10,
    agent: "Builder",
    parallelWith: [],
    blockedBy: []
  }
})
```

### Resume from Previous Session

```markdown
## Resuming Expedition

**Epic**: Payment Flow
**Last Session**: 2 hours ago
**Progress**: 4/10 steps completed

### Where We Left Off
- Steps 1-4 completed and committed
- Step 5 was in progress (Form validation)
- Steps 6-10 pending

**Resume Options**:
1. **Continue Step 5** (Recommended) - Pick up where you left off
2. **Review completed work** - Check what was done before
3. **Start fresh** - Re-plan remaining steps
```

---

## Dependency Graph

### Dependency Types

| Type | Symbol | Description |
|------|--------|-------------|
| Sequential | `->` | Must complete A before B |
| Parallel | `\|\|` | Can run A and B simultaneously |
| Blocking | `X` | External blocker (approval, API, etc.) |
| Optional | `?` | Can skip if time-constrained |

### Dependency Analysis Template

```markdown
### Step Dependencies

| Step | Depends On | Blocks | Parallel With |
|------|------------|--------|---------------|
| 1. Define types | - | 2, 3 | - |
| 2. Create API mock | 1 | 4 | 3 |
| 3. Build UI skeleton | 1 | 4 | 2 |
| 4. Integrate API | 2, 3 | 5 | - |
| 5. Add error handling | 4 | - | - |

**Critical Path**: 1 -> 2 -> 4 -> 5 (estimated: 45 min)
**Parallelizable**: Steps 2 and 3
**Blockers**: None identified
```

### Visual Dependency Graph

```
Step 1 (Types)
    |
    +---> Step 2 (API Mock) --+
    |                         +---> Step 4 (Integration) ---> Step 5 (Errors)
    +---> Step 3 (UI) --------+
```

---

## Velocity Tracking

Track actual vs estimated time to calibrate future estimates:

```markdown
### Velocity Analysis

**Session Stats**:
- Steps completed: 6
- Total time: 85 minutes
- Average: 14.2 min/step

**Calibration Factor**: 0.95x (slightly faster than estimates)

| Step | Estimated | Actual | Delta |
|------|-----------|--------|-------|
| 1 | 10 min | 8 min | -20% |
| 2 | 15 min | 18 min | +20% |
| 3 | 10 min | 9 min | -10% |

**Pattern Detected**: Faster on familiar tasks, slower on new APIs.
**Adjustment**: Add 1.2x multiplier for API integration steps.
```

---

## Session Retrospective

### Full Retrospective Template

```markdown
## Session Retrospective

**Date**: YYYY-MM-DD
**Duration**: Xh Ym
**Epic**: [Name]

### Progress Summary
- **Started at**: Step N
- **Ended at**: Step M
- **Completed**: X steps
- **Commits**: Y

### Metrics
| Metric | Value | Notes |
|--------|-------|-------|
| Steps/hour | X | Above/below average |
| Avg step time | Y min | On/off estimate |
| Drift incidents | Z | Managed/unmanaged |
| Blockers | N | Resolved/pending |

### What Went Well
- [Positive observation]

### What Slowed Us Down
- [Friction point]

### Learnings for Next Time
- [Actionable insight]

### Tomorrow's Starting Point
**Step**: [Next step name]
**Prep needed**: [Any preparation]
**First action**: [Concrete first action]
```

### Quick Retrospective (Short Sessions)

For sessions < 1 hour:

```markdown
## Quick Retro

**Completed**: Steps X-Y
**Blocked by**: Nothing / [blocker]
**Tomorrow**: Start Step Z
**Note**: [Key observation]
```

---

## Adaptive Pacing

### Pacing Modes

| Mode | When | Step Size | Check-in Frequency |
|------|------|-----------|-------------------|
| **Sprint** | Fresh, deadline pressure | Normal (10-15 min) | After each step |
| **Cruise** | Normal working | Normal | Every 2-3 steps |
| **Recovery** | After blocker/break | Smaller (5-10 min) | After each step |
| **Wind-down** | End of session | Smallest, clean stops | Frequent |

### Auto-Adjust Triggers

```yaml
Increase step size when:
  - Velocity > 1.2x estimate for 3+ steps
  - User requests "faster pace"
  - Simple, repetitive tasks

Decrease step size when:
  - Velocity < 0.8x estimate for 2+ steps
  - Errors or drift increasing
  - Complex/unfamiliar territory
  - User shows fatigue signals

Switch to Wind-down when:
  - Session > 3 hours
  - User mentions "one more thing then done"
  - Approaching natural break point
```
