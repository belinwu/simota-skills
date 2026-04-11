# Guardrail Protocol

Guardrail definitions and configuration for autonomous execution. Execution flow and recovery logic are defined in `AUTORUN.md`.

---

## Guardrail Levels

| Level | Name | Behavior | Use Case |
|-------|------|----------|----------|
| L1 | MONITORING | Log only, no pause | Lint warnings, minor deprecations, coverage drop < 5% |
| L2 | CHECKPOINT | Auto-verify, attempt auto-fix | Test failures < 20%, type errors, low/medium CVEs |
| L3 | PAUSE | Pause branch; auto-recover or escalate | Test failures > 50%, breaking changes, build failures, merge conflicts |
| L4 | ABORT | Immediate stop and rollback | Critical security, data integrity risk, user abort |

---

## Triggers by Level

### L1 — MONITORING

| Trigger | Action |
|---------|--------|
| `lint_warning` | Log, continue |
| `minor_deprecation` | Log, continue |
| `style_inconsistency` | Log, auto-fix if possible |
| `coverage_decrease_minor` (< 5%) | Log, continue |

### L2 — CHECKPOINT

| Trigger | Action |
|---------|--------|
| `test_failure_minor` (< 20%) | Auto-fix attempt → retest (max 3) |
| `security_warning` (non-critical) | Add Sentinel scan |
| `type_error` | Auto-fix attempt (max 2) |
| `performance_regression` (< 10%) | Log, optional Bolt |
| `dependency_vulnerability` (Low/Medium) | Log, suggest update |

### L3 — PAUSE

| Trigger | Action |
|---------|--------|
| `test_failure_major` (> 50%) | Rollback, re-decompose with Sherpa |
| `breaking_change` | Pause, verify consumers (Ripple) |
| `security_critical` (High) | Pause, require Sentinel |
| `merge_conflict` | Pause, resolve or escalate |
| `build_failure` | Rollback, fix attempt (max 2) |

### L4 — ABORT

| Trigger | Action |
|---------|--------|
| `critical_security` | Abort, rollback |
| `data_integrity_risk` | Abort, rollback |
| `infinite_loop_detected` | Abort |
| `user_abort` | Abort |

---

## Configuration by Task Type

| Task Type | Default Level | Pre-checks | Post-checks | Escalate On |
|-----------|--------------|------------|-------------|-------------|
| FEATURE | L2 | — | tests_pass, build_success | test_failure > 50%, security_critical |
| SECURITY | L2 | sentinel_scan | no_new_vulnerabilities, tests_pass | any_security_issue |
| REFACTOR | L2 | — | tests_unchanged, no_behavior_change | test_failure_any |
| API_BREAKING | L3 | ripple_impact_analysis | consumers_updated, migration_ready | consumer_not_updated |
| INCIDENT | L3 | — | service_restored, no_regression | service_not_restored |
| INFRA | L3 | dry_run_if_available | health_checks_pass | health_check_fail |

---

## Mandatory Checkpoints

| Checkpoint | Phase | Level | Check |
|------------|-------|-------|-------|
| POST_IMPLEMENT | After implementation | L2 | Tests pass, types valid |
| PRE_MERGE | Before aggregate | L2 | No conflicts |
| POST_MERGE | After aggregate | L2 | Combined tests pass |
| PRE_DELIVER | Before delivery | L2 | All acceptance criteria met |

---

## Escalation Path

```
L1 (Log) → issue persists → L2 (Checkpoint)
  ├─ auto-recovery success → CONTINUE
  └─ recovery failed → L3 (Pause)
      ├─ auto-recovery success → CONTINUE
      ├─ user confirms → CONTINUE/ADJUST
      └─ critical or no resolution → L4 (Abort) → ROLLBACK + STOP
```

---

## Parallel Execution Guardrails

- Each branch has **independent** L1/L2 guardrails
- L3 pauses **only the affected branch**
- L4 triggers **global abort** across all branches

See `PARALLEL.md` for branch-level guardrail details.

---

## Integration

- **Execution flow and recovery:** `AUTORUN.md`
- **Parallel branches:** `PARALLEL.md`
- **Harness evolution:** `HARNESS_EVOLUTION.md` (HE-01 tracks L2+ trigger frequency for simplification)
- **Reverse feedback:** High-priority feedback triggers L2; systemic issues (3+) trigger L3
