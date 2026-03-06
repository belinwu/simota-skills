# Defensive Controls: Headers, Validation, Secrets & Rate Limiting

Purpose: Apply established defensive controls when `SECURE` requires headers, validation, secret handling, or rate limiting.

## Contents

- security headers
- input validation
- secret management
- rate limiting

## 1. Security Headers

| Header | Purpose | Priority |
|--------|---------|----------|
| `Content-Security-Policy` | Prevent XSS and injection | Critical |
| `Strict-Transport-Security` | Force HTTPS | Critical |
| `X-Content-Type-Options` | Prevent MIME sniffing | High |
| `X-Frame-Options` | Prevent clickjacking | High |
| `X-XSS-Protection` | Legacy XSS filter | Medium |
| `Referrer-Policy` | Control referrer leakage | Medium |
| `Permissions-Policy` | Disable unnecessary browser features | Medium |

### Next.js

```typescript
// next.config.js
const securityHeaders = [
  {
    key: 'Content-Security-Policy',
    value: [
      "default-src 'self'",
      "script-src 'self' 'unsafe-inline' 'unsafe-eval'", // Tighten in production
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: https:",
      "font-src 'self'",
      "connect-src 'self' https://api.example.com",
      "frame-ancestors 'none'",
      "base-uri 'self'",
      "form-action 'self'",
    ].join('; '),
  },
  { key: 'Strict-Transport-Security', value: 'max-age=31536000; includeSubDomains; preload' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'X-Frame-Options', value: 'DENY' },
  { key: 'X-XSS-Protection', value: '1; mode=block' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
];

module.exports = {
  async headers() {
    return [{ source: '/:path*', headers: securityHeaders }];
  },
};
```

### Express.js (`helmet`)

```typescript
import helmet from 'helmet';
app.use(helmet());

app.use(
  helmet.contentSecurityPolicy({
    directives: {
      defaultSrc: ["'self'"], scriptSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"], imgSrc: ["'self'", 'data:', 'https:'],
      connectSrc: ["'self'", 'https://api.example.com'], fontSrc: ["'self'"],
      objectSrc: ["'none'"], frameSrc: ["'none'"], upgradeInsecureRequests: [],
    },
  })
);
app.use(helmet.hsts({ maxAge: 31536000, includeSubDomains: true, preload: true }));
app.use(helmet.frameguard({ action: 'deny' }));
app.use(helmet.noSniff());
app.use(helmet.xssFilter());
app.use(helmet.referrerPolicy({ policy: 'strict-origin-when-cross-origin' }));
```

### CSP Violation Reporting

```typescript
{
  key: 'Content-Security-Policy-Report-Only',
  value: "default-src 'self'; report-uri /api/csp-report",
}

app.post('/api/csp-report', express.json({ type: 'application/csp-report' }), (req, res) => {
  console.warn('CSP Violation:', req.body);
  res.status(204).end();
});
```

## 2. Input Validation

Boundary validation is mandatory. Prefer `Zod` when adding runtime schemas.

### Zod Schema Examples

```typescript
import { z } from 'zod';

const emailSchema = z.string().email('Invalid email format').max(254, 'Email too long');
const passwordSchema = z.string()
  .min(8, 'Password must be at least 8 characters')
  .max(128, 'Password too long')
  .regex(/[A-Z]/, 'Must contain uppercase letter')
  .regex(/[a-z]/, 'Must contain lowercase letter')
  .regex(/[0-9]/, 'Must contain number')
  .regex(/[^A-Za-z0-9]/, 'Must contain special character');
const urlSchema = z.string().url('Invalid URL')
  .refine((url) => url.startsWith('https://'), 'URL must use HTTPS');
const uuidSchema = z.string().uuid('Invalid ID format');

const userFormSchema = z.object({
  email: emailSchema,
  password: passwordSchema,
  name: z.string().min(1).max(100).trim(),
  age: z.number().int().min(13).max(120).optional(),
});
```

### Common Validation Patterns

```typescript
const identifierSchema = z.string()
  .regex(/^[a-zA-Z_][a-zA-Z0-9_]*$/, 'Invalid identifier');

const safePathSchema = z.string()
  .refine((path) => !path.includes('..') && !path.startsWith('/'), 'Invalid path');

const jsonInputSchema = z.string()
  .max(10000, 'Payload too large')
  .transform((val) => JSON.parse(val));

const tagsSchema = z.array(z.string().max(50)).max(10, 'Too many tags');
const statusSchema = z.enum(['active', 'inactive', 'pending']);
```

### Express Validation Middleware

```typescript
import { z, ZodSchema } from 'zod';
import { Request, Response, NextFunction } from 'express';

function validate(schema: ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse({
      body: req.body, query: req.query, params: req.params,
    });
    if (!result.success) {
      return res.status(400).json({
        error: 'Validation failed',
        details: result.error.issues.map((i) => ({
          path: i.path.join('.'), message: i.message,
        })),
      });
    }
    req.validated = result.data;
    next();
  };
}
```

## 3. Secret Management

Never hardcode secrets. Prefer environment variables with schema validation, then move to managed secret stores for production.

### Environment Variables

```typescript
import { z } from 'zod';

const envSchema = z.object({
  API_KEY: z.string().min(1),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  NODE_ENV: z.enum(['development', 'production', 'test']),
});

const env = envSchema.parse(process.env);
export { env };
```

### `.env` Hygiene

```bash
# .gitignore
.env
.env.local
.env.*.local
*.pem
*.key

# .env.example
API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:pass@localhost:5432/db
JWT_SECRET=generate_a_32_char_secret_here
```

### AWS Secrets Manager

```typescript
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager';

const client = new SecretsManagerClient({ region: 'ap-northeast-1' });

async function getSecret(secretName: string): Promise<Record<string, string>> {
  const command = new GetSecretValueCommand({ SecretId: secretName });
  const response = await client.send(command);
  if (!response.SecretString) throw new Error('Secret not found');
  return JSON.parse(response.SecretString);
}
```

### HashiCorp Vault

```typescript
import Vault from 'node-vault';

const vault = Vault({
  apiVersion: 'v1',
  endpoint: process.env.VAULT_ADDR,
  token: process.env.VAULT_TOKEN,
});

async function getSecret(path: string): Promise<Record<string, string>> {
  const result = await vault.read(`secret/data/${path}`);
  return result.data.data;
}
```

### Rotation Pattern

```typescript
class SecretCache {
  private cache = new Map<string, { value: string; expiresAt: number }>();
  private ttlMs = 5 * 60 * 1000;

  async get(key: string, fetcher: () => Promise<string>): Promise<string> {
    const cached = this.cache.get(key);
    if (cached && cached.expiresAt > Date.now()) return cached.value;
    const value = await fetcher();
    this.cache.set(key, { value, expiresAt: Date.now() + this.ttlMs });
    return value;
  }
}
```

## 4. Rate Limiting

Use stricter limits on auth and expensive endpoints. Move to Redis-backed limits when the system is distributed.

### Express Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';
import { createClient } from 'redis';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: { error: 'Too many requests, please try again later' },
  standardHeaders: true,
  legacyHeaders: false,
});
app.use(limiter);

const authLimiter = rateLimit({
  windowMs: 60 * 60 * 1000,
  max: 5,
  skipSuccessfulRequests: true,
  message: { error: 'Too many login attempts, please try again later' },
});
app.use('/api/auth/login', authLimiter);

const redisClient = createClient({ url: process.env.REDIS_URL });
await redisClient.connect();

const distributedLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  store: new RedisStore({
    sendCommand: (...args: string[]) => redisClient.sendCommand(args),
  }),
});
```

### Next.js API Rate Limiting

```typescript
import { LRUCache } from 'lru-cache';

type RateLimitOptions = { interval: number; uniqueTokenPerInterval: number };

export function rateLimit(options: RateLimitOptions) {
  const tokenCache = new LRUCache<string, number[]>({
    max: options.uniqueTokenPerInterval,
    ttl: options.interval,
  });

  return {
    check: (limit: number, token: string): Promise<void> =>
      new Promise((resolve, reject) => {
        const tokenCount = tokenCache.get(token) || [0];
        if (tokenCount[0] >= limit) { reject(new Error('Rate limit exceeded')); return; }
        tokenCount[0] += 1;
        tokenCache.set(token, tokenCount);
        resolve();
      }),
  };
}
```
