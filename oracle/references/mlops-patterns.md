# MLOps Patterns Reference

デプロイ戦略、モデルモニタリング、Feature Store のリファレンス。

---

## Deployment Strategies

| Strategy | Description | Risk | Rollback Speed |
|----------|-------------|------|----------------|
| **Shadow mode** | New model runs alongside, no user impact | Lowest | Instant (not serving) |
| **Canary** | Route X% traffic to new model | Low | Seconds |
| **Blue/Green** | Full swap between two environments | Medium | Seconds |
| **A/B test** | Split traffic for comparison | Low | Minutes |
| **Gradual rollout** | Increase traffic percentage over time | Low | Minutes |

### Deployment Checklist

```markdown
## Pre-Deploy
- [ ] Evaluation metrics meet or exceed baseline
- [ ] No regressions in regression test suite
- [ ] Safety guardrails tested
- [ ] Latency within SLO (p95 < Xms)
- [ ] Cost per query within budget
- [ ] Rollback plan documented

## Deploy
- [ ] Shadow mode validation (24h minimum)
- [ ] Canary at 5% for 1h
- [ ] Monitor error rate, latency, quality metrics
- [ ] Expand to 25% → 50% → 100%

## Post-Deploy
- [ ] Quality metrics stable for 24h
- [ ] No increase in user complaints
- [ ] Cost tracking aligned with projections
- [ ] Remove shadow/canary infrastructure
```

---

## Model Monitoring

### Key Metrics to Monitor

| Category | Metric | Alert Threshold |
|----------|--------|----------------|
| **Latency** | p50, p95, p99 response time | p95 > 2x baseline |
| **Error rate** | Failed requests / total | > 1% |
| **Token usage** | Input/output tokens per request | > 2x baseline |
| **Cost** | Cost per query, daily spend | > 120% budget |
| **Quality** | LLM-as-judge score (sampled) | < 90% of baseline |
| **Safety** | Guardrail trigger rate | > 5% |
| **Drift** | Input distribution change | Significant shift |

### Quality Monitoring Pipeline

```python
class QualityMonitor:
    def __init__(self, sample_rate: float = 0.05):
        self.sample_rate = sample_rate

    def should_sample(self) -> bool:
        return random.random() < self.sample_rate

    async def evaluate_sample(self, query: str, response: str):
        if not self.should_sample():
            return

        score = await llm_judge.evaluate(query, response)
        metrics.record("quality_score", score)

        if score < QUALITY_THRESHOLD:
            alert.send(f"Quality degradation: {score}")
```

---

## Feature Store Patterns

### Feature Store Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  Data Source │────→│  Feature     │────→│  Online Store │
│  (DB/Stream) │     │  Pipeline    │     │  (Redis/DDB)  │
└─────────────┘     └──────┬───────┘     └──────────────┘
                           │                     ↑
                           ↓                     │
                    ┌──────────────┐       ┌─────────────┐
                    │  Offline     │       │  LLM App    │
                    │  Store (S3)  │       │  (Serving)  │
                    └──────────────┘       └─────────────┘
```

### Feature Types for LLM Apps

| Feature | Source | Freshness | Use |
|---------|--------|-----------|-----|
| **User profile** | Database | Real-time | Personalization context |
| **Interaction history** | Event stream | Near real-time | Conversation context |
| **Content embeddings** | Batch pipeline | Daily | RAG retrieval |
| **User preferences** | Database | Real-time | Response customization |
| **Usage statistics** | Analytics | Hourly | Rate limiting, cost control |

---

## Model Registry

### Registry Schema

```json
{
  "model_id": "intent-classifier-v2.1",
  "provider": "anthropic",
  "model_name": "claude-haiku-4-5-20251001",
  "prompt_version": "v2.1.0",
  "status": "production",
  "metrics": {
    "accuracy": 0.94,
    "p95_latency_ms": 450,
    "cost_per_1k_queries": 0.12
  },
  "deployed_at": "2026-01-15T10:00:00Z",
  "rollback_to": "intent-classifier-v2.0"
}
```

---

## Experiment Tracking

### Experiment Log Template

```markdown
## Experiment: [Name]

### Hypothesis
[What we expect to happen]

### Variables
- Independent: [What we changed - model, prompt, temperature]
- Dependent: [What we measure - accuracy, latency, cost]
- Control: [What stays the same]

### Results
| Variant | Accuracy | Latency p95 | Cost/1k | Quality Score |
|---------|----------|-------------|---------|---------------|
| Control | X.XX | Xms | $X.XX | X.XX |
| Test | X.XX | Xms | $X.XX | X.XX |

### Decision
[Accept/Reject] — [Reasoning]
```
