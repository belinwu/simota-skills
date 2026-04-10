# Search Quality Evaluation Methods

**Purpose:** Metrics, methodologies, and tools for evaluating search quality.
**Read when:** Setting up search quality measurement or running relevance evaluations.

---

## Core Metrics

### Precision@k

```
Precision@k = (number of relevant docs in top-k) / k
```

- **When to use:** False positives are costly (e.g., legal search, medical)
- **Typical targets:** Precision@5 >= 0.8 for high-stakes search

### Recall@k

```
Recall@k = (number of relevant docs in top-k) / (total relevant docs)
```

- **When to use:** Completeness matters (e.g., RAG retrieval, patent search)
- **Typical targets:** Recall@20 >= 0.9 for RAG pipelines

### MRR (Mean Reciprocal Rank)

```
MRR = (1/N) * Σ (1 / rank_of_first_relevant_doc)
```

- **When to use:** Single best answer (e.g., FAQ, navigation search)
- **Typical targets:** MRR >= 0.7

### NDCG@k (Normalized Discounted Cumulative Gain)

```
DCG@k = Σ (relevance_i / log2(i + 1))   for i = 1..k
NDCG@k = DCG@k / IDCG@k                 (ideal DCG)
```

- **When to use:** Graded relevance, position matters (e.g., product search, web search)
- **Typical targets:** NDCG@10 >= 0.7

---

## Judgment Set Creation

### Manual Annotation

```yaml
JUDGMENT_SET:
  size: 100-200 queries
  annotators: 2-3 per query (for inter-annotator agreement)
  scale:
    0: "Not relevant"
    1: "Partially relevant"
    2: "Highly relevant"
  format:
    - query: "how to reset password"
      judgments:
        - doc_id: "doc_123"
          relevance: 2
          annotator: "A"
        - doc_id: "doc_456"
          relevance: 1
          annotator: "A"
```

### LLM-as-Judge

```python
JUDGE_PROMPT = """
Rate the relevance of the following document to the query.

Query: {query}
Document: {document}

Rate on a scale of 0-2:
0 = Not relevant
1 = Partially relevant
2 = Highly relevant

Respond with only the number.
"""

async def llm_judge(query: str, document: str) -> int:
    response = await llm.generate(
        JUDGE_PROMPT.format(query=query, document=document)
    )
    return int(response.strip())
```

### Click Data (Implicit Feedback)

```sql
-- Click-through rate as weak relevance signal
SELECT
  query,
  result_id,
  clicks::float / impressions AS ctr,
  avg_position,
  CASE
    WHEN clicks::float / impressions > 0.1 THEN 2
    WHEN clicks::float / impressions > 0.03 THEN 1
    ELSE 0
  END AS estimated_relevance
FROM search_analytics
WHERE impressions > 10
GROUP BY query, result_id;
```

---

## Evaluation Pipeline

### Offline Evaluation

```python
class SearchEvaluator:
    def __init__(self, judgment_set: dict, search_fn):
        self.judgments = judgment_set
        self.search = search_fn

    def evaluate(self, k: int = 10) -> dict:
        metrics = {"ndcg": [], "mrr": [], "precision": [], "recall": []}

        for query, expected in self.judgments.items():
            results = self.search(query, top_k=k)
            result_ids = [r.id for r in results]

            metrics["ndcg"].append(self._ndcg(result_ids, expected, k))
            metrics["mrr"].append(self._mrr(result_ids, expected))
            metrics["precision"].append(self._precision(result_ids, expected, k))
            metrics["recall"].append(self._recall(result_ids, expected, k))

        return {name: sum(vals)/len(vals) for name, vals in metrics.items()}
```

### A/B Testing for Search

```yaml
AB_TEST_DESIGN:
  method: interleaving  # Preferred for search A/B tests
  variants:
    control: "Current search configuration"
    treatment: "New ranking/retrieval changes"
  metrics:
    primary: "Click-through rate on top-3 results"
    guardrail: "Zero-result rate must not increase > 5%"
  duration: "2 weeks minimum"
  traffic_split: "50/50"
  significance: "p < 0.05"
```

### Interleaving Method

```
Control results:  [A, B, C, D, E]
Treatment results: [C, F, A, G, B]
Interleaved:      [A, C, B, F, D, G, E]
                    ↑C ↑T ↑C ↑T ↑C ↑T ↑C

User clicks on C (position 2, from Treatment) → Treatment wins this impression
```

---

## Regression Testing

### Relevance Regression Test

```yaml
REGRESSION_TEST:
  trigger: "On index mapping or analyzer change"
  golden_set: "tests/search/golden_queries.jsonl"
  thresholds:
    ndcg_at_10: ">= 0.72"
    mrr: ">= 0.65"
    zero_result_rate: "<= 0.05"
  action_on_failure: "Block deployment, alert search team"
```

### Golden Query Format

```jsonl
{"query": "wireless headphones", "expected_top_3": ["prod_123", "prod_456", "prod_789"], "min_ndcg": 0.8}
{"query": "ワイヤレスイヤホン", "expected_top_3": ["prod_123", "prod_456"], "min_ndcg": 0.7}
{"query": "bluetooth earbuds noise cancelling", "expected_top_3": ["prod_789", "prod_012"], "min_ndcg": 0.75}
```

---

## Diagnostic Queries

When search quality drops, investigate with:

```yaml
DIAGNOSTIC_CHECKLIST:
  - Zero-result queries: "What queries return no results?"
  - Low-click queries: "What queries have CTR < 1%?"
  - Position bias: "Are users only clicking position 1?"
  - Query reformulation: "Are users rephrasing queries?"
  - Filter impact: "Do filters eliminate too many results?"
  - Freshness: "Are stale documents ranked too high?"
  - Language mismatch: "Are Japanese queries matching English docs?"
```
