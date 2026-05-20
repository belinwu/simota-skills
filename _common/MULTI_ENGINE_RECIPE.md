# Multi-Engine Recipe Protocol

Cross-skill protocol for the `multi` Recipe — spawning Codex + Antigravity + Claude subagents in parallel for tasks where multi-engine perspectives improve quality. Adapted from `judge/references/tri-engine-review.md` for non-review skills.

**Audience**: Skills implementing a `multi` Recipe (Spark, Plea, Omen, Magi, Compete, Sentinel, Riff, Flux, Researcher, Vision, Saga, Atlas, Echo, Scout, and future additions).

**Prerequisites**: `_common/SUBAGENT.md §MULTI_ENGINE` (base engine dispatch mechanics), `judge/references/tri-engine-review.md` (canonical PREFLIGHT/FAN-OUT logic).

---

## When to Use Multi-Engine

A skill should ship a `multi` Recipe when at least one of these conditions holds:

1. **Training-data divergence value** — different engines (Codex/GitHub-heavy, Antigravity/Google-product-heavy, Claude/Anthropic-curated) have non-overlapping priors that meaningfully change the output (ideation, research design, competitive analysis, failure-mode enumeration).
2. **Self-bias risk** — the skill's output is evaluative and a single engine would inherit blind spots (security scanning, code review, persona channeling).
3. **Decision stakes warrant cross-validation** — strategic judgment, architectural choices, security findings, post-mortems where a single-engine answer is too narrow.

Do NOT add `multi` when:

- The task is deterministic (format conversion, code generation following a spec, math)
- Output quality is purely aesthetic (image gen, color tokens) — engine "agreement" is meaningless
- Single source of truth exists (test execution, build runs) — multi-engine doesn't add signal
- Spawn cost exceeds value (sub-30s tasks, one-line lookups)

---

## Three Pattern Types

Each skill's `multi` Recipe falls into one of three patterns. Choose the one that matches your skill's quality model.

### Pattern D — Divergence-Primary

**Use when**: Output value comes from *breadth of ideas / perspectives*. Disagreement is informative; single-engine insights are often the breakthrough.

**Examples**: Spark (proposals), Plea (synthetic demand), Omen (failure modes), Compete (competitive coverage), Riff (brainstorming), Flux (reframing), Researcher (research design), Vision (UX direction), Saga (narratives).

**Scoring**:
- `UNIVERSAL` (3/3) = broadly recognized; safe but possibly obvious
- `LIKELY` (2/3) = strong with one dissenter
- `VERIFIED-DIVERGENT` (1/3 after grounding) = single-engine breakthrough; NOT auto-low-value

**Synthesis**: Preserve divergence. Default to Portfolio merge (multiple complementary outputs); offer Compete merge (single best, re-mixing wording) only on explicit request.

**Filter**: Drop only hallucinated, duplicate, or vague outputs. Divergent outputs that pass grounding ship.

---

### Pattern C — Concurrence-Primary

**Use when**: Output value comes from *agreement reduces false positives*. Disagreement is noise; consensus is the quality signal.

**Examples**: Judge (code review), Sentinel (SAST), Probe (dynamic security), Attest (spec compliance).

**Scoring**:
- `CONFIRMED` (3/3) = high-confidence finding; ship
- `LIKELY` (2/3) = ship with concurrence tag
- `CANDIDATE` (1/3) = MUST pass grounding to ship; drop if rejected

**Synthesis**: Filter aggressively. Single-engine findings ship only after explicit grounding/verification by main context.

**Filter**: Drop style-only, already-mitigated, hallucinated, low-severity findings. Goal: every shipped finding is actionable.

---

### Pattern H — Hybrid (Both Axes Matter)

**Use when**: The skill produces *judgment* — both creative options AND confidence calibration matter. Concurrence raises confidence; divergence reveals trade-offs.

**Examples**: Magi (strategic deliberation), Atlas (architecture/ADR), Scout (RCA), Echo (UX walkthrough).

**Scoring** (use both axes):
- Confidence axis: `CONFIRMED` / `LIKELY` / `CANDIDATE` (per Pattern C)
- Perspective axis: `CONVERGENT` (all engines reach same conclusion) / `DIVERGENT` (engines split on conclusion — surface the split as a feature, not a bug)

**Synthesis**: Present both the consensus position AND the dissenting perspectives. For Magi-style 3-viewpoint skills, this becomes **3 engines × N viewpoints = N×3 matrix** — extract patterns from the matrix rather than averaging.

**Filter**: Drop hallucinations and incoherent outputs; preserve well-reasoned dissents.

---

## Canonical Flow (all patterns)

```
SCOPE → PREFLIGHT → FAN-OUT (parallel subagents) → NORMALIZE → CLUSTER → SCORE → GROUND/CALIBRATE → SYNTHESIZE → DELIVER
```

The flow is identical across patterns; what differs is the SCORE rubric and the SYNTHESIZE merge strategy.

### 1. SCOPE

Define the task target once. All three subagents share the same scope. Include skill-specific context (persona pool, plan being challenged, system under analysis, etc.) but NOT skill-specific frameworks/templates — those apply at SYNTHESIZE.

### 2. PREFLIGHT — engine availability detection

**Run in skill main context. Never delegate to subagents.** Subagent PATH is narrower than the user's interactive shell, leading to false-negative "unavailable" verdicts.

Canonical probe (per `judge/references/tri-engine-review.md §2`):

```bash
for cli in codex agy claude; do
  if command -v "$cli" >/dev/null 2>&1; then
    echo "$cli: $(command -v $cli) ($($cli --version 2>&1 | head -1))"
  else
    for p in "$HOME/.bun/bin/$cli" "$HOME/.local/bin/$cli" "/usr/local/bin/$cli" "/opt/homebrew/bin/$cli"; do
      if [ -x "$p" ]; then echo "$cli: $p ($($p --version 2>&1 | head -1))"; break; fi
    done || echo "$cli: NOT FOUND"
  fi
done
```

**Availability verdict — strict criteria** (identical to Judge tri-engine PREFLIGHT):

| Outcome | Treatment |
|---------|-----------|
| Binary found AND `--version` returns | `AVAILABLE` |
| Binary not found in any probed location | `UNAVAILABLE (binary missing)` |
| Binary found but `--version` exits non-zero | `AVAILABLE-WITH-WARNING` |
| Auth/network/timeout error | `AVAILABLE` — runtime failure, not unavailability |

**Never declare unavailable based on**: transient errors, prior session failures, absence from standard `$PATH` alone (always probe fallback paths).

### 3. FAN-OUT — parallel subagents

Spawn **three Agent calls in a single message** for genuine parallel execution. Each subagent has an independent context (no shared bias).

| Subagent | Engine | Baseline command |
|----------|--------|------------------|
| `{verb}-codex` | Codex CLI | `codex exec --full-auto "<prompt>"` |
| `{verb}-agy` | Antigravity CLI | `agy -p "<prompt>" --dangerously-skip-permissions` |
| `{verb}-claude` | Claude Code CLI (subagent) | Agent tool with `subagent_type: general-purpose` |

`{verb}` is skill-specific: `propose` (Spark), `demand` (Plea), `failure` (Omen), `deliberate` (Magi), etc.

**Loose prompt rule** (per `_common/SUBAGENT.md` MULTI_ENGINE): pass only Role + Target + Output format. Do NOT pass skill-specific frameworks, taxonomies, or templates — those are applied at SYNTHESIZE. The point is to let each engine's training-data priors drive independent output.

**JSON output schema** is mandatory for deterministic integration. Each skill defines its own schema in its `references/tri-engine-{verb}.md`, but always includes:

```json
{
  "engine": "codex|agy|claude",
  "outputs": [ /* skill-specific output items */ ],
  "engine_notes": "Optional: what bias/strength this engine knows it brings"
}
```

If an engine returns free-form Markdown, ask its subagent to re-emit as JSON before integrating.

### 4. NORMALIZE

Parse the three JSON blobs into a unified output list. Tag each output with its source engine. Preserve per-engine wording — divergent phrasing may carry signal.

### 5. CLUSTER — dedup across engines

Group outputs that describe the same item (defect / opportunity / failure mode / argument). Two outputs match when they share enough identity dimensions per the skill's domain definition.

**Generic identity rules** (refine per skill):
- Same primary subject (file, persona, system component, claim)
- Semantic overlap in the core statement
- Same category/class label

Record the set of engines that produced each cluster.

### 6. SCORE — pattern-specific

Apply the scoring rubric for your pattern type (D / C / H). See per-pattern tables above.

### 7. GROUND or CALIBRATE — skill main context, never delegated

**For Pattern C (Concurrence)**: GROUND `CANDIDATE` findings by reading the actual code/system. Mark `VERIFIED` / `REJECTED` / `NEEDS-INFO`.

**For Pattern D (Divergence)**: GROUND `VERIFIED-DIVERGENT` candidates against the artifact base — does the cited evidence/persona/system actually exist? CALIBRATE against real data when available (e.g., Plea against Voice/Trace).

**For Pattern H (Hybrid)**: Both. Ground confidence; preserve dissenting perspectives that are well-reasoned even if not converged.

**Always check**:
1. Hallucinated entities (functions, personas, competitors, APIs, file paths)
2. Duplicates already present in the target system
3. Vague or unmeasurable claims
4. Style/aesthetic-only opinions (drop unless task is explicitly about style)

### 8. SYNTHESIZE — pattern-specific

**Pattern D**: Portfolio (default) or Compete merge. Engine-attribution tag mandatory.
**Pattern C**: Filter to actionable findings only. Concurrence tag mandatory.
**Pattern H**: Present consensus + dissent. Both confidence tag AND perspective tag mandatory.

**Universal output requirements**:
- Engine-attribution tag on every shipped output: `[codex+agy+claude]` (3/3), `[codex+agy]` etc. (2/3), `[codex-verified]` (1/3 grounded)
- Engine status summary in header (which engines ran, which failed/unavailable)
- Rejection ledger (condensed): count by category — preserves SNR transparency without re-introducing noise
- Concurrence distribution: e.g., `UNIVERSAL: N, LIKELY: N, VERIFIED-DIVERGENT: N`

### 9. DELIVER

Output structure follows the skill's existing template, with multi-engine additions documented in that skill's `references/tri-engine-{verb}.md`.

---

## Parallel Subagent Prompt Skeleton

Use the Agent tool three times in the same message. Each subagent prompt follows this structure:

```
You are the {engine} {verb} subagent for {Skill}.

# Role
{One-line task persona}. You are one of three engines working independently — do not try to be exhaustive; surface what your training data suggests is most promising.

# Target
{Task-specific context: scope, persona, system, plan, etc.}

# Output format
Return ONLY JSON matching this exact schema (no commentary outside the JSON):

{skill-specific JSON schema}

# Constraints
- {Skill-specific quality constraints}
- Do not paraphrase or invent entities the system clearly does not have; if you assert reuse of existing data/logic, name it specifically
- Open with the deliverable (no completion preamble)
```

Engine-specific invocation:

```bash
# Codex (subagent runs this)
codex exec --full-auto "$(cat /tmp/prompt.md)"

# Antigravity (subagent runs this)
agy -p "$(cat /tmp/prompt.md)" --dangerously-skip-permissions
```

For the Claude subagent, use the Agent tool with `subagent_type: general-purpose` and the prompt above.

**Invocation invariants** (all engines): subscription auth only (no provider API keys), default model (no `-m` / `--model` / `-c model=...`), structured JSON output required.

---

## Degraded Modes

| Situation | Behavior |
|-----------|----------|
| 1 engine binary missing | Run the other two; note reduced confidence/diversity; CANDIDATE-tier outputs require stricter grounding |
| 2 engines fail | Single-engine output; treat every output as CANDIDATE; ground all before reporting; flag reduced confidence |
| All 3 fail | Abort multi mode; degrade to the skill's default Recipe |
| User explicitly requests single engine | Skip fan-out; use default Recipe |
| Trivial scope | Optionally skip multi; recommend default Recipe |
| Auth/quota error during execution | Surface the actual error in the report; do not silently degrade |

---

## Engine-Attribution Tag Convention

Every output shipped from a `multi` Recipe carries an engine-attribution tag. Tag formats:

| Engines flagging | Tag format | Meaning |
|------------------|------------|---------|
| 3 / 3 | `[codex+agy+claude]` | Universal / Confirmed |
| 2 / 3 | `[codex+agy]`, `[codex+claude]`, `[agy+claude]` | Likely (two-of-three) |
| 1 / 3 grounded | `[codex-verified]`, `[agy-verified]`, `[claude-verified]` | Single-engine, passed grounding |
| 1 / 3 rejected | (not shipped) | — |

For Pattern D skills with calibration (Plea): append a second tag `[validated]` / `[supported]` / `[hypothesis]` / `[synthetic-only]` per the skill's calibration rules.

For Pattern H skills (Magi/Atlas/Scout/Echo): append a perspective tag `[CONVERGENT]` or `[DIVERGENT-N]` (N = number of dissenting positions).

---

## CAPABILITIES_SUMMARY Conventions

Skills implementing a `multi` Recipe should add a capability line to their CAPABILITIES_SUMMARY block:

```
tri_engine_{verb}: `multi` Recipe — {one-line description of what fan-out produces}; {pattern type — Concurrence-primary / Divergence-primary / Hybrid}; {merge strategy default}; {key skill-specific feature, e.g., calibration tags, viewpoint matrix, persona axis}
```

Examples (already shipped):
- Spark: `tri_engine_proposal: ... Compete-merge or Portfolio-merge ... preserves divergent breakthrough proposals`
- Plea: `tri_engine_demand: ... cross-persona-universal signals AND single-engine divergent-voice insights ... calibration tags`

---

## Implementation Checklist

When adding `multi` Recipe to a new skill:

- [ ] Decide pattern type (D / C / H)
- [ ] Add `tri_engine_{verb}` line to CAPABILITIES_SUMMARY
- [ ] Add `Multi-Engine` row to the Recipes table with `multi` subcommand
- [ ] Add `multi` behavior note in Subcommand Dispatch
- [ ] Add `Multi-Engine Mode` section to SKILL.md (use Spark or Plea as template)
- [ ] Add `multi-engine` row to Output Routing
- [ ] Create `references/tri-engine-{verb}.md` with skill-specific:
  - JSON output schema
  - CLUSTER identity rules
  - SCORE rubric (per pattern type)
  - GROUND/CALIBRATE checks
  - SYNTHESIZE merge strategy
  - Subagent prompt skeleton
- [ ] Add `references/tri-engine-{verb}.md` and `_common/SUBAGENT.md` to Reference Map
- [ ] Add `tri_engine:` block to `_STEP_COMPLETE.Output` schema
- [ ] Verify CAPABILITIES_SUMMARY HTML comment block is intact (`<!--` opens, `-->` closes)

---

## Cross-References

- `_common/SUBAGENT.md §MULTI_ENGINE` — base protocol (engine dispatch, loose prompts, fallback rules)
- `judge/references/tri-engine-review.md` — canonical Pattern C implementation
- `spark/references/tri-engine-proposal.md` — canonical Pattern D implementation (with Portfolio/Compete merge)
- `plea/references/tri-engine-demand.md` — canonical Pattern D with calibration + cross-axis (persona × engine)
- `_common/OPUS_47_AUTHORING.md` — spawn prompt sizing, thinking-depth nudges, parallel-fan-out triggers
