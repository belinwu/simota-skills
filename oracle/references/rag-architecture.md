# RAG Architecture Reference

チャンク戦略、埋め込みモデル比較、ベクトルDB選定、検索品質メトリクスのリファレンス。

---

## Chunking Strategies

| Strategy | Chunk Size | Overlap | Best For |
|----------|-----------|---------|----------|
| **Fixed-size** | 500-1000 tokens | 50-100 tokens | General documents |
| **Sentence-based** | 3-5 sentences | 1 sentence | Factual content |
| **Paragraph-based** | 1-3 paragraphs | 1 paragraph | Structured docs |
| **Semantic** | Variable (by topic) | Topic boundary | Long documents |
| **Recursive** | Hierarchical splits | Parent context | Code, legal docs |

### Chunking Decision Matrix

| Content Type | Strategy | Size | Overlap |
|-------------|----------|------|---------|
| FAQ / Q&A | Sentence | 1-2 sentences | 0 |
| Technical docs | Paragraph | 200-500 tokens | 50 tokens |
| Legal contracts | Recursive | 500-1000 tokens | 100 tokens |
| Source code | AST-based | Function/class | Imports/context |
| Chat history | Turn-based | 5-10 turns | 2 turns |

---

## Embedding Models

| Model | Dimensions | Max Tokens | Quality | Speed | Cost |
|-------|-----------|------------|---------|-------|------|
| **text-embedding-3-large** | 3072 | 8191 | Excellent | Medium | $$ |
| **text-embedding-3-small** | 1536 | 8191 | Good | Fast | $ |
| **voyage-3** | 1024 | 32000 | Excellent | Medium | $$ |
| **Cohere embed-v3** | 1024 | 512 | Good | Fast | $ |
| **BGE-M3** | 1024 | 8192 | Good | Self-hosted | Free |

### Selection Criteria

```
IF cost-sensitive AND simple queries → text-embedding-3-small
IF long documents (>8k tokens) → voyage-3
IF multilingual → Cohere embed-v3 or BGE-M3
IF highest quality needed → text-embedding-3-large
IF self-hosted required → BGE-M3
```

---

## Vector Database Selection

| Database | Type | Scale | Features | Best For |
|----------|------|-------|----------|----------|
| **Pinecone** | Managed | Billions | Metadata filtering, namespaces | Production SaaS |
| **Weaviate** | Self-hosted/Cloud | Millions+ | Hybrid search, GraphQL | Full-featured search |
| **Qdrant** | Self-hosted/Cloud | Millions+ | Filtering, geo-search | Flexible deployment |
| **pgvector** | Extension | Millions | SQL integration, transactions | Existing Postgres |
| **ChromaDB** | Embedded | Thousands | Simple API, local | Prototyping |

### Decision Flow

```
Small scale (<10k docs) + Prototyping → ChromaDB
Existing PostgreSQL → pgvector
Production + Managed → Pinecone
Production + Self-hosted → Qdrant or Weaviate
Hybrid search needed → Weaviate
```

---

## Retrieval Quality Metrics

| Metric | Formula | Target | Measures |
|--------|---------|--------|----------|
| **Recall@K** | Relevant retrieved / Total relevant | >0.8 | Coverage |
| **Precision@K** | Relevant retrieved / K | >0.7 | Accuracy |
| **MRR** | 1/rank of first relevant | >0.6 | Ranking quality |
| **NDCG@K** | Normalized DCG | >0.7 | Ranking order |
| **Faithfulness** | Grounded claims / Total claims | >0.9 | Hallucination |
| **Answer relevancy** | Relevant answers / Total answers | >0.8 | Usefulness |

### Retrieval Pipeline Architecture

```
Query → [Query Expansion] → [Embedding] → [Vector Search]
                                              ↓
                                     [Hybrid Search (BM25)]
                                              ↓
                                     [Reranking (Cross-encoder)]
                                              ↓
                                     [Context Assembly]
                                              ↓
                                     [LLM Generation]
```

### Hybrid Search Configuration

```python
# Combine vector similarity + keyword search
def hybrid_search(query: str, k: int = 10, alpha: float = 0.7):
    vector_results = vector_db.search(embed(query), k=k*2)
    keyword_results = bm25_index.search(query, k=k*2)

    # Reciprocal Rank Fusion
    combined = reciprocal_rank_fusion(
        vector_results,
        keyword_results,
        weights=[alpha, 1-alpha]
    )
    return combined[:k]
```

---

## RAG Evaluation Framework

### End-to-End Evaluation

| Component | Metric | Tool |
|-----------|--------|------|
| Retrieval | Recall@K, Precision@K | RAGAS, custom |
| Generation | Faithfulness, Relevancy | RAGAS, LLM-as-judge |
| End-to-end | Answer correctness | Human eval, LLM-as-judge |

### Test Dataset Template

```json
{
  "test_id": "rag-001",
  "question": "What is the refund policy for annual plans?",
  "ground_truth": "Annual plans can be refunded within 30 days...",
  "expected_sources": ["docs/billing/refund-policy.md"],
  "category": "billing",
  "difficulty": "easy"
}
```
