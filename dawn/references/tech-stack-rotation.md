# Tech Stack Rotation

Reference for Dawn's `stack` recipe. Bias the daily idea around an explicit tech stack axis so the proposal exercises a specific learning surface — language, runtime, framework, or paradigm — that the user has not been using lately.

The goal is not to teach the stack but to give a meaningful reason to *use* it. The idea must still earn its place via utility / learning value / playful delight.

<!-- Last updated: 2026-05-23. Sources:
  - Bun 1.2+: https://bun.sh/blog/bun-v1.2 (official release notes)
  - Deno 2.x: https://deno.com/blog/v2.0 (official release blog)
  - Tauri 2.0: https://v2.tauri.app/blog/tauri-20/ (official stable release)
  - MCP: https://modelcontextprotocol.io/quickstart/server (official quickstart)
  - WASM 3.0 Component Model: https://platform.uno/blog/the-state-of-webassembly-2025-2026/
-->

---

## 1. Stack Axis Catalog

Rotate across these axes. Each invocation picks one cell — never the same as the last 7 entries in `memory/dawn_log.md`.

### Language Layer

| Stack | Strength | Idea seeds |
|-------|----------|-----------|
| Rust | Single binary, perf, memory safety | CLI parsers, log filters, mini interpreters, file watchers |
| Zig | Comptime, minimal runtime | Build-step tools, embedded toy compilers |
| Go | Concurrency, deploy simplicity | TUI dashboards, mini proxies, sync daemons |
| TypeScript + Bun 1.2+ | Fast startup, `bun build --compile` single binary, native fetch | Single-file APIs, dev-tool prototypes, compiled CLI tools |
| Deno 2.x | Node/npm compatibility, `deno compile`, built-in formatter/linter | Portable CLIs, secure script hosts, self-contained executables |
| Python + uv | Notebook → script velocity | Scrapers, data sketches, ad-hoc analysis |
| Elixir | Actor model, observability | Tiny pubsub servers, IoT message buses |
| Swift (CLI) | Apple ecosystem hooks | macOS automation, menubar utilities |

### Runtime / Platform Layer

| Stack | Strength | Idea seeds |
|-------|----------|-----------|
| WebGPU | GPU compute in browser | Real-time viz, particle simulations |
| WASM 3.0 (component model) | Sandboxed plugins, WIT interfaces, WasmGC — W3C standard Sep 2025 | Plugin hosts, untrusted-code runners, polyglot micro-tools |
| Tauri 2.x | Native window (incl. iOS/Android), small binary (~10 MB), Rust backend | Local-first desktop/mobile tools, menubar utilities |
| SQLite | Zero-config, embedded | Personal log apps, append-only stores |
| DuckDB | OLAP on a laptop | Local analytics, file-format converters |
| Cloudflare Workers | Edge compute | Cron jobs, webhook routers |
| MCP server (FastMCP / Python SDK) | Expose personal tools to Claude/AI agents via standard protocol | Local data bridges, private API wrappers, dev-tool MCP servers |

### Paradigm Layer

| Paradigm | Strength | Idea seeds |
|----------|----------|-----------|
| Event sourcing | Replayable history | Personal activity replays |
| CRDTs | Offline-first, multi-device | Collaborative scratchpads |
| Effect systems | Explicit IO | Tiny scripting DSLs |
| Functional reactive | Time-varying values | Live dashboards, signal viz |
| Constraint solving | Declarative search | Schedulers, layout solvers |

---

## 2. Selection Algorithm

```
1. Read memory/dawn_log.md last 7 entries → extract tech_layer column
2. Drop any layer that appears ≥ 1 time in the last 7
3. From remaining layers, weight toward "underused for 14+ days"
4. If user gave a hint ("Rust please"), respect it but still rotate domain
5. Pair the chosen stack with a domain (CLI / Web / data / OS / game) that
   doesn't repeat the last 3 entries
```

If the user explicitly names a stack, treat that as a hard constraint and rotate only the domain axis.

---

## 3. Stack-First Framing Pattern

When the stack is the seed, structure the 8-section brief so the stack's *unique strength* is the load-bearing reason the idea works at all. Avoid "you could also do this in any other language" framing.

| Section | Stack-aware emphasis |
|---------|----------------------|
| 3. なぜ面白いか | Include "why this stack specifically" — single binary / GPU / actor model / etc. |
| 4. MVPの仕様 | Show one code-shape that only this stack expresses cleanly |
| 5. 実装ステップ | Pin one step to a stack idiom (cargo workspace / bun build --compile / deno deploy) |
| 6. 技術スタック | Lead with the chosen stack and its standard tooling — no generic alternatives |
| 8. プロンプト | Hard-code the stack into the agent prompt; do not leave it open |

---

## 4. Anti-Patterns

- **Stack tourism**: choosing a trendy stack with no real strength match. If you can't name *why this stack*, switch.
- **Library showcase**: an idea whose only purpose is to demo a library. The stack must serve the user, not the other way around.
- **Polyglot creep**: pulling in 3+ stacks in section 6. One primary, at most one supporting.
- **Hello-world disguised**: scope creep to "and then add auth, db, deploy". The stack's strength should land within the 1-3 day MVP.

---

## 5. Stack × Domain Pairing Examples

These are seed combinations the candidate-generation step (DIVERGE) can sample from. Always run the diversity check against `memory/dawn_log.md` before committing.

| Stack | Domain | Seed shape |
|-------|--------|-----------|
| Rust + CLI | Local data | A `git log` style viewer for your shell history |
| Bun + Web | Tooling | Single-file localhost dashboard for `package.json` scripts |
| WebGPU + Viz | Personal data | GPU-accelerated heatmap of git activity |
| DuckDB + CLI | Analytics | Query your iMessage / Slack export with SQL |
| Tauri + Local-first | Productivity | Menubar timer that learns from your calendar |
| Go + TUI | DevOps | Live `kubectl get` style watcher for a non-k8s service |
| WASM 3.0 + Browser | Plugin hosting | Run untrusted user scripts inside a sandboxed page (WIT interface) |
| Elixir + Realtime | Hobby | A presence server for a 4-person side project |
| FastMCP + Python | AI agent bridge | An MCP server that exposes your local notes / calendar / shell history to Claude |
| Bun 1.2+ + CLI | Tooling | Single compiled binary that reads `package.json` and explains build scripts in plain English |

---

## 6. Output Adjustments for `stack` Recipe

- Section 1: include the stack token in the codename when natural (e.g., `rust-tail`, `bun-dash`).
- Section 6: 6-8 concrete libraries from that stack's standard ecosystem; cite real names (`clap`, `ratatui`, `hono`, `drizzle`, `wgpu`, `tokio`).
- Section 8 prompt: pin language version, package manager, and entry-point file explicitly so the coding agent does not drift to a generic stack.

---

## 7. Logging Note

When logging in `memory/dawn_log.md`, the `tech-layer` column should record the *primary* stack axis used (e.g., `Rust+CLI`, `WebGPU+Viz`). This keeps the rotation check working on subsequent invocations.
