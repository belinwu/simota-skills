# Slow Query Analysis & Benchmark Templates

## Slow Query Analysis

### PostgreSQL Slow Query Log

```sql
-- Enable slow query logging
ALTER SYSTEM SET log_min_duration_statement = '1000';  -- Log queries > 1s
ALTER SYSTEM SET log_statement = 'none';  -- Only slow queries
SELECT pg_reload_conf();

-- Query pg_stat_statements (if enabled)
SELECT
    query,
    calls,
    round(total_exec_time::numeric, 2) AS total_ms,
    round(mean_exec_time::numeric, 2) AS mean_ms,
    round(stddev_exec_time::numeric, 2) AS stddev_ms,
    rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;
```

### MySQL Slow Query Log

```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;  -- Queries > 1s
SET GLOBAL log_queries_not_using_indexes = 'ON';

-- Query performance_schema
SELECT
    DIGEST_TEXT,
    COUNT_STAR,
    ROUND(SUM_TIMER_WAIT/1000000000000, 3) AS total_sec,
    ROUND(AVG_TIMER_WAIT/1000000000000, 3) AS avg_sec,
    SUM_ROWS_EXAMINED,
    SUM_ROWS_SENT
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 20;
```

### Slow Query Report Template

```markdown
## Slow Query Analysis Report

### Query Profile

| Metric | Value |
|--------|-------|
| Query | `SELECT ...` |
| Avg Execution Time | 2.5s |
| Calls per Day | 1,000 |
| Total Time per Day | 41 minutes |
| Rows Examined | 1,000,000 |
| Rows Returned | 10 |

### Execution Plan Analysis

\`\`\`
Seq Scan on users  (cost=0.00..50000.00 rows=1000000 width=100)
  Filter: (status = 'active')
  Rows Removed by Filter: 999990
\`\`\`

### Root Cause
- No index on `status` column
- Filter removes 99.999% of rows (extremely low selectivity after scan)

### Recommendations

1. **Add index** (High Impact)
   \`\`\`sql
   CREATE INDEX CONCURRENTLY idx_users_status ON users(status);
   \`\`\`

2. **Consider partial index** (If status='active' is common query)
   \`\`\`sql
   CREATE INDEX CONCURRENTLY idx_users_active
   ON users(id) WHERE status = 'active';
   \`\`\`

### Expected Improvement
- Execution time: 2.5s → 5ms (500x faster)
- Rows examined: 1M → 10 (100,000x fewer)
```

---

## Benchmark Templates

### PostgreSQL (pgbench)

```bash
# Initialize benchmark tables
pgbench -i -s 10 mydb

# Run read-only benchmark
pgbench -c 10 -j 2 -T 60 -S mydb

# Run custom query benchmark
pgbench -c 10 -j 2 -t 1000 -f custom_query.sql mydb

# custom_query.sql
\set user_id random(1, 100000)
SELECT * FROM orders WHERE user_id = :user_id ORDER BY created_at DESC LIMIT 10;
```

### MySQL (sysbench)

```bash
# Prepare
sysbench oltp_read_write \
  --mysql-host=localhost \
  --mysql-db=mydb \
  --mysql-user=root \
  --tables=10 \
  --table-size=100000 \
  prepare

# Run
sysbench oltp_read_write \
  --mysql-host=localhost \
  --mysql-db=mydb \
  --mysql-user=root \
  --threads=4 \
  --time=60 \
  run

# Cleanup
sysbench oltp_read_write cleanup
```

### Benchmark Report Template

```markdown
## Benchmark Results: [Test Name]

### Environment
| Item | Value |
|------|-------|
| Database | PostgreSQL 15 |
| CPU | 4 cores |
| RAM | 16GB |
| Storage | SSD |
| Data Size | 1M rows |

### Results

| Metric | Before | After | Δ |
|--------|--------|-------|---|
| TPS | 100 | 500 | +400% |
| Avg Latency | 50ms | 10ms | -80% |
| P99 Latency | 200ms | 30ms | -85% |
| CPU Usage | 80% | 40% | -50% |

### Observations
- Index on `user_id` improved TPS by 400%
- P99 latency reduced significantly
- CPU usage dropped due to fewer full table scans
```
