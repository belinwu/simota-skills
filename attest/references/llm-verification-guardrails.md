# LLM-Assisted Specification Verification

Capabilities, guardrails, and anti-patterns for using LLMs in specification compliance verification.

---

## Capability Tiers

### Tier 1: Reliable (Use Freely)

| Task | Method | Expected Quality |
|------|--------|-----------------|
| Ambiguity detection | Pattern scan + LLM reasoning | High (~89% precision per Paska tool research) |
| BDD scenario generation | Template + LLM expansion | High (structural templates constrain output) |
| Explanation generation | LLM prose from structured findings | High (translating structured data to natural language) |
| Testability evaluation | Keyword + LLM classification | High (well-defined classification criteria) |
| Dangerous expression scan | Catalog match + LLM context | High (catalog provides anchor patterns) |

### Tier 2: Assisted (Human Review Required)

| Task | Risk | Mitigation |
|------|------|------------|
| Code-spec compliance judgment | Hallucinated evidence references | Always verify file:line references exist. Cross-check with grep. |
| Implicit assumption inference | Over-inference from absent information | Prefix inferences with confidence level. Flag as MEDIUM confidence. |
| Contradiction detection | False contradictions from misunderstood context | Require 2+ supporting evidence points per contradiction. |
| Spec gap identification | Inventing requirements not implied by spec | Ground all suggested criteria in spec context or domain conventions. |

### Tier 3: Forbidden

| Task | Why Forbidden |
|------|--------------|
| AI-only CERTIFIED verdict | Compliance certification requires deterministic rule application, not probabilistic reasoning |
| FAIL based solely on LLM inference | Absence reasoning is hallucination-prone; absence must be confirmed by code search |
| Formal verification substitute | LLMs cannot provide mathematical guarantees |
| Verdict override without evidence | All verdict changes must cite file:line or spec:section evidence |

---

## Prompt Strategies by Phase

| Phase | Strategy | Why |
|-------|----------|-----|
| INGEST | Zero-shot with spec format examples | Format detection is well-defined; examples anchor classification |
| EXTRACT | Few-shot with criterion extraction examples | Extraction quality improves with format-specific examples |
| GENERATE | Template-constrained generation | Templates prevent structural drift; LLM fills domain-specific content |
| VERIFY | Chain-of-Thought with evidence chain | CoT forces explicit reasoning steps, making verification auditable |
| ATTEST | Rule-based (no LLM for verdict) | Verdict rules are mechanical thresholds; LLM generates explanation text only |

### Evidence Chain Pattern (VERIFY phase)

```
Step 1: Identify what the criterion requires (quote spec)
Step 2: Search for implementation artifacts (list search terms)
Step 3: For each finding, assess match quality (quote code)
Step 4: Determine verdict based on evidence completeness
Step 5: Assign confidence based on evidence directness
```

---

## Guardrail Rules

1. **Evidence-First**: Never state a verdict without file:line or spec:section reference. If no evidence found, verdict is NOT_TESTED or FAIL (absence), never inferred PASS.

2. **Confidence Gating**: When verification confidence < 0.5, automatically route to NOT_TESTED with runtime verification plan. Never escalate low-confidence to PASS.

3. **Hallucination Detection**: Cross-verify all LLM-generated file references with actual file reads. If a referenced file or line doesn't exist, flag as hallucination and re-verify.

4. **Dual Verification for CRITICAL**: For CRITICAL criteria, run verification reasoning twice with different prompt framings. Disagreement triggers manual review flag.

5. **Adversarial Self-Check**: After generating adversarial probes, verify each probe's spec gap claim against actual spec text. Remove probes where the spec actually addresses the concern.

---

## LLM-AQuA-DiVeR Pattern

Adapted from ICSE 2025 research for Attest's stakeholder communication:

**Explanation Assistant role** (used in compliance report):
- Translate technical findings to business-readable language
- Explain WHY a criterion failed, not just THAT it failed
- Provide concrete impact statements for each finding

**Refinement Assistant role** (used in AMBIGUOUS_FLAG suggestions):
- Generate specific, measurable replacement criteria for ambiguous specs
- Propose testable alternatives that preserve business intent
- Structure suggestions as before/after pairs for easy review

---

## Anti-Patterns

| Anti-Pattern | Description | Prevention |
|-------------|-------------|------------|
| **Confident Hallucination** | LLM states "implementation found at file:line" for non-existent code | Always verify references with actual file reads |
| **Over-Inference** | LLM infers complex behavior from simple code patterns | Require multi-point evidence for MEDIUM+ findings |
| **Spec Projection** | LLM adds requirements not in spec based on "common practice" | Ground all criteria in quoted spec text |
| **False Absence** | LLM claims feature missing when it exists under different name/pattern | Use multiple search strategies before declaring absence |
| **Verdict Inflation** | LLM tends toward PASS when evidence is ambiguous | Default to PARTIAL when evidence is incomplete |
