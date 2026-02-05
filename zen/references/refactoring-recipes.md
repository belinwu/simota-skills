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

## Replace Conditional with Polymorphism

**When**: Switch/if-else chains that dispatch based on type or status

**Steps**:
1. Identify the condition that selects behavior
2. Create interface/base class for the common behavior
3. Create subclass/implementation for each case
4. Replace conditional with polymorphic dispatch
5. Run tests

**Before**:
```typescript
function calculateArea(shape: Shape): number {
  switch (shape.type) {
    case 'circle':
      return Math.PI * shape.radius ** 2;
    case 'rectangle':
      return shape.width * shape.height;
    case 'triangle':
      return 0.5 * shape.base * shape.height;
    default:
      throw new Error(`Unknown shape: ${shape.type}`);
  }
}
```

**After**:
```typescript
interface Shape {
  area(): number;
}

class Circle implements Shape {
  constructor(private radius: number) {}
  area(): number { return Math.PI * this.radius ** 2; }
}

class Rectangle implements Shape {
  constructor(private width: number, private height: number) {}
  area(): number { return this.width * this.height; }
}

class Triangle implements Shape {
  constructor(private base: number, private height: number) {}
  area(): number { return 0.5 * this.base * this.height; }
}
```

---

## Introduce Parameter Object

**When**: 3+ parameters frequently travel together, or function signatures are growing

**Steps**:
1. Identify parameters that logically group together
2. Create a class/interface for the group
3. Replace parameter list with the new object
4. Move related behavior into the object if applicable
5. Run tests

**Before**:
```typescript
function createEvent(
  title: string,
  startDate: Date,
  endDate: Date,
  location: string,
  isRecurring: boolean,
  recurrencePattern?: string
) { ... }

createEvent("Meeting", start, end, "Room A", true, "weekly");
```

**After**:
```typescript
interface EventConfig {
  title: string;
  dateRange: DateRange;
  location: string;
  recurrence?: RecurrenceConfig;
}

interface DateRange {
  start: Date;
  end: Date;
}

interface RecurrenceConfig {
  pattern: string;
}

function createEvent(config: EventConfig) { ... }

createEvent({
  title: "Meeting",
  dateRange: { start, end },
  location: "Room A",
  recurrence: { pattern: "weekly" },
});
```

---

## Decompose Conditional

**When**: Complex boolean expressions that are hard to read at a glance

**Steps**:
1. Identify the complex conditional
2. Extract each clause into a named function or variable
3. Replace original expression with named parts
4. Run tests

**Before**:
```typescript
if (
  user.subscription !== 'free' &&
  user.lastLogin > thirtyDaysAgo &&
  user.purchaseCount > 0 &&
  !user.isDeactivated
) {
  sendPromoEmail(user);
}
```

**After**:
```typescript
const isPaidUser = user.subscription !== 'free';
const isRecentlyActive = user.lastLogin > thirtyDaysAgo;
const hasPurchaseHistory = user.purchaseCount > 0;
const isActiveAccount = !user.isDeactivated;

const isEligibleForPromo = isPaidUser && isRecentlyActive && hasPurchaseHistory && isActiveAccount;

if (isEligibleForPromo) {
  sendPromoEmail(user);
}
```

---

## Replace Nested Conditional with Pipeline

**When**: Data transformation with multiple filter/map/reduce steps tangled in loops

**Steps**:
1. Identify the collection being processed
2. Convert loop body into chained operations (filter, map, reduce)
3. Give each step a meaningful name if complex
4. Run tests

**Before**:
```typescript
function getActiveUserEmails(users: User[]): string[] {
  const result: string[] = [];
  for (const user of users) {
    if (user.isActive) {
      if (user.email) {
        if (user.emailVerified) {
          result.push(user.email.toLowerCase());
        }
      }
    }
  }
  return result;
}
```

**After**:
```typescript
function getActiveUserEmails(users: User[]): string[] {
  return users
    .filter(user => user.isActive)
    .filter(user => user.email && user.emailVerified)
    .map(user => user.email!.toLowerCase());
}
```

---

## Extract Interface

**When**: Class has multiple responsibilities, or you need to improve testability

**Steps**:
1. Identify the subset of methods that represent a cohesive contract
2. Create an interface with those method signatures
3. Have the class implement the interface
4. Update consumers to depend on the interface
5. Run tests

**Before**:
```typescript
class PaymentService {
  async charge(amount: number, card: Card): Promise<Receipt> { ... }
  async refund(receiptId: string): Promise<void> { ... }
  getTransactionHistory(): Transaction[] { ... }
}

// Test requires a real PaymentService
function processOrder(service: PaymentService, order: Order) { ... }
```

**After**:
```typescript
interface PaymentGateway {
  charge(amount: number, card: Card): Promise<Receipt>;
  refund(receiptId: string): Promise<void>;
}

class StripePaymentService implements PaymentGateway {
  async charge(amount: number, card: Card): Promise<Receipt> { ... }
  async refund(receiptId: string): Promise<void> { ... }
  getTransactionHistory(): Transaction[] { ... }
}

// Now testable with mock
function processOrder(gateway: PaymentGateway, order: Order) { ... }
```

---

## Consolidate Duplicate Fragments

**When**: Same code appears in both branches of a conditional

**Steps**:
1. Identify identical code in if/else branches
2. Move common code before or after the conditional
3. Simplify the conditional to contain only differences
4. Run tests

**Before**:
```typescript
if (isSpecialDeal) {
  total = price * quantity * 0.95;
  sendConfirmation(total);
  logTransaction(total);
} else {
  total = price * quantity;
  sendConfirmation(total);
  logTransaction(total);
}
```

**After**:
```typescript
total = isSpecialDeal
  ? price * quantity * 0.95
  : price * quantity;
sendConfirmation(total);
logTransaction(total);
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
