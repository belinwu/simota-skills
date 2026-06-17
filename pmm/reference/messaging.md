# Messaging Reference

**Purpose:** The messaging house, proof-point grounding, and per-segment message variants.
**Read when:** You are at MESSAGE turning a position into what the product says.

## Contents
- The Messaging House
- Value Pillar → Proof Point Chain
- Proof-Point Grounding
- Value Before Features
- Per-Segment Variants
- Customer Language
- Messaging Output

---

## The Messaging House

A hierarchy that flows down from the positioning. Author top-down; verify bottom-up (every leaf grounded).

```
              CORE NARRATIVE  (one sentence: the promise to the segment)
             /        |        \
      VALUE PILLAR  VALUE PILLAR  VALUE PILLAR   (2-4 themes the segment values)
          |             |             |
       benefit       benefit       benefit       (the outcome of each pillar)
          |             |             |
     proof point    proof point   proof point     (the shipped capability that earns it)
          |             |             |
       feature       feature       feature        (the mechanism — support only)
```

- **Core narrative**: the single promise, derived from the positioning's value slot.
- **Value pillars**: 2-4 (more dilutes). Each is a reason-to-care, phrased as a customer outcome.
- **Proof points**: the evidence that the pillar is real — a shipped capability. **No pillar ships without ≥1 proof point.**

---

## Value Pillar → Proof Point Chain

Each pillar is only as strong as its proof. Build the chain explicitly:

```yaml
pillar: "Audit-ready in minutes, not weeks"
benefit: "Hand auditors a complete access trail on demand"
proof_point:
  capability: "Immutable append-only log + native SIEM export"
  evidence: "audit/logger.ts:8, audit/export.ts:22 (PDM: Done, High)"
  status: grounded        # grounded | partial | unsubstantiated
feature: "One-click Splunk/Datadog export"
```

`status: partial` (capability In-Progress/flagged) → soften the claim to match reality ("export to Splunk, with Datadog rolling out"), never overstate.
`status: unsubstantiated` (no shipped capability) → **drop the pillar or the claim**. Do not keep it as aspirational copy.

---

## Proof-Point Grounding

Inherited from PDM's evidence discipline. A message claim is a positive assertion about the product and must be backed:

| Claim type | Required grounding |
|-----------|--------------------|
| "We do X" | shipped capability + evidence (`file:line` / PDM `Done` row) |
| "Faster/cheaper/easier than Y" | a measure or a competitive frame (Compete), not adjective alone |
| "Customers achieve Z" | a Voice verbatim, case, or a defensible outcome chain — not invented |
| "Unlike competitors…" | Compete differentiation input |

If a claim cannot be grounded after checking PDM/Lens/Compete/Voice, mark it `Unsubstantiated` and exclude it. Surface excluded claims in "What I couldn't ground" so the team sees the gap (often a real roadmap signal → offer Spark/PDM).

---

## Value Before Features

Lead with the outcome; the feature is the proof, not the headline. The translation move:

```
feature              → "so that" →  value (the headline)
append-only log      → so that  →  "auditors trust the record hasn't been altered"
SIEM export          → so that  →  "your security team works in the tools they already use"
90-day retention     → so that  →  "you cover the full SOC 2 audit window"
```

Write the right column as the message; keep the left column as the proof line beneath it.

---

## Per-Segment Variants

The same product says different things to different segments — same proof points, different value emphasis.

| Segment | Leads with | De-emphasizes |
|---------|-----------|---------------|
| Security admin | compliance evidence, tamper-proof trail | setup speed |
| Engineering lead | native SIEM integration, low overhead | audit framing |
| Buyer/exec | SOC 2 readiness, risk reduction | implementation detail |

One messaging house per priority segment, or one house with a per-segment "leads with" row. Never a single message flattened across all.

---

## Customer Language

Use the segment's own words (Voice verbatims, Field research), not internal jargon. "Activity record auditors trust" beats "immutable event ledger" if that is how the buyer talks. Map internal feature names → customer language before shipping the message.

---

## Messaging Output

Feeds ENABLE and downstream handoffs (Saga to narrate, Funnel for the LP, Prose for copy). One house per segment:

```yaml
segment: "Security-conscious SaaS admin (SOC 2 prep)"
core_narrative: "Pass your access-review audit in an afternoon, not a sprint."
pillars:
  - pillar: "Audit-ready in minutes"
    benefit: "complete trail on demand"
    proof: "audit/logger.ts:8 + export.ts:22 (Done, High)"
    status: grounded
confidence: High
unsubstantiated_dropped: ["real-time threat alerting (roadmap, not shipped)"]
```
