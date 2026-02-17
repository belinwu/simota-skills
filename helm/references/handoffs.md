# Handoffs Reference — Helm

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

## Helm への入力ハンドオフ (→ Helm)

### COMPETE_TO_HELM

```yaml
payload:
  competitive_landscape:
    market_leader: "string"
    our_position: "Leader | Challenger | Nicher | Follower"
    direct_competitors:
      - { name: "string", estimated_revenue: "¥Xm", market_share: "X%", key_strengths: ["string"], key_weaknesses: ["string"], recent_moves: "string" }
    indirect_competitors:
      - { name: "string", threat_level: "HIGH | MEDIUM | LOW" }
  identified_opportunities:
    - { opportunity: "string", estimated_market_size: "¥Xm", timeline: "SHORT | MID | LONG", confidence: "HIGH | MEDIUM | LOW" }
  identified_threats:
    - { threat: "string", probability: "HIGH | MEDIUM | LOW", impact: "HIGH | MEDIUM | LOW", timeline: "SHORT | MID | LONG" }
  differentiation_gaps:
    - { gap: "string", vs_competitor: "string", strategic_importance: "HIGH | MEDIUM | LOW" }
  recommended_focus: { primary: "string", reasoning: "string" }
simulation_request:
  priority_horizon: "SHORT | MID | LONG | ALL"
  key_question: "string"
  specific_scenarios: ["市場拡大シナリオ", "競合対抗シナリオ"]
  output_format: "ROADMAP | KPI_FORECAST | RISK_MATRIX | ALL"
```

### PULSE_TO_HELM

```yaml
payload:
  current_kpis:
    revenue: { mrr: "¥Xm", arr: "¥Xm", growth_rate_mom: "X%", growth_rate_yoy: "X%" }
    customers: { total: X, new_per_month: X, churned_per_month: X, churn_rate_mrr: "X%", churn_rate_logo: "X%" }
    unit_economics: { arpu: "¥X", cac: "¥X", ltv: "¥X", ltv_cac_ratio: "X.X", payback_months: X }
    efficiency: { gross_margin: "X%", operating_margin: "X%", nps: XX, csat: "X%" }
  trend_analysis:
    direction: "IMPROVING | STABLE | DECLINING"
    key_concern: "string"
    positive_signals: ["string"]
    negative_signals: ["string"]
  kpi_targets:
    set_by: "Management | Board | Investor"
    targets: { mrr_target_12m: "¥Xm", churn_target: "X%", growth_rate_target: "X%" }
simulation_request:
  priority_horizon: "SHORT | MID"
  key_question: "string"
  gap_analysis_required: true
```

### VOICE_TO_HELM

```yaml
payload:
  feedback_summary: { data_sources: ["NPS調査", "カスタマーインタビュー", "サポートチケット"], sample_size: X, time_period: "YYYY-MM〜YYYY-MM" }
  key_insights:
    top_pain_points:
      - { pain: "string", frequency: "X%", severity: "HIGH | MEDIUM | LOW", strategic_implication: "string" }
    top_desires:
      - { desire: "string", frequency: "X%", willingness_to_pay: "HIGH | MEDIUM | LOW" }
    retention_drivers:
      - { driver: "string", impact_score: X }  # 1-10
  customer_segments:
    - { segment: "string", size: "X%", satisfaction: "X/10", churn_risk: "HIGH | MEDIUM | LOW", growth_potential: "HIGH | MEDIUM | LOW" }
  market_signals: { emerging_needs: ["string"], adjacent_opportunities: ["string"] }
simulation_request:
  focus: "PRODUCT_STRATEGY | CUSTOMER_EXPANSION | RETENTION"
  horizon: "MID | LONG"
```

### BRIDGE_TO_HELM

```yaml
payload:
  business_context: { stakeholder: "CEO | CFO | Board | Investor", urgency: "IMMEDIATE | QUARTERLY | ANNUAL", decision_deadline: "YYYY-MM-DD" }
  clarified_requirements:
    strategic_objective: "string"
    success_criteria: ["string"]
    constraints: { budget_cap: "¥Xm", timeline: "X months", risk_tolerance: "HIGH | MEDIUM | LOW" }
    non_goals: ["string"]
  open_questions:
    - { question: "string", impact: "HIGH | MEDIUM | LOW" }
simulation_request:
  frameworks_required: ["SWOT", "PESTLE", "Porter"]
  output_format: "BOARD_PRESENTATION | DETAILED_ROADMAP | QUICK_SUMMARY"
```

---

## Helm からの出力ハンドオフ (Helm →)

### HELM_TO_MAGI

```yaml
simulation_summary:
  horizon_analyzed: "SHORT | MID | LONG | ALL"
  frameworks_used: ["SWOT", "Porter", "Ansoff"]
  scenarios_generated: ["BASELINE", "OPTIMISTIC", "PESSIMISTIC"]
decision_required:
  decision_type: "GO_NO_GO | OPTION_SELECTION | PRIORITY_SETTING | RISK_ACCEPTANCE"
  question: "string"
  options:
    - { option_id: "A", label: "string", expected_return: "¥Xm / X%", risk_level: "HIGH | MEDIUM | LOW", key_assumptions: ["string"], pros: ["string"], cons: ["string"] }
    - { option_id: "B", label: "string", expected_return: "¥Xm / X%", risk_level: "HIGH | MEDIUM | LOW", key_assumptions: ["string"], pros: ["string"], cons: ["string"] }
  helm_preliminary_recommendation: { recommended_option: "A | B", confidence: "HIGH | MEDIUM | LOW", reasoning: "string" }
key_findings:
  - { finding: "string", strategic_implication: "string" }
risks_to_consider:
  - { risk: "string", probability: "HIGH | MEDIUM | LOW", impact: "HIGH | MEDIUM | LOW" }
artifacts:
  - { type: "STRATEGY_ROADMAP | KPI_FORECAST | RISK_MATRIX", location: "string" }
```

### HELM_TO_SCRIBE

```yaml
document_request:
  document_type: "PRD | SRS | BUSINESS_PLAN | BOARD_DECK | INVESTOR_MEMO"
  audience: "Board | Investors | Management | All-hands"
  format: "DETAILED | EXECUTIVE_SUMMARY | PRESENTATION"
  language: "Japanese"
content_to_formalize:
  strategy_summary: "string"
  key_decisions: ["string"]
  action_items: ["string"]
  kpi_targets: {}     # from simulation
  risk_matrix: {}     # from analysis
  timeline: {}        # from roadmap
artifacts_from_helm:
  - { type: "STRATEGY_ROADMAP", content: "string (markdown)" }
  - { type: "KPI_FORECAST_TABLE", content: "string (markdown table)" }
  - { type: "RISK_MATRIX", content: "string (markdown table)" }
special_instructions: { include_assumptions: true, include_sensitivity_analysis: true, executive_summary_required: true, page_limit: "X pages (optional)" }
```

### HELM_TO_CANVAS

```yaml
visualization_requests:
  - { viz_id: "VIZ_01", type: "TIMELINE | FLOWCHART | MATRIX | GRAPH | ROADMAP", title: "string", purpose: "string", data: {}, format: "MERMAID | ASCII | DRAWIO" }
  - { viz_id: "VIZ_02", type: "MATRIX", title: "リスク・機会マトリクス", data: { risks: [...], opportunities: [...] }, format: "ASCII" }
context_for_canvas: { business_context: "string", audience: "Board | Management | Team", style: "FORMAL | CASUAL | TECHNICAL" }
```

### HELM_TO_SHERPA

```yaml
strategy_to_execute:
  strategy_name: "string"
  phases:
    - { phase: "Phase 1", duration: "0-6ヶ月", objective: "string", milestones: ["string"] }
    - { phase: "Phase 2", duration: "6-18ヶ月", objective: "string", milestones: ["string"] }
decomposition_requirements: { step_granularity: "15min | 1hr | 1day", include_dependencies: true, risk_flags: true, commit_points: true }
constraints: { team_size: X, budget: "¥Xm", deadline: "YYYY-MM-DD", technology_constraints: ["string"] }
```

---

## INTERACTION_TRIGGERS

```yaml
ON_DATA_INSUFFICIENT:
  trigger_condition: "シミュレーションに必要なデータが不足している場合"
  timing: "BEFORE_START"
  question: "経営シミュレーションのために最低限の情報が必要です。以下のどちらで進めますか？"
  options:
    - "業界標準値で代替して進める（推奨）"
    - "データを提供する"
    - "最小限のデータで方向性だけ確認したい"

ON_HORIZON_AMBIGUOUS:
  trigger_condition: "分析する時間軸が不明確な場合"
  timing: "BEFORE_START"
  question: "どの時間軸を優先してシミュレーションを実施しますか？"
  options:
    - "短期（0-1年）— 来期の予算・目標設定（推奨）"
    - "中期（1-3年）— 成長戦略・市場ポジション設計"
    - "長期（3-10年）— ビジョン・M&A・Exit戦略"
    - "全時間軸（総合戦略）"

ON_STRATEGY_CHOICE:
  trigger_condition: "複数の有望な戦略オプションが並立し、どれも実行可能な場合"
  timing: "ON_DECISION"
  question: "以下の戦略オプションが同等の実行可能性を持っています。どの方向を優先しますか？"
  options:  # dynamically populated
    - "[オプションA] — リスク低・リターン中"
    - "[オプションB] — リスク中・リターン高"
    - "Helmの推奨に従う"

ON_IRREVERSIBLE_DECISION:
  trigger_condition: "M&A・Exit・大規模設備投資など元に戻せない意思決定を含む分析"
  timing: "ON_DECISION"
  question: "この分析は高リスクな意思決定を含みます。どのように進めますか？"
  options:
    - "Magiへ意思決定を委譲する（推奨）"
    - "Helmの分析のみ実施（判断は別途）"
    - "シナリオ分析のみ（コミットメントなし）"
```
