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
    correct_type: 15
    approximate_type: 10
    missing_type: 0
    wrong_type: -5

  detection:
    patterns:
      feat: ["add", "implement", "introduce", "new"]
      fix: ["fix", "resolve", "correct", "patch"]
      docs: ["document", "readme", "comment"]
      refactor: ["refactor", "restructure", "reorganize"]
      test: ["test", "spec", "coverage"]
      chore: ["update", "upgrade", "bump", "deps"]
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
    check_against:
      - Directory names in changes
      - Module names in project
      - Common component names
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

  quality_indicators:
    excellent:
      - Imperative mood ("add", "fix", "update")
      - Specific action described
      - Concise but complete
      - No filler words

    poor:
      - Past tense ("added", "fixed")
      - Vague ("update code", "fix stuff")
      - Too long (>72 chars)
      - Ends with period
      - Starts with capital

  vague_subject_patterns:
    - "fix bug"
    - "update code"
    - "changes"
    - "improvements"
    - "misc"
    - "stuff"
    - "wip"
    - "temp"
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

  quality_indicators:
    excellent:
      - Explains motivation
      - Describes approach chosen
      - Notes alternatives considered
      - Mentions trade-offs

    poor:
      - Repeats the subject
      - Describes obvious changes
      - Too terse for complexity
      - Missing for complex change

  wrap_rule: 72_characters
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
      pattern: "Co-authored-by: Name <email>"
      score: 1

  scoring:
    has_reference_when_needed: 5
    has_breaking_change_note: 5
    missing_reference: 0
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
      - Related files only
      - Single concern addressed

    non_atomic_indicators:
      - Mixed feature and fix
      - Unrelated files changed
      - Multiple concerns in one commit
      - "While I was here" changes
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
      - Empty or single-word subject
      - "fixup" or "squash" markers

    recommendation: "Squash before merge"

  fixup_detection:
    patterns:
      - "fix typo"
      - "oops"
      - "forgot to add"
      - "missing file"
    recommendation: "Squash into relevant commit"
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

  missing_context:
    before: "fix null check"
    after: |
      fix(api): handle null response from payment provider

      The payment provider occasionally returns null on timeout.
      Added defensive check and retry logic.

      Fixes #456
    improvement: "Added body explaining context and issue reference"
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

  redundant_words:
    issue: "Subject contains filler"
    fix: "Remove 'this commit', 'changes', etc."
    example:
      before: "this commit adds user login"
      after: "add user login"

  scope_mismatch:
    issue: "Scope doesn't match changes"
    fix: "Use scope from main changed directory"
    example:
      before: "feat(api): update login component"
      after: "feat(auth): update login component"
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
    # Rebase plan for {branch}
    # {total_commits} commits → {target_commits} commits

    pick {hash1} feat(auth): add OAuth2 provider
    squash {hash2} WIP oauth
    squash {hash3} fix typo
    reword {hash4} fix stuff  # → fix(auth): resolve token refresh
    pick {hash5} test(auth): add OAuth tests

    # Expected result:
    # 1. feat(auth): add OAuth2 provider
    # 2. test(auth): add OAuth tests
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
| Atomicity | {atom_score} | 30 | {atom_note} |
| Consistency | {cons_score} | 20 | {cons_note} |

### Issues
{issues_list}

### Suggested Rewrite
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
      Status: SUCCESS
      Output:
        commit_analysis:
          count: 5
          avg_score: 72
          wip_count: 1
          rebase_needed: true
          rebase_plan: |
            pick a1b2c3 feat(auth): add OAuth2
            squash d4e5f6 WIP
            reword g7h8i9 fix stuff
          improvements:
            - "Squash WIP commit"
            - "Reword 'fix stuff' to specific message"
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
      - auth (18%)
      - api (15%)
      - ui (12%)
      - core (10%)

    message_style:
      format: "conventional"
      case: "lowercase"
      max_length: 65  # Project average
      body_frequency: 40%

  apply:
    - Validate against detected conventions
    - Suggest project-aligned improvements
    - Flag deviations from team norms
```
