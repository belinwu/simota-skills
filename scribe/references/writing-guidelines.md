# Writing Guidelines (Detailed)

## Requirement Writing

### Good Example

```markdown
**REQ-001**: User can login with email address
- Input: Email address (RFC 5322 compliant), Password (8-128 characters)
- Success: Return JWT token, status 200
- Failure: Error code "AUTH_001", status 401
- Rate limit: 5 requests/minute (per IP)
```

### Bad Example

```markdown
Enable user login
```

**Why bad:** No inputs, outputs, constraints, or error handling defined. Untestable.

---

## Acceptance Criteria Writing

### Good Example

```markdown
**AC-001**: Successful Login
Given: Valid email address and password
When: Call login API
Then: JWT token is returned
And: Token expires in 24 hours
```

### Bad Example

```markdown
Login should work
```

**Why bad:** No preconditions, no expected behavior, no verifiable outcome.

---

## Checklist Item Writing

### Good Example

```markdown
- [ ] **IMPL-001**: Add login() method to UserService
  - Input: LoginDto (email, password)
  - Output: AuthResponse (token, expiresAt)
  - Exception: InvalidCredentialsException
  - Reference: REQ-001
```

### Bad Example

```markdown
- [ ] Implement login feature
```

**Why bad:** No method signature, no I/O contract, no traceability to requirements.
