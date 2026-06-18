# Adaptive Prompt Policy — Context-Adaptive Spawn Tuning

**Purpose:** Auto-tailor every spawn prompt to the current **project** and **session** context, and self-reinforce within the session from observed outcomes — so inter-agent instructions get sharper as a session progresses, without any durable global rewrite.
**Read when:** Composing a spawn prompt at an EXECUTE step, or deciding how directives adapt to project/session signals.

> **Scope is the safety model.** This policy operates **only within the current session + project**. It is **ephemeral** (resets at the session/project boundary) and **reversible** (every adjustment is per-spawn; nothing irreversible happens). Because no durable global file is written, **no approval gate is required** — this runs automatically in all modes. Durable, cross-project template rewrites are explicitly **out of scope** here; that path stays gated (offline `tune` → Darwin promotion → Guardian commit, see §6).

> **Honest mechanism.** This is **evidence-accumulating, case-based adaptation** — not neural RL. The hub cannot train weights mid-session. "Reinforcement" means: a journaled within-session record of `context-features → directive-choice → outcome`, consulted to bias the next spawn's directive selection. Bounded heuristics over a vetted directive library, never free-form prompt invention.

---

## 1. The three layers

```
① PROJECT PROFILE  — built once per session (first spawn / hub init), from project facts
② SESSION LEDGER   — grows through the session, from each spawn's outcome
③ ADAPTIVE ASSEMBLY — every EXECUTE step: base template ⊕ ① ⊕ ② → the spawn prompt
```

Layer ③ is the only thing that touches a spawn; ① and ② are the inputs it reads.

---

## 2. Layer ① — Project Profile (per-session, built once)

Assemble at the first spawn of the session and cache for the session. Sources and the directive defaults they imply:

| Source | Signal | Directive default it sets |
|--------|--------|---------------------------|
| `.agents/PROJECT.md` | project phase, goals, constraints | which references to front-load; tone |
| repo stack (lang / framework) | TS-strict / dynamic / native | tool-use directive emphasis (type rigor, test-first) |
| `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` | conventions, language, style | output language, naming, commit style passed to spawns |
| hub engine (Opus 4.8 / Fable 5 / Codex / agy) | authoring protocol | **Fable 5 → lighter prompt + `high` default effort + no-reasoning-reproduction; Opus 4.8 → full P1-P5 directives** (per `hub-authoring.md`) |
| domain affinity (Game/SaaS/…) | task domain | default add-on agents, envelope sizing |
| repo size / file count | scope | base output envelope (small repo → tighter) |

The Project Profile is **read-only project context** — it does not modify any project file.

---

## 3. Layer ② — Session Ledger (per-session, accumulates)

Held in working state for the session (optionally journaled, §5). After each spawn, record one row:

`{ agent, recipe, directive_choices, _STEP_COMPLETE.status, output_len vs envelope, token_cost, user_correction? }`

Within-session reinforcement signals → next-spawn adjustment:

| Observed this session | Adjustment to subsequent spawns |
|-----------------------|----------------------------------|
| Output overran its envelope | Tighten the envelope for that agent / similar tasks |
| `_STEP_COMPLETE: BLOCKED \| FAILED` | Raise effort, add context delta, add a thinking directive next attempt |
| Step succeeded cheaply and cleanly | Keep directives; consider trimming for token economy |
| **User corrected the output** (style, scope, wrong assumption) | Fold the correction into the constraints of subsequent same-agent spawns this session |
| Token budget pressure rising | Trim which references are loaded; shrink envelopes; switch context-strategy toward `reset` |
| Same agent ran before this session | Reuse its last-good directive set as the starting point |

Reinforcement is **monotone within the session and forgotten after it** — last session's mistakes never silently persist into a fresh one.

---

## 4. Layer ③ — Adaptive Assembly (every spawn)

At each EXECUTE step, compose:

```
spawn_prompt = base template (Agent Spawn Template)
             ⊕ Project Profile defaults (②)
             ⊕ Session Ledger adjustments (③)
```

**Bounded to vetted ranges — the assembly is selection, not invention:**
- Envelope length, effort tier, tool-use / thinking directives, and the reference subset are chosen from the libraries in `hub-authoring.md` / `OPUS_48_AUTHORING.md`. The policy **selects and dials within** those; it never authors a novel unsafe directive.
- **Never deletes a behavior or safety rule, acceptance criterion, or output-contract field** (Core Rule #4 — preserve behavior before style). Adaptation only *adds/sizes* guidance; it cannot strip the spawn's required structure.
- **Honors the hub-authoring protocol**: Opus 4.8 → the four directive fields; Fable 5 → lighter prompts, `high` effort, and the **no-reasoning-reproduction rule** (any "echo/show/transcribe your reasoning" wording is forbidden — it trips `refusal`).

The result is a spawn prompt tuned to *this* project and *this* session's accumulated signal, every time.

---

## 5. Optional warm-start (off by default)

The only persistence offered: journal the end-of-session Project Profile + last-good directive sets to `.agents/adaptive-prompt-policy.journal.md` (gitignored). On the next session **in the same project**, load it so the session starts pre-tuned instead of cold.

- This is a **context cache, not a template rewrite** — it pre-seeds Layer ① only, still bounded to vetted ranges, still overridable by this session's fresh signals.
- Off by default; enable explicitly. Even on, it never edits a spawn template, a SKILL.md, or any tracked file.

---

## 6. Out of scope (the gated path)

Durable, cross-project changes — rewriting the Agent Spawn Template, `hub-authoring.md`, `_common/HANDOFF.md`, or an agent's `SKILL.md` — are **not** done by this policy. If a within-session pattern proves broadly valuable, it is promoted through the **gated** path, never automatically:

`offline tune (corpus backtest) → Lore curation (METAPATTERNS) → Darwin promotion proposal → user approval → Guardian commit`

This keeps the irreversible, all-spawns-affecting writes behind evidence + approval, while the day-to-day session/project adaptation here stays fully automatic.

---

## 7. Guards

| Risk | Guard |
|------|-------|
| Overfitting to one task in the session | Adjustments are agent/task-class scoped, not global; a single outlier run does not flip a directive — require a repeated signal |
| Adaptation masking a real problem | Session Ledger surfaces persistent BLOCKED/FAILED to the normal error-handling escalation, it does not just keep re-tuning |
| Stripping required structure | §4 hard rule: never delete behavior/safety/AC/output-contract fields |
| Cross-session contamination | Ephemeral by default; warm-start (§5) is opt-in and pre-seeds Layer ① only |
| Unsafe directive on Fable 5 | §4 enforces the no-reasoning-reproduction rule from `hub-authoring.md` |

---

## 8. Relationship to neighbors

- **`context-strategy.md`** — sibling: that decides *what context flows* between agents (reset / persist / hybrid); this decides *how the spawn directives adapt* to project+session signals. Used together at spawn time.
- **`hub-authoring.md` / `OPUS_48_AUTHORING.md`** — the vetted directive library this policy selects from; the source of the P/F principles it must honor.
- **LEARN / `routing-learning.md`** — LEARN adapts *routing* (which chain) across runs with durable safety; this adapts *spawn directives* within a session, ephemerally. Same evidence spirit, different target and scope.
