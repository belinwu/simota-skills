# Standardized Handoff Formats Reference

Builder agent's standardized handoff templates for agent collaboration.

## FORGE_TO_BUILDER_HANDOFF

```markdown
## FORGE_TO_BUILDER_HANDOFF

**Prototype Location**: [path/to/components/]
**Verification Status**: [UI verified / Partially verified]

**What Works (Verified)**:
- [Feature 1]
- [Feature 2]

**Production Requirements**:
| Area | Current | Required |
|------|---------|----------|
| Type Safety | `any` types | Explicit interfaces |
| Error Handling | None | Try-catch + error boundaries |
| Validation | None | Zod schemas |
| API Integration | MSW mocks | Real API client |

**Mock Data to Replace**:
| Mock | Production Source |
|------|-------------------|
| MOCK_USER | UserRepository.findById() |
| MOCK_PRODUCTS | ProductService.list() |

**Domain Insights**:
- [Business rule 1]
- [Business rule 2]

**Request**: Convert to production-ready implementation
```

## SCOUT_TO_BUILDER_HANDOFF

```markdown
## SCOUT_TO_BUILDER_HANDOFF

**Investigation ID**: [ID]
**Severity**: [Critical / High / Medium / Low]
**Confidence**: [High / Medium / Low]

**Root Cause**:
| Aspect | Detail |
|--------|--------|
| Location | `src/path/file.ts:123` |
| Function | `functionName()` |
| Issue | [What is wrong] |

**Reproduction**:
1. [Step 1]
2. [Step 2]
3. Bug occurs

**Recommended Fix**:
```typescript
// BEFORE
[buggy code]

// AFTER
[fixed code]
```

**Edge Cases to Handle**:
- [Edge case 1]
- [Edge case 2]

**Request**: Implement fix and request Radar regression tests
```

## GUARDIAN_TO_BUILDER_HANDOFF

```markdown
## GUARDIAN_TO_BUILDER_HANDOFF

**Branch**: [Recommended branch name]
**Commit Strategy**: [Single / Split / Squash]

**Proposed Commits**:
| Order | Message | Files | Reason |
|-------|---------|-------|--------|
| 1 | feat(scope): description | file1.ts | Core feature |
| 2 | test(scope): description | file1.test.ts | Test coverage |

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

**Implementation Summary**:
- [Key change 1]
- [Key change 2]

**Current State**:
- Commits: [N commits]
- Files changed: [N files]
- Lines: +[N]/-[N]

**Files Changed**:
| File | Change Type | Description |
|------|-------------|-------------|
| src/domain/User.ts | feat | User entity with validation |
| src/api/userClient.ts | feat | API client with retry |

**Request**:
- Analyze change quality
- Optimize commit structure
- Generate PR description
```

## BUILDER_TO_RADAR_HANDOFF

```markdown
## BUILDER_TO_RADAR_HANDOFF

**Component**: [Class/Function name]
**File**: [path/to/file.ts]
**Implementation Type**: [New feature / Bug fix / Refactor]

**Critical Business Rules**:
- Rule 1: [Description]
- Rule 2: [Description]

**Edge Cases to Cover**:
| Case | Input | Expected |
|------|-------|----------|
| Empty input | `{}` | ValidationError |
| Invalid ID | `{ id: 'bad' }` | NotFoundError |
| Boundary | `{ count: 0 }` | Edge handling |

**Key Methods**:
| Method | Purpose | Test Focus |
|--------|---------|------------|
| create() | Factory method | Validation |
| update() | State change | Transitions |

**Test Skeleton Generated**: [Yes/No - path if yes]

**Request**: Add comprehensive test coverage
```

## BUILDER_TO_TUNER_HANDOFF

```markdown
## BUILDER_TO_TUNER_HANDOFF

**Query/Operation**: [Description]
**File**: [path/to/file.ts:line]

**Current Implementation**:
```typescript
[current code]
```

**Performance Concern**:
- Issue: [N+1 / Full scan / Lock contention / etc.]
- Data volume: [Expected row count]
- Frequency: [Calls per minute/hour]
- Current latency: [If measured]

**Context**:
- Database: [PostgreSQL / MySQL / MongoDB]
- ORM: [Prisma / TypeORM / Drizzle]
- Indexes: [Existing indexes on table]

**Request**: Analyze and suggest optimization
```

## BUILDER_TO_SENTINEL_HANDOFF

```markdown
## BUILDER_TO_SENTINEL_HANDOFF

**Component**: [Component name]
**File**: [path/to/file.ts]
**Security Concern**: [Auth / Input validation / Data handling]

**Implementation**:
```typescript
[code to review]
```

**Data Handled**:
| Data Type | Sensitivity | Current Protection |
|-----------|-------------|-------------------|
| Password | High | bcrypt hash |
| Email | Medium | Zod validation |
| API Key | High | Environment variable |

**Request**: Security review and hardening recommendations
```

## TUNER_TO_BUILDER_HANDOFF

```markdown
## TUNER_TO_BUILDER_HANDOFF

**Analysis**: [Query/Operation analyzed]
**Performance Issue**: [Identified issue]

**Current Performance**:
- Execution time: [ms]
- Rows scanned: [count]
- Index usage: [Used / Not used]

**Recommended Optimization**:
```typescript
// Optimized code
[code]
```

**Changes Required**:
| Change | Impact | Effort |
|--------|--------|--------|
| Add index on X | -80% latency | Low |
| Rewrite query | -50% latency | Medium |

**Request**: Apply optimization and verify improvement
```

## SENTINEL_TO_BUILDER_HANDOFF

```markdown
## SENTINEL_TO_BUILDER_HANDOFF

**Review**: [Component reviewed]
**Risk Level**: [Critical / High / Medium / Low]

**Vulnerabilities Found**:
| Issue | Location | Severity | Fix |
|-------|----------|----------|-----|
| SQL Injection | query.ts:45 | Critical | Use parameterized query |
| XSS | render.tsx:23 | High | Sanitize output |

**Recommended Fixes**:
```typescript
// Secure implementation
[code]
```

**Additional Hardening**:
- [ ] Add rate limiting
- [ ] Implement CSRF protection
- [ ] Add security headers

**Request**: Apply security fixes
```
