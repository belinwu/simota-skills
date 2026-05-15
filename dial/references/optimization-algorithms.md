# Optimization Algorithms

**Purpose:** Search-strategy selection criteria, budget sizing, and the Campaign-as-Code specification.
**Read when:** Choosing the algorithm to explore the parameter space, sizing the number of trials, or persisting the campaign as a reproducible artifact.

## Contents
- Algorithm Decision Matrix
- Grid Search
- Random Search
- Bayesian Optimization (BO)
- Multi-Armed Bandit (MAB)
- Evolutionary / CMA-ES
- Adaptive Concurrency Limits
- Tools and Libraries
- Search Budget Sizing
- Termination Criteria
- Campaign-as-Code Schema
- Reference Run Example

---

## Algorithm Decision Matrix

| Algorithm | Best for | Budget needed | Handles noise | Dim limit | Online? |
|-----------|----------|----------------|----------------|-----------|---------|
| **Grid** | Small discrete, ≤ 3 dim, strong prior, kernel/OS knobs | `≤ 50` evals | poor | 3 | No |
| **Random** | Quick baseline, ≤ 6 dim, fast iteration | `30–100` evals | OK | 6 | No |
| **Bayesian (GP / TPE)** | Continuous, noisy, expensive evaluation, ≤ 10 dim | `30–200` evals | strong | 10 | No |
| **MAB (Thompson / UCB)** | Online, traffic split between arms, discrete choices | continuous | strong | ≤ 4 arms | Yes |
| **Evolutionary / CMA-ES** | Non-convex, ≥ 10 dim, robust to noise, big budget | `200–5000` evals | OK | 30+ | No |
| **Adaptive Concurrency** | Runtime pool/queue sizing under variable backend | continuous | strong | 1 (limit) | Yes |

### Quick picker

```
Online vs offline?
├─ Online (production traffic always)
│  ├─ Single concurrency limit ────────────────→ Adaptive Concurrency
│  └─ Discrete arms ────────────────────────────→ MAB (Thompson)
└─ Offline (benchmark or shadow)
   ├─ Dim ≤ 3 AND discrete AND strong prior ────→ Grid
   ├─ Dim ≤ 6 AND need quick first pass ────────→ Random
   ├─ Dim ≤ 10 AND budget ≤ 200 ────────────────→ Bayesian
   └─ Dim ≥ 10 OR very non-convex ──────────────→ CMA-ES / Evolutionary
```

---

## Grid Search

Best when: parameter space is small, discrete, kernel/OS knobs with large discrete effects.

| Property | Value |
|----------|-------|
| Exhaustive | yes (within bounds and step) |
| Parallel | trivially parallel |
| Noise handling | poor (single eval per point) |
| When to retire | dim > 3 or eval cost > 1 min |

**Tip**: For kernel/OS where each eval is cheap but parameter has large effect, Grid is often optimal — Bayesian's exploration overhead is wasted.

---

## Random Search

Best when: quick baseline, fast iteration, dim > 3, want better-than-Grid coverage with the same budget.

| Property | Value |
|----------|-------|
| Coverage | better than Grid for dim ≥ 4 (Bergstra & Bengio 2012) |
| Parallel | trivially parallel |
| Noise handling | OK with repeats |
| When to retire | when you need exploitation, not just exploration |

**Use as warmup** for Bayesian — Random for the first 10–20 evals fills the prior, then switch to BO.

---

## Bayesian Optimization (BO)

Best when: continuous parameters, noisy expensive evaluations, dim ≤ 10, budget ≤ 200.

| Surrogate | When |
|-----------|------|
| Gaussian Process (GP) | small budget, continuous params, smooth surface |
| Tree-structured Parzen Estimator (TPE) | mixed continuous/categorical, larger budget |
| Random Forest (SMAC) | mostly categorical, large budget, conditional spaces |

| Acquisition function | Trade-off |
|----------------------|-----------|
| Expected Improvement (EI) | balanced, default |
| Upper Confidence Bound (UCB) | explicit exploration knob |
| Probability of Improvement (PI) | aggressive exploitation |

**Tools**: Optuna (TPE/GP), Hyperopt (TPE), BoTorch (GP), scikit-optimize (GP/RF), Vizier (Google), Ax (BoTorch).

**Default**: Optuna + TPE + EI for most application-tuning campaigns. Switch to BoTorch + GP when surface is smooth and you have rich profile data.

**Multi-objective BO**: Use BoTorch / Ax with qEHVI (expected hypervolume improvement) for Pareto-front search across e.g., latency × throughput × cost. See `feedback-loop.md`.

---

## Multi-Armed Bandit (MAB)

Best when: parameters are discrete choices and you can split production traffic across arms in real time.

| Algorithm | Use |
|-----------|-----|
| Thompson Sampling | strong default; handles delayed rewards |
| UCB1 | deterministic, simpler to debug |
| LinUCB / Contextual MAB | when context (user segment, time-of-day) shifts the best arm |
| Epsilon-greedy | poor; do not use as primary |

**Use cases**:
- Choose among `{LRU, LFU, ARC}` cache policies.
- Choose among autoscaler target percentages.
- A/B-test infrastructure already exists; piggyback the MAB on it.

**Risk**: MAB requires reward signal per arm. Reward must be measurable per request (latency, error, $/req) — not per quarter.

---

## Evolutionary / CMA-ES

Best when: dim ≥ 10, non-convex, noisy, budget can scale to thousands.

| Property | Value |
|----------|-------|
| Variant | CMA-ES (continuous), NSGA-II (multi-obj), Genetic (categorical) |
| Parallel | natural (one generation = one batch) |
| Noise handling | OK via resampling |
| Budget | 200–5000+ evals |

**Use case**: Tuning autoscaler policy across 15+ parameters where the surface is irregular.

---

## Adaptive Concurrency Limits

Best when: runtime pool / queue sizing facing a backend with variable latency.

References: [Netflix/concurrency-limits](https://github.com/Netflix/concurrency-limits) (Java library originating the patterns); [Envoy adaptive_concurrency filter](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/adaptive_concurrency_filter) (L7 proxy implementation that removes manual circuit-breaker tuning, used in production at Lyft).

| Algorithm | Mechanism |
|-----------|-----------|
| Vegas (TCP Vegas-inspired) | adjusts limit based on observed vs minimum RTT |
| Gradient2 | adjusts limit based on latency gradient |
| AIMD | additive increase, multiplicative decrease |
| Envoy `gradient_controller` | filter-level: minRTT sampling window + sample-aggregate percentile + concurrency-update interval |

**Use cases**:
- App-side: pool sizing in front of a variable-latency dependency. Replaces a tuned-but-static `maximumPoolSize` with an online controller.
- Proxy-side: enable Envoy's adaptive_concurrency filter at the service-mesh edge so each upstream gets per-cluster auto-tuned concurrency without per-service code changes. Recommended when the same backend serves many callers — the proxy is the natural choke point. [Source: Envoy docs - Adaptive Concurrency filter](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/adaptive_concurrency_filter)

**Boundary**: This is **the controller running in production**, not a tuning campaign. Dial's job is to design the controller (algorithm + signal + bounds + safety floor + filter config); operations runs it. Hand off Envoy/Istio filter rollout to **Gear** (config land) and SLO-budget wiring to **Beacon**.

---

## Tools and Libraries

| Tool | Languages | Best for |
|------|-----------|----------|
| Optuna | Python | Default BO/TPE; great UI; multi-objective; pruning |
| Hyperopt | Python | TPE; older but stable |
| Ax / BoTorch | Python | GP-based BO, multi-objective qEHVI, constraints |
| scikit-optimize | Python | Simple BO, lightweight |
| Vizier (Google OSS) | Python / RPC | Distributed BO, parallel trials |
| Ray Tune | Python | Distributed orchestration over Optuna/BoTorch/HEBO |
| concurrency-limits | Java | Adaptive Concurrency for JVM |
| linkerd-2 ALG | Rust | Adaptive routing in service mesh |
| KEDA | K8s | Autoscaler scalers (not tuner) |
| Kubernetes VPA | K8s | Autotune CPU/memory requests (uses recommender, not BO) |

---

## Search Budget Sizing

Budget = number of evaluations the campaign will run.

| Factor | Effect on budget |
|--------|-------------------|
| Dim | linear (BO) to combinatorial (Grid) |
| Noise σ | quadratic — `n ∝ (σ/MDE)²` per arm |
| Eval cost | sets wallclock budget |
| Parallel evaluators | reduces wallclock but not eval count |
| Algorithm | BO is 5–20× more sample-efficient than Random |

### Rule of thumb

```
budget_evals = max(
  30,                       # noise-floor minimum
  10 * dim,                 # BO rule of thumb
  (3 * sigma / MDE)^2       # statistical-power floor
)
```

**Stop early** if convergence is reached (see Termination).

---

## Termination Criteria

| Criterion | Definition | When to use |
|-----------|------------|-------------|
| Budget exhausted | reached `budget_evals` | always set as ceiling |
| Convergence | best score plateau for `K` evals | typical `K = 20` for BO |
| MDE achieved | improvement ≥ MDE with statistical significance | preferred for canary stage |
| Pareto-front stable | no new non-dominated points for `K` evals | multi-objective |
| SLO breach budget exhausted | guardrail trip count ≥ cap | safety stop, not success |
| Time-box | wallclock elapsed | hard ceiling for CI / canary |

Always set **at least two** criteria: a success criterion (convergence / MDE) and a safety criterion (budget / time-box / SLO breach).

---

## Campaign-as-Code Schema

Every Dial campaign is codified. Default format: YAML (CUE or Python script if rich constraints are needed).

```yaml
campaign:
  name: "checkout-jvm-gc-2026q2"
  version: 1
  owner: "performance@example.com"
  workload_class: "web"
  seed: 42

  baseline:
    p99_ms: 320
    error_rate: 0.0008
    rps: 1400
    sigma_p99_ms: 14
    profile_snapshot: "s3://dial/profiles/checkout/20260512.pyrope"

  objective:
    type: "scalarized"        # or "pareto"
    formula: "0.7 * normalize(p99_ms) + 0.3 * normalize(cost_per_req)"
    direction: minimize
    constraints:
      - "error_rate <= baseline.error_rate * 1.10"
      - "throughput_rps >= baseline.rps * 0.95"

  parameter_space:
    - name: "jvm.heap.max_mb"
      type: integer
      bounds: [2048, 8192]
      step: 256
      prior: 4096
    - name: "jvm.gc.max_pause_ms"
      type: integer
      bounds: [100, 400]
      step: 25
      prior: 200

  algorithm:
    name: "optuna.tpe"
    acquisition: "ei"
    n_startup_trials: 10

  budget:
    evals: 80
    wallclock_max: "4h"

  evaluator:
    type: "benchmark"           # benchmark | shadow | canary
    harness: "siege:checkout-load-2"
    repeats_per_eval: 3
    warmup_seconds: 60
    measurement_seconds: 240

  guardrail:
    slo_budget_pct_monthly: 5
    blast_radius_pct_traffic: 5
    rollback_trigger: "p99_ms > 2 * baseline.p99_ms for 60s OR error_rate > 2 * baseline.error_rate for 60s"
    kill_switch: "feature_flag:dial.checkout-jvm-gc.enabled"

  termination:
    - budget_exhausted
    - convergence:
        plateau_evals: 20
    - safety:
        slo_breach_count_max: 3

  land_plan:
    canary_ramp:
      - { pct: 1, hold: "30m" }
      - { pct: 5, hold: "2h" }
      - { pct: 25, hold: "6h" }
      - { pct: 100, hold: "indefinite" }
    promote_gate: "p99_ms <= winner_predicted_p99 * 1.10 AND error_rate <= baseline.error_rate"

  drift:
    workload_kl_max: 0.10
    pareto_front_shift_max_pct: 15
    re_tune_trigger: "any of [workload_drift, pareto_drift, slo_regression_30d]"

  artifacts:
    output_dir: "s3://dial/campaigns/checkout-jvm-gc-2026q2/"
    log_format: "optuna+json"
```

---

## Reference Run Example

A short illustrative loop (Python with Optuna).

```python
import optuna

def evaluator(trial):
    heap_mb       = trial.suggest_int("heap_mb", 2048, 8192, step=256)
    pause_target  = trial.suggest_int("pause_target", 100, 400, step=25)

    cfg = render_config(heap_mb=heap_mb, max_gc_pause=pause_target)
    deploy_to_benchmark_environment(cfg)
    result = run_benchmark(repeats=3, warmup_s=60, measure_s=240)

    if not guardrails_passed(result):
        return float("inf")

    return 0.7 * normalize(result.p99_ms) + 0.3 * normalize(result.cost_per_req)

study = optuna.create_study(
    direction="minimize",
    sampler=optuna.samplers.TPESampler(n_startup_trials=10, seed=42),
    pruner=optuna.pruners.MedianPruner(n_warmup_steps=2),
)
study.optimize(evaluator, n_trials=80, timeout=4 * 3600)

best = study.best_trial
print("winner:", best.params, "score:", best.value)
emit_canary_plan(best.params)
```

The actual landing happens through the **canary plan** (see `feedback-loop.md`), not by writing the winner directly to production.

---

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Grid Search on 6+ dim | switch to Bayesian or Random; you cannot fund the budget |
| BO without noise modeling | use heteroscedastic GP or repeated evaluation |
| Selecting winner by single benchmark run | repeat ≥ 3× and verify statistical separation |
| Co-tuning > 2 parameters in one campaign | decompose sequentially (see `parameter-space.md`) |
| Reusing same Bayesian study across workload shifts | start a new study after drift detection |
| Optimizing on a synthetic that no longer matches prod | refresh fixture (see `feedback-loop.md` drift) |
| Letting MAB run without a guardrail | every MAB needs SLO floor + kill-switch |
