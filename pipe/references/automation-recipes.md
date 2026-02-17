# Automation Recipes

PR/Issue automation, branch protection, merge queues, environment protection, and release automation patterns.

---

## PR Automation

### Auto-Labeler

```yaml
# .github/workflows/labeler.yml
name: Labeler

on:
  pull_request:
    types: [opened, synchronize]

permissions:
  contents: read
  pull-requests: write

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/labeler@v5
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
```

```yaml
# .github/labeler.yml (label rules)
frontend:
  - changed-files:
      - any-glob-to-any-file: ['src/components/**', 'src/pages/**', '*.css', '*.scss']

backend:
  - changed-files:
      - any-glob-to-any-file: ['src/api/**', 'src/server/**', 'src/db/**']

docs:
  - changed-files:
      - any-glob-to-any-file: ['docs/**', '*.md', '!CHANGELOG.md']

ci:
  - changed-files:
      - any-glob-to-any-file: ['.github/**']

dependencies:
  - changed-files:
      - any-glob-to-any-file: ['package.json', 'pnpm-lock.yaml', '**/package.json']

tests:
  - changed-files:
      - any-glob-to-any-file: ['**/*.test.*', '**/*.spec.*', '__tests__/**']
```

### PR Size Check

```yaml
# .github/workflows/pr-size.yml
name: PR Size Check

on:
  pull_request:
    types: [opened, synchronize]

permissions:
  pull-requests: write

jobs:
  size:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Check PR Size
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          ADDITIONS=$(gh pr view ${{ github.event.pull_request.number }} --json additions -q '.additions')
          DELETIONS=$(gh pr view ${{ github.event.pull_request.number }} --json deletions -q '.deletions')
          TOTAL=$((ADDITIONS + DELETIONS))

          if [ "$TOTAL" -gt 500 ]; then
            gh pr comment ${{ github.event.pull_request.number }} \
              --body "## Large PR Warning
          This PR has **${TOTAL} changed lines** (${ADDITIONS}+ / ${DELETIONS}-).
          Consider splitting into smaller PRs for easier review."
            gh pr edit ${{ github.event.pull_request.number }} --add-label "size/large"
          elif [ "$TOTAL" -gt 200 ]; then
            gh pr edit ${{ github.event.pull_request.number }} --add-label "size/medium"
          else
            gh pr edit ${{ github.event.pull_request.number }} --add-label "size/small"
          fi
```

### Auto-Assign Reviewers

```yaml
# .github/workflows/auto-assign.yml
name: Auto Assign

on:
  pull_request:
    types: [opened, ready_for_review]

permissions:
  pull-requests: write

jobs:
  assign:
    if: "!github.event.pull_request.draft"
    runs-on: ubuntu-latest
    steps:
      - uses: kentaro-m/auto-assign-action@v2
        with:
          configuration-path: '.github/auto-assign.yml'
```

```yaml
# .github/auto-assign.yml
addReviewers: true
addAssignees: author
numberOfReviewers: 2
reviewers:
  - team-lead
  - senior-dev-1
  - senior-dev-2
filterLabels:
  exclude:
    - wip
    - draft
```

### Dependabot Auto-Merge

```yaml
# .github/workflows/dependabot-merge.yml
name: Dependabot Auto-Merge

on:
  pull_request:
    types: [opened, synchronize]

permissions:
  contents: write
  pull-requests: write

jobs:
  auto-merge:
    if: github.actor == 'dependabot[bot]'
    runs-on: ubuntu-latest
    steps:
      - uses: dependabot/fetch-metadata@v2
        id: metadata

      - name: Auto-merge patch/minor updates
        if: steps.metadata.outputs.update-type != 'version-update:semver-major'
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh pr review "${{ github.event.pull_request.number }}" --approve
          gh pr merge "${{ github.event.pull_request.number }}" --auto --squash
```

---

## Issue Automation

### Issue Templates

```yaml
# .github/ISSUE_TEMPLATE/bug_report.yml
name: Bug Report
description: File a bug report
title: "[Bug]: "
labels: ["bug", "triage"]
assignees: []

body:
  - type: markdown
    attributes:
      value: "Thanks for taking the time to fill out this bug report!"

  - type: textarea
    id: description
    attributes:
      label: What happened?
      description: A clear description of the bug
      placeholder: Tell us what happened
    validations:
      required: true

  - type: textarea
    id: reproduction
    attributes:
      label: Steps to reproduce
      description: How can we reproduce the issue?
      value: |
        1. Go to '...'
        2. Click on '...'
        3. See error
    validations:
      required: true

  - type: dropdown
    id: severity
    attributes:
      label: Severity
      options:
        - Critical (app crash, data loss)
        - High (feature broken, no workaround)
        - Medium (feature broken, workaround exists)
        - Low (cosmetic, minor inconvenience)
    validations:
      required: true

  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: Browser, OS, version, etc.
      placeholder: "Chrome 120, macOS 14, Node 20"
```

### Stale Issues/PRs

```yaml
# .github/workflows/stale.yml
name: Stale

on:
  schedule:
    - cron: '0 0 * * *'  # Daily

permissions:
  issues: write
  pull-requests: write

jobs:
  stale:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/stale@v9
        with:
          stale-issue-message: 'This issue has been inactive for 30 days. It will be closed in 7 days unless there is new activity.'
          stale-pr-message: 'This PR has been inactive for 14 days. It will be closed in 7 days unless there is new activity.'
          stale-issue-label: 'stale'
          stale-pr-label: 'stale'
          days-before-stale: 30
          days-before-close: 7
          days-before-pr-stale: 14
          days-before-pr-close: 7
          exempt-issue-labels: 'pinned,security,roadmap'
          exempt-pr-labels: 'pinned,security'
```

---

## Branch Protection

### Recommended Configuration

| Setting | Value | Reason |
|---------|-------|--------|
| Require PR before merging | Yes | Prevent direct pushes |
| Required approvals | 1-2 | Code review enforcement |
| Dismiss stale reviews | Yes | Re-review after force push |
| Require status checks | Yes | CI must pass |
| Require branches up-to-date | Yes | Prevent merge conflicts |
| Require conversation resolution | Yes | All comments addressed |
| Require signed commits | Optional | Commit verification |
| Allow force pushes | No | Protect history |
| Allow deletions | No | Protect main branch |

### Required Status Checks

Configure which workflow jobs must pass before merging:

```
Required checks:
  ✓ lint
  ✓ test
  ✓ build
  ✓ security-scan
```

**Important:** Job names must match exactly. If using reusable workflows, the check name format is `<caller-job-name> / <reusable-job-name>`.

### CODEOWNERS

```
# .github/CODEOWNERS

# Default owners for everything
* @team-lead @senior-dev

# Frontend specialists
src/components/** @frontend-team
src/pages/** @frontend-team

# Backend specialists
src/api/** @backend-team
src/db/** @backend-team

# DevOps
.github/** @devops-team
Dockerfile @devops-team
docker-compose.yml @devops-team

# Security-sensitive files
src/auth/** @security-team @team-lead
.env.example @security-team
```

### Pattern-Based Protection (Rulesets)

GitHub Rulesets (newer) support regex-based branch targeting:

```
# Protect all release branches
Pattern: release/**
Rules:
  - Require PR
  - Require 2 approvals
  - Require status checks: [ci, security]
  - No force push
  - No deletion
```

---

## Merge Queue

### Setup

1. Enable merge queue in repository settings
2. Configure merge method (squash recommended)
3. Set up `merge_group` event in CI workflows

### CI Workflow for Merge Queue

```yaml
on:
  pull_request:
    branches: [main]
  merge_group:
    types: [checks_requested]

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint && pnpm test && pnpm build
```

### Configuration Options

| Setting | Default | Description |
|---------|---------|-------------|
| Merge method | Merge | merge / rebase / squash |
| Build concurrency | 5 | Max PRs building simultaneously |
| Min group size | 1 | Wait for N PRs before building |
| Max group size | 5 | Max PRs in a single group |
| Status check timeout | 60 min | Cancel if checks don't complete |
| Only merge non-failing | Yes | Remove failing PRs from queue |

### How It Works

```
PR #1 added to queue
PR #2 added to queue
├── Group 1: main + PR#1 + PR#2 → CI runs
│   ├── Pass → Merge both
│   └── Fail → Bisect
│       ├── main + PR#1 → CI runs
│       │   ├── Pass → Merge PR#1, requeue PR#2
│       │   └── Fail → Remove PR#1 from queue
│       └── main + PR#2 → CI runs
```

---

## Environment Protection

### Environment Configuration

```yaml
# In workflow
jobs:
  deploy-staging:
    environment: staging
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying to staging"

  deploy-production:
    needs: deploy-staging
    environment:
      name: production
      url: https://myapp.com
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying to production"
```

### Protection Rules

| Rule | Setting | Effect |
|------|---------|--------|
| Required reviewers | 1-6 people/teams | Manual approval before deploy |
| Wait timer | 0-43200 min | Delay before deployment starts |
| Branch restriction | main only | Only specific branches can deploy |
| Custom rules | External checks | Datadog, PagerDuty, etc. |
| Self-review prevention | Enabled | PR author cannot approve deploy |

### Secret Hierarchy

```
Organization secrets → Available to all repos
  └── Repository secrets → Available to all environments
       └── Environment secrets → Available to specific environment only
```

**Precedence:** Environment > Repository > Organization (most specific wins).

### Custom Protection Rules (External)

```yaml
# Example: Require Datadog check before production deploy
# Configured in environment settings → Custom deployment protection rules
# Uses GitHub App webhook to verify external conditions
```

---

## Release Automation

### Tag-Based Release

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags: ['v[0-9]+.[0-9]+.[0-9]+']

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate Release Notes
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          PREV_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")
          if [ -n "$PREV_TAG" ]; then
            gh release create ${{ github.ref_name }} \
              --generate-notes \
              --notes-start-tag "$PREV_TAG" \
              --title "Release ${{ github.ref_name }}"
          else
            gh release create ${{ github.ref_name }} \
              --generate-notes \
              --title "Release ${{ github.ref_name }}"
          fi
```

### Semantic Release

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches: [main]

permissions:
  contents: write
  issues: write
  pull-requests: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          persist-credentials: false

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - name: Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
        run: npx semantic-release
```

### Docker Image Release

```yaml
# .github/workflows/docker-release.yml
name: Docker Release

on:
  release:
    types: [published]

permissions:
  contents: read
  packages: write

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/metadata-action@v5
        id: meta
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=semver,pattern={{major}}

      - uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

## Preview Environments

### Vercel Preview per PR

```yaml
# .github/workflows/preview.yml
name: Preview Deploy

on:
  pull_request:
    types: [opened, synchronize]

permissions:
  pull-requests: write

jobs:
  preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Vercel Preview
        id: deploy
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          # No --prod flag = preview deployment

      - name: Comment Preview URL
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## Preview Deployment
            | Status | URL |
            |--------|-----|
            | Ready | ${{ steps.deploy.outputs.preview-url }} |`
            });
```

### Cleanup Preview on PR Close

```yaml
on:
  pull_request:
    types: [closed]

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: Delete preview environment
        run: |
          # Provider-specific cleanup
          echo "Cleaning up preview for PR #${{ github.event.pull_request.number }}"
```

---

## Notification Patterns

### Slack Notification on Failure

```yaml
- name: Notify Slack
  if: failure()
  uses: slackapi/slack-github-action@v2
  with:
    webhook: ${{ secrets.SLACK_WEBHOOK_URL }}
    webhook-type: incoming-webhook
    payload: |
      {
        "text": "CI Failed: ${{ github.repository }} (${{ github.ref_name }})",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*CI Failed* :x:\n*Repo:* ${{ github.repository }}\n*Branch:* ${{ github.ref_name }}\n*Commit:* ${{ github.sha }}\n<${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|View Run>"
            }
          }
        ]
      }
```

### PR Comment with Results

```yaml
- uses: actions/github-script@v7
  if: github.event_name == 'pull_request'
  with:
    script: |
      const body = `## CI Results
      | Check | Status |
      |-------|--------|
      | Lint | ${{ needs.lint.result == 'success' && '✅' || '❌' }} |
      | Test | ${{ needs.test.result == 'success' && '✅' || '❌' }} |
      | Build | ${{ needs.build.result == 'success' && '✅' || '❌' }} |`;

      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body
      });
```
