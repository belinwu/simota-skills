# Subagent Parallel Protocol

Common protocol for individual skills to spawn parallel sub-agents via the **Task tool**.
For Nexus internal parallel branches → `_common/PARALLEL.md`. For full team orchestration (4+ workers) → Rally.

---

## Scope: Three Layers of Parallelism

| Layer | Orchestrator | Workers | Use When |
|-------|-------------|---------|----------|
| **Skill-internal** (this doc) | Individual skill agent | 2-3 Task subagents | Independent subtasks within a single skill's work |
| **Nexus parallel branches** | Nexus | Agent chains per branch | AUTORUN_FULL multi-branch execution |
| **Rally team** | Rally | Multiple Claude instances | 4+ parallel workers, complex coordination |

---

## Decision: When to Spawn Subagents

### USE subagents when:
- 2-3 **independent** subtasks exist (no data dependencies)
- Multiple **perspectives/engines** improve quality (Multi-Engine Mode)
- Parallel **verification** reduces wall-clock time (test + lint + type-check)
- Different **code areas** need simultaneous investigation

### DO NOT use subagents when:
- Tasks have **sequential dependencies** (B needs A's output)
- Working on a **single file** (subagents cannot share file ownership)
- Task completes in **< 30 seconds** (spawn overhead exceeds benefit)
- **4+ workers** needed → use Rally instead
- Task requires **shared mutable state** or iterative refinement

### Decision Flow

```
Task received
  ├─ Single focus, < 30s? ──────────────────→ Do it yourself
  ├─ 2-3 independent subtasks? ─────────────→ Spawn subagents (this protocol)
  ├─ 4+ independent subtasks? ──────────────→ Delegate to Rally
  └─ Sequential chain? ────────────────────→ Do it yourself (or Nexus AUTORUN)
```

---

## Task Tool Quick Reference

### subagent_type Selection

| Type | Tools Available | Best For |
|------|----------------|----------|
| `Explore` | Read-only (Glob, Grep, Read, WebFetch, WebSearch) | Research, codebase exploration, information gathering |
| `Plan` | Read-only | Architecture analysis, approach design |
| `general-purpose` | All (including Edit, Write, Bash) | Implementation, testing, any task requiring changes |

### model Selection

| Complexity | Model | Use When |
|-----------|-------|----------|
| Low | `haiku` | Simple searches, formatting, extraction |
| Medium | `sonnet` | Standard analysis, code review, moderate reasoning |
| High | (default/inherit) | Complex reasoning, architecture decisions |

### Parallel Launch

Spawn multiple subagents by issuing **multiple Task tool calls in a single message**. The system executes them concurrently.

```
# In one message, call Task 2-3 times:
Task(subagent_type="Explore", prompt="Research area A...")
Task(subagent_type="Explore", prompt="Research area B...")
Task(subagent_type="Explore", prompt="Research area C...")
```

---

## Patterns

### RESEARCH_FAN_OUT

Multiple Explore agents investigate different areas in parallel.

**When:** Broad investigation across distinct code areas, documentation, or domains.

**Setup:**
- 2-3 `Explore` subagents, each with a distinct search scope
- Each agent receives: Role + Target area + Output format
- No shared files or overlapping scope

**Merge:** Union — collect all findings → deduplicate → consolidate → report.

---

### MULTI_ENGINE

Three AI engines (Codex, Gemini, Claude) independently work on the same task, leveraging diverse knowledge bases.

**When:** Quality-critical tasks where diverse perspectives catch blind spots (security scans, bug hunts, edge-case tests, refactoring proposals).

#### Engine Dispatch Table

| Engine | Command | Fallback (when `which` fails) |
|--------|---------|-------------------------------|
| Codex | `codex exec --full-auto` | Claude subagent (Task) |
| Gemini | `gemini -p --yolo` | Claude subagent (Task) |
| Claude | Claude subagent (Task) | — |

#### Loose Prompt Rules

External engines (Codex, Gemini) must receive **minimal, unbiased prompts** to maximize independent perspective:

**Pass only:**
1. **Role** — one line describing the task persona
2. **Target** — code, files, or context to analyze
3. **Output format** — expected structure of results

**Do NOT pass:** domain frameworks, category lists, methodology descriptions, checklists, or detailed procedures. Let each engine apply its own knowledge.

#### Dispatch Examples

```bash
# Codex
codex exec --full-auto "$(cat /tmp/prompt.md)"

# Gemini
gemini -p "$(cat /tmp/prompt.md)" --yolo
```

```yaml
# Claude (Task tool)
Task:
  subagent_type: general-purpose
  mode: dontAsk
  description: "[task description]"
  prompt: |
    [Role]. [Target]. [Output format].
```

#### Fallback Rule

When an engine is unavailable (`which` fails), its workload falls back to a Claude subagent. This ensures 3 independent analyses even when external tools are missing.

#### Merge Strategies for Multi-Engine

| Strategy | When | Process |
|----------|------|---------|
| **Union** | Findings should be comprehensive (scans, tests, investigations) | Collect all → deduplicate same-location/same-type → boost confidence for multi-engine hits → sort by severity → report |
| **Compete** | Best single output needed (refactoring, proposals) | Collect all → evaluate against criteria → select best (or combine best parts) → present with rationale |

Each skill defines its own merge details (criteria, dedup rules, output format) in its SKILL.md.

---

### INDEPENDENT_IMPL

Parallel implementation of independent files/modules.

**When:** Multiple files need changes with no shared dependencies.

**Setup:**
- Each `general-purpose` subagent owns specific files (declare ownership upfront)
- No two subagents may modify the same file

**Merge:** Concat — combine all changes (no conflicts expected).

---

### VERIFICATION_PARALLEL

Run multiple verification tasks simultaneously.

**When:** Test suite, linter, type checker, and/or security scan can all run independently.

**Setup:**
- Each subagent runs one verification tool
- Results are independent pass/fail

**Merge:** All-pass gate — all must pass for overall success. Any failure blocks.

---

### COMPETITIVE_APPROACH

Multiple subagents implement different solutions to the same problem, then the best is selected.

**When:** Design exploration, algorithm comparison, or uncertain approach.

**Setup:**
- 2-3 `general-purpose` subagents, each with a different approach/constraint
- Each works in isolation on the same problem

**Merge:** Compete — evaluate each against criteria → select winner → adopt (or combine best elements).

---

## Result Aggregation

| Strategy | Description | Use With |
|----------|-------------|----------|
| **Union** | Collect all → deduplicate → consolidate → rank | RESEARCH_FAN_OUT, MULTI_ENGINE (comprehensive) |
| **Concat** | Combine all outputs (no overlap expected) | INDEPENDENT_IMPL |
| **All-pass** | Every result must pass; any failure = overall failure | VERIFICATION_PARALLEL |
| **Compete** | Evaluate against criteria → select best | COMPETITIVE_APPROACH, MULTI_ENGINE (selective) |

---

## Error Handling

| Scenario | Action |
|----------|--------|
| **1 of 3 subagents fails** | Continue with remaining results; note reduced coverage in report |
| **All subagents fail** | Fall back to sequential single-agent execution |
| **Timeout** (subagent takes too long) | Use available results; note incomplete coverage |
| **Conflicting results** | Flag contradictions explicitly; escalate to user if safety-critical |
| **Engine unavailable** (MULTI_ENGINE) | Fallback to Claude subagent per dispatch table |

---

## Constraints

| Rule | Limit | Reason |
|------|-------|--------|
| Max parallel subagents | **3** | Beyond 3 → use Rally for proper coordination |
| File ownership | **Exclusive** | No two subagents modify the same file |
| Cost awareness | **Each subagent = separate Claude instance** | Only parallelize when benefit > overhead |
| Spawn decision | **Agent's judgment** | Unless Nexus explicitly instructs `multi-engine` |
