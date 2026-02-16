# Cast Persona Model

Persona model definition with Echo-compatible template mapping and Cast metadata extensions.

---

## Overview

Cast personas are fully compatible with Echo's `persona-template.md` format, extended with metadata for lifecycle management. Any Echo-compatible persona file can be read by Cast, and any Cast-generated persona can be used directly by Echo.

```
┌─────────────────────────────────────────────────────────────┐
│                    Echo Template (Base)                       │
│  Frontmatter + Profile + Quote + Goals + Emotion Triggers    │
│  + Context Scenarios + JTBD + Testing Focus + Source         │
├─────────────────────────────────────────────────────────────┤
│                    Cast Extensions (Additive)                │
│  version + status + confidence + evolution_count + tags      │
│  + echo_base_mapping + cast_managed + Evolution Log          │
└─────────────────────────────────────────────────────────────┘
```

---

## Frontmatter Schema

### Echo Standard Fields (Required)

```yaml
---
name: [Persona Name]              # English recommended (e.g., "First-Time Buyer")
service: [service-identifier]     # Kebab-case (e.g., "ec-platform")
type: custom                      # custom | base | internal
category: user                    # user | developer | designer | business | operations
created: [YYYY-MM-DD]
source: [analyzed files/documents]
---
```

### Cast Extension Fields (Optional, Backward-Compatible)

```yaml
---
# Echo standard fields (above)

# Cast metadata extensions
version: "1.0"                    # Semantic version (major.minor)
status: active                    # Lifecycle status
updated: [YYYY-MM-DD]            # Last modification date
evolution_count: 0                # Number of evolutions applied
confidence: 0.65                  # Data-grounded confidence score (0.0-1.0)
tags: [b2c, e-commerce]          # Classification tags
echo_base_mapping: Newbie         # Mapping to Echo base persona
cast_managed: true                # Flag indicating Cast manages this persona
---
```

### Cast SPEAK Extension Fields (Optional)

SPEAK モードで使用する音声プロファイル。未定義時は Auto-Derivation で既存属性から自動推定。

```yaml
---
# Cast SPEAK extension (additive — optional)
voice_profile:
  # AI テキスト生成スタイル（セリフ生成プロンプトの制御パラメータ）
  speaking_style:
    formality: casual              # casual | polite | formal | technical
    vocabulary_level: simple       # simple | moderate | advanced | specialized
    sentence_length: short         # short | medium | long | mixed
    emotional_tone: anxious        # anxious | cheerful | neutral | frustrated | enthusiastic | reserved
    linguistic_markers: []         # ペルソナ固有の口癖 (例: ["〜したいだけなのに", "なんで〜なの？"])

  # macOS say エンジン設定
  say:
    voice: "Kyoko"                 # macOS say ボイス名
    rate: 180                      # WPM (90-300, default: 180)

  # edge-tts エンジン設定 (Neural TTS)
  edge_tts:
    voice: "ja-JP-NanamiNeural"    # edge-tts ボイス名
    rate: "+0%"                    # "-50%" to "+100%"
    pitch: "+0Hz"                  # "-50Hz" to "+50Hz"
    volume: "+0%"                  # "-50%" to "+50%"

  # Google Cloud TTS 設定 (Neural2/WaveNet — 明示指定時のみ使用、autoには含まない)
  google_tts:
    voice: "ja-JP-Neural2-B"      # Google Cloud TTS voice name
    speaking_rate: 1.0             # 0.25-4.0 (default: 1.0)
    pitch: 0.0                     # -20.0 to +20.0 semitones (default: 0)
    volume_gain_db: 0.0            # -96.0 to +16.0 dB (default: 0)

  language: ja                     # ja | en | auto
  engine_preference: auto          # auto | say | edge-tts | google_tts
---
```

#### voice_profile Field Definitions

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `speaking_style.formality` | enum | auto-derived | 口調のフォーマルさ |
| `speaking_style.vocabulary_level` | enum | auto-derived | 語彙の難易度 |
| `speaking_style.sentence_length` | enum | auto-derived | 文の長さ傾向 |
| `speaking_style.emotional_tone` | enum | auto-derived | 感情的なトーン |
| `speaking_style.linguistic_markers` | string[] | `[]` | 口癖・語尾パターン |
| `say.voice` | string | auto-derived | macOS `say` ボイス名 |
| `say.rate` | integer | `180` | Words Per Minute (90–300) |
| `edge_tts.voice` | string | auto-derived | edge-tts Neural ボイス名 |
| `edge_tts.rate` | string | `"+0%"` | 速度調整 (-50% to +100%) |
| `edge_tts.pitch` | string | `"+0Hz"` | ピッチ調整 (-50Hz to +50Hz) |
| `edge_tts.volume` | string | `"+0%"` | ボリューム調整 (-50% to +50%) |
| `google_tts.voice` | string | auto-derived | Google Cloud TTS ボイス名 |
| `google_tts.speaking_rate` | float | `1.0` | 発話速度 (0.25–4.0) |
| `google_tts.pitch` | float | `0.0` | ピッチ（半音単位、-20.0 to +20.0） |
| `google_tts.volume_gain_db` | float | `0.0` | 音量ゲイン (dB、-96.0 to +16.0) |
| `language` | enum | `ja` | 発話言語 (ja / en / auto) |
| `engine_preference` | enum | `auto` | TTS エンジン選択 (auto / say / edge-tts / google_tts) |

#### Design Notes

- `speaking_style` はテキスト生成制御、`say`/`edge_tts`/`google_tts` は音声合成パラメータ — 関心事を分離
- `google_tts` は課金保護のため `engine_preference: auto` に含まない（明示指定時のみ使用）
- `voice_profile` がなくても SPEAK モードは動作する（Auto-Derivation で既存属性から推定）
- 永続化は EVOLVE モードの既存メカニズムで対応（新メカニズム不要）
- → Auto-Derivation ルール詳細: `speak-engine.md`

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version` | string | Cast-managed | Semantic version, bumps on evolution |
| `status` | enum | Cast-managed | Lifecycle state (see below) |
| `updated` | date | Cast-managed | ISO 8601 date of last update |
| `evolution_count` | integer | Cast-managed | Cumulative evolution count |
| `confidence` | float | Cast-managed | 0.0–1.0, evidence-based score |
| `tags` | string[] | Optional | Classification labels for filtering |
| `echo_base_mapping` | string | Recommended | One of Echo's 11 base personas |
| `cast_managed` | boolean | Cast-managed | `true` when Cast controls lifecycle |

### Status Values

| Status | Description | Transitions To |
|--------|-------------|----------------|
| `draft` | Newly generated, not yet validated | `active` |
| `active` | Validated and in use | `evolved`, `archived` |
| `evolved` | Updated via EVOLVE mode (transient) | `active` |
| `archived` | No longer active, preserved for reference | — |

---

## Section Structure

### Required Sections (Echo Compatible)

Every Cast-generated persona includes these sections from Echo's template:

```markdown
# [Persona Name]

## Profile                           # Basic attributes (Role, Tech Level, Device, etc.)
## Quote                             # Symbolic statement from persona's perspective
## Goals                             # 3 goals (Functional, Emotional, Social)
## Frustrations                      # 3 primary frustrations
## Key Behaviors                     # 3 typical behaviors
## Emotion Triggers                  # Mapped to Echo's -3 to +3 scale
## Context Scenarios                 # 5-dimension situations (Physical/Temporal/Social/Cognitive/Technical)
## JTBD (Jobs-to-be-Done)           # Functional/Emotional/Social jobs
## Echo Testing Focus                # Priority flows for Echo validation
## Source Analysis                   # Evidence sources with extracted information
## Evolution Log                     # Cast-specific: version history (added at end)
```

### Optional Sections (Detail-Level Dependent)

Included based on data availability and requested detail level:

| Section | When to Include | Primary Use |
|---------|----------------|-------------|
| **Internal Profile** | `type: internal` | Development org personas |
| **Demographics** | B2C emphasis, age/location relevant | Font size, localization, pricing |
| **Psychographics** | Decision-making data available | CTA, copy, social proof |
| **Digital Behavior** | Analytics/session data available | Auto-save, sync design |
| **Literacy & Experience** | Onboarding/help data available | Terminology, help format |
| **Social Context** | B2B emphasis, org data available | Approval flow, sharing |
| **Life Stage** | Lifecycle/pricing data available | Upsell, onboarding length |
| **Workflow Context** | `type: internal` | Daily tasks, collaboration |

---

## Echo Base Persona Mapping

Every Cast persona should map to one of Echo's 11 base personas for framework reuse:

| Echo Base Persona | Cast Mapping Criteria |
|-------------------|----------------------|
| The Newbie | Low tech level, first-time use, high confusion potential |
| The Power User | High tech level, efficiency-focused, shortcut-seeking |
| The Skeptic | Trust-focused, privacy-conscious, comparison-driven |
| The Mobile User | Mobile-primary, constrained environment |
| The Senior | Accessibility needs, slower pace preference |
| Accessibility User | Assistive tech dependency, keyboard-only |
| Low-Literacy User | Limited reading, icon/visual preference |
| Competitor Migrant | Cross-service experience, pattern expectations |
| Distracted User | Multi-tasking, frequent interruptions |
| Privacy Paranoid | Data-request questioning, abandonment-prone |
| Custom Persona | No clear base mapping (project-specific) |

### Mapping Rules

1. Map based on **dominant behavioral trait**, not demographics
2. A single Cast persona maps to **exactly one** Echo base persona
3. If multiple bases apply, choose the one most relevant to the service's primary flow
4. Use `Custom Persona` only when no base persona reasonably fits
5. Record mapping rationale in Source Analysis section

---

## Confidence Scoring Model

### Calculation

Confidence is the sum of source contributions, capped at 1.0:

```
confidence = min(1.0, Σ source_contributions)
```

### Source Contribution Values

| Source Type | Contribution | Evidence Required |
|-------------|-------------|-------------------|
| User interview (via Researcher) | +0.30 | Interview transcript/summary reference |
| Session replay (via Trace) | +0.25 | Session pattern data reference |
| User feedback (via Voice) | +0.20 | Feedback segment reference |
| Analytics data (via Pulse) | +0.20 | Metric/funnel data reference |
| Code/documentation analysis | +0.15 | File path + extracted attribute |
| README analysis only | +0.10 | README content reference |
| Inference (no direct evidence) | +0.05 | Marked with `[inferred]` |

### Confidence Decay Rules

→ Decay algorithm details: `evolution-engine.md`

### Attribute-Level Confidence

Individual attributes can carry confidence markers:

```markdown
| Attribute | Value |
|-----------|-------|
| Role | Online shopper |
| Tech Level | Medium [inferred] |
| Device | Mobile (65%) [Trace data] |
```

- `[inferred]` — No direct evidence, derived from context
- `[source name]` — Attributed to specific data source
- No marker — Multiple sources confirm

---

## Detail Levels

Cast supports 4 detail levels for persona generation:

### Minimal

Required fields only. Fast generation, suitable for quick exploration.

```markdown
# [Name]
## Profile
## Quote
## Goals / Frustrations / Behaviors
## Emotion Triggers
## Echo Testing Focus
## JTBD
## Source Analysis
## Evolution Log
```

### Standard

Core + primary extended attributes based on service type.

```markdown
# [Name]
## Profile
## Demographics [if B2C-relevant]
## Quote
## Psychographics [if decision data available]
## Goals / Frustrations / Behaviors
## Emotion Triggers
## Context Scenarios
## JTBD
## Echo Testing Focus
## Source Analysis
## Evolution Log
```

### Full

All available sections populated. For complex B2B/B2C services.

```markdown
# [Name]
## Profile
## Demographics
## Quote
## Psychographics
## Digital Behavior
## Literacy & Experience
## Social Context
## Life Stage
## Goals / Frustrations / Behaviors
## Emotion Triggers
## Context Scenarios
## JTBD
## Echo Testing Focus
## Source Analysis
## Evolution Log
```

### Internal

Development organization personas with workflow context.

```markdown
# [Name]
## Profile
## Internal Profile
## Quote
## Workflow Context
## Goals / Frustrations / Behaviors
## Emotion Triggers
## Context Scenarios
## JTBD
## Echo Testing Focus
## Source Analysis
## Evolution Log
```

---

## Versioning Rules

| Change Type | Version Bump | Example |
|-------------|-------------|---------|
| Attribute value update | Minor (x.Y) | 1.0 → 1.1 |
| New section added | Minor (x.Y) | 1.1 → 1.2 |
| Multiple attributes changed | Minor (x.Y) | 1.2 → 1.3 |
| Core Identity change | Major (X.0) — triggers new persona | 1.3 → (new persona 1.0) |
| Status change | No version bump | — |

---

## Example Persona (Cast-Generated, Abbreviated)

```markdown
---
name: First-Time Buyer
service: ec-platform
type: custom
category: user
created: 2026-02-01
source: [README.md, src/checkout/*, docs/user-guide.md]
version: "1.2"
status: active
updated: 2026-02-15
evolution_count: 2
confidence: 0.82
tags: [b2c, e-commerce, mobile-first]
echo_base_mapping: Newbie
cast_managed: true
---

# First-Time Buyer

## Profile

| Attribute | Value |
|-----------|-------|
| Role | Online shopper (first purchase) |
| Tech Level | Low-Medium [inferred] |
| Device | Mobile (70%) [Trace data], Desktop (30%) |

## Quote
> "買い物したいだけなのに、なんでこんなに入力が多いの？"

## Goals
1. Purchase desired item quickly and safely
2. Feel confident the purchase is secure
3. Get a good deal compared to alternatives

## Frustrations
1. Complex registration requiring too many fields
2. Unclear shipping costs until checkout
3. No guest checkout option

## Key Behaviors
- Compares prices across 2-3 sites before purchasing
- Abandons cart if registration is required before viewing total

## Emotion Triggers
| State | Trigger |
|-------|---------|
| Delighted (+3) | Found item cheaper than expected with free shipping |
| Frustrated (-2) | Required to create account before viewing cart total |
| Abandoned (-3) | Hidden fees revealed at final checkout step |

## Context Scenarios
### Scenario 1: Commute Shopping
Physical: Crowded train, one hand free · Temporal: 15min window · Social: Semi-public · Cognitive: Distracted · Technical: Mobile, unstable connection

## JTBD
- Functional: Purchase item and have it delivered reliably
- Emotional: Feel confident and not cheated
- Social: Be seen as a smart shopper

## Echo Testing Focus
- [ ] Product search → cart → checkout (guest flow)
- [ ] Mobile checkout form usability

## Source Analysis
| Source | Extracted Information |
|--------|----------------------|
| README.md | "perfect for first-time shoppers", mobile-first design |
| Trace session data (2026-02-08) | 70% mobile sessions, avg 3.2 page views |
| Voice NPS feedback (2026-02-14) | "shipping cost surprise" in 23% of detractors |

## Evolution Log
| Version | Date | Source | Changes | Confidence Delta |
|---------|------|--------|---------|-----------------|
| 1.0 | 2026-02-01 | README, src/checkout | Initial creation | 0.65 |
| 1.2 | 2026-02-15 | Voice NPS feedback | Shipping frustration added | +0.07 |
```

---

## Backward Compatibility

### Reading Existing Personas

Cast can read any Echo-format persona file:
- If `cast_managed` is absent → treat as unmanaged (read-only unless user requests Cast to adopt)
- If Cast metadata fields are missing → infer defaults: `version: "1.0"`, `status: active`, `confidence: 0.50`
- Never modify an unmanaged persona without explicit request

### Adopting Existing Personas

When asked to manage existing Echo personas:
1. Add Cast metadata to frontmatter (additive only)
2. Append Evolution Log section at end
3. Calculate initial confidence from Source Analysis
4. Register in registry.yaml
5. Set `cast_managed: true`

### Non-Cast Consumers

Agents that don't understand Cast extensions simply ignore the extra frontmatter fields and the Evolution Log section. The persona remains fully functional as a standard Echo persona.
