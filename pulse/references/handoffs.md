# Handoff Templates & Agent Collaboration

## Collaborating Agents

| Agent | Role | When to Invoke |
|-------|------|----------------|
| **Experiment** | A/B test design | When metrics need validation through experimentation |
| **Growth** | Conversion optimization | When funnel metrics indicate drop-off issues |
| **Radar** | Test coverage | When tracking code needs unit/integration tests |
| **Scout** | Issue investigation | When metrics show unexpected anomalies |
| **Canvas** | Visualization | When creating metric diagrams or dashboards |

---

## PULSE_TO_EXPERIMENT_HANDOFF

```markdown
## EXPERIMENT_HANDOFF (from Pulse)

### Metric Definition for A/B Test
- **Primary Metric:** [Metric name]
- **Definition:** [Exact calculation]
- **Current Baseline:** [Current value with confidence interval]
- **MDE:** [Minimum Detectable Effect]
- **Sample Size Required:** [Calculated based on baseline and MDE]

### Secondary Metrics
1. [Metric 2] - [Definition]
2. [Metric 3] - [Definition]

### Guardrail Metrics
1. [Metric that should NOT decrease] - [Threshold]

### Tracking Events
- Exposure event: [event_name]
- Conversion event: [event_name]
- Additional events: [list]

Suggested command: `/Experiment design test for [feature]`
```

**Shorthand:**
```
/Experiment design test
Context: Pulse defined [metric] with baseline [X%].
Goal: Validate [hypothesis] with MDE [Y%].
Tracking: Events [list] already implemented.
```

---

## PULSE_TO_GROWTH_HANDOFF

```markdown
## GROWTH_HANDOFF (from Pulse)

### Funnel Drop-off Analysis
- **Funnel:** [Funnel name]
- **Problem Step:** [Step X → Step Y]
- **Current Rate:** [X%]
- **Target Rate:** [Y%]
- **Data Period:** [Date range]

### Segment Breakdown
| Segment | Rate | Volume |
|---------|------|--------|
| [Segment 1] | [X%] | [N] |
| [Segment 2] | [X%] | [N] |

### Hypothesis
[Why users drop off at this step]

Suggested command: `/Growth optimize funnel step [X]`
```

**Shorthand:**
```
/Growth optimize funnel
Context: Pulse identified drop-off at [step].
Metric: Conversion rate is [X%], target is [Y%].
Data: [Relevant funnel data]
```

---

## PULSE_TO_CANVAS_HANDOFF

```markdown
## CANVAS_HANDOFF (from Pulse)

### Visualization Request
- **Type:** Metrics dashboard / Funnel diagram / Cohort heatmap
- **Metrics:** [List of metrics to visualize]
- **Relationships:** [How metrics connect]
- **Format:** Mermaid flowchart | Dashboard mockup

Suggested command: `/Canvas create metrics dashboard`
```

**Shorthand:**
```
/Canvas create metrics dashboard
Metrics: [list of metrics]
Relationships: [how metrics connect]
Format: [Mermaid flowchart | dashboard mockup]
```
