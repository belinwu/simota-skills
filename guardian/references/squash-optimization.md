# Squash Optimization Reference

> Guardian's analytical engine for squash decision-making, group detection, message synthesis, and commit sequence optimization.
> Non-loop branch analysis and PR preparation — Orbit handles loop-iteration squash execution.

---

## A. Squash Decision Engine

### Pairwise Scoring System

Evaluate each adjacent commit pair against 6 weighted factors. Positive scores favor squashing; negative scores favor keeping separate.

```yaml
squash_scoring:
  factors:
    temporal_proximity:
      weight: 15
      rules:
        same_minute: +15     # Rapid-fire commits (likely WIP)
        within_10min: +12    # Close sequence
        within_1hour: +8     # Same session
        within_4hours: +4    # Same work block
        within_1day: +1      # Same day
        beyond_1day: 0       # Different sessions
        beyond_1week: -5     # Intentionally separate work

    subject_relationship:
      weight: 25
      rules:
        identical_prefix: +25       # Same type(scope): prefix
        fixup_of_previous: +25      # "fix typo in ...", "forgot to add"
        wip_commit: +20             # "WIP", "wip", "work in progress", "tmp"
        same_feature_area: +15      # Related feature work
        same_type_different_scope: +5  # e.g., both feat but different modules
        unrelated_subjects: 0       # No clear relationship
        opposing_concerns: -15      # e.g., feat + refactor in same area
        different_logical_units: -25 # Clearly independent changes

    file_overlap:
      weight: 20
      rules:
        complete_overlap: +20   # 100% same files
        high_overlap: +15       # >70% overlap
        moderate_overlap: +10   # 30-70% overlap
        low_overlap: +3         # 10-30% overlap
        no_overlap: -5          # 0% overlap — likely independent
        lock_file_only: -10     # Lock file changes should stay separate

    author_attribution:
      weight: 15
      rules:
        same_author: +15        # No attribution concern
        same_org_team: +5       # Same team, consider Co-authored-by
        different_author: -10   # Attribution preservation needed
        multi_author_chain: -15 # Complex attribution — keep separate

    atomicity_impact:
      weight: 15
      rules:
        improves_atomicity: +15   # Combined commit is more atomic
        neutral_atomicity: +5     # No change in atomicity
        reduces_atomicity: -10    # Combined commit becomes multi-concern
        breaks_bisectability: -15 # Squashing would make git bisect harder

    test_coupling:
      weight: 10
      rules:
        test_with_implementation: +10  # Test + impl = good squash
        test_for_previous_impl: +8     # Test added for prior commit
        standalone_test: -5            # Independent test commit
        test_refactor_only: -3         # Separate concern
```

### Decision Thresholds

```yaml
squash_thresholds:
  strong_squash: ">= +30"     # Highly recommended — squash or fixup
  suggest_squash: "+15 to +29" # Suggested — present to user
  neutral: "-14 to +14"       # No recommendation — user decides
  keep_separate: "<= -15"     # Recommended to keep separate

  # Override rules (take precedence over score)
  force_squash:
    - "Subject matches: /^(WIP|wip|fixup!|squash!|tmp|temp)/i"
    - "Subject matches: /^(fix typo|forgot to|oops|address review)/i"
    - "Empty commit message"
  force_keep:
    - "Different authors AND no explicit Co-authored-by intent"
    - "Lock file changes (always separate commit)"
    - "Security-related commits (preserve audit trail)"
    - "Revert commits (preserve rollback capability)"
```

### Action Mapping

```yaml
action_mapping:
  fixup:
    description: "Absorb into previous — discard message"
    use_when:
      - "Score >= +30 AND commit is noise (WIP/typo/forgot)"
      - "Score >= +30 AND commit message adds no value"
    rebase_command: "fixup"

  squash:
    description: "Combine with previous — merge messages"
    use_when:
      - "Score >= +15 AND both messages contain useful info"
      - "Score >= +15 AND Co-authored-by preservation needed"
    rebase_command: "squash"

  pick:
    description: "Keep as independent commit"
    use_when:
      - "Score < +15"
      - "Force-keep override triggered"
    rebase_command: "pick"

  drop:
    description: "Remove entirely"
    use_when:
      - "Empty commit (no file changes)"
      - "Commit reverted later in sequence"
      - "Duplicate of another commit"
    rebase_command: "drop"
```

---

## B. Squash Group Detection Algorithm

### 5-Step Grouping Process

```yaml
group_detection:
  step_1_initial_clustering:
    description: "Create initial groups from pairwise scores"
    algorithm: |
      1. Score all adjacent commit pairs using Decision Engine
      2. Mark pairs with score >= +15 as "merge candidates"
      3. Chain consecutive merge candidates into initial groups
      4. Isolated commits become singleton groups

  step_2_merge_noise:
    description: "Absorb noise commits into nearest group"
    algorithm: |
      1. Identify noise commits (WIP, fixup, typo, tmp, empty message)
      2. For each noise commit, find nearest group by:
         a. File overlap (prefer highest)
         b. Temporal proximity (prefer closest)
         c. Subject similarity (prefer matching scope)
      3. Absorb noise into best-matching group
      4. If no suitable group, create "cleanup" group

  step_3_evaluate_merges:
    description: "Validate each group maintains atomicity"
    algorithm: |
      1. For each group, compute combined change set
      2. Check: does combined commit serve a single purpose?
      3. Check: does combined commit touch a reasonable file count?
      4. If group violates atomicity, split into subgroups
      5. Threshold: group with >3 distinct concerns → split

  step_4_dependency_ordering:
    description: "Order groups by dependency topology"
    priority_order:
      1: "Type definitions and interfaces"
      2: "Core implementation (models, services)"
      3: "Integration layer (controllers, routes)"
      4: "Tests"
      5: "Documentation and comments"
      6: "Configuration and build"
      7: "Style and formatting (noise)"

  step_5_output:
    description: "Generate final group assignments"
    output_format:
      groups:
        - id: 1
          action: "squash"
          commits: ["abc1234", "def5678"]
          anchor_commit: "abc1234"
          synthesized_message: "feat(auth): add OAuth2 provider integration"
          files: ["src/auth/oauth.ts", "src/auth/types.ts"]
          rationale: "Same feature, high file overlap (85%), same author"
        - id: 2
          action: "pick"
          commits: ["ghi9012"]
          anchor_commit: "ghi9012"
          synthesized_message: null  # Keep original
          files: ["tests/auth/oauth.test.ts"]
          rationale: "Standalone test commit, independent concern"
```

### Group Size Limits

```yaml
group_limits:
  max_commits_per_group: 8
  max_files_per_group: 30
  warning_threshold:
    commits: 5
    files: 20
  action_on_exceed:
    - "Split group at natural boundaries"
    - "Report warning in optimization output"
```

---

## C. Squash Message Synthesis

### Anchor Selection Strategy

```yaml
anchor_selection:
  priority_order:
    1_conventional_commit:
      description: "Prefer commit with valid Conventional Commits format"
      detection: "/^(feat|fix|docs|style|refactor|perf|test|chore|ci|build)(\\(.+\\))?!?: .+/"
      rationale: "Maintains project commit convention"

    2_longest_description:
      description: "Prefer commit with most descriptive message"
      criteria:
        - "Has body section"
        - "Subject length > 30 characters"
        - "Contains issue references"
      rationale: "Preserves the most context"

    3_chronological_first:
      description: "Fall back to first commit in group"
      criteria: "Oldest commit in temporal order"
      rationale: "Represents original intent"
```

### Body Construction Rules

```yaml
body_construction:
  principles:
    - "Focus on 'why' over 'what'"
    - "Exclude noise messages entirely (WIP, fixup, typo)"
    - "Consolidate duplicate issue references"
    - "Preserve breaking change notices"

  assembly:
    subject: "From anchor commit (potentially reworded)"
    body:
      include:
        - "Meaningful descriptions from non-anchor commits"
        - "Breaking change notices from any commit"
        - "Notable implementation decisions"
      exclude:
        - "WIP / fixup / typo / temp messages"
        - "Duplicate information already in subject"
        - "Auto-generated messages (merge commits, reverts of reverts)"
    footer:
      include:
        - "All unique issue references (Closes, Fixes, Relates to)"
        - "All unique Co-authored-by lines"
        - "BREAKING CHANGE notices"
      dedup: true
```

### Co-authored-by Preservation

```yaml
co_authored_by:
  strategy: "Collect and deduplicate across all squashed commits"
  rules:
    - "Extract Co-authored-by from all commit messages in group"
    - "Extract commit authors (Author header) for non-anchor commits"
    - "Deduplicate by email address"
    - "Anchor commit author is the main author (not listed as co-author)"
    - "Format: 'Co-authored-by: Name <email>'"
  verification:
    - "Count unique authors before squash"
    - "Count Co-authored-by + main author after squash"
    - "Counts must match — alert if attribution would be lost"
```

### Message Templates

```yaml
templates:
  standard_squash:
    format: |
      {type}({scope}): {subject}

      {body — consolidated from meaningful commits}

      {issue_refs — deduplicated}
      {co_authored_by — all contributors}
    example: |
      feat(auth): add OAuth2 provider integration

      Implement OAuth2 flow with support for Google and GitHub providers.
      Token refresh handles concurrent requests via mutex lock.

      Closes #123
      Co-authored-by: Alice <alice@example.com>

  multi_concern_squash:
    format: |
      {type}({scope}): {primary subject}

      {primary change description}

      Also includes:
      - {secondary change 1}
      - {secondary change 2}

      {issue_refs}
      {co_authored_by}
    example: |
      feat(auth): add OAuth2 provider integration

      Implement OAuth2 flow with Google and GitHub provider support.

      Also includes:
      - Add rate limiting for token refresh endpoint
      - Update auth middleware to support OAuth2 tokens

      Closes #123, Closes #125
```

---

## D. Commit Sequence Optimization

### 5-Phase Algorithm

```yaml
sequence_optimization:
  phase_1_analysis:
    description: "Analyze current commit sequence"
    steps:
      - "List all commits from merge-base to HEAD"
      - "Classify each commit (essential/supporting/noise)"
      - "Map file changes per commit"
      - "Identify author attribution"
      - "Detect WIP/noise patterns"

  phase_2_clustering:
    description: "Apply group detection algorithm"
    steps:
      - "Run pairwise scoring on all adjacent commits"
      - "Execute 5-step grouping (Section B)"
      - "Validate group atomicity"

  phase_3_dependency_ordering:
    description: "Order groups by dependency"
    steps:
      - "Build dependency graph from file imports/usage"
      - "Apply topological sort (Section B, step 4)"
      - "Resolve cycles by choosing minimal-risk break point"

  phase_4_noise_consolidation:
    description: "Handle remaining noise commits"
    strategies:
      minimal_noise:
        threshold: "< 3 noise commits"
        action: "fixup into nearest related commit"
      moderate_noise:
        threshold: "3-8 noise commits"
        action: "Consolidate into single 'chore: cleanup' commit at end"
      heavy_noise:
        threshold: "> 8 noise commits"
        action: "Recommend separating into cleanup PR"

  phase_5_validation:
    description: "Verify optimized sequence"
    checks:
      - "Each commit passes lint/build independently"
      - "Total diff matches original (no changes lost)"
      - "All authors attributed"
      - "All issue references preserved"
      - "Commit count reduced (improvement metric)"
```

### Lock File Handling

```yaml
lock_file_strategy:
  rule: "Always keep lock file changes in a separate commit"
  patterns:
    - "package-lock.json"
    - "yarn.lock"
    - "pnpm-lock.yaml"
    - "Gemfile.lock"
    - "poetry.lock"
    - "Cargo.lock"
    - "go.sum"
    - "composer.lock"
  commit_template: "chore(deps): update lock file"
  rationale: "Lock files generate large diffs that obscure real changes"
```

---

## E. Post-Squash Verification Guidance

### Immediate Checks

```yaml
immediate_verification:
  commit_count:
    check: "git rev-list --count {merge-base}..HEAD"
    expected: "Matches optimized plan count"
    action_on_mismatch: "Review rebase log for dropped/extra commits"

  diff_integrity:
    check: "git diff {backup-branch}..HEAD"
    expected: "Empty diff (no changes lost or introduced)"
    action_on_diff: "STOP — investigate missing or extra changes"

  attribution:
    check: "git log --format='%an <%ae>' {merge-base}..HEAD | sort -u"
    expected: "All original authors present (in commits or Co-authored-by)"
    action_on_missing: "Add missing Co-authored-by lines"

  issue_references:
    check: "git log --format='%B' {merge-base}..HEAD | grep -iE '(closes|fixes|relates to) #'"
    expected: "All original issue refs preserved"
    action_on_missing: "Amend commit messages to restore references"
```

### Build Verification

```yaml
build_verification:
  per_commit_build:
    command: "git rebase -i --exec 'npm run build' {merge-base}"
    purpose: "Ensure each commit builds independently"
    alternative: "git rebase -i --exec 'make check' {merge-base}"
    note: "Adapt build command to project's build system"

  per_commit_test:
    command: "git rebase -i --exec 'npm test' {merge-base}"
    purpose: "Ensure each commit passes tests independently"
    caution: "May be slow for large test suites — consider smoke tests"
```

### Rollback Plan

```yaml
rollback:
  backup_branch:
    before_rebase: "git branch backup/{branch-name}-pre-squash"
    restore: "git reset --hard backup/{branch-name}-pre-squash"
    cleanup: "git branch -d backup/{branch-name}-pre-squash"

  reflog:
    find: "git reflog show {branch-name}"
    restore: "git reset --hard {branch-name}@{N}"
    note: "Reflog entries expire after 90 days by default"

  remote_reset:
    caution: "Only if branch was already force-pushed"
    command: "git push --force-with-lease origin {branch-name}"
    note: "--force-with-lease prevents overwriting others' work"
```

### CI Gate Recommendations

```yaml
ci_gates:
  required_before_merge:
    - "Full test suite passes"
    - "Build succeeds on all target platforms"
    - "Lint and format checks pass"
  recommended:
    - "Security scan (SAST)"
    - "Dependency vulnerability check"
    - "Coverage threshold met"
  note: "Run CI after rebase to catch issues introduced by commit reordering"
```

---

## Orbit-Guardian Squash Boundary

```yaml
orbit_guardian_squash_boundary:
  orbit_domain:
    - "Loop-iteration squash execution (automated rebase)"
    - "LLM-generated squash commit messages within loop context"
    - "Branch isolation strategy for loop artifacts"
    - "Iter-level squash decision (within orbit's autonomous loop)"

  guardian_domain:
    - "Non-loop branch squash analysis and recommendations"
    - "PR preparation squash optimization"
    - "Multi-contributor attribution analysis"
    - "Squash scoring engine (pairwise evaluation)"
    - "Commit sequence optimization for review readiness"
    - "Post-squash verification guidance"

  overlap_resolution:
    rule: "Guardian reviews Orbit's loop output but does NOT re-squash"
    workflow: |
      1. Orbit completes loop → produces squashed commits
      2. Guardian receives commits as input
      3. Guardian evaluates for PR readiness (quality, message, attribution)
      4. Guardian may suggest message rewording but NOT re-squash
    rationale: "Orbit's squash decisions are contextually optimized for loop iteration; Guardian adds PR-level polish"
```
