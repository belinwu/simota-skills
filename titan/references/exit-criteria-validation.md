# Exit Criteria Auto-Validation

Defines automated validation of phase exit criteria before Titan approves phase transitions.

---

## Overview

Before any phase transition, Titan runs an automated validation chain to verify exit criteria are met. This prevents premature phase advancement and catches quality gaps early.

```
Phase work complete
  → Exit Criteria Validation
    → Pass (≥80%) → Next phase
    → Partial (60-79%) → Scope Reduction + proceed
    → Fail (<60%) → Anti-Stall activation
```

---

## Validation Chains (Phase-Specific)

Each phase uses a tailored validation chain optimized for its artifact types. The universal `Lens→Radar→Warden` chain is replaced with phase-appropriate agents.

| Phase | Validation Chain | Rationale |
|-------|-----------------|-----------|
| DISCOVER | Lens → Researcher → Compete → Warden | Validate research quality, persona completeness, competitive coverage |
| DEFINE | Lens → Canon → Magi → Warden | Validate specs against standards, decision quality |
| ARCHITECT | Lens → Atlas → Schema → Warden | Validate architecture integrity, dependency analysis, schema quality |
| BUILD | Lens → Radar → Warden | Validate code artifacts, test coverage, build health (default chain) |
| HARDEN | Sentinel → Radar → Warden | Validate security audit, test suite, quality gate |
| VALIDATE | Voyager → Echo → Warden | Validate E2E tests, UX persona review |
| LAUNCH | Lens → Quill → Gear → Warden | Validate docs, CI/CD pipeline, deployment readiness |
| GROW | Growth → Pulse → Warden | Validate SEO/CRO, analytics setup |
| EVOLVE | Voice → Sweep → Warden | Validate feedback collection, tech debt assessment |

### Chain Issuance

```markdown
## NEXUS_AUTORUN_FULL
Task: Validate Phase [PHASE_NAME] exit criteria
Chain: [Phase-specific chain from table above]
Context: Phase [N] complete, verify exit criteria before transition
Acceptance: Validation report with per-criterion pass/fail and overall score
```

---

## Phase-Specific Validation Checklists

### DISCOVER Phase Exit

| Criterion | Validation Method | Weight | Pass Threshold |
|-----------|------------------|--------|---------------|
| Product Definition exists | Lens: file exists + >100 lines | 0.30 | File present |
| Target personas defined | Lens: personas section present | 0.25 | ≥2 personas |
| Value proposition clear | Lens: value prop section present | 0.25 | Non-empty |
| Constraints identified | Lens: constraints listed | 0.20 | ≥1 constraint |

### DEFINE Phase Exit

| Criterion | Validation Method | Weight | Pass Threshold |
|-----------|------------------|--------|---------------|
| Roadmap complete | Lens: roadmap.md with features | 0.25 | ≥3 features |
| Feature specs written | Lens: specs/ directory populated | 0.25 | All roadmap items |
| SUCCESS_CRITERIA defined | Lens: measurable criteria | 0.25 | ≥3 criteria |
| KPIs specified | Lens: tracking events listed | 0.25 | ≥2 KPIs |

### ARCHITECT Phase Exit

| Criterion | Validation Method | Weight | Pass Threshold |
|-----------|------------------|--------|---------------|
| ADR documented | Lens: adr/ files exist | 0.25 | ≥1 ADR |
| API spec defined | Lens: API spec file exists | 0.20 | Endpoints listed |
| DB schema designed | Lens: schema file exists | 0.20 | Tables/models defined |
| Repo structure defined | Lens: directory layout | 0.20 | Structure documented |
| No circular deps | Atlas: dependency analysis | 0.15 | Zero circular |

### BUILD Phase Exit

| Criterion | Validation Method | Weight | Pass Threshold |
|-----------|------------------|--------|---------------|
| All features implemented | Lens: source files per spec | 0.25 | All spec items |
| Tests passing | Radar: test runner exit 0 | 0.30 | 100% pass |
| Build succeeds | Radar: build command exit 0 | 0.25 | Clean build |
| Basic coverage | Radar: coverage report | 0.20 | ≥60% |

### HARDEN Phase Exit

| Criterion | Validation Method | Weight | Pass Threshold |
|-----------|------------------|--------|---------------|
| Security audit pass | Sentinel report: no critical | 0.30 | Zero critical |
| Performance targets met | Bolt report: benchmarks | 0.25 | Within targets |
| Code quality approved | Warden: quality score | 0.25 | ≥B grade |
| All tests green | Radar: full suite | 0.20 | 100% pass |

### VALIDATE Phase Exit

| Criterion | Validation Method | Weight | Pass Threshold |
|-----------|------------------|--------|---------------|
| E2E tests passing | Voyager: E2E suite | 0.30 | ≥95% pass |
| UX validated | Echo: persona review | 0.25 | No critical issues |
| Experiments configured | Experiment: A/B setup | 0.20 | Config complete |
| Quality gate passed | Warden: final assessment | 0.25 | Approved |

### LAUNCH Phase Exit

| Criterion | Validation Method | Weight | Pass Threshold |
|-----------|------------------|--------|---------------|
| Documentation complete | Lens: README + API docs | 0.25 | All sections |
| Release notes written | Lens: CHANGELOG exists | 0.20 | Current version |
| CI/CD configured | Gear: pipeline check | 0.25 | Pipeline runs |
| Demos created | Lens: demo artifacts | 0.15 | ≥1 demo |
| Deployment ready | Guardian: PR ready | 0.15 | PR created |

### GROW Phase Exit

| Criterion | Validation Method | Weight | Pass Threshold |
|-----------|------------------|--------|---------------|
| SEO optimized | Growth: meta audit | 0.30 | Core tags present |
| Analytics active | Pulse: events firing | 0.30 | Key events tracked |
| Retention features | Lens: features present | 0.20 | ≥1 feature |
| Growth experiments | Experiment: setup | 0.20 | ≥1 experiment |

### EVOLVE Phase Exit

| Criterion | Validation Method | Weight | Pass Threshold |
|-----------|------------------|--------|---------------|
| Feedback collected | Voice: report exists | 0.30 | Actionable insights |
| Improvement plan | Lens: plan document | 0.30 | Prioritized list |
| Tech debt assessed | Sweep/Horizon: report | 0.20 | Inventory complete |
| Next cycle input | Lens: DISCOVER input ready | 0.20 | Personas + criteria updated |

---

## Scoring and Pass Rules

### Score Calculation

```
phase_exit_score = Σ(criterion_pass × weight) / Σ(weight)
```

Each criterion scores: 1.0 (full pass), 0.5 (partial), 0.0 (fail).

### Pass Thresholds

| Score | Verdict | Action |
|-------|---------|--------|
| **≥0.80** | **PASS** | Proceed to next phase immediately |
| **0.60–0.79** | **CONDITIONAL** | Scope Reduction: move failing criteria to next phase as Epics |
| **<0.60** | **FAIL** | Anti-Stall activation (L1 retry the failing Epics) |

### Conditional Pass Handling

When score is 0.60–0.79:

1. Identify failing criteria
2. Create backlog Epics for each failing criterion
3. Add Epics to the next phase's work queue (or current phase if revisiting)
4. Log the conditional pass with gaps in TITAN_STATE
5. Proceed to next phase

### Fail Handling

When score <0.60:

1. Identify which Epics produced insufficient artifacts
2. Route to Anti-Stall L1 (retry those specific Epics)
3. If L1 exhausted → L2 (scope reduction to accept lower bar)
4. Re-run exit validation after recovery

---

## Validation Overrides

In specific scenarios, validation thresholds can be relaxed:

| Scenario | Override | Justification |
|----------|---------|---------------|
| S scope (small project) | Reduce required artifacts | Small tools don't need all docs |
| L4 Degradation active | Accept partial pass (≥0.40) | Graceful degradation mode |
| PHASED_REVIEW mode | User approves despite score | Explicit user override |
