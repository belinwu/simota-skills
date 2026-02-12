# N+1 Detection, Cache Integration & ORM Optimization

## N+1 Query Auto-Detection

### Log Pattern Analysis

**Rails ActiveRecord:**
```
# N+1 Pattern in logs
Started GET "/orders" for 127.0.0.1
Processing by OrdersController#index
  Order Load (0.5ms)  SELECT "orders".* FROM "orders"
  User Load (0.3ms)  SELECT "users".* FROM "users" WHERE "users"."id" = 1
  User Load (0.3ms)  SELECT "users".* FROM "users" WHERE "users"."id" = 2
  User Load (0.3ms)  SELECT "users".* FROM "users" WHERE "users"."id" = 3
  # ... repeated N times
Completed 200 OK in 2500ms
```

**Detection Command:**
```bash
# Find repeated SELECT patterns
grep -oP 'SELECT.*FROM.*WHERE.*id = \d+' rails.log | \
  sed 's/id = [0-9]*/id = ?/' | \
  sort | uniq -c | sort -rn | head -20

# Output interpretation:
#  50 SELECT "users".* FROM "users" WHERE "users"."id" = ?
#     ↑ N+1 detected: 50 identical queries with different IDs
```

**Prisma/TypeORM:**
```
# Enable query logging
prisma:query SELECT * FROM Order WHERE userId = ?
prisma:query SELECT * FROM User WHERE id = 1
prisma:query SELECT * FROM User WHERE id = 2
prisma:query SELECT * FROM User WHERE id = 3
```

### N+1 Detection Checklist

```markdown
## N+1 Detection Report

### Symptoms
- [ ] Page load > 1s with multiple DB queries
- [ ] Similar queries repeated with different IDs
- [ ] Query count scales with data size (N records = N+1 queries)

### Identified Patterns

| Location | Pattern | Query Count | Impact |
|----------|---------|-------------|--------|
| OrderService.list() | User lookup per order | 50/page | HIGH |
| ProductController.show() | Review fetch per product | 20/product | MEDIUM |

### Fix Recommendations

| Pattern | Current | Recommended | ORM Example |
|---------|---------|-------------|-------------|
| Lazy load | N+1 queries | Eager load | `include: { user: true }` |
| Loop query | N queries | Batch query | `WHERE id IN (...)` |
| Nested load | N*M queries | JOIN | `leftJoinAndSelect()` |
```

### Automated N+1 Detection Script

```javascript
// Middleware to detect N+1 in development
const queryLog = [];
const N1_THRESHOLD = 5;

prisma.$use(async (params, next) => {
  const key = `${params.model}.${params.action}`;
  queryLog.push({ key, timestamp: Date.now() });

  // Detect repeated queries in 100ms window
  const recent = queryLog.filter(q =>
    q.key === key && Date.now() - q.timestamp < 100
  );

  if (recent.length >= N1_THRESHOLD) {
    console.warn(`⚠️ N+1 detected: ${key} called ${recent.length} times`);
  }

  return next(params);
});
```

---

## Cache Integration Strategy

### Cache Decision Matrix

| Query Type | Frequency | Volatility | Recommended Cache |
|------------|-----------|------------|-------------------|
| User profile | High | Low | Redis (TTL: 1hr) |
| Product catalog | High | Medium | Redis (TTL: 10min) |
| Search results | High | High | Application (TTL: 1min) |
| Analytics | Low | Low | Materialized view |
| Real-time data | High | High | No cache |

### Redis Cache Pattern

```typescript
// Cache-aside pattern
async function getUserWithCache(userId: string): Promise<User> {
  const cacheKey = `user:${userId}`;

  // Try cache first
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }

  // Fallback to database
  const user = await db.user.findUnique({ where: { id: userId } });

  // Store in cache
  await redis.setex(cacheKey, 3600, JSON.stringify(user));

  return user;
}

// Cache invalidation
async function updateUser(userId: string, data: UpdateUserDto) {
  await db.user.update({ where: { id: userId }, data });
  await redis.del(`user:${userId}`);  // Invalidate cache
}
```

### Query Result Caching with ORM

```typescript
// Prisma with Redis cache
import { createPrismaRedisCache } from 'prisma-redis-middleware';

const cacheMiddleware = createPrismaRedisCache({
  models: [
    { model: 'User', cacheTime: 3600 },
    { model: 'Product', cacheTime: 600 },
  ],
  storage: { type: 'redis', options: { client: redisClient } },
});

prisma.$use(cacheMiddleware);
```

---

## ORM Optimization Patterns

### Common ORM Issues

```markdown
## N+1 Problem
**Symptom**: Many small queries in loop
**Fix**: Eager loading / JOIN fetch

## Over-fetching
**Symptom**: SELECT * when only few columns needed
**Fix**: Select specific columns

## Under-indexed
**Symptom**: WHERE on non-indexed columns
**Fix**: Add indexes for query patterns

## Implicit Type Conversion
**Symptom**: Index not used due to type mismatch
**Fix**: Ensure consistent types
```

### ORM-Specific Recommendations

```typescript
// Prisma - Use include for eager loading
const users = await prisma.user.findMany({
  include: {
    posts: true,  // Eager load posts
  },
});

// TypeORM - Use relations or QueryBuilder
const users = await userRepository.find({
  relations: ['posts'],
});

// Drizzle - Use with for joins
const result = await db.query.users.findMany({
  with: {
    posts: true,
  },
});
```
