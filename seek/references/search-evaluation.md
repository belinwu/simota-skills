# Search Quality Evaluation Reference

Purpose: Run a disciplined offline + online evaluation program for ranking quality. Offline metrics (nDCG, MRR, MAP, Precision@k, Recall@k) catch regressions pre-deploy; online signals (CTR, position-bias-corrected engagement, reformulation rate) catch what judgments miss. Without both, ranking changes ship blind.

## Scope Boundary

- **Seek `eval`**: search retrieval evaluation — ranking quality metrics, golden-query sets, click models, offline + online methodology.
- **Experiment (separate skill)**: general A/B test statistics — power, sample size, SRM detection, CUPED variance reduction. Seek `eval` provides the metric; Experiment provides the stat framework.
- **Oracle `eval` (separate skill)**: LLM-output evaluation — faithfulness, grounding, factuality, hallucination detection. Applies to generation quality, not retrieval quality. Separate domain — do not conflate.

Rule of thumb: if you are judging "is this document relevant to the query?" → Seek `eval`. If you are judging "is the LLM's answer grounded in the retrieved context?" → Oracle `eval`.

## Offline Metrics

| Metric | Formula | When to use | Typical target |
|--------|---------|-------------|----------------|
| Precision@k | Relevant in top-k / k | False positives costly (one-shot answer) | P@5 ≥ 0.70 |
| Recall@k | Relevant in top-k / total relevant | Completeness matters (legal, medical, RAG candidate pool) | R@20 ≥ 0.80 |
| MRR | mean(1 / rank of first relevant) | Single-answer / known-item search | MRR ≥ 0.60 |
| MAP | mean AP across queries | Overall ordering quality, binary judgments | MAP ≥ 0.50 |
| nDCG@k | DCG@k / IDCG@k | Graded relevance (3- or 5-point) — production default | nDCG@10 ≥ 0.70 baseline, ≥ 0.85 high-traffic |

Graded judgments (0-3 or 0-4) unlock nDCG and are worth the annotation cost; binary-only setups miss the "good but not perfect" signal that drives most ranking improvements.

## Golden-Query Set

Curate **50-200 representative queries** covering:

- Head queries (top 10% by volume) — weighted heavily.
- Torso queries (next 30%) — coverage of the long body.
- Tail queries (random sample) — regression safety.
- Known-hard queries (typos, ambiguous intent, multi-term).
- Zero-result queries — verify fallback behavior.
- Category-balanced samples (so a single vertical does not dominate the metric).

For each query, collect 20-50 candidate docs and grade them. Sources:

- Manual annotation by domain experts (gold standard, expensive).
- LLM-as-judge (GPT-4 / Claude) with rubric + calibration against 20-50 expert-labeled pairs (cheap, acceptable if agreement κ ≥ 0.6).
- Click-derived pseudo-labels via a click model (see below).

Rotate and refresh 10-20% quarterly — query distributions drift.

## Click Models

Raw CTR is biased: position 1 gets clicks whether or not it is the best result. Debias with an explicit click model:

| Model | Assumption | Use when |
|-------|-----------|----------|
| Cascade | User scans top-down, stops at first click | Short result lists, one-click intent |
| Position-Based Model (PBM) | Click = examination × relevance, examination depends only on position | Default — simple and robust |
| Dynamic Bayesian Network (DBN) | Adds perseverance parameter after click | Long sessions, multi-click queries |
| User Browsing Model (UBM) | Examination depends on distance from last click | Mixed browsing behavior |

Output: a debiased relevance estimate per (query, doc) pair, usable as training signal for `rerank` and as a pseudo-judgment for nDCG.

## Online Signals

Offline metrics miss novelty, diversity, and actual user satisfaction. Track online:

- **CTR@k** (position-bias-corrected).
- **MRR of clicks** — proxy for how deep users scan before clicking.
- **Abandonment rate** — sessions with zero clicks (bad signal, but confounded by "user found answer in snippet").
- **Query reformulation rate** — user refines within 30s (strong bad signal).
- **Dwell time** on clicked result — proxy for satisfaction (>30s = good).
- **Result-page return rate** — user comes back and clicks another result (bad).
- **Null-result rate** — queries with zero hits (critical for tail coverage).

## A/B Test Design for Ranking

Ranking changes are harder to A/B than feature changes. Patterns:

- **Interleaving** (Team-Draft Interleaving, TDI): mix rankings A and B into a single list, attribute clicks. 10-100× more sensitive than split traffic; preferred when applicable.
- **Split traffic**: standard 50/50 when ranker change affects latency or UI. Use CUPED (Experiment skill) to reduce variance.
- **Switchback**: alternate ranker per time window — use when personalization cross-contamination is a risk.
- **Shadow mode**: score both rankers, serve ranker A, log ranker B's top-K. Catches catastrophic regressions pre-launch.

Delegate power analysis, sample-size calculation, SRM detection, and variance-reduction to `Experiment`. Seek `eval` supplies the metric (interleaving win-rate or Δ-CTR with position correction) and the click model.

## Evaluation Workflow

```
1. Build golden set (50-200 queries, graded 0-3).
2. Baseline: run current ranker on golden set → nDCG@10, MRR, Recall@20.
3. Candidate ranker: same run → Δ metrics.
4. If Δ nDCG@10 > +1% absolute AND no per-category regression > 2% → proceed.
5. Shadow-score in production for 1-3 days — watch null-result and latency.
6. Interleaving A/B → win-rate with 95% CI (Experiment).
7. Gate: interleaving win-rate > 55% with p < 0.05 → ship.
8. Post-launch: monitor nDCG drift weekly, CTR + reformulation daily.
```

## Anti-Patterns

- Single aggregate nDCG with no per-segment breakdown — hides category-level regressions.
- Training the ranker on the same queries used for evaluation (leakage).
- Ignoring position bias and declaring CTR uplift a win.
- No zero-result monitoring — a "better" ranker that also increases null-rate is a loss.
- Annotator pool of one — inter-annotator agreement κ < 0.4 means the judgments themselves are noise.
- Metric monoculture — shipping on nDCG alone, ignoring recall degradation for RAG candidate pools.
- Conflating Seek `eval` (ranking quality) with Oracle `eval` (LLM faithfulness) — they measure different stages of the RAG pipeline.

## Paired Deliverables

Every `eval` program ships:

1. Golden-query set spec: query selection, annotation rubric, grade scale.
2. Offline metric plan: primary (nDCG@k) + secondary (MRR, Recall@k), per-segment breakdown.
3. Click-model choice + debiasing pipeline.
4. Online signal dashboard spec.
5. A/B design (interleaving vs split + variance reduction) — cross-ref to `Experiment`.
6. Regression-gate thresholds with per-segment floors.

## Handoff

- To `Experiment`: stat framework — power, sample size, SRM, CUPED. Provide the metric definition.
- To `Radar`: regression test suite — snapshot nDCG per query per ranker commit.
- To `Beacon`: SLO for retrieval quality (nDCG drift > threshold → alert) and null-result rate.
- To `Stream`: click-log + judgment-log ingestion with session / position / dwell fields.
- To `Builder`: logging schema in the serving path — query, ranker version, shown docs, positions, click events.
- Boundary with Oracle `eval`: Seek `eval` ends at the ranked list; Oracle `eval` starts at the LLM-generated answer. Cross-link, do not overlap.
