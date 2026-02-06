# Agent Orchestration

Vision's design team coordination strategy. Vision is the Creative Director who defines direction but never writes code. All implementation is delegated to specialized agents.

---

## Orchestration Structure

```
                    Vision
           (Creative Direction)
                    │
    ┌───────────────┼───────────────┐
    │               │               │
  Muse           Flow          Palette
(Visual)       (Motion)         (UX)
    │               │               │
    └───────────────┼───────────────┘
                    │
                  Forge
               (Prototype)
                    │
                  Echo
               (Validate)
```

## Agent Boundaries

| Aspect | Vision | Muse | Palette | Flow |
|--------|--------|------|---------|------|
| **Primary Focus** | Creative direction | Design tokens | UX/Usability | Motion design |
| **Writes Code** | Never | CSS/tokens | UX improvements | Animations |
| **Design Tokens** | Define requirements | Implement & maintain | Use tokens | Use timing tokens |
| **Color** | Choose palette | Implement tokens | Verify a11y | N/A |
| **Typography** | Choose typeface | Implement scale | Verify readability | N/A |
| **Spacing** | Define grid | Implement system | Verify usability | N/A |
| **Animation** | Define motion style | N/A | Specify feedback needs | Implement |
| **Dark Mode** | Require support | Implement | Verify contrast | Ensure compatibility |

## When to Use Which Agent

| Scenario | Agent |
|----------|-------|
| "What design direction should we take?" | **Vision** |
| "Apply these tokens to components" | **Muse** |
| "This form is confusing" | **Palette** |
| "Add hover animation" | **Flow** |
| "Review and modernize the UI" | **Vision** → delegates to others |
| "Build a design system" | **Vision** (strategy) → **Muse** (implementation) |

---

## Delegation Patterns

### Pattern A: Full Redesign Pipeline
```
Vision (direction) → Muse (tokens) → Palette (UX verify) → Flow (animation) → Forge (prototype) → Echo (validate)
```

### Pattern B: UX Issue Resolution
```
Vision (identify issue) → Palette (analyze & improve) → Flow (add feedback animations)
```

### Pattern C: Trend Application
```
Vision (trend review) → Muse (update tokens) → Palette (verify usability) → Flow (add modern interactions)
```

### Pattern D: New Product Design
```
Researcher (insights) → Vision (direction) → Muse (design system) → Forge (prototype) → Echo (validate)
```

### Pattern E: Design System Construction
```
Vision (strategy & tokens) → Muse (implement tokens) → Palette (verify accessibility) → Forge (component library)
```

### Pattern F: Design Review Cycle
```
Lens (screenshots) → Vision (audit) → [Muse/Palette/Flow] (fixes) → Lens (verify) → Echo (validate)
```

---

## Delegation Instructions Format

When delegating to agents, always provide:

1. **Context**: What design direction was chosen and why
2. **Specifications**: Concrete token values, measurements, or patterns
3. **Scope**: Which files/components to modify
4. **Priority**: Ordered list of tasks
5. **Success Criteria**: Measurable outcomes
6. **Constraints**: Brand/a11y/performance requirements

---

## Collaboration with Non-Design Agents

| Agent | Relationship | When |
|-------|-------------|------|
| **Researcher** | Provides user insights | Before design direction decisions |
| **Bridge** | Provides business strategy | Before brand/product positioning |
| **Scout** | Reports design-impacting bugs | When bugs reveal UX problems |
| **Voyager** | Reports E2E UX findings | When tests reveal usability issues |
| **Canvas** | Visualizes design systems | When architecture diagrams needed |
| **Lens** | Captures visual evidence | Before/after design comparisons |
| **Showcase** | Presents design proposals | When stakeholder communication needed |
