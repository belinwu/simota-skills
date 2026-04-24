# Business Rule Mining (DRBM) Reference

Purpose: Decision Rule Business Mining (DRBM) — extract control-flow business rules from legacy code as condition/action/exception triples, validate against domain experts, and emit a Markdown rule registry. Goes beyond Fossil's default `extract` by formalizing rules as decision-table-ready structures rather than free-form catalog entries.

## Scope Boundary

- **fossil `bizrule`**: control-flow rule mining only. Output is a normalized triple registry (condition / action / exception) with provenance and decision-table compatibility.
- **fossil `extract` (default)**: broad rule extraction across code/tests/schema/comments/history. Use `bizrule` when the deliverable must feed a BRMS, decision table, or DMN model.
- **fossil `assess` / `archive` (elsewhere)**: risk and dead-code views. `bizrule` deliberately ignores dormant logic unless flagged for resurrection.
- **scribe (elsewhere)**: specification authoring. `bizrule` produces the rule list; Scribe formalizes it as a spec.
- **lens (elsewhere)**: code structure mapping. Lens answers "where is the logic"; `bizrule` answers "what does the logic decide".
- **triage (elsewhere)**: incident response. Rule mining is a planned excavation, not an outage activity.
- **mend (elsewhere)**: automated remediation. `bizrule` documents intent; Mend acts on alerts.

## Workflow

```
SCOPE      →  pick rule-bearing modules (validators, pricers, eligibility, workflow gates)
           →  declare rule scope: validation / calculation / routing / authorization

EXTRACT    →  walk conditionals, switch tables, guard clauses, magic constants
           →  for each branch, draft (Condition, Action, Exception) triple
           →  capture provenance: file:line, originating commit, owning test

NORMALIZE  →  collapse duplicate rules, separate intertwined rules, name each rule
           →  resolve overlapping predicates; flag mutually exclusive vs ordered

VALIDATE   →  cross-check against tests; if process logs exist, run process mining
           →  confirm with domain expert (sync or async questionnaire)
           →  mark unconfirmable rules SPECULATIVE

REGISTER   →  emit Markdown rule registry: stable IDs, triples, confidence, owners
           →  hand off to Scribe (spec), Builder (reimplementation), or BRMS import
```

## Condition / Action / Exception Triple

| Slot | Captures | Source signal |
|------|----------|---------------|
| Condition | Predicate that must hold | `if`, `when`, `case`, guard clauses, schema CHECK |
| Action | Decision or state change taken | assignment, return, emit, persist, route |
| Exception | Override / short-circuit / opt-out | early return, feature flag, role bypass, legacy customer ID list |

Every mined rule MUST populate all three slots. If Exception is "(none)" state it explicitly — empty fields hide unknowns.

## Rule Catalog (Registry) Template

```markdown
### BR-[NNN]: [Rule Name]
- Domain: [Pricing | Eligibility | Routing | Validation | Authorization]
- Condition: [predicate in domain language]
- Action: [decision taken when condition holds]
- Exception: [bypass / override / (none)]
- Source:
  - Code: `path/file.ext:LN` — [snippet]
  - Test: `tests/...::test_name`
  - History: `commit-sha` — [intent]
- Confidence: HIGH | MEDIUM | LOW | SPECULATIVE
- Owner / SME: [person or team, or UNKNOWN]
- Decision-table cell: [if applicable]
- Notes: [contradictions, temporal drift, kill-date]
```

## Mining Techniques

| Technique | Best for | Caution |
|-----------|----------|---------|
| AST predicate walk | Single-language monoliths with rich conditionals | Ignores DB-side rules (triggers, CHECK) |
| Decision-table reconstruction | Pricing matrices, eligibility tiers | Combinatorial explosion if predicates >5 |
| Process mining (event logs) | Workflow / approval flows with audit logs | Requires reliable event log; missing events = invisible rules |
| Test-as-truth back-derivation | Modules with strong characterization tests | Only as good as the test suite's coverage |
| Schema-side mining | CHECK constraints, triggers, computed columns | Often forgotten; rules here outlast app rewrites |
| Feature-flag inventory | Modern legacy with kill switches | Stale flags become permanent rules |

## ML-Aided / Process Mining Hooks

- **Decision Discovery (DMN-bound)**: feed event logs into pm4py / Disco / Celonis to derive decision points, then back-map to code.
- **Predicate clustering**: when 200+ similar `if` chains exist, cluster by predicate similarity to surface the underlying rule family before manual extraction.
- **LLM-assisted naming only**: use models to propose rule names, never to invent conditions. Hallucinated predicates corrupt the registry.

## Validation Loop

1. Mined triple → 2. Test confirms it → 3. SME confirms intent → 4. Promote confidence (HIGH).
- If any step fails: stay at LOW or SPECULATIVE; never silently upgrade.
- Re-mine after every major refactor; rule drift is the #1 source of regressions.

## Anti-Patterns

- Mining rules without recording provenance — rules without `file:line + commit` are unverifiable folklore.
- Treating every `if` as a business rule — most are technical guards (null checks, retries). Tag domain rules only.
- Skipping the Exception slot — exceptions encode the customer-specific carve-outs that survive every rewrite. Missing them is how migrations break VIP accounts.
- Mining only the happy path — error branches and rollback handlers carry compliance and refund rules.
- Letting the LLM invent predicates — model output is a naming aid, never a source of truth.
- Collapsing ordered rules into a flat list — order-sensitive rules (first-match wins) lose meaning when sorted alphabetically.
- Ignoring schema-side and trigger logic — DB-side rules outlive application code; missing them recreates bugs in the new system.
- Marking SME-unconfirmed rules HIGH — confidence requires triangulation; one source = LOW.
- Shipping the registry without owners — orphaned rules decay; every rule needs a named SME or `UNKNOWN` flag.

## Handoff

- **To Scribe**: rule registry → SRS / decision-table specification with SME-validated language.
- **To Builder**: HIGH-confidence triples → reimplementation guide; LOW/SPECULATIVE blocked pending validation.
- **To Shift**: registry feeds migration risk map; untested HIGH rules become characterization-test targets.
- **To Triage**: when an incident maps to a known BR-ID, reference the registry entry in the postmortem.
- **To Mend**: stable rules with clear rollback semantics become candidates for automated remediation runbooks.
- **To Lens**: if mining reveals unknown call sites, request a structure map before continuing.
