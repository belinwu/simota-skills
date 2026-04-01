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

## Connection Pooler Comparison (2025)

### PgBouncer vs Supavisor vs PgCat

| Feature | PgBouncer | Supavisor | PgCat |
|---------|-----------|-----------|-------|
| Language | C | Elixir | Rust |
| Architecture | Single-process | Distributed (OTP) | Multi-process |
| Modes | Session / Transaction / Statement | Transaction | Session / Transaction |
| Multi-tenant | Manual (per-database config) | Native (tenant isolation) | Native (sharding) |
| Serverless support | Limited | Excellent (HTTP/WebSocket) | Limited |
| HTTP connections | No | Yes | No |
| WebSocket connections | No | Yes | No |
| Sharding | No | No | Yes (built-in) |
| Performance (50+ connections) | Good | Good | Best |
| Observability | Basic metrics | Prometheus native | Prometheus native |
| Cloud integration | Self-hosted | Supabase native | Self-hosted |

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
