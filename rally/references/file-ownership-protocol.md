# File Ownership Protocol

Rally's file ownership management protocol.
A strict rule system to prevent edit conflicts during parallel work.

---

## Core Principles

1. **Exclusive write**: Only one teammate may have write access to any given file
2. **Shared read**: All teammates may read any file
3. **Declaration first**: Complete ownership declaration before spawning
4. **No gaps**: Every file to be modified must have an owner

---

## Ownership Declaration Format

### YAML Format

```yaml
ownership_map:
  [teammate_name]:
    exclusive_write:
      - [glob pattern 1]
      - [glob pattern 2]
    shared_read:
      - [glob pattern 1]
      - [glob pattern 2]
```

### Example: Frontend/Backend Split

```yaml
ownership_map:
  frontend-impl:
    exclusive_write:
      - src/components/**
      - src/pages/**
      - src/styles/**
      - src/hooks/**
    shared_read:
      - src/types/**
      - src/config/**
      - src/utils/**
      - package.json
  backend-impl:
    exclusive_write:
      - src/api/**
      - src/services/**
      - src/models/**
      - src/middleware/**
    shared_read:
      - src/types/**
      - src/config/**
      - src/utils/**
      - package.json
  test-writer:
    exclusive_write:
      - tests/**
      - __mocks__/**
      - jest.config.*
    shared_read:
      - src/**
```

---

## Directory-Based vs File-Based

### Directory-Based (Recommended)

Assign ownership at the directory level. Simpler to manage and less error-prone.

```yaml
frontend-impl:
  exclusive_write:
    - src/components/**   # Everything under this directory
    - src/pages/**
```

### File-Based

Use when files within the same directory must be split between teammates.

```yaml
teammate-a:
  exclusive_write:
    - src/utils/auth.ts
    - src/utils/token.ts
teammate-b:
  exclusive_write:
    - src/utils/validation.ts
    - src/utils/formatting.ts
```

**Caution:** File-based ownership has higher risk of errors. Use directory-based whenever possible.

---

## shared_read Rules

The following file categories should always be treated as `shared_read`:

| Category | Example Files | Reason |
|----------|--------------|--------|
| Type definitions | `src/types/**`, `*.d.ts` | Contracts referenced by everyone |
| Config files | `tsconfig.json`, `.eslintrc`, `package.json` | Project-wide settings |
| Environment | `.env.example` | Configuration reference |
| Utilities | `src/utils/**`, `src/lib/**` | Common logic |
| Constants | `src/constants/**` | Shared values |

**Important:** If a `shared_read` file needs modification, grant `exclusive_write` to **one teammate only**.

---

## Conflict Detection Methods

### Pre-Spawn Check

Validate the ownership map before spawning:

```
Check 1: No exclusive_write overlaps
  → teammate_a: src/components/**
  → teammate_b: src/components/Button.tsx  ← Overlap!

Check 2: All target files have an owner
  → src/middleware/auth.ts  ← No owner!

Check 3: shared_read / exclusive_write consistency
  → teammate_a: shared_read: src/types/**
  → teammate_b: exclusive_write: src/types/auth.ts  ← OK (one explicit writer)
```

### Runtime Check

Against teammate deliverables:
1. Collect `files_changed` from each teammate
2. Cross-reference against ownership map
3. Detect changes outside owned files → warn / rollback

---

## Conflict Resolution Flow

```
Conflict detected
    ↓
┌──────────────────┐
│ Classify conflict │
└────────┬─────────┘
         ↓
  ┌──────┴──────────┐
  ↓                 ↓
Minor (no same     Major (same line
 lines)              changes)
  ↓                 ↓
Auto-resolve       Manual merge or
via git merge      ON_RESULT_CONFLICT
                   trigger fires
```

### Resolution Options

1. **Re-partition ownership**: Consolidate conflicting files under one teammate
2. **Sequential execution**: Order affected tasks via blockedBy
3. **Interface separation**: Define a common interface first, then separate implementations
4. **Manual merge**: Delegate judgment to the user

---

## Ownership Templates

### Web Application (Typical)

```yaml
ownership_map:
  frontend:
    exclusive_write:
      - src/components/**
      - src/pages/**
      - src/styles/**
      - src/hooks/**
      - public/**
    shared_read:
      - src/types/**
      - src/config/**
  backend:
    exclusive_write:
      - src/api/**
      - src/services/**
      - src/models/**
      - src/middleware/**
      - prisma/**
    shared_read:
      - src/types/**
      - src/config/**
```

### Microservices (Service-Based Split)

```yaml
ownership_map:
  auth-service:
    exclusive_write:
      - services/auth/**
    shared_read:
      - shared/types/**
      - shared/config/**
  user-service:
    exclusive_write:
      - services/user/**
    shared_read:
      - shared/types/**
      - shared/config/**
```

### Monorepo (Package-Based Split)

```yaml
ownership_map:
  pkg-core:
    exclusive_write:
      - packages/core/**
    shared_read:
      - packages/types/**
  pkg-ui:
    exclusive_write:
      - packages/ui/**
    shared_read:
      - packages/types/**
      - packages/core/src/index.ts  # public API only
```
