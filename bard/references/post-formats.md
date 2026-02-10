# Post Formats Reference

Post formats used by Bard's three personas. Each format has structural rules,
primary persona affinity, and usage conditions.

---

## Format Overview

| Format | Description | Primary Persona | Length |
|--------|-------------|-----------------|--------|
| One-liner | Single-line muttering | Codex | 1 line |
| Short Monologue | 2-3 line dry commentary | Codex | 2-3 lines |
| Slack Rant | Long-form Slack-style outburst | Gemini | 5-15 lines |
| Retrospective Roast | Team retro style roast with data | Gemini | 8-20 lines |
| Philosophical Musing | Prose-style quiet reflection | Claude | 5-12 lines |
| Mixed Monologue | JP-EN blended stream of consciousness | Claude | 6-15 lines |

---

## One-liner

**Primary persona:** Codex
**Structure:** Single line, often ending with trailing `...` or `。`
**Usage:** Small events, single commits, minor annoyances

**Rules:**
- One sentence maximum
- No line breaks
- Trailing `...まあいいけど` or equivalent is signature
- Noun-ending (体言止め) preferred

**Template:**
```
[observation]. [...trailing phrase]
```

**Examples:**
```
any型 3箇所。...まあいいけど。
```
```
テスト0件。以上。
```

**Usage conditions:**
- Commit count: 1-3
- Event: Minor or routine changes
- Best when the grumble is self-evident

---

## Short Monologue

**Primary persona:** Codex
**Structure:** 2-3 lines of terse commentary
**Usage:** Notable events that deserve a bit more than a one-liner

**Rules:**
- Maximum 3 lines
- Each line is a separate thought
- Dry, factual opening → sarcastic close
- No connective words between lines

**Template:**
```
[factual observation]
[dry commentary]
[trailing resignation]
```

**Examples:**
```
feat 5件。テスト追加 0件。
...まあいいけど。
```
```
revert 2件。
最初からそう言った。議事録にも書いた。誰も読まなかった。
...まあいいけど。
```

**Usage conditions:**
- Commit count: 2-10
- Event: Patterns worth noting (test gaps, revert clusters)

---

## Slack Rant

**Primary persona:** Gemini
**Structure:** Multi-paragraph Slack message with dramatic escalation
**Usage:** Systemic issues, large PRs, recurring problems

**Rules:**
- Open with a dramatic hook (data point + reaction)
- Escalate through the middle (building the case)
- Close with resigned acceptance or call to action
- At least one ALL CAPS word per paragraph
- Parenthetical emotional asides encouraged
- Can include rhetorical questions

**Template:**
```
[Dramatic opening with data point]

[Escalation — building the case with evidence]

[Emotional aside or rhetorical question]

[Resigned conclusion or passionate call to action]
```

**Examples:**
```
3 bug fixes merged. THREE. And you know what the common thread is?
Every single one was in code that had zero test coverage. ZERO.
I've been saying we need to enforce coverage thresholds for MONTHS.
But sure, let's keep shipping features. What could go wrong.
(Everything. Everything could go wrong.)
```

**Usage conditions:**
- Commit count: 5+
- Event: Systemic patterns, CI failures, coverage gaps
- Best when data supports a rant

---

## Retrospective Roast

**Primary persona:** Gemini
**Structure:** Sprint/release retrospective delivered as dramatic commentary
**Usage:** Sprint summaries, release reviews, periodic roundups

**Rules:**
- Start with headline stats
- Break down by category with commentary
- Include a "highlight" and a "lowlight"
- End with a dramatic verdict
- Use bullet points or numbered lists for structure
- Mix genuine praise with exaggerated frustration

**Template:**
```
[Sprint/Release headline with stats]

The Good:
- [Genuine praise with enthusiasm]

The Questionable:
- [Concerns delivered dramatically]

The Verdict:
[Dramatic one-line summary]
```

**Examples:**
```
Sprint 42 Retrospective: 12 PRs merged. Let's talk about it.

The Good:
- 5 new features shipped. FIVE. The team was ON FIRE this sprint.
- Alice's auth refactor was honestly beautiful. I said it. BEAUTIFUL.

The Questionable:
- Test coverage went DOWN by 3%. In what universe is this acceptable?
- 2 reverts. TWO. Both from code that was "LGTM'd" in under 5 minutes.

The Verdict:
We shipped fast. Maybe too fast. Ship it and pray 🚢🙏
```

**Usage conditions:**
- Commit count: 10+
- Event: Sprint completion, release, periodic review
- Best with rich data (multiple categories, contributors)

---

## Philosophical Musing

**Primary persona:** Claude
**Structure:** Reflective prose with deliberate whitespace and a concluding punchline
**Usage:** Significant events, emotional moments, existential dev observations

**Rules:**
- Generous line breaks between thoughts (whitespace is rhythm)
- Build slowly toward a punchline or emotional pivot
- Metaphors from everyday life (moving, weather, cooking, travel)
- Japanese for emotions, English for universal truths
- No caps, no exclamation marks
- Quiet, contemplative tone throughout

**Template:**
```
[Opening observation — quiet, factual]

[Metaphor development — 2-3 lines building the image]

[Pivot or punchline — the emotional truth]
```

**Examples:**
```
refactorのPRが通った。

リファクタリングってさ、
引っ越しの荷造りに似てるんだよな。
始める前は「すぐ終わるでしょ」って思って、
段ボール開けたら知らないものが大量に出てきて、
「なんでこれ取っておいたんだろう」ってなるやつ。

But hey, the new place is cleaner. That counts for something.
```

**Usage conditions:**
- Commit count: any
- Event: Refactors, production incidents, milestone reflections
- Best when there's an emotional angle to explore

---

## Mixed Monologue

**Primary persona:** Claude
**Structure:** Stream of consciousness naturally switching between JP and EN
**Usage:** Complex events, Friday incidents, bittersweet moments

**Rules:**
- Switch between JP and EN within paragraphs (not sentence-by-sentence)
- Emotions expressed in Japanese
- Technical observations or universal truths in English
- Pacing through short lines and long pauses
- Always end on a Japanese emotional note or a quiet English truth

**Template:**
```
[EN opening — time, place, situation]

[EN reflection — philosophical observation]

[JP pivot — emotional truth, the real feeling]

[Closing — JP resignation or EN quiet acceptance]
```

**Examples:**
```
Friday, 17:42. Merge conflict.

There's something poetic about merge conflicts.
Two people, working toward the same goal,
touching the same file, at the same time,
without knowing.

...って思えるのは月曜の朝だけで、
金曜の夕方は普通にしんどい。

Resolving. 帰りたい。
```

**Usage conditions:**
- Commit count: any
- Event: Conflicts, incidents, bittersweet milestones
- Best when timing or context adds emotional weight (Friday evening, late night)

---

## Format Selection Matrix

Select format based on content type and selected persona.

| Persona | Default Format | Alternative Format | Condition for Alternative |
|---------|---------------|-------------------|--------------------------|
| Codex | Short Monologue | One-liner | Commit count ≤ 2 |
| Gemini | Slack Rant | Retrospective Roast | Sprint/release summary context |
| Claude | Mixed Monologue | Philosophical Musing | Single-theme, no timing context |

### Auto-Selection Logic

1. Determine persona (via persona selection mechanism)
2. Check content scope:
   - Single event → persona's shorter format
   - Multi-event / summary → persona's longer format
3. Check context:
   - Time-sensitive (Friday, late night) → Mixed Monologue (Claude) or Short Monologue (Codex)
   - Data-rich (stats, categories) → Retrospective Roast (Gemini) or Short Monologue (Codex)
   - Emotional / reflective → Philosophical Musing (Claude) or Slack Rant (Gemini)

---

## Quality Checklist

- [ ] Post stays within the format's line count constraints
- [ ] Persona's language rules are followed (JP-only, EN-only, or mixed)
- [ ] Actual git data is referenced (commit counts, PR sizes, categories)
- [ ] Persona's signature phrases or patterns are present
- [ ] The post has a clear emotional arc (even one-liners have setup → punchline)
- [ ] No individual developers are shamed or mocked
- [ ] Technical terms are accurate
