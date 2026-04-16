# Distributed Concurrency Patterns

Concurrency issue pattern catalog specific to distributed systems.

## 1. Distributed Lock Issues

### Pattern: Lock Contention Cascade
- Symptom: latency spikes, increasing timeouts
- Cause: Redis/ZooKeeper distributed lock contention cascades
- Detection: lock wait time metrics, sudden spike in lock acquisition failure rate
- Risk Score adjustment: Impact +2 (cascading), Recovery +1 (requires coordination)

### Pattern: Split-Brain Lock
- Symptom: duplicate writes to the same resource
- Cause: network partition splits the lock manager
- Detection: data inconsistencies, duplicate processing logs
- Risk Score adjustment: DataRisk +3 (data corruption)

### Pattern: Lock Expiry Race
- Symptom: intermittent data corruption
- Cause: processing time exceeds lock TTL; another process acquires the lock
- Detection: histogram comparison of lock TTL vs processing time

## 2. Eventual Consistency Conflicts

### Pattern: Read-Your-Write Violation
- Symptom: user sees stale data after an update
- Cause: read replica replication lag
- Detection: discrepancy between write timestamp and read result timestamp

### Pattern: Conflict Resolution Failure
- Symptom: data loss (prior write overwritten by last-write-wins)
- Cause: optimistic concurrency control without CRDT or vector clock
- Detection: "disappearance" pattern in version history
- Risk Score adjustment: DataRisk +3

### Pattern: Saga Compensation Failure
- Symptom: partially committed transaction
- Cause: compensation handler failure (insufficient idempotency, ordering dependency)
- Detection: Saga state machine lingering in COMPENSATING state
- Risk Score adjustment: Impact +2, Recovery +2

## 3. Microservice Race Conditions

### Pattern: Event Ordering Violation
- Symptom: processing result incorrect depending on execution order
- Cause: no ordering guarantee across partitions in message queue
- Detection: inconsistency between event timestamps and local clock

### Pattern: Thundering Herd
- Symptom: backend overload on cache expiry
- Cause: simultaneous TTL expiry floods origin with all requests
- Detection: periodic spikes in cache miss rate

### Pattern: Retry Storm
- Symptom: traffic amplification during failures
- Cause: retries without exponential backoff or jitter
- Detection: correlation between 4xx/5xx error rate and request volume

## 4. Container/Kubernetes Resource Issues

### Pattern: OOMKill Loop
- Symptom: Pod repeatedly restarting
- Cause: misconfigured memory limit or memory leak
- Detection: `kubectl get events --field-selector reason=OOMKilling`
- Investigation: time-series `kubectl top pod` + change identification via Rewind

### Pattern: CPU Throttling Latency
- Symptom: periodic P99 latency spikes
- Cause: throttling due to CPU limit
- Detection: `container_cpu_cfs_throttled_periods_total` metric

### Pattern: Ephemeral Storage Exhaustion
- Symptom: Pod eviction
- Cause: accumulation of log/tmp files
- Detection: `ephemeral-storage` usage trending

## 5. WebAssembly/Edge Computing Concurrency

### Pattern: SharedArrayBuffer Race
- Symptom: incorrect values in shared memory between Workers
- Cause: accessing SharedArrayBuffer without Atomics API
- Detection: non-deterministic variance in computation results

### Pattern: Edge Worker Connection Limit
- Symptom: intermittent timeouts
- Cause: concurrent connection limit in edge runtime (typically 6-10)
- Detection: spikes in 429 responses, connection pool exhaustion logs

## Rewind Escalation Criteria

When the following conditions apply, use `SPECTER_TO_REWIND_HANDOFF` (`_common/INVESTIGATION_ESCALATION.md`):

- Leak or race found but onset timing is unknown
- Evidence that the issue surfaced after a specific deployment
- Correlation with a configuration change (env var, feature flag) is suspected
