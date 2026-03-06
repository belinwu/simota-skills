# AI-Generated Code Security & Modern SAST

Purpose: Use this reference when the target code was AI-generated, AI-assisted, or depends on AI-native tooling that changes the threat model.

## Contents

- risk snapshot
- AI-specific anti-patterns
- review checklist
- SAST landscape
- hybrid LLM-SAST
- IDE and policy risks

## Risk Snapshot (2025-2026)

| Metric | Value |
|--------|-------|
| Vulnerable AI-generated code | `45-62%` |
| XSS failure rate | `86%` |
| Vulnerable Java AI-generated code | `72%` |
| XSS rate: AI code vs human code | `2.74x` |
| Organizations that deployed vulnerable AI-generated code | `81%` |
| Breaches linked to AI-generated code | `1 in 5` |
| High-risk vulnerability growth | `8.3% -> 11.3%` |
| AI share of production code | `24%` (`29%` in the US) |

Why AI misses security:

1. weak application-specific threat modeling
2. missing internal policy context
3. insecure training data
4. blind spots in auth and authorization logic
5. syntactic correctness is not the same as security correctness

## Top 10 AI-Specific Anti-Patterns

| Rank | Pattern | Score | Detection |
|------|---------|-------|-----------|
| 1 | `Slopsquatting` | `24` | registry lookup |
| 2 | XSS | `23` | output escaping review |
| 3 | Hardcoded secrets | `23` | regex and entropy |
| 4 | SQL injection | `22` | missing parameterization |
| 5 | Authentication failures | `22` | broken auth flow |
| 6 | Missing input validation | `21` | no boundary validation |
| 7 | Command injection | `21` | unsafe shell execution |
| 8 | Missing rate limiting | `20` | sensitive endpoints unprotected |
| 9 | Excessive data exposure | `20` | API over-returning |
| 10 | Unrestricted file upload | `20` | no type/size limits |

Language tendencies:

- `Java`: highest failure rate, especially XSS and log injection
- `Python`: shell injection and unsafe deserialization
- `JS/TS`: XSS, prototype pollution, `eval()` patterns
- `Go`: error-handling gaps and race-adjacent logic issues

## Review Checklist

### Critical

- no hardcoded secrets
- parameterized SQL and NoSQL
- escaped output
- no direct user input in shell execution
- authz checks present

### High

- boundary validation present
- no sensitive data in errors
- upload type and size limits
- minimal API responses
- rate limiting on exposed endpoints

### Medium

- packages exist and are maintained
- licenses are compatible
- deprecated APIs removed
- logs do not contain secrets

AI-specific scan extensions:

1. detect non-existent package recommendations
2. flag unsafe but common AI patterns such as `eval()`, `exec()`, `Function()`, `innerHTML`, and string-built SQL
3. validate auth-flow completeness
4. review error-handling consistency

## Modern SAST Landscape

| Tool | Strength | AI support |
|------|----------|------------|
| `Semgrep` | rule-based, fast, broad language support | AI filtering |
| `CodeQL` | semantic GitHub-native queries | custom queries |
| `Snyk Code` | IDE-native feedback | AI autofix |
| `Veracode` | enterprise reporting | AI code risk views |
| `Checkmarx` | platform integration | AI-assisted remediation |
| `SonarQube` | quality gate plus taint analysis | mixed quality + security |
| `DryRun Security` | PR-native, natural-language policy | MCP integration |
| `Endor Labs` | reachability and noise reduction | policy-driven |
| `Aikido` | developer-first triage | automated triage |
| `Mend SAST` | editor integration | MCP server |

## Hybrid LLM-SAST

Accuracy comparison:

| Approach | Accuracy |
|----------|----------|
| Rules only | `35.7%` |
| LLM only | `65.5%` |
| `LLM + SAST` | `89.5%` |

IRIS-style flow:

1. run `CodeQL` / `Semgrep`
2. collect context such as data flow and call sites
3. let an LLM classify TP vs FP
4. use the merged result for prioritization and repair guidance

Key insight:

- rules provide breadth and repeatability
- LLMs provide contextual reasoning
- the hybrid approach is better than either alone

## IDE And Policy Risks

IDE threat notes:

- `30+` IDE security issues were publicly discussed in 2025
- common failure modes: prompt injection, data exfiltration, and RCE through trusted features

Minimum controls:

- minimize extensions
- sandbox AI agents
- require human review before execution
- patch IDEs quickly

Policy rules:

1. define policies in natural language, not regex only
2. enforce them on PRs
3. include remediation examples
4. allow cross-file authorization and IDOR checks
5. centralize policy visibility

## Sentinel Integration

| Phase | Use AI-security detail for... |
|-------|-------------------------------|
| `SCAN` | unsafe AI patterns, non-existent packages, auth-flow gaps |
| `FILTER` | LLM-assisted false-positive review |
| `PRIORITIZE` | confidence boost from hybrid evidence |
| `SECURE` | safer autofix suggestions and defensive alternatives |
| `VERIFY` | confirm the fix did not introduce new insecure AI patterns |
