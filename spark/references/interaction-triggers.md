# Interaction Trigger Question Templates

AskUserQuestion tool YAML templates for Spark's decision points.
See `_common/INTERACTION.md` for standard formats.

---

## Core Trigger Templates

### BEFORE_FEATURE_SCOPE

```yaml
questions:
  - question: "What level of feature proposal do you need?"
    header: "Scope"
    options:
      - label: "Small improvement (Recommended)"
        description: "Extend existing functionality or improve UX"
      - label: "New feature"
        description: "Add new capability or workflow"
      - label: "Feature set"
        description: "Multiple related features as a package"
    multiSelect: false
```

### ON_PRIORITY_ASSESSMENT

```yaml
questions:
  - question: "How should we prioritize these features?"
    header: "Priority"
    options:
      - label: "Impact-Effort Matrix (Recommended)"
        description: "Quick visual quadrant analysis"
      - label: "RICE Score"
        description: "Detailed quantitative scoring"
      - label: "Persona Alignment"
        description: "Prioritize by target user needs"
      - label: "All frameworks"
        description: "Comprehensive analysis using all methods"
    multiSelect: false
```

### ON_PERSONA_SELECTION

```yaml
questions:
  - question: "Which user persona should this feature primarily target?"
    header: "Target"
    options:
      - label: "Power User"
        description: "Daily users seeking efficiency and advanced features"
      - label: "Casual User"
        description: "Occasional users needing simplicity"
      - label: "Admin/Manager"
        description: "Users with oversight and control needs"
      - label: "New User"
        description: "First-time users in onboarding phase"
    multiSelect: false
```

### ON_SCOUT_INVESTIGATION

```yaml
questions:
  - question: "Technical investigation needed. How should we proceed?"
    header: "Investigation"
    options:
      - label: "Request Scout investigation (Recommended)"
        description: "Have Scout analyze codebase for feasibility"
      - label: "Assume feasibility"
        description: "Proceed with proposal, note assumptions"
      - label: "Scope down"
        description: "Reduce feature scope to known-feasible parts"
    multiSelect: false
```

---

## Collaboration Trigger Templates

### ON_ECHO_HANDOFF

```yaml
questions:
  - question: "Echo identified latent needs. How should we proceed with feature proposal?"
    header: "Echo Input"
    options:
      - label: "Create proposal for top need (Recommended)"
        description: "Focus on highest-severity latent need"
      - label: "Create proposals for all needs"
        description: "Address multiple needs in prioritized order"
      - label: "Request more detail from Echo"
        description: "Need deeper persona analysis first"
      - label: "Combine with other input sources"
        description: "Wait for Voice/Researcher input before proposing"
    multiSelect: false
```

### ON_RESEARCHER_HANDOFF

```yaml
questions:
  - question: "Researcher provided insights. How should we create feature proposals?"
    header: "Research Input"
    options:
      - label: "Propose features for top pain points (Recommended)"
        description: "Focus on highest-impact research findings"
      - label: "Create persona-specific proposals"
        description: "Tailor proposals to new/updated personas"
      - label: "Address journey stage gaps"
        description: "Focus on journey pain points identified"
      - label: "Request journey map from Researcher"
        description: "Need visual journey context first"
    multiSelect: false
```

### ON_VOICE_HANDOFF

```yaml
questions:
  - question: "Voice aggregated user feedback. How should we prioritize feature proposals?"
    header: "Feedback Input"
    options:
      - label: "Address top feature requests (Recommended)"
        description: "Propose features matching highest-frequency requests"
      - label: "Focus on churn risk signals"
        description: "Prioritize features preventing user churn"
      - label: "Address pain point clusters"
        description: "Create proposals for common pain themes"
      - label: "Cross-reference with other inputs"
        description: "Validate feedback against Echo/Researcher findings"
    multiSelect: false
```

### ON_COMPETE_HANDOFF

```yaml
questions:
  - question: "Compete identified gaps. What differentiation strategy should we pursue?"
    header: "Compete Input"
    options:
      - label: "Close parity gaps (Recommended)"
        description: "Match competitor features users expect"
      - label: "Exploit blue ocean opportunities"
        description: "Build features no competitor has"
      - label: "Strengthen existing advantages"
        description: "Double down on our unique strengths"
      - label: "Defensive positioning"
        description: "Block competitive threats urgently"
    multiSelect: false
```

### ON_PULSE_HANDOFF

```yaml
questions:
  - question: "Pulse provided funnel metrics. What should drive feature proposals?"
    header: "Metrics Input"
    options:
      - label: "Address funnel drop-offs (Recommended)"
        description: "Propose features to improve conversion at weak points"
      - label: "Optimize for engagement metrics"
        description: "Focus on increasing user engagement"
      - label: "Target retention improvements"
        description: "Propose features reducing churn"
      - label: "Revenue-focused features"
        description: "Prioritize features with revenue impact"
    multiSelect: false
```

### ON_EXPERIMENT_REQUEST

```yaml
questions:
  - question: "How should we validate this hypothesis before full implementation?"
    header: "Validation"
    options:
      - label: "A/B test with Experiment (Recommended)"
        description: "Statistical validation with control group"
      - label: "Prototype with Forge first"
        description: "Quick prototype before A/B test"
      - label: "Validate with Echo personas"
        description: "Persona walkthrough instead of A/B test"
      - label: "Skip validation, proceed to implementation"
        description: "High confidence, validation not needed"
    multiSelect: false
```

### ON_EXPERIMENT_RESULT

```yaml
questions:
  - question: "Experiment returned results. What should we do with this hypothesis?"
    header: "Result Action"
    options:
      - label: "Proceed based on verdict (Recommended)"
        description: "Ship if validated, iterate if inconclusive, kill if invalidated"
      - label: "Request deeper analysis"
        description: "Need more data or segment breakdown"
      - label: "Iterate and re-test"
        description: "Modify hypothesis and run new test"
      - label: "Override verdict with justification"
        description: "Proceed despite results (document reasoning)"
    multiSelect: false
```

### ON_VALIDATION_LOOP

```yaml
questions:
  - question: "Echo validated the proposal. What's the next step?"
    header: "Next Step"
    options:
      - label: "Hand off to Sherpa for breakdown (Recommended)"
        description: "Proposal approved, ready for implementation planning"
      - label: "Request Experiment validation"
        description: "Need A/B test before implementation"
      - label: "Iterate on proposal"
        description: "Echo found issues, revise proposal"
      - label: "Hand off to Forge for prototype"
        description: "Need prototype before full implementation"
    multiSelect: false
```

---

## Extended Collaboration Trigger Templates

### ON_PULSE_METRICS

```yaml
questions:
  - question: "Pulse metrics indicate an opportunity. How should we propose the feature?"
    header: "Metrics Approach"
    options:
      - label: "Target highest drop-off (Recommended)"
        description: "Focus on the biggest conversion gap identified"
      - label: "Address trend anomaly"
        description: "Respond to significant metric change"
      - label: "Improve lagging segment"
        description: "Target underperforming user segment"
      - label: "Request deeper analysis"
        description: "Need more data before proposing"
    multiSelect: false
```

### ON_SECURITY_FEATURE

```yaml
questions:
  - question: "This feature has security/privacy implications. How to proceed?"
    header: "Security Review"
    options:
      - label: "Request Sentinel review (Recommended)"
        description: "Get security requirements before finalizing proposal"
      - label: "Include basic security requirements"
        description: "Add standard security criteria to proposal"
      - label: "Scope down to avoid sensitive data"
        description: "Reduce feature scope to minimize security concerns"
      - label: "Flag for security team review"
        description: "Mark proposal as requiring external security review"
    multiSelect: false
```

### ON_GROWTH_HANDOFF

```yaml
questions:
  - question: "This feature may impact SEO/Conversion. Request Growth review?"
    header: "Growth Review"
    options:
      - label: "Request Growth optimization review (Recommended)"
        description: "Get SEO/CRO requirements before implementation"
      - label: "Include basic SEO requirements"
        description: "Add standard meta tags and structure requirements"
      - label: "Skip Growth review"
        description: "Feature has no significant SEO/CRO impact"
    multiSelect: false
```

### ON_SHERPA_FEEDBACK

```yaml
questions:
  - question: "Sherpa raised feasibility concerns. How should we adjust?"
    header: "Scope Adjust"
    options:
      - label: "Reduce to MVP scope (Recommended)"
        description: "Accept Sherpa's recommended scope reduction"
      - label: "Phase into multiple releases"
        description: "Split feature into smaller, phased deliveries"
      - label: "Request Scout investigation"
        description: "Need technical investigation before deciding"
      - label: "Explore alternative approach"
        description: "Consider different implementation strategy"
    multiSelect: false
```

### ON_BUILDER_DIRECT

```yaml
questions:
  - question: "This feature seems simple. Bypass Sherpa and hand off directly to Builder?"
    header: "Direct Handoff"
    options:
      - label: "Direct to Builder (Recommended for simple features)"
        description: "Feature is straightforward, existing patterns apply"
      - label: "Route through Sherpa"
        description: "Want breakdown and risk assessment first"
      - label: "Request Scout feasibility check"
        description: "Verify simplicity assumption before deciding"
    multiSelect: false
```
