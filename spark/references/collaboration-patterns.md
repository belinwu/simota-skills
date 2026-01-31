# Spark Collaboration Patterns Reference

All handoff formats for agent collaboration.

## Pattern A: Latent Needs Discovery Loop

**Flow**: Echo → Spark → Echo validation

**Purpose**: Transform latent user needs identified by Echo into validated feature proposals.

### Echo → Spark Handoff Format

```markdown
## ECHO_TO_SPARK_HANDOFF

**Persona Analyzed**: [Persona name]
**Session Type**: [Walkthrough / Interview / Observation]

**Latent Needs Discovered**:
1. **Need**: [Unspoken need description]
   - **Evidence**: [User behavior/quote that revealed this]
   - **JTBD Context**: [Functional/Emotional/Social job]
   - **Severity**: [Critical / High / Medium / Low]

2. **Need**: [...]

**Confusion Points**:
- [UI element or flow that caused confusion]
- [Workaround user attempted]

**Recommended Focus**: [Most impactful need to address first]

**Validation Request**: After proposal, return to Echo for persona validation
```

### Spark → Echo Validation Request

```markdown
## SPARK_TO_ECHO_VALIDATION

**Proposal**: [Feature name]
**Target Persona**: [Persona from original handoff]

**Validation Questions**:
1. Would [Persona] understand this feature immediately?
2. Does this solve the latent need identified?
3. What confusion points might remain?

**Expected Echo Output**:
- Persona validation walkthrough
- Remaining friction points
- Approval / Iteration needed
```

---

## Pattern B: Research-Driven Proposal

**Flow**: Researcher → Spark

**Purpose**: Transform user research insights into actionable feature proposals.

### Researcher → Spark Handoff Format

```markdown
## RESEARCHER_TO_SPARK_HANDOFF

**Research Type**: [User Interview / Usability Test / Journey Map / Persona Creation]
**Participants**: [Number and segment]

**Key Insights**:
1. **Insight**: [Finding description]
   - **Evidence**: [Quote / Observation / Data point]
   - **Frequency**: [How many participants showed this]
   - **Impact**: [High / Medium / Low]

2. **Insight**: [...]

**Persona Updates**:
- [New persona created / Existing persona refined]
- [Key characteristics or goals updated]

**Journey Pain Points**:
| Stage | Pain Point | Severity | Opportunity |
|-------|------------|----------|-------------|
| [Stage] | [Pain] | [H/M/L] | [Feature idea] |

**Research Recommendation**: [Suggested feature direction]
```

---

## Pattern C: Feedback Integration

**Flow**: Voice → Spark

**Purpose**: Transform aggregated user feedback into prioritized feature proposals.

### Voice → Spark Handoff Format

```markdown
## VOICE_TO_SPARK_HANDOFF

**Feedback Period**: [Date range]
**Total Responses**: [Number]
**NPS Score**: [Score] (Δ [change from last period])

**Top Feature Requests** (by frequency):
| Rank | Request | Count | Sentiment | Representative Quote |
|------|---------|-------|-----------|---------------------|
| 1 | [Request] | [N] | [Pos/Neg/Neu] | "[Quote]" |
| 2 | [Request] | [N] | [Pos/Neg/Neu] | "[Quote]" |

**Pain Point Clusters**:
1. **Cluster**: [Theme name]
   - **Feedback Count**: [N]
   - **Common Phrases**: [Keywords]
   - **User Segment**: [Who is affected]

**Churn Risk Signals**:
- [Feedback indicating potential churn]

**Recommended Priority**: [Most urgent feedback to address]
```

---

## Pattern D: Competitive Differentiation

**Flow**: Compete → Spark

**Purpose**: Transform competitive analysis into differentiation-focused feature proposals.

### Compete → Spark Handoff Format

```markdown
## COMPETE_TO_SPARK_HANDOFF

**Competitors Analyzed**: [List of competitors]
**Analysis Date**: [Date]

**Feature Gap Analysis**:
| Feature | Us | Comp A | Comp B | Gap Type |
|---------|-----|--------|--------|----------|
| [Feature] | ❌ | ✅ | ✅ | Parity Gap |
| [Feature] | ✅ | ❌ | ❌ | Our Advantage |
| [Feature] | ❌ | ❌ | ❌ | Blue Ocean |

**Differentiation Opportunities**:
1. **Opportunity**: [Feature/approach]
   - **Why We Can Win**: [Our unique capability]
   - **Market Demand**: [Evidence of demand]
   - **Competitive Moat**: [Defensibility]

**Positioning Recommendation**:
- **Current Position**: [Where we are]
- **Target Position**: [Where we should be]
- **Gap to Close**: [What's needed]

**Urgency**: [Time-sensitive competitive threat?]
```

---

## Pattern E: Hypothesis Validation Loop

**Flow**: Spark → Experiment → Spark

**Purpose**: Validate feature hypotheses through A/B testing before full implementation.

### Spark → Experiment Handoff Format

```markdown
## SPARK_TO_EXPERIMENT_HANDOFF

**Feature Proposal**: [Feature name]
**Hypothesis ID**: H-[XXX]

**Hypothesis Statement**:
- **We believe**: [Change/feature]
- **For**: [Target persona]
- **Will achieve**: [Expected outcome]
- **Success metric**: [Primary metric]
- **Current baseline**: [Current value]
- **Target goal**: [Expected value after test]

**Test Design Request**:
- **Recommended method**: [A/B test / Feature flag / Prototype]
- **Sample size needed**: [Estimate or ask Experiment]
- **Duration**: [Suggested test period]
- **Segments**: [User segments to include/exclude]

**Minimum Viable Test**:
- [Simplest version to test the hypothesis]

**Decision Criteria**:
- **Ship if**: [Metric reaches X]
- **Iterate if**: [Metric between Y and X]
- **Kill if**: [Metric below Y]
```

### Experiment → Spark Result Format

```markdown
## EXPERIMENT_TO_SPARK_RESULT

**Hypothesis ID**: H-[XXX]
**Test Duration**: [Start] → [End]
**Sample Size**: [Control: N, Treatment: N]

**Results**:
| Metric | Control | Treatment | Δ | Significance |
|--------|---------|-----------|---|--------------|
| [Primary] | [Val] | [Val] | [%] | [p-value] |
| [Secondary] | [Val] | [Val] | [%] | [p-value] |

**Statistical Confidence**: [Confidence level]

**Verdict**: VALIDATED / INVALIDATED / INCONCLUSIVE

**Unexpected Findings**:
- [Any surprising results or side effects]

**Recommendation**:
- [Ship / Iterate / Kill / Extend test]
```

---

## Pattern F: Implementation Handoff

**Flow**: Spark → Sherpa/Forge → Builder

**Purpose**: Hand off validated proposals for implementation.

### Spark → Sherpa Handoff Format

```markdown
## SPARK_TO_SHERPA_HANDOFF

**Feature**: [Feature name]
**Priority**: [P1/P2/P3]
**Validation Status**: [Validated / Assumed feasible]

**Proposal Document**: [Link to proposal file]

**Implementation Scope**:
- **Must Have**: [Core requirements]
- **Should Have**: [Important but deferrable]
- **Could Have**: [Nice-to-have]

**Technical Context** (from Scout):
- **Relevant files**: [file:line references]
- **Data availability**: [Available / Partial / Missing]
- **Dependencies**: [List]

**Success Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Deadline/Sprint**: [Target completion]

**Request**: Break down into atomic implementation steps (15 min each)
```

### Spark → Forge Handoff Format

```markdown
## SPARK_TO_FORGE_HANDOFF

**Feature**: [Feature name]
**Prototype Scope**: [What to prototype]

**User Story**:
As a [persona], I want to [action] so that [benefit].

**Core Interaction**:
- [Primary user flow to prototype]
- [Key UI elements needed]

**Prototype Fidelity**: [Low / Medium / High]

**Validation Goal**:
- [What we want to learn from the prototype]

**NOT in Scope**:
- [What to explicitly exclude]

**Handoff to**: Builder (after prototype validation)
```

---

## Scout Integration

### When to Request Scout

- Need to verify data availability for a feature
- Want to understand existing implementation patterns
- Checking if similar functionality already exists
- Assessing technical feasibility

### Scout Request Template

```markdown
### Scout Investigation Request

**Feature Concept**: [Feature name / description]

**Investigation Scope**:
- [ ] Existing data structures that could support this feature
- [ ] Current workflows or logic that could be extended
- [ ] API endpoints that could be reused or modified
- [ ] Similar patterns already implemented in codebase
- [ ] External dependencies or integrations involved

**Specific Questions**:
1. Does [model/table] contain [required field/data]?
2. Is there existing logic for [specific functionality]?
3. What dependencies would be affected by this change?
4. Are there performance concerns with [data access pattern]?

**Context for Scout**:
- User story: [Brief user story]
- Expected data volume: [Estimate]
- Performance requirements: [If any]

**Expected Output**:
- List of relevant files/functions with line numbers
- Data availability assessment (Available / Partial / Missing)
- Technical feasibility rating (High / Medium / Low)
- Potential blockers or concerns

Suggested command:
`/Scout investigate [specific area] for [feature purpose]`
```

### Integrating Scout Findings

```markdown
### Scout Investigation Results

**Feature**: [Feature name]
**Investigation Date**: [Date]

**Findings Summary**:
- Data availability: [Available / Partial / Missing]
- Existing patterns: [Yes, in X / No]
- Feasibility: [High / Medium / Low]

**Key Discoveries**:
1. [Finding 1 with file:line reference]
2. [Finding 2 with file:line reference]

**Impact on Proposal**:
- [How findings affect the feature specification]
- [Adjustments needed based on technical reality]
```

---

## Canvas Integration

### Feature Roadmap

```markdown
### Canvas Integration: Feature Roadmap

Request Canvas to generate:

\`\`\`mermaid
gantt
    title Product Roadmap Q1-Q2
    dateFormat YYYY-MM
    section Quick Wins
        Feature A    :done, 2024-01, 2024-02
        Feature B    :active, 2024-02, 2024-03
    section Big Bets
        Feature C    :2024-03, 2024-05
        Feature D    :2024-05, 2024-07
    section Experiments
        Hypothesis E :2024-02, 2024-03
\`\`\`

To generate: `/Canvas create roadmap from this feature list`
```

### User Journey Map

```markdown
### Canvas Integration: User Journey

\`\`\`mermaid
journey
    title User Journey: [Feature Name]
    section Awareness
        Discover feature: 3: User
        Read description: 4: User
    section Activation
        First use: 5: User
        Complete task: 4: User
    section Retention
        Return usage: 5: User
        Form habit: 4: User
    section Advocacy
        Share feature: 3: User
        Recommend product: 4: User
\`\`\`
```

### Feature Dependency Graph

```markdown
### Canvas Integration: Feature Dependencies

\`\`\`mermaid
graph TD
    subgraph Proposed Feature
        NF[New Feature]
    end
    subgraph Existing Infrastructure
        DB1[(Users DB)]
        DB2[(Orders DB)]
        API1[/users API/]
        API2[/orders API/]
        SVC[Notification Service]
    end
    subgraph Dependencies
        NF --> DB1
        NF --> DB2
        NF --> API1
        NF --> API2
        NF -.-> SVC
    end

    style NF fill:#e1f5fe
    style DB1 fill:#fff3e0
    style DB2 fill:#fff3e0
\`\`\`

Legend:
- Solid arrow: Required dependency
- Dashed arrow: Optional enhancement
```

### Priority Visualization

```markdown
### Canvas Integration: Priority Matrix

\`\`\`
Priority Matrix Visualization

HIGH IMPACT
     │
     │  ┌─────────┐     ┌─────────┐
     │  │Feature C│     │Feature A│
     │  │(Big Bet)│     │(Quick   │
     │  │ Score:75│     │ Win)    │
     │  └─────────┘     │Score:150│
     │                  └─────────┘
HIGH─┼──────────────────────────────LOW
EFFORT                           EFFORT
     │  ┌─────────┐     ┌─────────┐
     │  │Feature D│     │Feature B│
     │  │(Time    │     │(Fill-In)│
     │  │ Sink)   │     │Score:30 │
     │  │ Skip    │     └─────────┘
     │  └─────────┘
     │
LOW IMPACT
\`\`\`
```

---

## BIDIRECTIONAL COLLABORATION MATRIX

### Input Partners (→ Spark)

| Partner | Input Type | Trigger | Handoff Format |
|---------|------------|---------|----------------|
| **Echo** | Latent needs, confusion points | Persona walkthrough complete | ECHO_TO_SPARK_HANDOFF |
| **Researcher** | Personas, insights, journey maps | Research synthesis complete | RESEARCHER_TO_SPARK_HANDOFF |
| **Voice** | Feedback clusters, NPS data | Feedback analysis complete | VOICE_TO_SPARK_HANDOFF |
| **Compete** | Gaps, positioning, opportunities | Competitive analysis complete | COMPETE_TO_SPARK_HANDOFF |
| **Pulse** | Funnel data, KPI trends | Metrics review complete | PULSE_TO_SPARK_HANDOFF |

### Output Partners (Spark →)

| Partner | Output Type | Trigger | Handoff Format |
|---------|-------------|---------|----------------|
| **Sherpa** | Task breakdown request | Proposal approved | SPARK_TO_SHERPA_HANDOFF |
| **Forge** | Prototype request | Validation needed | SPARK_TO_FORGE_HANDOFF |
| **Builder** | Implementation spec | Prototype validated | SPARK_TO_BUILDER_HANDOFF |
| **Experiment** | A/B test design | Hypothesis needs validation | SPARK_TO_EXPERIMENT_HANDOFF |
| **Canvas** | Roadmap visualization | Priority matrix complete | SPARK_TO_CANVAS_HANDOFF |
| **Echo** | Proposal validation | Draft proposal ready | SPARK_TO_ECHO_VALIDATION |
| **Scout** | Technical investigation | Feasibility unclear | Scout Investigation Request |
| **Growth** | SEO/CRO requirements | Growth feature proposed | SPARK_TO_GROWTH_HANDOFF |
