# Zen Refactoring Recipes

Step-by-step guides for common refactorings.

---

## Extract Method

**When**: Long method, duplicated code, code needing explanation

**Steps**:
1. Identify code fragment to extract
2. Check for local variables used (read and modified)
3. Create new method with intention-revealing name
4. Copy code to new method
5. Replace original code with method call
6. Pass read variables as parameters
7. Return modified variables (or use out parameters)
8. Run tests to verify behavior unchanged

**Before**:
```javascript
function printOwing() {
  // print banner
  console.log("***********************");
  console.log("**** Customer Owes ****");
  console.log("***********************");

  // calculate outstanding
  let outstanding = 0;
  for (const o of orders) {
    outstanding += o.amount;
  }

  // print details
  console.log(`name: ${name}`);
  console.log(`amount: ${outstanding}`);
}
```

**After**:
```javascript
function printOwing() {
  printBanner();
  const outstanding = calculateOutstanding();
  printDetails(outstanding);
}

function printBanner() {
  console.log("***********************");
  console.log("**** Customer Owes ****");
  console.log("***********************");
}

function calculateOutstanding() {
  return orders.reduce((sum, o) => sum + o.amount, 0);
}

function printDetails(outstanding) {
  console.log(`name: ${name}`);
  console.log(`amount: ${outstanding}`);
}
```

---

## Replace Conditional with Guard Clauses

**When**: Deeply nested conditionals, special cases mixed with main logic

**Steps**:
1. Identify special case conditions
2. Convert each to early return (guard clause)
3. Remove unnecessary else branches
4. Flatten remaining main logic
5. Run tests

**Before**:
```javascript
function getPayAmount() {
  let result;
  if (isDead) {
    result = deadAmount();
  } else {
    if (isSeparated) {
      result = separatedAmount();
    } else {
      if (isRetired) {
        result = retiredAmount();
      } else {
        result = normalPayAmount();
      }
    }
  }
  return result;
}
```

**After**:
```javascript
function getPayAmount() {
  if (isDead) return deadAmount();
  if (isSeparated) return separatedAmount();
  if (isRetired) return retiredAmount();
  return normalPayAmount();
}
```

---

## Introduce Explaining Variable

**When**: Complex expressions that are hard to understand

**Steps**:
1. Identify complex expression
2. Create well-named variable
3. Replace expression with variable
4. Run tests

**Before**:
```javascript
if (platform.toUpperCase().indexOf("MAC") > -1 &&
    browser.toUpperCase().indexOf("IE") > -1 &&
    wasInitialized() && resize > 0) {
  // do something
}
```

**After**:
```javascript
const isMacOS = platform.toUpperCase().indexOf("MAC") > -1;
const isIE = browser.toUpperCase().indexOf("IE") > -1;
const wasResized = wasInitialized() && resize > 0;

if (isMacOS && isIE && wasResized) {
  // do something
}
```

---

## Introduce Constant

**When**: Magic numbers or strings appear in code

**Steps**:
1. Identify magic value
2. Create descriptively named constant
3. Replace all occurrences
4. Run tests

**Before**:
```javascript
if (age >= 18) { /* ... */ }
if (status === 'pending') { /* ... */ }
const timeout = 86400000;
```

**After**:
```javascript
const LEGAL_ADULT_AGE = 18;
const STATUS_PENDING = 'pending';
const ONE_DAY_MS = 24 * 60 * 60 * 1000;

if (age >= LEGAL_ADULT_AGE) { /* ... */ }
if (status === STATUS_PENDING) { /* ... */ }
const timeout = ONE_DAY_MS;
```

### Naming Guidelines

- Use SCREAMING_SNAKE_CASE for constants
- Name should explain the meaning, not the value
- Group related constants together

```javascript
// ❌ Bad: Name describes value
const THIRTY_DAYS = 30;
const ONE_HUNDRED = 100;

// ✅ Good: Name describes meaning
const PASSWORD_EXPIRY_DAYS = 30;
const MAX_LOGIN_ATTEMPTS = 100;
```

---

## Before/After Report Template

```markdown
## Refactoring Report: [Component/File]

### Summary
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Lines of Code | 120 | 85 | -29% |
| Cyclomatic Complexity | 18 | 8 | -56% |
| Cognitive Complexity | 24 | 10 | -58% |
| Functions | 3 | 7 | +133% |
| Max Nesting Depth | 5 | 2 | -60% |
| Test Coverage | 75% | 82% | +7% |

### Code Smells Resolved
- ✅ Long Method → Extracted 4 focused functions
- ✅ Deep Nesting → Introduced guard clauses
- ✅ Magic Numbers → Created named constants
- ✅ Duplicate Code → Extracted shared helper

### Before
\`\`\`javascript
function processData(data) {  // CC: 18, Cognitive: 24
  if (data) {                 // Nesting +1
    if (data.items) {         // Nesting +2
      for (const item of data.items) {  // Nesting +3
        if (item.active) {    // Nesting +4
          if (item.value > 100) {  // Nesting +5
            // ... 30 lines of processing
          }
        }
      }
    }
  }
}
\`\`\`

### After
\`\`\`javascript
function processData(data) {  // CC: 3, Cognitive: 4
  if (!data?.items) return;

  const activeItems = filterActiveItems(data.items);
  const highValueItems = filterHighValue(activeItems);
  highValueItems.forEach(processItem);
}

function filterActiveItems(items) {
  return items.filter(item => item.active);
}

function filterHighValue(items) {
  return items.filter(item => item.value > HIGH_VALUE_THRESHOLD);
}

function processItem(item) {
  // ... focused processing logic
}
\`\`\`

### Changes Applied
1. ✅ Guard clause for early return
2. ✅ Extracted filterActiveItems (single responsibility)
3. ✅ Extracted filterHighValue (single responsibility)
4. ✅ Extracted processItem (single responsibility)
5. ✅ Introduced HIGH_VALUE_THRESHOLD constant
6. ✅ Used optional chaining for null safety

### Verification
- [x] All 24 tests pass
- [x] No behavior change (same inputs → same outputs)
- [x] Linting passes
- [x] Coverage maintained at 82%
```
