# Security-Aware Change Analysis Reference

Guardian's security analysis patterns and detection rules.

## Security Impact Categories

| Category | Description | Action |
|----------|-------------|--------|
| **CRITICAL** | Auth, crypto, secrets, permissions | Immediate Sentinel handoff |
| **SENSITIVE** | User data, session, API keys | Sentinel review recommended |
| **ADJACENT** | Code near security boundaries | Monitor for side effects |
| **NEUTRAL** | No security implications | Standard review |

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
