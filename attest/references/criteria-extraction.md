# Criteria Extraction Patterns

Patterns and strategies for extracting acceptance criteria from various specification formats.

---

## Source Format Detection

### Auto-Detection Rules

| Indicator | Detected Format | Confidence |
|-----------|----------------|------------|
| `## L3 受入基準` or `## Acceptance Criteria` | Accord L3 | HIGH |
| `## Functional Requirements` + numbered items | PRD/SRS | HIGH |
| `As a [role], I want [goal]` | User Story | HIGH |
| `MUST`, `SHALL`, `SHOULD` keywords (RFC 2119) | Formal Spec | MEDIUM |
| Unstructured prose with feature descriptions | Free-form | LOW |

### Confidence Threshold

- **HIGH** (≥0.8): Proceed with automatic extraction
- **MEDIUM** (0.5-0.8): Extract with AMBIGUOUS_FLAG on uncertain items
- **LOW** (<0.5): Flag SPEC_MISSING trigger, suggest Scribe/Accord

---

## Extraction Strategies by Format

### Accord L3 (Highest Fidelity)

Direct 1:1 mapping from Accord's acceptance criteria structure:

```
Source: ## L3 受入基準
  → Each bullet = one AC
  → ID: AC-{feature}-{NNN}
  → Priority: inherit from Accord L1 priority
  → Testability: evaluate using Testability Matrix below
```

### PRD/SRS (Formal Requirements)

```
Source: ## Functional Requirements / ## 機能要件
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

## AMBIGUOUS_FLAG Protocol

When a criterion is AMBIGUOUS:

```yaml
AMBIGUOUS_FLAG:
  criterion_id: AC-LOGIN-005
  original_text: "The login should be fast"
  ambiguity_type: UNMEASURABLE | CONTRADICTORY | INCOMPLETE | SUBJECTIVE
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

## Output Format

```yaml
EXTRACTED_CRITERIA:
  spec_source: "docs/login-spec.md"
  spec_format: ACCORD_L3 | PRD | USER_STORY | FREE_FORM
  extraction_confidence: 0.95
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
