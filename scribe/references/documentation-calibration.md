# Documentation Calibration System (INSCRIBE)

Template effectiveness tracking, specification adoption analysis, requirement completeness scoring, and document quality measurement.
Scribe gets better at creating specifications by learning from outcomes.

---

## Overview

The INSCRIBE phase runs post-document (or periodically) to close the feedback loop between specification creation and actual implementation outcomes. Without INSCRIBE, template selection stays static and writing patterns remain uncalibrated. With it, Scribe's documents become progressively more accurate, actionable, and useful.

```
RECORD ──→ EVALUATE ──→ CALIBRATE ──→ PROPAGATE
  │            │            │            │
  │ Log       │ Measure    │ Update    │ Share with
  │ documents │ adoption   │ template  │ Lore/Accord
  │ & usage   │ & accuracy │ weights   │
```

---

## RECORD — Log Documentation Activities

After each document, record:

```yaml
Document: [document-id]
Type: [PRD | SRS | HLD | LLD | Impl Checklist | Test Spec | Review Checklist]
Feature: [feature name]
Requirements_Count: [total REQ/FR IDs]
Acceptance_Criteria_Count: [total AC IDs]
Template_Used: [full/minimal]
Sections_Included: [list]
Quality_Checklist_Score:
  structure: [pass/partial/fail]
  content: [pass/partial/fail]
  testability: [pass/partial/fail]
  traceability: [pass/partial/fail]
Downstream_Handoff: [Sherpa/Builder/Radar/Voyager/Judge/None]
```

### What to Track

| Data Point | Why | Used For |
|-----------|-----|----------|
| Specification adoption | Are specs referenced during implementation? | Template usefulness improvement |
| Requirement completeness | Are all requirements testable and traceable? | Writing quality improvement |
| Template effectiveness | Which templates lead to fewest implementation gaps? | Template selection heuristic |
| Document accuracy | Do implementations match specifications? | Precision improvement |
| Handoff quality | Did downstream agents have sufficient detail? | Handoff completeness tuning |
| Revision frequency | How often are specs revised post-creation? | Initial quality improvement |

---

## EVALUATE — Measure Documentation Impact

### Specification Adoption Tracking

```
Adoption Rate = Documents Referenced by Downstream Agents / Total Documents Created

> 0.85  = High-impact documentation (maintain approach)
0.60-0.85 = Moderate adoption (review handoff quality, format)
< 0.60  = Low adoption (review document usefulness, audience alignment)
```

### Requirement Accuracy Tracking

```
Accuracy = Requirements Implemented as Specified / Total Requirements

> 0.90  = Excellent specification quality
0.75-0.90 = Good, some ambiguity issues
< 0.75  = Weak specs (review precision, testability)
```

### Evaluation Triggers

| Trigger | Check |
|---------|-------|
| Builder requests clarification | Specification clarity, completeness |
| Radar can't create tests from spec | Testability, acceptance criteria quality |
| Feature shipped with gaps | Requirement completeness |
| Document revised multiple times | Initial quality, stakeholder alignment |
| Quarterly review | Overall documentation effectiveness |

### Per-Period Evaluation Summary

```markdown
### Documentation Evaluation

| Metric | Value | Trend |
|--------|-------|-------|
| Documents created | 12 | — |
| Requirements defined | 48 | — |
| Acceptance criteria defined | 36 | — |
| Specification adoption rate | 83% (10/12) | ↑ |
| Requirement accuracy | 88% (42/48) | — |
| Quality checklist pass rate | 92% | — |
| Average revisions per document | 1.2 | ↓ |

**Strongest template**: SRS (highest downstream adoption)
**Weakest area**: HLD traceability (often missing links to SRS)
**Note**: Given-When-Then acceptance criteria reduced implementation gaps by 30%.
```

---

## CALIBRATE — Update Documentation Heuristics

### Template Effectiveness Scoring

Track which templates work best in which contexts:

```yaml
# Default template effectiveness by context
prd_effectiveness:
  new_feature: 0.90
  feature_enhancement: 0.80
  migration: 0.65
srs_effectiveness:
  api_feature: 0.95
  ui_feature: 0.80
  infrastructure: 0.85
hld_effectiveness:
  new_system: 0.90
  system_extension: 0.85
  refactoring: 0.70
checklist_effectiveness:
  complex_feature: 0.90
  simple_feature: 0.75
  bug_fix: 0.60

# Calibrated (from INSCRIBE data)
# Example: Minimal PRD template more effective for enhancements
prd_effectiveness:
  feature_enhancement: 0.80 → 0.90  # Minimal template reduced overhead, improved adoption
```

### Calibration Rules

1. **3+ documents required** before adjusting template effectiveness scores
2. **Max adjustment per cycle**: ±0.15 (prevent overcorrection)
3. **Decay**: Adjustments decay 10% per quarter toward defaults
4. **Override**: User explicit template preferences always win

### Writing Pattern Calibration

Track which writing patterns produce most actionable specs:

| Pattern | Adoption Impact | Clarity Score | Best For |
|---------|----------------|---------------|----------|
| REQ-XXX ID system | High | High | All document types |
| Given-When-Then AC | High | Very High | PRD, SRS, Test Spec |
| IMPL-XXX with I/O contract | High | High | Implementation checklists |
| ASCII diagrams (inline) | Medium | High | HLD, SRS |
| Traceability matrix | Medium | High | Multi-document projects |
| Quick/Minimal templates | High | Medium | Small features, bug fixes |

### Document Size Calibration

Track optimal document sizes by type:

| Document Type | Default Size | Calibrated Range | Notes |
|--------------|-------------|-----------------|-------|
| PRD (full) | 200-400 lines | 150-350 lines | Shorter docs had higher adoption |
| PRD (minimal) | 30-80 lines | 40-80 lines | Under 40 lines missed edge cases |
| SRS | 200-500 lines | 200-400 lines | Over 400 lines rarely fully read |
| HLD | 150-300 lines | 100-250 lines | Focus on diagrams over prose |
| LLD | 200-400 lines | 200-350 lines | Code examples improve clarity |
| Test Spec | 100-300 lines | 100-250 lines | Table format preferred over prose |

---

## PROPAGATE — Share Validated Patterns

### Journal Entry Format

Record INSCRIBE insights in `.agents/scribe.md`:

```markdown
## YYYY-MM-DD - INSCRIBE: [Document Type]

**Documents assessed**: N
**Overall adoption rate**: X%
**Key insight**: [description]
**Calibration adjustment**: [template/pattern: old → new]
**Apply when**: [future scenario]
**reusable**: true

<!-- EVOLUTION_SIGNAL
type: PATTERN
source: Scribe
date: YYYY-MM-DD
summary: [documentation insight]
affects: [Scribe, Accord, Sherpa]
priority: MEDIUM
reusable: true
-->
```

### Pattern Library

Build a library of effective documentation approaches by context:

| Context | Best Template | Key Elements | Adoption Rate |
|---------|--------------|-------------|---------------|
| New feature (complex) | Full PRD → SRS → HLD/LLD | REQ IDs, Given-When-Then AC, Traceability | High |
| Feature enhancement | Minimal PRD | REQ IDs, Edge cases, Out of scope | High |
| API endpoint | SRS | FR with I/O/Error, OpenAPI ref, Sequence diagram | Very High |
| Architecture change | HLD | System context, Component diagram, Integration design | High |
| Bug fix | Quick Checklist | Root cause, Fix steps, Regression tests | Medium-High |
| Test planning | Test Spec + BDD | Gherkin scenarios, Test data, Traceability matrix | High |

### Quick Calibration (Small Documents)

For documents with < 3 requirements:

```markdown
## Quick INSCRIBE

**Documents**: 1 completed
**Requirements**: 2 (too few to calibrate)
**Note**: Minimal PRD template was immediately adopted by Sherpa
**Action**: No weight change (insufficient data)
```

Rule: Do not adjust weights from a single small document. Accumulate data across documents.

---

## Integration with Ecosystem

INSCRIBE data feeds into documentation decisions:

| INSCRIBE Signal | Ecosystem Impact |
|----------------|-----------------|
| Specification adoption improving | Confidence in document quality increases |
| Adoption degrading | Re-examine template format, audience alignment |
| Template consistently underperforming | Revise template, try alternative format |
| High requirement accuracy | Specification approach is working — continue |
| Low downstream utilization | Adjust handoff format, improve detail level |
| Validated documentation pattern | Share with Lore, update Accord specification quality |

---

## Feedback to Ecosystem

When INSCRIBE discovers patterns valuable beyond a single document:

1. **Record in journal** with `reusable: true` tag
2. **Emit EVOLUTION_SIGNAL** for Lore to collect
3. **Feed to Accord** if requirement clarity patterns improve specification quality
4. **Inform Sherpa** if checklist patterns improve task decomposition
5. **Update writing guidelines** if new precision patterns are identified
