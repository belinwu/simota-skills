# Criteria Extraction & Specification Quality

Patterns for extracting acceptance criteria, assessing specification quality, detecting requirement smells, and classifying testability.

---

## Source Format Detection

### Auto-Detection Rules

| Indicator | Detected Format | Confidence |
|-----------|----------------|------------|
| `## L3 受入基準` or `## Acceptance Criteria` heading | Accord L3 | HIGH |
| `## Functional Requirements` + numbered items | PRD/SRS | HIGH |
| `As a [role], I want [goal]` | User Story | HIGH |
| `MUST`, `SHALL`, `SHOULD` keywords (RFC 2119) | Formal Spec | MEDIUM |
| Unstructured prose with feature descriptions | Free-form | LOW |

### Confidence Threshold

- **HIGH** (>=0.8): Proceed with automatic extraction
- **MEDIUM** (0.5-0.8): Extract with AMBIGUOUS_FLAG on uncertain items
- **LOW** (<0.5): Flag SPEC_MISSING trigger, suggest Scribe/Accord

---

## Extraction Strategies by Format

### Accord L3 (Highest Fidelity)

Direct 1:1 mapping from Accord's acceptance criteria structure:

```
Source: ## L3 Acceptance Criteria (受入基準)
  → Each bullet = one AC
  → ID: AC-{feature}-{NNN}
  → Priority: inherit from Accord L1 priority
  → Testability: evaluate using Testability Matrix below
```

### PRD/SRS (Formal Requirements)

```
Source: ## Functional Requirements (機能要件)
  → Each FR-NNN item = one or more ACs
  → Split compound requirements (A and B → AC for A, AC for B)
  → MUST → CRITICAL, SHALL → HIGH, SHOULD → MEDIUM, MAY → LOW
  → Cross-reference with non-functional requirements for constraints
```

### User Stories

```
Source: "As a [role], I want [goal], so that [benefit]"
  → Primary AC from the "want" clause
  → Additional ACs from acceptance criteria bullets
  → Implicit ACs from "so that" (verify the benefit is achievable)
```

### Free-form Text

```
Strategy: NLP-based extraction
  1. Identify action verbs (create, display, validate, prevent, allow)
  2. Extract subject-verb-object triples
  3. Convert to testable assertions
  4. Flag all as PARTIALLY_TESTABLE until human confirms
```

---

## Testability Classification

| Classification | Definition | Action |
|---------------|------------|--------|
| **TESTABLE** | Clear input → expected output, measurable | Generate BDD directly |
| **PARTIALLY_TESTABLE** | Some aspects measurable, others subjective | Generate BDD for measurable parts, flag rest |
| **AMBIGUOUS** | Cannot determine expected behavior | Issue AMBIGUOUS_FLAG, request clarification |

### Testability Matrix

| Criterion Pattern | Testability | Example |
|-------------------|------------|---------|
| "When X happens, Y is displayed" | TESTABLE | Login error shows message |
| "Must complete within N seconds" | TESTABLE | API response < 200ms |
| "Should be user-friendly" | AMBIGUOUS | Vague UX requirement |
| "Must handle errors gracefully" | PARTIALLY_TESTABLE | "Gracefully" needs definition |
| "Data must be encrypted at rest" | TESTABLE | Verify encryption config |
| "Should feel responsive" | AMBIGUOUS | "Feel" is subjective |

---

## Dangerous Expression Catalog

Scan spec text for these patterns during INGEST. Each match triggers AMBIGUOUS_FLAG.

| Category | Dangerous Expressions | Problem | Fix Example |
|---------|----------------------|---------|-------------|
| **Subjective adjectives** | fast, easy, user-friendly, intuitive | No measurement basis | "Respond within 200ms" |
| **Vague adverbs** | quickly, efficiently, seamlessly | Not quantifiable | "Complete in 3 steps or fewer" |
| **Superlatives** | best, most efficient, highest quality | No comparison basis | "Meet SLA 99.9%" |
| **Comparatives** | better, faster, more reliable | Comparison target unknown | "50% faster than current P95" |
| **Loopholes** | if possible, as appropriate, when feasible | Ambiguous obligation | "Must implement" or remove |
| **Vague pronouns** | it, they, the system | Referent unclear | Use specific component name |
| **Undefined references** | "See related document", "As discussed" | Target missing/unknown | Specific document name + section |
| **Negations** | "not slow", "not complex" | Positive criterion unknown | "Response time under 500ms" |
| **Open-ended lists** | "etc.", "and so on", "among others" | Unbounded scope | Exhaustive enumeration |

---

## Requirement Smells (12 Categories)

| # | Smell Type | Definition | Severity | Frequency |
|---|-----------|------------|----------|-----------|
| 1 | **Ambiguity** | Multiple interpretations possible | High | High |
| 2 | **Verifiability** | Cannot be tested or verified | High | Medium |
| 3 | **Consistency** | Contradicts other requirements | High | Medium |
| 4 | **Completeness** | Missing necessary information | Medium-High | Medium |
| 5 | **Complexity** | Overly complex statement | Medium | High |
| 6 | **Correctness** | Factually incorrect | High | Low |
| 7 | **Traceability** | No link to parent requirement | Medium | Medium |
| 8 | **Understandability** | Difficult for reader to understand | Medium | Low |
| 9 | **Redundancy** | Duplicate of another requirement | Low | Medium |
| 10 | **Reusability** | Over-specialized, not reusable | Low | Low |
| 11 | **Relevancy** | Out of project scope | Low | Low |
| 12 | **Undefined** | Unclassifiable quality issue | Variable | Low |

---

## Acceptance Criteria Quality Patterns

### Good Criteria Traits (INVEST + SMART)

| Trait | Check |
|-------|-------|
| **Independent** | Can be verified alone |
| **Negotiable** | Describes WHAT, not HOW |
| **Valuable** | Clear user/business value |
| **Estimable** | Scope is well-defined |
| **Small** | Completable in one sprint |
| **Testable** | PASS/FAIL deterministic |

### Quality Anti-Patterns

| Pattern | Symptom | Fix |
|---------|---------|-----|
| Vague language | "Works fast" | Define numeric threshold |
| Too many criteria | 20+ per story | Split the story |
| Too few criteria | 1 per story | Add normal/error/boundary |
| Missing NFR | No perf/security criteria | Explicitly include NFR |
| Missing context | No user perspective | Add "As a [role]" |
| Implementation details | "Use React" | Describe WHAT, not HOW |

---

## Spec Quality Metrics

| Metric | Target |
|--------|--------|
| **Ambiguity Rate** (AMBIGUOUS / total) | < 10% |
| **Testability Rate** (TESTABLE / total) | > 80% |
| **Completeness Rate** (all aspects covered) | > 90% |
| **Defect Injection Rate** (requirement-origin bugs) | < 10% |

### Quality Score

```
GOOD: Ambiguity < 10%, Testability > 80%, Completeness > 90%
FAIR: Ambiguity < 20%, Testability > 60%, Completeness > 70%
POOR: Below FAIR thresholds → route to Scribe/Accord for improvement
```

---

## AMBIGUOUS_FLAG Protocol

When a criterion is AMBIGUOUS:

```yaml
AMBIGUOUS_FLAG:
  criterion_id: AC-LOGIN-005
  original_text: "The login should be fast"
  ambiguity_type: UNMEASURABLE | CONTRADICTORY | INCOMPLETE | SUBJECTIVE | OPEN_ENDED
  what_is_missing: "No latency threshold defined"
  suggested_clarification: "Login response time should be under 500ms at P95"
  impact: HIGH  # How much this ambiguity affects verification
  route_to: Scribe  # Who should clarify
```

---

## Criterion ID Convention

```
AC-{FEATURE}-{NNN}

Examples:
  AC-LOGIN-001    → Login feature, first criterion
  AC-PAYMENT-015  → Payment feature, fifteenth criterion
  AC-GLOBAL-001   → Cross-cutting requirement
```

### Priority Assignment

| Priority | Keywords | RFC 2119 | Impact |
|----------|----------|----------|--------|
| **CRITICAL** | "must", "required", "shall" | MUST, SHALL | System unusable without |
| **HIGH** | "should", "expected" | SHOULD | Major functionality affected |
| **MEDIUM** | "may", "desirable" | MAY | Quality of experience |
| **LOW** | "nice to have", "optional" | — | Enhancement |

---

## INGEST-Time Quality Check Flow

```
1. Dangerous expression scan → AMBIGUOUS_FLAG
2. Testability classification → TESTABLE / PARTIALLY_TESTABLE / AMBIGUOUS
3. Completeness check → normal/error/boundary criteria present?
4. Consistency check → cross-criterion contradiction detection (→ Contradiction probes)
5. NFR check → performance/security/accessibility criteria present?
6. Quality score → GOOD / FAIR / POOR
```

---

## Output Format

```yaml
EXTRACTED_CRITERIA:
  spec_source: "docs/login-spec.md"
  spec_format: ACCORD_L3 | PRD | USER_STORY | FREE_FORM
  extraction_confidence: 0.95
  spec_quality: GOOD | FAIR | POOR
  total_criteria: 12
  by_priority:
    CRITICAL: 3
    HIGH: 5
    MEDIUM: 3
    LOW: 1
  by_testability:
    TESTABLE: 8
    PARTIALLY_TESTABLE: 3
    AMBIGUOUS: 1
  criteria:
    - id: AC-LOGIN-001
      text: "Valid credentials grant access to dashboard"
      priority: CRITICAL
      testability: TESTABLE
      source: "login-spec.md:L24"
      related_criteria: [AC-LOGIN-002, AC-LOGIN-003]
  ambiguity_flags:
    - criterion_id: AC-LOGIN-005
      type: UNMEASURABLE
      suggestion: "Define latency threshold"
```
