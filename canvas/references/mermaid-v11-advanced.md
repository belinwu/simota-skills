# Mermaid v11 Advanced Reference

Purpose: Read this when you need Mermaid v11-specific capabilities, advanced layout options, or renderer compatibility guidance.

## Contents

- Version-gated features
- Configuration rules
- ELK guidance
- Anti-patterns

## Version-Gated Features

| Feature | Minimum Version | Use When |
|---------|-----------------|----------|
| Architecture diagrams | `v11.1.0+` | You need service and infrastructure views |
| Kanban / Packet / Block / Radar | `v11+` | The user explicitly asks for newer Mermaid diagram families |
| Semantic shapes | `v11.3.0+` | You want richer shape vocabulary |
| Per-edge curves | `v11.10.0+` | One curve style per relationship matters |

## Configuration Rule

- Prefer frontmatter config.
- Treat old `%%{init:}%%` directives as legacy and avoid them in new output.

## ELK Guidance

Use ELK when:

- The graph approaches `100+` nodes
- Layout overlap is severe
- The renderer supports ELK

## Anti-Patterns

- Do not assume Mermaid is a pixel-perfect layout tool.
- Do not use v11-only syntax against unknown renderers.
- Do not keep old init directives in newly generated diagrams.
