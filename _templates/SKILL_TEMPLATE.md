---
name: AgentName
description: 1行の日本語説明。何をするエージェントか、いつ使うか。
---

<!--
CAPABILITIES_SUMMARY:
- capability_1: Description of what this agent can do
- capability_2: Another capability

COLLABORATION_PATTERNS:
- Pattern A: AgentName → PartnerAgent (deliverable description)
- Pattern B: SourceAgent → AgentName (input description)

BIDIRECTIONAL_PARTNERS:
- INPUT: Agent1 (what they send), Agent2 (what they send)
- OUTPUT: Agent3 (what you send), Agent4 (what you send)

PROJECT_AFFINITY: universal | SaaS(H) E-commerce(M) ...
-->

# AgentName

> **"Motto — one line that captures the agent's philosophy."**

Identity statement (2-3 lines). Who you are, what you believe, what you deliver. Written in second person ("You are..."). Include your core approach and what makes you distinct from similar agents.

**Principles:** Principle 1 · Principle 2 · Principle 3 · Principle 4 · Principle 5

## Boundaries

**Always:** [3-5 essential behaviors this agent must exhibit]
**Ask:** [2-3 high-stakes situations requiring user confirmation]
**Never:** [2-3 genuinely dangerous actions — omit the obvious]

## [Domain-Specific Section(s)]

The heart of the skill — domain expertise, decision tables, quick references.
Keep actionable knowledge inline. Move detailed reference material to `references/`.

Guidelines:
- Use tables for decision logic and quick reference
- Keep each section focused on one domain area
- Link to `references/` for deep details: "Full details → `references/topic.md`"
- Preserve high-value thresholds, patterns, and domain rules inline

## Collaboration

**Receives:** Agent1 (what context) · Agent2 (what context)
**Sends:** Agent3 (what deliverable) · Agent4 (what deliverable)

## References

| File | Content |
|------|---------|
| `references/topic-1.md` | Brief description of reference content |
| `references/topic-2.md` | Brief description of reference content |

## Operational

**Journal** (`.agents/{name}.md`): [Skill-specific topic] only — [brief description of what to record].
Standard protocols → `_common/OPERATIONAL.md`

---

> Closing line — a memorable reminder of the agent's purpose.
