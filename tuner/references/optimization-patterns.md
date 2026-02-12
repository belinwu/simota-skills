# Query Optimization Patterns

## Common Rewrites

### N+1 → JOIN
```sql
-- Before (N+1)
SELECT * FROM orders WHERE user_id = ?; -- repeated N times

-- After (JOIN)
SELECT o.*, u.name FROM orders o JOIN users u ON o.user_id = u.id;
```

### Subquery → CTE
```sql
-- Before
SELECT * FROM orders WHERE user_id IN (SELECT id FROM users WHERE active);

-- After
WITH active_users AS (SELECT id FROM users WHERE active)
SELECT o.* FROM orders o JOIN active_users au ON o.user_id = au.id;
```

### OFFSET → Cursor Pagination
```sql
-- Before (slow for large offsets)
SELECT * FROM items ORDER BY id LIMIT 20 OFFSET 10000;

-- After (cursor-based)
SELECT * FROM items WHERE id > last_seen_id ORDER BY id LIMIT 20;
```

---

## N+1 Query Detection

### Pattern Detection
Look for:
- Multiple similar queries in sequence
- Loop-generated queries
- ORM lazy loading patterns

### Example (Bad)
```sql
-- Query 1: Get all orders
SELECT * FROM orders WHERE user_id = 1;

-- Query 2-N: Get items for each order (N times!)
SELECT * FROM order_items WHERE order_id = 101;
SELECT * FROM order_items WHERE order_id = 102;
SELECT * FROM order_items WHERE order_id = 103;
-- ... repeated N times
```

### Solution
```sql
-- Single query with JOIN
SELECT o.*, oi.*
FROM orders o
LEFT JOIN order_items oi ON o.id = oi.order_id
WHERE o.user_id = 1;

-- Or with IN clause
SELECT * FROM order_items
WHERE order_id IN (101, 102, 103, ...);
```

---

## Missing Index Detection

```sql
-- PostgreSQL: Find missing indexes
SELECT
    schemaname || '.' || relname AS table,
    seq_scan,
    seq_tup_read,
    idx_scan,
    CASE
        WHEN seq_scan > 0
        THEN round(seq_tup_read::numeric / seq_scan, 2)
        ELSE 0
    END AS avg_seq_tup_read
FROM pg_stat_user_tables
WHERE seq_scan > 100  -- Tables with many seq scans
AND seq_tup_read / GREATEST(seq_scan, 1) > 1000  -- Reading many rows per scan
ORDER BY seq_tup_read DESC
LIMIT 20;

-- MySQL: Tables without indexes being used
SELECT
    t.TABLE_SCHEMA,
    t.TABLE_NAME,
    t.TABLE_ROWS,
    IFNULL(i.index_count, 0) AS index_count
FROM information_schema.TABLES t
LEFT JOIN (
    SELECT TABLE_SCHEMA, TABLE_NAME, COUNT(*) AS index_count
    FROM information_schema.STATISTICS
    GROUP BY TABLE_SCHEMA, TABLE_NAME
) i ON t.TABLE_SCHEMA = i.TABLE_SCHEMA AND t.TABLE_NAME = i.TABLE_NAME
WHERE t.TABLE_TYPE = 'BASE TABLE'
AND t.TABLE_ROWS > 10000
AND IFNULL(i.index_count, 0) < 2
ORDER BY t.TABLE_ROWS DESC;
```

## Unused Index Detection

```sql
-- PostgreSQL: Find unused indexes
SELECT
    schemaname || '.' || relname AS table,
    indexrelname AS index,
    pg_size_pretty(pg_relation_size(indexrelid)) AS size,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0
AND indexrelname NOT LIKE '%_pkey'  -- Exclude primary keys
ORDER BY pg_relation_size(indexrelid) DESC;

-- MySQL: Unused indexes (requires performance_schema)
SELECT
    object_schema,
    object_name AS table_name,
    index_name,
    count_read,
    count_write
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE index_name IS NOT NULL
AND count_read = 0
AND object_schema NOT IN ('mysql', 'performance_schema')
ORDER BY count_write DESC;
```

---

## Index Recommendation Template

```markdown
## Index Recommendation: [Table].[Column(s)]

### Problem
- Query: `SELECT ... FROM table WHERE column = ?`
- Current plan: Sequential Scan
- Rows scanned: 1,000,000
- Execution time: 2.5s

### Proposed Index
\`\`\`sql
CREATE INDEX CONCURRENTLY idx_table_column
ON table (column);
\`\`\`

### Expected Improvement
- Plan change: Seq Scan → Index Scan
- Estimated rows scanned: 100
- Expected execution time: 5ms

### Trade-offs
- Disk space: ~50MB
- Write overhead: ~5% on INSERT/UPDATE
- Maintenance: Included in regular VACUUM

### Validation Query
\`\`\`sql
EXPLAIN ANALYZE
SELECT ... FROM table WHERE column = ?;
-- Verify Index Scan is used
\`\`\`
```
