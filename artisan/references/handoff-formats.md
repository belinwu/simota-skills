# Handoff Formats

Input and output handoff templates for Artisan's inter-agent collaboration.

---

## Input Handoffs (Receiving)

### FORGE_TO_ARTISAN_HANDOFF

Prototype ready for production implementation.

```yaml
FORGE_TO_ARTISAN_HANDOFF:
  Prototype:
    component: "[path/to/prototype.tsx]"
    purpose: "[What it does]"
    interactions: "[User interactions to support]"
  Production_Requirements:
    - "TypeScript strict mode"
    - "Proper error handling"
    - "Loading states"
    - "Accessibility"
    - "Responsive design"
  State_Requirements:
    local_state: "[fields]"
    shared_state: "[fields]"
    server_state: "[API calls]"
  Notes:
    - "[Design decisions from prototyping]"
```

### VISION_TO_ARTISAN_HANDOFF

Design direction defined, implementation needed.

```yaml
VISION_TO_ARTISAN_HANDOFF:
  Design_Direction:
    style: "[Design system / visual direction]"
    tokens: "[Design token references]"
    layout: "[Layout specifications]"
  Components:
    - name: "[Component name]"
      design_spec: "[Visual specification]"
      interactions: "[Expected interactions]"
  Constraints:
    - "[Responsive breakpoints]"
    - "[Browser support requirements]"
    - "[Performance budget]"
```

---

## Output Handoffs (Sending)

### ARTISAN_TO_BUILDER_HANDOFF

Frontend complete, backend integration needed.

```yaml
ARTISAN_TO_BUILDER_HANDOFF:
  Frontend_Complete:
    components: "[list of components]"
    state_management: "[approach used]"
    data_requirements: "[what data is needed]"
  API_Contract_Needed:
    - endpoint: "/api/xxx"
      method: "POST"
      request_shape: "{ ... }"
      response_shape: "{ ... }"
  Integration_Points:
    - component: "[component name]"
      action: "form submission"
      target: "[endpoint]"
    - component: "[component name]"
      action: "data fetching"
      data_needed: "[data description]"
  Notes:
    - "[Frontend assumptions about data shape]"
```

### ARTISAN_TO_SHOWCASE_HANDOFF

Components ready for Storybook stories.

```yaml
ARTISAN_TO_SHOWCASE_HANDOFF:
  Components:
    - name: "[Component name]"
      path: "[src/components/Component]"
      variants:
        - "[primary, secondary, disabled]"
  Story_Requirements:
    - "All variants documented"
    - "Interactive states (hover, focus, active)"
    - "Dark mode variants"
    - "Responsive variants"
  Props_Documentation:
    - "[Key props that need documentation]"
```

### ARTISAN_TO_RADAR_HANDOFF

Components ready for test coverage.

```yaml
ARTISAN_TO_RADAR_HANDOFF:
  Components:
    - name: "[Component name]"
      path: "[file path]"
      test_priority: "high | medium | low"
  Test_Requirements:
    - "User interaction tests"
    - "Error state coverage"
    - "Accessibility assertions"
    - "Loading state transitions"
  Framework:
    test_runner: "[Vitest / Jest]"
    testing_lib: "[React Testing Library / Vue Test Utils]"
```

---

## Output Report Format

Standard format for Artisan completion reports.

```markdown
## Component: [Component Name]

### Overview
**Framework:** [React/Vue/Svelte]
**State Management:** [Zustand/Pinia/Context/Local]
**Styling:** [Tailwind/CSS Modules/CSS-in-JS]

### Components Created
| Component | Path | Purpose |
|-----------|------|---------|
| [name] | [path] | [description] |

### State Design
| Store/Hook | Scope | Description |
|------------|-------|-------------|
| [name] | [local/global] | [what it manages] |

### Accessibility
- [A11y consideration 1]
- [A11y consideration 2]

### Performance Notes
- [Performance consideration]

### Verification
1. [Manual verification step 1]
2. [Manual verification step 2]
```
