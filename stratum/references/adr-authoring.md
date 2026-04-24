# ADR Authoring Reference

Purpose: Capture architecturally significant decisions as immutable, append-only records using Michael Nygard's ADR template (2011) or MADR (Markdown Any Decision Records). Each ADR documents context, decision, and consequences for one decision so future readers can reconstruct *why*, not just *what*. Stratum authors ADRs that embed into Structurizr workspaces via `!adrs`.

## Scope Boundary

- **stratum `adr`**: author and index ADRs for architecture decisions surfaced during C4 modeling. Produces Markdown ADR files plus index, embedding-ready for `!adrs` in Structurizr DSL.
- **stratum `model` / `c4` / `dsl` (elsewhere)**: model creation. ADRs record decisions made *while* modeling — invoke `adr` when a non-trivial choice (boundary, technology, pattern) needs preservation.
- **stratum `evaluate` (elsewhere)**: ATAM/SAAM evaluation surfaces decisions; this recipe records them.
- **atlas (elsewhere)**: dependency analysis. Atlas may *propose* an ADR (e.g., "break circular dep"), Stratum *authors* it.
- **magi (elsewhere)**: multi-perspective deliberation for hard tradeoffs. Magi decides; Stratum records the decision as an ADR.
- **accord (elsewhere)**: requirements/spec authoring. ADRs record architecture choices that *implement* requirements, not the requirements themselves.
- **scribe (elsewhere)**: HLD/LLD authoring. Scribe embeds approved ADRs into design documents; it does not author them.
- **ADR vs RFC**: RFC = *proposing* a change before consensus (open, comment-driven, may be rejected). ADR = *recording* a decision after consensus (immutable, append-only, supersedes via new ADR). Convert accepted RFCs into ADRs; never edit an accepted ADR.

## Workflow

```
TRIGGER   →  decision surfaces during MODEL/EVALUATE/DSL or via Atlas/Magi handoff
          →  confirm decision is architecturally significant (cost-of-change > trivial)

DRAFT     →  pick template (Nygard / MADR); fill Context → Decision → Consequences
          →  write Y-statement: "In <context>, facing <concern>, we decided <option>
              to achieve <quality>, accepting <downside>"

REVIEW    →  status=proposed; circulate to architects/team; capture pushback inline
          →  if rejected, mark status=rejected (keep file for audit); do not delete

ACCEPT    →  status=accepted; assign monotonic ID (NNNN-kebab-title.md); commit
          →  index update: append to adrs/README.md or log4brains-generated index

EVOLVE    →  superseding decision arrives → new ADR with status=accepted, links
              "Supersedes NNNN"; old ADR flips to status=superseded with back-link
          →  hand off to Structurizr DSL (!adrs adrs) for workspace embedding
```

## Templates

### Michael Nygard (2011) — minimum viable

| Section | Content |
|---------|---------|
| Title | `NNNN. <imperative phrase>` (e.g., `0007. Use PostgreSQL for primary store`) |
| Status | `proposed` / `accepted` / `deprecated` / `superseded by NNNN` |
| Context | Forces at play: business, technical, organizational. No decision yet. |
| Decision | Active voice, single sentence: "We will ..." |
| Consequences | Positive, negative, and neutral outcomes. Make tradeoffs explicit. |

### MADR 4.0 — extended

Adds sections for `Decision Drivers`, `Considered Options`, `Decision Outcome`, `Pros and Cons of the Options`, optional `Confirmation` and `More Information`. Use MADR when multiple options were weighed and the alternatives have ongoing value (e.g., reviewers may revisit). Use Nygard when the decision space is narrow and brevity wins.

### Nygard vs MADR — selection table

| Need | Pick |
|------|------|
| Single obvious decision, brief rationale | Nygard |
| Multiple credible options compared | MADR |
| Heavy compliance/audit context | MADR (drivers + confirmation) |
| Lightweight startup cadence | Nygard |
| Tooling: log4brains / adr-tools defaults | adr-tools = Nygard, log4brains = MADR-friendly |

## Status Lifecycle

```
                   ┌──────────┐
   draft  ───────► │ proposed │ ──reject──► rejected (terminal, kept for audit)
                   └────┬─────┘
                        │ accept
                        ▼
                   ┌──────────┐
                   │ accepted │ ──obsolete (no replacement)──► deprecated
                   └────┬─────┘
                        │ replaced by new ADR
                        ▼
                   ┌────────────┐
                   │ superseded │ (links forward to NNNN)
                   └────────────┘
```

Rules: ADRs are append-only. Never edit an accepted ADR's Decision or Consequences — write a superseding ADR. Status changes (accepted → superseded) are the only allowed mutations.

## Y-Statements (Olaf Zimmermann)

Compress the rationale into one sentence to surface the *why*:

> "In the context of **<use case / functional requirement>**, facing **<non-functional concern>**, we decided for **<chosen option>** and against **<alternatives>**, to achieve **<quality attribute>**, accepting **<downside / cost>**."

Use as the opening line of the Decision section. Forces explicit alternatives and explicit accepted downsides — both common omissions.

## Repository Organization

| Element | Convention |
|---------|------------|
| Path | `docs/adrs/` or `adrs/` (top-level if heavily referenced) |
| Filename | `NNNN-kebab-title.md` — zero-padded monotonic, e.g., `0042-adopt-event-sourcing.md` |
| Index | `adrs/README.md` table: ID, title, status, date. Auto-generated by log4brains. |
| Linking | Markdown relative links between ADRs; never renumber after acceptance. |
| Embedding | Structurizr DSL: `!adrs adrs` reads the directory, formats supported include adrtools, MADR, log4brains. |

## Tools

| Tool | Format | Strengths | When |
|------|--------|-----------|------|
| `adr-tools` (npryce) | Nygard | Bash CLI, minimal deps, `adr new`/`adr link` | Small repos, brevity-first |
| `log4brains` | MADR-flavored | Static-site index, decision-log timeline | Multi-team, browsable history |
| `adr-manager` (web) | MADR | GUI authoring, GitHub PR integration | Non-CLI authors |
| Structurizr `!adrs` | adrtools / MADR / log4brains | Native workspace embedding | Always — pair with chosen authoring tool |

## Anti-Patterns

- Editing an accepted ADR — destroys the audit trail. Always supersede with a new ADR; flip the old to `superseded`.
- Recording trivial decisions ("use 4-space indent") — clutters the log and devalues the format. Apply the cost-of-change test: would reversing this be cheap? If yes, it's not an ADR.
- ADR without Consequences — only documenting what was chosen, not the accepted downsides. Hides debt; future readers can't tell what was traded away.
- Renumbering ADRs after acceptance — breaks every external link, citation, and superseded-by reference. IDs are immutable.
- Mixing RFC and ADR roles — using "proposed" status for months of debate. RFC the proposal, then convert to ADR on acceptance. Long-running `proposed` ADRs are RFC misnamed.
- One ADR per pull request as a rule — couples decision rhythm to code rhythm. ADRs follow decision events, not commits.
- Deleting rejected ADRs — kept rejections explain why an option *isn't* the path; deleting them invites the same debate twice.
- Vague Y-statement — omitting alternatives or downsides ("we decided X to achieve quality"). Without the rejected options and accepted cost, the rationale is unfalsifiable.
- ADR as design doc — long prose, diagrams, code samples. ADRs record the decision; the design lives in HLD/LLD (Scribe). Keep ADRs under ~1 page.

## Handoff

- **To Stratum `dsl`**: ADR directory path + chosen format (adrtools/MADR/log4brains) for `!adrs` embedding in workspace.
- **To Atlas**: accepted ADRs that affect dependency structure (boundary changes, layer rules) — Atlas updates its constraint model.
- **To Scribe**: list of accepted ADRs to cite in HLD/LLD architecture sections; supply Y-statements as section openers.
- **To Magi**: ADRs in `proposed` status with stalled review — escalate for multi-perspective deliberation, return decision for `acceptance`.
- **To Accord**: ADRs that imply new functional/non-functional requirements — Accord folds them into the requirements package.
