# Acceptance Recipe — Proof-Carrying PR Pipeline

Recipe contract for `nexus acceptance` — orchestrates the 5-layer Proof-Carrying PR pipeline (spec graph → oracle generation → adversarial exploration → Acceptance Gate → runtime oracle hookup) defined in `_common/PROOF_CARRYING.md`. Use when a change needs machine-adjudicated merge without human visual confirmation.

**Prerequisites**: `_common/PROOF_CARRYING.md` (mandatory — defines Tier policy, evidence fields, guardrails). Read first.

**Distinguishes from**:
- `feature` — implements a change with conventional tests. No spec graph, no evidence package, no Acceptance Gate.
- `apex` — full discovery→ship cycle including spec authoring. `acceptance` assumes the spec graph exists (or is being amended) and focuses on the verification + Gate.
- `summit` — strategic decisions and high-stakes releases. `acceptance` is the merge-time pipeline; `summit` is the upstream judgment.
- `judge` — single-shot tri-engine code review. `acceptance` is a structured pipeline producing a Proof-Carrying PR; `judge` can be invoked as a sub-step.

---

## When to Invoke

Trigger `nexus acceptance` when **all** apply:
- The change touches a Tier-S or Tier-A surface (payment / medical / PII / auth / core revenue flow)
- The repository (or product line) has at least a partial spec graph the change can be validated against
- The organization has committed to the Proof-Carrying PR regime (this is a workflow choice, not a one-off tactic)

Do **not** invoke when:
- Tier-B or Tier-C scope — use `feature` / standard PR + AI review
- No spec graph exists and the user is asking for a one-off fix — recommend `apex` to author the spec first, then `acceptance` for subsequent changes
- The user wants exploration, not shipping — use `judge` or `omen`

---

## Phase Contract

### Phase 0 — Tier Classification (Nexus, internal)

Read `_common/PROOF_CARRYING.md` Tier table. Classify the change by inspecting:
- Touched paths (auth/, billing/, payment/, pii/, etc. → Tier-S)
- Declared scope from user prompt
- `.agents/PROJECT.md` if a Tier policy file exists

Output: `tier: S | A | B | C`. If C, abort with a recommendation to use `feature` instead — `acceptance` is over-scope for Tier-C.

### Phase 1 — Spec Diff (sequential)

**Agent**: `attest` (spec compliance) + `accord` (if requirements need to be re-expressed as spec nodes) + `scribe` (only if spec graph needs human-readable annotation)

**Goal**: Produce `spec_diff` — the delta of spec graph nodes touched by this change. If the change is a spec-amendment (not just an implementation), the spec diff is itself subject to multi-view cross-check (see `PROOF_CARRYING.md` Spec Self-Bug section).

**Gate**: Spec diff is parseable, meta-invariants pass (no unreachable FSM nodes, all referenced columns exist, all API contracts have at least one consumer test).

### Phase 2 — Oracle Generation (parallel, fan-out)

**Agents** (run in parallel branches):
- `radar` — property-based + edge-case + regression tests
- `mint` — fixture and data generation (boundary, equivalence-class)
- `drill` — manual-equivalent E2E scenarios converted to executable form
- `voyager` — Playwright / CUA flows for UI surfaces (if `ui_dimension != none`)
- `sentinel` — SAST + security regression oracles
- `attest` — contract tests from API / DB invariants (if not already covered by attest in Phase 1)

**Engine routing for Tier-S** (G1 cross-engine diversity):
- Oracle generation → agy (long-context spec reasoning)
- Implementation engine recorded for later split-check

**Gate**: Generated oracles must be deterministic (seed = spec-graph hash) and pass shadow-run on `main` 3× before becoming Gate-blocking.

### Phase 3 — Adversarial Exploration (parallel, fan-out)

**Agents** (run in parallel, different personas):
- `vigil` — security attacker persona (auth bypass, IDOR, token replay)
- `voyager` + `navigator` — UI-level adversarial users (impatient, mobile, screen-reader, broken-connection, payment-failure, locale-edge)
- `sentinel` — static + dynamic attack surface
- `specter` — concurrency / race / state-machine edge cases
- `siege` — load / chaos (for Tier-S only)

**Engine routing for Tier-S** (G1 cross-engine diversity):
- Adversarial explorers → Claude (judgment + edge-case enumeration)

**Output contract**: Each adversarial agent must produce a non-trivial exploration report. Empty findings without an exploration log = rejected (semantic-emptiness rule, `PROOF_CARRYING.md` Anti-Patterns).

**Gate**: Adversarial findings either fixed in the same PR, or filed with explicit "won't fix" rationale that the Acceptance Gate can adjudicate.

### Phase 4 — Acceptance Gate (sequential)

**Agents**:
- `judge` — tri-engine evidence audit (schema completeness, semantic non-emptiness, cross-engine quorum)
- `attest` — final spec-implementation conformance verdict
- `guardian` — PR preparation with embedded evidence package

**Engine routing for Tier-S** (G1 cross-engine diversity):
- `judge` runs tri-engine (Claude + Codex + agy) — already its default for code-review use
- Gate verdict requires 2-of-3 quorum (CONFIRMED or LIKELY)

**Decision rules**:
1. Every required evidence field (intent / scope / spec_diff / generated_tests / execution_log / ui_trace / screenshot_diff / db_diff / api_contract_diff / adversarial_findings / rollback_condition / regression_proof) must be present and non-empty
2. Spec consistency: spec changes (if any) pass meta-oracle
3. Cross-engine quorum reached (Tier-S requirement)
4. No unspecifiable-quality red flag (brand / ethics / dark-pattern) — if flagged, route to human regardless of evidence completeness
5. Per-PR compute cap not exceeded

**Output**: PASS (merge eligible) / FAIL (specific gaps) / ESCALATE (unspecifiable-quality or compute-cap or Gate-rule conflict)

### Phase 5 — Runtime Oracle Hookup (sequential, on PASS only)

**Agents**:
- `beacon` — registers `rollback_condition` as a live SLO oracle
- `mend` — registers repair runbook with G3 circuit-breaker config (same-signature cap = 3/24h, escalation cap = 7d)

**Gate**: Runtime oracle is live in shadow mode for the canary window before promotion.

### Phase 6 — Random Sampling Audit (asynchronous, post-merge)

For successful Tier-S/A merges:
- Roll a deterministic dice (seed = PR ID + date) at the configured sample rate (5% S / 2% A per `PROOF_CARRYING.md` G2)
- If sampled, file a human-review task with the full evidence package attached
- Review findings feed back into Gate rule updates (no automatic re-routing — explicit human decision required)

This phase does **not** block merge. It audits the Gate, not the change.

---

## Chain Template (AUTORUN)

```
Phase 0: Nexus[classify-tier] → if tier=C: abort with feature recommendation; else continue
Phase 1: attest[spec-diff] (+ accord[spec-amend] if spec changes; + scribe if human-readable spec needed)
Phase 2 (parallel, engine=agy for Tier-S):
  ‖ radar[property+regression]
  ‖ mint[fixtures]
  ‖ drill[E2E scenarios]
  ‖ if ui_dimension != none: voyager[UI flows]
  ‖ sentinel[SAST + security regression]
  ‖ attest[contract tests]
Phase 3 (parallel, engine=claude for Tier-S):
  ‖ vigil[security attacker]
  ‖ if ui_dimension != none: voyager+navigator[adversarial users]
  ‖ sentinel[attack surface]
  ‖ specter[concurrency edges]
  ‖ if tier=S: siege[load+chaos]
Phase 4 (sequential, judge runs tri-engine):
  judge[tri-engine evidence audit] → attest[final conformance] → guardian[PR with evidence package]
Phase 5 (sequential, on PASS only):
  beacon[runtime oracle] → mend[repair runbook with circuit breaker]
Phase 6 (async post-merge):
  sample(rate=5% Tier-S / 2% Tier-A) → human-review task if sampled
```

---

## Failure Escalation

| Failure | Trigger | Escalation |
|---------|---------|------------|
| Spec parse fails | Phase 1 | Block; ask user to fix spec syntax or remove spec changes |
| Meta-oracle fails | Phase 1 | Block; spec change is internally inconsistent (e.g., unreachable state) |
| Oracle generation non-deterministic | Phase 2 | Block; seed not stable or generator has un-seeded randomness — investigate before allowing as Gate-blocking |
| Shadow-run flaky on main | Phase 2 | Defer new oracle to shadow-only for 3 more weeks; do not Gate-block |
| Adversarial empty without exploration log | Phase 3 | Hard re-run with explicit exploration requirement; reject if re-runs also empty |
| Cross-engine quorum fails (Tier-S) | Phase 4 | Block; require 2-of-3 CONFIRMED/LIKELY before merge eligible |
| Compute cap exceeded | Phase 4 | Escalate to human triage; do not auto-extend |
| Unspecifiable-quality flag raised | Phase 4 | Route to human review regardless of Tier evidence completeness |
| Repair-loop signature cap hit (same-signature 3/24h) | Phase 5 runtime | Auto-rollback, 7d escalation, no further auto-repair on that signature |
| Hot-fix needed mid-pipeline | Any phase | Switch to Hot-Fix Fast-Path: downgrade Tier-S→A, Tier-A→B; require normal-Gate follow-up within 24h |

---

## Cost & Scale Profile

| Tier | Typical Agent Count | Wall Time | Cost vs `feature` |
|------|--------------------:|----------:|------------------:|
| S | 14-22 | 35-70 min | 6-12× |
| A | 8-14 | 18-40 min | 3-6× |
| B | (use `feature` recipe) | — | 1× |
| C | (use `feature` or standard PR) | — | 1× |

Confirm with user before launching Tier-S — agent count and cost rival `apex`. Tier-A is comparable to `kaizen` scale.

---

## Anti-Patterns Specific to Acceptance

| Anti-Pattern | Counter-Rule |
|--------------|--------------|
| Running `acceptance` on Tier-C scope | Phase 0 aborts; use `feature` |
| Single-engine evidence for Tier-S | G1 cross-engine diversity is mandatory; Phase 4 quorum check enforces |
| Skipping shadow-run on new oracles | Phase 2 Gate; new oracles are shadow-only until 3 weeks of stability |
| Treating "no findings" as proof | Phase 3 requires exploration log; semantic-emptiness is rejected |
| Bypassing Gate for "urgent" merges | Use Hot-Fix Fast-Path; never invent `[skip-acceptance]` style labels |
| Auto-repair loop without circuit breaker | Phase 5 G3 enforces same-signature 3/24h cap |
| Spec change without meta-oracle re-validation | Phase 1 blocks; spec changes are themselves Proof-Carrying |
| Quality dimensions reduced to spec | Phase 4 unspecifiable-quality carve-out routes to human |

---

## Integration with Existing Recipes

- `apex` Phase 6 (Ship) can chain into `acceptance` for Tier-S deliverables. `apex` produces the spec and implementation; `acceptance` provides the Gate.
- `summit` strategic-decision deliverables that result in code changes flow through `acceptance` for Tier-S/A scope.
- `feature` is the recommended downgrade when `acceptance` Phase 0 classifies as Tier-B/C.
- `kaizen` improvements to Tier-S/A surfaces should chain `kaizen → acceptance` (kaizen produces the improvement; acceptance gates the merge).

---

## References

- `_common/PROOF_CARRYING.md` — the protocol; required reading
- `nexus/references/apex-recipe.md` — discovery→ship cycle; `acceptance` is the merge-gate portion
- `nexus/references/summit-recipe.md` — engine-strength routing pattern that `acceptance` Tier-S inherits
- `judge/SKILL.md` — tri-engine evidence audit
- `attest/SKILL.md` — spec compliance verification
- `beacon/SKILL.md` — runtime oracle registration
- `mend/SKILL.md` — repair runbook with circuit-breaker semantics
