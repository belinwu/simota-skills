# Result Type Patterns Reference

Builder agent's Result type and Railway Oriented Programming patterns.

## Basic Result Type

```typescript
// Result type definition
type Result<T, E> = Ok<T> | Err<E>;

class Ok<T> {
  readonly _tag = 'Ok' as const;
  constructor(readonly value: T) {}

  isOk(): this is Ok<T> { return true; }
  isErr(): this is Err<never> { return false; }

  map<U>(fn: (value: T) => U): Result<U, never> {
    return ok(fn(this.value));
  }

  flatMap<U, E>(fn: (value: T) => Result<U, E>): Result<U, E> {
    return fn(this.value);
  }

  unwrap(): T { return this.value; }
  unwrapOr(_defaultValue: T): T { return this.value; }
}

class Err<E> {
  readonly _tag = 'Err' as const;
  constructor(readonly error: E) {}

  isOk(): this is Ok<never> { return false; }
  isErr(): this is Err<E> { return true; }

  map<U>(_fn: (value: never) => U): Result<U, E> {
    return this as unknown as Result<U, E>;
  }

  flatMap<U, F>(_fn: (value: never) => Result<U, F>): Result<U, E | F> {
    return this as unknown as Result<U, E | F>;
  }

  unwrap(): never { throw this.error; }
  unwrapOr<T>(defaultValue: T): T { return defaultValue; }
}

// Factory functions
const ok = <T>(value: T): Ok<T> => new Ok(value);
const err = <E>(error: E): Err<E> => new Err(error);
```

## Railway Oriented Programming

```typescript
// Chain operations that can fail
async function processOrder(orderId: string): Promise<Result<Receipt, OrderError>> {
  return await findOrder(orderId)
    .then(result => result.flatMapAsync(validateInventory))
    .then(result => result.flatMapAsync(calculateTotal))
    .then(result => result.flatMapAsync(processPayment))
    .then(result => result.flatMapAsync(generateReceipt));
}

// Async flatMap extension
Ok.prototype.flatMapAsync = async function<U, E>(
  fn: (value: unknown) => Promise<Result<U, E>>
): Promise<Result<U, E>> {
  return fn(this.value);
};

Err.prototype.flatMapAsync = async function<U, F>(): Promise<Result<U, unknown>> {
  return this;
};
```

## Combining Multiple Results

```typescript
// Collect all results or fail on first error
function all<T, E>(results: Result<T, E>[]): Result<T[], E> {
  const values: T[] = [];
  for (const result of results) {
    if (result.isErr()) return result;
    values.push(result.value);
  }
  return ok(values);
}

// Collect all errors
function partition<T, E>(results: Result<T, E>[]): { ok: T[]; err: E[] } {
  const partition = { ok: [] as T[], err: [] as E[] };
  for (const result of results) {
    if (result.isOk()) partition.ok.push(result.value);
    else partition.err.push(result.error);
  }
  return partition;
}

// Usage
const validationResults = [
  validateEmail(data.email),
  validatePassword(data.password),
  validateAge(data.age),
];

const allValid = all(validationResults);
if (allValid.isErr()) {
  return { error: allValid.error };
}
```

## Pattern Matching with Result

```typescript
// Exhaustive pattern matching
function match<T, E, U>(
  result: Result<T, E>,
  handlers: {
    ok: (value: T) => U;
    err: (error: E) => U;
  }
): U {
  if (result.isOk()) return handlers.ok(result.value);
  return handlers.err(result.error);
}

// Usage
const message = match(fetchUser(userId), {
  ok: (user) => `Welcome, ${user.name}`,
  err: (error) => {
    switch (error.code) {
      case 'NOT_FOUND': return 'User not found';
      case 'UNAUTHORIZED': return 'Please log in';
      default: return 'An error occurred';
    }
  },
});
```

## fromPromise Utility

```typescript
async function fromPromise<T, E = Error>(
  promise: Promise<T>,
  errorMapper?: (error: unknown) => E
): Promise<Result<T, E>> {
  try {
    const value = await promise;
    return ok(value);
  } catch (error) {
    const mappedError = errorMapper
      ? errorMapper(error)
      : (error as E);
    return err(mappedError);
  }
}

// Usage
const result = await fromPromise(
  fetch('/api/users').then(r => r.json()),
  (e) => new ApiError('Failed to fetch users', e)
);
```
