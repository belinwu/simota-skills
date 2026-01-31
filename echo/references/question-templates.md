# Echo Question Templates Reference

YAML templates for AskUserQuestion tool at decision points.

## BEFORE_PERSONA_SELECT

```yaml
questions:
  - question: "Which persona should I adopt for this walkthrough?"
    header: "Persona"
    options:
      - label: "Newbie (Recommended)"
        description: "Zero knowledge, easily confused, reads nothing"
      - label: "Accessibility User"
        description: "Screen reader, keyboard-only, color blind simulation"
      - label: "Competitor Migrant"
        description: "Expects patterns from another service"
      - label: "Mobile User"
        description: "Small screen, slow connection, fat fingers"
    multiSelect: false
```

## BEFORE_CONTEXT_SELECT

```yaml
questions:
  - question: "Which usage context should I simulate?"
    header: "Context"
    options:
      - label: "Optimal conditions (Recommended)"
        description: "Focused user, good connection, desktop"
      - label: "Rushing Parent"
        description: "One-handed, distracted, minimal patience"
      - label: "Commuter"
        description: "Unstable, intermittent connection, privacy-aware"
      - label: "Custom context"
        description: "I'll specify the environmental factors"
    multiSelect: false
```

## ON_ACCESSIBILITY_CHECK

```yaml
questions:
  - question: "What level of accessibility check should I perform?"
    header: "A11y Check"
    options:
      - label: "Quick scan (Recommended)"
        description: "Check critical WCAG issues only"
      - label: "Full checklist"
        description: "Run complete WCAG 2.1 AA checklist"
      - label: "Specific disability"
        description: "Focus on one disability type (vision, motor, cognitive)"
    multiSelect: false
```

## ON_COMPETITOR_COMPARISON

```yaml
questions:
  - question: "Which competitor experience should I compare against?"
    header: "Competitor"
    options:
      - label: "Industry standard patterns"
        description: "Compare against common UX conventions"
      - label: "Specific competitor"
        description: "I'll specify which service to compare"
      - label: "No comparison"
        description: "Evaluate this product in isolation"
    multiSelect: false
```

## ON_ANALYSIS_DEPTH

```yaml
questions:
  - question: "What depth of analysis should I perform?"
    header: "Depth"
    options:
      - label: "Standard (Recommended)"
        description: "Emotion scoring, basic friction detection"
      - label: "Deep cognitive"
        description: "Include mental model gaps, cognitive load index"
      - label: "Full behavioral"
        description: "Add bias detection, dark patterns, JTBD analysis"
      - label: "Comprehensive"
        description: "All analysis types including cross-persona"
    multiSelect: false
```

## ON_MULTI_PERSONA

```yaml
questions:
  - question: "Should I run cross-persona comparison analysis?"
    header: "Multi-Persona"
    options:
      - label: "Single persona (Recommended)"
        description: "Focus on one user type for detailed analysis"
      - label: "Core personas (3)"
        description: "Compare Newbie, Power User, and Mobile User"
      - label: "Accessibility focus"
        description: "Compare with Senior and Accessibility personas"
      - label: "Full comparison"
        description: "Run all relevant personas for comprehensive matrix"
    multiSelect: false
```

## ON_UX_FRICTION

```yaml
questions:
  - question: "I found a significant UX friction point. How should I proceed?"
    header: "UX Issue"
    options:
      - label: "Create detailed report (Recommended)"
        description: "Document the issue with emotion scores and suggestions"
      - label: "Continue exploring"
        description: "Check if similar issues exist elsewhere"
      - label: "Prioritize this issue"
        description: "Get guidance on severity before continuing"
    multiSelect: false
```

## ON_DARK_PATTERN

```yaml
questions:
  - question: "I detected a potential dark pattern. How should I proceed?"
    header: "Dark Pattern"
    options:
      - label: "Document and continue (Recommended)"
        description: "Note the pattern with severity rating"
      - label: "Deep analysis"
        description: "Analyze user impact and ethical implications"
      - label: "Immediate escalation"
        description: "Flag as critical issue requiring review"
    multiSelect: false
```

## ON_PALETTE_HANDOFF

```yaml
questions:
  - question: "Significant friction found. Hand off to Palette for interaction fix?"
    header: "Palette"
    options:
      - label: "Yes, hand off to Palette (Recommended)"
        description: "Create detailed handoff for interaction improvement"
      - label: "Document only"
        description: "Document the issue without handoff"
      - label: "Continue walkthrough first"
        description: "Find all issues before any handoffs"
    multiSelect: false
```

## ON_SCOUT_HANDOFF

```yaml
questions:
  - question: "This might be a UI bug, not a design issue. Investigate with Scout?"
    header: "Scout"
    options:
      - label: "Yes, investigate with Scout (Recommended)"
        description: "Technical root cause analysis needed"
      - label: "Treat as UX issue"
        description: "Document as design/UX problem"
      - label: "Flag for later"
        description: "Note the ambiguity and continue"
    multiSelect: false
```

## ON_EXPERIMENT_HANDOFF

```yaml
questions:
  - question: "Generate A/B test hypotheses for Experiment agent?"
    header: "Experiment"
    options:
      - label: "Yes, generate hypotheses (Recommended)"
        description: "Create testable hypotheses from findings"
      - label: "No, findings only"
        description: "Keep as observation without test suggestions"
      - label: "Prioritized hypotheses"
        description: "Generate top 3 most impactful test ideas"
    multiSelect: false
```

## ON_CANVAS_HANDOFF

```yaml
questions:
  - question: "Generate journey visualization with Canvas?"
    header: "Canvas"
    options:
      - label: "Yes, generate journey map (Recommended)"
        description: "Create Mermaid journey diagram for stakeholders"
      - label: "Generate friction heatmap"
        description: "Visualize pain points across flow"
      - label: "Text report only"
        description: "Keep markdown format without visualization"
    multiSelect: false
```

## ON_SPARK_HANDOFF

```yaml
questions:
  - question: "Latent need discovered. Propose feature opportunity to Spark?"
    header: "Spark"
    options:
      - label: "Yes, hand off to Spark (Recommended)"
        description: "Create feature opportunity from JTBD insight"
      - label: "Document in report"
        description: "Include in findings without handoff"
      - label: "Needs more evidence"
        description: "Gather more data before proposing"
    multiSelect: false
```

## ON_VOICE_VALIDATION

```yaml
questions:
  - question: "Validate Echo predictions against real user feedback?"
    header: "Voice"
    options:
      - label: "Yes, validate with Voice (Recommended)"
        description: "Compare simulation vs actual user data"
      - label: "Mark for future validation"
        description: "Note predictions for later comparison"
      - label: "Skip validation"
        description: "Proceed with simulation findings only"
    multiSelect: false
```

## ON_SCORE_SUMMARY

```yaml
questions:
  - question: "Walkthrough complete. Generate Canvas journey visualization?"
    header: "Visualize"
    options:
      - label: "Yes, generate journey map"
        description: "Create Mermaid journey diagram via Canvas"
      - label: "No, text report only"
        description: "Keep the markdown report format"
    multiSelect: false
```

---

## Persona Generation Templates

### ON_PERSONA_GENERATION

```yaml
questions:
  - question: "どのソースからペルソナを生成しますか？"
    header: "Source"
    options:
      - label: "Auto-detect (Recommended)"
        description: "README、docs、srcを自動分析"
      - label: "Documentation only"
        description: "ドキュメントファイルのみ分析"
      - label: "Code only"
        description: "ソースコードのみ分析"
      - label: "Specify files"
        description: "分析対象ファイルを指定"
    multiSelect: false
```

### ON_PERSONA_COUNT

```yaml
questions:
  - question: "何体のペルソナを生成しますか？"
    header: "Count"
    options:
      - label: "3 (Recommended)"
        description: "Primary, Secondary, Edge Case"
      - label: "5"
        description: "より詳細なセグメント分け"
      - label: "Auto"
        description: "発見されたユーザータイプ数に応じて"
    multiSelect: false
```

### ON_PERSONA_SAVE

```yaml
questions:
  - question: "生成されたペルソナを保存しますか？"
    header: "Save"
    options:
      - label: "Yes, save all (Recommended)"
        description: ".agents/personas/{service}/ に保存"
      - label: "Review and edit first"
        description: "内容を確認してから保存"
      - label: "Save selected only"
        description: "一部のペルソナのみ保存"
    multiSelect: false
```

### ON_PERSONA_REVIEW

```yaml
questions:
  - question: "保存済みペルソナでレビューしますか？"
    header: "Persona"
    options:
      - label: "Use saved personas (Recommended)"
        description: ".agents/personas/ から読み込み"
      - label: "Use Echo base personas"
        description: "標準ペルソナを使用"
      - label: "Generate new personas"
        description: "新たにペルソナを生成"
    multiSelect: false
```

### BEFORE_PERSONA_GENERATION

```yaml
questions:
  - question: "サービス特化ペルソナが見つかりません。生成しますか？"
    header: "Persona"
    options:
      - label: "Yes, generate personas (Recommended)"
        description: "コード/ドキュメントから自動生成"
      - label: "Use Echo base personas"
        description: "標準ペルソナでレビューを続行"
      - label: "I'll provide personas"
        description: "手動でペルソナを定義"
    multiSelect: false
```
