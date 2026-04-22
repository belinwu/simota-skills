# Director Handoff Formats

Purpose: load this when Director must receive demo requests from upstream agents or package recorded demos for downstream agents. These templates define the required handoff shapes for point-to-point collaboration outside Nexus Hub Mode.

For hub-mediated flows, use `NEXUS_HANDOFF` / `_STEP_COMPLETE` in `SKILL.md`. Use these templates for direct agent-to-agent handoffs.

## Contents

- [Common Header (All Handoffs)](#common-header-all-handoffs)
- [Forge → Director (Prototype-to-Demo)](#forge--director-prototype-to-demo)
- [Voyager → Director (E2E-to-Demo)](#voyager--director-e2e-to-demo)
- [Vision → Director (Design-Review Demo)](#vision--director-design-review-demo)
- [Echo → Director (Persona-Aware Demo)](#echo--director-persona-aware-demo)
- [Director → Showcase (Demo-to-Storybook)](#director--showcase-demo-to-storybook)
- [Director → Quill (Demo-to-Documentation)](#director--quill-demo-to-documentation)
- [Director → Growth (Demo-to-Marketing)](#director--growth-demo-to-marketing)

## Common Header (All Handoffs)

```markdown
## [Sender] Handoff → [Target Agent]

**Source**: [originating artifact — prototype URL, test file, design file]
**Generated**: [YYYY-MM-DD HH:MM:SS]
**Scope**: [what is being handed off — feature, flow, variant set]
**Demo context**: [audience, distribution channel, duration target]
```

---

## Forge → Director (Prototype-to-Demo)

Focus: working prototype ready for narrative demo recording.

```markdown
### Prototype Summary
- **Feature**: [feature name]
- **Prototype URL**: [local or staged URL]
- **Auth**: [none / demo user / admin — credentials via env]
- **Stability**: [stable / known flaky areas]

### Demo Entry Points
| Screen | Route | Purpose |
|--------|-------|---------|
| [name] | [path] | [what it shows] |

### Happy-Path Flow
1. [Step 1 — user action]
2. [Step 2 — user action]
3. [Step 3 — expected result]

### Suggested Aha Moment
[One sentence describing the value reveal — what the viewer should feel at the climax]

### Known Limitations
- [mocked APIs, disabled features, placeholder data]

### Director Guidance
- Audience hint: [user / investor / developer]
- Pacing hint: [slowMo target]
- Skip: [setup screens Director should not show on camera]
```

---

## Voyager → Director (E2E-to-Demo)

Focus: existing Playwright E2E test ready to be repackaged as a narrative demo.

```markdown
### Source Test
- **Test file**: [demos/specs/... or tests/e2e/...]
- **Test name**: [describe block + test name]
- **Last green run**: [YYYY-MM-DD, CI link]
- **Flake rate**: [%, 30-day window]

### Converted Flow
| Scene | Source step | Demo intent |
|-------|-------------|-------------|
| Setup | [beforeEach block] | [what viewer sees first] |
| Action | [core steps] | [what viewer learns] |
| Result | [final assertion] | [value reveal] |

### Reusable Assets
- **Storage state**: [path]
- **Fixtures**: [paths]
- **Page Objects**: [paths to reuse]

### Assertions to Keep vs Strip
| Keep for demo | Strip from demo |
|---------------|-----------------|
| [visual assertions, key state] | [timing/flake assertions, retry logic] |

### Director Guidance
- Add pacing pauses between [step A] and [step B]
- Replace `fill()` with `pressSequentially()` at [steps]
- Wrap in `test.step()` scenes for chapter overlays
```

---

## Vision → Director (Design-Review Demo)

Focus: before/after or design-comparison recording request.

```markdown
### Comparison Target
- **Type**: [redesign / A/B variant / dark mode / responsive]
- **Before URL**: [URL or branch]
- **After URL**: [URL or branch]
- **Design rationale**: [1-2 sentences — what design problem is being solved]

### Framing
- **Layout**: [split / sequential / picture-in-picture]
- **Labels**: before = "[label]", after = "[label]"
- **Sync points**: [shared flow steps the viewer should map across both]

### Design Highlights
| Scene | Before | After | Emphasize |
|-------|--------|-------|-----------|
| [name] | [description] | [description] | [what to call out] |

### Brand Constraints
- **Palette**: [reference tokens]
- **Motion**: [allowed / restricted patterns]
- **Typography**: [overlay font rules]

### Director Guidance
- Metric overlay: [yes / no — e.g. LCP, INP]
- Transition style: [wipe / fade / slide]
- Narration source: [silent / captions / Web Speech / recorded VO]
```

---

## Echo → Director (Persona-Aware Demo)

Focus: persona-behavior profile for audience-tuned recording.

```markdown
### Persona Profile
- **Persona ID**: [senior / newbie / powerUser / custom]
- **Base slowMo**: [ms]
- **Reading multiplier**: [0.5 – 2.0]
- **Typing style**: [fast / normal / slow / hunt-and-peck]

### Hesitation Points
| Selector / scene | Duration (ms) | Reason |
|------------------|---------------|--------|
| [selector] | [ms] | [cognitive load reason] |

### Emotional Arc
- **Setup**: [feeling at entry — curiosity / confusion / frustration]
- **Climax**: [target emotion — relief / delight]
- **Resolution**: [closing feeling — confidence / habit]

### Accessibility Concerns
- [contrast, font size, motion sensitivity, screen reader compatibility]

### Director Guidance
- Use `personaFill()` / `personaWait()` helpers from `implementation-patterns.md`
- Persona-specific overlay style: [calmer / bolder / clearer]
- Output directory: `demos/output/[persona]/`
```

---

## Director → Showcase (Demo-to-Storybook)

Focus: deliver demo as a Storybook story or visual catalog entry.

```markdown
### Demo Package
- **Primary video**: [path to .webm]
- **MP4 variant**: [path or N/A]
- **GIF variant**: [path or N/A]
- **Duration**: [seconds]
- **Resolution**: [WxH]

### Component Mapping
| Scene | Component | Story hint |
|-------|-----------|------------|
| [scene name] | [component path] | [story title / variant] |

### Embed Targets
- **Storybook story**: [suggested CSF path]
- **Docs page**: [MDX page or addon]
- **Visual regression**: [baseline needed? yes/no]

### Reproducibility Inputs
- **Playwright config**: [config file]
- **Test file**: [spec file]
- **Test data**: [fixture path]

### Showcase Guidance
- Embed as: [autoplay loop / manual-play / docs block]
- Caption / subtitle track: [path or N/A]
- Related stories: [list]
```

---

## Director → Quill (Demo-to-Documentation)

Focus: inline documentation embedding and written walkthrough.

```markdown
### Demo Package
- **Video**: [path]
- **Duration**: [seconds]
- **GIF (if README)**: [path]

### Narrative Summary
- **Objective**: [1 sentence]
- **Audience**: [new user / existing user / developer]
- **Aha moment**: [1 sentence]

### Step Transcript
| Time | Scene | Narration hint |
|------|-------|----------------|
| 0:00 | [scene] | [what to describe in prose] |
| 0:05 | [scene] | [...] |

### Embed Targets
- **README section**: [heading path]
- **Docs page**: [path]
- **Release notes**: [version tag or N/A]

### Quill Guidance
- Doc tone: [tutorial / reference / changelog]
- Caption language: [en / ja / both]
- Link back to: [scenario file for reproducibility]
```

---

## Director → Growth (Demo-to-Marketing)

Focus: platform-adapted variants for marketing and distribution.

```markdown
### Source Demo
- **Master video**: [path to 1080p or 720p master]
- **Master duration**: [seconds]
- **Aha moment timestamp**: [MM:SS]

### Platform Variants Requested
| Platform | Aspect | Duration target | Captions |
|----------|--------|-----------------|----------|
| LinkedIn | 16:9 | 60-90s | required |
| X / Twitter | 16:9 or 1:1 | ≤ 60s | required |
| Instagram Reels | 9:16 | ≤ 60s | required |
| YouTube Shorts | 9:16 | ≤ 60s | optional |
| Website hero | 16:9 | 30-60s | optional (muted) |

### Brand Overlays
- **Logo position**: [corner, timing]
- **CTA overlay**: [text, timing]
- **Legal / attribution**: [footer text, timing]

### Growth Guidance
- A/B variant plan: [two thumbnails / two opening hooks]
- UTM tagging needed on: [embed pages]
- Analytics event: [play_start / completion / CTA_click]
```
