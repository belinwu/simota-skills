# Diagram Tools Comparison

Purpose: Read this when Mermaid is not sufficient and you need to choose another diagram format or tool.

## Contents

- Tool comparison
- Selection rules

## Comparison

| Tool | Best For | Tradeoff |
|------|----------|----------|
| Mermaid | Default docs-native diagrams | Limited pixel-level control |
| draw.io | Editable diagrams, workshops, handoff artifacts | XML overhead |
| D2 | Layout-heavy text diagrams | Extra toolchain |
| PlantUML | UML-heavy diagrams | Less native in modern docs flows |
| Structurizr | C4 at scale | Stronger setup dependency |
| ASCII | Terminal/comments/accessibility fallback | Low visual density |

## Selection Rules

- Use Mermaid by default.
- Use draw.io when the user needs editable output.
- Use D2 or PlantUML only when the user explicitly requests them or their feature set solves a real limitation.
- Use Structurizr when the task is large-scale C4 architecture and the environment already supports it.
- Use ASCII for plain text, comments, or fallback.
