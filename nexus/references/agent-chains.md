# Nexus Agent Chain Templates Reference

Complete chain templates and dynamic adjustment rules.

---

## Chain Templates by Task Type

| Type | Complexity | Chain Template |
|------|------------|----------------|
| BUG | simple | Scout → Lens → Builder → Radar |
| BUG | complex | Scout → Lens → Sherpa → Builder → Radar → Sentinel |
| INCIDENT | SEV1/2 | Triage → Scout → Builder → Radar → Triage (postmortem) |
| INCIDENT | SEV3/4 | Triage → Scout → Builder → Radar |
| API | new | Gateway → Builder → Radar → Quill |
| API | change | Gateway → Builder → Radar |
| FEATURE | S | Builder → Radar |
| FEATURE | M | Sherpa → Forge → Builder → Radar |
| FEATURE | L | Spark → Sherpa → Forge → Builder → Radar → Quill |
| FEATURE | UI | Spark → Forge → Muse → Builder → Lens → Radar |
| FEATURE | UX | Researcher → Echo → Spark → Builder → Radar |
| REFACTOR | small | Zen → Radar |
| REFACTOR | arch | Atlas → Sherpa → Zen → Radar |
| OPTIMIZE | app | Bolt → Radar |
| OPTIMIZE | db | Tuner → Schema → Builder → Radar |
| SECURITY | static | Sentinel → Builder → Radar → Sentinel |
| SECURITY | dynamic | Sentinel → Probe → Builder → Radar → Probe |
| SECURITY | full | Sentinel → Probe → Builder → Radar → Sentinel → Probe |
| INVESTIGATE | feature | Lens |
| INVESTIGATE | flow | Lens → Canvas |
| INVESTIGATE | onboarding | Lens → Scribe |
| INVESTIGATE | pre-impl | Lens → Builder → Radar |
| DOCS | - | Quill |
| INFRA | cloud | Scaffold → Gear → Radar |
| INFRA | local | Scaffold → Radar |
| QA | - | Lens → Echo → Radar |
| QA | e2e | Voyager → Lens → Radar |
| REVIEW | PR | Judge → Builder/Zen/Sentinel (based on findings) → Radar |
| REVIEW | pre-commit | Judge → Builder (if CRITICAL) |
| UX_RESEARCH | - | Researcher → Echo → Palette |
| DB_DESIGN | new | Schema → Builder → Radar |
| DB_DESIGN | optimize | Schema → Tuner → Builder → Radar |
| E2E | new | Voyager → Lens |
| E2E | ci | Voyager → Gear |
| COMPARE | quality-critical | Sherpa → Arena → Guardian |
| COMPARE | bug-fix | Scout → Arena → Radar |
| COMPARE | feature | Spark → Arena → Guardian |
| COMPARE | security | Arena → Sentinel → Arena (iterate) |
| BROWSER | data-collection | Navigator → Builder |
| BROWSER | bug-reproduction | Scout → Navigator → Triage |
| BROWSER | evidence | Navigator → Lens → Canvas |
| BROWSER | performance | Navigator → Bolt |
| DECISION | architecture | Magi → Builder/Zen (based on verdict) |
| DECISION | strategy | Bridge → Magi → Spark |
| DECISION | intent | Cipher → Forge/Builder |
| ANALYSIS | impact | Ripple → Builder → Radar |
| ANALYSIS | standards | Canon → Builder → Radar |
| ANALYSIS | cleanup | Sweep → Zen → Radar |
| DEPLOY | release | Guardian → Launch |
| DEPLOY | full | Radar → Guardian → Launch → Harvest |
| MODERNIZE | stack | Lens → Horizon → Sherpa → Builder → Radar |
| MODERNIZE | i18n | Polyglot → Artisan → Radar |
| MODERNIZE | structure | Grove → Sherpa → Zen → Radar |
| UX_DESIGN | flow | Flow → Artisan → Radar |
| UX_DESIGN | creative | Vision → Muse → Forge → Artisan → Radar |
| UX_DESIGN | audit | Warden → Palette → Artisan → Radar |
| UX_DESIGN | storybook | Showcase → Quill |
| UX_DESIGN | demo | Director → Voyager |
| UX_DESIGN | session | Trace → Echo → Palette |
| FEATURE | frontend | Forge → Artisan → Radar |
| FEATURE | cli | Anvil → Radar |
| TEST | quality | Hone (iterative PDCA) |
| INVESTIGATE | regression | Rewind → Scout → Builder → Radar |
| SECURITY | concurrency | Specter → Builder → Radar |
| DOCS | convert | Morph |
| DOCS | report | Harvest → Morph |
| STRATEGY | seo | Growth → Artisan → Radar |
| STRATEGY | compete | Compete → Spark → Builder → Radar |
| STRATEGY | feedback | Voice → Spark → Builder → Radar |
| STRATEGY | metrics | Pulse → Builder → Radar |
| STRATEGY | retention | Retain → Spark → Builder → Radar |
| STRATEGY | ab-test | Experiment → Builder → Radar |
| STRATEGY | data-pipeline | Stream → Schema → Builder → Radar |
| QUALITY | quick | Hone(Judge, Zen, Radar) → Canvas |
| QUALITY | standard | Hone(Judge, Zen, Radar, Sentinel) → Canvas |
| QUALITY | full | Hone(Judge, Zen, Radar, Sentinel, Atlas, Sweep) → Canvas |

---

## Forge → Builder Integration

When using Forge → Builder chains, Forge MUST output:
- `types.ts` → Builder converts to Value Objects
- `errors.ts` → Builder converts to DomainError classes
- `forge-insights.md` → Builder uses as business rules reference

Builder then applies:
1. **Clarify Phase**: Parse Forge outputs, detect ambiguities
2. **Design Phase**: TDD (test skeleton first), domain model design
3. **Build Phase**: Type-safe implementation with Event Sourcing/CQRS if needed
4. **Validate Phase**: Performance optimization, error handling verification

---

## Dynamic Chain Adjustment Rules

### Addition Triggers

- 3 consecutive test failures → Re-decompose with Sherpa
- Security-related code changes → Add Sentinel
- Security needs runtime validation → Add Probe after Sentinel
- UI changes included → Consider Muse/Palette
- UX assumptions need validation → Add Researcher before Echo
- Code changes exceed 50 lines → Consider refactoring with Zen
- Type errors occur → Return to Builder to strengthen type definitions
- Database queries slow (>100ms) → Add Tuner
- New tables/schemas needed → Add Schema before Builder
- Critical user flow changes → Add Voyager for E2E coverage
- Multi-page feature implementation → Add Voyager
- Builder detects ON_AMBIGUOUS_SPEC → Escalate to user or return to Spark
- Complex distributed workflow → Builder activates Event Sourcing/Saga patterns
- High read/write ratio disparity → Builder applies CQRS pattern

### Rally Parallel Escalation Triggers

- Chain has 2+ independent implementation steps → Escalate to Rally for parallel execution
- Sherpa decomposition produces `parallel_group` → Delegate to Rally via SHERPA_TO_RALLY_HANDOFF
- Feature scope spans 4+ files across 2+ domains (frontend/backend/DB) → Rally with Frontend/Backend Split
- Chain includes both Artisan and Builder implementation → Rally with Frontend/Backend Split
- 3+ independent bug fixes needed → Rally with Feature Parallel
- Implementation + test + docs needed simultaneously → Rally with Code/Test/Docs Triple
- Multi-module refactoring identified → Rally with Feature Parallel after Atlas/Sherpa

### Rally Non-Escalation (Keep Sequential)

- Investigation-only chains (Lens, Scout, Rewind) → No Rally
- Single-agent chains (Quill, Morph, Hone single cycle) → No Rally
- Changes under 10 lines total → No Rally
- High-risk security changes → Prefer sequential with checkpoints
- Each branch needs < 50 lines of code → Nexus _PARALLEL_BRANCHES sufficient

### Skip Triggers

- Changes under 10 lines AND tests exist → May skip Radar
- Pure documentation changes → Skip Radar/Sentinel
- Config files only → Only relevant agent
- Sentinel-only static issues → May skip Probe
- Schema unchanged → May skip Tuner

---

## Rally Parallel Chain Variants

When Rally is activated for parallel execution, standard chains transform into parallel variants.

### FEATURE Parallel Chains

| Base Chain | Rally Parallel Chain | Team Pattern |
|------------|---------------------|--------------|
| FEATURE/L | Spark → Sherpa → Rally(Forge+Artisan, Builder, Radar) | Frontend/Backend Split |
| FEATURE/M (multi-unit) | Sherpa → Rally(Builder×N, Radar) | Feature Parallel |
| FEATURE/fullstack | Rally(Artisan, Builder, Radar) | Frontend/Backend Split |

### BUG Parallel Chains

| Base Chain | Rally Parallel Chain | Team Pattern |
|------------|---------------------|--------------|
| BUG/multiple | Rally(Builder×N) → Radar | Feature Parallel |

### REFACTOR Parallel Chains

| Base Chain | Rally Parallel Chain | Team Pattern |
|------------|---------------------|--------------|
| REFACTOR/arch (multi-module) | Atlas → Sherpa → Rally(Zen×N) → Radar | Feature Parallel |

### TEST Parallel Chains

| Base Chain | Rally Parallel Chain | Team Pattern |
|------------|---------------------|--------------|
| TEST/coverage | Rally(Radar, Voyager) | Specialist Team |

### SECURITY Parallel Chains

| Base Chain | Rally Parallel Chain | Team Pattern |
|------------|---------------------|--------------|
| SECURITY/full | Rally(Sentinel, Probe) → Builder → Radar | Specialist Team |

### DOCS Parallel Chains

| Base Chain | Rally Parallel Chain | Team Pattern |
|------------|---------------------|--------------|
| DOCS/full | Rally(Quill, Canvas, Showcase) | Specialist Team |

### MODERNIZE Parallel Chains

| Base Chain | Rally Parallel Chain | Team Pattern |
|------------|---------------------|--------------|
| MODERNIZE/stack | Lens → Horizon → Sherpa → Rally(Builder×N) → Radar | Feature Parallel |

See `rally/references/integration-patterns.md` for detailed team composition and handoff formats.
