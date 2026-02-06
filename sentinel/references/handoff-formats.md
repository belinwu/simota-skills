# Handoff Formats

Input and output handoff templates for Sentinel's inter-agent collaboration.

---

## Output Handoffs (Sending)

### SENTINEL_TO_RADAR_HANDOFF

Security fix needs test verification.

```yaml
SENTINEL_TO_RADAR_HANDOFF:
  Security_Fix:
    description: "[What was fixed]"
    severity: "[CRITICAL / HIGH / MEDIUM / LOW]"
    owasp: "[A0X - Category]"
    files_changed:
      - "[file path]"
  Tests_Needed:
    - "Existing tests still pass"
    - "Security fix doesn't break functionality"
    - "Edge cases covered"
    - "Negative tests (malicious input rejected)"
  Specific_Test_Cases:
    - input: "[Malicious input]"
      expected: "[Expected rejection/sanitization]"
    - input: "[Attack vector]"
      expected: "[Expected defense]"
  Coverage_Target:
    scope: "Security-critical code paths"
    minimum: "80% on modified files"
```

### SENTINEL_TO_PROBE_HANDOFF

Static finding needs dynamic verification.

```yaml
SENTINEL_TO_PROBE_HANDOFF:
  Vulnerability_Found:
    type: "[SQL injection / XSS / SSRF / etc.]"
    location: "[file:line]"
    evidence: "[Static analysis finding]"
  Request:
    - "Verify vulnerability is exploitable"
    - "Test with OWASP ZAP automated scan"
    - "Document attack vectors and payloads"
  After_Fix:
    - "Re-test to confirm fix is effective"
    - "Check for bypass techniques"
    - "Verify no regression in other endpoints"
```

### SENTINEL_TO_SCOUT_HANDOFF

Vulnerability needs deeper investigation.

```yaml
SENTINEL_TO_SCOUT_HANDOFF:
  Vulnerability:
    type: "[Vulnerability type]"
    symptom: "[What was observed]"
  Investigation_Needed:
    - "How did this vulnerability get introduced?"
    - "Are there similar patterns elsewhere?"
    - "What guard should have prevented this?"
    - "Timeline of when this became vulnerable"
  Reason: "Need RCA before fixing to prevent recurrence"
```

### SENTINEL_TO_JUDGE_HANDOFF

Security-critical code needs review.

```yaml
SENTINEL_TO_JUDGE_HANDOFF:
  PR_Context:
    description: "[What the PR does]"
  Security_Focus_Areas:
    - "Input validation completeness"
    - "Error message information leakage"
    - "Authentication bypass possibilities"
    - "Authorization check coverage"
  Specific_Concerns:
    - "[Concern 1]"
    - "[Concern 2]"
```

### SENTINEL_TO_CANVAS_HANDOFF

Security visualization needed.

```yaml
SENTINEL_TO_CANVAS_HANDOFF:
  Visualization_Request:
    type: "[threat_model / security_layers / attack_flow]"
  Data:
    actors: "[External actors]"
    boundaries: "[Trust boundaries]"
    flows: "[Data flows]"
    threats: "[Threat vectors]"
    mitigations: "[Mitigation points]"
  Output_Format: "mermaid"
```

---

## Input Handoffs (Receiving)

### GEAR_TO_SENTINEL_HANDOFF

Dependency audit findings needing deep review.

```yaml
GEAR_TO_SENTINEL_HANDOFF:
  Audit_Results:
    tool: "[npm audit / Snyk / etc.]"
    findings:
      - package: "[package name]"
        version: "[current version]"
        severity: "[Critical / High / Medium / Low]"
        cve: "[CVE-XXXX-XXXXX]"
        fix_version: "[patched version]"
  Request:
    - "Assess exploitability in this codebase"
    - "Prioritize fixes by actual risk"
    - "Recommend remediation strategy"
```

### PROBE_TO_SENTINEL_HANDOFF

Dynamic testing results needing code-level fix.

```yaml
PROBE_TO_SENTINEL_HANDOFF:
  Dynamic_Findings:
    tool: "[OWASP ZAP / Burp Suite / etc.]"
    vulnerabilities:
      - type: "[Vulnerability type]"
        endpoint: "[Affected endpoint]"
        severity: "[Severity]"
        evidence: "[Proof of exploit]"
  Request:
    - "Implement code-level fix"
    - "Add input validation"
    - "Verify fix blocks the attack vector"
```

### NEXUS_TO_SENTINEL_HANDOFF

Security scan request from orchestrator.

```yaml
NEXUS_TO_SENTINEL_HANDOFF:
  Task:
    description: "[Security scan or fix request]"
    scope: "[Files / endpoints / dependencies]"
    priority: "[CRITICAL / HIGH / MEDIUM / LOW]"
  Context:
    project: "[Project context]"
    recent_changes: "[What changed recently]"
  Request:
    - "Scan for vulnerabilities"
    - "Fix highest priority issue"
    - "Report findings"
```

---

## Output Format Template

Standard response format for every Sentinel output:

```markdown
## Sentinel Security Report

**Scan Scope**: [Files / endpoints scanned]
**Severity**: CRITICAL / HIGH / MEDIUM / LOW
**OWASP**: A0X - Category Name

### Finding

**File**: `src/path/file.ts:42`
**Risk**: [What could happen if exploited]
**Evidence**: [Code snippet or pattern found]

### Fix Applied

**Change**: [What was changed]
**Verification**: [How to verify the fix]

---
**Status**: Fixed / Needs Review / Blocked
**Next Action**: Run tests / Request Probe verification / Deploy
```
