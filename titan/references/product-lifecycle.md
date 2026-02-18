# Product Lifecycle — 9 Phases

```
DISCOVER → DEFINE → ARCHITECT → BUILD → HARDEN → VALIDATE → LAUNCH → GROW → EVOLVE
    ↑                                                                           │
    └───────────────────────────────────────────────────────────────────────────┘
```

**CRITICAL — Scope-First Rule**: Before reading phase details, determine scope (S/M/L/XL). Use the scope-adaptive chain for each phase. S/M scopes skip most phases and produce NO standalone document files.

---

## Scope-Adaptive Quick Reference

| Scope | DISCOVER | DEFINE | ARCHITECT | BUILD | HARDEN | VALIDATE | LAUNCH | GROW | EVOLVE |
|-------|----------|--------|-----------|-------|--------|----------|--------|------|--------|
| **S** | Cipher (inline) | SKIP | SKIP | Forge→Builder→Radar | SKIP | Radar | SKIP | SKIP | SKIP |
| **M** | Cipher→Lens | SKIP | SKIP | Sherpa→Builder→Radar | Sentinel→Radar | Radar | SKIP | SKIP | SKIP |
| **L** | Cipher→Lens→Bridge | Spark→Scribe | Magi→Atlas→Schema→Grove | Sherpa→Rally→Radar | Full | Full | Full | SKIP | SKIP |
| **XL** | Full 8-agent | Full 6-agent | Full 7-agent | Full Rally | Full | Full | Full | Full | Full |

**"SKIP" means the phase is entirely omitted — no agents deployed, no artifacts created, no exit validation.**

---

## Phase 1: DISCOVER

**Purpose**: Understand intent and existing codebase. Scale effort to scope.
**Entry**: User provides product goal (may be vague) · **Exit**: Clear understanding of what to build (format varies by scope)

### Scope-Adaptive Chains

**S scope** — Cipher only (intent decode inline, NO document files):
```
NEXUS_AUTORUN_FULL — Chain: Cipher
Task: Decode user intent into precise implementation spec
Acceptance: Clear feature list and constraints (recorded in TITAN_STATE, NOT as separate files)
```

**M scope** — Cipher + Lens (add codebase understanding):
```
NEXUS_AUTORUN_FULL — Chain: Cipher → Lens
Task: Decode intent and understand existing codebase for integration
Acceptance: Implementation plan with integration points (recorded in TITAN_STATE)
```

**L scope** — Add business alignment:
```
NEXUS_AUTORUN_FULL — Chain: Cipher → Lens → Bridge
Acceptance: Product definition with features, constraints, integration points → `docs/product-definition.md`
```

**XL scope** — Full discovery (only scope that warrants full research):

1. **Intent Decoding** (Cipher): Analyze goal, resolve ambiguities → precise spec
2. **Business-Tech Alignment** (Bridge): Business requirements → technical constraints
3. **User Research** (Researcher): Target personas, journey maps
4. **Competitive Analysis** (Compete): SWOT, feature comparison matrix
5. **Feedback Integration** (Voice): Existing user feedback analysis
6. **Codebase Comprehension** (Lens): Existing code understanding
7. **Issue Investigation** (Scout): Existing bugs/issues review
8. **Incident Review** (Triage): Past incidents for reliability context

```
NEXUS_AUTORUN_FULL — Chain: Cipher → Bridge → Researcher → Compete → Voice → Lens
Acceptance: Product Definition with target users, value proposition, key features, constraints
```

**Artifacts by scope**: S/M: TITAN_STATE only (NO files) · L: `docs/product-definition.md` · XL: + personas, competitive analysis

### SCOPE_RECHECK Epic (Conditional)

Triggered when scope detection confidence is 0.40-0.59. Inserted into DISCOVER phase to refine scope before proceeding.

```
NEXUS_AUTORUN_FULL — Chain: Lens → Cipher → Bridge
Task: Re-evaluate project scope with DISCOVER artifacts
Context: Initial scope confidence was [X]. Re-assess with product definition, personas, and codebase analysis now available.
Acceptance: Updated scope (S/M/L/XL) with confidence ≥0.60, documented rationale
```

**Trigger rules:**
- `confidence 0.50-0.59`: Schedule SCOPE_RECHECK as final DISCOVER Epic (after main chain)
- `confidence 0.40-0.49`: Schedule SCOPE_RECHECK as first DISCOVER Epic (before main chain)
- `confidence <0.40`: Fire ON_AMBIGUOUS_GOAL trigger instead (user input required)

---

## Phase 2: DEFINE

**Purpose**: Create roadmap, feature specs, measurable success criteria.
**Entry**: Product Definition from DISCOVER · **Exit**: Roadmap + Feature Specs + KPIs + SUCCESS_CRITERIA finalized

### Scope-Adaptive Chains

**S scope** — SKIP entirely. No roadmap or specs needed. Intent from Cipher goes straight to BUILD.

**M scope** — SKIP entirely. Implementation plan from TITAN_STATE is sufficient. No separate spec documents.

**L scope** — Lightweight definition:
```
NEXUS_AUTORUN_FULL — Chain: Spark → Scribe
Task: Generate feature specs and roadmap from product definition
Acceptance: Roadmap with prioritized features, SUCCESS_CRITERIA defined → `docs/roadmap.md`
```

**XL scope** — Full definition with KPIs, standards, impact analysis:

1. **Feature Proposals** (Spark): Generate feature specs from product definition
2. **Specification Writing** (Scribe): Formalize into PRD/SRS documents
3. **KPI Design** (Pulse): Define tracking events and success metrics
4. **Decision Making** (Magi): Evaluate priorities, Go/No-Go decisions
5. **Standards Compliance** (Canon): Specs meet industry standards
6. **Impact Analysis** (Ripple): Implementation impact and risks

```
NEXUS_AUTORUN_FULL — Chain: Spark → Scribe → Pulse → Magi → Canon
Acceptance: Complete roadmap with prioritized features, KPI definitions, SUCCESS_CRITERIA finalized
```

**Artifacts by scope**: S/M: SKIP (no artifacts) · L: `docs/roadmap.md` · XL: + `docs/specs/`, KPI definitions

---

## Phase 3: ARCHITECT

**Purpose**: Technical design, system architecture, structural decisions.
**Entry**: Feature specs + technical constraints · **Exit**: ADR, API specs, DB schema, repo structure, infra plan

### Scope-Adaptive Chains

**S scope** — SKIP entirely. Builder decides architecture inline during BUILD.

**M scope** — SKIP entirely. Builder makes architectural decisions during implementation. If complex decisions arise, Magi is invoked ad-hoc from BUILD.

**L scope** — Core architecture only (no infrastructure planning):
```
NEXUS_AUTORUN_FULL — Chain: Magi → Atlas → Schema → Grove
Task: Design core architecture, data model, and repository structure
Acceptance: ADR for key decisions, DB schema, repo structure defined
```

**XL scope** — Full architecture with infrastructure planning:

1. **Architecture Decisions** (Magi): Multi-perspective evaluation of options
2. **Dependency Analysis** (Atlas): Map dependencies, detect circular references
3. **API Design** (Gateway): REST/GraphQL endpoints, OpenAPI spec
4. **Database Design** (Schema): ER diagrams, migrations, data model
5. **Repository Structure** (Grove): Directory layout, module organization
6. **Infrastructure Design** (Scaffold): Cloud/local infrastructure planning
7. **Visualization** (Canvas): Architecture diagrams

```
NEXUS_AUTORUN_FULL — Chain: Magi → Atlas → Gateway → Schema → Grove → Scaffold → Canvas
Acceptance: ADR, API specs, DB schema, repo structure, infrastructure plan
```

**Artifacts by scope**: S/M: SKIP (no artifacts) · L: ADR, DB schema, repo structure · XL: + `docs/api-spec.yaml`, architecture diagrams, infra plan

---

## Phase 4: BUILD

**Purpose**: Full implementation with maximum parallelization. **This is the core phase — all scopes execute BUILD.**
**Entry**: Intent (S/M) or Architecture (L/XL) · **Exit**: Working product (all features, basic tests passing)

### Scope-Adaptive Chains

**S scope** — Direct build with prototype-first approach:
```
NEXUS_AUTORUN_FULL — Chain: Forge → Builder → Radar
Task: Build [feature] with tests
Context: [Cipher intent from DISCOVER, inline in TITAN_STATE]
Acceptance: Working implementation with passing tests
```

**M scope** — Task decomposition then build:
```
NEXUS_AUTORUN_FULL — Chain: Sherpa → Builder → Radar
Task: Decompose and implement [features] with tests
Context: [Cipher+Lens output from DISCOVER, inline in TITAN_STATE]
Acceptance: All features implemented, tests passing, basic coverage ≥60%
```

**L scope** — Parallel feature streams:
```
NEXUS_AUTORUN_FULL — Chain: Sherpa → Rally → Radar
Rally: Team{ Feature A: Builder→Radar | Feature B: Artisan→Radar | ... }
Task: Parallel implementation of all roadmap features
Context: Architecture from ARCHITECT phase, specs from DEFINE
Acceptance: All features implemented, integration tests passing
```

**XL scope** — Full parallel orchestration with prototyping and competitive implementations:

1. **Task Decomposition** (Sherpa): Break features into atomic steps
2. **Parallel Orchestration** (Rally): Concurrent implementation streams
3. **Prototyping** (Forge): Rapid prototypes for complex features
4. **Production Backend** (Builder): Type-safe backend implementation
5. **Production Frontend** (Artisan): React/Vue/Svelte frontend
6. **CLI Tools** (Anvil): Command-line interface if applicable
7. **Multi-Implementation** (Arena): Competitive implementations for critical components
8. **Data Pipelines** (Stream): ETL/ELT pipeline implementation

```
NEXUS_AUTORUN_FULL — Chain: Sherpa → Forge → Builder → Radar (per feature)
Rally: Team{ Feature A: Sherpa→Forge→Builder→Radar | Feature B: Sherpa→Artisan→Radar | ... }
```

**Artifacts by scope**: All scopes: source code + test files · L/XL: + `docs/build-notes.md`

---

## Phase 5: HARDEN

**Purpose**: Security audit, code quality, performance optimization.
**Entry**: Working product, basic tests passing · **Exit**: Hardened product (security PASS, perf targets MET, quality APPROVED)

### Scope-Adaptive Chains

**S scope** — SKIP entirely. Radar in BUILD provides sufficient validation for small tools.

**M scope** — Lightweight security + test hardening:
```
NEXUS_AUTORUN_FULL — Chain: Sentinel → Radar
Task: Security scan and test coverage improvement
Acceptance: No critical security issues, test coverage ≥70%
```

**L scope** — Security + quality + performance:
```
NEXUS_AUTORUN_FULL — Chain: Rally{Sentinel+Probe} → Judge → Zen → Bolt → Warden
Acceptance: Security audit passed, code quality ≥B, performance targets met
```

**XL scope** — Full hardening with concurrency testing and PDCA cycles:

1. **Security Parallel** (Rally): Sentinel (SAST) + Probe (DAST) + Specter (concurrency)
2. **Code Quality** (Judge → Zen): Review then refactoring
3. **Performance Parallel** (Rally): Bolt (app perf) + Tuner (DB perf)
4. **Quality Cycles** (Hone): PDCA improvement iterations
5. **Quality Gate** (Warden): Final quality assessment
6. **Standards Check** (Canon): Compliance verification

```
NEXUS_AUTORUN_FULL — Chain: Rally{Sentinel+Probe+Specter} → Judge → Zen → Rally{Bolt+Tuner} → Hone → Canon → Warden
```

Agent details → `references/agent-deployment-matrix.md` · Exit validation → `references/exit-criteria-validation.md`

---

## Phase 6: VALIDATE

**Purpose**: E2E testing, UX verification, experiment setup.
**Entry**: Hardened product · **Exit**: Validated product (E2E green, UX approved, experiments configured)

### Scope-Adaptive Chains

**S scope** — Radar only (already included in BUILD chain, acts as validation):
```
NEXUS_AUTORUN_FULL — Chain: Radar
Task: Final test validation — ensure all tests pass and coverage is adequate
Acceptance: All tests green, no regressions
```

**M scope** — Radar with broader test coverage:
```
NEXUS_AUTORUN_FULL — Chain: Radar
Task: Comprehensive test validation — unit, integration, edge cases
Acceptance: All tests green, coverage ≥70%, edge cases covered
```

**L scope** — E2E + UX validation:
```
NEXUS_AUTORUN_FULL — Chain: Rally{Voyager+Radar} → Echo → Warden
Acceptance: E2E tests passing, UX validated by persona review, quality gate approved
```

**XL scope** — Full validation with experiments and behavioral analysis:

1. **Test Parallel** (Rally): Voyager (E2E) + Radar (unit/integration)
2. **UX Validation** (Echo): Persona-based usability testing
3. **Session Analysis** (Trace): Behavioral pattern analysis
4. **Experiment Setup** (Experiment): A/B test configuration
5. **Quality Gate** (Warden): Validation assessment
6. **Browser Automation** (Navigator): Automated browser checks

```
NEXUS_AUTORUN_FULL — Chain: Rally{Voyager+Radar} → Echo → Trace → Experiment → Navigator → Warden
```

Agent details → `references/agent-deployment-matrix.md` · Exit validation → `references/exit-criteria-validation.md`

---

## Phase 7: LAUNCH

**Purpose**: Release preparation, documentation, deployment.
**Entry**: Validated product · **Exit**: Released product (deployed, documented, demos created)

### Scope-Adaptive Chains

**S scope** — SKIP entirely. Small tools ship via commit/PR directly from BUILD.

**M scope** — SKIP entirely. Guardian handles PR strategy inline if needed.

**L scope** — Documentation + release management:
```
NEXUS_AUTORUN_FULL — Chain: Quill → Guardian → Launch → Gear
Task: Prepare release — documentation, PR, versioning, CI/CD
Acceptance: README updated, PR created, CHANGELOG written, CI pipeline configured
```

**XL scope** — Full launch with demos and architecture diagrams:

1. **Code Documentation** (Quill): JSDoc/TSDoc, README
2. **Architecture Diagrams** (Canvas): Final system diagrams
3. **Format Conversion** (Morph): Docs to PDF/HTML if needed
4. **PR Strategy** (Guardian): Commit structure, PR preparation
5. **Release Management** (Launch): Versioning, CHANGELOG, release notes
6. **Demo Parallel** (Rally): Showcase (Storybook) + Director (web demos) + Reel (CLI demos)
7. **CI/CD Setup** (Gear): Pipeline configuration
8. **Content Optimization** (Prism): NotebookLM prompts if applicable

```
NEXUS_AUTORUN_FULL — Chain: Quill → Canvas → Guardian → Launch → Rally{Showcase+Director+Reel} → Gear
```

Agent details → `references/agent-deployment-matrix.md` · Exit validation → `references/exit-criteria-validation.md`

---

## Phase 8: GROW

**Purpose**: SEO, growth features, retention strategies.
**Entry**: Released product · **Exit**: Growing product (SEO optimized, retention features, analytics live)

### Scope-Adaptive Chains

**S scope** — SKIP entirely. Small tools don't need growth optimization.

**M scope** — SKIP entirely. Growth is premature for medium features.

**L scope** — SKIP entirely. Growth phase is reserved for XL projects that need user acquisition and retention strategies.

**XL scope** — Full growth optimization:

1. **SEO/CRO** (Growth): Meta tags, OGP, structured data, conversion optimization
2. **Retention** (Retain): Re-engagement triggers, gamification, habit loops
3. **Internationalization** (Polyglot): i18n if multi-language needed
4. **Metrics Implementation** (Pulse): Tracking events, dashboard setup
5. **Data Pipeline** (Stream): Analytics data flow
6. **Experimentation** (Experiment): Growth experiments

```
NEXUS_AUTORUN_FULL — Chain: Growth → Retain → Pulse → Stream → Experiment
```

Agent details → `references/agent-deployment-matrix.md` · Exit validation → `references/exit-criteria-validation.md`

---

## Phase 9: EVOLVE

**Purpose**: Feedback-driven improvement, modernization cycle.
**Entry**: Metrics data + user feedback · **Exit**: Next iteration input → feeds back to DISCOVER

### Scope-Adaptive Chains

**S scope** — SKIP entirely. Small tools iterate via new `/Titan` invocations, not formal evolution cycles.

**M scope** — SKIP entirely. Improvements are handled as new tasks, not formal evolution.

**L scope** — SKIP entirely. Evolution is reserved for XL projects with active user bases and metrics.

**XL scope** — Full evolution cycle:

1. **Feedback Collection** (Voice): Feedback analysis, sentiment extraction
2. **Impact Analysis** (Ripple): Assess proposed changes
3. **Code Cleanup** (Sweep): Dead code removal, unused file detection
4. **Modernization** (Horizon): Library updates, deprecated API replacement
5. **CI/CD Improvement** (Gear): Pipeline optimization
6. **History Analysis** (Rewind): Regression investigation, code archaeology
7. **Narrative** (Bard): Project storytelling, sprint retrospectives
8. **Ecosystem Improvement** (Architect): Agent gap analysis, new agent proposals

```
NEXUS_AUTORUN_FULL — Chain: Voice → Ripple → Sweep → Horizon → Gear → Rewind
```

**Continuous Loop**: Feedback → updated personas · Metrics → refined criteria · Tech debt → arch improvements · Market changes → competitive re-analysis.

Agent details → `references/agent-deployment-matrix.md` · Exit validation → `references/exit-criteria-validation.md`

---

## Phase Dependency Graph

```
DISCOVER → DEFINE → ARCHITECT → BUILD → HARDEN → VALIDATE → LAUNCH → GROW → EVOLVE
                                   │                 │                          │
                                   └─ can overlap ───┘                         ↓
                                     (Harden + early Validate)        DISCOVER (next cycle)
```

---

## Phase Overlap Rules

For L/XL projects, adjacent phases can partially overlap to improve efficiency. Overlap is governed by strict rules to prevent quality degradation.

### Permitted Overlaps

| Current Phase | Overlap Phase | Condition | Allowed Overlap Work |
|--------------|--------------|-----------|---------------------|
| BUILD (>70% complete) | HARDEN | Core features implemented, tests green | Security scanning (Sentinel/Probe) |
| HARDEN (security done) | VALIDATE | Security audit passed, no critical issues | E2E test writing (Voyager) |
| VALIDATE | LAUNCH | E2E tests passing, UX approved | Documentation (Quill), CI/CD setup (Gear) |
| GROW | EVOLVE | Growth features deployed, analytics active | Feedback collection (Voice) |

### Prohibited Overlaps

| Overlap | Reason |
|---------|--------|
| DISCOVER ↔ BUILD | Building without validated requirements risks total rework |
| DISCOVER ↔ ARCHITECT | Architecture before requirements are stable is wasteful |
| DEFINE ↔ BUILD | Specs must be finalized before implementation |
| BUILD ↔ LAUNCH | Deploying incomplete product is dangerous |
| HARDEN ↔ LAUNCH | Security/quality must pass before release |

### Overlap Governance

1. **Current phase exit criteria take priority** — overlap work MUST NOT delay current phase completion
2. **Rally file ownership applies** — overlap work uses standard file ownership declarations (no write conflicts)
3. **Overlap work is tentative** — if current phase exit criteria fail, overlap work may be discarded
4. **S/M scope: no overlap** — sequential execution only (overhead of overlap coordination exceeds benefit)
5. **State tracking** — TITAN_STATE records overlap status: `overlap: [PHASE_A]+[PHASE_B_subset]`
