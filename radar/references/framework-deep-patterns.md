# Framework Deep Patterns

各テストフレームワーク固有の高度パターン集。

---

## Vitest Deep

### Workspace Strategy

```typescript
// vitest.workspace.ts
export default [
  {
    extends: './vitest.config.ts',
    test: {
      name: 'unit',
      include: ['src/**/*.test.ts'],
      environment: 'node',
    },
  },
  {
    extends: './vitest.config.ts',
    test: {
      name: 'integration',
      include: ['tests/integration/**/*.test.ts'],
// ...
```

```bash
# Run specific workspace project
npx vitest --project=unit
npx vitest --project=integration

# Run all projects
npx vitest --workspace
```

### Custom Pool Configuration

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    // threads (default): Worker threads, shared memory
    // forks: Child processes, full isolation
    // vmThreads: VM context isolation, fast but less isolated
    pool: 'threads',

    poolOptions: {
      threads: {
        minThreads: 1,
        maxThreads: 4,
        useAtomics: true, // Better synchronization
      },
      forks: {
// ...
```

| Pool | Isolation | Speed | Memory | Use Case |
|------|-----------|-------|--------|----------|
| `threads` | Medium | Fast | Shared | Default, most tests |
| `forks` | High | Medium | Per-process | Global state tests |
| `vmThreads` | Low | Fastest | Shared | Pure unit tests |

### Snapshot Serializer

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    snapshotSerializers: ['./tests/serializers/date-serializer.ts'],
  },
});

// tests/serializers/date-serializer.ts
export default {
  serialize(val: Date) {
    return `Date<${val.toISOString()}>`;
  },
  test(val: unknown) {
    return val instanceof Date;
  },
// ...
```

### Browser Mode

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    browser: {
      enabled: true,
      name: 'chromium',
      provider: 'playwright',
      headless: true,
    },
  },
});
```

### Performance Optimization

```typescript
export default defineConfig({
  test: {
    // Faster test discovery
    include: ['src/**/*.test.ts'], // Be specific
    exclude: ['node_modules', 'dist', '.git'],

    // Faster execution
    isolate: false,        // Skip isolation for pure tests
    passWithNoTests: true, // Don't fail on empty suites

    // Caching
    cache: {
      dir: 'node_modules/.vitest',
    },

// ...
```

---

## Jest Deep

### Module Resolution Advanced

```javascript
// jest.config.js
module.exports = {
  // Module name mapping for aliases
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '^@tests/(.*)$': '<rootDir>/tests/$1',
    // CSS/asset mocking
    '\\.(css|less|scss)$': 'identity-obj-proxy',
    '\\.(jpg|png|svg)$': '<rootDir>/tests/__mocks__/fileMock.js',
  },

  // Module file extensions priority
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json'],

  // Module directories for resolution
// ...
```

### SWC / esbuild Transformer

```javascript
// jest.config.js - Using SWC (fastest)
module.exports = {
  transform: {
    '^.+\\.(t|j)sx?$': ['@swc/jest', {
      jsc: {
        parser: {
          syntax: 'typescript',
          tsx: true,
          decorators: true,
        },
        transform: {
          react: { runtime: 'automatic' },
        },
      },
    }],
// ...
```

| Transformer | Speed | TypeScript | JSX | Decorators |
|------------|-------|-----------|-----|------------|
| `ts-jest` | Slow | Full check | Yes | Yes |
| `@swc/jest` | Fast | Transpile only | Yes | Yes |
| `esbuild-jest` | Fast | Transpile only | Yes | No |
| `babel-jest` | Medium | With presets | Yes | With plugin |

### Debugging Memory/Handles

```bash
# Detect open handles preventing Jest from exiting
npx jest --detectOpenHandles --forceExit

# Log heap usage per test
npx jest --logHeapUsage

# Run with Node inspector
node --inspect-brk node_modules/.bin/jest --runInBand
```

### Custom Snapshot Serializer

```javascript
// tests/serializers/component-serializer.js
module.exports = {
  serialize(val, config, indentation, depth, refs, printer) {
    // Remove dynamic attributes like data-testid
    return printer(val, config, indentation, depth, refs)
      .replace(/ data-testid="[^"]*"/g, '');
  },
  test(val) {
    return val && val.$$typeof === Symbol.for('react.test.json');
  },
};
```

---

## pytest Deep

### Plugin Ecosystem

| Plugin | Purpose | Install |
|--------|---------|---------|
| `pytest-asyncio` | Async test support | `pip install pytest-asyncio` |
| `pytest-timeout` | Per-test timeouts | `pip install pytest-timeout` |
| `pytest-xdist` | Parallel execution | `pip install pytest-xdist` |
| `pytest-mock` | Enhanced mocking | `pip install pytest-mock` |
| `pytest-freezegun` | Time freezing | `pip install pytest-freezegun` |
| `pytest-factoryboy` | Test data factories | `pip install pytest-factoryboy` |
| `pytest-cov` | Coverage reporting | `pip install pytest-cov` |
| `pytest-randomly` | Random test order | `pip install pytest-randomly` |

### conftest.py Inheritance

```
tests/
├── conftest.py              # Global fixtures (db, client)
├── unit/
│   ├── conftest.py          # Unit-specific (mocks, fakes)
│   └── test_service.py
├── integration/
│   ├── conftest.py          # Integration-specific (containers)
│   └── test_api.py
└── e2e/
    ├── conftest.py          # E2E-specific (browser)
    └── test_flow.py
```

```python
# tests/conftest.py (root)
import pytest

@pytest.fixture(scope="session")
def db():
    """Session-scoped database connection."""
    conn = create_test_db()
    yield conn
    conn.close()

@pytest.fixture(autouse=True)
def reset_db(db):
    """Reset DB state before each test."""
    db.execute("BEGIN")
    yield
# ...
```

### Factory Fixtures (pytest-factoryboy)

```python
# tests/factories.py
import factory
from pytest_factoryboy import register

class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Faker('name')
    email = factory.Faker('email')
    role = 'user'

class AdminFactory(UserFactory):
    role = 'admin'

# ...
```

### Marker Strategy

```python
# pyproject.toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks integration tests",
    "smoke: marks smoke tests for quick validation",
]

# Usage
@pytest.mark.slow
def test_full_migration():
    ...

@pytest.mark.integration
def test_database_query():
# ...
```

```bash
# Run only smoke tests
pytest -m smoke

# Exclude slow tests
pytest -m "not slow"

# Run integration + smoke
pytest -m "integration or smoke"
```

### Parallel Execution (pytest-xdist)

```bash
# Auto-detect CPU count
pytest -n auto

# Specific worker count
pytest -n 4

# Load balancing strategies
pytest -n 4 --dist=loadscope  # Group by module
pytest -n 4 --dist=loadfile   # Group by file
pytest -n 4 --dist=load       # Dynamic load balance
```

---

## Go Testing Deep

### t.Helper() / t.Cleanup() Guidelines

```go
// t.Helper(): mark function as test helper (better error reporting)
func assertUserValid(t *testing.T, user *User) {
    t.Helper() // Error line points to caller, not this function

    if user.ID == "" {
        t.Error("user ID is empty")
    }
    if user.Email == "" {
        t.Error("user email is empty")
    }
}

// t.Cleanup(): register cleanup that runs after test completes
func setupTestDB(t *testing.T) *sql.DB {
    t.Helper()
// ...
```

### Subtests + Parallel

```go
func TestAPI(t *testing.T) {
    // Setup shared resources
    server := setupTestServer(t)

    t.Run("GET /users", func(t *testing.T) {
        t.Parallel()
        resp, err := http.Get(server.URL + "/users")
        require.NoError(t, err)
        assert.Equal(t, 200, resp.StatusCode)
    })

    t.Run("POST /users", func(t *testing.T) {
        t.Parallel()
        body := strings.NewReader(`{"name":"John"}`)
        resp, err := http.Post(server.URL+"/users", "application/json", body)
// ...
```

### testify Best Practices

```go
import (
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
    "github.com/stretchr/testify/suite"
)

// require: stops test on failure (use for preconditions)
// assert: continues test on failure (use for assertions)

func TestUserService(t *testing.T) {
    user, err := service.GetUser("123")
    require.NoError(t, err)      // Stop if error (can't proceed)
    require.NotNil(t, user)      // Stop if nil (would panic below)

    assert.Equal(t, "John", user.Name)     // Continue if wrong
// ...
```

### Table-Driven Test Pattern

```go
func TestValidateEmail(t *testing.T) {
    tests := map[string]struct {
        input   string
        wantErr bool
    }{
        "valid email":       {"user@example.com", false},
        "no domain":         {"user@", true},
        "no at sign":        {"user.example.com", true},
        "empty":             {"", true},
        "unicode local":     {"用户@example.com", false},
        "plus addressing":   {"user+tag@example.com", false},
    }

    for name, tt := range tests {
        t.Run(name, func(t *testing.T) {
// ...
```

---

## Rust Testing Deep

### tokio::test Strategy

```rust
// Default: single-threaded, deterministic
#[tokio::test]
async fn test_sequential() {
    let result = fetch_data().await;
    assert_eq!(result.len(), 3);
}

// Multi-threaded: for testing concurrency
#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn test_concurrent() {
    let (a, b) = tokio::join!(
        fetch_data("a"),
        fetch_data("b"),
    );
    assert!(a.is_ok() && b.is_ok());
// ...
```

### rstest Parametrized

```rust
use rstest::rstest;

#[rstest]
#[case("hello", 5)]
#[case("", 0)]
#[case("日本語", 3)]
fn test_char_count(#[case] input: &str, #[case] expected: usize) {
    assert_eq!(input.chars().count(), expected);
}

// Fixture-based
#[rstest]
fn test_with_fixture(#[fixture] db: TestDb) {
    let users = db.query("SELECT * FROM users");
    assert!(!users.is_empty());
// ...
```

### proptest vs quickcheck

```rust
// proptest: more powerful, better shrinking
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_roundtrip_serialize(s in "\\PC*") {
        let serialized = serde_json::to_string(&s).unwrap();
        let deserialized: String = serde_json::from_str(&serialized).unwrap();
        prop_assert_eq!(s, deserialized);
    }

    #[test]
    fn test_sort_idempotent(mut v in prop::collection::vec(any::<i32>(), 0..100)) {
        v.sort();
        let sorted = v.clone();
// ...
```

| Feature | proptest | quickcheck |
|---------|----------|------------|
| Shrinking | Automatic, configurable | Automatic |
| Generators | Rich, composable | Arbitrary trait |
| Regex strategies | Yes | No |
| Config | Per-test | Global |
| Ecosystem | Growing | Mature |

---

## JUnit 5 Deep

### @Nested Tests

```java
@DisplayName("UserService")
class UserServiceTest {

    @Nested
    @DisplayName("when user exists")
    class WhenUserExists {
        private User user;

        @BeforeEach
        void setUp() {
            user = userService.create(new User("John", "john@test.com"));
        }

        @Test
        @DisplayName("returns user by ID")
// ...
```

### Extension Model

```java
// Custom extension for database cleanup
public class DatabaseCleanupExtension implements BeforeEachCallback, AfterEachCallback {
    @Override
    public void beforeEach(ExtensionContext context) {
        getDb(context).beginTransaction();
    }

    @Override
    public void afterEach(ExtensionContext context) {
        getDb(context).rollback();
    }
}

// Usage
@ExtendWith(DatabaseCleanupExtension.class)
// ...
```

### Testcontainers Integration

```java
@Testcontainers
class PostgresIntegrationTest {
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16")
        .withDatabaseName("testdb")
        .withUsername("test")
        .withPassword("test");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

// ...
```

---

## Quick Reference: Framework Selection

| Feature | Vitest | Jest | pytest | Go test | Rust test | JUnit 5 |
|---------|--------|------|--------|---------|-----------|---------|
| Parallel | `pool: 'threads'` | `--workers` | `-n auto` | `t.Parallel()` | `cargo nextest` | `@Execution(CONCURRENT)` |
| Snapshot | Built-in | Built-in | `snapshottest` | `cupaloy` | `insta` | N/A |
| Mocking | `vi.mock()` | `jest.mock()` | `pytest-mock` | Interface | `mockall` | Mockito |
| Coverage | `--coverage` | `--coverage` | `--cov` | `-coverprofile` | `tarpaulin` | JaCoCo |
| Watch | `vitest` | `jest --watch` | `ptw` | N/A | `cargo-watch` | N/A |
| Async | Native | Native | `pytest-asyncio` | Goroutines | `tokio::test` | CompletableFuture |
| Property | N/A | `fast-check` | `hypothesis` | `gopter` | `proptest` | `jqwik` |
