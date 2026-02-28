# Agent Categories

Complete catalog of all 62 agents organized by category.

---

## Category Overview

| Category | Count | Purpose | Code Generation |
|----------|-------|---------|-----------------|
| Orchestration | 3 | Task coordination and decomposition | No |
| Investigation | 8 | Research and analysis | No |
| Implementation | 6 | Code creation | Yes |
| Testing | 2 | Test creation | Yes |
| Security | 2 | Security analysis and testing | Yes |
| Review | 4 | Code review and quality | Mixed |
| Performance | 2 | Performance optimization | Yes |
| Documentation | 3 | Documentation generation | No (text) |
| Architecture | 4 | System design | Mixed |
| UX/Design | 6 | User experience and interface | Mixed |
| ... | (12 more rows) |

**Total: 62 agents** (2 absorbed: Cipher → Nexus, Bridge → Accord)

---

## Orchestration (3 agents)

Agents that coordinate other agents or decompose complex tasks.

### Nexus
- **Role**: Team orchestrator
- **Input**: User requests
- **Output**: Agent chain, coordination
- **Trigger**: Complex multi-agent tasks

### Sherpa
- **Role**: Task decomposition guide
- **Input**: Complex tasks
- **Output**: Atomic steps (15 min each)
- **Trigger**: Tasks that need breakdown

### Titan
- **Role**: Product lifecycle meta-orchestrator
- **Input**: Product goals (ambiguous or clear)
- **Output**: Complete products via 9-phase lifecycle
- **Trigger**: "Build a product", "full product lifecycle"

**Category Characteristics:**
- Never write code directly
- Coordinate other agents
- Manage workflows and product lifecycle
- Track progress

---

## Investigation (7 agents)

Agents that research, analyze, and propose without writing code.

> **Note:** Cipher (intent decoder) was absorbed into Nexus.

### Scout
- **Role**: Bug investigator
- **Input**: Bug reports
- **Output**: Root cause analysis, fix locations
- **Trigger**: "investigate", "find cause", "bug"

### Spark
- **Role**: Feature proposer
- **Input**: Feature ideas
- **Output**: Feature specifications (Markdown)
- **Trigger**: "propose", "idea", "new feature"

### Compete
- **Role**: Competitive analyst
- **Input**: Competitor names
- **Output**: SWOT analysis, feature matrix
- **Trigger**: "competitor", "differentiation", "compare"

### Voice
- **Role**: Feedback analyst
- **Input**: User feedback data
- **Output**: Sentiment analysis, insights
- **Trigger**: "feedback", "NPS", "review analysis"

### Researcher
- **Role**: User researcher
- **Input**: Research objectives
- **Output**: Interview guides, personas, journey maps
- **Trigger**: "interview", "persona", "research"

### Triage
- **Role**: Incident responder
- **Input**: Incident reports
- **Output**: Impact assessment, recovery steps
- **Trigger**: "incident", "outage", "recovery"

### Rewind
- **Role**: Git history investigator
- **Input**: Regression reports
- **Output**: Root cause from commit history
- **Trigger**: "git history", "regression", "when did this break"

**Category Characteristics:**
- Read and analyze code, don't write it
- Produce reports and recommendations
- Gather context for other agents
- Identify problems, not solutions

---

## Implementation (6 agents)

Agents that write production-quality code.

### Builder
- **Role**: Production code craftsman
- **Input**: Specifications, prototypes
- **Output**: Type-safe, production-ready code
- **Trigger**: "implement", "production", "type-safe"

### Forge
- **Role**: Rapid prototyper
- **Input**: Feature ideas, UI mockups
- **Output**: Working prototypes, MVP
- **Trigger**: "prototype", "quickly", "PoC"

### Artisan
- **Role**: Frontend specialist
- **Input**: UI requirements
- **Output**: React/Vue/Svelte components
- **Trigger**: "frontend", "component", "React"

### Schema
- **Role**: Database designer
- **Input**: Data requirements
- **Output**: Migrations, DDL, ER diagrams
- **Trigger**: "schema", "migration", "DB design"

### Arena
- **Role**: Multi-AI implementation
- **Input**: Complex requirements
- **Output**: Multiple AI solutions for comparison
- **Trigger**: "multiple implementations", "compare", "parallel"

### Architect
- **Role**: Agent meta-designer
- **Input**: Ecosystem gaps
- **Output**: SKILL.md, references/*.md
- **Trigger**: "new agent", "design agent"

**Category Characteristics:**
- Write production code
- Focus on quality and type safety
- Follow project conventions
- Generate testable code

---

## Testing (2 agents)

Agents that create and manage tests.

### Radar
- **Role**: Unit/integration test specialist
- **Input**: Code to test
- **Output**: Test files, coverage reports
- **Trigger**: "add tests", "coverage", "edge cases"

### Voyager
- **Role**: E2E test specialist
- **Input**: User flows
- **Output**: Playwright/Cypress tests
- **Trigger**: "E2E", "end-to-end", "user flow"

**Category Characteristics:**
- Write test code
- Focus on coverage and edge cases
- CI/CD integration
- Regression prevention

---

## Security (2 agents)

Agents that handle security analysis and testing.

### Sentinel
- **Role**: Static security analyst (SAST)
- **Input**: Source code
- **Output**: Vulnerability fixes, security patches
- **Trigger**: "security", "vulnerability", "audit"

### Probe
- **Role**: Dynamic security tester (DAST)
- **Input**: Running application
- **Output**: Penetration test results
- **Trigger**: "penetration", "dynamic test", "OWASP"

**Category Characteristics:**
- Security-focused analysis
- Vulnerability detection
- Compliance checking
- Risk mitigation

---

## Review (4 agents)

Agents that review and improve code quality.

### Judge
- **Role**: Code reviewer
- **Input**: PRs, code changes
- **Output**: Review comments, issue lists
- **Trigger**: "review", "PR check", "code check"

### Zen
- **Role**: Refactoring specialist
- **Input**: Code to improve
- **Output**: Refactored code (same behavior)
- **Trigger**: "refactor", "readable", "clean up"

### Sweep
- **Role**: Dead code remover
- **Input**: Codebase
- **Output**: Unused file detection, safe deletions
- **Trigger**: "unused", "dead code", "cleanup"

### Warden
- **Role**: V.A.I.R.E. quality gatekeeper
- **Input**: Features, flows, prototypes
- **Output**: Scorecard, PASS/FAIL verdict
- **Trigger**: "quality gate", "pre-release review", "V.A.I.R.E."

**Category Characteristics:**
- Quality improvement
- Code review automation
- Best practices enforcement
- UX quality gating (Warden)
- No feature changes

---

## Performance (2 agents)

Agents that optimize application performance.

### Bolt
- **Role**: Application optimizer
- **Input**: Slow code/pages
- **Output**: Optimized code
- **Trigger**: "slow", "performance", "optimize"

### Tuner
- **Role**: Database optimizer
- **Input**: Slow queries
- **Output**: Query rewrites, indexes
- **Trigger**: "query", "EXPLAIN", "index"

**Category Characteristics:**
- Performance measurement
- Bottleneck identification
- Optimization implementation
- Before/after comparison

---

## Documentation (3 agents)

Agents that create and maintain documentation.

### Quill
- **Role**: Documentation writer
- **Input**: Code, APIs
- **Output**: JSDoc, TSDoc, README
- **Trigger**: "document", "add comments", "type definitions"

### Scribe
- **Role**: Specification writer
- **Input**: Requirements
- **Output**: PRD, SRS, HLD, LLD documents
- **Trigger**: "specification", "design doc", "PRD"

### Canvas
- **Role**: Diagram creator
- **Input**: Code, concepts, specs
- **Output**: Mermaid diagrams, ASCII art
- **Trigger**: "diagram", "visualize", "flowchart"

**Category Characteristics:**
- Text generation (not code)
- API documentation
- Usage examples
- Visual representations

---

## Architecture (4 agents)

Agents that design system architecture.

### Atlas
- **Role**: Dependency analyst
- **Input**: Codebase
- **Output**: ADR/RFC, dependency maps
- **Trigger**: "dependency", "architecture", "design"

### Gateway
- **Role**: API designer
- **Input**: API requirements
- **Output**: OpenAPI specs, versioning
- **Trigger**: "API design", "OpenAPI", "endpoint"

### Scaffold
- **Role**: Infrastructure designer
- **Input**: Infrastructure requirements
- **Output**: Terraform, Docker Compose
- **Trigger**: "infrastructure", "Terraform", "environment setup"

### Ripple
- **Role**: Change impact analyzer
- **Input**: Proposed changes
- **Output**: Impact assessment, risk evaluation
- **Trigger**: "impact analysis", "what will break", "change assessment"

**Category Characteristics:**
- System-level design
- Long-term planning
- Documentation focus
- Trade-off analysis

---

## UX/Design (6 agents)

Agents that handle user experience and interface design.

### Vision
- **Role**: Creative director
- **Input**: Design objectives
- **Output**: Design direction, style guides
- **Trigger**: "design direction", "redesign", "vision"

### Palette
- **Role**: UX improver
- **Input**: UI with usability issues
- **Output**: Usability improvements
- **Trigger**: "usability", "cognitive load", "a11y"

### Muse
- **Role**: Design system manager
- **Input**: Inconsistent UI
- **Output**: Token application, visual unity
- **Trigger**: "token", "design system", "dark mode"

### Flow
- **Role**: Animation specialist
- **Input**: UI interactions
- **Output**: CSS/JS animations
- **Trigger**: "animation", "transition", "hover"

### Echo
- **Role**: Persona validator
- **Input**: UI flows
- **Output**: UX confusion reports
- **Trigger**: "persona", "validate", "confusion points"

### Showcase
- **Role**: Storybook manager
- **Input**: Components
- **Output**: CSF 3.0 stories
- **Trigger**: "Storybook", "story", "catalog"

**Category Characteristics:**
- User-focused design
- Visual consistency
- Accessibility
- Component documentation

---

## DevOps (4 agents)

Agents that handle infrastructure and tooling.

### Anvil
- **Role**: CLI/TUI builder
- **Input**: CLI requirements
- **Output**: CLI tools, terminal UI
- **Trigger**: "CLI", "terminal", "command line"

### Gear
- **Role**: CI/CD optimizer
- **Input**: Build configs
- **Output**: Optimized CI/CD, Docker
- **Trigger**: "CI", "build time", "Docker"

### Launch
- **Role**: Release manager
- **Input**: Release requirements
- **Output**: Versioning, CHANGELOG, release notes
- **Trigger**: "release", "version", "CHANGELOG"

### Pipe
- **Role**: GitHub Actions workflow architect
- **Input**: Workflow requirements, existing CI/CD
- **Output**: GHA workflows, Composite Actions, Reusable Workflows, security configs
- **Trigger**: "GHA workflow", "workflow design", "CI security", "pipeline"

### Orbit
- **Role**: Loop automation script generator and operations specialist
- **Input**: Loop goals, contract artifacts, state files
- **Output**: Runner/bootstrap/verify/recover scripts, contract diagnoses, failure classifications
- **Trigger**: "loop automation", "nexus-autoloop", "loop ops", "runner generation"

**Category Characteristics:**
- Infrastructure code
- Automation
- Developer experience
- Build optimization

---

## Modernization (2 agents)

Agents that update and modernize codebases.

### Horizon
- **Role**: Technology updater
- **Input**: Legacy code
- **Output**: Migration plans, PoCs
- **Trigger**: "deprecated", "upgrade", "migration"

### Polyglot
- **Role**: Internationalization specialist
- **Input**: Hardcoded strings
- **Output**: i18n implementation
- **Trigger**: "internationalization", "i18n", "translation"

**Category Characteristics:**
- Code transformation
- Compatibility maintenance
- Gradual migration
- Risk mitigation

---

## Growth (2 agents)

Agents that implement growth features.

### Growth
- **Role**: SEO/SMO/CRO specialist
- **Input**: Pages/components
- **Output**: SEO improvements, meta tags
- **Trigger**: "SEO", "OGP", "conversion"

### Retain
- **Role**: Retention strategist
- **Input**: Churn data
- **Output**: Retention features
- **Trigger**: "retention", "engagement", "churn"

**Category Characteristics:**
- Business metrics focus
- User engagement
- Data-driven decisions
- A/B testing ready

---

## Analytics (2 agents)

Agents that handle metrics and experiments.

### Pulse
- **Role**: Metrics designer
- **Input**: KPI requirements
- **Output**: Tracking events, dashboards
- **Trigger**: "KPI", "tracking", "dashboard"

### Experiment
- **Role**: A/B test designer
- **Input**: Hypotheses
- **Output**: Experiment designs
- **Trigger**: "A/B test", "hypothesis", "feature flag"

**Category Characteristics:**
- Measurement focus
- Statistical rigor
- Hypothesis validation
- Data pipeline integration

---

## Git/PR (2 agents)

Agents that manage version control workflows.

### Guardian
- **Role**: PR strategist
- **Input**: Code changes
- **Output**: Commit structure, branch strategy
- **Trigger**: "commit", "branch", "PR preparation"

### Harvest
- **Role**: PR reporter
- **Input**: PR history
- **Output**: Reports, release notes
- **Trigger**: "weekly report", "release notes", "work report"

**Category Characteristics:**
- Git workflow management
- No code changes
- Reporting and analysis
- PR optimization

---

## Browser (2 agents)

Agents that automate browser interactions.

### Navigator
- **Role**: Browser automation specialist
- **Input**: Browser tasks
- **Output**: Automated actions, screenshots
- **Trigger**: "browser automation", "scraping", "automate"

### Director
- **Role**: Demo video creator
- **Input**: Feature scenarios
- **Output**: Playwright-based demo recordings
- **Trigger**: "demo video", "product demo", "feature recording"

**Category Characteristics:**
- Playwright integration
- Visual verification
- Data extraction
- Task automation

---

## Data (2 agents)

Agents that handle data pipelines and transformations.

### Stream
- **Role**: ETL/ELT designer
- **Input**: Data requirements
- **Output**: Pipeline designs, Kafka/Airflow/dbt configs
- **Trigger**: "ETL", "data pipeline", "data flow"

### Morph
- **Role**: Document converter
- **Input**: Documents in various formats
- **Output**: Converted documents (Markdown ↔ Word/Excel/PDF/HTML)
- **Trigger**: "convert", "document format", "export"

**Category Characteristics:**
- Data transformation
- Format conversion
- Pipeline design
- Quality assurance

---

## Strategy (2 agents)

Agents that simulate and plan business strategy, or provide domain-specific advisory.

### Helm
- **Role**: Business strategy simulator
- **Input**: Financial data, market data, competitor intel, KPIs
- **Output**: Strategy roadmap, KPI forecast, scenario analysis, risk matrix
- **Trigger**: "経営戦略", "business plan", "SWOT", "シミュレーション", "M&A", "中期計画"

### Levy
- **Role**: Tax filing guidance agent (Japan)
- **Input**: Income data, expense records, financial questions
- **Output**: Income classification, deduction optimization, tax calculation, filing guidance
- **Trigger**: "確定申告", "税金", "控除", "青色申告", "e-Tax", "所得税", "節税"

**Category Characteristics:**
- Read and analyze data, don't write code
- Produce strategy documents, recommendations, and tax guidance
- 3-scenario output (Baseline/Optimistic/Pessimistic) is mandatory (Helm)
- All outputs include legal disclaimers (Levy)
- Collaborate with Compete, Pulse, Magi, Scribe, Canvas, Sherpa, Builder

---

## Translation (0 agents — absorbed)

> **Note:** Bridge (business-technical translator) was absorbed into Accord. Use Accord for cross-functional specification needs including business-technical translation.

---

## Incident (1 agent)

Agents that detect and analyze runtime issues.

### Specter
- **Role**: Concurrency/resource hunter
- **Input**: Code with potential issues
- **Output**: Race condition, memory leak, deadlock reports
- **Trigger**: "race condition", "memory leak", "deadlock"

**Category Characteristics:**
- Runtime issue detection
- Concurrency analysis
- Resource management
- Investigation only (no fixes)

---

## Communication (1 agent)

Agents that design and implement messaging integrations and real-time communication.

### Relay
- **Role**: Messaging integration & real-time communication specialist
- **Input**: Messaging platform requirements, channel specifications, bot requirements
- **Output**: Channel adapters, webhook handlers, WebSocket servers, bot frameworks
- **Trigger**: "Build a bot", "Webhook handler", "Real-time chat", "Multi-channel messaging"

**Category Characteristics:**
- Messaging platform integration
- Real-time communication design
- Bot development patterns
- Event-driven architecture

---

## Meta / Tooling (2 agents)

Agents that generate project-specific tooling and skills, or orchestrate ecosystem evolution.

### Sigil
- **Role**: Dynamic project-specific skill generator
- **Input**: Project codebase, tech stack, conventions
- **Output**: Claude Code skills (.claude/skills/*.md)
- **Trigger**: "Generate skills for this project", "Create skill for", "Analyze project and suggest skills"

### Darwin
- **Role**: Ecosystem self-evolution orchestrator
- **Input**: Git metrics, agent journals, activity logs, Health Scores, UQS
- **Output**: Ecosystem state report, evolution actions, dynamic affinity overrides
- **Trigger**: "evolution check", "ecosystem health", "agent fitness"

**Category Characteristics:**
- Analyzes project context before generating
- Generates Micro (10-80 lines) and Full (100-400 lines) skills
- Does not modify ecosystem agents
- Complements Architect (ecosystem) with project-specific skills
- Orchestrates ecosystem-wide evolution (Darwin)

---

## Category Selection Guide

When designing a new agent, use this decision tree:

```
Does it coordinate other agents?
├── Yes → Orchestration
└── No
    ├── Does it write production code?
    │   ├── Yes → Implementation
    │   └── No
    │       ├── Does it write test code?
    │       │   ├── Yes → Testing
    │       │   └── No
    │       │       ├── Does it analyze security?
    │       │       │   ├── Yes → Security
    │       │       │   └── No
    │       │       │       ├── Does it review code?
    │       │       │       │   ├── Yes → Review
    │       │       │       │   └── No → (continue below)
...
```

Complete decision tree available in validation checklist.
