# SLO/SLI Design Reference

SLO/SLI定義テンプレート、エラーバジェット計算、バーンレートのリファレンス。

---

## SLI (Service Level Indicator) Types

| SLI Type | Formula | Use Case |
|----------|---------|----------|
| **Availability** | Successful requests / Total requests | API uptime |
| **Latency** | Requests < threshold / Total requests | Response time |
| **Throughput** | Processed events / Expected events | Data pipeline |
| **Correctness** | Correct responses / Total responses | Data accuracy |
| **Freshness** | Data updated within window / Total data | Cache/replication |

### SLI Specification Template

```yaml
sli:
  name: "api-availability"
  description: "Proportion of successful HTTP requests"
  type: availability
  good_events: "http_status < 500"
  total_events: "all HTTP requests"
  measurement:
    source: prometheus
    query: |
      sum(rate(http_requests_total{status!~"5.."}[5m]))
      /
      sum(rate(http_requests_total[5m]))
  exclusions:
    - "health check endpoints"
    - "internal monitoring traffic"
```

---

## SLO (Service Level Objective) Templates

### Tiered SLO Framework

| Tier | Availability | Latency (p99) | Error Budget/month |
|------|-------------|---------------|-------------------|
| **Critical** (auth, payments) | 99.95% | 200ms | 21.6 min |
| **Core** (main features) | 99.9% | 500ms | 43.2 min |
| **Standard** (dashboards) | 99.5% | 1000ms | 3.6 hrs |
| **Best-effort** (batch jobs) | 99.0% | 5000ms | 7.2 hrs |

### SLO Document Template

```yaml
slo:
  service: "payment-api"
  tier: critical
  owner: "payments-team"
  objectives:
    - sli: availability
      target: 99.95
      window: 30d
      rolling: true
    - sli: latency
      target: 99.0
      threshold: 200ms
      percentile: p99
      window: 30d
  consequences:
    budget_exhausted:
      - "Freeze non-critical deployments"
      - "Redirect engineering to reliability"
    budget_below_25:
      - "Alert on-call lead"
      - "Increase deployment scrutiny"
```

---

## Error Budget Calculation

### Formulas

```
Error Budget = 1 - SLO Target

Example (99.9% SLO over 30 days):
  Budget = 1 - 0.999 = 0.001 = 0.1%
  Time budget = 30 days × 24h × 60m × 0.001 = 43.2 minutes
  Request budget = 1,000,000 requests × 0.001 = 1,000 failed requests allowed

Remaining budget:
  consumed = actual_bad_events / total_events
  remaining = error_budget - consumed
  remaining_pct = remaining / error_budget × 100
```

### Error Budget Policy

| Budget Remaining | Actions |
|-----------------|---------|
| > 50% | Normal development velocity |
| 25-50% | Increased review for risky changes |
| 10-25% | Only reliability improvements and critical fixes |
| < 10% | Freeze deployments, focus on reliability |
| 0% (exhausted) | Full freeze until budget regenerates |

---

## Burn Rate Alerts

### Multi-Window Burn Rate

| Alert | Burn Rate | Long Window | Short Window | Budget Consumed |
|-------|-----------|-------------|--------------|-----------------|
| **Page (critical)** | 14.4× | 1h | 5min | 2% in 1h |
| **Page (urgent)** | 6× | 6h | 30min | 5% in 6h |
| **Ticket (warning)** | 3× | 1d | 2h | 10% in 1d |
| **Ticket (low)** | 1× | 3d | 6h | 10% in 3d |

### Burn Rate Alert Implementation

```yaml
# Prometheus alerting rules
groups:
  - name: slo-burn-rate
    rules:
      - alert: HighBurnRate_Critical
        expr: |
          (
            sum(rate(http_errors_total[1h])) / sum(rate(http_requests_total[1h]))
          ) > (14.4 * 0.001)
          AND
          (
            sum(rate(http_errors_total[5m])) / sum(rate(http_requests_total[5m]))
          ) > (14.4 * 0.001)
        labels:
          severity: critical
        annotations:
          summary: "High burn rate: 2% budget consumed in 1 hour"

      - alert: HighBurnRate_Warning
        expr: |
          (
            sum(rate(http_errors_total[6h])) / sum(rate(http_requests_total[6h]))
          ) > (6 * 0.001)
          AND
          (
            sum(rate(http_errors_total[30m])) / sum(rate(http_requests_total[30m]))
          ) > (6 * 0.001)
        labels:
          severity: warning
```

---

## SLO Review Cadence

| Activity | Frequency | Participants |
|----------|-----------|-------------|
| **Error budget check** | Daily (automated) | On-call |
| **SLO dashboard review** | Weekly | Team lead |
| **SLO target review** | Quarterly | Engineering + Product |
| **SLO creation/retirement** | As needed | Architecture review |

### Quarterly Review Checklist

```markdown
- [ ] Are SLOs still aligned with user expectations?
- [ ] Were error budgets exhausted? Why?
- [ ] Are SLIs still measuring the right things?
- [ ] Should targets be tightened or relaxed?
- [ ] Are any SLOs consistently over-met (wasting budget)?
- [ ] New services that need SLOs?
- [ ] Retired services whose SLOs should be removed?
```
