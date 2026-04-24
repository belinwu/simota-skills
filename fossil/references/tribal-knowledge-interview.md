# Tribal Knowledge Interview Reference

Purpose: Capture undocumented "why this exists" knowledge from original implementers, retired engineers, and long-tenured operators through semi-structured interviews. Preserves oral history before it vanishes, applies Chesterton's fence to candidate-deletion code, and produces a knowledge-transfer ceremony that converts memory into durable artifacts.

## Scope Boundary

- **fossil `tribal`**: human-source archaeology only — interviews, retired-engineer outreach, oral history. Output: annotated transcripts + rule-intent register.
- **fossil `extract` / `assess` / `document` / `archive` (elsewhere)**: code/test/schema-side archaeology. Use `tribal` when code analysis stalls because intent is irrecoverable from artifacts alone.
- **fossil `bizrule` (elsewhere)**: code-derived rule triples. `tribal` supplies the *why* that `bizrule` cannot infer.
- **scribe (elsewhere)**: spec authoring. `tribal` collects raw intent; Scribe formalizes it.
- **lens (elsewhere)**: code comprehension. Lens explains structure; `tribal` explains motive.
- **triage (elsewhere)**: incident response. Tribal interviews are scheduled, not reactive.
- **mend (elsewhere)**: automated remediation. Mend executes; `tribal` reconstructs original intent so Mend doesn't automate the wrong thing.
- **researcher (elsewhere)**: end-user research. `tribal` targets internal builders/operators, not users.

## Workflow

```
IDENTIFY   →  list candidates: original committers, retired engineers, oncall veterans
           →  rank by recency, criticality of code owned, departure risk

OUTREACH   →  warm intro via current manager / HR alumni network
           →  set expectations: 60-90 min, recorded, attributed unless requested otherwise

PREP       →  pre-read code under investigation, draft question bank per module
           →  pre-share top 3 questions; respect interviewee's time

INTERVIEW  →  semi-structured: open "why" questions, follow the energy, never lead
           →  capture stories, not just facts — narrative encodes context

CHESTERTON →  for every "remove this?" candidate, locate the original reason before deciding
           →  if no reason found, mark UNKNOWN-FENCE, do not delete

CEREMONY   →  knowledge-transfer session: interviewee + 2-3 successors + recorder
           →  produce annotated walkthrough; archive recording + transcript

REGISTER   →  feed intents into rule registry as Notes / Owner / History fields
           →  flag rules now lacking a living SME
```

## Question Bank — "Why This Exists"

| Lens | Question template | What you're really asking |
|------|-------------------|---------------------------|
| Origin | "What problem did this solve when you wrote it?" | Surface the original requirement |
| Counterfactual | "What would have broken if you hadn't added it?" | Tests whether rule still applies |
| Context | "Who asked for it, and what were they worried about?" | Names the stakeholder + risk |
| Exception | "Which customer / case forced the carve-out?" | Recovers VIP / regulatory exceptions |
| Workaround | "What were you working around?" | Identifies upstream bug now possibly fixed |
| Decision | "What did you almost do instead, and why didn't you?" | Captures rejected alternatives (ADR-grade) |
| Drift | "Has the reason for this changed since then?" | Checks rule still earns its keep |
| Successor | "Who would know this if you weren't here?" | Maps remaining tribal-knowledge holders |

## Retired-Engineer Outreach Playbook

| Step | Action | Cautions |
|------|--------|----------|
| 1 | Confirm contact path through HR alumni / LinkedIn | Never contact via personal accounts without consent |
| 2 | State purpose, scope, and time ask up-front | Avoid open-ended "pick your brain" framing |
| 3 | Offer compensation / acknowledgement | Many alumni decline pay but accept attribution |
| 4 | Send 3 specific code snippets + 3 questions | Specificity respects time and surfaces memory |
| 5 | Record only with explicit consent | NDAs may still apply; verify with legal |
| 6 | Share back the captured artifact | Builds trust for follow-ups |

## Chesterton's Fence Rule

> "Do not remove a fence until you know why it was put up."

Application checklist for every deletion candidate:

1. Locate originating commit + author.
2. Read commit message, PR, linked issue.
3. If author reachable → ask. If not → search inbox, chat archives, postmortems.
4. If after reasonable search no reason is found → mark `UNKNOWN-FENCE`, retain code, add probe to verify dead-ness over N release cycles.
5. Only after probe confirms zero invocation → propose deletion with full audit trail.

Skipping any step turns Fossil into a regression generator.

## Knowledge-Transfer Ceremony Format

| Phase | Duration | Output |
|-------|----------|--------|
| Walkthrough | 30 min | Recorded screen-share + narration |
| Q&A | 20 min | Successor questions → transcript |
| Pair-write | 20 min | Successor drafts summary; original corrects |
| Sign-off | 10 min | Both sign annotated doc; archive in `.agents/fossil-tribal/` |

Two successors minimum — single-successor handoffs reintroduce the bus factor you just paid to remove.

## Anti-Patterns

- Conducting interviews without pre-read — wastes the interviewee's time and surfaces only generic memories.
- Leading questions ("you added this for compliance, right?") — primes recall and corrupts the record.
- Capturing facts without stories — narrative context is what makes the fact useful 5 years later.
- Treating one interview as ground truth — memory drifts; corroborate with code, tests, and a second source.
- Deleting code because "no one remembers why" — that is precisely Chesterton's fence; mark UNKNOWN-FENCE and probe.
- Skipping recording / transcript — the artifact is the deliverable; ephemeral chat does not preserve oral history.
- Single-successor ceremonies — re-creates the bus factor; require ≥2 listeners.
- Promising anonymity then attributing — destroys trust for all future outreach.
- Ignoring operators and SREs — long-tenured oncall staff hold runbook intent that engineers never wrote down.

## Handoff

- **To Scribe**: validated intent + ADR-grade rejected alternatives → spec / decision record.
- **To Triage**: oncall narratives with incident pointers → postmortem retro-fits.
- **To Mend**: confirmed remediation patterns from operator interviews → automated runbook candidates.
- **To Lens**: when interview reveals unknown call paths or hidden integrations, request structure map.
- **To `runbook` recipe**: operator interviews → seeded runbook drafts.
- **To `bizrule` recipe**: rule-intent answers populate the Owner/SME and Notes slots in the registry.
