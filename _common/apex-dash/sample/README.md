# apex-dash · sample (MVP)

A minimum-viable, runnable reference implementation of the apex-dash spec at `_common/apex-dash/`.
This sample exists so that:

- The schema (`EVENTS.md`), topology (`TOPOLOGY.md`), and UI behaviour (`UI.md`) can be verified end-to-end
- `forge` / `builder` can use it as a golden reference when generating per-repo dashboards

## Stack

| Layer | Choice |
|-------|--------|
| Server | Bun + Hono (SSE) |
| Client | React 18 + @xyflow/react v12 |
| Bundler | Vite 5 |
| State | zustand 5 |
| Watcher | chokidar 4 |

No Tailwind, no Framer Motion — animations are CSS keyframes. No replay UI in this MVP.

## Layout

```
sample/
├─ package.json
├─ tsconfig.json
├─ vite.config.ts
├─ index.html
├─ events/
│  └─ apex-20260430-120000-a3f/
│     └─ events.jsonl     ← seed events for the demo run
├─ server/
│  └─ index.ts            ← Hono server: /api/runs, /api/events/:run (SSE)
└─ src/
   ├─ main.tsx
   ├─ App.tsx
   ├─ store.ts            ← zustand + SSE ingestion
   ├─ reducer.ts          ← event → state fold
   ├─ types.ts            ← EVENTS.md mirror (TS-only)
   ├─ topology.ts         ← TOPOLOGY.md subset
   ├─ styles.css
   ├─ panels/
   │  ├─ Header.tsx
   │  ├─ PhaseRail.tsx
   │  ├─ Topology.tsx
   │  └─ EventStream.tsx
   └─ nodes/
      └─ AgentNode.tsx
```

## Run

```sh
cd _common/apex-dash/sample
bun install
bun run dev
# open http://127.0.0.1:5173
```

Two processes start:

- **server** on `127.0.0.1:5757` — tails `events/<run-id>/events.jsonl`
- **client** on `127.0.0.1:5173` — Vite dev server, proxies `/api/*` to the server

## Demo data

`events/apex-20260430-120000-a3f/events.jsonl` ships with a complete run (P1 → Ship) that exercises every event kind. To replay it from scratch:

```sh
# truncate and replay (server tails the change)
:> events/apex-20260430-120000-a3f/events.jsonl
bun run scripts/replay.ts   # (optional: not included in MVP — use `cat | tee` or a manual loop)
```

For quick visual verification, just refresh the browser; the SSE handler streams the existing file from the start.

## Endpoints

| Route | Purpose |
|-------|---------|
| `GET /api/runs` | List run-ids in `events/` |
| `GET /api/events/:run` | SSE stream of events.jsonl (existing + tail) |

## Postmortem

When a run finishes (`run_end` event observed), the **📄 postmortem** button in the header is enabled. It hits `GET /api/postmortem/:run` which:

- folds events through the same reducer the UI uses
- computes phase / agent durations, bottleneck, orbit metrics, engine boundaries
- writes `events/<run-id>/postmortem.md` (atomic) and returns the markdown for browser viewing

You can also generate one from the CLI:

```sh
bun run scripts/postmortem.ts                       # newest run
bun run scripts/postmortem.ts apex-20260430-120000-a3f
```

A pre-generated `events/apex-20260430-120000-a3f/postmortem.md` is shipped so the format is visible without running anything.

Spec: `_common/apex-dash/POSTMORTEM.md`.

## Limits of this MVP

- No replay slider, no theme toggle, no keyboard shortcuts
- No run-picker dropdown (uses newest run automatically)
- Topology omits conditional agents not in the seed run (gateway / polyglot / pixel, etc.)
- No tests — manual browser run verifies it

See the parent specs for the full surface to implement when promoting this MVP to a production dashboard.
