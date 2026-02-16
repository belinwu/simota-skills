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
