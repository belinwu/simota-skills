# Search Engine Comparison Guide

**Purpose:** Decision framework for search engine and vector DB selection.
**Read when:** Choosing between search engines or vector databases for a project.

---

## Full-Text Search Engines

| Feature | Elasticsearch | OpenSearch | Meilisearch | Typesense |
|---------|--------------|-----------|-------------|-----------|
| **License** | Elastic License 2.0 | Apache 2.0 | MIT | GPL-3.0 |
| **Vector Search** | Yes (8.x+) | Yes (2.x+) | Yes (1.3+) | Yes (0.25+) |
| **Japanese** | kuromoji plugin | kuromoji plugin | Limited | Limited |
| **Aggregations** | Advanced | Advanced | Basic | Basic |
| **Learning Curve** | High | High | Low | Low |
| **Managed Services** | Elastic Cloud | AWS OpenSearch | Meilisearch Cloud | Typesense Cloud |
| **Best For** | Enterprise, complex search | AWS-native, fork of ES | Dev-friendly, small-medium | Simple, typo-tolerant |
| **Max Scale** | PB-scale | PB-scale | ~10M docs | ~100M docs |

### Selection Guide

```
Is your data > 100M documents?
  ├─ Yes → Elasticsearch or OpenSearch
  │   ├─ AWS-native? → OpenSearch
  │   └─ Multi-cloud / on-prem? → Elasticsearch
  └─ No
      ├─ Need Japanese support? → Elasticsearch/OpenSearch
      ├─ Developer experience priority? → Meilisearch
      ├─ Typo tolerance critical? → Typesense
      └─ Already have ES expertise? → Elasticsearch
```

---

## Vector Databases

| Feature | pgvector | Pinecone | Weaviate | Qdrant | ChromaDB |
|---------|---------|---------|---------|-------|---------|
| **Type** | Extension | Managed SaaS | Self-hosted/Cloud | Self-hosted/Cloud | Embedded/Server |
| **License** | PostgreSQL | Proprietary | BSD-3 | Apache 2.0 | Apache 2.0 |
| **Index Types** | HNSW, IVFFlat | Proprietary | HNSW | HNSW | HNSW |
| **Filtering** | SQL WHERE | Metadata | GraphQL + filters | Payload filters | Metadata |
| **Hybrid Search** | tsvector + vector | Sparse + dense | BM25 + vector | Sparse + dense | Limited |
| **Max Scale** | ~10M vectors | Billions | 100M+ | 100M+ | ~1M |
| **Ops Complexity** | Low (part of PG) | Zero (managed) | Medium | Medium | Low |
| **Best For** | Existing PG, hybrid | Managed at scale | Multi-modal, GraphQL | Filtering + vector | Prototyping, small |
| **Cost** | Free (PG cost) | $70+/month | Free self-host | Free self-host | Free |

### Selection Guide

```
Already using PostgreSQL?
  ├─ Yes, < 5M vectors → pgvector (no new infra)
  └─ No or > 5M vectors
      ├─ Want zero ops? → Pinecone
      ├─ Heavy filtering + vector? → Qdrant
      ├─ Multi-modal (text + image)? → Weaviate
      ├─ Rapid prototyping? → ChromaDB
      └─ Large scale + cost-sensitive? → Qdrant self-hosted
```

---

## Hybrid Search Capability Comparison

| Capability | ES/OS 8.x | pgvector + pg | Weaviate | Qdrant |
|-----------|-----------|---------------|---------|--------|
| Native RRF | Yes | Manual (SQL) | Yes | Manual |
| BM25 + kNN | Yes | tsvector + vector | Yes | sparse + dense |
| Cross-encoder rerank | Plugin/app layer | App layer | Module | App layer |
| Filtered vector search | Pre/post filter | SQL WHERE | GraphQL filter | Payload filter |
| Multi-field boosting | Yes | Manual scoring | Yes | Manual |

---

## Cost Comparison (Approximate Monthly)

| Tier | Elasticsearch Cloud | AWS OpenSearch | Pinecone | Qdrant Cloud |
|------|-------------------|---------------|---------|-------------|
| Dev/Test | $95 (2GB RAM) | $30 (t3.small) | $0 (starter) | $0 (free tier) |
| Small Prod | $250 (4GB, HA) | $150 (m5.large) | $70 (s1.x1) | $25 (1GB) |
| Medium Prod | $800 (16GB, HA) | $500 (r5.xlarge) | $250 (s1.x4) | $100 (4GB) |
| Large Prod | $2500+ (64GB+) | $1500+ (custom) | Custom | $350+ (16GB) |

*Prices are approximate and vary by region and configuration.*

---

## Migration Paths

### Elasticsearch → OpenSearch

- API-compatible (mostly drop-in)
- Main differences: licensing, some plugins, version numbering
- Use snapshot/restore for data migration

### Single DB → Dedicated Search

```
Phase 1: Add search engine alongside DB (dual-write or CDC)
Phase 2: Migrate read queries to search engine
Phase 3: Remove search-related indexes from primary DB
Phase 4: Optimize search engine configuration
```

### pgvector → Dedicated Vector DB

```
Phase 1: Export embeddings to vector DB
Phase 2: Dual-read (query both, compare results)
Phase 3: Switch primary retrieval to vector DB
Phase 4: Keep pgvector as fallback / for joined queries
```
