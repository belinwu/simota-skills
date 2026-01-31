# Zen Code Smell Catalog & Complexity Metrics

Systematic detection and resolution of code smells with complexity measurements.

---

## CODE SMELL CATALOG

### Bloaters (Overly Large Code)

| Smell | Detection | Refactoring |
|-------|-----------|-------------|
| Long Method | > 20 lines | Extract Method |
| Large Class | > 200 lines, > 10 methods | Extract Class |
| Long Parameter List | > 4 parameters | Introduce Parameter Object |
| Data Clumps | Same fields in multiple classes | Extract Class |
| Primitive Obsession | Overuse of primitives for domain concepts | Replace with Value Object |

### Object-Orientation Abusers

| Smell | Detection | Refactoring |
|-------|-----------|-------------|
| Switch Statements | switch/if-else chains on type | Replace Conditional with Polymorphism |
| Refused Bequest | Subclass doesn't use inherited methods | Replace Inheritance with Delegation |
| Alternative Classes | Similar classes, different interfaces | Rename Method, Extract Superclass |
| Temporary Field | Fields only used in certain cases | Extract Class, Introduce Null Object |

### Change Preventers

| Smell | Detection | Refactoring |
|-------|-----------|-------------|
| Divergent Change | One class changes for many reasons | Extract Class |
| Shotgun Surgery | One change requires editing many classes | Move Method, Move Field, Inline Class |
| Parallel Inheritance | Creating subclass requires parallel subclass | Merge Hierarchies |

### Dispensables (Unnecessary Code)

| Smell | Detection | Refactoring |
|-------|-----------|-------------|
| Dead Code | Unused variables, functions, imports | Remove Dead Code |
| Speculative Generality | Unused abstractions "for future use" | Collapse Hierarchy, Inline Class |
| Comments | Comments explaining bad code | Rename, Extract Method (self-documenting) |
| Duplicate Code | Similar code in multiple places | Extract Method, Pull Up Method |
| Lazy Class | Class that does too little | Inline Class |

### Couplers (Excessive Coupling)

| Smell | Detection | Refactoring |
|-------|-----------|-------------|
| Feature Envy | Method uses another class's data more than its own | Move Method |
| Inappropriate Intimacy | Classes know too much about each other's internals | Move Method, Extract Class, Hide Delegate |
| Message Chains | a.getB().getC().getD() | Hide Delegate |
| Middle Man | Class only delegates to another | Remove Middle Man, Inline Method |

### Code Smell Report Format

```markdown
### Code Smell Analysis: [file]

| Line | Smell | Severity | Suggested Fix |
|------|-------|----------|---------------|
| 45 | Long Method | High | Extract calculateTotal() |
| 78 | Magic Number | Medium | Introduce MAX_RETRY constant |
| 102 | Dead Code | Low | Remove unused import |

**Priority**: Fix High severity items first
```

---

## COMPLEXITY METRICS

### Cyclomatic Complexity (CC)

Measures the number of linearly independent paths through code.

**Formula**: CC = E - N + 2P
- E: edges (control flow paths)
- N: nodes (statements)
- P: connected components (usually 1)

**Quick Calculation** - Count and add 1:
- `if`, `else if`, `else`
- `for`, `while`, `do-while`
- `case` (each case)
- `catch`
- `&&`, `||` (each operator)
- `? :` (ternary)

**Thresholds**:

| Score | Risk Level | Action Required |
|-------|------------|-----------------|
| 1-10 | Low | Acceptable, no action needed |
| 11-20 | Moderate | Consider refactoring |
| 21-50 | High | Must refactor, hard to test |
| 50+ | Very High | Untestable, split immediately |

### Cognitive Complexity

Measures how difficult code is to understand (not just test).

**Increments (+1 each)**:
- `if`, `else if`, `else`, `switch`
- `for`, `while`, `do-while`, `foreach`
- `catch`
- `break` or `continue` to label
- Sequences of binary logical operators
- Recursion

**Nesting Penalty**:
- +1 for each level of nesting (compounds difficulty)

**Thresholds**:

| Score | Readability | Action Required |
|-------|-------------|-----------------|
| 0-5 | Excellent | Keep as-is |
| 6-10 | Good | Consider simplifying |
| 11-15 | Moderate | Should simplify |
| 16+ | Poor | Must refactor |

### Complexity Report Format

```markdown
### Complexity Report: [file]

| Function | Lines | CC | Cognitive | Status |
|----------|-------|----|-----------| -------|
| processOrder | 45 | 12 | 8 | ⚠️ Moderate |
| validateInput | 80 | 25 | 18 | 🔴 High |
| formatDate | 10 | 3 | 2 | ✅ Good |
| handleSubmit | 60 | 35 | 22 | 🔴 Critical |

**File Average CC**: 18.75 (Target: < 10)
**Highest Cognitive**: 22 (Target: < 15)

**Recommendations**:
1. `handleSubmit`: Split into handleValidation, handleSubmission, handleResponse
2. `validateInput`: Extract validateRequired, validateFormat, validateRange
3. `processOrder`: Add guard clauses, reduce nesting
```
