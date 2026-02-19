# Cast Generation Workflows

Detailed workflow for CONJURE mode — rapid persona generation from diverse inputs.

---

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                 1. INPUT_ANALYSIS                             │
│  Identify source type, assess data quality, plan extraction  │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────────┐
│                 2. DATA_EXTRACTION                            │
│  Extract persona-relevant signals from each source           │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────────┐
│                 3. PERSONA_SYNTHESIS                          │
│  Synthesize extracted data into persona structure             │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
...
```

---

## Phase 1: INPUT_ANALYSIS

### Source Detection

When no explicit path is provided, Cast auto-detects sources in priority order:

| Priority | Source | What to Look For | Confidence Contribution |
|----------|--------|-------------------|------------------------|
| P0 | `.agents/personas/` | Existing personas to adopt/enrich | — |
| P1 | `README.md` | Target users, usage scenarios | +0.10 |
| P2 | `docs/**/*.md` | User guides, tutorials, personas | +0.15 |
| P3 | `src/**/auth*`, `src/**/user*` | Auth flows, user models, roles | +0.15 |
| P4 | `src/**/checkout*`, `src/**/onboard*` | User journeys, conversion paths | +0.15 |
| P5 | `tests/e2e/**` | Test scenarios as user stories | +0.10 |
| P6 | `package.json`, `*.config.*` | Project metadata, feature flags | +0.05 |

### Source Detection (Internal Personas)

| Priority | Source | What to Look For |
|----------|--------|-------------------|
| P0 | `CODEOWNERS`, `.github/CODEOWNERS` | Team structure, responsibility areas |
| P1 | `docs/CONTRIBUTING.md` | Development flow, guidelines |
| P2 | `.vscode/**`, `.idea/**`, `.editorconfig` | Development environment |
| P3 | `docker-compose*.yml` | Local development setup |
| P4 | `.github/workflows/*` | CI/CD workflows |
| P5 | `Makefile`, `scripts/**` | Development commands, automation |
| P6 | `docs/runbook*`, `docs/onboarding*` | Operations and onboarding |

### Input Quality Assessment

For each source, assess quality before extraction:

| Quality Factor | High | Medium | Low |
|---------------|------|--------|-----|
| **Explicitness** | "for developers" explicitly stated | Implied from context | Guessed from file names |
| **Recency** | Updated within 30 days | Updated within 90 days | 90+ days stale |
| **Specificity** | Named user types with details | General user mentions | No user mentions |
| **Breadth** | Multiple user dimensions covered | Some dimensions covered | Single dimension only |

---

## Phase 2: DATA_EXTRACTION

### Extraction Strategy by Source Type

#### A. Documentation Analysis

```markdown
## Extraction Keywords

### User Types
- "for developers", "for teams", "for enterprises"
- "beginner", "advanced", "admin", "guest"
- "customer", "admin", "user", "member", "subscriber"
- Role enumerations in any form

### Usage Scenarios
- "when you need to...", "use case:", "example:"
- "in cases like...", "perfect for..."
- Workflow descriptions, step-by-step guides

### Tech Level
- "no coding required" → Low
...
```

#### B. Code Structure Analysis

```markdown
## Code Analysis

### User Models
- `user.role`, `user.type`, `user.tier`, `user.plan`
- Enum/union types for user classifications
- Permission levels, access control lists
- Pricing tiers, subscription models

### Flow Analysis
- Route definitions → user journeys
- Form components → required inputs / friction points
- Error handlers → frustration triggers
- Loading states → patience requirements

### Feature Flags
...
```

#### C. Test Scenario Analysis

```markdown
## Test Analysis

### E2E Tests
- Test descriptions → user stories
- Test steps → expected flows
- Assertions → success criteria
- Test fixtures → user types

### User Stories in Tests
- "as a [role], I want to [action]"
- describe/it blocks with user context
- Test data factories → user archetypes
```

#### D. Handoff Data Analysis (from other agents)

```markdown
## Handoff Data Analysis

### From Researcher
- Interview transcripts → direct quotes, pain points, goals
- Survey results → demographics, psychographics
- Usability test findings → behavior patterns
- Affinity diagrams → theme clusters

### From Trace
- Session patterns → behavioral clusters
- Drop-off points → frustration indicators
- Navigation patterns → mental models
- Device/time distributions → context

### From Voice
...
```

### Extraction Output Format

```yaml
extracted:
  service_context:
    name: "ec-platform"
    type: "b2c"                    # b2b | b2c | both
    primary_platform: "mobile"     # mobile | desktop | both

  user_types:
    - name: "First-Time Buyer"
      evidence: "README.md line 42: 'perfect for first-time shoppers'"
      confidence: 0.15
    - name: "Enterprise Admin"
      evidence: "src/models/user.ts: role enum includes 'admin'"
      confidence: 0.15

  goals:
# ...
```

---

## Phase 3: PERSONA_SYNTHESIS

### Generation Rules

1. **Minimum 3 personas**: Primary (P0), Secondary (P1), Edge Case (P2)
2. **Map to Echo base personas**: Every persona gets an `echo_base_mapping`
3. **Evidence required**: Every attribute must reference a source
4. **Inferred marker**: Use `[inferred]` for attributes without direct evidence
5. **Confidence calculation**: Sum source contributions per persona

### Persona Priority Assignment

| Priority | Criteria | Example |
|----------|----------|---------|
| P0 (Primary) | Most common user type, highest data support | "Regular Buyer" |
| P1 (Secondary) | Second most common or business-critical | "Enterprise Admin" |
| P2 (Edge Case) | Underserved or high-friction segment | "Accessibility User" |
| P3+ (Additional) | Only if data strongly supports additional segments | "Competitor Migrant" |

### Synthesis Process

For each identified user type:

1. **Select Echo base mapping** based on dominant behavioral trait
2. **Populate Profile** from extracted user type data
3. **Compose Quote** from extracted pain points / goals (in Japanese)
4. **Map Goals** from extracted functional/emotional/social goals
5. **Map Frustrations** from extracted pain points
6. **Map Behaviors** from extracted behavioral patterns
7. **Compose Emotion Triggers** mapped to Echo's -3 to +3 scale
8. **Build Context Scenarios** from extracted usage contexts
9. **Derive JTBD** from goals and behaviors
10. **Define Echo Testing Focus** from primary user flows
11. **Record Source Analysis** with all evidence references
12. **Initialize Evolution Log** as version 1.0

### Detail Level Selection

```
IF user specifies detail level:
  Use specified level
ELSE IF extracted data covers 4+ extended dimensions:
  Use "Full"
ELSE IF extracted data covers 2-3 extended dimensions:
  Use "Standard"
ELSE IF type == internal:
  Use "Internal"
ELSE:
  Use "Minimal"
```

---

## Phase 4: VALIDATION

### Echo Compatibility Check

Verify generated persona against Echo's template requirements:

| Check | Rule | Action on Failure |
|-------|------|-------------------|
| Frontmatter fields | All Echo required fields present | Add missing fields with defaults |
| Profile section | Role, Tech Level, Device, Usage Context, Frequency present | Infer from other data |
| Quote section | Non-empty, in Japanese | Generate from goals/frustrations |
| Goals/Frustrations/Behaviors | Exactly 3 each | Merge or split to reach 3 |
| Emotion Triggers | 5 triggers covering +3, +2, -1, -2, -3 | Generate from context |
| Echo Testing Focus | At least 3 flows with checkboxes | Derive from JTBD |
| Source Analysis | At least 1 source | Error — cannot generate without source |

### Consistency Check

| Check | Rule |
|-------|------|
| Tech Level vs Behaviors | Low tech level should not have "uses keyboard shortcuts" |
| Device vs Context | Mobile-primary should have mobile context scenarios |
| Goals vs Frustrations | Should not contradict each other |
| Echo mapping vs Profile | Mapping should match dominant trait |

### Confidence Threshold

| Confidence | Status | Action |
|------------|--------|--------|
| ≥ 0.6 | `active` | Persona ready for use |
| 0.4 – 0.59 | `draft` | Usable but recommend enrichment |
| < 0.4 | `draft` | Warning — insufficient data, ask user |

---

## Phase 5: REGISTRATION

### File Operations

1. **Create directory** if not exists: `.agents/personas/{service-name}/`
2. **Write persona file**: `{persona-name}.md` (kebab-case)
3. **Update registry**: Add entry to `.agents/personas/registry.yaml`
4. **Report**: Output summary of generated personas

### Naming Convention

```
.agents/personas/{service-name}/{persona-name}.md

Examples:
.agents/personas/ec-platform/first-time-buyer.md
.agents/personas/ec-platform/power-shopper.md
.agents/personas/ec-platform/accessibility-user.md
.agents/personas/admin-dashboard/it-admin.md
```

Rules:
- Service name: kebab-case, matches project/service identifier
- Persona name: kebab-case, descriptive of the persona's primary trait
- No spaces, no uppercase in file names
- Internal personas: same directory, differentiated by `type: internal` in frontmatter

### Registration Summary Output

```markdown
## Cast: Persona Generation Complete

**Service:** ec-platform
**Personas generated:** 3
**Detail level:** Standard
**Registry updated:** ✅

| Persona | Priority | Echo Mapping | Confidence | File |
|---------|----------|-------------|------------|------|
| First-Time Buyer | P0 | Newbie | 0.65 | `first-time-buyer.md` |
| Power Shopper | P1 | Power User | 0.60 | `power-shopper.md` |
| Mobile Browser | P2 | Mobile User | 0.55 | `mobile-browser.md` |

**Sources analyzed:** README.md, src/checkout/*, docs/user-guide.md
**Next recommended:** `/Echo review with saved personas` or `/Cast fuse from trace`
```

---

## Auto-Detection Triggers

Cast can be auto-suggested when:

1. **Echo finds no saved personas** — Suggest `/Cast conjure` before review
2. **Researcher completes persona creation** — Suggest `/Cast fuse from researcher` to register
3. **Trace delivers behavioral data** — Suggest `/Cast evolve` with new patterns
4. **New service added to project** — Suggest `/Cast conjure for {service}`

---

## Internal Persona Generation

### Additional Rules for Internal Personas

1. Set `type: internal` and appropriate `category` (developer/designer/business/operations)
2. Include Internal Profile section (Job Type, Team, Experience, Responsibility)
3. Include Workflow Context section (Daily Tasks, Collaboration, Pain Points)
4. Map to Internal Base Personas (from Echo's persona-template.md)
5. Focus Emotion Triggers on DX/workflow experiences
6. Focus Echo Testing Focus on internal tools, docs, workflows

### Job Type Detection

| Signal | Inferred Job Type |
|--------|-------------------|
| CODEOWNERS: `@frontend-team` | Frontend Developer |
| CODEOWNERS: `@backend-team` | Backend Developer |
| CODEOWNERS: `@infra-team` | Infra Engineer |
| CODEOWNERS: `@qa-team` | QA Engineer |
| Storybook/Figma references | UI Designer |
| docs/runbook* exists | Ops Manager |
| admin/ directory exists | Content Editor / CS Representative |
| docs/onboarding* exists | New Engineer |
