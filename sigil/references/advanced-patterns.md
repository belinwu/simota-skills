# Advanced Patterns

Conditional skills, parameterized templates, monorepo patterns, skill composition, multi-language support, and learning from existing skills.

---

## Conditional Skills

Skills that adapt their output based on project context.

### Pattern: Branch by Framework Version

```markdown
## テンプレート

### Next.js App Router (next >= 13.4)

\```tsx
// App Router pattern with Server Components
export default async function Page() { ... }
\```

### Next.js Pages Router (next < 13.4)

\```tsx
// Pages Router pattern with getServerSideProps
export const getServerSideProps = async () => { ... }
\```
```

### Pattern: Branch by CSS Approach

```markdown
## スタイリング

> **検出ロジック**: tailwind.config → Tailwind, *.module.css → CSS Modules, styled-components in deps → Styled Components

### Tailwind CSS
\```tsx
<div className="flex items-center gap-4">
\```

### CSS Modules
\```tsx
import styles from './Component.module.css'
<div className={styles.container}>
\```
```

### Implementation Rule

- Always detect the condition during SCAN phase
- Include ALL applicable branches (don't assume one approach)
- Mark the detected branch with `(このプロジェクトで使用)` annotation

---

## Parameterized Templates

Template variables that Sigil fills during CRAFT phase.

### Standard Variables

| Variable | Source | Example |
|----------|--------|---------|
| `[ProjectName]` | Manifest name field | `my-app` |
| `[Framework]` | Framework detection | `Next.js` |
| `[FrameworkVersion]` | Manifest dependencies | `14.1.0` |
| `[ComponentDir]` | Directory analysis | `src/components` |
| `[TestDir]` | Test location detection | `__tests__` |
| `[TestFramework]` | DevDependency detection | `vitest` |
| `[CSSApproach]` | Config/dependency detection | `tailwind` |
| `[PackageManager]` | Lock file detection | `pnpm` |
| `[ImportAlias]` | tsconfig.json paths | `@/` |

### Substitution Rules

1. Variables in `[Brackets]` → replace with detected values
2. If value unknown → use framework default with `<!-- TODO: verify -->` comment
3. If multiple values possible → use conditional branch pattern instead
4. Never leave raw `[Variable]` placeholders in installed skills

---

## Monorepo Patterns

### Detection

| File | Monorepo Tool | Scope Strategy |
|------|--------------|----------------|
| `turbo.json` | Turborepo | Per-package skills + shared root skills |
| `nx.json` | Nx | Per-project skills + library skills |
| `pnpm-workspace.yaml` | pnpm workspaces | Per-package skills |
| `lerna.json` | Lerna | Per-package skills |
| `packages/*/package.json` | Generic | Per-package skills |

### Skill Scoping Strategy

```
monorepo-root/
├── .claude/skills/
│   ├── naming-rules/SKILL.md    ← Shared skills
│   └── pr-template/SKILL.md
├── .agents/skills/              ← Mirror of shared skills
│   ├── naming-rules/SKILL.md
│   └── pr-template/SKILL.md
├── packages/
│   ├── web/
│   │   ├── .claude/skills/
│   │   │   ├── new-page/SKILL.md       ← Web-specific skills
│   │   │   └── new-component/SKILL.md
│   │   └── .agents/skills/             ← Mirror
│   ├── api/
│   │   ├── .claude/skills/
│   │   │   ├── new-route/SKILL.md      ← API-specific skills
│   │   │   └── new-middleware/SKILL.md
│   │   └── .agents/skills/             ← Mirror
│   └── shared/
│       ├── .claude/skills/
│       │   └── new-util/SKILL.md       ← Shared library skills
│       └── .agents/skills/             ← Mirror
```

### Rules

- Root skills: Cross-cutting concerns (conventions, PR templates, deploy)
- Package skills: Framework-specific workflows (new-page for web, new-route for api)
- Shared package skills: Utility creation patterns
- Never duplicate a root skill inside a package
- Always sync `.claude/skills/*/SKILL.md` and `.agents/skills/*/SKILL.md` at each level

---

## Skill Composition

Patterns for skills that depend on or reference other skills.

### Pattern: Prerequisite Chain

```markdown
## 前提条件
- `naming-rules` スキルの規約に準拠すること
- `env-setup` スキルで環境変数が設定済みであること
```

### Pattern: Workflow Orchestration

```markdown
## 完全なフィーチャー作成フロー

1. `new-model` → データモデル作成
2. `new-service` → ビジネスロジック作成
3. `new-controller` → APIエンドポイント作成
4. `new-test` → テスト作成

各スキルを順番に実行すること。
```

### Rules

- Reference other skills by `name` (kebab-case)
- Never embed another skill's content — reference only
- If dependency creates circular reference → merge the skills
- Composition chains should be max 4-5 skills deep

---

## Multi-Language Projects

### Detection

| Signal | Languages | Skill Strategy |
|--------|-----------|---------------|
| `package.json` + `go.mod` | JS/TS + Go | Separate skill sets per language |
| `package.json` + `pyproject.toml` | JS/TS + Python | Separate skill sets per language |
| `Cargo.toml` + `package.json` | Rust + JS/TS (WASM) | Bridge skills for interop |
| Multiple `go.mod` | Go monorepo | Per-module skills |

### Naming Convention for Multi-Language Skills

```
[language-prefix]-[skill-name]/SKILL.md

Examples:
  ts-new-component/SKILL.md
  go-new-handler/SKILL.md
  py-new-router/SKILL.md
```

### Shared Cross-Language Skills

These skills apply regardless of language and don't need prefix:
- `naming-rules.md` (consolidated across languages)
- `pr-template.md`
- `deploy-flow.md`
- `env-setup.md`

---

## Learning from Existing Skills

When a project already has skills in `.claude/skills/*/SKILL.md` or `.agents/skills/*/SKILL.md`, Sigil should learn from them.

### What to Learn

| Aspect | Detection Method | Application |
|--------|-----------------|-------------|
| **Tone** | Formal vs casual language in descriptions | Match in new skills |
| **Structure** | Section order and naming | Follow same pattern |
| **Depth** | Lines per section, detail level | Match granularity |
| **Language** | Japanese vs English descriptions | Match language choice |
| **Template style** | Inline vs separate code blocks | Follow same approach |

### Learning Workflow

1. Read all existing skills in both directories
2. Identify common patterns (section structure, naming, depth)
3. Create a "style profile" for the project's skill set
4. Apply style profile to all newly generated skills
5. Flag significant deviations for user review

### Rules

- New skills should feel like they belong to the same author
- If existing skills have quality issues, don't propagate them — note for evolution
- If no existing skills, use Sigil's default templates from `skill-templates.md`
