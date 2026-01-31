# Branch Health Diagnostics Reference

Detailed methodology for Guardian's branch health assessment.

## Health Philosophy

Healthy branches:
- Stay synchronized with target branch
- Merge quickly without conflicts
- Maintain reviewable size
- Pass continuous integration

---

## Health Indicators

### 1. Sync Status (25% weight)

```yaml
sync_status:
  description: "How far behind the target branch"

  measurement:
    commits_behind:
      healthy: 0-5
      warning: 6-15
      critical: 16-30
      severe: 31+

    days_since_rebase:
      healthy: 0-3
      warning: 4-7
      critical: 8-14
      severe: 15+

  calculation: |
    behind_main = count_commits_behind(branch, target)
    last_sync = days_since_last_rebase_or_merge(branch, target)

    if behind_main <= 5 and last_sync <= 3:
      sync_score = 100
    elif behind_main <= 15 and last_sync <= 7:
      sync_score = 75
    elif behind_main <= 30 and last_sync <= 14:
      sync_score = 50
    else:
      sync_score = 25

  recommendations:
    warning: "Rebase soon to avoid conflicts"
    critical: "Rebase now - high conflict risk"
    severe: "Major rebase needed - consider splitting"

  commands:
    check: "git rev-list HEAD..origin/main --count"
    fix: "git fetch origin main && git rebase origin/main"
```

### 2. Branch Age (20% weight)

```yaml
branch_age:
  description: "Time since branch creation"

  thresholds:
    fresh:
      days: 0-3
      score: 100
      status: "healthy"

    active:
      days: 4-7
      score: 85
      status: "healthy"

    maturing:
      days: 8-14
      score: 65
      status: "warning"

    stale:
      days: 15-30
      score: 40
      status: "critical"

    abandoned:
      days: 31+
      score: 15
      status: "severe"

  activity_adjustment:
    recent_commits:
      condition: "Commit in last 24 hours"
      adjustment: "+10 to score"

    no_recent_activity:
      condition: "No commit in 3+ days"
      adjustment: "-10 to score"

  recommendations:
    maturing: "Complete or split soon"
    stale: "Needs attention - merge or split"
    abandoned: "Consider closing or rebasing fresh"
```

### 3. Conflict Potential (20% weight)

```yaml
conflict_potential:
  description: "Likelihood of merge conflicts"

  detection:
    file_overlap:
      check: "Files modified in both branches"
      method: |
        branch_files = git_diff_files(branch, merge_base)
        target_files = git_diff_files(target, merge_base)
        overlap = intersection(branch_files, target_files)

    hunk_overlap:
      check: "Line ranges overlap"
      method: |
        for file in overlapping_files:
          branch_hunks = get_changed_hunks(branch, file)
          target_hunks = get_changed_hunks(target, file)
          if hunks_overlap(branch_hunks, target_hunks):
            conflict_likely = true

  scoring:
    none:
      condition: "No overlapping files"
      score: 100

    unlikely:
      condition: "Overlapping files but different hunks"
      score: 80

    possible:
      condition: "Adjacent hunks"
      score: 60

    likely:
      condition: "Overlapping hunks detected"
      score: 30

    certain:
      condition: "Git reports merge conflict"
      score: 0

  conflict_files_report:
    format: |
      | File | Branch Lines | Target Lines | Risk |
      |------|--------------|--------------|------|
      {conflict_file_rows}

  recommendations:
    possible: "Monitor {files} for conflicts"
    likely: "Coordinate with owner of {files}"
    certain: "Resolve conflicts before continuing"
```

### 4. CI Status (15% weight)

```yaml
ci_status:
  description: "Continuous integration health"

  states:
    passing:
      condition: "All checks pass"
      score: 100

    pending:
      condition: "Checks in progress"
      score: 75  # Neutral

    flaky:
      condition: "Intermittent failures"
      score: 50

    failing:
      condition: "Consistent failures"
      score: 20

    no_ci:
      condition: "No CI configured or run"
      score: 40  # Unknown risk

  flaky_detection:
    method: "Same commit, different results"
    threshold: "2+ different outcomes"
    action: "Investigate test stability"

  failure_analysis:
    categories:
      test_failure:
        severity: "high"
        action: "Fix tests"
      lint_failure:
        severity: "medium"
        action: "Fix style issues"
      build_failure:
        severity: "high"
        action: "Fix build"
      security_scan:
        severity: "critical"
        action: "Address vulnerabilities"

  recommendations:
    failing: "Fix CI before review"
    flaky: "Investigate test stability"
    no_ci: "Ensure CI runs on branch"
```

### 5. Size Creep (10% weight)

```yaml
size_creep:
  description: "PR growing over time"

  measurement:
    initial_size:
      files: "Count at first commit"
      lines: "Lines at first commit"

    current_size:
      files: "Current file count"
      lines: "Current line count"

    growth_rate: "(current - initial) / initial"

  thresholds:
    stable:
      growth: "< 10%"
      score: 100

    minor_growth:
      growth: "10-25%"
      score: 85

    moderate_growth:
      growth: "25-50%"
      score: 65

    significant_growth:
      growth: "50-100%"
      score: 40

    explosive_growth:
      growth: "> 100%"
      score: 20

  tracking:
    per_commit:
      - Commit hash
      - Files added/modified
      - Lines added/removed
      - Cumulative size

  visualization: |
    Commit 1: ████ 12 files, 234 lines
    Commit 2: █████ 15 files, 312 lines
    Commit 3: ████████ 22 files, 456 lines
    Commit 4: ████████████ 35 files, 678 lines  ← 3x growth

  recommendations:
    moderate_growth: "Consider splitting if more growth expected"
    significant_growth: "Split into focused PRs"
    explosive_growth: "Must split - PR too large"
```

### 6. Review Status (10% weight)

```yaml
review_status:
  description: "Code review progress"

  states:
    active:
      indicators:
        - "Review comments in last 24h"
        - "Author responding to feedback"
      score: 100

    in_progress:
      indicators:
        - "Review started"
        - "Some comments addressed"
      score: 85

    awaiting_review:
      indicators:
        - "Review requested"
        - "No review activity yet"
      score: 70

    stale_review:
      indicators:
        - "No review activity in 3+ days"
        - "Open conversations"
      score: 40

    blocked:
      indicators:
        - "Changes requested"
        - "Not addressed"
      score: 25

    abandoned:
      indicators:
        - "No activity in 7+ days"
        - "Author unresponsive"
      score: 10

  metrics:
    time_to_first_review:
      target: "< 24 hours"

    review_cycles:
      healthy: "1-2 cycles"
      concerning: "4+ cycles"

    open_conversations:
      concerning: "> 5 unresolved"

  recommendations:
    stale_review: "Follow up with reviewers"
    blocked: "Address change requests"
    abandoned: "Close or reassign"
```

---

## Aggregate Health Score

```yaml
aggregate_calculation:
  formula: |
    health = (sync * 0.25) +
             (age * 0.20) +
             (conflict * 0.20) +
             (ci * 0.15) +
             (size * 0.10) +
             (review * 0.10)

  grades:
    excellent: [90, 100]
    healthy: [75, 89]
    warning: [50, 74]
    critical: [25, 49]
    severe: [0, 24]

  actions_by_grade:
    excellent: "Ready to merge"
    healthy: "Normal development"
    warning: "Needs attention soon"
    critical: "Requires immediate action"
    severe: "Consider closing/rebasing"
```

---

## Health Report Template

```markdown
## Branch Health Report

**Branch:** `{branch}`
**Target:** `{target}`
**Created:** {created_date} ({age} days ago)
**Last Commit:** {last_commit_date}

### Health Score: {score}/100 ({grade})

### Status Indicators
| Indicator | Status | Value | Score |
|-----------|--------|-------|-------|
| Sync with {target} | {sync_status} | {behind} behind | {sync_score} |
| Branch age | {age_status} | {age} days | {age_score} |
| Conflict risk | {conflict_status} | {conflict_files} files | {conflict_score} |
| CI status | {ci_status} | {ci_result} | {ci_score} |
| Size creep | {size_status} | {growth}% growth | {size_score} |
| Review status | {review_status} | {review_state} | {review_score} |

### Branch Timeline
```
{target} ───●────●────●────●────●────●────●────●────●─── HEAD
            │
            └────●────●────●────●────●────●─── {branch}
                 ↑                          ↑
            Created ({age}d)          Last commit ({last}d)
                            {behind} commits behind
```

### Issues Detected
{issues_list}

### Recommended Actions
1. {action_1}
2. {action_2}
3. {action_3}

### Conflict Risk Analysis
{conflict_analysis}

### Size History
{size_history}
```

---

## Proactive Health Monitoring

### Automated Checks

```yaml
automated_monitoring:
  schedule: "Daily at 9 AM"

  checks:
    stale_branches:
      condition: "age > 7 days AND no recent commits"
      action: "Notify author"

    sync_drift:
      condition: "behind > 15 commits"
      action: "Suggest rebase"

    conflict_emergence:
      condition: "conflict_potential increased"
      action: "Alert author"

    ci_degradation:
      condition: "CI was passing, now failing"
      action: "Notify author"

    size_explosion:
      condition: "growth > 50% in last day"
      action: "Suggest split"

  notifications:
    slack:
      channel: "#branch-health"
      format: |
        :warning: Branch Health Alert
        Branch: {branch}
        Issue: {issue}
        Recommendation: {recommendation}

    email:
      subject: "[Branch Health] {branch} needs attention"
      body: "{detailed_report}"
```

### Health Trends

```yaml
health_trends:
  track_per_branch:
    - Daily health score
    - Score changes
    - Issues resolved

  aggregate_metrics:
    team_avg_branch_age:
      target: "< 5 days"

    merge_success_rate:
      target: "> 90%"

    conflict_frequency:
      target: "< 10% of PRs"

  dashboards:
    branch_health_overview:
      - Active branches by health
      - Branches needing attention
      - Historical trends
```

---

## Integration with AUTORUN

```yaml
autorun_branch_health:
  auto_execute:
    - Calculate all health indicators
    - Generate health score
    - Identify issues
    - Propose remediation

  pause_conditions:
    - health_score < 25 (severe)
    - conflict_certain = true
    - ci_status = failing

  output_format:
    _STEP_COMPLETE:
      Agent: Guardian
      Status: SUCCESS | PARTIAL
      Output:
        branch_health:
          score: 68
          grade: warning
          indicators:
            sync: 75
            age: 60
            conflict: 80
            ci: 100
            size: 50
            review: 70
          issues:
            - "15 commits behind main"
            - "Branch age: 10 days"
            - "Size increased 45%"
          actions:
            - "Rebase onto main"
            - "Consider splitting"
      Next: Guardian  # Self for rebase guidance
```

---

## Remediation Workflows

### Rebase Workflow

```yaml
rebase_guidance:
  steps:
    1: "Ensure working directory is clean"
    2: "Fetch latest target branch"
    3: "Start interactive rebase"
    4: "Resolve any conflicts"
    5: "Verify tests pass"
    6: "Force push (with lease)"

  commands: |
    # Save current work
    git stash

    # Fetch latest
    git fetch origin main

    # Interactive rebase
    git rebase -i origin/main

    # After resolving conflicts
    git rebase --continue

    # Verify
    npm test

    # Push
    git push --force-with-lease

  conflict_resolution:
    per_file_guidance: true
    scout_handoff_if_complex: true
```

### Split Workflow

```yaml
split_guidance:
  steps:
    1: "Analyze current changes"
    2: "Identify logical split points"
    3: "Create split plan"
    4: "Execute progressive splits"

  strategies:
    by_module:
      when: "Changes span multiple modules"
      approach: "One PR per module"

    by_layer:
      when: "Changes span layers"
      approach: "API first, then UI"

    by_feature:
      when: "Multiple features mixed"
      approach: "One PR per feature"

  execution: |
    # Create branches for each split
    git checkout -b split-1-{feature}
    # Cherry-pick or reset to include only relevant commits
    git checkout {original} -- path/to/files

  sherpa_handoff:
    condition: "MEGA PR or complex split"
    format: GUARDIAN_TO_SHERPA_HANDOFF
```

---

## Branch Lifecycle

```yaml
branch_lifecycle:
  stages:
    created:
      expected_duration: "< 1 day"
      health_focus: "Initial setup"

    development:
      expected_duration: "1-5 days"
      health_focus: "Sync, CI, size"

    review:
      expected_duration: "1-3 days"
      health_focus: "Review status"

    ready:
      expected_duration: "< 1 day"
      health_focus: "Final checks"

    merged:
      cleanup: "Delete branch"

  warnings:
    extended_development:
      trigger: "development > 7 days"
      action: "Check for blockers, suggest split"

    stalled_review:
      trigger: "review > 3 days without activity"
      action: "Follow up with reviewers"

    merge_delay:
      trigger: "ready > 2 days without merge"
      action: "Check for blocking issues"
```
