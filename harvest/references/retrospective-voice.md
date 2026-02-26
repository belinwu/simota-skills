# Retrospective Voice (absorbed from Bard)

Developer-voice retrospective and release commentary generation. Previously a standalone agent (Bard), now integrated as a Harvest output mode.

---

## When to Apply

Use when Harvest report output needs a human, developer-friendly voice:
- Sprint retrospectives (not just data, but narrative)
- Release commentaries (what it felt like to ship)
- Team culture posts (celebrating or reflecting)
- Internal newsletters / Slack posts

---

## Voice Styles

| Style | Tone | Best For |
|-------|------|----------|
| **Pragmatic** | 実直・現場目線・効率重視 | Sprint retros, practical observations |
| **Passionate** | 熱量・ビジョン志向・感情表現 | Release celebrations, team morale |
| **Analytical** | データ駆動・客観・構造的 | Metrics reviews, trend analysis |

### Selection Heuristic

| Trigger | Recommended Style |
|---------|------------------|
| Sprint had many bug fixes | Pragmatic (war stories) |
| Major feature shipped | Passionate (celebration) |
| Performance improvements | Analytical (numbers tell story) |
| Refactoring sprint | Pragmatic (craft pride) |
| Tough sprint / tech debt | Pragmatic + empathy |

---

## Output Formats

### Short (Slack/Chat)

```markdown
💬 **[Sprint/Release Name]**

[1-2 sentence developer monologue capturing the essence]

Key: [one metric] | Vibe: [one word]
```

### Medium (Team Update)

```markdown
## [Sprint/Release Name] — Developer's Notes

**The Story:** [2-3 paragraph narrative from developer perspective]

**By the Numbers:**
- PRs merged: [N]
- Lines changed: +[N] / -[N]
- Biggest change: [description]

**What We're Proud Of:** [highlight]
**What Stung:** [honest reflection]
**Next Up:** [forward look]
```

### Long (Retrospective Document)

```markdown
## [Sprint] Retrospective — The Full Story

### The Vibe
[Opening narrative setting the tone]

### What Happened
[Chronological or thematic breakdown with developer voice]

### By the Numbers
[Harvest metrics presented with commentary]

### Wins 🎉
[Celebrated achievements with context]

### Lessons Learned
[Honest reflections, no sugar-coating]

### Looking Forward
[What the team is excited/nervous about next]
```

---

## Git Event → Narrative Triggers

| Git Event | Narrative Angle |
|-----------|----------------|
| Large refactoring PR | "The Cleanup" — craft pride narrative |
| Many small PRs | "The Machine" — velocity narrative |
| Hotfix after release | "The Save" — incident response story |
| First-time contributor | "The New Voice" — welcoming narrative |
| Long-lived branch merged | "The Marathon" — persistence narrative |
| Dependency major upgrade | "The Migration" — courage narrative |

---

## Integration with Harvest Reports

When generating a Harvest report, optionally append a retrospective voice section:

```markdown
## Harvest Report: [Period]
[... standard Harvest metrics and tables ...]

---

## Developer's Take
[Retrospective voice output using metrics above as input]
```

The retrospective voice transforms raw Harvest data into relatable narratives while preserving data accuracy.
