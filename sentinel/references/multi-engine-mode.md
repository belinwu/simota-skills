# Multi-Engine Mode

Three AI engines independently scan for vulnerabilities, then merge findings (**Union pattern**).
Different security knowledge bases across engines catch vulnerabilities that a single scan would miss.

---

## Activation

Triggered by Sentinel's own judgment or when instructed via Nexus with `multi-engine`.

## Engine Dispatch

| Engine | Command | Fallback |
|--------|---------|----------|
| Codex | `codex exec --full-auto` | Claude subagent |
| Gemini | `gemini -p --yolo` | Claude subagent |
| Claude | Claude subagent (Task) | — |

When an engine is unavailable (`which` fails), Claude subagent takes over.

---

## Loose Prompt Design

Pass only minimal context. Do not specify OWASP categories or vulnerability patterns.
Let each engine decide on its own what is dangerous.

**Pass:**
1. **Role** — one line: "Security auditor. Find vulnerabilities in code."
2. **Target code** — source to scan
3. **Context** — usage type (Web API / CLI / library, etc.)
4. **Output format** — vulnerability report: location, type, severity, fix suggestion

**Do NOT pass:** OWASP checklists, detailed vulnerability pattern descriptions, scanning procedures

---

## Dispatch: Codex / Gemini (External CLI)

```bash
codex exec --full-auto "$(cat /tmp/sentinel-prompt.md)"   # Codex
gemini -p "$(cat /tmp/sentinel-prompt.md)" --yolo          # Gemini
```

## Dispatch: Claude (Task tool)

```yaml
Task:
  subagent_type: general-purpose
  mode: dontAsk
  description: "Sentinel vulnerability scan"
  prompt: |
    As a security auditor, find vulnerabilities in the following code.
    For each finding, report location, type, severity, and fix suggestion.
    {target code}
    {context}
```

---

## Result Merge (Union)

1. Collect findings from all 3 engines
2. Deduplicate same-location, same-type findings
3. Sort all unique vulnerabilities by severity into a unified report
4. Boost confidence for items detected by multiple engines
