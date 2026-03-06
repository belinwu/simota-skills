# Test Documentation Anti-Patterns

Purpose: Use this file when a test spec has weak coverage strategy, poor traceability, low signal, or excessive execution cost.

Contents:

- `TD-01` to `TD-07`
- additional planning pitfalls
- quality metrics
- review gates

## `TD-01` to `TD-07`

| ID | Anti-Pattern | Risk | Prevention |
|----|--------------|------|------------|
| `TD-01` | Only unit or only integration tests | Coverage imbalance | Follow the test pyramid. |
| `TD-02` | Wrong test type for the job | Slow and noisy feedback | Define purpose per test layer. |
| `TD-03` | Testing the wrong functionality | High-value paths remain under-tested | Prioritize by business impact and change frequency. |
| `TD-04` | Testing internal implementation | Refactors break tests needlessly | Test public behavior and observable outcomes. |
| `TD-05` | Coverage fetish | High numbers with weak signal | Measure meaningful coverage and mutation quality. |
| `TD-06` | Flaky or slow suites | CI distrust and ignored failures | Set execution budgets and fix flakes immediately. |
| `TD-07` | Treating test code as second class | Test debt grows fast | Review and refactor test code like production code. |

## Additional Planning Pitfalls

- Manual execution as the default
- Bug fixes without regression tests
- Dogmatic TDD where it hurts discovery
- Writing tests before reading framework guidance
- Accepting anti-test team culture
- Hard-coded test data instead of factories or fixtures

## Quality Metrics

| Metric | Meaning | Target |
|--------|---------|--------|
| `PDWT` | Percentage of defects found by written tests | `>= 70%` |
| `PBCNT` | Percentage of bugs caught by new tests | Track trend |
| `PTVB` | Percentage of tests validating business logic | `>= 60%` |
| `PTD` | Percentage of tests with documented intent and setup | `>= 80%` |

Recommended pyramid:

`Unit : Integration : E2E = 70 : 20 : 10`

Avoid:

- inverted pyramid (`E2E` dominant)
- diamond shape (integration dominant)

## Review Gates

Reject or revise the test spec if any are missing:

- explicit test type and scope
- setup and data preparation
- positive, negative, and boundary cases
- critical-path coverage
- expected result per test case
- traceability to requirement IDs
- failure escalation path

## Scribe Usage

Use this file during:

- `STRUCTURE` to balance test types
- `REVIEW` to check signal, speed, and traceability
- handoff to Radar or Voyager when test depth is unclear

Source:

- Codepipes, "Software Testing Anti-Patterns"
