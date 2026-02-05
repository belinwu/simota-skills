# Nexus-Cipher Integration Reference

Cipher as the front-gate for ambiguous input clarification.

---

## Overview

Cipher is integrated as Nexus's intent clarification specialist. When context confidence is low, Nexus delegates to Cipher for intent decoding before proceeding with chain selection.

---

## Integration Architecture

```
User Request (potentially ambiguous)
              │
              ▼
┌─────────────────────────────┐
│         NEXUS               │
│   Context Scoring Phase     │
└──────────────┬──────────────┘
               │
    ┌──────────┴──────────┐
    ▼                     ▼
 confidence >= 0.60    confidence < 0.60
    │                     │
    ▼                     ▼
 Proceed           ┌─────────────────┐
 to Chain          │     CIPHER      │
 Selection         │ Intent Decoding │
    │              └────────┬────────┘
    │                       │
    │              ┌────────┴────────┐
    │              ▼                 ▼
    │          Clarified          Needs
    │          (auto)             Question
    │              │                 │
    │              ▼                 ▼
    │          Nexus             User
    │          (confidence       (single Q)
    │           boosted)             │
    │              │                 │
    └──────────────┴─────────────────┘
                   │
                   ▼
           Chain Selection
```

---

## CIPHER_GATE Trigger Conditions

```yaml
CIPHER_GATE:
  trigger_when:
    any_of:
      - context_confidence < 0.60
      - multiple_valid_interpretations: true
      - missing_critical_context: true
      - uncertainty_level: [MEDIUM, HIGH]

  pass_to_cipher:
    - original_request: "[User's exact words]"
    - context_snapshot:
        git_status: "[Current git state]"
        recent_activity: "[From .agents/PROJECT.md]"
        conversation_history: "[Relevant prior messages]"
    - confidence_breakdown: "[From context scoring]"
    - ambiguity_signals: "[What triggered Cipher]"
```

---

## Cipher Integration Flow

### Phase 1: Detection

```yaml
detect_ambiguity:
  signals:
    - vague_keywords: ["improve", "fix", "handle", "something"]
    - missing_specifics: [no_file_mentioned, no_clear_scope]
    - multiple_interpretations: [could_be_A, could_be_B]

  if_detected:
    action: INVOKE_CIPHER
    mode: auto  # Cipher decides if question needed
```

### Phase 2: Cipher Processing

```yaml
cipher_processing:
  input:
    request: "[Original request]"
    context: "[All available context]"

  cipher_actions:
    1. Check context (git, project.md, conversation)
    2. Identify if single interpretation is clear
    3. If clear: return clarified intent
    4. If unclear: formulate single focused question

  output:
    format: CIPHER_OUTPUT (see below)
```

### Phase 3: Nexus Integration

```yaml
integrate_cipher_output:
  on_clarified:
    - Extract intent, scope, assumptions
    - Boost context confidence (+0.20)
    - Proceed to chain selection
    - No user interaction needed

  on_ask_needed:
    - Present Cipher's question to user
    - Single question only (Cipher's decision)
    - Integrate answer
    - Re-run context scoring
    - Proceed if confidence >= 0.60
```

---

## CIPHER_OUTPUT Format

When Cipher completes intent clarification:

```yaml
CIPHER_OUTPUT:
  original: "[User's exact words]"
  clarified_intent: "[What user actually wants]"
  scope: [minimal|moderate|extensive]

  confidence: 0.XX  # Cipher's confidence in interpretation

  assumptions:
    - "[Assumption 1]"
    - "[Assumption 2]"

  context_used:
    - "[What context informed this interpretation]"

  recommended_agent: [AgentName]
  recommended_chain: [Chain if complex]

  ask_needed: [true|false]
  question:  # Only if ask_needed: true
    text: "[Single focused question]"
    options:
      - "[Option 1]"
      - "[Option 2]"
      - "[Option 3]"
    recommended: "[Option N]"
```

---

## Confidence Boosting

Cipher's clarification boosts Nexus's confidence:

| Cipher Outcome | Confidence Boost |
|----------------|------------------|
| Clarified without asking | +0.20 |
| Clarified after user answer | +0.25 |
| User provided additional context | +0.15 |

```yaml
post_cipher_confidence:
  original_confidence: 0.XX
  cipher_boost: +0.XX
  new_confidence: min(0.XX + boost, 1.0)

  if new_confidence >= 0.80:
    action: AUTO_PROCEED
  elif new_confidence >= 0.60:
    action: PROCEED_WITH_ASSUMPTIONS
  else:
    action: ESCALATE  # Rare - Cipher usually resolves
```

---

## Learning Loop

Record Cipher interactions for continuous improvement:

```yaml
cipher_learning:
  location: .agents/cipher.md

  record:
    interpretations:
      - request: "[Original]"
        clarified: "[What it meant]"
        correct: [true|false]

    vocabulary:
      - phrase: "[User's phrase]"
        means: "[Actual meaning in this project]"

    corrections:
      - interpreted_as: "[What Cipher thought]"
        actually_meant: "[What user corrected to]"

  apply_learning:
    - Improve future interpretations
    - Reduce question frequency
    - Project-specific vocabulary
```

---

## Question Reduction Strategy

Cipher's goal is to REDUCE questions, not ask them:

```yaml
question_philosophy:
  prefer:
    - Reading context over asking
    - Safe defaults over clarification
    - Single question over multiple

  ask_only_when:
    - Multiple valid paths with significant difference
    - No safe default exists
    - Context provides no signal

  never_ask:
    - When context is clear
    - When safe default available
    - When user is frustrated (detect from tone)
```

---

## AUTORUN Support

In AUTORUN/AUTORUN_FULL mode, Cipher operates automatically:

```yaml
autorun_behavior:
  cipher_auto_execution: true

  on_trigger:
    1. Cipher analyzes request
    2. If single clear interpretation: proceed silently
    3. If question needed: still ask (but only once)
    4. Log all assumptions

  output_in_nexus_complete:
    section: "Intent Clarification"
    content:
      - Original request
      - Interpreted as
      - Assumptions made
      - Context used
```

---

## Integration Metrics

Track Cipher integration effectiveness:

```yaml
metrics:
  cipher_invocation_rate: X%  # Target: < 30% of requests
  auto_clarification_rate: X%  # Target: > 80% of invocations
  question_rate: X%           # Target: < 20% of invocations
  interpretation_accuracy: X% # Target: > 95%

  autonomy_contribution:
    without_cipher: 45% autonomy
    with_cipher: +18% (target 63% from this alone)
```

---

## Error Handling

When Cipher cannot resolve:

```yaml
cipher_failure_handling:
  cannot_interpret:
    action: Return to Nexus with low confidence
    nexus_action: Present multi-approach options to user

  conflicting_signals:
    action: Surface conflict to user
    format: "[Signal A suggests X, Signal B suggests Y]"

  user_frustrated:
    action: Acknowledge, skip questions, use safest default
    note: "Proceeding with conservative approach due to urgency"
```
