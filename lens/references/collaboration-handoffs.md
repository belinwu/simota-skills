# Collaboration & Handoff Reference

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT PROVIDERS                          │
│  Cipher → Clarified investigation question                  │
│  Nexus → Routed investigation request                       │
│  User → Direct codebase questions                           │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
            ┌─────────────────┐
            │      LENS       │
            │  Comprehension  │
            │   Specialist    │
            └────────┬────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                   OUTPUT CONSUMERS                          │
│  Builder → Implementation context, code locations           │
│  Artisan → Frontend structure understanding                 │
│  Sherpa → Task breakdown with codebase context              │
│  Atlas → Architecture analysis input                        │
│  Scribe → Documentation material                            │
│  Canvas → Visualization data (flow diagrams, structure)     │
└─────────────────────────────────────────────────────────────┘
```

---

## Handoff Templates

### LENS_TO_BUILDER_HANDOFF

```markdown
## BUILDER_HANDOFF (from Lens)

### Codebase Context
- **Architecture:** [Pattern and key layers]
- **Relevant Modules:** [Modules that will be touched]
- **Conventions:** [Key patterns to follow]

### Target Area
- **Files:** [Specific files to modify]
- **Entry Points:** [Where changes should start]
- **Dependencies:** [What the target depends on]

### Implementation Notes
- [Convention to follow]
- [Related code to reference]
- [Potential pitfalls]

Suggested command: `/Builder implement [feature] in [location]`
```

### LENS_TO_SCRIBE_HANDOFF

```markdown
## SCRIBE_HANDOFF (from Lens)

### Documentation Material
- **Subject:** [What to document]
- **Architecture:** [Structure findings]
- **Key Flows:** [Flow trace results]
- **Conventions:** [Detected patterns]

### Source Files
| Topic | Source | Key Lines |
|-------|--------|-----------|

Suggested command: `/Scribe create documentation for [module]`
```

### LENS_TO_CANVAS_HANDOFF

```markdown
## CANVAS_HANDOFF (from Lens)

### Visualization Request
- **Type:** [Flow diagram / Structure map / Data flow]
- **Subject:** [What to visualize]

### Data
[Structured data from TRACE/CONNECT phases]

Suggested command: `/Canvas create [diagram type] for [subject]`
```
