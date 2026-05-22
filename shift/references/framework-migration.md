# Framework Migration Reference

Purpose: Execute a major framework version jump or cross-framework port with preserved behavior, measurable progress, and reversible phases. The recipe applies to front-end frameworks (Vue 2 → 3, React CRA → Next.js, Angular major), back-end frameworks (Express → Fastify / Hono, Spring Boot major), and full-stack stacks (Rails major, NestJS major).

## Scope Boundary

- **Shift `framework`**: executes a specific framework migration with a feature-parity checklist, incremental adapter pattern, and dual-run validation.
- **Shift `migrate` (default)**: general migration planning — picks Strangler Fig vs Branch by Abstraction at an architectural level, no framework-specific gotchas.
- **Horizon**: detects deprecated libraries/frameworks and suggests replacements — it produces the *input* for `framework`; it does not execute the migration.
- **Zen**: refactor within a framework — does not cross versions.
- **Launch**: plans the release where the migrated code ships; `framework` owns the code transition.

If the request is "what should we move off?" → Horizon. If it is "we have chosen Vue 3, now move us" → `framework`.

## Framework-Specific Gotchas

| From → To | Mechanical (codemod-able) | Semantic (must verify manually) |
|-----------|---------------------------|----------------------------------|
| Vue 2 → Vue 3 | `vue-codemod` (Options API skeleton, `v-model` arg rename, filters removal) | Reactivity from `this.$set` → proxy, event API (`$on`/`$off` removed), Vuex → Pinia store shape |
| React `18 → 19` | `react-codemod` (`Context.Provider` → `Context`, remove `forwardRef`, `React.useContext` → `use`) | Actions / `useActionState` adoption, `<Form>` semantics, Server Components migration, `ref` as prop |
| React CRA → Next.js (App Router) | File moves, import path rewrites (Next.js ships official codemods via `npx @next/codemod`) | Client/Server component boundary, `useRouter` API diff, env var prefix (`REACT_APP_` → `NEXT_PUBLIC_`), SSR hydration mismatches |
| Next.js `15 → 16` | Official `@next/codemod` set (App Router cache APIs, image / metadata rewrites) | Cache Components (Next.js 16) replacing implicit caching, async `params` / `searchParams`, partial pre-rendering boundaries |
| Angular N → N+2 | `ng update` schematics, Ivy opt-in | Standalone components, zoneless change detection, RxJS major bumps, strict template types |
| Rails N → N+1 | `rails app:update`, initializer regeneration | Zeitwerk autoloading, deprecation warnings, strong params edges, Active Record default changes |
| Spring Boot 2 → 3 | Jakarta namespace rename (`javax.*` → `jakarta.*`) | Native image constraints, observability API (Micrometer → OTel), security filter chain changes |
| Express → Fastify / Hono | Route registration shape | Middleware execution order, error-handling contract, async hook semantics, streaming response API |

Record anything you hit that is *not* on this list in `.agents/shift.md` for future reuse.

### Codemod-First Posture (2026 default)

For every row above, check the framework's *official* codemod set before hand-writing a transform:

- **React**: [`reactjs/react-codemod`](https://github.com/reactjs/react-codemod) (also distributed via Codemod.com migrations) — covers `Context.Provider`, `forwardRef`, `useContext → use`, and the legacy class-component path.
- **Vue**: [`vuejs/vue-codemod`](https://github.com/vuejs/vue-codemod) — Vue 2 → 3 API rewrites, jscodeshift-based.
- **Next.js**: `npx @next/codemod <transform> .` — version-pinned transforms shipped with the framework.
- **Codemod.com Studio + Hypermod**: visual / managed codemod runners that sit on top of `ast-grep` (jssg) and jscodeshift; use when the official codemods do not cover the delta.

A codemod cannot replace the semantic verification column above. Treat the codemod output as a starting diff and run the dual-run validation regardless.

## Workflow (overlays ASSESS → ... → COMPLETE)

```
ASSESS   →  pin current + target minor/patch versions exactly
         →  inventory: entry points, framework-coupled modules, plugin/middleware list
         →  capture Horizon findings if present (what forced this migration?)
         →  measure test coverage per surface; flag surfaces with <40% as high-risk

PLAN     →  feature-parity checklist (one row per framework feature in use)
         →  adapter strategy: shim, compat build, or dual-entry
         →  dual-run plan: run old + new against the same request set, diff responses
         →  deprecation-warning triage policy (fix now / defer with ticket / accept)
         →  rollback point per phase

PREPARE  →  pin lockfile; snapshot current behavior (golden fixtures, HAR, SQL trace)
         →  scaffold adapter / compat layer
         →  generate codemods for mechanical rewrites (ast-grep/jscodeshift)
         →  wire feature flags for per-route / per-module cutover

EXECUTE  →  migrate one bounded context at a time
         →  keep old adapter live behind flag
         →  turn on dual-run in staging; diff until delta is understood (expected vs regression)
         →  triage deprecation warnings after each phase — do not let them stack

VERIFY   →  feature-parity checklist: every row green
         →  dual-run delta: zero unexplained diffs
         →  perf benchmark within agreed envelope (default ≤±10% latency)
         →  dependent services (observability, auth, cache) still healthy

COMPLETE →  remove adapter/shim, remove feature flags, drop old framework deps
         →  delete dual-run harness
         →  document residual deprecation-warning budget for next cycle
```

## Feature-Parity Checklist Template

One row per feature surface. Do not shortcut the matrix.

| Feature | Old behavior (evidence) | New binding | Parity status | Owner |
|---------|-------------------------|-------------|---------------|-------|
| Login flow | `__tests__/login.spec.ts` passing on v2 | Hooked via new router | parity / diff / blocked | |
| File upload | Manual QA video | New multipart handler | | |

"Diff" status requires a diff explanation (expected change vs regression).

## Dual-Run Validation Pattern

1. Route a shadow copy of real traffic (or a captured request set) to the new stack.
2. Compare responses field-by-field — normalize timestamps and IDs before diff.
3. Classify each diff: **expected** (e.g., new error shape is intentional), **regression** (must fix), or **benign** (log format, header ordering).
4. Promote only when regression count is zero and expected diffs are documented.

Tools: `diffy` for JSON, framework-specific shadow-proxy (e.g., GoReplay, Envoy mirror filter), or a test harness replaying fixture requests.

## Deprecation-Warning Triage

- Capture warnings per phase (stderr, framework logger, browser console).
- Classify: `fix-now` (removed next minor), `defer` (file ticket, set expiry date), `accept` (third-party, pinned).
- A deferred warning without an expiry date is not deferred — it is ignored. Block `COMPLETE` if any warning lacks classification.

## Anti-Patterns

- Migrating in a single branch for 6+ weeks without landing to main. Ship adapter-first so partial progress is always merge-able.
- Treating codemod output as complete — mechanical rewrites cover shape, not semantics.
- Upgrading the framework and a major dependency (ORM, state lib) in the same phase. Split.
- Skipping dual-run because "tests pass" — tests cover known cases; dual-run catches unknown-unknowns.
- Leaving the compat shim in place after `COMPLETE` "just in case" — it becomes a second framework to maintain.

## Handoff

- → `Builder`: implementation tasks per phase, with codemod + adapter touchpoints called out.
- → `Radar`: dual-run harness as a regression test; feature-parity rows as acceptance tests.
- → `Gear`: CI pipeline needs the new framework's build tooling and may need parallel test lanes during dual-run.
- → `Launch`: cutover release plan, flag flip schedule, rollback runbook.
- ← `Horizon`: consumes "framework is deprecated" findings as the trigger for this recipe.
