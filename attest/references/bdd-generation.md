# BDD Scenario Generation

Rules and templates for generating Behavior-Driven Development scenarios from acceptance criteria.

---

## Generation Rules

### Core Principle

Every acceptance criterion produces **minimum 3 scenarios**:
1. **Happy path** — normal successful execution
2. **Negative path** — expected failure/rejection
3. **Edge/Boundary** — limits, thresholds, empty states

### Scenario ID Convention

```
SC-{criterion_id}-{type}-{NNN}

Types: HP (Happy Path), NP (Negative Path), BP (Boundary Probe), EP (Edge/Error Path)

Examples:
  SC-AC-LOGIN-001-HP-001  → Happy path for login criterion 1
  SC-AC-LOGIN-001-NP-001  → Negative path for login criterion 1
  SC-AC-LOGIN-001-BP-001  → Boundary probe for login criterion 1
```

---

## Given/When/Then Structure

### Given (Preconditions)

- Establish the initial state required for the scenario
- Include user roles, data state, system configuration
- Use concrete examples, not abstract descriptions

```gherkin
# Good
Given a registered user with email "user@example.com" and role "admin"

# Bad (too abstract)
Given a user exists in the system
```

### When (Action)

- One primary action per scenario
- Include the specific input values
- Describe the user action or system event

```gherkin
# Good
When the user submits the login form with email "user@example.com" and password "correct-password"

# Bad (multiple actions)
When the user opens the page and fills in the form and clicks submit
```

### Then (Expected Outcome)

- Observable, verifiable outcomes
- Include specific values where possible
- Multiple Then clauses for compound outcomes

```gherkin
# Good
Then the HTTP response status is 200
And the response body contains a valid JWT token
And the user is redirected to "/dashboard"

# Bad (vague)
Then the login is successful
```

---

## Scenario Templates by Category

### Happy Path Template

```gherkin
@happy-path @{criterion_id}
Scenario: {Descriptive name for successful case}
  Given {valid preconditions}
  And {additional context if needed}
  When {the primary action with valid inputs}
  Then {expected successful outcome}
  And {secondary outcomes}
```

### Negative Path Template

```gherkin
@negative @{criterion_id}
Scenario: {Descriptive name for failure case}
  Given {preconditions}
  When {the action with invalid/unauthorized input}
  Then {expected error response}
  And {system state remains unchanged}
```

### Boundary Probe Template

```gherkin
@boundary @{criterion_id}
Scenario: {Descriptive name for boundary case}
  Given {preconditions at boundary values}
  When {the action with boundary input}
  Then {expected behavior at boundary}
```

### Edge Case Template

```gherkin
@edge-case @{criterion_id}
Scenario: {Descriptive name for edge case}
  Given {unusual but valid preconditions}
  When {the action under edge conditions}
  Then {expected graceful handling}
```

---

## Common Scenario Patterns

### Authentication/Authorization

```gherkin
# Happy: Valid login
Scenario: User logs in with valid credentials
  Given a verified user with email "user@example.com"
  When the user submits login with correct password
  Then a session is created
  And the user is redirected to dashboard

# Negative: Invalid credentials
Scenario: Login rejected with wrong password
  Given a verified user with email "user@example.com"
  When the user submits login with incorrect password
  Then a 401 error is returned
  And no session is created

# Negative: Unauthorized access
Scenario: Non-admin cannot access admin panel
  Given a user with role "viewer"
  When the user requests "/admin/settings"
  Then a 403 error is returned

# Boundary: Account lockout threshold
Scenario: Account locked after max failed attempts
  Given a user with 4 failed login attempts
  When the user fails login again
  Then the account is locked
  And a lockout notification email is sent
```

### CRUD Operations

```gherkin
# Happy: Create
Scenario: Create new resource with valid data
  Given an authenticated user with "create" permission
  When the user submits a new {resource} with all required fields
  Then the {resource} is created with a unique ID
  And a 201 response is returned

# Negative: Duplicate
Scenario: Cannot create duplicate {resource}
  Given a {resource} with name "existing-name" already exists
  When the user creates a {resource} with name "existing-name"
  Then a 409 conflict error is returned

# Boundary: Maximum field length
Scenario: Create with maximum allowed name length
  Given an authenticated user
  When the user creates a {resource} with a 255-character name
  Then the {resource} is created successfully

# Boundary: Exceeds maximum
Scenario: Reject creation with name exceeding maximum
  Given an authenticated user
  When the user creates a {resource} with a 256-character name
  Then a 400 validation error is returned
```

### State Transitions

```gherkin
# Happy: Valid transition
Scenario: Order confirmed after payment
  Given an order in "PENDING" state
  When payment is successfully processed
  Then the order transitions to "CONFIRMED"

# Negative: Invalid transition
Scenario: Cannot ship an unconfirmed order
  Given an order in "PENDING" state
  When a ship request is submitted
  Then the request is rejected with "Invalid state transition"
  And the order remains in "PENDING" state
```

---

## Coverage Matrix

For each criterion, track scenario coverage:

```yaml
SCENARIO_COVERAGE:
  criterion_id: AC-LOGIN-001
  criterion_text: "Valid credentials grant access"
  scenarios:
    happy_path: 1    # Minimum 1
    negative: 2      # Minimum 1
    boundary: 1      # Minimum 1
    edge_case: 0     # Optional
  total: 4
  coverage_verdict: SUFFICIENT  # ≥3 scenarios = SUFFICIENT
```

### Minimum Coverage Requirements

| Priority | Min Scenarios | Required Types |
|----------|--------------|----------------|
| CRITICAL | 5 | HP(1) + NP(2) + BP(1) + EP(1) |
| HIGH | 3 | HP(1) + NP(1) + BP(1) |
| MEDIUM | 2 | HP(1) + NP(1) |
| LOW | 1 | HP(1) |

---

## Output Format

```yaml
BDD_SCENARIOS:
  spec_source: "docs/login-spec.md"
  total_criteria: 12
  total_scenarios: 42
  scenarios_by_type:
    happy_path: 12
    negative: 15
    boundary: 10
    edge_case: 5
  coverage_verdict: SUFFICIENT
  gherkin_file: "generated/login.feature"
```
