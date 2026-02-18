# Handoffs Reference — Totem

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

## Totem への入力ハンドオフ (→ Totem)

### LENS_TO_TOTEM

```yaml
payload:
  investigation_data:
    codebase_path: "string"
    files_analyzed:
      - path: "string"
        language: "string"
        loc: "number"
        last_modified: "YYYY-MM-DD"
    pattern_observations:
      naming:
        - { pattern: "string", frequency: "number", examples: ["string"] }
      structure:
        - { pattern: "string", location: "string", description: "string" }
      error_handling:
        - { pattern: "string", frequency: "number", examples: ["string"] }
    config_files_found:
      - { path: "string", type: "LINTER | FORMATTER | BUILD | TEST | CI", content_summary: "string" }
  investigation_scope:
    directories_covered: ["string"]
    total_files: "number"
    languages_detected: ["string"]
```

### REWIND_TO_TOTEM

```yaml
payload:
  git_history_analysis:
    repository: "string"
    commits_analyzed: "number"
    date_range:
      from: "YYYY-MM-DD"
      to: "YYYY-MM-DD"
    commit_patterns:
      - { format: "conventional | prefix | jira_id | free_form", count: "number", percentage: "X%" }
    contributor_patterns:
      - { contributor: "string", commit_count: "number", primary_style: "string" }
    branch_patterns:
      - { format: "string", count: "number", examples: ["string"] }
    merge_strategy:
      squash_count: "number"
      merge_count: "number"
      rebase_count: "number"
    temporal_changes:
      - { period: "YYYY-MM", pattern_shift: "string", dimension: "N | A | E | C | T | R | G | D" }
```

### JUDGE_TO_TOTEM

```yaml
payload:
  review_context:
    pr_or_commit: "string"
    files_in_review:
      - { path: "string", change_type: "ADD | MODIFY | DELETE", language: "string" }
    request_type: "CULTURAL_GUIDANCE | DEVIATION_CHECK | FULL_PROFILE"
    specific_concerns:
      - { dimension: "N | A | E | C | T | R | G | D", question: "string" }
  existing_profile:
    profile_date: "YYYY-MM-DD"
    available: true
    stale: false
```

### NEXUS_TO_TOTEM

```yaml
nexus_routing:
  to: Totem
  task_type: "CULTURE_PROFILING | DEVIATION_CHECK | ONBOARDING_GUIDE | DRIFT_ANALYSIS"
  context:
    user_request: "string"
    codebase_path: "string"
    scope: "FULL | MODULE | FILE_SET"
    target_modules: ["string"]
    existing_profile_available: true
  expected_output:
    - "dna_profile (Markdown)"
    - "handoff_yaml_for: [target agent]"
```

---

## Totem からの出力ハンドオフ (Totem →)

### TOTEM_TO_JUDGE

```yaml
payload:
  cultural_context:
    project_name: "string"
    profile_date: "YYYY-MM-DD"
    confidence: "HIGH | MEDIUM | LOW"
    dimension_scores:
      - { dim: "N", score: "X/3", confidence: "HIGH | MEDIUM | LOW", dominant_pattern: "string" }
      - { dim: "A", score: "X/3", confidence: "HIGH | MEDIUM | LOW", dominant_pattern: "string" }
      - { dim: "E", score: "X/3", confidence: "HIGH | MEDIUM | LOW", dominant_pattern: "string" }
      - { dim: "C", score: "X/3", confidence: "HIGH | MEDIUM | LOW", dominant_pattern: "string" }
      - { dim: "T", score: "X/3", confidence: "HIGH | MEDIUM | LOW", dominant_pattern: "string" }
      - { dim: "R", score: "X/3", confidence: "HIGH | MEDIUM | LOW", dominant_pattern: "string" }
      - { dim: "G", score: "X/3", confidence: "HIGH | MEDIUM | LOW", dominant_pattern: "string" }
      - { dim: "D", score: "X/3", confidence: "HIGH | MEDIUM | LOW", dominant_pattern: "string" }
    enforced_conventions:
      - { dimension: "N | A | E | C | T | R | G | D", convention: "string", enforcement: "AUTO | TEAM_AGREEMENT" }
    soft_conventions:
      - { dimension: "N | A | E | C | T | R | G | D", convention: "string", adherence: "X%" }
    known_subcultures:
      - { module: "string", deviations: ["string"], legitimate: true }
    active_drift_warnings:
      - { dimension: "string", direction: "EROSION | EVOLUTION", delta: "X.X", period: "string" }
```

### TOTEM_TO_ZEN

```yaml
payload:
  refactoring_guidance:
    project_name: "string"
    cultural_context:
      fingerprint: "string"
      key_conventions:
        - { dimension: "string", convention: "string", score: "X/3" }
    consistency_issues:
      - dimension: "string"
        description: "string"
        affected_files: ["string"]
        current_pattern: "string"
        target_pattern: "string"
        priority: "HIGH | MEDIUM | LOW"
    refactoring_constraints:
      - "string"
    alignment_targets:
      - { dimension: "string", current_score: "X/3", target_score: "X/3" }
```

### TOTEM_TO_SCRIBE

```yaml
payload:
  onboarding_material:
    project_name: "string"
    cultural_fingerprint: "string"
    conventions:
      naming:
        case: "string"
        function_pattern: "string"
        file_pattern: "string"
        examples_good: ["string"]
        examples_bad: ["string"]
      error_handling:
        pattern: "string"
        rules: ["string"]
        example_code: "string"
      testing:
        framework: "string"
        structure: "string"
        coverage_target: "string"
        mock_philosophy: "string"
        example_code: "string"
      git:
        commit_format: "string"
        branch_naming: "string"
        merge_strategy: "string"
        examples: ["string"]
      architecture:
        pattern: "string"
        layer_names: ["string"]
        dependency_rules: ["string"]
    subcultures:
      - { module: "string", differences: ["string"] }
    unique_aspects: "string"
```

### TOTEM_TO_SIGIL

```yaml
payload:
  convention_material:
    project_name: "string"
    profile_date: "YYYY-MM-DD"
    extractable_conventions:
      - convention_id: "CONV-XXX"
        dimension: "N | A | E | C | T | R | G | D"
        name: "string"
        description: "string"
        score: "X/3"
        enforcement_level: "AUTO | TEAM_AGREEMENT | IMPLICIT"
        codifiable: true
        rule_definition:
          pattern: "string"
          examples_pass: ["string"]
          examples_fail: ["string"]
          suggested_linter_rule: "string"
    skill_candidates:
      - { name: "string", type: "TEMPLATE | CHECKER | GENERATOR", based_on_dimensions: ["string"] }
```

### TOTEM_TO_GUARDIAN

```yaml
payload:
  git_convention_data:
    project_name: "string"
    commit_conventions:
      format: "conventional | prefix | jira_id | free_form"
      adherence_rate: "X%"
      pattern_regex: "string"
      examples_valid: ["string"]
      examples_invalid: ["string"]
    branch_conventions:
      format: "string"
      pattern_regex: "string"
      examples: ["string"]
    merge_strategy:
      preferred: "squash | merge | rebase"
      evidence: "string"
    pr_conventions:
      title_format: "string"
      template_used: true
      required_sections: ["string"]
    enforcement_recommendations:
      - { convention: "string", tool: "commitlint | branch-naming | pr-template", config_suggestion: "string" }
```

---

## Totem → Nexus (NEXUS_HANDOFF)

```yaml
## NEXUS_HANDOFF
Step: Totem
Agent: Totem
Summary: "<プロジェクト名>のDNA Profile完了。Confidence: [HIGH/MEDIUM/LOW]、Overall Scores: N:[X] A:[X] E:[X] C:[X] T:[X] R:[X] G:[X] D:[X]"
Key_findings:
  confidence: "HIGH | MEDIUM | LOW"
  dimension_scores:
    N: "X/3"
    A: "X/3"
    E: "X/3"
    C: "X/3"
    T: "X/3"
    R: "X/3"
    G: "X/3"
    D: "X/3"
  deviations_found:
    HIGH: "number"
    MEDIUM: "number"
    LOW: "number"
  drift_warnings: ["string"]
  subcultures_detected: ["string"]
Artifacts:
  - dna-profile.md
  - deviation-report.md
  - onboarding-guide.md
Risks:
  - "<プロファイリングで発見されたリスク>"
Open_questions: []
Suggested_next_agent: "<Judge | Zen | Scribe | Sigil | Guardian>"
Next_action: "<後続エージェントへの具体的な指示>"
```

---

## Nexus → Totem (ルーティング受信)

```yaml
nexus_routing:
  to: Totem
  task_type: "CULTURE_PROFILING | DEVIATION_CHECK | ONBOARDING_GUIDE | DRIFT_ANALYSIS"
  context:
    user_request: "<ユーザーの元の要求>"
    codebase_path: "string"
    scope: "FULL | MODULE | FILE_SET"
    target_modules: ["string"]
    existing_profile_available: true
  expected_output:
    - "dna_profile (Markdown)"
    - "handoff_yaml_for: <後続エージェント名>"
```

---

## ON_* Trigger AskUserQuestion Templates

### ON_SCOPE_SELECTION

```yaml
trigger: ON_SCOPE_SELECTION
condition: "プロファイリング対象のスコープが不明確"
question: "プロファイリングの対象スコープを選択してください"
options:
  - label: "全体プロファイリング"
    description: "リポジトリ全体を分析し、完全なDNA Profileを生成"
    value: "FULL"
  - label: "モジュール指定"
    description: "特定のモジュール/ディレクトリのみを分析"
    value: "MODULE"
    follow_up: "対象モジュールのパスを指定してください"
  - label: "差分プロファイリング"
    description: "既存プロファイルとの差分（ドリフト分析）のみ実行"
    value: "DRIFT"
  - label: "その他"
    description: "上記以外のスコープを指定"
    value: "OTHER"
```

### ON_PATTERN_CONFLICT

```yaml
trigger: ON_PATTERN_CONFLICT
condition: "同じ次元で2つ以上の競合するパターンが同程度の頻度で存在（40-60%の分布）"
question: "競合するパターンが検出されました。どちらを正規の規約として扱いますか？"
options:
  - label: "パターンA を採用"
    description: "[パターンAの具体的内容]（出現率: X%）"
    value: "PATTERN_A"
  - label: "パターンB を採用"
    description: "[パターンBの具体的内容]（出現率: Y%）"
    value: "PATTERN_B"
  - label: "両方を許容"
    description: "両パターンを有効な規約として扱い、スコアを調整"
    value: "BOTH_VALID"
  - label: "その他"
    description: "別の判断基準を指定"
    value: "OTHER"
```

### ON_INTENTIONAL_DEVIATION

```yaml
trigger: ON_INTENTIONAL_DEVIATION
condition: "逸脱の意図性スコアが 1-3（UNCERTAIN）の範囲"
question: "以下の逸脱が意図的かどうか判断できません。確認してください"
context:
  file: "[file_path]"
  dimension: "[N/A/E/C/T/R/G/D]"
  expected: "[期待されるパターン]"
  actual: "[実際のパターン]"
options:
  - label: "意図的な逸脱（規約進化）"
    description: "この変更は新しい規約として受け入れ、ベースラインを更新する"
    value: "INTENTIONAL_EVOLUTION"
  - label: "意図的だが例外（規約は変更しない）"
    description: "この箇所のみ例外として許可するが、規約自体は維持"
    value: "INTENTIONAL_EXCEPTION"
  - label: "非意図的（修正すべき）"
    description: "この逸脱は修正対象として Deviation Report に記録する"
    value: "ACCIDENTAL"
  - label: "その他"
    description: "別の判断を指定"
    value: "OTHER"
```

### ON_CULTURAL_DRIFT

```yaml
trigger: ON_CULTURAL_DRIFT
condition: "1つ以上の次元で 0.5 以上のスコア変化を検出"
question: "文化ドリフトが検出されました。対応方針を選択してください"
context:
  dimension: "[変化した次元]"
  previous_score: "X.X"
  current_score: "Y.Y"
  delta: "+/- Z.Z"
  direction: "EROSION | EVOLUTION | SHIFT"
  period: "[期間]"
options:
  - label: "進化として承認"
    description: "スコア変化を新しいベースラインとして受け入れる"
    value: "ACCEPT_EVOLUTION"
  - label: "侵食として対処"
    description: "元のスコアへの回復を目指し、対策を提案する"
    value: "ADDRESS_EROSION"
  - label: "モニタリング継続"
    description: "現時点ではアクション不要。次回プロファイリングで再評価"
    value: "MONITOR"
  - label: "その他"
    description: "別の対応方針を指定"
    value: "OTHER"
```

### ON_LOW_CONFIDENCE

```yaml
trigger: ON_LOW_CONFIDENCE
condition: "1つ以上の次元でサンプルサイズが閾値未満（信頼度 LOW）"
question: "以下の次元で十分なサンプルが得られませんでした。対応方法を選択してください"
context:
  low_confidence_dimensions:
    - { dimension: "[次元名]", sample_size: "N", required: "M" }
options:
  - label: "追加サンプルを収集"
    description: "分析スコープを広げて、より多くのファイルからサンプリングする"
    value: "EXPAND_SAMPLING"
  - label: "LOW 信頼度のままプロファイリング続行"
    description: "キャビート付きで結果を出力する（結果に LOW 信頼度マーク付与）"
    value: "PROCEED_WITH_CAVEAT"
  - label: "該当次元をスキップ"
    description: "信頼度 LOW の次元はプロファイルから除外する"
    value: "SKIP_DIMENSION"
  - label: "その他"
    description: "別の対応を指定"
    value: "OTHER"
```

### ON_MODULE_SUBCULTURE

```yaml
trigger: ON_MODULE_SUBCULTURE
condition: "モジュール間で 1.5 以上のスコア乖離を検出し、サブカルチャーの正当性が不明"
question: "モジュール間のスコア乖離が検出されました。サブカルチャーとして扱いますか？"
context:
  module: "[モジュールパス]"
  deviating_dimensions:
    - { dimension: "[次元名]", main_score: "X.X", module_score: "Y.Y", delta: "Z.Z" }
options:
  - label: "正当なサブカルチャー"
    description: "このモジュールは独自の規約を持つことが許容される。メインスコアから除外"
    value: "LEGITIMATE_SUBCULTURE"
  - label: "逸脱として扱う"
    description: "このモジュールはメインの規約に従うべき。逸脱として Deviation Report に記録"
    value: "TREAT_AS_DEVIATION"
  - label: "部分的にサブカルチャー"
    description: "一部の次元は独自規約を許容するが、残りはメインに準拠すべき"
    value: "PARTIAL_SUBCULTURE"
    follow_up: "独自規約を許容する次元を指定してください"
  - label: "その他"
    description: "別の判断を指定"
    value: "OTHER"
```
