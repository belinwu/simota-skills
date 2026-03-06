# Evaluation & Observability (2025-2026)

> LLM-as-Judge, metrics, regression testing, CI/CD integration, production observability, monitoring dashboards

## 1. Two-Layer Safety Net Model

```
Layer 1: Automated Metrics (first line of defense)
  ├── Text similarity: BLEU, ROUGE-L, BERTScore
  ├── Correctness: Exact Match, F1 Score
  ├── Quality scoring: LLM-as-Judge, GPTScore
  └── RAG-specific: Faithfulness, Relevancy, Context Precision

Layer 2: Human Review (second line of defense)
  ├── Likert scale evaluation (1-5)
  ├── Domain expert judgment
  ├── Edge case / nuance detection
  └── Bias / fairness audits

Core: Automated metrics flag obvious issues;
      human review catches nuance.
      → Combined performance exceeds either alone.
```

---

## 2. LLM-as-Judge Anti-Patterns

| # | Anti-Pattern | Problem | Mitigation |
|---|-------------|---------|-----------|
| **EV-01** | Self-evaluation | LLM judges its own output → reinforces errors | Use a different model as judge, or pair with human eval |
| **EV-02** | Position Bias | Prefers answer presented first in A/B comparison | Randomize order · run multiple times · average results |
| **EV-03** | Verbosity Bias | Rates longer answers as higher quality | Include conciseness in rubric · normalize by length |
| **EV-04** | No Rubric | Vague score definitions → inter-judge disagreement | Define anchored rubric with concrete examples per score |
| **EV-05** | Single Judge | One model's bias reflected directly | Multi-Judge (3+) with majority vote or average |
| **EV-06** | No Ground Truth | Absolute evaluation without reference → criteria drift | Always provide ground truth for reference grounding |
| **EV-07** | Regenerated test sets | New test data each run → noise, results incomparable | Fix a stable test set; only measure changes |
| **EV-08** | Monolithic evaluation | Retrieval + Generation evaluated as one → can't locate bottleneck | Component-level evaluation (Retrieval / Generation / Task) |

### Judge Prompt Template

```markdown
## Task
Evaluate the AI response on these criteria:
1. **Accuracy** (1-5): Are the facts correct?
2. **Relevance** (1-5): Does it answer the question?
3. **Completeness** (1-5): Are all aspects addressed?
4. **Clarity** (1-5): Is it well-organized and clear?

## Rubric Anchors
- 5: Excellent — fully correct, comprehensive, perfectly structured
- 3: Adequate — mostly correct, addresses main points, readable
- 1: Poor — factually wrong, misses the question, confusing

## Question
{question}

## Reference Answer (Ground Truth)
{reference}

## AI Response to Evaluate
{response}

## Output Format (JSON)
{ "accuracy": {"score": N, "reasoning": "..."}, ... "overall": N }
```

---

## 3. Task-Specific Metrics

| Task Type | Primary Metrics | Secondary Metrics |
|-----------|----------------|-------------------|
| **Classification** | Accuracy, F1, Precision, Recall | Confusion matrix |
| **Extraction** | Exact match, Partial match, F1 | Field-level accuracy |
| **Summarization** | ROUGE-L, BERTScore, Faithfulness | Length ratio |
| **Generation** | Human preference, LLM-judge score | Diversity, Fluency |
| **RAG** | Faithfulness, Relevancy, Recall@K | Context precision |
| **Code generation** | Pass@K, Execution success | Test pass rate |
| **Agentic** | Task completion rate, Step efficiency | Tool call accuracy, Cost |

---

## 4. CI/CD Integration

```
Development phase:
  1. Prompt change → eval suite auto-runs
  2. Regression detection (≥5% drop → block merge)
  3. Add new test cases from failure traces

Deployment phase:
  4. Shadow mode validation (24h minimum)
  5. Canary (5%) → 25% → 50% → 100%
  6. Quality metrics check at each stage

Production phase:
  7. Sampling evaluation (5% of requests)
  8. Drift detection alerts
  9. Periodic human evaluation (weekly/monthly)
  10. Feedback → next eval dataset

Anti-pattern: Treating evaluation as final pre-release check only
  → Cannot handle drift, model updates, or data changes
```

### Regression Detection

```python
def detect_regressions(current: dict, baseline: dict, threshold: float = 0.05) -> list:
    regressions = []
    for metric, value in current.items():
        if metric in baseline:
            delta = value - baseline[metric]
            if delta < -threshold:
                regressions.append({
                    "metric": metric, "baseline": baseline[metric],
                    "current": value, "delta": delta
                })
    return regressions
```

---

## 5. Observability — 7 Pillars

| # | Pillar | Required Metrics |
|---|--------|-----------------|
| **1** | Semantic instrumentation | trace_id, span_id, session_id |
| **2** | Full request-response capture | query, response, tool_calls, retrieved_docs |
| **3** | Continuous metrics monitoring | tokens, cost, latency_p95, eval_score |
| **4** | Integrated evaluation | auto_score, human_score, agreement_rate |
| **5** | Real-time alerting | alert_threshold, incident_count |
| **6** | Data export | export_format, destination |
| **7** | Enterprise security | access_control, compliance_status |

### Tracing Architecture

```
Session (multi-turn conversation)
  └── Trace (end-to-end request processing)
       ├── Span: Query processing
       ├── Span: Retrieval (RAG context fetch)
       ├── Span: Reranking
       ├── Span: Generation (LLM call)
       ├── Span: Tool Call (external API)
       └── Span: Guardrail validation

Each span includes:
  - Start/end timestamps
  - Token usage
  - Model version
  - Input/output
  - Custom metadata (experiment_id, user_segment)
```

---

## 6. Observability Anti-Patterns

| # | Anti-Pattern | Problem | Mitigation |
|---|-------------|---------|-----------|
| **OB-01** | Siloed data | Logs, eval, alerts in separate tools | Unified feedback loop: traces + eval + alerts |
| **OB-02** | Request-level isolation | Each request treated independently | Session-level tracing; conversation analysis |
| **OB-03** | Engineer-only evaluation | Only devs can run evals → scale constraint | Evaluation UI accessible to PM, QA, domain experts |
| **OB-04** | Black-box inference | Model internals opaque | Externalize CoT · detailed tool call logs · decision rationale |
| **OB-05** | No multi-step tracing | RAG/agent pipeline stages uninstrumented | Per-stage spans: Retrieval / Reranking / Generation / Tool Call |

---

## 7. Production Monitoring Dashboard

| Category | Metric | Alert Threshold |
|----------|--------|----------------|
| **Performance** | p50 / p95 / p99 latency | p95 > 2× baseline |
| **Quality** | LLM-as-Judge score (sampled) | < 90% of baseline |
| **Cost** | Tokens per request / daily spend | > 120% budget |
| **Errors** | Failed request rate | > 1% |
| **Safety** | Guardrail trigger rate | > 5% |
| **Drift** | Input distribution change | Significant shift detected |
| **User feedback** | 👍/👎 rate, NPS | Satisfaction < 80% |

### Deployment Checklist (from MLOps)

```markdown
## Pre-Deploy
- [ ] Eval metrics meet or exceed baseline
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
```

---

## 8. Evaluation Tools (2025-2026)

| Tool | Specialty | Key Feature |
|------|-----------|-------------|
| **DeepEval** | General LLM eval | 14+ metrics, RAG + fine-tuning |
| **RAGAS** | RAG-specific | Faithfulness, context relevancy, answer correctness |
| **Langfuse** | Tracing + eval | Open-source, LLM observability |
| **Braintrust** | Eval + logging | Prompt versioning + scoring |
| **Custom** | Domain-specific | Tailored test suites + LLM-as-Judge |

---

## 9. Oracle Integration

```
Oracle workflow integration:
  1. EVALUATE: Apply EV-01–08 anti-pattern checklist
  2. DESIGN: Ensure OB-01–05 are avoided in observability design
  3. ASSESS: Gap analysis of production monitoring dashboard
  4. SPECIFY: Include tracing + eval requirements in Builder specs

Quality gates:
  - LLM judges itself → require different model (EV-01)
  - Test set not fixed → require stable set creation (EV-07)
  - Observability = logs only → require tracing + eval integration (OB-01)
  - Evaluation is engineer-only → recommend accessible eval UI (OB-03)
  - No deployment checklist → require pre/post-deploy validation
```

**Source:** [Datadog: LLM Evaluation Framework Best Practices](https://www.datadoghq.com/blog/llm-evaluation-framework-best-practices/) · [Maxim AI: LLM Observability Best Practices 2025](https://www.getmaxim.ai/articles/llm-observability-best-practices-for-2025/) · [FutureAGI: LLM Evaluation Frameworks 2026](https://futureagi.substack.com/p/llm-evaluation-frameworks-metrics) · [Monte Carlo Data: LLM-as-Judge Best Practices](https://www.montecarlodata.com/blog-llm-as-judge/)
