# Skill Effectiveness Tracking (ATTUNE)

Quality trend tracking, project-type calibration, pattern library, and usage signal detection.
Sigil gets better at generating high-value skills by learning from outcomes.

---

## Overview

The ATTUNE phase runs post-batch (after VERIFY) to close the feedback loop between skill generation and actual project value. Without ATTUNE, Sigil generates skills based on static heuristics. With it, priority ranking and template selection become progressively more accurate.

```
OBSERVE ──→ MEASURE ──→ ADAPT ──→ PERSIST
  │             │          │         │
  │ Collect     │ Score    │ Update  │ Store in
  │ quality     │ trends   │ ranking │ journal
  │ signals     │ analysis │ weights │
```

---

## OBSERVE — Collect Quality Signals

After each skill generation batch, record:

```yaml
Batch: [project-name]-[date]
Project_Type: [web-app | api | cli | library | monorepo | full-stack]
Tech_Stack: [framework/language]
Skills_Generated: [count]
Quality_Scores:
  - name: [skill-name]
    type: [Micro | Full]
    score: [0-12]
    dimensions: [Format/Relevance/Completeness/Actionability]
    category: [workflow | convention | pattern | integration]
Existing_Skills_Found: [count]
Style_Profile_Applied: [yes | no]
Evolution_Opportunities: [count]
```

### Usage Signal Detection

While Sigil cannot directly measure skill usage, it can detect indirect signals during subsequent SCAN phases:

| Signal | Detection Method | Interpretation |
|--------|-----------------|----------------|
| Skill file unchanged since install | File modification time | Low usage (or perfectly sufficient) |
| Skill file manually modified | Diff against original | User adapted skill — learn from changes |
| Skill referenced in CLAUDE.md | Content search | High adoption signal |
| New files matching skill patterns | Directory scan | Skill is being followed |
| Skill deleted by user | Missing from directory | Skill was not valuable — investigate why |
| Skill sync drift | Directory comparison | One copy modified, other stale |

---

## MEASURE — Analyze Quality Trends

### Per-Project Quality Summary

```markdown
### Quality Summary: [Project Name]

| Metric | Value | Trend |
|--------|-------|-------|
| Skills generated | 8 | — |
| Average quality score | 10.2/12 | — |
| Pass rate (9+) | 87.5% (7/8) | — |
| Recraft rate | 12.5% (1/8) | — |
| Dominant category | Workflow (5/8) | — |

**Strongest dimension**: Actionability (avg 2.8/3)
**Weakest dimension**: Relevance (avg 2.3/3)
**Note**: Relevance improved with style profile application.
```

### Cross-Project Pattern Detection

Track quality across project types to identify:

| Project Type | Avg Score | Common High-Value Skills | Common Low-Value Skills |
|-------------|-----------|------------------------|------------------------|
| Next.js App Router | 10.5 | new-page, new-component, data-fetching | env-setup (too generic) |
| Express API | 9.8 | new-route, new-middleware, error-handling | naming-rules (obvious) |
| Go stdlib | 10.2 | new-handler, testing-pattern | new-middleware (too simple) |
| Python FastAPI | 10.0 | new-router, crud-pattern | new-schema (trivial) |
| Monorepo | 9.2 | deploy-flow, pr-template | package-specific (scope confusion) |

---

## ADAPT — Update Ranking and Templates

### Priority Weight Calibration

Base priority formula: `Priority = Frequency × Complexity × Risk × Onboarding`

Calibrate weights from quality outcomes:

```yaml
# Default weights
frequency_weight: 1.0
complexity_weight: 1.0
risk_weight: 1.0
onboarding_weight: 1.0

# Calibrated weights (from ATTUNE data)
# Example: Complexity-heavy skills consistently score higher
frequency_weight: 0.8   # Adjust down: simple frequent tasks need less guidance
complexity_weight: 1.3   # Adjust up: complex tasks benefit most from skills
risk_weight: 1.2         # Adjust up: risk reduction has high value
onboarding_weight: 0.9   # Adjust slightly: useful but often generic
```

### Adaptation Rules

1. **3+ data points required** before adjusting weights
2. **Max adjustment per batch**: ±0.3 per weight (prevent overcorrection)
3. **Decay**: Adjustments decay 10% per month toward defaults
4. **Override**: User explicit priority always wins over calibration

### Template Selection Calibration

Track which template patterns score highest by context:

| Context | Higher Scoring Template | Lower Scoring Template |
|---------|----------------------|----------------------|
| Next.js + Tailwind | Conditional CSS branch | Single CSS approach |
| API projects | Zod validation inline | Separate validation file |
| Monorepo | Package-scoped skills | Root-only skills |
| TypeScript strict | Full type annotations | Minimal types |

---

## PERSIST — Store Calibration Data

### Journal Entry Format

Record ATTUNE insights in `.agents/sigil.md`:

```markdown
## YYYY-MM-DD - ATTUNE: [Project Type]

**Batch size**: N skills
**Avg quality**: X.X/12
**Key insight**: [description]
**Calibration adjustment**: [weight: old → new]
**Apply when**: [future scenario]
**reusable**: true

<!-- EVOLUTION_SIGNAL
type: PATTERN
source: Sigil
date: YYYY-MM-DD
summary: [skill generation insight]
affects: [Sigil, relevant agents]
priority: MEDIUM
reusable: true
-->
```

### Pattern Library

Build a library of high-value skill patterns by project type:

| Project Type | Must-Have Skills | Avg Batch Size | Best First Skill | Quality Notes |
|-------------|-----------------|---------------|-----------------|---------------|
| Next.js (App Router) | new-page, new-component, new-server-action | 5-7 | new-component | Style profile critical for relevance |
| Express/Fastify | new-route, new-middleware, error-handling | 4-6 | new-route | Error handling pattern varies widely |
| FastAPI | new-router, new-model, crud-pattern | 4-5 | new-router | Pydantic version affects templates |
| Go (stdlib) | new-handler, new-service, testing-pattern | 4-6 | new-handler | Table-driven test patterns score high |
| Rails | new-model, new-controller, new-migration | 5-7 | new-model | Strong convention = high relevance |
| Monorepo | pr-template, deploy-flow, naming-rules | 3-5 + per-package | pr-template | Root vs package scope clarity key |

### Quick Calibration (Small Batches)

For batches < 3 skills:

```markdown
## Quick ATTUNE

**Skills**: 2 generated
**Avg quality**: 10.5/12
**Note**: Convention mirroring worked well for this Rails project
**Action**: No weight change (insufficient data)
```

Rule: Do not adjust weights from a single small batch. Accumulate data across batches.

---

## Integration with Skill Evolution

ATTUNE data feeds into evolution decisions:

| ATTUNE Signal | Evolution Impact |
|--------------|-----------------|
| Quality improving over batches | Skill generation approach is working — continue |
| Quality degrading | Re-examine SCAN accuracy, convention detection |
| Certain skill category consistently low | May indicate catalog gap — consider new template |
| User modifications detected | Learn from changes, update templates |
| Skills deleted | Investigate: wrong priority? duplicate? too generic? |

---

## Feedback to Ecosystem

When ATTUNE discovers patterns valuable beyond a single project:

1. **Record in journal** with `reusable: true` tag
2. **Emit EVOLUTION_SIGNAL** for Lore to collect
3. **Inform Architect** if a recurring project need suggests a new ecosystem agent
4. **Update skill-catalog.md** if new framework patterns emerge consistently
