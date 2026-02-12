# Nuclei Templates Reference

Nuclei enables rapid, template-based vulnerability scanning. Use custom templates for project-specific checks.

## Template Structure

```yaml
# nuclei-template-structure.yaml
id: template-unique-id
info:
  name: "Human readable name"
  author: "your-name"
  severity: critical|high|medium|low|info
  description: "What this template detects"
  reference:
    - https://cve.mitre.org/...
    - https://owasp.org/...
  tags: tag1,tag2,tag3

requests:
  - method: GET|POST|PUT|DELETE
    path:
      - "{{BaseURL}}/path"
    matchers:
      - type: word|regex|status|dsl
        words:
          - "pattern to match"
```

## Common Security Templates

### Sensitive File Exposure

```yaml
id: sensitive-file-exposure
info:
  name: "Sensitive File Exposure"
  author: "probe-agent"
  severity: high
  description: "Detects exposed sensitive files"
  tags: exposure,config,sensitive

requests:
  - method: GET
    path:
      - "{{BaseURL}}/.env"
      - "{{BaseURL}}/.git/config"
      - "{{BaseURL}}/config.php.bak"
      - "{{BaseURL}}/database.yml"
      - "{{BaseURL}}/wp-config.php.bak"
      - "{{BaseURL}}/.aws/credentials"
      - "{{BaseURL}}/.docker/config.json"
    matchers-condition: or
    matchers:
      - type: word
        words:
          - "DB_PASSWORD"
          - "AWS_SECRET"
          - "api_key"
          - "[core]"  # git config
        condition: or
      - type: status
        status:
          - 200
```

### Debug Endpoint Exposure

```yaml
id: debug-endpoint-exposure
info:
  name: "Debug Endpoint Exposure"
  author: "probe-agent"
  severity: medium
  description: "Detects exposed debug/admin endpoints"
  tags: debug,admin,misconfiguration

requests:
  - method: GET
    path:
      - "{{BaseURL}}/debug"
      - "{{BaseURL}}/_debug"
      - "{{BaseURL}}/actuator"
      - "{{BaseURL}}/actuator/health"
      - "{{BaseURL}}/actuator/env"
      - "{{BaseURL}}/__debug__"
      - "{{BaseURL}}/graphql?query={__schema{types{name}}}"
      - "{{BaseURL}}/api/swagger.json"
      - "{{BaseURL}}/phpinfo.php"
    stop-at-first-match: true
    matchers-condition: or
    matchers:
      - type: word
        words:
          - "\"status\":\"UP\""
          - "__schema"
          - "swagger"
          - "phpinfo()"
        condition: or
```

### JWT Weak Configuration

```yaml
id: jwt-weak-config
info:
  name: "JWT Weak Configuration"
  author: "probe-agent"
  severity: high
  description: "Detects JWT with weak algorithm or no signature"
  tags: jwt,auth,cryptography

requests:
  - method: GET
    path:
      - "{{BaseURL}}/api/user"
    headers:
      Authorization: "Bearer eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IlRlc3QiLCJhZG1pbiI6dHJ1ZX0."
    matchers:
      - type: dsl
        dsl:
          - "status_code != 401"
          - "!contains(body, 'invalid')"
          - "!contains(body, 'unauthorized')"
        condition: and
```

## Project-Specific Templates

### IDOR in User API

```yaml
id: idor-user-endpoint
info:
  name: "IDOR in User API"
  author: "probe-agent"
  severity: high
  description: "Tests for Insecure Direct Object Reference in user endpoints"
  tags: idor,api,authorization

requests:
  - method: GET
    path:
      - "{{BaseURL}}/api/users/{{user_id}}"
    payloads:
      user_id:
        - "1"
        - "2"
        - "999999"
        - "{{target_user_id}}"
    headers:
      Authorization: "Bearer {{auth_token}}"
    matchers-condition: and
    matchers:
      - type: status
        status:
          - 200
      - type: word
        words:
          - "email"
          - "phone"
        condition: or
    extractors:
      - type: json
        json:
          - ".email"
          - ".id"
```

### Rate Limit Bypass Check

```yaml
id: rate-limit-bypass
info:
  name: "Rate Limit Bypass Check"
  author: "probe-agent"
  severity: medium
  description: "Tests rate limiting on sensitive endpoints"
  tags: rate-limit,dos,brute-force

requests:
  - method: POST
    path:
      - "{{BaseURL}}/api/auth/login"
    body: '{"email":"test@test.com","password":"wrong"}'
    headers:
      Content-Type: "application/json"
    race: true
    race_count: 100
    matchers:
      - type: dsl
        dsl:
          - "status_code != 429"
        condition: and
```

## CI/CD Integration

```yaml
# .github/workflows/nuclei-scan.yml
name: Nuclei Security Scan

on:
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  nuclei-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Nuclei
        run: |
          go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

      - name: Update Templates
        run: nuclei -update-templates

      - name: Run Nuclei Scan
        run: |
          nuclei -u ${{ secrets.TARGET_URL }} \
            -t nuclei-templates/ \
            -t .nuclei/ \
            -severity critical,high \
            -sarif-export nuclei-results.sarif \
            -json-export nuclei-results.json

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: nuclei-results.sarif

      - name: Check for Critical Findings
        run: |
          if jq -e '.[] | select(.info.severity == "critical")' nuclei-results.json > /dev/null; then
            echo "Critical vulnerabilities found!"
            exit 1
          fi
```
