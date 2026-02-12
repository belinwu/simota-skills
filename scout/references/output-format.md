# Scout Output Format

## Investigation Report Template

```markdown
## Scout Investigation Report

### Bug Summary
**Title:** [Brief description]
**Severity:** Critical / High / Medium / Low
**Reproducibility:** Always / Sometimes / Rare

### Reproduction Steps
1. [Step 1]
2. [Step 2]

**Expected:** [What should happen]
**Actual:** [What actually happens]

### Root Cause Analysis
**Location:** `src/path/to/file.ts:123` in `functionName()`
**Cause:** [Explanation of why the bug occurs]

### Recommended Fix
**Approach:** [High-level fix strategy]
**Files to modify:** [List with changes needed]

### Regression Prevention
**Suggested tests for Radar:** [Test cases to prevent recurrence]
```

## Investigation Toolkit

| Category | Tools |
|----------|-------|
| **Code** | `git log`, `git blame`, `git bisect`, codebase search |
| **Runtime** | DevTools (Network, Console, Sources), debugger |
| **State** | React/Vue DevTools, Redux DevTools |
| **Data** | Database queries, API inspection |

## Investigation Completion Criteria

### Required (must satisfy all)
- [ ] Reproducible (or reproduction conditions identified)
- [ ] Root cause identified (can specify file:line)
- [ ] Impact scope understood
- [ ] Fix approach can be articulated

### Confidence Levels

| Level | Condition | How to Report |
|-------|-----------|---------------|
| **HIGH** | Reproduction success + root cause code identified | Report as confirmed |
| **MEDIUM** | Reproduction success + cause estimated | Report as estimated, provide verification method |
| **LOW** | Cannot reproduce + hypothesis only | Report as hypothesis, specify info needed |
