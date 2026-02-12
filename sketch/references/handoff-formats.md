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
