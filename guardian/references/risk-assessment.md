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
# ...
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
# ...
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
# ...
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
# ...
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
# ...
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
# ...
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
# ...
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
# ...
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
# ...
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

# ...
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
...
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
# ...
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
# ...
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
# ...
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
# ...
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
# ...
```
