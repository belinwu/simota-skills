# Compliance Report

Template and rules for generating specification compliance reports.

---

## Verdict Rules

### CERTIFIED

ALL of the following must be true:
- Every CRITICAL criterion: PASS
- Every HIGH criterion: PASS or NOT_TESTED (with runtime test plan)
- No CRITICAL adversarial probes open
- Traceability coverage >= 90%

### CONDITIONAL

ALL of the following must be true:
- No CRITICAL criterion: FAIL
- <=3 HIGH criteria: PARTIAL
- Remediation plan attached for all non-PASS items
- Timeline for remediation specified
- No unresolved CONTRADICTION probes

### REJECTED

ANY of the following triggers REJECTED:
- Any CRITICAL criterion: FAIL
- >3 HIGH criteria: FAIL
- Unresolved CONTRADICTION adversarial probes
- Traceability coverage < 50%
- Specification has >5 AMBIGUOUS_FLAGs without clarification

---

## Report Template

Note: Final output is rendered in Japanese per Output Language rules. The structure below defines the sections and their content.

```markdown
## Attest Compliance Report

### Summary

| Field | Value |
|-------|-------|
| Specification | [spec path/name] |
| Implementation | [files/modules list] |
| Mode | FULL / EXTRACT / AUDIT / ADVERSARIAL |
| **Verdict** | **CERTIFIED** / **CONDITIONAL** / **REJECTED** |
| Date | YYYY-MM-DD |

### Criteria Summary

| Verdict | CRITICAL | HIGH | MEDIUM | LOW | Total |
|---------|----------|------|--------|-----|-------|
| PASS | X | X | X | X | X |
| PARTIAL | X | X | X | X | X |
| FAIL | X | X | X | X | X |
| NOT_TESTED | X | X | X | X | X |
| AMBIGUOUS | X | X | X | X | X |
| **Total** | X | X | X | X | **X** |

### Traceability Matrix

| Criterion ID | Priority | Spec Section | Implementation | Tests | Verdict |
|-------------|----------|-------------|---------------|-------|---------|
| AC-XXX-001 | CRITICAL | spec.md:L24 | src/xxx.ts:42 | test/xxx.test.ts:15 | PASS |
| AC-XXX-002 | HIGH | spec.md:L31 | — | — | FAIL |
| ... | | | | | |

**Traceability Coverage:** XX% (criteria-to-implementation mapping completion rate)

### Findings (by severity)

#### CRITICAL

**[F-001] AC-XXX-002: {criterion description}**
- Verdict: FAIL
- Method: ABSENCE_CHECK
- Evidence: {description of missing implementation}
- Impact: {scope of this violation}
- Recommended action: Add implementation via Builder
- Assigned agent: Builder

#### HIGH

**[F-002] AC-XXX-005: {criterion description}**
- Verdict: PARTIAL
- Method: LOGIC_TRACE
- Evidence: `src/xxx.ts:89` — {partial implementation description}
- Gap: {description of missing parts}
- Recommended action: {specific fix description}
- Assigned agent: Builder

#### MEDIUM / LOW

[Same format as above]

### Adversarial Probe Results

| Probe ID | Category | Description | Risk | Spec Gap |
|----------|----------|-------------|------|----------|
| PRB-001 | Boundary | {description} | HIGH | {missing spec content} |
| PRB-002 | Omission | {description} | MEDIUM | {missing spec content} |
| PRB-003 | Implicit | {description} | LOW | {implicit assumption} |

### Specification Quality Feedback

| Issue | Type | Impact | Recommended Improvement |
|-------|------|--------|------------------------|
| {ambiguous criterion} | AMBIGUOUS | HIGH | {clarification proposal} |
| {missing requirement} | OMISSION | MEDIUM | {requirement to add} |

### Remediation Plan (for CONDITIONAL/REJECTED)

| # | Action | Assigned Agent | Priority | Estimate |
|---|--------|---------------|----------|----------|
| 1 | Add implementation for AC-XXX-002 | Builder | CRITICAL | — |
| 2 | Fix gap in AC-XXX-005 | Builder | HIGH | — |
| 3 | Convert BDD scenarios to tests | Radar | HIGH | — |
| 4 | Resolve specification ambiguities | Scribe | MEDIUM | — |

### BDD Scenarios (generated)

Total: X scenarios
- Happy Path: X
- Negative: X
- Boundary: X
- Edge Case: X

[Reference to scenario file]
```

---

## Traceability Matrix Format

The traceability matrix maps: **Specification -> Implementation -> Tests**

```
Spec Criterion --> Implementation File:Line --> Test File:Line
   AC-XXX-001  ->  src/handler.ts:42         ->  test/handler.test.ts:15
```

### Coverage Calculation

```
Traceability Coverage = (Criteria with Implementation Mapping) / (Total Criteria) x 100

Example:
  Total criteria: 12
  Mapped to implementation: 10
  Mapped to tests: 8
  Coverage: 10/12 = 83% (implementation), 8/12 = 67% (test)
```

### Coverage Thresholds

| Coverage | Assessment |
|----------|-----------|
| >= 90% | Excellent — supports CERTIFIED |
| 70-89% | Good — supports CONDITIONAL |
| 50-69% | Insufficient — requires remediation |
| < 50% | Unacceptable — triggers REJECTED |

---

## Handoff Formats

### To Builder (Violation Fixes)

```yaml
ATTEST_TO_BUILDER_HANDOFF:
  verdict: CONDITIONAL
  violations:
    - criterion_id: AC-XXX-002
      priority: CRITICAL
      gap: "Account lockout not implemented"
      spec_reference: "login-spec.md:L45"
      suggested_location: "src/controllers/auth.ts"
    - criterion_id: AC-XXX-005
      priority: HIGH
      gap: "Error message format doesn't match spec"
      current: "Generic error returned"
      expected: "Specific error with error code"
  bdd_scenarios: "generated/login.feature"
```

### To Radar (Test Generation)

```yaml
ATTEST_TO_RADAR_HANDOFF:
  bdd_scenarios:
    file: "generated/login.feature"
    total: 42
    by_priority:
      critical: 15
      high: 12
      medium: 10
      low: 5
  not_tested_criteria:
    - criterion_id: AC-XXX-003
      reason: "Requires runtime timing verification"
      suggested_test_type: "integration"
    - criterion_id: AC-XXX-008
      reason: "Requires browser rendering"
      suggested_test_type: "e2e"
```

### To Warden (Release Gate)

```yaml
ATTEST_TO_WARDEN_HANDOFF:
  verdict: CERTIFIED
  criteria_summary:
    total: 12
    pass: 10
    not_tested: 2
  traceability_coverage: 92%
  adversarial_probes:
    total: 18
    critical_open: 0
    high_open: 1
  spec_quality: GOOD
  recommendation: "Spec compliance verified. Proceed to V.A.I.R.E. evaluation."
```

### To Scribe (Spec Gap Report)

```yaml
ATTEST_TO_SCRIBE_HANDOFF:
  ambiguity_flags:
    - criterion_id: AC-XXX-005
      type: UNMEASURABLE
      suggestion: "Define response time threshold"
  omissions:
    - category: ERROR_HANDLING
      description: "No specification for rate limiting behavior"
    - category: EDGE_CASE
      description: "Behavior when session expires mid-action not specified"
  contradictions:
    - criteria: [AC-XXX-003, AC-XXX-009]
      description: "AC-003 says allow retry, AC-009 says lock immediately"
```
