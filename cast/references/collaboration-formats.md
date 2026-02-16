# Cast Collaboration Formats

5 collaboration patterns with detailed handoff formats for inter-agent communication.

---

## Pattern Overview

| Pattern | Flow | Purpose |
|---------|------|---------|
| **A** | Researcher → Cast[FUSE] → Echo | Research data → persona integration → UI validation |
| **B** | Trace → Cast[EVOLVE] | Behavioral data → persona evolution |
| **C** | Voice → Cast[FUSE] | Feedback segments → persona enrichment |
| **D** | Cast[DISTRIBUTE] → Spark | Personas → feature proposals |
| **E** | Cast[DISTRIBUTE] → Retain | Personas → retention strategies |

---

## Pattern A: Researcher → Cast → Echo

### Use Case

Researcher completes user interviews or usability tests. Cast integrates findings into personas. Echo validates UI with enriched personas.

### Step 1: Researcher → Cast Handoff

**Input format** (what Cast receives from Researcher):

```markdown
## CAST_HANDOFF: Research Integration

### Source
- **Agent:** Researcher
- **Research type:** [Interview/Usability Test/Survey]
- **Date:** YYYY-MM-DD
- **Participants:** [count]

### Findings

#### User Segments Identified
| Segment | Description | Evidence |
|---------|-------------|----------|
| [Segment 1] | [Description] | [Interview quote/data reference] |
| [Segment 2] | [Description] | [Interview quote/data reference] |

#### Goals Discovered
- [Goal 1] — Evidence: [quote/observation]
- [Goal 2] — Evidence: [quote/observation]

#### Pain Points Discovered
- [Pain 1] — Evidence: [quote/observation]
- [Pain 2] — Evidence: [quote/observation]

#### Behavioral Insights
- [Insight 1] — Evidence: [observation]
- [Insight 2] — Evidence: [observation]

#### Recommended Persona Updates
| Existing Persona | Suggested Changes | Confidence |
|-----------------|-------------------|------------|
| [Persona name] | [What to update] | [High/Medium/Low] |
| [New segment] | [Create new persona] | [High/Medium/Low] |
```

### Step 2: Cast Processing

Cast receives handoff and:
1. Matches findings to existing personas via FUSE mode
2. Creates new personas for unmatched segments via CONJURE
3. Updates confidence scores with research contribution (+0.30)
4. Updates registry

### Step 3: Cast → Echo Handoff

**Output format** (what Cast sends to Echo):

```markdown
## ECHO_HANDOFF: Updated Personas Ready

### Source
- **Agent:** Cast (via Researcher findings)
- **Personas updated:** [count]
- **Personas created:** [count]

### Persona Summary
| Persona | Status | Confidence | Echo Mapping | File |
|---------|--------|------------|-------------|------|
| [Name 1] | Updated (v1.1→v1.2) | 0.85 | Newbie | [path] |
| [Name 2] | New | 0.75 | Power User | [path] |

### Recommended Validation Flows
1. [Flow 1] — Test with [Persona 1] (new pain point discovered)
2. [Flow 2] — Test with [Persona 2] (new segment)

### Files
- `.agents/personas/{service}/[persona-1].md`
- `.agents/personas/{service}/[persona-2].md`
```

---

## Pattern B: Trace → Cast

### Use Case

Trace extracts behavioral patterns from session replay data. Cast evolves personas with behavioral evidence.

### Trace → Cast Handoff

**Input format** (what Cast receives from Trace):

```markdown
## CAST_HANDOFF: Behavioral Data

### Source
- **Agent:** Trace
- **Period:** YYYY-MM-DD to YYYY-MM-DD
- **Sessions analyzed:** [count]

### Behavioral Clusters

#### Cluster 1: [Cluster Name]
- **Size:** [% of sessions]
- **Device mix:** Mobile [%], Desktop [%]
- **Avg session duration:** [time]
- **Key navigation pattern:** [description]
- **Drop-off points:** [list]
- **Suggested persona mapping:** [Existing persona name or "New segment"]

#### Cluster 2: [Cluster Name]
- **Size:** [% of sessions]
- **Device mix:** Mobile [%], Desktop [%]
- **Avg session duration:** [time]
- **Key navigation pattern:** [description]
- **Drop-off points:** [list]
- **Suggested persona mapping:** [persona name]

### Drift Signals
| Persona | Axis | Current | Observed | Significance |
|---------|------|---------|----------|-------------|
| [Name] | Behavior | Desktop 60% | Desktop 40% | Moderate |
| [Name] | Pain Points | Cart abandonment 15% | Cart abandonment 25% | Significant |

### Raw Metrics
| Metric | Previous Period | Current Period | Change |
|--------|----------------|---------------|--------|
| Mobile sessions % | 60% | 70% | +10% |
| Avg pages/session | 4.2 | 3.8 | -0.4 |
| Cart abandonment | 15% | 25% | +10% |
```

### Cast Processing

Cast receives Trace handoff and:
1. Maps behavioral clusters to existing personas
2. Identifies drift signals across 4 axes
3. Applies EVOLVE workflow for each affected persona
4. Bumps confidence with Trace contribution (+0.25)
5. Updates evolution logs and registry

---

## Pattern C: Voice → Cast

### Use Case

Voice analyzes user feedback (NPS, reviews, support tickets). Cast fuses feedback insights into personas.

### Voice → Cast Handoff

**Input format** (what Cast receives from Voice):

```markdown
## CAST_HANDOFF: Feedback Integration

### Source
- **Agent:** Voice
- **Feedback type:** [NPS/CSAT/Reviews/Support Tickets]
- **Period:** YYYY-MM-DD to YYYY-MM-DD
- **Responses analyzed:** [count]

### Segment Insights

#### Promoters (NPS 9-10)
- **Theme 1:** [Positive theme] — Quote: "[user quote]"
- **Theme 2:** [Positive theme] — Quote: "[user quote]"
- **Suggested persona impact:** [Which persona, what to update]

#### Detractors (NPS 0-6)
- **Theme 1:** [Negative theme] — Quote: "[user quote]"
- **Theme 2:** [Negative theme] — Quote: "[user quote]"
- **Suggested persona impact:** [Which persona, what to update]

### Feedback-to-Persona Mapping
| Feedback Theme | Frequency | Affected Persona | Suggested Update |
|---------------|-----------|-----------------|-----------------|
| "Shipping cost surprise" | 23% of detractors | First-Time Buyer | Add to Frustrations |
| "Fast checkout" | 45% of promoters | Power Shopper | Confirm Goal |
| "Confusing returns" | 18% of detractors | First-Time Buyer | Add to Pain Points |

### Emerging Segments
- [New user type not covered by existing personas]: Evidence: "[feedback quotes]"
```

### Cast Processing

Cast receives Voice handoff and:
1. Maps feedback themes to existing persona attributes
2. Updates Frustrations/Goals based on feedback patterns
3. Refines Emotion Triggers from actual user quotes
4. Creates new personas for emerging segments
5. Bumps confidence with Voice contribution (+0.20)

---

## Pattern D: Cast → Spark

### Use Case

Cast distributes personas to Spark for feature ideation based on unmet needs and frustrations.

### Cast → Spark Handoff

**Output format** (what Cast sends to Spark):

```markdown
## SPARK_HANDOFF: Personas for Feature Ideation

### Source
- **Agent:** Cast
- **Personas included:** [count]
- **Focus:** Unmet needs and high-friction areas

### Persona Summaries (Feature-Focused)

#### [Persona 1 Name] (Confidence: 0.82)
**Role:** [Role]
**Primary frustration:** [Top frustration]
**Unmet needs:**
1. [Need 1] — JTBD: [functional job]
2. [Need 2] — JTBD: [emotional job]

**High-friction flows:**
- [Flow 1]: Emotion Score [-2] — [Description]
- [Flow 2]: Emotion Score [-3] — [Description]

**Feature opportunity signals:**
- [Signal 1 from behavioral/feedback data]
- [Signal 2 from behavioral/feedback data]

#### [Persona 2 Name] (Confidence: 0.75)
[Same structure]

### Cross-Persona Opportunities
| Opportunity | Affected Personas | Evidence | Priority |
|-------------|------------------|----------|----------|
| [Feature area 1] | [Persona 1, 2] | [Shared frustration/need] | High |
| [Feature area 2] | [Persona 1] | [Unique need] | Medium |

### Files
- `.agents/personas/{service}/[persona-1].md`
- `.agents/personas/{service}/[persona-2].md`
```

---

## Pattern E: Cast → Retain

### Use Case

Cast distributes personas to Retain for designing persona-specific retention and re-engagement strategies.

### Cast → Retain Handoff

**Output format** (what Cast sends to Retain):

```markdown
## RETAIN_HANDOFF: Personas for Retention Strategy

### Source
- **Agent:** Cast
- **Personas included:** [count]
- **Focus:** Lifecycle stages, churn risks, engagement patterns

### Persona Profiles (Retention-Focused)

#### [Persona 1 Name] (Confidence: 0.82)
**Role:** [Role]
**Lifecycle stage:** [Awareness/Adoption/Active/At-risk/Churned]
**Usage frequency:** [Daily/Weekly/Monthly]

**Engagement indicators:**
- Session frequency: [trend]
- Feature usage depth: [shallow/medium/deep]
- Last active: [date or "N/A for template"]

**Churn risk factors:**
1. [Risk factor 1] — Evidence: [data source]
2. [Risk factor 2] — Evidence: [data source]

**Retention levers:**
- [What keeps this persona engaged]
- [Trigger for re-engagement]
- [Value proposition that resonates]

**Emotion triggers (retention-relevant):**
| Positive | Negative |
|----------|----------|
| Delighted (+3): [trigger] | Frustrated (-2): [trigger] |
| Satisfied (+2): [trigger] | Abandoned (-3): [trigger] |

#### [Persona 2 Name] (Confidence: 0.75)
[Same structure]

### Cross-Persona Retention Matrix
| Strategy | [Persona 1] | [Persona 2] | [Persona 3] |
|----------|-------------|-------------|-------------|
| Onboarding email | High impact | Medium impact | Low impact |
| Feature discovery | Medium impact | High impact | High impact |
| Re-engagement push | High impact | Low impact | Medium impact |

### Files
- `.agents/personas/{service}/[persona-1].md`
- `.agents/personas/{service}/[persona-2].md`
```

---

## NEXUS Integration

### AUTORUN Step Complete Format

```markdown
_STEP_COMPLETE
- Agent: Cast
- Status: SUCCESS | PARTIAL | BLOCKED | FAILED
- Output:
  - Mode: CONJURE | FUSE | EVOLVE | AUDIT | DISTRIBUTE | SPEAK
  - Personas affected: [count]
  - Personas created: [count]
  - Confidence changes: [summary]
  - Registry updated: true | false
- Next: Echo | Spark | Retain | VERIFY | DONE
```

### NEXUS_HANDOFF Format

When Cast receives `## NEXUS_ROUTING`:

```markdown
## NEXUS_HANDOFF

### Step
[Current step in chain]

### Agent
Cast

### Summary
[1-2 sentence summary of what Cast did]

### Key Findings
- [Finding 1]
- [Finding 2]

### Artifacts
- `.agents/personas/{service}/[persona-1].md`
- `.agents/personas/registry.yaml`

### Risks
- [Any risks identified]

### Open Questions
- [Unresolved questions]

### Confirmations
- [Decisions made during execution]

### Suggested Next
- [Agent] for [purpose]

### Next Action
[Specific next step recommendation]
```

---

## General Handoff Principles

1. **Always include source attribution** — Every handoff identifies the originating agent and data
2. **Confidence is transparent** — All handoffs include confidence scores
3. **Evidence-backed** — Recommendations reference specific data points
4. **Actionable** — Handoffs include clear next steps for the receiving agent
5. **File references** — Always include paths to persona files for direct access
6. **Format adaptation** — Adapt handoff detail level to receiving agent's needs (see `distribution-adapters.md`)
