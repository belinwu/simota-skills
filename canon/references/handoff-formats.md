# Canon Handoff Formats & Collaboration Architecture

## Collaboration Architecture

```
                    ┌─────────────┐
                    │   Canon     │
                    │ (Standards) │
                    └──────┬──────┘
                           │
      ┌────────────────────┼────────────────────┐
      │                    │                    │
      ▼                    ▼                    ▼
┌──────────┐        ┌──────────┐        ┌──────────┐
│ Sentinel │        │ Palette  │        │ Builder  │
│(Security)│        │ (A11y)   │        │ (Code)   │
└──────────┘        └──────────┘        └──────────┘
      │                    │                    │
      └────────────────────┴────────────────────┘
                           │
                           ▼
                    ┌──────────┐
                    │  Radar   │
                    │ (Tests)  │
                    └──────────┘
```

## Canon → Builder Handoff (Implementation Fix)

```markdown
## Canon → Builder Handoff

### Compliance Finding
- **Finding ID:** CANON-XXX
- **Standard:** [Standard Name and Version]
- **Citation:** [Specific section/requirement]
- **Severity:** [Critical/High/Medium/Low]

### Current State
- **Location:** [File:line]
- **Issue:** [Description of non-compliance]
- **Evidence:** [Code snippet or configuration]

### Required Change
- **Requirement:** [What the standard requires]
- **Recommendation:** [How to achieve compliance]
- **Example:** [Compliant code example if applicable]

### Acceptance Criteria
- [ ] [Specific testable criterion 1]
- [ ] [Specific testable criterion 2]
- [ ] Standard requirement met: [citation]

### Verification
After implementation, verify with:
- [ ] Automated test: [test name/command]
- [ ] Manual check: [verification steps]
```

## Canon → Sentinel Handoff (Security Standard)

```markdown
## Canon → Sentinel Handoff

### Security Standard Violation
- **Standard:** OWASP ASVS [section]
- **Requirement:** [Requirement text]
- **Severity:** [Critical/High]

### Finding Details
- **CWE:** [CWE-XXX if applicable]
- **Location:** [File:line]
- **Vulnerability:** [Description]

### Remediation Guidance
- **Required Fix:** [What needs to change]
- **Reference Implementation:** [Link or example]
- **Testing:** [How to verify fix]

### Security Considerations
- [Additional security context]
- [Related vulnerabilities to check]
```

## Canon → Palette Handoff (Accessibility Standard)

```markdown
## Canon → Palette Handoff

### Accessibility Violation
- **Standard:** WCAG [version] [level]
- **Success Criterion:** [SC number and name]
- **Severity:** [Based on impact]

### Finding Details
- **Component:** [Component name/location]
- **Issue:** [Description of violation]
- **Impact:** [Who is affected and how]

### Remediation Guidance
- **Requirement:** [What WCAG requires]
- **Technique:** [WCAG technique reference]
- **Example:** [Accessible implementation]

### Testing
- [ ] Screen reader test: [steps]
- [ ] Keyboard navigation: [steps]
- [ ] Automated scan: [tool/command]
```

## Canon → Scribe Handoff (Documentation)

```markdown
## Canon → Scribe Handoff

### Compliance Documentation Request
- **Purpose:** [Audit preparation / Compliance proof / Policy document]
- **Standards:** [Standards to document compliance for]

### Required Documentation
- [ ] Compliance summary report
- [ ] Evidence collection
- [ ] Remediation tracking
- [ ] Sign-off records

### Format Requirements
- **Output Format:** [Markdown / Word / PDF]
- **Audience:** [Internal / External auditor / Customer]
- **Detail Level:** [Executive summary / Detailed evidence]
```

## NEXUS_HANDOFF Template

When user input contains `## NEXUS_ROUTING`, treat Nexus as the hub.
Do not instruct calling other agents. Always return results to Nexus.

```text
## NEXUS_HANDOFF
- Step: [X/Y]
- Agent: Canon
- Summary: 1-3 lines
- Key findings / decisions:
  - Standards assessed: [list]
  - Compliance level: [percentage or level]
  - Critical findings: [count]
- Artifacts (files/commands/links):
  - Compliance report
  - Findings list
- Risks / trade-offs:
  - [Compliance gaps]
  - [Resource requirements for remediation]
- Pending Confirmations:
  - Trigger: [INTERACTION_TRIGGER name if any]
  - Question: [Question for user]
  - Options: [Available options]
  - Recommended: [Recommended option]
- User Confirmations:
  - Q: [Previous question] → A: [User's answer]
- Open questions (blocking/non-blocking):
  - [Unconfirmed items]
- Suggested next agent: [Builder/Sentinel/Palette] (for remediation)
- Next action: CONTINUE (Nexus automatically proceeds)
```
