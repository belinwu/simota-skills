# Agent Categories

Complete catalog of all 42 agents organized by category.

---

## Category Overview

| Category | Count | Purpose | Code Generation |
|----------|-------|---------|-----------------|
| Orchestration | 2 | Task coordination and decomposition | No |
| Investigation | 6 | Research and analysis | No |
| Implementation | 5 | Code creation | Yes |
| Testing | 2 | Test creation | Yes |
| Security | 2 | Security analysis and testing | Yes |
| Review | 3 | Code review and quality | Mixed |
| Performance | 2 | Performance optimization | Yes |
| Documentation | 1 | Documentation generation | No (text) |
| Visualization | 1 | Diagram generation | No (diagrams) |
| Architecture | 3 | System design | Mixed |
| UX/Design | 6 | User experience and interface | Mixed |
| DevOps | 2 | Infrastructure and tooling | Yes (config) |
| Modernization | 2 | Technology updates | Yes |
| Growth | 2 | Business growth features | Mixed |
| Analytics | 2 | Metrics and experiments | Mixed |
| Git/PR | 2 | Version control management | No |
| Browser | 1 | Browser automation | Yes |

---

## Orchestration (2 agents)

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

**Category Characteristics:**
- Never write code directly
- Coordinate other agents
- Manage workflows
- Track progress

---

## Investigation (6 agents)

Agents that research, analyze, and propose without writing code.

### Scout
- **Role**: Bug investigator
- **Input**: Bug reports
- **Output**: Root cause analysis, fix locations
- **Trigger**: "調査して", "原因を特定", "バグ"

### Spark
- **Role**: Feature proposer
- **Input**: Feature ideas
- **Output**: Feature specifications (Markdown)
- **Trigger**: "提案して", "アイデア", "新機能"

### Compete
- **Role**: Competitive analyst
- **Input**: Competitor names
- **Output**: SWOT analysis, feature matrix
- **Trigger**: "競合", "差別化", "比較"

### Voice
- **Role**: Feedback analyst
- **Input**: User feedback data
- **Output**: Sentiment analysis, insights
- **Trigger**: "フィードバック", "NPS", "レビュー分析"

### Researcher
- **Role**: User researcher
- **Input**: Research objectives
- **Output**: Interview guides, personas, journey maps
- **Trigger**: "インタビュー", "ペルソナ", "リサーチ"

### Triage
- **Role**: Incident responder
- **Input**: Incident reports
- **Output**: Impact assessment, recovery steps
- **Trigger**: "障害", "インシデント", "復旧"

**Category Characteristics:**
- Read and analyze code, don't write it
- Produce reports and recommendations
- Gather context for other agents
- Identify problems, not solutions

---

## Implementation (5 agents)

Agents that write production-quality code.

### Builder
- **Role**: Production code craftsman
- **Input**: Specifications, prototypes
- **Output**: Type-safe, production-ready code
- **Trigger**: "実装して", "本番", "型安全"

### Forge
- **Role**: Rapid prototyper
- **Input**: Feature ideas, UI mockups
- **Output**: Working prototypes, MVP
- **Trigger**: "プロトタイプ", "素早く", "PoC"

### Artisan
- **Role**: Frontend specialist
- **Input**: UI requirements
- **Output**: React/Vue/Svelte components
- **Trigger**: "フロントエンド", "コンポーネント", "React"

### Schema
- **Role**: Database designer
- **Input**: Data requirements
- **Output**: Migrations, DDL, ER diagrams
- **Trigger**: "スキーマ", "マイグレーション", "DB設計"

### Arena
- **Role**: Multi-AI implementation
- **Input**: Complex requirements
- **Output**: Multiple AI solutions for comparison
- **Trigger**: "複数実装", "比較", "並列"

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
- **Trigger**: "テスト追加", "カバレッジ", "エッジケース"

### Voyager
- **Role**: E2E test specialist
- **Input**: User flows
- **Output**: Playwright/Cypress tests
- **Trigger**: "E2E", "エンドツーエンド", "ユーザーフロー"

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
- **Trigger**: "セキュリティ", "脆弱性", "監査"

### Probe
- **Role**: Dynamic security tester (DAST)
- **Input**: Running application
- **Output**: Penetration test results
- **Trigger**: "ペネトレーション", "動的テスト", "OWASP"

**Category Characteristics:**
- Security-focused analysis
- Vulnerability detection
- Compliance checking
- Risk mitigation

---

## Review (3 agents)

Agents that review and improve code quality.

### Judge
- **Role**: Code reviewer
- **Input**: PRs, code changes
- **Output**: Review comments, issue lists
- **Trigger**: "レビュー", "PR確認", "コードチェック"

### Zen
- **Role**: Refactoring specialist
- **Input**: Code to improve
- **Output**: Refactored code (same behavior)
- **Trigger**: "リファクタ", "読みやすく", "整理"

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
- **Trigger**: "遅い", "パフォーマンス", "最適化"

### Tuner
- **Role**: Database optimizer
- **Input**: Slow queries
- **Output**: Query rewrites, indexes
- **Trigger**: "クエリ", "EXPLAIN", "インデックス"

**Category Characteristics:**
- Performance measurement
- Bottleneck identification
- Optimization implementation
- Before/after comparison

---

## Documentation (1 agent)

Agents that create and maintain documentation.

### Quill
- **Role**: Documentation writer
- **Input**: Code, APIs
- **Output**: JSDoc, TSDoc, README
- **Trigger**: "ドキュメント", "コメント追加", "型定義"

**Category Characteristics:**
- Text generation (not code)
- API documentation
- Usage examples
- Inline comments

---

## Visualization (1 agent)

Agents that create visual representations.

### Canvas
- **Role**: Diagram creator
- **Input**: Code, concepts, specs
- **Output**: Mermaid diagrams, ASCII art
- **Trigger**: "図にして", "可視化", "フロー図"

**Category Characteristics:**
- Diagram generation
- Multiple format support
- Code-to-visual conversion
- Context summarization

---

## Architecture (3 agents)

Agents that design system architecture.

### Atlas
- **Role**: Dependency analyst
- **Input**: Codebase
- **Output**: ADR/RFC, dependency maps
- **Trigger**: "依存関係", "アーキテクチャ", "設計"

### Gateway
- **Role**: API designer
- **Input**: API requirements
- **Output**: OpenAPI specs, versioning
- **Trigger**: "API設計", "OpenAPI", "エンドポイント"

### Scaffold
- **Role**: Infrastructure designer
- **Input**: Infrastructure requirements
- **Output**: Terraform, Docker Compose
- **Trigger**: "インフラ", "Terraform", "環境構築"

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
- **Trigger**: "デザイン方向性", "リデザイン", "ビジョン"

### Palette
- **Role**: UX improver
- **Input**: UI with usability issues
- **Output**: Usability improvements
- **Trigger**: "使いやすさ", "認知負荷", "a11y"

### Muse
- **Role**: Design system manager
- **Input**: Inconsistent UI
- **Output**: Token application, visual unity
- **Trigger**: "トークン", "デザイン統一", "ダークモード"

### Flow
- **Role**: Animation specialist
- **Input**: UI interactions
- **Output**: CSS/JS animations
- **Trigger**: "アニメーション", "トランジション", "ホバー"

### Echo
- **Role**: Persona validator
- **Input**: UI flows
- **Output**: UX confusion reports
- **Trigger**: "ペルソナ", "検証", "混乱ポイント"

### Showcase
- **Role**: Storybook manager
- **Input**: Components
- **Output**: CSF 3.0 stories
- **Trigger**: "Storybook", "ストーリー", "カタログ"

**Category Characteristics:**
- User-focused design
- Visual consistency
- Accessibility
- Component documentation

---

## DevOps (2 agents)

Agents that handle infrastructure and tooling.

### Anvil
- **Role**: CLI/TUI builder
- **Input**: CLI requirements
- **Output**: CLI tools, terminal UI
- **Trigger**: "CLI", "ターミナル", "コマンドライン"

### Gear
- **Role**: CI/CD optimizer
- **Input**: Build configs
- **Output**: Optimized CI/CD, Docker
- **Trigger**: "CI", "ビルド時間", "Docker"

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
- **Trigger**: "非推奨", "アップグレード", "移行"

### Polyglot
- **Role**: Internationalization specialist
- **Input**: Hardcoded strings
- **Output**: i18n implementation
- **Trigger**: "国際化", "i18n", "翻訳"

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
- **Trigger**: "SEO", "OGP", "コンバージョン"

### Retain
- **Role**: Retention strategist
- **Input**: Churn data
- **Output**: Retention features
- **Trigger**: "リテンション", "継続率", "チャーン"

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
- **Trigger**: "KPI", "トラッキング", "ダッシュボード"

### Experiment
- **Role**: A/B test designer
- **Input**: Hypotheses
- **Output**: Experiment designs
- **Trigger**: "A/Bテスト", "仮説", "フィーチャーフラグ"

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
- **Trigger**: "コミット", "ブランチ", "PR準備"

### Harvest
- **Role**: PR reporter
- **Input**: PR history
- **Output**: Reports, release notes
- **Trigger**: "週報", "リリースノート", "作業報告"

**Category Characteristics:**
- Git workflow management
- No code changes
- Reporting and analysis
- PR optimization

---

## Browser (1 agent)

Agents that automate browser interactions.

### Navigator
- **Role**: Browser automation specialist
- **Input**: Browser tasks
- **Output**: Automated actions, screenshots
- **Trigger**: "ブラウザ操作", "スクレイピング", "自動化"

**Category Characteristics:**
- Playwright integration
- Visual verification
- Data extraction
- Task automation

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
    │       │       │       └── ...
    └── ...
```

Complete decision tree available in validation checklist.
