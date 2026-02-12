# Materialized Views & Table Partitioning

## Materialized Views

### When to Use

| Scenario | Use MV? | Reason |
|----------|---------|--------|
| Complex aggregation (daily/weekly) | ✅ Yes | Avoid repeated computation |
| Dashboard queries | ✅ Yes | Predictable, cacheable results |
| Real-time data | ❌ No | Staleness unacceptable |
| Infrequent queries | ❌ No | Storage overhead not justified |
| High-write tables | ⚠️ Depends | Refresh cost vs query benefit |

### PostgreSQL Materialized Views

```sql
-- Create materialized view for daily sales summary
CREATE MATERIALIZED VIEW mv_daily_sales AS
SELECT
    DATE(created_at) AS sale_date,
    product_id,
    SUM(quantity) AS total_quantity,
    SUM(amount) AS total_amount,
    COUNT(*) AS order_count
FROM orders
GROUP BY DATE(created_at), product_id
WITH DATA;

-- Create index on materialized view
CREATE INDEX idx_mv_daily_sales_date ON mv_daily_sales(sale_date);

-- Refresh strategies
-- Full refresh (blocks reads during refresh)
REFRESH MATERIALIZED VIEW mv_daily_sales;

-- Concurrent refresh (requires unique index)
CREATE UNIQUE INDEX idx_mv_daily_sales_pk ON mv_daily_sales(sale_date, product_id);
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_sales;

-- Check last refresh time (PostgreSQL 14+)
SELECT schemaname, matviewname,
       pg_catalog.pg_size_pretty(pg_relation_size(matviewname::regclass)) AS size
FROM pg_matviews
WHERE matviewname = 'mv_daily_sales';
```

### Refresh Strategies

| Strategy | Command | Use Case |
|----------|---------|----------|
| **Manual** | `REFRESH MATERIALIZED VIEW` | On-demand, after ETL |
| **Scheduled** | cron + psql | Regular intervals (hourly/daily) |
| **Trigger-based** | Custom function | Near real-time (complex) |
| **Concurrent** | `REFRESH CONCURRENTLY` | Zero-downtime refresh |

### Refresh Scheduling Example

```bash
# cron job for hourly refresh
0 * * * * psql -d mydb -c "REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_sales;"

# With logging
0 * * * * /usr/bin/psql -d mydb -c "REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_sales;" >> /var/log/mv_refresh.log 2>&1
```

### MySQL Alternative (Summary Tables)

```sql
-- MySQL doesn't have native materialized views
-- Use summary tables with scheduled refresh

CREATE TABLE summary_daily_sales (
    sale_date DATE PRIMARY KEY,
    product_id INT,
    total_quantity INT,
    total_amount DECIMAL(10,2),
    order_count INT,
    refreshed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY (sale_date, product_id)
);

-- Refresh procedure
DELIMITER //
CREATE PROCEDURE refresh_daily_sales()
BEGIN
    TRUNCATE TABLE summary_daily_sales;
    INSERT INTO summary_daily_sales (sale_date, product_id, total_quantity, total_amount, order_count)
    SELECT
        DATE(created_at),
        product_id,
        SUM(quantity),
        SUM(amount),
        COUNT(*)
    FROM orders
    GROUP BY DATE(created_at), product_id;
END //
DELIMITER ;

-- Schedule with MySQL Event Scheduler
CREATE EVENT refresh_daily_sales_event
ON SCHEDULE EVERY 1 HOUR
DO CALL refresh_daily_sales();
```

---

## Table Partitioning

### Partitioning Decision Matrix

| Table Size | Query Pattern | Partition? | Strategy |
|------------|---------------|------------|----------|
| < 10M rows | Any | ❌ No | Index optimization sufficient |
| 10M-100M | Time-based queries | ✅ Yes | Range by date |
| 10M-100M | Category-based queries | ✅ Yes | List by category |
| > 100M | Mixed patterns | ✅ Yes | Composite (range + list) |
| Any | Full table scans | ❌ No | Partitioning won't help |

### PostgreSQL Partitioning

```sql
-- Range partitioning by date (most common)
CREATE TABLE orders (
    id BIGSERIAL,
    user_id BIGINT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    amount DECIMAL(10,2),
    status VARCHAR(20)
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

CREATE TABLE orders_2024_q3 PARTITION OF orders
    FOR VALUES FROM ('2024-07-01') TO ('2024-10-01');

CREATE TABLE orders_2024_q4 PARTITION OF orders
    FOR VALUES FROM ('2024-10-01') TO ('2025-01-01');

-- Default partition for overflow
CREATE TABLE orders_default PARTITION OF orders DEFAULT;

-- Index on partitioned table (automatically created on each partition)
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_created_at ON orders(created_at);

-- List partitioning by category
CREATE TABLE products (
    id BIGSERIAL,
    name VARCHAR(255),
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10,2)
) PARTITION BY LIST (category);

CREATE TABLE products_electronics PARTITION OF products
    FOR VALUES IN ('electronics', 'computers', 'phones');

CREATE TABLE products_clothing PARTITION OF products
    FOR VALUES IN ('clothing', 'shoes', 'accessories');

CREATE TABLE products_other PARTITION OF products DEFAULT;
```

### Partition Maintenance

```sql
-- Create new partition before it's needed
CREATE TABLE orders_2025_q1 PARTITION OF orders
    FOR VALUES FROM ('2025-01-01') TO ('2025-04-01');

-- Detach old partition (for archiving)
ALTER TABLE orders DETACH PARTITION orders_2023_q1;

-- Archive to cold storage
-- (Move to slower/cheaper storage, compress, etc.)

-- Drop old partition (careful!)
DROP TABLE orders_2023_q1;

-- Check partition pruning in EXPLAIN
EXPLAIN (ANALYZE, COSTS)
SELECT * FROM orders
WHERE created_at >= '2024-07-01' AND created_at < '2024-08-01';
-- Should show only orders_2024_q3 partition being scanned
```

### MySQL Partitioning

```sql
-- Range partitioning in MySQL
CREATE TABLE orders (
    id BIGINT AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    created_at DATETIME NOT NULL,
    amount DECIMAL(10,2),
    PRIMARY KEY (id, created_at)  -- Partition key must be in PK
) PARTITION BY RANGE (YEAR(created_at) * 100 + MONTH(created_at)) (
    PARTITION p202401 VALUES LESS THAN (202402),
    PARTITION p202402 VALUES LESS THAN (202403),
    PARTITION p202403 VALUES LESS THAN (202404),
    PARTITION pmax VALUES LESS THAN MAXVALUE
);

-- Add new partition
ALTER TABLE orders ADD PARTITION (
    PARTITION p202404 VALUES LESS THAN (202405)
);

-- Reorganize default partition
ALTER TABLE orders REORGANIZE PARTITION pmax INTO (
    PARTITION p202404 VALUES LESS THAN (202405),
    PARTITION pmax VALUES LESS THAN MAXVALUE
);

-- Drop old partition
ALTER TABLE orders DROP PARTITION p202301;
```

### Partition Pruning Verification

```sql
-- PostgreSQL: Check partition pruning
EXPLAIN (ANALYZE)
SELECT COUNT(*) FROM orders
WHERE created_at BETWEEN '2024-07-01' AND '2024-07-31';

-- Look for:
-- "Append" node with only relevant partitions
-- NOT "Seq Scan on orders" (full table scan)

-- MySQL: Check partition pruning
EXPLAIN SELECT COUNT(*) FROM orders
WHERE created_at BETWEEN '2024-07-01' AND '2024-07-31';
-- Check 'partitions' column shows only relevant partitions
```

### Automated Partition Management

```sql
-- PostgreSQL: pg_partman extension (recommended)
-- Installation: CREATE EXTENSION pg_partman;

SELECT partman.create_parent(
    p_parent_table => 'public.orders',
    p_control => 'created_at',
    p_type => 'native',
    p_interval => 'monthly',
    p_premake => 3  -- Create 3 months ahead
);

-- Configure retention (auto-drop old partitions)
UPDATE partman.part_config
SET retention = '12 months',
    retention_keep_table = false
WHERE parent_table = 'public.orders';

-- Run maintenance (schedule via cron)
SELECT partman.run_maintenance();
```
