# Profiling & Instrumentation

**Purpose:** Design guidance for the measurement substrate used in the SCAN phase. No tuning starts without a profile.
**Read when:** Capturing a baseline profile, choosing metrics, detecting hot paths, or measuring the noise floor.

## Contents
- Three Pillars (Metrics / Traces / Profiles)
- Continuous Profiling Stacks
- Hot-Path Detection
- RED / USE / Four Golden Signals
- Trace Sampling Strategy
- Noise Floor Measurement
- Baseline Capture Checklist
- Instrumentation Anti-Patterns

---

## Three Pillars

| Pillar | What it answers | Tools | Use for Dial |
|--------|-----------------|-------|--------------|
| **Metrics** | "How many / how slow / how often" | Prometheus, OpenTelemetry Metrics, Datadog | Objective function inputs, SLO baselines, guardrail thresholds |
| **Traces** | "Where did this request spend its time" | OpenTelemetry Traces, Jaeger, Tempo, Honeycomb, Datadog APM | Hot-path detection, span-level latency breakdown |
| **Profiles** | "Which code consumed CPU / RAM / lock time" | Pyroscope, Parca, OpenTelemetry Profiles, async-profiler, py-spy, perf | Hot-path attribution, regression diff, GC / lock / I/O cost share |

**Dial assumption**: All three pillars feed candidate generation and evaluation. If any pillar is missing, hand off to Beacon to instrument before tuning begins.

---

## Continuous Profiling Stacks

Continuous profiling is the third performance signal beside metrics and traces. It answers "did this code path get more expensive this week?" as a queryable diff, not a hypothesis.

| Stack | Strengths | Notes |
|-------|-----------|-------|
| **Pyroscope 2.0 (Grafana)** | Rearchitected (April 2026): write-once object storage, stateless read path, ~95% symbol-storage reduction in Grafana's prod; rollouts that took 8–12h in v1 now finish in minutes | Default open-source choice. [Source: Grafana Labs - Pyroscope 2.0 release](https://grafana.com/blog/pyroscope-2-0-release/) |
| **Parca (CNCF, incubating)** | eBPF-native, zero-instrumentation for compiled languages, Polar Signals managed offering | Strong for Go/C/C++/Rust |
| **OpenTelemetry Profiles (signal)** | Public **Alpha since March 2026**, **RC in Q1 2026 per project plan, targeting GA in Q3 2026**; OTLP Profiles is round-trip with pprof; Collector ships pprof receiver + k8sattributesprocessor | Adopt for vendor neutrality once your collector + backend pair both support the signal; until then keep Pyroscope/Parca as the source of truth. [Source: OpenTelemetry blog - Profiles Alpha](https://opentelemetry.io/blog/2026/profiles-alpha/) |
| **Datadog Continuous Profiler** | Managed, integrated with APM, language SDK | Default if Datadog APM is already in place |
| **async-profiler (JVM)** | Low-overhead sampling, allocation profiling, lock profiling, wall-clock profiling | Use directly for JVM workloads |
| **py-spy / Pyroscope-py** | Python sampling profiler with no GIL contention | Use for Python workloads |
| **Linux perf / bpftrace** | Kernel-level, syscalls, scheduler, page-fault profiling | Use when bottleneck is below userspace |

**Rule of thumb**: Adopt continuous profiling _before_ any tuning campaign. A single-shot profile lies about steady-state; the diff over time tells the truth.

---

## Hot-Path Detection

A parameter is a tuning candidate only if it is on the hot path.

| Signal | Threshold | Meaning |
|--------|-----------|---------|
| CPU profile share | `≥ 5%` of total CPU samples | tunable candidate |
| Allocation profile share | `≥ 10%` of total alloc bytes | GC / heap-size candidate |
| Lock contention share | `≥ 5%` of total lock time | concurrency-parameter candidate |
| Span latency contribution | `≥ 10%` of p99 request latency | request-path knob candidate |
| Wait time (queue/IO) share | `≥ 5%` of total wall time | pool / batch candidate |
| GC pause cumulative | `≥ SLO_p99 / 4` | GC tuning candidate |

If a proposed parameter does not meet the threshold for its category, **route back to SCAN** with the missing evidence — do not enter FRAME.

---

## RED / USE / Four Golden Signals

Pick the right framework for the workload class.

| Framework | Signals | Workload class |
|-----------|---------|----------------|
| **RED** | Rate, Errors, Duration | Request-driven services (HTTP, RPC) |
| **USE** | Utilization, Saturation, Errors | Resources (CPU, memory, disk, network, pool) |
| **Four Golden Signals** (Google SRE) | Latency, Traffic, Errors, Saturation | General-purpose service |

**Dial mapping**:
- RED → objective function inputs (p99 latency, error rate, RPS).
- USE → saturation guardrails (pool / threadpool / CPU at risk of starvation).
- Four Golden Signals → minimum baseline before any campaign starts.

---

## Trace Sampling Strategy

Sampling affects what the optimizer can see. Wrong sampling produces invisible regressions.

| Strategy | When | Risk |
|----------|------|------|
| Head-based fixed % (e.g., 1%) | High volume, cost-sensitive | Misses rare slow requests; biased for tuning |
| Tail-based (error / slow capture) | Need every slow / failed request | Higher cost; richer signal for Dial |
| Probabilistic with stratification | Mixed traffic, want representative sample | Hard to set up correctly |
| 100% sampling on canary slice | Evaluating a candidate config under canary | Best for Dial canary stage |

**Dial rule**: Canary slices are always 100% sampled. Without it, you cannot statistically distinguish the candidate from the baseline at user-visible thresholds.

---

## Noise Floor Measurement

Noise floor is the spread of the objective metric under unchanged configuration. Without measuring it, you will chase noise.

### Protocol

1. Run the workload at steady state, configuration locked, for `N` independent windows (e.g., 30 × 1-minute windows).
2. Record the objective metric (p99 latency, $/req, throughput) per window.
3. Compute mean μ and standard deviation σ.
4. **Noise floor σ** = the value below which differences are indistinguishable from random variation.

### Application

| Decision | Rule |
|----------|------|
| Target effect | must be `≥ 3 × σ` to be detectable in a short campaign |
| Sample size per arm | `n ≥ 30` evaluations OR `n ≥ (3σ/MDE)²` whichever is larger |
| MDE | `≥ 2 × σ` for short campaigns; `≥ 1 × σ` only with `n ≥ 100` |

If the candidate's expected effect is smaller than 2σ, **do not start the campaign**. Either (a) increase sample window to shrink σ_mean, (b) pick a higher-leverage parameter, or (c) accept the parameter is not worth tuning.

---

## Baseline Capture Checklist

Before FRAME, capture and freeze:

- [ ] **Workload profile**: traffic shape (req/s by route), payload-size distribution, time-of-day curve, weekday vs weekend
- [ ] **SLO**: p50 / p95 / p99 latency, error rate, availability target, error budget
- [ ] **Current configuration**: every parameter you will consider, plus adjacent parameters
- [ ] **Profile snapshot**: CPU, alloc, lock, wall-clock flamegraphs
- [ ] **Trace sample**: representative slow request, representative median request
- [ ] **Noise floor**: σ per objective metric
- [ ] **Recent incidents**: last 30 days of SLO-related incidents (informs guardrails)
- [ ] **Dependency state**: upstream/downstream latency baselines (Dial must not optimize a parameter masked by an upstream change)

Output: `dial-baseline-{workload}-{YYYYMMDD}.yaml` (versioned input to the campaign artifact).

---

## Instrumentation Anti-Patterns

| Anti-pattern | Why it bites | Fix |
|--------------|--------------|-----|
| Optimizing on dev profile | Dev workload ≠ production shape; rankings invert | Run profile on staging shadow or production canary |
| Single 1-minute profile capture | Captures GC / cache transient; lies about steady state | Use continuous profiling over `≥ 1` hour |
| Ignoring upstream / downstream | A pool tune that "improves" latency is masking an upstream slowdown | Capture full dependency baseline |
| Mixing pre/post versions in profile diff | Two changes confused | Pin app version per profile window |
| Sampling that drops the tail | p99 invisible, optimizer flies blind | Tail-based sampling or 100% on canary |
| No σ measurement | Every "win" is plausibly noise | Mandatory σ before FRAME |

---

## Handoff into FRAME

When SCAN exits, emit:

```yaml
SCAN_OUTPUT:
  workload_class: "[web | batch | streaming | ml-serving]"
  baseline:
    p50_ms: <n>
    p95_ms: <n>
    p99_ms: <n>
    error_rate: <fraction>
    throughput_rps: <n>
    cost_per_req: <currency>
  hot_path_candidates:
    - parameter: "[name]"
      cost_share: <pct>
      evidence: "[profile node or span name]"
  noise_floor:
    metric: "[objective metric]"
    sigma: <n>
    mde_recommended: <n>
  slo:
    p99_target_ms: <n>
    error_budget_pct_monthly: <n>
  current_config:
    <param>: <value>
  dependencies_stable: <true | false>
```

FRAME then takes this as input. If `dependencies_stable: false`, **do not enter FRAME** — investigate upstream first.
