# EXPLAIN ANALYZE Guide

## Reading Execution Plans

Key metrics:
- **Actual Time:** Real execution time (ms)
- **Rows:** Actual vs estimated rows
- **Loops:** Number of iterations
- **Buffers:** Shared hit/read counts

## Common Node Types

| Node | Meaning | Concern |
|------|---------|---------|
| Seq Scan | Full table scan | Missing index |
| Index Scan | Index lookup | Good |
| Index Only Scan | Covered by index | Best |
| Nested Loop | Row-by-row join | OK for small sets |
| Hash Join | Hash-based join | Good for large sets |
| Sort | In-memory/disk sort | Check work_mem |

## Red Flags
- Seq Scan on large tables
- Estimated vs actual rows differ > 10x
- Sort using disk (external merge)
- Nested Loop with large outer set

---

## EXPLAIN Commands by Database

### PostgreSQL

```sql
-- Basic EXPLAIN
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- With execution statistics
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Detailed output (recommended for analysis)
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT * FROM users WHERE email = 'test@example.com';

-- Without actually executing (for dangerous queries)
EXPLAIN (COSTS, VERBOSE)
SELECT * FROM users WHERE email = 'test@example.com';
```

### MySQL

```sql
-- Basic EXPLAIN
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- Extended format
EXPLAIN FORMAT=JSON SELECT * FROM users WHERE email = 'test@example.com';

-- With actual execution (MySQL 8.0.18+)
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Show warnings after EXPLAIN
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
SHOW WARNINGS;
```

### SQLite

```sql
-- Query plan
EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = 'test@example.com';

-- Detailed bytecode (advanced)
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
```

---

## Execution Plan Analysis

### Key Metrics

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| **Seq Scan** | Small tables (<1K rows) | Medium tables | Large tables |
| **Index Scan** | Always preferred | - | - |
| **Nested Loop** | Small inner tables | Medium tables | Large tables both |
| **Hash Join** | Equal-sized tables | Very large hash | Memory exceeded |
| **Sort** | Uses index | Disk sort | Very large sort |
| **Rows** | Close to actual | 10x difference | 100x+ difference |

### Plan Node Types (PostgreSQL)

```markdown
## Sequential Scan (Seq Scan)
- Full table scan
- Warning: Table > 10K rows
- Fix: Add appropriate index

## Index Scan
- Uses index to find rows
- Best for selective queries
- Check: Index actually being used

## Index Only Scan
- Data retrieved from index alone
- Best possible scenario
- Requires VACUUM for visibility map

## Bitmap Index Scan
- Creates bitmap from index
- Good for: OR conditions, multiple indexes
- Watch: Recheck condition

## Nested Loop
- For each outer row, scan inner
- Good when: Inner is small/indexed
- Bad when: Both sides large

## Hash Join
- Builds hash table from one side
- Good for: Large equal joins
- Watch: work_mem usage

## Merge Join
- Both sides sorted, merge
- Good for: Large sorted datasets
- Requires: Both sides sorted
```

### Red Flags in Execution Plans

```markdown
## CRITICAL
- Seq Scan on table > 100K rows
- Nested Loop with large tables
- "Sort Method: external merge Disk"
- Rows estimate off by 100x+

## WARNING
- Bitmap Heap Scan with high "Recheck Cond" rows
- Hash Join with "Batches: X" (spilling to disk)
- Filter removing > 90% of rows
- Multiple sequential scans in one query

## GOOD SIGNS
- Index Only Scan
- Rows actual ≈ Rows estimated
- "Heap Fetches: 0" for Index Only Scan
- Small actual time values
```
