# V.A.I.R.E. Framework Reference

Complete reference for the V.A.I.R.E. framework.

> **2026 platform context.** The five dimensions remain stable; the *evidence* needed to score them has shifted. Apple **Liquid Glass** (iOS 26), Google **Material 3 Expressive** (spring-based physics motion, expressive type) and the rise of **ambient AI** inside the UI all change what "Score 2 / Score 3" looks like in practice. Sections that follow flag the dimension-specific implications; the framework itself is unchanged.

---

## Framework Overview

V.A.I.R.E. is a design language that defines experience quality across 5 dimensions.

```
        ┌─────────────────────────────────────────────────┐
        │                USER JOURNEY                      │
        │                                                  │
        │   Entry      Progress      Continuation   Exit   │
        │     │           │              │           │     │
        │     ▼           ▼              ▼           ▼     │
        │  ┌─────┐    ┌─────┐       ┌─────┐     ┌─────┐   │
        │  │  V  │───▶│  A  │──────▶│  I  │────▶│  E  │   │
        │  │alue │    │gency│       │dent │     │cho  │   │
        │  └─────┘    └─────┘       └─────┘     └─────┘   │
        │                                                  │
        │           ┌─────────────────────┐               │
        │           │    R e s i l i e n c e            │ │
        │           │    (Always present)               │ │
        │           └─────────────────────────────────────┘│
        └─────────────────────────────────────────────────┘
```

---

## Dimension 1: Value (Immediate Value Delivery)

### Definition

User understands "what they can do" and "what to do next" without confusion, reaching outcomes in minimum time.

### Temporal Position

**Entry** - Functions at the entry point of the experience.

### Core Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| Time-to-Value | Time to first value delivery | 30 seconds to few minutes |
| Activation Rate | First success experience rate | Industry average +20% |
| Task Success Rate | Task completion rate | 95%+ (critical flows) |
| Steps to Core Task | Steps to reach core task | ≤3 |

### Design Levers

| Lever | Description | Implementation |
|-------|-------------|----------------|
| **Time-to-Value Design** | Create "small success" in first 30 seconds to few minutes | Templates, demo data, guided tours |
| **Information Priority** | Main task front and center | Visual hierarchy, progressive disclosure |
| **Default Design** | Eliminate confusion | Recommended values, smart defaults |
| **Onboarding** | "Learn by doing" over explanations | Interactive tours |
| **Feedback** | Consistent action→response→result | Immediate UI response |
| **Perceived Speed** | Loading visibility | Skeleton screens, progressive display |

### Acceptance Criteria (Score 2)

- [ ] Entry to core task within 3 steps
- [ ] Primary button/next action is visually prioritized
- [ ] Empty state explains "what will happen/what to do next"
- [ ] Loading shows reason and progress

### Anti-Patterns

| Pattern | Description | Detection |
|---------|-------------|-----------|
| **Empty Landing** | Looks impressive but does nothing | Hero screen → nothing |
| **Choice Overload** | User bears burden of thinking | 5+ choices at same level |
| **Blind Failure** | Cause/next step unknown on failure | Dead end after error |

---

## Dimension 2: Agency (User Control & Autonomy)

### Definition

User can "choose", "decline", and "go back", not losing dignity in exchange for convenience.

### Temporal Position

**Progress** - Functions during progression.

### Core Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| Settings Reach Rate | Rate of reaching settings | Higher is better |
| Opt-out Rate | Notification OFF rate | Lower is better (high = design problem) |
| Undo Usage Rate | Undo/restore usage rate | Existence is important |
| Cancellation Ease | Cancellation completion rate | Equal ease to signup |

### Design Levers

| Lever | Description | Implementation |
|-------|-------------|----------------|
| **Consent Design** | Present purpose, benefit, alternative, revocation method | Clear consent flow |
| **Settings Center** | Adjustable notifications, privacy, personalization | Fine-grained control UI |
| **Reversibility** | Undo, drafts, restore, history, rollback | Operation history and undo stack |
| **Transparency** | Don't hide fees/conditions/limits/automation scope | Pre-disclosure |
| **Honest Choices** | Don't hide decline path | Equal visibility |
| **Easy Cancellation** | End as easily as start | Simple cancellation flow |

### Acceptance Criteria (Score 2)

- [ ] Important actions (delete/charge/publish) have preview and cancel path
- [ ] Permission requests (notification/location etc.) explain reason in context first
- [ ] Personalization/recommendations allow OFF/weak/strong choice (at least OFF)

### Anti-Patterns (Dark Patterns)

| Pattern | Description | Severity |
|---------|-------------|----------|
| **Confirmshaming** | Guilt-trip on decline | CRITICAL |
| **Roach Motel** | Easy to enter, hard to leave | CRITICAL |
| **Hidden Costs** | Fees revealed later | CRITICAL |
| **Trick Questions** | Confusing double negatives | HIGH |
| **Forced Continuity** | Hidden auto-renewal | HIGH |
| **Misdirection** | Visual manipulation of choice | HIGH |
| **Privacy Zuckering** | Data public by default | HIGH |

---

## Dimension 3: Identity (Self, Context, Belonging)

### Definition

Product fits as user's own tool rather than "someone's tool", giving continuity meaning.

### Temporal Position

**Continuation** - Functions during continued use.

### Core Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| Personalization Usage | Personalization usage rate | Exists and used |
| Retention | D1/D7/D30 retention | Industry benchmark +10% |
| Regret Rate | Regret rate (delete/report rate) | Lower is better |
| "My Tool" Sentiment | Do they say "my tool"? | Confirm in qualitative research |

### Design Levers

| Lever | Description | Implementation |
|-------|-------------|----------------|
| **Self-expression** | Profile, display name, icon, theme, sorting | Customization UI |
| **Context Adaptation** | Modes for beginner/expert, work/personal | Mode switching |
| **Language Personality** | Tone & manner, respect, distance, no shaming | Microcopy guide |
| **Community Design** | Participation barrier adjustment, anti-harassment, weak protection | Moderation |
| **Cultural Translation** | Understand memes without breaking them | Localization |

### Acceptance Criteria (Score 2)

- [ ] At least one setting where user can make it "their own"
- [ ] System messages don't attack user's character on failure
- [ ] Sharing/publishing defaults to private or has clear boundaries

### Anti-Patterns

| Pattern | Description | Detection |
|---------|-------------|-----------|
| **Forced Identity** | Real name required, excessive social integration forced | Required input fields |
| **Belonging Pressure** | Design makes not participating look like a loss | FOMO language |
| **Surface Culture** | Alienating with cringeworthy execution | Context-free memes |

---

## Dimension 4: Resilience (Recovery & Inclusion)

### Definition

User doesn't get stuck facing failure and uncertainty (connection, auth, input mistakes, errors, outages). System doesn't collapse under operation.

### Temporal Position

**Anytime** - Always functions (cross-cutting).

### Core Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| Crash-free Sessions | Crash-free session rate | 99.9%+ |
| Error Rate | Error occurrence rate | <5% common flows |
| Recovery Rate | Task completion rate after error | 90%+ |
| Support Classification | Support ticket classification (recovery path missing vs explanation missing) | Classify and improve |

### Design Levers

| Lever | Description | Implementation |
|-------|-------------|----------------|
| **State Design** | Clearly define loading/empty/error/offline/partial success | 5-state components |
| **Retry** | Retry, queue, backoff, resend | Auto-retry logic |
| **Data Protection** | Drafts, auto-save, idempotency | Local storage |
| **Observability** | Logs, traces, error IDs (connect to support) | Error ID display |
| **Accessibility** | Keyboard, contrast, screen reader, focus | WCAG 2.2 AA (ISO/IEC 40500:2025) — automated scanning via axe-core 4.10+ (https://github.com/dequelabs/axe-core/releases) |
| **Recovery UX** | Rescue for forgot password, device change, 2FA loss, billing trouble | Recovery flows |

### Acceptance Criteria (Score 2)

- [ ] Main flows have "connection failure branch" designed
- [ ] If dropped mid-input, can resume on return
- [ ] Errors show cause/impact/next step in human language
- [ ] Main operations completable by keyboard only (WCAG 2.2 SC 2.1.1)

### Five States Checklist

| State | Required | Description |
|-------|----------|-------------|
| **loading** | ✅ | Processing. Show reason and progress |
| **empty** | ✅ | No data. Guide next action |
| **error** | ✅ | Failure. Show cause, impact, next step |
| **offline** | ✅ | Offline. Guide limitations and recovery |
| **success** | ✅ | Success. Confirm result, present next choices |

### Anti-Patterns

| Pattern | Description | Detection |
|---------|-------------|-----------|
| **Infinite Loading** | No distinction between complete/fail | 30+ second spinner |
| **Silent Error** | Error not displayed | console.log only |
| **State Loss** | Back erases data | Form → back → empty |
| **Double Execution** | Same operation causes double processing | Button spam = duplicates |

---

## Dimension 5: Echo (Aftermath & Endings)

### Definition

At the exit of the experience, user's mind and body feel "settled". Achievement is not exaggerated, leaving closure, safety, and freedom for next. This supports long-term trust and return visits.

### Temporal Position

**Exit** - Functions at the exit of the experience.

### Core Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| Session End Satisfaction | Satisfaction at session end | Lightweight survey |
| Return Rate | Next day/week return | Healthy return (watch for over-dependence) |
| Regret Proxies | Immediate uninstall, immediate cancel, consecutive undo | Lower is better |
| Complaint Rate | Complaint rate | Lower is better |

### Design Levers

| Lever | Description | Implementation |
|-------|-------------|----------------|
| **Ending Design** | completion → confirmation → next choices → permission to rest | Completion screen design |
| **Summary** | Crystallize what was achieved briefly | Receipt/record/history |
| **Atmosphere** | Don't over-explain, but don't confuse | Progressive disclosure |
| **Symbols** | Consistent language, motion, sound (don't overdo) | Sound design |
| **Stopping Point** | Breaks for infinite scroll and binge watching | "Are you still watching?" |
| **Reminder Ethics** | Don't motivate through guilt | Neutral notification copy |

### Acceptance Criteria (Score 2)

- [ ] Core task completion shows both "result confirmation" and "next action", both choosable
- [ ] No forced flow to next (push) after completion
- [ ] Notifications and reminders have frequency adjust/stop/snooze

### Anti-Patterns

| Pattern | Description | Detection |
|---------|-------------|-----------|
| **Over-celebration** | Exaggerate achievement to exhaustion | 🎉🎊🎁 spam |
| **Never-ending** | No stopping point | Infinite scroll, autoplay |
| **FOMO Pressure** | Pressure with "miss out/falling behind" | "Only X hours left!", "Everyone's doing it" |

---

## Cross-Cutting Concerns

### AI/Automation Requirements

When including AI features, add these evaluations:

| Dimension | AI-Specific Requirement |
|-----------|------------------------|
| **A** Agency | Adjustable automation ON/OFF, strength, scope |
| **A** Agency | Pre-execution consent, post-execution history and undo |
| **R** Resilience | Don't get stuck on mistakes, hallucinations, misreasoning |
| **V** Value | Instantly understand what AI will do |
| **E** Echo | User finishes satisfied, not dependent on AI suggestions |

### Ambient AI Surfaces (2026)

By 2026, AI moved from "Chat with AI" buttons to ambient surfaces that appear when relevant and recede when not. V.A.I.R.E. evidence requirements when an ambient AI surface is present:

- **V (Value)** — the AI affordance appears *only when the user is doing something it can meaningfully accelerate* (Score 2+); always-on permanent chrome that adds noise without relevance = Score 1.
- **A (Agency)** — the user can dismiss / disable the surface globally, not only per-occurrence. "Turn it off" must be reachable in `≤ 2` clicks from the surface itself.
- **I (Identity)** — the AI does not speak in the brand's voice when it is uncertain. Confidence labels (`probably`, `not sure`) are preserved verbatim — never rewritten by the brand voice into false confidence.
- **R (Resilience)** — when the AI cannot answer, the surface degrades gracefully into the deterministic flow the user already knew, not a dead end.
- **E (Experience)** — the surface respects the user's flow: it does not interrupt focus mode, it does not animate into view during scroll, and its dismissal is *quiet* (no celebratory "got it!" theatre).

### Liquid Glass / Material 3 Expressive Surface Audits

When the design targets iOS 26+ (**Liquid Glass**) or Android (**Material 3 Expressive**):

- **V (Value)** — re-test legibility against the *dynamic* background, not a static frame. Liquid Glass tinting can drop contrast below the WCAG threshold on a previously-passing screen.
- **E (Experience)** — Material 3 Expressive's spring-based motion-physics is the *default*. Additional motion the team adds must justify itself against the platform baseline; ornamental motion is now extra noise on top of an already-physical interface.
- **R (Resilience)** — depth-aware materials behave differently under reduced-motion / reduced-transparency accessibility settings. Score the experience under those settings, not only the default.

### Always-On UI Requirements

When including notifications, widgets, voice UI:

| Requirement | Description |
|-------------|-------------|
| Interrupt Criteria | Urgency × Confidence × User state |
| Quiet Success | User doesn't get exhausted |
| Clear Stop | Snooze/stop is easy to find (Agency) |

### Trust-Critical Requirements

When including billing, cancellation, identity:

| Requirement | Description |
|-------------|-------------|
| Transparency | No hiding fees, conditions, renewal, cancellation method |
| Auth Recovery | Recovery when lost determines trust |
| Fraud Prevention Explanation | Friction requires explanation and rescue |

---

## Application Levels

| Level | Name | Applies To | Score Threshold |
|-------|------|---------|-----------------|
| **L0** | Minimum Viable VAIRE | All features | All dimensions ≥ 2 |
| **L1** | Standard | Main features (core flows) | All dimensions ≥ 2, 1+ at 3 |
| **L2** | Differentiation | Core experience, brand experience | Majority at 3 |

---

## Quick Reference Card

```
╔══════════════════════════════════════════════════════════════════╗
║                    V.A.I.R.E. QUICK REFERENCE                    ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  V = VALUE        | Can outcomes be reached in minimum time?     ║
║  A = AGENCY       | Can they choose, decline, go back?           ║
║  I = IDENTITY     | Does it become the user's own tool?          ║
║  R = RESILIENCE   | Does it not break, not block, allow recovery?║
║  E = ECHO         | Do they feel settled after completion?       ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  SCORE: 0=Not considered | 1=Partial | 2=Sufficient | 3=Exemplary║
║  PASS: All dimensions ≥ 2 | FAIL: Any dimension < 2              ║
╠══════════════════════════════════════════════════════════════════╣
║  NON-NEGOTIABLES:                                                ║
║  1. Location is known         6. Not just fast, but calming      ║
║  2. User has right to refuse  7. No deception (no dark patterns) ║
║  3. Can go back               8. Tolerates diversity             ║
║  4. Mistakes don't trap       9. Builds trust evidence           ║
║  5. Explanations are brief    10. Endings are designed           ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## Standards & Tools Reference (2025-2026)

| Standard / Tool | Status | Source |
|-----------------|--------|--------|
| WCAG 2.2 | ISO/IEC 40500:2025 (approved Oct 2025); authoritative current web accessibility standard | https://www.w3.org/WAI/news/2025-10-21/wcag22-iso/ |
| WCAG 3.0 | W3C Working Draft (Mar 2026); will not supersede WCAG 2 for several years after finalization | https://www.w3.org/WAI/news/2026-03-03/wcag3/ |
| EN 301 549 | Harmonized EU technical standard based on WCAG 2.1 AA; underpins EAA enforcement (active Jun 28, 2025) | https://www.etsi.org/deliver/etsi_en/301500_302000/301549/ |
| NN/G 10 Heuristics | Definitions refined Mar 2026 by Kate Moran & Feifei Liu; 10 heuristics themselves unchanged since 1994 | https://www.nngroup.com/articles/ten-usability-heuristics/ |
| Core Web Vitals | INP (≤200ms good) replaced FID as the interactivity Core Web Vital (Mar 2024); LCP + INP now Baseline Newly Available (Dec 2025) | https://web.dev/articles/inp |
| axe-core | v4.10 (latest); introduces HTML summary element rule; AI-assisted IGTs roadmapped for 2025 | https://docs.deque.com/axe-release-impact/4.10.0/en/release-notes/ |

> **Removed from scope**: FID (First Input Delay) — deprecated and removed from Core Web Vitals program March 2024, replaced by INP. Do not reference FID in Resilience performance scoring.
