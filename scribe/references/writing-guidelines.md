# Writing Guidelines

Purpose: Use this file when a draft is technically correct but still vague, untestable, or hard for downstream agents to act on.

Contents:

- Requirement writing
- Acceptance criteria writing
- Checklist item writing

## Requirement Writing

### Good Example

```markdown
**REQ-001**: User can log in with an email address.
- Input: Email address (RFC 5322 compliant), password (8-128 characters)
- Success: Return JWT token, status 200
- Failure: Error code "AUTH_001", status 401
- Rate limit: 5 requests/minute per IP
```

### Bad Example

```markdown
Enable user login
```

Why it fails:

- No input contract
- No output contract
- No constraints or error behavior
- Not testable

## Acceptance Criteria Writing

### Good Example

```markdown
**AC-001**: Successful login
Given a valid email address and password
When the login API is called
Then a JWT token is returned
And the token expires in 24 hours
```

### Bad Example

```markdown
Login should work
```

Why it fails:

- No preconditions
- No system action
- No observable result

## Checklist Item Writing

### Good Example

```markdown
- [ ] **IMPL-001**: Add `login()` to `UserService`
  - Input: `LoginDto` (`email`, `password`)
  - Output: `AuthResponse` (`token`, `expiresAt`)
  - Exception: `InvalidCredentialsException`
  - Reference: `REQ-001`
```

### Bad Example

```markdown
- [ ] Implement login feature
```

Why it fails:

- No concrete deliverable
- No I/O contract
- No traceability

## Quick Rules

- Prefer one testable sentence over a long paragraph.
- Write `What` and `Why` in PRD; move `How` to design docs.
- Every requirement should map to acceptance criteria, design, and tests.
- If a sentence cannot be verified, rewrite it.
