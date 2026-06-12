# Routing Quick Start — Extended

Extends the inline Routing Quick Start in `SKILL.md`. Canonical matrix: `reference/routing-matrix.md`.

## Standard Task-Type Chains (legacy `classify` flow)

| Task Type | Default Chain | Add When |
|-----------|---------------|----------|
| `BUG` | Scout[RCA] → Sherpa? → Radar[failing repro] → Builder[root-cause] → Radar[verify] → Guardian | `+Sentinel` for security, `+Trail` when a past commit introduced it, `+Ripple` for wide blast radius. Sherpa skip when files ≤ 2 or single-component fix. Phase contract ↓ |
| `FEATURE` | Lens?[reuse] → Sherpa[spec+AC] → Forge? → Builder → Radar[+verify gate] → Guardian | Lens reuse-scan on existing codebases (skip greenfield). Forge only when approach unproven (spike, not shipped). `+Muse`/`+Palette` for UI (skip on backend/CLI), `+Artisan` for frontend production. Phase contract ↓ |
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

- **SURVEY (Lens, conditional) — reuse before you build** — for any feature added to an **existing** codebase, scan for reusable implementations BEFORE decomposing: does the function / component / hook / pattern already exist? Extend or compose the existing one instead of reinventing it. Skip only for greenfield. The most common feature-implementation waste is re-deriving code that already ships — this step is the guard (repo rule: don't re-implement what already exists).
- **SPEC (Sherpa)** — decompose into atomic steps AND **lock acceptance criteria + scope boundary before any code** (front-loaded ACs become Radar's test targets and the VERIFY gate). Fold SURVEY's reuse findings into the plan (build-on-existing vs build-new, stated per step). Skip Sherpa only when the change is single-file atomic, but still state the ACs inline.
- **PROTOTYPE (Forge, conditional)** — run **only when the approach is unproven** (new UI pattern, uncertain API shape, integration risk). Forge output is a **throwaway spike to validate feasibility, NOT the shipped artifact**. Skip for well-understood CRUD/backend additions — Builder goes straight to production. Prevents both "rebuild from scratch, lose the spike's learnings" and "ship the prototype as production".
- **BUILD (Builder; +Artisan for frontend production)** — production implementation carrying forward the spike's validated decisions and SURVEY's reuse plan. UI surface routing: **+Muse** when introducing new design tokens/visual primitives, **+Palette** when interaction-heavy, **Artisan** owns frontend production code. Backend/CLI features skip all three.
- **VERIFY (Radar + gate)** — Radar adds edge-case/regression tests; THEN the **VERIFY gate requires existing build + test + lint/typecheck green** against the locked ACs. Not "new tests pass" — the whole check suite. Additionally confirm **each locked AC is actually satisfied** (covered by a test or demonstrated behavior), not merely that the suite is green — convergence on green ≠ the feature does what the spec required. A feature is not done until the gate passes (repo quality rule).
- **SHIP (Guardian)** — PR-prep: commit granularity, PR title/description, ACs linked to evidence.

**Anti-patterns prevented**: (1) prototype-shipped-as-production (PROTOTYPE spike discipline), (2) feature-without-acceptance-criteria (SPEC front-loads ACs), (3) "new tests green but build broken" (VERIFY runs the full suite, not just Radar's additions), (4) feature lands with no PR discipline (SHIP/Guardian — previously absent from the chain), (5) **reinventing code that already ships** (SURVEY reuse scan), (6) **green suite that doesn't meet the spec** (VERIFY's per-AC satisfaction check).

## BUG Phase Contract

Bug-fixing has a best-practice order the default chain must honor — **reproduce before you fix**:

- **RCA (Scout)** — root-cause analysis: why the bug occurs, where to fix, reproduction steps, impact/blast radius. **Confirm it IS a defect** (not expected behavior / misconfig / user error) before proceeding — a misread "bug" exits here with an explanation, no code.
- **DECOMPOSE (Sherpa, conditional)** — only when the fix touches 3+ files or spans components. Skip for single-component atomic fixes.
- **REPRODUCE-FIRST (Radar)** — encode Scout's reproduction steps as a **failing automated test BEFORE any fix**. The failing test is the acceptance criterion: red now, green after the fix. A regression test written *after* the fix can't prove it actually addresses the reported bug — it never failed.
- **FIX (Builder)** — fix the **root cause** Scout identified, not the symptom. Symptom-only patches (swallowing the error, masking the output, broad `try/except`) are rejected — repo rule: fix root causes, don't silence.
- **VERIFY (Radar + gate)** — the repro test now **passes** (bug gone), the existing build + test suite stays green (no new regression), and Scout's blast-radius areas are spot-checked. `+Sentinel` when the bug has a security dimension.
- **SHIP (Guardian)** — PR carrying the repro test + root-cause explanation, so the fix is auditable and the regression is permanently guarded.

**Anti-patterns prevented**: (1) regression test written after the fix that never actually failed (REPRODUCE-FIRST red→green), (2) symptom patch leaving the cause live (FIX root-cause discipline), (3) fix that breaks something else (VERIFY suite + blast-radius), (4) "fix" for a non-bug (RCA defect-confirmation gate), (5) fix lands with no PR/regression guard (SHIP — previously absent from the chain).

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
