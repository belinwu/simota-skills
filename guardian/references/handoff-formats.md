# Guardian Handoff Formats Reference

Standardized handoff templates for Guardian agent collaboration.

## PLAN_TO_GUARDIAN_HANDOFF

```markdown
## PLAN_TO_GUARDIAN_HANDOFF

**Task**: [Implementation task name]
**Scope**: [Files/modules affected]

**Planned Changes**:
| File | Change Type | Description |
|------|-------------|-------------|
| src/auth/oauth.ts | feat | OAuth2 provider integration |
| src/api/users.ts | refactor | Extract auth middleware |

**Suggested Branch Name**: [If any from plan]
**Timeline**: [Expected duration]

**Request**:
- Generate optimal branch name
- Propose commit structure
- Recommend PR strategy
```

## GUARDIAN_TO_BUILDER_HANDOFF

```markdown
## GUARDIAN_TO_BUILDER_HANDOFF

**Branch**: [Recommended branch name]
**Commit Strategy**: [Single / Split / Squash]

**Proposed Commits**:
| Order | Message | Files | Reason |
|-------|---------|-------|--------|
| 1 | feat(auth): add OAuth2 provider | oauth.ts, types.d.ts | Core feature |
| 2 | test(auth): add OAuth2 tests | oauth.test.ts | Test coverage |
| 3 | docs(auth): update auth docs | README.md | Documentation |

**PR Strategy**:
- Size: [XS/S/M/L/XL]
- Merge: [Squash/Merge/Rebase]
- Split: [Yes/No - reason]

**Next Steps**:
- [ ] Create branch
- [ ] Implement changes
- [ ] Stage per commit plan
```

## BUILDER_TO_GUARDIAN_HANDOFF

```markdown
## BUILDER_TO_GUARDIAN_HANDOFF

**Branch**: [Current branch name]
**Status**: [Ready for PR / Needs organization]

**Current State**:
- Commits: [N commits]
- Files changed: [N files]
- Lines: +[N]/-[N]

**Staged Changes**:
| File | Status | Description |
|------|--------|-------------|

**Request**:
- Analyze change quality
- Optimize commit structure
- Generate PR description
```

## GUARDIAN_TO_JUDGE_HANDOFF

```markdown
## GUARDIAN_TO_JUDGE_HANDOFF

**Branch**: [branch] → [target]
**PR Title**: [Suggested title]

**Analysis Summary**:
- Essential: [N files]
- Supporting: [N files]
- Noise: [N files - handled]

**Review Focus**:
| Priority | File | Reason |
|----------|------|--------|
| HIGH | src/auth/oauth.ts | Core logic changes |
| MEDIUM | src/api/middleware.ts | Edge case handling |
| LOW | types/auth.d.ts | Type definitions only |

**PR Description**:
[Generated description following template]

**Request**: Review prepared PR for quality issues
```

## JUDGE_TO_GUARDIAN_HANDOFF

```markdown
## JUDGE_TO_GUARDIAN_HANDOFF

**PR**: #[number] - [title]
**Verdict**: [Approved / Changes Requested / Blocked]

**Issues Found**:
| Severity | File | Issue | Recommendation |
|----------|------|-------|----------------|
| HIGH | oauth.ts:45 | Security flaw | Restructure needed |
| MEDIUM | test.ts | Missing coverage | Add tests |

**Restructuring Needed**: [Yes/No]
**Request**: [Reorganize commits / Split PR / Address issues]
```

## GUARDIAN_TO_CANVAS_HANDOFF

```markdown
## GUARDIAN_TO_CANVAS_HANDOFF

**Visualization Type**: [Dependency Graph / Impact Map / Merge Order]

**Data**:
```yaml
nodes:
  - id: "@app/shared"
    changes: 3
    risk: HIGH
  - id: "@app/auth"
    changes: 5
    risk: MEDIUM
edges:
  - from: "@app/auth"
    to: "@app/shared"
    type: "depends_on"
```

**Request**: Generate [Mermaid / ASCII] diagram for PR description
```

## GUARDIAN_TO_SHERPA_HANDOFF

```markdown
## GUARDIAN_TO_SHERPA_HANDOFF

**PR Size**: XL ([N] files, [N] lines)
**Reviewability**: Low

**Suggested Split**:
| PR | Title | Files | Dependencies |
|----|-------|-------|--------------|
| 1 | refactor: restructure auth | 15 | None |
| 2 | feat: add OAuth2 | 25 | PR 1 |
| 3 | test: auth coverage | 20 | PR 2 |

**Request**: Break down into manageable tasks with proper sequencing
```

## ZEN_TO_GUARDIAN_HANDOFF

```markdown
## ZEN_TO_GUARDIAN_HANDOFF

**Cleanup Complete**: [Yes/No]
**Changes Made**:
| Type | Files | Description |
|------|-------|-------------|
| Formatting | 25 | Auto-formatter applied |
| Naming | 3 | Variables renamed |
| Extraction | 2 | Functions extracted |

**Separated Commits**:
- `style: apply formatting` (25 files)
- `refactor: improve naming` (3 files)

**Ready for**: [Re-analysis / PR preparation]
```

## SCOUT_TO_GUARDIAN_HANDOFF

```markdown
## SCOUT_TO_GUARDIAN_HANDOFF

**Investigation**: [Conflict / History / Intent]

**Findings**:
| Aspect | Detail |
|--------|--------|
| Root Cause | [Description] |
| Original Intent | [What the code was meant to do] |
| Conflict Type | [Semantic / Structural / Adjacent] |

**Recommendation**: [How to resolve]
**Confidence**: [HIGH / MEDIUM / LOW]
```

## GUARDIAN_TO_SENTINEL_HANDOFF

```markdown
## GUARDIAN_TO_SENTINEL_HANDOFF

**Branch**: [branch] → [target]
**Security Classification**: CRITICAL

**Critical Changes**:
| File | Change Type | Risk Level |
|------|-------------|------------|
| src/auth/jwt.ts | Token validation | HIGH |
| src/auth/oauth.ts | OAuth provider | MEDIUM |

**Dangerous Patterns Found**:
| File | Pattern | Line | Type |
|------|---------|------|------|
| src/api/query.ts | raw SQL | 45 | Injection |

**Scope of Review**:
- [ ] Authentication flow integrity
- [ ] Token handling security
- [ ] Input validation completeness
- [ ] Secret exposure check

**Request**: Full security audit before PR approval
```

## GUARDIAN_TO_PROBE_HANDOFF

```markdown
## GUARDIAN_TO_PROBE_HANDOFF

**Branch**: [branch] → [target]
**Trigger**: API/Auth endpoint changes detected

**Changed Endpoints**:
| Endpoint | Method | Change Type |
|----------|--------|-------------|
| /api/auth/login | POST | Modified |
| /api/auth/oauth/callback | GET | New |
| /api/users/:id | PATCH | Modified |

**Test Targets**:
- [ ] Authentication bypass attempts
- [ ] Session fixation
- [ ] OAuth state validation
- [ ] Authorization boundary tests

**Request**: DAST scan on staging environment before merge
```

## GUARDIAN_TO_ATLAS_HANDOFF

```markdown
## GUARDIAN_TO_ATLAS_HANDOFF

**Branch**: [branch] → [target]
**Change Scope**: [N] modules affected

**Module Changes**:
| Module | Files Changed | Change Type |
|--------|---------------|-------------|
| @app/shared | 5 | API modification |
| @app/auth | 12 | Consumer update |
| @app/api | 8 | Consumer update |
| @app/web | 3 | Consumer update |

**Concerns**:
- Shared module API change affecting 3 consumers
- New dependency: @app/api → @app/auth (previously independent)

**Request**:
- Dependency graph impact analysis
- Coupling assessment
- Breaking change detection
- ADR recommendation if needed
```

## ATLAS_TO_GUARDIAN_HANDOFF

```markdown
## ATLAS_TO_GUARDIAN_HANDOFF

**Analysis Complete**: [Yes/No]
**Risk Level**: [LOW | MEDIUM | HIGH | CRITICAL]

**Findings**:
| Finding | Severity | Recommendation |
|---------|----------|----------------|
| @app/shared breaking change | HIGH | Version bump required |
| New @app/api→@app/auth coupling | MEDIUM | Consider abstraction |

**ADR Recommendation**:
- ADR-0023: Extract auth interface to prevent circular deps

**Impact on PR Strategy**:
1. Split @app/shared changes into separate PR (merge first)
2. Add abstraction layer before api→auth dependency
```

## Quality Gate Handoffs

### GUARDIAN_TO_JUDGE_HANDOFF (Quality Gate Mode)

```markdown
## GUARDIAN_TO_JUDGE_HANDOFF (Quality Gate)

**Branch**: [branch] → [target]
**PR Title**: [Suggested title]
**Mode**: QUALITY_GATE

**Quality Gate Request**:

### Dependency Changes
| Package | Change | Version | Risk |
|---------|--------|---------|------|
| lodash | Added | ^4.17.21 | LOW |
| crypto-js | Updated | 3.x → 4.x | MEDIUM |

### AI-Suspected Files
| File | Indicators | Confidence |
|------|------------|------------|
| src/utils/parser.ts | Generic naming | 70% |
| src/api/handler.ts | Uniform comments | 60% |

### Verification Checklist
- [ ] Validate dependencies against project requirements
- [ ] Check for hallucinated APIs/methods
- [ ] Verify import usage correctness
- [ ] Confirm breaking change handling

**Request**: Quality gate review before commit structuring
```

### JUDGE_TO_GUARDIAN_HANDOFF (Quality Gate Response)

```markdown
## JUDGE_TO_GUARDIAN_HANDOFF (Quality Gate)

**PR**: #[number] - [title]
**Mode**: QUALITY_GATE_RESPONSE
**Verdict**: [PASSED | ISSUES_FOUND | BLOCKED]

**Dependency Verification**:
| Package | Status | Notes |
|---------|--------|-------|
| lodash | ✓ VALID | Version appropriate |
| crypto-js | ⚠ WARNING | Breaking changes in v4 |

**AI Code Verification**:
| File | Result | Issues |
|------|--------|--------|
| src/utils/parser.ts | ✓ VALID | Logic correct |
| src/api/handler.ts | ⚠ ISSUE | Nonexistent API method used |

**Hallucinations Detected**:
- `handler.ts:45` - `response.sendJSON()` → should be `response.json()`

**Recommendation**: [Fix issues before commit | Proceed with warnings | Block]
```

---

## Extended Handoffs (New Capabilities)

### GUARDIAN_TO_RADAR_HANDOFF

```markdown
## GUARDIAN_TO_RADAR_HANDOFF

**Branch**: [branch] → [target]
**Trigger**: Risk mitigation / Coverage gap

**High-Risk Files Needing Tests**:
| File | Risk Score | Current Coverage | Gap |
|------|------------|------------------|-----|
| src/auth/jwt.ts | 92 | 45% | 55% |
| src/payment/retry.ts | 85 | 60% | 40% |

**Hotspot Files**:
| File | Churn Rate | Bug History | Priority |
|------|------------|-------------|----------|
| src/api/users.ts | 68% | 8 bugs | HIGH |
| src/auth/session.ts | 55% | 5 bugs | MEDIUM |

**Regression Risk**:
- Recent bugs: #456 (token refresh), #472 (session timeout)
- Add regression tests for these scenarios

**Coverage Goals**:
- [ ] Token refresh edge cases
- [ ] Session expiration handling
- [ ] Payment retry scenarios

**Request**: Add tests to mitigate risk before merge
```

### GUARDIAN_TO_ZEN_HANDOFF

```markdown
## GUARDIAN_TO_ZEN_HANDOFF

**Branch**: [branch] → [target]
**Trigger**: Hotspot / Technical debt cleanup

**Hotspot Analysis**:
| File | Type | Churn | Bugs | Recommendation |
|------|------|-------|------|----------------|
| src/api/users.ts | Problem Child | 68% | 8 | Full refactor |
| src/payment/calc.ts | Growing Monster | 71% | 3 | Decompose |
| src/utils/date.ts | Change Magnet | 42% | 2 | Stabilize API |

**Specific Issues**:
1. `users.ts:45-120` - God function, split into smaller units
2. `calc.ts` - 500 lines, extract modules
3. `date.ts` - Inconsistent API, standardize

**Refactoring Goals**:
- [ ] Extract user validation logic
- [ ] Split payment calculations by type
- [ ] Create consistent date formatting API

**Commit Strategy**:
- Refactoring in separate commits before feature
- Tests first approach recommended

**Request**: Clean up hotspots, return with separate refactoring commits
```

### GUARDIAN_QUALITY_REPORT_HANDOFF

```markdown
## GUARDIAN_QUALITY_REPORT_HANDOFF

**Branch**: [branch] → [target]
**PR Title**: [title]

**Quality Score**: {score}/100 ({grade})

### Score Breakdown
| Component | Score | Weight | Notes |
|-----------|-------|--------|-------|
| Size | 85 | 25% | 12 files, 340 lines |
| Focus | 70 | 20% | Related concerns |
| Commits | 80 | 15% | 3 atomic commits |
| Tests | 75 | 15% | Core logic covered |
| Docs | 80 | 10% | API docs updated |
| Risk | 70 | 15% | Auth changes |

### Risk Assessment
**Overall Risk**: 72/100 (HIGH)

| Factor | Score | Primary Concern |
|--------|-------|-----------------|
| Sensitivity | 80 | Auth file changes |
| Complexity | 65 | Moderate logic |
| Hotspots | 75 | 3 hotspot files |
| Dependencies | 60 | Shared utils |
| Coverage | 70 | Core covered |

### Commit Quality
| Commit | Score | Issues |
|--------|-------|--------|
| a1b2c3 | 95 | - |
| d4e5f6 | 25 | Vague message |
| g7h8i9 | 90 | - |

### Branch Health
| Indicator | Status | Score |
|-----------|--------|-------|
| Sync | 12 behind | 75 |
| Age | 8 days | 60 |
| Conflicts | None | 100 |
| CI | Passing | 100 |

### Reviewer Recommendations
| Reviewer | Ownership | Score |
|----------|-----------|-------|
| @alice | 45% | 92 |
| @bob | 32% | 85 |

### Pre-Merge Checklist
- [x] CI passing
- [x] No conflicts
- [ ] Security review (Sentinel)
- [ ] Additional tests needed

### Action Items
1. Rebase onto main
2. Reword commit d4e5f6
3. Complete Sentinel security review
```

### HARVEST_TO_GUARDIAN_HANDOFF (Enhanced)

```markdown
## HARVEST_TO_GUARDIAN_HANDOFF

**Request**: Code ownership data for [files]

**Ownership Data**:
| File | Primary Owner | Secondary | Last Touch |
|------|---------------|-----------|------------|
| src/auth/jwt.ts | @alice (78%) | @bob (15%) | 3 days |
| src/api/users.ts | @bob (55%) | @alice (30%) | 1 day |

**Review Patterns**:
| Reviewer | PRs Reviewed | Avg Response | Quality |
|----------|--------------|--------------|---------|
| @alice | 45 | 4 hours | 95% |
| @bob | 38 | 8 hours | 90% |
| @charlie | 22 | 12 hours | 85% |

**Team Conventions**:
- Commit format: Conventional Commits (87% compliance)
- Branch pattern: `<type>/<issue>-<description>`
- PR size median: 8 files, 180 lines
- Merge strategy: Squash (78%)

**Historical Patterns**:
- Similar changes reviewed by: @alice, @bob
- Average review cycles: 1.8
- Common issues: Missing tests, incomplete docs
```

### HARVEST_TO_GUARDIAN_HANDOFF (Extended - NEW)

**Bidirectional integration with pattern sync, ownership, and history analysis**

```markdown
## HARVEST_TO_GUARDIAN_HANDOFF (Extended)

**Request Type**: FULL_ANALYSIS | PATTERN_SYNC | OWNERSHIP_ONLY | HISTORY_QUERY

---

### Pattern Sync Data

**Historical Issue Patterns** (Last 90 days):
| Pattern | Occurrences | Files | Avg Fix Time |
|---------|-------------|-------|--------------|
| Missing null check | 23 | auth/, api/ | 15 min |
| Incomplete error handling | 18 | api/, services/ | 25 min |
| Magic numbers | 15 | utils/, config/ | 10 min |
| Generic naming | 12 | various | 5 min |

**Pattern Frequency by Directory**:
```yaml
pattern_distribution:
  auth/:
    null_check: 12
    error_handling: 8
    security_issue: 5
  api/:
    error_handling: 10
    validation: 7
    null_check: 6
  services/:
    async_handling: 9
    error_handling: 6
    logging: 4
```

**Seasonal Patterns**:
- Mondays: Higher issue rate (+15%)
- End of sprint: More incomplete PRs
- After release: Focus shifts to bug fixes

---

### Ownership Intelligence

**Code Ownership Graph**:
```yaml
ownership_map:
  src/auth/:
    primary: "@alice"
    secondary: ["@bob", "@charlie"]
    bus_factor: 2
    last_active: "2 days ago"

  src/api/:
    primary: "@bob"
    secondary: ["@alice", "@dave"]
    bus_factor: 3
    last_active: "1 day ago"

  src/payment/:
    primary: "@charlie"
    secondary: ["@alice"]
    bus_factor: 1  # Risk!
    last_active: "5 days ago"
```

**Reviewer Effectiveness**:
| Reviewer | Catch Rate | Response Time | Specialties |
|----------|------------|---------------|-------------|
| @alice | 92% | 4h | Auth, Security |
| @bob | 88% | 6h | API, Performance |
| @charlie | 85% | 8h | Payment, Database |

**Optimal Reviewer Suggestions**:
- For auth changes: @alice (primary), @bob (secondary)
- For API changes: @bob (primary), @alice (secondary)
- For payment: @charlie (required), @alice (coverage)

---

### Historical Analysis

**Similar PRs Analysis**:
| PR | Title | Similarity | Cycles | Outcome |
|----|-------|------------|--------|---------|
| #98 | feat(auth): add SSO | 85% | 2 | Merged |
| #76 | feat(auth): OAuth refresh | 78% | 3 | Merged |
| #45 | feat(auth): token rotation | 72% | 2 | Merged |

**Common Issues in Similar PRs**:
1. Token expiration edge cases (found in 3/3)
2. Error response formatting (found in 2/3)
3. Missing integration tests (found in 2/3)

**Predicted Review Outcome**:
- Expected cycles: 2.3
- Likely issues: Token edge cases, test coverage
- Recommended focus: Error handling, integration tests

---

### Quality Baseline

**Project Quality Trends**:
```yaml
quality_baseline:
  avg_quality_score: 74
  avg_risk_score: 52
  avg_review_cycles: 1.8
  merge_rate: 94%
  rollback_rate: 2%
```

**Directory-Specific Baselines**:
| Directory | Avg Quality | Avg Risk | Typical Issues |
|-----------|-------------|----------|----------------|
| auth/ | 72 | 68 | Security, tests |
| api/ | 78 | 45 | Validation, docs |
| ui/ | 82 | 35 | A11y, styling |
| core/ | 70 | 72 | Complexity, deps |

**Calibration Recommendations**:
- Quality score threshold: 74 (project average)
- Risk threshold: 52 (project average)
- Adjust for directory-specific baselines

---

### Learning Data Feed

**Recent Judge Findings** (Last 30 days):
| Finding Type | Count | Guardian Predicted | Accuracy |
|--------------|-------|-------------------|----------|
| Null pointer | 15 | 12 | 80% |
| Error handling | 18 | 14 | 78% |
| Security issue | 5 | 5 | 100% |
| Magic number | 8 | 10 | 80% |

**Pattern Drift Detection**:
- New pattern emerging: "Promise chain without finally"
- Declining pattern: "var instead of const" (0 in 30 days)
- Stable patterns: Most naming and structure issues

**Recommended Calibrations**:
1. Add "Promise chain without finally" to detection
2. Remove/lower "var usage" pattern weight
3. Increase "error handling" pattern sensitivity

```

### GUARDIAN_TO_HARVEST_HANDOFF (Feedback Loop)

**Return calibration and accuracy data to Harvest for tracking**

```markdown
## GUARDIAN_TO_HARVEST_HANDOFF

**Type**: PREDICTION_TRACKING | CALIBRATION_UPDATE

---

### Prediction Results (for this PR)

**Predictions Made**:
| Prediction | Confidence | Actual Outcome |
|------------|------------|----------------|
| Null pointer oauth.ts:45 | 85% | Confirmed |
| Race condition token.ts | 75% | False positive |
| Missing tests callback.ts | 80% | Confirmed |

**Accuracy Summary**:
- True Positives: 8
- False Positives: 2
- False Negatives: 1
- Accuracy: 72.7%

---

### Calibration Updates Applied

**Weight Adjustments**:
| Pattern | Previous | New | Reason |
|---------|----------|-----|--------|
| race_condition | 75% | 70% | FP in this codebase |
| null_pointer | 85% | 88% | Consistent TP |

**New Exceptions Added**:
| Pattern | Scope | Reason |
|---------|-------|--------|
| magic_numbers | constants/*.ts | Intentional definitions |
| generic_names | **/*.test.ts | Test convention |

---

### Quality Correlation

**Predicted vs Actual**:
- Predicted Quality: 78
- Actual Review Cycles: 2
- Predicted Risk: 65
- Actual Issues: 3 medium

**Correlation Notes**:
- Quality prediction was accurate (within 10%)
- Risk prediction was slightly low
- Recommend increasing risk weight for auth changes

```

### GUARDIAN_BRANCH_HEALTH_HANDOFF

```markdown
## GUARDIAN_BRANCH_HEALTH_HANDOFF

**Branch**: [branch]
**Target**: [target]

**Health Score**: {score}/100 ({grade})

### Status Summary
| Indicator | Status | Value | Action |
|-----------|--------|-------|--------|
| Sync | Warning | 12 behind | Rebase needed |
| Age | Warning | 8 days | Merge soon |
| Conflicts | Healthy | None | - |
| CI | Healthy | Passing | - |
| Size | Warning | Growing | Consider split |

### Timeline
```
main ────●────●────●────●────●────●────●──── HEAD
         │
         └────●────●────●────●────● [branch]
              ↑                   ↑
           Created             12 behind
```

### Recommended Actions
1. `git fetch origin main && git rebase origin/main`
2. Consider splitting (45 files)
3. Complete review within 3 days

### Conflict Prediction
No conflicts expected.
Watch: `src/api/middleware.ts` (active in main)
```
