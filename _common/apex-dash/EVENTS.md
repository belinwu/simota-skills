# apex-dash — Events Schema

Schema definition for `events.jsonl`. The producer (apex skills) and the consumer (dashboard server / client) **must follow the same schema** — that contract is the lifeline of consistency. Any schema change must update this document and bump `.spec-version`.

---

## 1. File Conventions

| Item | Value |
|------|-------|
| Path | `<repo>/.agents/apex/<run-id>/events.jsonl` |
| Format | JSON Lines (1 line per event, UTF-8, LF terminator) |
| Writes | Append-only. Past lines must never be rewritten |
| Ordering | Globally ordered by `seq`. The writer guarantees order via CAS or single-writer |
| Size budget | 200–800 bytes per event; 0.5–5 MB per run |
| Cleanup | Run directories older than 30 days are reaped by the generator script (see `GENERATION.md`) |

## 2. Common Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ts` | string (ISO8601 UTC) | ✓ | Event timestamp |
| `seq` | int | ✓ | Per-run sequence number, starts at 1, no gaps |
| `run_id` | string | ✓ | `apex-YYYYMMDD-HHMMSS-<short-hash>` |
| `kind` | string | ✓ | Event kind (table below) |
| `phase` | string | (kind-dependent) | `P0_Bootstrap` / `P1_Discovery` / … / `P6_Implementation` / `Ship` |
| `agent` | string | (kind-dependent) | Lowercase agent name (e.g. `plea`, `builder`) |
| `engine` | string | (kind-dependent) | `claude_code` or `codex_cli` |
| `meta` | object | optional | Kind-specific extras (see below) |

`meta` is a **flat object** (one nesting level). Binary data and full source are not stored; `meta.snippet` is capped at 280 characters.

## 3. Event Kinds

| `kind` | Purpose | Required extras |
|--------|---------|-----------------|
| `run_start` | Run begins | `meta.goal`, `meta.mode` (`AUTORUN` / `AUTORUN_FULL` / `GUIDED` / `INTERACTIVE`), `meta.scope` (`Lite` / `Standard` / `Full`) |
| `run_end` | Run ends | `meta.status` (`completed` / `aborted` / `error`), `meta.duration_ms` |
| `phase_enter` | Enter a phase | `phase`, `meta.parallel_tracks?` (e.g. `["tech","ux"]`) |
| `phase_exit` | Exit a phase | `phase`, `meta.exit_gate` (`pass` / `fail` / `skipped`) |
| `agent_start` | Agent spawned | `agent`, `phase`, `engine`, `meta.input_ref?`, `meta.expected_outputs?` |
| `agent_progress` | Optional in-flight progress | `agent`, `meta.progress` (0–1), `meta.note?` |
| `agent_end` | Agent completed | `agent`, `meta.status` (`done` / `blocked` / `need_info` / `error`), `meta.duration_ms`, `meta.output_ref?` |
| `tool_use` | Tool invocation | `agent`, `meta.tool` (`Read` / `Bash` / …), `meta.snippet?` |
| `checkpoint_wait` | Human-confirm waiting begins | `meta.label` (e.g. `Phase0_boundary_confirm`), `meta.deadline?`, `meta.mode` |
| `checkpoint_resolved` | Human confirmation closed | `meta.label`, `meta.outcome` (`approved` / `rejected` / `timeout_passed` / `timeout_aborted`) |
| `risk_gate` | Risk Gate verdict | `meta.verdict` (`Go` / `Conditional-Go` / `No-Go`), `meta.axes` (`{omen,ripple,echo}` each `pass` / `fail` / `pending`), `meta.notes?` |
| `orbit_iter` | One orbit loop iteration | `meta.iter`, `meta.convergence` (0–1), `meta.cost_per_task`, `meta.budget_used`, `meta.budget_max`, `meta.circuit` (`green` / `yellow` / `red`) |
| `engine_switch` | Engine boundary crossed | `meta.from`, `meta.to`, `meta.reason?` |
| `error` | Failure | `meta.severity` (`warn` / `error` / `fatal`), `meta.source` (`agent` / `server` / `hook`), `meta.message`, `meta.stack?` |
| `note` | Free-form diagnostic | `meta.text` |

## 4. JSON Schema (summary)

The full schema is materialised as a zod schema in `web/src/types/events.ts` at implementation time. Conceptual definition:

```ts
type Event = {
  ts: string;          // ISO8601
  seq: number;         // 1+
  run_id: string;
  kind: EventKind;
  phase?: Phase;
  agent?: string;
  engine?: "claude_code" | "codex_cli";
  meta?: Record<string, unknown>;
};

type EventKind =
  | "run_start" | "run_end"
  | "phase_enter" | "phase_exit"
  | "agent_start" | "agent_progress" | "agent_end"
  | "tool_use"
  | "checkpoint_wait" | "checkpoint_resolved"
  | "risk_gate"
  | "orbit_iter"
  | "engine_switch"
  | "error" | "note";

type Phase =
  | "P0_Bootstrap" | "P1_Discovery" | "P2_Ideate" | "P3_Verdict"
  | "P4_Spec" | "P5_Design" | "P6_Implementation" | "Ship";
```

## 5. State Transition Rules (reducer spec)

The same reducer is shared between server and client (single source of code).

| Event | Effect on state |
|-------|-----------------|
| `run_start` | `state.run_id`, `state.goal`, `state.mode`, `state.started_at`; all `state.phases.*.status = "pending"` |
| `phase_enter` | `state.current_phase = phase`; `state.phases[phase].status = "running"`; `state.phases[phase].started_at = ts` |
| `phase_exit` | `state.phases[phase].status = "done"` / `"failed"` / `"skipped"`; `state.phases[phase].ended_at = ts` |
| `agent_start` | `state.active_agents.push({name, phase, started_at, last_tool: null})` |
| `agent_progress` | `state.active_agents[name].progress = meta.progress`; update `note` |
| `agent_end` | Remove from `active_agents`; push to `state.completed_agents` |
| `tool_use` | `state.active_agents[name].last_tool = meta.tool`; `tool_count++` |
| `checkpoint_wait` | `state.checkpoints.push({label, status: "waiting", deadline})` |
| `checkpoint_resolved` | Update target checkpoint `status = outcome` |
| `risk_gate` | `state.risk_gate = { verdict, axes, at: ts }` |
| `orbit_iter` | `state.orbit.iters.push({...})`; `state.orbit.latest = ...` |
| `engine_switch` | `state.engine = meta.to`; push to `state.engine_history` |
| `error` | `state.errors.push(...)` (most recent 50 retained) |
| `run_end` | `state.ended_at = ts`; `state.final_status = meta.status` |

## 6. Validation

The producer side (emit helper) does **not** validate — best-effort append.
The consumer side **must guard**:

- Invalid JSON line → skip + record a `warn` in `state.errors`
- Unknown `kind` → accept; render the node greyed out
- Missing or duplicated `seq` → warn but continue
- Unknown `phase` / `agent` → accept; render as "unplaced node"

## 7. Sample

```jsonl
{"ts":"2026-04-30T12:00:00.000Z","seq":1,"run_id":"apex-20260430-120000-a3f","kind":"run_start","meta":{"goal":"passkey login","mode":"AUTORUN_FULL","scope":"Standard"}}
{"ts":"2026-04-30T12:00:00.500Z","seq":2,"run_id":"apex-20260430-120000-a3f","kind":"phase_enter","phase":"P0_Bootstrap"}
{"ts":"2026-04-30T12:00:01.000Z","seq":3,"run_id":"apex-20260430-120000-a3f","kind":"agent_start","agent":"spark","phase":"P0_Bootstrap","engine":"claude_code"}
{"ts":"2026-04-30T12:01:42.000Z","seq":4,"run_id":"apex-20260430-120000-a3f","kind":"agent_end","agent":"spark","meta":{"status":"done","duration_ms":101000,"output_ref":"P0/spark/candidates.md"}}
{"ts":"2026-04-30T12:02:00.000Z","seq":5,"run_id":"apex-20260430-120000-a3f","kind":"checkpoint_wait","meta":{"label":"Phase0_boundary_confirm","deadline":"2026-04-30T12:03:00.000Z","mode":"AUTORUN_FULL_60s"}}
{"ts":"2026-04-30T12:02:42.000Z","seq":6,"run_id":"apex-20260430-120000-a3f","kind":"checkpoint_resolved","meta":{"label":"Phase0_boundary_confirm","outcome":"timeout_passed"}}
```

## 8. Extension Policy

- New `kind` additions are backward compatible (existing kinds untouched)
- Adding fields to existing kinds is allowed; removing them is forbidden
- Adding enum values is allowed; removing them is forbidden
- Breaking changes bump the major version of `.spec-version`; the dashboard prompts for regeneration

## 9. Related

- `INTEGRATION.md` — the emit helper populates fields per this spec
- `DESIGN.md §4` — overall data flow
