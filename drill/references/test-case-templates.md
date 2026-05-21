# Test Case Templates

Canonical templates and tool-format mappings for Drill-authored test cases.

---

## Canonical Test Case (Markdown)

```markdown
### TC-AUTH-001 — Reject login with expired password

| Field | Value |
|-------|-------|
| Module | Authentication / Login |
| Priority | P0 |
| Type | Negative, Functional |
| Technique | Equivalence Partitioning, Error Guessing |
| Estimated Duration | 3 min |
| Automation Candidate | Yes (E2E) |
| Requirement IDs | FR-AUTH-12, AC-AUTH-005 |

**Preconditions**
- User account `qa.expired@example.com` exists in the test environment.
- Password expiry policy is enabled (90 days).
- The account's `password_changed_at` is set to ≥91 days ago.

**Test Data**
- Email: `qa.expired@example.com`
- Password: `ValidButExpired#2024`

**Steps**
| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Navigate to `/login` | Login form is visible with email and password fields |
| 2 | Enter the test data email | Email field accepts input; no validation error |
| 3 | Enter the test data password | Password field accepts input; characters are masked |
| 4 | Click **Sign in** | Form submits; loading indicator appears |
| 5 | Observe response | Inline error: "Your password has expired. Reset it to continue." Reset CTA is focused. No session cookie set. |

**Postconditions**
- No session is created.
- Audit log records `AUTH_FAILED_EXPIRED_PASSWORD` event.

**Defect Template (if FAIL)**
- Severity: Major / Critical
- Reproduction: Steps 1-5 above
- Expected vs Actual: (paste expected from step 5, paste actual observation)
- Evidence: (screenshot, network HAR, audit log entry, browser console)
- Environment: (env, build SHA, browser, account)
```

---

## Field Schema (Required)

| Field | Purpose | Common Mistake |
|-------|---------|----------------|
| `TC-ID` | Stable identifier for traceability and import | Letting IDs renumber on edit — lock them once issued |
| `Title` | One-line scenario summary, verb-first | Vague titles ("Test login") — be specific about the variant |
| `Module / Feature` | Group cases; maps to PRD section | Mixing scope ("Login + Profile") — split into two cases |
| `Priority` | P0-P3 (rubric in `risk-based-prioritization.md`) | "High/Medium/Low" — non-standard; use P0-P3 |
| `Type` | Functional / Negative / Boundary / UI / A11y / etc. | Single label only — use multiple if applicable |
| `Technique` | Which design technique produced this case | Omitting it — reviewers can't audit coverage without |
| `Preconditions` | State, data, role, environment | "User is logged in" without specifying role / permissions |
| `Test Data` | Concrete values or reference to data set | Inline secrets — reference fixtures, not real credentials |
| `Steps` | Numbered, one verb per step | Compound steps ("Open and click and verify") — split |
| `Expected Result` | Observable outcome per step or final | Subjective ("Looks good") — must be testable |
| `Postconditions` | Cleanup or state-restore | Missing — leads to test pollution |
| `Requirement IDs` | AC / FR / NFR references | None — breaks traceability |

### Optional Provenance Fields (AI-assisted authoring & high-risk AI components)

| Field | When | Notes |
|-------|------|-------|
| `ai_generated` | Test case body or any step was first-drafted by an LLM | `true` / `false`. TestRail AI exposes "Step (AI-Generated)" and "Expected Result (AI-Generated)" fields natively; Qase AIDEN attaches an `AI` tag — preserve provenance on round-trip. [Source: https://support.testrail.com/hc/en-us/articles/37119835854484] |
| `ai_review_status` | Same | `pending` / `approved` / `rejected`. Required when `ai_generated: true`; matches Qase AIDEN's "approve before saving" gate. [Source: https://docs.qase.io/aiden-qase-ai/ai-test-case-generator] |
| `external_issue_id` | Case derived from a tracker issue (Jira / GitHub / Linear) | Preserve the source URL or issue ID end-to-end (Scribe → Drill handoff must carry it). |
| `ai_component` | SUT embeds AI / ML / LLM | Free-form module reference (e.g., `reco-v3`). Mandatory on AI-Under-Test cases (§11). |
| `model_version` | Same | E.g., `claude-opus-4-7@2026-01`. Required for EU AI Act Article 18 traceability on high-risk AI. [Source: https://artificialintelligenceact.eu/article/43/] |
| `dataset_snapshot_id` | Same | Training / eval dataset hash or snapshot ID. |
| `non_determinism_disclosure` | AI output is non-deterministic | Disclose `temperature`, `top_p`, `seed` (if any), and the acceptable variance band (`==`, `BLEU≥X`, `JSON-schema-match`). |

---

## Exploratory Charter Template (SBTM)

Session-Based Test Management — `90-minute time-box` per charter.

```markdown
### CHARTER-CHK-003 — Explore checkout cart edge cases

**Mission**
Investigate how the cart and checkout handle unusual quantity, currency, and discount combinations.

**Areas In Scope**
- Cart quantity update controls
- Currency switching mid-checkout
- Stacking coupon + member discount + tax
- Inventory edge: last-unit, out-of-stock during checkout

**Areas Out of Scope**
- Payment provider integration (covered by TC-PAY-*)
- Shipping calculation (covered by TC-SHP-*)

**Test Ideas**
- Set quantity to 0, then to negative, then to 9999
- Add 50 items of the same SKU
- Switch currency from JPY to USD with discount applied
- Apply two coupons that conflict per policy
- Two browser tabs racing to checkout the last unit

**Oracles** (how you'll know something's wrong)
- Cart total never goes negative
- Currency switch recomputes all subtotals, not just one
- Stacking rule from PRD §4.3 is enforced
- Last-unit race shows clear out-of-stock to the loser

**Time-box**: 90 min  (split 60 min explore, 20 min notes, 10 min file)
**Risks**: P0 — checkout regression blocks revenue
**Tester**: (assigned)
**Date**: (YYYY-MM-DD)

**Session Notes**  *(fill during session)*
- Time on test design: __ min
- Time on testing: __ min
- Time on bug investigation: __ min
- New test ideas discovered: ...
- Bugs found: BUG-... (file with defect template)
- Follow-up regression cases needed: TC-... (lift to permanent suite)
```

---

## Tool Format Mappings

### TestRail (CSV import)

| TestRail Field | Drill Field | Notes |
|----------------|-------------|-------|
| `Section` | `Module` | TestRail organizes by Section |
| `Title` | `Title` | |
| `Priority` | `Priority` | Map P0→Critical, P1→High, P2→Medium, P3→Low |
| `Type` | `Type` | TestRail has a configurable Type field |
| `Preconditions` | `Preconditions` | |
| `Steps (Separated)` | `Steps` | One row per step; use Action / Expected Result columns |
| `References` | `Requirement IDs` | Comma-separated |
| `Estimate` | `Estimated Duration` | TestRail accepts `3m`, `1h30m` etc. |
| `Step (AI-Generated)` | step `Action` if drafted by LLM | Native TestRail AI field. Set `ai_generated: true` and `ai_review_status` in test case body. [Source: https://support.testrail.com/hc/en-us/articles/37119835854484] |
| `Expected Result (AI-Generated)` | step `Expected Result` if drafted by LLM | Native TestRail AI field; same provenance rule. |

### Zephyr Scale

| Zephyr Field | Drill Field | Notes |
|--------------|-------------|-------|
| `Name` | `Title` | |
| `Folder` | `Module` | Zephyr uses folder hierarchy |
| `Priority` | `Priority` | Highest / High / Normal / Low |
| `Labels` | `Type`, `Technique` | Use labels for both |
| `Pre-conditions` | `Preconditions` | |
| `Test Script (Steps)` | `Steps` | Each step has Description + Expected Result |
| `Component` | `Module` | Map to Jira Component |
| `Coverage` | `Requirement IDs` | Linked Jira Issues |

### Xray (Jira)

| Xray Field | Drill Field | Notes |
|------------|-------------|-------|
| `Summary` | `Title` | |
| `Test Type` | always `Manual` | Drill never outputs Cucumber / Generic |
| `Priority` | `Priority` | Jira priority |
| `Components` | `Module` | |
| `Labels` | `Technique`, `Type` | |
| `Action` (per step) | step `Action` | |
| `Data` (per step) | inline test data | |
| `Expected Result` (per step) | step `Expected Result` | |
| Note | `Postconditions` | Xray has no native postcondition — append to description |

### Qase

| Qase Field | Drill Field | Notes |
|------------|-------------|-------|
| `Title` | `Title` | |
| `Suite` | `Module` | |
| `Severity` + `Priority` | derive from `Priority` | P0→Critical/High, P1→Major/High, P2→Normal/Medium, P3→Minor/Low |
| `Preconditions` | `Preconditions` | |
| `Postconditions` | `Postconditions` | Qase supports natively |
| `Steps` | `Steps` | Action + Expected Result + Data per step |
| `Type` | `Type` | |
| `Behavior` | always `Positive` or `Negative` | |
| `Tag: AI` | `ai_generated: true` | Qase AIDEN attaches an `AI` tag automatically; preserve on round-trip. [Source: https://docs.qase.io/aiden-qase-ai/ai-test-case-generator] |
| `External Issue` | `external_issue_id` | Jira / GitHub issue link AIDEN uses for traceability. |

### Gherkin (Given/When/Then)

Use only when the consumer expects BDD-style scenarios. Most QA test management tools prefer structured fields over Gherkin.

```gherkin
Feature: Authentication — Expired Password

  Scenario: Reject login with expired password
    Given a user "qa.expired@example.com" with an expired password
    And the password expiry policy is enabled
    When the user attempts to sign in with valid credentials
    Then the response shows "Your password has expired. Reset it to continue."
    And no session cookie is set
    And the audit log records "AUTH_FAILED_EXPIRED_PASSWORD"
```

---

## IEEE 829 / ISO/IEC/IEEE 29119-3 Alignment

The canonical template above aligns with **ISO/IEC/IEEE 29119-3:2021** (Test Documentation) Test Case structure:
- Test case identifier → `TC-ID`
- Objective → embedded in `Title` + `Requirement IDs`
- Inputs → `Test Data`
- Outputs → `Expected Result`
- Environmental needs → `Preconditions`
- Special procedural requirements → covered by `Preconditions` and `Postconditions`
- Intercase dependencies → reference via `Requirement IDs` or sibling TC-IDs

Drill is compatible with both IEEE 829-1998 (superseded but still widely cited) and the current ISO/IEC/IEEE 29119-3. **Keyword-driven** test cases follow **ISO/IEC/IEEE 29119-5:2024** (new in 2024); Drill does not author keyword libraries directly but its step format is keyword-lift-compatible. [Source: https://en.wikipedia.org/wiki/ISO/IEC_29119]

---

## Sample — Accessibility WCAG 2.2 Manual Case (Focus Not Obscured)

```markdown
### TC-A11Y-014 — Sticky header does not obscure focused field on signup form

| Field | Value |
|-------|-------|
| Module | Accessibility / Signup |
| Priority | P1 |
| Type | Accessibility |
| Technique | A11y (WCAG 2.2 SC 2.4.11 Focus Not Obscured Minimum) |
| Estimated Duration | 5 min |
| Automation Candidate | Maybe (axe-core does not detect this; needs visual oracle) |
| Requirement IDs | AC-A11Y-2.4.11, NFR-A11Y-01 |

**Preconditions**
- Desktop browser (Chrome / Safari latest).
- Viewport 1280×800.
- Signup page loaded with the sticky promotional header visible (top 64 CSS px).

**Test Data**
- N/A (UI-only).

**Steps**
| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Scroll the page so the sticky header is pinned at the top | Sticky header remains visible across scroll |
| 2 | Press `Tab` from the URL bar into the page | First focusable element receives a visible focus ring |
| 3 | Continue pressing `Tab` through every signup form field | At each stop, **any part** of the focus indicator is visible above the sticky header (≥1 CSS px of the indicator outside the sticky chrome) |
| 4 | Resize browser to 320 CSS px width and zoom to 200% | Tab traversal still satisfies step 3 |

**Postconditions**
- No state change. Reset zoom to 100%.

**Defect Template (if FAIL)**
- Severity: Major (a11y legal floor in EU under EAA 2025-06)
- Reproduction: Steps 1-3 (specify the Tab-stop index where occlusion occurred)
- Expected vs Actual: paste expected from step 3; attach screenshot showing the occluded focus ring
- Evidence: screenshot, DevTools element snapshot of sticky element + focused element bounding boxes
```

[Source: https://www.allaccessible.org/blog/wcag-22-complete-guide-2025]
