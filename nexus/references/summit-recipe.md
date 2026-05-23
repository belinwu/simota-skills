# Nexus Summit Recipe Reference

> **"Three engines, four teams, one verdict — quality maximized through orchestrated diversity."**

## Contents

- [Overview](#overview)
- [Invocation and Prerequisites](#invocation-and-prerequisites)
- [When to Use Summit](#when-to-use-summit)
- [Topology](#topology)
- [Engine × Team Matrix](#engine--team-matrix)
- [Phase Contracts](#phase-contracts)
- [Sub-Orchestration via Arena](#sub-orchestration-via-arena)
- [Cross-Engine Quorum Rules](#cross-engine-quorum-rules)
- [AUTORUN Chain Template](#autorun-chain-template)
- [Failure Escalation](#failure-escalation)
- [Cost and Latency Profile](#cost-and-latency-profile)
- [Comparison with Apex and Judge](#comparison-with-apex-and-judge)

---

## Overview

Summit is a **quality-maximization recipe** that mobilizes three execution engines (Claude Code / Codex CLI / Antigravity CLI) across four functional teams (Analysis / Execution / Verification / Improvement). It produces engine-attributed, multi-perspective deliverables for strategic decisions and high-stakes outputs where the cost of failure dramatically exceeds the cost of triangulation.

**Key design decisions:**
- **Claude is always the hub**; Codex and Antigravity are accessed exclusively through `arena` (no direct CLI invocation from Nexus).
- **agy is a hard prerequisite** — if Antigravity CLI is not reachable at preflight, Summit refuses to launch (degradation to dual-engine is not allowed; that would defeat the recipe's purpose).
- **Tri-engine triangulation is load-bearing** in Phase 1 (Analysis) and Phase 4 (Verification). Single-engine outputs in these phases are treated as recipe violations.
- **Improvement loop is capped at 3 iterations** with Agent Tennis circuit breaker to prevent runaway cost.
- **User confirmation is mandatory** before launch (same gate as `apex`). Summit spawns 20-50 agents per run.

---

## Invocation and Prerequisites

### Invocation

```
/nexus summit                 # Goal-supplied mode (current task context)
/nexus summit "<goal>"        # Explicit goal mode
```

### Prerequisites (preflight, in Nexus main context)

| Prerequisite | Check | Failure Action |
|--------------|-------|---------------|
| `claude` binary | always available (host) | n/a |
| `codex` binary | reachable via `which codex` or fallback paths (`~/.bun/bin/`, `~/.local/bin/`, `/usr/local/bin/`, `/opt/homebrew/bin/`, `~/.npm-global/bin/`) | abort with "Codex CLI required for summit; install or use apex/feature instead" |
| `agy` binary | reachable via `which agy` or fallback paths (same list) | abort with "Antigravity CLI required for summit; install agy or use apex (claude+codex) instead" |
| `arena` skill available | check `~/.claude/skills/arena/SKILL.md` exists | abort with "arena skill required for engine bridging" |
| `arena.max_depth >= 2` (Codex config) | inspect `~/.codex/config.toml` | warn and continue; sub-spawning may fail |
| User cost acknowledgment | mandatory confirmation prompt | abort if declined |
| Mission charter producible | Phase 0 must produce valid `mission_charter.yaml` | abort if FRAMING fails |

**Why agy is mandatory (not optional):** Summit's value comes from three independent reasoning styles. With only two engines (claude + codex), output quality is statistically similar to running `judge` plus a normal feature chain — the orchestration overhead is not justified. Users wanting two-engine workflows should use `apex` instead.

---

## When to Use Summit

### Use Summit for

- Strategic decisions with multi-year impact (architecture pivots, platform migrations, product direction)
- Final pre-release verification for high-risk launches (financial, medical, safety-critical)
- Large refactors where blind spots compound (legacy modernization, security overhauls)
- Decisive differentiator features where competitor analysis must triangulate with internal user research and creative reframing
- Any task where the cost of an undetected error exceeds the cost of 20-50 agents and 1-2 hours of wall time

### Do NOT use Summit for

- Single-feature implementation → `feature` or `apex`
- PR review → `judge` (already tri-engine)
- Routine bug fixes → `bug`
- Performance tuning of a known hotspot → `optimize`
- Time-bounded tasks (under 30 min) → `feature` or direct agent
- Cost-sensitive contexts (individual hobby projects, small teams) → simpler recipes
- Linear tasks with no parallelism benefit → sequential chain

### Do NOT use Summit when

- agy is unavailable → use `apex`
- Codex is unavailable → use single-engine chain or `apex` if codex is the only missing piece
- User has not confirmed the cost envelope
- The task does not have a clear acceptance criteria definable in Phase 0

---

## Topology

```
                  ┌──────────────────────────────────┐
                  │       Nexus (Claude, hub)        │
                  └────────────────┬─────────────────┘
                                   │
       ┌───────────────────────────┼───────────────────────────┐
       │                           │                           │
   Phase 0                     Phase 1                     Phase 2
   FRAMING                     ANALYSIS                    PLANNING
   (Claude only)               (tri-engine ‖)              (Claude opus)
       │                           │                           │
       ▼                           ▼                           ▼
  mission_charter        analysis_consensus              execution_plan
                                                               │
                                                               ▼
                                    ┌──────────────────────────────────────┐
                                    │  Phase 3 EXECUTION TEAM              │
                                    │  arena[COLLABORATE]                  │
                                    │  ├─ Claude tasks (direct spawn)      │
                                    │  ├─ Codex tasks (arena → codex)      │
                                    │  └─ agy tasks (arena → agy)          │
                                    └──────────────────────────────────────┘
                                                               │
                                                               ▼
                                    ┌──────────────────────────────────────┐
                                    │  Phase 4 VERIFICATION TEAM (‖)       │
                                    │  ├─ judge (already tri-engine)       │
                                    │  ├─ Radar + Voyager (codex)          │
                                    │  └─ Ripple + arena[agy] (agy)        │
                                    └──────────────────────────────────────┘
                                                   │
                                  CONFIRMED/LIKELY findings
                                                   │
                                                   ▼
                                    ┌──────────────────────────────────────┐
                                    │  Phase 5 IMPROVEMENT LOOP (max 3×)   │
                                    │  orbit drives:                       │
                                    │  ├─ Claude: Zen + Hex + Atlas        │
                                    │  ├─ codex: Bolt                      │
                                    │  └─ agy: arena[agy] + Lore           │
                                    │  magi arbitrates → Phase 3 loop      │
                                    └──────────────────────────────────────┘
                                                               │
                                                               ▼
                                                          Phase 6
                                                          DELIVERY
                                                  (Guardian + Launch)
                                                               │
                                                               ▼
                                                   NEXUS_COMPLETE
```

---

## Engine × Team Matrix

| | Claude (hub) | Codex | Antigravity (agy) |
|---|---|---|---|
| **Analysis** | Lens / Scout / Atlas (structural + code + architecture) | arena[COMPETE, codex] (implementation-level analysis) | arena[COMPETE, agy] (long-context 1M, multimodal) |
| **Execution** | Builder / Artisan / Native (security, design judgment) | arena[COLLABORATE, codex] (bulk code generation, refactor) | arena[COMPETE, agy] (alternative implementations) |
| **Verification** | judge (built-in tri-engine review) | Radar (unit/integration tests) + Voyager (E2E) | Ripple (impact analysis) + arena[agy, review] |
| **Improvement** | Zen (refactor) + Hex (debt scoring) + Atlas (architecture) | Bolt (performance) | arena[agy] + Lore (architectural improvements, pattern extraction) |

**Engine selection rationale:**

| Task characteristic | Preferred engine | Why |
|--------------------|-----------------|-----|
| Security / design judgment | Claude | Deepest reasoning, OWASP knowledge baseline |
| Large-scale code generation / refactor | Codex | 192K context, sandbox-first, Terminal-Bench 2.0 leader |
| Long-context analysis (codebase > 200K tokens) | agy | 1M context window |
| Multimodal (images, diagrams, screenshots) | agy | Native multimodal support |
| Creative alternatives / divergent thinking | agy | Deep Think mode, different reasoning style |
| Test execution | Codex | Sandbox-first, fast iteration |
| Architecture decisions | Claude | Strongest at trade-off reasoning |

---

## Phase Contracts

### Phase 0: Framing (Claude only, 1-2 agents, 3-5 min)

**Input:** User request (goal text or "/nexus summit" with current task context)

**Agents:**
1. Nexus[classify] — task type detection, complexity scoring
2. Accord[L0-L1 spec] — staged elaboration of vision and requirements (optional, skip if user provides explicit goal)
3. Sherpa[atomic decomposition] — break into team missions

**Output:** `mission_charter.yaml`

```yaml
goal: "<explicit goal statement>"
acceptance_criteria:
  - "<measurable criterion 1>"
  - "<measurable criterion 2>"
team_missions:
  analysis:     "<what analysis must answer>"
  execution:    "<what execution must produce>"
  verification: "<what verification must validate>"
  improvement:  "<what improvement axis to optimize>"
cost_budget:
  max_agents: 50
  max_wall_time_minutes: 120
  max_loops: 3
risk_tier: strategic | release-critical | major-refactor
user_acknowledged: true
```

**Gate:** If `cost_budget.max_agents × estimated_token_cost > L4 threshold` OR `risk_tier ∈ {strategic, release-critical}` → require explicit user confirmation before proceeding to Phase 1.

---

### Phase 1: Analysis Team (tri-engine parallel, 6-9 agents, 8-15 min)

**Input:** `mission_charter.yaml`

**Parallel branches (L2 spawn, isolated sub-contexts):**

```yaml
parallel:
  - branch: claude_analysis
    engine: claude
    agents: [lens, scout, atlas]
    mission: structural + code + architectural analysis
    output: claude_analysis.json

  - branch: codex_analysis
    engine: codex (via arena)
    paradigm: COMPETE
    mode: Team
    mission: implementation-level analysis (code quality, perf hotspots, dependency risks)
    output: codex_analysis.json

  - branch: agy_analysis
    engine: agy (via arena)
    paradigm: COMPETE
    mode: Team
    mission: long-context + multimodal + divergent perspective
    output: agy_analysis.json
```

**Synthesis:** `magi[arbitrate-tri-engine]` runs Logos / Pathos / Sophia perspectives across all three engine reports.

**Output:** `analysis_consensus.md`
```yaml
consensus_findings: [...]    # 3/3 agreement
likely_findings:    [...]    # 2/3 agreement
minority_signals:   [...]    # 1/3 — kept for transparency, marked as low confidence
disputed_findings:  [...]    # active disagreement requiring user judgment
engine_attribution: {...}    # which finding came from which engine
```

**Gate:** If `disputed_findings / total_findings > 0.30` → escalate to user before Phase 2.

---

### Phase 2: Planning (Claude opus, 2-3 agents, 5-8 min)

**Input:** `analysis_consensus.md`

**Agents:**
1. Sherpa[plan_DAG] — convert findings into atomic task DAG
2. Magi[trade-off arbitration] — resolve plan-level conflicts

**Engine assignment rules (applied per-task in DAG):**
- Security-sensitive OR architecture-defining → Claude
- Bulk code generation OR test execution → Codex
- Multimodal OR alternative-exploration → agy
- If ambiguous → Claude (default safe)

**Output:** `execution_plan.yaml`
```yaml
tasks:
  - id: T1
    description: "..."
    engine: claude | codex | agy
    dependencies: []
    risk_level: low | medium | high
    estimated_agents: N
  - id: T2
    ...
parallel_groups:
  - [T1, T3]    # can run together
  - [T2]        # must wait for T1
```

**Model selection:** Phase 2 uses `claude-opus` for planning (Plan-and-Execute pattern: capable model plans, cheaper models execute — up to 90% cost reduction in execution phase).

---

### Phase 3: Execution Team (DAG-driven, 5-15 agents, 20-60 min)

**Coordinator:** arena[COLLABORATE]

**Process:**
1. arena receives `execution_plan.yaml` and DAG
2. Claude tasks → direct Agent spawn (foreground or L2 parallel as DAG allows)
3. Codex tasks → arena dispatches to `codex exec` with task-specific spec
4. agy tasks → arena dispatches to `agy` with task-specific spec
5. Per parallel_group, all tasks fan out concurrently
6. Integration step after each group: Nexus aggregates, resolves file-level conflicts using `conflict-resolution.md` ownership rules

**Checkpoint:** after each parallel_group completes, persist outputs (Core Rule: 4+ step chains need checkpoint-resume).

**Output:** Working implementation + per-task execution log + engine attribution per file.

---

### Phase 4: Verification Team (tri-engine quorum, 4-7 agents, 10-20 min)

**Parallel branches:**

```yaml
parallel:
  - branch: judge_review
    agent: judge
    mode: tri-engine (built-in: codex + agy + claude reviewers in parallel)
    output: judge_findings.json

  - branch: test_execution
    engine: codex
    agents: [radar, voyager]
    mission: run unit + integration + E2E tests
    output: test_results.json

  - branch: impact_analysis
    engine: agy (via arena)
    agents: [ripple, arena]
    mission: vertical (dependency) + horizontal (pattern consistency) impact + independent review
    output: impact_analysis.json
```

**Quorum rules:**

| Concurrence | Finding Severity | Action |
|-------------|------------------|--------|
| CONFIRMED (3/3 agree) | CRITICAL or HIGH | Block release → force Phase 5 |
| CONFIRMED (3/3 agree) | MEDIUM or LOW | Annotate, deliver with caveat |
| LIKELY (2/3 agree) | CRITICAL or HIGH | Force Phase 5 |
| LIKELY (2/3 agree) | MEDIUM or LOW | Annotate |
| CANDIDATE (1/3 only) | any | Grounding verification by Nexus → if VERIFIED → treat as LIKELY |

**Output:** `verification_report.md` with engine-attributed findings, concurrence labels, and quorum verdict.

**Gate:** If any CONFIRMED+CRITICAL/HIGH or LIKELY+CRITICAL/HIGH finding → mandatory Phase 5 loop.

---

### Phase 5: Improvement Team (PDCA loop, 3-6 agents per loop, max 3 loops)

**Driver:** orbit (autonomous loop runner)

**Per-loop process:**

```yaml
loop_iteration:
  parallel_improvement_proposals:
    - engine: claude
      agents: [zen, hex, atlas]
      mission: refactor + tech debt + architectural improvement proposals
    - engine: codex
      agent: bolt
      mission: performance improvement proposals
    - engine: agy (via arena)
      agents: [arena, lore]
      mission: cross-codebase pattern extraction + architectural alternatives

  arbitration:
    agent: magi
    role: select-improvements-to-apply
    output: applied_improvements.yaml (with per-improvement rationale)

  apply_loop:
    if applied_improvements.non_empty:
      → Phase 3 (re-execute affected tasks)
      → Phase 4 (re-verify)
      → check Phase 4 quorum:
          if CONFIRMED/LIKELY CRITICAL still present → next iteration (up to max_loops)
          else → exit loop, proceed to Phase 6
    else:
      → exit loop, proceed to Phase 6
```

**Circuit breakers:**

| Condition | Action |
|-----------|--------|
| `loop_count >= max_loops` (default 3) | Exit loop, deliver with caveat about remaining issues |
| Agent Tennis: same issue debated 3+ turns without resolution | Trip circuit breaker, escalate to user |
| Cost budget projected to exceed | Reduce loop scope to CRITICAL findings only |
| All quorum findings resolved | Exit loop early (success path) |

---

### Phase 6: Delivery (Claude, 1-2 agents, 3-5 min)

**Agents:**
1. Guardian[PR-prep] — classify changes, recommend granularity, prepare commit strategy
2. Launch[release-plan] — versioning, CHANGELOG, release notes, rollback plan

**Output:** `NEXUS_COMPLETE` with the full evidence trail:

```markdown
## Nexus Execution Report

Task: <goal>
Chain: summit (3-engine, 4-team)
Mode: AUTORUN_FULL with mandatory pre-launch confirmation

### Phase Results
| Phase | Status | Engine Attribution | Key Output |
| ...

### Engine Contributions
- Claude:    <files / decisions / findings>
- Codex:     <files / decisions / findings>
- agy:       <files / decisions / findings>

### Quorum Summary
- CONFIRMED findings: N (all resolved | N remaining)
- LIKELY findings:    N
- Minority signals:   N (kept for transparency)

### Improvement Loop Summary
- Loops executed: N / 3
- Improvements applied: N
- Circuit breaker tripped: yes/no

### Verification
- Tests:        pass/fail summary
- Build:        result
- judge:        N findings (severity breakdown)
- Ripple:       impact scope

### Summary
<status, recommended next steps, follow-ups>

### Cost
- Wall time:        N minutes
- Total agents:     N
- Estimated tokens: ~N M
```

---

## Sub-Orchestration via Arena

Arena is the **single point of contact** for Codex and agy. Nexus never calls codex or agy directly.

### Arena delegation patterns used by Summit

| Phase | Paradigm | Engines | Mode | Purpose |
|-------|----------|---------|------|---------|
| 1 ANALYSIS | COMPETE | codex (alone) | Team | Codex-perspective analysis |
| 1 ANALYSIS | COMPETE | agy (alone) | Team | agy-perspective analysis |
| 3 EXECUTION | COLLABORATE | codex + agy | Team | Task decomposition across engines |
| 3 EXECUTION | COMPETE | agy (alone) | Solo | Alternative implementation proposals |
| 4 VERIFICATION | COMPETE | agy (alone) | Solo | Independent review |
| 5 IMPROVEMENT | COMPETE | agy (alone) | Solo | Pattern extraction + architectural alternatives |

### Engine isolation contract

Each arena invocation produces an isolated sub-context for the target engine. Findings/outputs flow back to Nexus through `_STEP_COMPLETE` with engine attribution. **Cross-engine contamination is prevented at the arena boundary** — engines never see each other's intermediate outputs during a phase.

---

## Cross-Engine Quorum Rules

Applied in Phase 1 (Analysis synthesis) and Phase 4 (Verification).

### Concurrence Labels

| Label | Definition | Default Trust |
|-------|------------|---------------|
| CONFIRMED | 3/3 engines independently surface the same finding | High — proceed without grounding |
| LIKELY | 2/3 engines surface the same finding | Medium — proceed but flag |
| CANDIDATE | 1/3 engines surface a finding | Low — requires grounding verification by Nexus before action |
| MINORITY | 1/3 engines surface a finding that other engines explicitly considered and rejected | Very low — log as transparency, do not act |

### Grounding verification protocol (for CANDIDATE findings)

Nexus (in main context) reads the actual code referenced by the finding and classifies:

| Verdict | Definition | Treatment |
|---------|------------|-----------|
| VERIFIED | Finding accurately describes a real issue | Promote to LIKELY |
| REJECTED | Finding does not match code reality | Discard, log as engine false positive |
| MITIGATED | Finding describes a real issue that is already addressed elsewhere | Discard with note |
| STYLE-ONLY | Finding is preference, not correctness | Discard |
| NEEDS-INFO | Cannot verify without external context | Escalate to user |

### Disagreement escalation

If `disputed_findings / total_findings > 0.30` in Phase 1, Nexus pauses and presents the disagreement matrix to the user before proceeding. This catches recipe-level failures where one engine has fundamentally misunderstood the task.

---

## AUTORUN Chain Template

```yaml
recipe: summit
mode: AUTORUN_FULL
required_confirmation: true   # ALWAYS — same gate as apex
prerequisites:
  - claude_available: true
  - codex_available:  true    # abort if false
  - agy_available:    true    # abort if false (no dual-engine fallback)
  - arena_skill:      true
  - cost_acknowledged: true

phase_chain:
  - phase: 0_framing
    agents: [nexus.classify, accord, sherpa]
    engine: claude
    duration_minutes: [3, 5]

  - phase: 1_analysis
    parallel:
      - {engine: claude, agents: [lens, scout, atlas]}
      - {engine: codex,  agent: arena, paradigm: COMPETE, mode: Team}
      - {engine: agy,    agent: arena, paradigm: COMPETE, mode: Team}
    synthesis: {agent: magi, role: arbitrate-tri-engine}
    duration_minutes: [8, 15]
    gate: disputed_findings_ratio < 0.30

  - phase: 2_planning
    agents: [sherpa, magi]
    engine: claude
    model: opus
    duration_minutes: [5, 8]

  - phase: 3_execution
    coordinator: arena
    paradigm: COLLABORATE
    engines: [claude, codex, agy]
    duration_minutes: [20, 60]
    checkpoint: after_each_parallel_group

  - phase: 4_verification
    parallel:
      - {agent: judge, mode: tri-engine-builtin}
      - {engine: codex, agents: [radar, voyager]}
      - {engine: agy,   agents: [ripple, arena]}
    quorum: cross_engine_3_of_3
    duration_minutes: [10, 20]

  - phase: 5_improvement
    driver: orbit
    max_loops: 3
    arbiter: magi
    circuit_breakers:
      - agent_tennis_3_turns
      - cost_budget_overrun
      - loops_exceeded
    per_loop_minutes: [10, 15]

  - phase: 6_delivery
    agents: [guardian, launch]
    engine: claude
    output: NEXUS_COMPLETE
    duration_minutes: [3, 5]
```

---

## Failure Escalation

| Failure | Detection Phase | Mitigation | Escalation Threshold |
|---------|----------------|-----------|--------------------|
| agy CLI unreachable | Preflight | Abort with message "use apex instead" | Immediate |
| codex CLI unreachable | Preflight | Abort with message "use apex (claude only) instead" | Immediate |
| Phase 1 disputed findings > 30% | Phase 1 synthesis | Pause, present disagreement matrix | Immediate |
| Phase 4 CONFIRMED CRITICAL after max_loops | Phase 5 exit | Deliver with explicit "unresolved CRITICAL" caveat | Always |
| Agent Tennis (same issue 3+ turns) | Phase 5 loop | Circuit breaker, deliver | Always |
| Cost budget projected overrun | Per-phase gate | Reduce remaining scope to CRITICAL findings only; if still over, escalate | After 50% budget consumed |
| Engine returns invalid schema 3× | Per-phase | Treat engine as DEGRADED for remainder of run, continue with remaining 2 engines (Phase 1/4 quorum degrades to 2/2) | After 3rd schema violation |
| Total wall time > 2× estimate | Per-phase | Pause, present time-vs-quality trade-off to user | Always |

**Hard rule:** Summit never silently degrades to dual-engine. Either it runs as designed with 3 engines, or it aborts and recommends `apex`. Mid-run engine failure (after preflight) is treated as a recipe-level failure requiring user judgment.

---

## Cost and Latency Profile

### Per-phase profile

| Phase | Agents | Parallel | Wall Time | Tokens |
|-------|--------|----------|-----------|--------|
| 0 FRAMING | 1-2 | 1 | 3-5 min | ~30K |
| 1 ANALYSIS | 6-9 | 3 | 8-15 min | ~250K |
| 2 PLANNING | 2-3 | 1 | 5-8 min | ~60K (opus) |
| 3 EXECUTION | 5-15 | 3-5 | 20-60 min | ~400-1200K |
| 4 VERIFICATION | 4-7 | 3 | 10-20 min | ~200K |
| 5 IMPROVEMENT (per loop) | 3-6 | 3 | 10-15 min | ~150K |
| 6 DELIVERY | 1-2 | 1 | 3-5 min | ~20K |

### Total envelopes

| Scenario | Agents | Wall Time | Tokens |
|----------|--------|-----------|--------|
| No improvement loops | 20-38 | 49-113 min | 1.1-1.8M |
| 1 loop | 23-44 | 59-128 min | 1.25-1.95M |
| 2 loops | 26-50 | 69-143 min | 1.4-2.1M |
| 3 loops (max) | 29-56 | 79-158 min | 1.55-2.25M |

### Cost comparison

| Recipe | Agents | Wall Time | Relative Cost |
|--------|--------|-----------|---------------|
| `feature` | 3-5 | 5-15 min | 1× (baseline) |
| `apex` | 8-25 | 30-90 min | 4-8× |
| `summit` (no loops) | 20-38 | 49-113 min | 8-15× |
| `summit` (3 loops) | 29-56 | 79-158 min | 12-22× |

**Rule of thumb:** Summit costs 10-20× a typical `feature` chain. Use only when the cost of failure exceeds the cost of triangulation by at least an order of magnitude.

---

## Comparison with Apex and Judge

| Dimension | `apex` | `judge` | `summit` |
|-----------|--------|---------|---------|
| **Purpose** | Full-cycle feature delivery (discovery → ship) | Cross-engine code review | Quality-maximizing strategic execution |
| **Engines** | Claude + Codex | Claude + Codex + agy (review only) | Claude + Codex + agy (full participation) |
| **Structure** | Phase-driven linear with sub-orchestration | Single-phase parallel review | 4-team × 3-engine matrix with PDCA loop |
| **Teams** | Implicit (sub-orchestrators) | Single (verification) | Explicit (analysis / execution / verification / improvement) |
| **Verification** | Risk Gate (pre-implementation) + Judge in loop | Tri-engine quorum review | Cross-engine quorum + grounded verification + improvement loop |
| **Loop** | Implementation loop (Orbit) | None (single-shot) | Improvement loop (max 3, magi-arbitrated) |
| **Agents** | 8-25 | 3-6 | 20-50 |
| **Wall time** | 30-90 min | 5-15 min | 49-158 min |
| **Cost multiplier vs feature** | 4-8× | 0.5-1× | 8-22× |
| **agy required** | No (optional) | Yes (tri-engine review) | Yes (hard prerequisite) |
| **User confirmation** | Yes (mandatory) | No | Yes (mandatory) |
| **Best for** | New features needing full lifecycle | PR review, pre-commit checks | Strategic decisions, high-stakes releases |

### Decision tree

```
Is the task a new feature needing discovery → ship?
  └─ YES → apex
  └─ NO ↓

Is the task purely code review?
  └─ YES → judge
  └─ NO ↓

Does the task require strategic / release-critical quality maximization?
  └─ NO  → feature / bug / refactor / etc. (simpler recipes)
  └─ YES ↓

Is agy available?
  └─ NO  → apex (closest substitute) or simpler chain
  └─ YES ↓

Has user acknowledged 8-22× cost vs feature?
  └─ NO  → present cost envelope, get confirmation
  └─ YES → summit
```
