# Collaboration Handoffs

パートナーエージェントとのハンドオフテンプレート集。コアパターン（A-C）は完全定義、その他は概要のみ。

---

## Handoff Overview

```
              ┌─────────────────────────────────────────┐
              │            INPUT PROVIDERS               │
              │  Muse → Token definitions                │
              │  Frame → Figma Variables, design context  │
              │  Artisan → Component patterns             │
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
              │  Muse ← Token drift reports              │
              │  Artisan ← Make-to-production context    │
              │  Frame ← MCP extraction requests         │
              └─────────────────────────────────────────┘
```

---

## Core Pattern A: Token Sync Check (Muse → Loom)

### When
Muse がトークン定義を更新した後、Figma Variables との整合性を確認する必要がある時。

### Input (from Muse)

```yaml
MUSE_TO_LOOM_HANDOFF:
  Type: token_sync_request
  Payload:
    token_source:
      format: [css-vars | tailwind | panda-css | style-dictionary | w3c-dtcg]
      files:
        - path: [file path]
          changes: [new | modified | deleted]
    scope: [colors | spacing | typography | shadows | all]
    tokens_changed:
      - name: [token name]
        old_value: [previous value or null]
        new_value: [current value]
        category: [color | spacing | typography | shadow | border]
    figma_file_url: [optional]
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
        type: [VALUE_MISMATCH | MISSING_IN_FIGMA | NAME_DRIFT]
        priority: [P0 | P1 | P2 | P3]
        recommendation: [具体的な修正提案]
    guidelines_impact: [Guidelines.mdへの影響と必要な更新]
```

---

## Core Pattern B: Design Context Bridge (Frame → Loom)

### When
Frame が Figma ファイルからデザインコンテキストを抽出した後、Guidelines.md の生成/更新に使用する時。

### Input (from Frame)

```yaml
FRAME_TO_LOOM_HANDOFF:
  Type: design_context_delivery
  Payload:
    figma_file:
      url: [Figma file URL]
      name: [file name]
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
```

### Output (back to Frame, if needed)

```yaml
LOOM_TO_FRAME_HANDOFF:
  Type: extraction_request
  Request:
    action: [get_variable_defs | get_design_context | get_screenshot]
    target:
      file_url: [Figma file URL]
      node_ids: [specific nodes]
    reason: [why needed]
```

---

## Core Pattern C: Component Pattern Feed (Artisan → Loom)

### When
Artisan が実装済みコンポーネントのパターン情報を提供し、Guidelines.md にエンコードする時。

### Input (from Artisan)

```yaml
ARTISAN_TO_LOOM_HANDOFF:
  Type: component_pattern_feed
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
        styling:
          approach: [css-modules | tailwind | css-in-js]
          tokens_used: [list of design tokens]
```

### Output (to Artisan)

```yaml
LOOM_TO_ARTISAN_HANDOFF:
  Type: make_to_production_context
  Payload:
    validation_result:
      score: [XX%]
      verdict: [PASS | CONDITIONAL | REVISE | REBUILD]
    component_mapping:
      - figma_component: [Figma name]
        code_component: [code name]
        props_mapping:
          - figma_property: [Figma variant]
            code_prop: [React/Vue prop]
    guidelines_reference: [version]
    implementation_notes: [注意事項]
```

---

## Additional Patterns (Summary)

| Pattern | Flow | Trigger | Key Data |
|---------|------|---------|----------|
| **D: Direction Alignment** | Vision → Loom | Design direction established | Style, priorities, constraints, mood keywords → encoded as Guidelines rules |
| **E: Story Request** | Loom → Showcase | Make-generated component needs docs | Component name, variants, validation score → Storybook story request |
| **F: Token Drift Report** | Loom → Muse | Alignment audit finds issues | Drift report with priorities → Muse reviews and resolves |
| **G: MCP Delegation** | Loom → Frame | Additional Figma data needed | Extraction request (variables, context, screenshots) → Frame executes MCP calls |
| **H: A11y Compliance** | Loom → Canon | Validation finds a11y concerns | A11y findings → Canon performs WCAG compliance check |
| **I: Reverse Feedback** | Artisan → Loom | Implementation fidelity issues | Fidelity gaps → Loom updates Guidelines to prevent recurrence |
| **J: Quality Gate** | Loom → Warden | Pre-release quality check | Make output + validation report → V.A.I.R.E. assessment |

---

## Nexus Integration

### AUTORUN Step Complete Format

```yaml
_STEP_COMPLETE:
  Agent: Loom
  Status: [SUCCESS | PARTIAL | BLOCKED | FAILED]
  Output:
    guidelines: { path, version, scope }
    validation: { score, verdict, issues }
  Handoff:
    Format: LOOM_TO_[NEXT]_HANDOFF
    Content: [pattern-specific payload]
  Artifacts: [file list]
  Risks: [risk list]
  Next: [agent name]
  Reason: [why next agent]
```

---

## Handoff Quality Checklist

- [ ] Type フィールドがハンドオフの目的を明確に示している
- [ ] Payload に受信側が処理に必要な全データが含まれている
- [ ] Summary が1-3行で全体像を伝えている
- [ ] Next agent が指定されている（該当する場合）
- [ ] Risks が具体的で、影響範囲と緩和策を含む
