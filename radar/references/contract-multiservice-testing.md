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
// ...
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
// ...
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
# ...
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
// ...
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
// ...
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
// ...
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
# ...
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
// ...
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
// ...
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
// ...
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
// ...
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
// ...
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

// ...
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
...
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
