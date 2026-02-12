# Compete Interaction Triggers Reference

YAML question templates for `AskUserQuestion` tool at decision points.
See `_common/INTERACTION.md` for standard formats.

## ON_COMPETITOR_SCOPE

```yaml
questions:
  - question: "Please select the scope of competitors to analyze."
    header: "Competitor Scope"
    options:
      - label: "Direct competitors only (Recommended)"
        description: "Focus on 3-5 major companies in the same category"
      - label: "Direct + Indirect competitors"
        description: "Include alternative solutions in analysis"
      - label: "Entire market"
        description: "Include new entrants and adjacent markets"
    multiSelect: false
```

## ON_ANALYSIS_DEPTH

```yaml
questions:
  - question: "Please select the depth of analysis."
    header: "Analysis Depth"
    options:
      - label: "Feature comparison (Recommended)"
        description: "Compare presence and quality of key features"
      - label: "Strategic analysis"
        description: "Analyze business model, target, and pricing strategy"
      - label: "Comprehensive analysis"
        description: "Full picture of features + strategy + market position"
    multiSelect: false
```

## ON_DIFFERENTIATION_STRATEGY

```yaml
questions:
  - question: "Please select the direction of differentiation."
    header: "Differentiation"
    options:
      - label: "Feature differentiation"
        description: "Stand out with unique features"
      - label: "Experience differentiation"
        description: "Stand out with UX and ease of use"
      - label: "Price differentiation"
        description: "Stand out with pricing strategy"
      - label: "Niche focus"
        description: "Focus on specific segment"
    multiSelect: false
```

## ON_SPARK_HANDOFF

```yaml
questions:
  - question: "Competitive gap identified. How should we hand off to Spark?"
    header: "Spark Handoff"
    options:
      - label: "Request feature ideation (Recommended)"
        description: "Ask Spark to propose differentiating features"
      - label: "Share gap info only"
        description: "Share competitive analysis, let Spark decide approach"
      - label: "Technical investigation first"
        description: "Request Scout to assess feasibility before Spark"
    multiSelect: false
```

## ON_GROWTH_HANDOFF

```yaml
questions:
  - question: "Positioning analysis complete. How should we hand off to Growth?"
    header: "Growth Handoff"
    options:
      - label: "Full positioning strategy (Recommended)"
        description: "Provide complete positioning and SEO recommendations"
      - label: "SEO gaps only"
        description: "Focus on keyword and content opportunities"
      - label: "Messaging recommendations only"
        description: "Focus on differentiation messaging"
    multiSelect: false
```

## ON_ALERT_RESPONSE

```yaml
questions:
  - question: "Competitive alert detected. How should we respond?"
    header: "Alert Response"
    options:
      - label: "Activate response chain (Recommended)"
        description: "Impact assessment → Response planning → Execution"
      - label: "Continue monitoring"
        description: "Gather additional information before deciding"
      - label: "No action needed"
        description: "Impact is minimal, observe only"
    multiSelect: false
```

## ON_BENCHMARK_REQUEST

```yaml
questions:
  - question: "Benchmark request received. What comparison scope?"
    header: "Benchmark Scope"
    options:
      - label: "Direct competitors (Recommended)"
        description: "Compare against primary competitors"
      - label: "Industry average"
        description: "Compare against industry benchmarks"
      - label: "Best in class"
        description: "Compare against top performers across industries"
    multiSelect: false
```

## ON_VISUALIZATION_REQUEST

```yaml
questions:
  - question: "Visualization needed. What format?"
    header: "Viz Format"
    options:
      - label: "Mermaid diagram (Recommended)"
        description: "Interactive, version-controllable format"
      - label: "ASCII art"
        description: "Simple text-based visualization"
      - label: "Data for external tool"
        description: "Structured data for Figma/draw.io"
    multiSelect: false
```
