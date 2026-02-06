# OWASP Top 10 Checklist & Audit Templates

Systematic security audit checklist based on OWASP Top 10 (2021), audit report format, and dependency scanning.

---

## OWASP Top 10 Checklist (2021)

### A01: Broken Access Control
- [ ] Authorization checks on all endpoints
- [ ] Deny by default for resources
- [ ] Rate limiting on APIs
- [ ] CORS properly configured
- [ ] Directory listing disabled
- [ ] JWT/session validation on every request

### A02: Cryptographic Failures
- [ ] Sensitive data encrypted at rest
- [ ] TLS 1.2+ for data in transit
- [ ] Strong hashing for passwords (bcrypt, argon2)
- [ ] No deprecated crypto algorithms (MD5, SHA1)
- [ ] Secrets not in source code
- [ ] Proper key management

### A03: Injection
- [ ] Parameterized queries for SQL
- [ ] Input validation on all user data
- [ ] Output encoding for XSS prevention
- [ ] Command injection prevention
- [ ] LDAP injection prevention
- [ ] NoSQL injection prevention

### A04: Insecure Design
- [ ] Threat modeling performed
- [ ] Security requirements defined
- [ ] Secure design patterns used
- [ ] Business logic abuse prevention
- [ ] Rate limiting for resource-intensive operations

### A05: Security Misconfiguration
- [ ] Security headers configured (CSP, X-Frame-Options, etc.)
- [ ] Error messages don't leak info
- [ ] Unnecessary features disabled
- [ ] Default credentials changed
- [ ] Cloud/server hardening applied

### A06: Vulnerable Components
- [ ] Dependencies up to date
- [ ] No known CVEs in dependencies
- [ ] Components from trusted sources
- [ ] Unused dependencies removed
- [ ] SBOM (Software Bill of Materials) maintained

### A07: Authentication Failures
- [ ] Multi-factor authentication available
- [ ] Weak password prevention
- [ ] Brute force protection
- [ ] Secure password recovery
- [ ] Session management secure

### A08: Software and Data Integrity
- [ ] CI/CD pipeline secured
- [ ] Code signing implemented
- [ ] Dependency integrity verified
- [ ] Deserialization input validated

### A09: Security Logging & Monitoring
- [ ] Login/access failures logged
- [ ] Security events monitored
- [ ] Logs protected from tampering
- [ ] Alerting for suspicious activity

### A10: Server-Side Request Forgery (SSRF)
- [ ] URL validation for external requests
- [ ] Allowlist for permitted destinations
- [ ] Network segmentation in place

---

## Security Audit Report Template

### Executive Summary

| Metric | Value |
|--------|-------|
| Scan Date | YYYY-MM-DD |
| Files Scanned | X |
| Critical Issues | X |
| High Issues | X |
| Medium Issues | X |
| Low Issues | X |
| OWASP Coverage | X/10 |

### Risk Matrix

| Severity | Count | Status |
|----------|-------|--------|
| CRITICAL | X | Immediate action required |
| HIGH | X | Fix within 24 hours |
| MEDIUM | X | Fix within 1 week |
| LOW | X | Fix when convenient |

### Finding Template

```markdown
#### [SEVERITY-NNN] Finding Title

- **File**: `src/path/file.js:42`
- **OWASP**: A0X - Category Name
- **Risk**: Description of what could happen if exploited
- **Evidence**: `code snippet showing the issue`
- **Remediation**: Steps to fix the issue
- **Status**: Open / In Progress / Fixed
```

### Dependency Vulnerabilities Table

| Package | Version | Severity | CVE | Fix Version |
|---------|---------|----------|-----|-------------|
| example | 1.0.0 | High | CVE-XXXX-XXXXX | 1.0.1 |

### Recommendations Section

1. **Immediate**: Fix all Critical and High issues
2. **Short-term**: Update vulnerable dependencies
3. **Long-term**: Implement security testing in CI/CD

---

## Dependency Vulnerability Scanning

### npm/yarn Projects

```bash
# npm audit
npm audit --json > audit-report.json

# yarn audit
yarn audit --json > audit-report.json

# With Snyk
npx snyk test --json > snyk-report.json
```

### Interpreting Results

| Severity | Action |
|----------|--------|
| Critical | Block deployment |
| High | Fix before release |
| Moderate | Fix in next sprint |
| Low | Track and plan |

### Resolution Commands

```bash
npm update package-name
npm audit fix
npm audit fix --force  # For breaking changes
```

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Security Audit
  run: |
    npm audit --audit-level=high
    if [ $? -ne 0 ]; then
      echo "High severity vulnerabilities found"
      exit 1
    fi
```
