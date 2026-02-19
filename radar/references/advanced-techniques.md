# Advanced Testing Techniques

Property-Based Testing, Contract Testing, Mutation Testing, Snapshot strategy, and Testcontainers.

---

## Property-Based Testing

Instead of specific examples, define properties that should always hold true.

### JavaScript/TypeScript (fast-check)

```typescript
import fc from 'fast-check';

// Property: sort is idempotent
test('sorting twice gives same result as sorting once', () => {
  fc.assert(
    fc.property(fc.array(fc.integer()), (arr) => {
      const sorted = [...arr].sort((a, b) => a - b);
      const sortedTwice = [...sorted].sort((a, b) => a - b);
      expect(sorted).toEqual(sortedTwice);
    })
  );
});

// Property: encode then decode is identity
test('JSON roundtrip preserves data', () => {
// ...
```

### Python (Hypothesis)

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_idempotent(lst):
    sorted_once = sorted(lst)
    sorted_twice = sorted(sorted_once)
    assert sorted_once == sorted_twice

@given(st.text(), st.text())
def test_concat_length(a, b):
    assert len(a + b) == len(a) + len(b)
```

### Go (rapid)

```go
import "pgregory.net/rapid"

func TestSortIdempotent(t *testing.T) {
    rapid.Check(t, func(t *rapid.T) {
        arr := rapid.SliceOf(rapid.Int()).Draw(t, "arr")
        sort.Ints(arr)
        sorted := make([]int, len(arr))
        copy(sorted, arr)
        sort.Ints(arr)
        assert.Equal(t, sorted, arr)
    })
}
```

### When to Use Property-Based Testing

| Scenario | Example |
|----------|---------|
| Data transformation roundtrips | encode/decode, serialize/deserialize |
| Mathematical properties | commutativity, associativity, idempotency |
| Sorting / filtering | output always sorted, length preserved |
| Parser / validator | all valid inputs accepted, all invalid rejected |
| Business rules | discount never exceeds price, total >= 0 |

---

## Contract Testing (Pact)

Verify that API provider and consumer agree on the contract.

### Consumer Side

```typescript
// consumer.pact.test.ts
import { PactV4 } from '@pact-foundation/pact';

const provider = new PactV4({
  consumer: 'OrderService',
  provider: 'UserService',
});

test('get user by id', async () => {
  await provider
    .addInteraction()
    .given('user 1 exists')
    .uponReceiving('a request for user 1')
    .withRequest('GET', '/api/users/1')
    .willRespondWith(200, {
// ...
```

### Provider Side

```typescript
// provider.pact.test.ts
import { Verifier } from '@pact-foundation/pact';

test('verifies pact with consumer', async () => {
  const verifier = new Verifier({
    providerBaseUrl: 'http://localhost:3000',
    pactUrls: ['./pacts/orderservice-userservice.json'],
    stateHandlers: {
      'user 1 exists': async () => {
        await seedUser({ id: '1', name: 'Test User' });
      },
    },
  });

  await verifier.verifyProvider();
// ...
```

### When to Use Contract Testing

- Microservice-to-microservice communication
- Frontend-to-backend API contracts
- Third-party API integration (provider side)
- Preventing breaking changes across teams

---

## Mutation Testing

Verify that tests actually catch bugs by introducing small code changes (mutations).

### JavaScript/TypeScript (Stryker)

```json
// stryker.config.json
{
  "mutator": {
    "excludedMutations": ["StringLiteral"]
  },
  "testRunner": "vitest",
  "reporters": ["html", "clear-text", "progress"],
  "coverageAnalysis": "perTest",
  "thresholds": {
    "high": 80,
    "low": 60,
    "break": 50
  }
}
```

```bash
# Run mutation testing
npx stryker run

# Output: Mutation score (higher is better)
# Killed: 85/100 (85%) - your tests caught 85% of mutations
```

### Interpreting Results

| Status | Meaning | Action |
|--------|---------|--------|
| **Killed** | Test caught the mutation | Good - test is effective |
| **Survived** | Mutation wasn't caught | Bad - test gap exists |
| **No coverage** | No test runs this code | Missing test entirely |
| **Timeout** | Mutation caused infinite loop | Usually OK (caught) |

### When to Use

- Critical business logic (payment, auth, data transformation)
- After achieving high line coverage but uncertain about quality
- Before major refactoring (ensure tests are strong enough)

### Exclusion Rules

```json
// stryker.config.json - Fine-tuned exclusions
{
  "mutator": {
    "excludedMutations": [
      "StringLiteral",       // Log messages, error strings
      "ObjectLiteral"        // Config objects
    ]
  },
  "mutate": [
    "src/**/*.ts",
    "!src/**/*.d.ts",
    "!src/**/*.config.ts",
    "!src/**/generated/**",
    "!src/**/types/**",
    "!src/**/__mocks__/**"
// ...
```

### Performance Optimization

```json
{
  "concurrency": 4,
  "coverageAnalysis": "perTest",
  "incremental": true,
  "incrementalFile": ".stryker-tmp/incremental.json",
  "timeoutMS": 10000,
  "timeoutFactor": 1.5
}
```

| Option | Effect | Recommendation |
|--------|--------|----------------|
| `concurrency` | Parallel mutant execution | CPU cores - 1 |
| `coverageAnalysis: perTest` | Only run relevant tests per mutant | Always enable |
| `incremental` | Skip unchanged mutants | Enable for iterative runs |
| `timeoutMS` | Kill slow mutants | 10-30s depending on suite |

### Result Interpretation Benchmarks

| Mutation Score | Rating | Action |
|---------------|--------|--------|
| 90%+ | Excellent | Maintain; focus on new code |
| 75-89% | Good | Target critical surviving mutants |
| 60-74% | Acceptable | Systematic improvement needed |
| < 60% | Poor | Significant test gaps; prioritize |

### Mutation Strategy by Context

| Context | Strategy | Scope |
|---------|----------|-------|
| Default (PR) | Changed Files Only | `--incremental` |
| Critical Path | Targeted Modules | `--mutate src/core/**` |
| Weekly Audit | Full Suite | All source files |
| Pre-Release | Critical + Changed | Union of both scopes |

### Python (mutmut)

```bash
# Install
pip install mutmut

# Run mutation testing
mutmut run --paths-to-mutate=src/

# View results
mutmut results

# Show specific surviving mutant
mutmut show 42
```

### Go (go-mutesting)

```bash
# Install
go install github.com/zimmski/go-mutesting/cmd/go-mutesting@latest

# Run mutation testing
go-mutesting ./...

# With specific mutators
go-mutesting --mutator=expression/remove ./pkg/auth/...
```

---

## Snapshot Testing Strategy

### When Snapshots Are Appropriate

| Use Case | Appropriate | Reason |
|----------|-------------|--------|
| API response structure | ✅ Yes | Catches unintended schema changes |
| Error messages | ✅ Yes | Prevents accidental message changes |
| Configuration output | ✅ Yes | Catches config drift |
| UI component HTML | ⚠️ Careful | Brittle - use inline snapshots |
| Large data structures | ❌ No | Hard to review, easy to blindly update |

### Inline Snapshots (Preferred)

```typescript
// ✅ GOOD: Inline snapshot - easy to review
test('formats user display name', () => {
  expect(formatDisplayName({ first: 'John', last: 'Doe' }))
    .toMatchInlineSnapshot(`"John Doe"`);
});

// ✅ GOOD: API response structure
test('returns user shape', async () => {
  const user = await getUser('1');
  expect(user).toMatchInlineSnapshot(`
    {
      "email": "test@example.com",
      "id": "1",
      "name": "Test User",
    }
// ...
```

### File Snapshots (Use Sparingly)

```typescript
// ⚠️ CAREFUL: Only for complex, stable structures
test('generates correct config', () => {
  const config = generateConfig({ env: 'production' });
  expect(config).toMatchSnapshot();
  // Creates __snapshots__/config.test.ts.snap
});

// Always review snapshot updates carefully:
// pnpm test -- -u  (update snapshots)
```

---

## Testcontainers

Run real databases and services in Docker for integration tests.

### JavaScript/TypeScript

```typescript
import { PostgreSqlContainer } from '@testcontainers/postgresql';

describe('UserRepository (Postgres)', () => {
  let container: StartedPostgreSqlContainer;
  let db: Pool;

  beforeAll(async () => {
    container = await new PostgreSqlContainer()
      .withDatabase('testdb')
      .start();

    db = new Pool({ connectionString: container.getConnectionUri() });
    await runMigrations(db);
  }, 60000); // Longer timeout for container startup

// ...
```

### Go

```go
import (
    "github.com/testcontainers/testcontainers-go"
    "github.com/testcontainers/testcontainers-go/modules/postgres"
)

func TestWithPostgres(t *testing.T) {
    ctx := context.Background()

    container, err := postgres.Run(ctx, "postgres:16",
        postgres.WithDatabase("testdb"),
        postgres.WithUsername("test"),
        postgres.WithPassword("test"),
    )
    require.NoError(t, err)
    defer container.Terminate(ctx)
// ...
```

### Python

```python
from testcontainers.postgres import PostgresContainer

def test_with_postgres():
    with PostgresContainer("postgres:16") as postgres:
        engine = create_engine(postgres.get_connection_url())
        # Run tests against real Postgres
```

---

## Test Pyramid Revisited

```
        /\
       /  \      E2E (Few) → Voyager
      /----\     Contract Tests → Radar (Pact)
     /      \    Integration (Some) → Radar + Testcontainers
    /--------\   Property-Based → Radar (fast-check/Hypothesis)
   /          \  Unit (Many) → Radar (primary)
  /------------\ Mutation → Radar (verify test quality)
 /              \
/________________\
```

### When to Use Each

| Technique | Cost | Value | Use When |
|-----------|------|-------|----------|
| Unit tests | Low | High | Always (default) |
| Property-based | Medium | High | Data transformation, math, parsing |
| Integration (Testcontainers) | Medium | High | DB queries, API handlers |
| Contract tests | Medium | Medium | Microservices, API boundaries |
| Mutation testing | High | High | Critical code, before major refactor |
| Snapshot tests | Low | Medium | Stable output structures only |
