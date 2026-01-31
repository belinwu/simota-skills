# Scout Interaction Triggers Reference

Question templates for user confirmation at key decision points.

## Trigger Overview

| Trigger | Timing | When to Ask |
|---------|--------|-------------|
| BEFORE_PRODUCTION_DATA | BEFORE_START | Reproduction requires production data access |
| ON_SECURITY_RISK | ON_DECISION | Bug might be a security vulnerability |
| ON_INFRA_CHANGE | ON_DECISION | Investigation requires infrastructure changes |
| ON_BUILDER_HANDOFF | ON_COMPLETION | Ready to hand off to Builder for fix |
| ON_BISECT_FOUND | ON_DISCOVERY | Git bisect identified the problematic commit |
| ON_SENTINEL_HANDOFF | ON_DECISION | When handing off security issue to Sentinel |
| ON_RADAR_HANDOFF | ON_COMPLETION | When requesting regression tests |
| ON_CANVAS_REQUEST | ON_COMPLETION | When requesting visualization |
| ON_DEEP_DIVE_REQUEST | ON_DECISION | When receiving investigation request from other agents |
| ON_CONFLICT_INVESTIGATION | ON_DECISION | When analyzing merge conflict from Guardian |

---

## Question Templates

### BEFORE_PRODUCTION_DATA
```yaml
questions:
  - question: "Reproduction requires production data access. How would you like to proceed?"
    header: "Data Access"
    options:
      - label: "Use mock data (Recommended)"
        description: "Safely proceed investigation with mock data"
      - label: "Access production data"
        description: "Investigate with real data (caution required)"
      - label: "Skip this investigation"
        description: "Move to next step without data access"
    multiSelect: false
```

### ON_SECURITY_RISK
```yaml
questions:
  - question: "Potential security vulnerability detected. How would you like to proceed?"
    header: "Security"
    options:
      - label: "Audit with Sentinel (Recommended)"
        description: "Request security specialist agent to verify"
      - label: "Continue with awareness"
        description: "Continue investigation at own risk"
      - label: "Suspend investigation"
        description: "Stop investigation for safety"
    multiSelect: false
```

### ON_INFRA_CHANGE
```yaml
questions:
  - question: "Investigation requires infrastructure changes. Continue?"
    header: "Infra Change"
    options:
      - label: "Check with Gear (Recommended)"
        description: "Request infrastructure specialist agent to verify"
      - label: "Execute changes"
        description: "Proceed with necessary infrastructure changes"
      - label: "Skip this investigation"
        description: "Move to next step without infra changes"
    multiSelect: false
```

### ON_BUILDER_HANDOFF
```yaml
questions:
  - question: "Investigation complete. Would you like to request Builder for the fix?"
    header: "Handoff"
    options:
      - label: "Request Builder (Recommended)"
        description: "Hand off investigation results to Builder for fix"
      - label: "Continue investigation"
        description: "Continue investigation due to remaining unknowns"
      - label: "Report only"
        description: "Output investigation report and finish"
    multiSelect: false
```

### ON_BISECT_FOUND
```yaml
questions:
  - question: "Git bisect identified the problematic commit. How would you like to proceed?"
    header: "Bisect Result"
    options:
      - label: "Continue detailed analysis (Recommended)"
        description: "Analyze changes in identified commit in detail"
      - label: "Report to Builder immediately"
        description: "Hand off commit info to Builder for fix"
      - label: "Investigate impact scope"
        description: "Expand investigation to check for similar issues"
    multiSelect: false
```

---

## Collaboration Trigger Templates

### ON_SENTINEL_HANDOFF
```yaml
questions:
  - question: "Security vulnerability detected. How should we proceed?"
    header: "Security"
    options:
      - label: "Handoff to Sentinel (Recommended)"
        description: "Request security audit of vulnerability"
      - label: "Continue investigation"
        description: "Gather more evidence before handoff"
      - label: "Report and proceed to Builder"
        description: "Document risk and proceed with fix"
    multiSelect: false
```

### ON_RADAR_HANDOFF
```yaml
questions:
  - question: "Bug fix verified. Request regression tests from Radar?"
    header: "Regression"
    options:
      - label: "Request Radar tests (Recommended)"
        description: "Add regression tests to prevent recurrence"
      - label: "Skip regression tests"
        description: "Proceed without new tests"
      - label: "Manual test only"
        description: "Document manual verification steps"
    multiSelect: false
```

### ON_CANVAS_REQUEST
```yaml
questions:
  - question: "Complex bug flow identified. Request visualization from Canvas?"
    header: "Visualization"
    options:
      - label: "Request diagram (Recommended)"
        description: "Generate Mermaid/ASCII diagram for documentation"
      - label: "Skip visualization"
        description: "Proceed with text-only report"
      - label: "Create simple ASCII inline"
        description: "Include basic ASCII diagram in report"
    multiSelect: false
```

### ON_DEEP_DIVE_REQUEST
```yaml
questions:
  - question: "Technical investigation request received. What scope?"
    header: "Investigation"
    options:
      - label: "Full investigation (Recommended)"
        description: "Complete root cause analysis with report"
      - label: "Quick assessment"
        description: "Rapid triage with key findings only"
      - label: "Targeted analysis"
        description: "Focus on specific aspect only"
    multiSelect: false
```

### ON_CONFLICT_INVESTIGATION
```yaml
questions:
  - question: "Merge conflict investigation requested. How to proceed?"
    header: "Conflict"
    options:
      - label: "Analyze both changes (Recommended)"
        description: "Investigate intent and impact of both branches"
      - label: "Prioritize target branch"
        description: "Focus on preserving target branch changes"
      - label: "Prioritize source branch"
        description: "Focus on preserving source branch changes"
    multiSelect: false
```

---

## Usage Notes

- Use `AskUserQuestion` tool to present these options
- See `_common/INTERACTION.md` for standard interaction patterns
- Always include recommended option first
- Explain implications of each choice
