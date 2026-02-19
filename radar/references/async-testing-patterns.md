# Async Testing Patterns

言語横断の非同期テスト戦略：async/await、タイマー、ストリーム、レースコンディション。

---

## TypeScript / JavaScript

### async/await Fundamentals

```typescript
// ✅ Recommended: async/await with resolves/rejects
it('fetches user data', async () => {
  await expect(fetchUser('123')).resolves.toMatchObject({
    id: '123',
    name: expect.any(String),
  });
});

it('rejects for invalid user', async () => {
  await expect(fetchUser('invalid')).rejects.toThrow('User not found');
});

// ✅ Standard async/await
it('processes queue item', async () => {
  const result = await processQueueItem({ id: 1, data: 'test' });
// ...
```

### Vitest waitFor

```typescript
import { vi, expect, it } from 'vitest';

it('eventually updates state', async () => {
  const store = createStore();
  store.dispatch(fetchDataAction());

  // Poll until condition is met
  await vi.waitFor(() => {
    expect(store.getState().data).not.toBeNull();
  }, { timeout: 5000, interval: 100 });

  expect(store.getState().data).toHaveLength(3);
});
```

### Fake Timers + Async

```typescript
import { vi, beforeEach, afterEach } from 'vitest';

beforeEach(() => {
  vi.useFakeTimers();
});

afterEach(() => {
  vi.useRealTimers();
});

it('retries with exponential backoff', async () => {
  const mockFetch = vi.fn()
    .mockRejectedValueOnce(new Error('timeout'))
    .mockRejectedValueOnce(new Error('timeout'))
    .mockResolvedValueOnce({ data: 'success' });
// ...
```

### Stream / Observable Testing

```typescript
// ReadableStream testing
it('processes stream chunks', async () => {
  const stream = createDataStream();
  const reader = stream.getReader();
  const chunks: string[] = [];

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks.push(new TextDecoder().decode(value));
  }

  expect(chunks).toHaveLength(3);
  expect(chunks.join('')).toContain('complete');
});
// ...
```

### Promise.allSettled Testing

```typescript
it('handles mixed success/failure', async () => {
  const results = await Promise.allSettled([
    fetchUser('valid'),
    fetchUser('invalid'),
    fetchUser('another-valid'),
  ]);

  const fulfilled = results.filter(r => r.status === 'fulfilled');
  const rejected = results.filter(r => r.status === 'rejected');

  expect(fulfilled).toHaveLength(2);
  expect(rejected).toHaveLength(1);
  expect((rejected[0] as PromiseRejectedResult).reason.message).toContain('not found');
});
```

---

## Python

### pytest-asyncio

```python
# conftest.py
import pytest

# Use asyncio mode for all async tests
pytest_plugins = ['pytest_asyncio']

@pytest.fixture
async def db_session():
    session = await create_async_session()
    yield session
    await session.close()
```

```python
# tests/test_async_service.py
import pytest
import asyncio

@pytest.mark.asyncio
async def test_fetch_user(db_session):
    user = await user_service.get_by_id(db_session, user_id=123)
    assert user.name == "John Doe"

@pytest.mark.asyncio
async def test_concurrent_requests():
    """Test multiple concurrent API calls."""
    results = await asyncio.gather(
        fetch_data("/api/users"),
        fetch_data("/api/posts"),
# ...
```

### aiohttp / httpx AsyncClient

```python
# tests/test_async_http.py
import pytest
import httpx

@pytest.fixture
async def client():
    async with httpx.AsyncClient(base_url="http://testserver") as client:
        yield client

@pytest.mark.asyncio
async def test_api_endpoint(client):
    response = await client.get("/api/users/123")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 123
# ...
```

---

## Go

### t.Parallel()

```go
// tests/user_test.go
func TestUserService(t *testing.T) {
    t.Parallel() // Mark parent as parallel

    tests := []struct {
        name     string
        userID   string
        wantErr  bool
    }{
        {"valid user", "123", false},
        {"invalid user", "999", true},
        {"empty ID", "", true},
    }

    for _, tt := range tests {
// ...
```

### Channel-Based Synchronization

```go
func TestEventProcessor(t *testing.T) {
    // Channel to collect results
    results := make(chan Event, 10)

    processor := NewEventProcessor(func(e Event) {
        results <- e
    })

    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    go processor.Start(ctx)

    // Send events
    processor.Send(Event{Type: "user.created", Data: "123"})
// ...
```

### context.WithTimeout

```go
func TestSlowOperation(t *testing.T) {
    ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
    defer cancel()

    result, err := slowDatabaseQuery(ctx)
    require.NoError(t, err)
    assert.NotEmpty(t, result)
}

func TestContextCancellation(t *testing.T) {
    ctx, cancel := context.WithCancel(context.Background())

    errCh := make(chan error, 1)
    go func() {
        errCh <- longRunningTask(ctx)
// ...
```

### Race Detection

```bash
# Always run with race detector in CI
go test -race ./...

# Combine with coverage
go test -race -coverprofile=coverage.out ./...
```

```go
// Test specifically for race conditions
func TestConcurrentMapAccess(t *testing.T) {
    cache := NewSafeCache()

    var wg sync.WaitGroup
    for i := 0; i < 100; i++ {
        wg.Add(2)
        go func(id int) {
            defer wg.Done()
            cache.Set(fmt.Sprintf("key-%d", id), id)
        }(i)
        go func(id int) {
            defer wg.Done()
            cache.Get(fmt.Sprintf("key-%d", id))
        }(i)
// ...
```

---

## Rust

### tokio::test

```rust
// Single-threaded runtime (default)
#[tokio::test]
async fn test_fetch_user() {
    let user = fetch_user("123").await.unwrap();
    assert_eq!(user.name, "John");
}

// Multi-threaded runtime (for testing concurrent behavior)
#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn test_concurrent_processing() {
    let (tx, mut rx) = tokio::sync::mpsc::channel(100);

    // Spawn multiple tasks
    for i in 0..10 {
        let tx = tx.clone();
// ...
```

### Timeout Testing

```rust
#[tokio::test]
async fn test_operation_timeout() {
    let result = tokio::time::timeout(
        Duration::from_secs(2),
        slow_operation(),
    ).await;

    assert!(result.is_err(), "Expected timeout");
}

#[tokio::test]
async fn test_with_tokio_time() {
    tokio::time::pause(); // Freeze time

    let start = tokio::time::Instant::now();
// ...
```

### Channel Testing

```rust
#[tokio::test]
async fn test_mpsc_channel() {
    let (tx, mut rx) = tokio::sync::mpsc::channel::<String>(32);

    tokio::spawn(async move {
        tx.send("hello".to_string()).await.unwrap();
        tx.send("world".to_string()).await.unwrap();
    });

    assert_eq!(rx.recv().await, Some("hello".to_string()));
    assert_eq!(rx.recv().await, Some("world".to_string()));
    assert_eq!(rx.recv().await, None); // Channel closed
}
```

---

## Timeout Strategy

### Default Timeouts by Test Type

| Test Type | Default Timeout | Max Timeout | Rationale |
|-----------|----------------|-------------|-----------|
| Unit | 5s | 10s | Pure logic, no I/O |
| Integration | 30s | 60s | Database, API calls |
| Contract | 15s | 30s | Mock server setup |
| E2E | 60s | 120s | Browser operations |
| Performance | 120s | 300s | Measurement overhead |

### Framework Configuration

```typescript
// Vitest
export default defineConfig({
  test: {
    testTimeout: 10000,      // 10s per test
    hookTimeout: 30000,      // 30s for before/afterAll
    teardownTimeout: 10000,  // 10s for cleanup
  },
});
```

```python
# pytest
[tool.pytest.ini_options]
timeout = 30  # Default 30s per test

# Per-test override
@pytest.mark.timeout(60)
async def test_slow_integration():
    ...
```

```go
// Go - per-test timeout
func TestSlow(t *testing.T) {
    if testing.Short() {
        t.Skip("skipping slow test in short mode")
    }
    // ... slow test
}

// CLI: go test -timeout 60s ./...
```

```toml
# Rust - nextest
[profile.default]
slow-timeout = { period = "60s", terminate-after = 2 }
```

---

## Race Condition Detection & Prevention

### Common Symptoms

| Symptom | Likely Cause | Detection |
|---------|-------------|-----------|
| Test passes locally, fails in CI | Timing-dependent assertions | Run with `-race` / `--repeat` |
| Intermittent assertion failures | Shared mutable state | Isolate state per test |
| Deadlock in CI | Missing timeout | Add test-level timeouts |
| Wrong order of events | Assumed execution order | Use synchronization primitives |
| "Flaky" label | Any of the above | Statistical analysis (10+ runs) |

### Prevention Strategies

```typescript
// ❌ Race-prone: shared state
let sharedCounter = 0;
it('test 1', async () => { sharedCounter++; /* ... */ });
it('test 2', async () => { sharedCounter++; /* ... */ });

// ✅ Isolated: per-test state
it('test 1', async () => {
  const counter = createCounter();
  counter.increment();
  expect(counter.value).toBe(1);
});
```

```typescript
// ❌ Race-prone: time-dependent
it('completes within 100ms', async () => {
  const start = Date.now();
  await operation();
  expect(Date.now() - start).toBeLessThan(100); // Flaky in slow CI
});

// ✅ Stable: use fake timers or generous bounds
it('completes quickly', async () => {
  vi.useFakeTimers();
  const promise = operation();
  await vi.advanceTimersByTimeAsync(100);
  await expect(promise).resolves.toBeDefined();
  vi.useRealTimers();
});
```

```go
// ❌ Race-prone: goroutine without sync
func TestRacy(t *testing.T) {
    result := ""
    go func() { result = "done" }()
    time.Sleep(10 * time.Millisecond) // Hope it finishes
    assert.Equal(t, "done", result)
}

// ✅ Synchronized: channel or WaitGroup
func TestSafe(t *testing.T) {
    done := make(chan string, 1)
    go func() { done <- "done" }()

    select {
    case result := <-done:
// ...
```

---

## Quick Reference

| Language | Async Test | Fake Timers | Race Detection | Timeout |
|----------|-----------|-------------|----------------|---------|
| TypeScript | `async/await` | `vi.useFakeTimers()` | N/A | `testTimeout` |
| Python | `@pytest.mark.asyncio` | `freezegun` | N/A | `@pytest.mark.timeout` |
| Go | `t.Parallel()` | `clockwork` | `go test -race` | `go test -timeout` |
| Rust | `#[tokio::test]` | `tokio::time::pause()` | `miri` | `slow-timeout` |
