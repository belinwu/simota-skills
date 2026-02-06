# Secret Management

Environment variable best practices, .env file security, cloud secret stores, and rotation patterns.

---

## Environment Variables Best Practices

```typescript
// BAD: Hardcoded secrets
const API_KEY = 'sk_live_abc123';

// GOOD: From environment
const API_KEY = process.env.API_KEY;

// BETTER: With validation
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

---

## .env File Security

```bash
# .gitignore - ALWAYS include
.env
.env.local
.env.*.local
*.pem
*.key

# .env.example - Safe template (no real values)
API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:pass@localhost:5432/db
JWT_SECRET=generate_a_32_char_secret_here
```

---

## AWS Secrets Manager

```typescript
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager';

const client = new SecretsManagerClient({ region: 'ap-northeast-1' });

async function getSecret(secretName: string): Promise<Record<string, string>> {
  const command = new GetSecretValueCommand({ SecretId: secretName });
  const response = await client.send(command);

  if (!response.SecretString) {
    throw new Error('Secret not found');
  }

  return JSON.parse(response.SecretString);
}

// Usage
const secrets = await getSecret('production/api-keys');
const apiKey = secrets.STRIPE_API_KEY;
```

---

## HashiCorp Vault

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

// Usage
const secrets = await getSecret('production/database');
const dbPassword = secrets.password;
```

---

## Secret Rotation Pattern

```typescript
// Cache secrets with TTL for rotation
class SecretCache {
  private cache = new Map<string, { value: string; expiresAt: number }>();
  private ttlMs = 5 * 60 * 1000; // 5 minutes

  async get(key: string, fetcher: () => Promise<string>): Promise<string> {
    const cached = this.cache.get(key);
    if (cached && cached.expiresAt > Date.now()) {
      return cached.value;
    }

    const value = await fetcher();
    this.cache.set(key, { value, expiresAt: Date.now() + this.ttlMs });
    return value;
  }
}

const secretCache = new SecretCache();
const apiKey = await secretCache.get('API_KEY', () => getSecret('api-key'));
```
