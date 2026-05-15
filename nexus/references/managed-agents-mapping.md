# Managed Agents — Pattern Mapping

Anthropic's **Claude Managed Agents** (announced Code w/ Claude SF 2026) bundles four features that map closely to existing Nexus patterns. Use this reference to align local routing with the official vocabulary, and to surface upgrade paths when a chain would benefit from the managed-platform equivalent.

[Source: Anthropic — *Code with Claude SF 2026* and *New in Claude: Managed Agents* (2026)](https://claude.com/blog/new-in-claude-managed-agents)

---

## 1. The Four Features

| Managed Agents feature | What it is | Nexus equivalent | Where in Nexus |
|--------------------------|-----------|-----------------|----------------|
| **Multiagent Orchestration** | Lead agent decomposes the job and delegates each piece to a specialist; specialists can have different models, prompts, and tools; they coordinate over a shared filesystem. | Hub-and-spoke routing with `_AGENT_CONTEXT` / `_STEP_COMPLETE`; Recipe-driven chains; Rally for parallel branches. | `Core Contract`, `Recipes`, `references/orchestration-patterns.md`, `_common/PARALLEL.md` |
| **Outcomes** | Rubric-based automatic output evaluation and iterative improvement. Each spec defines what "done" looks like; the platform scores against it and loops until the rubric passes. | Evaluator-Loop pattern; Sprint Contract; Rubric System; Judge as quality gate. | `references/evaluator-loop.md`, `references/sprint-contract.md`, `references/rubric-system.md` |
| **Dreaming** | Off-line analysis of past sessions to curate memories and propagate distilled knowledge across future runs. | Lore — cross-agent pattern extraction, METAPATTERNS.md curation, freshness scoring, organizational unlearning. | Delegate to Lore; see `lore/SKILL.md` |
| **Webhooks** | Completion / state-change notifications to external systems (CI, Slack, dashboards). | PushNotification + Mend handoffs; Beacon for production alerting; explicit `_STEP_COMPLETE` schema. | `references/output-formats.md`, route via Mend/Beacon |

## 2. Selection Rules

Use the Nexus-local equivalent (default) when:
- The work runs inside a single Claude Code or Codex CLI session.
- All specialists are local skill agents under `~/.claude/skills/`.
- Coordination overhead is contained within a single user session.

Recommend escalating to the **managed platform** (and surface the recommendation in `NEXUS_COMPLETE`) when:
- The chain runs unattended over hours or days (Webhooks > local polling).
- A team-wide knowledge base must persist across many users' sessions (Dreaming > per-user Lore).
- The Outcome rubric must be enforced across many concurrent invocations with platform-level audit (Managed Outcomes > Evaluator-Loop in-session).
- The customer needs Anthropic Console audit trails for compliance (every step durably logged with the agent's identity, order, and reasoning).

Otherwise stay on the local hub-and-spoke chain. Adopting the managed platform for short-lived single-user tasks pays only coordination cost without unlocking its differentiators.

## 3. Anti-Pattern: Reinventing the Feature

When a request describes one of the four features in disguise, prefer the official feature in vocabulary even if implemented locally:

- "Score my output against criteria and rerun until it passes" → call this **Outcomes / Evaluator Loop**, not "validation chain".
- "Remember what worked across past projects" → call this **Dreaming**, route to Lore.
- "Tell my dashboard when it's done" → call this **Webhooks**, route to Mend / PushNotification.
- "Split this between specialists" → call this **Multiagent Orchestration**, route as a Nexus chain.

Shared vocabulary with the platform reduces translation cost when chains later migrate to managed agents.

## 4. Cited Deployment Patterns

Public reference deployments documented by Anthropic at SF 2026:
- **Harvey** (legal document drafting): completion rate ≈6× higher under Multiagent Orchestration vs single-agent baseline.
- **Netflix**: log-analysis lead agent fans out across multiple log sources in parallel; aggregates findings.
- **Spiral**: combines Multiagent Orchestration with Outcomes to enforce editorial-quality bars on generated long-form writing.
- **Wisedocs**: document verification 50% faster after migrating to managed agents with shared filesystem coordination.

Use these as evidence when proposing local chain patterns of the same shape (e.g., "we are using the Netflix pattern: lead agent fans out across N independent investigators").

---

## When to Read This File

- During `CLASSIFY` when the user explicitly mentions Managed Agents, Outcomes, Dreaming, or Webhooks.
- During `CHAIN_SELECT` when a request describes a managed-agents feature in plain English.
- During `DELIVER` to surface an escalation recommendation in `NEXUS_COMPLETE` if the local hub-and-spoke is not the right long-term home for the workload.
