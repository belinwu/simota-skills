# OWASP Top 10 (2025) Checklist & Audit Templates

Purpose: Map Sentinel findings to OWASP Top 10 (2025), run checklist-driven audits, and produce consistent security reports.

## Contents

- Top 10 overview
- category checklist
- audit report template
- risk matrix
- 2021 -> 2025 migration
- Sentinel scan mapping

## OWASP Top 10 (2025) Overview

| Rank | Category | Change from 2021 |
|------|----------|------------------|
| `A01` | Broken Access Control | Kept; SSRF folded in |
| `A02` | Security Misconfiguration | Moved up from `#5` to `#2` |
| `A03` | Software Supply Chain Failures | New category |
| `A04` | Cryptographic Failures | Moved down from `#2` |
| `A05` | Injection | Moved down from `#3`; Prompt Injection added |
| `A06` | Insecure Design | Moved down from `#4` |
| `A07` | Authentication Failures | Kept |
| `A08` | Software or Data Integrity Failures | Kept |
| `A09` | Logging & Alerting Failures | Renamed from Monitoring |
| `A10` | Mishandling of Exceptional Conditions | New category |

## Category Checklist

| Category | What to check |
|----------|---------------|
| `A01 Broken Access Control` | deny-by-default authz, ownership checks, IDOR/BOLA, SSRF allowlists, internal IP blocking |
| `A02 Security Misconfiguration` | security headers (`CSP`, `HSTS`, `X-Frame-Options`, `X-Content-Type-Options`), no stack traces, debug disabled, cloud hardening |
| `A03 Supply Chain Failures` | SBOM (`SPDX` / `CycloneDX`), transitive CVEs, unused packages, CI/CD security, artifact signatures, lockfile integrity |
| `A04 Cryptographic Failures` | encryption at rest/in transit, `TLS 1.2+`, strong password hashing (`bcrypt`, `argon2`), no `MD5`/`SHA1`, safe key management |
| `A05 Injection` | parameterized SQL, output encoding, command/LDAP/NoSQL protection, prompt-injection review for AI features |
| `A06 Insecure Design` | threat modeling, secure design patterns, resource-abuse prevention, rate limits on expensive operations |
| `A07 Authentication Failures` | MFA support, brute-force protection, secure recovery, safe session management |
| `A08 Software or Data Integrity Failures` | CI/CD protection, code signing, dependency integrity, deserialization validation |
| `A09 Logging & Alerting Failures` | auth failure logging, tamper resistance, alerting on suspicious activity |
| `A10 Exceptional Conditions` | empty `catch`, sensitive error leaks (`CWE-209`), fail-open (`CWE-636`), unhandled rejections, unsafe null access, resource leaks |

## Security Audit Report Template

### Executive Summary

| Metric | Value |
|--------|-------|
| Scan Date | `YYYY-MM-DD` |
| Files Scanned | `X` |
| Critical / High / Medium / Low | `X / X / X / X` |
| OWASP 2025 Coverage | `X/10` |

### Risk Matrix

| Severity | Count | Action |
|----------|-------|--------|
| `CRITICAL` | `X` | Immediate response |
| `HIGH` | `X` | Fix within `24h` |
| `MEDIUM` | `X` | Fix within `1 week` |
| `LOW` | `X` | Plan intentionally |

### Finding Template

```markdown
#### [SEVERITY-NNN] Finding Title
- **File**: `src/path/file.js:42`
- **OWASP 2025**: A0X - Category Name
- **Risk**: Impact if exploited
- **Evidence**: `code snippet showing the issue`
- **Remediation**: Exact fix or mitigation
- **Status**: Open / In Progress / Fixed
```

### Recommendation Cadence

1. `Immediate`: fix all `CRITICAL` and `HIGH`
2. `Short-term`: update vulnerable dependencies and harden configs
3. `Long-term`: integrate security checks into CI/CD

## 2021 -> 2025 Migration

| 2021 | 2025 | Note |
|------|------|------|
| A01 Broken Access Control | `A01` | SSRF integrated |
| A02 Cryptographic Failures | `A04` | Lower rank |
| A03 Injection | `A05` | Prompt Injection added |
| A04 Insecure Design | `A06` | Lower rank |
| A05 Security Misconfiguration | `A02` | Cloud misconfigurations emphasized |
| A06 Vulnerable Components | `A03` | Expanded to supply chain |
| A09 Logging & Monitoring | `A09` | Renamed to Logging & Alerting |
| A10 SSRF | folded into `A01` | No longer standalone |
| none | `A10 Exceptional Conditions` | New category covering `24` CWEs |

## Sentinel Scan Mapping

| Sentinel scan area | OWASP 2025 | Notes |
|--------------------|-------------|-------|
| Secret detection | `A07` | Credential and auth failure surface |
| SQLi / XSS / command injection | `A05` | Includes prompt injection for AI systems |
| Input validation | `A05` + `A10` | Injection plus exceptional-condition safety |
| Security headers | `A02` | Includes `CSP` |
| Dependency CVEs and SBOM | `A03` | Full supply-chain scope |
| Error handling and resource leaks | `A10` | Newly emphasized in 2025 |
