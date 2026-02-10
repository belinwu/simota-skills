# Contract & Multi-Service Testing

マイクロサービス間のAPI契約テストと統合テスト戦略。

---

## Agent Boundary

| Responsibility | Primary Agent | Notes |
|----------------|--------------|-------|
| API Contract Tests (unit-level) | **Radar** | Pact, gRPC, GraphQL contracts |
| Multi-Service Integration (unit-level) | **Radar** | Testcontainers, stubs |
| E2E Multi-Service Flows | **Voyager** | Browser-driven full stack |
| Service Infrastructure | **Gear** | Docker Compose, CI pipelines |
| API Design / Schema | **Architect** | OpenAPI, GraphQL schema |

---

## REST API Contract Testing (Pact)

### Consumer-Driven Contract

```typescript
// consumer/tests/user-api.pact.spec.ts
import { PactV4, MatchersV3 } from '@pact-foundation/pact';

const provider = new PactV4({
  consumer: 'frontend-app',
  provider: 'user-service',
  dir: './pacts',
});

describe('User API Contract', () => {
  it('gets user by ID', async () => {
    await provider
      .addInteraction()
      .given('user 123 exists')
      .uponReceiving('a request for user 123')
      .withRequest('GET', '/api/users/123', (builder) => {
        builder.headers({ Accept: 'application/json' });
      })
      .willRespondWith(200, (builder) => {
        builder
          .headers({ 'Content-Type': 'application/json' })
          .jsonBody({
            id: MatchersV3.integer(123),
            name: MatchersV3.string('John Doe'),
            email: MatchersV3.email('john@example.com'),
            createdAt: MatchersV3.iso8601DateTime(),
          });
      })
      .executeTest(async (mockServer) => {
        const response = await fetch(`${mockServer.url}/api/users/123`, {
          headers: { Accept: 'application/json' },
        });
        const user = await response.json();
        expect(user.id).toBe(123);
        expect(user.name).toBeTruthy();
      });
  });

  it('returns 404 for missing user', async () => {
    await provider
      .addInteraction()
      .given('user 999 does not exist')
      .uponReceiving('a request for non-existent user')
      .withRequest('GET', '/api/users/999')
      .willRespondWith(404, (builder) => {
        builder.jsonBody({
          error: MatchersV3.string('User not found'),
          code: MatchersV3.string('USER_NOT_FOUND'),
        });
      })
      .executeTest(async (mockServer) => {
        const response = await fetch(`${mockServer.url}/api/users/999`);
        expect(response.status).toBe(404);
      });
  });
});
```

### Provider Verification

```typescript
// provider/tests/pact-verification.spec.ts
import { Verifier } from '@pact-foundation/pact';

describe('Pact Verification', () => {
  it('validates contracts against user-service', async () => {
    const verifier = new Verifier({
      providerBaseUrl: 'http://localhost:3001',
      pactUrls: ['./pacts/frontend-app-user-service.json'],
      // Or from Pact Broker
      // pactBrokerUrl: process.env.PACT_BROKER_URL,
      // pactBrokerToken: process.env.PACT_BROKER_TOKEN,
      // providerVersion: process.env.GIT_SHA,

      stateHandlers: {
        'user 123 exists': async () => {
          await db.users.create({ id: 123, name: 'John Doe', email: 'john@example.com' });
        },
        'user 999 does not exist': async () => {
          await db.users.deleteWhere({ id: 999 });
        },
      },
    });

    await verifier.verifyProvider();
  });
});
```

### Pact Broker Integration

```yaml
# .github/workflows/pact.yml
jobs:
  consumer-test:
    steps:
      - run: npm test -- --project=pact
      - name: Publish Pact
        run: |
          npx pact-broker publish ./pacts \
            --consumer-app-version=${{ github.sha }} \
            --branch=${{ github.ref_name }} \
            --broker-base-url=${{ secrets.PACT_BROKER_URL }} \
            --broker-token=${{ secrets.PACT_BROKER_TOKEN }}

  can-i-deploy:
    needs: consumer-test
    steps:
      - name: Can I Deploy?
        run: |
          npx pact-broker can-i-deploy \
            --pacticipant=frontend-app \
            --version=${{ github.sha }} \
            --to-environment=production \
            --broker-base-url=${{ secrets.PACT_BROKER_URL }}
```

---

## gRPC Contract Testing

### buf Breaking Change Detection

```yaml
# buf.yaml
version: v2
modules:
  - path: proto
    lint:
      use:
        - DEFAULT
    breaking:
      use:
        - FILE
```

```bash
# Check for breaking changes against main branch
buf breaking proto --against '.git#branch=main'

# Check against Buf Schema Registry
buf breaking proto --against 'buf.build/myorg/myapi'
```

### gRPC Mock Testing

```typescript
// tests/grpc-service.spec.ts
import { createServer, createClient } from 'nice-grpc';
import { UserServiceDefinition } from './generated/user_service';

describe('User gRPC Service', () => {
  let server: any;
  let client: any;

  beforeAll(async () => {
    server = createServer();
    server.add(UserServiceDefinition, {
      async getUser(request) {
        if (request.id === '123') {
          return { id: '123', name: 'John', email: 'john@test.com' };
        }
        throw new Error('NOT_FOUND');
      },
    });
    const port = await server.listen('localhost:0');
    client = createClient(UserServiceDefinition, `localhost:${port}`);
  });

  afterAll(() => server.shutdown());

  it('returns user by ID', async () => {
    const user = await client.getUser({ id: '123' });
    expect(user.name).toBe('John');
  });
});
```

### Proto Compatibility Matrix

| Check | Tool | When |
|-------|------|------|
| Wire compatibility | `buf breaking` | Every PR |
| Linting | `buf lint` | Every PR |
| Code generation | `buf generate` | On proto change |
| Mock generation | `nice-grpc` / `grpcmock` | Test setup |

---

## GraphQL Contract Testing

### Schema-First Contract

```typescript
// tests/graphql-contract.spec.ts
import { buildSchema, graphql } from 'graphql';
import { readFileSync } from 'fs';

describe('GraphQL Schema Contract', () => {
  const schema = buildSchema(readFileSync('./schema.graphql', 'utf-8'));

  it('User type has required fields', () => {
    const userType = schema.getType('User');
    expect(userType).toBeDefined();

    const fields = (userType as any).getFields();
    expect(fields.id).toBeDefined();
    expect(fields.name).toBeDefined();
    expect(fields.email).toBeDefined();
  });

  it('resolves user query correctly', async () => {
    const result = await graphql({
      schema,
      source: '{ user(id: "123") { id name email } }',
      rootValue: {
        user: ({ id }: { id: string }) => ({
          id, name: 'John', email: 'john@test.com',
        }),
      },
    });

    expect(result.errors).toBeUndefined();
    expect(result.data?.user).toMatchObject({
      id: '123',
      name: 'John',
    });
  });
});
```

### Schema Diff Detection

```bash
# Install graphql-inspector
npm install -D @graphql-inspector/cli

# Check for breaking changes
npx graphql-inspector diff schema-main.graphql schema-pr.graphql

# Validate operations against schema
npx graphql-inspector validate './src/**/*.graphql' schema.graphql
```

### Apollo Federation Service Testing

```typescript
// tests/federation.spec.ts
import { ApolloServer } from '@apollo/server';
import { buildSubgraphSchema } from '@apollo/subgraph';

describe('User Subgraph', () => {
  let server: ApolloServer;

  beforeAll(async () => {
    server = new ApolloServer({
      schema: buildSubgraphSchema([{ typeDefs, resolvers }]),
    });
    await server.start();
  });

  afterAll(() => server.stop());

  it('resolves _entities for User', async () => {
    const result = await server.executeOperation({
      query: `
        query ($representations: [_Any!]!) {
          _entities(representations: $representations) {
            ... on User { id name email }
          }
        }
      `,
      variables: {
        representations: [{ __typename: 'User', id: '123' }],
      },
    });

    expect(result.body.kind).toBe('single');
  });
});
```

---

## Event-Driven Contract Testing

### AsyncAPI Specification

```yaml
# asyncapi.yaml
asyncapi: '2.6.0'
info:
  title: User Events
  version: '1.0.0'

channels:
  user/created:
    publish:
      message:
        payload:
          type: object
          required: [userId, email, timestamp]
          properties:
            userId:
              type: string
              format: uuid
            email:
              type: string
              format: email
            timestamp:
              type: string
              format: date-time
```

### Message Contract Validation

```typescript
// tests/event-contracts.spec.ts
import Ajv from 'ajv';
import addFormats from 'ajv-formats';
import asyncApiSchema from './asyncapi.json';

const ajv = new Ajv();
addFormats(ajv);

describe('Event Contracts', () => {
  it('user.created event matches schema', () => {
    const schema = asyncApiSchema.channels['user/created'].publish.message.payload;
    const validate = ajv.compile(schema);

    const event = {
      userId: '550e8400-e29b-41d4-a716-446655440000',
      email: 'user@example.com',
      timestamp: '2024-01-15T10:30:00Z',
    };

    expect(validate(event)).toBe(true);
  });

  it('rejects invalid event', () => {
    const schema = asyncApiSchema.channels['user/created'].publish.message.payload;
    const validate = ajv.compile(schema);

    const invalidEvent = { userId: 123 }; // missing fields, wrong type
    expect(validate(invalidEvent)).toBe(false);
  });
});
```

### Kafka Consumer/Producer Testing

```typescript
// tests/kafka-integration.spec.ts
import { Kafka } from 'kafkajs';
import { GenericContainer, Wait } from 'testcontainers';

describe('Kafka Event Integration', () => {
  let container: any;
  let kafka: Kafka;

  beforeAll(async () => {
    container = await new GenericContainer('confluentinc/cp-kafka:7.5.0')
      .withExposedPorts(9092)
      .withEnvironment({
        KAFKA_ADVERTISED_LISTENERS: 'PLAINTEXT://localhost:9092',
        KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: '1',
      })
      .withWaitStrategy(Wait.forLogMessage('started'))
      .start();

    kafka = new Kafka({
      brokers: [`localhost:${container.getMappedPort(9092)}`],
    });
  }, 60000);

  afterAll(async () => {
    await container?.stop();
  });

  it('publishes and consumes user.created event', async () => {
    const producer = kafka.producer();
    const consumer = kafka.consumer({ groupId: 'test-group' });

    await producer.connect();
    await consumer.connect();
    await consumer.subscribe({ topic: 'user.created' });

    const received: any[] = [];
    await consumer.run({
      eachMessage: async ({ message }) => {
        received.push(JSON.parse(message.value!.toString()));
      },
    });

    await producer.send({
      topic: 'user.created',
      messages: [{
        value: JSON.stringify({
          userId: '123',
          email: 'test@example.com',
          timestamp: new Date().toISOString(),
        }),
      }],
    });

    // Wait for consumption
    await new Promise(r => setTimeout(r, 2000));
    expect(received).toHaveLength(1);
    expect(received[0].userId).toBe('123');

    await producer.disconnect();
    await consumer.disconnect();
  });
});
```

---

## Testcontainers Deep Patterns

### Multi-Container Composition

```typescript
// tests/testcontainers-setup.ts
import { PostgreSqlContainer } from '@testcontainers/postgresql';
import { RedisContainer } from '@testcontainers/redis';
import { GenericContainer, Network } from 'testcontainers';

export async function setupTestEnvironment() {
  const network = await new Network().start();

  const postgres = await new PostgreSqlContainer('postgres:16')
    .withNetwork(network)
    .withNetworkAliases('db')
    .withDatabase('testdb')
    .start();

  const redis = await new RedisContainer('redis:7')
    .withNetwork(network)
    .withNetworkAliases('cache')
    .start();

  return {
    postgres,
    redis,
    network,
    cleanup: async () => {
      await redis.stop();
      await postgres.stop();
      await network.stop();
    },
  };
}
```

### LocalStack for AWS Services

```typescript
// tests/localstack.spec.ts
import { LocalstackContainer } from '@testcontainers/localstack';
import { S3Client, PutObjectCommand, GetObjectCommand } from '@aws-sdk/client-s3';

describe('S3 Integration', () => {
  let container: any;
  let s3: S3Client;

  beforeAll(async () => {
    container = await new LocalstackContainer('localstack/localstack:3')
      .withServices('s3')
      .start();

    s3 = new S3Client({
      endpoint: container.getConnectionUri(),
      region: 'us-east-1',
      credentials: { accessKeyId: 'test', secretAccessKey: 'test' },
      forcePathStyle: true,
    });

    // Create test bucket
    await s3.send(new (await import('@aws-sdk/client-s3')).CreateBucketCommand({
      Bucket: 'test-bucket',
    }));
  }, 60000);

  afterAll(() => container?.stop());

  it('uploads and retrieves file', async () => {
    await s3.send(new PutObjectCommand({
      Bucket: 'test-bucket',
      Key: 'test.txt',
      Body: 'Hello World',
    }));

    const result = await s3.send(new GetObjectCommand({
      Bucket: 'test-bucket',
      Key: 'test.txt',
    }));

    const body = await result.Body!.transformToString();
    expect(body).toBe('Hello World');
  });
});
```

### Container Reuse Strategy

| Strategy | Use Case | Tradeoff |
|----------|----------|----------|
| **Per-Test** | Full isolation | Slow (container startup per test) |
| **Per-Suite** | Balance of speed/isolation | State leak risk between tests |
| **Per-Run** | Maximum speed | Requires careful cleanup |
| **Reusable** | Local dev | `withReuse()` flag, manual cleanup |

```typescript
// Reusable container for local development
const container = await new PostgreSqlContainer()
  .withReuse()
  .start();
```

---

## Multi-Service Integration Patterns

### Service Stub (WireMock)

```typescript
// tests/wiremock-stub.spec.ts
import { WireMockContainer } from 'wiremock-testcontainers-node';

describe('Payment Service Integration', () => {
  let wiremock: any;

  beforeAll(async () => {
    wiremock = await new WireMockContainer('wiremock/wiremock:3.3.1')
      .withMapping({
        request: {
          method: 'POST',
          url: '/api/payments',
          bodyPatterns: [{ matchesJsonPath: '$.amount' }],
        },
        response: {
          status: 200,
          jsonBody: { id: 'pay_123', status: 'succeeded' },
        },
      })
      .start();
  });

  afterAll(() => wiremock?.stop());

  it('processes payment through stub', async () => {
    const paymentUrl = `http://localhost:${wiremock.getMappedPort(8080)}`;
    const response = await fetch(`${paymentUrl}/api/payments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ amount: 1000, currency: 'USD' }),
    });

    const result = await response.json();
    expect(result.status).toBe('succeeded');
  });
});
```

### Saga Testing Pattern

```typescript
// tests/order-saga.spec.ts
describe('Order Saga', () => {
  it('completes order when all services succeed', async () => {
    // 1. Create order
    const order = await orderService.create({ items: [{ id: 1, qty: 2 }] });
    expect(order.status).toBe('pending');

    // 2. Reserve inventory
    const reservation = await inventoryService.reserve(order.id, order.items);
    expect(reservation.status).toBe('reserved');

    // 3. Process payment
    const payment = await paymentService.charge(order.id, order.total);
    expect(payment.status).toBe('charged');

    // 4. Confirm order
    const confirmed = await orderService.confirm(order.id);
    expect(confirmed.status).toBe('confirmed');
  });

  it('compensates when payment fails', async () => {
    const order = await orderService.create({ items: [{ id: 1, qty: 2 }] });
    await inventoryService.reserve(order.id, order.items);

    // Payment fails
    paymentService.simulateFailure('insufficient_funds');
    await expect(paymentService.charge(order.id, order.total)).rejects.toThrow();

    // Compensation: inventory should be released
    const inventory = await inventoryService.getReservation(order.id);
    expect(inventory.status).toBe('released');

    // Order should be cancelled
    const cancelled = await orderService.get(order.id);
    expect(cancelled.status).toBe('cancelled');
  });
});
```

---

## Decision Tree: Contract Test Type Selection

```
API Communication?
        │
  ┌─────┴──────┐
  │            │
REST ▼     Event ▼
  │         │
  ▼         ▼
┌────────┐ ┌──────────┐
│ Pact   │ │ AsyncAPI │
│ or     │ │ schema   │
│ OpenAPI│ │ validate │
└────┬───┘ └────┬─────┘
     │          │
     ▼          ▼
┌──────────────────────┐
│ Need real service?   │
└──────────┬───────────┘
     ┌─────┴─────┐
     │           │
   Yes ▼       No ▼
┌──────────┐ ┌───────────┐
│Testcont. │ │ WireMock  │
│or Docker │ │ or MSW    │
│Compose   │ │ stub      │
└──────────┘ └───────────┘

Multi-page user flow? → Handoff to Voyager
```

---

## Quick Reference

| Test Type | Tool | Scope | Speed |
|-----------|------|-------|-------|
| REST Contract | Pact | Consumer↔Provider | Fast |
| gRPC Contract | buf breaking | Schema compatibility | Fast |
| GraphQL Contract | graphql-inspector | Schema diff | Fast |
| Event Contract | AsyncAPI + Ajv | Message schema | Fast |
| Service Integration | Testcontainers | Real service | Medium |
| Service Stub | WireMock / MSW | Mock service | Fast |
| Multi-Service E2E | Voyager handoff | Full stack | Slow |
