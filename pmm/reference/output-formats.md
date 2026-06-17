# Output Formats Reference

**Purpose:** Templates for PMM's deliverables.
**Read when:** You are at POSITION/MESSAGE/GTM/ENABLE and need a deliverable template.

## Contents
- Positioning Statement
- Messaging House
- GTM Plan
- Launch Plan
- One-Pager (enablement)
- FAQ / Objection Handling
- Advisor Answer (ask)

Every format leads with customer value, grounds claims in shipped capability (evidence), names the target segment, carries confidence, and ends with "What I couldn't ground."

---

## Positioning Statement (default)

```markdown
## Positioning: [Product / Feature] — [Target Segment]

**Sources:** product truth (PDM: 12 Done), audience (Cast: "Security admin"), frame (Compete map)

> For **[target segment]** who **[JTBD]**, **[product]** is a **[category]**
> that **[key value/outcome]**. Unlike **[primary alternative]**, **[product]
> [differentiator]**.

**Differentiator grounding:** `audit/export.ts:22` — native SIEM export (Done, High)
**Category choice:** subsegment ("audit log for SOC 2 prep") — rationale: …
**Confidence:** High

### What I couldn't ground
- "real-time alerting" advantage — roadmap only, excluded.
```

---

## Messaging House

```markdown
## Messaging House: [Product] — [Segment]

**Core narrative:** [one-sentence promise]

| Value pillar | Benefit (outcome) | Proof point (evidence) | Status | Conf. |
|--------------|-------------------|------------------------|--------|-------|
| Audit-ready in minutes | trail on demand | `logger.ts:8` + `export.ts:22` | grounded | High |
| Works in your stack | no new tools | native Splunk/Datadog `export.ts:22` | grounded | High |

**Value-before-features check:** headlines are outcomes; features sit beneath as proof. ✅

### Dropped (unsubstantiated)
- "real-time threat alerts" — not shipped (roadmap). → offer PDM/Spark.
```

---

## GTM Plan

```markdown
## GTM Plan: [Product / Feature]

**ICP:** [segment + qualification signals] (source: Cast/Field)
**Beachhead → expansion:** [order]
**Positioning/message:** → see Positioning + Messaging House
**Launch tier:** Tier 2 — [one-line justification]

### Channel mix
| Channel | Why (segment is here) | Asset → owner |
|---------|----------------------|----------------|
| Technical blog | devs read it | post → Prose |
| Landing page | self-serve entry | LP → Funnel |

### Success signal
- Serves: [activation / pipeline / adoption] — KPI design deferred to Pulse.

### What I couldn't ground
- [missing input]
```

---

## Launch Plan

```markdown
## Launch Plan: [Feature] — Tier [N] — target T

**Narrative spine:** [one line] → handed to Saga to craft.
**Technical release:** paired to Launch (`PMM_TO_LAUNCH_HANDOFF`).

### T-minus timeline
| When | Asset / action | Owner / handoff | Depends on |
|------|----------------|-----------------|------------|
| T-2wk | Landing page | → Funnel | positioning |
| T-0 | Announce | PMM coordinates | all + deploy |

### Offers
- Narrative → Saga · LP → Funnel · slides → Stage · release → Launch
```

---

## One-Pager (enablement)

```markdown
## [Product] One-Pager — [Segment]

# [Outcome headline — value, not feature]
[one-sentence core narrative]

**Why it matters to you**
- [benefit] — *[proof point / evidence]*
- [benefit] — *[proof point / evidence]*

**How it works** (proof, kept secondary)
- [feature → so that → value]

**Best for:** [ICP]   **Not for:** [anti-ICP — honesty builds trust]

> Final copy polish → Prose. Competitive comparison → Compete.
```

---

## FAQ / Objection Handling

```markdown
## [Product] FAQ — [Segment]

**Q: [common objection]**
A: [grounded answer — capability + evidence; no overclaim]

**Q: How is this different from [alternative]?**
A: [Compete-grounded differentiation — if no Compete input, mark and offer handoff]
```

Objections must be answered from real capability. An objection PMM cannot answer truthfully is a product gap → surface it, do not spin it.

---

## Advisor Answer (ask)

Compact, per-turn (tier S):

```markdown
**Position the audit log for SOC 2 buyers on "audit-ready in minutes"** — grounded in native SIEM export (`export.ts:22`, Done). Differentiator vs export-less rivals (Compete). Confidence: High.

> Next: want the full messaging house for this segment, or the launch plan?
```
