# Handoff Templates

**Purpose:** Clause と他エージェント間のハンドオフ形式定義。
**Read when:** 他エージェントとの連携が必要な場合。

---

## Inbound Handoffs

### From Comply (COMPLY_TO_CLAUSE_HANDOFF)

規制要件を法的文書に反映する必要がある場合。

```yaml
COMPLY_TO_CLAUSE_HANDOFF:
  source: Comply
  target: Clause
  context:
    regulatory_framework: "[SOC2 | PCI-DSS | HIPAA | ISO 27001 | ...]"
    requirements:
      - requirement_id: "[ID]"
        description: "[要件の説明]"
        impact_on_legal_docs: "[利用規約/プライバシーポリシーへの影響]"
    target_documents:
      - "[対象文書名]"
    priority: "[High | Medium | Low]"
  expected_output: "法的文書への反映案と整合性レポート"
```

### From Cloak (CLOAK_TO_CLAUSE_HANDOFF)

プライバシー実装とポリシー文書の整合を確認する場合。

```yaml
CLOAK_TO_CLAUSE_HANDOFF:
  source: Cloak
  target: Clause
  context:
    privacy_implementation:
      data_collected: ["[収集データ項目]"]
      processing_purposes: ["[処理目的]"]
      third_party_sharing: ["[第三者提供先]"]
      retention_periods: {"[データ種別]": "[期間]"}
    consent_mechanisms:
      - type: "[opt-in | opt-out | notice-only]"
        scope: "[対象データ・処理]"
    current_policy_version: "[バージョン/日付]"
  expected_output: "ポリシー文書との差分レポートと修正案"
```

### From Scribe (SCRIBE_TO_CLAUSE_HANDOFF)

仕様書から法的要件を抽出してレビューする場合。

```yaml
SCRIBE_TO_CLAUSE_HANDOFF:
  source: Scribe
  target: Clause
  context:
    specification_type: "[PRD | SRS | HLD]"
    legal_relevant_sections:
      - section: "[セクション名]"
        content_summary: "[要約]"
        legal_concern: "[法的懸念事項]"
    service_description: "[サービス概要]"
    target_jurisdictions: ["[法域]"]
  expected_output: "法的文書要件リストとチェックリスト"
```

---

## Outbound Handoffs

### To Builder (CLAUSE_TO_BUILDER_HANDOFF)

レビュー結果から実装が必要な項目がある場合。

```yaml
CLAUSE_TO_BUILDER_HANDOFF:
  source: Clause
  target: Builder
  context:
    implementation_items:
      - id: "[IMPL-01]"
        type: "[consent_flow | cookie_banner | age_gate | data_export | deletion_flow | opt_out]"
        requirement: "[法的要件の説明]"
        reference_finding: "[レビューレポートの発見事項ID]"
        reference_law: "[参照法令]"
        priority: "[High | Medium | Low]"
        acceptance_criteria:
          - "[基準1]"
          - "[基準2]"
    technical_constraints:
      - "[制約事項]"
  expected_output: "実装コードと動作確認結果"
```

### To Prose (CLAUSE_TO_PROSE_HANDOFF)

法的文書の平易化・UXライティング改善が必要な場合。

```yaml
CLAUSE_TO_PROSE_HANDOFF:
  source: Clause
  target: Prose
  context:
    document_type: "[利用規約 | プライバシーポリシー | ...]"
    readability_issues:
      - location: "[該当箇所]"
        current_text: "[現在の文面]"
        issue: "[問題点: 専門用語過多/曖昧/冗長/...]"
        target_audience: "[対象読者]"
    tone_requirements:
      formality: "[formal | semi-formal | casual]"
      language_level: "[専門家向け | 一般向け | 全年齢向け]"
    constraints:
      - "法的正確性を維持すること"
      - "[その他制約]"
  expected_output: "平易化された文面案"
```

### To Scribe (CLAUSE_TO_SCRIBE_HANDOFF)

法的要件を仕様文書として整理する場合。

```yaml
CLAUSE_TO_SCRIBE_HANDOFF:
  source: Clause
  target: Scribe
  context:
    legal_requirements:
      - id: "[REQ-01]"
        requirement: "[法的要件]"
        source_law: "[根拠法令]"
        priority: "[High | Medium | Low]"
        implementation_scope: "[影響範囲]"
    document_request:
      type: "[PRD | checklist | test_spec]"
      format: "[出力形式の希望]"
  expected_output: "法的要件を反映した仕様文書"
```
