# Vague Report Handling Reference

A detailed guide for inferring intent from vague bug reports, minimizing questions, and starting investigation effectively.

---

## Report Pattern Dictionary

### Primary Patterns (6 types)

| ID | Pattern Name | Example Keywords | Inferred Situation | Investigation Start Point |
|----|-------------|------------------|-------------------|--------------------------|
| P01 | Total Denial | "Doesn't work", "Broken", "Can't use", "Not showing" | Complete core feature failure | Entry point, recent changes |
| P02 | Comparison | "It worked before", "Until yesterday", "Just now", "Suddenly" | Regression | git log, deploy history |
| P03 | Vague Feeling | "Something's off", "Feels weird", "Uncomfortable" | Subtle deviation from expectation | UI, data display, timing |
| P04 | Urgency | "Fix ASAP", "Urgent", "Critical", "Blocked" | Business blocker | Impact scope, workarounds |
| P05 | Tech Term Mixed | "API returns null", "500 error", "Response slow" | Specific technical issue | Mentioned technical area |
| P06 | Image Only | [Screenshot only], [Video only] | Visual problem | Elements in image, error displays |

### Extended Patterns (14 types)

| ID | Pattern Name | Example Keywords | Inferred Situation | Investigation Start Point |
|----|-------------|------------------|-------------------|--------------------------|
| P07 | Conditional | "Only when...", "If I...", "Specific..." | Issue under specific conditions | Code path for mentioned condition |
| P08 | Environment | "In production", "On mobile", "In Chrome" | Environment-dependent issue | Environment diff, config, polyfills |
| P09 | User Specific | "User X said...", "Customer reported...", "From users..." | Specific user's problem | Permissions, roles, data state |
| P10 | Frequency | "Sometimes", "Occasionally", "Not every time" | Intermittent issue | Race conditions, cache, timing |
| P11 | Action Specific | "When I click...", "After entering...", "When saving..." | Specific action issue | Event handlers, validation |
| P12 | Data Specific | "With this data...", "For specific value..." | Data-driven issue | Data validation, edge cases |
| P13 | Time Specific | "Only in morning", "End of month", "Periodically" | Time-dependent issue | Cron, timezone, date calculation |
| P14 | Error Message | "It says...", "Error appeared..." | Explicit error | Error message source |
| P15 | Performance | "Slow", "Heavy", "Freezes" | Performance issue | N+1, memory leak, infinite loop |
| P16 | Security | "Shouldn't be visible", "Permission...", "Without login..." | Security issue | Auth, access control |
| P17 | Layout Broken | "Misaligned", "Overflowing", "Overlapping" | CSS/layout issue | Styles, responsive |
| P18 | Copy/Text | "Wrong text", "Translation wrong" | Localization/copy issue | Translation files, hardcoded text |
| P19 | Notification | "Email not arriving", "No notification..." | Async processing issue | Queue, external service integration |
| P20 | Integration | "Connection with X...", "External service..." | External integration issue | API integration, Webhook, OAuth |

---

## Context Analysis Guide

### Information to Collect and Methods

| Source | Command/Method | How to Use |
|--------|---------------|------------|
| **Recent commits** | `git log --oneline -20` | Identify change-related regressions |
| **Changed files** | `git diff HEAD~5 --name-only` | Identify impact scope |
| **Deploy history** | CI/CD logs, tag list | Identify release-related issues |
| **Related Issues** | GitHub Issues search | Find similar reports |
| **Error logs** | Server logs, browser console | Actual error content |
| **Report timing** | Report time vs last deploy time | New vs existing issue |

### Timing Analysis Matrix

| Report Timing | Inferred Cause | Priority Investigation Target |
|---------------|----------------|------------------------------|
| Right after deploy | Latest release changes | Recent commit diff |
| Monday morning | Weekend batch processing, data accumulation | Scheduled tasks, data volume |
| Start/End of month | Date calculation, aggregation processing | Date handling, boundary values |
| Specific time of day | Load, external services, Cron | Scheduled tasks |
| Random | Race condition, data dependency | Async processing, cache |

### Reporter Attribute Analysis

| Reporter | Expected Accuracy | Information to Supplement |
|----------|------------------|---------------------------|
| Developer | Technically accurate | Business impact |
| QA | Clear reproduction steps | Technical details |
| PO/PM | Clear business impact | Technical details, reproduction steps |
| End user | Experience-based report | Reproduction steps, environment info |
| Customer support | Aggregated multiple reports | Individual reproduction conditions |

---

## Hypothesis Generation Templates

### Three Axes for Hypothesis Generation

Generate hypotheses from vague reports using these 3 axes:

```
Hypothesis 1 (Most Frequent): Similar patterns that occurred before in this codebase
Hypothesis 2 (Recent Change): Possibly affected by recent changes
Hypothesis 3 (Pattern-based): Typical causes inferred from report pattern
```

### Hypothesis Templates by Bug Type

#### "Doesn't work" type (P01: Total Denial)

| Hypothesis | How to Verify |
|------------|---------------|
| H1: Broken by recent deploy | Check changes with `git log --since="yesterday"` |
| H2: Dependent service is down | Check external API, DB health |
| H3: Config/environment variable issue | Check environment settings, .env |

#### "It worked before" type (P02: Comparison)

| Hypothesis | How to Verify |
|------------|---------------|
| H1: Regression from recent commit | Identify cause commit with `git bisect` |
| H2: Dependency library update | Check package.json / lock file diff |
| H3: Database schema change | Check migration history |

#### "Something's off" type (P03: Vague Feeling)

| Hypothesis | How to Verify |
|------------|---------------|
| H1: Subtle UI display difference | Visual comparison, CSS changes |
| H2: Data display order/format | Sort, date format check |
| H3: Timing/response speed | Network, load time measurement |

#### "Happens sometimes" type (P10: Frequency)

| Hypothesis | How to Verify |
|------------|---------------|
| H1: Race condition | Check async processing, concurrent access |
| H2: Cache inconsistency | Test behavior after cache clear |
| H3: Data dependency (only with specific data) | Identify problem data, boundary values |

#### "Slow" type (P15: Performance)

| Hypothesis | How to Verify |
|------------|---------------|
| H1: N+1 query | SQL logs, query count |
| H2: Large data processing | Data volume, pagination |
| H3: External API timeout | Network logs, response time |

---

## Pre-Investigation Checklist

Items to check before asking questions. Only ask if all items checked and still unclear.

### Required Check Items

```markdown
## Pre-Question Checklist

### Codebase Verification
- [ ] Checked recent changes with `git log -20`
- [ ] Checked changed files with `git diff HEAD~5 --name-only`
- [ ] Read the code for the feature mentioned in report
- [ ] Checked related test code

### Log/Error Verification
- [ ] Checked server logs (if accessible)
- [ ] Checked browser console errors (for frontend)
- [ ] Searched for error stack traces

### Past Knowledge Verification
- [ ] Checked `.agents/scout.md` for similar investigation records
- [ ] Searched GitHub Issues for similar reports
- [ ] Checked `.agents/PROJECT.md` for project knowledge

### Hypothesis Verification
- [ ] Generated 3 hypotheses
- [ ] Started verification of most likely hypothesis
- [ ] Recorded verification results

### Question Necessity Assessment
- [ ] Still unclear after checking all above?
- [ ] Cannot proceed without this information?
- [ ] Is proceeding with assumptions dangerous?

→ Only ask minimal questions if all answers are "yes"
```

### Cases Where Questions Are Needed (Exceptions)

In these cases, asking questions for investigation efficiency is acceptable:

| Case | Required Question |
|------|------------------|
| Reproduction requires production data | "Do you have access to production data?" |
| Different behavior across environments | "Which environment is this occurring in?" |
| User-specific issue | "Can you provide the affected user's ID?" |
| Security risk | "May I proceed with this investigation?" |

---

## Techniques for Improving Inference Accuracy

### 1. Reading Implicit Information

| Report Content | Implicit Information |
|----------------|---------------------|
| "ASAP" | Affecting business, possibly customer-facing |
| "X said..." | Second-hand info, needs verification |
| "Usually works" | Low reproducibility, condition-dependent |
| "Didn't do anything" | May not be aware of changes |

### 2. Reading the Report's "Temperature"

| Temperature | Characteristics | Response |
|-------------|----------------|----------|
| Calm | Objective description | Investigate as written |
| Anxious | Emotional, rushing | Prioritize workaround |
| Resigned | "Not again" tone | Likely known issue |
| Angry | Strong dissatisfaction | High-impact problem |

### 3. Inferring What's Not Reported

| Not Included in Report | Inference |
|-----------------------|-----------|
| Reproduction steps | Frequent occurrence OR reproduction method unknown |
| Environment info | Not limited to specific environment |
| Error message | No explicit error OR overlooked |
| Expected behavior | Implicit expectation, spec understanding gap |

---

## Investigation Completion Criteria

### Reporting Method by Confidence Level

| Level | Condition | Report Format |
|-------|-----------|---------------|
| **HIGH** | Reproduction success + root cause code identified | "Root cause: {file}:{line}" - definitive |
| **MEDIUM** | Reproduction success + cause estimated | "Estimated cause: {description}" + verification method |
| **LOW** | Cannot reproduce + hypothesis only | "Hypothesis: {hypothesis}" + info needed for further investigation |

### Conditions for Ending Investigation

```
HIGH: Satisfy all
  ✓ Can reproduce (or identified reproduction conditions)
  ✓ Root cause identified (can specify file:line)
  ✓ Impact scope understood
  ✓ Fix approach can be articulated

MEDIUM: Satisfy these
  ✓ Can reproduce
  ✓ Can estimate cause
  ✓ Next investigation steps are clear

LOW: Record these
  ✓ Hypotheses tried and results
  ✓ Information needed for further investigation
  ✓ Current best guess
```

---

## Scout's Mindset

> "Investigate before asking"
>
> Scout is a detective. A detective doesn't interrogate the client with "Where were you? What did you do?"
> Instead, they observe the scene, gather evidence, and reason. Questions are the last resort.

### Investigation Attitude

1. **Trust the report** - Don't dismiss as "user error" without evidence
2. **Don't fear inference** - Form hypotheses and verify them
3. **Follow the trail** - Code, logs, and history don't lie
4. **Ask precisely** - Get minimum necessary information in one go
