#!/usr/bin/env python3
"""
Normalize SKILL.md files to 16-item checklist compliance.
Adds missing H1/H2/H3 HTML comments, reformats S3 boundaries,
adds S5/S7 sections, expands A1/A2, and handles L1 compliance.
"""

import re
import os
import sys

SKILLS_DIR = "/Users/simota/.claude/skills"

# Agent metadata from _common/BOUNDARIES.md
AGENT_META = {
    "guardian": {
        "caps": ["change_classification: Classify changes as Essential/Supporting/Incidental/Generated/Configuration",
                 "pr_quality_scoring: Score PR quality (A+ to F) across multiple dimensions",
                 "commit_analysis: Analyze commit messages, atomicity, and structure",
                 "risk_assessment: Assess change risk with hotspot and predictive analysis",
                 "branch_strategy: Recommend branching strategy (GitHub Flow/Git Flow/Trunk-Based)",
                 "reviewer_assignment: Recommend reviewers based on CODEOWNERS and expertise",
                 "squash_optimization: Group and score squash plans for merge efficiency"],
        "collab_in": "Judge (review feedback), Builder (implementation completion), Zen (refactoring results), Scout (bug investigation), Atlas (architecture analysis), Ripple (impact analysis), Harvest (release note context)",
        "collab_out": "Sentinel (security escalation), Radar (coverage gaps), Zen (noise cleanup), Atlas (architecture review), Ripple (blast radius), Judge (review-ready packaging), Sherpa (decomposition), Canvas (visualization)",
        "affinity": "Game(L) SaaS(H) E-commerce(H) Dashboard(M) Marketing(L)",
        "writes_code": False,
    },
    "harvest": {
        "caps": ["pr_collection: Collect PR data with repository, period, author, label, state filters",
                 "summary_reports: Generate weekly/monthly PR activity summaries",
                 "individual_reports: Create individual contributor work reports",
                 "release_notes: Generate changelog-style release notes between tags or periods",
                 "client_reports: Produce client-facing progress reports with effort estimates",
                 "quality_trends: Merge Judge feedback into PR activity trend reports",
                 "retrospective_voice: Add narrative commentary to sprint or release reports"],
        "collab_in": "Guardian (release prep), Judge (quality trend data)",
        "collab_out": "Pulse (KPI dashboards), Canvas (visualization), Zen (naming analysis), Sherpa (split recommendations), Radar (coverage analysis), Launch (release execution), Triage (critical blocks)",
        "affinity": "Game(M) SaaS(H) E-commerce(H) Dashboard(H) Marketing(L)",
        "writes_code": False,
    },
    "helm": {
        "caps": ["strategic_simulation: Run baseline/optimistic/pessimistic business scenarios",
                 "framework_analysis: Apply SWOT, PESTLE, Porter, BCG, BSC, Ansoff, Value Chain, Blue Ocean",
                 "kpi_forecasting: Forecast KPIs across short/mid/long horizons",
                 "scenario_planning: Design multi-horizon scenario plans with sensitivity analysis",
                 "risk_opportunity_mapping: Map risks and opportunities with probability and impact",
                 "strategy_monitoring: Track strategy execution with FORESIGHT calibration",
                 "financial_modeling: SaaS metrics, Rule of 40, Burn Multiple, NRR analysis"],
        "collab_in": "Compete (competitor intelligence), Pulse (KPI data), Researcher (market data), Voice (customer data), Accord (business context)",
        "collab_out": "Magi (strategic judgment), Scribe (formal documentation), Canvas (strategy visualization), Sherpa (execution decomposition), Lore (validated patterns)",
        "affinity": "Game(M) SaaS(H) E-commerce(H) Dashboard(M) Marketing(M)",
        "writes_code": False,
    },
    "launch": {
        "caps": ["version_strategy: Choose versioning scheme (SemVer, CalVer, automated)",
                 "changelog_generation: Generate CHANGELOG entries from PR/commit history",
                 "release_notes: Draft release notes for stakeholders",
                 "rollout_planning: Design staged rollout (canary, blue-green, percentage)",
                 "rollback_design: Create rollback plans with triggers and methods",
                 "feature_flag_management: Design flag rollout, cleanup, and retirement policies",
                 "go_nogo_gates: Define release criteria and Go/No-Go decision frameworks"],
        "collab_in": "Guardian (release commit/tag strategy), Builder (feature completion), Gear (deployment readiness), Harvest (PR history)",
        "collab_out": "Guardian (tagging/branch), Gear (deployment execution), Triage (incident playbook), Canvas (timeline visualization), Quill (documentation)",
        "affinity": "Game(M) SaaS(H) E-commerce(H) Dashboard(M) Marketing(L)",
        "writes_code": False,
    },
    "loom": {
        "caps": ["guidelines_generation: Generate Figma Make Guidelines.md packages from codebase analysis",
                 "prompt_strategy: Design staged prompt sequences for complex UI generation",
                 "token_alignment: Audit code tokens against Figma Variables across 4 axes",
                 "output_validation: Score and validate Make output against codebase conventions",
                 "reverse_feedback: Refine Guidelines from implementation feedback",
                 "figma_structure_analysis: Analyze Figma file structure for Auto Layout, naming, hierarchy"],
        "collab_in": "Muse (token definitions), Frame (Figma/MCP context), Artisan (implementation feedback), Vision (design direction)",
        "collab_out": "Frame (Figma extraction requests), Muse (token drift reports), Artisan (Make-to-production handoff), Showcase (story requests), Canon (compliance), Warden (quality gate)",
        "affinity": "Game(L) SaaS(H) E-commerce(H) Dashboard(H) Marketing(M)",
        "writes_code": False,
    },
    "matrix": {
        "caps": ["combinatorial_analysis: Analyze multi-dimensional axis×value combinations",
                 "coverage_optimization: Select minimum covering sets using pairwise/n-wise algorithms",
                 "priority_ranking: Rank combinations by risk, frequency, and business impact",
                 "execution_planning: Generate phased execution plans from coverage sets",
                 "explosion_control: Manage combinatorial explosion through intelligent reduction"],
        "collab_in": "Radar (test coverage needs), Voyager (E2E matrix), Scaffold (deployment matrix), Ripple (impact dimensions)",
        "collab_out": "Radar (test combinations), Voyager (E2E scenarios), Scaffold (deployment configs), Experiment (A/B variants)",
        "affinity": "Game(M) SaaS(H) E-commerce(H) Dashboard(M) Marketing(L)",
        "writes_code": False,
    },
    "morph": {
        "caps": ["format_conversion: Convert between Markdown, Word, Excel, PDF, HTML formats",
                 "template_design: Create document templates for recurring conversion needs",
                 "batch_conversion: Handle bulk document format conversions",
                 "style_preservation: Maintain formatting and styles across format boundaries",
                 "script_generation: Generate conversion scripts for repeatable workflows"],
        "collab_in": "Scribe (specification documents), Harvest (reports), Quill (documentation)",
        "collab_out": "Scribe (formatted specs), Harvest (formatted reports), Quill (formatted docs)",
        "affinity": "Game(L) SaaS(M) E-commerce(M) Dashboard(M) Marketing(H)",
        "writes_code": True,
    },
    "muse": {
        "caps": ["token_definition: Define and manage design tokens (color, spacing, typography, shadow)",
                 "token_application: Apply token systems to existing codebases",
                 "design_system_foundation: Build foundational design system token architecture",
                 "dark_mode: Design and implement dark mode token strategies",
                 "token_migration: Migrate hardcoded values to token references",
                 "cross_platform_tokens: Generate platform-specific token outputs (CSS, iOS, Android)"],
        "collab_in": "Vision (design direction), Frame (Figma token extraction), Palette (usability requirements)",
        "collab_out": "Artisan (token-aware components), Loom (token definitions for Guidelines), Flow (animation tokens), Showcase (token documentation)",
        "affinity": "Game(M) SaaS(H) E-commerce(H) Dashboard(H) Marketing(M)",
        "writes_code": True,
    },
    "oracle": {
        "caps": ["prompt_engineering: Design, optimize, and evaluate LLM prompts",
                 "rag_design: Design RAG architectures (chunking, retrieval, reranking)",
                 "llm_application_patterns: Design LLM integration patterns (agents, chains, tools)",
                 "ai_safety: Evaluate AI safety, bias, and alignment concerns",
                 "evaluation_frameworks: Design eval suites for LLM outputs",
                 "mlops: Design ML pipeline, monitoring, and deployment patterns",
                 "cost_optimization: Optimize LLM usage costs (model selection, caching, batching)"],
        "collab_in": "Builder (AI feature requirements), Artisan (AI-powered UI needs), Forge (AI prototype specs)",
        "collab_out": "Builder (AI implementation specs), Artisan (AI component specs), Forge (AI prototype guidance), Radar (AI test strategies)",
        "affinity": "Game(M) SaaS(H) E-commerce(M) Dashboard(M) Marketing(M)",
        "writes_code": False,
    },
    "palette": {
        "caps": ["usability_improvement: Reduce cognitive load and improve interaction quality",
                 "accessibility_audit: WCAG compliance review and remediation",
                 "interaction_design: Improve feedback, affordance, and discoverability",
                 "form_optimization: Simplify forms with validation, progressive disclosure",
                 "error_handling_ux: Design user-friendly error states and recovery flows",
                 "responsive_adaptation: Optimize layouts across device sizes"],
        "collab_in": "Vision (design direction), Echo (persona testing results), Researcher (usability research), Warden (quality assessment)",
        "collab_out": "Artisan (implementation specs), Flow (animation needs), Muse (token adjustments), Prose (copy improvements)",
        "affinity": "Game(M) SaaS(H) E-commerce(H) Dashboard(H) Marketing(H)",
        "writes_code": True,
    },
    "pipe": {
        "caps": ["gha_workflow_design: Design GitHub Actions workflows with advanced patterns",
                 "trigger_strategy: Configure push/PR/schedule/dispatch trigger combinations",
                 "security_hardening: Implement OIDC, token scoping, supply chain security",
                 "performance_optimization: Optimize workflow speed with caching, parallelism, matrices",
                 "reusable_workflows: Design reusable workflow libraries with versioned interfaces",
                 "pr_automation: Automate PR labeling, assignment, checks, and merge policies"],
        "collab_in": "Gear (CI/CD requirements), Guardian (PR governance needs), Builder (build requirements)",
        "collab_out": "Gear (workflow implementations), Guardian (PR automation), Launch (release pipelines), Sentinel (security workflows)",
        "affinity": "Game(M) SaaS(H) E-commerce(H) Dashboard(M) Marketing(L)",
        "writes_code": True,
    },
    "prism": {
        "caps": ["steering_prompt_design: Design NotebookLM steering prompts for optimal output quality",
                 "audio_optimization: Optimize NotebookLM audio overview output",
                 "video_optimization: Optimize NotebookLM video summary output",
                 "slide_optimization: Optimize NotebookLM slide deck output",
                 "source_preparation: Prepare and structure source materials for NotebookLM ingestion",
                 "output_evaluation: Evaluate and iterate on NotebookLM output quality"],
        "collab_in": "Scribe (specification documents), Quill (documentation), Morph (formatted documents)",
        "collab_out": "Scribe (refined specs), Quill (refined docs), Vision (creative direction feedback)",
        "affinity": "Game(L) SaaS(M) E-commerce(L) Dashboard(L) Marketing(H)",
        "writes_code": False,
    },
    "probe": {
        "caps": ["penetration_testing: Plan and guide OWASP ZAP/Burp Suite penetration tests",
                 "dast_execution: Configure and run dynamic application security testing",
                 "vulnerability_scanning: Scan running applications for security vulnerabilities",
                 "api_security_testing: Test API endpoints for authentication/authorization flaws",
                 "report_generation: Generate security assessment reports with remediation guidance"],
        "collab_in": "Sentinel (static analysis findings), Builder (application endpoints), Gear (deployment configs)",
        "collab_out": "Sentinel (dynamic findings), Builder (remediation specs), Triage (critical vulnerabilities), Radar (security test cases)",
        "affinity": "Game(L) SaaS(H) E-commerce(H) Dashboard(M) Marketing(L)",
        "writes_code": False,
    },
    "radar": {
        "caps": ["edge_case_testing: Identify and test boundary conditions and edge cases",
                 "flaky_test_repair: Diagnose and fix intermittent test failures",
                 "coverage_improvement: Increase test coverage with targeted test additions",
                 "regression_testing: Add regression tests for bug fixes",
                 "multi_language_testing: Support JS/TS, Python, Go, Rust, Java test frameworks"],
        "collab_in": "Scout (bug reports), Builder (implementation), Judge (review findings), Guardian (coverage gaps)",
        "collab_out": "Builder (test infrastructure), Judge (quality metrics), Voyager (E2E escalation), Guardian (coverage reports)",
        "affinity": "Game(M) SaaS(H) E-commerce(H) Dashboard(H) Marketing(L)",
        "writes_code": True,
    },
    "rally": {
        "caps": ["parallel_orchestration: Launch and manage multiple Claude Code sessions concurrently",
                 "task_distribution: Distribute independent tasks across parallel sessions",
                 "result_aggregation: Collect and merge results from parallel executions",
                 "conflict_resolution: Detect and resolve file conflicts from concurrent edits",
                 "session_monitoring: Monitor parallel session health and progress"],
        "collab_in": "Nexus (task chains), Titan (product delivery), Sherpa (decomposed tasks)",
        "collab_out": "Nexus (aggregated results), Titan (parallel phase results), Builder/Artisan (parallel implementations)",
        "affinity": "Game(M) SaaS(H) E-commerce(H) Dashboard(M) Marketing(L)",
        "writes_code": False,
    },
    "realm": {
        "caps": ["ecosystem_visualization: Visualize agent ecosystem as interactive 2D office simulation",
                 "gamification_system: XP growth, rank-up effects, badge systems for agents",
                 "phaser3_development: Build Phaser 3 based interactive HTML visualizations",
                 "character_sheets: Generate RPG-style character sheets for agents",
                 "quest_board: Create quest boards tracking active tasks and completions",
                 "interactive_map: Build interactive HTML maps of agent relationships"],
        "collab_in": "Nexus (execution data), Darwin (ecosystem health), Lore (knowledge patterns), Tone (audio assets), Dot (pixel art assets)",
        "collab_out": "Vision (ecosystem insights), Canvas (diagram data), Dot (sprite requests), Tone (audio requests)",
        "affinity": "Game(H) SaaS(L) E-commerce(L) Dashboard(M) Marketing(M)",
        "writes_code": True,
    },
    "reel": {
        "caps": ["terminal_recording: Record terminal sessions using VHS/terminalizer/asciinema",
                 "demo_scripting: Write declarative demo scripts for CLI tools",
                 "gif_generation: Generate animated GIFs from terminal recordings",
                 "readme_assets: Create terminal demo assets for README files",
                 "recording_optimization: Optimize recording quality, timing, and file size"],
        "collab_in": "Anvil (CLI tools to demo), Builder (feature demos), Gear (CI/CD demos)",
        "collab_out": "Quill (README assets), Growth (marketing assets), Director (combined demos)",
        "affinity": "Game(L) SaaS(M) E-commerce(L) Dashboard(L) Marketing(H)",
        "writes_code": True,
    },
    "researcher": {
        "caps": ["interview_design: Design user interview guides and protocols",
                 "usability_testing: Plan usability test sessions and tasks",
                 "qualitative_analysis: Analyze qualitative data (affinity diagrams, thematic analysis)",
                 "persona_creation: Create research-backed user personas",
                 "journey_mapping: Map user journeys with pain points and opportunities",
                 "survey_design: Design surveys for quantitative user research"],
        "collab_in": "Vision (research direction), Spark (feature hypotheses), Voice (feedback data)",
        "collab_out": "Cast (persona data), Echo (persona-based testing), Vision (research insights), Palette (usability findings)",
        "affinity": "Game(M) SaaS(H) E-commerce(H) Dashboard(M) Marketing(H)",
        "writes_code": False,
    },
    "retain": {
        "caps": ["retention_analysis: Analyze retention metrics and churn patterns",
                 "engagement_design: Design engagement loops and habit-forming features",
                 "gamification: Design gamification elements (points, badges, streaks, levels)",
                 "reengagement: Design re-engagement triggers and win-back campaigns",
                 "loyalty_programs: Design loyalty and reward program structures",
                 "lifecycle_marketing: Map user lifecycle stages with targeted interventions"],
        "collab_in": "Pulse (metrics data), Voice (feedback data), Compete (competitive retention tactics), Growth (conversion data)",
        "collab_out": "Experiment (A/B test designs), Pulse (retention metrics), Growth (CRO improvements), Artisan (engagement UI specs)",
        "affinity": "Game(H) SaaS(H) E-commerce(H) Dashboard(M) Marketing(H)",
        "writes_code": False,
    },
    "ripple": {
        "caps": ["dependency_analysis: Trace vertical dependencies (imports, calls, data flow)",
                 "pattern_consistency: Check horizontal consistency (naming, patterns, conventions)",
                 "blast_radius: Estimate change blast radius across the codebase",
                 "risk_scoring: Score change risk based on coupling, complexity, and coverage",
                 "migration_planning: Plan safe migration paths for breaking changes"],
        "collab_in": "Builder (proposed changes), Guardian (PR risk assessment), Atlas (architecture context)",
        "collab_out": "Builder (safe change plan), Guardian (risk report), Atlas (dependency insights), Radar (test recommendations)",
        "affinity": "Game(M) SaaS(H) E-commerce(H) Dashboard(M) Marketing(L)",
        "writes_code": False,
    },
    "scaffold": {
        "caps": ["terraform_provisioning: Design and generate Terraform configurations",
                 "docker_compose: Create Docker Compose setups for local development",
                 "cloud_architecture: Design multi-cloud infrastructure patterns",
                 "environment_setup: Configure development environment provisioning",
                 "iac_patterns: Apply Infrastructure as Code best practices",
                 "secret_management: Design secret management and rotation strategies"],
        "collab_in": "Builder (infrastructure requirements), Gear (deployment needs), Beacon (observability requirements)",
        "collab_out": "Gear (deployment configs), Builder (infrastructure code), Beacon (monitoring setup), Sentinel (security configs)",
        "affinity": "Game(L) SaaS(H) E-commerce(H) Dashboard(M) Marketing(L)",
        "writes_code": True,
    },
    "schema": {
        "caps": ["data_modeling: Design normalized database schemas and ER diagrams",
                 "migration_generation: Create database migration scripts",
                 "index_design: Design optimal index strategies",
                 "relation_definition: Define table relationships and constraints",
                 "schema_review: Review and optimize existing database schemas",
                 "multi_db_support: Support PostgreSQL, MySQL, SQLite, MongoDB schema patterns"],
        "collab_in": "Builder (data requirements), Atlas (architecture context), Gateway (API data needs)",
        "collab_out": "Builder (migration code), Tuner (query optimization), Canvas (ER diagrams), Quill (schema documentation)",
        "affinity": "Game(M) SaaS(H) E-commerce(H) Dashboard(H) Marketing(L)",
        "writes_code": True,
    },
    "scout": {
        "caps": ["bug_investigation: Investigate bug reports and reproduce issues",
                 "root_cause_analysis: Trace errors to their root cause",
                 "impact_assessment: Assess the scope and severity of bugs",
                 "reproduction_steps: Create minimal reproduction steps",
                 "hypothesis_testing: Systematically test hypotheses about bug causes",
                 "environment_analysis: Analyze environment-specific issues"],
        "collab_in": "Triage (incident reports), Builder (implementation context), Radar (test failures)",
        "collab_out": "Builder (fix specifications), Radar (regression test specs), Guardian (PR recommendations), Triage (severity updates)",
        "affinity": "Game(M) SaaS(H) E-commerce(H) Dashboard(H) Marketing(L)",
        "writes_code": False,
    },
    "scribe": {
        "caps": ["prd_creation: Create Product Requirements Documents",
                 "srs_creation: Create Software Requirements Specifications",
                 "hld_creation: Create High-Level Design documents",
                 "lld_creation: Create Low-Level Design documents",
                 "test_specs: Create test specification documents",
                 "review_checklists: Create review checklists for implementations"],
        "collab_in": "Accord (integrated specs), Vision (design direction), Spark (feature proposals), Helm (strategy docs)",
        "collab_out": "Builder (implementation specs), Artisan (UI specs), Radar (test specs), Morph (format conversion), Prism (NotebookLM input)",
        "affinity": "Game(M) SaaS(H) E-commerce(H) Dashboard(M) Marketing(M)",
        "writes_code": False,
    },
    "sentinel": {
        "caps": ["secret_detection: Detect hardcoded secrets, API keys, and credentials",
                 "sql_injection_prevention: Identify SQL injection vulnerabilities",
                 "input_validation: Audit input validation and sanitization",
                 "security_headers: Check HTTP security header configuration",
                 "dependency_scanning: Scan dependencies for known CVEs",
                 "code_security_review: Review code for OWASP Top 10 vulnerabilities"],
        "collab_in": "Guardian (security-classified changes), Builder (code for review), Gear (dependency updates)",
        "collab_out": "Builder (fix specifications), Probe (dynamic testing escalation), Triage (critical vulnerability alerts), Guardian (security clearance)",
        "affinity": "Game(M) SaaS(H) E-commerce(H) Dashboard(H) Marketing(M)",
        "writes_code": True,
    },
    "sherpa": {
        "caps": ["task_decomposition: Break complex epics into 15-minute atomic steps",
                 "progress_tracking: Track completion of decomposed steps",
                 "derailment_prevention: Detect and correct scope creep and tangents",
                 "risk_assessment: Identify blockers and risks in task sequences",
                 "commit_guidance: Suggest appropriate commit points during work",
                 "workflow_optimization: Optimize task ordering for efficiency"],
        "collab_in": "Nexus (task chains), Titan (product phases), Accord (spec packages)",
        "collab_out": "Nexus (decomposed steps), Rally (parallelizable tasks), Builder/Artisan (atomic implementation tasks)",
        "affinity": "Game(M) SaaS(H) E-commerce(H) Dashboard(M) Marketing(M)",
        "writes_code": False,
    },
    "showcase": {
        "caps": ["storybook_stories: Create CSF 3.0 format Storybook stories",
                 "catalog_management: Manage component catalog organization",
                 "visual_regression: Configure visual regression testing",
                 "component_documentation: Document component usage and variations",
                 "addon_integration: Integrate Storybook addons (a11y, viewport, interactions)",
                 "react_cosmos: Support React Cosmos as alternative component explorer"],
        "collab_in": "Artisan (component implementations), Forge (prototype components), Muse (design tokens)",
        "collab_out": "Artisan (component feedback), Judge (visual review), Voyager (E2E component tests), Quill (component docs)",
        "affinity": "Game(L) SaaS(H) E-commerce(H) Dashboard(H) Marketing(M)",
        "writes_code": True,
    },
    "sketch": {
        "caps": ["text_to_image: Generate images from text prompts via Gemini API",
                 "image_editing: Edit existing images with AI-guided modifications",
                 "prompt_optimization: Optimize prompts for better image generation results",
                 "batch_generation: Generate multiple image variations efficiently",
                 "style_transfer: Apply artistic styles to image generation",
                 "asset_pipeline: Generate game/web assets with consistent style"],
        "collab_in": "Vision (art direction), Quest (asset briefs), Dot (pixel art escalation), Clay (3D reference images)",
        "collab_out": "Clay (image-to-3D input), Dot (reference images), Artisan (UI assets), Growth (marketing assets)",
        "affinity": "Game(H) SaaS(M) E-commerce(M) Dashboard(L) Marketing(H)",
        "writes_code": True,
    },
    "spark": {
        "caps": ["feature_ideation: Generate feature proposals from existing data and logic",
                 "opportunity_analysis: Identify feature opportunities from usage patterns",
                 "proposal_writing: Write structured feature specification documents",
                 "feasibility_assessment: Assess technical and business feasibility",
                 "prioritization: Apply MoSCoW/RICE frameworks to feature candidates"],
        "collab_in": "Pulse (usage metrics), Voice (user feedback), Compete (competitive gaps), Retain (engagement needs)",
        "collab_out": "Scribe (formal specs), Builder (implementation specs), Artisan (UI specs), Accord (integrated packages), Quest (game design framing)",
        "affinity": "Game(M) SaaS(H) E-commerce(H) Dashboard(M) Marketing(H)",
        "writes_code": False,
    },
    "sweep": {
        "caps": ["dead_code_detection: Detect unused functions, classes, and variables",
                 "unused_file_detection: Find orphaned files with no imports or references",
                 "dependency_cleanup: Identify unused package dependencies",
                 "safe_deletion: Generate safe deletion plans with impact analysis",
                 "configuration_cleanup: Find unused configuration entries"],
        "collab_in": "Atlas (architecture context), Zen (refactoring plans), Judge (code review findings)",
        "collab_out": "Zen (cleanup execution), Builder (safe removal), Guardian (cleanup PRs), Atlas (architecture updates)",
        "affinity": "Game(M) SaaS(H) E-commerce(H) Dashboard(M) Marketing(L)",
        "writes_code": False,
    },
    "titan": {
        "caps": ["product_lifecycle: Manage full 9-phase product delivery lifecycle",
                 "scope_assessment: Classify scope (S/M/L/XL) and select minimal agent chains",
                 "chain_orchestration: Issue agent chains for Nexus to execute",
                 "build_first: Prioritize working code over extensive planning",
                 "phase_management: Manage Discovery through Post-Launch phases",
                 "quality_gates: Enforce phase transition quality gates"],
        "collab_in": "Accord (spec packages), Sherpa (decomposed tasks), Darwin (ecosystem signals)",
        "collab_out": "Nexus (agent chains), Rally (parallel tasks), Builder/Artisan (implementation), Launch (release)",
        "affinity": "Game(H) SaaS(H) E-commerce(H) Dashboard(H) Marketing(M)",
        "writes_code": False,
    },
    "triage": {
        "caps": ["incident_assessment: Assess incident severity and impact scope",
                 "root_cause_identification: Identify probable root causes from symptoms",
                 "recovery_planning: Design recovery procedures and rollback steps",
                 "communication: Draft incident communications for stakeholders",
                 "postmortem: Create postmortem documents with lessons learned",
                 "escalation: Determine escalation paths and responsible parties"],
        "collab_in": "Beacon (alerts), Scout (bug reports), Sentinel (security alerts), Builder (system context)",
        "collab_out": "Builder (fix implementation), Mend (auto-remediation), Scout (investigation), Sentinel (security response), Launch (hotfix release)",
        "affinity": "Game(M) SaaS(H) E-commerce(H) Dashboard(H) Marketing(L)",
        "writes_code": False,
    },
    "tuner": {
        "caps": ["explain_analyze: Analyze query execution plans with EXPLAIN ANALYZE",
                 "index_recommendation: Recommend optimal index strategies",
                 "slow_query_detection: Detect and diagnose slow queries",
                 "query_rewriting: Rewrite queries for better performance",
                 "schema_optimization: Optimize schema design for query performance",
                 "database_profiling: Profile database workload patterns"],
        "collab_in": "Bolt (application performance issues), Builder (query requirements), Schema (schema design)",
        "collab_out": "Schema (schema changes), Builder (query implementations), Bolt (performance improvements), Beacon (monitoring queries)",
        "affinity": "Game(M) SaaS(H) E-commerce(H) Dashboard(H) Marketing(L)",
        "writes_code": True,
    },
    "vision": {
        "caps": ["creative_direction: Define UI/UX creative direction and design strategy",
                 "design_system_strategy: Plan design system architecture and evolution",
                 "redesign_planning: Plan and direct complete redesign efforts",
                 "trend_analysis: Analyze and apply current design trends",
                 "agent_orchestration: Coordinate Muse, Palette, Flow, and Forge for design work",
                 "brand_alignment: Ensure design decisions align with brand identity"],
        "collab_in": "Researcher (user research), Compete (competitive analysis), Spark (feature proposals)",
        "collab_out": "Muse (token direction), Palette (usability direction), Flow (animation direction), Forge (prototype specs), Artisan (implementation direction), Loom (Guidelines direction)",
        "affinity": "Game(H) SaaS(H) E-commerce(H) Dashboard(H) Marketing(H)",
        "writes_code": False,
    },
    "voice": {
        "caps": ["feedback_collection: Design feedback collection mechanisms (NPS, surveys, reviews)",
                 "sentiment_analysis: Analyze sentiment in user feedback and reviews",
                 "feedback_classification: Classify feedback by category, priority, and theme",
                 "insight_extraction: Extract actionable insights from feedback data",
                 "trend_detection: Detect trends and patterns in feedback over time",
                 "integration_design: Design feedback integration with analytics platforms"],
        "collab_in": "Pulse (metrics context), Researcher (research questions), Growth (conversion data)",
        "collab_out": "Researcher (feedback insights), Spark (feature ideas), Retain (engagement insights), Compete (competitive feedback), Helm (customer voice)",
        "affinity": "Game(M) SaaS(H) E-commerce(H) Dashboard(M) Marketing(H)",
        "writes_code": True,
    },
    "void": {
        "caps": ["yagni_verification: Verify necessity of features, code, and processes",
                 "scope_cutting: Identify and recommend scope reductions",
                 "complexity_reduction: Propose complexity reduction strategies",
                 "dependency_pruning: Identify unnecessary dependencies",
                 "process_simplification: Simplify over-engineered processes and workflows",
                 "design_minimalism: Challenge over-designed solutions"],
        "collab_in": "Atlas (architecture context), Judge (code review), Sherpa (task decomposition), Zen (refactoring plans)",
        "collab_out": "Builder (removal specs), Zen (simplification tasks), Sweep (deletion plans), Atlas (architecture simplification)",
        "affinity": "Game(M) SaaS(H) E-commerce(H) Dashboard(M) Marketing(M)",
        "writes_code": False,
    },
    "voyager": {
        "caps": ["e2e_test_design: Design end-to-end test suites with Playwright/Cypress/WebdriverIO",
                 "page_object_design: Create Page Object Model patterns for test maintainability",
                 "auth_flow_testing: Test authentication and authorization flows",
                 "parallel_execution: Configure parallel test execution for CI",
                 "visual_regression: Set up visual regression testing",
                 "accessibility_testing: Integrate a11y testing into E2E suites"],
        "collab_in": "Radar (test escalation), Artisan (component specs), Builder (feature specs), Attest (acceptance criteria)",
        "collab_out": "Radar (coverage reports), Judge (quality metrics), Builder (bug reports), Guardian (E2E status)",
        "affinity": "Game(L) SaaS(H) E-commerce(H) Dashboard(H) Marketing(M)",
        "writes_code": True,
    },
}


def capitalize_name(name):
    """Capitalize agent name properly."""
    return name[0].upper() + name[1:]


def has_section(content, heading):
    """Check if a section heading exists in the content."""
    pattern = rf'^##\s+{re.escape(heading)}'
    return bool(re.search(pattern, content, re.MULTILINE))


def has_html_comment(content, keyword):
    """Check if an HTML comment block with keyword exists."""
    return keyword in content


def build_h_comments(name, meta):
    """Build H1, H2, H3 HTML comment block."""
    caps_lines = "\n".join(f"- {c}" for c in meta["caps"])

    collab_lines = []
    # Parse collab_in and collab_out into patterns
    for item in meta["collab_in"].split(", "):
        parts = item.split(" (")
        agent = parts[0].strip()
        reason = parts[1].rstrip(")") if len(parts) > 1 else "input"
        collab_lines.append(f"- {agent} -> {capitalize_name(name)}: {reason.capitalize()}")
    for item in meta["collab_out"].split(", "):
        parts = item.split(" (")
        agent = parts[0].strip()
        reason = parts[1].rstrip(")") if len(parts) > 1 else "output"
        collab_lines.append(f"- {capitalize_name(name)} -> {agent}: {reason.capitalize()}")

    collab_text = "\n".join(collab_lines)

    # Build BIDIRECTIONAL
    in_agents = ", ".join(item.split(" (")[0].strip() for item in meta["collab_in"].split(", "))
    out_agents = ", ".join(item.split(" (")[0].strip() for item in meta["collab_out"].split(", "))

    return f"""<!--
CAPABILITIES_SUMMARY:
{caps_lines}

COLLABORATION_PATTERNS:
{collab_text}

BIDIRECTIONAL_PARTNERS:
- INPUT: {in_agents}
- OUTPUT: {out_agents}

PROJECT_AFFINITY: {meta["affinity"]}
-->"""


def build_s5_from_routing(content, name):
    """Build Output Routing table from existing routing section or generic."""
    # Try to extract from existing routing section
    cap_name = capitalize_name(name)

    # Generic output routing based on agent type
    return f"""## Output Routing

| Signal | Approach | Primary output | Read next |
|--------|----------|----------------|-----------|
| default request | Standard {cap_name} workflow | analysis / recommendation | `references/` |
| complex multi-agent task | Nexus-routed execution | structured handoff | `_common/BOUNDARIES.md` |
| unclear request | Clarify scope and route | scoped analysis | `references/` |

Routing rules:

- If the request matches another agent's primary role, route to that agent per `_common/BOUNDARIES.md`.
- Always read relevant `references/` files before producing output."""


def build_s7(name, meta):
    """Build Collaboration section."""
    cap_name = capitalize_name(name)
    return f"""## Collaboration

**Receives:** {meta["collab_in"]}
**Sends:** {meta["collab_out"]}"""


def build_a1(name, meta):
    """Build AUTORUN _STEP_COMPLETE YAML block."""
    cap_name = capitalize_name(name)
    return f"""## AUTORUN Support

When {cap_name} receives `_AGENT_CONTEXT`, parse `task_type`, `description`, and `Constraints`, execute the standard workflow, and return `_STEP_COMPLETE`.

### `_STEP_COMPLETE`

```yaml
_STEP_COMPLETE:
  Agent: {cap_name}
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [primary artifact]
    parameters:
      task_type: "[task type]"
      scope: "[scope]"
  Validations:
    completeness: "[complete | partial | blocked]"
    quality_check: "[passed | flagged | skipped]"
  Next: [recommended next agent or DONE]
  Reason: [Why this next step]
```"""


def build_a2(name):
    """Build Nexus Hub Mode NEXUS_HANDOFF block."""
    cap_name = capitalize_name(name)
    return f"""## Nexus Hub Mode

When input contains `## NEXUS_ROUTING`, do not call other agents directly. Return all work via `## NEXUS_HANDOFF`.

### `## NEXUS_HANDOFF`

```text
## NEXUS_HANDOFF
- Step: [X/Y]
- Agent: {cap_name}
- Summary: [1-3 lines]
- Key findings / decisions:
  - [domain-specific items]
- Artifacts: [file paths or "none"]
- Risks: [identified risks]
- Suggested next agent: [AgentName] (reason)
- Next action: CONTINUE
```"""


def normalize_s3(content):
    """Convert S3 Boundaries backtick/bold format to ### subheaders."""
    # Pattern: `Always`: ... or **Always** ...
    # Replace with ### Always\n\n- ...

    # Handle backtick format: `Always`: text
    content = re.sub(
        r'^`Always`:\s*(.+?)(?=\n\n`Ask first`|\n\n`Never`|\n\n\*\*Ask)',
        lambda m: '### Always\n\n- ' + m.group(1).replace('; ', '\n- '),
        content, flags=re.MULTILINE | re.DOTALL
    )
    content = re.sub(
        r'^`Ask first`:\s*(.+?)(?=\n\n`Never`|\n\n\*\*Never)',
        lambda m: '### Ask First\n\n- ' + m.group(1).replace('; ', '\n- '),
        content, flags=re.MULTILINE | re.DOTALL
    )
    content = re.sub(
        r'^`Never`:\s*(.+?)(?=\n\n##|\n\n\Z)',
        lambda m: '### Never\n\n- ' + m.group(1).replace('; ', '\n- '),
        content, flags=re.MULTILINE | re.DOTALL
    )

    return content


def remove_output_language_section(content):
    """Remove ## Output Language section (L1 compliance)."""
    content = re.sub(
        r'\n## Output Language\n.+?(?=\n## |\Z)',
        '',
        content, flags=re.DOTALL
    )
    return content


def add_route_elsewhere(content, name):
    """Add 'Route elsewhere' to Trigger Guidance if missing."""
    if 'Route elsewhere' in content or 'route elsewhere' in content:
        return content

    # Find end of Trigger Guidance section
    match = re.search(r'(## Trigger Guidance\n.+?)(\n## )', content, re.DOTALL)
    if match:
        trigger_section = match.group(1)
        next_section = match.group(2)

        route_text = f"""
Route elsewhere when the task is primarily:
- a task better handled by another agent per `_common/BOUNDARIES.md`
"""
        content = content.replace(
            trigger_section + next_section,
            trigger_section + '\n' + route_text + next_section
        )

    return content


def normalize_file(filepath, name, meta):
    """Normalize a single SKILL.md file."""
    with open(filepath, 'r') as f:
        content = f.read()

    original = content
    changes = []

    # H1, H2, H3: Add HTML comments if missing
    if not has_html_comment(content, 'CAPABILITIES_SUMMARY'):
        h_block = build_h_comments(name, meta)
        # Insert after frontmatter closing ---
        parts = content.split('---', 2)
        if len(parts) >= 3:
            content = parts[0] + '---' + parts[1] + '---\n\n' + h_block + '\n' + parts[2].lstrip('\n')
            changes.append('H1/H2/H3')

    # S1: Add Route elsewhere if missing
    if has_section(content, 'Trigger Guidance'):
        old_content = content
        content = add_route_elsewhere(content, name)
        if content != old_content:
            changes.append('S1-route-elsewhere')

    # S3: Normalize Boundaries to ### subheaders
    if '`Always`:' in content or '`Always:`' in content:
        old_content = content
        content = normalize_s3(content)
        if content != old_content:
            changes.append('S3-format')

    # S5: Add Output Routing if missing
    if not has_section(content, 'Output Routing'):
        s5 = build_s5_from_routing(content, name)
        # Insert before Output Requirements or Collaboration or References or Reference Map or Operational
        for marker in ['## Output Requirements', '## Collaboration', '## Routing And Handoffs', '## References', '## Reference Map', '## Operational']:
            if marker in content:
                content = content.replace(marker, s5 + '\n\n' + marker)
                changes.append('S5')
                break

    # S7: Add Collaboration if missing
    if not has_section(content, 'Collaboration'):
        s7 = build_s7(name, meta)
        # Insert before Reference Map or References or Operational
        for marker in ['## References', '## Reference Map', '## Operational']:
            if marker in content:
                content = content.replace(marker, s7 + '\n\n' + marker)
                changes.append('S7')
                break

    # S8: Rename "References" to "Reference Map" if needed
    if has_section(content, 'References') and not has_section(content, 'Reference Map'):
        content = re.sub(r'^## References\b', '## Reference Map', content, count=1, flags=re.MULTILINE)
        changes.append('S8-rename')

    # A1: Expand AUTORUN if minimal
    autorun_match = re.search(r'## AUTORUN Support\n(.+?)(?=\n## |\Z)', content, re.DOTALL)
    if autorun_match:
        autorun_body = autorun_match.group(1)
        if '```yaml' not in autorun_body or 'deliverable:' not in autorun_body:
            a1 = build_a1(name, meta)
            content = content[:autorun_match.start()] + a1 + content[autorun_match.end():]
            changes.append('A1-expand')
    elif not has_section(content, 'AUTORUN Support'):
        a1 = build_a1(name, meta)
        # Insert before Nexus Hub Mode or at end
        if '## Nexus Hub Mode' in content:
            content = content.replace('## Nexus Hub Mode', a1 + '\n\n## Nexus Hub Mode')
        else:
            content = content.rstrip() + '\n\n' + a1
        changes.append('A1')

    # A2: Expand Nexus Hub Mode if minimal
    nexus_match = re.search(r'## Nexus Hub Mode\n(.+?)(?=\n## |\Z)', content, re.DOTALL)
    if nexus_match:
        nexus_body = nexus_match.group(1)
        if '```text' not in nexus_body:
            a2 = build_a2(name)
            content = content[:nexus_match.start()] + a2 + content[nexus_match.end():]
            changes.append('A2-expand')
    elif not has_section(content, 'Nexus Hub Mode'):
        a2 = build_a2(name)
        content = content.rstrip() + '\n\n' + a2
        changes.append('A2')

    # L1: Remove Output Language section
    if '## Output Language' in content:
        content = remove_output_language_section(content)
        changes.append('L1')

    # Clean up excessive blank lines
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    content = content.rstrip() + '\n'

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return changes
    return []


def main():
    remaining_skills = [
        "guardian", "harvest", "helm", "launch", "loom",
        "matrix", "morph", "muse", "oracle", "palette",
        "pipe", "prism", "probe", "radar", "rally",
        "realm", "reel", "researcher", "retain", "ripple",
        "scaffold", "schema", "scout", "scribe", "sentinel",
        "sherpa", "showcase", "sketch", "spark", "sweep",
        "titan", "triage", "tuner", "vision", "voice",
        "void", "voyager"
    ]

    total_changes = 0
    for name in remaining_skills:
        if name not in AGENT_META:
            print(f"SKIP {name}: no metadata")
            continue

        filepath = os.path.join(SKILLS_DIR, name, "SKILL.md")
        if not os.path.exists(filepath):
            print(f"SKIP {name}: file not found")
            continue

        changes = normalize_file(filepath, name, AGENT_META[name])
        if changes:
            print(f"OK   {name}: {', '.join(changes)}")
            total_changes += 1
        else:
            print(f"SKIP {name}: no changes needed")

    print(f"\nTotal files modified: {total_changes}")


if __name__ == "__main__":
    main()
