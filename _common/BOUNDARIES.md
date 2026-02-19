# Agent Boundaries (Master Reference)

Centralized responsibility boundaries for the entire agent ecosystem. Individual SKILL.md files reference this document instead of maintaining their own Agent Boundaries tables.

For disambiguation of commonly confused agent pairs, see `nexus/references/agent-disambiguation.md`.

---

## Meta-Orchestration

| Agent | Primary Role | Scope | Writes Code |
|-------|-------------|-------|-------------|
| **Nexus** | Task chain orchestration & execution | Single task chain | Never |
| **Titan** | Product lifecycle delivery (9 phases) | Full product (multi-phase) | Never |
| **Sherpa** | Task decomposition & workflow guidance | Single epic/story → atomic steps | Never |
| **Rally** | Parallel multi-session execution | Concurrent independent tasks | Never |
| **Darwin** | Ecosystem self-evolution | Cross-agent, systemic | Never |
| **Sigil** | Project-specific skill generation | Per-project lightweight skills | SKILL.md only |
| **Architect** | Ecosystem agent design | Permanent agent creation | SKILL.md only |

**Key distinctions:**
- Titan issues chains → Nexus executes them → Rally parallelizes when needed
- Sherpa decomposes → Nexus/Rally executes the decomposed steps
- Architect creates permanent ecosystem agents; Sigil creates project-specific skills

## Investigation & Analysis

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Scout** | Bug investigation & root cause analysis | "Why is it broken?" | Never |
| **Lens** | Codebase understanding & exploration | "How does it work?" | Never |
| **Rewind** | Git history investigation & regression analysis | "When did it break?" | Never |
| **Triage** | Incident response & recovery planning | "What's the severity? How to recover?" | Never |
| **Ripple** | Pre-change impact analysis | "What happens if we change X?" | Never |
| **Atlas** | Architecture analysis & ADR creation | "What IS the architecture?" | Never |
| **Sweep** | Dead code & unused file detection | "What can we remove?" | Never |

**Key distinctions:**
- Broken behavior → Scout. Understanding behavior → Lens. Git history → Rewind
- Current architecture → Atlas. Change impact → Ripple
- Incident severity → Triage. Bug root cause → Scout

## Security

| Agent | Primary Role | Method | Writes Code |
|-------|-------------|--------|-------------|
| **Sentinel** | Static security analysis | Code scan, CVE check, secret detection | Fixes only |
| **Probe** | Dynamic security testing | OWASP ZAP, penetration testing | Never |
| **Specter** | Concurrency & resource issue detection | Race conditions, memory/resource leaks | Never |

**Key distinctions:**
- Static code scan → Sentinel. Running app test → Probe. Concurrency → Specter

## Implementation

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Builder** | Production backend/logic implementation | Business logic, API, data models | Yes |
| **Artisan** | Production frontend implementation | React/Vue/Svelte, hooks, state | Yes |
| **Forge** | Rapid prototyping (full-stack) | Speed over quality, PoC | Yes |
| **Schema** | Database schema design & migration | Data modeling, normalization | Yes |
| **Anvil** | CLI/TUI development | Terminal interfaces, dev tools | Yes |
| **Arena** | Multi-engine competitive/collaborative development | Codex/Gemini comparison | Yes |

**Key distinctions:**
- Backend logic → Builder. Frontend → Artisan. Prototyping → Forge → then Artisan/Builder
- Clear requirements → Artisan directly. Exploration needed → Forge first

## Testing & Quality

| Agent | Primary Role | Scope | Writes Code |
|-------|-------------|-------|-------------|
| **Radar** | Unit/integration tests, edge cases, coverage | Test code | Yes |
| **Voyager** | E2E test specialist (Playwright/Cypress) | E2E test infrastructure | Yes |
| **Siege** | Load testing, chaos engineering, resilience | Non-functional testing | Yes |
| **Judge** | Code review & bug detection | PR review, quality check | Never |
| **Zen** | Refactoring & code smell remediation | Readability improvement | Yes (refactor only) |
| **Hone** | PDCA quality iteration cycle | Quality orchestration | Never |
| **Warden** | V.A.I.R.E. UX quality gate | Pre-release assessment | Never |

**Key distinctions:**
- Find problems → Judge. Fix code smells → Zen
- Unit tests → Radar. E2E tests → Voyager. Load tests → Siege

## Performance

| Agent | Primary Role | Layer | Writes Code |
|-------|-------------|-------|-------------|
| **Bolt** | Application-level performance | Frontend renders, backend N+1, caching | Yes |
| **Tuner** | Database query performance | EXPLAIN ANALYZE, indexes, query rewriting | Yes |

**Key distinctions:**
- App code slow → Bolt. Query slow → Tuner. Bolt may identify DB issues → hands off to Tuner

## Documentation

| Agent | Primary Role | Output Type | Writes Code |
|-------|-------------|------------|-------------|
| **Quill** | Code documentation | JSDoc/TSDoc, README, type definitions | Yes (docs/types) |
| **Scribe** | Specification documents | PRD, SRS, HLD, test specs | Never |
| **Canvas** | Visualization | Mermaid diagrams, ASCII art, draw.io | Yes (diagrams) |
| **Morph** | Format conversion | Markdown ↔ Word/Excel/PDF/HTML | Yes (scripts) |
| **Prism** | NotebookLM steering | Audio/Video quality prompts | Never |

**Key distinctions:**
- Code docs (JSDoc, README) → Quill. Spec docs (PRD, SRS) → Scribe. Diagrams → Canvas

## Architecture & Structure

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Atlas** | Architecture analysis & decisions | Dependencies, God Class, ADR/RFC | Never |
| **Gateway** | API design & review | OpenAPI, versioning, breaking changes | Yes (specs) |
| **Scaffold** | Infrastructure provisioning | Terraform, Docker, IaC | Yes |
| **Grove** | Repository structure design | Directory layout, conventions | Never |

## UX & Design

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Vision** | Creative direction & design strategy | Design system, redesign, trends | Never |
| **Muse** | Design token management | Color, spacing, typography tokens | Yes |
| **Palette** | Usability improvement | Cognitive load, a11y, interaction quality | Yes |
| **Flow** | Animation & motion | CSS/JS transitions, micro-interactions | Yes |
| **Echo** | Persona-based UI testing | Walk through as user type | Never |
| **Prose** | UX writing | Microcopy, error messages, voice & tone | Yes (text) |
| **Showcase** | Storybook catalog management | Component documentation, visual regression | Yes |
| **Trace** | Session replay analysis | Behavioral patterns from logs | Never |
| **Director** | Demo video production | Playwright-based recordings | Yes |
| **Reel** | Terminal recording | CLI demo GIF/video | Yes |

**Key distinctions:**
- Design direction → Vision. Tokens → Muse. Usability → Palette. Animation → Flow
- Write text → Prose. Test as persona → Echo. Research → Researcher

## User Research & Personas

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Researcher** | Research methodology design | Interviews, usability tests, journey maps | Never |
| **Cast** | Persona lifecycle management | Create, store, evolve, sync personas | Never |
| **Echo** | Persona-based UI simulation | Walk through UI as specific persona | Never |
| **Voice** | Feedback collection & analysis | NPS, reviews, sentiment analysis | Yes (integrations) |

**Key distinctions:**
- Manage personas → Cast. Simulate on UI → Echo. Design research → Researcher. Analyze feedback → Voice

## Strategy & Business

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Spark** | Feature ideation & proposal | New feature specs from existing data | Never |
| **Growth** | SEO/SMO/CRO optimization | Search ranking, conversion, sharing | Yes |
| **Compete** | Competitive intelligence | SWOT, positioning, feature matrix | Never |
| **Retain** | Retention & engagement | Churn prevention, gamification | Never |
| **Experiment** | A/B testing & hypothesis validation | Feature flags, statistical significance | Yes |
| **Pulse** | KPI & metrics infrastructure | Tracking events, dashboards | Yes |
| **Stream** | Data pipeline design | ETL/ELT, Kafka, Airflow, dbt | Yes |
| **Helm** | Business strategy simulation | SWOT/PESTLE, scenario planning | Never |
| **Compass** | Strategy execution monitoring | OKR cascade, drift detection | Never |

**Key distinctions:**
- Competitive intel → Compete. Business simulation → Helm. Compete feeds into Helm
- Feature ideas → Spark. Growth tactics → Growth. Metrics → Pulse

## Decision & Intent

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Magi** | Multi-perspective decision making | Logic/Empathy/Pragmatism triad | Never |
| **Bridge** | Business-tech translation | Requirement alignment, scope creep | Never |
| **Cipher** | Intent decoding | Ambiguity resolution, assumption surfacing | Never |
| **Refract** | Reframing & perspective shifting | Scale/stance/frame rotation | Never |

## DevOps & Release

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Gear** | Existing CI/CD maintenance | Dependencies, Docker, build optimization | Yes |
| **Pipe** | New GHA workflow design | Advanced GHA, reusable workflows | Yes |
| **Guardian** | Git/PR governance | Commit strategy, PR quality | Never |
| **Launch** | Release management | Versioning, CHANGELOG, rollback | Yes |
| **Harvest** | PR reporting | Weekly/monthly reports from git data | Never |
| **Latch** | Claude Code hooks | PreToolUse/PostToolUse event system | Yes |
| **Hearth** | Dev environment setup | dotfiles, shell, editor config | Yes |

**Key distinctions:**
- Existing CI maintenance → Gear. New GHA design → Pipe
- PR strategy → Guardian. Release execution → Launch. PR reports → Harvest

## Communication & Content

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Relay** | Messaging integration & bot development | WebSocket, webhooks, chat integrations | Yes |
| **Bard** | Developer voice & retrospective | Sprint retros, release commentary | Never |
| **Polyglot** | Internationalization (i18n/l10n) | Translations, locale formatting, RTL | Yes |

## Observability

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Beacon** | SRE & observability | SLO/SLI, tracing, alerting, dashboards | Yes |

## Specialized

| Agent | Primary Role | Focus | Writes Code |
|-------|-------------|-------|-------------|
| **Oracle** | AI/ML design & evaluation | Prompts, RAG, LLM patterns, MLOps | Never |
| **Aether** | AITuber system orchestration | Live streaming pipeline, TTS, avatar | Yes |
| **Navigator** | Browser automation | Playwright task execution | Yes |
| **Orbit** | Autonomous loop execution | Loop contracts, script generation | Yes |
| **Canon** | Standards compliance | OWASP, WCAG, OpenAPI, ISO 25010 | Never |
| **Matrix** | Combinatorial analysis | Multi-dimensional coverage optimization | Never |
| **Totem** | Cultural DNA profiling | Convention detection, drift monitoring | Never |
| **Void** | YAGNI verification | Scope cutting, complexity reduction | Never |
| **Sketch** | AI image generation | Gemini API image creation | Yes |
