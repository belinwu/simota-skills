# Streaming Architecture — Kafka Design

## Topic Design

```yaml
topic_naming_convention:
  pattern: "{domain}.{entity}.{event_type}"
  examples:
    - "orders.order.created"
    - "users.profile.updated"
    - "payments.transaction.completed"

topic_configuration:
  partitions:
    rule: "10x expected peak throughput in MB/s"
    minimum: 3
    maximum: 100  # Per topic, practical limit

  retention:
    production: "7d"  # Or based on replay requirements
    compacted: "infinite"  # For state topics

  replication_factor:
    production: 3
    staging: 2
    development: 1
```

## Consumer Group Design

```yaml
consumer_groups:
  naming: "{service}-{purpose}"
  examples:
    - "analytics-aggregator"
    - "notification-sender"
    - "audit-logger"

  scaling:
    rule: "consumers <= partitions"
    auto_scaling: "based on consumer lag"
```

## Event Schema Design

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["event_id", "event_type", "timestamp", "data"],
  "properties": {
    "event_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique event identifier for idempotency"
    },
    "event_type": {
      "type": "string",
      "enum": ["created", "updated", "deleted"]
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "version": {
      "type": "integer",
      "default": 1
    },
    "source": {
      "type": "string",
      "description": "Service that produced the event"
    },
    "correlation_id": {
      "type": "string",
      "description": "For tracing across services"
    },
    "data": {
      "type": "object",
      "description": "Event payload"
    }
  }
}
```

## Stream Processing Patterns

### Pattern 1: Stateless Transform

```python
# Simple mapping, filtering, enrichment
def process_event(event):
    return {
        **event,
        'processed_at': datetime.utcnow().isoformat(),
        'enriched_field': lookup_value(event['key']),
    }
```

### Pattern 2: Windowed Aggregation

```python
# Flink / Spark Structured Streaming
from pyspark.sql.functions import window, sum, count

orders_stream \
    .withWatermark("event_time", "10 minutes") \
    .groupBy(
        window("event_time", "1 hour", "15 minutes"),
        "store_id"
    ) \
    .agg(
        sum("amount").alias("total_revenue"),
        count("*").alias("order_count")
    )
```

### Pattern 3: Stream-Table Join

```python
# Enrich stream with dimension table
enriched = orders_stream.join(
    customers_table,
    orders_stream.customer_id == customers_table.id,
    "left"
)
```
