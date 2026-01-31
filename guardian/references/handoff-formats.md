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
