# Team Design Patterns

Catalog of team composition patterns used by Rally.
Select the optimal pattern based on the nature of the task.

---

## Pattern A: Frontend/Backend Split

**Team size:** 2-3
**When to use:** Projects where UI and API/data layers are clearly separated

```
Rally (Team Lead)
  ├── frontend-impl (general-purpose)
  │   └── exclusive_write: src/components/**, src/pages/**, src/styles/**
  ├── backend-impl (general-purpose)
  │   └── exclusive_write: src/api/**, src/services/**, src/models/**
  └── [optional] test-writer (general-purpose)
      └── exclusive_write: tests/**, __mocks__/**
```

**shared_read:** `src/types/**`, `src/config/**`, `package.json`

**Dependencies:**
- Type definition task executes first (no blockedBy)
- Frontend/backend start in parallel after type definitions complete
- Tests start after implementation completes

**Best suited for:**
- CRUD feature additions
- New page/endpoint pair implementation
- Authentication/authorization features

---

## Pattern B: Feature Parallel

**Team size:** 2-4
**When to use:** Implementing multiple independent features simultaneously

```
Rally (Team Lead)
  ├── feature-a (general-purpose)
  │   └── exclusive_write: src/features/feature-a/**
  ├── feature-b (general-purpose)
  │   └── exclusive_write: src/features/feature-b/**
  └── feature-c (general-purpose)
      └── exclusive_write: src/features/feature-c/**
```

**shared_read:** `src/shared/**`, `src/types/**`, `src/config/**`

**Dependencies:**
- All features fully independent → no blockedBy, immediate parallel
- If shared component changes are needed, consolidate to one teammate

**Best suited for:**
- Multiple independent screen implementations
- Independent endpoint additions across microservices
- Multiple bug fixes (when files don't overlap)

---

## Pattern C: Pipeline

**Team size:** 2-3
**When to use:** Work requiring staged phases like research → implementation → testing

```
Rally (Team Lead)
  ├── Phase 1: researcher (Explore) ← Investigation
  │   └── shared_read: src/** (no writes)
  ├── Phase 2: implementer (general-purpose) ← Implementation (after Phase 1)
  │   └── exclusive_write: src/**
  └── Phase 3: tester (general-purpose) ← Testing (after Phase 2)
      └── exclusive_write: tests/**
```

**Dependencies:**
- Phase 2 is blockedBy Phase 1
- Phase 3 is blockedBy Phase 2
- However, parts of Phase 1 and Phase 3 can overlap (e.g., test scaffold creation)

**Note:** Pipeline is inherently sequential. To increase parallelism:
- Researcher shares partial results so implementer can start early
- Tester pre-creates test scaffolds

**Best suited for:**
- Adding features to an unknown codebase
- Refactoring (impact analysis → implementation → regression tests)
- Performance improvement (profiling → fix → benchmarking)

---

## Pattern D: Specialist Team

**Team size:** 2-4
**When to use:** Tasks requiring different areas of expertise

```
Rally (Team Lead)
  ├── db-specialist (general-purpose)
  │   └── exclusive_write: migrations/**, src/models/**
  ├── api-specialist (general-purpose)
  │   └── exclusive_write: src/api/**, src/middleware/**
  └── security-specialist (general-purpose)
      └── exclusive_write: src/auth/**, src/security/**
```

**Best suited for:**
- Security feature additions (auth + encryption + audit logging)
- Database migration + API update + testing
- Feature additions involving infrastructure changes

---

## Pattern E: Code/Test/Docs Triple

**Team size:** 3
**When to use:** Advancing code, tests, and documentation simultaneously

```
Rally (Team Lead)
  ├── coder (general-purpose)
  │   └── exclusive_write: src/**
  ├── tester (general-purpose)
  │   └── exclusive_write: tests/**
  └── documenter (general-purpose)
      └── exclusive_write: docs/**, README.md
```

**Dependencies:**
- Coder and documenter can start in parallel (documenter begins with design docs)
- Tester starts after coder's type/interface definitions are complete
- Documenter does final API doc update (after coder finishes)

**Best suited for:**
- Full feature implementation (code + tests + documentation)
- OSS library feature additions

---

## Team Size Decision Criteria

| Factor | Small (2) | Medium (3) | Large (4-5) |
|--------|-----------|------------|-------------|
| Files changed | 2-3 | 4-8 | 9+ |
| Independence | Splittable into 2 areas | Splittable into 3 areas | Splittable into 4+ areas |
| Task complexity | Low-Medium | Medium | Medium-High |
| Time pressure | None | Present | Tight |

**Principle:** When in doubt, choose the **smaller team**. Coordination cost scales quadratically with team size.

---

## subagent_type Selection Guide

| subagent_type | Available Tools | Suitable Tasks |
|---------------|----------------|----------------|
| `general-purpose` | All tools (Edit, Write, Bash, Glob, Grep, Read, Task, etc.) | Implementation, test writing, bug fixes, refactoring |
| `Explore` | Read-only (Glob, Grep, Read, WebFetch, WebSearch) | Code investigation, impact analysis, documentation research |
| `Plan` | Read-only (Glob, Grep, Read) | Design documents, architecture review, implementation planning |
| `Bash` | Bash only | Build execution, test running, deploy scripts |

**Important:** `Explore` and `Plan` are **read-only**. Never assign implementation tasks to them.

---

## Model Selection Guide

| Model | Cost | Recommended Use |
|-------|------|-----------------|
| `opus` | High | Complex architecture design, security-related code, large-scale refactoring |
| `sonnet` | Medium (default) | General feature implementation, test writing, bug fixes |
| `haiku` | Low | Boilerplate fixes, formatting changes, simple replacements, doc updates |

**Cost optimization principles:**
1. Default is `sonnet` (behavior when unspecified)
2. Aggressively use `haiku` for simple tasks
3. Use `opus` only when truly needed (security, complex design)
4. Investigation tasks (Explore) often work fine with `haiku`
