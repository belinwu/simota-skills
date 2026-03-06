# False Positive Management

Purpose: Reduce noise without hiding true positives. Use this reference for confidence scoring, delta scanning, framework-aware suppression, and SARIF output.

## Contents

- FP rate targets
- framework-aware suppression
- delta scanning
- confidence scoring
- LLM-assisted filtering
- SARIF output

## FP Rate Targets

Raw static-analysis alerts often contain about `53%` false positives. Without filtering, teams stop trusting the tool.

| FP rate | Assessment | Developer trust | Resolution rate |
|---------|------------|-----------------|-----------------|
| `> 40%` | Harmful | Very low | `< 20%` |
| `20-40%` | Needs work | Low | `30-50%` |
| `10-20%` | Target range | Medium to high | `60-80%` |
| `< 10%` | Excellent | High | `> 85%` |

Alert-fatigue loop:

```text
Too many FPs -> alerts ignored -> real issues missed
-> security incidents -> trust in the scanner collapses
```

## Framework-Aware Suppression

Built-in rules create noise when they cannot see project-specific protections such as:

- custom auth middleware like `requireAuth()` or `checkPermission()`
- application sanitizers
- framework-provided CSRF protection
- API gateway throttling

Custom suppression example:

```yaml
rules:
  - id: ignore-sanitized-input
    patterns:
      - pattern: $FUNC($INPUT)
      - pattern-not-inside: |
          if (sanitize($INPUT)) { ... }
    message: "Unsanitized input detected"
    severity: WARNING
```

Project memory examples:

```text
sanitizer_functions: [sanitizeHtml, escapeSQL, purifyInput]
auth_middleware: [requireAuth, requireRole, requireApiKey]
csrf_protection: "Next.js built-in CSRF protection"
rate_limiting: "Handled at API Gateway"
```

## Delta And Diff-Based Scanning

Use changed code first. This removes legacy noise while keeping periodic full coverage.

| Mode | Scope | Use when |
|------|-------|----------|
| PR-level | Changed files only | Fast review and merge gates |
| Periodic | Full repository | Weekly or explicit full audits |
| Baseline | Existing findings suppressed | New scanner rollout on legacy code |

Sentinel process integration:

```text
SCAN -> PRIORITIZE -> FILTER -> SECURE -> VERIFY -> PRESENT
```

## Confidence Scoring Model

| Factor | Weight | Example |
|--------|--------|---------|
| Multi-engine consensus | `+30%` | `3/3` engines flagged the same issue |
| Known pattern match | `+20%` | Exact AWS key regex match |
| Data-flow reachability | `+25%` | User input reaches a sink |
| Framework mismatch | `-20%` | The framework auto-sanitizes or auto-protects |
| Test or mock location | `-30%` | File is under `__tests__/` or fixtures |

Confidence tiers:

| Tier | Range | Action |
|------|-------|--------|
| `HIGH` | `>= 80%` | Include immediately in `PRESENT` |
| `MEDIUM` | `50-79%` | Report with a verification note |
| `LOW` | `< 50%` | Suppress by default unless exhaustive output is requested |

## LLM-Based FP Filtering

LLMs help where rules are weak:

- cross-function data-flow reasoning
- upstream validation recognition
- exploit-feasibility assessment
- framework security guarantee recognition

Accuracy comparison:

| Approach | Accuracy |
|----------|----------|
| Rules only (SAST) | `35.7%` |
| LLM only | `65.5%` |
| `LLM + SAST (Hybrid)` | `89.5%` |

Trade-off rule:

- Prioritize true-positive recall over aggressive suppression.
- Use confidence scoring to reduce noise instead of hiding uncertain findings completely.

## SARIF Output

Use SARIF when CI, GitHub Code Scanning, or IDE tooling needs machine-readable results.

```json
{
  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/main/sarif-2.1/schema/sarif-schema-2.1.0.json",
  "version": "2.1.0",
  "runs": [{
    "tool": { "driver": { "name": "Sentinel", "version": "1.0" } },
    "results": [{
      "ruleId": "SECRET-001",
      "level": "error",
      "message": { "text": "Hardcoded API key detected" },
      "locations": [{
        "physicalLocation": {
          "artifactLocation": { "uri": "src/config.ts" },
          "region": { "startLine": 42 }
        }
      }],
      "properties": {
        "confidence": 0.92,
        "engines": ["codex", "gemini", "claude"]
      }
    }]
  }]
}
```

Typical integrations:

- GitHub Code Scanning
- VS Code SARIF Viewer
- CI/CD policy gates
