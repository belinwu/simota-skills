# Rally Coordination Protocol

Defines how Titan orchestrates parallel Epic execution through Rally, including file ownership, result merging, and integration testing.

---

## When to Use Rally

| Condition | Action |
|-----------|--------|
| Epics have no file overlap | Rally parallel execution |
| Epics share read-only dependencies | Rally with shared_read declaration |
| Epics write to same files | Sequential via Nexus (no Rally) |
| Mixed independence | Group independent → Rally; sequence dependent |

---

## File Ownership Declaration

Before issuing Rally, Titan MUST declare file ownership per team.

### Ownership Types

| Type | Meaning | Rule |
|------|---------|------|
| **exclusive_write** | Only this team writes here | No overlap between teams |
| **shared_read** | Any team can read | No restrictions |
| **interface_contract** | Shared types/interfaces | Must be resolved FIRST |

### Declaration Format

```markdown
## RALLY_FILE_OWNERSHIP
| Team | exclusive_write | shared_read | interface_contract |
|------|----------------|-------------|-------------------|
| Team A | src/feature-a/, tests/feature-a/ | src/types/ | src/types/feature-a.ts |
| Team B | src/feature-b/, tests/feature-b/ | src/types/ | src/types/feature-b.ts |
```

### Conflict Detection

1. **No exclusive_write overlap** — overlap detected → fall back to sequential
2. **Interface contracts first** — all contract files completed before teams start
3. **Config files** — shared_read only; config changes require sequential execution

---

## RALLY_AUTORUN Issuance Format

```markdown
## RALLY_AUTORUN
Teams:
  - name: [Team name]
    chain: [Agent1 → Agent2 → Agent3]
    task: [Epic description]
    acceptance: [Criteria]
    files:
      exclusive_write: [file/dir list]
      shared_read: [file/dir list]
  - name: [Team name]
    chain: [Agent4 → Agent5]
    task: [Epic description]
    acceptance: [Criteria]
    files:
      exclusive_write: [file/dir list]
      shared_read: [file/dir list]
Integration:
  shared_deps: [types, config — resolved before teams start]
  merge_strategy: [sequential-merge | branch-merge]
  integration_chain: Atlas → Radar → Judge
  acceptance: [Integration-level criteria]
```

---

## Shared Dependencies Resolution

Before Rally teams start:

1. **Identify shared types/interfaces** from architecture docs and specs
2. **Generate contracts first** via Nexus chain (Schema/Atlas)
3. **Verify completeness** — all teams confirm interfaces defined
4. **Lock shared files** — mark shared_read, no modifications during Rally

```
Titan: Identify shared deps
  → Nexus: Schema/Atlas → Generate shared types
  → Verify: All team interfaces covered
  → Lock: shared_read protection
  → Rally: Teams start parallel execution
```

---

## Result Merge Protocol

### Merge Sequence

```
All Rally teams complete
  ├─ 1. Collect results from each team
  ├─ 2. Check for unexpected file conflicts
  ├─ 3. Integration chain: Atlas → Radar → Judge
  │     ├─ Atlas: Verify no circular deps, interfaces aligned
  │     ├─ Radar: Full test suite (unit + integration)
  │     └─ Judge: Cross-team code quality review
  ├─ 4. Handle conflicts (if any)
  └─ 5. Update TITAN_STATE with merged results
```

### Integration Chain

| Step | Agent | Purpose | Failure Action |
|------|-------|---------|---------------|
| 1 | Atlas | Dependency analysis, circular ref detection | Flag conflicts → sequential resolution |
| 2 | Radar | Full test suite on merged code | Failed tests → identify team → L1 retry |
| 3 | Judge | Cross-team quality review | Quality issues → targeted Zen refactor |

---

## Conflict Resolution

### Resolution Rules

| Conflict Type | Resolution |
|--------------|-----------|
| Same file modified by both teams | Sequential re-execution of later team |
| Type/interface incompatibility | Re-generate shared types → both teams adapt |
| Test interference | Isolate tests per team, run separately |
| Import conflicts | Atlas resolution → auto-fix |

### Resolution Priority

1. **Types and interfaces** — resolve first (foundation)
2. **Config and shared state** — resolve second (runtime behavior)
3. **Implementation files** — resolve last (most flexible)
4. **Tests** — adapt to resolved implementation

---

## Common Rally Patterns by Phase

| Phase | Pattern | Teams |
|-------|---------|-------|
| BUILD | Feature parallel | Feature A, Feature B, ... |
| HARDEN | Concern parallel | Security, Performance, Quality |
| VALIDATE | Test parallel | E2E, UX, Experiment |
| LAUNCH | Output parallel | Docs, Demo, CI/CD |

### BUILD Phase Example

```markdown
## RALLY_AUTORUN
Teams:
  - name: auth-feature
    chain: Sherpa → Builder → Radar
    task: Implement authentication module
    files:
      exclusive_write: src/auth/, tests/auth/
      shared_read: src/types/, src/config/
  - name: dashboard-feature
    chain: Sherpa → Artisan → Radar
    task: Implement dashboard UI
    files:
      exclusive_write: src/dashboard/, tests/dashboard/
      shared_read: src/types/, src/components/shared/
Integration:
  shared_deps: src/types/user.ts, src/config/routes.ts
  integration_chain: Atlas → Radar → Judge
```

---

## Rally Failure Handling

| Scenario | Action |
|----------|--------|
| One team fails, others succeed | Accept successful → L1 retry failed team |
| Integration chain fails | Identify conflict → sequential resolution |
| All teams fail | Fall back to sequential Nexus execution |
| Shared deps incomplete | Abort Rally → resolve deps → restart |

Rally failures feed into Anti-Stall at L1 (team retry) or L2 (sequential fallback).
