# Investigation Escalation Protocol

Escalation standard across the investigation skill cluster (Scout, Lens, Rewind, Specter).

## Escalation Flow

```
[Vague Report / Unknown Issue]
    │
    ▼
  Lens (SCOPE→SURVEY) ─── comprehension sufficient ─── DONE
    │
    ▼ anomaly pattern / potential bug found
  Scout (TRIAGE→TRACE) ─── bug identified ─── Builder handoff
    │                         │
    │ history investigation    │ concurrency suspected
    │ needed                   │
    ▼                         ▼
  Rewind (bisect/archaeology)  Specter (SCAN→ANALYZE→SCORE)
    │                         │
    ▼ resource-related        ▼ onset timing needed
      change found
    └───→ Specter             └───→ Rewind
```

## Ownership Rule

One bug = one leader skill. Others serve as support roles. The leader is the skill that first completes TRIAGE/SCOPE.

## Unified Confidence Scale

| Level | Score | Evidence Threshold | Reporting Rule |
|-------|-------|--------------------|----------------|
| `HIGH` | ≥ 0.8 | 3+ independent evidence | Report as confirmed |
| `MEDIUM` | 0.5–0.79 | 2 independent evidence | Report as estimated; add verification steps |
| `LOW` | < 0.5 | ≤1 evidence | Report as hypothesis; list missing information |

## Cross-Cluster Handoff Formats

### LENS_TO_SCOUT_HANDOFF

```yaml
LENS_TO_SCOUT_HANDOFF:
  investigation_id: "[unique-id]"
  discovery_type: "[anomaly_pattern | potential_bug | dead_code_risk | comprehension_debt_hotspot]"
  location: "[file:line references]"
  evidence: "[what was observed during comprehension]"
  severity_estimate: "[HIGH | MEDIUM | LOW]"
  suggested_investigation_mode: "[Focused Hunt | History-Led | Observability-Led | Multi-Engine | Cascading Failure]"
```

### SCOUT_TO_LENS_HANDOFF

```yaml
SCOUT_TO_LENS_HANDOFF:
  investigation_id: "[unique-id]"
  request_type: "[context_needed | flow_trace_needed | dependency_map_needed]"
  bug_context: "[what is known so far]"
  specific_questions: "[what Scout needs to understand]"
  scope_hint: "[files/modules to focus on]"
```

### REWIND_TO_SPECTER_HANDOFF

```yaml
REWIND_TO_SPECTER_HANDOFF:
  investigation_id: "[unique-id]"
  bisect_result: "[commit hash and change summary]"
  change_type: "[resource_management | concurrency_modification | lock_change | async_pattern_change]"
  evidence: "[what the commit changed]"
  suggested_scan_focus: "[race_condition | memory_leak | resource_leak | deadlock]"
```

### SPECTER_TO_REWIND_HANDOFF

```yaml
SPECTER_TO_REWIND_HANDOFF:
  investigation_id: "[unique-id]"
  issue_type: "[race_condition | memory_leak | resource_leak | deadlock]"
  request: "[onset_identification | change_history | blame_analysis]"
  suspected_components: "[files/modules]"
  evidence: "[current analysis findings]"
```

## Stall Protocol (Cross-Cluster)

1. 3 probes without progress → switch hypothesis
2. All hypotheses exhausted → escalate to adjacent skill
3. 3+ round-trips between 2 skills → promote to Nexus (prevent Agent Tennis)

## Duplicate Investigation Prevention

- Do not start parallel investigations on the same bug across multiple skills
- Pass the Investigation_ID on escalation to prevent duplication
- The leader skill aggregates all escalation results and integrates them into the final report
