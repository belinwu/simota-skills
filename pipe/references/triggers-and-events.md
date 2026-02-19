# Triggers and Events

Comprehensive knowledge base for GitHub Actions event types, filtering, and trigger design patterns.

---

## Event Classification

### Code Events

| Event | Trigger | Key Activity Types | Notes |
|-------|---------|-------------------|-------|
| `push` | Branch/tag push | — | Most common CI trigger |
| `pull_request` | PR lifecycle | `opened`, `synchronize`, `reopened`, `closed`, `labeled`, `unlabeled`, `ready_for_review`, `converted_to_draft` | Safe for forks (read-only) |
| `pull_request_target` | PR targeting base | Same as `pull_request` | **Runs in base context — dangerous with fork code** |
| `merge_group` | Merge queue check | `checks_requested` | For merge queue CI |
| `create` | Branch/tag creation | — | |
| `delete` | Branch/tag deletion | — | |

### Repository Events

| Event | Trigger | Key Activity Types |
|-------|---------|-------------------|
| `issues` | Issue lifecycle | `opened`, `edited`, `deleted`, `labeled`, `assigned`, `closed` |
| `issue_comment` | Issue/PR comment | `created`, `edited`, `deleted` |
| `release` | Release lifecycle | `published`, `created`, `prereleased`, `released` |
| `discussion` | Discussion lifecycle | `created`, `answered`, `labeled` |

### Workflow Events

| Event | Trigger | Notes |
|-------|---------|-------|
| `workflow_dispatch` | Manual trigger | Supports input parameters (max 10) |
| `repository_dispatch` | API trigger | Custom event types + client_payload |
| `workflow_run` | Workflow completion | Chain workflows together |
| `workflow_call` | Reusable workflow | Called by other workflows |
| `schedule` | Cron schedule | UTC only, default branch only |

### External Events

| Event | Trigger | Notes |
|-------|---------|-------|
| `deployment` | Deployment created | |
| `deployment_status` | Deployment status change | |
| `registry_package` | Package published/updated | |
| `watch` | Star added | `started` activity type only |

---

## Filtering

### Branch and Tag Filters

```yaml
# Include specific branches
on:
  push:
    branches:
      - main
      - 'release/**'
      - '!release/**-alpha'  # Negate pattern

# Exclude branches
on:
  push:
    branches-ignore:
      - 'dependabot/**'
      - 'renovate/**'

# ...
```

**Rule:** `branches` and `branches-ignore` cannot be used together for the same event. Same for `tags`/`tags-ignore`. Use negation patterns (`!`) within `branches` instead.

### Path Filters

```yaml
# Run only when specific paths change
on:
  push:
    paths:
      - 'src/**'
      - 'package.json'
      - '!src/**/*.test.ts'  # Exclude test files

# Ignore paths
on:
  pull_request:
    paths-ignore:
      - 'docs/**'
      - '*.md'
      - '.github/**'
```

**Rule:** `paths` and `paths-ignore` cannot be used together. Use negation patterns within `paths`.

**Limitation:** Path filters apply at the workflow level only. For job-level path filtering, use `dorny/paths-filter` (see `advanced-patterns.md`).

### Activity Type Filters

```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened]  # Default types
  issues:
    types: [opened, labeled]
  release:
    types: [published]  # Most common for CD
```

**Default `pull_request` types:** `opened`, `synchronize`, `reopened`. Add `labeled` for label-triggered workflows.

### Combined Filters

```yaml
on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'package.json'
  pull_request:
    branches: [main]
    paths:
      - 'src/**'
      - 'package.json'
    types: [opened, synchronize, reopened]
```

**Behavior:** For `push`, ALL filters must match (AND logic). Branch AND path must both match.

---

## workflow_dispatch (Manual Trigger)

### Input Types

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deploy target environment'
        required: true
        type: choice
        options:
          - development
          - staging
          - production
        default: 'staging'

      dry_run:
        description: 'Perform dry run without actual deployment'
# ...
```

### Input Types Reference

| Type | Values | `github.event.inputs.*` | `inputs.*` |
|------|--------|------------------------|------------|
| `string` | Free text | String | String |
| `boolean` | true/false | **String** (`"true"`/`"false"`) | **Boolean** |
| `choice` | Predefined options | String | String |
| `number` | Numeric | **String** | **Number** |
| `environment` | Repo environments | String | String |

**Critical:** `github.event.inputs.*` converts ALL types to strings. Use `inputs.*` in reusable workflows for proper type preservation. For boolean in regular workflows: `github.event.inputs.dry_run == 'true'` (string comparison).

### Constraints

- Maximum **10** input parameters per workflow
- Maximum **65,535** characters total for input values
- `environment` type integrates with Environment Protection Rules

### Pattern: Parameterized Deploy

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - uses: actions/checkout@v4

      - name: Deploy
        if: inputs.dry_run == false
        run: |
          echo "Deploying ${{ inputs.version }} to ${{ inputs.environment }}"
          # deployment commands here

      - name: Dry Run
        if: inputs.dry_run == true
# ...
```

---

## repository_dispatch (API Trigger)

### Setup

```yaml
on:
  repository_dispatch:
    types: [deploy, rollback, sync-data]
```

### Triggering via API

```bash
# Using gh CLI
gh api repos/{owner}/{repo}/dispatches \
  -f event_type="deploy" \
  -f client_payload='{"environment":"production","version":"v1.2.3","ref":"main"}'

# Using curl
curl -X POST \
  -H "Authorization: token $PAT" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/{owner}/{repo}/dispatches \
  -d '{"event_type":"deploy","client_payload":{"env":"prod"}}'
```

### Accessing Payload

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: |
          echo "Environment: ${{ github.event.client_payload.environment }}"
          echo "Version: ${{ github.event.client_payload.version }}"
```

### Use Cases

- Cross-repository triggers (repo A completes → trigger repo B)
- External service webhooks (Slack command → deploy)
- Scheduled complex workflows (external scheduler → dispatch)

**Requirement:** Requires PAT or GitHub App token (GITHUB_TOKEN cannot trigger repository_dispatch).

---

## workflow_run (Workflow Chaining)

### Basic Chain

```yaml
# workflow-b.yml — runs after workflow-a completes
on:
  workflow_run:
    workflows: ["CI"]  # Name of the triggering workflow
    types: [completed]
    branches: [main]
```

### Conditional on Conclusion

```yaml
jobs:
  deploy:
    if: github.event.workflow_run.conclusion == 'success'
    runs-on: ubuntu-latest
    steps:
      - run: echo "CI passed, deploying..."
```

### Multi-Stage Chain

```
CI (push) → Deploy Staging (workflow_run) → Integration Tests (workflow_run)
```

```yaml
# deploy-staging.yml
on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]
    branches: [main]

jobs:
  deploy:
    if: github.event.workflow_run.conclusion == 'success'
    # ...

# integration-tests.yml
on:
  workflow_run:
# ...
```

### Accessing Triggering Workflow Artifacts

```yaml
jobs:
  process:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: build-output
          run-id: ${{ github.event.workflow_run.id }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Anti-Patterns

| Pattern | Risk | Mitigation |
|---------|------|------------|
| Circular chain (A → B → A) | Infinite loop | Always filter on `conclusion: success` + different branches |
| Deep chains (4+ levels) | Debug difficulty | Keep max 3 levels, combine with `needs:` where possible |
| No conclusion filter | Runs on failure too | Always add `if: github.event.workflow_run.conclusion == 'success'` |
| GITHUB_TOKEN chain trigger | Won't trigger next workflow | Use PAT or GitHub App for chain triggers |

---

## schedule (Cron)

### Syntax

```yaml
on:
  schedule:
    - cron: '30 5 * * 1'   # Monday 5:30 UTC (14:30 JST)
    - cron: '0 0 * * *'    # Daily midnight UTC (9:00 JST)
    - cron: '0 */6 * * *'  # Every 6 hours
```

### Cron Field Reference

```
┌───────── minute (0-59)
│ ┌───────── hour (0-23)
│ │ ┌───────── day of month (1-31)
│ │ │ ┌───────── month (1-12)
│ │ │ │ ┌───────── day of week (0-6, Sunday=0)
│ │ │ │ │
* * * * *
```

### Important Constraints

1. **UTC only** — All times are UTC. JST = UTC+9.
2. **Default branch only** — Scheduled workflows run only on the default branch.
3. **No execution guarantee** — During high load, scheduled runs may be delayed or skipped. GitHub guarantees "best effort."
4. **Minimum interval** — 5 minutes is the shortest practical interval (GitHub may throttle more frequent schedules).
5. **Auto-disable** — Scheduled workflows in repos with no activity for 60 days are automatically disabled.

### Pattern: Stale Check + Dependency Audit

```yaml
on:
  schedule:
    - cron: '0 1 * * 1'  # Weekly Monday 1:00 UTC

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pnpm audit --audit-level=high
      - run: pnpm outdated || true
```

---

## GITHUB_TOKEN Trigger Limitations

### The Rule

Events triggered by `GITHUB_TOKEN` **do not** create new workflow runs. This prevents infinite loops but blocks certain patterns.

### Affected Scenarios

| Action via GITHUB_TOKEN | Triggers new workflow? |
|------------------------|----------------------|
| `git push` | **No** |
| Create release | **No** |
| Create/update PR | **No** |
| `workflow_dispatch` | **Yes** (exception) |
| `repository_dispatch` | **Yes** (exception) |

### Workarounds

1. **PAT (Personal Access Token)** — Use a PAT to push, which will trigger workflows.
2. **GitHub App** — Create a GitHub App and use its installation token.
3. **workflow_dispatch** — Explicitly dispatch target workflow.

```yaml
# Using PAT to trigger downstream workflows
- uses: actions/checkout@v4
  with:
    token: ${{ secrets.PAT_TOKEN }}  # Not GITHUB_TOKEN
- run: |
    git commit -m "chore: auto-update"
    git push  # This WILL trigger push-based workflows
```

**Security note:** PATs have broader scope than GITHUB_TOKEN. Prefer GitHub App tokens for production. Use fine-grained PATs when PAT is necessary.

---

## pull_request vs pull_request_target

### Security Model

| Aspect | `pull_request` | `pull_request_target` |
|--------|---------------|----------------------|
| Code context | **PR head** (fork code) | **Base branch** (trusted code) |
| Secrets access | **No** (forks) | **Yes** |
| GITHUB_TOKEN permissions | Read-only (forks) | Full (base config) |
| Safe for untrusted code? | **Yes** | **Dangerous if checkout PR code** |

### Safe Pattern: Label-Based Approval

```yaml
on:
  pull_request_target:
    types: [labeled]

jobs:
  deploy-preview:
    if: github.event.label.name == 'safe-to-test'
    runs-on: ubuntu-latest
    steps:
      # SAFE: checkout base branch code
      - uses: actions/checkout@v4

      # DANGEROUS: checkout PR code — only after label approval
      - uses: actions/checkout@v4
        with:
# ...
```

### Dangerous Anti-Pattern

```yaml
# NEVER DO THIS
on:
  pull_request_target:

jobs:
  build:
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.ref }}  # Checks out fork code
      - run: npm install && npm test  # Executes untrusted code with secrets!
```

### Decision Guide

| Scenario | Use |
|----------|-----|
| CI for all PRs (including forks) | `pull_request` |
| PR comment/label automation | `pull_request_target` (no PR code checkout) |
| Deploy previews for trusted PRs | `pull_request_target` + label gate |
| Anything running PR code | `pull_request` (never `pull_request_target`) |

---

## merge_group Event

### Setup

```yaml
on:
  merge_group:
    types: [checks_requested]

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pnpm install --frozen-lockfile
      - run: pnpm test
```

### How Merge Queue Works

1. PR added to merge queue
2. GitHub creates temporary branch: `gh-readonly-queue/{base}/{pr-sha}`
3. `merge_group` event fires with `checks_requested`
4. CI runs on the combined code (base + queued PRs)
5. If CI passes → merge. If CI fails → PR removed from queue.

### Integration with CI

```yaml
# Support both regular PR CI and merge queue
on:
  pull_request:
    branches: [main]
  merge_group:
    types: [checks_requested]
```

**Note:** Required status checks must match between PR and merge queue workflows. Use the same job names or configure separately in branch protection.

---

## Event Selection Decision Tree

```
What triggers your workflow?
├── Code change?
│   ├── Direct push → push (branches + paths filter)
│   ├── Pull request → pull_request (+ types filter)
│   ├── Merge queue → merge_group
│   └── Fork PR needing secrets → pull_request_target (with label gate)
├── Manual trigger?
│   ├── Same repo → workflow_dispatch (with inputs)
│   └── Cross-repo/external → repository_dispatch
├── After another workflow?
│   └── workflow_run (with conclusion filter)
├── Scheduled?
│   └── schedule (cron, UTC, default branch only)
├── Release?
│   └── release (types: [published])
...
```

---

## Common Patterns

### CI for Push + PR (Standard)

```yaml
on:
  push:
    branches: [main]
    paths-ignore: ['docs/**', '*.md']
  pull_request:
    branches: [main]
    paths-ignore: ['docs/**', '*.md']
```

### Release on Tag Push

```yaml
on:
  push:
    tags: ['v[0-9]+.[0-9]+.[0-9]+']
```

### Nightly Build

```yaml
on:
  schedule:
    - cron: '0 18 * * *'  # 3:00 JST daily
  workflow_dispatch:  # Allow manual trigger too
```

### Multi-Event Workflow

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
    inputs:
      debug:
        type: boolean
        default: false
  schedule:
    - cron: '0 0 * * 1'  # Weekly
```

### PR Comment Trigger (ChatOps)

```yaml
on:
  issue_comment:
    types: [created]

jobs:
  deploy:
    if: |
      github.event.issue.pull_request &&
      contains(github.event.comment.body, '/deploy') &&
      github.event.comment.author_association == 'MEMBER'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying PR..."
```
