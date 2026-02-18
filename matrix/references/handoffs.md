# Handoff Templates

Matrix と他エージェント間のハンドオフYAMLテンプレート集。

---

## Matrix → Voyager（テストマトリクス）

```yaml
handoff:
  from: Matrix
  to: Voyager
  type: TEST_MATRIX_HANDOFF
  payload:
    matrix_plan:
      domain: test
      name: <マトリクス名>
      optimization_method: pairwise
      coverage_guarantee: "2-way 100%"
      reduction_rate: "67%"
    combinations:
      - id: 1
        priority: HIGH
        params:
          browser: Chrome
          os: Windows
          auth_state: logged_in
        rationale: "最大ユーザー構成、リスク高"
      - id: 2
        priority: HIGH
        params:
          browser: Firefox
          os: macOS
          auth_state: anonymous
        rationale: "未カバーペア補完"
      # ... 続く
    instructions_for_voyager:
      - "各組み合わせを独立したテストスイートとして実装してください"
      - "id順に優先度が高い順です"
      - "実行後、結果をMatrix形式で報告してください"
    result_format:
      - {id: 1, status: "pass|fail|skip", error_message: "任意"}
```

---

## Matrix → Siege（負荷テストマトリクス）

```yaml
handoff:
  from: Matrix
  to: Siege
  type: LOAD_MATRIX_HANDOFF
  payload:
    matrix_plan:
      domain: load
      name: <マトリクス名>
      optimization_method: pairwise
    combinations:
      - id: 1
        priority: HIGH
        params:
          concurrent_users: 100
          data_volume: medium
          endpoint: /api/search
          duration: 5min
        expected_metrics:
          p99_latency_ms: 500
          error_rate_percent: 0.1
      # ... 続く
    safety_limits:
      max_concurrent: 1000
      abort_on_error_rate: 5.0
      abort_on_latency_ms: 10000
```

---

## Matrix → Echo（UX検証マトリクス）

```yaml
handoff:
  from: Matrix
  to: Echo
  type: UX_MATRIX_HANDOFF
  payload:
    matrix_plan:
      domain: ux
      name: <マトリクス名>
    combinations:
      - id: 1
        priority: HIGH
        persona: beginner
        device: mobile
        scenario: first_visit
        focus_points:
          - "オンボーディング完了率"
          - "最初の離脱ポイント"
          - "ヘルプ参照頻度"
      - id: 2
        priority: HIGH
        persona: senior_user
        device: tablet
        scenario: purchase_flow
        focus_points:
          - "操作エラー頻度"
          - "確認ダイアログへの反応"
    persona_detail_request:
      agent: Cast
      note: "各ペルソナの詳細定義はCastに依頼済み"
```

---

## Matrix → Triage/Sentinel（リスクマトリクス）

```yaml
handoff:
  from: Matrix
  to: Triage
  type: RISK_MATRIX_HANDOFF
  payload:
    matrix_plan:
      domain: risk
      name: <マトリクス名>
    risk_items:
      - id: 1
        priority: CRITICAL
        risk_score: 9.8
        threat: SQLi
        attack_surface: API
        auth_level: anonymous
        data_sensitivity: restricted
        action: "P0 — 即時調査・対処"
      - id: 2
        priority: HIGH
        risk_score: 8.5
        threat: XSS
        attack_surface: Web_UI
        auth_level: anonymous
        data_sensitivity: internal
        action: "P0 — 今日中に対処"
    next_steps:
      triage: "P0 リスクの影響範囲を特定してください"
      sentinel: "P0/P1 リスクのコード静的解析を実行してください"
      probe: "P0/P1 リスクの動的テストを実行してください"
```

---

## Matrix → Experiment（実験マトリクス）

```yaml
handoff:
  from: Matrix
  to: Experiment
  type: EXPERIMENT_MATRIX_HANDOFF
  payload:
    matrix_plan:
      domain: experiment
      name: <マトリクス名>
    experiments:
      - id: 1
        priority: HIGH
        variables:
          cta_color: blue
          cta_text: "今すぐ試す"
        user_segment: new_users
        exposure_rate: 10%
        duration: 2weeks
        primary_metric: CVR
        secondary_metrics: [CTR, time_on_page]
    instructions_for_experiment:
      - "各実験のサンプルサイズを計算してください"
      - "フィーチャーフラグの実装仕様を生成してください"
      - "統計的有意性の判定基準を設定してください（p<0.05 推奨）"
```

---

## Matrix → Scaffold（デプロイマトリクス）

```yaml
handoff:
  from: Matrix
  to: Scaffold
  type: DEPLOY_MATRIX_HANDOFF
  payload:
    matrix_plan:
      domain: deploy
      name: <マトリクス名>
    deploy_sequence:
      - step: 1
        environment: staging
        region: ap-northeast-1
        version: v1.5.1
        traffic_split: "100%"
        validation:
          - health_check: /health
          - smoke_test: [/api/users, /api/search]
          - wait_minutes: 5
      - step: 2
        environment: production
        region: ap-northeast-1
        version: v1.5.1
        traffic_split: "10%"
        validation:
          - monitor_minutes: 30
          - error_rate_threshold: 0.1
          - rollback_on_breach: true
    rollback_plan:
      trigger:
        error_rate_percent: 0.5
        p99_latency_ms: 2000
      action: "前バージョンへの即時切り戻し"
```

---

## Matrix → Canvas（可視化依頼）

```yaml
handoff:
  from: Matrix
  to: Canvas
  type: VISUALIZATION_HANDOFF
  payload:
    visualization_type: matrix_heatmap
    data:
      axes: [browser, os, auth_state]
      combinations:
        - {browser: Chrome, os: Windows, auth_state: logged_in, status: included}
        - {browser: Firefox, os: macOS, auth_state: anonymous, status: included}
        - {browser: Safari, os: Windows, auth_state: excluded, status: excluded}
    style:
      included: "✅ 緑"
      excluded: "❌ 赤"
      not_tested: "⬜ グレー"
    output_format: mermaid  # or ascii, drawio
```

---

## Voyager/Siege/Echo → Matrix（結果報告）

```yaml
result_report:
  from: Voyager  # or Siege, Echo, etc.
  to: Matrix
  type: EXECUTION_RESULT
  payload:
    matrix_name: <マトリクス名>
    results:
      - id: 1
        status: pass
      - id: 2
        status: fail
        error: "Safari SSO token expired"
        affected_axes: {browser: Safari, auth_state: sso}
      - id: 3
        status: skip
        reason: "環境構築エラー"
    request: "カバレッジ再計算と未カバーペアの特定をお願いします"
```

---

## Nexus → Matrix（ルーティング）

```yaml
nexus_routing:
  to: Matrix
  task_type: MATRIX_PLANNING
  context:
    user_request: "ユーザーの元の要求"
    domain_hint: test  # Nexusが推定したドメイン
    axes_hint:   # Nexusが抽出した軸のヒント
      - Chrome/Firefox/Safari
      - Windows/macOS
    downstream_agents: [Voyager, Radar]
  expected_output:
    - matrix_plan (YAML)
    - execution_sequence
    - handoff_to: Voyager
```

---

## Matrix の結果サマリー（Nexus Hub モード向け）

```yaml
## NEXUS_HANDOFF
Step: Matrix
Agent: Matrix
Summary: "3軸×12組み合わせをPairwiseで4件に最適化（削減率67%）"
Key_findings:
  - "全2-wayペア（12/12）をカバー"
  - "Safari×Windowsの除外制約を適用"
  - "HIGH優先度: 2件、MEDIUM優先度: 2件"
Artifacts:
  - matrix_plan.yaml
  - coverage_report.md
Risks:
  - "SafariのSSO対応は別途手動確認が必要"
Open_questions: []
Suggested_next_agent: Voyager
Next_action: "Voyagerへテストマトリクスを渡してE2E実装を依頼"
```
