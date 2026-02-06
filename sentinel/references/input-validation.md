# Input Validation Patterns

Zod schema examples, common validation patterns, and Express middleware for input validation.

---

## Zod Schema Examples

```typescript
import { z } from 'zod';

// Email validation
const emailSchema = z.string()
  .email('Invalid email format')
  .max(254, 'Email too long');

// Password validation
const passwordSchema = z.string()
  .min(8, 'Password must be at least 8 characters')
  .max(128, 'Password too long')
  .regex(/[A-Z]/, 'Must contain uppercase letter')
  .regex(/[a-z]/, 'Must contain lowercase letter')
  .regex(/[0-9]/, 'Must contain number')
  .regex(/[^A-Za-z0-9]/, 'Must contain special character');

// URL validation
const urlSchema = z.string()
  .url('Invalid URL')
  .refine(
    (url) => url.startsWith('https://'),
    'URL must use HTTPS'
  );

// UUID validation
const uuidSchema = z.string().uuid('Invalid ID format');

// Number with bounds
const amountSchema = z.number()
  .positive('Amount must be positive')
  .max(1000000, 'Amount exceeds maximum');

// Sanitized string (no HTML)
const safeStringSchema = z.string()
  .max(1000)
  .transform((val) => val.replace(/<[^>]*>/g, ''));

// Form validation example
const userFormSchema = z.object({
  email: emailSchema,
  password: passwordSchema,
  name: z.string().min(1).max(100).trim(),
  age: z.number().int().min(13).max(120).optional(),
});

// Usage
function validateUserInput(data: unknown) {
  const result = userFormSchema.safeParse(data);
  if (!result.success) {
    throw new Error(result.error.issues[0].message);
  }
  return result.data;
}
```

---

## Common Validation Patterns

```typescript
// SQL-safe identifier (table/column names)
const identifierSchema = z.string()
  .regex(/^[a-zA-Z_][a-zA-Z0-9_]*$/, 'Invalid identifier');

// File path (prevent traversal)
const safePathSchema = z.string()
  .refine(
    (path) => !path.includes('..') && !path.startsWith('/'),
    'Invalid path'
  );

// JSON input with size limit
const jsonInputSchema = z.string()
  .max(10000, 'Payload too large')
  .transform((val) => JSON.parse(val));

// Array with length limit
const tagsSchema = z.array(z.string().max(50))
  .max(10, 'Too many tags');

// Enum validation
const statusSchema = z.enum(['active', 'inactive', 'pending']);
```

---

## Express Validation Middleware

```typescript
import { z, ZodSchema } from 'zod';
import { Request, Response, NextFunction } from 'express';

function validate(schema: ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse({
      body: req.body,
      query: req.query,
      params: req.params,
    });

    if (!result.success) {
      return res.status(400).json({
        error: 'Validation failed',
        details: result.error.issues.map((i) => ({
          path: i.path.join('.'),
          message: i.message,
        })),
      });
    }

    req.validated = result.data;
    next();
  };
}

// Usage
const createUserSchema = z.object({
  body: z.object({
    email: z.string().email(),
    password: z.string().min(8),
  }),
});

app.post('/users', validate(createUserSchema), (req, res) => {
  const { email, password } = req.validated.body;
  // Safe to use
});
```

---

## Environment Variable Validation

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
