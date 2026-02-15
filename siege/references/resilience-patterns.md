# Resilience Patterns Reference

サーキットブレーカー、バルクヘッド、リトライ検証パターンのリファレンス。

---

## Pattern Overview

| Pattern | Purpose | Failure Type |
|---------|---------|-------------|
| **Circuit Breaker** | Stop calling failing service | Downstream failure |
| **Retry** | Recover from transient errors | Transient failure |
| **Bulkhead** | Isolate failure domains | Resource exhaustion |
| **Timeout** | Bound wait time | Slow responses |
| **Fallback** | Provide degraded response | Any failure |
| **Rate Limiter** | Protect from overload | Traffic spike |
| **Shed Load** | Drop excess traffic | Capacity exceeded |

---

## Circuit Breaker

### State Machine

```
        success / threshold reset
    ┌──────────────────────────────────┐
    ↓                                  │
 [CLOSED] ──failure threshold──→ [OPEN] ──timeout──→ [HALF-OPEN]
    ↑                                                    │
    └──────────── success ───────────────────────────────┘
    └──────────── failure ──→ [OPEN] ←───────────────────┘
```

### Configuration Parameters

| Parameter | Description | Typical Value |
|-----------|-------------|---------------|
| **Failure threshold** | Failures to open | 5 failures in 60s |
| **Success threshold** | Successes to close | 3 consecutive |
| **Timeout** | Time in OPEN state | 30-60 seconds |
| **Half-open limit** | Requests allowed in HALF-OPEN | 1-3 requests |

### Implementation

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30, success_threshold=3):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        self.state = "CLOSED"
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None

    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
            else:
                raise CircuitOpenError()

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        if self.state == "HALF_OPEN":
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = "CLOSED"
                self.failure_count = 0
                self.success_count = 0

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            self.success_count = 0
```

---

## Retry Patterns

### Retry Strategies

| Strategy | Delay | Use Case |
|----------|-------|----------|
| **Immediate** | 0ms | Network blip |
| **Fixed delay** | 1s, 1s, 1s | Rate-limited API |
| **Exponential backoff** | 1s, 2s, 4s, 8s | General transient errors |
| **Exponential + jitter** | 1s±random, 2s±random | High concurrency |
| **Linear backoff** | 1s, 2s, 3s | Gradual recovery |

### Retry Decision Matrix

| Error Type | Retry? | Strategy |
|-----------|--------|----------|
| **4xx Client Error** | No (except 429) | — |
| **429 Too Many Requests** | Yes | Respect Retry-After header |
| **500 Internal Error** | Maybe (1-2 times) | Exponential backoff |
| **502/503/504** | Yes | Exponential backoff + jitter |
| **Connection timeout** | Yes | Exponential backoff |
| **Connection refused** | No (service down) | Circuit breaker instead |
| **DNS resolution** | Yes (once) | Short delay |

### Implementation with Jitter

```python
import random
import time

def retry_with_backoff(func, max_retries=3, base_delay=1.0, max_delay=30.0):
    for attempt in range(max_retries + 1):
        try:
            return func()
        except RetryableError as e:
            if attempt == max_retries:
                raise
            delay = min(base_delay * (2 ** attempt), max_delay)
            jitter = delay * random.uniform(0.5, 1.5)
            time.sleep(jitter)
```

---

## Bulkhead Pattern

### Isolation Strategies

| Type | Mechanism | Granularity |
|------|-----------|-------------|
| **Thread pool** | Separate thread pool per dependency | Per-dependency |
| **Semaphore** | Connection limit per dependency | Per-dependency |
| **Process** | Separate process per service | Per-service |
| **Pod** | Separate K8s deployment | Per-workload |

### Bulkhead Sizing

```
Pool size = (target_rps × p99_latency_seconds) × safety_margin

Example:
  Target: 100 RPS to payment service
  p99 latency: 500ms = 0.5s
  Safety margin: 2×

  Pool size = 100 × 0.5 × 2 = 100 threads/connections
```

---

## Testing Resilience Patterns

### Verification Checklist

```markdown
## Circuit Breaker Tests
- [ ] Opens after failure threshold exceeded
- [ ] Rejects calls while OPEN (returns fallback)
- [ ] Transitions to HALF-OPEN after timeout
- [ ] Closes after success threshold in HALF-OPEN
- [ ] Returns to OPEN on failure in HALF-OPEN
- [ ] Metrics exposed (state, failure count, rejected count)

## Retry Tests
- [ ] Retries on retryable errors
- [ ] Does NOT retry on non-retryable errors
- [ ] Respects max retry count
- [ ] Applies backoff between retries
- [ ] Adds jitter to prevent thundering herd
- [ ] Total timeout bounds all retries

## Bulkhead Tests
- [ ] Limits concurrent calls per dependency
- [ ] Rejects excess calls (not queued indefinitely)
- [ ] Failure in one bulkhead doesn't affect others
- [ ] Metrics exposed (active, queued, rejected)

## Combined Pattern Tests
- [ ] Retry → Circuit Breaker → Fallback chain works
- [ ] Retries count toward circuit breaker threshold
- [ ] Fallback activates when circuit is OPEN
```
