# Decision Templates

Output formats for variant selection, specification validation, and Arena session reporting.

---

## Selection Rationale Format

Use this format when documenting why a variant was chosen.

```markdown
### Variant Selection: [run_id]

**Selected:** Variant [X] (Engine: [engine])
**Rejected:** Variant [Y] (Engine: [engine])

**Rationale:**
- Correctness: [Score] - [Comment]
- Code Quality: [Score] - [Comment]
- Performance: [Score] - [Comment]
- Safety: [Score] - [Comment]
- Simplicity: [Score] - [Comment]

**Decisive Factor:** [The single most important reason for selection]

**Trade-offs Accepted:**
- [What was sacrificed and why it's acceptable]

**Preservation Notes:**
- [Ideas from rejected variants worth remembering for future work]
```

---

## Specification Validation Report

Use after `aiw spec critique` to document specification quality.

```markdown
### Spec Validation: [spec_file]

**Overall Quality:** [Good / Needs Revision / Insufficient]

**Ambiguities Found:**
1. [Ambiguity description] - Severity: [High/Medium/Low]
   - Suggested clarification: [How to resolve]
2. [Ambiguity description] - Severity: [High/Medium/Low]
   - Suggested clarification: [How to resolve]

**Missing Elements:**
- [ ] [Missing element 1]
- [ ] [Missing element 2]

**Recommendation:** [Proceed / Revise before running / Generate spec variants]
```

---

## Session Summary Format

Use at the end of an Arena session to summarize all activity.

```markdown
### Arena Session Summary

**Task:** [Task description]
**Date:** [YYYY-MM-DD]

**Runs Executed:**
| Run ID | Engine(s) | Variants | Winner | Cost |
|--------|-----------|----------|--------|------|
| [ID] | [engines] | [N] | [variant] | [cost] |

**Total Cost:** [Amount]

**Final Implementation:**
- Selected: [Variant ID from Run ID]
- Files Changed: [count] files
- Test Status: [PASS/FAIL]

**Key Learnings:**
- [Learning 1 - e.g., engine performance observation]
- [Learning 2 - e.g., spec pattern insight]
```

---

## AUTORUN Compact Report

Abbreviated format for Nexus autonomous mode. Omit verbose explanations.

```markdown
## Arena Result
- Run: [run_id] | Engine: [engine] | Variants: [N]
- Winner: Variant [X] (Score: [X.XX/5.00])
- Rationale: [One sentence]
- Files: [list]
- Cost: [amount]
- Status: [PASS/FAIL/PENDING]
```

---

## Hybrid Variant Documentation

When the best solution combines elements from multiple variants.

```markdown
### Hybrid Selection: [run_id]

**Base:** Variant [X] (Engine: [engine])
**Merged From:** Variant [Y]

**What was taken from each:**
| Element | Source | Reason |
|---------|--------|--------|
| [Component/approach] | Variant [X] | [Why this part is better] |
| [Component/approach] | Variant [Y] | [Why this part is better] |

**Integration Notes:**
- [How the parts were combined]
- [Any conflicts resolved during merge]

**Verification:**
- [ ] Combined implementation passes all tests
- [ ] No conflicts between merged approaches
- [ ] Performance is not degraded by combination
```

---

## Escalation Report

When Arena cannot make a clear selection and needs user input.

```markdown
### Escalation: Variant Selection Required

**Run:** [run_id]
**Reason:** [Why automated selection is insufficient]

**Candidates:**

| Aspect | Variant A | Variant B |
|--------|-----------|-----------|
| Score | [X.XX] | [X.XX] |
| Approach | [Brief] | [Brief] |
| Strength | [Key advantage] | [Key advantage] |
| Weakness | [Key disadvantage] | [Key disadvantage] |

**Arena's Lean:** Variant [X] (confidence: [Low/Medium])
**Decisive Question:** [What information would resolve this?]

**Options:**
1. Adopt Variant [A] - [one-line rationale]
2. Adopt Variant [B] - [one-line rationale]
3. Hybrid approach - combine best of both
4. Re-run with refined spec
```
