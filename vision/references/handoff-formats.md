# Handoff Formats

Standardized handoff templates for Vision's agent collaboration.

---

## Input Handoffs (→ Vision)

### NEXUS_TO_VISION_HANDOFF

```markdown
## NEXUS_TO_VISION_HANDOFF

**Task**: [Redesign / New product design / Design review / Trend application]
**Target**: [Repository path or application description]
**Framework**: [React / Vue / Svelte / HTML / auto-detect]
**Scope**: [Full redesign / Component-level / Page-level / Token-level]

**Context**:
- Brand assets: [Existing brand guidelines path or "none"]
- Current design system: [Existing tokens/styles path or "none"]
- Target audience: [Description]
- Business objectives: [Key goals]

**Request**: [Specific deliverable expected]
```

### RESEARCHER_TO_VISION_HANDOFF

```markdown
## RESEARCHER_TO_VISION_HANDOFF

**Research Summary**:
- Target Users: [Persona descriptions]
- Key Insights: [User behavior findings]
- Pain Points: [Identified UX issues]
- Competitor Analysis: [Competitive landscape]

**Design Implications**:
| Finding | Design Impact | Priority |
|---------|--------------|----------|
| [Finding] | [How it affects design] | [High/Med/Low] |

**Request**: Define design direction informed by these research findings
```

### SCOUT_TO_VISION_HANDOFF

```markdown
## SCOUT_TO_VISION_HANDOFF

**Design-Related Bugs**:
| Bug | Component | UX Impact | Severity |
|-----|-----------|-----------|----------|
| [Bug] | [Component] | [Impact] | [High/Med/Low] |

**Request**: Review design patterns causing recurring issues
```

---

## Output Handoffs (Vision →)

### VISION_TO_MUSE_HANDOFF

```markdown
## VISION_TO_MUSE_HANDOFF

### Design Direction Summary
- Visual Style: [Modern/Classic/Playful]
- Color Scheme: [Primary/Secondary tokens]
- Typography: [Font stack + scale]

### Token Specifications
[CSS variable definitions from Style Guide]

### Priority Components
1. [Component]: [Specific token application notes]
2. [Component]: [Specific token application notes]

### Dark Mode Requirements
- [Specific color adjustments]
- [Contrast requirements]

### Success Criteria
- [ ] All hardcoded values replaced with tokens
- [ ] Dark mode fully supported
- [ ] Spacing follows 8px grid
- [ ] Typography scale applied consistently
```

### VISION_TO_PALETTE_HANDOFF

```markdown
## VISION_TO_PALETTE_HANDOFF

### Heuristic Findings Summary
| Heuristic | Score | Primary Issue |
|-----------|-------|---------------|
| [Heuristic] | [1-5] | [Issue] |

### Priority Improvements
1. [Issue]: [Expected outcome]
2. [Issue]: [Expected outcome]

### Interaction Patterns to Apply
- [Pattern]: [Where to apply]
- [Pattern]: [Where to apply]

### Success Criteria
- [ ] Heuristic scores improved
- [ ] Feedback quality enhanced
- [ ] Error handling improved
```

### VISION_TO_FLOW_HANDOFF

```markdown
## VISION_TO_FLOW_HANDOFF

### Motion Philosophy
- Overall Feel: [Snappy/Smooth/Playful]
- Timing Convention: Fast (100-200ms), Normal (200-300ms), Slow (300-500ms)

### Priority Animations
| Element | Trigger | Animation | Duration | Easing |
|---------|---------|-----------|----------|--------|
| [Element] | [Trigger] | [Type] | [ms] | [easing] |

### Reduced Motion Requirements
- All animations must respect `prefers-reduced-motion`
- Alternative static states required

### Success Criteria
- [ ] Animations feel cohesive
- [ ] No layout thrashing
- [ ] Reduced motion supported
```

### VISION_TO_FORGE_HANDOFF

```markdown
## VISION_TO_FORGE_HANDOFF

### Prototype Scope
- Pages: [List of pages]
- Key Interactions: [List]

### Design Assets
- Moodboard: [Reference]
- Wireframes: [Reference]
- Token CSS: [Reference]

### Priority Features
1. [Feature]: [Functionality]
2. [Feature]: [Functionality]

### Success Criteria
- [ ] Core user flow functional
- [ ] Design tokens applied
- [ ] Responsive breakpoints working
```

### VISION_TO_ECHO_HANDOFF

```markdown
## VISION_TO_ECHO_HANDOFF

### Design Direction Summary
[Brief description of chosen direction]

### Validation Questions
1. [Question about user perception]
2. [Question about usability]
3. [Question about brand alignment]

### Test Scenarios
| Scenario | Expected Behavior | Persona |
|----------|-------------------|---------|
| [Scenario] | [Expected] | [Persona] |

### Success Criteria
- [ ] Positive user perception of direction
- [ ] Task completion rates maintained or improved
- [ ] Brand alignment confirmed
```
