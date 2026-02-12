# Review & Report Templates

## Review Checklist

### Readability
- [ ] Variable/function names are descriptive
- [ ] Code is self-documenting
- [ ] No magic numbers or strings
- [ ] Complexity is reasonable (CC < 10)

### Structure
- [ ] Functions are small and focused (< 20 lines)
- [ ] No unnecessary duplication
- [ ] Abstractions are appropriate
- [ ] Nesting depth <= 3 levels

### Correctness
- [ ] Edge cases handled
- [ ] Error cases handled appropriately
- [ ] No potential null/undefined issues
- [ ] Logic correct for all inputs

### Maintainability
- [ ] Easy to modify in future
- [ ] No hidden dependencies
- [ ] Code is testable
- [ ] Changes are reversible

---

## Review Output Format

```markdown
## Zen Code Review

### Summary
[1-2 sentence overall assessment]
**Review Level**: [Quick Scan / Standard / Deep Dive]

### Complexity Analysis
| File | Function | CC | Cognitive | Status |
|------|----------|----|-----------| -------|
| ... | ... | ... | ... | ... |

### Strengths
- [What's done well - be specific]

### Suggestions
- **[File:Line]** - [Suggestion]
  - Why: [Reasoning]
  - How: [Code example if helpful]

### Issues
- **[File:Line]** - [Issue] (Severity: Minor/Moderate/Critical)
  - Impact: [Why this matters]
  - Fix: [Recommended solution]

### Verdict
Approve | Request Changes | Comment Only
```

---

## Refactoring Report Format

```markdown
## Refactoring Report: [Component/File]

### Summary
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Lines of Code | X | Y | -Z% |
| Cyclomatic Complexity (max) | X | Y | -Z% |
| Cognitive Complexity (max) | X | Y | -Z% |
| Functions | X | Y | +Z |
| Max Nesting Depth | X | Y | -Z |
| Code Smells Resolved | - | - | N |

### Changes Applied
1. [Recipe]: [Target] → [Result]
2. [Recipe]: [Target] → [Result]

### Test Verification
- Pre-refactor: [Pass/Fail] (X tests)
- Post-refactor: [Pass/Fail] (X tests)
- Coverage: X% → Y%

### Remaining Opportunities
- [ ] [Next refactoring candidate]
```

---

## Code Standards Examples

### Good Zen Code

```javascript
// Descriptive names, early return, named constants
const MAX_RETRY_ATTEMPTS = 3;
const RETRY_DELAY_MS = 1000;

function processOrder(order) {
  if (!order?.isValid) return null;

  const total = calculateOrderTotal(order);
  const discount = applyDiscount(total, order.customer);

  return saveOrder(order, discount);
}
```

### Bad Zen Code

```javascript
// Magic numbers, deep nesting, vague names
function doIt(d) {
  if (d.v) {
    if (d.c > 100) {
      for (let i = 0; i < 3; i++) {
        // ... 50 lines of nested logic
      }
    }
  }
}
```
