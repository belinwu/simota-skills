# Context Analysis

Tech stack detection patterns, directory structure analysis, convention inference rules, monorepo support, and multi-language project handling for project skill generation.

---

## Tech Stack Detection

### Manifest File Mapping

| File | Stack | Key Fields |
|------|-------|------------|
| `package.json` | Node.js/JavaScript/TypeScript | dependencies, devDependencies, scripts |
| `tsconfig.json` | TypeScript | compilerOptions.strict, paths, baseUrl |
| `go.mod` | Go | module, require |
| `Cargo.toml` | Rust | dependencies, features |
| `pyproject.toml` / `setup.py` / `requirements.txt` | Python | dependencies, tool.poetry |
| `Gemfile` | Ruby | gem entries |
| `pom.xml` / `build.gradle` | Java/Kotlin | dependencies, plugins |
| `composer.json` | PHP | require, autoload |
| `pubspec.yaml` | Dart/Flutter | dependencies |
| `mix.exs` | Elixir | deps |
| `bun.lockb` / `bunfig.toml` | Bun runtime | (Bun-specific runtime detection) |

### Framework Detection

| Framework | Detection Signal | Priority Skills |
|-----------|-----------------|-----------------|
| **Next.js** | `next` in dependencies + `next.config.*` | new-page, new-api-route, new-component |
| **React (CRA/Vite)** | `react` + no `next` | new-component, new-hook, new-context |
| **Vue.js** | `vue` in dependencies | new-component, new-composable, new-store |
| **Nuxt** | `nuxt` in dependencies | new-page, new-server-route, new-composable |
| **Remix** | `@remix-run/node` in dependencies | new-route, new-loader, new-action |
| **Express** | `express` in dependencies | new-route, new-middleware, new-controller |
| **Fastify** | `fastify` in dependencies | new-route, new-plugin, new-schema |
| **Hono** | `hono` in dependencies | new-route, new-middleware, new-validator |
| **NestJS** | `@nestjs/core` in dependencies | new-module, new-controller, new-service |
| **tRPC** | `@trpc/server` in dependencies | new-router, new-procedure, new-middleware |
| **FastAPI** | `fastapi` in pyproject/requirements | new-router, new-model, new-schema |
| **Django** | `django` in requirements | new-app, new-model, new-view |
| **Rails** | `rails` in Gemfile | new-model, new-controller, new-migration |
| **Go (stdlib)** | `go.mod` present, no major framework | new-handler, new-middleware, new-model |
| **Gin** | `github.com/gin-gonic/gin` | new-handler, new-middleware |
| **Actix** | `actix-web` in Cargo.toml | new-handler, new-service |
| **Spring Boot** | `spring-boot-starter` in pom/gradle | new-controller, new-service, new-repository |
| **Laravel** | `laravel/framework` in composer | new-controller, new-model, new-migration |
| **Flutter** | `flutter` in pubspec.yaml | new-screen, new-widget, new-bloc |
| **SvelteKit** | `@sveltejs/kit` in dependencies | new-route, new-component, new-server |

---

## Directory Structure Analysis

### Common Patterns

| Pattern | Convention | Implication |
|---------|-----------|-------------|
| `src/app/` | Next.js App Router | Route-based file organization |
| `src/pages/` | Next.js Pages Router / Nuxt | File-based routing |
| `src/components/` | Component library | Shared component directory |
| `src/hooks/` or `src/composables/` | Custom hooks/composables | Reusable logic pattern |
| `src/lib/` or `src/utils/` | Utility functions | Shared utility directory |
| `src/services/` | Service layer | API/business logic separation |
| `src/stores/` or `src/store/` | State management | Centralized state |
| `__tests__/` or `*.test.*` or `*.spec.*` | Testing convention | Co-located vs separated tests |
| `e2e/` or `cypress/` or `playwright/` | E2E tests | E2E test framework |
| `prisma/` | Prisma ORM | Database schema location |
| `drizzle/` | Drizzle ORM | Database schema location |
| `migrations/` | DB migrations | Migration file location |
| `cmd/` | Go CLI entry points | Multi-binary project |
| `internal/` | Go internal packages | Private package convention |

### File Naming Convention Detection

1. Check existing files for pattern: `kebab-case.ts`, `camelCase.ts`, `PascalCase.tsx`, `snake_case.py`
2. Check component naming: `Button.tsx` vs `button.tsx` vs `button/index.tsx`
3. Check test co-location: `Button.test.tsx` next to `Button.tsx` vs `__tests__/Button.test.tsx`

---

## Monorepo Detection & Analysis

### Detection Signals

| File | Tool | Analysis Scope |
|------|------|---------------|
| `turbo.json` | Turborepo | Read `pipeline` keys for task relationships |
| `nx.json` | Nx | Read `projects` and `targetDefaults` |
| `pnpm-workspace.yaml` | pnpm workspaces | Read `packages` globs |
| `lerna.json` | Lerna | Read `packages` configuration |
| Root `package.json` with `workspaces` | npm/yarn workspaces | Read `workspaces` array |

### Monorepo Skill Generation Strategy

1. **Root-level scan**: Detect monorepo tool, enumerate packages
2. **Per-package scan**: Run full SCAN for each package independently
3. **Shared skills**: Generate cross-cutting skills at root level (naming-rules, pr-template, deploy-flow)
4. **Package-specific skills**: Generate framework-specific skills per package
5. **Deduplication**: Ensure no root skill duplicates a package skill

### Package Priority Order

1. **Primary application packages** (web, app, frontend)
2. **API/backend packages** (api, server, backend)
3. **Shared libraries** (shared, common, utils)
4. **Tooling packages** (config, scripts)

---

## Multi-Language Project Detection

### Detection Patterns

| Pattern | Languages | Skill Strategy |
|---------|-----------|---------------|
| `package.json` + `go.mod` in same repo | JS/TS + Go | Separate skill sets, shared conventions |
| `package.json` + `pyproject.toml` in same repo | JS/TS + Python | Separate skill sets, shared conventions |
| `Cargo.toml` + `package.json` (WASM) | Rust + JS/TS | Bridge skills for WASM interop |
| Multiple manifest files in subdirectories | Polyglot monorepo | Per-directory language skills |

### Handling Multi-Language Projects

1. Detect all manifest files and their locations
2. Group by language/framework
3. Generate language-specific skill sets independently
4. Create shared cross-language skills (naming-rules, pr-template)
5. Use language prefix for disambiguation when needed: `ts-new-component.md`, `go-new-handler.md`

---

## Convention Inference Rules

### Priority Order for Convention Detection

1. **Explicit config** — .eslintrc, .prettierrc, CLAUDE.md rules
2. **Existing code patterns** — Majority pattern wins (sample 10+ files)
3. **Framework defaults** — Use framework's recommended conventions
4. **Community standards** — Fall back to ecosystem norms

### Key Conventions to Detect

| Convention | How to Detect | Skill Impact |
|-----------|--------------|-------------|
| **Component structure** | Read 3+ existing components | Template generation |
| **Import style** | Alias paths vs relative, barrel exports | Import statements in templates |
| **State management** | Store files, context usage | State patterns in skills |
| **API layer** | fetch/axios/tRPC usage | Data fetching patterns |
| **Testing framework** | jest/vitest/pytest/go test | Test template generation |
| **CSS approach** | Tailwind/CSS Modules/styled-components | Styling in templates |
| **Error handling** | Try-catch patterns, Result types, error boundaries | Error patterns in skills |
| **Logging** | Logger library, console usage | Logging patterns |

---

## Config File Analysis

### Build & Tooling

| File | Insights |
|------|----------|
| `Makefile` / `Taskfile.yml` | Available commands, workflow automation opportunities |
| `docker-compose.yml` | Service architecture, local dev setup |
| `.github/workflows/*.yml` | CI/CD pipeline, deployment patterns |
| `.husky/` / `.lefthook.yml` | Git hooks, pre-commit checks |
| `turbo.json` / `nx.json` | Monorepo configuration |

### Code Quality

| File | Insights |
|------|----------|
| `.eslintrc*` / `eslint.config.*` | Linting rules, code style enforcement |
| `.prettierrc*` | Formatting preferences |
| `tsconfig.json` | TypeScript strictness, module resolution |
| `.editorconfig` | Editor settings (indent, line endings) |

---

## Existing Skills Audit

Before generating new skills, check:

1. **Project `.claude/skills/`** — Already installed skills
2. **Project `.agents/skills/`** — Already installed skills (mirror directory)
3. **Project `CLAUDE.md`** — Established conventions that might overlap with skills
4. **Ecosystem agents** — Ensure generated skills don't duplicate agent functionality

**Cross-directory deduplication:** A skill existing in either `.claude/skills/` or `.agents/skills/` counts as "existing". Do not generate a skill that already exists in either directory.

### Directory Sync Check

Both directories must be kept in sync (identical contents). During SCAN, detect sync drift:

1. List skills in `.claude/skills/` and `.agents/skills/`
2. Identify skills that exist in only one directory (orphans)
3. For each orphan, copy to the missing directory to restore sync
4. Report any sync repairs performed

### Duplication Detection

A skill is a duplicate if:
- Same name as existing skill (in either directory)
- > 70% functional overlap with existing skill (in either directory)
- Covers same workflow as an existing ecosystem agent's core function

---

## Existing Skill Learning

When the project already has skills, learn from them to maintain consistency.

### Style Profile Extraction

1. **Read all existing skills** in both `.claude/skills/` and `.agents/skills/`
2. **Analyze patterns**:
   - Section ordering and naming (Japanese vs English headings)
   - Description language and tone (formal vs casual)
   - Template depth (minimal vs comprehensive)
   - Code example style (inline vs separate blocks)
   - Checklist usage (present vs absent)
3. **Create style profile**: Document detected patterns
4. **Apply to new skills**: Match existing style in all new generations

### Consistency Rules

- If existing skills use Japanese section headings → use Japanese
- If existing skills use English section headings → use English
- If existing skills include checklists → include checklists
- If existing skills are verbose (>60 lines for Micro) → match depth
- If existing skills are concise (<30 lines for Micro) → match brevity
- If no existing skills → use Sigil's default templates from `skill-templates.md`
