# Verification Methods

Static verification techniques for determining whether implementation satisfies specification criteria.

---

## Verification Approach

Attest performs **static verification** — analyzing source code without executing it. This is fundamentally different from test execution (Radar/Voyager) or runtime probing (Probe).

### What Attest Can Verify

| Aspect | Method | Confidence |
|--------|--------|------------|
| Feature existence | Code search for routes, handlers, components | HIGH |
| Data flow correctness | Trace input → processing → output | MEDIUM |
| Error handling presence | Search for try/catch, error handlers, validators | HIGH |
| State transitions | Map state management logic to spec'd states | MEDIUM |
| API contract | Match endpoint signatures to spec | HIGH |
| Business rule implementation | Logic trace through conditionals | MEDIUM |
| Configuration compliance | Check config values against spec | HIGH |

### What Requires Runtime Verification (NOT_TESTED)

| Aspect | Why Static Fails | Route To |
|--------|-----------------|----------|
| Performance thresholds | Needs execution timing | Bolt/Siege |
| Concurrency behavior | Needs parallel execution | Specter |
| Visual rendering | Needs browser rendering | Voyager/Echo |
| External API integration | Needs live endpoints | Voyager |
| User experience quality | Needs human evaluation | Warden |

---

## Verification Methods

### 1. Code Search

**Purpose:** Confirm that implementation artifacts exist for a criterion.

```
Criterion: AC-LOGIN-001 "Login endpoint accepts email/password"
→ Search: route definition matching POST /login or /auth
→ Search: handler function processing email + password parameters
→ Evidence: src/routes/auth.ts:42 — POST /api/auth/login handler
→ Verdict: PASS (implementation exists)
```

### 2. Logic Trace

**Purpose:** Follow data flow to verify business logic matches spec.

```
Criterion: AC-PAYMENT-003 "Discount is applied before tax calculation"
→ Trace: order.total → applyDiscount() → calculateTax()
→ Verify: discount applied BEFORE tax (not after)
→ Evidence: src/services/order.ts:89-102 — discount at L89, tax at L98
→ Verdict: PASS (correct ordering)
```

### 3. State Check

**Purpose:** Verify state machine matches specification.

```
Criterion: AC-ORDER-005 "Order transitions: PENDING → CONFIRMED → SHIPPED"
→ Map: state machine in src/models/order.ts
→ Verify: only specified transitions exist
→ Evidence: src/models/order.ts:23-45 — state enum + transition guards
→ Verdict: PARTIAL (CANCELLED state exists but not in spec)
```

### 4. Error Path

**Purpose:** Confirm error handling matches specified failure modes.

```
Criterion: AC-LOGIN-004 "Invalid credentials return 401 with error message"
→ Search: authentication failure handling
→ Verify: 401 status code + error message format
→ Evidence: src/middleware/auth.ts:67 — returns 401 + { error: "Invalid credentials" }
→ Verdict: PASS
```

### 5. Absence Check

**Purpose:** Detect criteria with NO corresponding implementation.

```
Criterion: AC-LOGIN-007 "Account lockout after 5 failed attempts"
→ Search: login attempt counter, lockout mechanism
→ Result: No lockout logic found anywhere in codebase
→ Evidence: NONE
→ Verdict: FAIL (criterion not implemented)
```

---

## Verdict Assignment

### Per-Criterion Verdicts

| Verdict | Definition | Evidence Required |
|---------|-----------|-------------------|
| **PASS** | Implementation fully satisfies criterion | ≥1 code reference with matching logic |
| **PARTIAL** | Implementation addresses criterion but misses aspects | Code reference + gap description |
| **FAIL** | Implementation contradicts or completely omits criterion | Absence evidence or contradiction evidence |
| **NOT_TESTED** | Cannot verify statically; requires runtime testing | Explanation of why static analysis insufficient |
| **AMBIGUOUS** | Specification too vague to determine compliance | Reference to AMBIGUOUS_FLAG |

### Verdict Decision Flow

```
1. Can the criterion be verified statically?
   ├── No → NOT_TESTED (with reason + route to Radar/Voyager)
   └── Yes
       2. Does implementation exist for this criterion?
          ├── No → FAIL (absence)
          └── Yes
              3. Does implementation match specification?
                 ├── Fully → PASS
                 ├── Partially → PARTIAL (describe gaps)
                 └── Contradicts → FAIL (describe contradiction)
```

---

## Evidence Format

```yaml
EVIDENCE:
  criterion_id: AC-LOGIN-001
  verdict: PASS
  method: CODE_SEARCH + LOGIC_TRACE
  references:
    - file: src/routes/auth.ts
      line: 42
      snippet: "router.post('/api/auth/login', authController.login)"
      relevance: "Endpoint definition matching spec"
    - file: src/controllers/auth.ts
      line: 78-95
      snippet: "async login(req, res) { ... }"
      relevance: "Handler validates email + password"
  gaps: []  # Empty for PASS
  notes: "Implementation matches spec. Password hashing uses bcrypt."
```

### Gap Description (for PARTIAL/FAIL)

```yaml
EVIDENCE:
  criterion_id: AC-LOGIN-007
  verdict: FAIL
  method: ABSENCE_CHECK
  references: []
  gaps:
    - type: MISSING_IMPLEMENTATION
      description: "Account lockout mechanism not found"
      spec_requirement: "Lock account after 5 failed login attempts"
      searched_locations:
        - src/controllers/auth.ts
        - src/middleware/auth.ts
        - src/models/user.ts
      impact: CRITICAL
  notes: "No login attempt tracking or lockout logic exists in codebase"
```

---

## Confidence Scoring

Each verification carries a confidence level:

| Confidence | Range | Meaning |
|-----------|-------|---------|
| **HIGH** | 0.8-1.0 | Clear code evidence, unambiguous match |
| **MEDIUM** | 0.5-0.8 | Likely match but complex logic paths |
| **LOW** | 0.2-0.5 | Indirect evidence, inference required |

When confidence < 0.5: mark as NOT_TESTED with recommendation for runtime verification.

---

## Resource Allocation Guideline

When scope or time is limited, allocate verification effort by priority:

| Priority | Effort Share | Minimum Scope |
|----------|-------------|---------------|
| CRITICAL | 40% | Full verification (all 5 methods + adversarial probes) |
| HIGH | 30% | Inspection + Analysis + basic probes |
| MEDIUM | 20% | Inspection + basic probes |
| LOW | 10% | Inspection only |

When forced to reduce scope further, always complete all CRITICAL criteria first, then HIGH, then sample MEDIUM. LOW criteria are deferred to AUDIT mode.
