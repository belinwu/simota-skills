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

### Skip Triggers

- Changes under 10 lines AND tests exist → May skip Radar
- Pure documentation changes → Skip Radar/Sentinel
- Config files only → Only relevant agent
- Sentinel-only static issues → May skip Probe
- Schema unchanged → May skip Tuner
