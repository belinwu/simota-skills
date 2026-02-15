# Siege Handoff Formats

Bolt/Triage/Radar/Builder へのハンドオフテンプレート。

---

## Siege → Bolt (Performance Fix)

```markdown
## Performance Issue from Load Test

### Source
- **Test type**: [load/stress/soak]
- **Tool**: [k6/Locust/Artillery]
- **Results**: [link to test report]

### Bottleneck Identified
- **Component**: [service/endpoint/query]
- **Metric**: [latency/throughput/error rate]
- **At load**: [RPS/VU when issue appears]
- **Current**: [measured value]
- **Target SLO**: [required value]

### Evidence
```
[Relevant metrics/logs/traces]
```

### Recommended Actions
1. [Specific optimization suggestion]
2. [Alternative approach]

### Validation Criteria
- [ ] Metric meets target at [X] RPS
- [ ] No regression in other endpoints
- [ ] Load test rerun passes SLO thresholds
```

---

## Siege → Triage (Incident from Chaos)

```markdown
## Issue Discovered During Chaos Experiment

### Experiment
- **Scenario**: [failure injected]
- **Hypothesis**: [expected behavior]
- **Actual**: [what happened]

### Impact
- **User impact**: [description]
- **Duration**: [how long until recovery]
- **Blast radius**: [affected services/users]

### Root Cause Analysis
- **Missing resilience**: [circuit breaker/retry/fallback]
- **Monitoring gap**: [what wasn't detected]
- **Recovery gap**: [why recovery was slow]

### Immediate Actions
1. [Quick fix for the gap]

### Long-term Actions
1. [Resilience pattern to implement]
2. [Monitoring to add]
3. [Runbook to create/update]
```

---

## Siege → Radar (Test Gap from Mutations)

```markdown
## Test Gaps from Mutation Testing

### Summary
- **Mutation score**: [X]% (target: [Y]%)
- **Survived mutants**: [N]
- **Files affected**: [list]

### Top Surviving Mutants
| File | Line | Mutation | Type | Priority |
|------|------|----------|------|----------|
| [file] | [line] | [description] | [boundary/conditional/etc] | [P1/P2/P3] |

### Recommended Tests
1. **[File:Line]** — Add [boundary/negative/assertion] test for [description]
2. **[File:Line]** — Strengthen assertion in existing test [test name]

### Dead Code Candidates
- [File:Line] — Unreachable code, consider removal
```

---

## Siege → Builder (Resilience Implementation)

```markdown
## Resilience Pattern Implementation Request

### Context
- **Service**: [name]
- **Dependency**: [downstream service]
- **Failure scenario**: [what was tested]
- **Current behavior**: [what happens now]
- **Desired behavior**: [what should happen]

### Pattern Specification
- **Pattern**: [circuit breaker/retry/bulkhead/fallback]
- **Configuration**:
  - [parameter]: [value]
  - [parameter]: [value]

### Fallback Behavior
- [What to return when dependency is unavailable]
- [Degraded mode description]

### Acceptance Criteria
- [ ] Pattern implemented with specified configuration
- [ ] Metrics exposed (state, counts, latency)
- [ ] Unit tests for pattern behavior
- [ ] Chaos test validates resilience improvement
```

---

## Gateway → Siege (Contract Test Request)

```markdown
## Input: Contract Test Request

### API Change
- **Service**: [provider service]
- **Consumers**: [list of consuming services]
- **Change type**: [new endpoint/modified schema/deprecated field]
- **Breaking**: [yes/no/unknown]

### Contract Scope
- **Endpoints**: [list]
- **Events**: [list of async events]

### Requested Tests
- [ ] Consumer-driven contract for [consumer] → [provider]
- [ ] Event contract for [event name]
- [ ] Breaking change verification
```
