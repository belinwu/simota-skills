# Constraint Modes

Reference for Dawn's `constraint` recipe. Bias the daily idea around an explicit engineering constraint — single-file, no-deps, offline-only, single-binary, 100-LOC, single-language — so the proposal lands with a particular *aesthetic*. Constraints unlock creativity by removing options, not adding them.

The constraint is the headline. The idea must still satisfy at least one of utility / learning value / playful delight, but its identity is shaped by the constraint.

---

## 1. Constraint Catalog

Pick **one** primary constraint per invocation. Combining two is allowed only when they reinforce each other (e.g., `single-file` + `no-deps`).

| Constraint | Definition | Why it shapes the idea |
|------------|-----------|------------------------|
| `single-file` | All code lives in one file (HTML+CSS+JS, single `.py`, single `.rs`, etc.) | Forces inlining, reveals what's actually essential |
| `no-deps` | Zero runtime dependencies (stdlib only) | Forces understanding the platform; portable forever |
| `offline-only` | Runs with no network access; no telemetry, no CDN | Privacy-first, local-first, durable |
| `single-binary` | One executable, no installer, no runtime | Distribution simplicity; instant try |
| `100-loc` | Under 100 lines of code (excl. comments) | Tight scope; sharpens design |
| `single-language` | One language end-to-end (incl. build, deploy) | Reduces context switching; reveals language reach |
| `keyboard-only` | UI navigable without mouse / touch | DX flex; reveals real workflow |
| `no-config` | Zero config file; sensible defaults only | UX flex; opinionated by design |
| `read-only` | Tool never writes to disk except its own log | Safety guarantee; auditable |
| `single-window` | UI is one window, no modals or tabs | Forces hierarchy; rewards minimalism |
| `cli-first` | No web UI; pure terminal experience | Composability with pipes |
| `human-readable-storage` | Storage is plain text / JSON / TOML, no binary DB | Forkable, diffable, future-proof |

---

## 2. Constraint × Stack Compatibility

Some stacks express certain constraints naturally. Bias the pick when stack and constraint match.

| Constraint | Strong fit | Weak fit |
|------------|------------|----------|
| `single-file` | HTML, Python, Rust + `cargo-script`, Bun | Java, .NET |
| `no-deps` | Go, Rust, C, Zig, Deno (with `--no-remote`) | Node, Python (sometimes) |
| `single-binary` | Go, Rust, Zig, Bun (`bun build --compile`) | Python, Ruby |
| `100-loc` | APL, Roc, Clojure, Python | Java, C++ |
| `offline-only` | Tauri, native CLIs, PWA with cache-first | SaaS frontends |
| `keyboard-only` | TUI (ratatui, ink, blessed), neovim plugins | Touch-first apps |

---

## 3. Selection Algorithm

```
1. Pick a constraint not used in the last 7 entries (memory/dawn_log.md mood column)
2. Choose a stack from the strong-fit column for that constraint
3. Pick a domain (file processing / data viz / personal analytics / dev tool / game) that
   reinforces the constraint's natural strength
4. Run the cliché check; reject if the result is "TODO app but in 100 LOC"
```

---

## 4. Constraint-Driven Idea Seeds

Domain seeds where the constraint is the load-bearing element of the proposal:

| Constraint | Seed |
|------------|------|
| `single-file` | A self-contained HTML file that renders your CSV data with charts on file:// |
| `no-deps` | A Go program that compresses a directory using only `archive/tar` and `compress/gzip` |
| `offline-only` | A Tauri app for journaling that never has a network permission |
| `single-binary` | A 4MB Rust binary that serves your photos as a local web gallery |
| `100-loc` | A Python script that parses iMessage SQLite and prints a yearly conversation graph |
| `single-language` | A full-stack Bun app where build, server, client, and tests are all one TypeScript |
| `keyboard-only` | A TUI git branch picker with fuzzy search and preview |
| `no-config` | A CLI that infers project type and runs the right test command, no flags |
| `read-only` | A directory diff viewer that opens read-only file handles only |
| `human-readable-storage` | A note app whose data is one Markdown file per note, no SQLite |

---

## 5. Constraint Verification

Section 4 (MVP spec) **must** prove the constraint is real, not aspirational. Include one of:

- A `wc -l` style check (for `100-loc`)
- A dependency tree screenshot (for `no-deps`)
- A binary size measurement (for `single-binary`)
- A `tcpdump` / network panel screenshot proving no traffic (for `offline-only`)
- A keyboard-shortcut map covering all UI (for `keyboard-only`)

If you cannot describe the verification, the constraint is decoration, not engineering.

---

## 6. Output Adjustments for `constraint` Recipe

- Section 1: include the constraint as a tagline. Example: `tail-rs — single-binary, no-deps`
- Section 3: lead with "なぜこの制約か" — the aesthetic and engineering payoff
- Section 4: include the verification check (see § 5)
- Section 5: include one step explicitly named "constraint check" (e.g., "ステップ7: `cloc src/ | grep -E '^Total'` で 100 行以内を確認")
- Section 7: extensions must respect the constraint or note explicitly when they break it
- Section 8 prompt: hard-code the constraint as a non-negotiable requirement at the top

---

## 7. Anti-Patterns

- **Constraint theatre**: using `100-loc` but with 3 helper files. The constraint applies to the whole project.
- **Bait-and-switch**: starting `no-deps` and pulling in `requests` "just for HTTP". The constraint is the design.
- **Toy ceiling**: choosing a constraint so tight the idea cannot satisfy any of utility / learning / delight. Loosen one notch.
- **Aesthetic only**: the constraint sounds cool but doesn't shape the design. Pick a different constraint.

---

## 8. Logging Note

For `constraint` recipe, log the constraint in the `mood` column (e.g., `single-file`, `no-deps`, `offline-only`). This lets the rotation check avoid hitting the same constraint twice in a week.
