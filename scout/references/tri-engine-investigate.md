# Tri-Engine Parallel Investigation

Default flow for `/scout multi` (`consensus` Recipe in multi-engine mode). Run Codex, Antigravity, and Claude Code as three independent RCA subagents in parallel, integrate hypotheses across both axes (confidence + perspective), and deliver a **Pattern H — Hybrid** investigation report that ships a primary root cause backed by consensus while preserving well-reasoned alternative hypotheses as verification-recommended branches.

**Why three engines for RCA (Pattern H, not Pattern C):** A single-engine RCA is structurally prone to hypothesis lock-in — once an engine commits to a causal chain, downstream evidence is filtered through that frame ("the system as seen through the lens of the first hypothesis"). Independent fan-out across three engines with non-overlapping training-data priors (Codex/GitHub-heavy, Antigravity/Google-product-heavy, Claude/Anthropic-curated) breaks the lock and surfaces alternative root cause hypotheses that the primary engine never considered. **Concurrence raises confidence on the primary RCA; divergence is not noise — it preserves the alternative hypothesis space for parallel verification.** Scout's downstream (Builder) does not write code from a single committed RCA — it receives a primary-plus-alternative bundle with explicit verification ordering.

**Pattern H** = Pattern C confidence axis (CONFIRMED / LIKELY / CANDIDATE) × perspective axis (CONVERGENT / DIVERGENT). Both axes ship in the final report.

**Adapted from `_common/MULTI_ENGINE_RECIPE.md`. This file specifies only the Scout-specific deltas — JSON schema, CLUSTER identity rules, scoring rubric, GROUND protocol, SYNTHESIZE merge, and subagent prompt skeleton.**

---

## Flow

```
SCOPE → PREFLIGHT → FAN-OUT → NORMALIZE → CLUSTER → SCORE (confidence + perspective) → GROUND → SYNTHESIZE → REPORT
```

The skeleton is identical to `_common/MULTI_ENGINE_RECIPE.md §Canonical Flow`. Scout's deltas:

- **SCOPE** carries the bug report, symptom evidence, and any prior single-engine RCA that stalled.
- **CLUSTER** groups by *root cause hypothesis identity*, not by symptom — engines may phrase the same root cause differently.
- **SCORE** runs both axes; divergent hypotheses are preserved.
- **GROUND** requires actual code reading and reproduction attempt — never delegate to subagents.
- **SYNTHESIZE** produces primary RCA + alternative hypotheses with explicit verification ordering for Builder handoff.

---

## 1. SCOPE

Define the investigation target once. All three subagents share:

- Symptom and observed behavior (verbatim error message, stack trace, log lines)
- Reproduction status (reproduced / partially reproduced / not reproduced) and minimal repro if available
- Environment context (runtime, version, deployment)
- Prior investigation state if multi mode was triggered by `consensus` auto-promotion (3 hypotheses exhausted) — include the **ruled-out hypotheses with their elimination evidence** so subagents do not re-traverse dead ends
- Affected files / area (optional — subagents read the code themselves; do not pre-commit them to a specific location)

Do **not** pass RCA frameworks (5 Whys, Fishbone, Fault Tree templates) into subagents — each engine applies its own RCA priors. Frameworks apply at SYNTHESIZE.

## 2. PREFLIGHT

Inherit `_common/MULTI_ENGINE_RECIPE.md §2` verbatim. Engine availability detection runs in Scout main context only.

## 3. FAN-OUT — parallel RCA subagents

Spawn three Agent calls in a single message. Each subagent runs one engine and produces RCA hypotheses independently.

| Subagent | Engine | Baseline command |
|----------|--------|------------------|
| `investigate-codex` | Codex CLI | `codex exec --full-auto "<prompt>"` |
| `investigate-agy` | Antigravity CLI | `agy -p "<prompt>" --dangerously-skip-permissions` |
| `investigate-claude` | Claude Code CLI (subagent) | Agent tool with `subagent_type: general-purpose` |

**Loose prompt rule**: pass Role + Symptom evidence + Reproduction state + Ruled-out hypotheses + Output format only. Do NOT pass: 5-Whys templates, Fishbone categories, Causal Graph rules, RCA verb lists, or Scout's confidence rubric. Let each engine apply its own RCA priors.

**Required JSON output schema** (Scout-specific):

```json
{
  "engine": "codex|agy|claude",
  "hypotheses": [
    {
      "symptom": "Verbatim observed failure (error string, behavior, metric anomaly)",
      "root_cause_hypothesis": "One-sentence systemic root cause — NOT the surface symptom, NOT 'human error'",
      "causal_chain": [
        "Step 1: trigger condition",
        "Step 2: intermediate state transition",
        "Step 3: failure manifestation"
      ],
      "evidence": [
        {"type": "code|log|trace|metric|history|reproduction", "location": "file:line or log source", "quote": "verbatim evidence"}
      ],
      "reproduction_steps": ["Minimal repro step 1", "Minimal repro step 2"],
      "affected_areas": ["file/module/service path 1", "file/module/service path 2"],
      "severity": "Critical|High|Medium|Low",
      "confidence": 0.0,
      "rca_method": "5-whys|fishbone|fault-tree|causal-graph|pattern-match",
      "ruled_out": ["Hypothesis text 1 — why eliminated", "Hypothesis text 2 — why eliminated"]
    }
  ],
  "engine_notes": "Optional: what bias/strength this engine knows it brings"
}
```

Each engine returns 1-3 hypotheses. Single-hypothesis returns are acceptable when the engine has high conviction; multi-hypothesis returns are preferred for ambiguous symptoms.

If an engine is genuinely unavailable per PREFLIGHT, record the failure and proceed. Below two engines, all hypotheses become `CANDIDATE` and require stricter grounding (see §7).

## 4. NORMALIZE

Parse the three JSON blobs into a unified hypothesis list. Tag each hypothesis with its source engine. Preserve per-engine wording — divergent phrasing of the same root cause may reveal different angles on the same underlying mechanism, while genuinely different root cause hypotheses must remain distinct.

## 5. CLUSTER — group by root cause hypothesis identity (NOT by symptom)

**Scout's CLUSTER rule is the most consequential delta from generic Pattern H skills.** Engines investigating the same bug always agree on the symptom — they may diverge dramatically on the root cause. Symptom-based clustering would collapse meaningful divergence.

Two hypotheses belong to the **same cluster** when **all three** hold:

- **Same systemic root cause class** — e.g., "race condition in cache write" and "concurrent write to cache without lock" are the same cluster; "cache invalidation timing" and "cache key collision" are different clusters even though both involve the cache.
- **Same primary affected component** — file, module, service boundary, or external dependency named as the locus of the cause.
- **Same causal-chain shape** — the trigger → state-transition → failure sequence has the same key nodes, even if phrased differently. If one hypothesis says "race condition causes stale read" and another says "missing memory barrier causes stale read", they share the chain shape and cluster.

Two hypotheses belong to **different clusters** when **any** of these hold:

- Different layers of causation (application-code bug vs library bug vs infrastructure bug vs config drift)
- Different mechanisms (logic error vs race condition vs resource exhaustion vs upstream dependency)
- Different ultimate fix locations (different files / different owners)

**Record per cluster**: which engines produced it, the union of evidence across engines, the union of causal-chain steps, the highest confidence assigned across engines.

**Do not** force same-symptom hypotheses into the same cluster — divergent root causes for the same symptom are exactly the value Pattern H preserves.

## 6. SCORE — confidence axis × perspective axis

Apply both axes to every cluster.

### Confidence axis (per Pattern C rubric, adapted)

| Engines in cluster | Confidence label | Initial treatment |
|--------------------|------------------|-------------------|
| 3 / 3 | `CONFIRMED` | High confidence in root cause; spot-check at GROUND |
| 2 / 3 | `LIKELY` | Strong; note what the missing engine surfaced instead — that often becomes an alternative hypothesis cluster |
| 1 / 3 | `CANDIDATE` | Must pass GROUND to ship as either primary or alternative |

### Perspective axis (cross-cluster pattern)

After confidence scoring, examine the cluster set as a whole:

- `CONVERGENT` — all surviving clusters reduce to the same root cause class (CLUSTER rule collapsed all engines onto one). Ship as a single high-confidence RCA.
- `DIVERGENT-N` — N surviving clusters reflect genuinely different root cause hypotheses (N ≥ 2). The primary cluster (highest confidence + strongest evidence) ships as Primary RCA; remaining N-1 clusters ship as Alternative Hypotheses with verification ordering.

**Critical rule for Scout (Pattern H)**: A `DIVERGENT` result is **not a failure of the multi-engine flow** — it is the precise signal multi-engine investigation is designed to produce. Single-engine RCA cannot tell you when alternative root cause hypotheses are plausible; multi-engine can. Ship the divergence as explicit Alternative Hypotheses rather than collapsing.

## 7. GROUND — verify primary + alternatives (Scout main context, never delegated)

Grounding for RCA is **stricter than for Spark or Plea** because Scout's output drives downstream code changes. Two grounding actions are mandatory for every cluster that may ship (primary OR alternative):

### 7a. Code reading (mandatory for every shipping cluster)

For each cluster, read the cited `affected_areas` files and the `causal_chain` step locations using the Read tool. Answer explicitly:

1. **Does the code path described actually exist?** Engines can hallucinate function names, imports, or call chains. If the cited symbol is absent, mark `REJECTED-HALLUCINATION`.
2. **Does the causal chain match the actual control/data flow?** Trace from the trigger to the failure step. If any intermediate step does not exist in code, mark `REJECTED-CHAIN-BROKEN`.
3. **Is there an upstream mitigation already in place?** (Input validation, type guard, framework guarantee, lock, retry layer.) If the cluster's failure mode is already prevented in code, mark `REJECTED-MITIGATED`.
4. **Are the cited evidence quotes accurate?** Verify verbatim log/error strings against actual sources. Hallucinated evidence is `REJECTED-HALLUCINATION`.

### 7b. Reproduction attempt (mandatory when reproducible)

For each cluster, attempt reproduction using the cluster's `reproduction_steps` when:

- The original bug is reproducible
- The cluster's reproduction steps are tractable (no production data dependency)

A cluster that survives code-read GROUND but fails reproduction is `LIKELY-VERIFIED` (kept, but confidence downgraded one tier — CONFIRMED → LIKELY, LIKELY → CANDIDATE). A cluster that survives both is `VERIFIED`.

### 7c. Grounding verdicts

| Verdict | Meaning | Ship as |
|---------|---------|---------|
| `VERIFIED` | Code path exists + chain matches + repro reproduces | Primary or Alternative (per perspective axis) |
| `LIKELY-VERIFIED` | Code path exists + chain matches + repro inconclusive | Alternative only (never Primary unless no VERIFIED cluster exists) |
| `REJECTED-HALLUCINATION` | Cited code/evidence does not exist | Drop |
| `REJECTED-CHAIN-BROKEN` | Causal chain has a missing step | Drop |
| `REJECTED-MITIGATED` | Already prevented upstream | Drop |
| `NEEDS-INFO` | Cannot verify without information Scout does not have (prod data, infra access) | Escalate to user; do not ship |

Never ship a Primary RCA without at least one `VERIFIED` cluster. If all surviving clusters are `LIKELY-VERIFIED` after grounding, ship the highest-confidence as Primary with explicit confidence downgrade and call out the verification gap.

## 8. SYNTHESIZE — Primary RCA + Alternative Hypotheses with verification ordering

Scout's SYNTHESIZE is **the most distinctive step in the multi-engine flow** because Scout does not write fixes. The output must be a verification-ordered bundle that Builder can act on without re-doing the RCA.

### 8a. Select Primary RCA

Rank surviving clusters by:

1. Confidence label (`CONFIRMED > LIKELY > CANDIDATE`)
2. Within tier: grounding verdict (`VERIFIED > LIKELY-VERIFIED`)
3. Within verdict: evidence count and specificity (file:line + repro + log > inferred chain only)
4. Within evidence: causal chain specificity (named state transition > vague "something happens")

The top-ranked surviving cluster is the **Primary RCA**.

### 8b. Select Alternative Hypotheses (preserved divergence)

If perspective axis is `DIVERGENT-N`, the remaining N-1 surviving clusters ship as Alternative Hypotheses. Rank them by the same criteria as 8a.

If perspective axis is `CONVERGENT`, there are no Alternative Hypotheses — note this explicitly in the report ("Three engines reached the same root cause class").

### 8c. Author the verification-ordered handoff

The synthesized output is a Scout Investigation Report containing:

- **Primary RCA section** — full investigation report shape (see `references/output-format.md`), tagged with `[engine-attribution]` and `[CONVERGENT]` or `[DIVERGENT-N → primary]`
- **Alternative Hypotheses section** — one block per surviving alternative, each with: root cause hypothesis, causal chain, evidence, suggested verification step, engine-attribution tag, perspective tag `[DIVERGENT-N → alt-i]`
- **Verification Ordering block** — explicit instruction for Builder:

  ```
  Verification Order:
  1. Apply Primary RCA fix (see ## LLM Fix Prompt).
  2. If symptom persists after Primary fix, verify Alternative Hypothesis #1 by [specific verification step].
  3. If symptom still persists, verify Alternative Hypothesis #2 by [specific verification step].
  ```

- **Engine status summary** — which engines ran, which were unavailable, confidence distribution (`CONFIRMED: N, LIKELY: N, CANDIDATE-VERIFIED: N`), perspective verdict (`CONVERGENT` or `DIVERGENT-N`)
- **Rejection ledger** (condensed) — count by category (hallucination / chain-broken / mitigated / needs-info)
- **LLM Fix Prompt** — emitted **only for the Primary RCA** when its grounding verdict is `VERIFIED`. Suppress the Fix Prompt if Primary is `LIKELY-VERIFIED` (use `INVESTIGATE-FURTHER` verb) or if any alternative cluster has comparable or higher confidence in a different fix location (escalation to user judgment).

### 8d. Engine-attribution and perspective tags (mandatory on every shipped cluster)

| Engines flagging cluster | Attribution tag | Perspective tag |
|--------------------------|-----------------|-----------------|
| 3 / 3 | `[codex+agy+claude]` | `[CONVERGENT]` (if also the only surviving cluster) |
| 2 / 3 | `[codex+agy]` (any 2-combo) | `[CONVERGENT]` or `[DIVERGENT-N → primary/alt-i]` |
| 1 / 3, grounded | `[codex-verified]` / `[agy-verified]` / `[claude-verified]` | `[DIVERGENT-N → alt-i]` (almost always alternative) |

## 9. REPORT — extend canonical Scout Investigation Report

The multi-engine report extends `references/output-format.md` with:

- Front matter: `engine_concurrence` line + `perspective_verdict` line
- New section after Root Cause Analysis: `## Alternative Hypotheses` (omit if `CONVERGENT`)
- New section before LLM Fix Prompt: `## Verification Order`
- New section before Regression Prevention: `## Engine Status` (engines run, distribution, rejections)

`SCOUT_TO_BUILDER_HANDOFF` carries the verification ordering inline; Builder must process alternatives in the listed order before declaring the bug fixed.

---

## Parallel Subagent Prompt Skeleton

Use the Agent tool three times in the same message. Each subagent receives:

```
You are the {engine} investigation subagent for Scout.

# Role
Independently perform root cause analysis for the bug below. You are one of three engines working in parallel — do not aim for exhaustiveness; surface the root cause hypotheses your training data suggests are most plausible. Genuinely different hypotheses across engines are valuable; do not anchor to the most obvious explanation.

# Symptom
{Verbatim error message, stack trace, log lines, behavioral description}

# Reproduction state
{reproduced | partially reproduced | not reproduced}
{Minimal repro steps if available}

# Environment
{Runtime, version, deployment context}

# Ruled-out hypotheses (do not re-traverse)
{List from prior single-engine investigation if multi mode was auto-promoted, with elimination evidence}

# Output format
Return ONLY JSON matching this exact schema (no commentary outside the JSON):

{JSON schema from §3}

# Constraints
- Return 1-3 hypotheses. Single-hypothesis is acceptable for high-conviction cases; multiple are preferred for ambiguous symptoms.
- Each `root_cause_hypothesis` must name a SYSTEMIC cause, not a surface symptom and not "human error".
- Each `causal_chain` must trace trigger → state transition → failure. No hand-waving steps.
- Each `evidence` entry must cite a real source (file:line, log source, trace ID) with a verbatim quote. Do not invent evidence.
- Each hypothesis must include `reproduction_steps` even if speculative — label as "speculative repro" if unverified.
- Confidence is 0.0-1.0 numeric. Calibrate honestly; the integration step downgrades over-confident outputs.
- Do not write fix code — RCA only.
- Open with the deliverable (no completion preamble).
```

For Codex / Antigravity subagents, the subagent's first action is `codex exec --full-auto` / `agy -p` with this prompt. For the Claude subagent, use the Agent tool with `subagent_type: general-purpose` and the prompt above.

---

## Degraded Modes

| Situation | Behavior |
|-----------|----------|
| 1 engine binary missing | Run the other two; all clusters become at most `LIKELY` (2/3 ceiling) or `CANDIDATE` (1/2); stricter GROUND required |
| 2 engines fail | Single-engine RCA; every hypothesis is `CANDIDATE` and must be `VERIFIED` to ship as Primary; Alternative Hypotheses section omitted (no divergence to preserve from a single engine) |
| All 3 fail | Abort multi mode; degrade to default `bug` Recipe with Scout main context |
| User explicitly requests single engine | Skip fan-out; use default `bug` Recipe |
| Symptom is a known pattern (e.g., null deref with obvious cause) | Optionally skip multi; recommend default Recipe |
| Reproduction requires production data | Multi mode still useful for hypothesis breadth, but GROUND will produce many `NEEDS-INFO` verdicts; flag in report |

---

## Why This Works for RCA (Pattern H rationale)

- **Hypothesis lock-in is the dominant single-engine RCA failure mode.** Once committed, evidence is filtered through the lock. Independent fan-out breaks the lock structurally rather than relying on the engine's metacognition.
- **Concurrence on root cause class is rare for non-trivial bugs.** When three engines independently converge, the RCA is almost certainly correct. When they diverge, the divergence itself is the diagnostic — single-engine confidence in that case would be falsely high.
- **Scout's downstream is fix-routing, not fix-writing.** Builder receives an explicit verification order across primary + alternatives, eliminating the "fix didn't work, re-investigate from scratch" cycle. The alternative hypotheses are pre-grounded and ready to verify.
- **Pattern H is not Pattern C with extra steps.** Pattern C drops dissent; Pattern H ships dissent as a feature. This matches the actual epistemic state of RCA — multiple plausible root causes for the same symptom is the common case, not the edge case.

---

## Cross-References

- `_common/MULTI_ENGINE_RECIPE.md` — base protocol (canonical flow, PREFLIGHT, engine-attribution conventions, Pattern H definition)
- `_common/SUBAGENT.md §MULTI_ENGINE` — engine dispatch, loose-prompt rule, fallback rules
- `judge/references/tri-engine-review.md` — Pattern C canonical implementation (confidence-only axis, dissent dropped)
- `spark/references/tri-engine-proposal.md` — Pattern D canonical implementation (divergence-primary, dissent preserved as Portfolio)
- `scout/references/output-format.md` — Scout's canonical Investigation Report shape that multi-engine output extends
- `scout/references/fix-prompt-generation.md` — LLM Fix Prompt rules; multi mode emits one Fix Prompt for the Primary RCA only
- `_common/INVESTIGATION_ESCALATION.md` — confidence scale aligned across Scout / Lens / Trail / Specter
- `_common/OPUS_47_AUTHORING.md` — spawn prompt sizing (P2), tool-use eagerness during GROUND (P3), thinking depth during SYNTHESIZE (P5)
