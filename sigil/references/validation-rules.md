# Validation Rules

Quality scoring rubric, validation checklist, common failure patterns, and report templates for generated skills.

---

## Format Validation Rules

### Frontmatter Validation

| Rule | Check | Severity |
|------|-------|----------|
| YAML block present | File starts with `---` | FAIL |
| `name` field | Non-empty, kebab-case, 2-4 words | FAIL |
| `description` field | Non-empty, single sentence, Japanese | FAIL |
| No extra fields | Only `name` and `description` | WARN |

### Section Structure Validation

| Section | Micro | Full | Check |
|---------|-------|------|-------|
| H1 title | ✅ Required | ✅ Required | Single `#` heading matches skill name |
| Purpose/目的 | ✅ Required | ✅ Required | Explains when/why to use |
| Steps/手順 or Workflow | ✅ Required | ✅ Required | Numbered steps or phase headings |
| Template/テンプレート | Optional | ✅ Required | Code blocks with language tags |
| Conventions/規約 | ✅ Required | Optional | Project-specific rules list |
| Error handling | Optional | ✅ Required | Error patterns and recovery |
| Testing section | Optional | ✅ Required | Test conventions and examples |
| Checklist | Optional | ✅ Required | Actionable checklist items |

### Code Block Validation

- All code blocks MUST have language tags (```tsx, ```python, etc.)
- Template placeholders use `[BracketNotation]` (not `{curly}` to avoid YAML conflicts)
- No hardcoded paths specific to a single developer's machine
- No secrets, tokens, or credentials in examples

---

## Content Validation Rules

### Convention Conformity

| Check | Method | Threshold |
|-------|--------|-----------|
| Naming matches project | Compare against 3+ existing files | 100% match |
| Import style matches | Check alias paths, barrel exports | Consistent |
| File structure matches | Compare directory patterns | Consistent |
| Error handling matches | Check try-catch, Result types, etc. | Consistent |
| Test location matches | Co-located vs separated | Consistent |

### Actionability Checks

- Every step MUST be executable (no "configure as needed")
- Template code MUST be syntactically valid
- File paths MUST use project's actual directory structure
- Commands MUST be runnable in project context

### Completeness Rules

**Micro Skill minimum:**
- Purpose section: 1-2 sentences minimum
- Steps: 3+ numbered steps
- At least one of: Template OR Conventions

**Full Skill minimum:**
- Purpose section: 3+ sentences with prerequisites
- Workflow: 3+ phases with substeps
- Templates: 2+ patterns/variations
- Error handling section with specific patterns
- Testing section with framework-specific examples
- Checklist: 3+ actionable items

---

## Quality Scoring Rubric (12-Point Scale)

### Dimension 1: Format (0-3)

| Score | Criteria |
|-------|----------|
| 0 | Missing frontmatter or H1 title |
| 1 | Frontmatter present but sections incomplete |
| 2 | All required sections present, properly structured |
| 3 | Perfect structure with consistent formatting, lang tags on all code blocks |

### Dimension 2: Relevance (0-3)

| Score | Criteria |
|-------|----------|
| 0 | Wrong framework or technology |
| 1 | Correct framework but generic patterns (not project-specific) |
| 2 | Matches project conventions (naming, imports, structure) |
| 3 | Uses exact patterns extracted from project's existing code |

### Dimension 3: Completeness (0-3)

| Score | Criteria |
|-------|----------|
| 0 | Missing critical steps or sections |
| 1 | Main flow covered but gaps in edge cases |
| 2 | All steps covered including common variations |
| 3 | Edge cases, error paths, and rollback procedures included |

### Dimension 4: Actionability (0-3)

| Score | Criteria |
|-------|----------|
| 0 | Vague or abstract instructions ("configure appropriately") |
| 1 | Some steps are executable, others need interpretation |
| 2 | All steps are clear and executable |
| 3 | Copy-paste ready templates with working examples |

### Score Interpretation

| Total | Grade | Action |
|-------|-------|--------|
| 10-12 | Excellent | Install immediately |
| 9 | Pass | Install (minimum threshold) |
| 6-8 | Review | Trigger ON_QUALITY_BELOW_THRESHOLD, attempt recraft |
| 3-5 | Fail | Mandatory recraft, investigate root cause |
| 0-2 | Critical | Abort, review SCAN phase data |

---

## Common Failure Patterns

### F1: Generic Template Syndrome
- **Symptom**: Template uses React defaults when project uses Vue
- **Cause**: SCAN phase skipped or incomplete
- **Fix**: Re-run SCAN, verify framework detection

### F2: Convention Mismatch
- **Symptom**: Skill uses camelCase when project uses kebab-case
- **Cause**: Insufficient existing file analysis during DISCOVER
- **Fix**: Read 3+ existing files of same type, extract patterns

### F3: Phantom Dependency
- **Symptom**: Template references library not in project's dependencies
- **Cause**: Using catalog defaults instead of project actuals
- **Fix**: Cross-reference template imports against package.json/go.mod

### F4: Incomplete Workflow
- **Symptom**: Steps stop before the task is actually done (missing test step)
- **Cause**: Insufficient domain understanding
- **Fix**: Trace complete developer workflow for this task type

### F5: Stale Skill
- **Symptom**: Skill references deprecated API or outdated patterns
- **Cause**: Project evolved since skill was generated
- **Fix**: Trigger evolution workflow (SCAN → DIFF → PLAN → UPDATE → VERIFY)

### F6: Ecosystem Overlap
- **Symptom**: Generated skill duplicates ecosystem agent functionality
- **Cause**: Insufficient deduplication check during DISCOVER
- **Fix**: Verify skill scope doesn't overlap with any of the 56+ ecosystem agents

---

## Validation Report Template

```markdown
## Skill Validation Report

### Summary
- **Skills validated**: [count]
- **Passed (9+)**: [count]
- **Review needed (6-8)**: [count]
- **Failed (<6)**: [count]

### Per-Skill Scores

| Skill | Format | Relevance | Completeness | Actionability | Total | Result |
|-------|--------|-----------|-------------|---------------|-------|--------|
| [name] | [0-3] | [0-3] | [0-3] | [0-3] | [0-12] | PASS/REVIEW/FAIL |

### Issues Found
- [Skill name]: [Issue description] → [Recommended fix]

### Sync Status
- `.claude/skills/`: [count] files
- `.agents/skills/`: [count] files
- Sync: IN_SYNC | DRIFT_REPAIRED | PARTIAL_FAIL
```
