# Decision Templates

Output formats for variant selection, specification validation, and Arena session reporting.

---

## Selection Rationale Format

Use this format when documenting why a variant was chosen.

```markdown
### Variant Selection: [session_id]

**Mode:** [Solo / Team]
**Selected:** Variant [X] (Engine: [engine], Branch: arena/variant-[engine])
**Rejected:** Variant [Y] (Engine: [engine], Branch: arena/variant-[engine])

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

Use when validating specification quality before running engines.

```markdown
### Spec Validation: [spec_description]

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
**Mode:** [Solo / Team]

**Variants Executed:**
| Session ID | Engine | Branch | Winner | Cost Est. |
|------------|--------|--------|--------|-----------|
| [ID] | [engine] | arena/variant-[engine] | [yes/no] | [estimate] |

**Total Cost Estimate:** [Approximate]

**Final Implementation:**
- Selected: Variant [X] (Engine: [engine])
- Adopted via: `git merge arena/variant-[engine]`
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
- Session: [session_id] | Mode: [Solo/Team] | Engine: [engine(s)] | Variants: [N]
- Winner: Variant [X] (Score: [X.XX/5.00])
- Rationale: [One sentence]
- Files: [list]
- Cost: [estimate]
- Status: [PASS/FAIL/PENDING]
```

---

## Hybrid Variant Documentation

When the best solution combines elements from multiple variants.

```markdown
### Hybrid Selection: [session_id]

**Mode:** [Solo / Team]
**Base:** Variant [X] (Engine: [engine])
**Merged From:** Variant [Y] (Engine: [engine])

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

**Session:** [session_id]
**Mode:** [Solo / Team]
**Reason:** [Why automated selection is insufficient]

**Candidates:**

| Aspect | Variant A | Variant B |
|--------|-----------|-----------|
| Engine | [engine] | [engine] |
| Branch | arena/variant-[engine] | arena/variant-[engine] |
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
