# Handoff Formats

## NEXUS_HANDOFF - Receiving from Nexus

```yaml
## NEXUS_HANDOFF
task: "Improve code quality for payment module"
context:
  target_files:
    - src/payment/processor.ts
    - src/payment/validator.ts
  constraints:
    - "No breaking changes"
    - "Must maintain 80%+ coverage"
  mode: STANDARD
  target_uqs: 80
previous_findings:
  - agent: Scout
    summary: "Found potential null pointer issues"
```

## HONE_COMPLETE - Returning to Nexus

```yaml
## HONE_COMPLETE
status: SUCCESS | PARTIAL | BLOCKED
summary: "2 PDCA cycles completed, UQS improved from 65 to 83"
termination_reason: GOAL_ACHIEVED | DIMINISHING_RETURNS | MAX_CYCLES | MANUAL | BLOCKED
metrics:
  initial_uqs: 65
  final_uqs: 83
  total_delta: 18
  cycles_completed: 2
improvements:
  - domain: code_correctness
    delta: +15
    agent: Judge → Builder
  - domain: complexity
    delta: +10
    agent: Zen
  - domain: coverage
    delta: +12
    agent: Radar
blockers: [] # or list of blocking issues
recommended_next:
  - agent: Guardian
    reason: "Code ready for PR preparation"
```

## Nexus Hub Mode

When user input contains `## NEXUS_ROUTING`, treat Nexus as hub:
- Do not instruct other agent calls
- Always return results to Nexus (append `## NEXUS_HANDOFF` at output end)
- Include all required handoff fields

```text
## NEXUS_HANDOFF
- Step: [X/Y]
- Agent: Hone
- Summary: 1-3 lines describing quality improvement outcome
- Key findings / decisions:
  - Quality score: [before] → [after]
  - Iterations: [count]
  - Convergence: [achieved/not yet]
- Artifacts (files modified):
  - [file paths]
- Risks / trade-offs:
  - [Over-optimization risks]
- Open questions (blocking/non-blocking):
  - [Any quality concerns]
- Suggested next agent: [Agent] (reason)
- Next action: CONTINUE | VERIFY | DONE
```

## HONE_TO_AGENT_HANDOFF

```markdown
## [AGENT]_HANDOFF (from Hone)

### Quality Improvement Results
- **Target:** [What was improved]
- **Iterations:** [Count]
- **Score progression:** [X → Y → Z]
- **Final score:** [Score/100]

### Changes Made
- [Change 1]
- [Change 2]

### Learnings
- [Reusable pattern discovered]
```

## RALLY_TO_HONE_HANDOFF

When Rally teams complete parallel work, results may need quality improvement cycles.

```yaml
RALLY_TO_HONE_HANDOFF:
  Context:
    phase: "[Current phase]"
    rally_teams: "[Number of teams completed]"
    integration_status: "[PASS / PARTIAL / FAIL]"
  Quality_Assessment:
    overall_score: "[Initial quality score]"
    domains:
      - domain: "[code_correctness / complexity / coverage / security]"
        score: "[Current score]"
        priority: "[P0 / P1 / P2]"
  Mode_Selection:
    # Based on quality score:
    # score >= 80 → QUICK (1-2 cycles, polish only)
    # score 60-79 → STANDARD (2-4 cycles, targeted improvement)
    # score < 60  → DEEP (4-6 cycles, comprehensive improvement)
    mode: "[QUICK / STANDARD / DEEP]"
    target_uqs: "[Target quality score]"
    max_cycles: "[Maximum PDCA cycles]"
  Files:
    - "[file paths from Rally output]"
  Constraints:
    - "[No breaking changes]"
    - "[Maintain test coverage]"
```
