# CQRS Patterns Reference

Builder agent's Command/Query Responsibility Segregation patterns.

## Command Side

```typescript
// Command
interface Command {
  readonly type: string;
}

class CreateOrderCommand implements Command {
  readonly type = 'CreateOrder';
  constructor(
    readonly customerId: string,
    readonly items: Array<{ productId: string; quantity: number }>
  ) {}
}

// Command Handler
interface CommandHandler<T extends Command> {
  handle(command: T): Promise<Result<void, DomainError>>;
}

class CreateOrderHandler implements CommandHandler<CreateOrderCommand> {
  constructor(
    private readonly orderRepository: OrderRepository,
    private readonly productRepository: ProductRepository,
    private readonly eventPublisher: EventPublisher
  ) {}

  async handle(command: CreateOrderCommand): Promise<Result<void, DomainError>> {
    // Load products
    const products = await Promise.all(
      command.items.map(item => this.productRepository.findById(item.productId))
    );

    // Create order
    const orderResult = Order.create(new CustomerId(command.customerId));
    if (orderResult.isErr()) return orderResult;

    const order = orderResult.value;

    // Add items
    for (let i = 0; i < command.items.length; i++) {
      const product = products[i];
      if (!product) return err(new ProductNotFoundError(command.items[i].productId));

      const addResult = order.addItem(product, command.items[i].quantity);
      if (addResult.isErr()) return addResult;
    }

    // Save and publish events
    await this.orderRepository.save(order);
    for (const event of order.getUncommittedEvents()) {
      await this.eventPublisher.publish(event);
    }

    return ok(undefined);
  }
}

// Command Bus
class CommandBus {
  private handlers = new Map<string, CommandHandler<Command>>();

  register<T extends Command>(commandType: string, handler: CommandHandler<T>): void {
    this.handlers.set(commandType, handler as CommandHandler<Command>);
  }

  async dispatch<T extends Command>(command: T): Promise<Result<void, DomainError>> {
    const handler = this.handlers.get(command.type);
    if (!handler) {
      return err(new UnknownCommandError(command.type));
    }
    return handler.handle(command);
  }
}
```

## Query Side

```typescript
// Query
interface Query<TResult> {
  readonly type: string;
}

class GetOrdersByCustomerQuery implements Query<OrderSummary[]> {
  readonly type = 'GetOrdersByCustomer';
  constructor(
    readonly customerId: string,
    readonly page: number = 1,
    readonly limit: number = 20
  ) {}
}

// Query Handler
interface QueryHandler<TQuery extends Query<TResult>, TResult> {
  handle(query: TQuery): Promise<TResult>;
}

class GetOrdersByCustomerHandler implements QueryHandler<GetOrdersByCustomerQuery, OrderSummary[]> {
  constructor(private readonly readDb: ReadDatabase) {}

  async handle(query: GetOrdersByCustomerQuery): Promise<OrderSummary[]> {
    // Fetch from optimized read-only view
    const result = await this.readDb.query<OrderSummary>(
      `SELECT
         o.id,
         o.status,
         o.total_amount,
         o.item_count,
         o.created_at
       FROM order_summaries o
       WHERE o.customer_id = $1
       ORDER BY o.created_at DESC
       LIMIT $2 OFFSET $3`,
      [query.customerId, query.limit, (query.page - 1) * query.limit]
    );
    return result.rows;
  }
}

// Query Bus
class QueryBus {
  private handlers = new Map<string, QueryHandler<Query<unknown>, unknown>>();

  register<TQuery extends Query<TResult>, TResult>(
    queryType: string,
    handler: QueryHandler<TQuery, TResult>
  ): void {
    this.handlers.set(queryType, handler as QueryHandler<Query<unknown>, unknown>);
  }

  async dispatch<TResult>(query: Query<TResult>): Promise<TResult> {
    const handler = this.handlers.get(query.type);
    if (!handler) {
      throw new UnknownQueryError(query.type);
    }
    return handler.handle(query) as Promise<TResult>;
  }
}
```

## Read Model Projection

```typescript
// Event Handler for Read Model
class OrderSummaryProjection {
  constructor(private readonly readDb: ReadDatabase) {}

  async handle(event: DomainEvent): Promise<void> {
    switch (event.eventType) {
      case 'OrderPlaced':
        await this.onOrderPlaced(event as OrderPlaced);
        break;
      case 'OrderItemAdded':
        await this.onOrderItemAdded(event as OrderItemAdded);
        break;
      case 'OrderShipped':
        await this.onOrderShipped(event as OrderShipped);
        break;
    }
  }

  private async onOrderPlaced(event: OrderPlaced): Promise<void> {
    await this.readDb.query(
      `INSERT INTO order_summaries (id, customer_id, status, total_amount, item_count, created_at)
       VALUES ($1, $2, $3, $4, $5, $6)`,
      [event.orderId, event.customerId, 'PLACED', event.totalAmount, event.items.length, event.occurredAt]
    );
  }

  private async onOrderShipped(event: OrderShipped): Promise<void> {
    await this.readDb.query(
      `UPDATE order_summaries SET status = 'SHIPPED', tracking_number = $2 WHERE id = $1`,
      [event.orderId, event.trackingNumber]
    );
  }
}
```
