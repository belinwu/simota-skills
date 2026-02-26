# Integration Patterns

Concrete patterns for Rally integration with Nexus orchestration and specific agent chains.

---

## Nexus → Rally Escalation Criteria

When Nexus designs an agent chain, it should escalate to Rally when ANY of these conditions apply:

| Condition | Example | Escalation |
|-----------|---------|------------|
| Chain has 2+ independent implementation steps | Builder (frontend) + Builder (backend) | Rally splits into parallel teammates |
| Feature scope spans 4+ files across 2+ domains | API + UI + DB + tests | Rally with Frontend/Backend Split |
| Sherpa decomposition produces `parallel_group` | Sherpa identifies parallelizable units | Rally receives SHERPA_TO_RALLY_HANDOFF |
| Task explicitly requests parallel execution | "Implement these features in parallel" | Rally directly |
| Chain includes both Artisan and Builder | Frontend + Backend implementation | Rally with Frontend/Backend Split |
| Chain includes implementation + test + docs | Builder + Radar + Quill | Rally with Code/Test/Docs Triple |
| Multiple independent bug fixes needed | 3+ unrelated bugs | Rally with Feature Parallel |

### Escalation Decision Flow

```
Nexus chain design
    ↓
Check parallelizability
    ├── Single agent or pure sequential → Execute sequentially (no Rally)
    ├── 2+ independent impl steps → Rally (parallel teammates)
    ├── Investigation only → No Rally (Lens/Scout are single-session)
    └── Uncertain → Sherpa decomposes → Check for parallel_group
                                            ├── parallel_group found → Rally
                                            └── all sequential → Nexus executes
```

### When NOT to Escalate to Rally

- Investigation-only chains (Lens, Scout, Rewind)
- Single-agent chains (Quill, Morph, Judge)
- Sequential-only chains where each step depends on the previous
- Changes under 10 lines total
- High-risk security changes (prefer sequential with checkpoints)

---

## Parallel Chain Variants

These are Rally-enhanced versions of standard Nexus chain templates.

### FEATURE Parallel Variants

| Base Chain | Rally Variant | Team Pattern | When to Use |
|------------|---------------|--------------|-------------|
| FEATURE/L | Sherpa → Rally(Forge+Builder, Artisan, Radar) | Frontend/Backend Split | Large fullstack feature |
| FEATURE/M | Rally(Builder×2, Radar) | Feature Parallel | 2+ independent feature units |
| FEATURE/fullstack | Rally(Artisan, Builder, Radar) | Frontend/Backend Split | Frontend + Backend + Tests |
| FEATURE/frontend | Rally(Artisan×2+, Radar) | Feature Parallel | Multiple independent UI features |

**Example: FEATURE/L Parallel**
```
Sherpa decomposes → Identifies parallel groups
    ↓
Rally receives SHERPA_TO_RALLY_HANDOFF
    ↓
Rally spawns:
  ├── frontend-impl (general-purpose): Artisan role
  │   └── exclusive_write: src/components/**, src/pages/**
  ├── backend-impl (general-purpose): Builder role
  │   └── exclusive_write: src/api/**, src/services/**
  └── test-writer (general-purpose): Radar role
      └── exclusive_write: tests/**
    ↓
All complete → Rally synthesizes → Returns to Nexus
```

### BUG Parallel Variants

| Base Chain | Rally Variant | Team Pattern | When to Use |
|------------|---------------|--------------|-------------|
| BUG (multiple) | Rally(Builder×N, Radar) | Feature Parallel | 3+ independent bugs |

### REFACTOR Parallel Variants

| Base Chain | Rally Variant | Team Pattern | When to Use |
|------------|---------------|--------------|-------------|
| REFACTOR/arch | Atlas → Sherpa → Rally(Zen×N, Radar) | Feature Parallel | Multi-module refactoring |
| MODERNIZE/stack | Horizon → Sherpa → Rally(Builder×N, Radar) | Feature Parallel | Multi-area modernization |

### SECURITY Parallel Variants

| Base Chain | Rally Variant | Team Pattern | When to Use |
|------------|---------------|--------------|-------------|
| SECURITY/full | Rally(Sentinel, Probe) → Builder → Radar | Specialist Team | Static + Dynamic scan in parallel |

### TEST Parallel Variants

| Base Chain | Rally Variant | Team Pattern | When to Use |
|------------|---------------|--------------|-------------|
| TEST/coverage | Rally(Radar, Voyager) | Specialist Team | Unit + E2E tests in parallel |
| TEST/quality | Judge → Rally(Builder×N) | Pipeline | Parallel fix implementation after PDCA |

### DOCS Parallel Variants

| Base Chain | Rally Variant | Team Pattern | When to Use |
|------------|---------------|--------------|-------------|
| DOCS/full | Rally(Quill, Canvas, Showcase) | Specialist Team | Code docs + diagrams + stories in parallel |

---

## Agent-Specific Integration Patterns

### Builder + Artisan (Frontend/Backend Split)

The most common Rally pattern. Split implementation between frontend (Artisan) and backend (Builder).

```yaml
team_design:
  pattern: "Frontend/Backend Split"
  teammates:
    - name: "frontend-impl"
      role: "Artisan"
      subagent_type: "general-purpose"
      model: "sonnet"
      exclusive_write:
        - src/components/**
        - src/pages/**
        - src/styles/**
        - src/hooks/**
      context_injection:
        - "Apply Artisan patterns: hooks design, state management, Server Components"
        - "Reference: Forge prototype output (if available)"
# ...
```

### Radar + Voyager (Test Parallelization)

Split unit testing and E2E testing.

```yaml
team_design:
  pattern: "Specialist Team"
  teammates:
    - name: "unit-tester"
      role: "Radar"
      subagent_type: "general-purpose"
      model: "sonnet"
      exclusive_write:
        - tests/unit/**
        - __mocks__/**
      context_injection:
        - "Focus on edge case coverage and regression tests"
        - "Reference implementation files in shared_read"
    - name: "e2e-tester"
      role: "Voyager"
# ...
```

### Sentinel + Probe (Security Parallelization)

Run static analysis (Sentinel) and dynamic testing (Probe) simultaneously.

```yaml
team_design:
  pattern: "Specialist Team"
  teammates:
    - name: "static-scanner"
      role: "Sentinel"
      subagent_type: "general-purpose"
      model: "sonnet"
      exclusive_write:
        - reports/security-static/**
      context_injection:
        - "Run static analysis: hardcoded secrets, SQL injection, XSS, dependency CVEs"
        - "Output findings in structured format for Builder handoff"
    - name: "dynamic-scanner"
      role: "Probe"
      subagent_type: "general-purpose"
# ...
```

### Builder × N (Feature Parallel)

Multiple independent implementations in parallel.

```yaml
team_design:
  pattern: "Feature Parallel"
  teammates:
    - name: "feature-a-impl"
      role: "Builder"
      subagent_type: "general-purpose"
      model: "sonnet"
      exclusive_write:
        - src/features/feature-a/**
        - tests/features/feature-a/**
    - name: "feature-b-impl"
      role: "Builder"
      subagent_type: "general-purpose"
      model: "sonnet"
      exclusive_write:
# ...
```

### Judge + Rally (Quality PDCA with Parallel Fixes)

Judge identifies quality issues via PDCA cycle, then Rally parallelizes the fixes.

```
Judge (PDCA Cycle)
    ↓ Identifies N independent quality issues
Rally receives issue list
    ↓
Rally spawns Builder × N (one per independent fix area)
    ↓
All fixes complete → Rally synthesizes
    ↓
Judge (next PDCA iteration) - verify improvements
```

---

## Nexus ↔ Rally Handoff Integration

### Nexus AUTORUN → Rally Flow

When Nexus AUTORUN encounters a parallelizable step:

```
Nexus AUTORUN executing chain: Sherpa → [parallel step] → Radar
    ↓
Nexus detects parallel_group in Sherpa output
    ↓
Nexus invokes Rally via _AGENT_CONTEXT:
  _AGENT_CONTEXT:
    Role: Rally
    Task: Execute parallel implementation
    Mode: AUTORUN
    Chain: [Sherpa completed]
    Input: Sherpa's SHERPA_TO_RALLY_HANDOFF
    Constraints:
      - Max team size: 4
      - File ownership from Sherpa's decomposition
    Expected_Output: Unified implementation result
...
```

### Nexus Hub Mode → Rally Flow

When Nexus is in Hub Mode and delegates to Rally:

```
Nexus Hub sends:
  ## NEXUS_ROUTING
  - Task: Implement features A, B, C in parallel
  - Chain: [...previous agents...] → Rally → [...next agents...]
  - Context: [accumulated context from previous agents]
    ↓
Rally executes, returns:
  ## NEXUS_HANDOFF
  - Step: X/Y
  - Agent: Rally
  - Summary: Parallel execution completed (3 teammates, all tasks done)
  - Key findings: [team composition, results]
  - Artifacts: [files changed by each teammate]
  - Suggested next agent: Radar (verify combined output)
    ↓
...
```

### Nexus PARALLEL.md ↔ Rally Distinction

| Aspect | Nexus _PARALLEL_BRANCHES | Rally Teams |
|--------|--------------------------|-------------|
| Execution model | Single session, simulated parallel | Multi-session, true parallel |
| Max branches | 4 | 10 teammates (recommended 2-4) |
| File ownership | Via file_ownership YAML | Via ownership_map in teammate prompts |
| Conflict resolution | CONCAT/RESOLVE/MANUAL strategies | ON_RESULT_CONFLICT trigger |
| Guardrails | Per-branch L1-L4 | Rally monitors via TaskList |
| When to use | Simple parallel (2-3 branches, light tasks) | Complex parallel (real implementation, heavy tasks) |

**Decision guide:**
- Nexus can handle lightweight parallel branches internally (e.g., 2 validators)
- Rally is needed for real implementation work (e.g., frontend + backend + tests)
- If each branch needs more than ~50 lines of code → use Rally
- If branches need different agent roles → use Rally

---

## Rally ↔ Sherpa Integration

### Sherpa Decomposition → Rally Execution

Sherpa is the natural upstream partner for Rally. When Sherpa decomposes an Epic:

```
Sherpa decomposes Epic into Atomic Steps
    ↓
Sherpa identifies parallel_group markers:
  Epic: Auth Feature
  Steps:
    1. Define types (sequential)
    2. parallel_group:  ← Rally trigger
       - 2a. Implement login API (backend)
       - 2b. Implement login UI (frontend)
    3. Write tests (after 2a, 2b complete)
    ↓
Nexus (or Sherpa directly) delegates to Rally via:
  ## SHERPA_TO_RALLY_HANDOFF
  - Epic: Auth Feature
  - Parallel Groups:
...
```

### Rally Result → Sherpa Progress Update

After Rally completes parallel execution, Sherpa can update progress:

```
Rally returns:
  ## RALLY_TO_NEXUS_HANDOFF
  - Completed: 4/4 tasks
  - Files Changed: [list]
    ↓
Sherpa marks parallel_group steps as completed
Sherpa continues with remaining sequential steps
```

---

## Collaboration Pattern Details

### Pattern A: Plan-then-Rally (Sherpa → Rally)

**Flow:** Sherpa → Rally → Teammates → Rally → Nexus

**Best for:** Complex features that need decomposition before parallelization.

```
User: "Add authentication feature"
  ↓
Nexus routes to: Sherpa → Rally
  ↓
Sherpa decomposes:
  - Step 1: Define auth types (sequential)
  - Step 2: parallel_group [API impl, UI impl]
  - Step 3: Write tests (sequential)
  ↓
Rally receives SHERPA_TO_RALLY_HANDOFF
Rally executes Step 1 → parallel Step 2 → Step 3
Rally returns to Nexus
```

### Pattern B: Nexus-delegates-Rally

**Flow:** Nexus → Rally → Teammates → Rally → Nexus

**Best for:** When Nexus detects parallelizable work mid-chain without Sherpa.

```
Nexus chain: Scout → [Builder(frontend) + Builder(backend)] → Radar
  ↓
Nexus detects parallel implementation step
Nexus invokes Rally for the parallel phase only
  ↓
Rally spawns 2 teammates, executes, returns
  ↓
Nexus continues to Radar
```

### Pattern C: Direct Rally

**Flow:** User → Rally → Teammates → Rally → User

**Best for:** Explicit parallel execution requests.

```
User: "Implement these 3 features in parallel"
  ↓
Rally directly designs team, spawns, executes
  ↓
Rally reports results to user
```

### Pattern D: Rally-with-Specialist

**Flow:** Rally → Specialist teammate → Rally

**Best for:** Delegating specialized work to expert agents via teammates.

```
Rally needs investigation → Spawns Explore teammate
Rally needs architecture review → Spawns Plan teammate
Rally needs security scan → Spawns general-purpose teammate with Sentinel instructions
```

---

## Rally Team Composition by Nexus Chain Type

Quick reference for how Rally should compose teams based on the originating Nexus chain type.

| Nexus Chain Type | Rally Team Pattern | Teammate Roles | Typical Size |
|------------------|-------------------|----------------|--------------|
| FEATURE/L | Frontend/Backend Split | Artisan + Builder + Radar | 3 |
| FEATURE/fullstack | Frontend/Backend Split | Artisan + Builder | 2-3 |
| FEATURE/multi | Feature Parallel | Builder × N | 2-4 |
| BUG/multiple | Feature Parallel | Builder × N | 2-3 |
| REFACTOR/arch | Feature Parallel | Zen × N | 2-4 |
| SECURITY/full | Specialist Team | Sentinel + Probe | 2 |
| TEST/coverage | Specialist Team | Radar + Voyager | 2 |
| MODERNIZE/stack | Feature Parallel | Builder × N | 2-4 |
| DOCS/full | Code/Test/Docs Triple | Quill + Canvas + Showcase | 3 |
| INFRA/multi | Feature Parallel | general-purpose × N | 2-3 |
