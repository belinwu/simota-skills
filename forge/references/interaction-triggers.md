# Forge Interaction Triggers

Question templates for user decision points.

---

## Trigger Summary

| Trigger | Timing | When to Ask |
|---------|--------|-------------|
| BEFORE_PROTOTYPE_SCOPE | BEFORE_START | When defining the scope of the prototype |
| ON_TECH_CHOICE | ON_DECISION | When choosing implementation technology/framework |
| ON_MOCK_DATA | ON_DECISION | When deciding mock data strategy (inline/MSW/json-server) |
| ON_CORE_OVERWRITE | ON_RISK | When changes may affect core utilities or shared components |
| ON_LIBRARY_ADD | ON_RISK | When adding external libraries to the project |

---

## Question Templates

### BEFORE_PROTOTYPE_SCOPE

```yaml
questions:
  - question: "Confirming prototype scope. What level of implementation?"
    header: "Scope"
    options:
      - label: "Single component (Recommended)"
        description: "Focus on one UI component, minimal implementation"
      - label: "Full page"
        description: "Build entire flow for one screen"
      - label: "End-to-end"
        description: "Thin implementation from frontend to backend"
    multiSelect: false
```

### ON_TECH_CHOICE

```yaml
questions:
  - question: "Please select the implementation technology for the prototype."
    header: "Tech Choice"
    options:
      - label: "Use existing stack (Recommended)"
        description: "Implement with project's existing tech, no learning curve"
      - label: "Lightweight alternative"
        description: "Quick validation with vanilla JS/HTML"
      - label: "Try new technology"
        description: "Introduce new tech for validation purposes"
    multiSelect: false
```

### ON_MOCK_DATA

```yaml
questions:
  - question: "Please select the mock data strategy."
    header: "Mock Strategy"
    options:
      - label: "Inline constants (Recommended)"
        description: "Define data directly in file, fastest to run"
      - label: "MSW handlers"
        description: "Mock actual API requests, production-like behavior"
      - label: "json-server"
        description: "Start external mock server, full REST API emulation"
    multiSelect: false
```

### ON_CORE_OVERWRITE

```yaml
questions:
  - question: "This may affect existing core utilities. How would you like to proceed?"
    header: "Core Change"
    options:
      - label: "Implement in new file (Recommended)"
        description: "Build in new file without touching existing code"
      - label: "Copy and modify"
        description: "Copy existing code and adjust for prototype"
      - label: "Modify existing directly"
        description: "Change existing code with understanding of risks"
    multiSelect: false
```

### ON_LIBRARY_ADD

```yaml
questions:
  - question: "External library addition is needed. How would you like to proceed?"
    header: "Library"
    options:
      - label: "Use standard API (Recommended)"
        description: "Implement with fetch/DOM API, no new dependencies"
      - label: "Use lightweight library"
        description: "Achieve functionality with minimal library"
      - label: "Add full-featured library"
        description: "Introduce full library for future expansion"
    multiSelect: false
```
