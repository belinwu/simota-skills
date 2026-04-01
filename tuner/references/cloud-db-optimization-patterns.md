# Cloud DB Optimization Patterns

Purpose: Use this file when optimizing queries for cloud-managed databases (Aurora, Neon, PlanetScale) or selecting a cloud DB for a project.

Contents:
- Aurora: QPM and query plan management
- Neon: cold start optimization
- PlanetScale: NVMe Metal performance
- Cloud DB selection comparison
- Migration considerations

---

## Aurora: Query Plan Management (QPM)

Aurora PostgreSQL uses `apg_plan_mgmt` for Query Plan Management, preventing plan regression when the optimizer changes plans.

### Version: apg_plan_mgmt v2.9 (Aurora PostgreSQL 16.x+)

```sql
-- Enable QPM
SET rds.force_admin_logging_level = 'debug5';
LOAD 'apg_plan_mgmt';

-- Capture current plans
SELECT apg_plan_mgmt.capture_plan_baselines('automatic');

-- View managed plans
SELECT * FROM apg_plan_mgmt.dba_plans
ORDER BY plan_created DESC;
```

### aurora_stat_plans

`aurora_stat_plans` extends `pg_stat_statements` with plan-level statistics unique to Aurora.

```sql
-- Plans with highest total cost
SELECT queryid, planid,
       total_time / calls AS avg_ms,
       plan_hash,
       calls
FROM aurora_stat_plans
ORDER BY total_time DESC
LIMIT 20;

-- Detect plan changes for a specific query
SELECT queryid, planid, plan_created, calls
FROM aurora_stat_plans
WHERE queryid = '<target_queryid>'
ORDER BY plan_created DESC;
```

### Reader Instance Optimization

```sql
-- Route read-only queries to Reader endpoint
-- Application connection string pattern:
-- writer: cluster-xxx.cluster-rds.amazonaws.com
-- reader: cluster-xxx.cluster-ro-rds.amazonaws.com

-- Identify read-heavy queries for reader offload
SELECT query, calls, total_time / calls AS avg_ms
FROM pg_stat_statements
WHERE query NOT ILIKE '%insert%'
  AND query NOT ILIKE '%update%'
  AND query NOT ILIKE '%delete%'
ORDER BY calls DESC
LIMIT 20;
```

### Aurora-Specific Settings

| Parameter | Recommended | Notes |
|-----------|-------------|-------|
| `apg_plan_mgmt.capture_plan_baselines` | `automatic` | Auto-capture for all queries |
| `apg_plan_mgmt.use_plan_baselines` | `true` | Enforce captured plans |
| `apg_plan_mgmt.plan_retention_period` | `32` days | Adjust based on workload stability |
| `aurora_max_babelfish_tds_connections` | — | Only for Babelfish; irrelevant for standard PG |

---

## Neon: Cold Start Optimization

Neon uses a serverless architecture with compute auto-suspend. Cold starts occur when a suspended compute resumes.

### Cold Start Baseline

| Scenario | Typical Latency |
|----------|----------------|
| Compute suspended (auto-suspend) | 300–500ms |
| Warm compute | < 5ms |
| Connection pool (Pooled mode) | < 20ms via Neon proxy |

### Reducing Cold Start Impact

**1. Disable auto-suspend for latency-sensitive workloads**

```bash
# Neon CLI
neon projects update <project-id> --suspend-timeout 0
# Or set via Neon Console: Project Settings → Compute → Auto-suspend timeout
```

**2. Use Pooled Connection Mode**

```
# Direct connection (cold start possible)
postgresql://user:pass@ep-xxx.neon.tech/dbname

# Pooled connection (Neon proxy manages pool, no cold start for pool)
postgresql://user:pass@ep-xxx-pooler.neon.tech/dbname?pgbouncer=true
```

**3. Keep-alive Pattern (for serverless functions)**

```typescript
// Warm the connection before the critical path
export async function warmDb(sql: NeonQueryFunction) {
  await sql`SELECT 1`;
}

// Call at function init (outside handler)
const warmPromise = warmDb(sql);
export async function handler(event) {
  await warmPromise; // ensures warm connection
  // ... actual query
}
```

### Copy-on-Write (CoW) Branching

Neon's CoW architecture enables instant database branches for development and testing.

```bash
# Create a branch from production snapshot
neon branches create --name preview/feature-xyz --parent main

# Use branch connection string
neon connection-string preview/feature-xyz
```

**Use cases:**
- Preview environments per PR: ~0ms branch creation
- Load testing against production data snapshot
- Schema migration testing before applying to main

---

## PlanetScale: NVMe Metal Performance

PlanetScale (MySQL-compatible) runs on NVMe-backed bare metal, offering predictable low-latency for high-throughput OLTP.

### Performance Characteristics

| Metric | Typical Value |
|--------|---------------|
| Query latency (simple SELECT) | 1–3ms |
| Write throughput (single shard) | 10K–50K QPS |
| Connection overhead | Low (Vitess connection pooling) |
| Storage I/O | NVMe, local (not network-attached) |

### Vitess Query Optimization

PlanetScale uses Vitess under the hood. Key patterns:

```sql
-- Always use shard key in WHERE clause for cross-shard query avoidance
-- Shard key is typically the primary key or a defined vindex

-- Good: hits single shard
SELECT * FROM orders WHERE user_id = 12345 LIMIT 10;

-- Problematic: scatter query (hits all shards)
SELECT COUNT(*) FROM orders WHERE status = 'pending';
```

### Schema Change Safety

```sql
-- PlanetScale uses gh-ost for non-blocking schema changes
-- Deploy requests handle schema migrations — no direct DDL in production
-- Always test schema changes on a branch first
```

---

## Cloud DB Selection Comparison

| Criteria | Aurora PostgreSQL | Neon | PlanetScale |
|----------|-------------------|------|-------------|
| Engine | PostgreSQL-compatible | PostgreSQL | MySQL (Vitess) |
| Scaling model | Vertical (instance) + Read replicas | Serverless (auto-scale) | Horizontal (sharding via Vitess) |
| Cold start | None (always-on) | 300–500ms (suspendable) | None |
| Cost model | Instance + storage | Compute-seconds + storage | Row-reads + storage |
| Best for | Enterprise, steady high traffic | Serverless, dev/test, variable load | High-throughput OLTP, sharding |
| Branching | Snapshot clone (minutes) | Instant CoW branch | Schema branch (deploy requests) |
| Connection pooling | RDS Proxy (PgBouncer-compatible) | Neon Proxy (built-in pooler) | Vitess (built-in) |
| Multi-region | Global Database (active-active) | Read replicas (beta) | Not native |
| Max connections | ~5000 (via RDS Proxy) | ~10000 (pooled) | Vitess-managed |
| Migration tooling | pg_upgrade, DMS | pg_dump, logical replication | Planetscale CLI, deploy requests |

---

## Migration Considerations

### Migrating to Aurora PostgreSQL

```bash
# Use AWS DMS for online migration
# Or pg_dump/restore for offline migration

# Key checks pre-migration:
# 1. Aurora-incompatible extensions (check aws.extensions)
# 2. Sequence max values (Aurora uses different sequence backend)
# 3. Partitioning behavior (Aurora adds aurora_partition_advisor)
# 4. Custom pg_hba.conf entries (managed by RDS)
```

### Migrating to Neon

```bash
# pg_dump from source
pg_dump -Fc --no-acl --no-owner \
  -h source-host -U source-user source-db > backup.dump

# Restore to Neon
pg_restore -Fc --no-acl --no-owner \
  -d "postgresql://user:pass@ep-xxx.neon.tech/neondb" backup.dump

# Enable logical replication for live migration (Neon supports it)
# Source: set wal_level = logical, max_replication_slots >= 1
```

### Common Migration Pitfalls

| Issue | Aurora | Neon | PlanetScale |
|-------|--------|------|-------------|
| Extensions not supported | `uuid-ossp` (use `gen_random_uuid()`) | PostGIS (check version) | MySQL-only extensions |
| Connection limits | Higher with RDS Proxy | Use pooled endpoint | Vitess handles |
| Prepared statements | Supported | Supported (use `neon` driver) | Limited in sharded setup |
| `LISTEN/NOTIFY` | Supported | Not supported (serverless) | Not supported (MySQL) |
| Transaction semantics | Standard PostgreSQL | Standard PostgreSQL | MySQL MVCC |
