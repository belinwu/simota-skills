# aiw Tool Guide

Comprehensive guide for the `aiw` (AI Workflow Orchestrator) CLI tool used by Arena for multi-engine parallel implementation.

---

## Overview

`aiw` is a CLI tool that provides unified control over multiple AI engines, enabling parallel implementation and comparison workflows.

### Key Characteristics

| Characteristic | Description |
|----------------|-------------|
| **No API Key Required** | Each engine (Claude Code, Codex CLI, Gemini CLI) has its own authentication mechanism, so aiw itself requires no additional API key configuration |
| **Zero Config** | Ready to use immediately after `aiw init` |
| **Engine Transparent** | Operate multiple engines through a single unified interface |

### Prerequisites

Each engine requires individual setup beforehand:
- **Claude Code**: `claude` command must be available
- **Codex CLI**: `codex` command must be available
- **Gemini CLI**: `gemini` command must be available

Since aiw wraps and invokes each engine's CLI, individual API key configuration is completed during each engine's setup process.

### Quick Start

```bash
# Initialize (once only)
aiw init

# Ready to use immediately
aiw run --spec spec.yaml --variants 2
```

---

## Core Workflow: 5 Phases

```
1. SPEC     - aiw spec generate / critique
      |
2. RUN      - aiw run --spec --variants N --engine X
      |
3. EVALUATE - aiw show / diff / quality metrics analysis
      |
4. ADOPT    - aiw adopt <run_id> <variant>
      |
5. VERIFY   - Tests, build, security confirmation
```

---

## Phase 1: SPEC (Specification)

Ensure clear specifications before implementation.

```bash
# Initialize aiw if not already done
aiw init

# Generate specification from description
aiw spec generate "feature description"

# Critique specification for ambiguities
aiw spec critique <spec_file>
```

**Spec Quality Checklist:**
- [ ] Clear acceptance criteria
- [ ] Input/output definitions
- [ ] Error handling requirements
- [ ] Performance constraints (if any)
- [ ] Security considerations

---

## Phase 2: RUN (Parallel Execution)

Execute implementations across multiple engines.

```bash
# Basic parallel run (2 variants, default engine)
aiw run --spec spec.yaml --variants 2

# Specify engine
aiw run --spec spec.yaml --variants 3 --engine claude-code

# Multi-engine comparison
aiw run --spec spec.yaml --variants 2 --engine claude-code
aiw run --spec spec.yaml --variants 2 --engine codex-cli
aiw run --spec spec.yaml --variants 2 --engine gemini-cli
```

### Engine Selection Guide

| Engine | Strengths | Best For |
|--------|-----------|----------|
| `claude-code` | Nuanced understanding, safety | Complex logic, security-sensitive |
| `codex-cli` | Fast iteration, code-focused | Algorithmic tasks, refactoring |
| `gemini-cli` | Broad context, creative | Novel approaches, exploration |

### Engine Selection Heuristics

- **Default to `claude-code`** for most tasks (best balance of quality and safety)
- **Use `codex-cli`** when speed matters more than nuance, or for pure algorithmic work
- **Use `gemini-cli`** when you want creative/divergent approaches
- **Use all engines** only when quality justifies the cost (security-critical, high-stakes)

---

## Phase 3: EVALUATE (Comparison)

Analyze and compare generated variants.

```bash
# Show all variants from a run
aiw show <run_id>

# Diff between specific variants
aiw diff <run_id> <variant_a> <variant_b>

# Check costs
aiw cost <run_id>
```

### Evaluation Focus Areas

1. **Correctness** (40%) - Does it meet the specification?
2. **Code Quality** (25%) - Readability, maintainability, patterns
3. **Performance** (15%) - Efficiency, resource usage
4. **Safety** (15%) - Error handling, security
5. **Simplicity** (5%) - Avoids over-engineering

---

## Phase 4: ADOPT (Selection)

Select and adopt the winning variant.

```bash
# Adopt the selected variant
aiw adopt <run_id> <variant_id>
```

Always document the selection rationale (see `references/decision-templates.md` for format).

---

## Phase 5: VERIFY (Confirmation)

Confirm the adopted implementation.

```bash
# Run tests
npm test  # or project-specific test command

# Build verification
npm run build  # or project-specific build command

# Security scan (if applicable)
# Delegate to Sentinel for detailed analysis
```

### Verification Checklist

- [ ] All existing tests pass
- [ ] New functionality has test coverage
- [ ] Build succeeds without warnings
- [ ] No security vulnerabilities introduced
- [ ] Performance within acceptable bounds

---

## Cost Management

### Monitoring Commands

```bash
# Check cost for a specific run
aiw cost <run_id>

# Compare cost efficiency across runs
aiw cost --summary
```

### Cost Optimization Strategies

| Strategy | When to Apply |
|----------|--------------|
| Reduce variant count | Budget-constrained tasks |
| Single engine first | Explore before committing to multi-engine |
| Spec critique first | Prevent wasted runs from ambiguous specs |
| Reuse prior runs | When iterating on similar specs |

---

## Common Patterns

### Pattern: Iterative Refinement

```bash
# Round 1: Broad exploration
aiw run --spec spec.yaml --variants 3 --engine claude-code

# Evaluate and identify best approach
aiw show <run_id>

# Round 2: Refine best approach with different engines
aiw run --spec refined-spec.yaml --variants 2 --engine codex-cli
```

### Pattern: Security-Critical Implementation

```bash
# Generate with safety-focused engine
aiw run --spec spec.yaml --variants 2 --engine claude-code

# Compare, adopt, then hand off to Sentinel for deep review
aiw adopt <run_id> <best_variant>
# -> Sentinel for security audit
```
