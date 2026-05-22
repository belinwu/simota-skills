# Database Monitoring & Observability

Purpose: Use this file when the task is ongoing DB monitoring, alert design, or observability-driven tuning.

Contents:
- five monitoring pillars
- `pg_stat_statements` vs `pg_stat_monitor`
- alert thresholds
- dashboard guidance

## Five Monitoring Pillars

| ID | Pillar | Key metrics |
|----|--------|-------------|
| `MO-01` | query performance | p50/p95/p99 latency, slow-query count, executions |
| `MO-02` | resource usage | CPU, memory, disk I/O |
| `MO-03` | connection management | active/idle connections, pool usage, waiters |
| `MO-04` | locks and contention | lock wait time, deadlocks, contention rate |
| `MO-05` | maintenance health | autovacuum, table bloat, index bloat |

## `pg_stat_statements` vs `pg_stat_monitor`

| Tool | Best use |
|------|----------|
| `pg_stat_statements` | long-term trend analysis |
| `pg_stat_monitor` | deeper real-time debugging and richer dimensions |

Recommended `pg_stat_statements` posture:
- enable via `shared_preload_libraries`
- keep `track = 'top'` unless deeper nesting is necessary
- size `pg_stat_statements.max` to fit memory budget
- on **PG18+**, `pg_stat_statements` exposes ≥ 45 columns including a new `wal_buffers_full` column, and `IN (...)` lists are normalised more aggressively — refresh dashboards that bucketed on `query` text (`https://www.data-bene.io/en/blog/cumulative-statistics-in-postgresql-18/`)

## AI-Assisted SQL Tuning Platforms (2026-05)

These platforms layer rule + ML-driven tuning on top of `pg_stat_statements` / auto_explain output. Use as recommendation engines feeding Tuner — never as a substitute for plan-evidence review.

| Platform | Specialisation | 2026 capability surface |
|----------|----------------|-------------------------|
| **pganalyze** | PostgreSQL-only; deep root-cause analysis | Query / Index / VACUUM Advisor, auto_explain integration with per-query trace correlation (`https://pganalyze.com/comparison/pganalyze-vs-datadog`) |
| **Datadog DBM** | Multi-engine; APM correlation | Auto-collects `EXPLAIN ANALYZE` for PostgreSQL, ingests auto_explain output, DBM Recommendations surface prioritised bottlenecks (`https://www.datadoghq.com/blog/database-monitoring-explain-analyze/`, `https://www.datadoghq.com/blog/database-monitoring-recommendations/`) |
| **EverSQL** (Datadog integration) | Automated SQL rewrite + index recommendation | One-click rewrite of slow queries surfaced in DBM (`https://docs.datadoghq.com/integrations/eversql/`) |
| **AWS DevOps Guru for RDS** | Aurora/RDS host-level ML | Anomaly detection on host metrics + slow query log; routes to Performance Insights |

Tuner contract: AI advisors generate **candidates**, not commitments. Always re-EXPLAIN against the actual workload, quantify the write overhead, and check adjacent queries for regression before accepting an AI-recommended index DDL.

## Alert Thresholds

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| query latency p95 | `> 500ms` | `> 2000ms` | investigate slow queries |
| connection usage | `> 80%` | `> 95%` | expand pool or find leaks |
| CPU usage | `> 75%` | `> 90%` | optimize workload or scale |
| memory usage | `> 80%` | `> 95%` | revisit memory settings |
| disk I/O latency | `> 10ms` | `> 50ms` | check indexes or storage |
| deadlocks | `> 0/hr` | `> 5/hr` | review transaction design |
| replication lag | `> 1s` | `> 10s` | inspect replica and network |
| table bloat | `> 20%` | `> 50%` | tune vacuum or reclaim space |
| autovacuum delay | `> 1hr` | `> 24hr` | tune autovacuum |
| unused index count | `> 5` | `> 20` | review removal candidates |

Operational quality gates:
- cache hit ratio `< 95%` -> revisit `shared_buffers` or indexing
- dead tuple ratio `> 20%` -> tune autovacuum

## Dashboard Guidance

Recommended panels:
- QPS and active connections
- p50/p95/p99 latency
- top slow queries
- cache hit ratio and disk I/O
- bloat and autovacuum status
- long transactions and deadlocks
