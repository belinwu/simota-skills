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
test('shows success message', async () => {
  await submitForm();
  expect(await screen.findByText('Success')).toBeInTheDocument();
});
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

  vi.useRealTimers();
});
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

  test('creates user', async () => {
    // Each test starts with clean state
  });
});
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
  expect(result).toBe('2024-01-15');

  vi.useRealTimers();
});
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
  expect(users).toHaveLength(1);
});

// Override for specific test
test('handles timeout', async () => {
  server.use(
    http.get('/api/users', async () => {
      await new Promise((r) => setTimeout(r, 10000));
      return HttpResponse.json([]);
    })
  );
  // Test timeout handling...
});
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
