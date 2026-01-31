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
        score: 60
      - range: [36, 50]
        score: 40
      - range: [51, 100]
        score: 20
      - range: [101, infinity]
        score: 0

    lines:
      - range: [0, 100]
        score: 100
      - range: [101, 200]
        score: 90
      - range: [201, 400]
        score: 75
      - range: [401, 700]
        score: 60
      - range: [701, 1000]
        score: 40
      - range: [1001, 2000]
        score: 20
      - range: [2001, infinity]
        score: 0

  adjustments:
    test_heavy:
      condition: test_lines > 50% of total_lines
      adjustment: +10 (cap at 100)
      reason: "Test files are easier to review"

    doc_heavy:
      condition: doc_lines > 30% of total_lines
      adjustment: +5 (cap at 100)
      reason: "Documentation is less risky"

    generated_files:
      condition: generated_files present
      adjustment: exclude from count
      reason: "Generated files don't need review"
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
      indicators:
        - Files in 2-3 related modules
        - Feature + its tests
        - Fix + related refactoring
      score: 80

    loosely_related:
      indicators:
        - Files in multiple modules
        - Multiple features
        - Feature + unrelated cleanup
      score: 50

    mixed:
      indicators:
        - Many unrelated changes
        - "While I was here" changes
        - Multiple bug fixes
      score: 25

    everything:
      indicators:
        - No clear relationship
        - Formatting + features + fixes
        - "Kitchen sink" PR
      score: 0

  type_analysis:
    single_type:
      examples: [feat_only, fix_only, refactor_only]
      multiplier: 1.0

    complementary_types:
      examples: [feat + test, fix + docs]
      multiplier: 0.95

    mixed_types:
      examples: [feat + fix, refactor + feat]
      multiplier: 0.8

    many_types:
      examples: [feat + fix + chore + docs]
      multiplier: 0.6
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
        - minimal_scope: 0-10
        - reversible: 0-5

    consistency:
      weight: 20
      criteria:
        - style_uniform: 0-10
        - scope_consistent: 0-10

  message_quality_rubric:
    format_compliance:
      15: "Perfect conventional commits format"
      10: "Conventional with minor issues"
      5: "Partially formatted"
      0: "No format followed"

    subject_clarity:
      15: "Clear, specific, actionable"
      10: "Understandable but could be clearer"
      5: "Vague but conveys intent"
      0: "Unclear or misleading"

    scope_accuracy:
      10: "Scope matches file changes"
      7: "Scope approximately matches"
      3: "Scope loosely related"
      0: "Scope incorrect or missing"

  atomicity_rubric:
    single_purpose:
      15: "One logical change"
      10: "Main change with necessary supporting"
      5: "2-3 related changes"
      0: "Many unrelated changes"

    minimal_scope:
      10: "Only necessary files changed"
      7: "Mostly necessary, some extra"
      3: "Many unnecessary files"
      0: "Extensive unnecessary changes"
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

    partial_coverage:
      condition: some_logic_tested
      score: 50

    minimal:
      condition: few_tests_exist
      score: 25

    none:
      condition: no_tests_for_changes
      score: 0

  quality_assessment:
    excellent:
      indicators:
        - Unit tests for logic
        - Integration tests for flows
        - Edge cases covered
        - Error paths tested
      score: 100

    good:
      indicators:
        - Unit tests present
        - Main paths covered
        - Some edge cases
      score: 75

    adequate:
      indicators:
        - Basic tests present
        - Happy path covered
      score: 50

    poor:
      indicators:
        - Minimal tests
        - Only trivial cases
      score: 25

  adjustments:
    test_only_pr:
      condition: pr_is_only_tests
      adjustment: score = 100
      reason: "Test PRs inherently have full coverage"

    config_change:
      condition: only_config_files
      adjustment: score = 80 if no_logic
      reason: "Config changes may not need tests"
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

    medium_need:
      conditions:
        - API modifications
        - Behavior changes
        - New options
      weight: 0.7

    low_need:
      conditions:
        - Bug fixes
        - Internal refactoring
        - Test additions
      weight: 0.3

    no_need:
      conditions:
        - Style changes
        - Dependency updates
        - Internal optimizations
      weight: 0

  presence_check:
    locations:
      - README.md updates
      - CHANGELOG entries
      - JSDoc/docstrings
      - API documentation
      - Inline comments

  quality_rubric:
    excellent:
      criteria:
        - Clear explanations
        - Examples provided
        - Edge cases noted
        - Migration guide if breaking
      score: 100

    good:
      criteria:
        - Adequate explanations
        - Basic examples
      score: 75

    minimal:
      criteria:
        - Brief notes
        - Changes mentioned
      score: 50

    poor:
      criteria:
        - Incomplete
        - Unclear
      score: 25
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
      new_feature: +15 risk
      bug_fix: +10 risk
      refactoring: +20 risk
      breaking_change: +30 risk
      dependency_update: +15 risk

    coverage_gap:
      no_tests: +25 risk
      partial_tests: +10 risk
      full_tests: +0 risk

  score_mapping:
    risk_0_20: score 100
    risk_21_40: score 80
    risk_41_60: score 60
    risk_61_80: score 40
    risk_81_100: score 20
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
    D:  [35, 49]
    F:  [0, 34]

  recommendations:
    by_grade:
      A+: "Excellent PR, ready for quick merge"
      A: "Strong PR, standard review sufficient"
      B+: "Good PR, normal review process"
      B: "Acceptable PR, careful review recommended"
      C: "Consider improvements or splitting"
      D: "Should restructure before review"
      F: "Must restructure, not reviewable as-is"
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

    fast_release:
      condition: release_frequency > weekly
      action: higher_atomicity_weight
      reason: "Frequent releases need atomic changes"

    legacy_codebase:
      condition: avg_file_age > 3_years
      action: lower_focus_penalty
      reason: "Legacy often requires broader changes"
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
      expected_score: 80-95
      size_tolerance: low
      test_requirement: high

    refactoring:
      expected_score: 70-85
      size_tolerance: high
      test_requirement: medium

    documentation:
      expected_score: 85-100
      size_tolerance: high
      test_requirement: none
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
      Output:
        quality_score:
          total: 78
          grade: "B+"
          components:
            size: 85
            focus: 70
            commits: 80
            tests: 75
            docs: 80
            risk: 70
          recommendations: [...]
```
