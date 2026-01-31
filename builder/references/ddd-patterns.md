# DDD Patterns Reference

Builder agent's Domain-Driven Design implementation patterns.

## Entity

Entities have identity that persists over time.

```typescript
// Entity base class
abstract class Entity<T> {
  protected readonly _id: T;

  constructor(id: T) {
    this._id = id;
  }

  get id(): T {
    return this._id;
  }

  equals(other: Entity<T>): boolean {
    return this._id === other._id;
  }
}

// User Entity
class User extends Entity<UserId> {
  private _email: Email;
  private _name: UserName;
  private _status: UserStatus;

  private constructor(id: UserId, email: Email, name: UserName, status: UserStatus) {
    super(id);
    this._email = email;
    this._name = name;
    this._status = status;
  }

  static create(props: CreateUserProps): Result<User, ValidationError> {
    const emailResult = Email.create(props.email);
    if (emailResult.isErr()) return err(emailResult.error);

    const nameResult = UserName.create(props.name);
    if (nameResult.isErr()) return err(nameResult.error);

    return ok(new User(
      UserId.generate(),
      emailResult.value,
      nameResult.value,
      UserStatus.PENDING
    ));
  }

  activate(): Result<void, DomainError> {
    if (this._status !== UserStatus.PENDING) {
      return err(new InvalidStateError('User must be pending to activate'));
    }
    this._status = UserStatus.ACTIVE;
    return ok(undefined);
  }
}
```

## Value Object

Value Objects are immutable and compared by value.

```typescript
// Value Object base
abstract class ValueObject<T> {
  protected readonly props: T;

  protected constructor(props: T) {
    this.props = Object.freeze(props);
  }

  equals(other: ValueObject<T>): boolean {
    return JSON.stringify(this.props) === JSON.stringify(other.props);
  }
}

// Email Value Object
class Email extends ValueObject<{ value: string }> {
  private static readonly EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  private constructor(value: string) {
    super({ value });
  }

  static create(email: string): Result<Email, ValidationError> {
    const trimmed = email.trim().toLowerCase();
    if (!this.EMAIL_REGEX.test(trimmed)) {
      return err(new ValidationError('Invalid email format'));
    }
    return ok(new Email(trimmed));
  }

  get value(): string {
    return this.props.value;
  }
}

// Money Value Object
class Money extends ValueObject<{ amount: number; currency: Currency }> {
  private constructor(amount: number, currency: Currency) {
    super({ amount, currency });
  }

  static create(amount: number, currency: Currency): Result<Money, ValidationError> {
    if (amount < 0) {
      return err(new ValidationError('Amount cannot be negative'));
    }
    return ok(new Money(amount, currency));
  }

  add(other: Money): Result<Money, DomainError> {
    if (this.props.currency !== other.props.currency) {
      return err(new CurrencyMismatchError());
    }
    return Money.create(this.props.amount + other.props.amount, this.props.currency);
  }
}
```

## Aggregate Root

Aggregates encapsulate entities and enforce invariants.

```typescript
// Order Aggregate Root
class Order extends Entity<OrderId> {
  private _items: OrderItem[];
  private _status: OrderStatus;
  private _customerId: CustomerId;

  // Only the aggregate root can modify children
  addItem(product: Product, quantity: number): Result<void, DomainError> {
    if (this._status !== OrderStatus.DRAFT) {
      return err(new InvalidStateError('Cannot modify confirmed order'));
    }

    const existingItem = this._items.find(i => i.productId.equals(product.id));
    if (existingItem) {
      existingItem.increaseQuantity(quantity);
    } else {
      this._items.push(OrderItem.create(product, quantity));
    }

    return ok(undefined);
  }

  confirm(): Result<OrderConfirmed, DomainError> {
    if (this._items.length === 0) {
      return err(new EmptyOrderError());
    }
    if (this._status !== OrderStatus.DRAFT) {
      return err(new InvalidStateError('Order already confirmed'));
    }

    this._status = OrderStatus.CONFIRMED;

    // Return domain event
    return ok(new OrderConfirmed(this._id, this._customerId, this.totalAmount));
  }

  get totalAmount(): Money {
    return this._items.reduce(
      (sum, item) => sum.add(item.subtotal).unwrap(),
      Money.zero(Currency.USD)
    );
  }
}
```

## Repository

Repositories abstract persistence.

```typescript
// Repository interface (domain layer)
interface UserRepository {
  findById(id: UserId): Promise<User | null>;
  findByEmail(email: Email): Promise<User | null>;
  save(user: User): Promise<void>;
  delete(id: UserId): Promise<void>;
}

// Implementation (infrastructure layer)
class PrismaUserRepository implements UserRepository {
  constructor(private readonly prisma: PrismaClient) {}

  async findById(id: UserId): Promise<User | null> {
    const data = await this.prisma.user.findUnique({
      where: { id: id.value }
    });
    return data ? UserMapper.toDomain(data) : null;
  }

  async save(user: User): Promise<void> {
    const data = UserMapper.toPersistence(user);
    await this.prisma.user.upsert({
      where: { id: data.id },
      create: data,
      update: data,
    });
  }
}
```

## Domain Service

Services for logic that doesn't belong to a single entity.

```typescript
// Domain Service
class TransferService {
  constructor(
    private readonly accountRepo: AccountRepository,
    private readonly eventPublisher: DomainEventPublisher
  ) {}

  async transfer(
    fromId: AccountId,
    toId: AccountId,
    amount: Money
  ): Promise<Result<TransferCompleted, DomainError>> {
    const fromAccount = await this.accountRepo.findById(fromId);
    const toAccount = await this.accountRepo.findById(toId);

    if (!fromAccount || !toAccount) {
      return err(new AccountNotFoundError());
    }

    // Business rule: debit and credit
    const debitResult = fromAccount.debit(amount);
    if (debitResult.isErr()) return err(debitResult.error);

    const creditResult = toAccount.credit(amount);
    if (creditResult.isErr()) {
      // Rollback
      fromAccount.credit(amount);
      return err(creditResult.error);
    }

    await this.accountRepo.save(fromAccount);
    await this.accountRepo.save(toAccount);

    const event = new TransferCompleted(fromId, toId, amount);
    await this.eventPublisher.publish(event);

    return ok(event);
  }
}
```
