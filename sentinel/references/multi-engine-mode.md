# Multi-Engine Mode

Purpose: Dispatch independent security scans and merge by union when one engine may miss logic, context, or framework-specific findings.

## Activation

- Trigger when the user or Nexus explicitly requests `multi-engine`.
- Trigger when findings are ambiguous, cross-domain, or likely to benefit from multiple security knowledge bases.
- Fall back to the Claude subagent when an external engine is unavailable.

## Dispatch

| Engine | Command | Fallback |
|--------|---------|----------|
| Codex | `codex exec --full-auto` | Claude subagent |
| Gemini | `gemini -p --yolo` | Claude subagent |
| Claude | Claude subagent (`Task`) | — |

## Prompt Contract

Pass only minimal context. Let each engine decide what is dangerous.

**Pass:**
1. Role: one line, for example `Security auditor. Find vulnerabilities in code.`
2. Target code
3. Usage context, for example Web API, CLI, library, worker
4. Output format: location, type, severity, fix suggestion

**Do not pass:**
- OWASP checklists
- detailed vulnerability pattern catalogs
- step-by-step scanning procedures

## External CLI Dispatch

```bash
codex exec --full-auto "$(cat /tmp/sentinel-prompt.md)"   # Codex
gemini -p "$(cat /tmp/sentinel-prompt.md)" --yolo         # Gemini
```

## Claude Task Dispatch

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

## Merge Rules

1. Collect all findings from all engines.
2. Deduplicate by the same location and the same vulnerability type.
3. Sort the unified set by severity.
4. Boost confidence for findings detected by multiple engines.
5. Keep single-engine findings as lower-confidence candidates instead of dropping them silently.
