# Guardian Collaboration Patterns Reference

Detailed collaboration patterns and flows with partner agents.

## Pattern A: Plan-to-Commit Flow

**Flow**: `Plan → Guardian → Builder`

**Purpose**: Transform implementation plan into optimized Git strategy before coding begins.

```
┌────────┐    Implementation Plan    ┌──────────┐    Commit Strategy    ┌─────────┐
│  Plan  │ ────────────────────────▶ │ Guardian │ ────────────────────▶ │ Builder │
└────────┘                           └──────────┘                       └─────────┘
              Branch strategy              │              Staged files
              Scope analysis               │              per commit
                                          ↓
                                   PR size forecast
```

**Trigger Conditions**:
- Task planning complete
- Multi-file implementation planned
- Feature branch needed

**Guardian Actions**:
1. Analyze planned scope and files
2. Generate optimal branch name
3. Propose commit structure
4. Forecast PR size and reviewability
5. Recommend split strategy if needed

## Pattern B: Build-to-Review Flow

**Flow**: `Builder → Guardian → Judge`

**Purpose**: Analyze completed changes and prepare optimized PR for review.

```
┌─────────┐    Code Changes    ┌──────────┐    Prepared PR    ┌─────────┐
│ Builder │ ─────────────────▶ │ Guardian │ ────────────────▶ │  Judge  │
└─────────┘                    └──────────┘                   └─────────┘
              Staged files           │           PR description
              Commit history         │           Review focus
                                    ↓
                              Signal/Noise filter
```

**Trigger Conditions**:
- Code implementation complete
- Ready to create PR
- Changes need organization

**Guardian Actions**:
1. Classify changes (Essential/Supporting/Noise)
2. Optimize commit granularity
3. Generate PR description
4. Identify review focus areas
5. Recommend merge strategy

## Pattern C: Noise Separation Loop

**Flow**: `Guardian ↔ Zen`

**Purpose**: Iteratively clean up noise while preserving essential changes.

```
┌──────────┐    Noise Identified    ┌─────────┐    Cleaned Diff    ┌──────────┐
│ Guardian │ ─────────────────────▶ │   Zen   │ ────────────────▶ │ Guardian │
└──────────┘                        └─────────┘                   └──────────┘
     │         Formatting issues         │           Clean code        │
     │         Style violations          │           Separated         │
     │                                   │           commits           │
     └───────────────────────────────────┴─────────────────────────────┘
                              Iteration until clean
```

**Trigger Conditions**:
- High noise ratio detected (>30%)
- Mixed formatting and logic changes
- Style violations in diff

**Guardian Actions**:
1. Identify noise files/hunks
2. Request Zen cleanup
3. Re-analyze cleaned diff
4. Verify separation quality
5. Finalize commit structure

## Pattern D: PR Visualization

**Flow**: `Guardian → Canvas`

**Purpose**: Generate visual representation of change dependencies.

```
┌──────────┐    Change Graph    ┌────────┐
│ Guardian │ ─────────────────▶ │ Canvas │
└──────────┘                    └────────┘
              File dependencies      │
              Module impact          │
              Merge order            ↓
                                Mermaid/ASCII diagram
```

**Trigger Conditions**:
- Complex multi-module changes
- Monorepo impact analysis
- PR split visualization needed

**Guardian Actions**:
1. Map file dependencies
2. Calculate change impact
3. Request Canvas visualization
4. Include in PR description

## Pattern E: Conflict Resolution

**Flow**: `Guardian ↔ Scout`

**Purpose**: Investigate and resolve merge conflicts with technical context.

```
┌──────────┐    Conflict Type    ┌─────────┐    Investigation    ┌──────────┐
│ Guardian │ ──────────────────▶ │  Scout  │ ─────────────────▶ │ Guardian │
└──────────┘                     └─────────┘                    └──────────┘
     │         Semantic conflict       │          Root cause         │
     │         File history needed     │          Intent analysis    │
     │                                 │                             │
     └─────────────────────────────────┴─────────────────────────────┘
                              Resolution guidance
```

**Trigger Conditions**:
- Semantic merge conflict detected
- Intent unclear from diff alone
- History investigation needed

**Guardian Actions**:
1. Classify conflict type
2. Request Scout investigation if semantic
3. Synthesize resolution guidance
4. Propose merge approach

## Pattern F: Pre-Commit Quality Gate

**Flow**: `Guardian ↔ Judge`

**Purpose**: Verify dependency changes and detect AI hallucinations before commit.

```
┌──────────┐   Dependency/AI Changes   ┌─────────┐   Verification   ┌──────────┐
│ Guardian │ ─────────────────────────▶ │  Judge  │ ────────────────▶ │ Guardian │
└──────────┘                           └─────────┘                   └──────────┘
     │         Package changes              │          Valid/Invalid       │
     │         AI-suspected code            │          Hallucination       │
     │         New imports                  │          check result        │
     └──────────────────────────────────────┴──────────────────────────────┘
                                  Commit structure finalized
```

**Trigger Conditions**:
- `package.json`, `requirements.txt`, `go.mod` etc. modified
- AI-suspected code detected (>10% of changes)
- New imports from unfamiliar packages
- Substantial logic changes in single file

**Guardian Actions**:
1. Identify dependency changes
2. Flag AI-suspected code
3. Request Judge quality gate verification
4. Integrate verification results
5. Finalize commit structure

## Pattern G: Architecture Impact Analysis

**Flow**: `Guardian ↔ Atlas`

**Purpose**: Assess architectural impact of cross-module changes.

```
┌──────────┐   Cross-Module Changes   ┌─────────┐   Impact Report   ┌──────────┐
│ Guardian │ ────────────────────────▶ │  Atlas  │ ────────────────▶ │ Guardian │
└──────────┘                          └─────────┘                   └──────────┘
     │         3+ modules affected         │          Dependencies        │
     │         New inter-module deps       │          Coupling analysis   │
     │         Shared module changes       │          Risk assessment     │
     └─────────────────────────────────────┴───────────────────────────────┘
                                   PR strategy adjusted
```

**Trigger Conditions**:
- Changes span 3+ distinct modules/packages
- New dependency between previously independent modules
- Core/shared module significantly modified
- Circular dependency risk detected

**Guardian Actions**:
1. Detect cross-module changes
2. Request Atlas impact analysis
3. Incorporate architectural concerns
4. Adjust PR strategy based on impact

## Bidirectional Collaboration Matrix

### Input Partners (→ Guardian)

| Partner | Input Type | Trigger | Handoff Format |
|---------|------------|---------|----------------|
| **Plan** | Implementation plan | Task planning complete | PLAN_TO_GUARDIAN_HANDOFF |
| **Builder** | Code changes | Before commit/PR | BUILDER_TO_GUARDIAN_HANDOFF |
| **Judge** | Review findings | Issues need restructuring | JUDGE_TO_GUARDIAN_HANDOFF |
| **Zen** | Refactoring diffs | Cleanup complete | ZEN_TO_GUARDIAN_HANDOFF |
| **Scout** | Technical context | Investigation complete | SCOUT_TO_GUARDIAN_HANDOFF |
| **Atlas** | Architecture impact | Analysis complete | ATLAS_TO_GUARDIAN_HANDOFF |

### Output Partners (Guardian →)

| Partner | Output Type | Trigger | Handoff Format |
|---------|-------------|---------|----------------|
| **Builder** | Commit structure | Strategy decided | GUARDIAN_TO_BUILDER_HANDOFF |
| **Judge** | Prepared PR | PR ready for review | GUARDIAN_TO_JUDGE_HANDOFF |
| **Canvas** | Visualization request | Dependency graph needed | GUARDIAN_TO_CANVAS_HANDOFF |
| **Sherpa** | Task breakdown | Large PR needs splitting | GUARDIAN_TO_SHERPA_HANDOFF |
| **Sentinel** | Security review request | CRITICAL/SENSITIVE changes | GUARDIAN_TO_SENTINEL_HANDOFF |
| **Probe** | DAST request | API/Auth changes detected | GUARDIAN_TO_PROBE_HANDOFF |
| **Atlas** | Architecture analysis | Cross-module changes | GUARDIAN_TO_ATLAS_HANDOFF |
| **Radar** | Test coverage request | Risk mitigation needed | GUARDIAN_TO_RADAR_HANDOFF |
| **Zen** | Hotspot refactoring | Tech debt cleanup needed | GUARDIAN_TO_ZEN_HANDOFF |
| **Nexus** | AUTORUN results | Chain execution | _STEP_COMPLETE format |

---

## Pattern H: Risk-Aware Review

**Flow**: `Guardian → Radar`

**Purpose**: Request test coverage for high-risk changes to mitigate regression risk.

```
┌──────────┐   High-Risk Files   ┌─────────┐   Test Coverage   ┌──────────┐
│ Guardian │ ──────────────────▶ │  Radar  │ ────────────────▶ │ Guardian │
└──────────┘                     └─────────┘                   └──────────┘
     │         Risk assessment        │          New tests          │
     │         Hotspot files          │          Coverage report    │
     │         Coverage gaps          │                             │
     └────────────────────────────────┴─────────────────────────────┘
                              Risk mitigated
```

**Trigger Conditions**:
- Risk score > 65 (HIGH)
- Hotspot files modified
- Coverage gap detected
- Regression history in affected files

**Guardian Actions**:
1. Identify high-risk files
2. Calculate coverage gaps
3. Request Radar test additions
4. Re-assess risk after coverage
5. Update PR recommendations

---

## Pattern I: Hotspot Refactoring

**Flow**: `Guardian → Zen`

**Purpose**: Proactively address technical debt in frequently changed files.

```
┌──────────┐   Hotspot Analysis   ┌─────────┐   Refactored Code  ┌──────────┐
│ Guardian │ ───────────────────▶ │   Zen   │ ─────────────────▶ │ Guardian │
└──────────┘                      └─────────┘                    └──────────┘
     │         Problem child files     │          Clean code          │
     │         Growing monsters        │          Separate commits    │
     │         Churn analysis          │                              │
     └─────────────────────────────────┴──────────────────────────────┘
                              Tech debt reduced
```

**Trigger Conditions**:
- Problem Child hotspot detected
- Growing Monster pattern found
- Churn rate > 50%
- Multiple bug fixes in file history

**Guardian Actions**:
1. Detect hotspot patterns
2. Analyze technical debt
3. Request Zen refactoring
4. Incorporate cleanup into PR strategy
5. Separate refactoring commits

---

## Pattern J: Quality Gate Flow

**Flow**: `Guardian ↔ Judge (Quality Gate)`

**Purpose**: Verify PR quality meets standards before review.

```
┌──────────┐    Quality Score    ┌─────────┐    Gate Result    ┌──────────┐
│ Guardian │ ──────────────────▶ │  Judge  │ ────────────────▶ │ Guardian │
└──────────┘                     └─────────┘                   └──────────┘
     │         Quality metrics        │          Pass/Fail          │
     │         Risk assessment        │          Improvements       │
     │         Commit analysis        │          needed             │
     └────────────────────────────────┴─────────────────────────────┘
                              Quality verified
```

**Trigger Conditions**:
- Quality score calculated
- Risk assessment complete
- Before PR creation

**Guardian Actions**:
1. Calculate quality score
2. Assess risk factors
3. Request Judge quality gate
4. Apply gate recommendations
5. Finalize PR strategy

---

## Pattern K: Reviewer Assignment

**Flow**: `Guardian → Harvest → Guardian`

**Purpose**: Recommend optimal reviewers based on code ownership.

```
┌──────────┐   Ownership Query   ┌─────────┐   Ownership Data   ┌──────────┐
│ Guardian │ ──────────────────▶ │ Harvest │ ────────────────▶ │ Guardian │
└──────────┘                     └─────────┘                   └──────────┘
     │         Changed files          │          Author history     │
     │         Module scope           │          Review patterns    │
     │                                │          Availability       │
     └────────────────────────────────┴─────────────────────────────┘
                              Reviewers recommended
```

**Trigger Conditions**:
- PR preparation complete
- Reviewer assignment needed
- Large or sensitive changes

**Guardian Actions**:
1. Identify changed files/modules
2. Query Harvest for ownership data
3. Calculate reviewer scores
4. Recommend primary/secondary reviewers
5. Include in PR preparation
