# Streaming Architecture — Kafka Design

Purpose: topic, consumer, schema, and delivery guidance for event-driven and Kafka-based pipelines.

## Contents

1. Topic design
2. Consumer-group rules
3. Event schema
4. Delivery guarantees
5. Outbox and processing patterns

## Topic Design

```yaml
topic_naming_convention:
  pattern: "{domain}.{entity}.{event}"
  examples:
    - "orders.order.created"
    - "users.profile.updated"
    - "payments.transaction.completed"
```

### Topic Configuration Rules

| Setting | Rule |
|---------|------|
| Partitions | `10x` expected peak throughput in MB/s |
| Minimum partitions | `3` |
| Practical maximum | `100` per topic |
| Production retention | `7d` by default, extend for replay needs |
| Compacted retention | effectively infinite for state topics |
| Replication factor | prod `3`, staging `2`, dev `1` |

Anti-pattern guards:
- do not create a god topic
- do not use `1` partition for scalable workloads
- do not jump to `1000` partitions without a hard need

## Consumer Group Rules

```yaml
consumer_groups:
  naming: "{service}-{purpose}"
  examples:
    - "analytics-aggregator"
    - "notification-sender"
    - "audit-logger"
```

Rules:
- `consumers <= partitions`
- scale off consumer lag, not guesswork
- separate groups by purpose, not convenience

## Event Schema

Required metadata:
- `event_id`
- `event_type`
- `timestamp`
- `version`
- `source`
- `correlation_id`
- `data`

Compatibility rules:
- allow additive fields
- do not remove fields or change types without versioning
- use Schema Registry for shared or critical streams

Recommended event size: `1KB-10KB`. If payloads grow beyond that, prefer reference patterns.

## Delivery Guarantees

| Level | Use When | Notes |
|-------|----------|-------|
| At-most-once | loss is acceptable | avoid for business-critical data |
| At-least-once | default | combine with idempotent consumers |
| Exactly-once | narrow Kafka-to-Kafka cases | external systems still need idempotent sinks |

Prefer "effectively once": `acks=all` + manual commit after processing + idempotent sink or deduplication.

## Outbox And Processing Patterns

Use Outbox when DB writes and event publication must remain atomic:
1. write business data and outbox record in one DB transaction
2. capture outbox changes with CDC
3. publish to Kafka from the CDC pipeline

Common processing shapes:
- stateless transform
- windowed aggregation
- stream-table join

Operational guards:
- use manual commit after successful processing
- send poison pills to a DLT/DLQ
- track consumer lag, throughput, error rate, rebalance frequency, disk usage, and under-replicated partitions

## 2026 Platform Baseline

- **KRaft mode (Zookeeper-free)** is the default for new clusters; ZooKeeper migration paths have been generally available since Kafka `3.9`. Dynamic KRaft quorums (Kafka `3.9+`) make controller-quorum changes operational rather than disruptive. Treat any new cluster on ZooKeeper in 2026 as a migration target.
- **Tiered Storage** is production-ready (Kafka `3.9+`): hot, recent log segments stay on broker-local disk; closed segments offload to S3 / GCS / Azure Blob / HDFS via the broker's `RemoteStorageManager`. Operational implication: extend retention to weeks / months on cold storage without paying for matching broker disk, and treat broker disk as a working-set cache, not a long-term store.
- **Iceberg Topics / Kafka-Iceberg integration**: the 2026 trend is to surface a Kafka topic as an **Apache Iceberg** table on object storage with zero-ETL and zero-copy semantics (Aiven Iceberg Topics, AutoMQ, WarpStream Iceberg-native flows). Caveat: only **closed segments** are exposed to Iceberg consumers, so this is **not** sub-second real-time — for that, keep a Flink / Kafka Streams consumer next to the broker. Use Iceberg-topic exposure when downstream is Spark / Trino / Flink batch and you want to skip a copy job.
- **Flink as the real-time processor** is the 2026 default when the workload is more than stateless transforms. Kafka Streams remains appropriate for JVM-only, tightly-coupled topologies; Flink wins for cross-language and stateful workflows with strong watermark semantics.

### When To Reach For Each Storage Tier

| Need | 2026 default |
|------|---------------|
| Replay last `7 d` for incident recovery | Broker-local retention; standard Kafka |
| Replay last `90 d+` for backfills | Tiered Storage with closed-segment offload to S3 / GCS / Azure Blob |
| Run Spark / Trino / Flink batch on the same data without re-publishing | Iceberg Topics on object storage |
| Sub-second stream-stream join over hours of state | Flink with RocksDB state backend (or Kafka Streams equivalent) — not Iceberg |
