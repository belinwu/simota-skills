# Handoff Templates

## SENTINEL_TO_PROBE (Validation Request)

```markdown
## Sentinel → Probe Validation Request

**Potential Vulnerability**: [Type]
**File**: [file:line]
**Code Pattern**: `[vulnerable code snippet]`
**Risk Level**: [Based on pattern]

**Validation Request**:
- Confirm exploitability via API endpoint
- Test with various injection payloads
- Determine actual impact (data exposure, auth bypass, etc.)
```

## Probe Validation Response

```markdown
## Probe Validation Result

**Original Finding**: [Vulnerability type]
**Endpoint Tested**: [Method URL]
**Result**: CONFIRMED EXPLOITABLE | FALSE POSITIVE | PARTIALLY EXPLOITABLE

**Evidence**:
- Request: `[exploit request]`
- Response: [what happened]
- CVSS: [score] ([vector string])

**Recommended Action**: [next step]
**Suggested next**: Builder for remediation | Radar for regression tests
```

## PROBE_TO_BUILDER (Fix Request)

```markdown
## BUILDER_HANDOFF (from Probe)

### Confirmed Vulnerability
- **Type:** [OWASP category]
- **Severity:** [Critical/High/Medium/Low]
- **CVSS:** [Score]
- **Location:** [URL/endpoint]

### Proof of Concept
```
[Exploit steps or curl command]
```

### Remediation
- **Recommended fix:** [Description]
- **Code location:** [file:line]
- **Deadline:** [Based on severity SLA]

Suggested command: `/Builder fix vulnerability in [file]`
```

## PROBE_TO_RADAR (Regression Tests)

```markdown
## RADAR_HANDOFF (from Probe)

### Security Regression Tests Needed
- **Vulnerability:** [Type]
- **Endpoint:** [URL]
- **Test cases:**
  - [ ] Verify fix blocks original exploit
  - [ ] Verify similar patterns are also protected
  - [ ] Verify no bypass via encoding/case variation

Suggested command: `/Radar add security regression tests`
```
