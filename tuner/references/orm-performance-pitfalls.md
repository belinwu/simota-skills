# ORM Performance Pitfalls

Purpose: Use this file when the bottleneck sits in ORM-generated SQL, hydration, serialization, or ORM choice.

Contents:
- `OP-01..08`
- ORM comparison
- raw-SQL switch criteria
- review checklist

## ORM Pitfalls

| ID | Pitfall | Typical ORM | Response |
|----|---------|-------------|----------|
| `OP-01` | object hydration cost | TypeORM, Sequelize | use raw SQL or lighter mapping for large result sets |
| `OP-02` | cold-start delay | Prisma | measure serverless overhead, often around `300ms` |
| `OP-03` | serialization overhead | Prisma | re-measure on high-throughput endpoints |
| `OP-04` | lazy-loading trap | all ORMs | use explicit eager loading |
| `OP-05` | production `synchronize: true` | TypeORM | forbid in production |
| `OP-06` | over-fetching | all ORMs | use explicit `select` |
| `OP-07` | over-wide transaction scope | all ORMs | shrink transaction boundaries |
| `OP-08` | false type-safety assumptions | TypeORM and similar | validate runtime behavior |

## ORM Comparison

| ORM | Strength | Risk |
|-----|----------|------|
| Drizzle | lightweight, predictable SQL, good for serverless | fewer guardrails against N+1 |
| Prisma | excellent DX and type safety | `~300ms` cold start, serialization cost, SQL may need review |
| TypeORM | flexible patterns | hydration cost, weaker type guarantees, lower maintenance confidence |
| Sequelize | legacy reach | heaviest hydration, weaker TS support |

General performance order for CRUD-heavy paths:

```text
Drizzle ≈ raw SQL > Prisma > TypeORM > Sequelize
```

## When to Switch to Raw SQL

- analytical queries with many joins, grouping, or window functions
- bulk operations on `10,000+` rows
- DB-specific features the ORM cannot express well
- serverless paths where Prisma-like cold start matters
- high-throughput APIs around `1000+ RPS`

Recommended hybrid:
- CRUD -> ORM
- reporting and analytics -> raw SQL
- bulk operations -> raw SQL or DB-native bulk tools

## Review Checklist

- `findMany()` or equivalent uses explicit `select`
- relations use eager loading where appropriate
- no DB query runs inside loops
- transaction scope is minimal
- ORM bulk writes are not used for `10,000+` row operations
- production does not use `synchronize: true`
- generated SQL is reviewed with `EXPLAIN ANALYZE`

---

## Prisma 7 Architecture Changes (2025)

Prisma 7 replaced the Rust-based query engine with a TypeScript/WASM implementation, significantly reducing bundle size and cold-start overhead.

### Performance Impact

| Metric | Prisma 6 (Rust engine) | Prisma 7 (WASM) | Change |
|--------|------------------------|-----------------|--------|
| Bundle size | ~14MB | ~1.6MB | -89% |
| Cold start (serverless) | ~1500ms | ~115ms | -92% |
| Query speed (CRUD) | baseline | ~3.4x faster | +240% |
| Memory footprint | Higher (native binary) | Lower (WASM) | Reduced |

### Migration Notes

```typescript
// Prisma 7: no separate binary download required
// The WASM engine is bundled with the package

// Edge runtime support (Cloudflare Workers, Vercel Edge)
import { PrismaClient } from '@prisma/client/edge'

// Standard usage unchanged
const prisma = new PrismaClient()
```

**Key behavioral changes in Prisma 7:**
- No `prisma generate` binary side-effects on cold starts
- `datasourceUrl` can be set per-query (multi-tenant patterns simplified)
- `$transaction` API unchanged
- D1 (Cloudflare) driver adapter now stable

---

## Drizzle ORM Performance Characteristics

Drizzle is a lightweight TypeScript ORM designed for predictable SQL generation and serverless performance.

### Key Metrics

| Metric | Value |
|--------|-------|
| Bundle size | ~57KB |
| Cold start (serverless) | ~75ms |
| SQL predictability | High (1:1 mapping to generated SQL) |
| N+1 risk | Low with Relational Queries API |

### Drizzle Relational Queries: Structural N+1 Elimination

Drizzle's Relational Queries API generates a single SQL statement (or minimal JOIN query) for nested relations, structurally preventing N+1.

```typescript
// N+1 risk pattern (avoid)
const users = await db.select().from(usersTable);
for (const user of users) {
  const posts = await db.select().from(postsTable)
    .where(eq(postsTable.userId, user.id));
}

// Drizzle Relational Queries (N+1 free)
const usersWithPosts = await db.query.users.findMany({
  with: {
    posts: true,
  },
});
// Generates: SELECT + single JOIN or 2 queries with IN clause
```

---

## ORM Selection Comparison (2025)

| ORM | Bundle | Cold Start | Query Speed | N+1 Safety | Type Safety | Best For |
|-----|--------|-----------|-------------|------------|-------------|----------|
| Drizzle | 57KB | ~75ms | Fastest (≈ raw SQL) | High (Relational API) | Excellent | Serverless, edge, performance-critical |
| Prisma 7 | 1.6MB | ~115ms | Fast (3.4x vs Prisma 6) | Good (include) | Excellent | Full-stack, DX-focused, rapid development |
| TypeORM | ~5MB | ~300ms | Moderate | Poor (lazy default) | Moderate | Legacy, enterprise patterns |
| Sequelize | ~10MB | ~400ms | Slow | Poor | Weak | Legacy Node.js projects |

**General performance order (2025):**

```text
Drizzle ≈ raw SQL > Prisma 7 >> TypeORM > Sequelize
```

**Decision guide:**
- Serverless / edge: Drizzle (bundle size + cold start)
- Rapid development / strong DX: Prisma 7
- N+1-critical reporting: Drizzle Relational Queries or raw SQL
- Legacy TypeORM migration: evaluate Prisma 7 or Drizzle
