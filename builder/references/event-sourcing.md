# Event Sourcing & Saga Patterns Reference

Builder agent's Event Sourcing and Saga implementation patterns.

## Domain Event

```typescript
// Domain Event base
abstract class DomainEvent {
  readonly occurredAt: Date;
  readonly eventId: string;

  constructor() {
    this.occurredAt = new Date();
    this.eventId = crypto.randomUUID();
  }

  abstract get eventType(): string;
}

// Concrete event
class OrderPlaced extends DomainEvent {
  constructor(
    readonly orderId: OrderId,
    readonly customerId: CustomerId,
    readonly items: OrderItem[],
    readonly totalAmount: Money
  ) {
    super();
  }

  get eventType(): string {
    return 'OrderPlaced';
  }
}

class OrderShipped extends DomainEvent {
  constructor(
    readonly orderId: OrderId,
    readonly trackingNumber: string,
    readonly carrier: string
  ) {
    super();
  }

  get eventType(): string {
    return 'OrderShipped';
  }
}
```

## Event Store

```typescript
interface EventStore {
  append(streamId: string, events: DomainEvent[], expectedVersion?: number): Promise<void>;
  read(streamId: string, fromVersion?: number): Promise<StoredEvent[]>;
  subscribe(eventTypes: string[], handler: EventHandler): Subscription;
}

// PostgreSQL implementation
class PostgresEventStore implements EventStore {
  async append(
    streamId: string,
    events: DomainEvent[],
    expectedVersion?: number
  ): Promise<void> {
    await this.db.transaction(async (tx) => {
      // Optimistic locking
      if (expectedVersion !== undefined) {
        const currentVersion = await tx.query(
          'SELECT MAX(version) FROM events WHERE stream_id = $1',
          [streamId]
        );
        if (currentVersion.rows[0].max !== expectedVersion) {
          throw new ConcurrencyError('Stream has been modified');
        }
      }

      // Append events
      for (let i = 0; i < events.length; i++) {
        const event = events[i];
        await tx.query(
          `INSERT INTO events (stream_id, event_type, data, metadata, version)
           VALUES ($1, $2, $3, $4, $5)`,
          [
            streamId,
            event.eventType,
            JSON.stringify(event),
            JSON.stringify({ occurredAt: event.occurredAt }),
            (expectedVersion ?? 0) + i + 1,
          ]
        );
      }
    });
  }
}
```

## Event-Sourced Aggregate

```typescript
abstract class EventSourcedAggregate<TId> {
  protected _id: TId;
  protected _version: number = 0;
  protected _uncommittedEvents: DomainEvent[] = [];

  protected apply(event: DomainEvent): void {
    this.when(event);
    this._uncommittedEvents.push(event);
  }

  protected abstract when(event: DomainEvent): void;

  getUncommittedEvents(): DomainEvent[] {
    return [...this._uncommittedEvents];
  }

  clearUncommittedEvents(): void {
    this._uncommittedEvents = [];
  }

  loadFromHistory(events: DomainEvent[]): void {
    for (const event of events) {
      this.when(event);
      this._version++;
    }
  }
}

// Order as Event-Sourced Aggregate
class Order extends EventSourcedAggregate<OrderId> {
  private _status: OrderStatus = OrderStatus.DRAFT;
  private _items: OrderItem[] = [];

  static create(customerId: CustomerId): Order {
    const order = new Order();
    order.apply(new OrderCreated(OrderId.generate(), customerId));
    return order;
  }

  addItem(product: Product, quantity: number): void {
    if (this._status !== OrderStatus.DRAFT) {
      throw new InvalidOperationError('Cannot modify confirmed order');
    }
    this.apply(new OrderItemAdded(this._id, product.id, quantity, product.price));
  }

  protected when(event: DomainEvent): void {
    switch (event.eventType) {
      case 'OrderCreated':
        const created = event as OrderCreated;
        this._id = created.orderId;
        this._status = OrderStatus.DRAFT;
        break;
      case 'OrderItemAdded':
        const itemAdded = event as OrderItemAdded;
        this._items.push(new OrderItem(itemAdded.productId, itemAdded.quantity, itemAdded.price));
        break;
      // ... other events
    }
  }
}
```

## Saga / Process Manager

```typescript
// Saga for Order Fulfillment
class OrderFulfillmentSaga {
  private state: SagaState = 'STARTED';
  private compensationActions: (() => Promise<void>)[] = [];

  constructor(
    private readonly inventoryService: InventoryService,
    private readonly paymentService: PaymentService,
    private readonly shippingService: ShippingService,
    private readonly eventPublisher: EventPublisher
  ) {}

  async execute(order: Order): Promise<Result<void, SagaError>> {
    try {
      // Step 1: Reserve Inventory
      const reserveResult = await this.inventoryService.reserve(order.items);
      if (reserveResult.isErr()) {
        return err(new SagaError('INVENTORY_FAILED', reserveResult.error));
      }
      this.compensationActions.push(() => this.inventoryService.release(order.items));

      // Step 2: Process Payment
      const paymentResult = await this.paymentService.charge(order.customerId, order.totalAmount);
      if (paymentResult.isErr()) {
        await this.compensate();
        return err(new SagaError('PAYMENT_FAILED', paymentResult.error));
      }
      this.compensationActions.push(() => this.paymentService.refund(paymentResult.value.transactionId));

      // Step 3: Create Shipment
      const shipmentResult = await this.shippingService.createShipment(order);
      if (shipmentResult.isErr()) {
        await this.compensate();
        return err(new SagaError('SHIPPING_FAILED', shipmentResult.error));
      }

      // Success
      this.state = 'COMPLETED';
      await this.eventPublisher.publish(new OrderFulfilled(order.id));
      return ok(undefined);

    } catch (error) {
      await this.compensate();
      return err(new SagaError('UNEXPECTED_ERROR', error));
    }
  }

  private async compensate(): Promise<void> {
    this.state = 'COMPENSATING';
    // Execute compensation actions in reverse order
    for (const action of this.compensationActions.reverse()) {
      try {
        await action();
      } catch (error) {
        console.error('Compensation failed:', error);
        // Log and continue (manual intervention needed)
      }
    }
    this.state = 'COMPENSATED';
  }
}
```

## Outbox Pattern (Event Delivery Guarantee)

```typescript
// Write to Outbox table, deliver in separate process
class OutboxEventPublisher implements EventPublisher {
  constructor(private readonly db: Database) {}

  async publish(event: DomainEvent): Promise<void> {
    // Add to Outbox within transaction
    await this.db.query(
      `INSERT INTO outbox (event_id, event_type, payload, created_at, published_at)
       VALUES ($1, $2, $3, NOW(), NULL)`,
      [event.eventId, event.eventType, JSON.stringify(event)]
    );
  }
}

// Outbox Processor running in separate process
class OutboxProcessor {
  async process(): Promise<void> {
    const unpublished = await this.db.query(
      `SELECT * FROM outbox WHERE published_at IS NULL ORDER BY created_at LIMIT 100`
    );

    for (const row of unpublished.rows) {
      try {
        await this.messageQueue.publish(row.event_type, row.payload);
        await this.db.query(
          `UPDATE outbox SET published_at = NOW() WHERE event_id = $1`,
          [row.event_id]
        );
      } catch (error) {
        console.error('Failed to publish event:', row.event_id, error);
      }
    }
  }
}
```
