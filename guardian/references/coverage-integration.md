# Test Coverage Integration Reference

Guardian's integration with CI coverage reports and Test Score calculation.

## Overview

Coverage Integration enables Guardian to:
- Parse CI coverage reports automatically
- Correlate coverage with changed files
- Extend the Test Score component in Quality Scoring
- Identify coverage gaps requiring attention

**Expected Impact**: Coverage oversight reduction by **90%**

---

## CI Coverage Report Parsing

### Supported Formats

```yaml
coverage_formats:
  lcov:
    file: "coverage/lcov.info"
    parser: lcov_parser
    metrics: [lines, branches, functions]

  cobertura:
    file: "coverage/cobertura.xml"
    parser: xml_parser
    metrics: [lines, branches, complexity]

  istanbul:
    file: "coverage/coverage-summary.json"
    parser: json_parser
    metrics: [lines, statements, branches, functions]

  jacoco:
    file: "target/site/jacoco/jacoco.xml"
    parser: xml_parser
    metrics: [instructions, branches, lines, complexity]

  go_cover:
    file: "coverage.out"
    parser: go_parser
    metrics: [statements]

  pytest_cov:
    file: "coverage.xml"
    parser: xml_parser
    metrics: [lines, branches]
```

### Coverage Data Extraction

```yaml
coverage_extraction:
  per_file:
    - file_path: string
    - line_coverage: percentage
    - branch_coverage: percentage
    - function_coverage: percentage
    - uncovered_lines: [line_numbers]
    - uncovered_branches: [branch_ids]

  aggregate:
    - total_lines: number
    - covered_lines: number
    - total_branches: number
    - covered_branches: number
    - overall_percentage: number

  delta:
    - coverage_before: percentage
    - coverage_after: percentage
    - coverage_delta: +/- percentage
    - regression: boolean
```

---

## Change-Coverage Correlation

### Mapping Changed Files to Coverage

```yaml
change_coverage_mapping:
  process:
    1: "Get list of changed files from PR"
    2: "Extract coverage data for each file"
    3: "Calculate coverage for changed lines specifically"
    4: "Identify uncovered new/modified code"

  changed_line_coverage:
    calculation: |
      changed_lines = get_changed_lines(file)
      covered_changed = intersection(changed_lines, covered_lines)
      change_coverage = len(covered_changed) / len(changed_lines)

  critical_gap_detection:
    condition: "changed_line_coverage < 0.5"
    action: "Flag for Radar handoff"
```

### Coverage Impact Analysis

```yaml
coverage_impact:
  scenarios:
    new_code_no_tests:
      detection: "Added lines with 0% coverage"
      severity: HIGH
      action: "Require tests before merge"

    reduced_coverage:
      detection: "Overall coverage decreased"
      severity: MEDIUM
      action: "Warn, recommend additional tests"

    hotspot_uncovered:
      detection: "Hotspot file with coverage < 50%"
      severity: HIGH
      action: "Prioritize test addition"

    critical_path_uncovered:
      detection: "Auth/payment code with coverage < 80%"
      severity: CRITICAL
      action: "Block until coverage improved"
```

---

## Extended Test Score Component

### Original Test Score (Basic)

```yaml
original_test_score:
  100: all_changes_tested
  80: core_logic_tested
  50: partial_coverage
  25: minimal_tests
  0: no_tests
```

### Enhanced Test Score (Extended)

```yaml
enhanced_test_score:
  components:
    line_coverage:
      weight: 30%
      scoring:
        100: ">= 90%"
        80: "70-89%"
        60: "50-69%"
        40: "30-49%"
        20: "10-29%"
        0: "< 10%"

    branch_coverage:
      weight: 25%
      scoring:
        100: ">= 85%"
        80: "65-84%"
        60: "45-64%"
        40: "25-44%"
        20: "10-24%"
        0: "< 10%"

    changed_line_coverage:
      weight: 25%
      scoring:
        100: ">= 90%"
        80: "70-89%"
        50: "50-69%"
        25: "25-49%"
        0: "< 25%"
      note: "Coverage specifically for lines changed in this PR"

    test_quality:
      weight: 10%
      factors:
        - test_count_delta: "+2 tests per new function"
        - test_types: "Unit + Integration presence"
        - assertion_density: ">= 3 assertions per test"

    coverage_delta:
      weight: 10%
      scoring:
        100: "Increased by >= 5%"
        75: "Maintained or slight increase"
        50: "Decreased by < 2%"
        25: "Decreased by 2-5%"
        0: "Decreased by > 5%"

  calculation: |
    test_score = (
      line_coverage_score * 0.30 +
      branch_coverage_score * 0.25 +
      changed_line_score * 0.25 +
      test_quality_score * 0.10 +
      coverage_delta_score * 0.10
    )
```

---

## Coverage Gap Detection

### Gap Categories

```yaml
coverage_gaps:
  critical:
    description: "Must fix before merge"
    conditions:
      - "Auth/security code with < 80% coverage"
      - "New payment logic with < 90% coverage"
      - "Changed code with 0% coverage"
    action: BLOCK

  high:
    description: "Strongly recommend fixing"
    conditions:
      - "Core business logic with < 70% coverage"
      - "Hotspot file with < 60% coverage"
      - "Coverage regression > 5%"
    action: WARN_STRONG

  medium:
    description: "Recommend addressing"
    conditions:
      - "Changed files with < 50% coverage"
      - "New functions without tests"
      - "Branches not covered"
    action: WARN

  low:
    description: "Nice to have"
    conditions:
      - "Utility code with < 70% coverage"
      - "Minor coverage decrease"
    action: SUGGEST
```

### Gap Report Template

```markdown
## Coverage Gap Analysis

**PR**: #123 - feat(auth): add OAuth2 support
**Overall Change Coverage**: 65%

### Critical Gaps (Must Fix)
| File | Changed Lines | Covered | Gap | Issue |
|------|---------------|---------|-----|-------|
| src/auth/oauth.ts | 120 | 48 | 60% | Auth code < 80% |
| src/auth/token.ts | 45 | 0 | 100% | No tests |

### High Priority Gaps
| File | Coverage | Reason |
|------|----------|--------|
| src/api/callback.ts | 55% | Core logic uncovered |

### Uncovered Lines Detail
**src/auth/oauth.ts** (Lines 45-78):
- Token validation logic
- Error handling paths
- Edge case: expired token

### Recommendations
1. Add unit tests for OAuth token validation
2. Cover error handling in callback endpoint
3. Add integration test for full OAuth flow

### Coverage Impact
- Before: 72%
- After: 68%
- Delta: **-4%** (Regression)
```

---

## Radar Integration

### Auto-Handoff Conditions

```yaml
radar_handoff:
  triggers:
    - condition: "critical_gap_exists"
      priority: IMMEDIATE
      blocking: true

    - condition: "coverage_regression > 5%"
      priority: HIGH
      blocking: false

    - condition: "hotspot_coverage < 50%"
      priority: HIGH
      blocking: false

    - condition: "changed_line_coverage < 50% AND risk_score > 60"
      priority: MEDIUM
      blocking: false
```

### Handoff Format

```markdown
## GUARDIAN_TO_RADAR_HANDOFF (Coverage)

**PR**: #123 - feat(auth): add OAuth2 support
**Trigger**: Coverage gap in high-risk files

**Coverage Summary**:
| Metric | Value | Target | Gap |
|--------|-------|--------|-----|
| Overall | 68% | 80% | -12% |
| Changed Lines | 65% | 80% | -15% |
| Branch | 55% | 70% | -15% |

**Files Needing Tests**:
| File | Current | Target | Priority |
|------|---------|--------|----------|
| src/auth/oauth.ts | 40% | 80% | CRITICAL |
| src/auth/token.ts | 0% | 80% | CRITICAL |
| src/api/callback.ts | 55% | 70% | HIGH |

**Specific Coverage Needs**:
1. Token validation: Lines 45-60
2. Error handling: Lines 72-85
3. Refresh flow: Lines 90-120

**Test Type Recommendations**:
- Unit: Token validation, error cases
- Integration: Full OAuth flow
- Edge: Expired token, invalid state

**Request**: Add tests to achieve 80% coverage on critical files
```

---

## Quality Score Impact

### Test Score Contribution

```yaml
quality_score_integration:
  test_score_weight: 15%  # In overall quality score

  test_score_breakdown:
    line_coverage: 4.5%    # (30% of 15%)
    branch_coverage: 3.75% # (25% of 15%)
    changed_coverage: 3.75% # (25% of 15%)
    test_quality: 1.5%     # (10% of 15%)
    coverage_delta: 1.5%   # (10% of 15%)

  impact_examples:
    excellent_coverage:
      line: 95%
      branch: 90%
      changed: 100%
      quality: HIGH
      delta: +3%
      test_score: 95
      quality_contribution: 14.25  # (95 * 0.15)

    poor_coverage:
      line: 40%
      branch: 30%
      changed: 25%
      quality: LOW
      delta: -5%
      test_score: 25
      quality_contribution: 3.75   # (25 * 0.15)
```

---

## AUTORUN Integration

### Auto-Execute Actions

```yaml
autorun_coverage:
  auto_execute:
    - Parse CI coverage report
    - Calculate change coverage
    - Generate coverage gap report
    - Calculate enhanced test score
    - Determine Radar handoff need

  auto_handoff:
    condition: "critical_gap OR (coverage_regression > 5% AND risk_high)"
    target: Radar
    blocking: varies_by_severity

  output:
    coverage:
      overall: 68%
      changed_lines: 65%
      branch: 55%
      delta: -4%
      test_score: 52
    gaps:
      critical: 2
      high: 1
      medium: 3
    handoff_needed: true
    handoff_priority: HIGH
```

### Status Determination

```yaml
coverage_status:
  SUCCESS:
    - No critical gaps
    - Coverage >= target
    - No significant regression

  PARTIAL:
    - High priority gaps exist
    - Coverage below target
    - Radar handoff requested

  BLOCKED:
    - Critical gaps in security code
    - Severe coverage regression
    - Required coverage not met
```

---

## Coverage Report Template

```markdown
## Coverage Integration Report

### PR Coverage Summary
```
Overall:        ██████░░░░ 68% (Target: 80%)
Changed Lines:  ██████░░░░ 65%
Branch:         █████░░░░░ 55%
Delta:          ▼ -4% (Regression)
```

### Test Score Breakdown
| Component | Score | Weight | Contribution |
|-----------|-------|--------|--------------|
| Line Coverage | 60 | 30% | 18 |
| Branch Coverage | 50 | 25% | 12.5 |
| Changed Coverage | 55 | 25% | 13.75 |
| Test Quality | 70 | 10% | 7 |
| Coverage Delta | 25 | 10% | 2.5 |
| **Total** | | | **53.75** |

### Gaps by Severity
- CRITICAL: 2 files
- HIGH: 1 file
- MEDIUM: 3 files

### Action Required
- [ ] Add tests for src/auth/oauth.ts (CRITICAL)
- [ ] Add tests for src/auth/token.ts (CRITICAL)
- [ ] Improve src/api/callback.ts coverage (HIGH)

### Radar Handoff: **RECOMMENDED**
```
