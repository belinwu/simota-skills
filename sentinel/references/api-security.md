# API Security & OWASP API Top 10

Purpose: Use this reference when auditing HTTP APIs, GraphQL services, OAuth flows, or API-specific authorization and SSRF risks.

## Contents

- OWASP API Top 10
- BOLA / property-level auth / BFLA
- API checklist
- response filtering and SSRF
- GraphQL controls
- OAuth 2.1 checks

## OWASP API Security Top 10 (2023)

| Rank | Category | Severity | Frequency |
|------|----------|----------|-----------|
| `API1` | Broken Object Level Authorization (BOLA) | Critical | `40%` of API attacks |
| `API2` | Broken Authentication | Critical | High |
| `API3` | Broken Object Property Level Authorization | High | High |
| `API4` | Unrestricted Resource Consumption | High | Medium |
| `API5` | Broken Function Level Authorization (BFLA) | Critical | Medium |
| `API6` | Unrestricted Access to Sensitive Business Flows | High | Medium |
| `API7` | Server-Side Request Forgery (SSRF) | High | Medium |
| `API8` | Security Misconfiguration | Medium | Very high |
| `API9` | Improper Inventory Management | Medium | High |
| `API10` | Unsafe API Consumption | Medium | Medium |

## Key Vulnerabilities

### API1: BOLA

Use this section when object IDs appear in routes or queries.

Detection signals:

1. Object IDs are exposed in routes like `/orders/:id`
2. Ownership is not checked server-side
3. IDs are predictable

Mitigations:

- enforce ownership checks on every object access
- prefer UUIDs over sequential IDs
- use centralized authorization or row-level security

```typescript
// Anti-pattern: no ownership check
app.get('/api/orders/:id', async (req, res) => {
  const order = await Order.findById(req.params.id);
  res.json(order);
});

// Pattern: ownership enforced
app.get('/api/orders/:id', async (req, res) => {
  const order = await Order.findOne({
    _id: req.params.id,
    userId: req.user.id,
  });
  if (!order) return res.status(404).json({ error: 'Not found' });
  res.json(order);
});
```

### API3: Broken Object Property Level Authorization

Formerly called mass assignment.

Detection signals:

1. `req.body` is written directly to the database
2. field-level access control is missing
3. responses expose unnecessary fields

Mitigations:

- use explicit allowlists
- validate input shape with JSON Schema or `Zod`
- separate DTOs from persistence models

```typescript
// Anti-pattern: accepts every field
app.put('/api/users/:id', async (req, res) => {
  await User.findByIdAndUpdate(req.params.id, req.body);
});

// Pattern: allowlist only
app.put('/api/users/:id', async (req, res) => {
  const { name, email, avatar } = req.body;
  await User.findByIdAndUpdate(req.params.id, { name, email, avatar });
});
```

### API5: BFLA

Detection signals:

1. admin or privileged routes lack authorization middleware
2. method-level authorization is inconsistent
3. `/admin` paths rely on UI hiding instead of server checks

Mitigations:

- centralized policy-as-code or middleware
- RBAC / ABAC on handlers and methods
- deny by default

## API Security Checklist

### Authentication And Authorization

- require authentication on every non-public endpoint
- enforce ownership checks for object access (`BOLA`)
- enforce function-level authorization (`BFLA`)
- verify JWT signature and expiry
- scope API keys
- prefer OAuth `Authorization Code + PKCE`
- keep session management strict

### Input And Output

- validate request bodies and params
- block mass assignment with allowlists
- return DTOs, not raw models
- paginate and rate limit expensive queries
- constrain file type and size on uploads
- validate path parameters (`UUID`, identifier format)

### Infrastructure And Configuration

- forbid `CORS: *` for privileged APIs
- force HTTPS
- version APIs and retire stale endpoints
- keep internal errors out of responses
- disable public docs for sensitive internal endpoints

## Common Patterns

### Rate Limiting

Implementation patterns live in `defensive-controls.md` § Rate Limiting.

### Response Filtering

```typescript
const toUserDTO = (user: User) => ({
  id: user.id,
  name: user.name,
  email: user.email,
  avatar: user.avatar,
});
```

### SSRF Prevention

```typescript
import { URL } from 'url';
import ipaddr from 'ipaddr.js';

function isAllowedUrl(urlString: string): boolean {
  const url = new URL(urlString);
  if (!['http:', 'https:'].includes(url.protocol)) return false;

  const addr = ipaddr.parse(url.hostname);
  if (addr.range() !== 'unicast') return false;

  const allowedDomains = ['api.example.com', 'cdn.example.com'];
  if (!allowedDomains.includes(url.hostname)) return false;

  return true;
}
```

## GraphQL Security

- enforce query depth limits
- enforce query complexity analysis
- disable introspection in production unless required
- use persisted queries when possible
- apply field-level authorization
- limit batching abuse

```typescript
import depthLimit from 'graphql-depth-limit';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [depthLimit(5)],
  introspection: process.env.NODE_ENV !== 'production',
});
```

## OAuth 2.1 Checks

- `Authorization Code + PKCE` is mandatory
- detect and remove `Implicit Grant`
- rotate refresh tokens
- prefer strong client authentication such as `mTLS` where relevant

Sentinel checks:

- `code_verifier` / `code_challenge` present
- no `response_type=token`
- refresh-token rotation implemented
