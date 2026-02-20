# Vague Goal Handling

Framework for transforming ambiguous goals into actionable loop contracts.

## Goal Quality Assessment Matrix

| Grade | Signal | Action | Example |
|-------|--------|--------|---------|
| **Strong** | Objective is specific, ACs are measurable, verify command exists | Proceed to script generation | "Add JWT auth to /api/login with RS256 signing" |
| **Weak** | Objective exists but ACs lack verify commands or are partially subjective | Strengthen ACs using templates below, then proceed | "Add authentication" (no specifics on method or endpoints) |
| **Vague** | Objective uses generic verbs ("improve", "fix", "refactor") with no measurable outcome | Apply Three-Hypothesis Protocol before proceeding | "Make the app faster" |
| **Missing** | No goal.md or goal.md is empty/placeholder | Classify as CONTRACT_MISSING, request goal from user or Nexus | (empty file or "TODO: add goal") |

## Vague Goal Pattern Dictionary
### "improve X" / "make X better"
| # | Hypothesis | AC Template | Verify Command |
|---|-----------|-------------|----------------|
| 1 | Performance: X has measurable latency/throughput regression | Response time < Nms at P95 | `k6 run load-test.js --summary-trend 'http_req_duration:p(95)<N'` |
| 2 | Quality: X has lint/type/test failures | All checks pass | `npm run lint && npm test` |
| 3 | Readability: X has complexity/duplication issues | Complexity score reduced | `npx jscpd --threshold 5 src/X/` |

### "fix tests" / "fix CI"
| # | Hypothesis | AC Template | Verify Command |
|---|-----------|-------------|----------------|
| 1 | Specific test file(s) failing | Named test files pass | `npm test -- --testPathPattern='<failing>'` |
| 2 | Environment/config issue | Full test suite passes in clean env | `npm ci && npm test` |
| 3 | Flaky test (intermittent) | Test passes 5 consecutive runs | `for i in {1..5}; do npm test || exit 1; done` |

### "refactor X"
| # | Hypothesis | AC Template | Verify Command |
|---|-----------|-------------|----------------|
| 1 | Extract module: X is a God class/file | X split into ≤N files, each <200 lines | `wc -l src/X/*.ts` |
| 2 | Remove duplication: X has copy-paste code | Duplication score < 5% | `npx jscpd src/X/` |
| 3 | Simplify interface: X has too many exports | Public API reduced to ≤N exports | `grep -c '^export' src/X/index.ts` |

### "clean up X"
| # | Hypothesis | AC Template | Verify Command |
|---|-----------|-------------|----------------|
| 1 | Dead code removal | No unused exports | `npx ts-prune src/X/` |
| 2 | Formatting/lint compliance | Zero lint errors | `npx eslint src/X/ --max-warnings 0` |
| 3 | Dependency cleanup | No unused dependencies | `npx depcheck` |

### "make it faster" / "optimize"
| # | Hypothesis | AC Template | Verify Command |
|---|-----------|-------------|----------------|
| 1 | Bundle size reduction | Bundle < N KB | `npm run build && du -sh dist/` |
| 2 | Runtime performance | Benchmark < Nms | `npm run bench` |
| 3 | Startup time | Cold start < Ns | `time node dist/index.js --dry-run` |

## Three-Hypothesis Protocol

When goal quality is **Vague**:

1. **Infer context** (see Non-Ask-First Rule below)
2. **Generate 3 hypotheses** from the Pattern Dictionary above
3. **Rank by evidence** — use inference results to identify the most likely hypothesis
4. **Present to user** — propose the top hypothesis as default, list alternatives:
   ```
   Goal "fix tests" detected as Vague. Based on CI logs, 3 test files are failing.
   Proposed contract:
     Objective: Fix 3 failing test files in src/__tests__/
     AC: npm test exits 0 with all 3 files passing
     Verify: npm test -- --testPathPattern='(auth|user|payment)'
   Alternatives:
     H2: Full environment reset (npm ci && npm test)
     H3: Flaky test stabilization (5 consecutive passes)
   Proceed with H1? [Y/n]
   ```
5. **If user confirms or no response within context** → proceed with top hypothesis
6. **If user selects alternative** → adjust contract accordingly

## AC Strengthening Templates

Transform vague ACs into measurable ones:

| Vague AC | Measurable AC | Verify Command |
|----------|--------------|----------------|
| "Code is clean" | Zero lint errors, zero type errors | `npm run lint && tsc --noEmit` |
| "Tests pass" | All test suites exit 0, coverage ≥ N% | `npm test -- --coverage --coverageThreshold='{"global":{"lines":N}}'` |
| "Performance is good" | P95 latency < Nms under M concurrent users | `k6 run --vus M --duration 30s load-test.js` |
| "No regressions" | All existing tests pass, no new lint warnings | `npm test && npm run lint -- --max-warnings 0` |
| "UI looks correct" | Visual regression diff < 0.1% | `npx playwright test --project=visual` |
| "Works on mobile" | Lighthouse mobile score ≥ 90 | `npx lighthouse --preset=desktop --output=json URL` |
| "Handles errors" | All error paths return correct HTTP status | `npm run test:error-paths` |
| "Is accessible" | Zero axe-core violations | `npx playwright test --project=a11y` |

## Non-Ask-First Rule

Before asking the user to clarify a vague goal, **attempt inference** from available sources:

| Source | What to Look For | Inference |
|--------|-----------------|-----------|
| `git log --oneline -20` | Recent commit messages mentioning the goal topic | Scope and intent of recent work |
| `package.json` scripts | Available test/lint/build commands | Verify command candidates |
| CI config (`.github/workflows/`) | Failing checks, test commands | Which checks are broken |
| `runner.log` (if exists) | Previous failure patterns | Root cause of "fix" goals |
| `progress.md` (if exists) | Previous iteration outcomes | What was already attempted |
| Test output (`npm test 2>&1`) | Specific failing tests | Exact scope of "fix tests" |

**Rule:** Exhaust at least 3 inference sources before asking. If inference yields a Strong hypothesis (≥2 sources agree), proceed without asking. **Exception:** If the inferred scope is large (>10 files, >3 acceptance criteria) or irreversible, confirm with user regardless.
