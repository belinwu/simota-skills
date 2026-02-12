# Interaction Triggers

YAML question templates for Magi's `AskUserQuestion` decision points. See `_common/INTERACTION.md` for standard formats.

---

## ON_DECISION_SCOPE

```yaml
questions:
  - question: "どのタイプの意思決定として審議しますか？"
    header: "Decision Type"
    options:
      - label: "アーキテクチャ判断 (推奨)"
        description: "システム設計、技術スタック、パターン選択の判断"
      - label: "トレードオフ解決"
        description: "競合する品質属性間のバランス判断"
      - label: "Go/No-Go判定"
        description: "リリース可否、機能承認の判定"
      - label: "戦略的意思決定"
        description: "Build vs Buy、投資 vs 延期の判断"
    multiSelect: false
```

## ON_CONTEXT_INSUFFICIENT

```yaml
questions:
  - question: "審議に必要な情報が不足しています。どのように進めますか？"
    header: "Context Gap"
    options:
      - label: "追加情報を提供する (推奨)"
        description: "不足している情報を共有してから審議を開始"
      - label: "仮定を置いて進行"
        description: "安全な仮定を文書化して審議を進行"
      - label: "スコープを絞る"
        description: "判断範囲を限定して審議可能な部分のみ評価"
    multiSelect: false
```

## ON_SPLIT_VERDICT

```yaml
questions:
  - question: "三視点で意見が分かれました。どの方針で進めますか？"
    header: "Split Vote"
    options:
      - label: "[Logos の推奨]"
        description: "技術的観点: [根拠要約] (信頼度: X)"
      - label: "[Pathos の推奨]"
        description: "人間中心的観点: [根拠要約] (信頼度: X)"
      - label: "[Sophia の推奨]"
        description: "戦略的観点: [根拠要約] (信頼度: X)"
    multiSelect: false
```

## ON_UNANIMOUS_REJECT

```yaml
questions:
  - question: "全視点が否決しました。どのように進めますか？"
    header: "Rejected"
    options:
      - label: "否決を受け入れる (推奨)"
        description: "提案を取り下げ、代替アプローチを検討"
      - label: "条件付きで再審議"
        description: "制約を変更して再度審議を実施"
      - label: "リスク受容で強行"
        description: "リスクを文書化した上でユーザー判断で進行"
    multiSelect: false
```

## ON_IRREVERSIBLE_ACTION

```yaml
questions:
  - question: "この判断は取り消し困難です。審議結果に基づいて進めますか？"
    header: "Irreversible"
    options:
      - label: "審議結果通りに進行 (推奨)"
        description: "Magiの審議結果に従って実行"
      - label: "可逆な代替案を検討"
        description: "段階的・可逆的なアプローチを探る"
      - label: "判断を保留"
        description: "追加情報を集めてから再審議"
    multiSelect: false
```

## ON_MODE_SELECTION

```yaml
questions:
  - question: "Which deliberation mode should be used?"
    header: "Mode"
    options:
      - label: "Simple Mode (Recommended)"
        description: "Internal deliberation via Logos/Pathos/Sophia three perspectives (fast, low cost)"
      - label: "Engine Mode"
        description: "External deliberation via Claude/Codex/Gemini three engines (high diversity, higher cost)"
      - label: "Auto"
        description: "System auto-selects based on decision importance and reversibility"
    multiSelect: false
```

## ON_DOMAIN_OVERLAP

Use ON_DECISION_SCOPE template with adjusted options reflecting the overlapping domains detected. Present each candidate domain as an option with its relevance rationale.
