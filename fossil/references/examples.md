# Fossil Examples

## Example 1: Business Rule Catalog (E-commerce Order Module)

```markdown
# Business Rule Catalog: Order Module

**Scope:** src/orders/, src/checkout/, src/shipping/
**Files analyzed:** 47
**Rules extracted:** 12
**Date:** 2026-04-09

## Summary

| Confidence | Count |
|-----------|-------|
| HIGH | 5 |
| MEDIUM | 4 |
| LOW | 2 |
| SPECULATIVE | 1 |

---

### Rule ORD-001: Free Shipping Threshold

- **Description:** Orders totaling ¥10,000 or more qualify for free shipping
- **Confidence:** HIGH
- **Source:**
  - Code: `src/shipping/calculator.ts:45` — `if (order.subtotal >= 10000) return 0`
  - Test: `tests/shipping.test.ts:test('free shipping over 10000')`
  - Schema: `orders.free_shipping_threshold DEFAULT 10000`
  - History: `commit a1b2c3d "feat(shipping): add free shipping rule" (2024-03-15)`
- **Test coverage:** Yes — `shipping.test.ts:L23-L35`
- **Migration risk:** Low
- **Notes:** Threshold is hardcoded in 3 places; should be configurable

---

### Rule ORD-002: Maximum Cart Items

- **Description:** Cart is limited to 99 items
- **Confidence:** MEDIUM
- **Source:**
  - Code: `src/cart/validation.ts:22` — `if (items.length > 99) throw CartLimitError`
  - Test: `tests/cart.test.ts:test('rejects cart with 100+ items')`
- **Test coverage:** Yes
- **Migration risk:** Low
- **Notes:** Limit may be arbitrary; no business justification found in comments or history

---

### Rule ORD-007: [SPECULATIVE] Holiday Surcharge

- **Description:** Orders placed during Golden Week may have a 5% surcharge
- **Confidence:** SPECULATIVE
- **Source:**
  - Code: `src/pricing/surcharge.ts:88` — Dead code block with `isGoldenWeek()` check
  - History: `commit f4e5d6c "add holiday pricing" (2023-04-20)` followed by `commit g7h8i9j "disable holiday surcharge temporarily" (2023-05-02)`
- **Test coverage:** No (tests also commented out)
- **Migration risk:** Medium — may need reactivation
- **Notes:** Logic exists but is disabled. Confirm with business whether this rule is still planned
```

## Example 2: Migration Risk Map

```markdown
# Migration Risk Map: Auth Module → OAuth2

**Current:** Custom session-based auth (src/auth/)
**Target:** OAuth2 + JWT

## Risk Summary

| Risk level | Rules | Action needed |
|-----------|-------|---------------|
| High | 3 | Must resolve before migration |
| Medium | 4 | Plan mitigation |
| Low | 5 | Monitor during migration |

## High-Risk Items

### RISK-001: Implicit Session Timeout Rules
Multiple timeout values hardcoded across 7 files with no single source of truth.
- `auth/session.ts:30` — 30 minutes
- `middleware/timeout.ts:15` — 15 minutes (different!)
- `config/auth.json` — 3600 seconds
**Action:** Consolidate before migration; determine authoritative value

### RISK-002: Admin Backdoor Authentication
`src/auth/admin.ts:45` contains a legacy authentication bypass for internal tools.
No test coverage. Only found via code + comment archaeology.
**Action:** Confirm if still needed; design OAuth2 equivalent or remove
```
