# apex-dash — Architecture Design

This document defines the **architecture, data flow, tech stack, and file layout** required to implement apex-dash. Schema, UI layout, and integration details are split out into `EVENTS.md` / `UI.md` / `INTEGRATION.md`.

---

## 1. Goals

| ID | Goal | Measure |
|----|------|---------|
| G1 | apex progress is visibly "alive" on screen | Phase transition / agent start / agent end reflected in UI within 1s |
| G2 | Past runs can be replayed | Fully reconstructible from `events.jsonl` |
| G3 | No changes to existing skills | Apex-side change limited to one emit call per relevant point |
| G4 | Per-repo auto-generation | Fully automated by the prompt in `GENERATION.md` |
| G5 | 60 fps with 1,000 events/min | Virtual scroll + GPU compositing properties only |

## 2. Design Principles

1. **Single source of truth = `events.jsonl`**. State is the fold (reducer) of events.
2. **Append-only / Immutable**. `events.jsonl` is only appended; past lines are never rewritten.
3. **Stateless server**. The server tails the file and broadcasts via SSE; it holds no state. Restarting the server preserves consistency.
4. **Receiver only**. Apex calls one emit helper; the dashboard never calls back into apex.
5. **Fixed topology + animated state**. Graph layout is static; state is expressed through motion.
6. **Local first**. Listens on `localhost` only. No authentication. Sharing is done by handing over the recorded `events.jsonl`.

## 3. Overall Architecture

```
                ┌──────────────────────────────────────────┐
                │ Producer: Claude Code session            │
                │   Nexus / Vision / Orbit / specialists   │
                └──────────────┬───────────────────────────┘
                               │ PostToolUse / Stop hook
                               │   ↓
                ┌──────────────┴───────────────────────────┐
                │ Producer: Codex CLI subagents (Phase 6)  │
                │   builder / judge / radar / voyager …    │
                └──────────────┬───────────────────────────┘
                               │ orbit audit script
                               ▼
                ┌──────────────────────────────────────────┐
                │ Storage  (per repo, per run)             │
                │ <repo>/.agents/apex/<run-id>/            │
                │   ├─ events.jsonl       (append-only)   │
                │   ├─ state.json         (snapshot)       │
                │   └─ artifacts/         (symlinks)       │
                └──────────────┬───────────────────────────┘
                               │ chokidar tail
                               ▼
                ┌──────────────────────────────────────────┐
                │ Server   Bun + Hono                      │
                │   GET /                → SPA             │
                │   GET /api/runs                          │
                │   GET /api/state/:run                    │
                │   GET /api/events/:run  (SSE)            │
                │   GET /api/replay/:run  (SSE, throttled) │
                └──────────────┬───────────────────────────┘
                               │ Server-Sent Events
                               ▼
                ┌──────────────────────────────────────────┐
                │ Client   React + xyflow + Recharts       │
                │   - zustand store (event-sourced)        │
                │   - panels: Topology / Phase rail / …    │
                │   - animations: Framer Motion / CSS      │
                └──────────────────────────────────────────┘
```

## 4. Data Flow (in time order)

1. An apex agent performs a tool call or transitions a phase
2. The Claude Code `PostToolUse` hook calls the emit helper (see `INTEGRATION.md`)
3. The emit helper appends one line to `events.jsonl` and optionally regenerates `state.json`
4. The server watches `events.jsonl` via chokidar
5. On change, it reads the new lines and pushes them to every SSE subscriber
6. The client receives via `EventSource`, folds each event through the zustand reducer
7. React re-renders only the panels whose store slices changed
8. xyflow updates affected nodes via `updateNodeData` (no relayout)

## 5. Components

### 5.1 Producer (apex side)
- Sole interface is `_common/scripts/apex-emit.sh` (see `INTEGRATION.md §2 Emit protocol`)
- Takes an event kind plus arbitrary `key=value` fields
- Failures are silently ignored — apex execution must not be blocked

### 5.2 Storage
- Path convention: `<repo>/.agents/apex/<run-id>/`
- run-id format: `apex-YYYYMMDD-HHMMSS-<short-hash>`
- `GENERATION.md` requires `.agents/apex/` to be added to `.gitignore`

### 5.3 Server
- Runtime: **Bun** (fallback: Node 20+)
- Framework: **Hono**
- Static serving + SSE only. No database, cache, or auth
- Default port: 5757. On collision, auto-increments to 5758, 5759, … (see `GENERATION.md` customization)
- Launch: `bun run server/index.ts --repo=<path> --port=<n> --open`

### 5.4 Client
- React 18 + TypeScript (strict)
- Bundler: **Vite** (DX-first, stable HMR)
- State: **zustand** (slice-based; SSE ingestion via middleware)
- Graph: **@xyflow/react v12**
- Charts: **Recharts**
- Animation: **Framer Motion** + CSS keyframes
- Style: **Tailwind CSS v4**
- Virtual scroll: **@tanstack/react-virtual**

## 6. Tech Stack Rationale

| Layer | Choice | Rationale / Alternative |
|-------|--------|-------------------------|
| Runtime | Bun | Already standard across this skill ecosystem. Alt: Node 20+ |
| Server | Hono | Shortest path to SSE. Alt: Fastify |
| Bundler | Vite | Stable HMR, plays well with xyflow. Alt: Bun bundler |
| Graph | @xyflow/react v12 | Custom nodes/edges, minimap, controls built in; MIT |
| Charts | Recharts | Both RadarChart and LineChart. Alt: Visx |
| Animation | Framer Motion + CSS | Node transitions and shake/pulse. Alt: GSAP |
| State | zustand | Localised re-renders vs. Context, lighter than Redux |
| File watch | chokidar | Robust to append loss. Alt: node:fs.watch |
| Style | Tailwind v4 | Instant state-color recognition. Alt: vanilla CSS |

## 7. File Layout (post-generation)

```
<repo>/.agents/apex-dash/
  package.json
  tsconfig.json
  vite.config.ts
  .spec-version              # source commit hash
  server/
    index.ts                 # Hono server entry
    tailer.ts                # chokidar watcher
    state.ts                 # event → state reducer (server side)
    routes/
      runs.ts
      events.ts
      replay.ts
  web/
    index.html
    src/
      main.tsx
      App.tsx
      store.ts
      hooks/
        useSSE.ts
        useReplay.ts
      panels/
        Header.tsx
        PhaseRail.tsx
        Topology.tsx          # the main panel
        ActiveAgents.tsx
        RiskGateRadar.tsx
        OrbitChart.tsx
        Checkpoints.tsx
        EngineSwitch.tsx
        EventStream.tsx
      nodes/
        PhaseGroupNode.tsx
        AgentNode.tsx
        SubOrchestratorNode.tsx
      edges/
        FlowEdge.tsx
        EngineBoundaryEdge.tsx
      lib/
        topology.ts          # mirrors TOPOLOGY.md
        animations.ts
        colors.ts
        time.ts
      types/
        events.ts            # mirrors EVENTS.md
        state.ts
```

LOC budget: roughly 1,500–2,000 lines total (excluding tests).

## 8. Performance Targets

| Metric | Target |
|--------|--------|
| Event ingest → UI reflection | < 1 s |
| Event throughput | 1,000 events/min sustained, 5,000 events/min burst |
| Topology canvas FPS | 60 fps (30 nodes, 5 active) |
| EventStream rendering | Smooth at 10,000 rows (virtualised) |
| Memory | < 500 MB over an 8-hour run |
| Cold start to SPA paint | < 3 s |

## 9. Security / Privacy

- **Bind to localhost only**. Never bind beyond `127.0.0.1`
- No authentication (local tool)
- Snippets in `events.jsonl` are short-form (≤280 chars). No secrets are persisted
- Artifacts are referenced via symlink only, never copied
- `GENERATION.md` mandates `.agents/apex/` in `.gitignore`

## 10. Extensibility

- The events schema and topology data are pluggable → reusable for other Nexus recipes
- Panels are pluggable: register additional panels in `web/src/panels/index.ts`
- Theming: colors and logos are isolated to a single theme file for branding

## 11. Non-Goals

- Multi-user viewing / authentication / RBAC
- Cloud sync / persistence
- Long-term metrics retention (e.g. Prometheus integration)
- Production SLO monitoring (owned by `beacon`)
- Becoming a registered skill (this is a per-apex local tool)

## 12. Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Server tailer locking during append | Open in `r` mode; appender uses POSIX append-only semantics |
| Concurrent runs confuse the UI | Run-id is in the path; UI exposes a run picker |
| Port collision | Auto-increment + listening verification on startup |
| UI freeze under event burst | Virtual scroll + interval-based batching |
| Stale generation prompt | `.spec-version` records source hash; mismatch triggers regenerate prompt |

## 13. References

- `EVENTS.md` — every event kind + JSON Schema
- `TOPOLOGY.md` — apex topology data
- `UI.md` — layout / animation spec
- `INTEGRATION.md` — emit protocol / Nexus apex hook
- `GENERATION.md` — generator prompt / file manifest
