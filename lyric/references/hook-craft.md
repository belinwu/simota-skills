# Hook / Chorus Craft Reference

Purpose: The hook is the song's reason for existence — the phrase listeners replay in their heads. This reference covers memorability principles, title-placement strategy, the lyric-hook vs melodic-hook distinction, and the earworm research that explains why some choruses stick. Hooks fail from being too long, too generic, or having no anchor word — this guide targets each failure mode with corrective patterns.

## Scope Boundary

- **lyric `hook`**: chorus and hook craft only — memorability principles, repetition design, anchor-word selection, title-placement strategy, opening-line hooks. Produces hook drafts and revision checklists.
- **lyric `compose` (default)**: full song generation. Use `hook` when the chorus is weak/forgettable while verses are fine.
- **lyric `verse` (sibling)**: verse craft. Verses set up the emotional pressure; hooks discharge it.
- **lyric `bridge` (sibling)**: bridge departure. Hooks are the home; bridge is the away. Boundaries differ — hook forbids new info, bridge requires it.
- **lyric `metatags` / `style` (sibling)**: format-only and prompt-only recipes. `hook` works the chorus content itself; format/style come after.
- **Saga (elsewhere)**: narrative storytelling. Saga produces story arcs; hook-craft produces a 2-4 line earworm with melodic implications.
- **Tone (elsewhere)**: audio generation. Hook-craft never writes API code; once hook is set, Tone handles Suno generation.

## Workflow

```
ANCHOR     →  identify the anchor word/phrase (usually the song title)
           →  test: would the listener recognize the song from this phrase alone?

PLACE      →  decide title placement — top of chorus, bottom of chorus, or both
           →  top-loaded for radio/pop, bottom-loaded for narrative reveal

REPEAT     →  design repetition — exact, varied, or call-and-response
           →  every chorus must repeat the anchor at least twice

CONTRAST   →  contrast hook against verse — melody, rhythm, register, vocabulary
           →  if chorus reads like another verse, the hook is dead

LIMIT      →  cap chorus at 4 lines (Suno melodic-consistency hard rule)
           →  cut adjectives, conjunctions, qualifiers — leave nouns and verbs

SING-CHECK →  hum the chorus 5 minutes after writing without looking
           →  if you can't recall it, the hook is not yet a hook
```

## Memorability Principles

| Principle | Mechanism | Practical rule |
|-----------|-----------|----------------|
| Repetition | Spaced repetition of anchor consolidates memory | Anchor phrase appears 2-4× per chorus |
| Simplicity | Cognitive load — short phrases beat complex ones | Average chorus line ≤ 7 syllables |
| Contrast | Pattern interrupt against verse engages attention | Different rhythm, register, or melodic shape |
| Singability | Open vowels (ah, oh) sustain better than closed (i, e) | End anchor on open vowel where possible |
| Concreteness | Specific words encode better than abstract | "Whiskey on her breath" > "memories of her" |
| Emotion-spike | Peak emotional moment lives in chorus | Verse builds, chorus releases |
| Title-as-hook | Title in the chorus creates identification | 80%+ of pop hits include title in chorus |

## Title Placement Strategies

| Strategy | Pattern | Example use |
|----------|---------|-------------|
| Top-loaded | Title is line 1 of chorus | Pop, radio — instant recognition |
| Bottom-loaded | Title is final line of chorus | Country, ballad — narrative payoff |
| Sandwich | Title opens AND closes chorus | Anthemic — maximum recall |
| Refrain | Title repeated every line | Dance, EDM, kids — pure hook |
| Buried | Title once, mid-chorus | Indie, art-pop — subtle, riskier |

Default for Suno: top-loaded or sandwich — Suno's chorus melody varies less when the anchor sits in a fixed position across repeats.

## Lyric Hook vs Melodic Hook

| Type | What sticks | Lyric-craft implication |
|------|-------------|--------------------------|
| Lyric hook | Words alone are memorable ("I want to hold your hand") | Anchor phrase must be 2-5 syllables, conversational |
| Melodic hook | Melody is memorable, words are vehicle ("la la la", "na na na") | Use vowel-rich filler; lyrics secondary to melody |
| Hybrid (most pop) | Both reinforce each other | Anchor phrase shape matches melodic peak |

For Suno: lyric-hook strategy is more controllable via prompt; melodic-hook depends on Suno's melodic generation and is harder to direct deterministically. Default to lyric-hook craft.

## Opening-Line Hooks (Verse 1 Line 1)

The first line is a hook of its own — listeners decide within 7 seconds whether to keep listening.

| Pattern | Example shape | Effect |
|---------|---------------|--------|
| Specific scene | "Tuesday morning, sirens woke me up" | Cinematic, draws in |
| Question | "What if I told you I never left?" | Engages listener directly |
| Confession | "I lied about the morning we met" | Vulnerability hook |
| Image | "Cigarette smoke and a yellow cab" | Atmospheric, mood-first |
| Action | "I packed my car at 4 AM" | Momentum, story-in-motion |

Avoid: weather descriptions, generic "I" statements, abstract feelings. They are the AI-default opening and signal generic output.

## Earworm (INMI) Research Findings

Involuntary Musical Imagery research (Williamson, Jakubowski et al.):

- Earworms favor **medium tempo** (90-130 BPM) over very fast or slow.
- **Repetitive melodic shapes** with small contour leaps (≤ a fifth) stick best.
- **Unfilled gaps** — leaving a beat or syllable unfilled — triggers mental completion (the "Zeigarnik effect").
- **First and last lines** of a chorus encode strongest (primacy and recency).
- **Unusual but pronounceable** lyric phrases beat both totally generic and totally obscure.

Practical rule: write hooks with deliberate rhythmic gaps — Suno fills them melodically, and listeners' brains fill them on replay.

## Anti-Patterns

- **Chorus too long** — > 4 lines causes Suno to vary melody across repeats, killing hook consistency. Hard cap.
- **No anchor word** — chorus has no single repeatable phrase; nothing to remember. Every chorus needs one identifiable hook phrase.
- **Generic anchor** — "love is forever", "you are my world"; reads as filler and renders flat. Specificity even in 3 words ("burn the letters", "midnight bus") beats abstraction.
- **Hook = verse continuation** — chorus shares verse vocabulary, register, and rhythm; no contrast. Listener can't tell where verse ends.
- **Title buried or absent** — listener can't name the song after listening. Default to title-in-chorus unless genre justifies otherwise (some indie/art-pop).
- **Adjective-clogged chorus** — "the slow, sad, lonely sound of fading dreams"; cut to nouns and verbs.
- **Negative-direction anchor** — "I don't want this anymore" — Suno may render the negation awkwardly; positive constructions sing cleaner.
- **Too-clever phrase** — wordplay that requires re-reading; choruses must land in one pass.
- **Different chorus each time** — V1-chorus differs lyrically from V2-chorus without intent. Choruses repeat in full (Suno rule); minor variants only on final chorus.

## Handoff

- **To Tone**: finalized chorus text + anchor placement notes + tempo target. Flag if chorus depends on a specific melodic gap so Tone can verify Suno output.
- **To `lyric verse`**: pressure-discharge contract — chorus releases the emotional pressure verse built. Misalignment means re-crafting one or the other.
- **To `lyric bridge`**: hook signature for bridge to depart from and return to. Bridge contrast is measured against the established hook.
- **To `lyric metatags`**: chorus structure tag placement (`[Chorus]` immediately before, no embedded directions in lyric body).
- **To Saga**: when the song carries a product/brand narrative, hand off the anchor phrase as a candidate brand-line.
- **To `lyric refine`**: once hook is locked, refinement on full-song variants runs through `refine`.
