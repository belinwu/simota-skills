# Muse Handoff Formats

Standardized handoff templates for agent collaboration.

---

## Input Handoffs (→ Muse)

### FORGE_TO_MUSE_HANDOFF

```markdown
## FORGE_TO_MUSE_HANDOFF

**Prototype Created**: [Component/page description]
**Prototype Location**: [File path]
**Visual State**: [Has styling / Unstyled / Partial]

**Token Needs**:
- Colors: [brand colors used / hardcoded values present]
- Spacing: [consistent / inconsistent / magic numbers]
- Typography: [follows scale / ad-hoc sizes]

**Request**: Apply design tokens to prototype, ensure design system compliance
```

### VISION_TO_MUSE_HANDOFF

```markdown
## VISION_TO_MUSE_HANDOFF

**Creative Direction**: [Design brief description]
**Brand Guidelines**: [File path or description]
**Color Palette**: [Primary, secondary, accent colors]
**Typography Direction**: [Font families, scale preference]

**Token Requirements**:
- New tokens needed: [list]
- Existing tokens to update: [list]
- Dark mode: [required / optional]

**Request**: Implement design direction as design tokens
```

### ARTISAN_TO_MUSE_HANDOFF

```markdown
## ARTISAN_TO_MUSE_HANDOFF

**Component Built**: [Component name]
**Component Location**: [File path]
**Styling Approach**: [Tailwind / CSS Modules / styled-components]

**Token Issues Found**:
- Hardcoded values: [count and examples]
- Missing tokens: [tokens that should exist]
- Inconsistencies: [description]

**Request**: Audit and tokenize component styles
```

### NEXUS_TO_MUSE_HANDOFF

```markdown
## NEXUS_TO_MUSE_HANDOFF

**Design Task**: [Description]
**Type**: [Token audit / Dark mode / System construction / Token application]
**Target**: [Specific files or components]

**Context**:
- Project: [project description]
- Framework: [Tailwind / CSS variables / Panda CSS / etc.]
- Dark mode: [required / existing / not needed]
- Existing tokens: [path to token files if any]

**Request**: [Specific design system deliverable]
```

---

## Output Handoffs (Muse →)

### MUSE_TO_PALETTE_HANDOFF

```markdown
## MUSE_TO_PALETTE_HANDOFF

**Visual Change**: [Description of token/color change]
**Files Changed**:
| File | Change |
|------|--------|
| [path] | [what changed] |

**Colors Involved**:
- Background: [token or value]
- Foreground: [token or value]
- Interactive: [token or value]

**A11y Checks Required**:
- [ ] Contrast ratio meets WCAG AA (4.5:1 text, 3:1 UI)
- [ ] Focus states visible on all backgrounds
- [ ] Color is not sole indicator of state
- [ ] Works in both light and dark modes

**Request**: Verify accessibility compliance for color changes
```

### MUSE_TO_FLOW_HANDOFF

```markdown
## MUSE_TO_FLOW_HANDOFF

**Tokens Created**: [Animation/transition related tokens]
**Token Values**:
| Token | Value | Purpose |
|-------|-------|---------|
| --duration-fast | 150ms | Micro-interactions |
| --duration-normal | 300ms | Standard transitions |
| --duration-slow | 500ms | Page transitions |
| --easing-default | cubic-bezier(0.4, 0, 0.2, 1) | Standard ease |

**Request**: Apply motion tokens to component transitions
```

### MUSE_TO_CANVAS_HANDOFF

```markdown
## MUSE_TO_CANVAS_HANDOFF

**Design System Created**: [System name or scope]
**Visualization Needed**:
- [ ] Color palette diagram (primitive + semantic)
- [ ] Typography scale visualization
- [ ] Spacing system grid
- [ ] Token dependency graph

**Token Data**:
| Category | Count | Key Tokens |
|----------|-------|------------|
| Colors | [N] | primary, neutral, semantic |
| Spacing | [N] | 8px grid scale |
| Typography | [N] | Major third scale |

**Request**: Create design system visualization diagrams
```

### MUSE_TO_SHOWCASE_HANDOFF

```markdown
## MUSE_TO_SHOWCASE_HANDOFF

**Tokens Updated**: [Description of changes]
**Token Files**:
| File | Purpose |
|------|---------|
| [path] | [description] |

**Storybook Updates Needed**:
- [ ] Token documentation stories
- [ ] Color palette story
- [ ] Typography scale story
- [ ] Spacing reference story
- [ ] Dark mode toggle decorator

**Request**: Update Storybook token documentation
```

### MUSE_TO_JUDGE_HANDOFF

```markdown
## MUSE_TO_JUDGE_HANDOFF

**Design System Code Written**: [Description]
**Files Changed**:
| File | Lines | Change |
|------|-------|--------|
| [path] | [N] | [what changed] |

**Review Focus Areas**:
- Token naming: [consistent with conventions?]
- Dark mode: [all tokens have dark variants?]
- No hardcoded values: [magic numbers eliminated?]
- Framework compat: [works with project's CSS framework?]

**Request**: Review design system code quality
```

---

## Collaboration Patterns

### Pattern A: Prototype Tokenization
```
Forge (prototype) → FORGE_TO_MUSE → Muse (tokenize) → MUSE_TO_PALETTE → Palette (a11y)
```

### Pattern B: Creative Direction Implementation
```
Vision (direction) → VISION_TO_MUSE → Muse (tokens) → MUSE_TO_SHOWCASE → Showcase (docs)
```

### Pattern C: Component Audit
```
Artisan (component) → ARTISAN_TO_MUSE → Muse (audit + fix) → MUSE_TO_JUDGE → Judge (review)
```

### Pattern D: Full Design System Pipeline
```
Vision → Muse (tokens) → MUSE_TO_PALETTE → Palette (a11y) → MUSE_TO_FLOW → Flow (motion) → MUSE_TO_SHOWCASE → Showcase (docs)
```

### Pattern E: Dark Mode Implementation
```
Muse (dark mode) → MUSE_TO_PALETTE → Palette (contrast check) → Muse (adjust) → MUSE_TO_JUDGE → Judge (review)
```

### Pattern F: Token Sync
```
Figma → Muse (sync + transform) → MUSE_TO_SHOWCASE → Showcase (update stories)
```

### Pattern G: Design System Visualization
```
Muse (system created) → MUSE_TO_CANVAS → Canvas (diagrams) → MUSE_TO_SHOWCASE → Showcase (catalog)
```
