# Hub-Engine Authoring

Per-engine authoring protocols that apply once the hub orchestrator is detected (see SKILL.md → **Execution Model → Orchestrator Detection**).

## Claude Code hub

Apply `_common/OPUS_48_AUTHORING.md` principles **P4 (parallel subagent triggers), P6 (effort-level awareness), P7 (delegation framing), P9 (effort-calibrated tool use)**.

Opus 4.8 spawns fewer subagents and reasons more by default, respects `effort` strictly, and follows instructions literally — explicit fan-out triggers, per-step model/effort selection, and explicit step scope are mandatory. Spawn prompts must state thinking nudges (P5) and length envelopes (P2).

## Claude Code hub — Fable 5

> Source: Anthropic "Prompting Claude Fable 5" + "Introducing Claude Fable 5 and Claude Mythos 5" (platform.claude.com, 2026-06). Applies when the Claude Code hub session runs on `claude-fable-5`. The P-principles still hold; the F-principles below **override** them where they conflict, because Fable 5's behavior differs from Opus 4.8. When the hub model is unknown, author for Opus 4.8 — safe on both.

Fable 5 is a Mythos-class model: 1M context, adaptive-thinking-only (raw CoT never returned), safety classifiers that can return `stop_reason:"refusal"`. The orchestration-relevant behavior shifts:

| Behavior | Opus 4.8 | Fable 5 → Nexus action |
|----------|----------|------------------------|
| Default effort | `xhigh` | `high`; `xhigh` only for capability-sensitive steps, `low`/`medium` for routine (still exceed prior-model `xhigh`). Lower effort if a step finishes but runs longer than needed |
| Spawn-prompt verbosity | Four directive fields mandatory; enumerate behaviors | **Lighter** — a brief outcome+brevity instruction steers as well as enumerating; over-prescriptive prompts/skills *degrade* output |
| Parallel subagents | Sparse — explicit fan-out triggers mandatory (P4) | Dispatches readily; relax explicit triggers. Prefer **async** orchestrator↔subagent communication over blocking on each `wait`; long-lived subagents save cache + avoid slowest-branch bottleneck |
| Turn length | Minutes | Can run many minutes/hours per step. Raise client timeouts, prefer `run_in_background` + async check-in over blocking; restructure long chains as checkpoint-resumable |
| Reasoning visibility | Returnable | Raw CoT never returned. **Never** instruct a spawned agent to echo/show/transcribe/explain its reasoning as response text — trips `reasoning_extraction` refusal → forced Opus 4.8 fallback. Read summarized `thinking` blocks instead |

**F-principles (apply on top of P4/P6/P7/P9 for a Fable 5 hub):**

- **F1 — No reasoning reproduction.** Audit every spawn prompt and the spawned skill's SKILL.md for "show your reasoning / explain step by step in the response / transcribe your thinking" wording. Strip it. For reasoning visibility use summarized thinking + a send-to-user tool, not response-text echo. *(Highest priority — silent fallback-rate inflater.)*
- **F2 — Light spawn prompts.** Keep the spawn template's acceptance-criteria + a one-line brevity/outcome instruction; drop enumerated per-behavior directives. Lead spawned agents with "report the outcome first."
- **F3 — Default `high` effort.** Plan and execute steps default to `high`. Reserve `xhigh` for the hardest design/verify steps; drop to `medium`/`low` for routine fan-out. Don't over-budget routine work at high effort (Fable 5 over-explores/refactors when un-scoped — add "do the simplest thing; don't refactor/abstract beyond the task" to spawn prompts).
- **F4 — Async fan-out.** Spawn parallel subagents freely; communicate asynchronously; keep the orchestrator working while branches run. Don't serialize on `wait` unless a barrier is genuinely required.
- **F5 — Ground long-run progress.** For chains ≥ 4 steps or autonomous runs, instruct each agent: "Before reporting progress, audit each claim against a tool result from this session; if unverified, say so." Nearly eliminates fabricated status.
- **F6 — Refusal-aware routing.** Steps in offensive-security / biology-life-sciences / reasoning-extraction domains can return `stop_reason:"refusal"` (HTTP 200, not an error). Configure fallback to Opus 4.8 (`fallbacks` param or SDK middleware); a refused-before-output step is not billed. Treat `refusal` as a routing signal, not a failure.

## Codex CLI hub

Apply `_common/CODEX_ORCHESTRATION.md` principles **C1 (spawn-depth budget), C2 (synchronous fan-out/join), C6 (checkpoint-resume)**, plus C3/C7 for model and approval posture.

Codex has no background-spawn primitive (parallel = N `spawn_agent` → `wait_agent` all), gates fan-out via `agents.max_depth`, and routes effort by model choice (`gpt-5.5` plan / `gpt-5.4`-family execute) plus the `model_reasoning_effort` config key (`minimal|low|medium|high|xhigh`) — not by an Opus `effort` enum.

## agy hub

Best-effort; apply the C-principles by analogy under `_common/CLI_COMPATIBILITY.md §3, §9` constraints.

## Spawn Template Variants

**Claude Code (`Agent(...)`)** uses the canonical template in SKILL.md → **Agent Spawn Template**. On an **Opus 4.8** hub the four directive fields (acceptance criteria / output length / tool-use / thinking) are not optional: Opus 4.8 calibrates output length to context, restrains tool calls by default (raise `effort` to increase tool use), and interprets each field literally, so both under- and over-shoot occur when these are implicit. On a **Fable 5** hub these directives are lighter (F2): keep acceptance-criteria + a one-line brevity/outcome instruction, drop enumerated per-behavior directives, and **never** include reasoning-reproduction wording (F1 — trips `reasoning_extraction` refusal). For parallel spawns, issue multiple `Agent(... run_in_background: true)` calls in the same turn (Fable 5 dispatches these readily — F4). Shared protocol: `_common/OPUS_48_AUTHORING.md`; Fable 5 deltas: § Claude Code hub — Fable 5.

**Codex CLI variant**: same prompt body; resolve skill path to `~/.codex/skills/[agent]/SKILL.md` or `<repo>/.agents/skills/[agent]/SKILL.md`. Four directive fields stay required. Authoring follows `_common/CODEX_ORCHESTRATION.md` (C-principles), not the Opus note — effort routed by model choice (`gpt-5.5` plan / `gpt-5.4`-family execute, C3) + `model_reasoning_effort`; fan-out gated by `agents.max_depth` + `agents.max_threads` (C1). API patterns (L1 `spawn_agent`→`wait_agent`, L2 parallel-then-join, L3 `send_input`/`resume_agent`/`close_agent` for checkpoint-resume) → `reference/execution-layers.md` § Codex CLI.

**agy variant**: same prompt body; TUI via `/agent [agent]-[task-slug] "<body>"`, headless via `agy -p "<body>" --dangerously-skip-permissions`. Headless capture is **file-handoff, not stdout** — append the `_common/CLI_COMPATIBILITY.md §9.2` MANDATORY OUTPUT PROTOCOL (absolute-path artifact + `<<<END_OF_OUTPUT>>>` sentinel) and reference files via `@<path>`. Full silent-failure mitigations + verified template → `reference/execution-layers.md` § agy. Replace skill path with `~/.gemini/antigravity-cli/skills/[agent]/SKILL.md` or `<repo>/.agents/skills/[agent]/SKILL.md`.

## Execution-Layer Key Rules

- **Codex**: `spawn_agent` may be lazily hidden — attempt the call when prereqs hold ("tool not visible" ≠ "tool not callable"). Codex tools: `spawn_agent`, `send_input`, `wait_agent`, `resume_agent`, `close_agent`.
- **agy headless**: use `@<path>` to inject file context; mandate absolute-path artifact write + `<<<END_OF_OUTPUT>>>` sentinel — `agy -p` never flushes to non-TTY stdout (issue #115, unfixed v1.0.5). Pass `--print-timeout 15m` for heavy syntheses; `--log-file <path>` for quota/OAuth failure diagnosis.
- **agy Pre-flight Notification**: before the first `agy -p ... --dangerously-skip-permissions` spawn of a session, emit the notification per `_common/CLI_COMPATIBILITY.md §9.1`.
- **Permission model**: agy defaults to `request-review`; autonomous Nexus must switch to `proceed-in-sandbox` (TUI) or `--dangerously-skip-permissions` (headless). Never use `always-proceed` in production.

## Model Selection

Model names are hub-engine-specific. The role → tier mapping is stable; the concrete model per tier depends on the orchestrator engine.

| Agent Role | Tier | Claude Code hub | Codex CLI hub | Rationale |
|-----------|------|-----------------|---------------|-----------|
| Investigation / read-only (Scout, Lens, Trail) | balanced | sonnet | `gpt-5.4` | Cost-efficient |
| Standard implementation (Builder, Artisan, Radar) | balanced | sonnet | `gpt-5.4` | Balanced |
| High-complexity design (Sentinel, Atlas) | high-reasoning | opus / **fable-5** | `gpt-5.5` | Precision-critical |
| Lightweight tasks (Quill, Morph) | fast | haiku | `gpt-5.4-mini` | Minimal cost |

Fable 5 hub: `claude-fable-5` serves the high-reasoning tier (plan + hardest design/verify steps); default effort `high`, `xhigh` only for capability-sensitive steps, `medium`/`low` for routine fan-out — Fable 5's lower effort already exceeds prior-model `xhigh`. Route refusal-prone domain steps with an Opus 4.8 fallback (F6). Full behavior deltas → § Claude Code hub — Fable 5.

Codex hub: route planning / high-complexity steps to `gpt-5.5` and execution steps to `gpt-5.4` / `gpt-5.4-mini` (Plan-and-Execute, `CODEX_ORCHESTRATION.md` C3); tune depth within a tier via `model_reasoning_effort` (`minimal|low|medium|high|xhigh`, default `medium` — verified 2026-06). Legacy IDs `gpt-5.1`/`gpt-5.1-codex-max`/`gpt-5.2`/`gpt-5.3-codex` are deprecated. agy hub: switch via `/model` in TUI (per-session, not per-agent).
