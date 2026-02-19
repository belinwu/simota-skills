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
# ...
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
# ...
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
# ...
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
# ...
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
# ...
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
# ...
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
...
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
# ...
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
...
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
# ...
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
# ...
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
...
```
