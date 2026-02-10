# Radar Handoff Formats

Standardized handoff templates for agent collaboration.

---

## Input Handoffs (→ Radar)

### SCOUT_TO_RADAR_HANDOFF

```markdown
## SCOUT_TO_RADAR_HANDOFF

**Bug Investigated**: [Bug description]
**Root Cause**: [Root cause analysis]
**Affected Code**: [File:line references]

**Reproduction Steps**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Regression Test Request**:
- Test the fix: [What to verify]
- Edge cases: [Related scenarios to cover]
- Boundary values: [Specific values to test]

**Request**: Write regression test preventing this bug from recurring
```

### SHOWCASE_TO_RADAR_HANDOFF

```markdown
## SHOWCASE_TO_RADAR_HANDOFF

**Story Coverage Report**:
| Component | Stories | Play Tests | A11y |
|-----------|---------|------------|------|
| [Component] | [N] | [N] | [Status] |

**Gap Analysis**:
- Play functions cover: [user interactions]
- Unit tests should cover: [business logic, edge cases]
- Missing test scenarios: [specific suggestions]

**Flaky Test Warning**:
- Animation timing may affect snapshot tests
- prefers-reduced-motion variant should be tested

**Request**: Add component-level tests to complement story coverage
```

### ZEN_TO_RADAR_HANDOFF

```markdown
## ZEN_TO_RADAR_HANDOFF

**Refactoring Planned**: [Description of refactoring]
**Files Affected**: [List of files]

**Pre-Refactor Verification**:
- Current behavior to preserve: [behaviors]
- Edge cases to verify: [edge cases]
- Test coverage before: [X%]

**Request**: Verify existing tests pass, add missing coverage before refactoring begins
```

### BUILDER_TO_RADAR_HANDOFF

```markdown
## BUILDER_TO_RADAR_HANDOFF

**Feature Implemented**: [Description]
**Files Changed**:
| File | Change |
|------|--------|
| [path] | [what changed] |

**Test Requirements**:
- Business logic to test: [rules]
- Error handling to verify: [error scenarios]
- Integration points: [API/DB interactions]

**Request**: Add unit and integration tests for new feature
```

### FLOW_TO_RADAR_HANDOFF

```markdown
## FLOW_TO_RADAR_HANDOFF

**Animation Added**: [Description]
**Files Changed**:
| File | Change |
|------|--------|
| [path] | [what changed] |

**Test Considerations**:
- Animation timing may affect snapshot tests
- prefers-reduced-motion variant should be tested
- Visual regression: compare with/without animation

**Potential Flaky Points**:
- Timing-dependent assertions
- Viewport-dependent animations

**Request**: Verify no visual regression, add animation-aware tests if needed
```

---

## Output Handoffs (Radar →)

### RADAR_TO_VOYAGER_HANDOFF

```markdown
## RADAR_TO_VOYAGER_HANDOFF

**Unit/Integration Coverage**:
| Area | Tests | Coverage |
|------|-------|----------|
| [Module] | [N] | [X%] |

**E2E Test Needed**:
- User journey: [Description]
- Critical path: [Steps]
- Cross-page flows: [pages involved]

**Boundary**:
- Radar: Single function/component tests (completed)
- Voyager: Multi-page user journeys (requested)

**Request**: Create E2E tests for critical user journeys
```

### RADAR_TO_GEAR_HANDOFF

```markdown
## RADAR_TO_GEAR_HANDOFF

**Test Infrastructure Issue**: [Description]
**Current Config**:
| Setting | Value | Issue |
|---------|-------|-------|
| [config] | [value] | [problem] |

**CI Impact**:
- Test execution time: [current → desired]
- Flaky test rate: [X%]
- Parallelization: [current state]

**Request**: Optimize CI test pipeline configuration
```

### RADAR_TO_ZEN_HANDOFF

```markdown
## RADAR_TO_ZEN_HANDOFF

**Test Code Quality Issues**:
| File | Issue | Severity |
|------|-------|----------|
| [path] | Duplicate setup code | Medium |
| [path] | Mixed concerns in single test | High |
| [path] | Overly complex test helpers | Low |

**Refactoring Suggestions**:
- Extract shared fixtures to factory pattern
- Split large test files by concern
- Simplify nested describe blocks

**Request**: Refactor test code for readability and maintainability
```

### RADAR_TO_JUDGE_HANDOFF

```markdown
## RADAR_TO_JUDGE_HANDOFF

**Tests Written**: [Count and description]
**Coverage Change**: [X% → Y%]
**Files Changed**:
| File | Tests Added | Coverage |
|------|-------------|----------|
| [path] | [N] | [X%] |

**Review Focus Areas**:
- Mock strategy: [appropriate?]
- Edge case coverage: [sufficient?]
- Test naming: [clear and descriptive?]

**Request**: Review test quality and coverage effectiveness
```

### RADAR_TO_SHOWCASE_HANDOFF

```markdown
## RADAR_TO_SHOWCASE_HANDOFF

**Component Tests Added**:
| Component | Tests | Coverage | Behavior Tested |
|-----------|-------|----------|-----------------|
| [name] | [N] | [X%] | [behaviors] |

**Story Suggestions**:
- Components with complex state: [list]
- Error states discovered: [list]
- Edge cases worth visualizing: [list]

**Request**: Create stories showcasing tested states and edge cases
```

---

## Collaboration Patterns

### Pattern A: Bug Fix Verification
```
Scout (investigation) → SCOUT_TO_RADAR → Radar (regression test) → RADAR_TO_JUDGE → Judge (review)
```

### Pattern B: Pre-Refactor Safety Net
```
Zen (refactoring plan) → ZEN_TO_RADAR → Radar (verify + add tests) → Zen (refactor) → Radar (re-verify)
```

### Pattern C: Story-to-Test Sync
```
Showcase (story coverage) → SHOWCASE_TO_RADAR → Radar (unit tests) → RADAR_TO_SHOWCASE → Showcase (update stories)
```

### Pattern D: New Feature Testing
```
Builder (implementation) → BUILDER_TO_RADAR → Radar (tests) → RADAR_TO_VOYAGER → Voyager (E2E)
```

### Pattern E: Animation Test Safety
```
Flow (animation) → FLOW_TO_RADAR → Radar (verify no regression) → RADAR_TO_SHOWCASE → Showcase (animation stories)
```

### Pattern F: Test Quality Cycle
```
Radar (write tests) → RADAR_TO_JUDGE → Judge (review) → Radar (fix issues) → RADAR_TO_ZEN → Zen (refactor tests)
```

### Pattern G: CI Pipeline Optimization
```
Radar (slow/flaky tests) → RADAR_TO_GEAR → Gear (CI optimization) → Radar (verify improvements)
```

### Pattern H: Coverage-Driven Development
```
Radar (audit) → RADAR_TO_SHOWCASE → Showcase (stories) → SHOWCASE_TO_RADAR → Radar (tests) → RADAR_TO_VOYAGER → Voyager (E2E)
```

### Pattern I: Judge Quality Sync
```
Judge (TQ review) → JUDGE_TO_RADAR → Radar (fix findings) → RADAR_TO_JUDGE → Judge (re-review)
```

---

## Judge Integration

### JUDGE_TO_RADAR_HANDOFF (Input)

```markdown
## JUDGE_TO_RADAR_HANDOFF

**Review Result**: [TQ-xxx findings]
**Files Reviewed**:
| File | Findings | Severity |
|------|----------|----------|
| [path] | [TQ-xxx: description] | [HIGH/MEDIUM/LOW] |

**Action Required**:
| Finding | TQ Code | Action | Priority |
|---------|---------|--------|----------|
| [description] | [TQ-xxx] | [fix action] | [HIGH/MED/LOW] |

**Request**: Address test quality findings from Judge review
```

### Edge Case Response Catalog

Judge が「missing edge cases」(TQ-005) を指摘した場合の Radar アクション対応表:

| Judge Finding | Radar Action | Example |
|---------------|-------------|---------|
| Missing null/undefined input | Add null guard test | `expect(() => fn(null)).toThrow()` |
| Missing error path | Add error scenario test | `mockApi.mockRejectedValue(new Error())` |
| Missing boundary value | Add boundary test | `expect(validate(0)).toBe(false)` / `expect(validate(1)).toBe(true)` |
| Missing concurrent scenario | Add parallel test | `Promise.all([op1(), op2()])` race test |
| Missing empty collection | Add empty input test | `expect(process([])).toEqual([])` |
| Missing large input | Add stress test | `expect(process(Array(10000))).not.toThrow()` |

### Over-Mocking Response Catalog

Judge が「over-mocking」(TQ-003) を指摘した場合の Radar アクション対応表:

| Judge Finding | Radar Action | Approach |
|---------------|-------------|----------|
| Internal function mocked | Use DI or test public API | Remove mock, test through public interface |
| Too many mocks (>3) | Simplify or use integration test | Reduce mocks, consider Testcontainers |
| Mock returns hardcoded data | Use factory/builder pattern | `createMockUser()` instead of inline object |
| Mock verifies call count | Assert on behavior/output | Replace `toHaveBeenCalledTimes` with output assertion |
| Implementation detail tested | Test behavior only | Focus on return values and side effects |
