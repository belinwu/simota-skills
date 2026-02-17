# Handoff Templates

Standardized handoff formats for Sigil agent collaboration (9 bidirectional patterns).

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
- [ ] Validate against existing skills (both .claude/skills/ and .agents/skills/)
- [ ] Sync-write to project .claude/skills/ and .agents/skills/
- [ ] Repair any sync drift (orphan skills in only one directory)
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

### JUDGE_TO_SIGIL_HANDOFF

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Judge → Sigil
- **Summary**: Quality review feedback on generated skills

### Review Results
| Skill | Score | Issues |
|-------|-------|--------|
| [name] | [N]/12 | [issue list] |

### Critical Issues
- [Skill name]: [Issue description, severity, recommended fix]

### Quality Patterns
- **Strengths**: [What Sigil is doing well]
- **Weaknesses**: [Recurring quality issues]
- **Recommendations**: [Specific improvement actions]

### Sigil Actions Required
- [ ] Address critical issues (score < 9/12)
- [ ] Recraft failed skills
- [ ] Apply quality pattern improvements to future generations
```

### CANON_TO_SIGIL_HANDOFF

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Canon → Sigil
- **Summary**: Standards compliance requirements for skill generation

### Applicable Standards
- **Standard**: [OWASP/WCAG/OpenAPI/etc.]
- **Relevant rules**: [Specific rules that apply to generated skills]
- **Compliance level**: [Required compliance level]

### Compliance Gaps
- [Gap 1: description and affected skill area]
- [Gap 2: description and affected skill area]

### Sigil Actions Required
- [ ] Incorporate standard requirements into relevant skills
- [ ] Add compliance checks to skill templates
- [ ] Validate existing skills against standards
```

### HONE_TO_SIGIL_HANDOFF

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Hone → Sigil
- **Summary**: Iterative improvement request for generated skills

### PDCA Cycle Context
- **Plan**: [Original quality target]
- **Do**: [What was attempted]
- **Check**: [Quality measurement results]
- **Act**: [Specific improvements needed]

### Improvement Targets
| Skill | Current Score | Target Score | Focus Areas |
|-------|-------------|-------------|-------------|
| [name] | [N]/12 | [N]/12 | [areas to improve] |

### Sigil Actions Required
- [ ] Recraft targeted skills with improvement focus
- [ ] Re-score quality after changes
- [ ] Report improvement delta to Hone
```

---

## Outbound Handoffs (Sigil →)

### SIGIL_TO_GROVE_HANDOFF

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Sigil → Grove
- **Summary**: Generated skill structure for directory optimization

### Generated Skills
| Skill | Type | Primary Path | Mirror Path | Lines |
|-------|------|-------------|-------------|-------|
| [name] | Micro/Full | .claude/skills/[name].md | .agents/skills/[name].md | [N] |

### Directory Structure
- **Primary skills directory**: [.claude/skills/ layout]
- **Mirror skills directory**: [.agents/skills/ layout]
- **References**: [Any references/ subdirectories created in both dirs]
- **Total files**: [N files generated (×2 for dual-write)]

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
- **Synced to**: [project path]/.claude/skills/ and .agents/skills/
- **Files created**: [N] (synced to both directories)
- **Sync status**: IN_SYNC / DRIFT_REPAIRED / PARTIAL_FAIL
- **Validation**: PASS/FAIL

### Artifacts
- [List of skill files (synced in both .claude/skills/ and .agents/skills/)]

### Risks
- [Any risks or limitations]

### Suggested Next Agent
- [Agent name if further action needed, or "none"]
```

### SIGIL_TO_JUDGE_HANDOFF

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Sigil → Judge
- **Summary**: Quality review request for generated skills

### Skills for Review
| Skill | Type | Lines | Self-Score | Path |
|-------|------|-------|-----------|------|
| [name] | Micro/Full | [N] | [N]/12 | .claude/skills/[name].md |

### Context
- **Project**: [project name/path]
- **Framework**: [detected framework]
- **Generation method**: [from SCAN or user request]

### Review Focus
- [ ] Format compliance (frontmatter, sections, code blocks)
- [ ] Convention conformity (matches project patterns)
- [ ] Actionability (steps are executable)
- [ ] Completeness (all required sections present)

### Judge Actions Required
- [ ] Score each skill on 12-point rubric
- [ ] Report critical issues
- [ ] Return JUDGE_TO_SIGIL_HANDOFF with results
```

### SIGIL_TO_HONE_HANDOFF

```markdown
## NEXUS_HANDOFF
- **Step**: [N] / **Agent**: Sigil → Hone
- **Summary**: Improvement results for verification

### Improvement Results
| Skill | Before | After | Changes Made |
|-------|--------|-------|-------------|
| [name] | [N]/12 | [N]/12 | [summary of changes] |

### Changes Applied
- [Skill name]: [Specific changes made]

### Hone Actions Required
- [ ] Verify improvement meets target
- [ ] Check for diminishing returns
- [ ] Decide: continue iteration or accept current quality
```
