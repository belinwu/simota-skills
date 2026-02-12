# Handoff Patterns

## Receiving from Pulse

When Pulse defines metrics for experimentation:

```markdown
## Received from Pulse

**Primary Metric:** checkout_completed_rate
**Definition:** users_who_completed_checkout / users_who_started_checkout
**Current Baseline:** 3.2% (95% CI: 3.0-3.4%)
**Tracking Events:**
- Exposure: experiment_exposure (experiment_name='new_checkout')
- Conversion: checkout_completed

**Experiment Design:**
- MDE: 10% relative lift (3.52% treatment rate)
- Sample Size: 78,000 per variant
- Duration: 8 days at 20,000 daily traffic
```

## Handoff to Forge

```
/Forge prototype experiment variant
Context: Experiment [name] needs treatment variant.
Change: [Description of change]
Constraint: Must be measurable via [event_name]
```

## Handoff to Growth

```
/Growth implement winning variant
Context: Experiment [name] showed [X%] lift.
Recommendation: Roll out [treatment description]
Data: [Link to experiment report]
```

---

## EXPERIMENT_TO_GROWTH_HANDOFF

```markdown
## GROWTH_HANDOFF (from Experiment)

### Test Results
- **Experiment:** [Experiment name]
- **Duration:** [X days]
- **Sample Size:** [N per variant]
- **Result:** Winner / No significant difference / Inconclusive

### Validated Insights
- **Primary Metric:** [X% change, p-value, CI]
- **Secondary Metrics:** [Summary]
- **Recommendation:** Ship / Iterate / Abandon

### Implementation Notes
- Feature flag: [flag key]
- Winning variant: [variant name]
- Cleanup needed: [flag removal, dead code]

Suggested command: `/Growth implement winning variant`
```

## EXPERIMENT_TO_LAUNCH_HANDOFF

```markdown
## LAUNCH_HANDOFF (from Experiment)

### Feature Flag Cleanup
- **Flag key:** [flag_key]
- **Status:** Test complete, ready for full rollout
- **Winning variant:** [variant]
- **Cleanup tasks:**
  - [ ] Remove flag checks from code
  - [ ] Remove losing variant code
  - [ ] Update feature documentation

Suggested command: `/Launch plan rollout for [feature]`
```
