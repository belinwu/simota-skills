# apex-dash — Generation Spec

Defines the inputs, generator prompt, output manifest, customisation surface, and verification steps for **per-repo auto-generation** of a dashboard.

---

## 1. Generation Strategy

- **Generator skill**: `forge` (rapid prototype) or `builder` (production grade). Default is `forge` to get a working dashboard quickly; promote to `builder` later if hardening is required
- **Output location**: `<repo>/.agents/apex-dash/` (inside the repo)
- **Source of truth**: every `.md` file under this directory (`_common/apex-dash/`)
- **Reproducibility**: source commit hash is persisted to `.spec-version`
- **Idempotency**: if it already exists, skip; pass `--regenerate` to rebuild

## 2. Pre-Scan Inputs

The generator skill collects the following before invoking the prompt.

### 2.1 Repository Information

| Item | Source | Default |
|------|--------|---------|
| `repo_root` | `git rev-parse --show-toplevel` | cwd |
| `repo_name` | `basename $repo_root` | "project" |
| `package_manager` | Detect `bun.lockb` / `pnpm-lock.yaml` / `yarn.lock` / `package-lock.json` in order | bun |
| `node_version` | `.nvmrc` / `package.json#engines.node` | "20" |
| `existing_ports` | Extract used ports from `dev`/`start` scripts | [] |
| `tailwind_version` | Existing dependency, if any | latest |
| `has_typescript` | Presence of `tsconfig.json` | true |
| `gitignored_paths` | Existing `.gitignore` | [] |

### 2.2 Skill Ecosystem Information

| Item | Source |
|------|--------|
| `apex_topology_version` | Header metadata of `_common/apex-dash/TOPOLOGY.md` |
| `events_schema_version` | Header metadata of `_common/apex-dash/EVENTS.md` |
| `spec_commit_hash` | `git -C ~/.claude/skills rev-parse HEAD` |

### 2.3 Port Selection

Try `5757, 5758, 5759, 5760, …` skipping anything in `existing_ports`. Confirm via `netstat -an | grep LISTEN`.

## 3. Output Manifest

The generator must write **all of the following** files.

```
<repo>/.agents/apex-dash/
├─ .spec-version                  # source commit hash
├─ .gitignore                     # node_modules / dist / .runtime.log
├─ package.json
├─ tsconfig.json
├─ tsconfig.node.json
├─ vite.config.ts
├─ tailwind.config.ts
├─ postcss.config.js
├─ README.md                      # local launch instructions
├─ server/
│  ├─ index.ts                    # Hono entry
│  ├─ tailer.ts                   # chokidar wrapper
│  ├─ state.ts                    # event → state reducer
│  └─ routes/
│     ├─ runs.ts
│     ├─ events.ts                # SSE
│     └─ replay.ts                # SSE (throttled)
├─ web/
│  ├─ index.html
│  └─ src/
│     ├─ main.tsx
│     ├─ App.tsx
│     ├─ store.ts
│     ├─ index.css                # Tailwind directives
│     ├─ hooks/
│     │  ├─ useSSE.ts
│     │  └─ useReplay.ts
│     ├─ panels/
│     │  ├─ Header.tsx
│     │  ├─ PhaseRail.tsx
│     │  ├─ Topology.tsx
│     │  ├─ ActiveAgents.tsx
│     │  ├─ RiskGateRadar.tsx
│     │  ├─ OrbitChart.tsx
│     │  ├─ Checkpoints.tsx
│     │  ├─ EngineSwitch.tsx
│     │  └─ EventStream.tsx
│     ├─ nodes/
│     │  ├─ PhaseGroupNode.tsx
│     │  ├─ AgentNode.tsx
│     │  └─ SubOrchestratorNode.tsx
│     ├─ edges/
│     │  ├─ FlowEdge.tsx
│     │  └─ EngineBoundaryEdge.tsx
│     ├─ lib/
│     │  ├─ topology.ts           # mirrors TOPOLOGY.md
│     │  ├─ animations.ts
│     │  ├─ colors.ts
│     │  └─ time.ts
│     └─ types/
│        ├─ events.ts             # zod schema mirroring EVENTS.md
│        └─ state.ts
└─ scripts/
   └─ smoke.ts                    # boot + SSE check
```

## 4. Required Dependencies (`package.json`)

```jsonc
{
  "name": "apex-dash",
  "private": true,
  "type": "module",
  "scripts": {
    "dev":   "concurrently -k \"bun run server/index.ts\" \"vite\"",
    "build": "vite build && bun build server/index.ts --target=bun --outfile=dist/server.js",
    "start": "bun run dist/server.js",
    "smoke": "bun run scripts/smoke.ts"
  },
  "dependencies": {
    "hono": "^4",
    "@hono/node-server": "^1",
    "chokidar": "^4",
    "zod": "^3"
  },
  "devDependencies": {
    "react": "^18",
    "react-dom": "^18",
    "@xyflow/react": "^12",
    "recharts": "^2",
    "framer-motion": "^11",
    "zustand": "^4",
    "@tanstack/react-virtual": "^3",
    "tailwindcss": "^4",
    "@tailwindcss/postcss": "^4",
    "vite": "^5",
    "@vitejs/plugin-react": "^4",
    "typescript": "^5",
    "@types/react": "^18",
    "@types/react-dom": "^18"
  }
}
```

## 5. Generator Prompt (passed to forge / builder)

A copy-pasteable template. Only the `<...>` placeholders are filled by the pre-scan results.

```
[ROLE] forge / rapid prototype builder

[GOAL]
Generate a complete `apex-dash` Web dashboard at <repo_root>/.agents/apex-dash/.
This dashboard visualises a /nexus apex run in real time with React + xyflow.

[INPUTS]
- spec dir: ~/.claude/skills/_common/apex-dash/
  - DESIGN.md     : architecture & file layout
  - EVENTS.md     : events.jsonl schema (producer/consumer share)
  - TOPOLOGY.md   : declarative graph data
  - UI.md         : layout / animation / theme / shortcuts
  - INTEGRATION.md: emit protocol & auto-spawn flow
- repo info:
  - repo_root        = <repo_root>
  - package_manager  = <bun|pnpm|npm|yarn>
  - node_version     = <e.g. 20>
  - chosen_port      = <5757+, free>
  - has_typescript   = <true|false>
- spec commit hash  = <hash>

[OUTPUT]
- write all files under <repo_root>/.agents/apex-dash/ exactly as listed in
  GENERATION.md §3 (manifest).
- write .spec-version = "<hash>"
- write .gitignore = node_modules/, dist/, .runtime.log
- ensure `bun run dev` starts the dashboard and the SPA renders an empty topology
  with all phases pending.

[CONSTRAINTS]
1. Do NOT modify anything outside <repo_root>/.agents/apex-dash/.
2. Do NOT add network calls beyond localhost.
3. Do NOT include authentication.
4. Bind server to 127.0.0.1:<chosen_port> only.
5. Mirror the schema in EVENTS.md exactly (zod schema in web/src/types/events.ts).
6. Mirror the topology in TOPOLOGY.md exactly (web/src/lib/topology.ts).
7. Implement node/edge animations per UI.md §3-§4.
8. Implement keyboard shortcuts per UI.md §7.
9. Implement replay mode per UI.md §8 (server route /api/replay/:run + client hook).
10. Pass `bun run smoke` (script defined in scripts/smoke.ts).

[ACCEPTANCE CRITERIA]
- `bun install` succeeds in the generated dir.
- `bun run dev` opens http://127.0.0.1:<chosen_port> and renders SPA.
- A test events.jsonl in .agents/apex/test-run/ drives the UI:
   - phase rail updates
   - active agents card appears
   - completed agents turn green
   - risk_gate radar renders
   - orbit_iter chart renders
   - replay slider scrubs through history
- No console errors, no React warnings, TypeScript strict passes.

[DELIVER]
- print a tree of created files
- print the launch command (`bun run dev`)
- print the smoke result
```

## 6. Per-Repo Customisation

| Item | Default | Override location |
|------|---------|-------------------|
| Port | auto from 5757 | `<dash_root>/config.json` → `"port": N` |
| Theme | dark | `"theme": "light"` |
| Density | normal | `"density": "compact"` |
| Logo | apex wordmark | Replace `<dash_root>/web/public/logo.svg` |
| Topology | apex default | Add `<dash_root>/web/src/lib/topology.local.ts` to override |
| Extra panel | none | Add `<dash_root>/web/src/panels/local/*.tsx` and register in `panels/index.ts` |

## 7. Verification (generator-side smoke)

`scripts/smoke.ts` spec:

1. Start the server in a separate process (port via CLI argument)
2. Within 5s, confirm `GET /api/runs` returns 200
3. Append 5 events to a test `.agents/apex/smoke-run/events.jsonl`
4. Connect SSE to `GET /api/events/smoke-run` and assert all 5 events arrive within 5s
5. Kill the server, exit 0

On failure: non-zero exit code with the failure point on stderr. The auto-spawn flow (`INTEGRATION.md §3`) catches this and falls back gracefully.

## 8. Regeneration and Compatibility

| Scenario | Behavior |
|----------|----------|
| Minor schema update in `_common/apex-dash/` | Existing dashboard continues to work (backward compatible) |
| Major update | Dashboard shows a "regenerate recommended" banner on launch; user passes `--regenerate` |
| Generation failure | Keep the previous version; record a `note` to `events.jsonl` (auto rollback) |
| Mid-generation interruption | Leave `<dash_root>/.generation.lock`; auto-clean on next start |

## 9. Privacy / Security Checklist (mandatory for generators)

- [ ] localhost binding only
- [ ] No authentication code
- [ ] events.jsonl writes confined to inside the repo
- [ ] node_modules listed in `.gitignore`
- [ ] No third-party telemetry / analytics
- [ ] Environment variables never injected into the web bundle (server-side only)

## 10. Sample Orchestration (Nexus side, pseudocode)

```python
# Pre-flight pseudocode for Nexus apex
def ensure_dashboard(repo_root):
    dash = f"{repo_root}/.agents/apex-dash"
    if exists(dash) and version_match(dash, current_spec_hash):
        return dash
    if exists(dash):
        warn("apex-dash spec mismatch — regenerate? [y/N]")
        if not confirmed: return dash  # use stale
    # generate
    spawn_agent("forge", prompt=GENERATION_PROMPT.format(
        repo_root=repo_root,
        package_manager=detect_package_manager(repo_root),
        node_version=detect_node_version(repo_root),
        chosen_port=pick_free_port(starting=5757),
        has_typescript=exists(f"{repo_root}/tsconfig.json"),
        hash=current_spec_hash(),
    ))
    if not run_smoke(dash):
        emit_error("dashboard smoke failed; continuing without dashboard")
        return None
    return dash
```

## 11. Related

- `DESIGN.md` — what to build
- `EVENTS.md` / `TOPOLOGY.md` / `UI.md` — how to build it (referenced by the prompt)
- `INTEGRATION.md` — auto-spawn and emit conventions
