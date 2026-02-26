# Handoff Formats

Accordの全ハンドオフ方向のYAMLテンプレート。

---

## Inbound Handoffs（Accord が受け取る）

### RESEARCHER_TO_ACCORD

```yaml
RESEARCHER_TO_ACCORD:
  source: Researcher
  target: Accord
  payload:
    insights:
      user_needs: ["[ユーザーニーズ]"]
      pain_points: ["[ペインポイント]"]
      journey_highlights: ["[ジャーニーの重要ポイント]"]
    personas: ["[ペルソナ名: 概要]"]
    evidence:
      research_method: "[インタビュー/サーベイ/観察]"
      sample_size: "[N]"
    expected_output: "ペルソナ・インサイト反映済み仕様パッケージ"
```

### CAST_TO_ACCORD

```yaml
CAST_TO_ACCORD:
  source: Cast
  target: Accord
  payload:
    personas:
      - name: "[ペルソナ名]"
        role: "[役割]"
        goals: ["[目標]"]
        frustrations: ["[不満]"]
        tech_literacy: "[高/中/低]"
    context:
      persona_source: "[生成/既存レジストリ]"
    expected_output: "L0ターゲットユーザー定義への反映"
```

### VOICE_TO_ACCORD

```yaml
VOICE_TO_ACCORD:
  source: Voice
  target: Accord
  payload:
    feedback:
      nps_score: "[0-10]"
      themes: ["[フィードバックテーマ]"]
      quotes: ["[代表的なユーザー声]"]
    sentiment: "[Positive/Neutral/Negative]"
    expected_output: "フィードバック反映済み仕様パッケージ"
```

---

## Outbound Handoffs（Accord が送る）

### ACCORD_TO_SHERPA

```yaml
ACCORD_TO_SHERPA:
  source: Accord
  target: Sherpa
  payload:
    specification:
      scope: "[Full/Standard/Lite]"
      requirements_count: "[N]"
      priority_breakdown:
        must: ["REQ-001", "REQ-003"]
        should: ["REQ-002"]
        could: ["REQ-005"]
    deliverables:
      l0_vision: "[ビジョン概要]"
      requirements: ["REQ-XXX: 概要"]
    context:
      teams: ["Biz", "Dev", "Design"]
      timeline: "[マイルストーン]"
    expected_output: "Atomic Steps（15分以内の単位）への分解"
```

### ACCORD_TO_BUILDER

```yaml
ACCORD_TO_BUILDER:
  source: Accord
  target: Builder
  payload:
    l2_dev:
      architecture: "[アーキテクチャ概要]"
      apis: ["API-001: 概要"]
      data_models: ["DATA-001: 概要"]
      tradeoffs: ["[選択: 理由]"]
      dependencies: ["[依存先: バージョン]"]
    requirements:
      must: ["REQ-XXX: 実装対象"]
    acceptance_criteria:
      bdd_scenarios: ["AC-XXX: Given-When-Then"]
    context:
      non_functional: { performance: "[基準]", security: "[基準]" }
    expected_output: "L2-Dev に基づく実装"
```

### ACCORD_TO_RADAR

```yaml
ACCORD_TO_RADAR:
  source: Accord
  target: Radar
  payload:
    bdd_scenarios:
      - id: "AC-XXX"
        linked_req: "REQ-XXX"
        given: "[前提条件]"
        when: "[操作]"
        then: "[期待結果]"
    edge_cases:
      - case: "[ケース名]"
        input: "[入力]"
        expected: "[期待動作]"
    coverage_target:
      must_reqs: ["REQ-XXX"]
      scope: "[Full/Standard/Lite]"
    expected_output: "BDDシナリオに基づくテストケース"
```

### ACCORD_TO_VOYAGER

```yaml
ACCORD_TO_VOYAGER:
  source: Accord
  target: Voyager
  payload:
    acceptance_criteria:
      scenarios: ["AC-XXX: Given-When-Then"]
    user_flows:
      - flow: "[フロー名]"
        steps: ["[ステップ1]", "[ステップ2]"]
        branches: ["[分岐条件 → 代替パス]"]
    context:
      target_env: "[ブラウザ/デバイス]"
      a11y_level: "[WCAG AA/AAA]"
    expected_output: "E2Eテストシナリオ"
```

### ACCORD_TO_CANVAS

```yaml
ACCORD_TO_CANVAS:
  source: Accord
  target: Canvas
  payload:
    diagram_requests:
      - type: "[flowchart/sequence/er/state]"
        source: "[L2-Dev/L2-Design/L1]"
        content: "[図解対象の内容]"
    context:
      format: "[Mermaid/ASCII/draw.io]"
      audience: "[Biz/Dev/Design/All]"
    expected_output: "仕様パッケージに埋め込む図解"
```

### ACCORD_TO_SCRIBE

```yaml
ACCORD_TO_SCRIBE:
  source: Accord
  target: Scribe
  payload:
    spec_package:
      scope: "[Full/Standard/Lite]"
      sections_completed: ["L0", "L1", "L2-Dev", "L3"]
    formal_doc_request:
      type: "[PRD/SRS/HLD/LLD]"
      audience: "[経営層/開発チーム/外部クライアント]"
      format: "[Markdown/Word/PDF]"
    context:
      traceability: "[完全/部分的]"
    expected_output: "正式文書（PRD/SRS等）"
```

### ACCORD_TO_LORE

```yaml
ACCORD_TO_LORE:
  source: Accord
  target: Lore
  payload:
    pattern:
      type: "SPECIFICATION_PATTERN"
      context: "[適用コンテキスト]"
      scope: "[Full/Standard/Lite]"
      effectiveness:
        alignment_score: "[High/Medium/Low]"
        revisions: "[修正回数]"
        downstream_adoption: "[採用率]"
      insight: "[発見したパターン]"
      reusable: true
    expected_output: "ナレッジベースへの登録"
```
