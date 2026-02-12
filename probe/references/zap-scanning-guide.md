# OWASP ZAP Scanning Guide

## Scan Types

| Scan | Purpose | Duration | Impact |
|------|---------|----------|--------|
| Spider | Discover pages/endpoints | Minutes | None |
| Passive Scan | Analyze responses | Real-time | None |
| Active Scan | Test for vulnerabilities | Hours | May modify data |
| Ajax Spider | JavaScript-heavy apps | Minutes | None |

## ZAP CLI Commands

```bash
# Start ZAP in daemon mode
zap.sh -daemon -port 8080

# Spider a target
zap-cli spider https://target.example.com

# Run active scan
zap-cli active-scan https://target.example.com

# Generate report
zap-cli report -o report.html -f html
```

## ZAP API (Python)

```python
from zapv2 import ZAPv2

zap = ZAPv2(apikey='your-api-key', proxies={'http': 'http://127.0.0.1:8080'})

# Spider
zap.spider.scan('https://target.example.com')

# Active scan
zap.ascan.scan('https://target.example.com')

# Get alerts
alerts = zap.core.alerts()
```

---

## Baseline Scan Configuration

```yaml
# zap-baseline.yaml
env:
  contexts:
    - name: "Application Context"
      urls:
        - "${TARGET_URL}"
      includePaths:
        - "${TARGET_URL}.*"
      excludePaths:
        - ".*logout.*"
        - ".*\.js$"
        - ".*\.css$"
      authentication:
        method: "form"
        parameters:
          loginUrl: "${LOGIN_URL}"
          loginRequestData: "username={%username%}&password={%password%}"

jobs:
  - type: spider
    parameters:
      maxDuration: 5
      maxDepth: 5
  - type: passiveScan-wait
    parameters:
      maxDuration: 10
  - type: activeScan
    parameters:
      maxRuleDurationInMins: 5
      maxScanDurationInMins: 30
```

## API Scan Configuration

```yaml
# zap-api-scan.yaml
env:
  contexts:
    - name: "API Context"
      urls:
        - "${API_BASE_URL}"
      technology:
        include:
          - "API"
          - "Language.JavaScript"

jobs:
  - type: openapi
    parameters:
      apiUrl: "${OPENAPI_SPEC_URL}"
  - type: activeScan
    policyDefinition:
      rules:
        - id: 40012  # Cross Site Scripting (Reflected)
          strength: "HIGH"
        - id: 40014  # Cross Site Scripting (Persistent)
          strength: "HIGH"
        - id: 40018  # SQL Injection
          strength: "HIGH"
        - id: 40019  # SQL Injection - MySQL
          strength: "MEDIUM"
        - id: 90019  # Server Side Include
          strength: "MEDIUM"
        - id: 90020  # Remote OS Command Injection
          strength: "HIGH"
```

## Authentication Test Scenarios

```yaml
# auth-test-scenarios.yaml
scenarios:
  - name: "Session Fixation"
    steps:
      - action: "Get session before login"
      - action: "Login with valid credentials"
      - verify: "Session ID changed after login"

  - name: "Session Timeout"
    steps:
      - action: "Login and get session"
      - action: "Wait for timeout period"
      - verify: "Session is invalidated"

  - name: "Logout Effectiveness"
    steps:
      - action: "Login and perform actions"
      - action: "Logout"
      - verify: "Previous session cannot be reused"

  - name: "Concurrent Session"
    steps:
      - action: "Login from location A"
      - action: "Login same user from location B"
      - verify: "Policy enforced (allow/deny/invalidate)"
```
