# Ordering-Sensitivity Reference

Purpose: Detect bugs that rely on an ordering guarantee that does not actually hold — unordered iteration treated as ordered, sort stability assumed where absent, concurrent writes with implicit ordering, and read-your-write expectations on eventually consistent stores. These produce intermittent, environment-dependent failures that look random but are deterministic once the ordering hazard is named.

## Scope Boundary

- **Specter `order`**: Ordering-sensitivity hazards in iteration, sort, concurrent writes, and eventual consistency reads.
- **Specter `race`**: Classical data races on shared memory / primitives. If the bug is a lost update or torn read, stay in `race`.
- **Probe**: Type-level ordering contract (e.g., `ReadonlyArray` vs `Set` API misuse caught at type-check). If TS/Flow catches it, route to Probe.
- **Sentinel (resource perf)**: Sort performance, index missing, scan-instead-of-seek. If the issue is speed, not correctness, route to Sentinel.
- **Forge**: Prototype code where ordering shortcuts are acceptable; Specter does not hunt order ghosts in throwaway PoCs.

If the code assumes `Object.keys` returns insertion order across engines → `order`. If two threads race on the same field → `race`. If `ORDER BY` is missing but indexes exist → Sentinel for perf, `order` for correctness.

## Ordering Hazard Catalog

| Hazard | Where it hides | Failure mode |
|--------|----------------|--------------|
| Unordered-iteration reliance | `Object.keys`, `Set`, `Map` (cross-engine), `HashMap`, Python `dict` pre-3.7 | Different output per runtime / version |
| Sort-stability assumption | `Array.prototype.sort` pre-ES2019, `qsort`, some `ORDER BY` ties | Tie-breaker output flips between runs |
| Missing `ORDER BY` | SQL pagination, "latest N", report generation | Pages drift, duplicates or gaps under concurrent writes |
| Concurrent-write race with implicit order | Append-only log, event bus, shared counter | Events arrive in unexpected order; fan-out sees stale state |
| Read-your-write on eventual store | Replica read after primary write, S3, Cassandra QUORUM | User sees stale data immediately after their own write |
| Vector-clock / Lamport misuse | Distributed event ordering | Events ordered "correctly" per clock but causally wrong |
| Kafka partition-less ordering | Multi-partition topic with per-key ordering need | Per-entity events reorder across partitions |
| `forEach` with async | `array.forEach(async …)` | Tasks launch in order but complete unordered |
| JSON key ordering | Signature / hash input | Hash mismatch between serializers |

## Workflow

```
TRIAGE  →  map symptom: flaky result, cross-engine diff, stale read, ordering drift
        →  3 hypotheses: (iteration order) (sort stability) (missing ORDER BY or partition key) (eventual-consistency read)

SCAN    →  grep iteration: Object.keys, Object.values, Object.entries, .forEach, for..in
        →  grep SQL: SELECT ... LIMIT without ORDER BY, pagination without tiebreaker
        →  grep sort: .sort\(\) without comparator, qsort, unstable algorithms
        →  grep async: forEach\(.*async, for..in with await
        →  check Kafka/Kinesis partition keys; check read consistency level per query

ANALYZE →  for each site, prove or disprove the ordering guarantee
        →  check runtime: V8 > Node 12 maintains integer-key order, but cross-engine varies
        →  check DB: MySQL vs Postgres vs SQLite differ on implicit order
        →  check read-your-write: is the read issued against the same replica as the write?

SCORE   →  ordering bug causing duplicate charges or data loss → CRITICAL
        →  cross-engine UI drift → MEDIUM
        →  pagination with missing ORDER BY → HIGH (silent data loss on pagination)

REPORT  →  site, guarantee assumed, guarantee actual, Bad→Good, test suggestion
```

## Unordered-Iteration Examples

```ts
// Bad: Object.keys order is not contract — numeric keys sort ascending, strings by insertion (V8 quirk)
const config = { '1': 'a', '2': 'b', name: 'x' };
Object.keys(config); // ['1', '2', 'name'] — not insertion order

// Good: use Map when order matters
const config = new Map([['name', 'x'], ['1', 'a'], ['2', 'b']]);
[...config.keys()]; // ['name', '1', '2'] — guaranteed insertion order

// Bad: Set iteration cross-engine
for (const x of new Set(items)) { ... } // order differs across JS engines historically

// Good: explicit sort or explicit structure
for (const x of [...new Set(items)].sort()) { ... }
```

## Sort-Stability Example

```ts
// Bad: pre-ES2019 Array.sort was not stable; still unstable in some older engines
users.sort((a, b) => a.role.localeCompare(b.role));
// Ties on role have undefined relative order

// Good: explicit tiebreaker
users.sort((a, b) => a.role.localeCompare(b.role) || a.id - b.id);
```

SQL equivalent: always add a deterministic tiebreaker column (typically primary key).

```sql
-- Bad: LIMIT without ORDER BY — silent data loss on pagination
SELECT * FROM orders LIMIT 50 OFFSET 0;
SELECT * FROM orders LIMIT 50 OFFSET 50;   -- rows may repeat or vanish

-- Good: deterministic order
SELECT * FROM orders ORDER BY created_at DESC, id DESC LIMIT 50 OFFSET 0;

-- Better: keyset pagination — stable under concurrent writes
SELECT * FROM orders WHERE (created_at, id) < ($last_ts, $last_id) ORDER BY created_at DESC, id DESC LIMIT 50;
```

## Read-Your-Write Pattern

After a write, subsequent reads on eventually consistent stores may not see the write.

```ts
// Bad: write to primary, immediately read from any replica
await db.primary.insert('users', user);
const fresh = await db.replica.find('users', user.id); // may be null

// Good option A: sticky read — route to primary for a short TTL after write
await cache.set(`rw:${user.id}`, 'primary', 30);
const target = (await cache.get(`rw:${user.id}`)) === 'primary' ? db.primary : db.replica;

// Good option B: read from primary within session write window
const sessionWriteDeadline = Date.now() + 5000;
const target = Date.now() < sessionWriteDeadline ? db.primary : db.replica;

// Good option C: token-based consistency (wait until replica catches up)
const { writeToken } = await db.primary.insert(...);
await db.replica.waitForToken(writeToken);
```

Pick the pattern based on tolerable staleness and read volume.

## Concurrent-Write Implicit Ordering

```ts
// Bad: assume event bus delivers in enqueue order across partitions
bus.publish('order.created', { id: 1 });
bus.publish('order.paid',    { id: 1 }); // may arrive before 'created' on a different partition

// Good: partition by key
bus.publish('order.created', { id: 1 }, { partitionKey: 'order-1' });
bus.publish('order.paid',    { id: 1 }, { partitionKey: 'order-1' });
// Same partition → FIFO per key guaranteed
```

Kafka / Kinesis / SNS all require explicit partition / message-group keys for per-entity ordering.

## Anti-Patterns

- Relying on `Object.keys` / `JSON.stringify` for a stable signature without sorting keys.
- `SELECT … LIMIT N` without `ORDER BY` — silent data loss on pagination and parallel writes.
- `.forEach(async …)` expecting sequential execution — use `for..of` with `await`.
- Using `Set` iteration for user-visible UI ordering — cross-engine drift.
- Multi-partition Kafka topic for per-entity ordered events without partition key.
- Assuming replica reads see own writes — works on laptop, breaks in production.
- Unstable `sort()` with a comparator that returns 0 on equal fields — always add a tiebreaker.
- Vector-clock merge without causal-order verification — concurrent events get serialized arbitrarily.
- Using wall-clock timestamps as the sole ordering key across hosts — skew breaks it (see `time` recipe).

## Handoff

**To Builder** (fix in code):
- Ordering guarantee expected vs guarantee actual.
- Correct primitive (`Map` over `Object`, explicit `ORDER BY` + tiebreaker, partition key).
- Bad → Good snippet.
- Read-consistency strategy when eventual consistency is involved.

**To Radar** (test additions):
- Cross-engine iteration-order tests (if multi-runtime).
- Pagination-under-concurrent-write test.
- Read-your-write staleness test for replica reads.

**To Schema** (when ORDER BY / partition needs DB work):
- Index needed for `(sort_col, id)` keyset pagination.
- Partition key choice for event topics.

**To Specter `time`** (when ordering depends on clocks):
- Any ordering scheme using wall-clock timestamps across hosts → review for skew hazard.
