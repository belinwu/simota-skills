# Connection Pool Tuning

Purpose: Use this file when the issue is connection pressure, pool sizing, or wait-event diagnosis.

Contents:
- sizing formula
- PostgreSQL settings
- monitoring queries

## Pool Size Formula

```text
pool_size = (core_count * 2) + effective_spindle_count
```

Typical range: `10-20` connections for many applications, but validate against workload and DB limits.

## Key PostgreSQL Settings

- `max_connections`
- `work_mem`
- `shared_buffers`
- `effective_cache_size`

## Monitoring

```sql
SELECT count(*) FROM pg_stat_activity WHERE state = 'active';
SELECT count(*) FROM pg_stat_activity WHERE state = 'idle';
SELECT wait_event_type, count(*) FROM pg_stat_activity GROUP BY 1;
```

---

## Connection Pooler Comparison (2026-05)

### PgBouncer vs Supavisor vs PgCat

| Feature | PgBouncer | Supavisor | PgCat |
|---------|-----------|-----------|-------|
| Language | C | Elixir (OTP) | Rust |
| Architecture | Single-process | Distributed (OTP) | Multi-process |
| Modes | Session / Transaction / Statement | Session (port 5432) / Transaction (port 6543) | Session / Transaction |
| Prepared statements in transaction mode | **Enabled by default since 1.24.0 (2025-01)** with `max_prepared_statements = 200` (`https://www.crunchydata.com/blog/prepared-statements-in-transaction-mode-for-pgbouncer`); originally added in 1.21 (`https://pganalyze.com/blog/5mins-postgres-pgbouncer-prepared-statements-transaction-mode`) | Named prepared statement support since Supavisor 1.0 | Supported |
| Multi-tenant | Manual (per-database config) | Native (tenant isolation) | Native (sharding) |
| Serverless support | Limited | Excellent (HTTP/WebSocket) | Limited |
| HTTP connections | No | Yes | No |
| WebSocket connections | No | Yes | No |
| Sharding | No | No | Yes (built-in) |
| Performance (50+ connections) | Good | Good (proxies millions of client conns into a stateful native PG pool) | Best |
| Observability | Basic metrics | Prometheus native | Prometheus native |
| Cloud integration | Self-hosted | Supabase native, integrates with Prisma/Drizzle/Psycopg | Self-hosted |

**2026-05 update**: `max_prepared_statements > 0` is now the **PgBouncer 1.24+ default**, which removes the historical silent re-parse penalty for JDBC/asyncpg/pg-protocol-binary clients in transaction mode. Audit any PgBouncer install on `<1.24` and either upgrade or explicitly set `max_prepared_statements = 200`.

**Supavisor port convention** (Supabase, in effect since 2025-02-28): port `5432` is session mode and port `6543` is transaction mode. The legacy session-mode-on-6543 layout was deprecated. Update connection strings before assuming the historical mapping.

### When to Use Each

| Use Case | Recommended | Reason |
|----------|-------------|--------|
| Serverless / edge functions | Supavisor | HTTP/WebSocket, no persistent TCP required |
| Multi-tenant SaaS | Supavisor | Tenant isolation, per-tenant pool |
| High connection count (50+) | PgCat | Lower latency per connection at scale |
| Sharded PostgreSQL | PgCat | Built-in shard routing |
| Traditional server deployment | PgBouncer | Battle-tested, simple configuration |
| Supabase hosted | Supavisor | Already integrated in Supabase platform |

### Supavisor Configuration Patterns

```toml
# supavisor.toml — multi-tenant example
[global]
proxy_port = 5432

[[tenants]]
id = "tenant_123"
db_host = "db.tenant-123.example.com"
db_port = 5432
db_name = "postgres"
pool_size = 10
mode = "transaction"
```

### PgCat Configuration Patterns

```toml
# pgcat.toml — sharding example
[general]
host = "0.0.0.0"
port = 5432
pool_size = 20

[pools.mydb]
mode = "transaction"
default_role = "any"

[pools.mydb.shards.0]
database = "shard0"
servers = [["shard0-db.internal", 5432, "primary"]]

[pools.mydb.shards.1]
database = "shard1"
servers = [["shard1-db.internal", 5432, "primary"]]
```

---

## PostgREST Pool Size Rule

When using PostgREST alongside a connection pooler:

```text
PostgREST pool size ≤ (pooler max_connections) / (number of PostgREST instances)
```

- PostgREST opens one connection per pool slot at startup
- Exceeding pooler limits causes connection exhaustion
- Recommended: set `db-pool` in PostgREST config to `(max_connections * 0.8) / instances`

```ini
# postgrest.conf
db-pool = 10                          # per instance
db-pool-acquisition-timeout = 10      # seconds to wait for a pool slot
db-pool-max-lifetime = 1800           # recycle connections every 30 min
```
