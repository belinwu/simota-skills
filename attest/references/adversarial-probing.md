# Adversarial Probing Catalog

Systematic adversarial verification across 6 categories to discover gaps between specifications and implementations.

---

## Overview

Adversarial probing goes beyond confirming what the spec says. It actively searches for what the spec **doesn't say** — the assumptions, contradictions, and edge cases that become production incidents.

### Probe ID Convention

```
PRB-{category_code}-{NNN}

Category codes: BND (Boundary), OMS (Omission), CTR (Contradiction),
                IMP (Implicit), NEG (Negative), CNC (Concurrency)
```

### Risk Classification

| Risk | Definition | Action Required |
|------|-----------|----------------|
| **CRITICAL** | Will cause data loss, security breach, or system failure | Block CERTIFIED, require fix |
| **HIGH** | Will cause user-facing errors or broken workflows | Block CERTIFIED, remediation plan |
| **MEDIUM** | May cause unexpected behavior in edge cases | Flag for remediation |
| **LOW** | Minor behavioral gaps, unlikely in practice | Document for awareness |

---

## Category 1: Boundary (BND)

**Focus:** Edge values, limits, thresholds, and extremes.

### Common Probes

| Probe | What to Check | Example |
|-------|--------------|---------|
| BND-001 | Empty/null input | What happens with empty string, null, undefined? |
| BND-002 | Maximum length | String at max length, max+1 |
| BND-003 | Zero values | Quantity=0, price=0, count=0 |
| BND-004 | Negative values | Negative quantity, negative price |
| BND-005 | Integer overflow | Values near MAX_INT, MIN_INT |
| BND-006 | Float precision | 0.1 + 0.2 calculations, currency rounding |
| BND-007 | Collection limits | Empty list, list with 1 item, list at max |
| BND-008 | Date boundaries | Leap year, year 2038, timezone midnight |
| BND-009 | Unicode extremes | Emoji, RTL text, zero-width characters |
| BND-010 | File size limits | Zero-byte file, max size, just over max |

### Boundary Probe Template

```yaml
PROBE:
  id: PRB-BND-001
  category: Boundary
  target_criterion: AC-XXX-001
  description: "Empty email input on login form"
  spec_says: "User submits email and password"
  spec_gap: "No specification for empty email handling"
  expected_behavior: "Validation error displayed"
  risk: MEDIUM
  suggested_criterion: "When email field is empty, display 'Email is required' error"
```

---

## Category 2: Omission (OMS)

**Focus:** Requirements the specification forgot to mention.

### Common Probes

| Probe | What to Check | Example |
|-------|--------------|---------|
| OMS-001 | Error messages | What error text is shown for each failure mode? |
| OMS-002 | Loading states | What does the UI show while data loads? |
| OMS-003 | Empty states | What if the list/table has zero items? |
| OMS-004 | Default values | What are the defaults for optional fields? |
| OMS-005 | Pagination | What happens with 10,000 results? |
| OMS-006 | Timeout handling | What if an external service doesn't respond? |
| OMS-007 | Partial failure | What if 3 of 5 items in a batch fail? |
| OMS-008 | Undo/rollback | Can the user undo this action? |
| OMS-009 | Notification | Should the user be notified of this event? |
| OMS-010 | Audit trail | Should this action be logged/tracked? |

### Omission Detection Strategy

1. For each specified feature, ask: "What happens when it fails?"
2. For each data entity, ask: "What are all the states it can be in?"
3. For each user action, ask: "What happens before and after?"
4. For each integration, ask: "What if it's unavailable?"

---

## Category 3: Contradiction (CTR)

**Focus:** Conflicting requirements within or across specifications.

### Common Probes

| Probe | What to Check | Example |
|-------|--------------|---------|
| CTR-001 | Cross-feature conflicts | Feature A allows X, Feature B prevents X |
| CTR-002 | Priority conflicts | "Must be simple" vs "Must support all edge cases" |
| CTR-003 | Permission conflicts | Admin can do X everywhere, but not in this module? |
| CTR-004 | Data model conflicts | Field required in Create but optional in Update |
| CTR-005 | Timing conflicts | "Real-time" vs "batch processing" for same data |
| CTR-006 | UX vs Security | "Seamless experience" vs "re-authenticate every 15 min" |

### Contradiction Detection Strategy

1. Collect all requirements mentioning the same entity/feature
2. Compare behavioral assertions across requirements
3. Flag where one requirement implies negation of another
4. Check cross-module consistency for shared data/flows

---

## Category 4: Implicit (IMP)

**Focus:** Unstated assumptions that implementations depend on.

### Common Probes

| Probe | What to Check | Example |
|-------|--------------|---------|
| IMP-001 | Timezone handling | Does "today" mean user's TZ or server TZ? |
| IMP-002 | Locale/language | Is currency formatting locale-dependent? |
| IMP-003 | Authentication state | Does this feature assume user is logged in? |
| IMP-004 | Network conditions | Does this assume always-online? |
| IMP-005 | Data ordering | Is the list sorted? By what? |
| IMP-006 | Concurrent users | Can multiple users edit the same resource? |
| IMP-007 | Browser/device | Which browsers/devices must be supported? |
| IMP-008 | Data retention | How long is this data kept? |
| IMP-009 | Rate limiting | Are there API call limits? |
| IMP-010 | Idempotency | Can this action be safely retried? |

### Implicit Assumption Extraction

For each feature, ask:
1. **Who?** — What user roles/states are assumed?
2. **Where?** — What environment/platform is assumed?
3. **When?** — What timing/ordering is assumed?
4. **How much?** — What volume/scale is assumed?
5. **What if not?** — What if the assumption is violated?

---

## Category 5: Negative (NEG)

**Focus:** Forbidden, invalid, and unauthorized paths.

### Common Probes

| Probe | What to Check | Example |
|-------|--------------|---------|
| NEG-001 | Invalid input format | SQL injection, XSS, malformed JSON |
| NEG-002 | Unauthorized access | Accessing other user's data |
| NEG-003 | Invalid state transitions | Shipping a cancelled order |
| NEG-004 | Expired resources | Using expired token, link, coupon |
| NEG-005 | Missing required fields | Submitting form with required fields empty |
| NEG-006 | Duplicate actions | Double-clicking submit, double payment |
| NEG-007 | Out-of-order operations | Step 3 before Step 1 |
| NEG-008 | Resource exhaustion | Too many requests, full disk, OOM |
| NEG-009 | Privilege escalation | Regular user accessing admin endpoints |
| NEG-010 | Data integrity | Deleting parent with active children |

---

## Category 6: Concurrency (CNC)

**Focus:** Race conditions, ordering issues, and parallel execution problems.

### Common Probes

| Probe | What to Check | Example |
|-------|--------------|---------|
| CNC-001 | Simultaneous updates | Two users editing the same document |
| CNC-002 | Read-after-write | Reading data immediately after writing |
| CNC-003 | Double submission | Form submitted twice in rapid succession |
| CNC-004 | Stale cache | Showing outdated data after update |
| CNC-005 | Lost updates | Last write wins vs merge strategy |
| CNC-006 | Deadlock potential | Circular resource dependencies |
| CNC-007 | Queue ordering | Message processing order guarantee |
| CNC-008 | Session conflicts | Same user logged in on multiple devices |

---

## Probe Output Format

```yaml
ADVERSARIAL_PROBES:
  total: 18
  by_category:
    boundary: 4
    omission: 5
    contradiction: 1
    implicit: 3
    negative: 3
    concurrency: 2
  by_risk:
    critical: 1
    high: 4
    medium: 8
    low: 5
  probes:
    - id: PRB-OMS-003
      category: Omission
      target: AC-LOGIN-001
      description: "Login spec doesn't mention account lockout"
      spec_gap: "No lockout mechanism specified after failed attempts"
      risk: CRITICAL
      suggested_criterion: "After 5 failed login attempts, lock account for 30 minutes"
      implementation_status: NOT_IMPLEMENTED
```

---

## Probe Execution Strategy

### Priority Order

1. **Contradiction** — Most damaging, spec-level defect
2. **Omission** — Missing requirements become production bugs
3. **Negative** — Security and validation gaps
4. **Boundary** — Data integrity risks
5. **Implicit** — Hidden assumption failures
6. **Concurrency** — Complex but specific scenarios

### Minimum Probes per Mode

| Mode | Min Probes | Category Coverage |
|------|-----------|-------------------|
| FULL | 12 | All 6 categories |
| ADVERSARIAL | 24 | All 6, deep coverage |
| AUDIT | 6 | Focus on Omission + Contradiction |
| EXTRACT | 0 | No probing (extraction only) |
