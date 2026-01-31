# Validation Recipes Reference

Builder agent's Zod validation patterns.

## Basic Object Validation

```typescript
import { z } from 'zod';

// User schema with refinements
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email('Invalid email format'),
  name: z.string().min(1, 'Name is required').max(100),
  age: z.number().int().min(0).max(150).optional(),
  role: z.enum(['admin', 'user', 'guest']),
  createdAt: z.coerce.date(),
});

type User = z.infer<typeof UserSchema>;
```

## Nested Objects and Arrays

```typescript
const AddressSchema = z.object({
  street: z.string().min(1),
  city: z.string().min(1),
  postalCode: z.string().regex(/^\d{3}-\d{4}$/, 'Format: 123-4567'),
  country: z.string().length(2), // ISO country code
});

const OrderSchema = z.object({
  id: z.string().uuid(),
  customer: z.object({
    name: z.string(),
    email: z.string().email(),
  }),
  items: z.array(z.object({
    productId: z.string(),
    quantity: z.number().int().positive(),
    price: z.number().positive(),
  })).min(1, 'Order must have at least one item'),
  shippingAddress: AddressSchema,
  billingAddress: AddressSchema.optional(),
});
```

## Conditional Validation (Discriminated Union)

```typescript
const PaymentSchema = z.discriminatedUnion('method', [
  z.object({
    method: z.literal('credit_card'),
    cardNumber: z.string().regex(/^\d{16}$/),
    expiryMonth: z.number().min(1).max(12),
    expiryYear: z.number().min(2024),
    cvv: z.string().regex(/^\d{3,4}$/),
  }),
  z.object({
    method: z.literal('bank_transfer'),
    bankCode: z.string().length(4),
    accountNumber: z.string().min(7).max(14),
  }),
  z.object({
    method: z.literal('paypal'),
    email: z.string().email(),
  }),
]);
```

## Custom Refinements

```typescript
const PasswordSchema = z.string()
  .min(8, 'Password must be at least 8 characters')
  .regex(/[A-Z]/, 'Must contain uppercase letter')
  .regex(/[a-z]/, 'Must contain lowercase letter')
  .regex(/[0-9]/, 'Must contain number')
  .regex(/[^A-Za-z0-9]/, 'Must contain special character');

const RegistrationSchema = z.object({
  email: z.string().email(),
  password: PasswordSchema,
  confirmPassword: z.string(),
}).refine(data => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});
```

## Transform and Preprocess

```typescript
const SearchQuerySchema = z.object({
  q: z.string().transform(s => s.trim().toLowerCase()),
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  sort: z.enum(['asc', 'desc']).default('desc'),
  tags: z.preprocess(
    (val) => typeof val === 'string' ? val.split(',') : val,
    z.array(z.string()).default([])
  ),
});
```

## Safe Parsing Pattern

```typescript
function parseRequest<T>(
  schema: z.ZodType<T>,
  data: unknown
): Result<T, ValidationError> {
  const result = schema.safeParse(data);

  if (!result.success) {
    const errors = result.error.errors.map(e => ({
      path: e.path.join('.'),
      message: e.message,
    }));
    return err(new ValidationError('Validation failed', errors));
  }

  return ok(result.data);
}

// Usage
const result = parseRequest(UserSchema, requestBody);
if (result.isErr()) {
  return res.status(400).json({ errors: result.error.details });
}
const user = result.value;
```
