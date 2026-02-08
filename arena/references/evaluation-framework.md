# Evaluation Framework

Quality metrics, scoring methodology, and comparison report templates for variant evaluation.

**Pipeline position:** This framework covers the REVIEW → EVALUATE stages of the Arena workflow:
- Solo Mode: `SPEC → SCOPE LOCK → EXECUTE → **REVIEW → EVALUATE** → ADOPT → VERIFY`
- Team Mode: `SPEC → DESIGN → SPAWN → COMPETE → **REVIEW → EVALUATE** → ADOPT → CLEANUP`

---

## Variant Scoring Matrix

| Criterion | Weight | Score (1-5) | Weighted | Description |
|-----------|--------|-------------|----------|-------------|
| Correctness | 40% | | | Meets specification requirements completely |
| Code Quality | 25% | | | Readability, maintainability, idiomatic patterns |
| Performance | 15% | | | Efficiency, resource usage, scalability |
| Safety | 15% | | | Error handling, input validation, security |
| Simplicity | 5% | | | Avoids over-engineering, minimal complexity |
| **Total** | 100% | | | |

### Score Definitions

| Score | Label | Meaning |
|-------|-------|---------|
| 5 | Excellent | Exceeds requirements, best-in-class |
| 4 | Good | Meets all requirements with minor room for improvement |
| 3 | Adequate | Meets core requirements, some gaps |
| 2 | Below Average | Partial implementation, notable issues |
| 1 | Poor | Fails to meet requirements |

### Weight Adjustment Guidelines

Default weights work for most scenarios. Adjust when:

| Scenario | Adjustment |
|----------|------------|
| Security-critical code | Safety: 30%, Code Quality: 20% |
| Performance-sensitive path | Performance: 30%, Simplicity: 0% |
| Prototype / exploration | Simplicity: 15%, Performance: 5% |
| Legacy codebase integration | Code Quality: 35%, Correctness: 30% |

---

## Post-Completion Review Checklist (MANDATORY)

After each variant completes execution, Arena MUST run this review checklist **before** proceeding to comparative evaluation. This is a quality gate — no variant enters EVALUATE without a completed review.

### Review Steps (run on each variant)

| # | Check | Command / Method | Result | Severity |
|---|-------|------------------|--------|----------|
| 1 | **Scope Validation** | `git diff --name-only $BASE_COMMIT..arena/variant-{engine}` | PASS if only allowed files modified | **CRITICAL** — revert unauthorized files |
| 2 | **Build Verification** | Run project build command (e.g., `npm run build`, `go build ./...`) | PASS / FAIL / SKIP (no build configured) | **CRITICAL** — FAIL = disqualify |
| 3 | **Test Execution** | Run project test command (e.g., `npm test`, `pytest`, `go test ./...`) | PASS / FAIL / SKIP (no tests configured) | **HIGH** — FAIL = penalize Correctness |
| 4 | **Automated Code Review** | `codex review --uncommitted` | Summary of findings | **MEDIUM** — feeds Code Quality & Safety |
| 5 | **Acceptance Criteria** | Read implementation, check each criterion from spec | Met / Unmet per criterion | **HIGH** — all unmet = disqualify |

**Execution order matters:** Scope → Build → Test → Review → Acceptance. If Build fails, skip remaining checks (variant is already disqualified).

### Solo Mode Review

Arena leader runs the checklist **after each engine commits**, before moving to the next variant or EVALUATE:

```bash
# After codex variant commits:
git checkout arena/variant-codex

# 1. Scope check
git diff --name-only $BASE_COMMIT..HEAD
# Compare against allowed_files, revert any violations

# 2. Build
npm run build  # or project-specific build command

# 3. Test
npm test  # or project-specific test command

# 4. codex review
codex review --uncommitted

# 5. Acceptance criteria — Read files, verify spec requirements
# Record all results before moving to gemini variant
```

### Team Mode Review

Arena leader runs the checklist **after all subagents complete and report back**. Use the worktree directories or checkout each branch:

```bash
# Review variant-codex (using worktree if still available, or checkout)
cd /tmp/$SESSION_ID/variant-codex  # or: git checkout arena/variant-codex

# Run the same 5-step checklist
# Repeat for variant-gemini
```

### Review Result Template

Record results for each variant using this structure:

```yaml
review_result:
  variant: "arena/variant-{engine}"
  engine: "{codex | gemini}"
  checks:
    scope:
      status: PASS | FAIL
      unauthorized_files: []  # Files that were reverted
      notes: ""
    build:
      status: PASS | FAIL | SKIP
      error_output: ""  # First 10 lines of error if FAIL
    test:
      status: PASS | FAIL | SKIP
      passed: 0
      failed: 0
      skipped: 0
      failure_summary: ""  # Key failures if any
    codex_review:
      findings_count: 0
      critical_findings: []  # Security, correctness issues
      quality_findings: []   # Style, maintainability issues
    acceptance_criteria:
      - criterion: "[From spec]"
        met: true | false
        evidence: "[How verified]"
  overall_verdict: PASS | FAIL | WARN
  disqualified: false
  disqualification_reason: ""  # If disqualified
```

### Disqualification Rules

| Condition | Verdict | Action |
|-----------|---------|--------|
| Build fails | **DISQUALIFY** | Variant cannot be adopted; skip remaining checks |
| Scope violation (core logic in forbidden files) | **DISQUALIFY** | Cannot revert without breaking implementation |
| All acceptance criteria unmet | **DISQUALIFY** | Engine did not address the spec |
| Scope violation (reverted successfully) | **WARN** | Note violation, deduct from Code Quality score |
| Some tests fail | **WARN** | Penalize Correctness score; still evaluate |
| codex review finds critical issues | **WARN** | Penalize Safety score; still evaluate |
| No tests exist / cannot run | **PASS with note** | Cannot verify; note in evaluation |

### Integration with Evaluation Scoring

Review results directly feed into the 5-criteria scoring:

| Review Check | Scoring Impact |
|-------------|----------------|
| Scope validation | Code Quality: scope violations = -1 point |
| Build verification | Correctness: build fail = disqualify |
| Test execution | Correctness: all pass = +1, failures = -1 per severity |
| codex review findings | Code Quality: quality findings, Safety: security findings |
| Acceptance criteria | Correctness: directly determines base score |

---

## Evaluation Data Collection

Arena collects evaluation data directly from Git and file reading — no external abstraction layer.

### Variant Comparison via Git

```bash
# Diff between two variant branches
git diff arena/variant-codex..arena/variant-gemini

# Diff a variant against the base commit
git diff $BASE_COMMIT..arena/variant-codex

# See files changed by a variant
git diff --stat $BASE_COMMIT..arena/variant-codex

# Show a specific file in a variant branch
git show arena/variant-codex:path/to/file
```

### Direct File Reading

For detailed review, checkout each branch and read files directly:

```bash
git checkout arena/variant-codex
# Use Read tool to inspect implementation files

git checkout arena/variant-gemini
# Use Read tool to inspect implementation files
```

### Automated Review Integration

Use `codex review` as supplementary quality signal:

```bash
# Review uncommitted changes (checkout variant branch first)
git checkout arena/variant-codex
codex review --uncommitted
```

**How to integrate review results:**
- Feed `codex review` findings into **Code Quality** score (patterns, readability, maintainability)
- Feed security-related findings into **Safety** score (vulnerabilities, input validation)
- Review output is supplementary evidence — Arena's own analysis takes precedence

### Test Result Integration

Run tests on each variant branch and reflect results in Correctness score:

```bash
git checkout arena/variant-codex
# Run project-specific test command (npm test, pytest, etc.)
```

**Scoring impact:**
| Test Result | Correctness Impact |
|------------|-------------------|
| All tests pass + new tests added | Score 4-5 |
| All existing tests pass, no new tests | Score 3-4 |
| Some test failures | Score 2-3 (depending on severity) |
| Major test failures | Score 1-2 |
| Tests cannot run | Score 1 (investigate) |

---

## Comparison Report Template

```markdown
## Arena Comparison Report

### Session Information
- Session ID: [session_id]
- Spec: [Spec description]
- Mode: [Solo / Team]
- Engines: [List of engines used]
- Variants Generated: [N]
- Date: [YYYY-MM-DD]

### Variant Summaries

#### Variant A (Engine: [engine], Branch: arena/variant-[engine])
- Approach: [Brief description of implementation strategy]
- Strengths: [Key advantages]
- Weaknesses: [Key disadvantages]
- Test Result: [PASS/FAIL/PARTIAL]
- codex review: [Summary of findings, if run]
- Score: [X.XX/5.00]

#### Variant B (Engine: [engine], Branch: arena/variant-[engine])
- Approach: [Brief description of implementation strategy]
- Strengths: [Key advantages]
- Weaknesses: [Key disadvantages]
- Test Result: [PASS/FAIL/PARTIAL]
- codex review: [Summary of findings, if run]
- Score: [X.XX/5.00]

### Head-to-Head Comparison

| Aspect | Variant A | Variant B | Winner |
|--------|-----------|-----------|--------|
| Correctness | [score] | [score] | [A/B/Tie] |
| Code Quality | [score] | [score] | [A/B/Tie] |
| Performance | [score] | [score] | [A/B/Tie] |
| Safety | [score] | [score] | [A/B/Tie] |
| Simplicity | [score] | [score] | [A/B/Tie] |
| **Weighted Total** | **[total]** | **[total]** | **[Winner]** |

### Selection Decision
- **Selected:** Variant [X]
- **Rationale:** [Why this variant won - focus on decisive factors]
- **Trade-offs Accepted:** [What was sacrificed and why it's acceptable]
- **Dissenting Strengths:** [What the losing variant did better - preserve for future reference]

### Cost Estimate
- Engine invocations: [N per variant]
- Approximate prompt size: [small/medium/large]
- Provider dashboards: [OpenAI / Google AI Studio for exact costs]
```

---

## Quick Evaluation (for AUTORUN mode)

When time is constrained, use this abbreviated format:

```markdown
## Quick Eval: [session_id]
| Variant | Engine | Correct | Quality | Perf | Safety | Simple | Total |
|---------|--------|---------|---------|------|--------|--------|-------|
| A | [engine] | [1-5] | [1-5] | [1-5] | [1-5] | [1-5] | [X.XX] |
| B | [engine] | [1-5] | [1-5] | [1-5] | [1-5] | [1-5] | [X.XX] |

**Winner:** Variant [X] ([one-line rationale])
**Mode:** [Solo/Team]
**Cost:** [estimate]
```

---

## Evaluation Anti-Patterns

Avoid these common evaluation mistakes:

| Anti-Pattern | Problem | Correction |
|--------------|---------|------------|
| **Recency bias** | Favoring the last variant reviewed | Score each criterion independently, then compare |
| **Halo effect** | One strong criterion overshadowing weaknesses | Apply weighted scoring strictly |
| **Complexity worship** | Preferring "clever" over "clear" | Simplicity criterion exists for a reason |
| **Sunk cost** | Favoring variant from expensive engine | Judge output, not input cost |
| **Feature creep** | Rewarding variants that add unrequested features | Score against spec, not beyond it |

---

## Tie-Breaking Rules

When variants score within 0.2 points of each other:

1. **Correctness wins** - If one is more correct, it wins regardless of total
2. **Simplicity wins** - Among equally correct variants, prefer simpler
3. **Safety wins** - If security is relevant, prefer safer
4. **Cost wins** - If all else equal, prefer cheaper engine
5. **Escalate** - If truly indistinguishable, present both to user with trade-offs
