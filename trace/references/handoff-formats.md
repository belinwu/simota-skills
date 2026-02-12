# Handoff Templates

Standard handoff formats for Trace → other agents.

---

## TRACE_TO_RESEARCHER_HANDOFF

```markdown
## RESEARCHER_HANDOFF (from Trace)

### Persona Validation Findings
- **Analysis Period:** [Date range]
- **Sessions Analyzed:** [Count]

### Validation Results

| Persona | Expected Behavior | Actual Behavior | Match % | Recommendation |
|---------|-------------------|-----------------|---------|----------------|
| [Name] | [Expected] | [Actual] | [%] | [Action] |

### Suggested Persona Updates
1. **[Persona]**: [Suggested change with evidence]

### Evidence Sessions
- Session #[ID]: [Anonymized description]

Suggested command: `/Researcher update personas based on Trace findings`
```

---

## TRACE_TO_ECHO_HANDOFF

```markdown
## ECHO_HANDOFF (from Trace)

### Discovered Problem
- **Location:** [Page/Flow]
- **Frustration Score:** [Score]
- **Affected Personas:** [List]

### Evidence
- Rage clicks: [%]
- Back loops: [%]
- Abandonment: [%]
- Sessions analyzed: [Count]

### Simulation Request
- **Persona to simulate:** [Name]
- **Focus area:** [Specific element/flow]
- **Hypothesis:** [What we think is wrong]

Suggested command: `/Echo simulate [flow] as [persona] focusing on [area]`
```

---

## TRACE_TO_PALETTE_HANDOFF

```markdown
## PALETTE_HANDOFF (from Trace)

### UX Problem Identified
- **Location:** [Page/Element]
- **Severity:** [🔴/🟡/🟢]
- **Affected Users:** [% of sessions]

### Evidence
- **Frustration signals:** [List with data]
- **User journey disruption:** [Description]
- **Persona impact:** [Which personas most affected]

### Recommended Fix
- **Issue:** [Description]
- **Hypothesis:** [Why this is happening]
- **Suggested improvement:** [Direction, not implementation]

Suggested command: `/Palette fix [element] based on Trace findings`
```
