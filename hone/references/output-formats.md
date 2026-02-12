# Output Formats

## Cycle Start Report

```markdown
## Hone Cycle {N} - PLAN Phase

### Current Quality State
| Domain | Agent | Score | Target | Gap |
|--------|-------|-------|--------|-----|
| Code Correctness | Judge | 70 | 85 | 15 |
| Complexity | Zen | 65 | 80 | 15 |
| Test Coverage | Radar | 55 | 75 | 20 |
| Documentation | Quill | 80 | 80 | 0 |

### UQS Summary
- **Current UQS**: 67.5 (Fair)
- **Target UQS**: 80 (Good)
- **Gap**: 12.5 points

### Improvement Plan
1. [Priority: HIGH] Run Judge → Builder to fix 2 HIGH issues
2. [Priority: MEDIUM] Run Radar to add tests for uncovered logic
3. [Priority: MEDIUM] Run Zen to reduce complexity in core module

### Agents Selected
- Judge (analysis) → Builder (fixes)
- Radar (test addition)
- Zen (simplification)
```

## Cycle End Report

```markdown
## Hone Cycle {N} - CHECK Phase

### Before/After Comparison
| Domain | Before | After | Delta | Status |
|--------|--------|-------|-------|--------|
| Code Correctness | 70 | 85 | +15 | Improved |
| Complexity | 65 | 78 | +13 | Improved |
| Test Coverage | 55 | 72 | +17 | Improved |
| Documentation | 80 | 80 | 0 | Unchanged |

### UQS Progress
- **Before**: 67.5 (Fair)
- **After**: 79.2 (Acceptable)
- **Delta**: +11.7 points
- **Target**: 80 (Good)
- **Remaining Gap**: 0.8 points

### Actions Completed
- [x] Judge: Found 2 HIGH, 1 MEDIUM issues
- [x] Builder: Fixed 2 HIGH issues
- [x] Radar: Added 5 test cases, coverage +17%
- [x] Zen: Reduced avgCC from 15 to 11

### ACT Decision
**Continue**: Target not met (79.2 < 80), but improving (+11.7 delta)
```

## Session End Report

```markdown
## Hone Session Complete

### Summary
| Metric | Start | End | Total Delta |
|--------|-------|-----|-------------|
| UQS | 67.5 | 81.3 | +13.8 |
| Cycles | - | 2 | - |
| Termination | - | Goal achieved | - |

### Cumulative Improvements
- **Judge**: 3 issues found → 3 fixed
- **Zen**: avgCC 15 → 10 (-33%)
- **Radar**: coverage 55% → 78% (+23%)
- **Quill**: no changes needed

### Quality Journey
Cycle 1: 67.5 ──+11.7──▶ 79.2
Cycle 2: 79.2 ──+2.1───▶ 81.3 (Target: 80)

### Termination Reason
**Goal Achieved**: UQS 81.3 exceeds target 80.

### Learnings Recorded
- Pattern: High complexity correlates with low coverage
- Recommendation: Run Zen before Radar in future sessions
```

## History Recording

Record session history in `.agents/hone.md`:

```markdown
# Hone Session History

## Session: 2024-01-15T10:30:00Z

### Configuration
- Mode: STANDARD
- Target UQS: 80
- Max Cycles: 3
- Domains: code, tests

### Timeline
| Cycle | Start UQS | End UQS | Delta | Duration |
|-------|-----------|---------|-------|----------|
| 1 | 65.0 | 76.5 | +11.5 | 4:32 |
| 2 | 76.5 | 81.2 | +4.7 | 3:15 |

### Termination
- Reason: Goal achieved (81.2 >= 80)
- Total cycles: 2

### Learnings
- Pattern: Judge → Zen → Radar order most effective
- Note: Complexity reduction enabled better test coverage
```

## Examples

### Example 1: Standard Improvement Session

```
User: "Improve the quality of the auth module"

Hone:
  PLAN (Cycle 1):
    - Run Judge on src/auth/ → Found 1 CRITICAL, 2 HIGH
    - Run Radar analysis → Coverage at 45%
    - Run Zen analysis → avgCC = 18
    - Initial UQS: 52 (Poor)
    - Target: 80 (STANDARD mode)

  DO (Cycle 1):
    - Route to Builder: Fix CRITICAL null check
    - Route to Builder: Fix HIGH validation issues
    - Route to Radar: Add tests for auth flows
    - Route to Zen: Simplify complex functions

  CHECK (Cycle 1):
    - Judge: 0 CRITICAL, 0 HIGH (fixed)
    - Coverage: 67% (+22%)
    - avgCC: 12 (-33%)
    - UQS: 71 (+19)
    - Delta: +19 (significant improvement)

  ACT (Cycle 1):
    - Continue: 71 < 80, delta is meaningful

  [Cycle 2...]

  CHECK (Cycle 2):
    - UQS: 82 (+11)

  ACT (Cycle 2):
    - TERMINATE: Goal achieved (82 >= 80)
```

### Example 2: Diminishing Returns Detection

```
User: "Keep improving until perfect"

Hone:
  Mode: INTENSIVE (max 5 cycles, target 90)

  Cycle 1: 60 → 75 (+15) - Continue
  Cycle 2: 75 → 83 (+8) - Continue
  Cycle 3: 83 → 86 (+3) - Warning: delta < 5%
  Cycle 4: 86 → 87 (+1) - Diminishing returns detected

  TERMINATE: 2 consecutive cycles with delta < 5%
  Final UQS: 87 (Good)

  Recommendation: Further improvement requires architectural
  changes beyond iterative refinement. Consider Atlas for
  structural analysis.
```

### Example 3: Domain-Focused Session

```
User: "Focus only on test coverage"

Hone:
  Mode: STANDARD (test-focused weights)
  Domains: [tests]

  UQS Weights (adjusted):
    - Radar: 0.70
    - Judge: 0.20
    - Quill: 0.10

  PLAN:
    - Current coverage: 55%
    - Target coverage: 80%
    - Agents: Radar (primary), Judge (verify test quality)

  [Execute focused improvement...]

  Result:
    - Coverage: 55% → 82%
    - Test-focused UQS: 64 → 85
```

## Error Handling

### Agent Failure Recovery

| Failure Type | Recovery Action |
|--------------|-----------------|
| Agent timeout | Skip agent, note in report, continue cycle |
| Agent error | Retry once, then skip with warning |
| Breaking change detected | Pause cycle, ask user |
| Build failure after fix | Revert to checkpoint, report blocker |
| All agents fail | Terminate with BLOCKED status |

### Quality Measurement Failure

| Failure | Fallback |
|---------|----------|
| Coverage tool unavailable | Use file-level heuristics |
| Complexity tool fails | Skip Zen scoring |
| Warden unavailable | Skip UX scoring (if not UI-focused) |

## Boundaries Checklist

Before starting a session:
- [ ] Target files exist and are accessible
- [ ] At least one quality agent is available
- [ ] Test framework is configured (if including tests)
- [ ] UQS baseline can be measured

Before each cycle:
- [ ] Previous cycle's learnings are recorded
- [ ] Baseline measurement is complete
- [ ] Agent order is determined

Before termination:
- [ ] Termination reason is documented
- [ ] Before/After summary is generated
- [ ] History is recorded in `.agents/hone.md`
- [ ] HONE_COMPLETE format is prepared (if Nexus-invoked)
