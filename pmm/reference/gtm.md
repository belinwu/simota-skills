# Go-to-Market Reference

**Purpose:** ICP/segmentation, channel mix, launch tiers, and the T-minus launch timeline.
**Read when:** You are at GTM assembling how the product reaches the market.

## Contents
- GTM Plan Structure
- ICP & Segmentation
- Channel Mix
- Launch Tiers
- T-minus Launch Timeline
- Marketing Launch vs Technical Release
- Delegation Boundaries

---

## GTM Plan Structure

A GTM plan answers: *who* we sell to, *what* we say, *where* we reach them, *when* and at *what intensity* we launch. PMM owns who/what/where/intensity; the technical when (deploy) pairs to Launch.

```
GTM PLAN
├── ICP & segmentation        (who, in what order)
├── Positioning & message ref (what — from POSITION/MESSAGE)
├── Channel mix               (where the segment already is)
├── Launch tier               (intensity, justified)
├── T-minus timeline          (asset checklist + owners/handoffs)
└── Success signals           (which metric the launch serves — defer KPI design to Pulse)
```

---

## ICP & Segmentation

- **ICP (Ideal Customer Profile)**: the segment that gets the most value and is most reachable. Tie to a Cast/Field persona; do not invent.
- **Beachhead first**: sequence segments — one beachhead, then expansion. Resist "all segments at launch."
- **Qualification signals**: firmographic/behavioral traits that identify the ICP (company size, role, trigger event). Sourced, not assumed.

If no persona source exists → Ask First (define provisional ICP or request Cast/Field).

---

## Channel Mix

Match channels to **where the segment already is**, not to channels you like.

| Segment trait | Likely channels |
|---------------|-----------------|
| Developer / technical | docs, GitHub, dev communities, technical blog, Growth/SEO (GEO) |
| SMB self-serve | landing page (Funnel), paid search, lifecycle email |
| Enterprise / security buyer | sales enablement (one-pager, pitch), webinars, analyst/compliance proof |
| Existing users (expansion) | in-product, changelog, lifecycle (pair with Bond for retention) |

Each channel needs an asset → name the owning agent (LP → Funnel, SEO → Growth, slides → Stage, video → Cue/Director, narrative → Saga, copy → Prose). PMM assigns; the specialists build.

---

## Launch Tiers

Right-size the launch effort to the change. Justify the tier — over-launching a minor feature burns credibility; under-launching a major one wastes it.

| Tier | When | Typical scope |
|------|------|---------------|
| **Tier 1 — major** | new product, category move, flagship feature | full asset set, narrative, PR, sales enablement, exec involvement, coordinated date |
| **Tier 2 — standard** | notable feature, segment expansion | LP update, blog, email, in-product, social, one-pager |
| **Tier 3 — light** | minor feature, improvement | changelog, in-product note, optional social |

State the tier and the one-line justification at the top of the launch plan.

---

## T-minus Launch Timeline

A backward-planned asset checklist with owners and handoffs. Example Tier-2 shape:

```markdown
## Launch Timeline: [Feature] — Tier 2 — target date T

| When  | Asset / action                     | Owner / handoff        | Depends on        |
|-------|------------------------------------|------------------------|-------------------|
| T-3wk | Positioning + messaging house      | PMM                    | PDM ship-confirm  |
| T-2wk | Narrative / launch story           | → Saga                 | messaging house   |
| T-2wk | Landing page                       | → Funnel               | positioning       |
| T-1wk | Blog post + email copy             | → Prose                | messaging house   |
| T-1wk | Sales one-pager + FAQ              | PMM (→ Prose polish)   | messaging house   |
| T-1wk | Technical release readiness        | → Launch (paired)      | code Done (PDM)   |
| T-0   | Announce + publish                 | PMM coordinates        | all above + deploy|
| T+1wk | Capture feedback                   | → Voice                | live              |
```

Every row that is craft (narrative, LP, copy, slides, video) is a handoff, not PMM-executed. PMM owns the timeline and the strategy rows.

---

## Marketing Launch vs Technical Release

Keep them paired and distinct — this is the PMM↔Launch seam:

| | PMM (marketing launch) | Launch (technical release) |
|--|------------------------|----------------------------|
| Owns | tier, narrative, audience, channels, asset timeline | versioning, changelog, rollout, rollback, feature flags |
| Trigger | the market moment | the deploy |
| Failure mode | message lands flat / wrong audience | bad deploy / regression |

Coordinate the date via `PMM_TO_LAUNCH_HANDOFF`. PMM never sets the rollout/rollback; Launch never writes the positioning.

---

## Delegation Boundaries

| GTM need | Route to | Never do instead |
|----------|----------|------------------|
| Priority order of launches/segments | Rank | Score them yourself |
| KPI / metric definition + dashboard | Pulse | Define KPIs yourself |
| Competitive battle card for sales | Compete | Author the battle card yourself |
| Landing page build | Funnel / Bazaar | Build the page yourself |
| Channel SEO/CRO execution | Growth | Execute channel tactics yourself |
| Technical release mechanics | Launch | Plan versioning/rollout yourself |
| Market sizing / business case | Helm | Size the market yourself |
