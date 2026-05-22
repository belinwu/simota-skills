# Prompt Catalog

Purpose: Select the right NotebookLM prompt family, duration, and style, then produce a concise steering prompt that fits the audience and source.

## Contents

- Core prompt rules
- Format selection matrix
- Canonical prompt skeletons
- Duration calibration
- Source-prep meta prompts

## Core Prompt Rules

- Keep steering prompts at `150 words` or less.
- Keep instructions to `8` or fewer.
- Use the three-layer structure:
  - `Audience`
  - `Focus`
  - `Tone`
- Prefer `2-3` high-value patterns instead of stacking every pattern.
- State what to skip, not only what to include.

### Pattern Library

| Pattern | Use it when... | Default effect |
|---------|----------------|----------------|
| `Audience Anchor` | Audience level or decision context matters most | Improves fit and relevance |
| `Negative Space` | The source is broad or noisy | Reduces repetition and drift |
| `Focus Laser` | The task must go deep on `1-2` topics | Raises depth and clarity |
| `Tone Dial` | Brand voice or audience tone matters | Improves engagement |
| `Duration Target` | Time or slide count must stay tight | Improves pacing |
| `Structural Blueprint` | The format needs explicit sequencing | Improves flow and completeness |

## Format Selection Matrix

| Family | Best for | Default duration / size | Use this when... |
|--------|----------|-------------------------|------------------|
| `Audio Deep Dive` | Deep understanding, technical or strategic learning | `15-30 min` | Audience wants depth and can stay engaged |
| `Audio Brief` | Executive summary, sharing, short updates | `3-10 min` | Time is scarce and actionability matters |
| `Audio Critique` | Research review, product evaluation | `10-20 min` | Sources contain claims, trade-offs, or evidence to assess |
| `Audio Debate` | Multi-perspective comparison | `15-25 min` | Sources intentionally conflict or compare viewpoints |
| `Audio Lecture` | Teaching, tutorials, onboarding | `15-30 min` | Audience needs stepwise learning |
| `Audio Interactive` | Real-time Q&A with hosts (Interactive Mode) | `unbounded — driven by user turns` | Audience benefits from interrupting and steering the discussion |
| `Video Explainer` | Concept explanation with visuals | `2-10 min` | Visual reinforcement matters |
| `Video Brief` | Teasers, short shareable summaries | `30-90 sec` to `2-3 min` | Awareness and quick distribution matter |
| `Video Cinematic` | Immersive, deep-dive visual storytelling (Veo 3-powered) | `5-15 min` | Source narrative deserves cinematic pacing AND user is on Google AI Ultra (English only; daily quota) |
| `Presenter Slides` | Live presentation | `10-20 slides` | A speaker will talk over the deck |
| `Detailed Deck` | Handout or self-serve reading | `15-30 slides` | The deck must stand alone |
| `Infographic` | Visual summary | 60-second scan target | Data must be understood quickly |
| `Mind Map` | Topic structure and hierarchy | depth depends on topic | The main value is organization, not narrative |
| `Deep Research` | Full investigation | scope-driven | Source quality is strong and the task requires depth |
| `Data Table` | Structured comparison of qualitative content | rows scale with sources | Audience needs side-by-side facts exportable to Sheets |
| `Flashcards / Quiz` | Active recall and self-check | deck size / question count | Audience is studying or onboarding and needs retrieval practice |

## Audience-Fit Defaults

| Audience | Preferred audio | Preferred video | Preferred slides |
|----------|-----------------|-----------------|------------------|
| `C-suite` | `Brief: Executive Summary` | `Explainer: Corporate` | `Presenter: Internal` |
| `PM` | `Brief` or `Deep Dive` | `Explainer: Corporate` | `Presenter: Internal` |
| `Senior Engineer` | `Deep Dive: Technical` | `Explainer: Whiteboard` | `Detailed: Handout` |
| `Junior Dev` | `Lecture: Tutorial` | `Explainer: Classroom` | `Detailed: Educational` |
| `Researcher` | `Critique: Research` | `Explainer: Academic` | `Detailed: Handout` |
| `General Public` | `Deep Dive: General` | `Brief: Casual` | `Presenter: TED-style` |
| `Student` | `Lecture: Tutorial` | `Explainer: Classroom` | `Detailed: Educational` |
| `Sales` | `Brief: Social Share` | `Brief: Casual` | `Presenter: Internal` |

## Video Style Matrix

As of 2026-05, NotebookLM exposes the following first-party visual styles for Video Overviews. The official set has consolidated to eight predefined styles below; legacy descriptive labels (Abstract / Corporate / Casual / Academic / News) should be mapped onto the closest official style before steering.

| Official style | Best for | Avoid when... |
|----------------|----------|---------------|
| `Classic` | Polished executive or internal business updates | Audience expects playful or hand-drawn feel |
| `Whiteboard` | Engineering, systems, step-by-step explanation | Audience expects a polished executive feel |
| `Watercolor` | Soft, narrative storytelling and emotional framing | Dense technical operational detail dominates |
| `Retro Print` | Historical, editorial, magazine-style framing | Audience expects modern minimal aesthetic |
| `Heritage` | Cultural, archival, long-arc storytelling | Topic is breaking news or short-lived |
| `Paper-craft` | Tactile, playful, education-friendly framing | Audience expects high-fidelity realism |
| `Kawaii` | Cute, beginner-friendly, lightweight summaries | Brand voice must stay formal or technical |
| `Anime` | Energetic, narrative-driven explanations | Audience expects strictly factual, neutral framing |
| `Cinematic (Veo 3)` | Immersive deep-dive videos with fluid animation | User is not on Google AI Ultra, content is not English, or daily quota would be exceeded |

## Infographic Style Matrix

NotebookLM ships 10 predefined infographic styles (rolled out 2026-03). Pick the style after the content type is fixed, not before.

| Style | Best for | Avoid when... |
|-------|----------|---------------|
| `Sketch Note` | Visual note-taking summaries | Audience expects formal corporate output |
| `Kawaii` | Beginner-friendly, lightweight summaries | Brand voice must stay formal |
| `Professional` | Executive, B2B, investor-facing artifacts | Audience expects playful or educational tone |
| `Scientific` | Research, lab, or technical breakdowns | Content is opinion- or narrative-driven |
| `Anime` | Energetic narrative-driven summaries | Audience expects strictly neutral framing |
| `Clay` | Friendly, approachable conceptual visuals | High data density must dominate |
| `Editorial` | Magazine-style, story-led summaries | Audience needs raw structured data |
| `Instructional` | Step-by-step or how-to summaries | Content has no clear sequence |
| `Bento Grid` | Multi-fact dashboards and at-a-glance comparisons | Single narrative arc is the point |
| `Bricks` | Modular, component-style summaries | Continuous storytelling is required |

## Canonical Prompt Skeletons

Use these as baseline templates. Replace bracketed values and keep the final prompt concise.

### Audio Deep Dive

```text
Target audience: [audience and knowledge level].
Focus heavily on: [1-2 topics].
Tone: [tone].
Duration: aim for [duration].
Discuss: [required themes].
Skip: [what not to cover].
Use concrete comparisons or examples where helpful.
```

### Audio Brief

```text
Target audience: [busy audience].
Open with the single most important insight.
Cover the top [3-5] points only.
Tone: [tone], concise and direct.
Duration: [duration].
Skip: background, caveats, or implementation detail unless critical.
End with: what this means and what to do next.
```

### Audio Critique

```text
Target audience: [audience].
Analyze the source critically.
Evaluate strengths, weaknesses, assumptions, and missing evidence.
Tone: [tone], evidence-first.
Duration: [duration].
Skip: generic praise or unsupported claims.
End with a verdict and next questions.
```

### Audio Debate

```text
Target audience: [audience].
Present the strongest arguments on each side of [question].
Keep both sides balanced before reaching a synthesis.
Tone: [tone].
Duration: [duration].
Skip: false certainty.
End with the conditions under which each side is more persuasive.
```

### Audio Lecture

```text
Target audience: [beginners / learners].
Assume: [knowledge level].
Teach the topic in a step-by-step way.
Tone: patient, encouraging, and clear.
Duration: [duration].
Use concrete examples and simple analogies.
Skip: unexplained jargon.
```

### Audio Interactive

```text
Target audience: [audience].
Format: Interactive Mode — invite the listener to interrupt and ask questions.
Open with the most important framing in under 60 seconds.
Tone: [tone], conversational and pause-friendly.
When the user interrupts, treat the interruption as the new priority.
Skip: long uninterrupted monologues; leave breathing room every 60-90 seconds.
End each turn with an implicit invitation for the next question.
```

### Video Explainer

```text
Target audience: [audience].
Format: Video Explainer in [visual style].
Focus on: [core topic].
Tone: [tone].
Duration: [duration].
Use visuals to reinforce the key concepts, not decorate them.
Keep on-screen text minimal and readable.
Skip: points that cannot be shown or explained clearly on screen.
```

### Video Brief

```text
Target audience: [audience].
Format: Video Brief in [visual style].
Hook the viewer immediately with the strongest insight.
Tone: [tone].
Duration: [duration].
Cover only the most shareable or decision-relevant points.
End with a clear takeaway or CTA.
```

### Video Cinematic (Veo 3)

```text
Target audience: [audience].
Format: Cinematic Video Overview (Veo 3) — fluid animation, immersive pacing.
Lead with a single human-scale opening image or scene.
Tone: [tone], story-led rather than slide-led.
Duration: [duration].
Constraint: English only; user must be on Google AI Ultra. Do not promise this format unless tier is confirmed.
Use the source as a narrative spine; do not narrate page-by-page.
Skip: bullet-point delivery; let visuals carry secondary detail.
```

### Presenter Slides

```text
Target audience: [audience].
Create Presenter Slides for a live talk.
Keep each slide to one message.
Use [style] tone and pacing.
Target length: [slide count].
Minimize slide text and maximize clarity.
Skip detail that belongs in speaker notes, not on the slide.
```

### Detailed Deck

```text
Target audience: [audience].
Create a Detailed Deck that can be read without a presenter.
Include: context, evidence, structure, and conclusions.
Tone: [tone].
Target length: [slide count].
Use clear sections and self-contained explanations.
Skip decorative slides that add no understanding.
```

### Deep Research

```text
Target audience: [audience].
Produce a Deep Research output on [topic].
Prioritize: evidence quality, synthesis, trade-offs, and open questions.
Tone: [tone].
Scope: [specific scope].
Skip: unsupported extrapolation and off-topic context.
End with actionable recommendations and unresolved questions.
```

### Data Table

```text
Target audience: [audience].
Format: Data Table in Studio (export-ready for Google Sheets).
Rows: [entities being compared].
Columns: [attributes / dimensions to compare].
Tone: factual, neutral, source-grounded.
Fill cells only from the sources; mark missing data as "—".
Skip: narrative prose; rely on the table itself.
```

### Flashcards / Quiz

```text
Target audience: [learners / level].
Format: [Flashcards | Quiz] for active recall.
Card / question count: [count].
Difficulty: [intro / mixed / advanced].
Tone: clear, unambiguous, single-fact per card.
Cover: [core topics].
Skip: trivia, ambiguous wording, multi-answer phrasing.
```

## Duration Calibration

| Goal | Audio | Video | Slides |
|------|-------|-------|--------|
| Overview / teaser | `3-5 min` | `30-90 sec` | `5-8` |
| Standard summary | `8-12 min` | `2-3 min` | `10-15` |
| Deep exploration | `15-25 min` | `5-10 min` | `20-30` |
| Comprehensive | `25-30 min` | `10-15 min` | `30+` |

## Source-Prep Meta Prompts

Use these when the user is not ready for a final steering prompt.

### Source Quality Check

```text
Review the source set for quality, focus, and gaps.
Identify weak or redundant sources, note if the set is too broad, and recommend the best notebook composition pattern.
```

### Format Selection Check

```text
Recommend the best NotebookLM output format for this audience, purpose, and source set.
Compare the top two options and explain what would be lost with the weaker choice.
```

### Iteration Setup

```text
Assess the current steering prompt.
Keep what is working, change only one variable, and suggest the next A/B test.
```
