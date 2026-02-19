# Handoff Protocol (Common Definition)

Standard format for `## NEXUS_HANDOFF` output. Designed for flexibility: include what's relevant, skip what's not.

---

## NEXUS_HANDOFF Format

### Required Fields (always include)

| Field | Description |
|-------|-------------|
| **Summary** | What was accomplished (1-3 sentences) |
| **Next** | Recommended next agent or action |

### Recommended Fields (include for complex tasks)

| Field | Description |
|-------|-------------|
| **Findings** | Key discoveries, root causes, analysis results |
| **Risks** | Identified risks, concerns, potential issues |
| **Open questions** | Unresolved items that need attention |

### Optional Fields (include when applicable)

| Field | Description |
|-------|-------------|
| **Step** | Step number in chain (e.g., 2/5) |
| **Agent** | Current agent name |
| **Artifacts** | Files created or modified |
| **Pending Confirmations** | Decisions awaiting user input |
| **User Confirmations** | Decisions already confirmed by user |
| **Suggested alternatives** | Alternative approaches considered |
| **Guardrail Events** | Safety events triggered during execution |

---

## Examples

### Minimal (simple task)

```
## NEXUS_HANDOFF
- Summary: Root cause identified — null check missing in `auth.ts:42`
- Next: Builder (implement fix)
```

### Standard (typical task)

```
## NEXUS_HANDOFF
- Step: 2/4
- Agent: Scout
- Summary: Investigated login failure. Root cause: token refresh race condition in `auth/refresh.ts:87`
- Findings: Two concurrent refresh calls invalidate each other's tokens
- Artifacts: Investigation notes in `.agents/scout.md`
- Risks: Fix may affect session handling in other flows
- Next: Builder (implement mutex-based refresh)
```

### Full (complex/high-risk task)

```
## NEXUS_HANDOFF
- Step: 3/7
- Agent: Sentinel
- Summary: Security audit complete. 2 critical, 1 medium vulnerability found
- Findings: SQL injection in search endpoint, XSS in comment rendering, weak CSRF token
- Artifacts: `reports/security-audit.md`
- Risks: SQL injection is exploitable in production
- Pending Confirmations: Deploy hotfix vs scheduled release?
- User Confirmations: "Prioritize security over feature work" (confirmed 2024-01-15)
- Open questions: Third-party dependency CVE-2024-XXXX — vendor patch ETA unknown
- Suggested alternatives: WAF rule as interim mitigation
- Guardrail Events: L3 triggered (critical security), auto-paused for review
- Next: Builder (implement fixes, priority: SQL injection first)
```

---

## Rules

1. **Always include Summary + Next** — these are the minimum for any handoff
2. **Add detail proportional to complexity** — simple tasks need minimal handoff
3. **Be specific in Next** — include what the next agent should do, not just who
4. **Findings should be actionable** — include file paths, line numbers, evidence
5. **Risks should be concrete** — "might break X" is better than "there are risks"
