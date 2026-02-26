# Cast Distribution Adapters

Agent-specific format transformations for persona delivery. Each adapter extracts and reformats the persona data most relevant to the receiving agent.

---

## Overview

Different agents need different views of the same persona. Distribution adapters transform Cast's canonical persona format into agent-optimized summaries.

```
┌──────────────────┐
│  Cast Persona     │
│  (Full Format)    │
└────────┬─────────┘
         │
    ┌────┴────┐
    │ Adapter  │
    └────┬────┘
         │
    ┌────┴──────────────────────────────┐
    │                                    │
    ↓           ↓           ↓           ↓
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│  Echo   │ │ Spark  │ │ Retain │ │ Others │
│ Format  │ │ Format │ │ Format │ │ Format │
└────────┘ └────────┘ └────────┘ └────────┘
```

---

## Echo Adapter

**Purpose:** Deliver personas for UI walkthrough validation.

**Focus:** Emotion triggers, testing flows, context scenarios, behavioral patterns.

### Transformation

| Source Section | Echo Needs | Transformation |
|---------------|------------|---------------|
| Full persona | Complete | Pass through as-is (native format) |
| Cast metadata | Confidence only | Show confidence score for prioritization |
| Evolution Log | Last change only | Show most recent evolution for context |
| Tags | Filtering | Enable persona selection by tag |

### Output Format

Echo receives the persona file as-is (no transformation needed — Cast generates in Echo format). Additional context provided:

```markdown
## ECHO_CONTEXT

### Persona Confidence
- {persona_name}: {confidence} ({confidence_level})

### Recent Changes (for review focus)
- v{version} ({date}): {changes_summary}

### Recommended Review Priority
1. [Flow] — Reason: [new pain point / low emotion score]
2. [Flow] — Reason: [behavioral change detected]
```

**Files delivered:** Direct reference to `.agents/personas/{service}/{persona}.md`

---

## Spark Adapter

**Purpose:** Deliver personas for feature ideation and product proposals.

**Focus:** Unmet needs, frustrations, JTBD, feature opportunity signals.

### Transformation

| Source Section | Spark Needs | Transformation |
|---------------|------------|---------------|
| Goals | Feature targets | Extract as opportunity areas |
| Frustrations | Problem spaces | Extract as pain-to-solve list |
| JTBD | Need framework | Extract Functional/Emotional/Social |
| Behaviors | Usage context | Summarize as constraints |
| Emotion Triggers | Priority signals | Extract negative triggers as opportunities |
| Echo Testing Focus | Friction areas | Extract as improvement targets |
| Profile | User context | Summarize Role + Tech Level |

### Output Format

```markdown
## Persona: {name}

**Role:** {role} | **Tech Level:** {tech_level} | **Confidence:** {confidence}

### Unmet Needs
1. **{need_1}** — JTBD: {functional_job}
   - Current frustration: {related_frustration}
   - Emotion: {trigger_score} when {trigger_condition}
2. **{need_2}** — JTBD: {emotional_job}
   - Current frustration: {related_frustration}

### Feature Opportunity Signals
- {signal_1}: Evidence from {source}
- {signal_2}: Evidence from {source}

### Constraints
- Device: {device}
- Context: {usage_context}
- Frequency: {usage_frequency}

### Key Behaviors (Design Constraints)
- {behavior_1}
- {behavior_2}
- {behavior_3}
```

---

## Retain Adapter

**Purpose:** Deliver personas for retention strategy and re-engagement design.

**Focus:** Lifecycle stage, engagement patterns, churn risks, emotion triggers.

### Transformation

| Source Section | Retain Needs | Transformation |
|---------------|------------|---------------|
| Profile | Lifecycle stage | Extract Usage Frequency, map to lifecycle |
| Goals | Value drivers | What keeps them engaged |
| Frustrations | Churn risks | What pushes them away |
| Emotion Triggers | Engagement levers | Positive = retain, Negative = churn risk |
| Digital Behavior | Engagement patterns | Session duration, frequency, device |
| JTBD | Core value | Why they use the service |
| Life Stage | Timing context | Budget, time constraints |

### Output Format

```markdown
## Persona: {name}

**Role:** {role} | **Lifecycle:** {inferred_lifecycle_stage} | **Confidence:** {confidence}

### Engagement Profile
- Usage: {usage_frequency}
- Session: {avg_session_duration}
- Platform: {primary_device}

### Value Drivers (Why They Stay)
1. {goal_1} — Emotion: {positive_trigger}
2. {goal_2} — JTBD: {functional_job}

### Churn Risk Factors
1. {frustration_1} — Severity: {emotion_score}
2. {frustration_2} — Severity: {emotion_score}

### Re-engagement Triggers
- Positive: {delight_trigger} (+3), {satisfaction_trigger} (+2)
- Recovery: {relief_trigger} (+1) after {frustration_trigger}

### Lifecycle Recommendations
- **Onboarding:** {recommendation based on tech_level and behaviors}
- **Activation:** {recommendation based on goals}
- **Retention:** {recommendation based on emotion triggers}
- **Recovery:** {recommendation based on frustrations}
```

---

## Compete Adapter

**Purpose:** Deliver personas for competitive analysis and positioning.

**Focus:** Expectations, comparison behaviors, competitor experience.

### Transformation

| Source Section | Compete Needs | Transformation |
|---------------|------------|---------------|
| Profile | User context | Role, tech level |
| Psychographics | Decision style | Values, risk tolerance, information gathering |
| Behaviors | Comparison patterns | How they evaluate alternatives |
| Frustrations | Switching triggers | What makes them consider competitors |
| Goals | Expectation baseline | What they expect from any solution |
| JTBD | Need alignment | How well current solution meets jobs |

### Output Format

```markdown
## Persona: {name}

**Role:** {role} | **Decision Style:** {decision_making_style} | **Confidence:** {confidence}

### Expectations Baseline
- Must-have: {top_goal}
- Nice-to-have: {secondary_goals}
- Deal-breaker: {top_frustration}

### Comparison Behavior
- Information gathering: {style}
- Risk tolerance: {level}
- Switching cost tolerance: {inferred from behaviors}

### Competitive Vulnerability
- {frustration_1}: Competitor could win by solving this
- {frustration_2}: Unmet need creates opportunity

### Loyalty Anchors
- {goal_1}: Currently satisfied by this service
- {positive_trigger}: Emotional lock-in
```

---

## Accord Adapter

**Purpose:** Deliver personas for cross-team unified specification and stakeholder alignment.

**Focus:** Business context, simplified profile, key metrics.

### Transformation

| Source Section | Accord Needs | Transformation |
|---------------|------------|---------------|
| Profile | Executive summary | Simplified role description |
| Goals | Business objectives | Map to business KPIs |
| Frustrations | Risk areas | Translate to business impact |
| JTBD | Value proposition | Business-language jobs |
| Demographics | Market context | Segment size, spending |
| Confidence | Data quality | Trust level for decisions |

### Output Format

```markdown
## Persona: {name}

**Segment:** {role} | **Priority:** {priority} | **Data Confidence:** {confidence_level}

### Business Summary
{1-2 sentence description in business language}

### Key Metrics Context
- Usage: {frequency} user
- Platform: {device}
- Segment size: {if available, otherwise "estimation needed"}

### Business Objectives Alignment
1. {goal mapped to business KPI}
2. {goal mapped to business KPI}

### Risk Areas
1. {frustration mapped to business impact}
2. {frustration mapped to business impact}

### Decision Confidence
- Based on: {list of data sources}
- Reliability: {confidence_level} ({confidence_score})
- Recommendation: {use for decisions / validate further}
```

---

## Generic Adapter (Fallback)

For agents not listed above, Cast provides a minimal summary:

```markdown
## Persona Summary: {name}

**Role:** {role} | **Confidence:** {confidence}
**Echo Base Mapping:** {echo_base_mapping}
**Tags:** {tags}

### Core
- **Goal:** {primary_goal}
- **Frustration:** {primary_frustration}
- **Behavior:** {primary_behavior}

### Context
- **Device:** {device}
- **Usage:** {usage_frequency}
- **Tech Level:** {tech_level}

### File
`.agents/personas/{service}/{persona-name}.md`
```

---

## Adapter Selection Logic

```
IF target_agent == "echo":
  use Echo Adapter (pass-through + context)
ELIF target_agent == "spark":
  use Spark Adapter (needs-focused)
ELIF target_agent == "retain":
  use Retain Adapter (lifecycle-focused)
ELIF target_agent == "compete":
  use Compete Adapter (comparison-focused)
ELIF target_agent == "accord":
  use Accord Adapter (business-language)
ELSE:
  use Generic Adapter (minimal summary)
```

---

## Multi-Persona Distribution

When distributing multiple personas to a single agent:

1. **Header** with service context and persona count
2. **Summary table** for quick comparison
3. **Individual profiles** in agent-specific format
4. **Cross-persona insights** highlighting patterns across personas
5. **Recommended actions** specific to receiving agent's capabilities

```markdown
## Cast Distribution: {service_name} → {target_agent}

**Personas:** {count} | **Service type:** {b2b/b2c} | **Registry version:** {date}

### Quick Comparison
| Persona | Priority | Confidence | Key Need | Key Risk |
|---------|----------|------------|----------|----------|
| {name_1} | P0 | {confidence} | {top_need} | {top_risk} |
| {name_2} | P1 | {confidence} | {top_need} | {top_risk} |

### Individual Profiles
[Agent-specific format for each persona]

### Cross-Persona Patterns
- **Universal need:** {shared across all personas}
- **Segment-specific:** {unique to specific personas}
- **Opportunity:** {gap identified across persona comparison}
```
