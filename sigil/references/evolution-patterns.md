# Evolution Patterns

Skill lifecycle management, evolution triggers, update strategies, and migration patterns.

---

## Skill Lifecycle States

```
ACTIVE → STALE → DEPRECATED → ARCHIVED
  ↑        │         │
  └── UPDATE ←┘         │
  ↑                     │
  └──── REPLACE ←───────┘
```

| State | Definition | Detection | Action |
|-------|-----------|-----------|--------|
| **ACTIVE** | Skill matches current project context | Quality score ≥ 9/12 on re-evaluation | None — skill is healthy |
| **STALE** | Skill partially mismatches current context | Quality score 6-8/12 on re-evaluation | Trigger evolution workflow |
| **DEPRECATED** | Skill significantly outdated or superseded | Quality score < 6/12 or replaced by successor | Mark deprecated, create successor |
| **ARCHIVED** | Skill no longer applicable to project | Framework/library removed from project | Remove from active directories |

---

## Evolution Triggers

### Automatic Detection (during SCAN)

| Trigger | Detection Method | Example |
|---------|-----------------|---------|
| **Dependency version change** | Compare manifest versions with skill assumptions | React 18 → 19 (Server Components) |
| **Framework migration** | Detect framework change in manifest | Pages Router → App Router |
| **New convention adoption** | Config file changes (.eslintrc, tsconfig) | Strict mode enabled |
| **Directory restructure** | Directory layout differs from skill paths | src/ → app/ migration |
| **Testing framework change** | Test runner change in devDependencies | Jest → Vitest |

### User-Initiated

| Trigger | Signal |
|---------|--------|
| **Explicit request** | User asks to update/refresh skills |
| **Bug report** | User reports skill generates incorrect code |
| **Feature request** | User wants skill to cover new patterns |

---

## Update Strategies

### Strategy 1: In-Place Update (Default)

**When**: Minor changes, convention updates, small additions.

1. Read existing skill content
2. Identify sections needing update
3. Modify only affected sections
4. Preserve all unaffected content and structure
5. Re-validate with quality scoring

**Example**: Updating import paths after tsconfig alias change.

### Strategy 2: Replace

**When**: Major framework migration, fundamental approach change.

1. Archive old skill (rename with `.deprecated.md` suffix)
2. Generate entirely new skill from current context
3. Preserve original skill name for continuity
4. Log replacement in `.agents/PROJECT.md`

**Example**: Rewriting Next.js skill from Pages Router to App Router.

### Strategy 3: Split

**When**: Skill has grown too complex, covers multiple concerns.

1. Identify distinct responsibilities in current skill
2. Generate 2-3 focused Micro Skills from one Full Skill
3. Archive original skill
4. Update any references to original skill

**Example**: Splitting `api-pattern` into `new-api-route` + `auth-middleware` + `error-handling`.

### Strategy 4: Merge

**When**: Multiple small skills overlap significantly.

1. Identify skills with >50% functional overlap
2. Combine into single comprehensive skill
3. Archive merged skills
4. Promote to Full Skill if complexity warrants

**Example**: Merging `new-get-route` + `new-post-route` into `new-api-route`.

---

## Migration Patterns

### Framework Version Upgrade

```
1. Detect version change in manifest
2. Identify breaking changes (check changelog/migration guide patterns)
3. Map old patterns → new patterns
4. Update templates in affected skills
5. Update convention references
6. Re-validate all affected skills
```

### Framework Switch

```
1. Detect framework removal + addition in manifest
2. Mark all old-framework skills as DEPRECATED
3. Run full DISCOVER phase for new framework
4. Generate new skill set from catalog
5. Archive deprecated skills after user confirmation
```

### Convention Evolution

```
1. Detect config file changes (eslint, prettier, tsconfig)
2. Extract new convention rules
3. Update convention-type skills (naming-rules, etc.)
4. Update template sections in workflow-type skills
5. Re-validate convention compliance
```

---

## Evolution Workflow Template

```markdown
## Skill Evolution Report

### Trigger
- **Type**: [dependency_change | framework_migration | convention_update | user_request]
- **Detail**: [specific change detected]
- **Affected skills**: [list of skill names]

### Analysis
| Skill | Current State | Strategy | Impact |
|-------|--------------|----------|--------|
| [name] | STALE/DEPRECATED | In-place/Replace/Split/Merge | [description] |

### Changes Applied
- [Skill name]: [description of changes]

### Quality Re-Evaluation
| Skill | Before | After | Delta |
|-------|--------|-------|-------|
| [name] | [score]/12 | [score]/12 | [+/-N] |

### Sync Status
- All updated skills synced to `.claude/skills/` and `.agents/skills/`: YES/NO
```
