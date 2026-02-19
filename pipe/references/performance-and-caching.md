# Performance and Caching

Job dependency optimization, caching strategies, matrix testing, artifact management, concurrency control, and cost management.

---

## Caching Strategies

### actions/cache

**Limits:** 10 GB per repository. Entries not accessed for 7 days are evicted. FIFO eviction when limit exceeded.

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.pnpm-store
    key: pnpm-${{ runner.os }}-${{ hashFiles('**/pnpm-lock.yaml') }}
    restore-keys: |
      pnpm-${{ runner.os }}-
```

### Key Design Principles

1. **Include lockfile hash** — ensures cache invalidation on dependency change
2. **Include OS** — prevents cross-OS cache corruption
3. **Use restore-keys for fallback** — partial match allows stale-but-useful cache

### Language-Specific Cache Patterns

#### Node.js (pnpm)

```yaml
# Option A: Built-in cache (simpler)
- uses: pnpm/action-setup@v4
  with:
    version: 9
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: 'pnpm'

# Option B: Manual cache (more control)
- uses: actions/cache@v4
  with:
    path: |
      ~/.pnpm-store
      node_modules/.cache
# ...
```

#### Node.js (npm)

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: 'npm'
```

#### Python (uv)

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/uv
    key: uv-${{ runner.os }}-${{ hashFiles('**/uv.lock') }}
    restore-keys: uv-${{ runner.os }}-
```

#### Go

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/go/pkg/mod
      ~/.cache/go-build
    key: go-${{ runner.os }}-${{ hashFiles('**/go.sum') }}
    restore-keys: go-${{ runner.os }}-
```

#### Rust

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.cargo/bin/
      ~/.cargo/registry/index/
      ~/.cargo/registry/cache/
      ~/.cargo/git/db/
      target/
    key: cargo-${{ runner.os }}-${{ hashFiles('**/Cargo.lock') }}
    restore-keys: cargo-${{ runner.os }}-
```

### Docker Layer Cache

```yaml
- uses: docker/build-push-action@v6
  with:
    context: .
    push: true
    tags: myapp:latest
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

**`mode=max`** caches all layers (not just final image layers). More cache space used but faster rebuilds.

### Cache Competition in Parallel Jobs

When multiple parallel jobs write to the same cache key, only the first to complete wins. Others get a "cache already exists" warning.

**Mitigation:** Use job-specific cache keys:

```yaml
key: pnpm-${{ runner.os }}-${{ matrix.node }}-${{ hashFiles('**/pnpm-lock.yaml') }}
```

Or use a dedicated setup job that saves the cache, with downstream jobs restoring only:

```yaml
jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/cache@v4
        with:
          path: node_modules
          key: deps-${{ hashFiles('**/pnpm-lock.yaml') }}
      - run: pnpm install --frozen-lockfile

  test:
    needs: setup
    strategy:
      matrix:
# ...
```

---

## Job Dependency Graphs

### Basics: `needs`

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [...]

  test:
    runs-on: ubuntu-latest
    steps: [...]

  build:
    needs: [lint, test]  # Runs after BOTH complete
    runs-on: ubuntu-latest
    steps: [...]

  deploy:
# ...
```

**Execution:** `lint` and `test` run in parallel → `build` waits for both → `deploy` waits for `build`.

### Diamond Pattern

```
    lint
   /    \
setup    test → deploy
   \    /
    build
```

```yaml
jobs:
  setup:
    # ...
  lint:
    needs: setup
  test:
    needs: setup
  build:
    needs: setup
  deploy:
    needs: [lint, test, build]
```

### Conditional Execution

```yaml
jobs:
  check:
    runs-on: ubuntu-latest
    outputs:
      has-changes: ${{ steps.filter.outputs.src }}
    steps:
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            src:
              - 'src/**'

  test:
    needs: check
# ...
```

### Run Despite Upstream Failure

```yaml
deploy:
  needs: [test, lint]
  if: always() && needs.test.result == 'success'
  # Runs even if lint fails, as long as test passed
```

**Status functions:**
- `success()` — all previous jobs succeeded (default implicit)
- `failure()` — at least one previous job failed
- `cancelled()` — workflow was cancelled
- `always()` — always run, check individual `needs.*.result`

---

## Matrix Strategy

### Basic Matrix

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node: [18, 20, 22]
      fail-fast: false  # Don't cancel other jobs on first failure
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
```

This creates 9 jobs (3 OS x 3 Node versions).

### Include/Exclude

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest]
    node: [18, 20]
    include:
      # Add a specific combination with extra variable
      - os: ubuntu-latest
        node: 22
        experimental: true
    exclude:
      # Remove a specific combination
      - os: macos-latest
        node: 18
```

### Dynamic Matrix

```yaml
jobs:
  prepare:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - id: set-matrix
        run: |
          echo 'matrix={"include":[{"project":"api","path":"packages/api"},{"project":"web","path":"packages/web"}]}' >> "$GITHUB_OUTPUT"

  build:
    needs: prepare
    strategy:
      matrix: ${{ fromJSON(needs.prepare.outputs.matrix) }}
    runs-on: ubuntu-latest
# ...
```

### Limits

- Maximum **256 jobs** per workflow execution
- `max-parallel` controls concurrent job count:

```yaml
strategy:
  max-parallel: 3  # Run at most 3 matrix jobs simultaneously
  matrix:
    shard: [1, 2, 3, 4, 5, 6]
```

---

## Artifact Management (v4)

### Upload

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: build-output
    path: |
      dist/
      !dist/**/*.map  # Exclude source maps
    retention-days: 7  # Default: 90 days
    if-no-files-found: error  # warn | ignore | error
```

### Download (Same Workflow)

```yaml
- uses: actions/download-artifact@v4
  with:
    name: build-output
    path: dist/
```

### Cross-Workflow Download

```yaml
- uses: actions/download-artifact@v4
  with:
    name: build-output
    run-id: ${{ github.event.workflow_run.id }}
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

### v4 Improvements

- Upload speed **~90% faster** than v3
- Maximum **500 artifacts** per job
- Immutable artifacts (same name = error, not overwrite)
- File permissions **not preserved** (workaround: tar before upload)

### Merge Multiple Artifacts

```yaml
# Upload per-shard results
- uses: actions/upload-artifact@v4
  with:
    name: test-results-${{ matrix.shard }}
    path: results/

# Later job: download all
- uses: actions/download-artifact@v4
  with:
    pattern: test-results-*
    merge-multiple: true
    path: all-results/
```

---

## Concurrency Control

### PR Workflows: Cancel Previous

```yaml
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
```

When a new push arrives on the same branch, the previous run is cancelled.

### Deploy Workflows: Queue

```yaml
concurrency:
  group: deploy-${{ github.event.inputs.environment || 'staging' }}
  cancel-in-progress: false  # Don't cancel, queue instead
```

Only one deployment runs at a time per environment.

### Job-Level Concurrency

```yaml
jobs:
  deploy:
    concurrency:
      group: deploy-production
      cancel-in-progress: false
    steps: [...]
```

### Group Name Patterns

| Pattern | Use Case |
|---------|----------|
| `${{ github.workflow }}-${{ github.ref }}` | Per-workflow, per-branch |
| `ci-${{ github.head_ref \|\| github.ref }}` | PR-aware (uses PR source branch) |
| `deploy-${{ inputs.environment }}` | Per-environment |
| `release` | Global release lock |

---

## Runner Selection and Cost

### Hosted Runner Comparison

| Runner | vCPU | RAM | Cost/min | Best For |
|--------|------|-----|----------|----------|
| `ubuntu-latest` | 4 | 16 GB | $0.008 | Standard CI/CD |
| `ubuntu-24.04` | 4 | 16 GB | $0.008 | Pinned OS version |
| `macos-latest` | 3 (M1) | 7 GB | $0.08 | iOS/macOS builds |
| `macos-latest-xlarge` | 12 (M1) | 30 GB | $0.12 | Large macOS builds |
| `windows-latest` | 4 | 16 GB | $0.016 | Windows builds |

### Larger Runners (Linux)

| Size | vCPU | RAM | Cost/min |
|------|------|-----|----------|
| 4-core | 4 | 16 GB | $0.016 |
| 8-core | 8 | 32 GB | $0.032 |
| 16-core | 16 | 64 GB | $0.064 |
| 32-core | 32 | 128 GB | $0.128 |
| 64-core | 64 | 256 GB | $0.256 |

### ARM Runners

- **37% cost reduction** compared to equivalent x86
- Available as `ubuntu-24.04-arm` or larger ARM runners
- Ideal for ARM-native builds (Docker ARM images, Go ARM binaries)

### Cost Optimization Tips

1. **Use `ubuntu-latest`** unless OS-specific builds are needed
2. **Cancel in-progress** runs on new push (`cancel-in-progress: true`)
3. **Path filters** to skip unnecessary workflows
4. **Conditional jobs** to skip when no relevant changes
5. **Cache aggressively** to reduce install/build time
6. **Timeout** to prevent runaway jobs: `timeout-minutes: 15`
7. **ARM runners** for applicable workloads (37% savings)

---

## Execution Time Optimization

### Combine Steps

```yaml
# SLOW: Multiple run steps (each has overhead)
- run: pnpm lint
- run: pnpm typecheck
- run: pnpm test

# FASTER: Single run step
- run: |
    pnpm lint
    pnpm typecheck
    pnpm test
```

### Shallow Clone

```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 1  # Default. Only latest commit
    # fetch-depth: 0  # Full history (needed for git log, semantic-release)
```

### Conditional Steps

```yaml
- name: Deploy
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
  run: ./deploy.sh
```

### Timeout

```yaml
jobs:
  test:
    timeout-minutes: 15  # Kill if exceeds 15 minutes
    steps:
      - name: Long test
        timeout-minutes: 10  # Per-step timeout
        run: pnpm test
```

### Parallel Test Sharding

```yaml
jobs:
  test:
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - run: pnpm test --shard=${{ matrix.shard }}/4

  merge-coverage:
    needs: test
    steps:
      - uses: actions/download-artifact@v4
        with:
          pattern: coverage-*
          merge-multiple: true
# ...
```

---

## Expressions and Outputs

### Step Outputs

```yaml
steps:
  - id: version
    run: echo "value=$(node -p "require('./package.json').version")" >> "$GITHUB_OUTPUT"

  - run: echo "Version is ${{ steps.version.outputs.value }}"
```

### Job Outputs

```yaml
jobs:
  detect:
    outputs:
      changed: ${{ steps.check.outputs.changed }}
    steps:
      - id: check
        run: echo "changed=true" >> "$GITHUB_OUTPUT"

  build:
    needs: detect
    if: needs.detect.outputs.changed == 'true'
```

### Useful Functions

| Function | Example | Purpose |
|----------|---------|---------|
| `contains()` | `contains(github.event.labels.*.name, 'deploy')` | Check array membership |
| `startsWith()` | `startsWith(github.ref, 'refs/tags/')` | String prefix check |
| `format()` | `format('cache-{0}-{1}', runner.os, hashFiles('lock'))` | String formatting |
| `fromJSON()` | `fromJSON(needs.setup.outputs.matrix)` | Parse JSON string |
| `toJSON()` | `toJSON(github.event)` | Serialize to JSON |
| `hashFiles()` | `hashFiles('**/pnpm-lock.yaml')` | File hash for cache keys |

### Status Check Functions

```yaml
# Run cleanup even if previous steps failed
- if: always()
  run: ./cleanup.sh

# Run only on failure (notifications)
- if: failure()
  run: ./notify-failure.sh

# Run on success or failure, but not cancellation
- if: success() || failure()
  run: ./report.sh
```
