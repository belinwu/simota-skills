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
