# Commit Message Analysis Reference

Detailed methodology for Guardian's commit message quality assessment.

## Analysis Philosophy

Good commit messages:
- Tell a story of the project's evolution
- Enable effective `git bisect` and `git blame`
- Facilitate automated changelog generation
- Help reviewers understand intent

---

## Message Structure Analysis

### Conventional Commits Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Component Analysis

#### 1. Type Prefix

```yaml
type_analysis:
  valid_types:
    feat: "New feature"
    fix: "Bug fix"
    docs: "Documentation only"
    style: "Formatting, no logic change"
    refactor: "Code restructure, no behavior change"
    perf: "Performance improvement"
    test: "Adding/updating tests"
    chore: "Maintenance tasks"
    ci: "CI/CD changes"
    build: "Build system changes"
    revert: "Revert previous commit"

  scoring:
# ...
```

#### 2. Scope

```yaml
scope_analysis:
  purpose: "Identify affected module/component"

  valid_patterns:
    module_based: "auth", "api", "ui", "core"
    feature_based: "login", "checkout", "profile"
    layer_based: "db", "cache", "http"

  scoring:
    accurate_scope: 10
    broad_scope: 7
    missing_scope: 3
    wrong_scope: 0

  validation:
# ...
```

#### 3. Subject Line

```yaml
subject_analysis:
  rules:
    max_length: 72
    min_length: 10
    case: lowercase_start
    punctuation: no_period
    tense: imperative
    content: specific_action

  scoring:
    perfect_subject: 15
    good_subject: 12
    acceptable_subject: 8
    poor_subject: 4
    bad_subject: 0
# ...
```

#### 4. Body

```yaml
body_analysis:
  purpose: "Explain 'why', not 'what'"

  scoring:
    excellent_body: 5
    good_body: 4
    minimal_body: 2
    missing_when_needed: 0
    not_needed: 5  # Simple changes

  when_required:
    - Complex logic changes
    - Breaking changes
    - Non-obvious decisions
    - Performance trade-offs
# ...
```

#### 5. Footer

```yaml
footer_analysis:
  elements:
    issue_references:
      patterns:
        - "Closes #123"
        - "Fixes #456"
        - "Relates to #789"
      score: 3

    breaking_changes:
      pattern: "BREAKING CHANGE: description"
      required_when: api_or_behavior_change
      score: 2

    co_authors:
# ...
```

---

## Commit Sequence Analysis

### Atomicity Assessment

```yaml
atomicity_analysis:
  principles:
    - Each commit should be independently deployable
    - Each commit should pass tests
    - Each commit should have single purpose

  scoring:
    perfectly_atomic: 30
    mostly_atomic: 25
    partially_atomic: 15
    not_atomic: 5

  detection:
    atomic_indicators:
      - Single file type changed (e.g., all .ts)
# ...
```

### Commit Sequence Quality

```yaml
sequence_analysis:
  logical_order:
    correct:
      - Refactoring before feature
      - Tests with implementation
      - Docs after feature
    incorrect:
      - Tests before implementation
      - Docs scattered randomly
      - Fixes for just-added code

  wip_commits:
    detection:
      - Subject contains "WIP", "wip", "work in progress"
      - Subject contains "temp", "tmp"
# ...
```

---

## Message Improvement Suggestions

### Rewrite Templates

```yaml
rewrites:
  vague_to_specific:
    before: "fix bug"
    after: "fix(auth): resolve token refresh race condition"
    improvement: "Added type, scope, and specific description"

  past_to_imperative:
    before: "added login feature"
    after: "feat(auth): add login feature"
    improvement: "Changed to imperative mood with type prefix"

  too_long:
    before: "feat: add the ability for users to reset their passwords..."
    after: "feat(auth): add password reset functionality"
    improvement: "Condensed to under 72 characters"
# ...
```

### Common Patterns and Fixes

```yaml
pattern_fixes:
  capitalization:
    issue: "Subject starts with capital"
    fix: "Use lowercase (except proper nouns)"
    example:
      before: "Add user authentication"
      after: "add user authentication"

  period_ending:
    issue: "Subject ends with period"
    fix: "Remove trailing period"
    example:
      before: "fix login timeout issue."
      after: "fix login timeout issue"

# ...
```

---

## Interactive Rebase Guidance

### Rebase Plan Generation

```yaml
rebase_guidance:
  analysis_steps:
    1: "Identify WIP and fixup commits"
    2: "Group related commits"
    3: "Order logically (foundation first)"
    4: "Generate rebase script"

  commands:
    pick: "Keep commit as-is"
    reword: "Keep changes, edit message"
    squash: "Combine with previous, keep message"
    fixup: "Combine with previous, discard message"
    drop: "Remove commit entirely"

  script_template: |
# ...
```

### Squash Recommendations

```yaml
squash_patterns:
  should_squash:
    - WIP commits into feature commits
    - "fix typo" into parent commit
    - "forgot to add" into parent
    - Multiple small fixes into one fix

  should_not_squash:
    - Independent features
    - Logically separate fixes
    - Changes by different authors
    - Changes to different modules
```

> **Advanced squash analysis**: Pairwise scoring engine, group detection, message synthesis, and sequence optimization → `references/squash-optimization.md`

### Interactive Rebase Script Template

```bash
# Interactive rebase — review and edit the todo list before execution
git rebase -i $(git merge-base HEAD main)

# Example todo list (generated by Guardian):
# pick abc1234 feat(auth): add OAuth2 provider integration
# fixup def5678 WIP: oauth progress
# fixup ghi9012 fix typo in oauth config
# pick jkl3456 test(auth): add OAuth2 integration tests
# reword mno7890 update docs  →  docs(auth): update OAuth2 setup guide
```

### Non-Interactive Alternative (Soft Reset)

For environments where `git rebase -i` is unavailable or impractical:

```bash
# 1. Create backup
git branch backup/pre-squash

# 2. Soft reset to merge-base (keeps all changes staged)
git reset --soft $(git merge-base HEAD main)

# 3. Re-commit in optimal structure
git add src/auth/oauth.ts src/auth/types.ts
git commit -m "feat(auth): add OAuth2 provider integration"

git add tests/auth/
git commit -m "test(auth): add OAuth2 integration tests"

git add docs/
git commit -m "docs(auth): update OAuth2 setup guide"

# 4. Verify diff integrity
git diff backup/pre-squash..HEAD  # Should be empty
```

---

## Report Templates

### Individual Commit Report

```markdown
## Commit Analysis: {hash}

**Subject:** `{subject}`
**Author:** {author}
**Files:** {file_count}

### Score: {score}/100

| Component | Score | Max | Notes |
|-----------|-------|-----|-------|
| Type prefix | {type_score} | 15 | {type_note} |
| Scope | {scope_score} | 10 | {scope_note} |
| Subject | {subject_score} | 15 | {subject_note} |
| Body | {body_score} | 5 | {body_note} |
| Footer | {footer_score} | 5 | {footer_note} |
...
```
{suggested_message}
```
```

### Branch Commit Summary

```markdown
## Commit Message Analysis

**Branch:** `{branch}`
**Commits:** {count}
**Overall Score:** {avg_score}/100

### Commit Scores
| Hash | Subject | Score | Issues |
|------|---------|-------|--------|
{commit_rows}

### Distribution
```
Excellent (90-100): {excellent_count} ████
Good (70-89):       {good_count}      ██████
Fair (50-69):       {fair_count}      ███
Poor (0-49):        {poor_count}      █
```

### Common Issues
{common_issues_list}

### Recommended Rebase Plan
```bash
{rebase_script}
```
```

---

## Integration with AUTORUN

```yaml
autorun_commit_analysis:
  auto_execute:
    - Analyze all commit messages
    - Calculate individual and aggregate scores
    - Generate improvement suggestions
    - Propose rebase plan if needed

  pause_conditions:
    - avg_score < 40
    - wip_commits > 3
    - Rebase recommended

  output_format:
    _STEP_COMPLETE:
      Agent: Guardian
# ...
```

---

## Project Convention Learning

Guardian learns project-specific conventions:

```yaml
convention_learning:
  analyze:
    - Last 100 commits
    - Merged PR commits
    - Release commits

  detect:
    type_frequency:
      feat: 35%
      fix: 28%
      chore: 15%
      refactor: 12%
      other: 10%

    scope_patterns:
# ...
```
