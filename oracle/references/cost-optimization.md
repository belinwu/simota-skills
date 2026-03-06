# Cost Optimization (2025-2026)

> Token economics, model selection, prompt caching, batching, model routing, cost monitoring

## 1. Token Economics (2025-2026 Pricing)

| Model | Input (per 1M) | Output (per 1M) | Speed | Quality |
|-------|----------------|------------------|-------|---------|
| **Claude Opus 4.6** | $15.00 | $75.00 | Slow | Highest |
| **Claude Sonnet 4.6** | $3.00 | $15.00 | Medium | High |
| **Claude Haiku 4.5** | $0.80 | $4.00 | Fast | Good |
| **GPT-4o** | $2.50 | $10.00 | Medium | High |
| **GPT-4o-mini** | $0.15 | $0.60 | Fast | Good |

### Cost Formula

```
Monthly cost = (input_tokens × input_price + output_tokens × output_price)
               × requests_per_day × 30

Example: 1000 req/day, avg 500 input + 200 output, Claude Sonnet 4.6
= (500 × $3/1M + 200 × $15/1M) × 1000 × 30 = $135/month
```

---

## 2. 5-Stage Cost Reduction Framework

### Stage 1: Prompt Optimization (−10 to 30%)

| Technique | Savings | Risk |
|-----------|---------|------|
| Remove redundant context | 10-30% | None if careful |
| Compress instructions | 10-20% | May reduce clarity |
| Reduce few-shot examples | 20-50% | Medium quality risk |
| Set max_tokens to actual need | 5-15% | None |
| Remove over-prompting from pre-4.6 era | 10-20% | None (4.6 is more responsive) |

### Stage 2: Model Routing (−30 to 60%)

```python
def select_model(task: Task) -> str:
    # Start with cheapest viable model; escalate on failure
    if task.complexity == "simple" and task.latency_budget < 500:
        return "claude-haiku-4-5-20251001"
    elif task.requires_reasoning or task.complexity == "complex":
        return "claude-sonnet-4-6"
    elif task.complexity == "hardest":
        return "claude-opus-4-6"
    else:
        return "claude-sonnet-4-6"  # Default
```

**Dynamic model selection pattern:**
Start with Haiku 4.5 → validate output → escalate to Sonnet if validation fails.
Haiku 4.5 delivers ~90% of Sonnet's agentic performance at 2× speed, 3× cost savings.

### Stage 3: Caching (−10 to 90%)

| Strategy | Expected Hit Rate | Savings | Best For |
|----------|------------------|---------|----------|
| **Prompt cache** (provider-level) | Automatic | Up to 90% input cost, 80% latency | Repeated system prompts, tool definitions |
| **Exact cache** (application-level) | 40-70% for FAQ | Direct cost reduction | Identical repeated queries |
| **Semantic cache** | 10-30% for chat | Variable | Similar queries |

**Prompt caching specifics:**
- Caches system prompts, tool definitions, shared RAG context
- Latency reduction: up to 80%
- Input token cost reduction: up to 90%
- Effectiveness depends on prompt stability; dynamic content reduces hit rate
- Cache invalidation policy design is required

### Stage 4: Batching (−20 to 40%)

- **Batch API**: Multiple prompts in a single request; lower per-call overhead
- **Continuous batching**: Groups requests dynamically on GPU backends
- **Parallel processing**: Retrieval and model warm-up concurrently
- Best for: async workflows where latency tolerance > 30s

### Stage 5: Error Cost Elimination (−5 to 10%)

- Circuit breaker to prevent infinite retry loops
- Early validation failure detection
- Avoid unnecessary re-generation
- Monitor wasted tokens on errors (target: <5% of total spend)

### Compound Effect

```
Techniques are complementary:
  Prompt compression + model routing + caching = 60-80% cost reduction
  without quality compromise.

Example: 5,000 users × 50K req/day
  No optimization: $6,000/month
  With prompt cache: $2,625/month (56% reduction)
  With full pipeline: ~$1,200/month (80% reduction)
```

---

## 3. Effort Parameter Optimization (Claude 4.6)

| Effort | Use Case | Token Impact | Latency |
|--------|----------|-------------|---------|
| `low` | Classification, simple extraction | Minimal thinking | Fast |
| `medium` | General tasks, content generation | Balanced | Medium |
| `high` | Agentic coding, complex reasoning | Deep thinking | Slower |
| `max` | Research, deep analysis | Maximum reasoning | Slowest |

**Cost tip:** Use `medium` as default for most applications. Reserve `high`/`max` for genuinely complex tasks. Setting max_tokens to 64k at medium effort gives room for thinking without runaway token usage.

---

## 4. Model Registry

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

## 5. Cost Monitoring Dashboard

| Metric | Granularity | Alert Threshold |
|--------|------------|----------------|
| **Daily spend** | Per model | > 120% of budget |
| **Cost per query** | Per endpoint | > 2× baseline |
| **Token efficiency** | Per prompt version | Output/Input ratio spike |
| **Cache hit rate** | Per cache | < 50% of expected |
| **Error cost** | Wasted tokens on errors | > 5% of total |
| **Thinking tokens** | Per effort level | Unexpected increase |

---

## 6. Cost Reduction Checklist

- [ ] Use cheapest model that meets quality requirements
- [ ] Enable prompt caching for system prompts and tool definitions
- [ ] Implement application-level caching for repeated/similar queries
- [ ] Set max_tokens to actual need (not default maximum)
- [ ] Use appropriate effort level (don't default to `high` for everything)
- [ ] Monitor and eliminate token waste (retries, errors)
- [ ] Batch similar requests where latency allows
- [ ] Set spending alerts and hard limits per model/endpoint
- [ ] Track cost per feature, not just total spend
- [ ] Review model selection quarterly as pricing and capabilities evolve

---

## 7. Oracle Integration

```
Oracle workflow integration:
  1. DESIGN: Include cost implications in every architecture decision
  2. ASSESS: Audit current model selection and caching strategy
  3. SPECIFY: Include cost constraints in Builder handoff specs
  4. EVALUATE: Measure cost per query alongside quality metrics

Quality gates:
  - No cost estimate → require budget projection before design approval
  - Using Opus for simple tasks → require model routing justification
  - No caching strategy → recommend caching ROI analysis
  - max_tokens at default → require actual output size analysis
```

**Source:** [Koombea: LLM Cost Optimization Guide](https://ai.koombea.com/blog/llm-cost-optimization) · [FutureAGI: LLM Cost Optimization 2025](https://futureagi.com/blogs/llm-cost-optimization-2025) · [PremAI: Save 90% on LLM API Costs](https://blog.premai.io/how-to-save-90-on-llm-api-costs-without-losing-performance/) · [Anthropic: Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
