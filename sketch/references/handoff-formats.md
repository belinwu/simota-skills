# Sketch — Handoff Formats

---

## Collaboration Handoffs

### INPUT (from Vision)

```yaml
VISION_TO_SKETCH:
  creative_direction: "[Style, mood, color palette summary]"
  target_use: "[Web hero / Marketing banner / App icon / etc.]"
  requirements:
    aspect_ratio: "[16:9 / 1:1 / etc.]"
    style: "[Photorealistic / Illustration / etc.]"
    constraints: ["No people", "Brand colors: #xxx"]
  reference_images: ["[paths if any]"]
```

### OUTPUT (to Muse)

```yaml
SKETCH_TO_MUSE:
  generated_images: ["[file paths]"]
  metadata: "[metadata.json path]"
  prompt_used: "[Final English prompt]"
  integration_notes: "[How to use in design system]"
```

---

## AUTORUN Formats

### Input Format (_AGENT_CONTEXT)

```yaml
_AGENT_CONTEXT:
  Role: Sketch
  Task: [Text-to-image / Image editing / Batch generation / Style transfer]
  Mode: AUTORUN
  Chain: [Previous agents in chain]
  Input:
    task_type: single_shot | iterative | batch | reference_based
    description: "[What to generate - Japanese or English]"
    style: "[Photorealistic / Illustration / 3D / Abstract / auto]"
    aspect_ratio: "[1:1 / 16:9 / etc. or auto]"
    resolution: "[1K / 2K / 4K]"
    model_preference: "[flash / pro / auto]"
    reference_images: ["[paths if any]"]
    count: [number of images]
    output_dir: "[output directory path]"
  Constraints:
    - [Person generation policy]
    - [Budget/cost limits]
    - [Brand guidelines]
  Expected_Output: [Python script / Batch script / Edit script]
```

### Output Format (_STEP_COMPLETE)

```yaml
_STEP_COMPLETE:
  Agent: Sketch
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [Python script path]
    prompt_crafted: "[Final English prompt]"
    parameters:
      model: "gemini-2.5-flash-image"
    cost_estimate: "[estimated cost]"
    output_files: ["[generated file paths]"]
  Delegations:
    - Agent: Muse
      Task: [Design system integration if needed]
  Validations:
    policy_check: "[passed / flagged / adjusted]"
    code_syntax: "[valid / error]"
    api_key_safety: "[secure — env var only]"
  Next: Muse | Canvas | Growth | VERIFY | DONE
  Reason: [Why this next step]
```

---

## AUTORUN Complete Chain Example

Vision → Sketch → Muse の完全な AUTORUN チェーンフロー。

### Step 1: Vision が _STEP_COMPLETE を Nexus に返却

```yaml
_STEP_COMPLETE:
  Agent: Vision
  Status: SUCCESS
  Output:
    deliverable: "docs/creative-direction.md"
    creative_direction:
      style: "Modern minimalist, clean lines"
      mood: "Professional yet approachable"
      color_palette: ["#1A1A2E", "#16213E", "#0F3460", "#E94560"]
      typography: "Sans-serif, geometric"
    target_assets:
      - type: "hero_image"
        aspect_ratio: "16:9"
        use: "Landing page above the fold"
      - type: "social_media"
        aspect_ratio: "1:1"
        use: "Instagram/Twitter posts"
  Next: Sketch
  Reason: "Creative direction established, need image generation code"
```

### Step 2: Nexus が Sketch に _AGENT_CONTEXT を発行

```yaml
_AGENT_CONTEXT:
  Role: Sketch
  Task: Text-to-image
  Mode: AUTORUN
  Chain: [Vision]
  Input:
    task_type: batch
    description: "Modern minimalist SaaS landing page hero image with abstract geometric shapes, professional color palette (#1A1A2E, #0F3460, #E94560), clean composition. Also generate matching social media post image."
    style: "Photorealistic"
    aspect_ratio: "16:9"
    model_preference: "flash"
    count: 2
    output_dir: "./generated/campaign-2026"
  Constraints:
    - "No person generation"
    - "Brand colors must be prominent"
    - "Cost: minimize (use Flash)"
  Expected_Output: Python script
```

### Step 3: Sketch が処理を実行

Sketch 内部処理:

1. `_AGENT_CONTEXT.Input` を解析
2. `task_type: batch` → BATCH モードを選択
3. `description` から4層プロンプトを構築:
   - **Subject**: "Modern minimalist SaaS landing page with abstract geometric shapes"
   - **Style**: "photorealistic, clean modern aesthetic, professional"
   - **Composition**: "widescreen 16:9, centered, ample negative space"
   - **Technical**: "8K detail, sharp focus, color graded with #1A1A2E #0F3460 #E94560"
4. `Constraints` を確認 → 人物なし、Flash モデル使用
5. Python バッチスクリプトを生成
6. `_STEP_COMPLETE` を返却

### Step 4: Sketch が _STEP_COMPLETE を返却

```yaml
_STEP_COMPLETE:
  Agent: Sketch
  Status: SUCCESS
  Output:
    deliverable: "scripts/generate_campaign_2026.py"
    prompt_crafted: "Modern minimalist SaaS landing page with abstract geometric shapes, clean lines and bold color accents, photorealistic rendering, centered composition with ample negative space, widescreen 16:9, 8K detail, sharp focus, professional color palette featuring deep navy and coral red accents"
    parameters:
      model: "gemini-2.5-flash-image"
      aspect_ratios: ["16:9", "1:1"]
      batch_size: 2
    cost_estimate: "$0.04-0.08 (2 images × Flash)"
    output_files:
      - "./generated/campaign-2026/hero_16x9.png"
      - "./generated/campaign-2026/social_1x1.png"
      - "./generated/campaign-2026/metadata.json"
  Delegations:
    - Agent: Muse
      Task: "Integrate generated images into design token system, ensure color consistency with brand palette"
  Validations:
    policy_check: "passed — no person generation, no copyrighted content"
    code_syntax: "valid — Python 3.8+ compatible"
    api_key_safety: "secure — os.environ['GEMINI_API_KEY'] only"
  Next: Muse
  Reason: "Images generated successfully, Muse should integrate into design system and verify brand consistency"
```

### Step 5: Nexus が Muse に _AGENT_CONTEXT を発行

```yaml
_AGENT_CONTEXT:
  Role: Muse
  Task: Design system integration
  Mode: AUTORUN
  Chain: [Vision, Sketch]
  Input:
    images:
      - path: "./generated/campaign-2026/hero_16x9.png"
        use: "Landing page hero"
      - path: "./generated/campaign-2026/social_1x1.png"
        use: "Social media posts"
    brand_palette: ["#1A1A2E", "#16213E", "#0F3460", "#E94560"]
    integration_task: "Register as design tokens, verify color consistency"
  Expected_Output: Design token definitions + integration guide
```

---

## Nexus Hub Handoff

When user input contains `## NEXUS_ROUTING`, treat Nexus as hub. Do not instruct calling other agents directly — always return via `## NEXUS_HANDOFF`.

```text
## NEXUS_HANDOFF
- Step: [X/Y]
- Agent: Sketch
- Summary: 1-3 lines
- Key findings / decisions:
  - Prompt: [Crafted prompt summary]
  - Model: [Selected model]
  - Parameters: [Key parameters]
- Artifacts (files/commands/links):
  - Python script: [path]
  - Metadata: [path]
- Risks / trade-offs:
  - [Content policy considerations]
  - [Cost implications]
- Pending Confirmations:
  - Trigger: [INTERACTION_TRIGGER name if any]
  - Question: [Question for user]
  - Options: [Available options]
  - Recommended: [Recommended option]
- User Confirmations:
  - Q: [Previous question] → A: [User's answer]
- Open questions (blocking/non-blocking):
  - [Clarifications needed]
- Suggested next agent: Muse | Canvas | Growth (reason)
- Next action: CONTINUE (Nexus automatically proceeds)
```

### Nexus Handoff Example

```text
## NEXUS_HANDOFF
- Step: 2/4
- Agent: Sketch
- Summary: SaaS ランディングページ用ヒーロー画像の生成コードを作成。Flash モデルで16:9 + 1:1の2枚バッチ生成スクリプトを納品。
- Key findings / decisions:
  - Prompt: "Modern minimalist SaaS landing page, abstract geometric shapes, deep navy and coral accents, photorealistic, 16:9"
  - Model: gemini-2.5-flash-image (Flash)
  - Parameters: batch=2, aspect_ratios=[16:9, 1:1], no person generation
- Artifacts:
  - Python script: scripts/generate_campaign_2026.py
  - Metadata: ./generated/campaign-2026/metadata.json
- Risks / trade-offs:
  - Flash モデルのため最高品質ではないが、コスト効率は最適
  - 抽象的なプロンプトのため、1-2回の反復調整が必要な可能性
- Pending Confirmations: None
- User Confirmations:
  - Q: Person generation? → A: No (Vision directive)
- Open questions: None
- Suggested next agent: Muse (design system integration, color consistency verification)
- Next action: CONTINUE
```
