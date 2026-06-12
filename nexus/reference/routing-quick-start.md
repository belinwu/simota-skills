# Routing Quick Start — Extended

Extends the inline Routing Quick Start in `SKILL.md`. Canonical matrix: `reference/routing-matrix.md`.

## Standard Task-Type Chains (legacy `classify` flow)

| Task Type | Default Chain | Add When |
|-----------|---------------|----------|
| `BUG` | Scout → Sherpa? → Builder → Radar | `+Sentinel` for security. Sherpa skip when files ≤ 2 or single-component fix |
| `FEATURE` | Sherpa[spec+AC] → Forge? → Builder → Radar[+verify gate] → Guardian | Forge only when approach unproven (spike, not shipped). `+Muse`/`+Palette` for UI (skip on backend/CLI), `+Artisan` for frontend production. Phase contract ↓ |
| `SECURITY` | Sentinel → Builder → Radar | `+Probe` for dynamic testing, `+Specter` for concurrency risk |
| `REFACTOR` | Zen → Radar? | `+Sherpa` for multi-file refactors, `+Atlas` for architecture, `+Grove` for structure. Radar skip for pure rename/extract |
| `OPTIMIZE` | Bolt (code-side) / Tuner (DB queries) → Radar | `+Schema` for DB index/migration |
| `DESIGN_SYSTEM_DOCS` | Muse → Vitrine + Canvas → Quill | `+Vision` for direction, `+Artisan` for live examples |
| `DESIGN_WORKFLOW` | Atelier (orchestrates: Vision → Muse/Frame → Forge → Artisan → Vitrine → Canvas) | Full design→code loop with design-system persistence. When request spans direction + tokens + prototype + implementation + catalog |
| `MOBILE_NATIVE` | **Native** → Radar → Vitrine → Launch | iOS Swift/SwiftUI or Android Kotlin/Compose. Pure-native only (RN/Flutter/KMP/CMP → Forge). Add-ons + full row → `reference/routing-matrix.md` MOBILE_NATIVE |
| `IOS_UI_TEST` | **Snap** → Gear → Launch | XCUITest authoring, accessibilityIdentifier audit, App Store screenshot pipeline (fastlane snapshot). Pure XCUITest scope (Appium/Detox/Maestro → Voyager). Add-ons → `reference/routing-matrix.md` IOS_UI_TEST |
| `PORTING` | Lens/Atlas → **Port → Native** → Voyager → Launch | Web → iOS/Android porting design + implementation. Add-ons (Fossil/Field/Scaffold/Polyglot/Cloak/Crypt) → `reference/routing-matrix.md` PORTING. Cross-platform UI component-name lookup → `port/reference/ui-terminology-matrix.md` |

## FEATURE Phase Contract

`feature` is the highest-traffic Recipe; its chain row is a summary. Phase semantics (read before executing a non-trivial feature):

- **SPEC (Sherpa)** — decompose into atomic steps AND **lock acceptance criteria + scope boundary before any code** (front-loaded ACs become Radar's test targets and the VERIFY gate). Skip Sherpa only when the change is single-file atomic, but still state the ACs inline.
- **PROTOTYPE (Forge, conditional)** — run **only when the approach is unproven** (new UI pattern, uncertain API shape, integration risk). Forge output is a **throwaway spike to validate feasibility, NOT the shipped artifact**. Skip for well-understood CRUD/backend additions — Builder goes straight to production. Prevents both "rebuild from scratch, lose the spike's learnings" and "ship the prototype as production".
- **BUILD (Builder; +Artisan for frontend production)** — production implementation carrying forward the spike's validated decisions. UI surface routing: **+Muse** when introducing new design tokens/visual primitives, **+Palette** when interaction-heavy, **Artisan** owns frontend production code. Backend/CLI features skip all three.
- **VERIFY (Radar + gate)** — Radar adds edge-case/regression tests; THEN the **VERIFY gate requires existing build + test + lint/typecheck green** against the locked ACs. Not "new tests pass" — the whole check suite. A feature is not done until the gate passes (repo quality rule).
- **SHIP (Guardian)** — PR-prep: commit granularity, PR title/description, ACs linked to evidence.

**Anti-patterns prevented**: (1) prototype-shipped-as-production (PROTOTYPE spike discipline), (2) feature-without-acceptance-criteria (SPEC front-loads ACs), (3) "new tests green but build broken" (VERIFY runs the full suite, not just Radar's additions), (4) feature lands with no PR discipline (SHIP/Guardian — previously absent from the chain).

## Sherpa Skip Conditions

Skip Sherpa from the default chain only when ALL apply:
- Task touches ≤ 2 files
- No implicit intermediate steps
- Single atomic operation completable in one focused step

## Chain Adjustment Rules

- `3+` files touched → add Sherpa (if not already in chain).
- Ambiguous or multi-step requirements → add Sherpa.
- `3+` test failures → add Sherpa for re-decomposition.
- Security-sensitive changes → add Sentinel or Probe.
- UI changes → add Muse or Palette.
- Slow database path → add Tuner.
- `2+` independent implementation tracks → consider Rally.
- `<10` changed lines with existing tests → Radar may be skipped.
- Pure documentation work → skip Radar and Sentinel unless the change affects executable behavior.

## Clarification and Decision Rules

- If context is clear, proceed.
- If unclear, inspect git state and `.agents/PROJECT.md`.
- If confidence remains low, ask the user one focused question.
- If the action is risky or irreversible, confirm before execution.
- Always confirm `L4` security, destructive actions, external system changes, and 10+ file edits.

## Anti-Pattern References

Before expanding a chain, consult the anti-pattern references when the plan starts looking expensive, overly dynamic, or hard to verify:
- Orchestration design risk → `reference/orchestration-anti-patterns.md`
- Decomposition or routing quality risk → `reference/task-routing-anti-patterns.md`
- Production reliability risk → `reference/production-reliability-anti-patterns.md`
- Handoff and schema risk → `reference/agent-communication-anti-patterns.md`
