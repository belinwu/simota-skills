# Proof-Carrying PR Protocol

Cross-skill protocol for shipping changes with **machine-verifiable evidence packages** that an Acceptance Gate can adjudicate without human visual confirmation. Inspired by the AAOS (Autonomous Acceptance OS) framing: encode product correctness as executable specifications, then refuse to merge any PR whose evidence package does not match the spec graph.

**Audience**: Skills participating in change-shipping pipelines (`attest`, `judge`, `guardian`, `radar`, `voyager`, `sentinel`, `vigil`, `mend`, `beacon`, `nexus[acceptance]`, `nexus[apex]`, `nexus[summit]`).

**Prerequisites**: `_common/HANDOFF.md` (handoff schema), `_common/MULTI_ENGINE_RECIPE.md` (cross-engine fan-out).

---

## Core Premise

The bottleneck in AI-assisted shipping is no longer code generation — it is the last-mile human judgment ("does this work as intended? does it break existing flows? is it brand-appropriate?"). Eliminating that bottleneck requires:

1. A **specification graph** (state machines, API contracts, DB invariants, a11y constraints, KPI floors, regression memory) that is machine-readable and acts as a **judge**, not as documentation.
2. An **oracle generator** that derives test oracles (contract, E2E, property-based, fuzz, VRT, a11y, DB integrity, security regression) from the spec graph.
3. **Adversarial AI explorers** — not approvers — that try to break the change.
4. A **Proof-Carrying PR**: every PR must carry an evidence package, and an **Acceptance Gate** (not a human) decides merge.
5. **Runtime oracles + auto-rollback** as the last safety net, with circuit breakers to prevent repair-loop oscillation.

The constraint that distinguishes this from "AI writes tests": AI agents are positioned as **adversarial explorers**, not approvers. Their value is "couldn't break it", not "looks fine".

---

## Tier-Based Application Policy

Not every PR needs full proof. Apply by criticality tier:

| Tier | Scope | Required Evidence | Gate Behavior |
|------|-------|-------------------|---------------|
| **S** | Payment / Medical / Aviation / PII / Auth-critical | All 5 layers mandatory (spec graph + oracles + adversarial + Proof-Carrying PR + runtime oracle) | Block merge until full evidence + 2-of-3 cross-engine quorum |
| **A** | Core revenue features / Customer-facing flows | Spec graph + generated oracles + Proof-Carrying PR (layers 1+2+4) | Block on spec mismatch; advisory on adversarial gaps |
| **B** | Internal tools / Secondary features | Spec graph + automated tests + standard PR | Block on test failure; spec graph optional |
| **C** | UI tweaks / Copy changes / Docs | Conventional PR + AI review | Standard CI; no spec graph required |

Every PR must declare its Tier at the top. Tier-S+A PRs without an evidence package are auto-rejected.

**Why Tier-based**: AAOS at full scope is over-engineering for ~99% of PRs (omen FM-L4-1: evidence-completeness illusion; magi DA challenge: YAGNI for non-critical paths). Tier-based application is the DA-compelled boundary that keeps the cost-benefit positive.

---

## Evidence Package — Required Fields

Every Tier-S/A PR must attach:

| Field | What | Owner Skill |
|-------|------|-------------|
| `intent` | Change purpose in 1-3 sentences | author / `scribe` |
| `scope` | Affected files, modules, user journeys | `ripple` |
| `spec_diff` | Diff of spec graph nodes touched | `attest` / `accord` |
| `generated_tests` | Auto-generated contract / property / fuzz / E2E / a11y / VRT | `radar` / `voyager` / `mint` / `drill` |
| `execution_log` | Full test run output (pass / fail / coverage) | CI |
| `ui_trace` | Playwright / CUA trace for UI changes | `voyager` / `navigator` |
| `screenshot_diff` | Before/after with diff% | `voyager` (visual comparison) |
| `db_diff` | Schema + sample-row delta | `schema` / `tuner` |
| `api_contract_diff` | OpenAPI / Pact contract delta | `attest` |
| `adversarial_findings` | What attackers / edge-case agents tried + couldn't break | `vigil` / `sentinel` / `voyager` |
| `rollback_condition` | Runtime metrics that auto-roll-back the change | `beacon` / `mend` |
| `regression_proof` | Evidence existing spec invariants are preserved | `attest` / `radar` |

Missing fields = automatic Gate rejection. The author cannot self-attest completeness — at least one independent agent (or engine, see Cross-Engine Diversity below) must verify each field.

---

## Acceptance Gate — Decision Rules

The Gate (typically `judge` + `attest`) is the merge authority for Tier-S/A. Rules:

1. **Schema completeness** — every required field above must be present and non-empty. Empty `adversarial_findings` ≠ "no findings"; require a non-trivial exploration report.
2. **Spec consistency** — if `spec_diff` is non-empty, the spec change itself must be re-validated against meta-invariants (see Spec Self-Bug below).
3. **Cross-engine quorum** — for Tier-S, evidence must be produced or verified across at least 2 different engines (Claude + Codex, or Codex + agy). Single-engine evidence is CANDIDATE, not CONFIRMED.
4. **No semantic short-circuit** — schema-valid but semantically empty outputs (e.g. "no issues found" with zero exploration) trigger a hard re-run, not a pass.
5. **Random sampling escape valve** — see Success-PR Random Review below.

If the Gate rejects, the change cannot bypass via `--no-verify` style escapes. The only legitimate bypass is the Hot-Fix Fast-Path (see below).

---

## Three Mandatory Guardrails (omen-derived)

These are not optional polish — without them the Proof-Carrying PR pipeline degrades into a more expensive version of conventional CI.

### G1. Cross-Engine Diversity for Adversarial Roles

**Problem**: If `implementer-AI`, `oracle-generator-AI`, and `adversarial-explorer-AI` all run on the same model family, they share blind spots. The adversary cannot find a bug the implementer didn't think of, because both reason from the same priors. omen FM-L3-4 calls this **correlated LLM failure** — the most insidious failure mode because no individual run looks wrong.

**Rule**: For Tier-S, the implementer engine and the adversarial-verifier engine must be different families. Recommended split:
- Implementer → Codex (code-gen strength)
- Oracle generator → agy (long-context spec reasoning)
- Adversarial explorer → Claude (judgment + edge-case enumeration)

For Tier-A, two-engine split is sufficient. Tier-B can run single-engine.

Reference: `_common/MULTI_ENGINE_RECIPE.md` (engine dispatch), `nexus/references/summit-recipe.md` (engine-strength routing).

### G2. Success-PR Random Review

**Problem**: When humans only see failed PRs (as the AAOS end-state implies — "the only PRs humans review are the ones that failed"), reviewer skill atrophies (omen FM-L4-6, RPN=900) and Gate false-negatives become invisible (omen FM-L4-1). Confidence in the Gate becomes self-referential.

**Rule**: A randomly sampled fraction of *successful* Tier-S/A PRs must be routed to human review post-merge. Suggested rate: 5% for Tier-S, 2% for Tier-A. Findings feed back to:
- Gate rule updates (false-negative correction)
- Adversarial explorer prompt tuning (new attack vectors)
- Reviewer skill maintenance

Random sampling is recorded as Gate evidence, not as a delay — sampled PRs ship normally; the review is asynchronous and audits the Gate, not the change.

### G3. Repair-Loop Circuit Breaker

**Problem**: Runtime oracles trigger auto-rollback → trace capture → minimal-repro generation → AI-authored fix PR → Acceptance Gate re-runs. This is theoretically a closed loop. In practice, the same root cause can manifest as multiple distinct-looking symptoms, and the AI repair-PR system can generate cosmetically-different fixes for the same underlying bug indefinitely. omen FM-L5: **infinite remediation loop**.

**Rule**: Repair attempts are rate-limited per failure signature:
- Same signature (normalized stack + endpoint + error class): **max 3 repair attempts per 24h**
- After cap, the Gate escalates to a human and refuses further auto-repair on that signature for 7d
- Different signature on the same module: separate counter

Repair-loop telemetry (signature counts, escalation rate) is a first-class SLO. A rising escalation rate is itself a signal of spec-graph rot or correlated-failure leakage.

Reference: `mend/SKILL.md` (repair runbook safety tiers), `beacon/SKILL.md` (runtime oracle metrics).

---

## Spec Self-Bug Problem

The spec graph is now the oracle. **What validates the oracle?** This is the classic specification-of-specification problem (omen FM-L1-1, magi Sophia S2). AAOS-style systems collapse silently when the spec is wrong, because every layer below trusts it.

**Mitigation**: Spec changes themselves are subject to:

1. **Multi-view cross-check** — same intent expressed as (a) user story, (b) state machine, (c) API contract / DB invariant. The three must be consistent; divergence flags the spec change for human review.
2. **Meta-invariant tests** — small set of invariants that must hold across all spec versions (e.g. "no state in the FSM is unreachable", "every API contract has at least one consumer test", "no DB invariant references a column that doesn't exist").
3. **Spec-graph diff is itself Proof-Carrying** — spec changes get their own evidence package, generated by a different agent than the one proposing the spec change.

The spec is never trusted just because it parses. It is trusted because it passes its own meta-oracle.

---

## Unspecifiable-Quality Carve-Out

Some properties resist machine specification:
- Brand voice, tone, cultural appropriateness
- "Feel" of UI motion / interaction quality
- Dark-pattern detection
- Ethical edge cases (discrimination, fairness, manipulation)

**Rule**: These are explicitly declared **out of scope** for the Acceptance Gate. Changes touching these dimensions require human review regardless of Tier. The Gate must not silently approve them on the basis that "no oracle flagged it" — absence of evidence is not evidence of absence.

This is the Procrustes-effect mitigation (magi Sophia S7). Without it, AAOS-style systems reduce product quality to "what the spec graph can represent", and unspecifiable dimensions decay invisibly.

---

## Hot-Fix Fast-Path

**Problem**: Heavyweight evidence requirements on every PR — including 3am production fixes — create organizational pressure to invent unofficial bypasses (`[skip-acceptance]` labels, emergency branches). Once a bypass exists, it normalizes and the whole regime degrades (magi Pathos P1).

**Rule**: Provide an official Fast-Path so no one invents an unofficial one:

1. **Trigger**: P0/P1 incident declared by `triage` (or equivalent on-call agent)
2. **Reduced Gate**: Tier-S downgrades to Tier-A evidence requirements; Tier-A downgrades to Tier-B
3. **Time-boxed**: Fast-Path PR must be replaced by a normal-Gate follow-up within **24h** or it auto-creates a tracking issue and pages the team
4. **Logged**: Every Fast-Path use is auditable; >3/month per service triggers a process review

The Fast-Path is not an escape hatch — it is the official channel that prevents escape-hatch invention.

---

## Spec Graph Versioning

Spec graph must be version-controlled alongside code:

- Same repository, same PR
- State-machine nodes are atomic merge units; concurrent edits to the same node trigger conflict resolution (not auto-merge)
- Spec-graph hash is fed as a seed into property-based / fuzz oracle generation, so identical spec produces identical tests (determinism = reproducible Gate verdicts)
- Past spec versions are retained for historical-bug replay

Without this, the spec graph either drifts from code (defeating the purpose) or becomes a parallel-development bottleneck.

---

## Cost & Scalability Guardrails

Full evidence generation per PR is expensive. Without explicit bounds the regime is fiscally unsustainable.

- **Per-PR compute cap**: declare a $ ceiling (e.g. $5/PR for Tier-A, $20/PR for Tier-S). Exceeding the cap escalates to human triage rather than silently consuming budget.
- **Impact-based test selection**: ML-driven selection of which generated oracles to actually run per PR, based on diff analysis. Full re-run only on schedule (nightly / pre-release).
- **Shadow run before block**: new oracle types run in shadow (logged but non-blocking) for ≥3 weeks before becoming Gate-blocking, to surface flakiness.

---

## What Belongs HERE vs in Skill-Specific Files

This protocol defines the **shared concepts and vocabulary**. Skill-specific implementation lives in:

- `attest/SKILL.md` — spec compliance verification (Layer 1 + Layer 4 Gate)
- `radar/` `voyager/` `drill/` `mint/` — oracle generation (Layer 2)
- `vigil/` `sentinel/` `voyager/` — adversarial exploration (Layer 3)
- `judge/` — Acceptance Gate adjudication (Layer 4)
- `guardian/` — PR preparation with evidence package (Layer 4 delivery)
- `beacon/` `mend/` — runtime oracle + repair loop (Layer 5)
- `nexus/references/acceptance-recipe.md` — orchestrated chain

When implementing one of the above, reference this protocol rather than restating it. When the protocol itself changes, downstream skills inherit automatically.

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Counter-Rule |
|--------------|--------------|--------------|
| Full AAOS on every PR | YAGNI for ~99% of changes; cost-prohibitive | Tier-based application (S/A/B/C) |
| Single-engine evidence | Correlated failure invisible | G1 Cross-Engine Diversity for Tier-S |
| "No findings" passes the Gate | Schema-valid semantic emptiness | Require non-trivial adversarial exploration report |
| Humans only see failed PRs | Reviewer atrophy + invisible false-negatives | G2 Success-PR Random Review |
| Auto-repair without stop condition | Infinite remediation loop | G3 Repair-Loop Circuit Breaker |
| Spec trusted because it parses | Spec self-bug invisible | Multi-view cross-check + meta-invariants |
| All quality reduced to spec | Brand / ethics / feel decay silently | Unspecifiable-Quality Carve-Out |
| Heavyweight Gate on hot-fixes | Invents unofficial bypasses | Hot-Fix Fast-Path with time-boxed follow-up |
| Spec graph in a separate repo | Drift or parallel-dev bottleneck | Same-repo, same-PR, node-atomic merges |
| Unbounded compute per PR | Fiscally unsustainable | Per-PR cap + impact-based selection + shadow-then-block |

---

## References

- AAOS (Autonomous Acceptance OS) original proposal — 5-layer architecture: spec graph → oracle generator → adversarial explorers → Proof-Carrying PR + Acceptance Gate → runtime oracle + auto-rollback
- AWS formal-methods practice for S3 — formal spec + model checking for correctness at scale
- Pact — consumer-driven contract testing pattern
- Property-based testing (Hypothesis / fast-check / PropEr) — properties over examples
- OpenAI Computer-Using Agent + Anthropic Computer Use — adversarial UI exploration substrate
- Argo Rollouts / Flagger — SLO-based progressive delivery with auto-rollback (runtime oracle precedent)
- Magi verdict on AAOS proposal — 3-0 GO-WITH-CONDITIONS, 12 conditions, 5 premise-collapse scenarios
- Omen pre-mortem on AAOS proposal — 32 failure modes, 6 S≥9 Must-Act risks (correlated LLM failure, evidence-completeness illusion, reviewer atrophy, repair storm, spec self-bug, Goodhart inevitability)
