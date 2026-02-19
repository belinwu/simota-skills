# Flaky Test Guide

Diagnosis, prevention, and fixing of flaky tests.

---

## Common Causes & Fixes

| Cause | Symptom | Fix |
|-------|---------|-----|
| **Race condition** | Passes locally, fails in CI | Use `waitFor`, `findBy*`, proper async handling |
| **Timing dependency** | Fails intermittently | Use fake timers, avoid real delays |
| **Test order dependency** | Fails when run in isolation | Ensure proper setup/teardown |
| **Shared state** | Fails after other tests | Reset state in `beforeEach` |
| **Network flakiness** | Timeout errors | Mock external APIs with MSW |
| **Date/time dependency** | Fails on specific dates | Mock `Date.now()`, use fake timers |
| **Viewport dependency** | Fails on different screen sizes | Set explicit viewport in test config |
| **Locale dependency** | Fails in different CI regions | Use fixed locale in test setup |

---

## Race Condition Fixes

```typescript
// ❌ BAD: Race condition - element might not exist yet
test('shows success message', async () => {
  await submitForm();
  expect(screen.getByText('Success')).toBeInTheDocument(); // May fail!
});

// ✅ GOOD: Wait for element to appear
test('shows success message', async () => {
  await submitForm();
  await waitFor(() => {
    expect(screen.getByText('Success')).toBeInTheDocument();
  });
});

// ✅ BETTER: Use findBy (built-in waitFor)
// ...
```

---

## Timing Issues (Fake Timers)

```typescript
// ❌ BAD: Real timers are slow and flaky
test('debounced search', async () => {
  fireEvent.change(input, { target: { value: 'test' } });
  await new Promise(r => setTimeout(r, 500)); // Slow and flaky!
  expect(mockSearch).toHaveBeenCalled();
});

// ✅ GOOD: Use fake timers
test('debounced search', async () => {
  vi.useFakeTimers();

  fireEvent.change(input, { target: { value: 'test' } });
  await vi.advanceTimersByTimeAsync(500);

  expect(mockSearch).toHaveBeenCalledWith('test');
// ...
```

---

## Test Isolation

```typescript
// ✅ GOOD: Proper isolation with setup/teardown
describe('UserService', () => {
  let service: UserService;
  let mockDb: MockDatabase;

  beforeEach(() => {
    mockDb = new MockDatabase();
    service = new UserService(mockDb);
  });

  afterEach(() => {
    mockDb.reset();
    vi.clearAllMocks();
  });

// ...
```

---

## Date/Time Mocking

```typescript
// ✅ GOOD: Mock Date for deterministic tests
test('shows "today" for current date', () => {
  vi.setSystemTime(new Date('2024-01-15'));

  const result = formatRelativeDate(new Date('2024-01-15'));
  expect(result).toBe('Today');

  vi.useRealTimers();
});

// ✅ GOOD: Consistent timezone
test('formats date in UTC', () => {
  vi.setSystemTime(new Date('2024-01-15T12:00:00Z'));

  const result = formatDate(new Date(), { timeZone: 'UTC' });
// ...
```

---

## Network Mocking (MSW)

```typescript
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';

const server = setupServer(
  http.get('/api/users', () => {
    return HttpResponse.json([{ id: 1, name: 'Test User' }]);
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('fetches users', async () => {
  const users = await fetchUsers();
// ...
```

---

## Flaky Test Detection

### CI Retry Strategy

```yaml
# .github/workflows/test.yml
- name: Run tests with retry
  uses: nick-fields/retry@v2
  with:
    max_attempts: 3
    command: pnpm test
    # Log flaky tests for investigation
    on_retry_command: echo "::warning::Flaky test detected - retry needed"
```

### Vitest Retry Configuration

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    retry: process.env.CI ? 2 : 0, // Retry in CI only
    reporters: ['default', 'hanging-process'], // Detect hanging tests
  },
});
```

### Jest Retry

```javascript
// jest.config.js
module.exports = {
  // Retry failed tests
  retryTimes: process.env.CI ? 2 : 0,
};
```

---

## Flaky Test Quarantine

When a test is identified as flaky but cannot be immediately fixed:

```typescript
// ✅ GOOD: Mark as flaky with ticket reference
test.skip('flaky: payment webhook processing', () => {
  // TODO(radar): Fix flaky test - race condition in webhook handler
  // Ticket: PROJ-1234
  // Root cause: Shared database state between parallel test workers
});

// ❌ BAD: Silent skip without context
test.skip('payment test', () => {
  // No explanation why this is skipped
});
```

---

## Prevention Checklist

Before writing a test, verify:

- [ ] No real timers (`setTimeout`, `setInterval`) - use fake timers
- [ ] No real network calls - use MSW or mocks
- [ ] No shared state between tests - use `beforeEach` cleanup
- [ ] No date/time assumptions - mock `Date.now()`
- [ ] No file system assumptions - use temp directories
- [ ] No execution order dependency - each test is self-contained
- [ ] Explicit waits (`waitFor`, `findBy*`) instead of arbitrary delays
- [ ] Test passes when run in isolation (`test.only`)
- [ ] Test passes when run 10 times in a row

---

## Advanced Retry Strategy

### CI Provider Configurations

```yaml
# GitHub Actions - nick-fields/retry
- name: Run tests with retry
  uses: nick-fields/retry@v3
  with:
    timeout_minutes: 10
    max_attempts: 3
    retry_on: error
    retry_wait_seconds: 10
    command: npx vitest run --reporter=junit --outputFile=test-results.xml
    on_retry_command: echo "::warning::Flaky test detected on attempt ${{ steps.retry.outputs.attempt_number }}"
```

```yaml
# GitLab CI
test:
  script: npx vitest run
  retry:
    max: 2
    when:
      - runner_system_failure
      - script_failure
```

### Framework-Level Retry with Exponential Backoff

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    retry: process.env.CI ? 2 : 0,
    // Per-test retry override
    // test('flaky test', { retry: 3 }, async () => { ... })
  },
});
```

```python
# pytest - pytest-rerunfailures
# pip install pytest-rerunfailures
# pytest --reruns 3 --reruns-delay 2

# Or per-test
@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_external_api():
    ...
```

```go
// Go - custom retry helper
func retryTest(t *testing.T, maxRetries int, testFn func(t *testing.T) error) {
    t.Helper()
    var err error
    for i := 0; i < maxRetries; i++ {
        err = testFn(t)
        if err == nil {
            return
        }
        time.Sleep(time.Duration(math.Pow(2, float64(i))) * time.Second)
    }
    t.Fatalf("test failed after %d retries: %v", maxRetries, err)
}
```

---

## Statistical Flaky Detection

### Repeated Execution

```bash
# Vitest: repeat test N times
npx vitest run --repeat=10

# pytest: repeat with pytest-repeat
pip install pytest-repeat
pytest --count=10

# Go: repeat test
go test -count=10 ./...

# Rust: repeat with nextest
cargo nextest run --retries 0 -j 1 --run-ignored=all
```

### Flaky Metrics

| Metric | Formula | Healthy | Warning | Critical |
|--------|---------|---------|---------|----------|
| **Flaky Rate** | Flaky tests / Total tests | < 1% | 1-5% | > 5% |
| **MTBF** (Mean Time Between Failures) | Avg runs between failures | > 50 runs | 10-50 | < 10 |
| **Flaky Clusters** | Co-occurring flaky tests | 0 clusters | 1-2 | > 2 |

### Detection Script

```bash
#!/bin/bash
# scripts/detect-flaky.sh - Run tests N times and report flaky ones
RUNS=${1:-10}
FAILURES=()

for i in $(seq 1 $RUNS); do
  echo "Run $i/$RUNS..."
  npx vitest run --reporter=json --outputFile=".flaky-run-$i.json" 2>/dev/null
  if [ $? -ne 0 ]; then
    FAILED=$(jq -r '.testResults[].assertionResults[] | select(.status=="failed") | .fullName' ".flaky-run-$i.json")
    FAILURES+=("$FAILED")
  fi
done

echo "=== Flaky Test Report ==="
# ...
```

---

## CI Environment Differences

### Local vs CI Comparison

| Factor | Local | CI (GitHub Actions) | Impact |
|--------|-------|---------------------|--------|
| **CPU** | Multi-core (8-16) | 2 vCPU (ubuntu-latest) | Parallel tests slower |
| **Memory** | 16-64 GB | 7 GB | OOM for large suites |
| **Disk I/O** | SSD (fast) | Network-attached | File-heavy tests slower |
| **Network** | Low latency | Variable latency | External call flakiness |
| **Timezone** | Local TZ | UTC | Date-dependent tests fail |
| **Locale** | User locale | en_US.UTF-8 | Formatting differences |
| **Parallelism** | Often sequential | Matrix / parallel jobs | State isolation issues |
| **DNS** | Cached | Fresh lookup | Resolution timing |

### Mitigation Strategies

```typescript
// Force UTC timezone in tests
// vitest.config.ts
export default defineConfig({
  test: {
    env: {
      TZ: 'UTC',
    },
  },
});
```

```yaml
# GitHub Actions: increase resources for heavy suites
jobs:
  test:
    runs-on: ubuntu-latest
    # Or use larger runner:
    # runs-on: ubuntu-latest-16-cores
    env:
      NODE_OPTIONS: "--max-old-space-size=4096"
      TZ: UTC
      LC_ALL: en_US.UTF-8
```

```typescript
// Adjust timeouts for CI environment
const TIMEOUT_MULTIPLIER = process.env.CI ? 3 : 1;

export default defineConfig({
  test: {
    testTimeout: 10000 * TIMEOUT_MULTIPLIER,
    hookTimeout: 30000 * TIMEOUT_MULTIPLIER,
  },
});
```
