# Shareability Design

Reference for Dawn's `viral` recipe. Bias the daily idea so its very first run produces a shareable artifact — a screenshot, a short GIF, a single-line tweet, a repo README graphic, a blog hook. The aesthetic axis is "tomorrow you'll want to show someone."

This is **not** marketing-think. The shareable artifact is just an honest screenshot of the build doing something delightful. If the artifact is fake, the idea fails.

---

## 1. The 5-Second Wow Rule

When someone scrolls past a screenshot of your project on a feed, they have ~5 seconds. The idea must produce something that makes a curious engineer pause within those 5 seconds.

Concretely, the artifact must satisfy at least one of:

- **Visual surprise** — an unexpected layout, color, or motion
- **Cognitive surprise** — a fact, number, or relationship the viewer didn't know
- **Aesthetic density** — a satisfying amount of information in a small frame
- **Identity flag** — clearly *this engineer's* taste (handle / colors / domain)

If the artifact is "another Tailwind landing page" or "another `ls` output", it does not pass.

---

## 2. Artifact Types and Fit

| Artifact | Best for | Failure mode |
|----------|----------|--------------|
| Static screenshot | Dense data / typography / layout | Looks like every other dashboard |
| Animated GIF (≤ 6s) | Motion / interaction / state change | Too long; viewer leaves |
| Short video clip (≤ 30s) | Workflow demos / before-after | Production cost too high for 1-3 day MVP |
| Terminal cast | CLI tools / TUI workflows | Tiny font; unreadable on mobile |
| Single number | Personal stats / weird metrics | Without context, just noise |
| Repo README graphic | Open-source distribution | README photo without a corresponding live demo |
| Tweet-line | Quote-style insight | Trying to be funny without earning it |

Pick the artifact type **before** scoping the MVP. The MVP must produce *that exact artifact* on first run.

---

## 3. Shareability Patterns

### A. Personal data made strange

Take data the user already has (calendar, terminal history, screen time, music history, GitHub commits) and render it in a form they have never seen.

| Seed | Artifact |
|------|----------|
| Year of git commits as a heatmap with mood colors | One PNG |
| Terminal history grouped by intent | A pie chart with 5 buckets |
| All files you opened today as a tree | An ASCII tree |
| Years of iMessage tone over time | A line chart with annotations |

### B. Constraint-as-aesthetic

A constraint (single-file, no-deps, sub-1KB) is itself the share-line. The artifact is the constraint *evidence* (binary size, line count) plus the working demo.

### C. Inversion

Take a tool everyone knows and invert one axis (read-only vs read-write, observable vs imperative, static vs animated, server-side vs client-side, public vs private).

### D. Number that should not exist

A measurement nobody has done before, on a question only this engineer thought to ask. The number is the share.

| Seed | Number |
|------|--------|
| How many times do I open and close the same file in a day? | 47 |
| What's the average lifespan of a `// TODO` comment in my repos? | 38 days |
| How many distinct chord progressions did I listen to this year? | 1,283 |

### E. Aesthetic-first

Build something where the *visual* is the entire point — generative art, type specimens, color systems, ASCII portraits.

---

## 4. Demo Asset Spec (Section 4 Adjustment)

For the `viral` recipe, section 4 of the brief **must** include:

- The exact artifact format (PNG / GIF / line / clip / cast)
- The dimensions or duration (e.g., 1200×630 PNG, 6s GIF, ≤ 280 chars)
- The first-run script that produces it (`npm run demo`, `python -m demo`, `make share`)
- A textual description of what's in the frame ("a 12×52 grid of squares colored by commit count, with month labels along the top")

Without these, the artifact is wishful thinking.

---

## 5. Selection Algorithm

```
1. Pick a shareability pattern (§ 3) not used in the last 7 entries (mood column)
2. Pick the artifact type (§ 2) and check it's feasible inside 1-3 days
3. Pick a domain — preferably user-data or aesthetic, not feature-tool
4. Cliché-check: ban "wrapped" clones, generic dashboards, contribution-graph copies
```

---

## 6. Output Adjustments for `viral` Recipe

- Section 1: codename should hint at the artifact (e.g., `chord-year`, `idle-tree`, `git-heat`)
- Section 3: at least one bullet describes the *moment of share*
- Section 4: include artifact spec (§ 4) and a sketch of the frame
- Section 5: include "ステップ N: `make share` でアセットを書き出す" as an explicit step
- Section 7: extensions should propose follow-up artifacts (a series, an annual recap, a printable poster)
- Section 8 prompt: include a `demo` or `share` build target so the agent can produce the asset on first run

---

## 7. Anti-Patterns

- **Bait artifact**: a beautiful mockup that the build cannot actually produce
- **Tooling demo**: the artifact is "look at this nice React component" — there is no story
- **Wrapped clone**: another Spotify-Wrapped knock-off
- **Mocked numbers**: stats that aren't real, just plausible
- **Endless GIF**: 30s GIFs that lose the viewer at second 5
- **Inside-baseball**: artifact only legible to the author; no curious-engineer hook

---

## 8. Logging Note

For `viral` recipe, log the *artifact type* in the `mood` column (`png`, `gif`, `cli-cast`, `tweet`, `readme-graphic`). This keeps the rotation check from generating five GIF ideas in a row.
