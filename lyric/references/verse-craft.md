# Verse Craft Reference

Purpose: Verses carry the song's argument — they set scene, establish perspective, and build emotional pressure toward the chorus. This reference distills Pat Pattison's object-writing technique, prosody alignment, and verse-specific craft decisions into a checklist usable for both first drafts and surgical revision. Verses fail not from bad ideas but from abstract telling, perspective drift, and unsingable phonemes — this guide targets each.

## Scope Boundary

- **lyric `verse`**: verse-section craft only — story/setup, POV/tense, image-to-emotion ratio, internal rhyme density, line-length contour, sense-bound imagery. Produces verse drafts and revision checklists.
- **lyric `compose` (default)**: full song generation including verses, but does not deep-dive verse-specific prosody. Use `verse` when verses are the bottleneck (weak, generic, or rhythmically off).
- **lyric `hook` (sibling)**: chorus/hook craft. Verses set up; hooks land. Boundaries differ — `verse` allows narrative breath, `hook` forbids it.
- **lyric `bridge` (sibling)**: bridge departure. Verses are the home perspective; bridge is the away perspective.
- **lyric `refine` (sibling)**: feedback-driven revision across the whole song. Use `verse` for targeted verse-only craft work before `refine`.
- **Saga (elsewhere)**: customer/product narrative storytelling. Saga produces non-musical narrative; verse-craft applies music-specific prosody constraints (syllable counts, melodic alignment).
- **Tone (elsewhere)**: audio generation. Verse-craft outputs lyrics; Tone wires Suno API calls. Verse-craft never writes API code.

## Workflow

```
SCENE      →  pick a single moment (time, place, sensory anchor)
           →  decide POV (1st / 2nd / 3rd) and tense (past / present)

OBJECT     →  Pattison object writing — saturate the moment with all 7 senses
           →  log raw observations (sight, sound, smell, taste, touch, organic, kinesthetic)

DISTILL    →  cut to 60-80% imagery, 20-40% interior reaction
           →  collapse abstractions into concrete nouns and verbs

CONTOUR    →  set line-length pattern (e.g., short-short-long-long, or stair-step)
           →  match syllable counts across parallel lines for melodic consistency

RHYME      →  end-rhyme scheme (avoid AABB default) + 1-2 internal rhymes per stanza
           →  assonance/consonance for sub-rhyme texture without forced couplets

SING-CHECK →  read aloud at target tempo; flag consonant clusters, awkward stresses
           →  swap unsingable words for synonyms with cleaner phoneme flow
```

## Pat Pattison Object Writing — 7 Senses

| Sense | Prompt | Verse use |
|-------|--------|-----------|
| Sight | What's in the frame, color, light? | Visual anchor, scene establishment |
| Sound | Ambient, voice, silence quality? | Atmosphere, time-of-day cues |
| Smell | Air, surfaces, bodies, weather? | Memory triggers, intimacy markers |
| Taste | What's in the mouth, residue? | Visceral specificity, rare in pop |
| Touch | Texture, temperature, pressure? | Body-in-space grounding |
| Organic | Body sensations (heartbeat, gut, breath)? | Internal emotion made physical |
| Kinesthetic | Movement, motion, body in space? | Energy/tempo cues for melody |

Pattison's rule: senses 5 (touch), 6 (organic), 7 (kinesthetic) are underused — leaning on them produces verses that feel embodied rather than observed.

## Verse Craft Decisions

| Decision | Options | Default heuristic |
|----------|---------|-------------------|
| POV | 1st (I), 2nd (you), 3rd (she/he/they) | 1st for confessional, 2nd for direct address, 3rd for storytelling |
| Tense | Past, present, mixed | Present for immediacy, past for reflection — never mix mid-verse |
| Image:Emotion ratio | 60:40 to 80:20 | Higher imagery for indie/folk, more interiority for ballad/R&B |
| Line length | Uniform vs contoured | Contoured (short-short-long-long) creates melodic interest |
| Internal rhyme density | 0-2 per line | 1 mid-line rhyme per stanza adds texture without overcrowding |
| Verse 1 vs Verse 2 | Setup vs deepen | V1 establishes scene, V2 raises stakes or shifts angle — never repeat V1 content |
| Lines per verse | 4 / 6 / 8 | 4 for tight pop, 6-8 for narrative folk/country |

## Line-Length Contour Patterns

| Pattern | Shape | Effect |
|---------|-------|--------|
| Uniform | 4-4-4-4 | Steady, hypnotic — risks monotony |
| Stair-step up | 3-4-5-6 | Building tension toward chorus |
| Stair-step down | 6-5-4-3 | Settling, reflective |
| Pendulum | 4-6-4-6 | Conversational, breath-natural |
| Long-short trap | 7-3-7-3 | Country/storytelling — punchline rhythm |

Match patterns across V1 and V2 for melodic recyclability — Suno generates more consistent melodies when verses share contour.

## Anti-Patterns

- **Telling not showing** — "I felt so sad" instead of "the kettle screamed in the empty kitchen"; reduces lyric to therapy-journal abstraction. Pattison rule: name the object, not the feeling.
- **Perspective drift** — starting in 1st person, sliding to 3rd by line 4. Suno vocalists treat each line literally — drift confuses listeners and breaks identification.
- **Tense drift** — mixing past and present mid-verse without intentional jolt. Forces re-orientation that kills emotional momentum.
- **Abstract overload** — strings of nouns like "love, time, hope, pain" with no concrete anchor; reads as greeting-card filler and Suno renders flat.
- **Unsingable consonant clusters** — "strict thrust" or "sixths" buried mid-line; AI vocals slur, rush, or skip. Read every line aloud at tempo.
- **AABB couplet default** — primary signal of AI-generated lyric. Vary with ABAB, ABCB, or rhyme only lines 2 and 4.
- **Verse 2 = Verse 1 paraphrase** — same scene re-described loses listener interest by line 9. V2 must escalate (raise stakes, shift angle, reveal new fact).
- **Pre-chorus content in verse** — verse leaks the chorus emotional payload, leaving chorus underweight. Keep verse 60-80% setup, save the punch for the hook.
- **Over-rhyming** — internal rhymes on every line creates sing-songy children's-rhyme feel; cap at 1-2 per stanza unless genre demands (rap, vaudeville).

## Handoff

- **To Tone**: finalized verse text + line-length contour notes for Suno API generation. Flag any deliberately unusual phoneme runs so Tone can flag for re-generation.
- **To `lyric hook`**: verse emotional setup summary — what pressure has the verse built? Hook must release that exact pressure.
- **To `lyric bridge`**: verse home-perspective declaration. Bridge will depart from this; without a clear home, departure has no contrast.
- **To Saga**: when verse-narrative needs to align with a broader product/customer story arc, hand off scene anchor and POV decision.
- **To `lyric refine`**: once verses are crafted, full-song refinement (variant generation, A/B, melody-fit feedback) runs through `refine`.
