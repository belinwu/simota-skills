# Contract Testing Patterns

Pact CDC、AsyncAPIイベント契約、CI統合のリファレンス。

---

## Contract Testing Overview

| Type | Direction | Tool | Use Case |
|------|-----------|------|----------|
| **Consumer-Driven (CDC)** | Consumer → Provider | Pact | HTTP APIs |
| **Provider-Driven** | Provider → Consumer | OpenAPI + validation | Public APIs |
| **Bi-directional** | Both ways | Pact + OpenAPI | Hybrid |
| **Event Contract** | Publisher → Subscriber | Pact / AsyncAPI | Messaging |

---

## Pact Consumer-Driven Contracts

### Consumer Test (JavaScript)

```javascript
const { PactV3, MatchersV3 } = require('@pact-foundation/pact');
const { like, eachLike, string } = MatchersV3;

const provider = new PactV3({
  consumer: 'OrderService',
  provider: 'ProductService',
});

describe('Product API', () => {
  it('returns product details', async () => {
    await provider
      .given('product 123 exists')
      .uponReceiving('a request for product 123')
      .withRequest({
        method: 'GET',
        path: '/api/products/123',
        headers: { Accept: 'application/json' },
      })
      .willRespondWith({
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: {
          id: string('123'),
          name: string('Widget'),
          price: like(9.99),
          inStock: like(true),
        },
      })
      .executeTest(async (mockServer) => {
        const product = await fetchProduct(mockServer.url, '123');
        expect(product.name).toBe('Widget');
      });
  });
});
```

### Provider Verification (Python)

```python
from pact import Verifier

def test_provider():
    verifier = Verifier(
        provider="ProductService",
        provider_base_url="http://localhost:8080",
    )

    output, _ = verifier.verify_pacts(
        pact_url="https://pact-broker.example.com/pacts/provider/ProductService/consumer/OrderService/latest",
        provider_states_setup_url="http://localhost:8080/_pact/setup",
        publish_verification_results=True,
        provider_app_version="1.2.3",
    )

    assert output == 0
```

---

## AsyncAPI Event Contracts

### Event Contract Definition

```yaml
asyncapi: '2.6.0'
info:
  title: Order Events
  version: '1.0.0'

channels:
  orders/created:
    publish:
      operationId: orderCreated
      message:
        name: OrderCreated
        payload:
          type: object
          required: [orderId, customerId, totalAmount, createdAt]
          properties:
            orderId:
              type: string
              format: uuid
            customerId:
              type: string
            totalAmount:
              type: number
              minimum: 0
            items:
              type: array
              items:
                type: object
                required: [productId, quantity]
                properties:
                  productId:
                    type: string
                  quantity:
                    type: integer
                    minimum: 1
            createdAt:
              type: string
              format: date-time
```

### Message Pact Test

```javascript
const { MessageConsumerPact } = require('@pact-foundation/pact');

describe('Order Created Event', () => {
  const messagePact = new MessageConsumerPact({
    consumer: 'InventoryService',
    provider: 'OrderService',
  });

  it('processes order created event', () => {
    return messagePact
      .expectsToReceive('an order created event')
      .withContent({
        orderId: like('ord-123'),
        customerId: like('cust-456'),
        totalAmount: like(99.99),
        items: eachLike({ productId: 'prod-789', quantity: 2 }),
      })
      .verify(async (message) => {
        const result = await processOrderEvent(message);
        expect(result.inventoryUpdated).toBe(true);
      });
  });
});
```

---

## CI Integration

### Pact Broker Workflow

```
Consumer CI:                    Provider CI:
1. Run consumer tests      →   1. Pull pacts from broker
2. Generate pact files     →   2. Verify against provider
3. Publish to Pact Broker  →   3. Publish verification results
4. can-i-deploy check      →   4. can-i-deploy check
5. Deploy consumer         →   5. Deploy provider
```

### GitHub Actions Pipeline

```yaml
contract-test:
  runs-on: ubuntu-latest
  steps:
    - name: Run consumer tests
      run: npm test -- --testPathPattern=pact

    - name: Publish pacts
      run: |
        npx pact-broker publish ./pacts \
          --consumer-app-version=${{ github.sha }} \
          --branch=${{ github.ref_name }} \
          --broker-base-url=${{ secrets.PACT_BROKER_URL }} \
          --broker-token=${{ secrets.PACT_BROKER_TOKEN }}

    - name: Can I Deploy?
      run: |
        npx pact-broker can-i-deploy \
          --pacticipant=OrderService \
          --version=${{ github.sha }} \
          --to-environment=production \
          --broker-base-url=${{ secrets.PACT_BROKER_URL }}
```

---

## Breaking Change Detection

| Change Type | Breaking? | Detection |
|-------------|-----------|-----------|
| **Add optional field** | No | Safe |
| **Add required field** | Yes (provider) | Pact verification fails |
| **Remove field** | Yes (if consumed) | Consumer test fails |
| **Change field type** | Yes | Both sides fail |
| **Change enum values** | Maybe | Depends on consumer usage |
| **Change URL path** | Yes | Consumer test fails |
| **Add new endpoint** | No | Safe |

### Contract Versioning Strategy

```markdown
- Use Pact Broker with `can-i-deploy` before every deployment
- Tag pacts with branch name and environment
- Use pending pacts for new interactions (WIP)
- Enable `enablePending: true` on provider verification
- Run webhook on pact change to trigger provider verification
```
