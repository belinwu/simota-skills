# Advanced Patterns

Monorepo CI, self-hosted runners, multi-platform builds, deployment pipelines, service containers, debugging, and expressions.

---

## Monorepo CI

### The Challenge

Built-in `paths` filters work at the **workflow level** only. You cannot conditionally skip individual jobs based on changed paths without additional tooling.

### dorny/paths-filter

Job-level and step-level conditional execution based on changed files.

```yaml
jobs:
  detect:
    runs-on: ubuntu-latest
    outputs:
      api: ${{ steps.filter.outputs.api }}
      web: ${{ steps.filter.outputs.web }}
      shared: ${{ steps.filter.outputs.shared }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            api:
              - 'packages/api/**'
              - 'packages/shared/**'
            web:
              - 'packages/web/**'
              - 'packages/shared/**'
            shared:
              - 'packages/shared/**'

  test-api:
    needs: detect
    if: needs.detect.outputs.api == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pnpm --filter api test

  test-web:
    needs: detect
    if: needs.detect.outputs.web == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pnpm --filter web test
```

### TurboRepo Integration

```yaml
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2  # Need parent commit for diff

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      # Only build/test packages that changed since last commit
      - run: pnpm turbo run build test --filter='[HEAD^1]'
```

### Required Checks + Path Filters Problem

**Problem:** If a required check is skipped (due to path filter), the PR is blocked because the check never reports a status.

**Solutions:**

```yaml
# Solution 1: Always-run job that reports success
jobs:
  detect:
    outputs:
      api: ${{ steps.filter.outputs.api }}
    steps:
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            api:
              - 'packages/api/**'

  test-api:
    needs: detect
    if: needs.detect.outputs.api == 'true'
    runs-on: ubuntu-latest
    steps:
      - run: pnpm --filter api test

  # This job always runs and is the required check
  ci-gate:
    needs: [detect, test-api]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - name: Check results
        run: |
          if [ "${{ needs.test-api.result }}" = "failure" ]; then
            exit 1
          fi
          echo "All required checks passed or were skipped"
```

```yaml
# Solution 2: Separate workflow per package with path filter
# packages/api/.github/workflows/ci.yml
on:
  pull_request:
    paths: ['packages/api/**', 'packages/shared/**']
```

---

## Self-Hosted Runners

### Actions Runner Controller (ARC)

Kubernetes-based auto-scaling for self-hosted runners.

```yaml
# runner-deployment.yaml (Kubernetes)
apiVersion: actions.summerwind.dev/v1alpha1
kind: RunnerDeployment
metadata:
  name: example-runner
spec:
  replicas: 3
  template:
    spec:
      repository: my-org/my-repo
      labels:
        - self-hosted
        - linux
        - x64
---
apiVersion: actions.summerwind.dev/v1alpha1
kind: HorizontalRunnerAutoscaler
metadata:
  name: example-autoscaler
spec:
  scaleTargetRef:
    name: example-runner
  minReplicas: 1
  maxReplicas: 10
  metrics:
    - type: PercentageRunnersBusy
      scaleUpThreshold: '0.75'
      scaleDownThreshold: '0.25'
      scaleUpFactor: '2'
      scaleDownFactor: '0.5'
```

### Ephemeral Runners

Create a fresh runner for each job, destroy after completion:

```yaml
# In workflow
runs-on: [self-hosted, ephemeral]
```

**Benefits:** No state leakage between jobs, clean environment, reduced security risk.

### Runner Groups and Labels

```yaml
# Use specific runner groups/labels
jobs:
  build:
    runs-on: [self-hosted, linux, gpu]  # GPU-enabled runner

  test:
    runs-on: [self-hosted, linux, x64]  # Standard runner

  ios:
    runs-on: [self-hosted, macOS, arm64]  # Apple Silicon runner
```

### Security Considerations

| Risk | Mitigation |
|------|------------|
| **Public repos:** Anyone can trigger workflows | Never use self-hosted runners for public repos |
| **Persistent state:** Previous job artifacts remain | Use ephemeral runners |
| **Network access:** Runner has LAN access | Isolate runners in dedicated VPC/subnet |
| **Privilege escalation:** Container breakout | Run as non-root, use rootless containers |
| **Supply chain:** Malicious workflow code | Restrict who can modify `.github/workflows/` |

### Custom Runner Images

```dockerfile
# Dockerfile for custom runner
FROM ghcr.io/actions/actions-runner:latest

# Install project-specific tools
RUN apt-get update && apt-get install -y \
    build-essential \
    chromium-browser \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate
```

---

## Multi-Platform Builds

### Docker Buildx + QEMU

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-qemu-action@v3

      - uses: docker/setup-buildx-action@v3

      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/build-push-action@v6
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ghcr.io/${{ github.repository }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Matrix OS Builds

```yaml
jobs:
  build:
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            target: linux-x64
          - os: macos-latest
            target: darwin-arm64
          - os: windows-latest
            target: win-x64
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - run: npm run build -- --target ${{ matrix.target }}
      - uses: actions/upload-artifact@v4
        with:
          name: binary-${{ matrix.target }}
          path: dist/
```

---

## Deployment Pipelines

### Staged Deployment

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pnpm install --frozen-lockfile && pnpm build
      - uses: actions/upload-artifact@v4
        with:
          name: build
          path: dist/

  deploy-staging:
    needs: build
    environment:
      name: staging
      url: https://staging.myapp.com
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: build
      - run: ./deploy.sh staging

  deploy-production:
    needs: deploy-staging
    environment:
      name: production
      url: https://myapp.com
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: build
      - run: ./deploy.sh production
```

### Blue-Green Deploy Pattern

```yaml
jobs:
  deploy:
    environment: production
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to inactive slot
        run: |
          ACTIVE=$(curl -s https://myapp.com/slot)
          INACTIVE=$([ "$ACTIVE" = "blue" ] && echo "green" || echo "blue")
          ./deploy.sh "$INACTIVE"

      - name: Health check
        run: |
          for i in {1..10}; do
            STATUS=$(curl -s -o /dev/null -w '%{http_code}' "https://${INACTIVE}.myapp.com/health")
            [ "$STATUS" = "200" ] && exit 0
            sleep 5
          done
          exit 1

      - name: Switch traffic
        run: ./switch-traffic.sh "$INACTIVE"

      - name: Rollback on failure
        if: failure()
        run: ./switch-traffic.sh "$ACTIVE"
```

### Rollback Workflow

```yaml
# .github/workflows/rollback.yml
name: Rollback

on:
  workflow_dispatch:
    inputs:
      environment:
        type: environment
        required: true
      version:
        type: string
        description: 'Version to rollback to'
        required: true

jobs:
  rollback:
    environment: ${{ inputs.environment }}
    runs-on: ubuntu-latest
    steps:
      - name: Rollback
        run: |
          echo "Rolling back ${{ inputs.environment }} to ${{ inputs.version }}"
          ./deploy.sh ${{ inputs.environment }} ${{ inputs.version }}
```

---

## Service Containers

### Database Testing

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    env:
      DATABASE_URL: postgresql://test:test@localhost:5432/testdb
      REDIS_URL: redis://localhost:6379

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm db:migrate
      - run: pnpm test:integration
```

### Container Job vs Runner Job

| Aspect | Container Job | Runner Job |
|--------|--------------|------------|
| Runs in | Docker container | Runner VM directly |
| Services | `localhost` hostname | `localhost` (mapped ports) |
| Performance | Slightly slower (container overhead) | Faster |
| Isolation | Better | Less |
| Use when | Need specific OS/tools | Standard builds |

```yaml
# Container job
jobs:
  test:
    runs-on: ubuntu-latest
    container:
      image: node:20-slim
    services:
      db:
        image: postgres:16
    # In container, service hostname is the service name, not localhost
    env:
      DATABASE_URL: postgresql://test:test@db:5432/testdb
```

---

## Debugging and Troubleshooting

### Enable Debug Logging

```yaml
# Method 1: Repository secret
# Set secret: ACTIONS_STEP_DEBUG = true

# Method 2: Re-run with debug
# Click "Re-run all jobs" → check "Enable debug logging"

# Method 3: In workflow
- name: Debug info
  run: |
    echo "Event: ${{ github.event_name }}"
    echo "Ref: ${{ github.ref }}"
    echo "SHA: ${{ github.sha }}"
    echo "Actor: ${{ github.actor }}"
    echo "Runner OS: ${{ runner.os }}"
    echo "Runner Arch: ${{ runner.arch }}"
```

### Local Testing with `act`

```bash
# Install
brew install act  # macOS
# or: curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | bash

# Run default event (push)
act

# Run specific event
act pull_request

# Run specific job
act -j test

# Run with specific workflow
act -W .github/workflows/ci.yml

# Run with inputs
act workflow_dispatch --input environment=staging

# List available workflows
act -l

# Dry run (show what would happen)
act -n

# Use specific runner image
act -P ubuntu-latest=catthehacker/ubuntu:act-latest
```

### Common `act` Limitations

| Limitation | Workaround |
|-----------|------------|
| No `services:` support | Use docker-compose alongside |
| No `cache` action | Set `ACT=true` env and skip cache steps |
| No OIDC | Mock with environment variables |
| No GitHub API (some) | Provide `GITHUB_TOKEN` via `.secrets` file |
| No `reusable workflows` | Inline the reusable workflow content |

### Common Error Patterns

| Error | Cause | Fix |
|-------|-------|-----|
| `Resource not accessible by integration` | Missing permissions | Add required `permissions:` |
| `No matching runner` | Wrong `runs-on` label | Check available runner labels |
| `Cache not found` | Key mismatch or first run | Verify `hashFiles()` path, check restore-keys |
| `Annotations limit exceeded` | Too many lint warnings | Filter to errors only in CI |
| `Job cancelled` | Concurrency group cancelled it | Check `cancel-in-progress` settings |
| `Deployment protection rules not satisfied` | Missing approval | Approve in environment settings |

### Runner Image Software

Check pre-installed software on GitHub-hosted runners:

```yaml
- name: Check installed software
  run: |
    node --version
    python3 --version
    docker --version
    # Full list: https://github.com/actions/runner-images
```

---

## Expressions, Contexts, and Conditions

### Key Contexts

| Context | Description | Example |
|---------|-------------|---------|
| `github` | Event/workflow info | `github.ref`, `github.sha`, `github.actor` |
| `env` | Environment variables | `env.MY_VAR` |
| `job` | Current job info | `job.status` |
| `steps` | Step outputs/status | `steps.my-step.outputs.value` |
| `needs` | Job dependency outputs | `needs.build.outputs.version` |
| `matrix` | Matrix values | `matrix.os`, `matrix.node` |
| `inputs` | Workflow inputs | `inputs.environment` |
| `secrets` | Secrets | `secrets.GITHUB_TOKEN` |
| `runner` | Runner info | `runner.os`, `runner.arch`, `runner.temp` |

### Conditional Patterns

```yaml
# Run on specific branch
if: github.ref == 'refs/heads/main'

# Run on tag
if: startsWith(github.ref, 'refs/tags/')

# Run on PR (not push)
if: github.event_name == 'pull_request'

# Run on specific actor
if: github.actor == 'dependabot[bot]'

# Combine conditions
if: |
  github.ref == 'refs/heads/main' &&
  github.event_name == 'push'

# Check label
if: contains(github.event.pull_request.labels.*.name, 'deploy')

# Check previous job result
if: always() && needs.test.result == 'success'

# Skip for draft PRs
if: "!github.event.pull_request.draft"
```

### GITHUB_OUTPUT

```yaml
# Set output
- id: my-step
  run: |
    echo "version=1.2.3" >> "$GITHUB_OUTPUT"
    echo "changed=true" >> "$GITHUB_OUTPUT"

# Multiline output
- id: multiline
  run: |
    {
      echo 'content<<EOF'
      cat report.txt
      echo 'EOF'
    } >> "$GITHUB_OUTPUT"

# Use output
- run: echo "Version: ${{ steps.my-step.outputs.version }}"
```

### GITHUB_ENV

```yaml
# Set environment variable for subsequent steps
- run: echo "MY_VAR=hello" >> "$GITHUB_ENV"

# Use in next step
- run: echo "$MY_VAR"  # Output: hello
```

### Dynamic Values

```yaml
# fromJSON: Parse JSON string to object
strategy:
  matrix: ${{ fromJSON(needs.setup.outputs.matrix) }}

# format: String formatting
- run: echo ${{ format('Hello {0}, welcome to {1}!', github.actor, github.repository) }}

# contains: Check array/string membership
if: contains(fromJSON('["main", "develop"]'), github.ref_name)

# hashFiles: Generate hash for cache keys
key: deps-${{ hashFiles('**/pnpm-lock.yaml', '**/package.json') }}

# toJSON: Debug - print entire context
- run: echo '${{ toJSON(github.event) }}'
```

---

## Community Resources

| Resource | URL | Description |
|----------|-----|-------------|
| Awesome Actions | `sdras/awesome-actions` | Curated action list |
| Runner Images | `actions/runner-images` | Pre-installed software specs |
| GitHub Actions Docs | docs.github.com/actions | Official documentation |
| act | `nektos/act` | Local workflow testing |
| actionlint | `rhysd/actionlint` | Workflow YAML linter |
