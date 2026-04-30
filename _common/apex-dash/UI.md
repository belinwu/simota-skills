# apex-dash — UI / UX Specification

Defines the screen layout, panel responsibilities, node and edge animations, theme, and replay-mode controls.

---

## 1. Layout Grid

### 1.1 Target Resolutions

| Tier | Min | Default | Max |
|------|-----|---------|-----|
| Width | 1280 | 1920 | 2560 |
| Height | 720 | 1080 | 1440 |

The lower bound is 1280×720; experience is tuned for 1920×1080. Three columns + two rows + header + bottom log.

### 1.2 Top-Level Composition (1920×1080)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Header   60px                                                               │
├──────────────────────────────────────────────────────────────────────────────┤
│  Phase rail   48px                                                           │
├──────────────────────────────────────────────────────────────┬───────────────┤
│                                                              │               │
│                                                              │  Right rail   │
│  Topology canvas       (primary)                             │  360px        │
│  flex-1 / 720px+                                             │               │
│                                                              │  ─ Active     │
│                                                              │  ─ Risk Gate  │
│                                                              │  ─ Checkpts   │
│                                                              │  ─ Engine     │
├──────────────────────────────────────────────────────────────┤               │
│  Mid panel  240px                                            │               │
│   ┌─Orbit chart──────────────────┬─Phase summary────────┐    │               │
│   │ line: convergence + cost      │ scope / mode etc.   │    │               │
│   └───────────────────────────────┴──────────────────────┘    │               │
├──────────────────────────────────────────────────────────────┴───────────────┤
│  Event stream  240px (collapsible to 80px)                                   │
└──────────────────────────────────────────────────────────────────────────────┘
```

## 2. Panel Specs

### 2.1 Header (60px)

```
[ apex-20260430-120000 ]  goal: passkey login   AUTORUN_FULL   ⏱ 30:20  [Live ▶ | Replay ↻]   [⚙]
```

| Element | Behavior |
|---------|----------|
| Run id | Click opens a run picker dropdown |
| Goal | Live goal text; tooltip shows rationale |
| Mode | Badge; `AUTORUN_FULL` is highlighted |
| Elapsed | mm:ss / hh:mm:ss; updates every second |
| Live/Replay toggle | In replay mode, exposes the speed slider |
| Settings | Theme and density toggles |

### 2.2 Phase Rail (48px)

A horizontal indicator equal-spacing P0 through Ship.

- Status colors: pending = grey / running = blue pulse / done = green / failed = red / skipped = dotted
- Current phase rendered **bold + underline + ▮ progress bar**
- Click smooth-pans + zooms the Topology canvas to that phase

### 2.3 Topology Canvas (primary)

xyflow-rendered hub-and-spoke graph.

- Minimap: bottom right, always visible
- Controls: bottom left (zoom / fit / lock)
- Background: dot pattern, light slate
- Camera follow: on `phase_enter`, smooth pan to the phase group / 800ms / ease-in-out
- Off-screen activations show a peek pointer hint ("⇨ atlas active")

Node and edge animations are specified in §3 / §4.

### 2.4 Right Rail (360px)

#### 2.4.1 Active Agents
A stack of cards, one per active agent.

```
┌─────────────────────────────┐
│ ⏵ atlas      P5 Tech 03:12  │
│   tool: Read  ▮▮▮▯▯ 60%     │
│   last: forge.config.ts     │
└─────────────────────────────┘
```

Color: a fixed per-agent color matched to topology. Elapsed time updates every second.

#### 2.4.2 Risk Gate (radar chart)

Axes: omen / ripple / echo. Values: 0–1 (pass=1, conditional=0.5, fail=0, pending=transparent). `Conditional-Go` tints yellow; `No-Go` tints red.

#### 2.4.3 Checkpoints

A vertical timeline. While `checkpoint_wait` is active, a countdown timer is shown (only for `mode=AUTORUN_FULL_60s`).

#### 2.4.4 Engine Switch

A large badge for the current engine (`claude_code` / `codex_cli`); switch history below in smaller type.

### 2.5 Mid Panel (240px)

#### 2.5.1 Orbit Chart
Recharts LineChart. X = `iter`. Y = `convergence` (0–1) and `cost_per_task` (dual axis). Background tints yellow when `circuit=yellow`, red when `red`.

#### 2.5.2 Phase Summary
Scope, mode, conditional-agent activations, and a heuristic remaining-time estimate.

### 2.6 Event Stream (240px, collapsible)

A virtualised list (`@tanstack/react-virtual`).

- Row format: `[hh:mm:ss] [kind] [agent] [meta digest]`
- Color: per-kind left band (agent_start = blue / agent_end = green / error = red / checkpoint = yellow)
- Filters: by kind (checkboxes), by agent, errors only
- Pin: important rows can be pinned to the top
- Click: highlights and pans the corresponding node on the canvas

## 3. Node Animation Spec

| status | Visual | Implementation hint |
|--------|--------|---------------------|
| `pending` | opacity .4 / dotted outline / saturation 0 | CSS class `.pending` |
| `running` | Glow (`box-shadow: 0 0 12px var(--accent)`); breathe scale 1.0 ↔ 1.04 over 1.6s ease-in-out infinite | CSS keyframes `pulse` |
| `running + tool_use` | Brief scale spike to 1.06 over 200ms | Reuse Framer Motion `whileTap` |
| `waiting` | Yellow pulse + ⏸ icon at center | keyframes `pulseYellow` |
| `done` | Green check at top-left, 70% saturation, no shadow | static |
| `error` | Red, light shake (translateX ±2 px / 60ms / 4 cycles) | Framer Motion variant |
| `skipped` | Diagonal stripes, opacity .3 | repeating-linear-gradient |

Color tokens (`colors.ts`):
- `accent` (running): `#3b82f6` (blue-500)
- `success` (done): `#10b981` (emerald-500)
- `warning` (waiting): `#f59e0b` (amber-500)
- `danger` (error): `#ef4444` (rose-500)
- `muted` (pending/skipped): `#64748b` (slate-500)

## 4. Edge Animation Spec

| Edge type | Idle | Active (data flow) |
|-----------|------|--------------------|
| `flow` | Thin grey line (`stroke-width: 1.2px`) | 3–5 particles glide source → target on a 4s loop |
| `escalation` | Hidden by default | On No-Go: red reverse particles for 1.2s |
| `engineBoundary` | Vertical dashed bar with label "claude_code ⇒ codex_cli" | On crossing: vertical falling particles |

Particle implementation: SVG `<animateMotion>` or xyflow `MarkerType.ArrowClosed` plus a custom edge component.

## 5. Camera Behavior

| Trigger | Action | Duration |
|---------|--------|----------|
| `phase_enter` | Fit to the phase group | 800ms ease-in-out |
| "Fit view" button | Show full canvas | 600ms |
| "Follow active" toggle | Track current active agent (centroid if multiple) | Live |
| Event row click | Pan to the node and flash highlight | 600ms |

## 6. Theming

Both light and dark are supported. Default is dark (long-session friendly).

```
--bg-base:     #0b1220
--bg-elev:     #111a2e
--text:        #e2e8f0
--text-muted:  #94a3b8
--border:      #1e293b
--accent:      #3b82f6
--success:     #10b981
--warning:     #f59e0b
--danger:      #ef4444
--phase-stripe: rgba(59,130,246,0.06)   # phase group background
--codex-tint:   rgba(167,139,250,0.08)  # P6 background (post engine boundary)
```

In light theme, replace `bg-*` with `#f8fafc` / `#ffffff` and `text` with slate-900 family.

Typography: Inter for general UI, JetBrains Mono for the event stream and numerals.

## 7. Interactions

| Shortcut | Function |
|----------|----------|
| `f` | Fit view |
| `g` | Toggle follow-active |
| `r` | Toggle replay panel |
| `j` / `k` | Event stream prev/next |
| `1`–`8` | Pan phase rail to that phase |
| `e` | Collapse / expand event stream |
| `?` | Shortcut overview modal |

## 8. Replay Mode

Toggle "Live ▶" to "Replay ↻" in the header to expose a slider and speed control.

```
[ ◀◀ ] [ ▶ / ⏸ ] [ ▶▶ ]   ━━━●━━━━━━━━━━   00:12:42 / 00:30:20   speed [1× ▾]
```

| Control | Behavior |
|---------|----------|
| Play/Pause | Re-emit events in time order; pace via `setTimeout` over `ts` deltas |
| Speed | 0.5× / 1× / 2× / 4× / 10× |
| Seek | Slider drag folds events up to that `seq`, then resumes |
| Step | Single-event manual advance (`◀◀` / `▶▶`) |

Implementation: server route `/api/replay/:run` re-streams via SSE with adjusted pacing; the client uses the same pipeline as Live.

## 9. Accessibility

- Every interaction has a keyboard equivalent
- State conveys via animation **plus** icon + label (color-vision considerations)
- Honour `prefers-reduced-motion`: degrade animations to fade only
- ARIA live region announces critical events (`risk_gate`, `error`, `checkpoint`)

## 10. Responsiveness

| Width | Behavior |
|-------|----------|
| ≥1600 | All panels visible |
| 1280–1599 | Right rail toggleable; collapsed by default |
| <1280 | Mid panel and Event stream tabbed |

## 11. Performance Budget

| Metric | Budget |
|--------|--------|
| Topology canvas FPS | ≥58 (5 active nodes) |
| Event stream row insert | <50ms |
| State reflection (event → DOM) | <500ms p95 |
| Initial load | <3s cold, <1s warm |
| Memory | <500 MB over 8h run |

## 12. Related

- `TOPOLOGY.md` — origin data for node positions
- `EVENTS.md` — which event drives which animation
- `DESIGN.md §5.4` — chosen libraries
