# Load Testing Guide

k6/Locust/Artillery設定、ランプアップ戦略、SLO検証のリファレンス。

---

## Tool Comparison

| Feature | k6 | Locust | Artillery |
|---------|-----|--------|-----------|
| **Language** | JavaScript | Python | YAML/JS |
| **Protocol** | HTTP, WS, gRPC | HTTP, custom | HTTP, WS, Socket.io |
| **Distributed** | k6 Cloud, k6-operator | Built-in | Artillery Cloud |
| **Metrics** | Built-in + extensions | Minimal built-in | Built-in |
| **Learning curve** | Medium | Low | Low |
| **Best for** | Performance CI/CD | Custom protocols | Quick API tests |

---

## k6 Configuration Patterns

### Basic Load Test

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 50 },   // Ramp up
    { duration: '5m', target: 50 },   // Steady state
    { duration: '2m', target: 100 },  // Peak
    { duration: '5m', target: 100 },  // Sustained peak
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    http_req_failed: ['rate<0.01'],
    checks: ['rate>0.99'],
  },
};

export default function () {
  const res = http.get('https://api.example.com/items');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```

### SLO Validation Test

```javascript
export const options = {
  scenarios: {
    slo_validation: {
      executor: 'constant-arrival-rate',
      rate: 100,           // 100 RPS
      timeUnit: '1s',
      duration: '10m',
      preAllocatedVUs: 50,
      maxVUs: 200,
    },
  },
  thresholds: {
    // SLO: 99.9% availability
    http_req_failed: ['rate<0.001'],
    // SLO: p99 latency < 200ms
    http_req_duration: ['p(99)<200'],
  },
};
```

---

## Ramp-Up Strategies

| Strategy | Pattern | Use Case |
|----------|---------|----------|
| **Linear ramp** | Gradual increase | General load testing |
| **Step ramp** | Plateau at each level | Find breaking point |
| **Spike** | Sudden jump to peak | Flash sale simulation |
| **Soak** | Steady for hours | Memory leak detection |
| **Stress** | Beyond expected peak | Find system limits |

### Step Ramp Pattern

```javascript
export const options = {
  stages: [
    { duration: '5m', target: 100 },  // Step 1
    { duration: '5m', target: 100 },  // Hold
    { duration: '5m', target: 200 },  // Step 2
    { duration: '5m', target: 200 },  // Hold
    { duration: '5m', target: 400 },  // Step 3
    { duration: '5m', target: 400 },  // Hold
    { duration: '5m', target: 0 },    // Ramp down
  ],
};
```

---

## Locust Configuration

```python
from locust import HttpUser, task, between

class ApiUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def list_items(self):
        self.client.get("/api/items")

    @task(1)
    def create_item(self):
        self.client.post("/api/items", json={
            "name": "test-item",
            "price": 9.99
        })

    def on_start(self):
        """Login on start."""
        self.client.post("/auth/login", json={
            "username": "loadtest",
            "password": "test123"
        })
```

---

## Artillery Configuration

```yaml
config:
  target: "https://api.example.com"
  phases:
    - duration: 120
      arrivalRate: 10
      name: "Warm up"
    - duration: 300
      arrivalRate: 50
      name: "Sustained load"
    - duration: 120
      arrivalRate: 100
      name: "Peak"
  ensure:
    p95: 500
    maxErrorRate: 1

scenarios:
  - name: "Browse and purchase"
    flow:
      - get:
          url: "/api/products"
          capture:
            - json: "$[0].id"
              as: "productId"
      - get:
          url: "/api/products/{{ productId }}"
      - post:
          url: "/api/cart"
          json:
            productId: "{{ productId }}"
            quantity: 1
```

---

## CI Integration

### k6 in CI Pipeline

```yaml
# GitHub Actions
load-test:
  runs-on: ubuntu-latest
  steps:
    - uses: grafana/k6-action@v0.3.1
      with:
        filename: tests/load/api-test.js
        flags: --out json=results.json
    - name: Check results
      run: |
        if jq -e '.root_group.checks.passes / .root_group.checks.total < 0.99' results.json; then
          echo "Load test failed: check pass rate below 99%"
          exit 1
        fi
```

### Load Test Report Template

```markdown
## Load Test Report

### Test Parameters
- Duration: [X] minutes
- Peak VUs: [N]
- Target RPS: [N]

### Results
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| p95 latency | < 500ms | Xms | PASS/FAIL |
| p99 latency | < 1000ms | Xms | PASS/FAIL |
| Error rate | < 1% | X% | PASS/FAIL |
| Throughput | > 100 RPS | X RPS | PASS/FAIL |

### Bottlenecks Identified
1. [Description + evidence]

### Recommendations
1. [Action item]
```
