# Interaction Triggers

Accordが判断を求めるべきタイミングとYAMLテンプレート。

---

## トリガー一覧

| Trigger | Condition | Default Action |
|---------|-----------|---------------|
| SCOPE_UNCLEAR | 複雑度指標がLow/Medium/Highの混在 | Standard で進行 |
| TEAM_UNKNOWN | 関与チーム構成が不明 | 3チーム全参加を前提 |
| REQUIREMENTS_OVERFLOW | 要件が10+かつ分解未済 | Sherpa連携を提案 |
| L2_TECH_DEPTH | L2-Devでアーキテクチャ判断が必要 | Atlas/Gateway相談を提案 |
| L2_DESIGN_SCOPE | L2-Designで視覚的成果物が必要 | Vision/Palette委譲を提案 |
| STAKEHOLDER_EXPANSION | 法務・セキュリティ等の追加チーム | スコープ拡張を確認 |

---

## YAML テンプレート

### SCOPE_UNCLEAR

```yaml
INTERACTION_TRIGGER:
  type: SCOPE_UNCLEAR
  condition: "複雑度指標がLow/Medium/Highの混在で明確なスコープが選択できない"
  question: "プロジェクトの複雑度が混在しています。どのスコープで仕様を作成しますか？"
  options:
    - "Full（全セクション完備、12+ 要件向け）"
    - "Standard（関与L2のみ、4-11 要件向け）(Recommended)"
    - "Lite（インライン記述、1-3 要件向け）"
    - "Other（詳細を教えてください）"
  context:
    complexity_indicators: "[検出した複雑度指標]"
    teams_involved: "[検出したチーム構成]"
  default: "Standard"
```

### TEAM_UNKNOWN

```yaml
INTERACTION_TRIGGER:
  type: TEAM_UNKNOWN
  condition: "要件からチーム構成を推測できない"
  question: "この仕様に関与するチームはどれですか？"
  options:
    - "ビジネス・開発・デザイン（3チーム全て）(Recommended)"
    - "開発・デザイン（2チーム）"
    - "ビジネス・開発（2チーム）"
    - "Other（詳細を教えてください）"
  context:
    detected_keywords: "[要件から検出したチーム関連キーワード]"
  default: "ビジネス・開発・デザイン（3チーム全て）"
```

### REQUIREMENTS_OVERFLOW

```yaml
INTERACTION_TRIGGER:
  type: REQUIREMENTS_OVERFLOW
  condition: "要件数が10を超え、単一仕様パッケージでは管理が困難"
  question: "要件が10件以上あります。先にSherpaでタスク分解してから仕様化しますか？"
  options:
    - "Sherpaで分解後に各パートを仕様化(Recommended)"
    - "そのまま1つのFull仕様パッケージとして作成"
    - "優先度の高い要件のみ先に仕様化"
    - "Other（詳細を教えてください）"
  context:
    requirements_count: "[検出した要件数]"
    estimated_scope: "Full"
  default: "Sherpaで分解後に各パートを仕様化"
```

### L2_TECH_DEPTH

```yaml
INTERACTION_TRIGGER:
  type: L2_TECH_DEPTH
  condition: "L2-Devセクションでアーキテクチャ選定・技術判断が必要"
  question: "技術的なアーキテクチャ判断が必要です。どう進めますか？"
  options:
    - "Atlas/Gatewayに技術設計を相談してからL2-Devを記述(Recommended)"
    - "既存アーキテクチャを前提にL2-Devを記述"
    - "L2-Devは概要のみ記述し、詳細は開発チームに委譲"
    - "Other（詳細を教えてください）"
  context:
    technical_decision: "[判断が必要な技術課題]"
    existing_architecture: "[既存のアーキテクチャ情報]"
  default: "Atlas/Gatewayに技術設計を相談してからL2-Devを記述"
```

### L2_DESIGN_SCOPE

```yaml
INTERACTION_TRIGGER:
  type: L2_DESIGN_SCOPE
  condition: "L2-Designで視覚的な成果物（モックアップ、ワイヤーフレーム）が必要"
  question: "デザイン成果物が必要です。Accordではフロー・要件のみ定義します。視覚的成果物はVision/Paletteに委譲しますか？"
  options:
    - "フロー・要件のみ定義し、視覚成果物はVision/Palette委譲(Recommended)"
    - "既存デザインシステムの参照で十分（視覚成果物不要）"
    - "デザインチームが別途Figmaで作成予定"
    - "Other（詳細を教えてください）"
  context:
    design_needs: "[検出したデザイン要件]"
    existing_design_system: "[既存デザインシステムの有無]"
  default: "フロー・要件のみ定義し、視覚成果物はVision/Palette委譲"
```

### STAKEHOLDER_EXPANSION

```yaml
INTERACTION_TRIGGER:
  type: STAKEHOLDER_EXPANSION
  condition: "法務・セキュリティ・コンプライアンス等、標準3チーム以外のステークホルダーが必要"
  question: "標準の3チーム（Biz/Dev/Design）以外のステークホルダーが関与しそうです。仕様パッケージのスコープを拡張しますか？"
  options:
    - "L2に追加セクション（L2-Legal/L2-Security等）を追加(Recommended)"
    - "既存のL2-Bizセクション内で追加ステークホルダーの要件を記述"
    - "追加ステークホルダーの要件は別文書（Scribe委譲）"
    - "Other（詳細を教えてください）"
  context:
    additional_stakeholders: "[検出した追加ステークホルダー]"
    regulatory_requirements: "[規制・コンプライアンス要件]"
  default: "L2に追加セクション（L2-Legal/L2-Security等）を追加"
```

---

## トリガー検出のヒューリスティクス

| 検出キーワード | 推定トリガー |
|-------------|------------|
| 「どのくらいの規模」「複雑」「簡単」 | SCOPE_UNCLEAR |
| 「誰が使う」「どのチーム」「関係者」 | TEAM_UNKNOWN |
| 複数のユーザーストーリー/REQ列挙 | REQUIREMENTS_OVERFLOW |
| 「アーキテクチャ」「技術選定」「DB設計」 | L2_TECH_DEPTH |
| 「UI」「モックアップ」「デザイン」「画面」 | L2_DESIGN_SCOPE |
| 「法務」「セキュリティ」「コンプライアンス」「個人情報」 | STAKEHOLDER_EXPANSION |
