# Handoff Formats

Standardized handoff templates for agent collaboration and Canvas integration.

## Input Handoff Names

| Handoff | Source Agent | Purpose |
|---------|-------------|---------|
| SCOUT_TO_RIPPLE | Scout | Bug fix impact analysis |
| ATLAS_TO_RIPPLE | Atlas | Architecture change impact |
| SPARK_TO_RIPPLE | Spark | Feature proposal impact |

## RIPPLE_TO_BUILDER

```markdown
## RIPPLE_TO_BUILDER_HANDOFF

### Change Summary
[What needs to be implemented]

### Impact Awareness
- **Direct Files:** [list]
- **Transitive Files:** [list]
- **Breaking Changes:** [warnings]

### Pattern Requirements
- **Must follow:** [pattern 1], [pattern 2]
- **Reference files:** [similar implementations]

### Test Requirements
- **Existing tests to update:** [list]
- **New tests needed:** [suggested test cases]

### Risk Mitigations
- [mitigation 1]
- [mitigation 2]
```

## RIPPLE_TO_GUARDIAN

```markdown
## RIPPLE_TO_GUARDIAN_HANDOFF

### Change Scope Analysis
- **Total files:** X
- **Logical groupings:** [grouping suggestions]
- **Dependencies between groups:** [graph]

### Recommended PR Strategy
- **Option A:** Single PR (if scope < 10 files)
- **Option B:** Stacked PRs (recommended for larger scope)

### Breaking Change Warnings
[List of breaking changes that affect PR messaging]

### Review Focus Areas
[What reviewers should pay attention to]
```

## RIPPLE_TO_ZEN

```markdown
## RIPPLE_TO_ZEN_HANDOFF

### Refactoring Scope
- **Target:** [file/module]
- **Current patterns:** [existing patterns]
- **Target patterns:** [desired patterns]

### Affected Areas
- **Files to modify:** [list with line estimates]
- **Tests to update:** [list]

### Pattern Constraints
- **Must maintain:** [patterns that cannot change]
- **Can update:** [patterns that can be improved]

### Risk Boundaries
- **Safe changes:** [low-risk refactoring]
- **Careful changes:** [higher-risk areas]
```

## Canvas Integration

### Dependency Impact Diagram

```markdown
## CANVAS_REQUEST

### Diagram Type: Dependency Impact Graph
### Purpose: Visualize change ripple effect

### Changed Module
- Name: [module name]
- Location: [file path]

### Impact Levels
- Level 0: [changed file]
- Level 1: [direct dependents]
- Level 2: [transitive dependents]

### Highlight
- Breaking changes in red
- High-risk areas in orange
- Test files in green
```

### Pattern Compliance Diagram

```markdown
## CANVAS_REQUEST

### Diagram Type: Pattern Compliance Matrix
### Purpose: Show pattern adherence across change scope

### Patterns Checked
- Pattern A: [name] - ✅/⚠️/❌
- Pattern B: [name] - ✅/⚠️/❌

### Files Analyzed
- [file 1]: [compliance status]
- [file 2]: [compliance status]
```
