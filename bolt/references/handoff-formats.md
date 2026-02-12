# Handoff Formats & Templates

## Handoff Patterns (ASCII Flow)

```
Bolt identifies DB bottleneck
  └─→ Tuner: EXPLAIN analysis & index design

Tuner finds N+1 in application
  └─→ Bolt: Eager loading / DataLoader implementation

Bolt finds deprecated heavy library
  └─→ Horizon: Modern replacement PoC

Bolt optimizes bundle
  └─→ Gear: Build configuration updates
```

---

## Agent Handoff Templates

**To Radar (Test Request):**
```markdown
@Radar - Performance test needed for optimized code

Optimized: [component/function name]
Change: [what was changed]
Expected: [performance improvement]
Test type: [benchmark/regression/stress]
```

**To Canvas (Diagram Request):**
```markdown
@Canvas - Performance visualization needed

Type: [flowchart/sequence/comparison]
Subject: [cache flow/query optimization/render cycle]
Key points: [what to highlight]
```

**To Growth (Core Web Vitals):**
```markdown
@Growth - Performance optimization may affect web vitals

Changes: [bundle size/render time/layout shift]
Impact: [LCP/INP/CLS affected]
Measurement needed: [Lighthouse/field data]
```

---

## Nexus Hub Mode NEXUS_HANDOFF Template

When user input contains `## NEXUS_ROUTING`, treat Nexus as hub.
- Do not instruct other agent calls
- Always return results to Nexus (append `## NEXUS_HANDOFF` at output end)

```text
## NEXUS_HANDOFF
- Step: [X/Y]
- Agent: [AgentName]
- Summary: 1-3 lines
- Key findings / decisions:
  - ...
- Artifacts (files/commands/links):
  - ...
- Risks / trade-offs:
  - ...
- Open questions (blocking/non-blocking):
  - ...
- Pending Confirmations:
  - Trigger: [INTERACTION_TRIGGER name if any, e.g., ON_PERF_TRADEOFF]
  - Question: [Question for user]
  - Options: [Available options]
  - Recommended: [Recommended option]
- User Confirmations:
  - Q: [Previous question] → A: [User's answer]
- Suggested next agent: [AgentName] (reason)
- Next action: CONTINUE (Nexus automatically proceeds)
```
