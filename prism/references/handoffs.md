# Handoff Formats

Prismと他エージェント間のハンドオフテンプレート集。

---

## Inbound Handoffs (→ Prism)

### SCRIBE_TO_PRISM_HANDOFF

Scribeが構造化したドキュメントをPrismがプロンプト設計に活用する。

```yaml
SCRIBE_TO_PRISM_HANDOFF:
  source_type: [PDF / Google Docs / Markdown]
  source_summary: |
    [ドキュメントの概要。3-5文で内容を説明]
  structure:
    sections: [セクション数]
    hierarchy: [フラット / 階層的 / 時系列]
    word_count: [概算ワード数]
  audience: [ターゲットオーディエンスが判明している場合]
  goal: [ユーザーの最終目標]
  notes: |
    [Scribeからの補足情報。構造上の特記事項等]
```

### QUILL_TO_PRISM_HANDOFF

Quillが仕上げた文章をPrismがNotebookLMソースとして最適化する。

```yaml
QUILL_TO_PRISM_HANDOFF:
  content_type: [記事 / レポート / ガイド / エッセイ]
  content_summary: |
    [コンテンツの概要]
  tone: [Quillが使用したトーン]
  word_count: [ワード数]
  target_format: [Audio / Video / Slide / Infographic — 判明している場合]
  audience: [ターゲットオーディエンス]
  notes: |
    [Quillからの補足。特に強調したいポイント等]
```

### RESEARCHER_TO_PRISM_HANDOFF

Researcherの調査結果をPrismがコンテンツ化のためにプロンプト設計する。

```yaml
RESEARCHER_TO_PRISM_HANDOFF:
  research_topic: [調査テーマ]
  findings_summary: |
    [主要な発見事項。5-10ポイント]
  source_count: [調査で使用したソース数]
  source_types: [論文 / 記事 / データ / インタビュー等]
  confidence_level: [高 / 中 / 低]
  key_data_points:
    - [データポイント1]
    - [データポイント2]
  target_format: [推奨される出力フォーマット]
  audience: [ターゲットオーディエンス]
  notes: |
    [調査上の制限事項や注意点]
```

### VOICE_TO_PRISM_HANDOFF

Voiceのオーディエンス分析をPrismがプロンプトのAudience Layer設計に活用する。

```yaml
VOICE_TO_PRISM_HANDOFF:
  audience_profile:
    primary: [プライマリオーディエンス]
    secondary: [セカンダリオーディエンス、ある場合]
    knowledge_level: [初心者 / 中級 / 上級 / 専門家]
    pain_points:
      - [課題1]
      - [課題2]
    preferred_tone: [カジュアル / プロフェッショナル / 学術的]
  communication_strategy: |
    [Voiceが推奨するコミュニケーションアプローチ]
  content_goal: [認知向上 / 教育 / 説得 / 行動喚起]
  notes: |
    [オーディエンス固有の注意事項]
```

---

## Outbound Handoffs (Prism →)

### PRISM_TO_USER_DELIVERY

Prismからユーザーへの最終デリバリー（最も一般的なハンドオフ）。

```yaml
PRISM_TO_USER_DELIVERY:
  format: [Audio Overview / Video Overview / Slide Deck / Infographic / Mind Map]
  style: [Deep Dive / Brief / Critique / Debate / Lecture / Explainer 等]
  steering_prompt: |
    [そのままNotebookLMに貼り付けて使えるプロンプト全文]
  source_preparation:
    notebook_pattern: [Single Deep / Multi-Perspective / Hierarchical / Comparative / Chronological]
    recommended_sources: [推奨ソース数]
    optimization_notes:
      - [ソース最適化アドバイス1]
      - [ソース最適化アドバイス2]
  quality_criteria:
    - criterion: [評価基準1]
      target: [目標値/状態]
    - criterion: [評価基準2]
      target: [目標値/状態]
  alternative_prompt: |
    [別アプローチのプロンプト（オプション）]
  alternative_rationale: |
    [代替プロンプトを選ぶ理由]
```

### PRISM_TO_MORPH_HANDOFF

PrismのNotebookLM出力を別フォーマットに変換する際にMorphへ渡す。

```yaml
PRISM_TO_MORPH_HANDOFF:
  original_format: [NotebookLMで生成した元フォーマット]
  original_content_summary: |
    [生成された内容の概要]
  target_format: [変換先のフォーマット]
  key_messages:
    - [維持すべきメッセージ1]
    - [維持すべきメッセージ2]
  audience: [ターゲットオーディエンス]
  tone: [維持すべきトーン]
  constraints:
    - [変換時の制約1]
    - [変換時の制約2]
```

### PRISM_TO_GROWTH_HANDOFF

NotebookLM出力の配信・エンゲージメント最適化をGrowthに依頼する。

```yaml
PRISM_TO_GROWTH_HANDOFF:
  content_type: [Audio / Video / Slide / Infographic]
  content_summary: |
    [コンテンツの概要]
  audience:
    primary: [プライマリオーディエンス]
    platform: [配信プラットフォーム]
  engagement_hooks:
    - [注目を引くポイント1]
    - [注目を引くポイント2]
  distribution_notes: |
    [配信に関する推奨事項]
  metrics_to_track:
    - [追跡すべき指標1]
    - [追跡すべき指標2]
```

### PRISM_TO_CANVAS_HANDOFF

Infographic出力のビジュアルデザイン強化をCanvasに依頼する。

```yaml
PRISM_TO_CANVAS_HANDOFF:
  content_type: Infographic
  content_summary: |
    [インフォグラフィックの内容概要]
  data_points:
    - [可視化すべきデータ1]
    - [可視化すべきデータ2]
  visual_requirements:
    orientation: [Vertical / Horizontal]
    color_palette: [指定がある場合]
    style: [Clean / Bold / Minimalist 等]
  target_audience: [ターゲット]
  usage_context: [Web / Print / Presentation / SNS]
```

---

## Collaboration Patterns

### Pattern A: Source Enhancement Pipeline

```
Scribe (構造化)    Quill (仕上げ)
       \              /
        → Prism (プロンプト設計) → User (NotebookLMで生成)
```

**Trigger:** ユーザーが未整理のソース資料を持っている
**Flow:** Scribe/Quillがソースを整理 → Prismが最適なプロンプトを設計 → ユーザーが実行

### Pattern B: Research-to-Content Pipeline

```
Researcher (調査) → Prism (プロンプト設計) → User (生成) → Morph (変換)
```

**Trigger:** リサーチ結果をNotebookLMでコンテンツ化したい
**Flow:** Researcherが調査 → Prismがソース構成+プロンプト設計 → ユーザーが生成 → Morphが他形式に変換

### Pattern C: Audience-Optimized Pipeline

```
Voice (オーディエンス分析) → Prism (プロンプト設計) → User (生成) → Growth (配信最適化)
```

**Trigger:** 特定のオーディエンスに最適化されたコンテンツが必要
**Flow:** Voiceがオーディエンス分析 → Prismがオーディエンスに合わせたプロンプト設計 → ユーザーが生成 → Growthが配信最適化

### Pattern D: Iterative Refinement Loop

```
User ↔ Prism (相談 → 提案 → 評価 → 調整)
```

**Trigger:** 生成結果の品質を改善したい
**Flow:** ユーザーが生成結果を共有 → Prismが評価+改善プロンプトを提案 → ユーザーが再生成 → 繰り返し

---

## Handoff Best Practices

1. **必須フィールドは必ず埋める** — audience と goal は常に含める
2. **ソース情報を具体的に** — 「ドキュメント」ではなく「50ページのPDF技術レポート」
3. **制約を明示する** — Free/Plus tier、時間制限、言語制約等
4. **前段エージェントの判断を尊重する** — Voiceのオーディエンス分析を上書きしない
5. **代替案を含める** — メインプロンプトに加えて代替アプローチも提示

---

Remember: A good handoff carries enough context that the receiving agent (or user) can proceed without asking clarifying questions.
