# Official Design Patterns Reference

> Source: "The Complete Guide to Building Skills for Claude" (Anthropic, 2025)

Architect が ENVISION / DESIGN フェーズで参照する公式デザインパターンリファレンス。

---

## 1. 3つのユースケースカテゴリ

### Category 1: Document & Asset Creation

**Used for**: Creating consistent, high-quality output — documents, presentations, apps, designs, code

**Key Techniques**:
- Embedded style guides and brand standards
- Template structures for consistent output
- Quality checklists before finalizing
- No external tools required — uses Claude's built-in capabilities

**Real example**: `frontend-design` skill, Office skills (docx, pptx, xlsx, ppt)

### Category 2: Workflow Automation

**Used for**: Multi-step processes that benefit from consistent methodology, including multi-MCP coordination

**Key Techniques**:
- Step-by-step workflow with validation gates
- Templates for common structures
- Built-in review and improvement suggestions
- Iterative refinement loops

**Real example**: `skill-creator` skill

### Category 3: MCP Enhancement

**Used for**: Workflow guidance to enhance tool access an MCP server provides

**Key Techniques**:
- Coordinates multiple MCP calls in sequence
- Embeds domain expertise
- Provides context users would otherwise need to specify
- Error handling for common MCP issues

**Real example**: `sentry-code-review` skill (Sentry)

### Approach Selection: Problem-first vs Tool-first

| Approach | When | User Mindset |
|----------|------|-------------|
| **Problem-first** | "I need to set up a project workspace" | Describes outcomes; skill handles tools |
| **Tool-first** | "I have Notion MCP connected" | Has access; skill provides expertise |

> Most skills lean one direction. Knowing which framing fits the use case helps choose the right pattern.

---

## 2. 5つの公式パターン

### Pattern 1: Sequential Workflow Orchestration

**Use when**: Users need multi-step processes in a specific order.

```markdown
## Workflow: Onboard New Customer
### Step 1: Create Account
Call MCP tool: `create_customer`
Parameters: name, email, company
### Step 2: Setup Payment
Call MCP tool: `setup_payment_method`
Wait for: payment method verification
### Step 3: Create Subscription
Call MCP tool: `create_subscription`
Parameters: plan_id, customer_id (from Step 1)
### Step 4: Send Welcome Email
Call MCP tool: `send_email`
Template: welcome_email_template
```

**Key Techniques**: Explicit step ordering, dependencies between steps, validation at each stage, rollback instructions for failures

---

### Pattern 2: Multi-MCP Coordination

**Use when**: Workflows span multiple services.

**Example**: Design-to-development handoff

| Phase | Service | Actions |
|-------|---------|---------|
| 1. Design Export | Figma MCP | Export assets, generate specs, create manifest |
| 2. Asset Storage | Drive MCP | Create folder, upload assets, generate links |
| 3. Task Creation | Linear MCP | Create tasks, attach links, assign team |
| 4. Notification | Slack MCP | Post summary to #engineering with links and refs |

**Key Techniques**: Clear phase separation, data passing between MCPs, validation before next phase, centralized error handling

---

### Pattern 3: Iterative Refinement

**Use when**: Output quality improves with iteration.

```markdown
## Iterative Report Creation
### Initial Draft
1. Fetch data via MCP
2. Generate first draft report
3. Save to temporary file
### Quality Check
1. Run validation script: `scripts/check_report.py`
2. Identify issues (missing sections, formatting, data errors)
### Refinement Loop
1. Address each identified issue
2. Regenerate affected sections
3. Re-validate
4. Repeat until quality threshold met
### Finalization
1. Apply final formatting
2. Generate summary
3. Save final version
```

**Key Techniques**: Explicit quality criteria, iterative improvement, validation scripts, knowing when to stop

---

### Pattern 4: Context-Aware Tool Selection

**Use when**: Same outcome, different tools depending on context.

**Example**: Smart file storage with decision tree

| Condition | Tool |
|-----------|------|
| Large files (>10MB) | Cloud storage MCP |
| Collaborative docs | Notion/Docs MCP |
| Code files | GitHub MCP |
| Temporary files | Local storage |

**Key Techniques**: Clear decision criteria, fallback options, transparency about choices (explain to user why that tool was chosen)

---

### Pattern 5: Domain-Specific Intelligence

**Use when**: Skill adds specialized knowledge beyond tool access.

**Example**: Financial compliance in payment processing

```markdown
### Before Processing (Compliance Check)
1. Fetch transaction details via MCP
2. Apply compliance rules:
   - Check sanctions lists
   - Verify jurisdiction allowances
   - Assess risk level
3. Document compliance decision
### Processing
IF compliance passed → process transaction
ELSE → flag for review, create compliance case
### Audit Trail
- Log all compliance checks
- Record processing decisions
- Generate audit report
```

**Key Techniques**: Domain expertise embedded in logic, compliance before action, comprehensive documentation, clear governance

---

### Pattern Selection Guide

| Your Need | Primary Pattern | Secondary Pattern |
|-----------|----------------|-------------------|
| Ordered multi-step process | Sequential Workflow | — |
| Cross-service coordination | Multi-MCP Coordination | Sequential Workflow |
| Quality-sensitive output | Iterative Refinement | Sequential Workflow |
| Context-dependent routing | Context-Aware Tool Selection | Domain-Specific Intelligence |
| Regulatory/domain constraints | Domain-Specific Intelligence | Sequential Workflow |
| Complex workflow spanning services + quality | Multi-MCP Coordination | Iterative Refinement |

---

## 3. 計画方法論

### Use Case Definition Template

```
Use Case: [Name]
Trigger: [What user says or does]
Steps:
1. [Action with tool/MCP reference]
2. [Action]
3. [Action]
Result: [Expected outcome]
```

### Technical Requirements Checklist

1. **Tools inventory**: Built-in capabilities vs MCP requirements
2. **File structure**: `SKILL.md` + `scripts/` + `references/` + `assets/`
3. **Dependencies**: Environment requirements → `compatibility` field
4. **Folder naming**: kebab-case, matching `name` field

### Planning Questions

- What does a user want to accomplish?
- What multi-step workflows does this require?
- Which tools are needed (built-in or MCP)?
- What domain knowledge or best practices should be embedded?

---

## 4. 成功基準フレームワーク

### Quantitative Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Trigger accuracy | 90%+ on relevant queries | 10-20 test queries, track auto-load rate |
| Workflow efficiency | X tool calls (baseline comparison) | Same task with/without skill |
| API reliability | 0 failed calls per workflow | MCP server logs, retry rates |

### Qualitative Metrics

| Metric | Assessment |
|--------|-----------|
| Self-guided completion | Users don't need to prompt Claude about next steps |
| Correction-free execution | Same request 3-5 times yields consistent quality |
| First-try accessibility | New user accomplishes task with minimal guidance |

### Baseline Comparison Template

| Dimension | Without Skill | With Skill |
|-----------|--------------|------------|
| User instructions | Provided each time | Automatic |
| Back-and-forth | ~15 messages | ~2 clarifying questions |
| Failed API calls | ~3 requiring retry | 0 |
| Token consumption | ~12,000 | ~6,000 |

> Note: These are aspirational targets — rough benchmarks rather than precise thresholds. Anthropic is actively developing more robust measurement guidance and tooling.

---

## 5. Progressive Disclosure 設計原則

### Three-Level System

| Level | Content | Loading | Design Goal |
|-------|---------|---------|-------------|
| **1st** | YAML frontmatter | Always in system prompt | Minimal: just enough for Claude to know WHEN to use |
| **2nd** | SKILL.md body | When skill judged relevant | Full instructions, core workflow |
| **3rd** | `references/`, `scripts/`, `assets/` | On-demand navigation | Detailed docs, validation, templates |

### Application in Design

- **SKILL.md**: Keep under 5,000 words. Focus on core instructions.
- **references/**: Detailed API patterns, rate limiting, pagination, error codes
- **scripts/**: Deterministic validation (code > language instructions for critical checks)
- **assets/**: Templates, fonts, icons used in output

---

## 6. Composability 原則

### Portability

- Skills work identically across **Claude.ai**, **Claude Code**, and **API**
- Create once, works across all surfaces
- Note environment dependencies in `compatibility` field

### MCP Complementarity (Kitchen Analogy)

| | MCP | Skills |
|---|-----|--------|
| **Metaphor** | Professional kitchen | Recipes |
| **Provides** | Tool access, real-time data | Workflows, best practices |
| **Answers** | What Claude **can** do | How Claude **should** do it |

### Multi-Skill Coexistence

- Skills should work alongside others
- Don't assume exclusive capability
- Design for composition, not isolation

### Distribution Considerations

| Surface | Capability |
|---------|-----------|
| Claude.ai | Upload via Settings > Capabilities > Skills |
| Claude Code | Place in skills directory |
| API | `/v1/skills` endpoint, `container.skills` parameter |
| Organization | Admin workspace-wide deployment |
