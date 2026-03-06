# RAG Design & Anti-Patterns (2025-2026)

> Architecture patterns, modern variants (GraphRAG, Agentic RAG, Self-RAG), anti-patterns, evaluation model

## 1. Modern RAG Architecture Taxonomy

| Architecture | Mechanism | Best For | Complexity |
|-------------|-----------|----------|-----------|
| **Vanilla RAG** | Query → Retrieve → Generate | Simple Q&A, FAQ | Low |
| **Hybrid RAG** | BM25 + Dense Vector + Reranker | Production default | Medium |
| **Self-RAG** | Model decides when to retrieve; self-critiques | High factuality needs | Medium |
| **Corrective RAG** | Evaluates retrieval quality; re-retrieves on failure | Reliability-critical | Medium |
| **GraphRAG** | Knowledge graph traversal + community summaries | Multi-hop reasoning, global Q&A | High |
| **Agentic RAG** | Agent plans multi-step retrieval dynamically | Complex research, compliance checks | High |
| **Multi-Agent RAG** | Specialized agents per knowledge domain | Enterprise multi-domain | Very High |

### Decision Flow

```
Simple Q&A over single corpus → Hybrid RAG (default)
Need multi-hop reasoning / global summaries → GraphRAG
Need dynamic strategy adaptation → Agentic RAG
Need high factuality + self-correction → Self-RAG or Corrective RAG
Multiple isolated knowledge domains → Multi-Agent RAG
```

---

## 2. Hybrid Search (Production Default)

```
Query → [Query Expansion / HyDE] → [Embedding]
                                        ↓
                               [Dense Vector Search]
                                        +
                               [BM25 Keyword Search]
                                        ↓
                               [Reciprocal Rank Fusion]
                                        ↓
                               [Cross-Encoder Reranking]
                                        ↓
                               [Top 5-8 Context Assembly]
                                        ↓
                               [LLM Generation]
```

**Key insight:** Hybrid search (BM25 + Dense Vector) shows double-digit relevance improvement over vector-only. Cross-Encoder Reranking is the single highest-ROI improvement.

---

## 3. Chunking Strategies

| Strategy | Best For | Size Guide |
|----------|----------|-----------|
| **Fixed-size** | General documents | 500-1000 tokens, 50-100 overlap |
| **Semantic** | Long documents, topic shifts | Variable (by topic boundary) |
| **Paragraph-based** | Structured docs | 200-500 tokens |
| **AST-based** | Source code | Function/class level |
| **Hierarchical / Parent-child** | Complex docs needing both detail and context | Parent summary + child chunks |

**Anti-pattern RP-02:** Naive fixed chunking (512 tokens, ignore headings) → Faithfulness 0.47-0.51.
**Fix:** Semantic chunking with heading preservation → Faithfulness 0.79-0.82.

---

## 4. Embedding & Vector DB Selection

### Embedding Models (2025)

```
Cost-sensitive + simple queries → text-embedding-3-small
Long documents (>8k tokens)    → voyage-3
Multilingual                   → Cohere embed-v3 or BGE-M3
Highest quality                → text-embedding-3-large
Self-hosted required           → BGE-M3
```

### Vector Database Selection

```
Prototyping (<10k docs)        → ChromaDB
Existing PostgreSQL            → pgvector
Production + Managed           → Pinecone
Production + Self-hosted       → Qdrant or Weaviate
Hybrid search needed           → Weaviate
```

---

## 5. RAG 10 Anti-Patterns

| # | Anti-Pattern | Symptom | Mitigation |
|---|-------------|---------|-----------|
| **RP-01** | Retrieval as afterthought | RAG bolted onto LLM PoC | Design retrieval as first-class system with own SLOs |
| **RP-02** | Naive fixed chunking | 512-token blind splits | Semantic chunking, heading preservation |
| **RP-03** | Monolithic index | All content in one vector DB | Domain-separated indexes (FAQ / policy / technical / logs) |
| **RP-04** | Prompt-heavy, query-light | Focus on prompt template, ignore query pipeline | Query rewrite, intent classification, clarification turns |
| **RP-05** | No evaluation framework | No Recall@K or Precision@K metrics | 3-tier evaluation (Retrieval / Generation / Task) |
| **RP-06** | Knowledge base chaos | Contradictory, outdated documents | Document quality management, version control, conflict detection |
| **RP-07** | Direct live data connection | RAG connected to live APIs | 3-tier knowledge base (static core / periodic / on-demand) |
| **RP-08** | No guardrails | Governance not integrated | Input filtering, source whitelisting, output validation |
| **RP-09** | Context window overload | Entire documents in context | Top 5-8 chunks only, reranker for context compression |
| **RP-10** | No reranking | Raw vector search results used | Cross-Encoder Reranker (highest ROI single improvement) |

---

## 6. Cascade Failure Model

```
Each RAG layer at 95% accuracy:
  Retrieval (0.95) × Reranking (0.95) × Generation (0.95) × Guardrails (0.95)
  = 0.81 (19% failure rate)

Mitigation: Independent quality gates per layer
  - Retrieval: Recall@K ≥ 0.8
  - Reranking: Precision@5 ≥ 0.7
  - Generation: Faithfulness ≥ 0.8
  - Guardrails: Policy violation < 1%
```

---

## 7. RAG Evaluation — 3-Tier Model

| Tier | Target | Metrics | Threshold |
|------|--------|---------|-----------|
| **Retrieval** | Search quality | Recall@K, Precision@K, MRR, NDCG | Recall@5 ≥ 0.8, Precision@5 ≥ 0.7 |
| **Generation** | Output quality | Faithfulness, Relevancy, Answer Correctness | Faithfulness ≥ 0.8 |
| **Task** | Business value | Deflection Rate, Handle Time, CSAT | Task-specific |

**Evaluation anti-patterns:**
- Regenerating test sets each run → noise, incomparable results
- Evaluating Retrieval + Generation as one unit → can't locate bottleneck
- Measuring only vague "accuracy" → no actionable improvement signal

**Tools:** RAGAS (RAG-specific metrics), DeepEval (14+ metrics), custom test suites

---

## 8. GraphRAG Specifics

```
GraphRAG approach:
  1. Extract entities and relationships from documents
  2. Build knowledge graph with community detection
  3. Generate community summaries at multiple levels
  4. Query → graph traversal → relevant communities → LLM synthesis

Advantages:
  - Multi-hop reasoning across documents
  - Global summarization (not just local passage retrieval)
  - Explainable reasoning paths (trace through graph)

When to use:
  - Questions requiring information synthesis across many documents
  - "What are the main themes across all reports?"
  - Compliance checks spanning multiple policies
```

---

## 9. Oracle Integration

```
Oracle workflow integration:
  1. ASSESS: Check RP-01–10 anti-patterns in existing system
  2. DESIGN: Default to Hybrid Search; consider GraphRAG for multi-hop needs
  3. EVALUATE: Apply 3-tier evaluation model
  4. SPECIFY: Include Retrieval SLOs in Builder handoff specs

Quality gates:
  - No Retrieval SLO → block at DESIGN (RP-01)
  - Fixed-size-only chunking → require semantic chunking review (RP-02)
  - "Accuracy" as sole metric → require 3-tier evaluation (RP-05)
  - No Reranker → recommend ROI analysis (RP-10)
```

**Source:** [Redwerk: RAG Best Practices](https://redwerk.com/blog/rag-best-practices/) · [LangWatch: Ultimate RAG Blueprint 2025-2026](https://langwatch.ai/blog/the-ultimate-rag-blueprint-everything-you-need-to-know-about-rag-in-2025-2026) · [Martin Fowler: GenAI Patterns](https://martinfowler.com/articles/gen-ai-patterns/) · [Evidently AI: RAG Evaluation](https://www.evidentlyai.com/llm-guide/rag-evaluation) · [Data Nucleus: RAG Enterprise Guide 2025](https://datanucleus.dev/rag-and-agentic-ai/what-is-rag-enterprise-guide-2025)
