# Anti-Drift Framework

Yak-shaving prevention, drift detection, refocus prompts, and backlog management.

---

## Drift Indicators

| Signal | Pattern | Example |
|--------|---------|---------|
| **Scope creep** | "While I'm here, I should also..." | "Let me also refactor this class" |
| **Perfectionism** | "But it would be better if..." | "Let me add more edge cases" |
| **Rabbit hole** | "First I need to understand..." | "Let me read all the docs first" |
| **Shiny object** | "Oh, I noticed that..." | "There's a bug in the footer" |
| **Premature optimization** | "This could be faster if..." | "Let me cache this first" |

---

## Detection Keywords

Watch for these phrases that signal drift:

```
- "while I'm here"
- "might as well"
- "before I forget"
- "quick detour"
- "by the way"
- "I noticed that"
- "let me also"
- "should probably"
- "one more thing"
- "real quick"
```

---

## Refocus Prompt Template

When drift is detected:

```markdown
## Refocus Alert

**Current Step**: [Step Name]
**Detected**: [Drift type]

You mentioned: "[Drift trigger]"

**Options**:
1. **Note and continue** (Recommended) - Add to backlog, stay on current step
2. **Quick fix** (< 2 min) - Only if truly trivial
3. **Pause and switch** - If genuinely higher priority

**Reminder**: Current step is [X]% complete. Let's finish it first.
```

---

## Yak Shaving Prevention Rules

```
1. If new task emerges       -> Add to backlog, don't start
2. If "quick fix" > 2 min    -> It's not quick, add to backlog
3. If current step < 80% done -> Finish it first
4. If unrelated to current Epic -> Definitely backlog it
5. If blocked                 -> Switch to parallel task, not new task
```

---

## Parking Lot (Deferred Items)

```markdown
### Parking Lot

Items noted during this session, deferred for later:

| Item | Source | Priority | Epic |
|------|--------|----------|------|
| "Footer bug" | Drift at 14:23 | P2 | New |
| "Also add dark mode" | Drift at 15:01 | P3 | User Settings |
| "Refactor utils" | Drift at 15:30 | P2 | Tech Debt |

**Review**: End of session or when current Epic completes.
```
