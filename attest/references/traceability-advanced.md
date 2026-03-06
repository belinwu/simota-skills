# Advanced Traceability Techniques

Bidirectional traceability, automation, gap analysis, and coverage optimization.

---

## 1. Bidirectional Traceability (BDTM)

### Overview

```
Forward Traceability:
  Requirements -> Design -> Implementation -> Tests
  "Are all requirements implemented?"

Backward Traceability:
  Tests -> Implementation -> Design -> Requirements
  "Does all code/tests have a requirement justification?"

Bidirectional = Forward + Backward:
  - Detect unimplemented requirements (Forward Gap)
  - Detect code/tests without requirements (Backward Gap = Gold Plating)
```

### Bidirectional Mapping in Attest

| Direction | Mapping | Detected Issue |
|-----------|---------|---------------|
| **Forward** | AC-ID -> Implementation file:line -> Test file:line | Unimplemented criteria (FAIL) |
| **Backward** | Implementation file -> AC-ID | Implementation without requirement (Gold Plating) |
| **Test Forward** | AC-ID -> Test case | Untested criteria |
| **Test Backward** | Test case -> AC-ID | Tests without criteria (Orphan Test) |

### Output Format

```yaml
BIDIRECTIONAL_TRACEABILITY:
  forward:
    total_criteria: 12
    mapped_to_implementation: 10
    mapped_to_tests: 8
    gaps:
      - criterion_id: AC-LOGIN-007
        type: FORWARD_GAP
        description: "No implementation mapping"
      - criterion_id: AC-LOGIN-003
        type: TEST_GAP
        description: "Implementation exists, no tests"
  backward:
    orphan_implementations:
      - file: src/utils/legacyAuth.ts
        description: "Implementation not mapped to any criterion"
    orphan_tests:
      - file: test/deprecated.test.ts
        description: "Test not mapped to any criterion"
  coverage:
    implementation: 83%  # 10/12
    test: 67%           # 8/12
    full_chain: 67%     # Requirement -> Implementation -> Test complete chain
```

---

## 2. Gap Analysis

### 4 Gap Types

| Gap Type | Definition | Risk | Detection Method |
|----------|-----------|------|-----------------|
| **Implementation Gap** | No implementation for a criterion | High | Forward trace |
| **Test Gap** | Implementation exists but no tests | Medium-High | Forward trace |
| **Specification Gap** | Implementation exists but no criterion | Medium | Backward trace |
| **Coverage Gap** | Tests exist but are insufficient | Medium | Coverage analysis |

### Gap Priority Matrix

```
              Criterion exists   No criterion
Has impl      [Normal]           [Spec Gap]
              Has tests          -> Recommend adding spec
              No tests
              [Test Gap]

No impl       [Impl Gap]         [N/A]
              -> Add impl         Out of scope
```

### Gap Detection in AUDIT Mode

```
AUDIT mode additional analysis:
  1. Build Forward mapping: criteria -> implementation
  2. Build Forward mapping: implementation -> tests
  3. Build Backward mapping: tests -> criteria
  4. Classify each gap type
  5. Calculate coverage rates
  6. Generate gap report
```

---

## 3. Traceability Automation

### Automated Mapping Techniques

| Technique | Description | Accuracy | Use Case |
|-----------|-------------|----------|----------|
| **Naming convention** | Infer AC-ID from file/test names | High | When test names include AC-ID |
| **Comment/tag based** | Search for `@covers AC-LOGIN-001` tags | High | When tagging is enforced |
| **Pattern matching** | Match route/handler names with criterion keywords | Medium | When naming conventions are consistent |
| **Code search** | Grep for criterion keywords | Medium-Low | Fallback technique |
| **LLM inference** | AI matches code intent with criteria | Medium | When other methods are inconclusive |

### Recommended Tag Conventions

```
Code side:
  // @requirement AC-LOGIN-001
  // @covers AC-LOGIN-001, AC-LOGIN-002

Test side:
  describe('AC-LOGIN-001: Valid credentials grant access', () => { ... })
  // @criterion AC-LOGIN-001

Gherkin side:
  @AC-LOGIN-001
  Scenario: Successful login with valid credentials
```

---

## 4. Coverage Optimization

### Coverage Levels

| Level | Definition | Formula |
|-------|-----------|---------|
| **L1: Requirements Coverage** | Criteria mapped to implementation | Criteria with impl / Total criteria |
| **L2: Test Coverage** | Criteria mapped to tests | Criteria with tests / Total criteria |
| **L3: Full Chain Coverage** | Criteria -> impl -> test complete chain | Full chain criteria / Total criteria |
| **L4: Result Coverage** | Criteria with passing tests | PASS criteria / Total criteria |

### Coverage Thresholds

| Level | CERTIFIED | CONDITIONAL | REJECTED |
|-------|-----------|-------------|----------|
| L1 | >= 90% | >= 70% | < 70% |
| L2 | >= 80% | >= 60% | < 60% |
| L3 | >= 70% | >= 50% | < 50% |

---

## 5. Regulatory Traceability

Regulated industries (FDA 21 CFR Part 11, ISO 26262, DO-178C, ISO 29148) require bidirectional traceability and full chain coverage. Use AUDIT mode + L3 full chain coverage. Refer to each standard's documentation for detailed requirements.

---

## 6. Traceability Anti-Patterns

| Anti-Pattern | Symptom | Mitigation |
|-------------|---------|------------|
| **Manual-Only RTM** | Excel-managed, quickly becomes stale | Tag-based automated mapping |
| **One-Way Only** | Forward only, ignoring Backward | Require bidirectional tracing |
| **Snapshot RTM** | Created only at project start | Continuous updates (periodic AUDIT mode runs) |
| **Over-Granular** | Mapping every variable and line | Maintain criterion-level granularity |
| **Orphan Tolerance** | Allowing code without requirements | Report Backward Gaps as MEDIUM or above |
