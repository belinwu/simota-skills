# AI Reverse Engineering Reference

Purpose: Read this when static extraction is insufficient and you need LLM-assisted synthesis from code, specs, or mixed artifacts.

## Contents

- When to use AI assistance
- Extraction workflow
- Static analysis helpers
- Verification rules
- Limits and mitigations

## Use AI Assistance When

- The codebase is large and cross-cutting
- Symbol extraction alone misses intent or runtime relationships
- You need a best-effort candidate before manual verification
- The requested diagram spans multiple layers of abstraction

## Workflow

1. Inventory the source files, routes, models, and key symbols.
2. Extract concrete facts first with static tools or code search.
3. Ask the model to propose a diagram shape from verified facts.
4. Cross-check every node and edge against source files.
5. Mark uncertainty explicitly instead of inventing structure.

## Static Analysis Helpers

| Tool | Useful for |
|------|------------|
| `pyan` | Python call graphs |
| `PyCG` | Python call graph extraction |
| `code2flow` | Multi-language flow approximation |
| `callGraph` | Dependency and call structure |
| `PhpDependencyAnalysis` | PHP dependency extraction |

## Guardrails

- Treat the model as a synthesis step, not a source of truth.
- Do not add nodes, relationships, or state transitions that cannot be traced back.
- Prefer a simpler diagram over a speculative one.
- If the model output and source disagree, the source wins.

## Mitigation Patterns

| Risk | Mitigation |
|------|------------|
| Hallucinated edge | Require source citation for each relationship |
| Wrong abstraction | Narrow the scope and redraw |
| Missing runtime nuance | Add a note: static approximation only |
| Too much density | Split into one clearer diagram per question |
