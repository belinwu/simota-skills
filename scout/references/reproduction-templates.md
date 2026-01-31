# Scout Reproduction Templates Reference

Standardized templates for documenting bug reproduction across different bug types.

## UI Bug Template

```markdown
## UI Bug Reproduction

**Environment:**
- Browser: [Chrome 120 / Firefox 121 / Safari 17]
- OS: [macOS 14 / Windows 11 / Ubuntu 22]
- Screen size: [1920x1080 / Mobile 375x667]
- User role: [Admin / Regular / Guest]

**Setup State:**
- [ ] Fresh login (no cached state)
- [ ] Specific data exists: [describe]
- [ ] Feature flags: [list any]

**Steps:**
1. Navigate to [URL/page]
2. [User action]
3. [User action]
4. Observe [element/area]

**Expected:** [What should appear/happen]
**Actual:** [What actually appears/happens]

**Visual Evidence:** [Screenshot or recording link]

**Reproducibility:** [Always / 80% / Specific conditions]
```

---

## API Bug Template

```markdown
## API Bug Reproduction

**Endpoint:** [METHOD /api/path]

**Request:**
```json
{
  "headers": {
    "Authorization": "Bearer [token type]",
    "Content-Type": "application/json"
  },
  "body": { }
}
```

**Expected Response:**
```json
{
  "status": 200,
  "body": { }
}
```

**Actual Response:**
```json
{
  "status": [actual],
  "body": { }
}
```

**cURL Command:**
```bash
curl -X POST https://api.example.com/endpoint \
  -H "Authorization: Bearer xxx" \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

**Reproducibility:** [Always / Specific conditions]
```

---

## State Management Bug Template

```markdown
## State Bug Reproduction

**State Location:** [Redux store / React Context / Component state]
**State Path:** [store.user.profile / context.theme]

**Initial State:**
```json
{ }
```

**Action/Trigger:** [What causes the state change]

**Expected State:**
```json
{ }
```

**Actual State:**
```json
{ }
```

**State Timeline:**
1. [Time T0] Initial state: {...}
2. [Time T1] Action dispatched: {...}
3. [Time T2] State after: {...}

**DevTools Evidence:** [Redux DevTools / React DevTools screenshot]
```

---

## Async Bug Template

```markdown
## Async Bug Reproduction

**Async Operation:** [API call / Timer / Event listener]

**Sequence:**
```
User    →  Component  →  Service  →  API
  │           │            │          │
  ├──click────┤            │          │
  │           ├──fetch─────┤          │
  │           │            ├──request─┤
  │           │            │    ⚡ Error occurs here
```

**Timing Information:**
- Operation start: [timestamp]
- Expected completion: [duration]
- Actual completion: [duration]
- Error occurred at: [timestamp]

**Race Condition Factors:**
- [ ] Rapid user interaction
- [ ] Slow network
- [ ] Component unmount
- [ ] Multiple concurrent requests

**Console Logs (with timestamps):**
```
[10:00:00.000] Starting fetch...
[10:00:00.050] Component rendering...
[10:00:00.100] User navigated away
[10:00:00.500] Fetch completed - setState on unmounted!
```
```

---

## General Bug Report Template

```markdown
## Bug Report

**Title:** [Brief description]
**Severity:** Critical / High / Medium / Low
**Reproducibility:** Always / Sometimes / Rare

**Environment:**
- [Browser/OS/Node version]
- [Environment: Dev/Staging/Prod]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Behavior:** [What should happen]
**Actual Behavior:** [What actually happens]

**Error Messages:**
```
[Paste exact error text]
```

**Additional Context:**
- Recent changes: [If known]
- Affected users: [Scope]
- Workaround: [If any]
```

---

## Template Selection Guide

| Bug Type | Template | Key Focus |
|----------|----------|-----------|
| Visual/UI | UI Bug | Screenshots, viewport, user role |
| API | API Bug | Request/response, cURL command |
| State | State Management | State snapshots, timeline |
| Timing | Async Bug | Sequence diagram, timestamps |
| General | Bug Report | Standard format for any bug |
