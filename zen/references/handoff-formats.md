# Zen Agent Handoff Formats

Standardized handoff templates for agent collaboration.

---

## JUDGE_TO_ZEN_HANDOFF

```markdown
## JUDGE_TO_ZEN_HANDOFF

**Review ID**: [PR# or commit SHA]
**Type**: Non-blocking Quality Observations

**Quality Observations**:

### [INFO-001] [Title]
| Aspect | Detail |
|--------|--------|
| File | `path/to/file.ts:42` |
| Observation | [What could be improved] |
| Suggestion | [How to improve] |

**Note**: These are non-blocking suggestions. Code works correctly but could be cleaner.

**Request**: Refactor at your discretion (separate commit/PR)
```

---

## ZEN_TO_RADAR_HANDOFF

```markdown
## ZEN_TO_RADAR_HANDOFF

**Refactoring ID**: [Description or branch name]
**Phase**: [Pre-Refactor / Post-Refactor]

**Files to Verify**:
| File | Refactoring Applied | Risk Level |
|------|---------------------|------------|
| `file.ts` | Extract Method | Low |
| `utils.ts` | Rename + Simplify | Medium |

**Verification Request**:
- [ ] Run all tests for affected files
- [ ] Verify coverage >= previous level
- [ ] Check no new failures introduced

**Expected Behavior**: Identical to before refactoring

**Request**: Confirm behavior unchanged via test verification
```

---

## RADAR_TO_ZEN_HANDOFF

```markdown
## RADAR_TO_ZEN_HANDOFF

**Verification ID**: [ID]
**Phase**: [Pre-Refactor / Post-Refactor]

**Test Results**:
| Metric | Before | After | Status |
|--------|--------|-------|--------|
| Total Tests | X | X | ✅ |
| Passing | X | X | ✅ |
| Coverage | X% | X% | ✅ |

**Verdict**: ✅ Safe to proceed / ⚠️ Issues detected

**Issues** (if any):
- [Test failure details]

**Request**: [Proceed with refactoring / Fix issues first]
```

---

## ZEN_TO_CANVAS_HANDOFF

```markdown
## ZEN_TO_CANVAS_HANDOFF

**Refactoring ID**: [Description]
**Visualization Type**: [Before/After Comparison / Dependency Graph / Class Diagram]

**Context**:
| Aspect | Before | After |
|--------|--------|-------|
| Classes | 1 (God class) | 4 (focused) |
| Dependencies | 8 | 3 per class |
| CC Average | 25 | 8 |

**Visualization Request**:
- Before: [What the original structure looked like]
- After: [What the refactored structure looks like]

**Files Changed**:
- `src/services/UserService.ts` → split into 3 files

**Request**: Generate comparison diagram for documentation
```

---

## ZEN_TO_JUDGE_HANDOFF

```markdown
## ZEN_TO_JUDGE_HANDOFF

**Refactoring ID**: [Description]
**Type**: Post-Refactor Review Request

**Changes Summary**:
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Lines | X | X | -X% |
| CC | X | X | -X% |
| Cognitive | X | X | -X% |

**Refactorings Applied**:
- [Refactoring 1]
- [Refactoring 2]

**Files Changed**:
| File | Change Type |
|------|-------------|
| `file.ts` | Modified |

**Verification**:
- [ ] All tests pass
- [ ] No behavior change

**Request**: Review refactored code for any remaining issues
```

---

## ATLAS_TO_ZEN_HANDOFF

```markdown
## ATLAS_TO_ZEN_HANDOFF

**Analysis ID**: [ID]
**Focus**: Complexity Hotspots

**Hotspots Identified**:
| File | Function | CC | Cognitive | Priority |
|------|----------|----|-----------| ---------|
| `file.ts` | `processOrder` | 35 | 28 | Critical |
| `utils.ts` | `validate` | 22 | 15 | High |

**Architectural Context**:
- [Why these functions became complex]
- [Dependencies to consider]

**Recommended Approach**:
- [Suggested refactoring strategy]

**Request**: Reduce complexity of identified hotspots
```

---

## ZEN_TO_QUILL_HANDOFF

```markdown
## ZEN_TO_QUILL_HANDOFF

**Refactoring ID**: [Description]
**Documentation Impact**: [High / Medium / Low]

**Changes Requiring Documentation**:
| Change | Type | Documentation Needed |
|--------|------|---------------------|
| `UserService` split | Class extraction | Update API docs |
| `validate()` renamed | Rename | Update usage examples |

**New Modules Created**:
- `src/services/UserValidator.ts`
- `src/services/UserNotifier.ts`

**Public API Changes**:
- `createUser()` → signature unchanged
- `validateUser()` → moved to `UserValidator`

**Request**: Update documentation for refactored modules
```

---

## BUILDER_TO_ZEN_HANDOFF

```markdown
## BUILDER_TO_ZEN_HANDOFF

**Implementation ID**: [PR# or description]
**Cleanup Scope**: [Specific file / Module / Feature area]

**Areas Needing Cleanup**:
| File | Issue | Priority |
|------|-------|----------|
| `file.ts` | Hastily written, needs polish | Medium |
| `utils.ts` | Duplicate code introduced | High |

**Context**:
- [Why cleanup is needed]
- [What behavior must be preserved]

**Request**: Apply Zen refactoring while preserving behavior
```

---

## HONE_TO_ZEN_HANDOFF

```markdown
## HONE_TO_ZEN_HANDOFF

**PDCA Cycle**: [Cycle N]
**Phase**: DO (Refactoring Step)
**Origin**: Hone Quality Orchestrator

**Quality Target**:
| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| CC (max) | X | Y | -Z |
| Cognitive (max) | X | Y | -Z |
| Code Smells | X | 0 | -X |

**Scope**:
| File | Issue | Priority |
|------|-------|----------|
| `file.ts` | [Quality finding from CHECK phase] | High |

**Constraints**:
- Time budget: [X minutes]
- Must pass CHECK phase validation after refactoring
- Diminishing returns threshold: [X% improvement minimum]

**Request**: Apply targeted refactoring to meet quality targets
```

---

## GUARDIAN_TO_ZEN_HANDOFF

```markdown
## GUARDIAN_TO_ZEN_HANDOFF

**PR/Branch**: [PR# or branch name]
**Type**: [Noise Separation / Hotspot Refactoring]

**Noise Identified**:
| File | Noise Type | Action |
|------|-----------|--------|
| `file.ts` | Style inconsistency | Separate into cleanup commit |
| `utils.ts` | Dead imports | Remove in pre-cleanup |

**Context**:
- [Why Guardian is requesting separation]
- [PR strategy: cleanup-first or cleanup-after]

**Request**: [Separate noise from feature changes / Refactor tech debt hotspot]
```

---

## ZEN_TO_HONE_HANDOFF

```markdown
## ZEN_TO_HONE_HANDOFF

**PDCA Cycle**: [Cycle N]
**Phase**: DO → CHECK (Verification Request)

**Refactoring Applied**:
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| CC (max) | X | Y | -Z% |
| Cognitive (max) | X | Y | -Z% |
| Code Smells | X | Y | -Z |

**Changes**:
- [Refactoring 1]
- [Refactoring 2]

**Request**: Verify improvements in CHECK phase, determine if another cycle is needed
```

---

## ZEN_TO_GUARDIAN_HANDOFF

```markdown
## ZEN_TO_GUARDIAN_HANDOFF

**Type**: [Cleanup Complete / Refactoring Complete]

**Changes Made**:
| File | Change | Commit Strategy |
|------|--------|-----------------|
| `file.ts` | Style cleanup | Separate commit |
| `utils.ts` | Dead code removal | Separate commit |

**Suggested Commit Messages**:
- `refactor: clean up style inconsistencies in file.ts`
- `refactor: remove dead imports from utils.ts`

**Request**: Review commit strategy, proceed with PR preparation
```

---

## ZEN_CONSISTENCY_AUDIT_HANDOFF

```markdown
## ZEN_CONSISTENCY_AUDIT_HANDOFF

**Audit ID**: [Description or branch name]
**Category**: [Error Handling / API Call / State Mgmt / Logging / Naming / Import-Export]
**Scope Tier**: [Focused / Module / Project-wide]

**Canonical Pattern**:
| Aspect | Detail |
|--------|--------|
| Pattern | [Description of dominant pattern] |
| Usage | [X/Y files, Z%] |
| Justification | [Why this is canonical] |

**Deviations Found**:
| # | File:Line | Current Pattern | Canonical | Severity | Effort |
|---|-----------|----------------|-----------|----------|--------|
| 1 | `path/file.ts:42` | [variant] | [canonical] | HIGH | Low |
| 2 | `path/other.ts:18` | [variant] | [canonical] | MEDIUM | Medium |

**Migration Plan**:
| Phase | Files | Change | Lines |
|-------|-------|--------|-------|
| 1 | [files] | [pattern change] | ~N |

**Tools Used**: [ast-grep / eslint / ruff / manual scan]

**Request**: [Review audit results / Execute migration phase 1]
```

---

## COLLABORATION PATTERNS

### Pattern A: Quality Improvement Flow
```
Judge (INFO findings) → JUDGE_TO_ZEN_HANDOFF → Zen → ZEN_TO_RADAR_HANDOFF → Radar
```

### Pattern B: Pre-Refactor Verification
```
Zen → ZEN_TO_RADAR_HANDOFF (pre) → Radar → RADAR_TO_ZEN_HANDOFF → Zen refactors → ZEN_TO_RADAR_HANDOFF (post)
```

### Pattern C: Refactoring Documentation
```
Zen (major changes) → ZEN_TO_CANVAS_HANDOFF → Canvas (before/after diagrams)
```

### Pattern D: Post-Refactor Review
```
Zen → ZEN_TO_JUDGE_HANDOFF → Judge (re-review)
```

### Pattern E: Complexity Hotspot Fix
```
Atlas (hotspots) → ATLAS_TO_ZEN_HANDOFF → Zen → ZEN_TO_ATLAS_HANDOFF
```

### Pattern F: Documentation Update
```
Zen (API changes) → ZEN_TO_QUILL_HANDOFF → Quill
```

### Pattern G: PDCA Quality Cycle
```
Hone (PLAN) → Judge (CHECK) → Builder (DO-fix) → Zen (DO-refactor) → Radar (CHECK-test) → Hone (ACT)
```

### Pattern H: PR Noise Separation
```
Guardian (noise detected) → GUARDIAN_TO_ZEN_HANDOFF → Zen (cleanup) → ZEN_TO_GUARDIAN_HANDOFF → Guardian (commit strategy)
```

### Pattern I: Tech Debt Hotspot Refactoring
```
Guardian (hotspot identified) → GUARDIAN_TO_ZEN_HANDOFF → Zen (refactor) → ZEN_TO_RADAR_HANDOFF → Radar (verify)
```
