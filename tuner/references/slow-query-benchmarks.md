# Slow Query Analysis & Benchmarks

Purpose: Use this file when enabling slow-query logging, collecting top offenders, or benchmarking improvements.

Contents:

- PostgreSQL slow-query setup
- MySQL slow-query setup
- benchmark commands
- reporting link

## PostgreSQL Slow Queries

```sql
ALTER SYSTEM SET log_min_duration_statement = '1000';
ALTER SYSTEM SET log_statement = 'none';
SELECT pg_reload_conf();

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

On **PostgreSQL 18+**, `pg_stat_statements` adds the `wal_buffers_full` column and normalises `IN (...)` lists more aggressively (`https://www.data-bene.io/en/blog/cumulative-statistics-in-postgresql-18/`). Add `wal_buffers_full` to ordering when WAL pressure is the suspected bottleneck:

```sql
-- PG18+: surface WAL-buffer-pressured statements
SELECT query, calls, wal_buffers_full,
       round(total_exec_time::numeric / NULLIF(calls,0), 2) AS mean_ms
FROM pg_stat_statements
WHERE wal_buffers_full > 0
ORDER BY wal_buffers_full DESC
LIMIT 20;
```

Combine with `auto_explain` for plan capture — Datadog DBM and pganalyze both consume `auto_explain` output for post-hoc bottleneck attribution (`https://www.datadoghq.com/blog/database-monitoring-explain-analyze/`).

## MySQL Slow Queries

```sql
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;
SET GLOBAL log_queries_not_using_indexes = 'ON';

SELECT
    DIGEST_TEXT,
    COUNT_STAR,
    ROUND(SUM_TIMER_WAIT/1000000000000, 3) AS total_sec,
    ROUND(AVG_TIMER_WAIT/1000000000000, 3) AS avg_sec
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 20;
```

## Benchmarks

### PostgreSQL (`pgbench`)

```bash
pgbench -i -s 10 mydb
pgbench -c 10 -j 2 -T 60 -S mydb
pgbench -c 10 -j 2 -t 1000 -f custom_query.sql mydb
```

### MySQL (`sysbench`)

```bash
sysbench oltp_read_write --mysql-host=localhost --mysql-db=mydb --mysql-user=root --tables=10 --table-size=100000 prepare
sysbench oltp_read_write --mysql-host=localhost --mysql-db=mydb --mysql-user=root --threads=4 --time=60 run
sysbench oltp_read_write cleanup
```

## Reporting

Use [performance-report-template.md](~/.claude/skills/tuner/references/performance-report-template.md) for the canonical before/after report format.
