# Builder Code Examples Reference

Forge conversion patterns, test skeletons, anti-pattern fixes, and case studies.

## Forge → Builder Conversion Patterns

### Mock Data → Value Object

```typescript
// Forge mock data
const MOCK_USER = {
  email: 'test@example.com',
  name: 'Test User',
};

// Builder generates Value Object
class Email extends ValueObject<{ value: string }> {
  private static readonly PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  static create(email: string): Result<Email, ValidationError> {
    if (!this.PATTERN.test(email)) {
      return err(new ValidationError('Invalid email format'));
    }
    return ok(new Email(email.toLowerCase().trim()));
// ...
```

### MSW Handler → API Client

```typescript
// Forge MSW handler
http.get('/api/users/:id', ({ params }) => {
  return HttpResponse.json(MOCK_USERS.find(u => u.id === params.id));
});

// Builder generates API Client
class UserApiClient extends ApiClient {
  async getUser(id: UserId): Promise<Result<User, ApiError>> {
    return this.request<UserDto>({
      method: 'GET',
      url: `/api/users/${id.value}`,
    }).then(result => result.map(UserMapper.toDomain));
  }
}
```

### Error Mock → DomainError

```typescript
// Forge error mock
http.post('/api/users', async ({ request }) => {
  const body = await request.json();
  if (!body.email) {
    return HttpResponse.json(
      { error: 'Email is required' },
      { status: 400 }
    );
  }
});

// Builder generates DomainError
class EmailRequiredError extends DomainError {
  constructor() {
    super('EMAIL_REQUIRED', 'Email is required');
// ...
```

---

## Specification Analysis Template

```markdown
## Specification Analysis Result

### Clear Requirements
- [ ] Requirement 1: [Specific content]
- [ ] Requirement 2: [Specific content]

### Inferred Requirements (Confirmation Recommended)
- [ ] Inference 1: [Content] → Rationale: [Why inferred]
- [ ] Inference 2: [Content] → Rationale: [Why inferred]

### Undefined Requirements (Confirmation Required)
- [ ] Unknown 1: [Content] → Impact: [Implementation impact]
- [ ] Unknown 2: [Content] → Impact: [Implementation impact]

### Edge Cases
...
```

---

## Test Skeleton Generation

```typescript
// Builder generates test skeleton (Radar extends)
describe('UserService', () => {
  describe('createUser', () => {
    // Happy path
    it('should create user with valid data', async () => {
      // Arrange: Valid user data
      // Act: Call createUser()
      // Assert: User entity is returned
    });

    // Edge cases
    it('should return ValidationError for empty email', async () => {
      // TODO: Radar implements
    });

// ...
```

---

## Seven Deadly Sins: Bad → Good Examples

### The `any` Escape

```typescript
// ❌ BAD: Gives up type safety
function processData(data: any) {
  return data.items.map(item => item.value);
}

// ✅ GOOD: Types catch bugs at compile time
interface DataPayload {
  items: Array<{ value: number }>;
}
function processData(data: DataPayload) {
  return data.items.map(item => item.value);
}
```

### The Happy Path Trap

```typescript
// ❌ BAD: What if API fails? What if user is null?
async function loadUser(id: string) {
  const user = await api.getUser(id);
  return user.profile.displayName;
}

// ✅ GOOD: Explicit failure handling
async function loadUser(id: string): Promise<Result<string, UserError>> {
  const result = await api.getUser(id);
  if (result.isErr()) {
    return err(new UserNotFoundError(id));
  }
  return ok(result.value.profile?.displayName ?? 'Anonymous');
}
```

### The Magic Number

```typescript
// ❌ BAD: Why 100? What does it mean?
if (items.length > 100) {
  paginate(items);
}

// ✅ GOOD: Intent is clear, easy to change
const PAGINATION_THRESHOLD = 100; // UX研究: 100件超で描画が遅延
if (items.length > PAGINATION_THRESHOLD) {
  paginate(items);
}
```

### The Leaky Abstraction

```typescript
// ❌ BAD: Component knows too much about API
function UserList() {
  const [users, setUsers] = useState([]);
  useEffect(() => {
    fetch('/api/users').then(r => r.json()).then(setUsers);
  }, []);
  return <ul>{users.map(u => <li>{u.name}</li>)}</ul>;
}

// ✅ GOOD: Separation of concerns
function useUsers() {
  return useQuery(['users'], () => userService.getAll());
}

function UserList() {
// ...
```

### The Silent Failure

```typescript
// ❌ BAD: Bug? What bug? I see nothing.
try {
  await saveData(payload);
} catch (e) {
  // silence is golden... until production breaks
}

// ✅ GOOD: Failures are visible and actionable
try {
  await saveData(payload);
} catch (e) {
  logger.error('Failed to save data', { payload, error: e });
  throw new DataPersistenceError('Save failed', { cause: e });
}
```

### The Async Void

```typescript
// ❌ BAD: Fire and forget... and lose errors
useEffect(() => {
  async function load() {
    const data = await fetchData();
    setData(data);
  }
  load(); // Promise ignored!
}, []);

// ✅ GOOD: Errors are caught
useEffect(() => {
  let cancelled = false;
  fetchData()
    .then(data => { if (!cancelled) setData(data); })
    .catch(err => { if (!cancelled) setError(err); });
// ...
```

---

## Case Study 1: Forge → Builder Handoff (User Authentication)

**Scenario**: Forge delivered a working login prototype with MSW mocks. Builder must transform it into production-ready authentication.

**Forge Deliverables**:
```
components/prototypes/LoginForm.tsx  - Working UI
mocks/handlers.ts                    - MSW mock responses
types.ts                             - Basic TypeScript types
```

**Builder's Transformation Process**:

```
🔷 BLUEPRINT
├── Identify Value Objects: Email, Password, SessionToken
├── Identify Entities: User (has identity across sessions)
├── Design error types: InvalidCredentials, AccountLocked, RateLimited
└── Map API contract from MSW handlers

🔨 FORGE
├── Create Email Value Object with validation
├── Create AuthService with proper error handling
├── Implement secure token storage (httpOnly cookie strategy)
└── Add rate limiting awareness to client

🛡️ TEMPER
├── Handle: Network failure, timeout, 401, 403, 429
├── Add: Retry with exponential backoff for 5xx
...
```

**Key Transformations**:

```typescript
// Forge mock type
interface LoginResponse {
  token: string;
  user: any;  // 🔴 any!
}

// Builder production type
interface AuthResult {
  sessionToken: SessionToken;  // Value Object
  user: AuthenticatedUser;     // Entity
  expiresAt: Date;
}

type LoginError =
  | InvalidCredentialsError
// ...
```

---

## Case Study 2: Scout → Builder Handoff (Race Condition Fix)

**Scenario**: Scout identified a race condition in shopping cart quantity updates. Users clicking rapidly caused inventory inconsistencies.

**Scout's Investigation Report**:
```markdown
## Root Cause
- `updateQuantity()` sends API calls without waiting
- Fast clicks create interleaved requests
- Final state depends on response order (non-deterministic)

## Reproduction
1. Click +/- button rapidly 10 times
2. Observe: UI shows 5, server shows 3

## Suggested Fix
- Debounce user input OR
- Queue requests sequentially OR
- Use optimistic locking with version
```

**Builder's Solution**:

```
🔷 BLUEPRINT
├── Option analysis: debounce vs queue vs optimistic locking
├── Choose: Optimistic locking (most robust for concurrent scenarios)
└── Design: CartItem with version field

🔨 FORGE
├── Add version to CartItem entity
├── Implement optimistic lock check in API
└── Handle version conflict in client

🛡️ TEMPER
├── Handle conflict: Show user "Cart was updated, refresh?"
├── Add retry logic: Auto-retry with fresh version on conflict
└── Prevent: Double-submit with request deduplication

...
```

**Implementation**:

```typescript
// Before (race condition prone)
async function updateQuantity(itemId: string, quantity: number) {
  await api.patch(`/cart/${itemId}`, { quantity });
}

// After (race condition safe)
class CartService {
  private pendingUpdates = new Map<string, AbortController>();

  async updateQuantity(
    itemId: CartItemId,
    quantity: Quantity,
    version: number
  ): Promise<Result<CartItem, CartError>> {
    // Cancel any pending update for this item
// ...
```
