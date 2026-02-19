# Agent Disambiguation Guide

When multiple agents appear to fit a task, use these decision rules for correct routing.

---

## High Priority — Frequently Confused Pairs

### Gear vs Pipe (DevOps / CI/CD)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Fix CI", "speed up build", "update dependencies" | **Gear** | Maintenance of existing pipelines |
| "Design new workflow", "reusable workflow", "security hardening for GHA" | **Pipe** | New GHA architecture or advanced patterns |
| "Add caching to CI" | **Gear** | Optimization of existing pipeline |
| "Matrix strategy", "composite action design", "OIDC setup" | **Pipe** | Advanced GHA-specific features |
| Docker optimization, local dev setup | **Gear** | Not GHA-specific |
| Observability/alerting setup | **Gear** + Beacon | Infrastructure concern |

**Rule of thumb**: Existing pipeline maintenance → Gear. New GHA workflow design or advanced GHA features → Pipe.

---

### Cast vs Echo vs Researcher (Persona / User Research)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Create personas", "persona registry", "sync personas across agents" | **Cast** | Persona lifecycle management |
| "Test this UI as a beginner", "walk through this flow" | **Echo** | Persona-based UI simulation |
| "Design interview guide", "usability test plan", "journey mapping" | **Researcher** | Research methodology design |
| "Update persona with new data" | **Cast** | Persona evolution |
| "What would a mobile user think of this?" | **Echo** | Persona simulation |
| "Analyze survey results" | **Voice** | Feedback data analysis (not persona) |

**Rule of thumb**: Manage/store/evolve personas → Cast. Simulate personas on UI → Echo. Design research methodology → Researcher.

**Chain pattern**: Cast (create) → Researcher (validate with methodology) → Echo (simulate on UI)

---

### Sigil vs Architect (Skill/Agent Creation)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Create a new ecosystem agent" | **Architect** | Permanent agent in `~/.claude/skills/` |
| "Generate project-specific skills" | **Sigil** | Ephemeral skills in `.claude/skills/` or `.agents/skills/` |
| "Design SKILL.md (400+ lines) with references" | **Architect** | Full agent design framework |
| "Analyze this project and create shortcuts" | **Sigil** | Project context → lightweight skills |
| "Ecosystem gap analysis" | **Architect** | Ecosystem-level concern |
| "Improve this agent's SKILL.md" | **Architect** | Agent enhancement |

**Rule of thumb**: Ecosystem-wide permanent agent → Architect. Project-specific lightweight skill → Sigil.

---

## Medium Priority — Sometimes Confused Pairs

### Artisan vs Forge (Frontend Implementation)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Prototype this quickly", "just make it work" | **Forge** | Speed over quality |
| "Production-ready component", "hooks design", "state management" | **Artisan** | Production quality |
| "Validate idea with working demo" | **Forge** | Proof of concept |
| "Convert prototype to production" | **Forge → Artisan** | Standard handoff |
| "Build this React component" (no existing prototype) | **Artisan** | Direct production build |
| Backend mock/API stub | **Forge** | Backend prototyping |

**Rule of thumb**: Uncertain requirements or exploration → Forge first. Clear requirements → Artisan directly. Never use both if requirements are already clear.

---

### Atlas vs Ripple (Architecture Analysis)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Analyze dependencies", "find God Classes", "circular references" | **Atlas** | Current architecture evaluation |
| "What's the impact of changing X?", "is this change safe?" | **Ripple** | Pre-change impact assessment |
| "Create ADR", "architecture decision" | **Atlas** → Magi | Architecture documentation |
| "Should we proceed with this refactor?" | **Ripple** | Risk evaluation before action |
| "Module decomposition strategy" | **Atlas** | Structural analysis |
| "Will renaming this break anything?" | **Ripple** | Change impact |

**Rule of thumb**: "What IS the architecture?" → Atlas. "What HAPPENS IF we change it?" → Ripple.

---

### Scout vs Lens (Code Investigation)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Why is X broken?", "find the bug" | **Scout** | Bug-driven investigation |
| "How does X work?", "explain this module" | **Lens** | Comprehension-driven exploration |
| "What caused this regression?" | **Rewind** → Scout | Git history then RCA |
| "Does feature X exist?", "where is X implemented?" | **Lens** | Code exploration |
| "Reproduce this error" | **Scout** | Bug reproduction |
| "Map the data flow for X" | **Lens** → Canvas | Understanding then visualization |

**Rule of thumb**: Broken behavior → Scout. Understanding behavior → Lens.

---

### Voice vs Researcher (User Insights)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Analyze app store reviews", "NPS survey", "sentiment analysis" | **Voice** | Quantitative feedback analysis |
| "Design interview questions", "usability test plan" | **Researcher** | Research methodology |
| "What are users saying about X?" | **Voice** | Existing feedback collection |
| "What do users NEED from X?" | **Researcher** | Deep user understanding |
| "Create feedback collection system" | **Voice** | Feedback infrastructure |
| "Create journey map" | **Researcher** | User experience mapping |

**Rule of thumb**: Collect/analyze existing feedback → Voice. Design new research → Researcher.

---

### Palette vs Flow (UI Interaction)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Improve usability", "reduce cognitive load", "a11y" | **Palette** | UX quality improvement |
| "Add hover animation", "loading transition", "modal animation" | **Flow** | CSS/JS animation implementation |
| "This button feels unresponsive" | **Palette** | Interaction quality |
| "Animate this page transition" | **Flow** | Motion design |
| "Micro-interaction design" | **Palette** (simple) / **Flow** (complex) | Complexity determines agent |

**Rule of thumb**: UX/usability concern → Palette. Animation implementation → Flow.

---

### Prose vs Palette (Content & UX)

| Signal | Route to | Rationale |
|--------|----------|-----------|
| "Write error messages", "improve button labels" | **Prose** | Content creation |
| "Evaluate UX quality", "audit interaction patterns" | **Palette** | UX assessment |
| "Onboarding copy", "voice & tone guide" | **Prose** | Content strategy |
| "Form feels confusing" | **Palette** (assess) → Prose (rewrite) | Assessment then content |

**Rule of thumb**: Write/rewrite text → Prose. Evaluate/improve interaction → Palette.

---

## Low Priority — Rarely Confused

### Judge vs Zen

**Rule**: "Find problems" → Judge. "Fix code smells" → Zen. Judge discovers, Zen fixes.

### Sentinel vs Probe

**Rule**: Static code scan → Sentinel. Running app penetration test → Probe.

### Quill vs Scribe

**Rule**: Code documentation (JSDoc, README) → Quill. Specification documents (PRD, SRS) → Scribe.

### Helm vs Compete

**Rule**: Business strategy simulation → Helm. Competitive intelligence gathering → Compete. Compete output feeds into Helm input.

### Titan vs Nexus

**Rule**: "Build a product from scratch" → Titan. "Execute this task chain" → Nexus. Titan issues chains TO Nexus.

---

## Small Project Optimization

For S/M scope projects, skip agents that add overhead without proportional value:

| Skip | Use Instead | When |
|------|-------------|------|
| Vision | Palette/Muse directly | No full UX redesign needed |
| Forge | Artisan directly | Requirements are clear |
| Cast | Echo standalone | Simple persona needs |
| Pipe | Gear | Basic CI/CD only |
| Compete | Skip entirely | Internal tools, no competitors |
| Scribe | Skip entirely | S scope, no formal specs needed |
| Researcher | Echo directly | No formal research methodology needed |
