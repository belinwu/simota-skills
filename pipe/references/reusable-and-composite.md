# Reusable Workflows and Composite Actions

Design guide for DRY CI/CD pipelines using GitHub Actions reuse mechanisms.

---

## Reusable Workflows vs Composite Actions

### Comparison

| Aspect | Reusable Workflow | Composite Action |
|--------|-------------------|------------------|
| **Definition** | `.github/workflows/*.yml` | `.github/actions/*/action.yml` or separate repo |
| **Execution unit** | Entire workflow (jobs) | Steps within a job |
| **Runner** | Defined internally | Inherits from caller |
| **Trigger** | `workflow_call` | `uses:` in step |
| **Secrets** | `secrets: inherit` or explicit | Via `env:` from caller |
| **Nesting** | Up to 4 levels | Up to 10 levels |
| **Outputs** | Job-level outputs | Step-level outputs |
| **Visibility** | Same repo, org, or public | Same repo, org, or public |
| **SLSA** | Enables Level 3 | No SLSA benefit |
| **Environment secrets** | Supported (with `environment:`) | Supported (via caller) |

### When to Use Which

| Scenario | Choice | Reason |
|----------|--------|--------|
| Shared CI pipeline (lint → test → build) | **Reusable Workflow** | Controls full job graph |
| Shared setup steps (checkout + node + pnpm) | **Composite Action** | Reusable step sequence |
| Standardized deployment pipeline | **Reusable Workflow** | Environment protection, secrets |
| Cross-repo shared logic | **Either** | Reusable for pipelines, Composite for steps |
| Marketplace-publishable tool | **Composite Action** | Marketplace supports actions, not workflows |
| SLSA Level 3 provenance | **Reusable Workflow** | Required for L3 attestation |

### Decision Rule

- **3+ workflows share the same job structure** → Reusable Workflow
- **3+ jobs share the same setup steps** → Composite Action
- **1-2 occurrences** → Don't abstract. Copy is fine.

---

## Reusable Workflows

### Basic Pattern

```yaml
# .github/workflows/ci-reusable.yml (callee)
name: Reusable CI

on:
  workflow_call:
    inputs:
      node-version:
        type: string
        default: '20'
      run-e2e:
        type: boolean
        default: false
    secrets:
      NPM_TOKEN:
        required: false
    outputs:
      test-result:
        description: "Test result status"
        value: ${{ jobs.test.outputs.result }}

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint

  test:
    runs-on: ubuntu-latest
    outputs:
      result: ${{ steps.test.outputs.result }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - id: test
        run: |
          pnpm test
          echo "result=success" >> "$GITHUB_OUTPUT"

  build:
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm build
```

### Calling a Reusable Workflow

```yaml
# .github/workflows/ci.yml (caller)
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  ci:
    uses: ./.github/workflows/ci-reusable.yml
    with:
      node-version: '20'
      run-e2e: false
    secrets: inherit  # Pass all secrets

  notify:
    needs: ci
    if: failure()
    runs-on: ubuntu-latest
    steps:
      - run: echo "CI failed! Test result: ${{ needs.ci.outputs.test-result }}"
```

### Secret Handling

```yaml
# Option A: Inherit all secrets (simple)
jobs:
  ci:
    uses: ./.github/workflows/ci-reusable.yml
    secrets: inherit

# Option B: Explicit secrets (more secure)
jobs:
  ci:
    uses: ./.github/workflows/ci-reusable.yml
    secrets:
      NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
      DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
```

**Recommendation:** Use `secrets: inherit` for same-repo reusable workflows. Use explicit secrets for cross-repo workflows.

### Cross-Repository Usage

```yaml
jobs:
  ci:
    uses: my-org/.github/.github/workflows/ci-reusable.yml@main
    with:
      node-version: '20'
    secrets: inherit
```

**Requirements:**
- Reusable workflow must be in a public repo, OR
- Reusable workflow must be in the same org with Actions sharing enabled

### Nesting Limits

- Maximum **4 levels** of reusable workflow calls
- A reusable workflow can call another reusable workflow
- Circular calls are prohibited

### Output Propagation

```yaml
# Reusable workflow outputs
on:
  workflow_call:
    outputs:
      version:
        description: "Detected version"
        value: ${{ jobs.detect.outputs.version }}

jobs:
  detect:
    outputs:
      version: ${{ steps.v.outputs.version }}
    steps:
      - id: v
        run: echo "version=1.2.3" >> "$GITHUB_OUTPUT"

# Caller accesses output
jobs:
  ci:
    uses: ./.github/workflows/detect.yml
  deploy:
    needs: ci
    steps:
      - run: echo "Deploying version ${{ needs.ci.outputs.version }}"
```

---

## Composite Actions

### Basic Pattern

```yaml
# .github/actions/setup-node-pnpm/action.yml
name: 'Setup Node + pnpm'
description: 'Install Node.js and pnpm with caching'

inputs:
  node-version:
    description: 'Node.js version'
    default: '20'
    required: false
  install-deps:
    description: 'Run pnpm install'
    default: 'true'
    required: false

outputs:
  cache-hit:
    description: 'Whether cache was hit'
    value: ${{ steps.cache.outputs.cache-hit }}

runs:
  using: 'composite'
  steps:
    - uses: pnpm/action-setup@v4
      with:
        version: 9

    - uses: actions/setup-node@v4
      id: cache
      with:
        node-version: ${{ inputs.node-version }}
        cache: 'pnpm'

    - if: inputs.install-deps == 'true'
      shell: bash
      run: pnpm install --frozen-lockfile
```

### Usage

```yaml
# In any workflow
steps:
  - uses: actions/checkout@v4
  - uses: ./.github/actions/setup-node-pnpm
    with:
      node-version: '20'
  - run: pnpm test
```

### Important: `shell` is Required

Every `run:` step in a composite action **must** specify `shell:`:

```yaml
runs:
  using: 'composite'
  steps:
    - run: echo "Hello"
      shell: bash  # REQUIRED in composite actions
```

### Advanced: Multi-Step with Conditionals

```yaml
# .github/actions/build-and-test/action.yml
name: 'Build and Test'
description: 'Build the project and optionally run tests'

inputs:
  skip-tests:
    description: 'Skip test execution'
    default: 'false'
  coverage:
    description: 'Generate coverage report'
    default: 'false'

runs:
  using: 'composite'
  steps:
    - shell: bash
      run: pnpm build

    - if: inputs.skip-tests != 'true'
      shell: bash
      run: |
        if [ "${{ inputs.coverage }}" = "true" ]; then
          pnpm test --coverage
        else
          pnpm test
        fi

    - if: inputs.coverage == 'true'
      uses: actions/upload-artifact@v4
      with:
        name: coverage
        path: coverage/
```

---

## Action Types Comparison

| Type | Runtime | Platform | Speed | Use Case |
|------|---------|----------|-------|----------|
| **Composite** | Reuses existing actions + shell | All | Fast | Combining existing actions |
| **JavaScript** | Node.js | All | Fastest | Custom logic, API calls |
| **Docker** | Container | Linux only | Slower | Specific environment needs |

### When to Choose Each

- **Composite:** Default choice. Combines existing actions and shell commands.
- **JavaScript:** When you need complex logic, API interactions, or cross-platform support.
- **Docker:** When you need a specific runtime environment (e.g., specific Python version, system packages).

---

## Organization Workflow Templates

### Structure

```
org/.github/
├── workflow-templates/
│   ├── ci.yml
│   ├── ci.properties.json
│   ├── deploy.yml
│   └── deploy.properties.json
└── actions/
    └── setup-node-pnpm/
        └── action.yml
```

### Template Properties

```json
// workflow-templates/ci.properties.json
{
  "name": "Organization CI",
  "description": "Standard CI pipeline for all repositories",
  "iconName": "octicon rocket",
  "categories": ["JavaScript", "TypeScript"],
  "filePatterns": ["package.json"]
}
```

### Template Workflow

```yaml
# workflow-templates/ci.yml
name: CI

on:
  push:
    branches: [$default-branch]  # Replaced with repo's default branch
  pull_request:
    branches: [$default-branch]

jobs:
  ci:
    uses: my-org/.github/.github/workflows/ci-reusable.yml@main
    secrets: inherit
```

Members can select this template from Actions → New workflow → "Workflows created by my-org".

---

## DRY Patterns

### Pattern: Shared Setup → Composite Action

**Before (duplicated in every workflow):**

```yaml
# workflow-a.yml, workflow-b.yml, workflow-c.yml all have:
steps:
  - uses: actions/checkout@v4
  - uses: pnpm/action-setup@v4
    with:
      version: 9
  - uses: actions/setup-node@v4
    with:
      node-version: 20
      cache: 'pnpm'
  - run: pnpm install --frozen-lockfile
```

**After (extracted to composite):**

```yaml
# All workflows:
steps:
  - uses: actions/checkout@v4
  - uses: ./.github/actions/setup-node-pnpm
```

### Pattern: Shared Pipeline → Reusable Workflow

**Before (duplicated CI config):**

```yaml
# packages/api/ci.yml and packages/web/ci.yml both define lint/test/build jobs
```

**After (shared reusable + per-package caller):**

```yaml
# packages/api/ci.yml
jobs:
  ci:
    uses: ./.github/workflows/ci-reusable.yml
    with:
      working-directory: packages/api

# packages/web/ci.yml
jobs:
  ci:
    uses: ./.github/workflows/ci-reusable.yml
    with:
      working-directory: packages/web
```

### Anti-Pattern: Over-Abstraction

Don't create a composite action for a single step used in one place:

```yaml
# BAD: Unnecessary abstraction
- uses: ./.github/actions/run-lint  # Just wraps `pnpm lint`

# GOOD: Just run the command
- run: pnpm lint
```

**Rule of Three:** Extract to a shared action/workflow only when the same pattern appears in 3+ places.

---

## Versioning and Releases

### For Composite Actions in Separate Repos

```bash
# Tag-based versioning
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# Move major version tag (convention for actions)
git tag -fa v1 -m "Update v1 to v1.0.0"
git push origin v1 --force
```

### Usage with Versions

```yaml
# Using major version tag (auto-updates within major)
- uses: my-org/setup-action@v1

# Using exact version (pinned)
- uses: my-org/setup-action@v1.0.0

# Using SHA (most secure)
- uses: my-org/setup-action@abc123def456
```

### For In-Repo Actions

No versioning needed — they always use the current branch version:

```yaml
- uses: ./.github/actions/setup-node-pnpm  # Always current
```

---

## Testing Reusable Workflows

### Local Testing with `act`

```bash
# Test a specific workflow
act -W .github/workflows/ci.yml

# Test with specific event
act push -W .github/workflows/ci.yml

# Test with inputs
act workflow_dispatch -W .github/workflows/deploy.yml \
  --input environment=staging
```

### Workflow Dispatch for Manual Testing

```yaml
# Add workflow_dispatch to reusable workflows for direct testing
on:
  workflow_call:
    inputs:
      node-version:
        type: string
        default: '20'
  workflow_dispatch:  # Allows manual trigger for testing
    inputs:
      node-version:
        type: string
        default: '20'
```
