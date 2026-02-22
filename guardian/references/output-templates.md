# Guardian Output Templates

> Guardian が生成する各種レポートのテンプレート集。
> SKILL.md の各セクションから参照される。

---

## Section 1: Change Analysis Report

```markdown
## Guardian Change Analysis

**Branch:** `feat/user-auth` → `main`
**Changes:** 47 files, +1,234/-567 lines

### Signal/Noise Breakdown
```
Essential:    ████████░░ 80% (12 files)
Supporting:   █░░░░░░░░░ 10% (5 files)
Incidental:   █░░░░░░░░░ 10% (30 files)
```

### Essential Changes (Review Priority: HIGH)
| File | Change Type | Summary |
|------|-------------|---------|
| `src/auth/oauth.ts` | feat | OAuth2 provider integration |
| `src/api/users.ts` | fix | Rate limiting implementation |

### Supporting Changes
- `tests/auth/oauth.test.ts` - Tests for OAuth2 flow
- `types/auth.d.ts` - Type definitions

### Noise (Consider Separating)
- 28 files - Import reordering (auto-formatter)
- `package-lock.json` - 2,847 lines (dependency update)

...
```

---

## Section 2: PR Quality Score Report

```markdown
## PR Quality Score: 78/100 (Good)

### Component Breakdown
```
Size:          ████████░░ 85/100  (12 files, 340 lines)
Focus:         ███████░░░ 70/100  (Related concerns: auth + API)
Commits:       ████████░░ 80/100  (3 atomic, conventional)
Tests:         ███████░░░ 75/100  (Core logic covered)
Documentation: ████████░░ 80/100  (API docs updated)
Risk:          ███████░░░ 70/100  (Auth changes - moderate risk)
```

### Grade: B+

### Improvement Suggestions
1. Split auth and API changes into separate PRs (+10 focus)
2. Add edge case tests for token refresh (+5 tests)
```

### Scoring Calculation Details

```yaml
quality_scoring:
  size_score:
    100: files <= 5 AND lines <= 100
    90: files <= 10 AND lines <= 200
    75: files <= 20 AND lines <= 400
    50: files <= 50 AND lines <= 800
    25: files <= 100 AND lines <= 1500
    0: files > 100 OR lines > 1500

  focus_score:
    100: single_concern AND single_type
    80: single_concern AND multiple_types
    60: related_concerns
    40: loosely_related
    20: multiple_unrelated
# ...
```

---

## Section 3: Commit Message Analysis Report

```markdown
## Commit Message Analysis

**Branch:** `feat/user-auth`
**Commits:** 5

### Message Quality Scores
| Commit | Subject | Score | Issues |
|--------|---------|-------|--------|
| `a1b2c3` | feat(auth): add OAuth2 provider | 95 | - |
| `d4e5f6` | fix stuff | 25 | Vague, no type |
| `g7h8i9` | WIP | 0 | WIP commit |
| `j0k1l2` | test(auth): add OAuth tests | 90 | - |
| `m3n4o5` | update deps | 40 | No type, vague |

### Average Score: 50/100 (Needs Work)
...
```bash
git rebase -i HEAD~5
# pick a1b2c3 feat(auth): add OAuth2 provider
# squash g7h8i9 WIP
# reword d4e5f6 fix(auth): resolve token refresh race condition
# pick j0k1l2 test(auth): add OAuth tests
# reword m3n4o5 chore(deps): upgrade oauth2-client to v2.0
```
```

### Message Quality Patterns

```yaml
commit_message_analysis:
  excellent_patterns:
    - type(scope): imperative verb + concise description
    - Body explains motivation and context
    - References related issues
    - Breaking changes clearly marked

  warning_patterns:
    - Vague subjects: "fix bug", "update code", "changes"
    - Past tense: "fixed", "added", "updated"
    - Missing type prefix
    - Overly long subject (>72 chars)
    - No body for complex changes

  error_patterns:
# ...
```

---

## Section 4: Risk Assessment Report

```markdown
## Change Risk Assessment

**Branch:** `feat/payment-retry` → `main`
**Overall Risk Score:** 72/100 (HIGH)

### Risk Breakdown
```
File Sensitivity:   █████████░ 90/100  (Payment handling)
Change Complexity:  ██████░░░░ 60/100  (Moderate logic)
Hotspot Overlap:    ████████░░ 80/100  (3 hotspot files)
Dependency Impact:  ██████░░░░ 55/100  (Shared utils)
Test Coverage:      ███████░░░ 70/100  (Core covered)
Author Familiarity: ██████░░░░ 60/100  (Some ownership)
```

### High-Risk Files
| File | Risk Score | Reason |
|------|------------|--------|
| `src/payment/retry.ts` | 95 | Payment logic, hotspot |
| `src/payment/processor.ts` | 85 | Core payment, shared |
| `src/utils/currency.ts` | 70 | Used by 12 modules |

### Risk Mitigation Recommendations
1. **Add Sentinel review** - Payment logic requires security audit
2. **Increase test coverage** - Add retry edge cases (+15% coverage)
3. **Staged rollout** - Deploy to 10% initially, monitor errors
4. **Prepare rollback** - Feature flag for instant disable

### Regression Risk
...
```

---

## Section 5: Hotspot Detection Report

```markdown
## Hotspot Analysis

**Repository:** `my-app`
**Analysis Period:** Last 90 days

### Top Hotspots
| Rank | File | Changes | Churn | Bugs | Type |
|------|------|---------|-------|------|------|
| 1 | `src/api/users.ts` | 47 | 68% | 8 | Problem Child |
| 2 | `src/utils/date.ts` | 35 | 42% | 2 | Change Magnet |
| 3 | `src/auth/session.ts` | 28 | 55% | 5 | Problem Child |
| 4 | `src/payment/calc.ts` | 22 | 71% | 3 | Growing Monster |
| 5 | `src/core/engine.ts` | 18 | 25% | 1 | Knowledge Silo |

### Hotspot Visualization
```
Changes in Last 90 Days
src/api/users.ts      ████████████████████████████████████████████████ 47
src/utils/date.ts     ████████████████████████████████████ 35
src/auth/session.ts   █████████████████████████████ 28
src/payment/calc.ts   ███████████████████████ 22
src/core/engine.ts    ███████████████████ 18
```

### Current PR Impact
**This PR modifies 3 hotspot files:**
- `src/api/users.ts` (Problem Child) - Adding more logic
- `src/auth/session.ts` (Problem Child) - Modifying core
- `src/payment/calc.ts` (Growing Monster) - New calculations

### Recommendations
1. **Prioritize** `src/api/users.ts` for refactoring
   - 8 bugs in 90 days indicates design issues
   - Handoff to Zen for cleanup

2. **Decompose** `src/payment/calc.ts`
   - 71% churn rate is unsustainable
   - Handoff to Atlas for architecture review
...
```

---

## Section 6: Reviewer Recommendation Report

```markdown
## Reviewer Recommendations

**PR:** feat/payment-retry
**Files Changed:** 12

### Recommended Reviewers

| Priority | Reviewer | Ownership | Load | Expertise | Score |
|----------|----------|-----------|------|-----------|-------|
| 1 | @alice | 45% | 2 PRs | Payment | 92 |
| 2 | @bob | 32% | 1 PR | Auth, API | 85 |
| 3 | @charlie | 18% | 3 PRs | Testing | 72 |

### File Ownership Map
```
src/payment/retry.ts      @alice (78%), @bob (15%)
src/payment/processor.ts  @alice (65%), @david (20%)
src/api/payment.ts        @bob (55%), @alice (30%)
src/utils/currency.ts     @charlie (40%), @eve (35%)
```

### Review Assignment Suggestion

**Primary Reviewer:** @alice
- Highest ownership in payment files
- Domain expert in payment processing
- Low current review load

**Secondary Reviewer:** @bob
- API layer expertise
- Complements @alice's payment focus
- Can review integration points

### Code Coverage by Reviewers
With @alice + @bob: 87% of changed files have expert reviewer
```

### Ownership Scoring

```yaml
ownership_scoring:
  recent_commits:
    weight: 0.5
    decay: exponential
    window: 180_days
  historical_commits:
    weight: 0.3
    window: all_time
  review_history:
    weight: 0.2
    window: 90_days
```

---

## Section 7: Branch Health Report

```markdown
## Branch Health Report

**Branch:** `feat/user-auth`
**Created:** 8 days ago
**Last Commit:** 2 days ago

### Health Score: 65/100 (Warning)

### Status Indicators
| Indicator | Status | Value | Recommendation |
|-----------|--------|-------|----------------|
| Sync with main | Warning | 12 behind | Rebase soon |
| Branch age | Warning | 8 days | Complete or split |
| Conflict risk | Healthy | Low | - |
| CI status | Healthy | Passing | - |
...
```
main ─────●────●────●────●────●────●────●────●────●────●────●────● HEAD
          │
          └────●────●────●────●────●────● feat/user-auth
               ↑                        ↑
            Branch point            12 commits behind
```

### Recommendations
1. **Rebase onto main**
   ```bash
   git fetch origin main
   git rebase origin/main
   ```

2. **Consider splitting** - Branch has grown to 45 files
   - Core auth: 20 files (ship first)
   - OAuth providers: 15 files (separate PR)
   - Tests: 10 files (with OAuth)

3. **Update timeline** - 8 days old, merge soon or split

...
```

---

## Section 8: Pre-Merge Checklist

```markdown
## Pre-Merge Checklist

**PR:** #123 - feat(auth): add OAuth2 support
**Target:** main
**Risk Level:** HIGH

### Required (Must Complete)
- [x] CI pipeline passing
- [x] No merge conflicts
- [x] 2+ approvals obtained
- [x] All conversations resolved

### Security (Required for this PR)
- [ ] Sentinel security review complete
- [ ] No hardcoded credentials
...
```

---

## Section 9: Repository Pattern Report

```markdown
## Repository Pattern Analysis

**Repository:** `my-app`
**Analyzed:** Last 500 commits, 150 PRs

### Commit Message Patterns

**Detected Format:** Conventional Commits
**Compliance Rate:** 87%

**Common Scopes:**
| Scope | Usage | Description |
|-------|-------|-------------|
| auth | 23% | Authentication |
| api | 19% | API endpoints |
...
```
<type>(<scope>): <subject>

<body>

Closes #<issue>
```

### Branch Naming Pattern

**Detected Pattern:** `<type>/<issue>-<description>`
**Examples:**
- `feat/123-user-authentication`
- `fix/456-login-timeout`

**Generated Regex:** `^(feat|fix|chore|docs|refactor)/\d+-[a-z-]+$`

### PR Size Calibration

**Team's Typical PR:**
- Median: 8 files, 180 lines
- 75th percentile: 15 files, 400 lines
...
```

### Pattern Learning Configuration

```yaml
pattern_extraction:
  commit_messages:
    analyze: [type prefixes, scope naming, subject length, body frequency]
    output: [detected format, common scopes, recommended template]

  branch_naming:
    analyze: [prefix patterns, separator style, issue reference, case convention]
    output: [detected pattern regex, naming template]

  pr_sizing:
    analyze: [median files, median lines, 90th percentile, team tolerance]
    output: [calibrated thresholds, project-specific recommendations]
```

---

## Section 10: Commit Split Plan

```markdown
## Current: 1 commit with 47 files

### Recommended Split:

| Order | Commit | Files | Reason |
|-------|--------|-------|--------|
| 1 | `feat(auth): add OAuth2 provider integration` | 8 | Core feature |
| 2 | `test(auth): add OAuth2 integration tests` | 4 | Test coverage |
| 3 | `docs(auth): update authentication docs` | 2 | Documentation |
| 4 | `style: apply auto-formatter changes` | 33 | Formatting only |

### Git Commands to Execute:
```bash
# Unstage all
git reset HEAD

# Stage and commit OAuth feature
git add src/auth/oauth.ts src/auth/providers/* types/auth.d.ts
git commit -m "feat(auth): add OAuth2 provider integration"

# Stage and commit tests
git add tests/auth/
git commit -m "test(auth): add OAuth2 integration tests"

# Continue for remaining commits...
```
```

---

## Section 11: Squash Optimization Report

```markdown
## Squash Optimization Report

**Branch:** `{branch}` → `{target}`
**Original Commits:** {original_count}
**Optimized Commits:** {optimized_count}

### Before / After
```
Before: ████████████████████ {original_count} commits
After:  ████████░░░░░░░░░░░░ {optimized_count} commits  ({reduction_pct}% reduction)
```

### Squash Groups

| Group | Action | Commits | Files | Result Message |
|-------|--------|---------|-------|----------------|
| 1 | squash | `{hash1}`, `{hash2}` | 5 | `feat(auth): add OAuth2 provider` |
| 2 | fixup | `{hash3}` → `{hash1}` | 2 | _(absorbed into Group 1)_ |
| 3 | pick | `{hash4}` | 3 | `test(auth): add OAuth2 tests` |
| 4 | pick | `{hash5}` | 1 | `chore(deps): update lock file` |

### Decision Rationale

| Group | Score | Key Factors |
|-------|-------|-------------|
| 1 | +42 | temporal_proximity(+12), subject_relationship(+25), file_overlap(+15), same_author(+15), atomicity(-10), test_coupling(-15) |
| 2 | +55 | fixup! prefix(force), file_overlap(+20), same_author(+15), temporal(+15) |
| 3 | -18 | different_concern(-25), no_overlap(-5), standalone_test(-5), same_author(+15) |

### Synthesized Commit Messages

**Group 1:**
```
feat(auth): add OAuth2 provider integration

Implement OAuth2 flow with support for Google and GitHub providers.
Token refresh handles concurrent requests via mutex lock.

Closes #123
Co-authored-by: Alice <alice@example.com>
```

**Group 3:** _(keep original)_
```
test(auth): add OAuth2 integration tests
```

### Rebase Script (Ready to Paste)

```bash
# Run: git rebase -i $(git merge-base HEAD main)
# Then replace the todo list with:
pick {hash1} feat(auth): add OAuth2 provider integration
fixup {hash3} fix typo in oauth config
squash {hash2} add token refresh mechanism
pick {hash4} test(auth): add OAuth2 integration tests
pick {hash5} chore(deps): update lock file
```

### Post-Squash Verification Checklist

- [ ] Commit count matches plan: {optimized_count}
- [ ] `git diff backup/{branch}-pre-squash..HEAD` is empty
- [ ] All authors attributed (Co-authored-by present)
- [ ] All issue references preserved
- [ ] `git rebase --exec 'npm run build' $(git merge-base HEAD main)` passes
- [ ] CI pipeline passes on rebased branch
```

---

## Section 12: PR Split Strategy

```markdown
## PR Analysis: 73 files, 2,847 lines (Size: XL)

### Recommended Split:

| PR | Title | Files | Lines | Dependencies |
|----|-------|-------|-------|--------------|
| 1 | `refactor(auth): restructure auth module` | 15 | ~400 | None |
| 2 | `feat(auth): add OAuth2 support` | 25 | ~800 | PR 1 |
| 3 | `test(auth): comprehensive auth tests` | 20 | ~1000 | PR 2 |
| 4 | `docs(auth): update auth documentation` | 8 | ~400 | PR 2 |

### Merge Order:
PR 1 → PR 2 → (PR 3 ∥ PR 4)

### Parallelization:
...
```

---

## Section 14: PR Description Templates

### Bad Example (Avoid)

```markdown
## Summary
Fixed stuff

## Changes
- Changed some files
```

**Problems:** Vague summary, no test plan, no "why"

### Good Example (Follow)

```markdown
## Summary
- Fix token refresh race condition that caused intermittent 401 errors
- Add mutex lock to prevent concurrent refresh requests

## Test plan
- [ ] Trigger concurrent API calls with expired token
- [ ] Verify only one refresh request is made
- [ ] Confirm no 401 errors in rapid succession

## Changes
- `src/auth/token.ts` - Add mutex for refresh operation
- `src/auth/interceptor.ts` - Queue requests during refresh

Closes #456
```

### Generated PR Description Example

```markdown
## Summary
- Add OAuth2 provider integration for Google and GitHub
- Implement secure token refresh with automatic retry
- Enable session persistence across browser restart

## Test plan
- [ ] Complete OAuth2 login flow with Google account
- [ ] Complete OAuth2 login flow with GitHub account
- [ ] Verify token refresh with expired access token
- [ ] Confirm session persists after browser close/reopen
- [ ] Run existing auth test suite (all should pass)

## Changes

### Features
...
```

### PR Description Template

```markdown
## Summary
[1-3 bullet points: what changed and why]

## Test plan
[Checklist of verification steps]

## Changes (optional for small PRs)
[Key files with brief description]

## Breaking changes (if applicable)
[Migration steps]

## Notes (optional)
[Additional context, related issues]
```

---

## Section 16: Monorepo PR Split

```markdown
## Recommended PR Structure for Monorepo

| PR | Package | Risk | Merge Order |
|----|---------|------|-------------|
| 1 | `@app/shared` - validation utils | HIGH | First |
| 2 | `@app/auth` - OAuth2 support | MEDIUM | After PR 1 |
| 3 | `@app/web` - OAuth2 UI | LOW | After PR 2 |

### Rationale:
- Shared changes have highest blast radius
- Merge from lowest dependency to highest
- Allows incremental testing at each level
```

---

## Section 17: Release Notes

```markdown
## v1.3.0 Release Notes

### Features
- OAuth2 provider integration (#123)
- User profile image upload (#125)

### Bug Fixes
- Fixed login session timeout (#124)
- Resolved race condition in cart (#126)

### Breaking Changes
- Authentication API now requires `scope` parameter
  - Migration: Add `scope: "read"` to auth requests

### Dependencies
...
```

---

## Section 18: Progressive PR Split Plan (MEGA)

```markdown
## MEGA PR Split Plan: 247 files, 8,340 lines

### Overview
**Original Scope**: Complete auth system migration
**Recommended Split**: 5 PRs over 2 weeks

### Week 1

| PR | Title | Files | Lines | Risk | Dependencies |
|----|-------|-------|-------|------|--------------|
| 1 | refactor(auth): extract shared utilities | 35 | ~1,200 | LOW | None |
| 2 | feat(auth): new token management | 48 | ~1,800 | MEDIUM | PR 1 |

### Week 2

...
```
Week 1 Day 1-2: PR 1 (Foundation)
Week 1 Day 3-5: PR 2 (Core feature)
Week 2 Day 1-3: PR 3 (OAuth - needs careful review)
Week 2 Day 3-4: PR 4 (Migration)
Week 2 Day 5:   PR 5 (Tests - can parallel with PR 4 review)
```

### Risk Mitigation
- PR 3 (OAuth) is highest risk → dedicated review session
- Feature flag for gradual rollout
- Rollback plan per PR included
```

### Chunked Analysis Mode

```yaml
chunked_analysis:
  phase_1_overview:
    - File count and line statistics
    - Package/module distribution
    - High-level change categories
    - Initial split recommendation

  phase_2_module_analysis:
    - Per-module change breakdown
    - Cross-module dependencies
    - Risk assessment per module
    - Suggested merge order

  phase_3_detailed:
    - Essential vs noise per chunk
# ...
```

---

## AI-Generated Code Detection Patterns

```yaml
ai_code_indicators:
  naming_patterns:
    - Generic variable names: data, result, temp, value, item, output
    - Sequential naming: data1, data2, func1, func2
    - Overly verbose: getUserByIdFromDatabase, processDataAndReturnResult

  structural_patterns:
    - Unusual code density (high logic per function)
    - Inconsistent with project patterns
    - Overly uniform comment styles
    - Perfect but context-unaware implementations

  project_mismatch:
    - Different naming conventions than existing code
    - Unfamiliar utility patterns
# ...
```
