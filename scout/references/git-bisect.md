# Scout Git Bisect Reference

Use git bisect to efficiently find the commit that introduced a bug.

## Basic Bisect Workflow

```bash
# Start bisect session
git bisect start

# Mark current (broken) commit as bad
git bisect bad

# Mark known good commit (when it worked)
git bisect good <commit-hash>

# Git will checkout a commit in between
# Test the bug, then mark as good or bad
git bisect good  # if bug is NOT present
git bisect bad   # if bug IS present

# Repeat until Git finds the culprit
# Git will output: "first bad commit is..."

# End bisect session
git bisect reset
```

---

## Finding the Good Commit

```bash
# Check recent commits
git log --oneline -20

# Check commits from specific date
git log --oneline --since="2024-01-01" --until="2024-01-15"

# Check commits by author
git log --oneline --author="name"

# Check last known working release
git tag --list
```

---

## Automated Bisect (with test script)

```bash
# Create test script that exits 0 (good) or 1 (bad)
cat > test-bug.sh << 'EOF'
#!/bin/bash
npm install --silent
npm run build --silent
# Run specific test that catches the bug
npm test -- --grep "specific test" --silent
EOF

chmod +x test-bug.sh

# Run automated bisect
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
git bisect run ./test-bug.sh
```

---

## Handling Complex Cases

### Skip untestable commits
```bash
git bisect skip  # Skip current commit (won't build, etc.)
```

### Bisect with path filter
```bash
# Only consider commits touching specific files
git bisect start -- src/components/
```

### Save and restore session
```bash
git bisect log > bisect-log.txt  # Save progress
git bisect replay bisect-log.txt # Restore later
```

---

## Bisect Best Practices

### Before starting
- Ensure you can reliably reproduce the bug
- Have a quick test to verify bug presence
- Stash or commit any local changes

### During bisect
- Keep notes on what you're testing
- If a commit won't build, use `git bisect skip`
- Test the SAME way each time

### After finding culprit
- Verify by checking out that commit
- Review the diff carefully
- Check if it was a direct cause or exposed existing bug

---

## Bisect Workflow Diagram

```
Known Good                              Known Bad
    │                                       │
    └──────────┬────────┬────────┬─────────┘
               │        │        │
         Test midpoint commit
               │
    ┌──────────┴──────────┐
    │                     │
  Good?                 Bad?
    │                     │
Search right half   Search left half
    │                     │
    └─────────┬───────────┘
              │
        Repeat until
        single commit
              │
         Found culprit!
```

---

## Common Bisect Scenarios

| Scenario | Approach |
|----------|----------|
| Bug in last week | `git bisect good HEAD~20` |
| Bug after release | `git bisect good v1.0.0` |
| Bug in specific file | `git bisect start -- src/file.ts` |
| Build failures | Use `git bisect skip` |
| Complex test | Create automated script |

---

## Bisect Output Example

```
$ git bisect bad
$ git bisect good abc1234
Bisecting: 15 revisions left to test after this (roughly 4 steps)
[def5678...] Fix: update validation logic

$ git bisect good
Bisecting: 7 revisions left to test after this (roughly 3 steps)
...

$ git bisect bad
ghi9012... is the first bad commit
commit ghi9012...
Author: Developer <dev@example.com>
Date:   Mon Jan 15 10:30:00 2024

    refactor: change data processing order
```
