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
# ...
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
# ...
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
# ...
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
# ...
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
# ...
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
# ...
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
# ...
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
...
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
# ...
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
# ...
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
# ...
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
# ...
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
# ...
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
# ...
```
