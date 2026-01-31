# Scout Debug Strategy Reference

Systematic debugging approaches organized by error type, reproducibility, and environment.

## By Error Type

| Error Type | First Step | Tools | Look For |
|------------|------------|-------|----------|
| TypeError | Check stack trace | DevTools Console | Null/undefined access |
| NetworkError | Network tab | DevTools Network | Failed requests, CORS |
| SyntaxError | Check line number | Linter, Editor | Typos, missing brackets |
| ReferenceError | Check variable scope | DevTools Sources | Undefined variables |
| RangeError | Check numeric operations | Console logs | Array bounds, recursion |
| Custom Error | Search error message | Codebase search | Where error is thrown |

---

## By Reproducibility

| Reproducibility | Strategy | Focus |
|-----------------|----------|-------|
| Always | Direct debugging | Step through with debugger |
| Sometimes (>50%) | Add logging | Capture state at key points |
| Rarely (<20%) | Stress testing | Race conditions, edge cases |
| Never locally | Environment diff | Config, data, versions |

---

## By Environment

| Works In | Fails In | Investigation |
|----------|----------|---------------|
| Dev | Prod | Env vars, API endpoints, build config |
| Prod | Dev | Data differences, missing mocks |
| Chrome | Firefox/Safari | Browser-specific APIs, CSS |
| Fast machine | Slow machine | Race conditions, timeouts |
| Fresh install | Existing user | Cached data, migrations |

---

## Quick Triage Flowchart

```
Error Reported
    │
    ├─ Can reproduce locally?
    │   ├─ Yes → Use debugger, step through
    │   └─ No  → Get more details (env, data, steps)
    │
    ├─ Error message clear?
    │   ├─ Yes → Search codebase for error source
    │   └─ No  → Add logging to narrow down
    │
    ├─ Recent change?
    │   ├─ Yes → Check git log, bisect
    │   └─ No  → Deeper investigation needed
    │
    └─ Data-dependent?
        ├─ Yes → Get sample data, test variations
        └─ No  → Focus on code logic
```

---

## Investigation Toolkit Quick Reference

### Code Exploration
- `git log --oneline -20 -- path/to/file` - Recent changes to file
- `git blame path/to/file` - Who changed what
- `git bisect` - Find the commit that introduced the bug
- Search for error message in codebase

### Runtime Debugging
- Browser DevTools (Network, Console, Sources)
- Strategic console.log with context
- Debugger breakpoints
- React DevTools / Vue DevTools for state inspection

### Data Investigation
- Check database state
- Inspect API request/response
- Validate data format and types

---

## Debugging Checklist

1. **Gather Information**
   - [ ] Exact error message
   - [ ] Stack trace
   - [ ] Environment details
   - [ ] When it started

2. **Reproduce**
   - [ ] Follow reported steps
   - [ ] Try minimal case
   - [ ] Test in different environments

3. **Trace**
   - [ ] Add logging at key points
   - [ ] Check network requests
   - [ ] Review recent commits

4. **Locate**
   - [ ] Identify file and line
   - [ ] Understand the condition
   - [ ] Check related code
