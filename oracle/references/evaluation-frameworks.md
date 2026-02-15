# Evaluation Frameworks Reference

LLM-as-judge、回帰テスト、ベンチマーク設計のリファレンス。

---

## LLM-as-Judge

### Judge Prompt Template

```markdown
## Task
Evaluate the following AI response on these criteria:
1. **Accuracy** (1-5): Are the facts correct?
2. **Relevance** (1-5): Does it answer the question?
3. **Completeness** (1-5): Are all aspects addressed?
4. **Clarity** (1-5): Is it well-organized and clear?

## Question
{question}

## Reference Answer (Ground Truth)
{reference}

## AI Response to Evaluate
{response}

## Output Format
Return JSON:
{
  "accuracy": { "score": N, "reasoning": "..." },
  "relevance": { "score": N, "reasoning": "..." },
  "completeness": { "score": N, "reasoning": "..." },
  "clarity": { "score": N, "reasoning": "..." },
  "overall": N,
  "issues": ["..."]
}
```

### Judge Calibration

| Technique | Description |
|-----------|-------------|
| **Reference grounding** | Always provide ground truth for comparison |
| **Rubric anchoring** | Define what each score means with examples |
| **Position bias mitigation** | Randomize order when comparing A vs B |
| **Multi-judge** | Use 3+ judges, take majority or average |
| **Human calibration** | Periodically validate judge scores against human ratings |

---

## Evaluation Metrics

### Task-Specific Metrics

| Task Type | Primary Metrics | Secondary Metrics |
|-----------|----------------|-------------------|
| **Classification** | Accuracy, F1, Precision, Recall | Confusion matrix |
| **Extraction** | Exact match, Partial match, F1 | Field-level accuracy |
| **Summarization** | ROUGE-L, BERTScore, Faithfulness | Length ratio |
| **Generation** | Human preference, LLM-judge score | Diversity, Fluency |
| **RAG** | Faithfulness, Relevancy, Recall@K | Context precision |
| **Code generation** | Pass@K, Execution success | Test pass rate |

### Composite Scoring

```python
def calculate_composite_score(results: dict) -> float:
    weights = {
        "accuracy": 0.30,
        "relevance": 0.25,
        "completeness": 0.20,
        "clarity": 0.15,
        "safety": 0.10,
    }
    return sum(results[k] * w for k, w in weights.items())
```

---

## Regression Testing

### Test Suite Structure

```
eval/
├── datasets/
│   ├── classification_tests.jsonl
│   ├── extraction_tests.jsonl
│   ├── rag_tests.jsonl
│   └── safety_tests.jsonl
├── baselines/
│   ├── v1.0.0_results.json
│   └── v1.1.0_results.json
├── run_eval.py
└── report.py
```

### Test Case Format

```jsonl
{"id": "cls-001", "input": "Cancel my account", "expected": {"intent": "cancellation"}, "tags": ["billing", "critical"]}
{"id": "cls-002", "input": "How much does it cost?", "expected": {"intent": "pricing"}, "tags": ["sales"]}
{"id": "ext-001", "input": "John Smith, john@example.com", "expected": {"name": "John Smith", "email": "john@example.com"}, "tags": ["extraction"]}
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
                    "metric": metric,
                    "baseline": baseline[metric],
                    "current": value,
                    "delta": delta
                })
    return regressions
```

---

## Benchmark Design

### Custom Benchmark Checklist

- [ ] Define clear evaluation criteria with rubrics
- [ ] Include diverse test cases (easy, medium, hard)
- [ ] Balance across categories and topics
- [ ] Include adversarial/edge cases
- [ ] Establish human performance baseline
- [ ] Version control test datasets
- [ ] Prevent data contamination (check training data)
- [ ] Define statistical significance thresholds
- [ ] Automate scoring where possible
- [ ] Document limitations and known biases

### Evaluation Report Template

```markdown
## Evaluation Report: [Prompt/Model Version]

### Summary
- **Overall Score**: X.XX / 5.00
- **vs. Baseline**: +X.X% / -X.X%
- **Regressions**: [count] metrics below threshold

### Results by Category
| Category | Score | Baseline | Delta | Status |
|----------|-------|----------|-------|--------|
| Accuracy | X.XX | X.XX | +/-X% | PASS/FAIL |

### Regressions
[List any metrics that decreased beyond threshold]

### Recommendations
1. [Action item based on findings]
```
