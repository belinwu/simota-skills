# Agent Collaboration Handoff Templates

## Schema → Tuner Handoff

```markdown
## Schema → Tuner Optimization Request

**New Tables Created**: orders, order_items
**Expected Query Patterns**:
- Find orders by user_id (frequent)
- Find orders by date range (frequent)
- Aggregate order totals by user (daily)

**Request**: Review and optimize for these patterns
```

## Tuner → Schema Handoff

```markdown
## Tuner → Schema Index Request

**Analysis Complete**: orders table
**Recommended Indexes**:

1. `CREATE INDEX idx_orders_user_id ON orders(user_id);`
   - Query: Find user's orders
   - Improvement: Seq Scan → Index Scan

2. `CREATE INDEX idx_orders_created_at ON orders(created_at);`
   - Query: Date range queries
   - Consider: BRIN index for time-series

**Please add to migration**: Yes / No
```

## Tuner → Bolt Handoff

```markdown
## Tuner → Bolt Optimization Request

**DB Optimization Complete**: Query improved 90%
**Remaining Bottleneck**: Application layer N+1

**Issue Location**: OrderService.getOrdersWithItems()
**Current Behavior**: 1 query + N item queries
**Suggested Fix**: Eager loading or batch fetch

**Coordinate with**: Builder for implementation
```

## TUNER_TO_SCHEMA_HANDOFF

```markdown
## SCHEMA_HANDOFF (from Tuner)

### Index Recommendations
- **Table:** [table name]
- **Recommended indexes:** [list with rationale]
- **Expected improvement:** [query time reduction]

### Schema Change Requests
- [ ] [Migration needed]

Suggested command: `/Schema create migration for [index]`
```
