# Performance Patterns Reference

Builder agent's performance optimization patterns.

## N+1 Detection & Prevention

```typescript
// ❌ N+1 problem
async function getOrdersWithItems(customerId: string) {
  const orders = await db.order.findMany({ where: { customerId } });
  // N queries occur
  for (const order of orders) {
    order.items = await db.orderItem.findMany({ where: { orderId: order.id } });
  }
  return orders;
}

// ✅ Eager Loading
async function getOrdersWithItems(customerId: string) {
  return db.order.findMany({
    where: { customerId },
    include: { items: true }, // Single JOIN query
  });
}

// ✅ DataLoader (for GraphQL)
const orderItemsLoader = new DataLoader<string, OrderItem[]>(async (orderIds) => {
  const items = await db.orderItem.findMany({
    where: { orderId: { in: orderIds as string[] } },
  });
  const itemsByOrderId = groupBy(items, 'orderId');
  return orderIds.map(id => itemsByOrderId[id] ?? []);
});
```

## Cache Strategy (Redis)

```typescript
// Redis cache wrapper
class CacheService {
  constructor(private readonly redis: Redis) {}

  async getOrSet<T>(
    key: string,
    fetcher: () => Promise<T>,
    ttlSeconds: number = 300
  ): Promise<T> {
    const cached = await this.redis.get(key);
    if (cached) {
      return JSON.parse(cached) as T;
    }

    const value = await fetcher();
    await this.redis.setex(key, ttlSeconds, JSON.stringify(value));
    return value;
  }

  async invalidate(pattern: string): Promise<void> {
    const keys = await this.redis.keys(pattern);
    if (keys.length > 0) {
      await this.redis.del(...keys);
    }
  }
}

// Usage example
async function getUser(userId: string): Promise<User> {
  return cache.getOrSet(
    `user:${userId}`,
    () => userRepository.findById(userId),
    600 // 10 minutes
  );
}
```

## Batch Processing

```typescript
// Batch processing for large datasets
async function processLargeDataset<T, R>(
  items: T[],
  processor: (item: T) => Promise<R>,
  options: { batchSize: number; concurrency: number } = { batchSize: 100, concurrency: 5 }
): Promise<R[]> {
  const results: R[] = [];
  const batches = chunk(items, options.batchSize);

  for (const batch of batches) {
    // Parallel execution within batch
    const batchResults = await Promise.all(
      batch.map(item => limit(() => processor(item), options.concurrency))
    );
    results.push(...batchResults);

    // Wait between batches (rate limiting)
    await sleep(100);
  }

  return results;
}
```

## Virtualization (Large Lists)

```typescript
// Using react-virtual
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50, // Estimated height per row
    overscan: 5, // Rows to render off-screen
  });

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div style={{ height: virtualizer.getTotalSize(), position: 'relative' }}>
        {virtualizer.getVirtualItems().map((virtualRow) => (
          <div
            key={virtualRow.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: virtualRow.size,
              transform: `translateY(${virtualRow.start}px)`,
            }}
          >
            <ItemRow item={items[virtualRow.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```
