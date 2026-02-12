# Artisan: Nexus Integration Templates

## AUTORUN Input Context (from Nexus)

```yaml
_AGENT_CONTEXT:
  Role: Artisan
  Task: "[from Nexus]"
  Mode: "AUTORUN"
  Chain:
    Previous: "[previous agent or null]"
    Position: "[step X of Y]"
    Next_Expected: "[next agent or DONE]"
  History:
    - Agent: "[previous agent]"
      Summary: "[what they did]"
  Constraints:
    Framework: "[React/Vue/Svelte]"
    State_Management: "[Zustand/Pinia/Context]"
    Styling: "[Tailwind/CSS Modules/CSS-in-JS]"
  Expected_Output:
    - Production components
    - Type definitions
    - State management setup
```

## AUTORUN Output Format (to Nexus)

```yaml
_STEP_COMPLETE:
  Agent: Artisan
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    framework: "[React/Vue/Svelte]"
    components_created:
      - name: "[component name]"
        path: "[file path]"
        purpose: "[description]"
    state_management: "[approach used]"
    type_safety: "STRICT | PARTIAL"
    accessibility: "PASS | WARN | FAIL"
  Artifacts:
    - "[List of created/modified files]"
  Risks:
    - "[Identified risks]"
  Next: Builder | Showcase | Radar | Flow | VERIFY | DONE
  Reason: "[Why this next step]"
```

## Nexus Hub Mode (NEXUS_HANDOFF)

When user input contains `## NEXUS_ROUTING`, return results via this format:

```text
## NEXUS_HANDOFF
- Step: [X/Y]
- Agent: Artisan
- Summary: 1-3 lines
- Key findings / decisions:
  - Components: [count]
  - State management: [approach]
  - Framework patterns: [used]
- Artifacts (files/commands/links):
  - Component files: [paths]
  - Types: [paths]
  - Hooks/composables: [paths]
- Risks / trade-offs:
  - [Performance considerations]
  - [Browser compatibility]
- Pending Confirmations:
  - Trigger: [INTERACTION_TRIGGER name if any]
  - Question: [Question for user]
  - Options: [Available options]
  - Recommended: [Recommended option]
- User Confirmations:
  - Q: [Previous question] -> A: [User's answer]
- Open questions (blocking/non-blocking):
  - [API contract questions for Builder]
- Suggested next agent: Builder | Showcase | Radar
- Next action: Paste this response to Nexus
```
