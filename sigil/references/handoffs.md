# Handoff Templates

Standardized handoff formats for Sigil agent collaboration.

---

## Inbound Handoffs (→ Sigil)

### LENS_TO_SIGIL_HANDOFF

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Lens → Sigil
- **Summary**: Codebase analysis results for skill generation

### Analysis Results
- **Tech stack**: [Framework, language, key libraries]
- **Architecture**: [Monolith/Microservice, patterns used]
- **Conventions**: [Naming, file structure, testing patterns]
- **Key directories**: [src/, app/, lib/ structure]

### Discovered Patterns
- **Component pattern**: [How components are structured]
- **Data fetching**: [How data is fetched and cached]
- **State management**: [How state is managed]
- **Error handling**: [Error handling approach]

### Skill Opportunities
- [Opportunity 1: description]
- [Opportunity 2: description]
- [Opportunity 3: description]

### Sigil Actions Required
- [ ] Generate skills based on discovered patterns
- [ ] Validate against existing skills
- [ ] Install to project .claude/skills/
```

### ARCHITECT_TO_SIGIL_HANDOFF

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Architect → Sigil
- **Summary**: Ecosystem patterns for project-specific skill adaptation

### Ecosystem Patterns
- **Agent pattern**: [Pattern that could become a project skill]
- **Workflow template**: [Reusable workflow to adapt]
- **Convention set**: [Standard conventions to customize]

### Adaptation Guidelines
- **Target project**: [Project name/path]
- **Customization needs**: [What to adapt for this project]
- **Constraints**: [Project-specific limitations]

### Sigil Actions Required
- [ ] Adapt ecosystem patterns to project context
- [ ] Generate project-specific skills
- [ ] Validate fit with project conventions
```

---

## Outbound Handoffs (Sigil →)

### SIGIL_TO_GROVE_HANDOFF

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Sigil → Grove
- **Summary**: Generated skill structure for directory optimization

### Generated Skills
| Skill | Type | Path | Lines |
|-------|------|------|-------|
| [name] | Micro/Full | .claude/skills/[name].md | [N] |

### Directory Structure
- **Skills directory**: [.claude/skills/ layout]
- **References**: [Any references/ subdirectories created]
- **Total files**: [N files generated]

### Grove Actions Required
- [ ] Review skill directory organization
- [ ] Suggest structural improvements if needed
- [ ] Validate against project directory conventions
```

### SIGIL_TO_NEXUS_HANDOFF

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Sigil → Nexus
- **Summary**: New skills generated and installed

### Generated Skills
| Skill | Type | Description |
|-------|------|-------------|
| [name] | Micro/Full | [description] |

### Installation Status
- **Installed to**: [project path]/.claude/skills/
- **Files created**: [N]
- **Validation**: PASS/FAIL

### Artifacts
- [List of generated files]

### Risks
- [Any risks or limitations]

### Suggested Next Agent
- [Agent name if further action needed, or "none"]
```
