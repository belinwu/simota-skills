# Change Risk Assessment Reference

Detailed methodology for Guardian's change risk quantification.

## Risk Philosophy

Risk assessment helps:
- Prioritize review attention
- Allocate appropriate testing resources
- Plan deployment strategies
- Prepare mitigation measures

---

## Risk Factor Framework

### 1. File Sensitivity (25% weight)

```yaml
file_sensitivity:
  critical_files:
    score: 90-100
    patterns:
      - "**/auth/**"
      - "**/security/**"
      - "**/crypto/**"
      - "**/payment/**"
      - "**/billing/**"
      - "**/*.key"
      - "**/*.pem"
      - ".env*"
      - "**/secrets/**"
      - "**/permissions/**"
      - "**/rbac/**"

  high_sensitivity:
    score: 70-89
    patterns:
      - "**/api/**"
      - "**/middleware/**"
      - "**/session/**"
      - "**/user/**"
      - "**/database/**"
      - "**/migration/**"

  medium_sensitivity:
    score: 40-69
    patterns:
      - "**/core/**"
      - "**/service/**"
      - "**/controller/**"
      - "**/model/**"
      - "**/config/**"

  low_sensitivity:
    score: 10-39
    patterns:
      - "**/utils/**"
      - "**/helpers/**"
      - "**/components/**"
      - "**/ui/**"

  minimal_sensitivity:
    score: 0-9
    patterns:
      - "**/test/**"
      - "**/*.test.*"
      - "**/*.spec.*"
      - "**/docs/**"
      - "**/*.md"
      - "**/stories/**"

  calculation: |
    sensitivity_score = max(sensitivity(file) for file in changed_files)
    # Most sensitive file determines score
```

### 2. Change Complexity (20% weight)

```yaml
change_complexity:
  metrics:
    cyclomatic_complexity_delta:
      description: "Change in code paths"
      calculation: "new_complexity - old_complexity"
      thresholds:
        low: delta <= 0
        medium: delta 1-5
        high: delta 6-15
        critical: delta > 15

    lines_of_logic:
      description: "Non-trivial line changes"
      excludes:
        - Blank lines
        - Comments only
        - Import statements
        - Type definitions
      thresholds:
        low: < 50
        medium: 50-150
        high: 150-300
        critical: > 300

    function_changes:
      description: "Functions added/modified"
      thresholds:
        low: < 3
        medium: 3-8
        high: 9-15
        critical: > 15

    branching_changes:
      description: "if/switch/try blocks added"
      thresholds:
        low: < 3
        medium: 3-7
        high: 8-15
        critical: > 15

  score_calculation: |
    complexity_indicators = [
      cyclomatic_delta_score,
      logic_lines_score,
      function_change_score,
      branching_score
    ]
    complexity_score = weighted_average(complexity_indicators)
```

### 3. Hotspot Overlap (15% weight)

```yaml
hotspot_overlap:
  hotspot_definition:
    change_frequency: "> 10 commits in 90 days"
    bug_density: "> 3 bug fixes in 90 days"
    churn_rate: "> 50% of lines changed in 90 days"

  overlap_calculation: |
    hotspot_files = identify_hotspots(repository)
    changed_hotspots = intersection(changed_files, hotspot_files)
    overlap_ratio = len(changed_hotspots) / len(changed_files)
    hotspot_score = overlap_ratio * 100

  risk_amplification:
    problem_child_hotspot:
      multiplier: 1.5
      reason: "High change + high bugs = volatile code"

    growing_monster_hotspot:
      multiplier: 1.3
      reason: "Increasing complexity is unstable"

    knowledge_silo_hotspot:
      multiplier: 1.2
      reason: "Limited reviewers available"
```

### 4. Dependency Impact (15% weight)

```yaml
dependency_impact:
  import_analysis:
    direct_dependents:
      description: "Files that import changed files"
      calculation: "count(files importing changed_file)"

    transitive_dependents:
      description: "Files affected through dependency chain"
      calculation: "traverse_import_graph(changed_file)"

    shared_module_impact:
      description: "Impact if shared/core module changed"
      multiplier: "1 + (dependent_count / 10)"

  score_calculation: |
    base_score = 0
    for file in changed_files:
      direct = count_direct_dependents(file)
      transitive = count_transitive_dependents(file)
      is_shared = is_in_shared_module(file)

      file_impact = (direct * 2) + (transitive * 0.5)
      if is_shared:
        file_impact *= 1.5

      base_score = max(base_score, file_impact)

    dependency_score = min(100, base_score)

  monorepo_considerations:
    cross_package_impact:
      detection: "Changes affect multiple packages"
      amplifier: 1.3

    shared_package_change:
      detection: "Core/shared package modified"
      amplifier: 1.5
```

### 5. Test Coverage (15% weight)

```yaml
test_coverage:
  coverage_analysis:
    line_coverage:
      excellent: "> 90%"
      good: "70-90%"
      fair: "50-70%"
      poor: "< 50%"

    branch_coverage:
      excellent: "> 85%"
      good: "60-85%"
      fair: "40-60%"
      poor: "< 40%"

    change_coverage:
      description: "Tests exist for changed code"
      calculation: "changed_lines_with_tests / total_changed_lines"

  score_calculation: |
    if change_coverage > 0.9:
      test_risk = 10  # Low risk
    elif change_coverage > 0.7:
      test_risk = 30
    elif change_coverage > 0.5:
      test_risk = 50
    elif change_coverage > 0.3:
      test_risk = 70
    else:
      test_risk = 90  # High risk

  coverage_regression:
    detection: "New code has lower coverage than existing"
    amplifier: 1.2
    action: "Flag for Radar test addition"
```

### 6. Author Familiarity (10% weight - reduced from original)

```yaml
author_familiarity:
  ownership_analysis:
    high_familiarity:
      condition: "Author has > 50% commits to changed files"
      score: 10  # Low risk

    medium_familiarity:
      condition: "Author has 20-50% commits"
      score: 40

    low_familiarity:
      condition: "Author has 5-20% commits"
      score: 60

    unfamiliar:
      condition: "Author has < 5% commits"
      score: 80

    first_contribution:
      condition: "Author's first commit to these files"
      score: 90

  recency_weight:
    recent_work: "Commits in last 30 days weighted 2x"
    older_work: "Commits > 90 days weighted 0.5x"

  team_knowledge:
    single_expert:
      detection: "Only one person knows this code"
      amplifier: 1.3
      reason: "Bus factor risk"
```

### 7. Ripple Impact (10% weight - NEW)

**Integration with Ripple agent for cross-codebase impact analysis**

```yaml
ripple_impact:
  description: |
    Measures the potential downstream impact of changes
    using Ripple agent's dependency and pattern analysis.

  components:
    dependency_depth:
      weight: 40%
      description: "How deep in the dependency tree are consumers"
      scoring:
        low: "Only direct dependents (1 level)"
        medium: "2-3 levels of dependents"
        high: "4+ levels or circular paths"

    pattern_consistency:
      weight: 30%
      description: "Does change break existing patterns"
      scoring:
        consistent: "Follows established patterns"
        minor_deviation: "Small variation from patterns"
        breaking: "Introduces new/conflicting pattern"

    consumer_count:
      weight: 30%
      description: "Number of files/modules affected"
      scoring:
        low: "< 5 consumers"
        medium: "5-20 consumers"
        high: "> 20 consumers"

  score_calculation: |
    ripple_score = (
      dependency_depth_score * 0.4 +
      pattern_consistency_score * 0.3 +
      consumer_count_score * 0.3
    )

  integration_triggers:
    auto_request_ripple:
      - "Shared module modified"
      - "API contract changed"
      - "Core utility updated"
      - "Cross-module dependencies added"

  handoff_format:
    request: GUARDIAN_TO_RIPPLE_HANDOFF
    response: RIPPLE_TO_GUARDIAN_HANDOFF
```

### Ripple Integration Protocol

```yaml
ripple_integration:
  when_to_request:
    conditions:
      - shared_module_changed: true
      - dependency_impact > 3
      - api_signature_changed: true
      - pattern_deviation_detected: true

  request_format:
    type: GUARDIAN_TO_RIPPLE_HANDOFF
    includes:
      - Changed files list
      - Change type (addition/modification/deletion)
      - Suspected impact scope
      - Specific questions

  response_processing:
    on_receive: RIPPLE_TO_GUARDIAN_HANDOFF
    actions:
      - Incorporate ripple_score into risk assessment
      - Adjust quality score based on pattern compliance
      - Add affected files to review scope
      - Generate additional recommendations

  risk_amplification:
    high_ripple_impact:
      threshold: "ripple_score > 70"
      amplifier: 1.3
      actions:
        - "Recommend split by impact zone"
        - "Suggest staged rollout"
        - "Flag for additional review"

    breaking_pattern:
      threshold: "pattern_consistency == breaking"
      amplifier: 1.5
      actions:
        - "Require pattern documentation"
        - "Recommend ADR creation"
        - "Alert architecture team"
```

### RIPPLE_TO_GUARDIAN_HANDOFF Processing

```yaml
ripple_response_handling:
  response_structure:
    impact_analysis:
      direct_dependents: [file_list]
      transitive_dependents: [file_list]
      ripple_depth: number
      affected_modules: [module_list]

    pattern_analysis:
      current_patterns: [pattern_list]
      deviations: [deviation_list]
      consistency_score: number
      recommendations: [list]

    risk_indicators:
      breaking_changes: [list]
      migration_needed: boolean
      consumer_updates_required: [list]

  integration_actions:
    update_risk_score:
      - Add ripple_score as 7th factor
      - Recalculate overall risk
      - Adjust category if threshold crossed

    update_recommendations:
      - Include Ripple's suggestions
      - Add affected files to review focus
      - Generate migration guidance if needed

    update_handoffs:
      - Include ripple impact in Judge handoff
      - Add pattern notes to Zen handoff
      - Include architecture notes for Atlas
```

### Quality Score Integration

```yaml
ripple_quality_impact:
  pattern_compliance_bonus:
    description: "Bonus for following patterns"
    condition: "pattern_consistency == consistent"
    bonus: "+5 focus score"

  pattern_breaking_penalty:
    description: "Penalty for breaking patterns"
    condition: "pattern_consistency == breaking"
    penalty: "-10 focus score, -5 risk score"

  documentation_requirement:
    condition: "breaking_pattern AND no_documentation"
    penalty: "-10 documentation score"
    action: "Require pattern documentation"
```

---

## Updated Risk Factor Framework (with Ripple)

| Factor | Weight | Description |
|--------|--------|-------------|
| File Sensitivity | 25% | Impact of files being changed |
| Change Complexity | 20% | Cyclomatic complexity delta |
| Hotspot Overlap | 15% | Frequently changed files |
| Dependency Impact | 10% | Direct/transitive dependents |
| Test Coverage | 10% | Coverage of changed code |
| Author Familiarity | 10% | Code ownership history |
| **Ripple Impact** | **10%** | **Cross-codebase propagation** |

---

## Risk Categories

```yaml
risk_categories:
  critical:
    score_range: [85, 100]
    characteristics:
      - Security-critical files
      - No test coverage
      - High complexity
      - Many dependents
    required_actions:
      - Senior developer review
      - Security review (Sentinel)
      - Comprehensive testing
      - Staged rollout
      - Rollback plan

  high:
    score_range: [65, 84]
    characteristics:
      - Important business logic
      - Partial test coverage
      - Moderate complexity
      - Some dependents
    required_actions:
      - Additional reviewer
      - Integration testing
      - Monitor after deploy

  medium:
    score_range: [40, 64]
    characteristics:
      - Standard code changes
      - Adequate coverage
      - Normal complexity
    required_actions:
      - Standard review
      - Normal testing
      - Standard deployment

  low:
    score_range: [0, 39]
    characteristics:
      - Low-impact changes
      - Good coverage
      - Simple changes
    required_actions:
      - Standard review
      - May expedite if needed
```

---

## Risk Report Template

```markdown
## Change Risk Assessment

**Branch:** `{branch}` → `{target}`
**Overall Risk Score:** {score}/100 ({category})

### Risk Factor Breakdown
```
File Sensitivity:   {bar} {sensitivity}/100  ({sensitivity_desc})
Change Complexity:  {bar} {complexity}/100   ({complexity_desc})
Hotspot Overlap:    {bar} {hotspot}/100      ({hotspot_count} files)
Dependency Impact:  {bar} {dependency}/100   ({dependent_count} dependents)
Test Coverage Gap:  {bar} {coverage}/100     ({coverage_pct}% covered)
Author Familiarity: {bar} {familiarity}/100  ({familiarity_desc})
```

### High-Risk Files
| File | Risk Score | Primary Factor |
|------|------------|----------------|
{high_risk_files}

### Risk Factors Detail

#### Sensitivity Analysis
{sensitivity_details}

#### Complexity Analysis
{complexity_details}

#### Hotspot Impact
{hotspot_details}

### Mitigation Recommendations
{mitigation_list}

### Required Actions
- [ ] {action_1}
- [ ] {action_2}
- [ ] {action_3}

### Deployment Strategy
{deployment_recommendation}
```

---

## Mitigation Strategies

### By Risk Category

```yaml
mitigation_strategies:
  critical_risk:
    pre_merge:
      - Sentinel security review
      - Probe DAST if API changes
      - Load testing if performance-critical
      - Pair programming review

    deployment:
      - Feature flag required
      - Canary deployment (1% → 10% → 50% → 100%)
      - Real-time monitoring
      - Instant rollback capability

    post_deploy:
      - 24-hour monitoring window
      - On-call engineer assigned
      - Automated alerts configured

  high_risk:
    pre_merge:
      - Two reviewer approval
      - Extended test suite run
      - Manual QA for critical paths

    deployment:
      - Feature flag recommended
      - Staged rollout (10% → 50% → 100%)
      - Enhanced monitoring

    post_deploy:
      - Business hours deploy only
      - Monitor for 4 hours

  medium_risk:
    pre_merge:
      - Standard review
      - CI test suite

    deployment:
      - Standard deployment
      - Normal monitoring

  low_risk:
    pre_merge:
      - Single reviewer
      - Fast-track possible

    deployment:
      - Any time deployment
      - Standard monitoring
```

### Specific Mitigations

```yaml
specific_mitigations:
  no_test_coverage:
    action: "Add tests before merge"
    handoff: Radar
    blocking: true

  security_sensitive:
    action: "Security review required"
    handoff: Sentinel
    blocking: true

  hotspot_modification:
    action: "Consider refactoring first"
    handoff: Zen
    blocking: false

  unfamiliar_author:
    action: "Pair with code owner"
    handoff: null
    blocking: false

  high_complexity:
    action: "Split into smaller changes"
    handoff: Guardian (self)
    blocking: false

  many_dependents:
    action: "Impact analysis required"
    handoff: Atlas
    blocking: true
```

---

## Regression Risk Prediction

### Historical Analysis

```yaml
regression_prediction:
  analysis:
    recent_bugs:
      description: "Bug fixes in changed files (90 days)"
      weight: 0.4

    revert_history:
      description: "Reverted commits affecting files"
      weight: 0.3

    flaky_tests:
      description: "Test flakiness in affected areas"
      weight: 0.2

    previous_regression:
      description: "Past regressions from similar changes"
      weight: 0.1

  calculation: |
    regression_risk = (
      recent_bugs * 0.4 +
      revert_count * 0.3 +
      flaky_test_score * 0.2 +
      historical_regression * 0.1
    )

  output:
    high: "> 70% regression probability"
    medium: "40-70% regression probability"
    low: "< 40% regression probability"

  recommendations:
    high:
      - "Add regression tests for issues #xxx, #yyy"
      - "Review fix patterns in similar files"
      - "Consider alternative approach"

    medium:
      - "Ensure related tests pass"
      - "Monitor after deploy"

    low:
      - "Standard testing sufficient"
```

---

## Integration with AUTORUN

```yaml
autorun_risk_assessment:
  auto_execute:
    - Calculate all risk factors
    - Generate risk score
    - Identify mitigation needs
    - Determine deployment strategy

  pause_conditions:
    - risk_score > 85 (CRITICAL)
    - security_files_changed AND no_security_review
    - coverage_gap > 50%

  output_format:
    _STEP_COMPLETE:
      Agent: Guardian
      Status: SUCCESS | PARTIAL
      Output:
        risk_assessment:
          total_score: 72
          category: HIGH
          factors:
            sensitivity: 80
            complexity: 65
            hotspot: 75
            dependency: 60
            coverage: 70
            familiarity: 55
          high_risk_files:
            - path: "src/auth/jwt.ts"
              score: 92
              reason: "Auth + hotspot + low coverage"
          mitigations:
            - "Security review required"
            - "Add token refresh tests"
          deployment_strategy: "staged_rollout"
      Next: Sentinel  # If security review needed
```

---

## Risk Trending

### Historical Risk Tracking

```yaml
risk_trending:
  per_pr:
    - Track risk scores over time
    - Identify patterns
    - Alert on increasing risk

  per_file:
    - Monitor file risk over time
    - Detect deteriorating code
    - Suggest proactive refactoring

  per_author:
    - Track author risk patterns
    - Identify training opportunities
    - Celebrate improvement

  alerts:
    increasing_risk:
      condition: "3 consecutive PRs with higher risk"
      action: "Review development practices"

    persistent_hotspot:
      condition: "File in top 5 hotspots for 6 months"
      action: "Prioritize refactoring"

    coverage_decline:
      condition: "Coverage decreased 3 times"
      action: "Enforce coverage requirements"
```
