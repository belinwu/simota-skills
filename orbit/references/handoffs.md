# Orbit Handoff Templates

## NEXUS_TO_ORBIT_HANDOFF

```yaml
NEXUS_TO_ORBIT_HANDOFF:
  task_type: LOOP_OPS
  objective: "stabilize loop operation contract"
  artifacts:
    goal_file: "<path>"
    progress_file: "<path>"
    done_file: "<path|optional>"
    state_file: "<path>"
    runner_log: "<path|optional>"
  constraints:
    - "no destructive reset"
    - "preserve baseline dirty files"
  expected_output:
    - "contract diagnosis"
    - "safe next action"
```

### Input Validation Rules

```yaml
NEXUS_TO_ORBIT_VALIDATION:
  required_fields:
    task_type:
      type: string
      allowed_values: [LOOP_OPS]
      on_invalid: REJECT
      reason: "Orbit only handles LOOP_OPS tasks — route non-loop tasks to appropriate agent"
    objective:
      type: string
      min_length: 10
      on_invalid: REJECT
      reason: "Objective too vague to derive contract — request clarification from Nexus"
    artifacts.goal_file:
      type: path
      must_exist: false  # bootstrap flow creates it
      on_missing: CONTRACT_MISSING
      action: "Trigger Script Generation pipeline (bootstrap mode)"
    artifacts.progress_file:
      type: path
      must_exist: false
      on_missing: CONTRACT_MISSING
      action: "Initialize empty progress.md with iteration 0 entry"
    artifacts.state_file:
      type: path
      must_exist: false
      on_missing: CONTRACT_MISSING
      action: "Create state.env with NEXT_ITERATION=1, LAST_STATUS=READY"

  optional_fields:
    artifacts.done_file:
      type: path
      on_present: "Include in DONE verification gate"
      on_missing: "Normal — DONE not yet claimed"
    artifacts.runner_log:
      type: path
      on_present: "Parse for failure taxonomy classification"
      on_missing: "Skip log-based analysis"
    constraints:
      type: array
      default: ["no destructive reset", "preserve baseline dirty files"]
      on_missing: "Apply defaults"
    expected_output:
      type: array
      default: ["contract diagnosis", "safe next action"]
      on_missing: "Apply defaults"

  validation_flow:
    1: "Check task_type == LOOP_OPS → REJECT if not"
    2: "Check objective length >= 10 → REJECT if too short"
    3: "Check required artifact paths → classify missing as CONTRACT_MISSING"
    4: "Apply optional field defaults for any missing optional fields"
    5: "Proceed to Daily Process Step 1 (Intake)"
```

## ORBIT_TO_NEXUS_HANDOFF

```yaml
ORBIT_TO_NEXUS_HANDOFF:
  summary: "<1-3 lines>"
  status_assessment: "CONTRACT_MISSING|STATE_DRIFT|VERIFY_GAP|COMMIT_SCOPE_RISK|TOOL_FAILURE"
  decisions:
    - "<decision 1>"
    - "<decision 2>"
  artifacts:
    - "<path:line>"
  next_action: "CONTINUE|VERIFY|DONE"
  suggested_next_agent: "Builder|Guardian|Radar|NONE"
```

## ORBIT_TO_BUILDER_HANDOFF

```yaml
ORBIT_TO_BUILDER_HANDOFF:
  failure_class: "<taxonomy class>"
  target_files:
    - "<file1>"
    - "<file2>"
  constraints:
    - "maintain status footer format"
    - "no schema-destructive change"
  acceptance:
    - "progress entry includes verification result"
```

## ORBIT_TO_GUARDIAN_HANDOFF

```yaml
ORBIT_TO_GUARDIAN_HANDOFF:
  concern: "commit scope safety"
  baseline_source: "<state dir>/dirty-start-paths.txt"
  candidate_scope:
    - "<path1>"
    - "<path2>"
  policy:
    - "stage candidate-only"
    - "no baseline path commit"
```

## SCOUT_TO_ORBIT_HANDOFF

```yaml
SCOUT_TO_ORBIT_HANDOFF:
  source_agent: Scout
  incident_type: "loop_anomaly|state_corruption|silent_failure"
  findings:
    root_cause: "<RCA summary>"
    affected_artifacts:
      - "<file:line>"
    evidence:
      - "<log excerpt or diff reference>"
  orbit_action_requested:
    - "contract_audit"
    - "state_recovery"
    - "failure_classification"
  constraints:
    - "do not discard Scout's evidence chain"
    - "preserve investigation context in progress.md"
  expected_output:
    - "failure taxonomy classification"
    - "contract repair plan or safe next action"
    - "handoff to Builder/Guardian if implementation needed"
```

## ORBIT_TO_RADAR_HANDOFF

```yaml
ORBIT_TO_RADAR_HANDOFF:
  concern: "DONE verification gap closure"
  done_file: "<path>"
  acceptance_criteria:
    - "<criterion 1>"
    - "<criterion 2>"
  missing_evidence:
    - verification: "<verify_cmd that was not run or failed>"
      expected: "<expected outcome>"
    - verification: "<another missing check>"
      expected: "<expected outcome>"
  constraints:
    - "run all missing verifications before confirming DONE"
    - "report pass/fail per criterion — do not aggregate"
    - "if any criterion fails, recommend CONTINUE (not DONE)"
  expected_output:
    - "per-criterion verification results"
    - "DONE confirmation or CONTINUE recommendation with evidence"
```

## ORBIT_TO_SCOUT_HANDOFF

```yaml
ORBIT_TO_SCOUT_HANDOFF:
  target_agent: Scout
  task_type: LOOP_INVESTIGATION
  trigger_reason: "loop_anomaly_unresolved|persistent_tool_failure|unexplained_state_corruption"
  context:
    loop_dir: "<path>"
    failure_class: "CONTRACT_MISSING|STATE_DRIFT|VERIFY_GAP|COMMIT_SCOPE_RISK|TOOL_FAILURE"
    severity: "P0|P1|P2"
    orbit_analysis_summary: "<Orbit's initial analysis summary (1-3 lines)>"
  investigation_request:
    type: "root_cause_analysis|artifact_forensics|runner_log_audit"
    questions:
      - "<specific question to investigate 1>"
      - "<specific question to investigate 2>"
    artifacts_to_examine:
      - "<file:line>"
    evidence_chain:
      - "<evidence already confirmed by Orbit>"
  constraints:
    - "preserve all original artifacts — no modification"
    - "return findings as SCOUT_TO_ORBIT_HANDOFF with evidence chain intact"
  expected_output:
    - "root cause classification"
    - "reproduction steps or trigger conditions"
    - "recommended contract repair or recovery action"
```

### ORBIT_TO_SCOUT_HANDOFF Trigger Conditions

| Trigger | Condition | Question for Scout |
|---------|-----------|-------------------|
| TOOL_FAILURE 3× consecutive | retry exhausted + environment check inconclusive | Identify failure pattern from `runner.log` |
| STATE_DRIFT recurrence | drift reappears after `recover.sh` | Forensics on what is overwriting state.env |
| VERIFY_GAP persistent | verify.sh fails every iteration, cause unknown | Investigate environment dependency of verify command |

---

## Handoff Transformation Lifecycle Examples

### Example 1: Standard Flow (Nexus → Orbit → Nexus → Builder)

**Scenario:** Loop iteration 12 shows `state.env` NEXT_ITERATION=14 but `progress.md` only has entries up to iteration 11. STATE_DRIFT detected.

**Step 1: NEXUS_TO_ORBIT_HANDOFF (received)**

```yaml
NEXUS_TO_ORBIT_HANDOFF:
  task_type: LOOP_OPS
  objective: "diagnose iteration counter mismatch in api-refactor loop"
  artifacts:
    goal_file: ".nexus-loop/goal.md"
    progress_file: ".nexus-loop/progress.md"
    done_file: null
    state_file: ".nexus-loop/state.env"
    runner_log: ".nexus-loop/runner.log"
  constraints:
    - "no destructive reset"
    - "preserve baseline dirty files"
  expected_output:
    - "contract diagnosis"
    - "safe next action"
```

**Step 2: Orbit Processing**
1. Intake: Classify as **Audit** (existing loop with suspected issues)
2. Contract Check: **Partial** — state.env and progress.md disagree
3. Risk Classification: **STATE_DRIFT / P1** — resume corruption risk
4. Evidence: `state.env:NEXT_ITERATION=14`, `progress.md:last_entry=iteration 11`, gap of 2 iterations unrecorded

**Step 3: ORBIT_TO_NEXUS_HANDOFF (emitted)**

```yaml
ORBIT_TO_NEXUS_HANDOFF:
  summary: "STATE_DRIFT detected — state.env skipped 2 iterations ahead of progress.md evidence"
  status_assessment: STATE_DRIFT
  decisions:
    - "Reset NEXT_ITERATION to 12 (progress.md last + 1)"
    - "Preserve runner.log for post-recovery analysis"
  artifacts:
    - ".nexus-loop/state.env:1 (NEXT_ITERATION=14, expected 12)"
    - ".nexus-loop/progress.md:last_entry (iteration 11)"
  next_action: CONTINUE
  suggested_next_agent: Builder
```

**Step 4: ORBIT_TO_BUILDER_HANDOFF (emitted — chained)**

```yaml
ORBIT_TO_BUILDER_HANDOFF:
  failure_class: STATE_DRIFT
  target_files:
    - ".nexus-loop/state.env"
    - ".nexus-loop/progress.md"
  constraints:
    - "maintain status footer format"
    - "do not discard runner.log entries for iterations 12-13"
  acceptance:
    - "state.env NEXT_ITERATION matches progress.md last entry + 1"
    - "progress.md includes recovery note for gap"
```

### Example 2: Scout-Originated Flow (Scout → Orbit → Guardian)

**Scenario:** Scout identified silent `state.env` corruption — `LAST_STATUS` was overwritten from `CONTINUE` to empty string, causing loop to skip verification gate.

**Step 1: SCOUT_TO_ORBIT_HANDOFF (received)**

```yaml
SCOUT_TO_ORBIT_HANDOFF:
  source_agent: Scout
  incident_type: state_corruption
  findings:
    root_cause: "state.env LAST_STATUS field was overwritten to empty string by truncated write"
    affected_artifacts:
      - ".nexus-loop/state.env:2"
    evidence:
      - "git diff shows LAST_STATUS=CONTINUE → LAST_STATUS= (empty)"
      - "runner.log iter-6: 'skipping verification — status empty'"
  orbit_action_requested:
    - "failure_classification"
    - "state_recovery"
  constraints:
    - "do not discard Scout's evidence chain"
    - "preserve investigation context in progress.md"
  expected_output:
    - "failure taxonomy classification"
    - "contract repair plan or safe next action"
    - "handoff to Builder/Guardian if implementation needed"
```

**Step 2: Orbit Processing**
1. Intake: Classify as **Recovery** (state inconsistency reported by Scout)
2. Contract Check: **Partial** — state.env corrupted, verification gate bypassed
3. Risk Classification: **STATE_DRIFT / P1** — empty LAST_STATUS caused unverified iteration
4. Secondary concern: **COMMIT_SCOPE_RISK** — iteration 6 committed without verification gate

**Step 3: ORBIT_TO_GUARDIAN_HANDOFF (emitted)**

```yaml
ORBIT_TO_GUARDIAN_HANDOFF:
  concern: "commit scope safety — iteration 6 committed without verification gate"
  baseline_source: ".nexus-loop/dirty-start-paths.txt"
  candidate_scope:
    - "files committed in iter-6 auto-commit (verify=SKIP due to empty status)"
  policy:
    - "audit iter-6 commit for unverified changes"
    - "if changes are safe, annotate commit; if unsafe, prepare revert"
    - "enforce atomic state.env writes to prevent future truncation"
```
