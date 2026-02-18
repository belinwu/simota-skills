# Handoff Templates — エージェント間ハンドオフYAML集

Refract から他エージェントへのハンドオフ形式。`perspective_map` を受け取ったエージェントが必要な情報を得られる構造。

---

## Refract → Magi（意思決定前の盲点確認）

```yaml
handoff:
  from: Refract
  to: Magi
  type: PERSPECTIVE_MAP_FOR_DECISION
  payload:
    theme: "<意思決定テーマ>"
    dominant_frame:
      summary: "<現在の支配的見方を1文>"
      assumptions:
        - "<暗黙の前提1>"
        - "<暗黙の前提2>"
    perspective_map:
      field_rotations:
        - type: "Zoom Out"
          question: "<問い>"
          new_visible: "<新しく見えたもの>"
          hidden_revealed: "<隠れていたもの>"
          importance: HIGH  # HIGH / MEDIUM / LOW
        - type: "Temporal Zoom"
          question: "<問い>"
          new_visible: "<新しく見えたもの>"
          hidden_revealed: "<隠れていたもの>"
          importance: MEDIUM
      standpoint_rotations:
        - type: "Adversarial Shift"
          question: "<問い>"
          new_visible: "<新しく見えたもの>"
          hidden_revealed: "<隠れていたもの>"
          importance: HIGH
      lens_rotations:
        - type: "Systems Lens"
          question: "<問い>"
          new_visible: "<新しく見えたもの>"
          hidden_revealed: "<隠れていたもの>"
          importance: HIGH
        - type: "Inversion Lens"
          question: "<問い>"
          new_visible: "<新しく見えたもの>"
          hidden_revealed: "<隠れていたもの>"
          importance: MEDIUM
    key_blind_spots:
      - "<最重要の盲点1>"
      - "<最重要の盲点2>"
    questions_for_magi:
      logos: "<技術/論理的観点で再評価すべき問い>"
      pathos: "<感情/倫理的観点で見落としている問い>"
      sophia: "<ビジネス/実利的観点で見落としている問い>"
    instructions_for_magi:
      - "上記の視点マップを参考に、見落としを考慮した上で意思決定してください"
      - "key_blind_spots に示した観点を特にPathos/Sophiaの評価に組み込んでください"
```

---

## Refract → Helm（戦略立案の視野拡大）

```yaml
handoff:
  from: Refract
  to: Helm
  type: PERSPECTIVE_MAP_FOR_STRATEGY
  payload:
    theme: "<戦略テーマ>"
    current_strategic_frame:
      summary: "<現在の戦略フレーム>"
      time_horizon: "<短期/中期/長期>"
      key_assumptions:
        - "<戦略の前提1>"
        - "<戦略の前提2>"
    strategic_insights:
      new_opportunities:
        - perspective: "<視点タイプ>"
          insight: "<発見された機会>"
          urgency: HIGH  # HIGH / MEDIUM / LOW
      hidden_risks:
        - perspective: "<視点タイプ>"
          risk: "<見落とされていたリスク>"
          severity: HIGH
      assumptions_to_challenge:
        - assumption: "<再検討すべき前提>"
          evidence: "<なぜ再検討すべきか>"
    cross_domain_analogies:
      - domain: "<参照ドメイン>"
        analogy: "<構造的類似性>"
        applicable_insight: "<転用できる洞察>"
    time_axis_insights:
      short_term_blindspot: "<短期視野での見落とし>"
      long_term_opportunity: "<長期視野で見えた機会>"
    instructions_for_helm:
      - "上記インサイトをSWOT/シナリオプランニングに組み込んでください"
      - "特にhidden_risksは戦略リスクとして評価してください"
```

---

## Refract → Bridge（ステークホルダー認識ギャップ）

```yaml
handoff:
  from: Refract
  to: Bridge
  type: PERSPECTIVE_MAP_FOR_GAP_TRANSLATION
  payload:
    theme: "<ギャップテーマ>"
    identified_gaps:
      - group_a:
          label: "<グループA（例: ビジネス側）>"
          dominant_frame: "<Aの見え方>"
          key_language: "<Aが使う言葉・メタファー>"
        group_b:
          label: "<グループB（例: エンジニア側）>"
          dominant_frame: "<Bの見え方>"
          key_language: "<Bが使う言葉・メタファー>"
        gap_root_cause: "<なぜ同じ問題を違う問題として見ているか>"
    standpoint_analysis:
      hierarchy_levels:
        - level: "経営層"
          frame: "<この問題がどう見えるか>"
          language: "<使われる言語>"
        - level: "実務担当"
          frame: "<この問題がどう見えるか>"
          language: "<使われる言語>"
    shared_foundations:
      common_goal: "<両者が実は同意している目標>"
      common_enemy: "<両者が共通して避けたいこと>"
    translation_needs:
      - term: "<翻訳が必要な用語>"
        group_a_meaning: "<Aの解釈>"
        group_b_meaning: "<Bの解釈>"
        suggested_neutral: "<中立な言い換え>"
    instructions_for_bridge:
      - "identified_gaps を元に双方向翻訳ドキュメントを作成してください"
      - "shared_foundations を橋渡しの出発点として活用してください"
```

---

## Refract → Scribe（多角視点の文書化）

```yaml
handoff:
  from: Refract
  to: Scribe
  type: PERSPECTIVE_MAP_FOR_DOCUMENTATION
  payload:
    theme: "<文書化テーマ>"
    multi_perspective_content:
      scale_perspectives:
        - scale: "マクロ（Zoom Out）"
          definition: "<広義の定義>"
          context: "<適用コンテキスト>"
        - scale: "ミクロ（Zoom In）"
          definition: "<狭義の定義>"
          context: "<適用コンテキスト>"
      stakeholder_perspectives:
        - stakeholder: "<ステークホルダー1>"
          interpretation: "<この概念の意味>"
          importance: HIGH
        - stakeholder: "<ステークホルダー2>"
          interpretation: "<この概念の意味>"
          importance: MEDIUM
      frame_perspectives:
        - frame: "Systems"
          interpretation: "<システム的解釈>"
          key_elements: ["<要素1>", "<要素2>"]
        - frame: "First Principles"
          interpretation: "<原理的解釈>"
          key_elements: ["<要素1>"]
    document_structure_recommendation:
      required_sections:
        - "<省略すると偏る視点を含むセクション>"
      glossary_additions:
        - term: "<統一すべき用語>"
          unified_definition: "<推奨定義>"
    instructions_for_scribe:
      - "multi_perspective_content の各視点が文書に反映されることを確認してください"
      - "特定の視点が支配的になりすぎないよう構成してください"
```

---

## Refract → Nexus（視点変換結果のルーティング）

```yaml
## NEXUS_HANDOFF
Step: Refract
Agent: Refract
Summary: "<テーマ>に対して<N>軸<M>回転を実施。<最重要洞察1文>"
Key_findings:
  dominant_frame: "<特定した支配的フレーム>"
  axes_applied: [視野, 視座, 視点]
  rotation_count: <N>
  key_insights:
    - "<洞察1>"
    - "<洞察2>"
  blind_spots_revealed:
    - "<盲点1>"
    - "<盲点2>"
Artifacts:
  - perspective_map.md
Risks:
  - "<視点変換で発見されたリスク>"
Open_questions: []
Suggested_next_agent: "<Magi / Helm / Bridge / Scribe>"
Next_action: "<後続エージェントへの具体的な指示>"
```

---

## Nexus → Refract（ルーティング受信）

```yaml
nexus_routing:
  to: Refract
  task_type: PERSPECTIVE_REFRAMING
  context:
    user_request: "<ユーザーの元の要求>"
    theme: "<リフレーミング対象のテーマ>"
    current_frame_hint: "<現在の支配的フレームのヒント>"
    axes_requested:    # 省略時は全3軸
      - 視野
      - 視座
      - 視点
    downstream_agent_hint: "<Magi / Helm / Bridge / Scribe>"
  expected_output:
    - perspective_map (Markdown)
    - handoff_yaml_for: "<後続エージェント名>"
```
