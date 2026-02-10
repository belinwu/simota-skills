# Architect Handoff Formats

Standardized handoff templates for agent collaboration.

---

## Input Handoffs (→ Architect)

### NEXUS_TO_ARCHITECT_HANDOFF

When Nexus identifies an ecosystem gap requiring a new agent or improvement.

```yaml
NEXUS_TO_ARCHITECT_HANDOFF:
  Request_Type: new_agent | improve_agent | ecosystem_review
  Source_Agent: Nexus
  Priority: P0 | P1 | P2 | P3
  Context:
    gap_description: "[What capability is missing or insufficient]"
    trigger: "[What user request or routing failure revealed the gap]"
    affected_workflows: ["[Workflow 1]", "[Workflow 2]"]
  Existing_Agents:
    related: ["[Agent that partially covers this]"]
    insufficient_because: "[Why existing agents don't suffice]"
  Constraints:
    - "[Ecosystem constraint 1]"
    - "[Integration constraint 2]"
  Request: "[Specific deliverable expected from Architect]"
```

### ATLAS_TO_ARCHITECT_HANDOFF

When Atlas provides ecosystem analysis or dependency mapping for agent design.

```yaml
ATLAS_TO_ARCHITECT_HANDOFF:
  Request_Type: ecosystem_analysis | dependency_map | architecture_review
  Source_Agent: Atlas
  Context:
    analysis_scope: "[What was analyzed]"
    findings:
      dependencies: ["[Dependency 1]", "[Dependency 2]"]
      circular_refs: ["[Circular reference if any]"]
      god_classes: ["[Over-coupled agent if any]"]
    recommendations:
      - "[Recommendation 1]"
      - "[Recommendation 2]"
  Affected_Agents: ["[Agent 1]", "[Agent 2]"]
  Request: "[Design action needed from Architect]"
```

### JUDGE_TO_ARCHITECT_FEEDBACK

When Judge discovers quality issues in agent SKILL.md files during code review.

```yaml
JUDGE_TO_ARCHITECT_FEEDBACK:
  Feedback_Type: structural_issue | content_gap | integration_broken | naming_violation | pattern_inconsistency
  Source_Agent: Judge
  Priority: high | medium | low
  Issue:
    agent_name: "[Agent whose SKILL.md has issues]"
    files:
      - file: "[File path]"
        line: [line number]
        description: "[What issue was found]"
    pattern: "[Recurring pattern if detected across multiple agents]"
  Suggested_Action:
    action: "add_section | fix_template | update_handoff | restructure"
    detail: "[Specific fix recommendation]"
  Scope:
    agents_affected: [count]
    files_affected: [count]
```

---

## Output Handoffs (Architect →)

### ARCHITECT_TO_NEXUS_HANDOFF

Notify Nexus of new agent availability or routing updates needed.

```yaml
ARCHITECT_TO_NEXUS_HANDOFF:
  Notification_Type: new_agent | agent_updated | agent_deprecated | routing_change
  Agent:
    name: "[Agent name]"
    category: "[Category]"
    purpose: "[One-line purpose]"
    capabilities: ["[Capability 1]", "[Capability 2]"]
  Routing_Updates:
    add_routes:
      - trigger: "[User intent pattern]"
        route_to: "[Agent name]"
        priority: [1-10]
    modify_routes:
      - trigger: "[Existing pattern]"
        change: "[What to change]"
  Integration:
    input_partners: ["[Agent 1]", "[Agent 2]"]
    output_partners: ["[Agent 1]", "[Agent 2]"]
    collaboration_patterns:
      - name: "[Pattern name]"
        flow: "[Agent] → [Agent] → [Agent]"
  Files_Created:
    - path: "[SKILL.md path]"
      lines: [count]
    - path: "[references path]"
      count: [file count]
  Request: "Update routing matrix and agent catalog"
```

### ARCHITECT_TO_QUILL_HANDOFF

Request documentation updates after agent creation or improvement.

```markdown
## QUILL_HANDOFF (from Architect)

### Agent [Created | Updated]
- **Name:** [Agent name]
- **Category:** [Category]
- **Purpose:** [One-line purpose]
- **Value:** [World with vs without]

### Files [Generated | Modified]
- `[agent]/SKILL.md` ([X] lines)
- `[agent]/references/*.md` ([Y] files)

### Documentation Needed
- [ ] Update README.md agent catalog
- [ ] Add usage examples
- [ ] Update category table
- [ ] Update collaboration diagrams

Suggested command: `/Quill update documentation for [agent]`
```

### ARCHITECT_TO_CANVAS_HANDOFF

Request visualization of agent relationships or ecosystem diagrams.

```markdown
## CANVAS_HANDOFF (from Architect)

### Visualization Request
- **Type:** Agent relationship diagram
- **Agent:** [Agent name]
- **Category:** [Category]

### Relationships to Show
- INPUT from: [Agent list]
- OUTPUT to: [Agent list]
- Pattern: [Collaboration pattern]

### Diagram Specifications
- **Format:** Mermaid | ASCII | draw.io
- **Scope:** Single agent | Category | Full ecosystem
- **Include:** Handoff labels on edges

Suggested command: `/Canvas create agent relationship diagram for [agent]`
```

### ARCHITECT_TO_JUDGE_HANDOFF

Request quality review of generated or modified SKILL.md.

```yaml
ARCHITECT_TO_JUDGE_HANDOFF:
  Request_Type: skill_review | improvement_review
  Agent:
    name: "[Agent name]"
    action: "created | improved"
  Files_To_Review:
    - path: "[SKILL.md path]"
      focus: ["structure", "completeness", "consistency"]
    - path: "[reference file path]"
      focus: ["content quality", "actionability"]
  Review_Criteria:
    - "All standard sections present per skill-template.md"
    - "Boundaries well-defined (Always 4-8, Ask 2-5, Never 3-6)"
    - "INTERACTION_TRIGGERS with YAML templates"
    - "No overlap > 30% with existing agents"
    - "Handoff templates complete for all declared partners"
  Expected_Output:
    - "Pass/Fail verdict per criterion"
    - "Specific line-level feedback for issues"
    - "Overall quality grade"
  Request: "Review SKILL.md quality and report issues"
```

---

## Reverse Feedback Processing Workflow

When Architect receives feedback from downstream agents:

```
1. RECEIVE    → Parse feedback template, identify priority and source
2. VALIDATE   → Confirm the reported issue exists (read affected files)
3. ASSESS     → Determine scope (single agent vs ecosystem-wide pattern)
4. SCORE      → Calculate current Health Score for affected agent(s)
5. PROPOSE    → Generate Enhancement Proposal if score warrants action
6. ACT        → Implement fix or schedule for next review cycle
7. NOTIFY     → Inform source agent of resolution via handoff
```

### Priority Handling

| Priority | Response | Action |
|----------|----------|--------|
| **High** | Immediate | Fix in current session, notify source agent |
| **Medium** | Next cycle | Add to improvement queue, fix in next review |
| **Low** | Scheduled | Document for next ecosystem-wide review |

---

## Collaboration Patterns (Handoff Flows)

### Pattern A: Research-to-Design
```
Atlas (ecosystem analysis) → ATLAS_TO_ARCHITECT → Architect (design) → ARCHITECT_TO_QUILL → Quill (docs)
```

### Pattern B: Gap-to-Implementation
```
Nexus (gap signal) → NEXUS_TO_ARCHITECT → Architect (design) → ARCHITECT_TO_NEXUS → Nexus (routing update)
```

### Pattern C: Review-to-Improve
```
Judge (feedback) → JUDGE_TO_ARCHITECT_FEEDBACK → Architect (improve) → ARCHITECT_TO_JUDGE → Judge (re-review)
```

### Pattern D: Quality Feedback Loop
```
Judge (SKILL.md review) → JUDGE_TO_ARCHITECT_FEEDBACK → Architect (fix) → ARCHITECT_TO_NEXUS → Nexus (update)
```

### Pattern E: Enhancement Cycle
```
Architect (assess) → ARCHITECT_TO_JUDGE → Judge (review) → JUDGE_TO_ARCHITECT_FEEDBACK → Architect (improve)
```

### Pattern F: Full Ecosystem Review
```
Architect (batch assess) → ARCHITECT_TO_CANVAS → Canvas (dashboard) → ARCHITECT_TO_NEXUS → Nexus (bulk update)
```
