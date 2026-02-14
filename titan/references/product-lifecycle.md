# Product Lifecycle — 9 Phases

```
DISCOVER → DEFINE → ARCHITECT → BUILD → HARDEN → VALIDATE → LAUNCH → GROW → EVOLVE
    ↑                                                                           │
    └───────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: DISCOVER

**Purpose**: Understand market, users, competitive landscape, existing codebase.
**Entry**: User provides product goal (may be vague) · **Exit**: Product Definition Document (users, value prop, features, constraints, SUCCESS_CRITERIA draft)

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

**Artifacts**: `docs/product-definition.md`, personas, competitive analysis · Agent details → `references/agent-deployment-matrix.md` · Exit validation → `references/exit-criteria-validation.md`

---

## Phase 2: DEFINE

**Purpose**: Create roadmap, feature specs, measurable success criteria.
**Entry**: Product Definition from DISCOVER · **Exit**: Roadmap + Feature Specs + KPIs + SUCCESS_CRITERIA finalized

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

**Artifacts**: `docs/roadmap.md`, `docs/specs/`, KPI definitions, success criteria · Agent details → `references/agent-deployment-matrix.md` · Exit validation → `references/exit-criteria-validation.md`

---

## Phase 3: ARCHITECT

**Purpose**: Technical design, system architecture, structural decisions.
**Entry**: Feature specs + technical constraints · **Exit**: ADR, API specs, DB schema, repo structure, infra plan

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

**Artifacts**: `docs/adr/`, `docs/api-spec.yaml`, DB schema, architecture diagrams · Agent details → `references/agent-deployment-matrix.md` · Exit validation → `references/exit-criteria-validation.md`

---

## Phase 4: BUILD

**Purpose**: Full implementation with maximum parallelization.
**Entry**: Architecture + feature specs · **Exit**: Working product (all features, basic tests passing)

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

**Artifacts**: Source code, test files, `docs/build-notes.md` · Agent details → `references/agent-deployment-matrix.md` · Exit validation → `references/exit-criteria-validation.md`

---

## Phase 5: HARDEN

**Purpose**: Security audit, code quality, performance optimization.
**Entry**: Working product, basic tests passing · **Exit**: Hardened product (security PASS, perf targets MET, quality APPROVED)

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

1. **Test Parallel** (Rally): Voyager (E2E) + Radar (unit/integration)
2. **UX Validation** (Echo): Persona-based usability testing
3. **Session Analysis** (Trace): Behavioral pattern analysis
4. **Experiment Setup** (Experiment): A/B test configuration
5. **Quality Gate** (Warden): Validation assessment
6. **Browser Automation** (Navigator): Automated browser checks

Agent details → `references/agent-deployment-matrix.md` · Exit validation → `references/exit-criteria-validation.md`

---

## Phase 7: LAUNCH

**Purpose**: Release preparation, documentation, deployment.
**Entry**: Validated product · **Exit**: Released product (deployed, documented, demos created)

1. **Code Documentation** (Quill): JSDoc/TSDoc, README
2. **Architecture Diagrams** (Canvas): Final system diagrams
3. **Format Conversion** (Morph): Docs to PDF/HTML if needed
4. **PR Strategy** (Guardian): Commit structure, PR preparation
5. **Release Management** (Launch): Versioning, CHANGELOG, release notes
6. **Demo Parallel** (Rally): Showcase (Storybook) + Director (web demos) + Reel (CLI demos)
7. **CI/CD Setup** (Gear): Pipeline configuration
8. **Content Optimization** (Prism): NotebookLM prompts if applicable

Agent details → `references/agent-deployment-matrix.md` · Exit validation → `references/exit-criteria-validation.md`

---

## Phase 8: GROW

**Purpose**: SEO, growth features, retention strategies.
**Entry**: Released product · **Exit**: Growing product (SEO optimized, retention features, analytics live)

1. **SEO/CRO** (Growth): Meta tags, OGP, structured data, conversion optimization
2. **Retention** (Retain): Re-engagement triggers, gamification, habit loops
3. **Internationalization** (Polyglot): i18n if multi-language needed
4. **Metrics Implementation** (Pulse): Tracking events, dashboard setup
5. **Data Pipeline** (Stream): Analytics data flow
6. **Experimentation** (Experiment): Growth experiments

Agent details → `references/agent-deployment-matrix.md` · Exit validation → `references/exit-criteria-validation.md`

---

## Phase 9: EVOLVE

**Purpose**: Feedback-driven improvement, modernization cycle.
**Entry**: Metrics data + user feedback · **Exit**: Next iteration input → feeds back to DISCOVER

1. **Feedback Collection** (Voice): Feedback analysis, sentiment extraction
2. **Impact Analysis** (Ripple): Assess proposed changes
3. **Code Cleanup** (Sweep): Dead code removal, unused file detection
4. **Modernization** (Horizon): Library updates, deprecated API replacement
5. **CI/CD Improvement** (Gear): Pipeline optimization
6. **History Analysis** (Rewind): Regression investigation, code archaeology
7. **Narrative** (Bard): Project storytelling, sprint retrospectives
8. **Ecosystem Improvement** (Architect): Agent gap analysis, new agent proposals

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

Harden and Validate can partially overlap: E2E test writing can begin while performance optimization is in progress, as long as security audit is complete.
