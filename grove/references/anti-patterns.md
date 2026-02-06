# Repository Structure Anti-Patterns

Detection rules, severity levels, and remediation strategies.

---

## Anti-Pattern Catalog

### AP-001: God Directory

**Severity:** High
**Detection:** A single directory contains 50+ files at one level.

```
# BAD: Everything dumped in src/
src/
├── auth.ts
├── authController.ts
├── authService.ts
├── user.ts
├── userController.ts
├── userService.ts
├── payment.ts
├── ... (50+ more files)
```

**Impact:**
- Difficult to navigate and find files
- No logical grouping of related code
- Merge conflicts increase with team size

**Fix:**
```
# GOOD: Feature-based modules
src/
├── features/
│   ├── auth/
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   └── index.ts
│   ├── user/
│   └── payment/
└── shared/
```

**Audit command:**
```bash
# Count files per directory (flag directories with 50+ files)
find src -maxdepth 1 -type f | wc -l
```

---

### AP-002: Scattered Tests

**Severity:** High
**Detection:** Test files located outside `tests/` directory without co-location convention.

```
# BAD: Tests scattered across project
src/auth/auth.test.ts
src/user/__tests__/user.test.ts
tests/payment.test.ts
test/integration.test.ts
spec/e2e.test.ts
```

**Impact:**
- Inconsistent test discovery
- CI configuration complexity
- Hard to measure coverage by module

**Fix (Option A: Centralized):**
```
tests/
├── unit/
│   ├── auth/
│   └── user/
├── integration/
└── e2e/
```

**Fix (Option B: Co-located — Go/Rust convention):**
```
src/auth/
├── auth.service.ts
├── auth.service.test.ts    # Co-located
```

**Rule:** Choose ONE pattern and apply consistently. Do not mix.

---

### AP-003: Config Soup

**Severity:** Medium
**Detection:** 10+ configuration files at project root.

```
# BAD: Root cluttered with configs
/
├── .eslintrc.js
├── .eslintrc.json           # Duplicate!
├── .prettierrc
├── .prettierrc.js           # Duplicate!
├── tsconfig.json
├── tsconfig.build.json
├── tsconfig.test.json
├── jest.config.ts
├── vitest.config.ts         # Conflict with jest!
├── .babelrc
├── webpack.config.js
├── postcss.config.js
├── tailwind.config.js
├── next.config.js
├── ... (15+ more)
```

**Impact:**
- Visual noise in project root
- Duplicate/conflicting configurations
- Hard to understand which configs are active

**Fix:**
```
# GOOD: Consolidate where possible
/
├── config/                  # Non-standard configs
│   ├── webpack.config.js
│   └── postcss.config.js
├── eslint.config.js         # Flat config (one file)
├── tsconfig.json            # Must be at root
├── vitest.config.ts         # Choose ONE test framework
└── tailwind.config.js       # Framework requires root
```

**Strategies:**
1. Use flat configs (ESLint flat config, single tsconfig with `extends`)
2. Move non-root-required configs to `config/`
3. Eliminate duplicates (pick one format per tool)
4. Remove unused configs from abandoned tools

---

### AP-004: Script Chaos

**Severity:** Medium
**Detection:** Shell/helper scripts scattered at project root or in random locations.

```
# BAD: Scripts everywhere
/
├── setup.sh
├── deploy.sh
├── seed-db.sh
├── run-tests.sh
├── fix-permissions.sh
├── migrate.sh
├── utils/
│   └── backup.sh
├── helpers/
│   └── generate-cert.sh
```

**Impact:**
- No discoverability for available scripts
- Unclear which scripts are safe to run
- No categorization by purpose

**Fix:**
```
scripts/
├── setup.sh            # Environment setup
├── seed.sh             # Database seeding
├── deploy.sh           # Deployment
├── migrate.sh          # Database migration
└── README.md           # Script documentation
```

---

### AP-005: Doc Desert

**Severity:** High
**Detection:** No `docs/` directory, or `docs/` exists but is empty/contains only README.

```
# BAD: No documentation structure
/
├── src/
├── README.md           # Only documentation
└── (no docs/)
```

**Impact:**
- No requirements traceability
- No design decisions recorded
- Onboarding difficulty
- Knowledge locked in individuals

**Fix:**
```
docs/
├── prd/                # Requirements
├── specs/              # Specifications
├── design/             # Design documents
├── checklists/         # Implementation/review checklists
├── test-specs/         # Test specifications
├── adr/                # Architecture decisions
├── guides/             # Developer guides
└── api/                # API documentation
```

---

### AP-006: Orphaned Docs

**Severity:** Medium
**Detection:** `docs/` contains unstructured, flat files without subdirectories.

```
# BAD: Flat docs dump
docs/
├── api-design.md
├── auth-requirements.md
├── database-schema.md
├── deployment-notes.md
├── meeting-notes-2024-01.md    # Not technical documentation
├── old-design.md               # Stale document
├── README.md
├── setup-guide.md
├── todo.md                     # Not documentation
└── v2-migration-plan.md
```

**Impact:**
- No categorization, hard to find documents
- Stale documents mixed with current
- Non-documentation files pollute the directory

**Fix:**
1. Categorize into subdirectories (prd/, design/, guides/, etc.)
2. Remove non-documentation files (meeting notes, todos)
3. Archive stale documents or delete
4. Apply naming conventions (PRD-, HLD-, etc.)

---

### AP-007: Missing Specs

**Severity:** High
**Detection:** `docs/prd/` or `docs/design/` is empty or absent in a project with active development.

```
# BAD: Code without specifications
docs/
├── guides/
│   └── getting-started.md
└── api/
    └── openapi.yaml
# No prd/, no design/, no checklists/
```

**Impact:**
- No formal requirements → scope creep
- No design documents → inconsistent architecture
- No checklists → quality gaps

**Fix:**
- Create PRD for each feature before implementation
- Create HLD for system-level changes
- Create LLD for complex features
- Use implementation checklists for tracking

---

### AP-008: Flat Hell

**Severity:** Medium
**Detection:** All source files at single level, no subdirectories in `src/`.

```
# BAD: Everything flat
src/
├── app.ts
├── authController.ts
├── authMiddleware.ts
├── authService.ts
├── database.ts
├── logger.ts
├── paymentController.ts
├── paymentService.ts
├── userController.ts
├── userModel.ts
├── userService.ts
└── utils.ts
```

**Impact:**
- No module boundaries
- Circular dependency risk
- Cannot scale beyond ~20 files

**Fix:** Group by feature or layer (feature-based grouping preferred for most projects).

---

### AP-009: Nested Abyss

**Severity:** Medium
**Detection:** Directory nesting deeper than 6 levels from project root.

```
# BAD: Too deep
src/modules/core/services/auth/providers/oauth/google/handlers/callback/
└── handler.ts   # 10 levels deep
```

**Impact:**
- Long import paths
- Cognitive overhead navigating
- Often indicates over-engineering

**Fix:**
- Maximum 4-5 levels from project root
- Flatten unnecessarily deep structures
- Use path aliases to simplify imports

---

### AP-010: Duplicate Structures

**Severity:** Low
**Detection:** Multiple directories serving the same purpose.

```
# BAD: Duplicated purpose
/
├── lib/            # Shared code?
├── shared/         # Shared code?
├── utils/          # Shared code?
├── helpers/        # Shared code?
├── common/         # Shared code?
├── tests/          # Tests?
├── test/           # Tests?
├── __tests__/      # Tests?
└── spec/           # Tests?
```

**Fix:** Pick ONE name per purpose and consolidate.

---

## Severity Guide

| Severity | Description | Action |
|----------|-------------|--------|
| **High** | Actively impedes development | Fix immediately |
| **Medium** | Causes friction, scales poorly | Fix in next refactor |
| **Low** | Cosmetic / minor inconsistency | Fix when convenient |

---

## Audit Report Format

```markdown
## Repository Structure Audit

**Repository:** {name}
**Date:** YYYY-MM-DD
**Overall Health:** {score}/100

### Anti-Patterns Detected

| ID | Pattern | Severity | Location | Status |
|----|---------|----------|----------|--------|
| AP-001 | God Directory | High | src/ (67 files) | 🔴 |
| AP-005 | Doc Desert | High | docs/ missing | 🔴 |
| AP-003 | Config Soup | Medium | root (14 configs) | 🟡 |

### Structure Score Breakdown

| Category | Score | Max | Notes |
|----------|-------|-----|-------|
| Directory Structure | 15 | 25 | God Directory detected |
| Doc Completeness | 0 | 25 | No docs/ directory |
| Test Organization | 18 | 20 | Consistent structure |
| Config Hygiene | 8 | 15 | Too many root configs |
| Anti-pattern Score | 5 | 15 | 2 high severity issues |
| **Total** | **46** | **100** | |

### Recommendations (Priority Order)

1. **[High]** Create docs/ directory with standard structure
2. **[High]** Split src/ into feature modules
3. **[Medium]** Consolidate config files
```
