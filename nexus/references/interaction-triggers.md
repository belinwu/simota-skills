# Nexus Interaction Triggers Reference

Question templates for GUIDED/INTERACTIVE modes.

---

## Trigger Summary

| Trigger | Timing | When |
|---------|--------|------|
| ON_CHAIN_DESIGN | BEFORE_START | Confirm chain before execution |
| ON_COMPLEX_OVERRIDE | ON_DECISION | AUTORUN but task is COMPLEX |
| ON_AGENT_ESCALATION | ON_DECISION | Agent reported blocking question |
| ON_CHAIN_ADJUSTMENT | ON_DECISION | Dynamic chain modification |
| ON_PARALLEL_CONFLICT | ON_DECISION | Parallel branches have conflicts |
| ON_GUARDRAIL_L3 | ON_DECISION | L3 guardrail triggered |
| ON_GUARDRAIL_L4 | ON_DECISION | L4 guardrail triggered |
| ON_VERIFICATION_FAILURE | ON_COMPLETION | Final verification failed |
| ON_MULTI_AGENT_CHOICE | ON_DECISION | Multiple agents could handle task |
| ON_PROACTIVE_START | BEFORE_START | /Nexus invoked without arguments |
| ON_ROUTING_EXPLANATION | ON_CHAIN_DESIGN | After chain selection explanation |
| ON_AMBIGUOUS_TASK | ON_CLASSIFICATION | Task classification is unclear |

---

## Question Templates

### ON_CHAIN_DESIGN

```yaml
questions:
  - question: "Recommended chain for this task. Proceed?"
    header: "Chain Design"
    options:
      - label: "Execute as planned (Recommended)"
        description: "[Agent1] → [Agent2] → [Agent3]"
      - label: "Add more agents"
        description: "Include additional verification/documentation"
      - label: "Simplify chain"
        description: "Use minimal agents only"
    multiSelect: false
```

### ON_PARALLEL_CONFLICT

```yaml
questions:
  - question: "Parallel branches have conflicting file changes. How to resolve?"
    header: "Conflict"
    options:
      - label: "Merge sequentially (Recommended)"
        description: "Execute Branch A first, then B with conflict resolution"
      - label: "Prioritize Branch A"
        description: "Keep Branch A changes, discard B conflicts"
      - label: "Prioritize Branch B"
        description: "Keep Branch B changes, discard A conflicts"
      - label: "Manual resolution"
        description: "Pause and request user intervention"
    multiSelect: false
```

### ON_MULTI_AGENT_CHOICE

```yaml
questions:
  - question: "Multiple agents could handle this task. Which to use?"
    header: "Agent Choice"
    options:
      - label: "[Primary Agent] (Recommended)"
        description: "Best fit based on task classification"
      - label: "[Alternative Agent 1]"
        description: "Alternative approach"
      - label: "[Alternative Agent 2]"
        description: "Different methodology"
    multiSelect: false
```

### ON_PROACTIVE_START

```yaml
questions:
  - question: "プロアクティブ分析が完了しました。次のアクションを選択してください。"
    header: "Next Action"
    options:
      - label: "推奨アクション #1 を実行（推奨）"
        description: "[最優先の提案内容とエージェント]"
      - label: "推奨アクション #2 を実行"
        description: "[次の提案内容とエージェント]"
      - label: "前回の作業を継続"
        description: "Activity Log の最終作業を再開"
      - label: "新しいタスクを指示"
        description: "/Nexus [タスク] で新規タスクを開始"
    multiSelect: false
```

### ON_ROUTING_EXPLANATION

```yaml
questions:
  - question: "チェーン構成を確認しました。どのように進めますか？"
    header: "Chain Confirm"
    options:
      - label: "この構成で実行（推奨）"
        description: "[選定されたチェーン]"
      - label: "代替案を見る"
        description: "他のアプローチを検討"
      - label: "チェーンをカスタマイズ"
        description: "エージェントの追加/削除を指定"
    multiSelect: false
```

### ON_AMBIGUOUS_TASK

```yaml
questions:
  - question: "タスクの解釈に複数の可能性があります。どのアプローチで進めますか？"
    header: "Approach"
    options:
      - label: "[アプローチA]（推奨）"
        description: "[Chain A] - [概要]"
      - label: "[アプローチB]"
        description: "[Chain B] - [概要]"
      - label: "[アプローチC]"
        description: "[Chain C] - [概要]"
      - label: "タスクを明確化する"
        description: "より具体的な指示を提供"
    multiSelect: false
```

---

## Handling Pending Confirmations

When Nexus receives a NEXUS_HANDOFF with Pending Confirmations:

1. **Parse the pending confirmation** - Extract trigger, question, options
2. **Present to user using AskUserQuestion** - Convert to proper format
3. **Record user's answer** - Add to User Confirmations
4. **Pass to next agent** - Include User Confirmations in NEXUS_ROUTING

```
Agent → NEXUS_HANDOFF (with Pending Confirmations)
↓
Nexus → AskUserQuestion (present options to user)
↓
User → Selects option
↓
Nexus → NEXUS_ROUTING (with User Confirmations)
↓
Next Agent → Proceeds based on user's decision
```

---

## AUTORUN_FULL Handoff Flow

In AUTORUN_FULL mode, most handoffs are automatic:

```
Agent → NEXUS_HANDOFF (no Pending Confirmations)
↓
Nexus → Check Guardrail Events
↓
├─ L1/L2: Auto-continue
├─ L3: Auto-recover or pause
└─ L4: Abort and rollback
↓
Nexus → Update Context
↓
Next Agent (auto-routed)
```
