# Directory Templates

Language-specific directory structure templates and conventions.

---

## Universal Base Structure

Every project, regardless of language, should have this base:

```
{project}/
├── src/                    # Source code
├── tests/                  # Test files
├── docs/                   # Documentation (see docs-structure.md)
├── scripts/                # Helper scripts (setup, seed, deploy)
├── tools/                  # Internal CLI/TUI tools
├── config/                 # Configuration files
├── infra/                  # Infrastructure as Code
├── .github/                # CI/CD workflows
├── .agents/                # Agent journals
│   └── PROJECT.md
├── README.md
├── CHANGELOG.md
└── LICENSE
```

---

## TypeScript / JavaScript

### Standard Project

```
src/
├── features/               # Feature modules
│   ├── auth/
│   │   ├── auth.service.ts
│   │   ├── auth.controller.ts
│   │   ├── auth.types.ts
│   │   └── index.ts        # Barrel export
│   └── user/
│       ├── user.service.ts
│       ├── user.repository.ts
│       ├── user.types.ts
│       └── index.ts
├── shared/                 # Shared utilities
│   ├── utils/
│   ├── types/
│   └── constants/
├── config/                 # App configuration
│   ├── database.ts
│   └── env.ts
└── index.ts                # Entry point

tests/
├── unit/
│   └── features/
│       ├── auth/
│       └── user/
├── integration/
│   └── api/
├── e2e/
│   └── flows/
└── fixtures/
    ├── users.json
    └── helpers.ts
```

### Key Conventions

- Barrel exports (`index.ts`) per feature module
- Path aliases in `tsconfig.json`: `@/features/*`, `@/shared/*`
- Co-located types within feature modules
- Test directory mirrors `src/` structure

### React / Next.js Frontend

```
src/
├── app/                    # Next.js App Router (or pages/)
│   ├── (auth)/
│   │   ├── login/
│   │   └── register/
│   ├── dashboard/
│   └── layout.tsx
├── components/             # UI Components
│   ├── ui/                 # Primitive components (Button, Input)
│   ├── features/           # Feature-specific components
│   └── layouts/            # Layout components
├── hooks/                  # Custom React hooks
├── lib/                    # Utility functions
├── services/               # API client / external services
├── stores/                 # State management (Zustand, Jotai)
├── styles/                 # Global styles, design tokens
│   ├── tokens.css
│   └── globals.css
└── types/                  # Shared type definitions
```

---

## Python

### Standard Project

```
src/
└── {package_name}/         # Top-level package
    ├── __init__.py
    ├── main.py             # Entry point
    ├── features/
    │   ├── __init__.py
    │   ├── auth/
    │   │   ├── __init__.py
    │   │   ├── service.py
    │   │   ├── models.py
    │   │   └── schemas.py
    │   └── user/
    │       ├── __init__.py
    │       ├── service.py
    │       ├── models.py
    │       └── schemas.py
    ├── shared/
    │   ├── __init__.py
    │   ├── utils.py
    │   ├── exceptions.py
    │   └── constants.py
    └── config/
        ├── __init__.py
        └── settings.py

tests/
├── conftest.py
├── unit/
│   └── features/
│       ├── test_auth.py
│       └── test_user.py
├── integration/
│   └── test_api.py
└── fixtures/
    └── data.py
```

### Key Conventions

- Package name matches `pyproject.toml` `[project.name]`
- `__init__.py` with explicit `__all__` for public API
- `conftest.py` at test root for shared fixtures
- Type hints throughout, validated by mypy/pyright

### FastAPI / Django Variant

```
# FastAPI
src/{package}/
├── api/
│   ├── v1/
│   │   ├── endpoints/
│   │   └── router.py
│   └── deps.py
├── core/
│   ├── config.py
│   └── security.py
├── models/
├── schemas/
└── services/

# Django
src/{project}/
├── {project}/              # Project settings
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── auth/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── tests/
│   └── user/
└── manage.py
```

---

## Go

### Standard Project

```
cmd/                        # Entry points
├── server/
│   └── main.go
└── cli/
    └── main.go

internal/                   # Private packages (not importable)
├── auth/
│   ├── handler.go
│   ├── service.go
│   ├── repository.go
│   └── auth_test.go        # Co-located tests
├── user/
│   ├── handler.go
│   ├── service.go
│   └── user_test.go
└── shared/
    ├── middleware/
    ├── config/
    └── errors/

pkg/                        # Public packages (importable)
├── httputil/
└── validation/

tests/                      # Integration / E2E tests
├── integration/
└── e2e/

api/                        # API definitions (OpenAPI, protobuf)
└── openapi.yaml
```

### Key Conventions

- `cmd/` for binaries, `internal/` for private, `pkg/` for public
- Unit tests co-located with source (`*_test.go`)
- Integration tests in separate `tests/` directory
- No `src/` directory (Go convention)
- Flat package structure preferred over deep nesting

---

## Rust

### Standard Project (Binary)

```
src/
├── main.rs                 # Entry point
├── lib.rs                  # Library root (optional)
├── features/
│   ├── mod.rs
│   ├── auth/
│   │   ├── mod.rs
│   │   ├── service.rs
│   │   └── models.rs
│   └── user/
│       ├── mod.rs
│       └── service.rs
├── shared/
│   ├── mod.rs
│   ├── config.rs
│   └── errors.rs
└── tests/                  # Integration tests (cargo convention)
    ├── auth_test.rs
    └── common/
        └── mod.rs

benches/                    # Benchmarks
└── bench_main.rs
```

### Workspace (Multi-crate)

```
Cargo.toml                  # Workspace definition
crates/
├── core/
│   ├── Cargo.toml
│   └── src/
├── api/
│   ├── Cargo.toml
│   └── src/
├── cli/
│   ├── Cargo.toml
│   └── src/
└── shared/
    ├── Cargo.toml
    └── src/
```

### Key Conventions

- Unit tests inline with `#[cfg(test)] mod tests`
- Integration tests in `tests/` directory
- Workspace for multi-crate projects
- `benches/` for criterion benchmarks

---

## Monorepo

### Turborepo / pnpm Workspace

```
apps/                       # Deployable applications
├── web/                    # Frontend app
│   ├── src/
│   ├── package.json
│   └── tsconfig.json
├── api/                    # Backend app
│   ├── src/
│   ├── package.json
│   └── tsconfig.json
└── admin/                  # Admin panel
    └── ...

packages/                   # Shared packages
├── ui/                     # Shared UI components
│   ├── src/
│   └── package.json
├── config/                 # Shared configurations
│   ├── eslint/
│   ├── typescript/
│   └── package.json
├── types/                  # Shared type definitions
│   └── package.json
└── utils/                  # Shared utilities
    └── package.json

docs/                       # Monorepo-level docs
scripts/                    # Monorepo-level scripts
infra/                      # Shared infrastructure

turbo.json                  # Pipeline configuration
pnpm-workspace.yaml         # Workspace definition
```

### Nx Workspace

```
apps/
├── web/
└── api/

libs/                       # Shared libraries (Nx convention)
├── shared/
│   ├── ui/
│   ├── utils/
│   └── types/
├── feature/
│   ├── auth/
│   └── user/
└── data-access/
    ├── api-client/
    └── database/

nx.json
```

### Key Conventions

- `apps/` for deployables, `packages/` (or `libs/`) for shared
- Each package has its own `package.json` and `tsconfig.json`
- Shared configs in `packages/config/`
- Root `docs/` for project-wide documentation
- Per-app docs in `apps/{app}/docs/` if needed

---

## Directory Responsibility Matrix

| Directory | Owner Agent | Purpose | Required |
|-----------|------------|---------|----------|
| `src/` | Builder, Artisan | Source code | Yes |
| `tests/` | Radar, Voyager | Test files | Yes |
| `docs/` | Scribe, Quill, Atlas, Gateway, Canvas | Documentation | Yes |
| `scripts/` | Anvil, Builder | Helper scripts | Recommended |
| `tools/` | Anvil | Internal CLI/TUI | Optional |
| `config/` | Gear | Environment config | Recommended |
| `infra/` | Scaffold | IaC | Optional |
| `.github/` | Gear, Guardian | CI/CD | Recommended |
| `.agents/` | All agents | Journals | Yes |
