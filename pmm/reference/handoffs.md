# Handoff Formats Reference

**Purpose:** Inbound and outbound handoff templates for PMM.
**Read when:** You are receiving work from or routing work to a partner agent.

Canonical Nexus schema → `_common/HANDOFF.md`. These are PMM's domain-specific payloads.

## Contents
- Inbound
- Outbound
- Routing Rules

---

## Inbound

### NEXUS_TO_PMM_HANDOFF
```yaml
NEXUS_TO_PMM_HANDOFF:
  goal: "[position / message / gtm / launch / enable question]"
  scope: "[product, feature, segment, or 'whole product']"
  recipe_hint: "[position | message | gtm | launch | enable | ask]"
  known_inputs: "[any product-truth / persona / competitive data already on hand]"
```

### PDM_TO_PMM_HANDOFF
```yaml
PDM_TO_PMM_HANDOFF:
  shipped_features:
    - feature: "[feature]"
      status: "[Done | In-Progress]"
      evidence: ["file:line"]
      confidence: "[High | Medium | Low]"
  not_shipped: ["[roadmap items — exclude from messaging]"]
  reason: "Product truth for grounding the message."
```

### COMPETE_TO_PMM_HANDOFF
```yaml
COMPETE_TO_PMM_HANDOFF:
  alternatives:
    - name: "[competitor / substitute]"
      claims: "[what they position on]"
      gaps: "[where they fall short]"
  differentiation_axes: ["[axis the segment values]"]
  positioning_map: "[axes + plotted points, if available]"
```

### CAST_TO_PMM_HANDOFF
```yaml
CAST_TO_PMM_HANDOFF:
  personas:
    - name: "[persona / ICP]"
      jtbd: "[job-to-be-done]"
      pains: ["..."]
      gains: ["..."]
      language: ["[their own words]"]
```

---

## Outbound

### PMM_TO_SAGA_HANDOFF
```yaml
PMM_TO_SAGA_HANDOFF:
  messaging_spine:
    core_narrative: "[the promise]"
    pillars: ["[value pillar + proof]"]
    segment: "[target]"
  reason: "Messaging strategy set; narrative craft is Saga's domain."
```

### PMM_TO_FUNNEL_HANDOFF
```yaml
PMM_TO_FUNNEL_HANDOFF:
  positioning: "[statement]"
  headline_value: "[outcome headline]"
  proof_points: ["[capability + evidence]"]
  segment: "[target ICP]"
  reason: "Positioning/message ready; landing-page construction is Funnel's domain."
```

### PMM_TO_PROSE_HANDOFF
```yaml
PMM_TO_PROSE_HANDOFF:
  approved_message:
    headline: "[value headline]"
    body_points: ["[grounded claim]"]
  voice_tone: "[from Cast/brand, if known]"
  reason: "Message approved; production microcopy is Prose's domain."
```

### PMM_TO_LAUNCH_HANDOFF
```yaml
PMM_TO_LAUNCH_HANDOFF:
  launch:
    feature: "[feature]"
    marketing_tier: "[Tier 1 | 2 | 3]"
    target_date: "[T]"
    market_dependencies: "[assets that must be ready]"
  reason: "Marketing launch planned; technical release (versioning/rollout/rollback) is Launch's domain."
```

---

## Routing Rules

| Outbound trigger | Route to | Never do instead |
|------------------|----------|------------------|
| Message needs a finished story | Saga | Write the narrative yourself |
| Positioning needs a landing page | Funnel / Bazaar | Build the page yourself |
| Message needs production copy | Prose | Ship polished copy as final yourself |
| Need a competitive battle card | Compete | Author the battle card yourself |
| Launch needs the technical release | Launch | Plan versioning/rollout yourself |
| Launch items need priority order | Rank | Score them yourself |
| Need KPIs / metric dashboard | Pulse | Define KPIs yourself |
| Pitch needs slides | Stage | Design slides yourself |
| Positioning map needs rendering | Canvas | Hand-draw beyond simple ASCII |
| Need "what's actually built" | PDM | Assume capability |

Offer outbound handoffs as suggestions in the report; execute them only under Nexus AUTORUN or explicit user request.
