# Distributed Tracing Reference

OpenTelemetry計装設計、スパン命名規則、サンプリング戦略のリファレンス。

---

## OpenTelemetry Instrumentation

### Auto vs Manual Instrumentation

| Approach | Coverage | Effort | Customization |
|----------|----------|--------|---------------|
| **Auto-instrumentation** | HTTP, DB, messaging | Minimal | Limited |
| **Manual spans** | Business logic | Medium | Full |
| **Hybrid** (recommended) | Both layers | Medium | Full |

### SDK Setup Pattern

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

resource = Resource.create({
    "service.name": "payment-service",
    "service.version": "1.2.0",
    "deployment.environment": "production",
})

provider = TracerProvider(resource=resource)
provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="otel-collector:4317"))
)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("payment-service")
```

### Manual Span Creation

```python
@tracer.start_as_current_span("process_payment")
def process_payment(order_id: str, amount: float):
    span = trace.get_current_span()
    span.set_attribute("order.id", order_id)
    span.set_attribute("payment.amount", amount)
    span.set_attribute("payment.currency", "USD")

    try:
        result = charge_card(amount)
        span.set_attribute("payment.status", "success")
        span.set_status(StatusCode.OK)
        return result
    except PaymentError as e:
        span.set_status(StatusCode.ERROR, str(e))
        span.record_exception(e)
        raise
```

---

## Span Naming Conventions

| Layer | Format | Examples |
|-------|--------|---------|
| **HTTP server** | `HTTP {METHOD} {route}` | `HTTP GET /api/users/:id` |
| **HTTP client** | `HTTP {METHOD}` | `HTTP POST` |
| **Database** | `{db.system} {operation} {table}` | `postgresql SELECT orders` |
| **Message publish** | `{queue} publish` | `orders.created publish` |
| **Message consume** | `{queue} process` | `orders.created process` |
| **Business logic** | `{verb}_{noun}` | `validate_payment`, `calculate_tax` |
| **External service** | `{service}.{operation}` | `stripe.create_charge` |

### Attribute Standards

| Category | Attribute | Example |
|----------|-----------|---------|
| **User** | `user.id`, `user.role` | `"u-123"`, `"admin"` |
| **Business** | `order.id`, `payment.amount` | `"ord-456"`, `99.99` |
| **Error** | `error.type`, `error.message` | `"PaymentDeclined"` |
| **Feature** | `feature.flag`, `experiment.variant` | `"new-checkout"`, `"B"` |

---

## Sampling Strategies

| Strategy | Description | Use When |
|----------|-------------|----------|
| **Always on** | Sample 100% | Low traffic, debugging |
| **Probabilistic** | Sample X% uniformly | Medium traffic |
| **Rate limiting** | Max N traces/sec | High traffic |
| **Tail-based** | Decide after span completes | Need error/slow traces |
| **Parent-based** | Follow parent's decision | Cross-service consistency |

### Tail-Based Sampling Rules

```yaml
# OpenTelemetry Collector config
processors:
  tail_sampling:
    decision_wait: 10s
    policies:
      - name: errors
        type: status_code
        status_code: { status_codes: [ERROR] }
      - name: slow-requests
        type: latency
        latency: { threshold_ms: 2000 }
      - name: critical-endpoints
        type: string_attribute
        string_attribute:
          key: http.route
          values: ["/api/payments", "/api/auth"]
      - name: baseline
        type: probabilistic
        probabilistic: { sampling_percentage: 5 }
    decision_cache_size: 50000
```

---

## Context Propagation

### Propagation Formats

| Format | Header | Ecosystem |
|--------|--------|-----------|
| **W3C Trace Context** | `traceparent`, `tracestate` | Standard (recommended) |
| **B3** | `X-B3-TraceId`, `X-B3-SpanId` | Zipkin |
| **Jaeger** | `uber-trace-id` | Jaeger |

### Cross-Service Propagation Checklist

```markdown
- [ ] All HTTP clients inject trace context headers
- [ ] All HTTP servers extract trace context headers
- [ ] Message queues propagate trace context in headers/metadata
- [ ] Async workers link to parent span via context
- [ ] Batch jobs create new root spans with links to triggers
- [ ] Third-party API calls create client spans
```

---

## Trace Analysis Patterns

| Pattern | What to Look For | Action |
|---------|-----------------|--------|
| **Long spans** | Single span > SLO threshold | Optimize or decompose |
| **Wide traces** | Fan-out > 50 spans | Check N+1 queries |
| **Deep traces** | Depth > 10 levels | Simplify call chain |
| **Orphan spans** | Missing parent spans | Fix context propagation |
| **Gap spans** | Time gaps between child spans | Check queuing/scheduling |
