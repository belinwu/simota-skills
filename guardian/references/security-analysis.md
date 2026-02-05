# Security-Aware Change Analysis Reference

Guardian's security analysis patterns, detection rules, and escalation criteria.

## Security Impact Categories

| Category | Description | Action |
|----------|-------------|--------|
| **CRITICAL** | Auth, crypto, secrets, permissions | Immediate Sentinel handoff |
| **SENSITIVE** | User data, session, API keys | Sentinel review recommended |
| **ADJACENT** | Code near security boundaries | Monitor for side effects |
| **NEUTRAL** | No security implications | Standard review |

---

## Classification Criteria

### CRITICAL Classification

**Auto-handoff to Sentinel: REQUIRED (Blocking)**

```yaml
critical_criteria:
  file_patterns:
    - "**/auth/**"
    - "**/security/**"
    - "**/crypto/**"
    - "**/permissions/**"
    - "**/rbac/**"
    - "**/acl/**"
    - "**/*.key"
    - "**/*.pem"
    - ".env*"
    - "**/secrets/**"

  code_patterns:
    - jwt_handling: "jwt.sign|jwt.verify|jsonwebtoken"
    - crypto_operations: "crypto\.|bcrypt|argon2|scrypt"
    - auth_logic: "authenticate|authorize|login|logout|session"
    - permission_checks: "hasPermission|canAccess|isAuthorized"
    - key_management: "privateKey|secretKey|apiKey|API_KEY"

  change_types:
    - Token generation or validation logic modified
    - Password hashing algorithm changed
    - Session management altered
    - Permission check removed or weakened
    - Crypto implementation modified
    - Secret handling changed

  auto_triggers:
    - ANY file in critical directory changed
    - ANY critical code pattern modified
    - Dangerous pattern detected (eval, exec, raw SQL)
    - Secret exposure risk identified
```

### SENSITIVE Classification

**Auto-handoff to Sentinel: RECOMMENDED (Non-blocking)**

```yaml
sensitive_criteria:
  file_patterns:
    - "**/api/**"
    - "**/middleware/**"
    - "**/handlers/**"
    - "**/user/**"
    - "**/profile/**"
    - "**/payment/**"
    - "**/session/**"

  code_patterns:
    - user_data: "user\.|profile\.|email|phone|address"
    - api_endpoints: "@Get|@Post|router\.|app\.get|app\.post"
    - data_validation: "validate|sanitize|escape"
    - session_ops: "session\.|cookie\.|localStorage"

  change_types:
    - User data access patterns changed
    - API endpoint authorization modified
    - Input validation logic altered
    - Session/cookie handling updated

  combined_triggers:
    - SENSITIVE file + auth-related import
    - SENSITIVE file + database write operation
    - API endpoint + missing validation
```

### ADJACENT Classification

**Monitor and flag, no auto-handoff**

```yaml
adjacent_criteria:
  file_patterns:
    - "**/config/**"
    - "**/settings/**"
    - "**/database/**"
    - "**/migration/**"

  change_types:
    - Configuration that affects security behavior
    - Database schema changes for auth tables
    - Environment variable handling
    - Third-party service integration

  monitoring:
    - Flag in PR description
    - Recommend reviewer attention
    - Include in security checklist
```

### NEUTRAL Classification

**Standard review process**

```yaml
neutral_criteria:
  indicators:
    - No security-related file patterns matched
    - No dangerous code patterns detected
    - No auth/crypto imports
    - Pure UI/presentation changes
    - Test file only changes
    - Documentation updates

  action:
    - Standard review process
    - No security handoff needed
```

---

## Escalation Decision Flow

```
┌─────────────────────────────────────┐
│     Analyze Changed Files            │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│   Match Against File Patterns        │
└─────────────────┬───────────────────┘
                  ↓
         ┌───────────────┐
         │ Critical      │──YES──→ CRITICAL Classification
         │ Pattern?      │         → AUTO Sentinel Handoff (BLOCKING)
         └───────┬───────┘
                 │NO
                 ↓
┌─────────────────────────────────────┐
│   Scan for Dangerous Code Patterns   │
└─────────────────┬───────────────────┘
                  ↓
         ┌───────────────┐
         │ Dangerous     │──YES──→ CRITICAL Classification
         │ Pattern?      │         → AUTO Sentinel Handoff (BLOCKING)
         └───────┬───────┘
                 │NO
                 ↓
         ┌───────────────┐
         │ Sensitive     │──YES──→ SENSITIVE Classification
         │ Pattern?      │         → Sentinel Handoff (RECOMMENDED)
         └───────┬───────┘
                 │NO
                 ↓
         ┌───────────────┐
         │ Adjacent      │──YES──→ ADJACENT Classification
         │ Pattern?      │         → Flag in PR (MONITOR)
         └───────┬───────┘
                 │NO
                 ↓
                 NEUTRAL Classification
                 → Standard Review
```

---

## Sentinel Auto-Link Protocol

### Handoff Trigger Conditions

```yaml
auto_handoff_triggers:
  immediate_blocking:
    conditions:
      - classification: CRITICAL
      - dangerous_pattern_count: "> 0"
      - secret_exposure: true
    action:
      type: GUARDIAN_TO_SENTINEL_HANDOFF
      blocking: true
      timeout: "24h"

  recommended_non_blocking:
    conditions:
      - classification: SENSITIVE
      - auth_files_involved: true
    action:
      type: GUARDIAN_TO_SENTINEL_HANDOFF
      blocking: false
      flag_in_pr: true

  conditional:
    conditions:
      - classification: SENSITIVE
      - no_auth_involvement: true
    action:
      type: FLAG_FOR_REVIEW
      suggest_sentinel: true
```

### Response Handling Protocol

```yaml
sentinel_response_handling:
  on_approved:
    action: "Clear security gate"
    update_status: SUCCESS
    pr_badge: "Security Approved"
    proceed_to: Judge

  on_issues_high:
    action: "Block merge"
    update_status: BLOCKED
    create_issues: true
    notify: PR_AUTHOR
    require: "Fix and re-review"

  on_issues_medium:
    action: "Warn but allow proceed"
    update_status: PARTIAL
    flag_issues: true
    require: "Acknowledge before merge"

  on_issues_low:
    action: "Advisory only"
    update_status: SUCCESS
    include_in_pr: true
    recommend: "Address in follow-up"

  on_timeout:
    action: "Escalate to human"
    update_status: BLOCKED
    alert: SECURITY_TEAM
    fallback: "Manual review required"
```

---

## Probe Integration (DAST)

### API Change Detection

```yaml
probe_triggers:
  endpoint_changes:
    - New API endpoint created
    - Authentication middleware modified
    - Authorization logic changed
    - Input validation altered

  auto_handoff:
    condition: "api_endpoint_changed AND (auth_modified OR validation_modified)"
    target: Probe
    request: DAST_SCAN
    environment: STAGING
```

### Probe Handoff Template

```markdown
## GUARDIAN_TO_PROBE_HANDOFF

**Trigger**: API endpoint security verification

**Changed Endpoints**:
| Endpoint | Method | Change | Risk |
|----------|--------|--------|------|
| /api/auth/login | POST | Auth logic modified | HIGH |
| /api/users/:id | PATCH | Validation changed | MEDIUM |

**DAST Targets**:
- [ ] Authentication bypass
- [ ] Authorization boundary
- [ ] Input injection
- [ ] Session fixation
- [ ] CSRF protection

**Request**: Execute DAST scan before merge approval
```

## Security-Related File Patterns

```yaml
security_file_patterns:
  critical:
    directories:
      - auth/
      - security/
      - crypto/
      - permissions/
      - rbac/
      - acl/
    files:
      - "**/auth*.{ts,js,py,go,java}"
      - "**/login*.{ts,js,py,go,java}"
      - "**/session*.{ts,js,py,go,java}"
      - "**/*.key"
      - "**/*.pem"
      - ".env*"
      - "**/secrets.*"

  sensitive:
    directories:
      - api/
      - middleware/
      - handlers/
    patterns:
      - "**/user*.{ts,js,py,go,java}"
      - "**/profile*.{ts,js,py,go,java}"
      - "**/payment*.{ts,js,py,go,java}"

  adjacent:
    - config/
    - settings/
    - database/
```

## Dangerous Code Patterns

```yaml
dangerous_patterns:
  credential_exposure:
    - password
    - token
    - secret
    - api_key
    - apiKey
    - private_key
    - jwt
    - bearer

  injection_risk:
    - eval(
    - exec(
    - innerHTML
    - dangerouslySetInnerHTML
    - raw(
    - unsafeHTML
    - "sql`" # Raw SQL

  crypto_concerns:
    - md5
    - sha1
    - DES
    - "rand()" # Non-crypto random
```

## Security Analysis Report Template

```markdown
## Security Impact Assessment

### Classification
```
CRITICAL:   ██░░░░░░░░ 2 files (auth/)
SENSITIVE:  ███░░░░░░░ 4 files (api/, user data)
ADJACENT:   █░░░░░░░░░ 1 file (config/)
NEUTRAL:    ██████░░░░ 15 files
```

### Critical Changes (Sentinel Handoff Required)
| File | Change | Risk |
|------|--------|------|
| `src/auth/jwt.ts` | Token validation modified | HIGH - verify no bypass |
| `src/auth/oauth.ts` | New OAuth provider | MEDIUM - scope review |

### Dangerous Patterns Detected
| File | Pattern | Line | Concern |
|------|---------|------|---------|
| `src/api/query.ts` | raw SQL | 45 | Injection risk |
| `src/utils/render.ts` | innerHTML | 23 | XSS potential |

### Recommendation
1. **Handoff to Sentinel** for static security analysis
2. **Handoff to Probe** for DAST if API changes detected
3. Block merge until security review complete
```

## AI-Generated Code Detection

### Detection Patterns (Code-Based Only)

```yaml
ai_code_indicators:
  naming_patterns:
    - Generic variable names: data, result, temp, value, item, output
    - Sequential naming: data1, data2, func1, func2
    - Overly verbose: getUserByIdFromDatabase, processDataAndReturnResult

  structural_patterns:
    - Unusual code density (high logic per function)
    - Inconsistent with project patterns
    - Overly uniform comment styles
    - Perfect but context-unaware implementations

  project_mismatch:
    - Different naming conventions than existing code
    - Unfamiliar utility patterns
    - Imports not matching project structure
```

### AI Code Categories

| Category | Indicator | Action |
|----------|-----------|--------|
| **Verified** | Reviewed and tested | Proceed normally |
| **Suspected** | Pattern match detected | Request Judge verification |
| **Untested** | New code without tests | Radar test coverage |
| **Human** | No AI indicators | Standard review |

### AI Detection in Analysis Report

```markdown
### AI Code Assessment
```
AI Suspected:   ██░░░░░░░░ 20% (5 files)
Untested:       █░░░░░░░░░ 10% (3 files)
Verified/Human: ███████░░░ 70% (17 files)
```

**Suspected AI-Generated Files**:
| File | Indicators | Recommendation |
|------|------------|----------------|
| `src/utils/parser.ts` | Generic naming, uniform comments | Request Judge verification |
| `src/api/handler.ts` | Perfect but context-unaware | Add integration tests |

→ Handoff to Judge for dependency verification and hallucination check
```
