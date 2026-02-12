# SARIF Integration Reference

SARIF (Static Analysis Results Interchange Format) enables standardized security findings integration with GitHub Security tab and other tools.

## SARIF Output Template

```json
{
  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
  "version": "2.1.0",
  "runs": [
    {
      "tool": {
        "driver": {
          "name": "Probe Security Scanner",
          "version": "1.0.0",
          "rules": [
            {
              "id": "PROBE-SQL-001",
              "name": "SQL Injection",
              "shortDescription": {
                "text": "SQL Injection vulnerability detected"
              },
              "fullDescription": {
                "text": "User input is directly concatenated into SQL query without proper sanitization"
              },
              "help": {
                "text": "Use parameterized queries or prepared statements"
              },
              "properties": {
                "security-severity": "9.8",
                "tags": ["security", "sql-injection", "owasp-a03"]
              }
            }
          ]
        }
      },
      "results": [
        {
          "ruleId": "PROBE-SQL-001",
          "level": "error",
          "message": {
            "text": "SQL Injection confirmed at /api/users endpoint"
          },
          "locations": [
            {
              "physicalLocation": {
                "artifactLocation": {
                  "uri": "src/api/users.js"
                },
                "region": {
                  "startLine": 42
                }
              }
            }
          ],
          "fingerprints": {
            "primaryLocationLineHash": "abc123"
          }
        }
      ]
    }
  ]
}
```

## ZAP to SARIF Conversion

```python
# zap_to_sarif.py
import json
import sys

def convert_zap_to_sarif(zap_json_path, output_path):
    with open(zap_json_path) as f:
        zap_data = json.load(f)

    severity_map = {
        "High": "error",
        "Medium": "warning",
        "Low": "note",
        "Informational": "note"
    }

    sarif = {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {
                "driver": {
                    "name": "OWASP ZAP",
                    "version": "2.14.0",
                    "rules": []
                }
            },
            "results": []
        }]
    }

    rules_added = set()

    for site in zap_data.get("site", []):
        for alert in site.get("alerts", []):
            rule_id = f"ZAP-{alert['pluginid']}"

            # Add rule definition if not already added
            if rule_id not in rules_added:
                sarif["runs"][0]["tool"]["driver"]["rules"].append({
                    "id": rule_id,
                    "name": alert["name"],
                    "shortDescription": {"text": alert["name"]},
                    "fullDescription": {"text": alert.get("desc", "")},
                    "help": {"text": alert.get("solution", "")}
                })
                rules_added.add(rule_id)

            # Add result for each instance
            for instance in alert.get("instances", []):
                sarif["runs"][0]["results"].append({
                    "ruleId": rule_id,
                    "level": severity_map.get(alert["riskdesc"].split()[0], "note"),
                    "message": {"text": f"{alert['name']} at {instance.get('uri', 'unknown')}"},
                    "locations": [{
                        "physicalLocation": {
                            "artifactLocation": {"uri": instance.get("uri", "")},
                            "region": {"startLine": 1}
                        }
                    }]
                })

    with open(output_path, 'w') as f:
        json.dump(sarif, f, indent=2)

if __name__ == "__main__":
    convert_zap_to_sarif(sys.argv[1], sys.argv[2])
```

## GitHub Actions - Security SARIF Upload

```yaml
# .github/workflows/security-sarif.yml
name: Security Scan with SARIF

on:
  push:
    branches: [main]
  pull_request:

jobs:
  security-scan:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v4

      - name: Run Security Scan
        run: |
          # Run your security tools
          # Export results to SARIF format

      - name: Upload SARIF to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: security-results.sarif
          category: "probe-security-scan"
```

## GitHub Actions - DAST Security Gate

```yaml
name: Security Scan

on:
  pull_request:
    branches: [main]

jobs:
  dast-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Start application
        run: |
          docker-compose up -d
          sleep 30  # Wait for app to start

      - name: OWASP ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.10.0
        with:
          target: 'http://localhost:3000'
          rules_file_name: '.zap/rules.tsv'

      - name: Check for high severity
        run: |
          if grep -q "High" zap-report.html; then
            echo "High severity vulnerabilities found!"
            exit 1
          fi

      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: zap-report
          path: zap-report.html
```

## Security Gate Rules

```tsv
# .zap/rules.tsv
# Rule ID	Action	Description
10010	IGNORE	Cookie No HttpOnly Flag (known false positive)
10020	WARN	X-Frame-Options Header Not Set
10021	FAIL	X-Content-Type-Options Header Missing
40012	FAIL	Cross Site Scripting (Reflected)
40014	FAIL	Cross Site Scripting (Persistent)
40018	FAIL	SQL Injection
90019	FAIL	Server Side Include
90020	FAIL	Remote OS Command Injection
```
