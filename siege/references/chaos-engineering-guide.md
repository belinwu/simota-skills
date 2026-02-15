# Chaos Engineering Guide

定常状態仮説、障害注入シナリオ、ゲームデイ計画のリファレンス。

---

## Chaos Engineering Principles

| Principle | Description |
|-----------|-------------|
| **Build a hypothesis around steady state** | Define normal behavior first |
| **Vary real-world events** | Inject realistic failures |
| **Run experiments in production** | Staging != production |
| **Automate experiments** | Continuous chaos, not one-off |
| **Minimize blast radius** | Start small, expand gradually |

---

## Steady-State Hypothesis

### Defining Steady State

```markdown
## Steady-State Hypothesis Template

### System Under Test
[Service/component being tested]

### Normal Behavior (Steady State)
- Error rate: < [X]%
- Latency p99: < [X]ms
- Throughput: > [X] requests/sec
- Success rate: > [X]%

### Experiment
**Action**: [What failure to inject]
**Expected**: [System should maintain steady state OR degrade gracefully]
**Not Expected**: [What should NOT happen — cascading failures, data loss]

### Abort Conditions
- Error rate exceeds [X]%
- Latency exceeds [X]ms
- Any data corruption detected
- Manual kill switch triggered
```

### Metrics to Monitor During Chaos

| Layer | Metrics |
|-------|---------|
| **User-facing** | Error rate, latency, success rate |
| **Application** | Exception rate, queue depth, thread count |
| **Infrastructure** | CPU, memory, disk, network |
| **Dependencies** | Response time, error rate per dependency |

---

## Failure Injection Scenarios

### Infrastructure Failures

| Scenario | Tool | Command/Config |
|----------|------|---------------|
| **Kill pod** | kubectl | `kubectl delete pod <name> -n <ns>` |
| **CPU stress** | stress-ng | `stress-ng --cpu 4 --timeout 60s` |
| **Memory pressure** | stress-ng | `stress-ng --vm 2 --vm-bytes 80% --timeout 60s` |
| **Network latency** | tc | `tc qdisc add dev eth0 root netem delay 200ms 50ms` |
| **Packet loss** | tc | `tc qdisc add dev eth0 root netem loss 10%` |
| **DNS failure** | iptables | `iptables -A OUTPUT -p udp --dport 53 -j DROP` |
| **Disk full** | fallocate | `fallocate -l 10G /tmp/fill-disk` |

### Application Failures

| Scenario | Description | Tests |
|----------|-------------|-------|
| **Dependency timeout** | Slow downstream service | Timeout handling, circuit breaker |
| **Dependency error** | 500 from downstream | Error handling, fallback |
| **Connection pool exhaustion** | Max DB connections | Pool sizing, queuing |
| **Thread pool saturation** | All workers busy | Backpressure, rejection |
| **Cache failure** | Redis unavailable | Cache-aside, degraded mode |
| **Message queue lag** | Consumer can't keep up | Backpressure, dead letter |

---

## Chaos Tools

| Tool | Scope | Complexity | Production Ready |
|------|-------|-----------|-----------------|
| **Chaos Monkey** | Kill instances | Low | Yes |
| **Litmus Chaos** | Kubernetes | Medium | Yes |
| **Gremlin** | Full platform | Low (SaaS) | Yes |
| **Chaos Mesh** | Kubernetes | Medium | Yes |
| **Toxiproxy** | Network (dev/test) | Low | No (test only) |
| **tc/netem** | Network (Linux) | Medium | Yes (careful) |

### Litmus Chaos Example

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: pod-kill-experiment
spec:
  appinfo:
    appns: production
    applabel: app=payment-service
  chaosServiceAccount: litmus-admin
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: '30'
            - name: CHAOS_INTERVAL
              value: '10'
            - name: FORCE
              value: 'false'
```

### Toxiproxy for Development

```python
# Add latency to Redis dependency
toxiproxy.create_proxy("redis", "localhost:26379", "redis:6379")
toxiproxy.proxy("redis").add_toxic("latency", {
    "type": "latency",
    "attributes": {"latency": 1000, "jitter": 500}
})

# Simulate connection reset
toxiproxy.proxy("redis").add_toxic("reset", {
    "type": "reset_peer",
    "attributes": {"timeout": 0}
})
```

---

## Game Day Checklist

```markdown
## Pre-Game (1 week before)
- [ ] Hypothesis documented and reviewed
- [ ] Monitoring dashboards prepared
- [ ] Abort criteria defined
- [ ] Blast radius limited (canary segment)
- [ ] All participants briefed
- [ ] Communication plan ready (stakeholders notified)
- [ ] Rollback/kill switch tested

## During Game
- [ ] Baseline metrics captured (15 min steady state)
- [ ] Injection started at [time]
- [ ] Monitoring active by all participants
- [ ] Timeline being documented
- [ ] Abort criteria continuously checked

## Post-Game
- [ ] Injection stopped, system recovered
- [ ] Results documented against hypothesis
- [ ] Gaps identified (detection, response, recovery)
- [ ] Action items created with owners
- [ ] Findings shared with broader team
```

---

## Maturity Model

| Level | Practice | Example |
|-------|----------|---------|
| **1 — Ad hoc** | Manual experiments in staging | Kill a pod, see what happens |
| **2 — Planned** | Scheduled game days | Monthly chaos game day |
| **3 — Automated** | Chaos in CI/CD pipeline | Automated resilience tests |
| **4 — Continuous** | Production chaos (controlled) | Continuous random pod kills |
| **5 — Advanced** | Multi-failure, cascading scenarios | Zone failure + traffic spike |
