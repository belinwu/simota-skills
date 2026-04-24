# Runbook Codification Reference

Purpose: Convert undocumented operational knowledge embedded in legacy code, oncall chat scrollback, and tribal lore into versioned, testable runbooks (Trigger / Steps / Verification / Rollback). Establishes freshness metrics so runbooks decay visibly, and integrates with Triage (incident response) and Mend (automated remediation) so codified procedures become executable workflows.

## Scope Boundary

- **fossil `runbook`**: codify operational procedures from code + chat + tribal sources into runbook documents with freshness metrics.
- **fossil `extract` / `assess` / `document` / `archive` (elsewhere)**: business-rule and risk archaeology. `runbook` is operational, not rule-focused.
- **fossil `bizrule` (elsewhere)**: rule triples. Runbooks may reference rule IDs but capture *operator* steps.
- **fossil `tribal` (elsewhere)**: human interviews. `tribal` supplies oral history; `runbook` formalizes it as procedure.
- **scribe (elsewhere)**: general document authoring. Use `runbook` when the artifact is an operational SOP with verification + rollback.
- **lens (elsewhere)**: code comprehension. Lens locates the conditional branches; `runbook` translates them into operator steps.
- **triage (elsewhere)**: live incident response. `runbook` produces the document Triage executes.
- **mend (elsewhere)**: automated remediation. `runbook` produces the human-grade procedure; Mend automates suitable ones.
- **beacon (elsewhere)**: SLO and alert design. Beacon defines when to alert; runbooks define what to do when alerted.

## Workflow

```
SCOPE       →  pick alert / failure modes lacking written procedure
            →  collect oncall chat scrollback, postmortems, ad-hoc scripts

DECOMPOSE   →  walk code paths triggered by the alert; map conditional branches
            →  each branch → procedural step with verification

DRAFT       →  fill Trigger / Steps / Verification / Rollback skeleton
            →  steps must be copy-pasteable; never assume tacit knowledge

VALIDATE    →  tabletop exercise with on-call engineer who has *not* run it
            →  if they get stuck, fix the runbook, not the engineer

ANNOTATE    →  attach freshness metadata: last-tested, last-fired, owner, expiry
            →  link to alert ID, related rule IDs, and known-failed scenarios

ROUTE       →  hand off automatable runbooks to Mend; manual ones stay in Triage
            →  schedule next review based on freshness policy
```

## Runbook Structure

```markdown
# RB-[NNN]: [Runbook Name]

- Trigger: [alert ID, error signature, customer signal, scheduled event]
- Severity: [SEV1 | SEV2 | SEV3]
- Owner: [team or named SME]
- Last-tested: YYYY-MM-DD
- Last-fired:  YYYY-MM-DD (count: N in last 90d)
- Expiry: YYYY-MM-DD (auto-stale if not re-tested by then)
- Related: [BR-NNN rule IDs, ADRs, prior postmortems]

## Steps
1. [imperative action] — expect: [observable outcome]
2. ...

## Verification
- [check 1: command / dashboard / metric to confirm recovery]
- [check 2: ...]

## Rollback
- Pre-conditions for rollback safety
- Step-by-step reversal
- Post-rollback verification

## Known Failure Modes
- [scenario] → [escalation path]
```

## Code-to-Runbook Conversion Patterns

| Code pattern | Runbook translation |
|--------------|---------------------|
| `if errCode == X` branch | Step: "Check error code; if X, go to step N" |
| Retry loop with backoff | Step: "Wait N min, retry up to M times before escalating" |
| Feature-flag toggle | Step: "Toggle flag `name` in [console]; verify propagation" |
| Cron / batch script | Trigger entry + verification of last-run timestamp |
| Database fix-up SQL in comments | Verification block + Rollback block (idempotent SQL) |
| Hardcoded customer-ID carve-out | Known Failure Mode entry referencing BR rule ID |
| Manual fix in oncall chat | Step transcribed verbatim; tag `tribal-source` until validated |

## Oncall-to-Runbook Conversion

1. Pull last 90 days of incident channels for the alert.
2. Cluster threads by symptom; pick the canonical resolution path.
3. Annotate divergent paths as Known Failure Modes.
4. Interview the most recent resolver (see `tribal-knowledge-interview.md` question bank).
5. Tabletop with a fresh engineer; iterate until they finish unaided.
6. Promote to active runbook only after one successful real-incident use.

## Freshness Metrics

| Metric | Definition | Stale threshold | Action |
|--------|------------|-----------------|--------|
| `last-tested` | Date of most recent tabletop or live execution | > 180 days | Schedule game-day |
| `last-fired` | Date alert last triggered | > 365 days unused | Review for relevance / archive |
| `time-to-resolve` | Median resolution time over recent firings | regression > 50% | Re-validate steps |
| `escalation-rate` | % of firings escalated past runbook | > 20% | Steps insufficient; revise |
| `expiry` | Hard expiry; runbook flagged stale until refreshed | reached | Block as authoritative |

Surface metrics in runbook header; stale runbooks are worse than missing ones because they invite false confidence.

## Integration with Triage and Mend

| Hand-off | Criteria | Owner |
|----------|----------|-------|
| → Triage | Runbook requires human judgment; rollback risk > automation tolerance | Triage executes during incident |
| → Mend | Steps are deterministic, verification automatable, rollback well-defined | Mend automates with safety-tier classification |
| → Beacon | Trigger ambiguous or noisy; tune alert before codifying | Fix detection first |
| Stay manual | Cross-team coordination, customer comms, irreversible action | Triage owns indefinitely |

Mend candidacy checklist: idempotent steps, machine-readable verification, single-command rollback, no human decision branches inside the procedure.

## Anti-Patterns

- Codifying steps without verification — operators cannot tell if recovery worked, so they retry blindly.
- Omitting rollback — half a runbook; turns recovery into a one-way door.
- Copying chat scrollback verbatim without tabletop — captures one engineer's path, not the canonical fix.
- Hiding freshness metadata — undated runbooks rot invisibly; treat undated == stale.
- Promoting tribal procedures straight to Mend automation — automating unvalidated steps amplifies blast radius.
- Single-author runbooks with no successor reviewer — bus factor of one; require second-pair-of-eyes signoff.
- Runbooks for alerts that should not exist — fix the alert (Beacon) before codifying noise.
- Steps that require tacit knowledge ("the usual cleanup") — opaque to fresh oncall; spell every command.
- Letting expired runbooks stay authoritative — auto-flag and demote on expiry; do not silently extend.

## Handoff

- **To Triage**: validated runbooks become first-response references; Triage logs every firing back into freshness metrics.
- **To Mend**: Mend-ready runbooks (idempotent + verifiable + reversible) → automated remediation candidates with safety-tier review.
- **To Beacon**: noisy or ambiguous triggers → alert refinement before further codification.
- **To Scribe**: customer-facing or audit-relevant procedures → polished SOP / compliance evidence.
- **To `tribal` recipe**: gaps surfaced during decomposition → interview targets.
- **To `bizrule` recipe**: branch decisions referencing business rules → cross-link via BR-IDs.
- **To Lens**: when conversion reveals unknown invocations, request a structure map before publishing the runbook.
