# Phase Context Scoring

Evaluates phase readiness before execution to prevent premature phase starts and identify gaps.

---

## Overview

Before starting any phase, Titan calculates a Phase Readiness Score to determine if the phase can begin immediately or needs preparation.

```
Phase_Readiness = prior_artifacts(0.35) + clarity(0.30) + resources(0.20) + deps(0.15)
```

---

## Score Components

### Prior Artifacts (weight: 0.35)

Measures completeness of outputs from preceding phases.

| Score | Condition |
|-------|-----------|
| 1.0 | All required artifacts from prior phase present and validated |
| 0.75 | All required artifacts present, not all validated |
| 0.50 | Most required artifacts present (≥70%) |
| 0.25 | Some artifacts present (<70%) |
| 0.0 | No prior artifacts (first phase or gap) |

### Clarity (weight: 0.30)

Measures how well-defined the phase's inputs and goals are.

| Score | Condition |
|-------|-----------|
| 1.0 | Clear goals, defined acceptance criteria, no ambiguity |
| 0.75 | Goals clear, some criteria need refinement |
| 0.50 | General direction clear, specifics undefined |
| 0.25 | Vague goals, significant interpretation needed |
| 0.0 | No clarity — phase goals unknown |

### Resources (weight: 0.20)

Measures availability of required agents, tools, and external dependencies.

| Score | Condition |
|-------|-----------|
| 1.0 | All agents available, no external dependencies pending |
| 0.75 | All agents available, minor external deps manageable |
| 0.50 | Most agents available, some deps need resolution |
| 0.25 | Key agents or dependencies unavailable |
| 0.0 | Critical resources missing |

### Dependencies (weight: 0.15)

Measures resolution of cross-phase and external dependencies.

| Score | Condition |
|-------|-----------|
| 1.0 | All dependencies resolved |
| 0.75 | Dependencies resolved, some with workarounds |
| 0.50 | Most dependencies resolved (≥70%) |
| 0.25 | Many unresolved dependencies |
| 0.0 | Blocked by critical unresolved dependency |

---

## Readiness Thresholds

| Score | Verdict | Action |
|-------|---------|--------|
| **≥0.80** | **READY** | Start phase immediately |
| **0.60–0.79** | **CONDITIONAL** | Start with explicit assumptions documented |
| **0.40–0.59** | **PREPARE** | Issue preparation Epics before main phase work |
| **<0.40** | **NOT READY** | Re-execute prior phase or fill gaps first |

---

## Actions per Verdict

### READY (≥0.80)

- Proceed to phase execution immediately
- No additional preparation needed
- Log readiness score in TITAN_STATE

### CONDITIONAL (0.60–0.79)

- Document assumptions for missing/incomplete inputs
- List gaps under `## Phase Assumptions` in TITAN_STATE
- Proceed with phase execution
- Schedule gap-filling as parallel Epics if possible

### PREPARE (0.40–0.59)

- Generate preparation Epics to fill gaps:
  - Missing artifacts → generate via targeted Nexus chain
  - Unclear goals → Cipher analysis Epic
  - Missing deps → resolve dependency Epic
- Execute preparation Epics FIRST
- Re-score readiness after preparation
- Proceed only when score ≥0.60

### NOT READY (<0.40)

- Identify which prior phase produced insufficient output
- Return to prior phase with targeted Epics
- Anti-Stall L2 (Skip+return) if prior phase already attempted
- Re-score after prior phase re-execution

---

## Phase-Specific Readiness Profiles

### DISCOVER (First Phase)

| Component | Source | Typical Score |
|-----------|--------|--------------|
| Prior artifacts | User input / existing codebase | 0.25–0.75 |
| Clarity | User goal statement | 0.50–1.0 |
| Resources | Always available | 1.0 |
| Dependencies | None for first phase | 1.0 |

**Note**: DISCOVER typically starts with lower prior_artifacts score; this is expected.

### BUILD (Critical Phase)

| Component | Source | Minimum for START |
|-----------|--------|------------------|
| Prior artifacts | ARCHITECT outputs (ADR, API spec, schema) | 0.75+ |
| Clarity | Feature specs from DEFINE | 0.75+ |
| Resources | Builder/Artisan/Forge available | 1.0 |
| Dependencies | Architecture decisions made | 0.75+ |

**Note**: BUILD has highest readiness requirements — insufficient architecture leads to rework.

### LAUNCH (Delivery Phase)

| Component | Source | Minimum for START |
|-----------|--------|------------------|
| Prior artifacts | VALIDATE outputs (E2E pass, UX approved) | 0.80+ |
| Clarity | Release plan clear | 0.75+ |
| Resources | Guardian/Launch/Quill available | 1.0 |
| Dependencies | All tests green, security cleared | 0.80+ |

**Note**: LAUNCH should never start without validated product.

---

## Scoring Examples

### Example 1: BUILD after complete ARCHITECT

```
prior_artifacts: 0.90 (ADR + API spec + schema + structure all present)
clarity: 0.85 (feature specs clear, acceptance criteria defined)
resources: 1.00 (all agents available)
deps: 0.75 (one external API key pending, workaround exists)

Phase_Readiness = (0.90 × 0.35) + (0.85 × 0.30) + (1.00 × 0.20) + (0.75 × 0.15)
               = 0.315 + 0.255 + 0.200 + 0.1125
               = 0.8825 → READY
```

### Example 2: BUILD after partial ARCHITECT

```
prior_artifacts: 0.50 (ADR exists, no API spec, basic schema)
clarity: 0.50 (general features known, no detailed specs)
resources: 1.00 (all agents available)
deps: 0.50 (architecture decisions incomplete)

Phase_Readiness = (0.50 × 0.35) + (0.50 × 0.30) + (1.00 × 0.20) + (0.50 × 0.15)
               = 0.175 + 0.150 + 0.200 + 0.075
               = 0.600 → CONDITIONAL (document assumptions, proceed)
```

### Example 3: LAUNCH without VALIDATE

```
prior_artifacts: 0.25 (build works but no E2E, no UX review)
clarity: 0.75 (release plan exists)
resources: 1.00 (all agents available)
deps: 0.25 (tests not validated, security not cleared)

Phase_Readiness = (0.25 × 0.35) + (0.75 × 0.30) + (1.00 × 0.20) + (0.25 × 0.15)
               = 0.0875 + 0.225 + 0.200 + 0.0375
               = 0.550 → PREPARE (run validation first)
```
