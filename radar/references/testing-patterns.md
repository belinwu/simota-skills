# Testing Patterns

Core testing patterns for unit and integration tests across frameworks.

---

## Arrange-Act-Assert (AAA)

The fundamental test structure pattern.

```typescript
test('adds item to cart', () => {
  // Arrange
  const cart = new Cart();
  const item = { id: '1', price: 100 };

  // Act
  cart.add(item);

  // Assert
  expect(cart.items).toHaveLength(1);
  expect(cart.total).toBe(100);
});
```

---

## Test Naming Conventions

### Given-When-Then

```typescript
// ✅ GOOD: Descriptive test names
test('GIVEN an empty cart WHEN checkout is clicked THEN it shows empty warning', () => {
  // ...
});

// ✅ GOOD: Behavior-focused
test('calculateDiscount throws error for negative percentage', () => {
  expect(() => calculateDiscount(100, -5)).toThrow('Invalid percentage');
});

// ❌ BAD: Vague
test('should work', () => { /* Work how? */ });
```

---

## React Testing Library

### Basic Patterns

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

const user = userEvent.setup();

test('submits form with valid data', async () => {
  const onSubmit = vi.fn();
  render(<LoginForm onSubmit={onSubmit} />);

  await user.type(screen.getByLabelText('Email'), 'test@example.com');
  await user.type(screen.getByLabelText('Password'), 'password123');
  await user.click(screen.getByRole('button', { name: 'Login' }));

  expect(onSubmit).toHaveBeenCalledWith({
    email: 'test@example.com',
// ...
```

### Query Priority

```typescript
// Priority order (most to least preferred):
// 1. getByRole - accessible to everyone
// 2. getByLabelText - form fields
// 3. getByPlaceholderText - fallback for inputs
// 4. getByText - non-interactive elements
// 5. getByTestId - last resort

screen.getByRole('button', { name: 'Submit' });
screen.getByRole('textbox', { name: 'Email' });
screen.getByRole('checkbox', { name: 'Remember me' });
```

### Async Testing

```typescript
test('shows loading then data', async () => {
  render(<UserList />);

  // Loading state (sync)
  expect(screen.getByText('Loading...')).toBeInTheDocument();

  // Wait for data (async)
  expect(await screen.findByText('John Doe')).toBeInTheDocument();

  // Loading should be gone
  expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
});
```

### Custom Render with Providers

```typescript
// test-utils.tsx
import { render, RenderOptions } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';

function AllProviders({ children }: { children: React.ReactNode }) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>{children}</BrowserRouter>
    </QueryClientProvider>
  );
}
// ...
```

---

## MSW (Mock Service Worker)

### Setup

```typescript
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';

const server = setupServer(
  http.get('/api/users', () => {
    return HttpResponse.json([{ id: 1, name: 'Test User' }]);
  }),
  http.post('/api/users', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({ id: 2, ...body }, { status: 201 });
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
// ...
```

### Error Scenarios

```typescript
test('handles server error', async () => {
  server.use(
    http.get('/api/users', () => {
      return HttpResponse.json({ message: 'Internal Error' }, { status: 500 });
    })
  );

  render(<UserList />);
  expect(await screen.findByText('Failed to load users')).toBeInTheDocument();
});

test('handles network error', async () => {
  server.use(
    http.get('/api/users', () => {
      return HttpResponse.error();
// ...
```

---

## Test Data Management

### Factory Pattern

```typescript
// factories/user.factory.ts
import { faker } from '@faker-js/faker';

interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user';
  createdAt: Date;
}

export function createUser(overrides: Partial<User> = {}): User {
  return {
    id: faker.string.uuid(),
    email: faker.internet.email(),
// ...
```

### Fixture Pattern

```typescript
// fixtures/orders.fixture.ts
export const fixtures = {
  emptyOrder: {
    id: 'order-1',
    items: [],
    total: 0,
    status: 'pending' as const,
  },
  singleItemOrder: {
    id: 'order-2',
    items: [{ productId: 'prod-1', quantity: 1, price: 100 }],
    total: 100,
    status: 'pending' as const,
  },
  completedOrder: {
// ...
```

### Database Seeding (Integration Tests)

```typescript
import { prisma } from '../lib/prisma';
import { createUser } from '../factories/user.factory';

export async function seedTestDatabase() {
  await prisma.user.deleteMany();
  await prisma.order.deleteMany();

  const users = await Promise.all([
    prisma.user.create({ data: createUser({ role: 'admin' }) }),
    prisma.user.create({ data: createUser({ role: 'user' }) }),
  ]);

  return { users };
}

// ...
```

---

## Integration Test Patterns

### API Tests (supertest)

```typescript
describe('POST /api/orders', () => {
  test('creates order and returns 201', async () => {
    const response = await request(app)
      .post('/api/orders')
      .send({ productId: '123', quantity: 2 })
      .expect(201);

    expect(response.body).toMatchObject({
      id: expect.any(String),
      status: 'pending',
    });
  });
});
```

### Database Tests (Testcontainers)

```typescript
describe('UserRepository', () => {
  let db: TestDatabase;

  beforeAll(async () => {
    db = await TestDatabase.start();
  });

  afterAll(() => db.stop());
  beforeEach(() => db.reset());

  test('creates user and retrieves by email', async () => {
    const repo = new UserRepository(db.connection);
    await repo.create({ email: 'test@example.com', name: 'Test' });
    const user = await repo.findByEmail('test@example.com');
    expect(user?.name).toBe('Test');
// ...
```

---

## E2E Testing Patterns (Playwright)

### Page Object Model

```typescript
class CheckoutPage {
  constructor(private page: Page) {}

  async fillShippingAddress(address: Address) {
    await this.page.fill('[data-testid="address"]', address.street);
    await this.page.fill('[data-testid="city"]', address.city);
  }

  async submitOrder() {
    await this.page.click('[data-testid="submit-order"]');
    await this.page.waitForURL('**/confirmation');
  }
}

test('user can complete checkout', async ({ page }) => {
// ...
```

---

## Coverage Configuration

### Vitest

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      reportsDirectory: './coverage',
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 75,
        statements: 80,
      },
// ...
```

### Jest

```javascript
// jest.config.js
module.exports = {
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  coverageThreshold: {
    global: { branches: 75, functions: 80, lines: 80, statements: 80 },
    './src/utils/payment.ts': {
      branches: 100, functions: 100, lines: 100,
    },
  },
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.test.{ts,tsx}',
    '!src/**/*.stories.{ts,tsx}',
// ...
```

### Coverage Commands

```bash
# Run tests with coverage
pnpm test --coverage

# Specific file
pnpm test src/utils/payment.test.ts --coverage

# HTML report
pnpm test --coverage --coverage.reporter=html
open coverage/index.html
```

---

## Mock Strategy Decision Tree

```
Is it an external service (3rd party API, payment)?
  → YES: Always mock (unreliable, costs money)
  → NO: Continue...

Is it a database?
  → Unit tests: Mock the repository
  → Integration tests: Use real DB (testcontainers)

Is it a sibling service in your system?
  → Unit tests: Mock the client
  → Integration tests: Consider contract tests

Is it slow (> 100ms)?
  → Consider mocking for unit tests
  → Use real implementation for integration tests
```
