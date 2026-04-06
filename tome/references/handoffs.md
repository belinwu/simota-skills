# Handoff Templates

**Purpose:** Handoff templates between Tome and other agents.
**Read when:** Confirming inter-agent collaboration formats.

---

## Incoming Handoffs

### From User (Direct Request)

```yaml
USER_TO_TOME:
  target:
    type: "[commit | pr | branch | file_range]"
    ref: "[specific reference]"
  audience:
    level: "[beginner | intermediate | advanced]"
  output:
    format: "[learning_doc | glossary | decision_record | tutorial]"
  notes: "[additional requests or focus areas]"
```

### From Rewind (Git Investigation Results)

```yaml
REWIND_TO_TOME_HANDOFF:
  investigation:
    target: "[investigation subject]"
    commits: "[key commit list]"
    root_cause: "[root cause]"
    timeline: "[change timeline]"
  request:
    focus: "[documentation focus]"
    audience: "[target audience]"
    format: "[output format]"
```

### From Harvest (PR Information)

```yaml
HARVEST_TO_TOME_HANDOFF:
  pr_data:
    number: "[PR number]"
    title: "[PR title]"
    description: "[PR description]"
    files_changed: "[changed file list]"
    commits: "[commit list]"
    reviews: "[review comments]"
  request:
    focus: "[documentation focus]"
    audience: "[target audience]"
```

### From Lens (Codebase Investigation)

```yaml
LENS_TO_TOME_HANDOFF:
  investigation:
    scope: "[investigation scope]"
    findings: "[findings]"
    architecture: "[related architecture]"
    data_flow: "[data flow]"
  request:
    focus: "[explanation focus]"
    audience: "[target audience]"
```

### From Scout (Bug Investigation)

```yaml
SCOUT_TO_TOME_HANDOFF:
  investigation:
    bug: "[bug summary]"
    root_cause: "[root cause]"
    reproduction: "[reproduction steps]"
    fix_location: "[fix location]"
  request:
    focus: "[learning doc for bug fix]"
    audience: "[target audience]"
```

---

## Outgoing Handoffs

### To Quill (Inline Documentation)

```yaml
TOME_TO_QUILL_HANDOFF:
  source:
    learning_doc: "[path to generated learning document]"
    key_insights: "[key insights]"
  request:
    action: "[inline comments / JSDoc / README updates]"
    target_files: "[target file list]"
    priority_items:
      - "[most important annotation point 1]"
      - "[most important annotation point 2]"
```

### To Scribe (Specification Documents)

```yaml
TOME_TO_SCRIBE_HANDOFF:
  source:
    learning_doc: "[path to generated learning document]"
    decisions: "[recorded design decision list]"
  request:
    action: "[spec/design document promotion]"
    format: "[ADR | HLD | design doc]"
    spec_candidates:
      - item: "[item to promote to spec]"
        rationale: "[why it should become a spec]"
```

### To Canvas (Visualization)

```yaml
TOME_TO_CANVAS_HANDOFF:
  source:
    learning_doc: "[path to generated learning document]"
    flows: "[flows to visualize]"
  request:
    action: "[Mermaid/ASCII diagram generation]"
    diagram_types:
      - type: "[sequence | flowchart | state | class]"
        scope: "[diagram scope]"
        highlight: "[change portion highlight instructions]"
```

### To Lore (Knowledge Catalog)

```yaml
TOME_TO_LORE_HANDOFF:
  source:
    learning_doc: "[path to generated learning document]"
    patterns: "[extracted general patterns]"
  request:
    action: "[knowledge catalog registration]"
    insights:
      - pattern: "[pattern name]"
        description: "[pattern description]"
        applicability: "[applicability scope]"
```
