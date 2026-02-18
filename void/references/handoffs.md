# Handoff Templates — エージェント間ハンドオフYAML集

Void への入力・Void からの出力ハンドオフ形式。

---

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

## Void への入力ハンドオフ (→ Void)

### SPARK_TO_VOID (Pattern A: Idea Gate)

```yaml
payload:
  feature_proposal:
    name: "<提案機能名>"
    description: "<機能概要>"
    target_users: ["<ユーザーセグメント>"]
    estimated_effort: "S | M | L | XL"
    business_justification: "<ビジネス上の理由>"
  evaluation_request:
    scope: "SINGLE_FEATURE"
    urgency: "HIGH | MEDIUM | LOW"
    context: "<なぜYAGNI検証が必要か>"
```

### SHERPA_TO_VOID (Pattern B: Scope Check)

```yaml
payload:
  task_scope:
    epic_name: "<Epic名>"
    total_steps: X
    estimated_duration: "<時間>"
    scope_items:
      - { item: "<スコープ項目>", priority: "MUST | SHOULD | COULD | WONT" }
  scope_concern:
    reason: "<スコープが広すぎると感じる理由>"
    suggested_cuts: ["<Sherpaが考える不要項目>"]
```

### BUILDER_TO_VOID (Pattern C: Impl Review)

```yaml
payload:
  implementation:
    module: "<モジュール名>"
    files: ["<ファイルパス>"]
    lines_of_code: X
    complexity_metrics:
      cyclomatic: X
      cognitive: X
  review_request:
    concern: "<過剰実装の懸念点>"
    specific_targets: ["<検証したい具体的要素>"]
```

### ATLAS_TO_VOID (Pattern D: Arch Simplify)

```yaml
payload:
  architecture:
    component: "<コンポーネント名>"
    layers: X
    abstractions: ["<抽象化リスト>"]
    patterns_used: ["<使用パターン>"]
  simplification_request:
    over_engineering_suspicion: "<過剰設計の疑い>"
    target_abstractions: ["<検証対象の抽象化>"]
```

### PULSE_TO_VOID (Pattern E: Usage Audit)

```yaml
payload:
  usage_data:
    period: "YYYY-MM-DD to YYYY-MM-DD"
    features:
      - feature: "<機能名>"
        dau: X
        dau_percent: "X%"
        trend: "UP | FLAT | DOWN"
        last_used: "YYYY-MM-DD"
  low_usage_candidates:
    - { feature: "<機能名>", usage_percent: "X%", reason: "<低使用の理由推定>" }
```

### COMPETE_TO_VOID (Pattern F: Compete Trim)

```yaml
payload:
  competitive_analysis:
    our_unique_features:
      - feature: "<機能名>"
        competitors_with_similar: X
        competitors_without: X
        differentiation_value: "HIGH | MEDIUM | LOW | NONE"
  trim_candidates:
    - { feature: "<機能名>", reason: "<競合にもなく差別化価値が低い>" }
```

---

## Void からの出力ハンドオフ (Void →)

### VOID_TO_MAGI (Removal Decision)

```yaml
subtraction_proposal:
  targets:
    - target_name: "<対象名>"
      category: "FEATURE | ABSTRACTION | SCOPE | DEPENDENCY | CONFIGURATION"
      cost_of_keeping: X.X
      removal_risk: X.X
      confidence: "X%"
      recommendation: "REMOVE | SIMPLIFY | DEFER | KEEP-WITH-WARNING"
      blast_radius:
        files: X
        tests: X
        apis: X
        users: "X (estimated)"
      subtraction_pattern: "<パターン名>"
      five_questions_summary:
        who_uses: "<1文>"
        what_breaks: "<1文>"
        last_changed: "YYYY-MM-DD"
        why_built: "<1文>"
        keeping_cost: "<1文>"
decision_required:
  question: "<Magiに判断を求める問い>"
  options:
    - { label: "APPROVE removal", risk: "string" }
    - { label: "APPROVE simplification", risk: "string" }
    - { label: "DEFER decision", risk: "string" }
  default: "APPROVE removal"
```

### VOID_TO_SHERPA (Revised Scope)

```yaml
scope_revision:
  original_scope_items: X
  recommended_cuts:
    - { item: "<項目>", reason: "<カット理由>", cok_score: X.X }
  revised_scope_items: X
  scope_reduction_percent: "X%"
  estimated_time_saved: "<時間>"
instructions_for_sherpa:
  - "revised scope でタスク再分解を実施してください"
  - "カットした項目は backlog に記録してください"
```

### VOID_TO_ZEN (Simplification Targets)

```yaml
simplification_targets:
  - target_name: "<対象名>"
    current_state: "<現在の状態>"
    subtraction_pattern: "ABSTRACTION_COLLAPSE | PATTERN_SIMPLIFICATION"
    specific_action: "<具体的な簡素化アクション>"
    expected_reduction:
      lines: "X lines"
      files: "X files"
      complexity: "X → Y"
    cok_score: X.X
instructions_for_zen:
  - "上記のsimplification targetsに対してリファクタリングを実施してください"
  - "動作を変えずに簡素化してください"
```

### VOID_TO_SWEEP (Deletion Targets)

```yaml
deletion_targets:
  - target: "<ファイル/コード/機能>"
    category: "FEATURE | ABSTRACTION | DEPENDENCY | CONFIGURATION"
    approval_status: "APPROVED_BY_MAGI | VOID_HIGH_CONFIDENCE"
    blast_radius:
      files_to_delete: ["<ファイルパス>"]
      files_to_modify: ["<ファイルパス>"]
      tests_to_update: ["<テストファイル>"]
    rollback_plan: "<ロールバック手順>"
instructions_for_sweep:
  - "deletion_targets のファイル/コードを安全に削除してください"
  - "関連するテスト・インポートも更新してください"
```

### VOID_TO_SCRIBE (Deprecation Docs)

```yaml
deprecation_documentation:
  deprecated_items:
    - item: "<廃止対象>"
      reason: "<廃止理由>"
      alternative: "<代替手段>"
      timeline: "<廃止スケジュール>"
      migration_guide: "<移行手順の概要>"
  document_types_needed:
    - "DEPRECATION_NOTICE"
    - "MIGRATION_GUIDE"
    - "CHANGELOG_ENTRY"
instructions_for_scribe:
  - "上記の廃止対象について、ユーザー向けの告知文書を作成してください"
  - "移行ガイドには具体的な手順を含めてください"
```

---

## Void → Nexus (NEXUS_HANDOFF)

```yaml
## NEXUS_HANDOFF
Step: Void
Agent: Void
Summary: "<テーマ>に対してX対象を評価。REMOVE: X, SIMPLIFY: X, DEFER: X"
Key_findings:
  targets_evaluated: X
  avg_cost_of_keeping: X.X
  recommendations:
    remove: X
    simplify: X
    defer: X
    keep_with_warning: X
  blast_radius_summary: "files: X, tests: X, APIs: X"
Artifacts:
  - subtraction-proposal.md
Risks:
  - "<評価で発見されたリスク>"
Open_questions: []
Suggested_next_agent: "<Magi | Sweep | Zen | Scribe>"
Next_action: "<後続エージェントへの具体的な指示>"
```

---

## Nexus → Void (ルーティング受信)

```yaml
nexus_routing:
  to: Void
  task_type: "YAGNI_CHECK | SCOPE_REDUCTION | COMPLEXITY_AUDIT | FEATURE_PRUNING"
  context:
    user_request: "<ユーザーの元の要求>"
    audit_scope: "PROJECT | MODULE | FEATURE"
    target_hints: ["<対象のヒント>"]
    usage_data_available: true
    downstream_agent_hint: "<Magi | Sweep | Zen | Scribe>"
  expected_output:
    - subtraction_proposal (Markdown)
    - handoff_yaml_for: "<後続エージェント名>"
```
