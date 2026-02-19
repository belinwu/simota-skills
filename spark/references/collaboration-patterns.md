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
...
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
...
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
...
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
...
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
...
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
...
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
...
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
...
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
...
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
...
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
...
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
...
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
...
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
...
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

---

## Pattern G: Metrics-Driven Proposal

**Flow**: Pulse → Spark → Implementation

**Purpose**: Transform quantitative metrics and funnel data into actionable feature proposals.

### Pulse → Spark Handoff Format

```markdown
## PULSE_TO_SPARK_HANDOFF

**Analysis Period**: [Date range]
**Primary Metric**: [North Star Metric name]

**Funnel Drop-off Analysis**:
| Stage | Current Rate | Target Rate | Drop-off % | Priority |
|-------|--------------|-------------|------------|----------|
| [Stage 1] | [X%] | [Y%] | [Z%] | [P1/P2/P3] |
| [Stage 2] | [X%] | [Y%] | [Z%] | [P1/P2/P3] |

**KPI Trends**:
| Metric | Current | 30-day Trend | Anomaly? |
|--------|---------|--------------|----------|
| [Metric 1] | [Value] | [↑/↓/→] [%] | [Yes/No] |
...
```

### Spark Response: Metrics-to-Proposal Conversion

```markdown
## SPARK_METRICS_PROPOSAL

**Source**: Pulse funnel analysis [Date]
**Target Metric**: [Metric from Pulse handoff]

**Proposal**: [Feature name]

**Data-Driven Rationale**:
- Current: [Baseline metric]
- Gap: [Target - Current]
- Root cause hypothesis: [From Pulse analysis]

**Acceptance Criteria** (from Pulse baseline):
- [ ] [Metric] improves from [X] to [Y]
- [ ] No regression in [Guardrail metric]
...
```

### Metrics → Feature Mapping Patterns

| Metric Issue | Feature Pattern | Example |
|--------------|-----------------|---------|
| Signup drop-off | Reduce friction | Remove optional fields |
| Low engagement | Add value earlier | Quick wins onboarding |
| High churn | Improve retention | Re-engagement triggers |
| Low conversion | Clarify value | Social proof, testimonials |
| Feature discovery | Improve visibility | Feature hints, tours |

---

## Pattern H: Security Review

**Flow**: Spark → Sentinel → Spark iteration

**Purpose**: Ensure security and privacy considerations are addressed before implementation.

### When to Trigger

- Feature involves user data handling
- Feature adds authentication/authorization
- Feature integrates external services
- Feature processes sensitive information (PII, financial, health)
- Feature adds new input surfaces

### Spark → Sentinel Handoff Format

```markdown
## SPARK_TO_SENTINEL_HANDOFF

**Feature Proposal**: [Feature name]
**Proposal Doc**: [Link to proposal file]

**Security-Relevant Aspects**:

**Data Handling**:
- [ ] Collects new user data: [Yes/No - specify types]
- [ ] Stores sensitive data: [Yes/No - specify]
- [ ] Transmits data externally: [Yes/No - to where]
- [ ] Data retention requirements: [Specify]

**Authentication/Authorization**:
- [ ] New auth flows: [Describe if any]
...
```

### Sentinel → Spark Security Requirements

```markdown
## SENTINEL_TO_SPARK_SECURITY_REQUIREMENTS

**Feature**: [Feature name]
**Review Date**: [Date]
**Risk Level**: [Critical/High/Medium/Low]

**Required Security Controls**:
1. **[Control Type]**: [Specific requirement]
   - Implementation: [How to implement]
   - Priority: [Must have / Should have]

2. **[Control Type]**: [Specific requirement]
   - Implementation: [How to implement]
   - Priority: [Must have / Should have]

...
```

### Security Feature Checklist

Use this checklist when proposing features with security implications:

```markdown
### Security Feature Checklist

**Input Validation**:
- [ ] All user inputs validated
- [ ] Input length limits defined
- [ ] File type restrictions (if uploads)
- [ ] Sanitization for XSS prevention

**Authentication & Authorization**:
- [ ] Auth requirements documented
- [ ] Permission model defined
- [ ] Session timeout specified
- [ ] Rate limiting considered

**Data Protection**:
...
```

---

## Pattern I: Growth Integration

**Flow**: Spark → Growth → Spark refinement

**Purpose**: Validate SEO, Social, and Conversion optimization aspects of feature proposals.

### When to Trigger

- Feature adds new pages or routes
- Feature changes user-facing content
- Feature affects conversion funnels
- Feature impacts social sharing
- Feature modifies landing pages

### Spark → Growth Handoff Format

```markdown
## SPARK_TO_GROWTH_HANDOFF

**Feature Proposal**: [Feature name]
**Feature Type**: [New page / Enhancement / Flow change]

**SEO Impact Assessment**:
- [ ] Adds new pages: [Yes/No - list URLs]
- [ ] Changes URL structure: [Yes/No - before/after]
- [ ] Modifies content: [Yes/No - which pages]
- [ ] Affects meta tags: [Yes/No - specify]

**Social Sharing Impact**:
- [ ] New shareable content: [Yes/No - type]
- [ ] OG image requirements: [Describe]
- [ ] Share text recommendations: [Describe]
...
```

### Growth → Spark Optimization Requirements

```markdown
## GROWTH_TO_SPARK_REQUIREMENTS

**Feature**: [Feature name]
**Review Date**: [Date]

**SEO Requirements**:
| Requirement | Priority | Specification |
|-------------|----------|---------------|
| Meta title | Must | [Format/template] |
| Meta description | Must | [Character limit, keywords] |
| Heading structure | Should | [H1/H2 hierarchy] |
| Schema markup | Should | [JSON-LD type] |
| Canonical URL | Must | [Pattern] |

**OGP/Social Requirements**:
...
```

### Feature Type → Growth Focus Matrix

| Feature Type | SEO Focus | Social Focus | CRO Focus |
|--------------|-----------|--------------|-----------|
| New landing page | High (meta, structure, schema) | High (OG, share text) | High (CTA, trust) |
| Feature page | Medium (meta, internal links) | Medium (OG) | Medium (adoption CTA) |
| Dashboard/App page | Low (noindex often) | Low | Medium (engagement) |
| Blog/Content | High (all SEO) | High (all social) | Medium (email signup) |
| Checkout flow | Low (noindex) | Low | Critical (friction removal) |
| Settings page | Low | Low | Low |
