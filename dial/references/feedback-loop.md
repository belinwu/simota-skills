# Feedback Loop

**Purpose:** Design guidance for objective functions, statistical gates, canary + auto-rollback, guardrails, and drift detection.
**Read when:** Closing the safety loop during the FRAME / LAND / MONITOR phases.

## Contents
- Objective Function Design
- Scalarized vs Pareto
- Constraint Encoding
- Goodhart's Law Defense
- Statistical Gate
- Canary Ramp Schedule
- Auto-Rollback Triggers
- Blast Radius and Kill Switch
- Drift Detection
- Re-tuning Trigger Policy
- Land Plan Checklist

---

## Objective Function Design

The objective is what the optimizer maximizes (or minimizes). Wrong objective = optimizer wins, system loses.

### Inputs

| Input | Source | Typical scale |
|-------|--------|----------------|
| p99 latency | Beacon / APM | ms |
| Error rate | Beacon / APM | fraction |
| Throughput | Beacon / load gen | RPS |
| $/req | Ledger / Beacon | currency |
| Energy / kWh | Carbon dashboard | optional |
| GC pause cumulative | Profile | ms/min |
| Tail latency stretch (p99 / p50) | Computed | ratio |

### Direction

Always declare:

```
direction: minimize | maximize
```

### Normalization

Mix-of-units objective must normalize each term. Choose one:

| Method | Use when |
|--------|----------|
| Min-max to `[0, 1]` over recent baseline window | Stable workload |
| Z-score | Heavy-tailed metric |
| Log-transform | Wide-range metric (e.g., $/req) |
| Reference ratio (`x / baseline`) | Quick interpretation |

---

## Scalarized vs Pareto

### Scalarized (weighted sum)

```
score = 0.7 * normalize(p99_ms) + 0.3 * normalize(cost_per_req)
```

| Pros | Cons |
|------|------|
| Single number; BO friendly | Hides trade-offs; weights are subjective |
| Easy CI / pass-fail | Weight change = different winner |

**Use when**: stakeholders agree on weights, or the trade-off is asymmetric (latency dominates cost by orders of magnitude).

### Pareto (multi-objective)

Find the non-dominated set. No single winner; the human picks the operating point.

| Pros | Cons |
|------|------|
| Honest about trade-off | Needs visualization (Canvas handoff) |
| Works under shifting weights | Larger search budget |

**Tools**: BoTorch qEHVI, NSGA-II.

**Use when**: trade-off is genuinely two-sided (latency × throughput × cost) and stakeholders need to choose, not be told.

**Rule**: If the team cannot agree on weights within one meeting, the objective is Pareto, not scalarized.

---

## Constraint Encoding

A constraint is a hard rule the optimizer must respect.

```yaml
constraints:
  - "error_rate <= baseline.error_rate * 1.10"
  - "throughput_rps >= baseline.rps * 0.95"
  - "p95_ms <= 800"
  - "rss_mb <= container_mem_mb * 0.85"
```

| Encoding | Behavior |
|----------|----------|
| Penalty (return `inf` on violation) | Strong, prevents exploration of infeasible region |
| Soft penalty (`score += large_const`) | Gentle, allows borderline exploration |
| Surrogate constraint (Constrained BO) | Most principled — models feasibility |

**Recommended default**: hard penalty (`return inf`) for safety-critical constraints (error rate, OOM); soft penalty for soft preferences.

---

## Goodhart's Law Defense

> "When a measure becomes a target, it ceases to be a good measure."

Defenses:

| Defense | Mechanism |
|---------|-----------|
| Multi-metric objective | Optimizer cannot win one at the cost of another |
| Constraints on adjacent metrics | Latency improvement bounded by error-rate cap |
| Hidden holdout metric | Track but don't optimize; alert on regression |
| Synthetic adversarial workload | Beats single-shape overfitting |
| Periodic re-baseline | Detect when "winner" decayed |

**Hidden holdout example**: optimize p99 latency, but monitor `tail_stretch = p99 / p50`. If tail stretch worsens, optimizer is hiding latency cost in the tail.

---

## Statistical Gate

Before declaring a candidate the winner, statistical separation from baseline must be established.

### Minimum Detectable Effect (MDE)

```
MDE >= 2 * sigma_baseline   (short campaigns)
MDE >= 1 * sigma_baseline   (long campaigns, n >= 100)
```

If the candidate's expected effect < MDE, **do not declare a winner** — increase sample size or accept the parameter is not worth tuning.

### Sample size per arm

```
n >= max(30, (3 * sigma / MDE)^2)
```

### Significance gate

| Test | Use when |
|------|----------|
| Welch's t-test (one-sided) | Comparing two arm means, unequal variance |
| Mann-Whitney U | Non-normal distributions, p99 latency typical |
| Bayesian posterior CI excludes baseline | Bayesian BO / MAB native |
| Sequential testing (mSPRT, always-valid) | Online MAB to prevent peeking inflation |

**Recommended**: Mann-Whitney for latency, Bayesian posterior for BO / MAB. Welch's t-test for throughput / $/req.

### Multiple comparisons

If `K` arms are compared in one campaign, apply Bonferroni (`α / K`) or Holm correction. Skipping this inflates false-win rate to `1 - (1 - α)^K`.

---

## Canary Ramp Schedule

Production validation is mandatory for user-impact-critical parameters. Synthetic alone is insufficient.

| Stage | Traffic | Hold | Gate |
|-------|---------|------|------|
| Shadow (mirror traffic, no user impact) | 100% mirror | 1h | functional sanity, error rate parity |
| Canary 1% | 1% | 30m | no auto-rollback trigger, no error-rate spike |
| Canary 5% | 5% | 2h | objective within `MDE` of predicted, error rate within constraint |
| Canary 25% | 25% | 6h | objective statistically separated from baseline |
| 100% | 100% | indefinite | promoted; baseline updates after 7d |

**Hold time** must cover one diurnal cycle for traffic-shape-sensitive parameters (typically 24h before 100%).

**Auto-promote** is allowed only when all stage gates pass without manual intervention. Manual promote is required for irreversible config (e.g., schema-touching pool changes).

---

## Auto-Rollback Triggers

```yaml
rollback_trigger:
  any_of:
    - "p99_ms > 2 * baseline.p99_ms for 60s"
    - "error_rate > 2 * baseline.error_rate for 60s"
    - "saturation_pct > 95 for 30s"
    - "oom_kill_count > 0 in 5m"
    - "user_signal:guardrail_alert from Beacon"
```

| Trigger property | Recommended |
|------------------|-------------|
| Detection window | `30s` for hard safety, `60s` for soft latency |
| Min sustain time | `2 × detection window` to filter noise |
| Action | revert to last-good config + alert + page on-call |
| Cooldown | `≥ 24h` before re-trying same config |

**Two-out-of-three rule** for noisy environments: require two independent triggers (latency AND error, not OR) to avoid flapping. Sacrifice a small response-time delay for stability.

---

## Blast Radius and Kill Switch

### Blast radius cap

```
blast_radius_pct_traffic: 5
```

The campaign cannot expose more than this fraction of traffic to the candidate at any time before final promote. Hard cap; the canary ramp respects it.

### Kill switch

Every campaign must wire a feature-flag kill switch that:

- reverts the candidate to baseline in `≤ 60s` when flipped,
- can be flipped by on-call without the campaign owner,
- is in a separate dimension from the candidate's identity (use a flag system like Statsig / GrowthBook / Unleash, not the candidate's own config).

**Test the kill switch before any traffic ramp**. An untested kill switch is a kill *belief*.

---

## Drift Detection

A tuned parameter is only optimal for the workload it was tuned on. Workload changes invalidate the tuning.

### Workload drift

| Signal | Threshold |
|--------|-----------|
| Traffic-shape KL divergence vs baseline | `≥ 0.10` |
| Top-route share shift | `≥ 15%` |
| Payload-size 95th-percentile shift | `≥ 30%` |
| Time-of-day distribution shift | `≥ 20%` mass change |

### Pareto-front drift

Periodically re-run a small slice of the original campaign (`5–10` evals) to verify the Pareto front. If the new front Pareto-dominates the deployed point, retune.

### Config drift

The applied config differs from the canonical artifact. Detect via:
- IaC + GitOps audit (Gear handoff).
- Beacon assertion: deployed config hash must equal artifact hash.

### SLO regression

If SLO regresses despite no deployment, workload drifted. Treat as re-tune signal.

---

## Re-tuning Trigger Policy

```yaml
re_tune_triggers:
  - workload_drift:
      condition: "kl_divergence >= 0.10"
      cooldown: "7d"
  - pareto_drift:
      condition: "shift_pct >= 15"
      cooldown: "14d"
  - slo_regression_30d:
      condition: "p99_ms_avg_30d > baseline.p99_ms * 1.15"
      cooldown: "14d"
  - config_drift:
      condition: "deployed_hash != artifact_hash"
      cooldown: "immediate"
  - quarterly_refresh:
      schedule: "first business day of Feb, May, Aug, Nov"
```

**Cooldown** prevents oscillation. Without it, two opposed signals fire alternately and the loop thrashes.

---

## Land Plan Checklist

Before landing (entering canary 1%):

- [ ] Winner statistically separated from baseline (gate passed)
- [ ] All hard constraints satisfied
- [ ] Predicted effect within prediction interval of benchmark
- [ ] Guardrail wired: SLO budget allocated, auto-rollback trigger live
- [ ] Kill switch tested with synthetic traffic
- [ ] On-call notified, runbook linked
- [ ] Beacon dashboard for the campaign live and visible
- [ ] Ledger / cost-impact estimate calculated (if cost was an objective)
- [ ] Revert path validated (last-good config archived, can be redeployed in `≤ 10m`)
- [ ] Campaign artifact (YAML) merged to repo with reviewer approval
- [ ] Drift-detection job scheduled (`re_tune_triggers` registered)

If any item is unchecked, **do not start canary ramp**. The campaign is incomplete, not "almost ready."

---

## Anti-Patterns

| Anti-pattern | Consequence | Fix |
|--------------|-------------|-----|
| Optimize p50 when SLO is p99 | Latency win invisible to users; tail worse | Optimize p99 + constrain p50 |
| Single trigger auto-rollback | False positives flap | Two-out-of-three rule |
| Synthetic-only promote | Production workload reveals regression after 100% | Mandatory canary for user-impact-critical |
| Reuse winner across workloads | Drift wipes the gain silently | Drift detection + re-tune policy |
| Adjust objective weights mid-flight | Goodhart squared | Freeze objective for campaign lifetime |
| Skip kill-switch test | Untested kill is kill *belief* | Synthetic trigger before any ramp |
| One-time tuning labeled "auto" | The "auto" never runs | If no MONITOR phase, it's not autotuning — call it what it is |
