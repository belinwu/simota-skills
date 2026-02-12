# Data Reliability — Quality, CDC, Idempotency, Backfill

## Data Quality Checks

### Quality Check Layers

```
┌─────────────────────────────────────────────────────┐
│                   Source Layer                       │
│  - Freshness (data arrived on time?)                │
│  - Volume (expected row count?)                     │
│  - Schema (columns match?)                          │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│                 Transform Layer                      │
│  - Uniqueness (no duplicates?)                      │
│  - Completeness (null checks)                       │
│  - Validity (values in range?)                      │
│  - Consistency (cross-field rules)                  │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│                   Sink Layer                         │
│  - Reconciliation (source vs target counts)         │
│  - Business rules (domain-specific)                 │
│  - Anomaly detection (statistical)                  │
└─────────────────────────────────────────────────────┘
```

### Great Expectations Suite

```python
# great_expectations/expectations/orders_suite.json
{
    "expectation_suite_name": "orders_validation",
    "expectations": [
        {
            "expectation_type": "expect_table_row_count_to_be_between",
            "kwargs": {
                "min_value": 1000,
                "max_value": 1000000
            }
        },
        {
            "expectation_type": "expect_column_values_to_not_be_null",
            "kwargs": {
                "column": "order_id"
            }
        },
        {
            "expectation_type": "expect_column_values_to_be_unique",
            "kwargs": {
                "column": "order_id"
            }
        },
        {
            "expectation_type": "expect_column_values_to_be_between",
            "kwargs": {
                "column": "total_amount",
                "min_value": 0,
                "max_value": 10000000
            }
        },
        {
            "expectation_type": "expect_column_values_to_match_regex",
            "kwargs": {
                "column": "email",
                "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"
            }
        }
    ]
}
```

### Quality Gate Integration

```python
# Airflow task with quality gate
def run_quality_gate(**context):
    from great_expectations.core.batch import RuntimeBatchRequest

    result = context.run_checkpoint(
        checkpoint_name="orders_checkpoint",
        batch_request=RuntimeBatchRequest(
            datasource_name="warehouse",
            data_connector_name="default",
            data_asset_name="orders",
        ),
    )

    if not result["success"]:
        raise AirflowException(
            f"Quality check failed: {result['run_results']}"
        )

    return result
```

---

## CDC (Change Data Capture)

### CDC Pattern Selection

| Pattern | Latency | Complexity | Use Case |
|---------|---------|------------|----------|
| **Timestamp-based** | Minutes-Hours | Low | Simple updates with updated_at |
| **Trigger-based** | Seconds | Medium | Legacy DBs without log access |
| **Log-based (Debezium)** | Sub-second | High | Real-time sync, no DB impact |

### Debezium Configuration

```json
{
  "name": "postgres-orders-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "${secrets.db_password}",
    "database.dbname": "orders_db",
    "database.server.name": "orders",
    "table.include.list": "public.orders,public.order_items",
    "plugin.name": "pgoutput",
    "slot.name": "debezium_orders",
    "publication.name": "orders_publication",
    "transforms": "unwrap",
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
    "transforms.unwrap.drop.tombstones": "false",
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter"
  }
}
```

### CDC Event Structure

```json
{
  "before": null,
  "after": {
    "order_id": 12345,
    "customer_id": 100,
    "total_amount": 9999,
    "status": "completed"
  },
  "source": {
    "version": "2.4.0",
    "connector": "postgresql",
    "name": "orders",
    "ts_ms": 1704067200000,
    "db": "orders_db",
    "schema": "public",
    "table": "orders",
    "txId": 54321,
    "lsn": 123456789
  },
  "op": "c",
  "ts_ms": 1704067200100
}
```

---

## Idempotency Patterns

### Idempotency Key Strategy

```python
def generate_idempotency_key(event: dict) -> str:
    """Generate deterministic key for deduplication."""
    components = [
        event['source'],
        event['entity_type'],
        event['entity_id'],
        event['event_type'],
        event['timestamp'][:19],  # Truncate to second
    ]
    return hashlib.sha256('|'.join(components).encode()).hexdigest()
```

### Deduplication Approaches

#### 1. At-Source Deduplication (Redis)

```python
def process_with_dedup(event):
    key = f"processed:{event['event_id']}"

    if redis.exists(key):
        logger.info(f"Duplicate event: {event['event_id']}")
        return None

    result = process_event(event)

    # Mark as processed with TTL
    redis.setex(key, 86400 * 7, "1")  # 7 days

    return result
```

#### 2. At-Sink Deduplication (UPSERT)

```sql
-- PostgreSQL UPSERT
INSERT INTO processed_events (event_id, data, processed_at)
VALUES (%(event_id)s, %(data)s, NOW())
ON CONFLICT (event_id)
DO UPDATE SET
    data = EXCLUDED.data,
    processed_at = NOW()
WHERE processed_events.data IS DISTINCT FROM EXCLUDED.data;
```

#### 3. Exactly-Once with Kafka Transactions

```python
producer = KafkaProducer(
    transactional_id='etl-processor-1',
    enable_idempotence=True,
)

producer.init_transactions()

try:
    producer.begin_transaction()
    producer.send('output-topic', value=result)
    producer.send_offsets_to_transaction(
        offsets, consumer_group_id
    )
    producer.commit_transaction()
except Exception:
    producer.abort_transaction()
    raise
```

---

## Backfill Strategy

### Backfill Decision Matrix

| Scenario | Strategy | Time | Risk |
|----------|----------|------|------|
| Schema change only | Reprocess all | Hours | Low |
| Bug fix (recent) | Reprocess affected window | Minutes-Hours | Low |
| Logic change | Full historical reprocess | Hours-Days | Medium |
| New source added | Incremental from start | Days | Low |

### Backfill Playbook Template

```markdown
## Backfill Plan: [Pipeline Name]

### Reason
- [Why backfill is needed]

### Scope
- Start date: YYYY-MM-DD
- End date: YYYY-MM-DD
- Estimated rows: [count]
- Estimated duration: [hours]

### Pre-Backfill Checklist
- [ ] Production pipeline paused
- [ ] Downstream consumers notified
- [ ] Backup of target tables created
- [ ] Monitoring alerts adjusted

### Execution Steps
1. Pause production DAG
2. Clear target partition range
3. Run backfill command:
   ```bash
   airflow dags backfill \
     --start-date YYYY-MM-DD \
     --end-date YYYY-MM-DD \
     --reset-dagruns \
     pipeline_name
   ```
4. Verify row counts
5. Run quality checks
6. Resume production DAG

### Rollback Plan
- Restore from backup: [command]
- Resume from checkpoint: [command]

### Post-Backfill
- [ ] Verify data quality
- [ ] Notify downstream consumers
- [ ] Document in runbook
```
