# Full Routing Matrix

**Purpose:** Canonical full task-type to chain mapping.
**Read when:** The quick-start matrix is insufficient and you need the full mapping.

Complete task type → agent chain mapping. The SKILL.md contains the top 5 most common patterns; this file contains the full matrix.

---

| Task Type | Primary Chain | Recipe Hints | Additions |
|-----------|---------------|-------------|-----------|
| BUG | Scout → **Sherpa** → Builder → Radar | Scout[bug], Sherpa[epic], Builder[fix], Radar[regression] | +Sentinel (security). Skip Sherpa only when single-file atomic fix |
| INCIDENT | Triage → Scout → Builder | Scout[bug], Builder[fix] | +Mend (known pattern), +Radar, +Triage (postmortem), +Flux (deep postmortem), +Matrix (failure scenarios) |
| FEATURE | **Sherpa** → Forge → Builder → Radar | Sherpa[epic], Forge[ui], Builder[api], Radar[edge] | +Muse (UI), +Artisan (frontend), +Matrix (variant exploration), +Flux (lateral thinking), +Riff (idea exploration). Skip Sherpa only when single-file atomic change |
| INVESTIGATE | Lens | — | +Scout (bug-related), +Canvas (viz), +Rewind (git) |
| BRAINSTORM | Riff | — | +Flux (reframe first), +Spark (spec after), +Magi (decide after), +Void (prune after) |
| DECISION | Magi | — | +Accord (biz-tech), +Flux (reframe), +Riff (explore before deciding) |
| SECURITY | Sentinel → Builder → Radar | Sentinel[scan], Builder[fix], Radar[edge] | +Probe (dynamic), +Specter (concurrency), +Breach (red-team), +Vigil (detection) |
| REFACTOR | Zen → Radar | —, Radar[coverage] | +Atlas (architectural), +Grove (structure) |
| OPTIMIZE | Bolt/Tuner → Radar | —, Radar[edge] | +Schema (DB), +Flux (first-principles), +Matrix (target combos) |
| ANALYSIS | Ripple → Builder → Radar | Builder[fix], Radar[edge] | +Canon (standards), +Sweep (cleanup) |
| API | Gateway → Builder → Radar | Builder[api], Radar[edge] | +Quill, +Schema |
| DEPLOY | Guardian → Launch | — | +Harvest (reporting) |
| MODERNIZE | Horizon → Builder → Radar | Builder[crud], Radar[coverage] | +Polyglot (i18n), +Grove (structure), +Flux (first-principles), +Matrix (migration paths) |
| DOCS | Quill | — | +Canvas, +Morph (convert), +Scribe (specs) |
| STRATEGY | Spark → Builder → Radar | Builder[ddd], Radar[edge] | +Growth/Compete/Voice/Pulse/Retain/Experiment, +Helm (simulation) |
| STRATEGY_SIM | Helm | Sherpa[story] | +Compete (intel), +Pulse (KPI), +Magi (decision), +Scribe (docs), +Canvas (viz), +Sherpa (execution) |
| INFRA | Scaffold → Gear → Radar | Radar[edge] | +Anvil (CLI), +Pipe (GHA workflows) |
| GHA_WORKFLOW | Pipe | Sentinel[scan] | +Gear (maintenance), +Launch (release), +Sentinel (security) |
| PARALLEL | Rally | Sherpa[epic] | +Sherpa (decomposition), see Rally escalation |
| PROJECT | Titan | Sherpa[epic] | Full product lifecycle — Titan orchestrates 9 phases, issues chains to Nexus |
| MESSAGING | Relay → Builder → Radar | Builder[api], Radar[edge] | +Sentinel (security), +Scaffold (infra) |
| BOT | Relay → Builder → Radar | Builder[api], Radar[edge] | +Sentinel (security) |
| REALTIME | Relay → Scaffold → Builder | Builder[api] | +Radar (tests) |
| WEBHOOK | Gateway → Relay → Builder | Builder[api] | +Radar (tests), +Sentinel (security) |
| HOOKS | Latch | — | +Gear (Git hooks), +Sentinel (security) |
| SKILL_GEN | Sigil | — | +Lens (codebase analysis), +Grove (structure) |
| EVOLUTION | Darwin | — | +Architect (improvement), +Void (sunset), +Lore (knowledge), +Canvas (viz) |
| KNOWLEDGE_SYNC | Lore | — | +Darwin (evolution input), +Architect (design insights), +Nexus (routing feedback) |
| QUALITY | Judge → Canvas | Judge[pr], Radar[coverage] | +Zen (smells), +Radar (coverage), +Sentinel (security), +Atlas (arch), +Sweep (dead code), +Matrix (combinatorial) |
| COMPARE | Arena | Scout[bug] | +Scout (bug-fix), +Sentinel (security), +Guardian (quality gate), +Matrix (dimension analysis), +Flux (reframe) |
| UX_RESEARCH | Researcher → Echo → Palette | — | +Cast (persona), +Trace (session data) |
| E2E | Voyager → Lens | Radar[edge] | +Gear (CI), +Echo (persona-based), +Matrix (test matrix) |
| BROWSER | Navigator → Builder | Scout[bug], Builder[fix] | +Scout (bug repro), +Bolt (perf), +Lens (evidence) |
| DB_DESIGN | Schema → Builder → Radar | Builder[ddd], Radar[edge] | +Tuner (optimize), +Atlas (arch review) |
| OBSERVABILITY | Beacon → Gear → Builder | Builder[fix] | +Triage (incident link), +Scaffold (capacity) |
| AI_FEATURE | Oracle → Builder → Radar | Builder[api], Radar[edge] | +Gateway (API), +Stream (pipeline), +Sentinel (safety) |
| PRERELEASE | Warden → Guardian → Launch | Sentinel[scan], Radar[coverage] | +Sentinel (security gate), +Radar (test gate) |
| REQUIREMENTS | Accord → Scribe → Sherpa | Sherpa[epic] | +Canvas (diagram), +Magi (decision), +Saga (narrative), +Cast (persona) |
| DESIGN_SYSTEM | Vision → Muse → Showcase → Quill | — | +Palette (tokens), +Artisan (impl) |
| DESIGN_SYSTEM_DOCS | Muse → Showcase + Canvas → Quill | — | +Vision (direction), +Artisan (live examples) |
| CONTENT | Prose → Echo → Artisan | — | +Polyglot (i18n), +Researcher (insights) |
| DEV_EXPERIENCE | Hearth → Gear → Latch | — | +Anvil (CLI), +Sigil (project skills), +Hone (CLI audit) |
| LOAD_TEST | Siege → Bolt → Builder | Builder[fix], Radar[edge] | +Beacon (SLO), +Triage (resilience), +Matrix (scenario combos) |
| DEMO | Director/Reel → Quill | Forge[fullstack] | +Showcase (catalog), +Growth (marketing) |
| SPRINT_RETRO | Harvest → Canvas | — | +Quill (publish), +Triage (incident link) |
| KNOWLEDGE | Scribe → Prism | — | +Quill (polish), +Morph (format convert) |
| AITUBER | Cast → Aether → Builder | Builder[api] | +Artisan (avatar UI), +Scaffold (infra), +Beacon (monitoring) |
| REVIEW | Judge → Builder | Judge[pr], Builder[fix] | +Zen (refactor), +Sentinel (security), +Matrix (impact dimensions), +Flux (blind-spot) |
| YAGNI | Void → Sweep/Zen | — | +Magi (approval), +Pulse (usage data) |
| REMEDIATE | Mend → Radar | Radar[regression] | +Beacon (SLO check), +Gear (infra config), +Triage (escalation) |
| SPEC_VERIFY | Attest | Radar[coverage] | +Scribe (spec gaps), +Radar (BDD→tests), +Builder (violation fixes), +Warden (release gate) |
| LOOP_OPS | Orbit | Builder[fix], Radar[coverage] | +Builder (script changes), +Guardian (commit policy), +Radar (verification closure) |
| GAME | Quest → Forge → Builder → Radar | Forge[fullstack], Builder[api], Radar[edge] | +Tone (audio), +Dot (pixel), +Clay (3D), +Lyric (music), +Saga (narrative), +Matrix (balance) |
| DESIGN | Frame → Artisan → Radar | Forge[ui], Radar[edge] | +Muse (tokens), +Loom (guidelines), +Vision (direction), +Forge (prototype) |
| DESIGN_WORKFLOW | Atelier (orchestrator) | Forge[ui], Forge[fullstack] | Full design→code loop: Vision → Muse/Frame → Forge → Artisan → Showcase → Canvas. Persists design system to `.agents/design-system/`. Use when the task spans design direction + tokens + prototype + implementation + catalog in a single pipeline |
| ARCHITECTURE | Stratum → Canvas | — | +Lens (analysis), +Atlas (review), +Scribe (docs), +Ripple (impact) |
| CREATIVE | Vision → Sketch → Artisan | — | +Clay (3D), +Dot (pixel), +Growth (marketing) |
| MOCKUP | Pixel → Radar | Radar[coverage] | +Frame (Figma source), +Muse (tokens), +Flow (animations), +Warden (fidelity gate) |
| DESIGN_AUDIT | Pixel[gap-report] → Canon/Judge | Judge[intent] | +Artisan (remediation), +Muse (token regression), +Voyager (VRT baseline). Trigger: "gap analysis", "fidelity audit", "design review". Produces 8-dim × 5-severity × 9-RC Markdown+JSON report with visual artifacts |
| BRANDING | Crest → Quill | — | +Growth (SEO/SMO), +Canvas (viz), +Prose (content), +Harvest (portfolio) |
| BUSINESS | Levy → Scribe | Builder[ddd] | +Schema (data), +Builder (calc), +Canvas (flow) |
| ECOSYSTEM | Darwin → Gauge → Canvas | — | +Architect (design), +Realm (viz), +Void (prune), +Lore (knowledge) |
| PRIVACY | Cloak → Builder → Radar | Sentinel[scan], Builder[fix], Radar[edge] | +Comply (regulatory), +Sentinel (static scan), +Canon (standards) |
| COMPLIANCE | Comply → Builder → Radar | Sentinel[scan], Builder[fix], Radar[coverage] | +Cloak (privacy), +Canon (standards), +Scribe (policy docs) |
| CRYPTO | Crypt → Builder → Radar | Sentinel[scan], Builder[fix], Radar[edge] | +Sentinel (security review), +Probe (TLS validation) |
| VIDEO_SCRIPT | Cue → Director/Reel | — | +Prose (copy), +Growth (marketing), +Canvas (storyboard) |
| LEGACY | Fossil → Shift → Builder | Builder[harden], Radar[coverage] | +Rewind (git history), +Lens (exploration), +Tome (documentation) |
| LANDING_PAGE | Funnel → Artisan → Radar | Forge[landing], Radar[edge] | +Growth (SEO/CRO), +Prose (copy), +Pixel (mockup), +Echo (persona test) |
| FINOPS | Ledger → Scaffold → Gear | — | +Pulse (metrics), +Beacon (monitoring), +Canvas (dashboard spec) |
| TEST_DATA | Mint → Radar | Radar[coverage] | +Schema (DB fixtures), +Siege (load data), +Builder (factory impl) |
| SEARCH | Seek → Builder → Radar | Builder[api], Radar[edge] | +Oracle (RAG/embeddings), +Schema (indexes), +Tuner (query perf) |
| MULTI_TENANT | Shard → Schema → Builder | Sentinel[scan], Builder[ddd], Radar[edge] | +Sentinel (security), +Scaffold (infra), +Radar (isolation tests) |
| MIGRATION | Shift → Builder → Radar | Builder[harden], Radar[regression] | +Fossil (legacy analysis), +Horizon (modernize), +Rewind (history) |
| PRESENTATION | Stage → Canvas | — | +Cue (narrative), +Quill (content), +Morph (export) |
| LEARNING | Tome → Quill | — | +Canvas (diagrams), +Rewind (change context), +Prism (audio) |
| WORKFLOW | Weave → Builder → Radar | Builder[api], Radar[edge] | +Canvas (diagram), +Schema (persistence), +Attest (spec verify) |
| ARTICLE | Zine → Growth | — | +Prose (microcopy polish), +Stage (slide version), +Saga (narrative reshape), +Canvas (article diagrams), +Morph (PDF/Word export), +Tome (diff → learning source). Trigger: "tech blog", "note/Zenn/Qiita/dev.to", "連載", "記事" |
| SCHEDULE | Tempo → Builder → Gear | Builder[api], Radar[edge] | +Weave (retry state machine), +Beacon (schedule SLO/alerts), +Pipe (GHA cron), +Voyager (temporal test scenarios), +Judge (correctness review), +Triage (incident → replay plan). Trigger: "cron", "timezone", "DST", "retry/backoff", "backfill", "business calendar" |
| GRAMMAR | Grok → Builder → Radar | Builder[crud], Sentinel[injection], Radar[edge] | +Sentinel (regex security audit), +Canon (grammar → standards compliance), +Atlas (parser module boundary), +Shift (codemod migration), +Judge (grammar review). Trigger: "regex", "parser", "grammar", "DSL design", "AST transform", "ReDoS" |
| DAILY_IDEA | Dawn | Forge[ui], Forge[fullstack] | +Forge (prototype), +Builder (production), +Zine (article). Trigger: "今日のアイデア", "毎朝のアイデア", "週末ハック", "副業プロジェクト案", "コーディングエージェントに渡せる題材". Don't confuse with Spark (existing-product feature proposals) |
