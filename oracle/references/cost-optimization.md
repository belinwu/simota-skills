# Cost Optimization Reference

トークン経済、モデル選定マトリクス、プロンプト圧縮、キャッシュROI のリファレンス。

---

## Token Economics

### Token Pricing Comparison (per 1M tokens)

| Model | Input | Output | Speed | Quality |
|-------|-------|--------|-------|---------|
| **Claude Opus 4.6** | $15.00 | $75.00 | Slow | Highest |
| **Claude Sonnet 4.5** | $3.00 | $15.00 | Medium | High |
| **Claude Haiku 4.5** | $0.80 | $4.00 | Fast | Good |
| **GPT-4o** | $2.50 | $10.00 | Medium | High |
| **GPT-4o-mini** | $0.15 | $0.60 | Fast | Good |

### Cost Estimation Formula

```
Cost = (input_tokens × input_price + output_tokens × output_price) × requests_per_day × 30

Example: 1000 requests/day, avg 500 input + 200 output tokens, Claude Sonnet
= (500 × $3/1M + 200 × $15/1M) × 1000 × 30
= ($0.0015 + $0.003) × 30000
= $135/month
```

---

## Model Selection Matrix

### Decision Framework

```
Task complexity:
  Simple (classification, extraction) → Haiku
  Medium (summarization, Q&A) → Sonnet or GPT-4o-mini
  Complex (reasoning, code, analysis) → Sonnet
  Hardest (research, multi-step reasoning) → Opus

Latency requirement:
  < 500ms → Haiku or GPT-4o-mini
  < 2s → Sonnet
  < 10s → Opus

Budget per query:
  < $0.001 → Haiku or GPT-4o-mini
  < $0.01 → Sonnet
  < $0.10 → Opus
```

### Model Routing

```python
def select_model(task: Task) -> str:
    if task.complexity == "simple" and task.latency_budget < 500:
        return "claude-haiku-4-5-20251001"
    elif task.requires_reasoning or task.complexity == "complex":
        return "claude-sonnet-4-5-20250929"
    elif task.complexity == "hardest":
        return "claude-opus-4-6"
    else:
        return "claude-sonnet-4-5-20250929"  # Default
```

---

## Prompt Compression Techniques

| Technique | Token Reduction | Quality Impact |
|-----------|----------------|---------------|
| **Remove whitespace/formatting** | 5-10% | None |
| **Abbreviate instructions** | 10-20% | Low risk |
| **Reduce few-shot examples** | 20-50% | Medium risk |
| **Use structured references** | 10-15% | Low risk |
| **LLMLingua compression** | 30-60% | Medium risk |
| **Summary of long context** | 40-70% | Variable |

### Before/After Example

```
# Before (150 tokens)
You are a helpful customer support agent. Your job is to help customers
with their questions about our product. You should always be polite and
professional. If you don't know the answer, say "I don't know" rather
than making something up. Always provide sources for your claims.

# After (80 tokens)
Role: Customer support agent.
Rules: Be polite. Cite sources. Say "I don't know" if uncertain.
Never fabricate information.
```

---

## Caching ROI Calculator

### Cache Hit Rate Impact

| Cache Hit Rate | Cost Reduction | LLM Calls Saved |
|---------------|---------------|-----------------|
| 10% | 10% | 1 in 10 |
| 30% | 30% | 3 in 10 |
| 50% | 50% | 5 in 10 |
| 70% | 70% | 7 in 10 |

### Caching Strategy by Use Case

| Use Case | Expected Hit Rate | Cache Strategy |
|----------|------------------|----------------|
| FAQ bot | 50-80% | Exact + Semantic cache |
| Code review | 5-15% | Prompt caching only |
| Data extraction | 20-40% | Exact cache by document |
| Chat support | 10-30% | Semantic cache |
| Classification | 40-70% | Exact cache |

### ROI Calculation

```
Monthly LLM cost without cache: $1000
Cache infrastructure cost: $50/month
Cache hit rate: 50%

Savings = $1000 × 0.50 - $50 = $450/month
ROI = $450 / $50 = 900%
Break-even hit rate = $50 / $1000 = 5%
```

---

## Cost Monitoring Dashboard

### Key Metrics

| Metric | Granularity | Alert Threshold |
|--------|------------|----------------|
| **Daily spend** | Per model | > 120% of budget |
| **Cost per query** | Per endpoint | > 2x baseline |
| **Token efficiency** | Per prompt version | Output/Input ratio spike |
| **Cache hit rate** | Per cache | < 50% of expected |
| **Error cost** | Wasted tokens on errors | > 5% of total |

### Cost Reduction Checklist

- [ ] Use cheapest model that meets quality requirements
- [ ] Implement caching for repeated/similar queries
- [ ] Compress prompts without quality loss
- [ ] Reduce max_tokens to actual need (not default)
- [ ] Monitor and eliminate token waste (retries, errors)
- [ ] Use prompt caching for repeated system prompts
- [ ] Batch similar requests where latency allows
- [ ] Set spending alerts and hard limits
