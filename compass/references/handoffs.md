# Handoffs Reference — Compass

エージェント間ハンドオフテンプレート（YAML形式）。

## Generic Handoff Header (共通)

```yaml
handoff_header:
  version: "1.0"
  from_agent: "[Agent]"
  to_agent: "[Agent]"
  timestamp: "YYYY-MM-DDTHH:MM:SSZ"
  context:
    trigger: "[string]"
    priority: "HIGH | MEDIUM | LOW"
```

以下の各ハンドオフでは共通ヘッダを省略し、payloadスキーマのみ記載する。

---

## Compass への入力ハンドオフ (→ Compass)

### HELM_TO_COMPASS

```yaml
payload:
  strategy_roadmap:
    strategy_name: "string"
    time_horizon: "SHORT | MID | LONG"
    phases:
      - phase: "Phase 1"
        duration: "0-6ヶ月"
        objective: "string"
        milestones:
          - { name: "string", due_date: "YYYY-MM-DD", weight: "HIGH | MEDIUM | LOW", success_criteria: "string" }
        kpi_targets:
          - { kpi: "string", target: "number | string", measurement: "string" }
  assumptions:
    - id: "A-001"
      text: "string"
      category: "MARKET | CUSTOMER | FINANCIAL | TECHNOLOGY | REGULATORY"
      linked_metric: "string"
      threshold:
        green: "string"
        yellow: "string"
        red: "string"
        black: "string"
  strategic_objectives:
    - { objective: "string", priority: "HIGH | MEDIUM | LOW", time_bound: "YYYY-MM-DD" }
  scenario_context:
    active_scenario: "BASELINE | OPTIMISTIC | PESSIMISTIC"
    key_drivers: ["string"]
monitoring_request:
  scope: "FULL | MILESTONES_ONLY | ASSUMPTIONS_ONLY | OKR_ONLY"
  frequency: "WEEKLY | MONTHLY | QUARTERLY"
  alert_recipients: ["Helm", "Sherpa", "Magi"]
```

### PULSE_TO_COMPASS

```yaml
payload:
  kpi_actuals:
    period: "YYYY-MM"
    metrics:
      - { kpi: "string", value: "number", previous_value: "number", target: "number", unit: "string" }
  trend_data:
    - { kpi: "string", values: [{ period: "YYYY-MM", value: "number" }] }
  anomalies:
    - { kpi: "string", type: "SPIKE | DROP | FLATLINE", magnitude: "X%", detected_at: "YYYY-MM-DD" }
  data_quality:
    completeness: "X%"
    freshness: "YYYY-MM-DD"
    reliability: "HIGH | MEDIUM | LOW"
```

### COMPETE_TO_COMPASS

```yaml
payload:
  market_signals:
    - signal: "string"
      type: "COMPETITOR_MOVE | MARKET_SHIFT | REGULATION | TECHNOLOGY"
      impact_on_assumptions:
        - { assumption_id: "A-XXX", impact: "VALIDATES | CHALLENGES | INVALIDATES", evidence: "string" }
      urgency: "HIGH | MEDIUM | LOW"
  competitive_landscape_change:
    summary: "string"
    affected_strategies: ["string"]
```

### REFRACT_TO_COMPASS

```yaml
payload:
  perspective_insights:
    theme: "string"
    assumptions_to_reconsider:
      - assumption_id: "A-XXX"
        original_frame: "string"
        alternative_perspective: "string"
        recommended_action: "RE_EVALUATE | MONITOR_CLOSELY | NO_CHANGE"
    blind_spots_in_monitoring:
      - area: "string"
        insight: "string"
        suggested_metric: "string"
```

---

## Compass からの出力ハンドオフ (Compass →)

### COMPASS_TO_HELM

```yaml
monitoring_report:
  overall_status: "GREEN | YELLOW | RED | BLACK"
  drift_score: "X.X"
  period: "YYYY-MM-DD"
revision_triggers:
  - trigger_type: "ASSUMPTION_BREACH | MILESTONE_DELAY | KPI_MISS | MULTI_BREACH"
    severity: "YELLOW | RED | BLACK"
    details:
      - { item: "string", expected: "string", actual: "string", gap: "X%" }
  assumptions_status:
    total: X
    valid: X
    watch: X
    breach: X
    breached_assumptions:
      - { id: "A-XXX", text: "string", metric: "string", threshold: "string", actual: "string" }
  milestone_status:
    total: X
    on_track: X
    at_risk: X
    delayed: X
    delayed_milestones:
      - { name: "string", due: "YYYY-MM-DD", progress: "X%", delay_days: X }
recommendation:
  action: "MINOR_ADJUSTMENT | STRATEGY_REVISION | SCENARIO_SWITCH | FULL_REPLANNING"
  rationale: "string"
  affected_phases: ["Phase X"]
```

### COMPASS_TO_MAGI

```yaml
escalation_report:
  overall_status: "BLACK"
  trigger: "MULTI_ASSUMPTION_BREACH | STRATEGY_UNACHIEVABLE"
  drift_score: "X.X"
breach_summary:
  breached_assumptions:
    - { id: "A-XXX", text: "string", category: "string", breach_severity: "string" }
  correlation: "COMMON_ROOT_CAUSE | CASCADING | INDEPENDENT"
  root_cause_hypothesis: "string"
impact_assessment:
  strategic_objectives_at_risk: ["string"]
  estimated_impact: "string"
  time_to_critical: "X weeks/months"
pivot_options:
  - { option: "string", feasibility: "HIGH | MEDIUM | LOW", risk: "HIGH | MEDIUM | LOW" }
decision_required:
  question: "string"
  deadline: "YYYY-MM-DD"
  default_action: "string"
```

### COMPASS_TO_SHERPA

```yaml
adjustment_request:
  overall_status: "YELLOW"
  trigger: "KPI_MISS | MILESTONE_DELAY | ASSUMPTION_WATCH"
areas_needing_adjustment:
  - area: "string"
    current_status: "string"
    gap: "X%"
    suggested_adjustment: "string"
    priority: "HIGH | MEDIUM | LOW"
affected_milestones:
  - { name: "string", current_progress: "X%", target_progress: "X%", gap: "X%" }
okr_impacts:
  - { okr: "string", current: "X%", at_risk: true, suggested_focus: "string" }
resource_reallocation:
  suggestion: "string"
  rationale: "string"
```

### COMPASS_TO_SCRIBE

```yaml
document_request:
  document_type: "HEALTH_REPORT | QUARTERLY_REVIEW | DRIFT_ALERT | OKR_STATUS | EXECUTIVE_SUMMARY"
  audience: "Board | Management | Team | All-hands"
  format: "DETAILED | EXECUTIVE_SUMMARY | PRESENTATION"
content:
  health_report: {}     # Strategy Health Report content
  key_findings: ["string"]
  alerts: [{ alert: "string", severity: "string", routing: "string" }]
  recommendations: ["string"]
special_instructions:
  include_trend_charts: true
  include_assumption_details: true
  executive_summary_required: true
```

### COMPASS_TO_CANVAS

```yaml
visualization_requests:
  - viz_id: "VIZ_01"
    type: "DASHBOARD"
    title: "Strategy Health Dashboard"
    data:
      status_indicators: [{ area: "string", status: "G/Y/R/B", score: "X%" }]
      drift_score_history: [{ period: "string", score: "X.X" }]
    format: "MERMAID | ASCII"
  - viz_id: "VIZ_02"
    type: "TIMELINE"
    title: "Milestone Progress Timeline"
    data:
      milestones: [{ name: "string", planned: "YYYY-MM-DD", actual_progress: "X%" }]
    format: "MERMAID"
  - viz_id: "VIZ_03"
    type: "TREE"
    title: "OKR Cascade Tree"
    data:
      okr_tree: {}
    format: "MERMAID"
context_for_canvas:
  business_context: "string"
  audience: "Board | Management | Team"
```

## Compass → Nexus (NEXUS_HANDOFF)

```yaml
## NEXUS_HANDOFF
Step: Compass
Agent: Compass
Summary: "<テーマ>の戦略健全性モニタリング完了。Overall Status: [G/Y/R/B]、Drift Score: X.X"
Key_findings:
  overall_status: "GREEN | YELLOW | RED | BLACK"
  assumptions_valid: "X/Y"
  okr_alignment_score: "XX%"
  drift_score: "X.X"
  alerts_issued:
    - severity: "YELLOW | RED | BLACK"
      target_agent: "[Agent]"
      action: "[アクション]"
Artifacts:
  - strategy-health-report.md
Risks:
  - "<モニタリングで発見されたリスク>"
Open_questions: []
Suggested_next_agent: "<Helm | Magi | Sherpa | Scribe | Canvas>"
Next_action: "<後続エージェントへの具体的な指示>"
```

---

## Nexus → Compass (ルーティング受信)

```yaml
nexus_routing:
  to: Compass
  task_type: STRATEGY_MONITORING
  context:
    user_request: "<ユーザーの元の要求>"
    monitoring_scope: "FULL | MILESTONES | ASSUMPTIONS | OKR | DRIFT"
    helm_roadmap_available: true
    pulse_data_available: true
  expected_output:
    - strategy_health_report (Markdown)
    - handoff_yaml_for: "<後続エージェント名>"
```
