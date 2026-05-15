# Agent Integrations

**Purpose:** Handoff templates, joint-execution flows, and operational boundaries between Dial and adjacent agents.
**Read when:** Firing a handoff, designing a cross-agent campaign, or re-confirming role boundaries.

## Contents
- Collaboration Map
- Handoff Templates
- Cross-Agent Campaign Flow
- Boundary Recap
- Failure-Mode Routing

---

## Collaboration Map

```
                    ┌─────────────────────────────────────┐
                    │ INPUT (problem → loop need)         │
                    │  User     → tuning mechanism wanted │
                    │  Bolt     → one-shot is recurring   │
                    │  Tuner    → DB knob has dynamic opt │
                    │  Beacon   → SLO breach pattern      │
                    │  Oracle   → AI serving knob runtime │
                    │  Siege    → param sensitivity found │
                    │  Atlas    → arch bottleneck knob    │
                    └────────────────┬────────────────────┘
                                     ↓
                            ┌────────────────┐
                            │      Dial      │
                            │ loop designer  │
                            └────┬──────┬────┘
                                 ↓      ↓
       ┌─────────────────────────┘      └─────────────────────────┐
       ↓                                                          ↓
┌───────────────────────────────┐         ┌──────────────────────────────────┐
│ OUTPUT (loop component)        │         │ OUTPUT (verification / observe)  │
│  Bolt   → impl the delta       │         │  Siege   → bench at scale        │
│  Tuner  → DB-internal trade    │         │  Beacon  → SLO + guardrail wire  │
│  Gear   → land in build/runtime│         │  Canvas  → Pareto / trajectory   │
│  Builder→ campaign runner code │         │                                  │
└───────────────────────────────┘         └──────────────────────────────────┘
```

---

## Handoff Templates

### Bolt → Dial: `BOLT_TO_DIAL`

```yaml
BOLT_TO_DIAL_HANDOFF:
  reason: "one-shot optimization is a recurring need; promote to continuous loop"
  context:
    workload: "<workload class>"
    parameter_already_tuned: "<param>"
    current_value: "<value>"
    found_via: "<bolt recipe / profile evidence>"
    estimated_revisit_cadence: "<weekly | monthly | quarterly | continuous>"
  evidence:
    profile_snapshot: "<URL or path>"
    baseline_metrics:
      p99_ms: <n>
      error_rate: <n>
      cost_per_req: <n>
  requested_outcome: "design a tuning loop that re-tunes <param> as workload evolves"
  open_questions:
    - "<any unknown the source could not resolve>"
```

### Tuner → Dial: `TUNER_TO_DIAL`

```yaml
TUNER_TO_DIAL_HANDOFF:
  reason: "pool/cache/batch size has a dynamic optimum; escalate to ongoing tuning"
  context:
    db_engine: "<postgres | mysql | ...>"
    parameter: "<connection_pool_size | shared_buffers | ...>"
    static_optimum_observed: "<value>"
    workload_variance: "<low | medium | high>"
  boundary_note: "Tuner owns DB-internal trade-off (max_connections, work_mem). Dial owns app-side pool sizing campaign."
  requested_outcome: "design Adaptive Concurrency or BO campaign for pool size at app boundary"
```

### Beacon → Dial: `BEACON_TO_DIAL`

```yaml
BEACON_TO_DIAL_HANDOFF:
  reason: "SLO breach pattern repeating; suspect tunable parameter"
  context:
    slo:
      target_p99_ms: <n>
      target_error_rate: <n>
      monthly_error_budget_pct: <n>
    breach_pattern:
      first_seen: "<YYYY-MM-DD>"
      frequency: "<X breaches / week>"
      shape: "<diurnal | weekly | sustained>"
    suspected_parameter_class: "<gc | pool | cache | batch | autoscaler>"
  evidence:
    alert_log: "<URL>"
    profile_snapshot: "<URL>"
  requested_outcome: "design tuning loop that closes feedback from this SLO signal"
```

### Oracle → Dial: `ORACLE_TO_DIAL`

```yaml
ORACLE_TO_DIAL_HANDOFF:
  reason: "AI serving workload needs runtime tuning loop"
  context:
    workload: "<llm-serving | rag | inference-batch>"
    model_serving_stack: "<vllm-v1 | vllm-legacy | sglang | tensorrt-llm | tgi>"
    stack_specific_anchors:
      vllm:
        runner: "<mrv2 | legacy>"          # MRV2 ≈ +56% TPS on GB200
        spec_decode_method: "<none | ngram | eagle | mtp | medusa>"
        attention_backend: "<fa2 | fa3 | fa4>"
        cpu_kv_offload: <true | false>
      sglang:
        radix_prefix_cache: <true | false>  # ~+29% TPS on H100 if prefix-heavy
      tensorrt_llm:
        engine_rebuild_min: <n>            # 20-30 min typical
    static_config:
      max_num_seqs_or_equiv: <n>
      gpu_memory_utilization: <n>
      kv_cache_block_size: <n>
    observed_pain:
      ttft_p99_ms: <n>
      tps_avg: <n>
      cost_per_1k_tokens: <n>
  boundary_note: "Oracle owns model architecture, training-side hyperparameters, AND the serving-stack choice. Dial owns runtime knobs inside the chosen stack. Switching stacks (vLLM → SGLang etc.) is an Oracle / Horizon decision, not a Dial campaign."
  requested_outcome: "design Pareto BO over (max_num_seqs × max_num_batched_tokens × gpu_memory_util) with TTFT × TPS × $/1k objective; treat spec-decode method and attention backend as categorical sub-campaigns ordered before the continuous search"
```

### Dial → Bolt: `DIAL_TO_BOLT`

```yaml
DIAL_TO_BOLT_HANDOFF:
  reason: "smallest verified delta identified — land the individual change"
  winner:
    parameters:
      <param>: <value>
    expected_impact:
      p99_ms_delta_pct: <n>
      cost_per_req_delta_pct: <n>
    confidence: "<MDE-passed | borderline>"
  guardrail_already_wired:
    slo_budget_pct: <n>
    rollback_trigger: "<expression>"
    kill_switch_flag: "<flag name>"
  canary_plan:
    stages: [1%, 5%, 25%, 100%]
    hold_per_stage: ["30m", "2h", "6h", "indefinite"]
  campaign_artifact: "<URL to campaign YAML>"
```

### Dial → Tuner: `DIAL_TO_TUNER`

```yaml
DIAL_TO_TUNER_HANDOFF:
  reason: "DB-side parameter surfaces in tuning; need DB-internal trade-off analysis"
  context:
    workload: "<workload class>"
    app_side_finding: "<e.g., hikari maxPool above X triggers WAL bloat>"
    db_engine: "<postgres | mysql>"
  question: "<e.g., is shared_buffers / work_mem at current level safe with hikari.max_pool = X across N replicas?>"
  boundary_note: "Dial does not touch DB-internal knobs. Tuner owns EXPLAIN, indexes, DB config."
```

### Dial → Siege: `DIAL_TO_SIEGE`

```yaml
DIAL_TO_SIEGE_HANDOFF:
  reason: "need scaled benchmark to evaluate candidate configuration"
  campaign:
    name: "<campaign-name>"
    artifact: "<URL to YAML>"
  benchmark_spec:
    harness: "<k6 | locust | autocannon | jmh | custom>"
    target_rps: <n>
    duration_per_eval: "240s"
    warmup_per_eval: "60s"
    repeats_per_eval: 3
    workload_fixture: "<URL>"
    resource_isolation: "<dedicated K8s ns | bare metal>"
  return:
    per_eval_metrics:
      - p99_ms
      - error_rate
      - throughput_rps
      - cost_per_req
    format: "<JSON Lines | CSV>"
```

### Dial → Gear: `DIAL_TO_GEAR`

```yaml
DIAL_TO_GEAR_HANDOFF:
  reason: "winner approved — land configuration in build / runtime config"
  config_delta:
    file: "<helm/values.yaml | dockerfile | env>"
    before: "<...>"
    after: "<...>"
  rollout_method: "<rolling | blue-green | canary feature-flag>"
  rollback_path: "<git revert / feature-flag flip / helm rollback>"
  observability:
    new_metric_keys: ["<...>"]
    new_alert_rules: ["<...>"]
```

### Dial → Beacon: `DIAL_TO_BEACON`

```yaml
DIAL_TO_BEACON_HANDOFF:
  reason: "campaign needs instrumentation: objective metric + guardrail SLO + drift detector"
  metrics_to_emit:
    - name: "dial.checkout.p99_ms"
      type: histogram
      unit: ms
    - name: "dial.checkout.cost_per_req_usd"
      type: gauge
  slo_to_define:
    target_p99_ms: <n>
    error_budget_pct_monthly: <n>
  guardrail_alert:
    expression: "p99_ms > 2 * baseline for 60s"
    notify: "<pagerduty service>"
  drift_alert:
    kl_divergence_ge: 0.10
    notify: "<email / slack>"
```

### Dial → Canvas: `DIAL_TO_CANVAS`

```yaml
DIAL_TO_CANVAS_HANDOFF:
  reason: "visualize Pareto front / search trajectory / campaign timeline for stakeholder review"
  inputs:
    optuna_study: "<URL>"
    pareto_points: "<JSON>"
    baseline_point: "<x, y, z>"
  diagrams_requested:
    - type: pareto_2d
      axes: ["p99_ms", "cost_per_req"]
    - type: timeline
      events: ["campaign_start", "convergence", "canary_1%", "canary_100%"]
    - type: parameter_importance
      source: "optuna.importance"
```

### Dial → Builder: `DIAL_TO_BUILDER`

```yaml
DIAL_TO_BUILDER_HANDOFF:
  reason: "campaign-as-code artifact needs to become a runnable harness in the repo"
  artifact: "<URL to campaign YAML>"
  target_repo: "<path>"
  required_modules:
    - "optuna study runner"
    - "config renderer (YAML -> deploy)"
    - "evaluator stub (calls Siege harness)"
    - "guardrail watcher (subscribes Beacon)"
  acceptance:
    - "campaign reproducible from artifact + seed"
    - "guardrail integration tested with synthetic SLO breach"
    - "kill switch tested via feature flag"
```

---

## Cross-Agent Campaign Flow

A typical end-to-end Dial campaign exercises 5–7 agents.

```
[User / Beacon / Bolt / Tuner / Oracle] → Dial
                                            │
                              ┌── SCAN ──── │ → reads profile from Beacon / APM
                              │
                              ├── FRAME ─── │ → objective + guardrail with Beacon SLO context
                              │
                              ├── DESIGN ── │ → parameter space, algorithm, budget
                              │
                              ├── EVALUATE  │ → DIAL_TO_SIEGE (benchmark) per eval
                              │             │ → guardrail watch via Beacon
                              │
                              ├── LAND ──── │ → DIAL_TO_BOLT (impl) → canary
                              │             │ → DIAL_TO_GEAR (config land)
                              │             │ → DIAL_TO_BEACON (alerts live)
                              │
                              └── MONITOR ──│ → drift detector watches Beacon
                                            │ → re-tune triggers re-entry to SCAN

Visualization handoff (optional, any phase): DIAL_TO_CANVAS for Pareto / trajectory.
Stakeholder review handoff (optional, post LAND): handoff to Scribe for write-up.
```

---

## Boundary Recap

| vs | Dial owns | They own |
|----|-----------|----------|
| **Bolt** | Continuous loop design | Individual one-shot optimization implementation |
| **Tuner** | App-side pool/cache/batch sizing loop | DB-internal: query plans, indexes, EXPLAIN, SQL rewriting, shared_buffers, work_mem |
| **Siege** | Benchmark as evaluator inside campaign | Load test design, chaos, contract test, resilience |
| **Beacon** | Tuning objective metric + guardrail SLO | Production monitoring, alerting infra, dashboards |
| **Oracle** | Runtime/serving knobs for AI | Model architecture, training hyperparameters, evals |
| **Atlas** | Tuning-only when refactor is overkill | Architectural decomposition, dependency restructuring |
| **Gear** | Tuned-config spec | Build pipeline, deploy mechanics, IaC |
| **Horizon** | Tuning ladder for legacy params | Library/framework migration without a tuning loop |
| **Builder** | Campaign artifact (YAML/Python) | Production-grade implementation of the harness |
| **Guardian** | Guardrail spec | PR / commit policy on the config delta |
| **Launch** | Rollout plan input | Feature-flag release coordination |

---

## Failure-Mode Routing

| Symptom in Dial output | Route to |
|------------------------|----------|
| Cannot identify hot path | back to SCAN → Beacon (instrument profiling) |
| Noise floor too high to detect MDE | Beacon (better metric resolution) or accept parameter not tunable |
| Synthetic benchmark inverts production result | Siege (refresh fixture) + back to SCAN |
| Winner regresses post-canary | revert via kill switch; root-cause via Scout; if dependency drift, Trail |
| Workload shape changed mid-campaign | abort campaign; re-enter SCAN after stabilization |
| DB-internal contention surfaces | Tuner |
| Architectural ceiling (cannot tune past it) | Atlas |
| Library is the bottleneck, not the parameter | Horizon |
| Implementation defect surfaces | Builder + Scout |
| Cost objective dominates | Ledger (cost analysis) co-design |
