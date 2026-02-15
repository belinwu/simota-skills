# Siege Interaction Triggers

質問テンプレート集（AskUserQuestion 形式）。

---

## ON_LOAD_TARGET

```yaml
trigger: ON_LOAD_TARGET
condition: "Load test target or SLO not specified"
question: "What load should we validate against?"
options:
  - label: "Current production traffic (baseline)"
    description: "Match current peak traffic patterns from monitoring data"
  - label: "2× current peak"
    description: "Standard safety margin for growth and spikes"
  - label: "Specific RPS target"
    description: "You specify exact requests per second and duration"
  - label: "Find the breaking point"
    description: "Stress test to discover maximum capacity"
```

---

## ON_CHAOS_SCOPE

```yaml
trigger: ON_CHAOS_SCOPE
condition: "Chaos experiment scope not defined"
question: "What blast radius should the chaos experiment have?"
options:
  - label: "Single pod/instance"
    description: "Lowest risk — kill or degrade one instance"
  - label: "Single service dependency"
    description: "Block or slow one downstream service"
  - label: "Availability zone"
    description: "Simulate full zone failure"
  - label: "Custom scenario"
    description: "You describe the specific failure to inject"
```

---

## ON_PRODUCTION_TEST

```yaml
trigger: ON_PRODUCTION_TEST
condition: "Test targets production or production-like environment"
question: "This test may affect production traffic. How should we proceed?"
options:
  - label: "Staging only"
    description: "Run all tests against staging environment"
  - label: "Production canary segment"
    description: "Limit to canary traffic (< 5% of users)"
  - label: "Production with safety controls"
    description: "Full production with kill switch and abort criteria"
  - label: "Shadow mode"
    description: "Mirror production traffic to test environment"
```

---

## ON_MUTATION_CI

```yaml
trigger: ON_MUTATION_CI
condition: "Mutation testing CI integration requested"
question: "How should mutation testing run in CI?"
options:
  - label: "Changed files only (incremental)"
    description: "Fast — only mutate files changed in the PR"
  - label: "Critical paths only"
    description: "Mutate only business-critical modules"
  - label: "Full suite (nightly)"
    description: "Complete mutation run as nightly job"
  - label: "Threshold gate"
    description: "Block PR if mutation score drops below threshold"
```

---

## ON_CONTRACT_BREAKING

```yaml
trigger: ON_CONTRACT_BREAKING
condition: "Potentially breaking API/event contract change detected"
question: "A potentially breaking contract change was detected. How should we proceed?"
options:
  - label: "Run can-i-deploy check"
    description: "Verify all consumers are compatible with the change"
  - label: "Version the endpoint"
    description: "Create new version, deprecate old one"
  - label: "Coordinate with consumers first"
    description: "Notify and align with consumer teams before change"
  - label: "Add backwards compatibility"
    description: "Make the change non-breaking with default values"
```

---

## ON_RESILIENCE_PATTERN

```yaml
trigger: ON_RESILIENCE_PATTERN
condition: "Resilience pattern needed but type not specified"
question: "What resilience pattern should we verify?"
options:
  - label: "Circuit breaker"
    description: "Dependency failure isolation and recovery"
  - label: "Retry with backoff"
    description: "Transient error recovery with exponential backoff"
  - label: "Bulkhead isolation"
    description: "Resource isolation between workloads"
  - label: "Full resilience stack"
    description: "Circuit breaker + retry + timeout + fallback"
```
