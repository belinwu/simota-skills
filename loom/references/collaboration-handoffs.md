# Collaboration Handoffs

パートナーエージェントとのハンドオフテンプレート集。各パターンの入力/出力フォーマットを定義。

---

## Handoff Overview

```
              ┌─────────────────────────────────────────┐
              │            INPUT PROVIDERS               │
              │  Muse → Token definitions                │
              │  Frame → Figma Variables, design context  │
              │  Artisan → Component patterns             │
              │  Vision → Design direction                │
              └──────────────────┬──────────────────────┘
                                 ↓
                       ┌─────────────────┐
                       │      Loom       │
                       │  Guidelines &   │
                       │  Make Optimizer  │
                       └────────┬────────┘
                                ↓
              ┌─────────────────────────────────────────┐
              │           OUTPUT CONSUMERS               │
              │  User ← Guidelines.md, prompts, reports  │
              │  Frame ← MCP extraction requests         │
              │  Muse ← Token drift reports              │
              │  Artisan ← Make-to-production context    │
              │  Showcase ← Story requests               │
              └─────────────────────────────────────────┘
```

---

## Pattern A: Token Sync Check (Muse → Loom)

### When
Muse がトークン定義を更新した後、Figma Variables との整合性を確認する必要がある時。

### Input (from Muse)

```yaml
MUSE_TO_LOOM_HANDOFF:
  Type: token_sync_request
  Trigger: "Token definitions updated, alignment check needed"
  Payload:
    token_source:
      format: [css-vars | tailwind | panda-css | style-dictionary]
      files:
        - path: [file path]
          changes: [new | modified | deleted]
    scope: [colors | spacing | typography | shadows | all]
    tokens_changed:
      - name: [token name]
        old_value: [previous value or null if new]
        new_value: [current value]
        category: [color | spacing | typography | shadow | border]
    figma_file_url: [optional — Figma file URL for Variables comparison]
```

### Output (to Muse)

```yaml
LOOM_TO_MUSE_HANDOFF:
  Type: token_drift_report
  Summary: "[N] token alignment issues found ([P0]: [n], [P1]: [n])"
  Report:
    alignment_rate: [XX%]
    issues:
      - token: [code token name]
        figma_variable: [Figma variable name]
        type: [VALUE_MISMATCH | MISSING_IN_FIGMA | NAME_DRIFT | ...]
        priority: [P0 | P1 | P2 | P3]
        code_value: [value]
        figma_value: [value]
        recommendation: [具体的な修正提案]
    guidelines_impact: [Guidelines.mdへの影響と必要な更新]
  Next: [Muse | DONE]
```

---

## Pattern B: Design Context Bridge (Frame → Loom)

### When
Frame が Figma ファイルからデザインコンテキストを抽出した後、Guidelines.md の生成/更新に使用する時。

### Input (from Frame)

```yaml
FRAME_TO_LOOM_HANDOFF:
  Type: design_context_delivery
  Trigger: "Design context extracted for Guidelines generation"
  Payload:
    figma_file:
      url: [Figma file URL]
      name: [file name]
      version: [version number or last modified date]
    variables:
      collections:
        - name: [collection name]
          modes: [mode names]
          variables:
            - name: [variable name]
              type: [COLOR | FLOAT | STRING | BOOLEAN]
              values: { [mode]: [value] }
    components:
      - name: [component name]
        properties:
          - name: [property name]
            type: [VARIANT | BOOLEAN | TEXT | INSTANCE_SWAP]
            options: [values]
        auto_layout:
          direction: [HORIZONTAL | VERTICAL]
          gap: [value]
          padding: [top, right, bottom, left]
    styles:
      colors: [color style list]
      text: [text style list]
      effects: [effect style list]
    screenshots:
      - node_id: [node ID]
        description: [what it shows]
```

### Output (back to Frame, if needed)

```yaml
LOOM_TO_FRAME_HANDOFF:
  Type: extraction_request
  Trigger: "Additional Figma data needed for Guidelines"
  Request:
    action: [get_variable_defs | get_design_context | get_screenshot]
    target:
      file_url: [Figma file URL]
      node_ids: [specific nodes, if applicable]
    reason: [why this data is needed]
    priority: [high | medium | low]
```

---

## Pattern C: Component Pattern Feed (Artisan → Loom)

### When
Artisan が実装済みコンポーネントのパターン情報を提供し、Guidelines.md にエンコードする時。

### Input (from Artisan)

```yaml
ARTISAN_TO_LOOM_HANDOFF:
  Type: component_pattern_feed
  Trigger: "Component patterns ready for Guidelines encoding"
  Payload:
    components:
      - name: [ComponentName]
        file_path: [source file path]
        framework: [React | Vue | Svelte]
        props:
          - name: [prop name]
            type: [string | boolean | enum]
            values: [possible values]
            default: [default value]
        variants:
          - name: [variant name]
            description: [when to use]
        composition:
          children: [child component names]
          slots: [named slots]
        styling:
          approach: [css-modules | tailwind | css-in-js | styled-components]
          tokens_used: [list of design tokens referenced]
```

### Output (to Artisan)

```yaml
LOOM_TO_ARTISAN_HANDOFF:
  Type: make_to_production_context
  Trigger: "Figma Make output validated, ready for production implementation"
  Payload:
    validation_result:
      score: [XX%]
      verdict: [PASS | CONDITIONAL | REVISE | REBUILD]
    component_mapping:
      - figma_component: [Figma component name]
        code_component: [matching code component name]
        props_mapping:
          - figma_property: [Figma variant property]
            code_prop: [React/Vue prop name]
            values_mapping: { [figma_value]: [code_value] }
    guidelines_reference: [Guidelines.md path/version]
    implementation_notes:
      - [注意事項: Figma Make出力とコードの差異など]
```

---

## Pattern D: Direction Alignment (Vision → Loom)

### When
Vision がデザイン方針を策定した後、Guidelines.md のトーンと優先度に反映する時。

### Input (from Vision)

```yaml
VISION_TO_LOOM_HANDOFF:
  Type: design_direction
  Trigger: "Design direction established, encode in Guidelines"
  Payload:
    direction:
      style: [modern-minimal | bold-playful | enterprise-professional | ...]
      priorities:
        - [priority 1: e.g., "accessibility first"]
        - [priority 2: e.g., "mobile-first responsive"]
        - [priority 3: e.g., "consistent spacing rhythm"]
      constraints:
        - [constraint 1: e.g., "max 3 colors per screen"]
        - [constraint 2: e.g., "no shadows on mobile"]
      mood_keywords: [clean, spacious, trustworthy, ...]
      reference_designs: [URLs or descriptions]
```

### Output (to Vision)

```yaml
LOOM_TO_VISION_HANDOFF:
  Type: guidelines_direction_confirmation
  Summary: "Design direction encoded in Guidelines v[X.Y.Z]"
  Encoded_as:
    - direction_rule: [how the direction was translated to Guidelines rules]
    - priority_mapping: [how priorities influence token/component choices]
    - constraint_enforcement: [how constraints are codified]
  Open_questions:
    - [areas where direction needs clarification]
```

---

## Pattern E: Story Request (Loom → Showcase)

### When
Figma Make で生成されたコンポーネントの Storybook ドキュメント化が必要な時。

### Output (to Showcase)

```yaml
LOOM_TO_SHOWCASE_HANDOFF:
  Type: story_request
  Trigger: "Make-generated component needs Storybook documentation"
  Payload:
    component:
      name: [ComponentName]
      source: "Figma Make generation"
      guidelines_version: [X.Y.Z]
    variants:
      - name: [variant]
        props: { [prop]: [value] }
        description: [when to use]
    stories_needed:
      - default: "Default state with recommended props"
      - variants: "All variant combinations"
      - states: "Interactive states (hover, focus, disabled)"
      - responsive: "Mobile/Tablet/Desktop views"
    validation_score: [XX%]
    notes: [Figma Make出力からの実装時の注意事項]
```

---

## Nexus Integration

### AUTORUN Handoff Format

Nexus AUTORUN チェーン内で使用するハンドオフ：

```yaml
_STEP_COMPLETE:
  Agent: Loom
  Status: SUCCESS
  Output:
    guidelines:
      - path: "guidelines.md"
        version: "1.0.0"
        scope: "full"
    validation:
      - score: 85
        verdict: "CONDITIONAL"
        issues: 3
  Handoff:
    Format: LOOM_TO_ARTISAN_HANDOFF
    Content:
      validation_result:
        score: 85
        verdict: CONDITIONAL
      component_mapping: [...]
      implementation_notes: [...]
  Artifacts:
    - guidelines.md (v1.0.0)
    - validation-report.md
    - token-alignment-report.md
  Risks:
    - "3 token mismatches require Muse review before production use"
  Next: Artisan
  Reason: "Guidelines validated, ready for Make-to-production implementation"
```

### Hub Mode Handoff

Nexus Hub Mode での返却フォーマット：

```text
## NEXUS_HANDOFF
- Step: [X/Y]
- Agent: Loom
- Summary: [1-3行のサマリー]
- Key findings / decisions:
  - Guidelines v[X.Y.Z] generated with [scope] scope
  - Token alignment rate: [XX%]
  - Validation score: [XX%] ([verdict])
  - [重要な発見事項]
- Artifacts (files/commands/links):
  - guidelines.md (v[X.Y.Z])
  - validation-report.md
  - token-alignment-report.md
  - prompt-sequence.md (if applicable)
- Risks / trade-offs:
  - [トークン不整合のリスク]
  - [検証で発見された問題]
- Open questions (blocking/non-blocking):
  - [blocking: 未解決の重要な問題]
  - [non-blocking: 改善提案]
- Pending Confirmations:
  - Trigger: [INTERACTION_TRIGGER if any]
  - Question: [ユーザーへの質問]
  - Options: [選択肢]
  - Recommended: [推奨選択肢]
- User Confirmations:
  - Q: [以前の質問] → A: [ユーザーの回答]
- Suggested next agent: [AgentName] (reason)
- Next action: CONTINUE | VERIFY | DONE
```

---

## Handoff Quality Checklist

すべてのハンドオフに適用：

- [ ] Type フィールドがハンドオフの目的を明確に示している
- [ ] Payload に受信側が処理に必要な全データが含まれている
- [ ] 不足データがある場合は明示的に「不明」「要確認」と記載
- [ ] Summary が1-3行で全体像を伝えている
- [ ] Next agent が指定されている（該当する場合）
- [ ] Risks が具体的で、影響範囲と緩和策を含む
