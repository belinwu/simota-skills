# Test Specification Template

## Template

```markdown
# Test Specification: [Feature Name]

## Document Info

| Item | Value |
|------|-------|
| Version | 1.0 |
| Author | [Name] |
| Status | Draft / Review / Approved |
| Created | YYYY-MM-DD |
| Updated | YYYY-MM-DD |
| Related PRD | PRD-[name] |
| Related SRS | SRS-[name] |

## Change History
...
```
' OR '1'='1
'; DROP TABLE users; --
1' AND '1'='1
```

**Expected Result:**
- All payloads are safely handled
- No SQL errors exposed
- No data leakage

### 5.3 Accessibility Tests

#### TC-A001: Screen Reader Compatibility

| Field | Value |
|-------|-------|
| **ID** | TC-A001 |
| **Title** | Form labels for screen readers |
| **Standard** | WCAG 2.1 Level AA |
...
```json
{
  "email": "valid@example.com",
  "password": "ValidPass123!",
  "name": "Test User"
}
```

#### Invalid Data Set
```json
{
  "email": "invalid-email",
  "password": "short",
  "name": ""
}
```

### 6.3 Data Setup Scripts
```sql
-- Insert test users
INSERT INTO users (email, name, role) VALUES
  ('test_admin@example.com', 'Admin User', 'admin'),
  ('test_user@example.com', 'Regular User', 'user');
```

---

## 7. Traceability Matrix

| Requirement | Test Cases | Status |
|-------------|------------|--------|
| FR-001 | TC-001, TC-002, TC-N001 | Ready |
| FR-002 | TC-003, TC-N002 | Ready |
| NFR-P001 | TC-P001 | Ready |
| NFR-S001 | TC-S001 | Ready |

---

## 8. Test Execution
...
```markdown
**Bug ID:** BUG-XXX
**Title:** [Brief description]
**Severity:** Critical / Major / Minor
**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
**Expected:** [What should happen]
**Actual:** [What actually happened]
**Environment:** [Browser/OS/Version]
**Screenshots:** [Attach if applicable]
```

---

## 10. Appendix

### A. Test Case Status Definitions
| Status | Definition |
|--------|------------|
| Not Run | Test has not been executed |
| Pass | Test completed successfully |
| Fail | Test did not meet expected results |
| Blocked | Test cannot run due to dependency |
| Skipped | Test intentionally not run |

### B. Glossary
...
```

---

## Quick Test Spec (Minimal)

For smaller features:

```markdown
# Test Spec: [Feature Name]

**Date:** YYYY-MM-DD | **Author:** [Name]

## Test Cases

| ID | Title | Priority | Steps | Expected Result | Status |
|----|-------|----------|-------|-----------------|--------|
| TC-001 | [Title] | P0 | [Steps] | [Result] | Not Run |
| TC-002 | [Title] | P1 | [Steps] | [Result] | Not Run |
| TC-N001 | [Negative] | P1 | [Steps] | [Error shown] | Not Run |

## Test Data
- Valid: [data]
- Invalid: [data]
...
```

---

## Gherkin Format Template

For BDD-style test specifications:

```gherkin
Feature: [Feature Name]
  As a [persona]
  I want to [action]
  So that [benefit]

  Background:
    Given the user is logged in
    And the system is in [state]

  @P0 @smoke
  Scenario: Successful [action]
    Given [precondition]
    When [action]
    Then [expected result]
    And [additional verification]
// ...
```

---

## Test Specification Quality Checklist

- [ ] All test cases have IDs (TC-XXX)
- [ ] All test cases have priority
- [ ] Traceability to requirements exists
- [ ] Preconditions are clear
- [ ] Test steps are reproducible
- [ ] Expected results are verifiable
- [ ] Test data is prepared
- [ ] Negative test cases are included
- [ ] Boundary value tests are included
- [ ] Exit criteria are defined
