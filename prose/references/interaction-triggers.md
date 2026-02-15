# Prose Interaction Triggers

質問テンプレート集（AskUserQuestion 形式）。

---

## ON_TONE_DECISION

```yaml
trigger: ON_TONE_DECISION
condition: "Tone for the copy context is ambiguous"
question: "What tone should this copy use?"
options:
  - label: "Casual and friendly"
    description: "Conversational, contractions, warm — suited for consumer apps"
  - label: "Professional and clear"
    description: "Neutral, precise, trustworthy — suited for B2B/enterprise"
  - label: "Playful and energetic"
    description: "Fun, emoji-ok, celebratory — suited for creative/social products"
  - label: "Serious and formal"
    description: "No contractions, precise language — for legal, billing, security"
```

---

## ON_SENSITIVE_COPY

```yaml
trigger: ON_SENSITIVE_COPY
condition: "Copy involves sensitive context (billing, security, data deletion)"
question: "This copy involves a sensitive context. How should we handle it?"
options:
  - label: "Clear and reassuring"
    description: "Acknowledge seriousness, explain clearly, offer support paths"
  - label: "Minimal and factual"
    description: "State facts only, no emotional language, maximum precision"
  - label: "Guided with safety nets"
    description: "Step-by-step with confirmation, undo options, and warnings"
  - label: "Match existing patterns"
    description: "Follow the existing copy patterns for similar sensitive areas"
```

---

## ON_COPY_SCOPE

```yaml
trigger: ON_COPY_SCOPE
condition: "Copy scope is broader than a single screen"
question: "What scope should this copy work cover?"
options:
  - label: "Single screen/component"
    description: "One specific UI element or page"
  - label: "Full feature flow"
    description: "All screens in a user journey (e.g., checkout flow)"
  - label: "Voice & tone guidelines"
    description: "Brand-level copy guidelines for the whole product"
  - label: "Audit existing copy"
    description: "Review and improve existing copy across the product"
```

---

## ON_EXISTING_TRANSLATIONS

```yaml
trigger: ON_EXISTING_TRANSLATIONS
condition: "Product already has translations or i18n setup"
question: "Does this product have existing translations to consider?"
options:
  - label: "No i18n yet"
    description: "Single language — write copy translation-ready for future"
  - label: "Yes, with translation keys"
    description: "Use existing key structure, provide copy for all keys"
  - label: "Yes, multiple languages live"
    description: "Changes need coordination with translation team"
  - label: "Not sure"
    description: "Check the codebase for i18n setup before proceeding"
```

---

## ON_VOICE_CHANGE

```yaml
trigger: ON_VOICE_CHANGE
condition: "Request implies changing the product's voice or tone"
question: "Changing voice/tone affects the entire product. How should we approach this?"
options:
  - label: "Define new voice guidelines"
    description: "Create a new voice framework, then apply to specific areas"
  - label: "Audit and align to existing voice"
    description: "Find and fix inconsistencies with the current voice"
  - label: "A/B test voice variants"
    description: "Create variants for testing before full rollout"
  - label: "Apply to new feature only"
    description: "Use the new voice for this feature, keep existing elsewhere"
```

---

## ON_AUDIENCE_TYPE

```yaml
trigger: ON_AUDIENCE_TYPE
condition: "Target audience for the copy is unclear"
question: "Who is the primary audience for this copy?"
options:
  - label: "End users (non-technical)"
    description: "Plain language, no jargon, friendly tone"
  - label: "Developers / technical users"
    description: "Technical terms OK, precise, documentation-style"
  - label: "Mixed audience"
    description: "Plain language with optional technical details"
  - label: "Internal team"
    description: "Admin/internal tools, can assume domain knowledge"
```
