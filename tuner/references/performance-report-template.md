# Performance Report Template

```markdown
## Database Performance Report

### Executive Summary

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Avg Query Time | 500ms | 50ms | 90% |
| Slow Queries/hr | 100 | 5 | 95% |
| Index Usage | 60% | 95% | 58% |
| Disk I/O | 80% | 30% | 62% |

### Top Issues Identified

1. **Missing index on users.email** - 40% of slow queries
2. **N+1 in orders listing** - 100+ queries per page
3. **Full table scan on logs** - 10M+ rows scanned

### Changes Applied

#### Index Additions
\`\`\`sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at);
\`\`\`

#### Query Rewrites
- Converted lazy loading to eager loading in OrderService
- Added pagination to log queries

### Validation Results

| Query | Before | After | Status |
|-------|--------|-------|--------|
| User lookup | 200ms | 2ms | ✅ |
| Order listing | 5s | 100ms | ✅ |
| Log search | 30s | 500ms | ✅ |

### Recommendations for Future

1. Set up slow query monitoring
2. Regular index usage review
3. Query pattern analysis before new features
```
