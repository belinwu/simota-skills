# Fossil Extraction Patterns

## Code-Level Extraction

### Conditional Branch Analysis

Look for business rules encoded in `if/else`, `switch`, and guard clauses.

```
Pattern: Nested conditionals with magic numbers
Signal: if (order.total > 10000 && customer.tier === 3)
Action: Extract as "High-value order threshold rule"
Confidence: MEDIUM (code-only, needs test/comment confirmation)
```

### Magic Number Decoding

| Code pattern | Likely meaning | Extraction |
|-------------|---------------|------------|
| `status === 7` | Domain-specific state | Map to enum/constant; find all states |
| `amount > 50000` | Business threshold | Document threshold and its purpose |
| `days <= 30` | Time window rule | Document SLA or retention period |
| `retry < 3` | Operational limit | Document retry policy |

### Validation Rule Extraction

```
Source: Input validation functions, middleware, model validators
Look for:
- Required field checks → mandatory data rules
- Format validations (regex) → data format rules
- Range checks → business constraint rules
- Cross-field validations → business logic rules
- Custom error messages → rule descriptions
```

## Test-Level Extraction

### Assertion-to-Rule Mapping

```
Test: expect(calculateDiscount(order)).toBe(0.15)
Rule: Orders receive 15% discount under certain conditions
Action: Read test name, setup, and assertions to reconstruct full rule
```

### Edge Case Mining

```
Test name patterns that reveal rules:
- "should reject when..." → constraint rule
- "should apply discount when..." → business rule
- "should not allow..." → prohibition rule
- "handles legacy..." → backward compatibility rule
- "regression: #123" → historical bug-driven rule
```

### Fixture Analysis

```
Test fixtures reveal:
- Valid/invalid data boundaries → validation rules
- User roles and permissions → authorization rules
- State transitions → workflow rules
- Date ranges → temporal rules
```

## Schema-Level Extraction

### Column Archaeology

| Signal | Investigation |
|--------|--------------|
| `is_active` / `deleted_at` | Soft delete policy |
| `legacy_*` prefix | Migration-era columns |
| `_v2` suffix | Schema evolution point |
| Nullable column that was NOT NULL | Rule relaxation event |
| CHECK constraint | Business constraint |
| DEFAULT value | Business default rule |
| Unused index | Performance rule from past load pattern |

### Naming Convention Evolution

```
Pattern: users.account_type → users.plan_tier (renamed)
Signal: Column rename in migration history
Action: Document that "account_type" and "plan_tier" are the same concept
Risk: Code may still reference old name via raw SQL
```

## Comment/History Extraction

### Comment Pattern Recognition

| Pattern | Value |
|---------|-------|
| `// HACK:` / `// WORKAROUND:` | Compensating logic for upstream issue |
| `// NOTE:` / `// IMPORTANT:` | Design decision or constraint |
| `// TODO:` / `// FIXME:` | Known incomplete implementation |
| `// @see ticket-123` | External context reference |
| `// DO NOT REMOVE` | Critical but non-obvious dependency |

### Commit Message Mining

```bash
# Find commits that mention business rules
git log --all --grep="business rule" --grep="requirement" --grep="regulation" --or

# Find reverted commits (may indicate abandoned rules)
git log --all --grep="Revert"

# Find commits with "fix" that reference specific modules
git log --all --grep="fix" -- path/to/module/
```

## Cross-Reference Validation

### Multi-Source Confirmation Matrix

```
Rule: "Orders over ¥10,000 get free shipping"

Code:    if (order.total >= 10000) shipping = 0  ← Found
Test:    test('free shipping for orders over 10000') ← Confirmed
Schema:  orders.shipping_threshold DEFAULT 10000 ← Confirmed
Comment: // Free shipping threshold per business req ← Confirmed
History: commit abc123 "add free shipping rule" ← Confirmed

Confidence: HIGH (4/5 sources confirm)
```

### Conflict Resolution

When sources disagree:

1. **Code vs Test**: Code is current truth; test may be outdated
2. **Code vs Comment**: Code is current truth; comment may be stale
3. **Code vs Schema**: Check which was modified more recently
4. **Multiple code paths**: May be A/B test or gradual rollout
5. **Dead code vs Live code**: Dead code may preserve abandoned rule

## Migration Risk Scoring

| Factor | Low risk | Medium risk | High risk |
|--------|----------|-------------|-----------|
| Test coverage | >80% of rule | 40-80% | <40% |
| Source confirmation | 3+ sources | 2 sources | 1 source only |
| Last modification | <6 months | 6-24 months | >24 months |
| Dependencies | 0-2 dependents | 3-5 | 6+ |
| Complexity | Linear logic | Branching | Nested + external |
