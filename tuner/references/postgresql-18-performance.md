# PostgreSQL 18 Performance Features

Purpose: Use this file when working with PostgreSQL 18 features, planning upgrades, or leveraging new performance capabilities.

Contents:
- AIO subsystem
- pg_stat_io enhancements
- WAL I/O tracking
- per-backend I/O functions
- Merge Join improvements
- Multicolumn B-tree Skip Scan
- Migration checklist

---

## AIO Subsystem

PostgreSQL 18 introduces a native Asynchronous I/O subsystem that replaces the previous synchronous pread/pwrite calls.

### Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `io_method` | `worker` | I/O method: `sync`, `worker`, or `io_uring` (Linux only) |
| `io_combine_limit` | `128kB` | Maximum bytes combined into a single I/O operation |

### Recommended Settings

```sql
-- For NVMe storage (Linux)
io_method = 'io_uring'
io_combine_limit = '256kB'

-- For general use
io_method = 'worker'
io_combine_limit = '128kB'
```

### Expected Impact

- Sequential scan throughput: 20-40% improvement on NVMe with `io_uring`
- Checkpoint I/O: reduced stall during heavy write workloads
- Parallel query I/O: improved utilization of parallel workers

---

## pg_stat_io Enhancements

PostgreSQL 18 adds byte-level statistics to `pg_stat_io`, enabling precise I/O accounting.

### New Columns

| Column | Type | Description |
|--------|------|-------------|
| `read_bytes` | bigint | Total bytes read |
| `write_bytes` | bigint | Total bytes written |
| `extend_bytes` | bigint | Total bytes written to extend relations |

### Useful Queries

```sql
-- I/O breakdown by backend type
SELECT backend_type, context,
       read_bytes / 1024 / 1024 AS read_mb,
       write_bytes / 1024 / 1024 AS write_mb,
       hits, reads, writes
FROM pg_stat_io
ORDER BY read_bytes + write_bytes DESC;

-- Compare cache hit ratio with byte volume
SELECT backend_type,
       hits::float / NULLIF(hits + reads, 0) AS hit_ratio,
       read_bytes / 1024 AS read_kb
FROM pg_stat_io
WHERE context = 'normal';
```

---

## WAL I/O Tracking

`pg_stat_io` now tracks WAL write activity separately, enabling WAL tuning based on measured throughput.

```sql
-- WAL I/O statistics
SELECT backend_type, context,
       write_bytes / 1024 / 1024 AS wal_write_mb,
       writes AS wal_writes
FROM pg_stat_io
WHERE object = 'wal';
```

---

## Per-Backend I/O Function

```sql
-- pg_stat_get_backend_io(pid) — new in PostgreSQL 18
SELECT * FROM pg_stat_get_backend_io(pg_backend_pid());

-- Check I/O for a specific backend
SELECT pid, read_bytes, write_bytes
FROM pg_stat_activity
CROSS JOIN LATERAL pg_stat_get_backend_io(pid)
WHERE state = 'active';
```

Use this for live debugging of slow queries on specific connections.

---

## Merge Join: Incremental Sort Support

PostgreSQL 18 allows Merge Join to leverage Incremental Sort, removing the requirement for full pre-sort.

### Impact

- Queries with partial sort keys: 30-50% improvement in elapsed time
- Reduces sort spill-to-disk risk on large joins

### Verification

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT a.id, b.value
FROM table_a a
JOIN table_b b ON a.id = b.a_id
ORDER BY a.category, a.id;
-- Look for "Incremental Sort" above "Merge Join" in the plan
```

---

## Multicolumn B-tree Skip Scan

PostgreSQL 18 introduces Skip Scan for B-tree indexes, enabling index usage even when the leading column is not in the WHERE clause.

### Before (PostgreSQL 17 and earlier)

```sql
-- Index: (status, created_at)
-- Query: WHERE created_at > '2025-01-01'
-- Result: Sequential Scan (leading column 'status' not present)
```

### After (PostgreSQL 18)

```sql
-- Same index, same query
-- Result: Index Scan with Skip Scan on 'status' values
-- Effective when 'status' has low cardinality (< ~100 distinct values)
```

### When Skip Scan Helps

| Leading column cardinality | Skip Scan benefit |
|---------------------------|-------------------|
| < 10 distinct values | High — strongly recommended |
| 10–100 distinct values | Moderate |
| > 100 distinct values | Low — consider redesigning index |

### Verification

```sql
SET enable_skipscan = on; -- default in PG18
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders WHERE created_at > now() - interval '7 days';
-- Look for "Skip Scan" in Index Scan node
```

---

## Migration Checklist

When upgrading from PostgreSQL 17 to 18:

### Pre-Upgrade

- [ ] Run `pg_upgrade --check` to identify incompatibilities
- [ ] Review indexes on columns with low-cardinality leading keys — Skip Scan may change plan choices
- [ ] Audit `io_method` setting for your OS/storage type
- [ ] Benchmark `pg_stat_io` baseline on PG17 for comparison

### Post-Upgrade

- [ ] Enable `io_uring` if running on Linux with kernel ≥ 5.19 and NVMe storage
- [ ] Re-run `ANALYZE` on large tables to refresh planner statistics
- [ ] Monitor `pg_stat_io.read_bytes` to confirm I/O improvement
- [ ] Check Merge Join plans for Incremental Sort adoption
- [ ] Validate Skip Scan behavior for multicolumn indexes with low-cardinality leading columns
- [ ] Update monitoring dashboards to include `read_bytes`, `write_bytes` columns

### Incompatibilities to Watch

- `io_uring` requires Linux kernel ≥ 5.19; fall back to `worker` on older kernels
- Skip Scan may change query plans — verify regressions with `EXPLAIN (ANALYZE, BUFFERS)`
- `pg_stat_io` schema changes require monitoring query updates
