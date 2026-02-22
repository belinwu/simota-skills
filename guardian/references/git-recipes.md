# Guardian Git Command Recipes

> 頻出する Git / gh CLI コマンドのリファレンス。

---

## Analyze Changes

```bash
# View staged changes summary
git diff --cached --stat

# View all changes against target branch
git diff main...HEAD --stat

# Find large file changes
git diff main...HEAD --numstat | sort -k1 -rn | head -20

# List commits not in main
git log main..HEAD --oneline
```

---

## Interactive Commit Structuring

```bash
# Split staged changes interactively
git add -p

# Unstage specific files
git reset HEAD -- path/to/file

# Amend last commit (before push only)
git commit --amend

# Interactive rebase to restructure
git rebase -i HEAD~5
```

### Squash Analysis Commands

```bash
# List all commits from merge-base with stats
git log --oneline --stat $(git merge-base HEAD main)..HEAD

# Compact commit + file list for analysis
git log --format='%h %s' --name-only $(git merge-base HEAD main)..HEAD

# Detect WIP / noise commits
git log --oneline $(git merge-base HEAD main)..HEAD | \
  grep -iE '(^[a-f0-9]+ (WIP|wip|tmp|temp|fixup!|squash!|fix typo|forgot|oops|address review))'

# File overlap between adjacent commits (compare two commits)
comm -12 \
  <(git diff-tree --no-commit-id --name-only -r COMMIT_A | sort) \
  <(git diff-tree --no-commit-id --name-only -r COMMIT_B | sort)

# Verify each commit builds independently
git rebase -i --exec 'npm run build' $(git merge-base HEAD main)

# Verify each commit passes tests independently
git rebase -i --exec 'npm test' $(git merge-base HEAD main)
```

### Squash Backup & Restore

```bash
# Create backup branch before rebase
git branch backup/$(git branch --show-current)-pre-squash

# Restore from backup if squash goes wrong
git reset --hard backup/$(git branch --show-current)-pre-squash

# Verify diff integrity after squash (should output nothing)
git diff backup/$(git branch --show-current)-pre-squash..HEAD
```

### Co-authored-by Extraction & Verification

```bash
# Extract all unique authors from branch commits
git log --format='%an <%ae>' $(git merge-base HEAD main)..HEAD | sort -u

# Extract existing Co-authored-by lines from commit messages
git log --format='%B' $(git merge-base HEAD main)..HEAD | \
  grep -i '^Co-authored-by:' | sort -u

# Count unique contributors (authors + co-authors)
{
  git log --format='%an <%ae>' $(git merge-base HEAD main)..HEAD
  git log --format='%B' $(git merge-base HEAD main)..HEAD | \
    grep -i '^Co-authored-by:' | sed 's/Co-authored-by: //'
} | sort -u | wc -l
```

---

## Branch Operations

```bash
# Create branch with proper naming
git checkout -b feat/user-authentication

# Rename current branch
git branch -m old-name feat/new-name

# Delete merged branch
git branch -d feat/completed-feature
```

---

## PR Operations with gh CLI

> **Note**: PR body should follow best practices in SKILL.md Section 14.
> Key sections: Summary → Test plan → Changes.

```bash
# Create PR with generated description (file-based)
gh pr create --title "feat(auth): add OAuth2" --body-file pr-body.md

# Create PR with inline body using HEREDOC (recommended for automation)
gh pr create --title "feat(auth): add OAuth2 provider" --body "$(cat <<'EOF'
## Summary
- Add OAuth2 provider integration for Google and GitHub
- Implement token refresh mechanism with automatic retry

## Test plan
- [ ] Complete OAuth2 login flow with Google account
- [ ] Complete OAuth2 login flow with GitHub account
- [ ] Verify token refresh with expired access token

## Changes
- `src/auth/oauth.ts` - OAuth2 provider implementation
- `src/auth/providers/` - Google, GitHub provider configs

Closes #123
EOF
)"

# Minimal PR for small fixes
gh pr create --base main --title "fix(auth): resolve token refresh race condition" --body "$(cat <<'EOF'
## Summary
- Fix race condition that caused intermittent 401 errors during concurrent requests

## Test plan
- [ ] Trigger 10+ concurrent API calls with expired token
- [ ] Verify only one refresh request is made

Closes #456
EOF
)"

# View PR diff stats
gh pr diff 123 --stat

# List files changed in PR
gh pr view 123 --json files --jq '.files[].path'

# View PR details
gh pr view 123
```

---

## Hotspot Analysis Commands

```bash
# Most changed files in last 90 days
git log --since="90 days ago" --pretty=format: --name-only | \
  sort | uniq -c | sort -rn | head -20

# Files with most authors
git log --pretty=format:'%an' --name-only | \
  awk 'NF==1{author=$0} NF>1{print author, $0}' | \
  sort | uniq | cut -d' ' -f2- | sort | uniq -c | sort -rn

# Bug fix frequency per file
git log --oneline --all --grep="fix" -- . | wc -l
```

---

## Conflict Resolution

```bash
# View conflicting files
git diff --name-only --diff-filter=U

# Accept theirs (incoming) for specific file
git checkout --theirs path/to/file

# Accept ours (current) for specific file
git checkout --ours path/to/file

# After resolving, mark as resolved
git add path/to/resolved/file

# For lock files - regenerate
rm package-lock.json && npm install
```
