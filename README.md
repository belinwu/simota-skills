# AI Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Agents](https://img.shields.io/badge/Agents-71-blue.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A skill collection that enables collaborative development with a team of specialized AI agents.

## Features

- **71 Specialized Agents** - Covering bug investigation, testing, security, UI/UX, infrastructure, and more
- **Nexus Orchestrator** - Analyzes tasks and automatically designs optimal agent chains
- **Platform Agnostic** - Works with Claude Code, Codex CLI, Gemini CLI, and others

## Quick Start

### Installation

```bash
# For Claude Code
git clone https://github.com/simota/agent-skills.git ~/.claude/skills

# For other platforms
git clone https://github.com/simota/agent-skills.git /path/to/your/skills
```

### Usage

```
/Nexus I want to implement a login feature
/Scout Investigate the cause of this bug
/Radar Improve test coverage
/Vision I want to redesign the dashboard with a modern look
```

## Overview

This repository contains 71 specialized AI agents covering various aspects of software development. Each agent specializes in a specific domain and is coordinated by the **Nexus** orchestrator.

## Agent Catalog

### Orchestration

| Agent | Description | Output |
|-------|-------------|--------|
| **Nexus** | _"The right agent at the right time changes everything."_ - Team orchestrator. Decomposes requests and designs optimal agent chains | Prompts, progress management |
| **Sherpa** | _"The mountain doesn't care about your deadline. Plan accordingly."_ - Task decomposition guide. Breaks complex tasks into atomic steps completable within 15 minutes | Checklists |
| **Architect** | _"Every agent is a possibility. Every SKILL.md is a birth certificate."_ - Meta-designer that creates new skill agents. Ecosystem gap analysis, duplication detection, SKILL.md generation | SKILL.md, references |
| **Rally** | _"One task, many hands. Parallel by design."_ - Multi-session parallel orchestrator. Spawns and manages multiple Claude instances via Claude Code Agent Teams API for concurrent task execution | Team management, parallel execution |
| **Hone** | _"A blade sharpened once cuts well. A blade honed repeatedly cuts perfectly."_ - Quality Orchestrator that iteratively improves quality through PDCA cycles. Runs Measure > Improve > Verify > Learn cycles with diminishing returns detection for efficient termination | Quality improvement cycles |
| **Titan** | _"Give me a dream. I'll give you the product."_ - Product lifecycle meta-orchestrator. Coordinates all 69 agents across 9 phases (DISCOVER→BUILD→LAUNCH→EVOLVE) to deliver complete products from ambiguous goals | Product delivery |
| **Sigil** | _"Every project has patterns waiting to become power."_ - Dynamic skill generator. Analyzes project codebases, discovers patterns and conventions, and generates optimized Claude Code skills for the project's `.claude/skills/` directory | Project-specific skills |

### Investigation & Planning (Non-coding)

| Agent | Description | Output |
|-------|-------------|--------|
| **Scout** | _"Every bug has a story. I read the ending first."_ - Bug investigation and root cause analysis (RCA). Identifies reproduction steps and fix locations | Investigation report |
| **Ripple** | _"Every change sends ripples. Know where they land before you leap."_ - Pre-change impact analysis. Evaluates risk from both vertical (dependencies, affected files) and horizontal (pattern consistency, naming conventions) perspectives | Impact analysis report |
| **Spark** | _"The best feature is the one users didn't know they needed."_ - Feature proposals. Suggests features leveraging existing data/logic as Markdown specs | Specification document |
| **Compete** | _"Know your enemy. Know the market. Know yourself."_ - Competitive research, differentiation, and positioning. SWOT analysis, feature matrices | Competitive analysis report |
| **Voice** | _"Feedback is a gift. Analysis is unwrapping it."_ - User feedback collection, NPS survey design, sentiment analysis, and insight extraction | Feedback report |
| **Researcher** | _"Users don't lie. They just don't know what they want yet."_ - User research design, interview guides, qualitative analysis, persona/journey map creation | Research report |
| **Cipher** | _"Don't listen to words. Listen to silence."_ - Decodes user intent. Converts ambiguous requests into precise specifications | Requirements specification |
| **Trace** | _"Every click tells a story. I read between the actions."_ - Session replay analysis, per-persona behavioral pattern extraction, UX problem storytelling. Works with Researcher/Echo | Behavioral analysis report |
| **Canon** | _"Standards are the accumulated wisdom of the industry. Apply them, don't reinvent them."_ - Investigates and analyzes using global/industry standards. Evaluates compliance with OWASP/WCAG/OpenAPI/ISO 25010, detects violations, and suggests improvements | Compliance report |
| **Lens** | _"See the code, not just search it."_ - Codebase comprehension specialist. Systematically investigates code structure, feature exploration, and data flow tracing for questions like "Does feature X exist?", "How does flow Y work?", "What is this module's responsibility?" | Investigation report |
| **Magi** | _"Three minds, one verdict. Consensus through diversity."_ - Multi-perspective decision making from three viewpoints (Logic, Empathy, Pragmatism). Architecture selection, tradeoff analysis, Go/No-Go decisions | Decision report |
| **Bridge** | _"The gap between 'what they want' and 'what we build' is where projects die."_ - Translates and mediates between business requirements and technical implementation. Requirements clarification, scope creep detection, expectation gap resolution | Requirements translation report |

**Scout > Ripple > Builder chain**: Scout (bug investigation) > Ripple (fix impact analysis) > Builder (implementation)
**Ripple > Guardian chain**: Ripple (impact analysis) > Guardian (PR strategy)
**Researcher > Trace > Echo chain**: Researcher (persona definition) > Trace (real-data validation) > Echo (simulation confirmation)
**Sentinel > Canon > Builder chain**: Sentinel (vulnerability detection) > Canon (OWASP compliance evaluation) > Builder (fix implementation)
**Gateway > Canon > Gateway chain**: Gateway (API design) > Canon (OpenAPI/RFC compliance check) > Gateway (corrections)
**Echo > Canon > Palette chain**: Echo (UX issues) > Canon (WCAG compliance evaluation) > Palette (accessibility fixes)

### Git/PR Management

| Agent | Description | Output |
|-------|-------------|--------|
| **Guardian** | _"Every commit tells a story. Make it worth reading."_ - Git/PR gatekeeper. Signal/Noise analysis of changes, commit granularity optimization, branch naming, PR strategy proposals | Analysis report, PR preparation |
| **Harvest** | _"Code writes history. I harvest its meaning."_ - PR information collection and report generation. Fetches PR info via gh commands to auto-generate weekly/monthly reports and release notes | Work reports, release notes |
| **Launch** | _"Shipping is not the end. It's the beginning of accountability."_ - Release management. Versioning strategy, CHANGELOG generation, release notes, rollback plans, feature flag design | Release plans, CHANGELOG |
| **Rewind** | _"Every bug has a birthday. Every regression has a parent commit. Find them."_ - Git history investigation, regression root cause analysis, code archaeology. Travels back in time to uncover the truth | History investigation report |
| **Bard** | _"Code is silence. Poetry gives it voice."_ - Developer grumble agent with three AI personas. Transforms git history, PRs, and milestones into authentic developer monologues, rants, and musings | Narratives, commentary |

**Guardian > Judge > Zen chain**: Guardian (PR preparation) > Judge (review) > Zen (fixes)
**Guardian > Launch chain**: Guardian (change analysis) > Launch (release plan)
**Rewind > Scout chain**: Rewind (regression identification) > Scout (detailed investigation)
**Harvest > Bard chain**: Harvest (PR statistics) > Bard (sprint retrospective narrative)
**Launch > Bard chain**: Launch (release execution) > Bard (release celebration)
**Rewind > Bard chain**: Rewind (code archaeology) > Bard (project origin story)

### Quality Assurance

| Agent | Description | Output |
|-------|-------------|--------|
| **Radar** | _"Untested code is unfinished code."_ - Unit/integration test addition, flaky test fixing, coverage improvement | Test code |
| **Voyager** | _"E2E tests are the user's advocate in CI/CD."_ - E2E test specialist. Playwright/Cypress setup, Page Object design, visual regression, CI integration | E2E test code |
| **Sentinel** | _"Security is not a feature. It's a responsibility."_ - Static security analysis (SAST), vulnerability pattern detection, input validation | Security fixes |
| **Probe** | _"A system is only as secure as its weakest endpoint."_ - Dynamic security testing (DAST), OWASP ZAP/Nuclei integration, penetration testing | Vulnerability report |
| **Judge** | _"Good code needs no defense. Bad code has no excuse."_ - Code review via codex review, automated PR review, pre-commit checks, AI hallucination detection | Review report |
| **Zen** | _"Clean code is not written. It's rewritten."_ - Refactoring and code quality improvement (behavior unchanged) | Code improvements |
| **Sweep** | _"Dead code is technical debt that earns no interest."_ - Unused file detection, dead code identification, orphaned file discovery, safe deletion proposals | Cleanup proposals |
| **Warden** | _"Quality is not negotiable. Ship nothing unworthy."_ - V.A.I.R.E. quality standards guardian. Pre-release evaluation, scorecards, pass/fail decisions | Quality evaluation report |
| **Specter** | _"The bugs you can't see are the ones that haunt you."_ - Ghost hunter for "invisible" issues in concurrency, async processing, and resource management. Detects and analyzes Race Conditions, Memory Leaks, Resource Leaks, and Deadlocks | Detection report |

### Implementation

| Agent | Description | Output |
|-------|-------------|--------|
| **Builder** | _"Types are contracts. Code is a promise."_ - Production implementation. Type-safe craftsman with TDD, Event Sourcing, CQRS, and performance optimization. Detects spec ambiguity, supports auto-handoff from Forge | Production code |
| **Artisan** | _"Prototypes promise. Production delivers."_ - Production frontend implementation craftsman. React/Vue/Svelte, Hooks design, state management, Server Components, form handling, data fetching | Frontend code |
| **Forge** | _"Done is better than perfect. Ship it, learn, iterate."_ - Prototyping. Prioritizes working software over perfection. Outputs types.ts, errors.ts, forge-insights.md for Builder handoff | MVP/PoC |
| **Arena** | _"Arena is the judge, not a player. External engines compete; the best solution wins."_ - Drives codex exec / gemini CLI directly for parallel implementation, evaluation, and adoption. Supports Solo Mode (sequential) and Team Mode (Agent Teams parallel) | Comparative implementation and evaluation |

### Performance

| Agent | Description | Output |
|-------|-------------|--------|
| **Bolt** | _"Speed is a feature. Slowness is a bug you haven't fixed yet."_ - Application performance improvement. Frontend (re-render reduction) and backend (N+1 fix) optimization | Optimized code |
| **Tuner** | _"A fast query is a happy user. A slow query is a lost customer."_ - DB performance optimization. EXPLAIN ANALYZE analysis, index recommendations, slow query improvement | Query optimization |

### UI/UX

| Agent | Description | Output |
|-------|-------------|--------|
| **Vision** | _"Design is not how it looks. Design is how it feels."_ - Creative direction. Design direction decisions, Design System creation, Muse/Palette/Flow/Forge orchestration | Design strategy |
| **Palette** | _"Usability is invisible when done right, painful when done wrong."_ - Usability improvement, cognitive load reduction, a11y support | UX improvements |
| **Muse** | _"Tokens are the DNA of design. Mutate them with care."_ - Design token application, spacing/border-radius/shadow unification, dark mode support | Visual improvements |
| **Flow** | _"Motion creates emotion. Animation breathes life."_ - UI animation, hover effects, loading states, modal transitions | Animations |
| **Echo** | _"I don't test interfaces. I feel what users feel."_ - Persona validation. Embodies users to report confusion points in UI flows | UX report |
| **Showcase** | _"Components without stories are components without context."_ - Storybook story creation, catalog management, Visual Regression integration. CSF 3.0 format | Storybook Stories |

### Documentation

| Agent | Description | Output |
|-------|-------------|--------|
| **Scribe** | _"A specification is a contract between vision and reality."_ - Document writer for PRD/SRS/HLD/LLD, implementation checklists, and test specifications | Specs, design docs |
| **Quill** | _"Code tells computers what to do. Documentation tells humans why."_ - JSDoc/TSDoc additions, README updates, typing `any` to proper type definitions | Documentation |
| **Morph** | _"A document is timeless. Its format is temporary."_ - Document format conversion (Markdown <> Word/Excel/PDF/HTML). Converts Scribe specs and Harvest reports to various formats | Converted documents |
| **Prism** | _"One source, many lights."_ - NotebookLM steering prompt design consultant. Advises on source preparation and optimal output format selection (Audio/Video/Slide/Infographic/Mind Map) | Steering prompts |

**Scribe vs Quill vs Morph vs Prism responsibilities**:
- **Scribe**: Project documentation (PRD, SRS, design docs, checklists, test specifications)
- **Quill**: Code documentation (JSDoc/TSDoc, README, type definitions)
- **Morph**: Format conversion (Markdown > PDF/Word/HTML, etc.)
- **Prism**: NotebookLM content optimization (steering prompts for Audio/Video/Slide)

### Visualization

| Agent | Description | Output |
|-------|-------------|--------|
| **Canvas** | _"A diagram is worth a thousand lines of documentation."_ - Design visualization. Converts code, specs, and context into Mermaid diagrams or ASCII art (flowcharts, sequence diagrams, state machines, class diagrams, ER diagrams, etc.) | Mermaid diagrams / ASCII Art |
| **Sketch** | _"From words to worlds, prompt to pixel."_ - AI image generation code craftsman. Produces production-ready Python code for image generation via Gemini API. Prompt engineering, batch generation, cost estimation | Python code |

### Architecture

| Agent | Description | Output |
|-------|-------------|--------|
| **Atlas** | _"Dependencies are destiny. Map them before they map you."_ - Dependency analysis, circular reference detection, ADR/RFC creation | Design documents |
| **Horizon** | _"Today's innovation is tomorrow's legacy code. Plan accordingly."_ - Modernization. Deprecated library detection, native API replacement, PoC creation | Migration plans |
| **Gateway** | _"APIs are promises to the future. Design them like contracts."_ - API design, review, OpenAPI spec generation, versioning strategy, breaking change detection | API specifications |
| **Grove** | _"A well-structured repository is a well-structured mind."_ - Repository structure design, optimization, and auditing. Directory design, docs/ organization, test structure, anti-pattern detection | Structure design, audit reports |

### Communication

| Agent | Description | Output |
|-------|-------------|--------|
| **Relay** | _"Every message finds its way. Every channel speaks the same language."_ - Messaging integration, bot development, and real-time communication specialist. Channel adapters, webhook handlers, WebSocket servers, event-driven architecture | Channel adapters, message handlers, bot framework |

**Relay > Builder > Radar chain**: Relay (messaging design) > Builder (implementation) > Radar (tests)
**Gateway > Relay chain**: Gateway (webhook API spec) > Relay (handler design)

### Data

| Agent | Description | Output |
|-------|-------------|--------|
| **Schema** | _"A schema is a contract with the future."_ - DB schema design, migration creation, ER diagram design | Migrations / schema definitions |
| **Stream** | _"Data flows like water. My job is to build the pipes."_ - Data pipelines. ETL/ELT design, Kafka/Airflow/dbt, batch/streaming selection, data quality management | Pipeline design, DAGs, dbt models |

**Schema > Stream chain**: Schema (data model) > Stream (pipeline design)

### DevOps

| Agent | Description | Output |
|-------|-------------|--------|
| **Anvil** | _"The terminal is the first interface. Make it unforgettable."_ - Terminal UI construction, CLI development support, dev tool integration (Linter/test runner/build) | CLI/TUI code |
| **Gear** | _"The best CI/CD is the one nobody thinks about."_ - Dependency management, CI/CD optimization, Docker configuration, operational monitoring | Configuration files |
| **Scaffold** | _"Infrastructure is the silent foundation of every dream."_ - Cloud infrastructure (Terraform/CloudFormation/Pulumi), local dev environments (Docker Compose), IaC design | Infrastructure config |
| **Hearth** | _"Your tools should feel like home."_ - Personal dev environment craftsman. Generates, optimizes, and audits config files (zsh/tmux/neovim/ghostty), dotfile management, shell/terminal/editor setup | Config files |

### Internationalization

| Agent | Description | Output |
|-------|-------------|--------|
| **Polyglot** | _"Every language deserves respect. Every user deserves their mother tongue."_ - i18n support. Replaces hardcoded strings with t() functions, formats dates/currencies with Intl API | i18n implementation |

### Growth

| Agent | Description | Output |
|-------|-------------|--------|
| **Growth** | _"Traffic without conversion is just expensive vanity."_ - SEO (meta/OGP/JSON-LD), SMO (social share display), CRO (CTA improvement) | Growth initiatives |
| **Retain** | _"Acquisition is expensive. Retention is profitable."_ - Retention strategies, re-engagement, churn prevention. Gamification, habit-forming design | Retention initiatives |

### Analytics

| Agent | Description | Output |
|-------|-------------|--------|
| **Pulse** | _"What gets measured gets managed. What gets measured wrong gets destroyed."_ - KPI definition, tracking event design, dashboard spec creation | Metrics design |
| **Experiment** | _"Every hypothesis deserves a fair trial. Every decision deserves data."_ - A/B test design, hypothesis documentation, sample size calculation, feature flag implementation | Experiment reports |

### Operations

| Agent | Description | Output |
|-------|-------------|--------|
| **Triage** | _"In chaos, clarity is the first act of healing."_ - Incident response, impact assessment, recovery procedures, postmortem creation | Operations reports |

### Browser Automation

| Agent | Description | Output |
|-------|-------------|--------|
| **Navigator** | _"The browser is a stage. Every click is a scene."_ - Browser automation via Playwright/Chrome DevTools. Data collection, form interaction, screenshots, network monitoring | Automation scripts |
| **Director** | _"A demo that moves hearts moves products."_ - Automated feature demo video recording using Playwright E2E tests. Scenario design, recording settings, implementation patterns, quality checklists | Demo videos (.webm) |
| **Reel** | _"The terminal is a stage. Every keystroke is a performance."_ - Terminal recording and CLI demo video generation using VHS/terminalizer/asciinema. Creates GIF/MP4/WebM from declarative .tape files | GIF/video (.gif/.mp4) |

**Anvil > Reel > Quill chain**: Anvil (CLI development) > Reel (demo recording) > Quill (README GIF embedding)
**Director + Reel > Showcase chain**: Director (web recording) + Reel (terminal recording) > Showcase (visual documentation)
**Director vs Reel responsibilities**:
- **Director**: Browser (Web UI) demo videos (Playwright, .webm output)
- **Reel**: Terminal (CLI) demo recordings (VHS, GIF/MP4 output)

## Workflows

### Basic Usage

1. Invoke an agent with `/AgentName`
2. The agent executes the task
3. Suggests handoff to other agents as needed

### Orchestration with Nexus

Use **Nexus** for complex tasks. Nexus operates in the following modes:

| Mode | Trigger | Behavior | Interaction |
|------|---------|----------|-------------|
| **Full Auto** | `## NEXUS_AUTORUN` + simple task | Fully automatic execution | Only on errors |
| **Guided** | `## NEXUS_GUIDED` or default | Confirms at decision points | Option-based interaction |
| **Interactive** | `## NEXUS_INTERACTIVE` | Confirms at each step | Always interactive |
| **Continue** | `## NEXUS_HANDOFF` | Result handoff | Interaction as needed |

### Interactive Execution (Guided/Interactive)

Each agent asks for user confirmation at important decision points (using the platform's interaction capabilities):

- **Start confirmation**: Confirms approach after chain design, before execution
- **Decision point confirmation**: Security risks, destructive changes, multiple approaches, etc.
- **Questions as options**: Choose from 2-4 options ("Other" is always available)

```yaml
# Example option-based question
questions:
  - question: "A potential security vulnerability was found. How would you like to proceed?"
    header: "Security"
    options:
      - label: "Audit with Sentinel (Recommended)"
        description: "Request review from the security specialist agent"
      - label: "Continue with acknowledged risk"
        description: "Proceed at your own risk"
      - label: "Abort investigation"
        description: "Stop for safety"
```

### Automatic Mode Selection by Complexity

| Indicator | SIMPLE | COMPLEX |
|-----------|--------|---------|
| Estimated steps | 1-2 | 3+ |
| Affected files | 1-3 | 4+ |
| Security-related | No | Yes |
| Destructive changes | No | Yes |

- **SIMPLE + NEXUS_AUTORUN**: Fully automatic execution
- **COMPLEX**: Automatically switches to Guided mode (interaction required)

See `_common/INTERACTION.md` for details.

### Chain Templates by Task Type

#### Investigation & Understanding

| Task | Description | Chain |
|------|-------------|-------|
| INVESTIGATE/feature | Feature existence/implementation investigation | Lens |
| INVESTIGATE/flow | Data flow/processing flow tracing | Lens > Canvas |
| INVESTIGATE/onboarding | Full codebase understanding | Lens > Scribe |
| INVESTIGATE/pre-impl | Investigation then implementation | Lens > Builder > Radar |

> **Lens vs Scout**: Lens = codebase understanding and feature exploration ("Does X exist?", "How does Y flow?"), Scout = bug investigation and root cause analysis ("Why did it break?")

#### Bug Fixes

| Task | Description | Chain |
|------|-------------|-------|
| BUG/simple | Simple bug fix | Scout > Builder > Radar |
| BUG/complex | Complex bug (RCA required) | Scout > Sherpa > Builder > Radar > Sentinel |
| BUG/frontend | Frontend bug | Scout > Artisan > Radar |

#### Feature Development

| Task | Description | Chain |
|------|-------------|-------|
| FEATURE/S | Small feature | Builder > Radar |
| FEATURE/M | Medium feature | Sherpa > Forge > Builder > Radar |
| FEATURE/L | Large feature | Spark > Sherpa > Forge > Builder > Radar > Quill |
| FEATURE/frontend | Frontend feature | Sherpa > Forge > Artisan > Radar |
| FEATURE/fullstack | Full-stack feature | Sherpa > Forge > Artisan > Builder > Radar |
| FEATURE/api | API development | Gateway > Builder > Radar |

#### UI/UX

| Task | Description | Chain |
|------|-------------|-------|
| UI/new | New UI implementation | Vision > Forge > Showcase > Muse > Artisan > Radar |
| UI/redesign | UI redesign | Vision > Muse > Palette > Flow > Artisan > Radar |
| UI/component | Component creation | Forge > Showcase > Muse > Artisan > Radar |
| UI/animation | Animation addition | Flow > Artisan > Radar |
| UX/research | UX research | Researcher > Echo > Palette |
| UX/improve | UX improvement | Echo > Palette > Artisan > Radar |
| UX/session-analysis | Session analysis | Trace > Echo > Palette |
| UX/persona-validation | Persona validation | Researcher > Trace > Echo |

#### Refactoring

| Task | Description | Chain |
|------|-------------|-------|
| REFACTOR/small | Small refactor | Zen > Radar |
| REFACTOR/arch | Architecture improvement | Atlas > Sherpa > Zen > Radar |
| REFACTOR/legacy | Legacy modernization | Horizon > Sherpa > Zen > Radar |

#### Performance

| Task | Description | Chain |
|------|-------------|-------|
| PERF/frontend | Frontend optimization | Bolt > Artisan > Radar |
| PERF/backend | Backend optimization | Bolt > Builder > Radar |
| PERF/db | Database optimization | Tuner > Schema > Builder > Radar |

#### Security

| Task | Description | Chain |
|------|-------------|-------|
| SECURITY/audit | Static analysis | Sentinel > Builder > Radar |
| SECURITY/pentest | Dynamic testing | Probe > Builder > Radar > Probe |
| SECURITY/full | Full audit | Sentinel > Probe > Builder > Radar > Sentinel |

#### Testing

| Task | Description | Chain |
|------|-------------|-------|
| TEST/unit | Unit test addition | Radar |
| TEST/e2e | E2E test addition | Voyager |
| TEST/coverage | Coverage improvement | Radar > Voyager |

#### Review

| Task | Description | Chain |
|------|-------------|-------|
| REVIEW/pr | PR review | Judge > Zen/Builder/Sentinel |
| REVIEW/security | Security review | Judge > Sentinel |

#### Git/PR

| Task | Description | Chain |
|------|-------------|-------|
| GIT/pr-prep | PR preparation | Guardian > Judge |
| GIT/commit-split | Commit splitting | Guardian |
| GIT/pr-full | Implement > PR > Review | Builder > Guardian > Judge > Zen |
| GIT/release | Release notes generation | Guardian |

#### Decision Making

| Task | Description | Chain |
|------|-------------|-------|
| DECISION/arch | Architecture selection | Magi > Builder/Zen |
| DECISION/strategy | Strategic decisions | Bridge > Magi > Spark |
| DECISION/intent | Intent analysis | Cipher > Forge/Builder |

#### Analysis

| Task | Description | Chain |
|------|-------------|-------|
| ANALYSIS/impact | Change impact analysis | Ripple > Builder > Radar |
| ANALYSIS/standards | Standards compliance check | Canon > Builder > Radar |
| ANALYSIS/cleanup | Code cleanup | Sweep > Zen > Radar |

#### Documentation

| Task | Description | Chain |
|------|-------------|-------|
| DOCS/prd | PRD creation | Scribe |
| DOCS/srs | SRS creation | Scribe |
| DOCS/design | Design document creation | Scribe |
| DOCS/spec-to-build | Spec to implementation | Spark > Scribe > Sherpa > Builder |
| DOCS/code | Code documentation | Quill |
| DOCS/component | Component documentation | Showcase > Quill |
| DOCS/architecture | Architecture diagrams | Canvas |
| DOCS/convert | Format conversion | Morph |
| DOCS/report | PR report | Harvest > Morph |

#### Demo & Recording

| Task | Description | Chain |
|------|-------------|-------|
| DEMO/cli | CLI demo GIF creation | Anvil > Reel > Quill |
| DEMO/prototype | Prototype demo | Forge > Reel > Growth |
| DEMO/web-terminal | Web + terminal combo demo | Director + Reel > Showcase |
| DEMO/docs | Documentation demo | Scribe > Reel > Quill |
| DEMO/ci-update | CI-integrated demo auto-update | Gear > Reel > Gear |
| DEMO/showcase | Production CLI demo | Builder > Reel > Growth |

#### Infrastructure & DevOps

| Task | Description | Chain |
|------|-------------|-------|
| INFRA/ci | CI/CD setup | Gear > Radar |
| INFRA/cloud | Cloud setup | Scaffold > Gear |
| INFRA/cli | CLI development | Anvil > Radar |

#### Deploy & Release

| Task | Description | Chain |
|------|-------------|-------|
| DEPLOY/release | Release execution | Guardian > Launch |
| DEPLOY/full | Full pipeline | Radar > Guardian > Launch > Harvest |

#### Modernization

| Task | Description | Chain |
|------|-------------|-------|
| MODERNIZE/stack | Tech stack refresh | Lens > Horizon > Sherpa > Builder > Radar |
| MODERNIZE/i18n | Internationalization | Polyglot > Artisan > Radar |
| MODERNIZE/structure | Repository structure improvement | Grove > Sherpa > Zen > Radar |

#### Strategy & Growth

| Task | Description | Chain |
|------|-------------|-------|
| STRATEGY/seo | SEO improvement | Growth > Artisan > Radar |
| STRATEGY/compete | Competitive analysis to implementation | Compete > Spark > Builder > Radar |
| STRATEGY/feedback | Feedback integration | Voice > Spark > Builder > Radar |
| STRATEGY/metrics | Metrics infrastructure | Pulse > Builder > Radar |
| STRATEGY/retention | Retention initiatives | Retain > Spark > Builder > Radar |
| STRATEGY/ab-test | A/B test design | Experiment > Builder > Radar |
| STRATEGY/data | Data pipeline | Stream > Schema > Builder > Radar |

#### Parallel Execution (Rally Integration)

For large-scale tasks where parallel execution is beneficial, Nexus escalates to Rally.

| Task | Description | Parallel Chain |
|------|-------------|---------------|
| FEATURE/L (parallel) | Large-scale full-stack | Sherpa > Rally(Artisan + Builder + Radar) |
| FEATURE/fullstack (parallel) | Frontend + Backend | Rally(Artisan, Builder, Radar) |
| FEATURE/multi (parallel) | Multiple independent features | Sherpa > Rally(Builder x N, Radar) |
| BUG/multiple (parallel) | Multiple independent bug fixes | Rally(Builder x N) > Radar |
| REFACTOR/arch (parallel) | Multi-module refactoring | Atlas > Sherpa > Rally(Zen x N) > Radar |
| SECURITY/full (parallel) | Static + dynamic parallel scan | Rally(Sentinel, Probe) > Builder > Radar |
| TEST/coverage (parallel) | Unit + E2E parallel testing | Rally(Radar, Voyager) |
| MODERNIZE/stack (parallel) | Multi-area modernization | Horizon > Sherpa > Rally(Builder x N) > Radar |
| DOCS/full (parallel) | Code docs + diagrams + stories | Rally(Quill, Canvas, Showcase) |

> **Rally Escalation Criteria**: Rally is triggered when there are 2+ independent implementation steps, changes span 4+ files across 2+ domains, or Sherpa detects a `parallel_group`.

> **Nexus parallel vs Rally**: Nexus's built-in `_PARALLEL_BRANCHES` is for lightweight parallelism (each branch < 50 lines). Rally's multi-session parallelism is used for substantial implementation work.

#### Product Lifecycle (Titan)

| Task | Description | Chain |
|------|-------------|-------|
| PROJECT/full | Full product from ambiguous goal | Titan (9-phase lifecycle via Nexus) |
| PROJECT/mvp | MVP-focused delivery | Titan (DISCOVER→BUILD→VALIDATE→LAUNCH) |

> **Titan vs Nexus**: Titan = product-level orchestration (what to build, when, and which agents). Nexus = task-level execution (how to chain agents for each task). Titan issues task chains to Nexus.

#### Other

| Task | Description | Chain |
|------|-------------|-------|
| INCIDENT | Incident response | Triage > Scout > Builder |
| TEST/quality | Iterative quality improvement | Hone |
| SECURITY/concurrency | Concurrency bug detection | Specter > Builder > Radar |
| INVESTIGATE/regression | Regression investigation | Rewind > Scout > Builder > Radar |

#### Messaging & Real-time

| Task | Description | Chain |
|------|-------------|-------|
| MESSAGING/bot | Bot development | Relay > Builder > Radar |
| MESSAGING/webhook | Webhook handler | Gateway > Relay > Builder > Radar |
| MESSAGING/realtime | Real-time communication | Relay > Scaffold > Builder > Radar |
| MESSAGING/multi-channel | Multi-channel integration | Relay > Builder > Radar |

## Shared Knowledge

Agents share knowledge through the `.agents/` directory:

| File | Purpose | When to Update |
|------|---------|---------------|
| `PROJECT.md` | Shared knowledge + activity log | **Required for all agents after completing work** |
| `{agent}.md` | Agent-specific learnings | When domain-specific discoveries are made |

### PROJECT.md Structure

- **Architecture Decisions** - Record of architecture choices
- **Domain Glossary** - Unified terminology
- **API & External Services** - External service constraints
- **Known Gotchas** - Known pitfalls
- **Security Considerations** - Security constraints
- **Performance Budgets** - Performance targets
- **Activity Log** - Agent work history

## Agent Principles

All agents follow these principles:

### Common Rules

- **Changes under 50 lines** - Aim for small, safe changes
- **Respect existing patterns** - Follow project conventions
- **Run tests** - Run tests before and after changes
- **Journal only significant learnings** - Don't record routine work

### Boundary Types

| Marker | Meaning |
|--------|---------|
| Always do | Must always be done |
| Ask first | Requires confirmation |
| Never do | Must never be done |

## Directory Structure

```
skills/
├── _common/
│   └── INTERACTION.md  # Shared interaction rules
├── _templates/
│   └── PROJECT.md      # Project knowledge template
├── architect/SKILL.md  # Agent design meta-designer
├── anvil/SKILL.md      # CLI/TUI construction
├── arena/SKILL.md      # External engine competition (Solo/Team Mode)
├── artisan/SKILL.md    # Frontend implementation
├── atlas/SKILL.md      # Architecture
├── bard/SKILL.md       # Developer grumble agent
├── bolt/SKILL.md       # Performance
├── bridge/SKILL.md     # Business <> Tech translation
├── builder/SKILL.md    # Production implementation
├── canvas/SKILL.md     # Visualization
├── cipher/SKILL.md     # Intent decoding
├── compete/SKILL.md    # Competitive research
├── director/SKILL.md   # Demo video recording
├── echo/SKILL.md       # Persona validation
├── experiment/SKILL.md # A/B test design
├── flow/SKILL.md       # Animation
├── forge/SKILL.md      # Prototyping
├── gateway/SKILL.md    # API design
├── gear/SKILL.md       # DevOps
├── grove/SKILL.md      # Repository structure design
├── growth/SKILL.md     # SEO/CRO
├── guardian/SKILL.md   # Git/PR management
├── harvest/SKILL.md    # PR info collection & report generation
├── hearth/SKILL.md     # Personal dev environment config
├── hone/SKILL.md       # PDCA quality improvement
├── horizon/SKILL.md    # Modernization
├── judge/SKILL.md      # Code review (codex review)
├── launch/SKILL.md     # Release management
├── lens/SKILL.md       # Codebase comprehension & investigation
├── magi/SKILL.md       # Multi-perspective decision making
├── morph/SKILL.md      # Document format conversion
├── muse/SKILL.md       # Design
├── navigator/SKILL.md  # Browser automation
├── nexus/SKILL.md      # Orchestrator
├── palette/SKILL.md    # UX
├── polyglot/SKILL.md   # i18n
├── prism/SKILL.md      # NotebookLM steering prompt design
├── probe/SKILL.md      # Dynamic security testing (DAST)
├── pulse/SKILL.md      # Metrics design
├── quill/SKILL.md      # Documentation
├── radar/SKILL.md      # Testing
├── rally/SKILL.md      # Multi-session parallel orchestrator
├── reel/SKILL.md       # Terminal recording & CLI demo video generation
├── relay/SKILL.md      # Messaging integration & real-time communication
├── researcher/SKILL.md # User research
├── ripple/SKILL.md     # Pre-change impact analysis
├── retain/SKILL.md     # Retention
├── rewind/SKILL.md     # Git history investigation
├── scaffold/SKILL.md   # Infrastructure
├── schema/SKILL.md     # DB schema design
├── scribe/SKILL.md     # Project documentation (PRD/SRS/design docs)
├── scout/SKILL.md      # Bug investigation
├── sentinel/SKILL.md   # Static security analysis (SAST)
├── sherpa/SKILL.md     # Task decomposition
├── sigil/SKILL.md      # Dynamic project-specific skill generation
├── showcase/SKILL.md   # Storybook story management
├── sketch/SKILL.md     # AI image generation (Gemini API)
├── spark/SKILL.md      # Feature proposals
├── specter/SKILL.md    # Concurrency & async issue detection
├── stream/SKILL.md     # Data pipelines
├── sweep/SKILL.md      # Dead code detection
├── titan/SKILL.md      # Product lifecycle meta-orchestrator
├── trace/SKILL.md      # Session replay analysis
├── triage/SKILL.md     # Incident response
├── tuner/SKILL.md      # DB performance optimization
├── vision/SKILL.md     # Creative direction
├── voice/SKILL.md      # User feedback
├── voyager/SKILL.md    # E2E testing
├── warden/SKILL.md     # V.A.I.R.E. quality gate
└── zen/SKILL.md        # Refactoring
```

## Usage Examples

### Single Agent Usage

> Category-by-category examples for all 71 agents.

#### Orchestration

##### Chain Design (Nexus)

```
/Nexus
I want to implement a login feature. What steps should I follow?
```

**Output**: Task classification (FEATURE/M), recommended chain (Sherpa > Forge > Builder > Radar), prompt for the first step

---

##### Task Decomposition (Sherpa)

```
/Sherpa
The payment feature implementation task is too complex to organize. Please break it down.
```

**Output**: List of atomic steps completable within 15 minutes, progress checklist, specific instructions for the first task to start

---

##### Agent Design (Architect)

```
/Architect
Design an agent specialized in input validation.
I want it to handle Zod/Yup schema validation and error message generation.
```

**Output**: SKILL.md (complete specification), references/*.md (3-7 domain-specific knowledge files), Nexus integration design

---

##### Product Delivery (Titan)

```
/Titan
Build me a task management SaaS with team collaboration features.
```

**Output**: 9-phase product lifecycle execution — market analysis, architecture design, parallel implementation via Rally, security hardening, E2E validation, documentation, and launch preparation. All decisions logged autonomously.

---

##### Project Skill Generation (Sigil)

```
/Sigil
Analyze this project and generate useful skills for the team.
```

**Output**: Tech stack analysis, skill opportunity discovery, Micro/Full skills generated to `.claude/skills/` (e.g., new-page, new-api-route, deploy-flow)

---

##### Targeted Skill Creation (Sigil)

```
/Sigil
Generate a skill for creating new API routes in this Express project.
```

**Output**: Project-specific `new-route.md` skill with templates matching the project's existing patterns and conventions

---

**Architect vs Sigil responsibilities**:
- **Architect**: Designs universal ecosystem agents (400-1400 lines, SKILL.md)
- **Sigil**: Generates project-specific skills from live context (10-400 lines, .claude/skills/)

---

#### Investigation & Planning

##### Bug Investigation (Scout)

```
/Scout
Users are reporting they can't log in. Please investigate the cause.
```

**Output**: Investigation report including reproduction steps, root cause, files to fix, and recommended fix approach

---

##### Feature Proposal (Spark)

```
/Spark
Suggest features to improve this application's usability.
```

**Output**: Feature proposal specification (Markdown) leveraging existing data/logic

---

##### Session Replay Analysis (Trace)

```
/Trace
The checkout flow has a high abandonment rate. Please analyze actual session data.
```

**Output**: Frustration signal detection, per-persona behavioral patterns, UX problem report

---

##### Persona Validation (Trace)

```
/Trace
Validate the "Mobile-First Millennial" persona defined by Researcher against real data.
```

**Output**: Persona definition validity check, sub-segment discovery, handoff to Researcher

**Trace vs Echo vs Researcher responsibilities**:
- **Researcher**: Creates personas (from interviews and research)
- **Trace**: Validates personas with real data (from session logs)
- **Echo**: Embodies personas to validate UI (simulation)

---

#### Git/PR Management

##### PR Preparation (Guardian)

```
/Guardian
Before creating a PR from this branch, suggest a commit structure and PR strategy.
```

**Output**: Signal/Noise analysis of changes, commit split plan, branch naming suggestions, PR description draft

---

##### Commit Splitting (Guardian)

```
/Guardian
I have changes across 47 files. Split them into appropriately granular commits.
```

**Output**: Commit split plan by logical unit, example git add commands

---

##### Branch Naming (Guardian)

```
/Guardian
Suggest a branch name for the task "Add OAuth2 to user authentication".
```

**Output**: Convention-compliant branch name candidates (e.g., feat/oauth2-integration)

---

**Guardian vs Judge vs Zen responsibilities**:
- **Guardian**: PR preparation (change analysis, commit structure, branch naming)
- **Judge**: PR review (bug detection, issue identification)
- **Zen**: Code fixes (refactoring, quality improvement)

---

##### Weekly Work Report (Harvest)

```
/Harvest
Summarize this week's PR activity into a report.
```

**Output**: Markdown report with PR statistics, category distribution, contributor rankings, and highlights

---

##### Release Notes Generation (Harvest)

```
/Harvest
Generate release notes from PRs between v1.1.0 and v1.2.0.
```

**Output**: Changelog-format release notes categorized into Features/Bug Fixes/Improvements/Breaking Changes

---

##### Individual Work Report (Harvest)

```
/Harvest
Create a monthly work report for @username.
```

**Output**: Detailed PR activity for the specific user, category breakdown, weekly trends, highlights

---

##### Sprint Retrospective (Bard)

```
/Bard
Tell me about this week's sprint with some developer commentary.
```

**Output**: Developer-style commentary on the sprint based on PR/commit data

---

##### Release Celebration (Bard)

```
/Bard
Celebrate the v2.0.0 release with some developer musings.
```

**Output**: Authentic developer narrative based on release contents

---

**Harvest vs Bard responsibilities**:
- **Harvest**: Tells the story in numbers (statistical reports, weekly summaries, release notes)
- **Bard**: Tells the story in words (developer monologues, rants, musings)

---

#### Quality Assurance

##### Test Addition (Radar)

```
/Radar
Check test coverage for this area and add missing tests.
```

**Output**: Added edge case tests, boundary value tests, and error case tests

---

##### E2E Test Creation (Voyager)

```
/Voyager
Create E2E tests for the flow from login to purchase completion.
```

**Output**: Playwright/Cypress E2E test code (with Page Object Model design, auth state management, CI integration config)

---

##### Security Audit (Sentinel)

```
/Sentinel
Audit the security of this API.
```

**Output**: Vulnerability detection (SQL injection, XSS, etc.) and fix code

---

##### PR Review (Judge)

```
/Judge
Review this PR. Check for bugs and security issues.
```

**Output**: Automated review via codex review, severity-ranked issue list, suggested fix agents

---

##### Pre-commit Check (Judge)

```
/Judge
Review the changes before committing.
```

**Output**: Review of uncommitted changes, bug/security issue detection, commit go/no-go decision

---

##### Refactoring (Zen)

```
/Zen
This file has poor readability. Please refactor it.
```

**Output**: Readable code split by responsibility (behavior unchanged)

**Note**: Review agent responsibilities:
- **Judge**: PR review via codex review, bug detection, AI hallucination detection (no code modifications)
- **Zen**: Code quality **improvement** (refactoring, readability enhancement)

---

#### Implementation

##### Production Implementation (Builder)

```
/Builder
The prototype works, but please bring it up to production quality.
```

**Output**: Production code with type safety, error handling, and validation added

**Builder capabilities**:
- **Clarify Phase**: Detects spec ambiguity, presents questions or multiple proposals
- **Design Phase**: TDD (test-first design)
- **Build Phase**: Event Sourcing / CQRS / Saga pattern support
- **Validate Phase**: N+1 detection, caching strategy, performance optimization
- **Forge handoff**: types.ts > Value Object, errors.ts > DomainError, forge-insights.md > Business Rules

---

##### Prototyping (Forge)

```
/Forge
Create a prototype of this screen. A working state is fine for now.
```

**Output**: Quickly built UI component that works with mock data

---

##### Frontend Implementation (Artisan)

```
/Artisan
Bring the user profile prototype created by Forge to production quality.
Ensure TypeScript strict mode, proper error handling, and accessibility.
```

**Output**: Type-safe, production-quality React/Vue/Svelte components, custom Hooks, state management integration

**Artisan's key areas**:
- **Hooks design**: Custom Hook creation, proper useEffect/useMemo usage
- **State management**: Zustand/Jotai/Redux Toolkit selection and implementation
- **Server Components**: Server/client separation in React 19/Next.js App Router
- **Form handling**: React Hook Form + Zod validation
- **Data fetching**: Caching strategy with TanStack Query/SWR

---

#### Performance

##### Performance Improvement (Bolt)

```
/Bolt
This page loads slowly. Please improve it.
```

**Output**: Bottleneck identification and optimization (memoization, lazy loading, query improvement, etc.)

**Bolt's scope**:
- **Frontend**: Re-render reduction, React.memo/useMemo, lazy loading, bundle size
- **Backend**: N+1 detection, DataLoader introduction, connection pooling, async processing

---

##### DB Performance Optimization (Tuner)

```
/Tuner
The product listing page query is slow. Analyze with EXPLAIN ANALYZE and optimize.
```

**Output**: Execution plan analysis, index recommendations, query rewrite

**Bolt vs Tuner responsibilities**:
- **Bolt**: Application layer (how queries are issued, caching)
- **Tuner**: Database layer (how queries execute, indexes)

---

#### UI/UX

##### Creative Direction (Vision)

```
/Vision
I want to redesign the dashboard with a modern look.
The current design feels dated, so incorporate current design trends.
```

**Output**: Three design direction proposals, style guide for the selected direction, delegation plan to Muse/Palette/Flow/Forge

---

##### Design Review (Vision)

```
/Vision
Review the current UI design and identify areas for improvement.
```

**Output**: Heuristic evaluation results, prioritized improvement list, assigned agent for each improvement

---

##### UX Improvement (Palette)

```
/Palette
We received feedback that this form has poor usability. Please improve it.
```

**Output**: Feedback improvements, cognitive load reduction, error display improvements

---

##### Design Unification (Muse)

```
/Muse
The design lacks consistency. Please unify it.
```

**Output**: Unification to design tokens, spacing/border-radius/shadow adjustments

---

##### UI Animation (Flow)

```
/Flow
Add animations to this screen to improve interactions.
```

**Output**: Appropriate transitions, hover effects, loading animations added

---

##### Persona Validation (Echo)

```
/Echo
Validate this UI's usability from an elderly user persona's perspective.
```

**Output**: UX report with confusion points and improvement proposals from the specified persona's perspective

---

##### Storybook Story Creation (Showcase)

```
/Showcase
Create Storybook stories for the newly created Button component.
```

**Output**: CSF 3.0 Story file (all variants, interaction tests, autodocs)

**Showcase capabilities**:
- **CREATE**: New component story creation
- **MAINTAIN**: Existing story updates, CSF3 migration
- **AUDIT**: Story coverage and quality auditing

---

##### Storybook Coverage Audit (Showcase)

```
/Showcase
Audit current Storybook coverage. Identify missing stories.
```

**Output**: Coverage report, quality scores, improvement action list

---

#### Documentation

##### PRD Creation (Scribe)

```
/Scribe
Create a PRD (Product Requirements Document) for the user authentication feature.
Include social login and two-factor authentication in scope.
```

**Output**: Complete PRD (overview, user stories, functional requirements, non-functional requirements, acceptance criteria, edge cases)

---

##### SRS Creation (Scribe)

```
/Scribe
Create an SRS (Software Requirements Specification) for the payment module.
Stripe integration and subscription support are required.
```

**Output**: Complete SRS (functional requirements, data model, API specs, non-functional requirements, traceability matrix)

---

##### Implementation Checklist Creation (Scribe)

```
/Scribe
Create an implementation checklist for the search feature.
```

**Output**: Pre-implementation checks, phase-by-phase tasks, quality assurance checks, pre-deployment verification

---

##### Test Specification Creation (Scribe)

```
/Scribe
Create a test specification for the order flow.
Cover normal cases, error cases, and boundary values comprehensively.
```

**Output**: Test case list (ID, priority, steps, expected results), test data, traceability

---

**Scribe vs Quill responsibilities**:
- **Scribe**: Project documentation (specifications, design docs, checklists)
- **Quill**: Code documentation (JSDoc, README, type definitions)

---

##### Documentation Addition (Quill)

```
/Quill
Add documentation to this function. There's feedback that the logic is hard to understand.
```

**Output**: JSDoc/TSDoc, usage examples, parameter descriptions added

---

#### Visualization

##### Diagram Creation (Canvas)

```
/Canvas
Visualize this authentication flow as a diagram.
```

**Output**: Mermaid-format sequence diagrams, flowcharts, state machine diagrams, etc.

---

##### Reverse-engineer Diagrams from Code (Canvas)

```
/Canvas
Visualize the processing flow in src/services/payment/
```

**Output**: Flowchart or sequence diagram generated by analyzing the code

---

##### Conversation Context Organization (Canvas)

```
/Canvas
Organize our conversation so far into a mind map.
```

**Output**: Mind map organizing the conversation content

---

##### ASCII Art Diagrams (Canvas)

```
/Canvas
Create an ASCII art diagram of this API's processing flow.
```

**Output**: ASCII-format flowchart displayable in terminals and code comments

---

##### AI Image Generation Code (Sketch)

```
/Sketch
Generate Python code to create product thumbnail images using Gemini API.
Include batch generation for multiple products.
```

**Output**: Production-ready Python code with Gemini API integration, prompt optimization, batch processing, cost estimation

---

**Canvas vs Sketch responsibilities**:
- **Canvas**: Diagrams and charts (Mermaid, ASCII art, draw.io)
- **Sketch**: AI image generation code (Python code for Gemini API)

---

##### NotebookLM Prompt Design (Prism)

```
/Prism
I want to create an engaging podcast-style audio overview of our API documentation using NotebookLM.
Help me design the optimal steering prompt.
```

**Output**: Optimized steering prompt, source preparation advice, output format recommendations

---

#### Architecture

##### Architecture Analysis (Atlas)

```
/Atlas
Analyze code dependencies and clarify the impact scope of changes.
```

**Output**: Dependency map, problem area identification, ADR/RFC for improvements

---

##### Modernization (Horizon)

```
/Horizon
Check library versions in use and identify deprecated or vulnerable ones.
```

**Output**: Deprecated library detection, alternative proposals, migration PoC

---

##### API Design (Gateway)

```
/Gateway
Design user management API endpoints. Follow REST API best practices.
```

**Output**: OpenAPI specification, endpoint design, versioning strategy

---

##### API Breaking Change Detection (Gateway)

```
/Gateway
Check if this PR's changes break API backward compatibility.
```

**Output**: List of breaking changes, affected clients, migration guide

---

#### Data

##### DB Schema Design (Schema)

```
/Schema
Design a DB schema for the order management system.
Consider relationships between orders, line items, customers, and products.
```

**Output**: ER diagram (Mermaid format), DDL, migration files, index design

**Schema vs Tuner responsibilities**:
- **Schema**: Logical design (table structure, relations, normalization)
- **Tuner**: Physical optimization (index tuning, query improvement)

---

##### Migration Creation (Schema)

```
/Schema
Create a migration to add a profile image URL to the users table.
```

**Output**: Both Up/Down migrations, rollback procedures

---

#### DevOps

##### CLI/TUI Construction (Anvil)

```
/Anvil
Create a command-line tool. Include help display, progress bars, etc.
```

**Output**: CLI with argument parsing, help generation, progress bars, colored output

---

##### CI/CD Improvement (Gear)

```
/Gear
CI execution time is too long. Please reduce it.
```

**Output**: Cache optimization, parallelization, removal of unnecessary steps

---

##### Infrastructure Setup (Scaffold)

```
/Scaffold
Create Terraform configuration for building a staging environment on AWS.
```

**Output**: Terraform/CloudFormation/Pulumi configuration files, environment variable templates

---

##### Personal Dev Environment Setup (Hearth)

```
/Hearth
Optimize my zsh configuration. It's slow to start up and I want better completions.
```

**Output**: Optimized .zshrc with startup profiling, lazy-loading plugins, and completion configuration

---

##### Dotfile Management (Hearth)

```
/Hearth
Set up my neovim configuration with LSP support and lazy.nvim plugin management.
```

**Output**: init.lua structure, lazy.nvim setup, LSP configuration, keybindings

**Hearth vs Gear vs Scaffold responsibilities**:
- **Hearth**: Personal environment (dotfiles, shell, editor, terminal)
- **Gear**: Project-level DevOps (CI/CD, Docker, monitoring)
- **Scaffold**: Infrastructure provisioning (cloud, Docker Compose, IaC)

---

##### Local Development Environment Setup (Scaffold)

```
/Scaffold
Set up a Docker Compose environment so new developers can start immediately.
```

**Output**: docker-compose.yml, .env.example, setup scripts

---

#### Communication

##### Slack Bot Development (Relay)

```
/Relay
Build a Slack bot that responds to /remind commands and sends scheduled reminders.
Support thread replies and slash commands.
```

**Output**: Channel adapter design, command parser specification, webhook handler middleware chain, event routing matrix

---

##### Multi-Channel Notification (Relay)

```
/Relay
Design a notification system that sends alerts to both Slack and Discord.
Each platform should display messages in its native format.
```

**Output**: Unified message schema, platform-specific adapters, fan-out routing design

---

**Relay vs Gateway vs Stream responsibilities**:
- **Relay**: Messaging platform integration (channel adapters, webhooks, WebSocket, bots)
- **Gateway**: REST/GraphQL API design (OpenAPI specs, versioning, endpoints)
- **Stream**: Data pipelines (ETL/ELT, Kafka, Airflow, batch processing)

---

#### Internationalization

##### i18n Implementation (Polyglot)

```
/Polyglot
Internationalize the application for global expansion.
```

**Output**: Hardcoded strings converted to i18n, date/currency format internationalization

---

#### Growth

##### SEO Improvement (Growth)

```
/Growth
Improve the preview display when sharing on social media.
```

**Output**: OGP tags, meta information, structured data added

---

##### Retention Initiatives (Retain)

```
/Retain
User retention rates are declining. Suggest retention improvement strategies.
```

**Output**: Retention analysis framework, re-engagement trigger design, gamification proposals

---

#### Analytics

##### Metrics Design (Pulse)

```
/Pulse
Define KPIs for this service and design tracking events.
```

**Output**: KPI definitions, event design, dashboard specifications

---

##### A/B Test Design (Experiment)

```
/Experiment
Design an A/B test to verify the effect of changing the CTA button color.
```

**Output**: Hypothesis document, sample size calculation, feature flag implementation guide

---

#### Operations

##### Incident Response (Triage)

```
/Triage
API responses are slow in production. Please handle initial response.
```

**Output**: Impact assessment, recovery procedures, escalation decisions

---

##### Postmortem Creation (Triage)

```
/Triage
Create a postmortem for the recent incident.
```

**Output**: Incident timeline, root cause, prevention measures

---

#### Investigation & Planning (Additional)

##### Competitive Research (Compete)

```
/Compete
Analyze competitors A and B and identify differentiation points.
```

**Output**: Competitive feature matrix, SWOT analysis, positioning map

---

##### User Research Design (Researcher)

```
/Researcher
Design user interviews to validate the new feature.
```

**Output**: Interview guide, question list, persona/journey map

---

##### Feedback Analysis (Voice)

```
/Voice
Analyze recent app store reviews and extract insights.
```

**Output**: Sentiment analysis, feedback classification, improvement priority list

---

#### Security (Additional)

##### Dynamic Security Testing (Probe)

```
/Probe
Conduct penetration testing on the authentication API.
```

**Output**: OWASP ZAP/Nuclei scan results, vulnerability report, fix priority

**Sentinel vs Probe responsibilities**:
- **Sentinel**: Static analysis (SAST) - reads code to detect vulnerabilities
- **Probe**: Dynamic testing (DAST) - attacks running application to detect vulnerabilities

---

#### Terminal Recording

##### CLI Demo GIF Creation (Reel)

```
/Reel
Record a GIF showing installation through basic usage of this CLI tool.
I'll embed it in the README.
```

**Output**: VHS .tape file, optimized GIF (under 5MB), Markdown embed code

---

##### Terminal Session Recording (Reel)

```
/Reel
Create a demo video of the interactive setup wizard in action.
Include the user selecting options.
```

**Output**: terminalizer recording, edited YAML, GIF output

---

**Director vs Reel responsibilities**:
- **Director**: Browser (Web UI) demo videos (Playwright, .webm output)
- **Reel**: Terminal (CLI) demo recordings (VHS/terminalizer/asciinema, GIF/MP4 output)

---

### Multi-Agent Collaboration (Nexus)

#### New Feature Development (Auto-execution)

```
/Nexus
I want to add a user profile editing feature
- Edit name, email, and avatar image
- With validation
- Show toast on successful save

## NEXUS_AUTORUN
```

**Execution chain**: Spark (spec) > Sherpa (task decomposition) > Forge (prototype) > Builder (production implementation) > Radar (tests) > Quill (documentation)

---

#### Bug Fix (Complex Case)

```
/Nexus
Investigate and fix a payment error that only occurs in production.
It doesn't reproduce locally.

## NEXUS_AUTORUN
```

**Execution chain**: Scout (investigation) > Sherpa (task decomposition) > Builder (fix) > Radar (regression tests) > Sentinel (security verification)

---

#### Large-scale Refactoring

```
/Nexus
The authentication module has become spaghetti code.
I want to refactor it to follow Clean Architecture.
```

**Execution chain**: Atlas (architecture design) > Sherpa (phased plan) > Zen (refactoring) > Radar (tests)

---

#### UI Feature Addition

```
/Nexus
Add a review submission feature to the product detail page.
I want users to be able to input star ratings and comments.
```

**Execution chain**: Spark (spec) > Forge (UI prototype) > Muse (design adjustment) > Builder (implementation) > Radar (tests)

---

### Step-by-Step Execution (Manual Control)

#### Gradual Feature Development

```
/Nexus
I want to add a search feature.
```

#### AUTORUN Mode (Automatic Execution - Recommended)

```
## NEXUS_AUTORUN_FULL
I want to add a search feature.
```

Nexus automatically executes the chain:

```
## Nexus Execution: Add search feature
- Chain: **Spark** > **Sherpa** > **Builder** > **Radar**
- Mode: AUTORUN_FULL

### Executing Step 1/4: Spark
_AGENT_CONTEXT:
  Role: Spark
  Task: Create search feature specification

[Creating specification as Spark...]

_STEP_COMPLETE:
  Agent: Spark
  Status: SUCCESS
  Next: Sherpa

### Executing Step 2/4: Sherpa
[Automatically proceeding to next step...]
```

**No copy-paste needed** - automatically executes to the final deliverable.

#### GUIDED Mode (Manual Handoff)

When invoking each agent manually:

```
## NEXUS_GUIDED
I want to add a search feature.
```

Nexus designs the chain and presents the next step:

```
## Nexus Plan: Add search feature
- Chain: **Spark** > **Sherpa** > **Builder** > **Radar**
- Current step: 1/4

### Next Step: Spark
Invoke **Spark** with the following context:
[Context information]
```

---

### Task Decomposition in Practice (Sherpa)

#### Breaking Large Tasks into Small Steps

```
/Sherpa
I want to implement an e-commerce checkout flow.
```

**Output**:

```
## Sherpa's Guide
**Current Objective:** Checkout flow implementation
**Progress:** 0/8 steps completed

### NOW: Create type definitions for cart contents
Define CartItem and CartSummary interfaces.
*(Shall I invoke Builder?)*

### Upcoming Path:
- [ ] Create cart API endpoint
- [ ] Shipping address input form
- [ ] Payment method selection UI
- [ ] Order confirmation screen
- [ ] Order completion processing
- [ ] Error handling
- [ ] Add tests

**Status:** On Track
```

## Customization

### Adding New Agents

1. Create `skills/[AgentName]/SKILL.md`
2. Define `name` and `description` in frontmatter
3. Specify boundaries (Always do / Ask first / Never do)
4. Add AUTORUN Support and Nexus Hub Mode sections

### Modifying Agents

Edit each `SKILL.md` directly. Format:

```markdown
---
name: AgentName
description: Agent description
---

[Detailed agent instructions]
```

## License

MIT