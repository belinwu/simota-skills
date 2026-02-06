# Task Breakdown Framework

Task hierarchy definitions, T-shirt sizing, time estimation formulas, and complexity factors.

---

## Task Hierarchy

| Level | Size | Description | Example |
|-------|------|-------------|---------|
| **Epic** | 1-5 days | Large feature or initiative | "Implement payment system" |
| **Story** | 2-8 hours | User-facing functionality | "Add checkout form" |
| **Task** | 30-120 min | Technical work unit | "Create PaymentForm component" |
| **Atomic Step** | 5-15 min | Single action, testable, committable | "Define PaymentProps interface" |

---

## Epic Input Template

```markdown
## Epic: [Name]

**Goal**: [What we're trying to achieve]
**Success Criteria**: [How we know it's done]
**Constraints**: [Time, tech, scope limits]
**Out of Scope**: [What we're NOT doing]

**Initial Estimate**: [T-shirt size: XS/S/M/L/XL]
**Risk Level**: [Low / Medium / High]
```

---

## T-Shirt Sizing

| Size | Minutes | Complexity | Example |
|------|---------|------------|---------|
| **XS** | 5-10 | Trivial, no unknowns | Add a constant, rename variable |
| **S** | 10-15 | Simple, clear path | Add a field, simple function |
| **M** | 15-30 | Moderate, some decisions | New component, API endpoint |
| **L** | 30-60 | Complex, multiple parts | Feature with tests |
| **XL** | 60+ | **Too big - break down further** | - |

---

## Complexity Factors

| Factor | Multiplier | Description |
|--------|------------|-------------|
| New technology | 1.5x | First time using library/API |
| Unclear requirements | 1.5x | Need investigation |
| External dependency | 2x | Third-party API, approval needed |
| High risk | 1.5x | Can break existing functionality |
| Multiple files | 1.3x | Changes across many files |

---

## Estimation Formula

```
Actual Time = Base Estimate x Complexity Multiplier x Risk Buffer

Risk Buffer:
- Low: 1.0x
- Medium: 1.3x
- High: 1.5x
```

### Estimation Output Template

```markdown
### Time Estimate: [Step Name]

| Aspect | Value |
|--------|-------|
| Base Size | M (20 min) |
| Complexity | New API (1.5x) |
| Risk Level | Medium (1.3x) |
| **Estimated** | **39 min** |

Over 15 min threshold - consider breaking down further.
```

---

## Breakdown Rules

1. Keep breaking down until every step is < 15 minutes
2. Each Atomic Step must be testable (you can verify it works)
3. Each Atomic Step must be committable (clean save point)
4. Identify the agent responsible for each step (Builder, Forge, Zen, etc.)
5. Mark dependencies between steps before starting
6. Flag XL items immediately - they always need further decomposition
