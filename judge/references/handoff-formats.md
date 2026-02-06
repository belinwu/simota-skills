# Handoff Formats

Standardized handoff templates for Judge's agent collaboration.

---

## Input Handoffs (→ Judge)

### BUILDER_TO_JUDGE_HANDOFF

```markdown
## BUILDER_TO_JUDGE_HANDOFF

**Implementation ID**: [PR# or description]
**Type**: [Feature / Bug Fix / Refactor]

**Changes Summary**:
| File | Change Type | Description |
|------|-------------|-------------|
| `file.ts` | Modified | [What changed] |

**Implementation Details**:
- [Key decision 1]
- [Key decision 2]

**Review Focus Areas**:
- [Area 1 - e.g., error handling]
- [Area 2 - e.g., edge cases]

**Test Status**: [Tests added / Needs Radar]

**Request**: Code review for correctness, security, intent alignment
```

### SCOUT_TO_JUDGE_HANDOFF

```markdown
## SCOUT_TO_JUDGE_HANDOFF

**Investigation ID**: [ID]
**Bug Status**: Fix implemented

**Investigation Summary**:
| Aspect | Detail |
|--------|--------|
| Root Cause | [What was wrong] |
| Location | `file.ts:42` |
| Fix Applied | [What was changed] |

**Verification Request**:
- Verify fix addresses root cause
- Check for edge cases
- Ensure no regression introduced

**Files Changed**: [List of files]

**Request**: Review fix and verify correctness
```

### GUARDIAN_TO_JUDGE_HANDOFF

```markdown
## GUARDIAN_TO_JUDGE_HANDOFF

**PR ID**: [PR#]
**Commit Strategy**: [Single / Multi-commit / Squash]

**PR Structure**:
| Commit | Scope | Description |
|--------|-------|-------------|
| [SHA] | [scope] | [description] |

**Request**: Review code quality across organized commits
```

### SENTINEL_TO_JUDGE_HANDOFF

```markdown
## SENTINEL_TO_JUDGE_HANDOFF

**Security Audit ID**: [ID]
**Original Finding**: [Judge finding ID]

**Security Assessment**:
| Aspect | Result |
|--------|--------|
| OWASP Category | [e.g., A03:2021 Injection] |
| Exploitability | [High / Medium / Low] |
| Impact | [Critical / High / Medium / Low] |
| Verified | [Yes / No / Partial] |

**Remediation**:
```typescript
// Recommended fix
[code]
```

**Verification Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Request**: Incorporate into final review verdict
```

---

## Output Handoffs (Judge →)

### JUDGE_TO_BUILDER_HANDOFF

```markdown
## JUDGE_TO_BUILDER_HANDOFF

**Review ID**: [PR# or commit SHA]
**Verdict**: REQUEST CHANGES
**Review Mode**: [PR Review / Pre-Commit / Commit Review]

**Findings Summary**:
| Severity | Count | Status |
|----------|-------|--------|
| Critical | X | Must fix |
| High | X | Should fix |
| Medium | X | Consider |

**Required Fixes**:

### [CRITICAL-001] [Title]
| Aspect | Detail |
|--------|--------|
| File | `path/to/file.ts:42` |
| Issue | [Description] |
| Impact | [What happens if not fixed] |
| Suggested Fix | [How to fix] |

### [HIGH-001] [Title]
| Aspect | Detail |
|--------|--------|
| File | `path/to/file.ts:87` |
| Issue | [Description] |
| Suggested Fix | [How to fix] |

**Acceptance Criteria**:
- [ ] All CRITICAL findings resolved
- [ ] HIGH findings addressed or documented
- [ ] Re-review by Judge after fixes

**Request**: Implement fixes and request re-review
```

### JUDGE_TO_SENTINEL_HANDOFF

```markdown
## JUDGE_TO_SENTINEL_HANDOFF

**Review ID**: [PR# or commit SHA]
**Security Finding**: [Finding ID from Judge report]

**Potential Vulnerability**:
| Aspect | Detail |
|--------|--------|
| Type | [XSS / SQL Injection / Auth Bypass / etc.] |
| File | `path/to/file.ts:42` |
| Code | [Problematic code snippet] |

**Judge's Assessment**:
- Severity: [CRITICAL / HIGH]
- Confidence: [High / Medium / Low]
- Initial Impact: [Description]

**Evidence from Review**:
```
[codex review output excerpt]
```

**Request**: Deep security analysis with:
- Exploit scenario assessment
- OWASP classification
- Remediation guidance
- Fix verification criteria
```

### JUDGE_TO_ZEN_HANDOFF

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

### JUDGE_TO_RADAR_HANDOFF

```markdown
## JUDGE_TO_RADAR_HANDOFF

**Review ID**: [PR# or commit SHA]
**Finding Coverage Gap**: True

**Findings Without Tests**:
| Finding ID | Type | File | Test Needed |
|------------|------|------|-------------|
| CRITICAL-001 | Bug fix | `file.ts:42` | Regression test |
| HIGH-002 | Edge case | `file.ts:87` | Edge case test |

**Test Requirements**:
- [ ] Regression test for CRITICAL-001 scenario
- [ ] Edge case test for HIGH-002 condition
- [ ] Integration test for affected flow

**Request**: Add test coverage before merge approval
```
