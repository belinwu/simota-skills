# PR Quality Scoring Reference

Detailed methodology for Guardian's quantitative PR quality assessment.

## Scoring Philosophy

Guardian's quality scoring provides objective, reproducible assessments that:
- Remove subjectivity from PR evaluation
- Enable cross-team benchmarking
- Track quality trends over time
- Identify improvement opportunities

---

## Score Components

### 1. Size Score (25% weight)

Measures PR size against reviewability thresholds.

```yaml
size_scoring:
  calculation: |
    file_score = map_to_range(file_count, thresholds.files)
    line_score = map_to_range(line_count, thresholds.lines)
    size_score = min(file_score, line_score)

  thresholds:
    files:
      - range: [0, 5]
        score: 100
      - range: [6, 10]
        score: 90
      - range: [11, 20]
        score: 75
      - range: [21, 35]
# ...
```

### 2. Focus Score (20% weight)

Measures how focused the PR is on a single concern.

```yaml
focus_scoring:
  calculation: |
    concern_count = count_distinct_concerns(changes)
    type_count = count_distinct_types(changes)
    focus_score = calculate_focus(concern_count, type_count)

  concern_detection:
    single_concern:
      indicators:
        - All files in same module/directory
        - Single feature or bug fix
        - Related by functionality
      score: 100

    related_concerns:
# ...
```

### 3. Commit Score (15% weight)

Evaluates commit message quality and structure.

```yaml
commit_scoring:
  components:
    message_quality:
      weight: 50
      criteria:
        - format_compliance: 0-15
        - subject_clarity: 0-15
        - scope_accuracy: 0-10
        - body_quality: 0-5
        - reference_links: 0-5

    atomicity:
      weight: 30
      criteria:
        - single_purpose: 0-15
# ...
```

### 4. Test Score (15% weight)

Measures test coverage for changes.

```yaml
test_scoring:
  calculation: |
    coverage_score = calculate_coverage(changed_files, test_files)
    quality_score = assess_test_quality(test_files)
    test_score = (coverage_score * 0.7) + (quality_score * 0.3)

  coverage_assessment:
    full_coverage:
      condition: all_logic_files_have_tests
      score: 100

    core_coverage:
      condition: core_logic_tested AND edge_cases_partial
      score: 80

# ...
```

### 5. Documentation Score (10% weight)

Evaluates documentation updates.

```yaml
documentation_scoring:
  calculation: |
    need_score = assess_documentation_need(changes)
    presence_score = check_documentation_presence(changes)
    quality_score = evaluate_documentation_quality(docs)
    doc_score = (presence_score / need_score) * quality_score

  need_assessment:
    high_need:
      conditions:
        - New public API
        - Breaking changes
        - New features
        - Configuration changes
      weight: 1.0
# ...
```

### 6. Risk Score (15% weight)

Inverse of change risk - lower risk = higher score.

```yaml
risk_scoring:
  calculation: |
    raw_risk = calculate_risk_score(changes)  # From risk-assessment.md
    risk_component_score = 100 - raw_risk

  risk_factors:
    file_sensitivity:
      auth_files: +30 risk
      payment_files: +30 risk
      security_files: +25 risk
      core_logic: +20 risk
      utility_files: +5 risk
      test_files: +0 risk

    change_type:
# ...
```

---

## Aggregate Score Calculation

```yaml
aggregate_calculation:
  formula: |
    total = (size_score * 0.25) +
            (focus_score * 0.20) +
            (commit_score * 0.15) +
            (test_score * 0.15) +
            (doc_score * 0.10) +
            (risk_score * 0.15)

  grade_mapping:
    A+: [95, 100]
    A:  [85, 94]
    B+: [75, 84]
    B:  [65, 74]
    C:  [50, 64]
# ...
```

---

## Score Report Template

```markdown
## PR Quality Score: {total}/100 ({grade})

### Component Breakdown
| Component | Score | Weight | Contribution |
|-----------|-------|--------|--------------|
| Size | {size}/100 | 25% | {size*0.25} |
| Focus | {focus}/100 | 20% | {focus*0.20} |
| Commits | {commit}/100 | 15% | {commit*0.15} |
| Tests | {test}/100 | 15% | {test*0.15} |
| Documentation | {doc}/100 | 10% | {doc*0.10} |
| Risk (inverse) | {risk}/100 | 15% | {risk*0.15} |

### Visual Breakdown
```
Size:    {bar} {size}/100
Focus:   {bar} {focus}/100
Commits: {bar} {commit}/100
Tests:   {bar} {test}/100
Docs:    {bar} {doc}/100
Risk:    {bar} {risk}/100
```

### Grade: {grade}
{grade_description}

### Improvement Opportunities
{improvements_list}

### Comparison
- vs Team Average: {delta_team}
- vs Repository P50: {delta_p50}
- Trend (last 5 PRs): {trend}
```

---

## Calibration

### Project-Specific Calibration

Guardian learns project-specific thresholds:

```yaml
calibration:
  method: analyze_recent_prs
  sample_size: 50
  metrics:
    - median_files_per_pr
    - median_lines_per_pr
    - common_score_distribution
    - team_size_factor

  adjustments:
    larger_team:
      condition: team_size > 10
      action: stricter_size_thresholds
      reason: "Larger teams need smaller PRs"

# ...
```

### Benchmarking

```yaml
benchmarks:
  industry:
    excellent_pr:
      size: "<10 files, <200 lines"
      focus: "Single concern"
      commits: "Atomic, well-described"
      tests: "Full coverage"

  by_pr_type:
    feature:
      expected_score: 75-90
      size_tolerance: medium
      test_requirement: high

    bugfix:
# ...
```

---

## Integration with AUTORUN

```yaml
autorun_quality_scoring:
  auto_execute:
    - Calculate all component scores
    - Generate grade and recommendations
    - Include in GUARDIAN_TO_JUDGE_HANDOFF

  pause_conditions:
    - score < 35 (F grade)
    - risk_component > 85
    - no_tests AND logic_changes

  output_format:
    _STEP_COMPLETE:
      Agent: Guardian
      Status: SUCCESS
# ...
```
