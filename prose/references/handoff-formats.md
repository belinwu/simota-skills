# Prose Handoff Formats

Echo/Polyglot/Artisan/Palette へのハンドオフテンプレート。

---

## Prose → Echo (Persona Validation)

```markdown
## Copy for Persona Validation

### Copy Context
- **Feature/Flow**: [feature name]
- **Copy type**: [microcopy/error/onboarding/notification]
- **Voice attributes**: [list from voice guide]
- **Tone**: [tone for this context]

### Copy to Validate
| Screen/State | Copy | Intended Effect |
|-------------|------|----------------|
| [screen] | "[exact copy text]" | [what user should understand/feel] |
| [screen] | "[exact copy text]" | [what user should understand/feel] |

### Validation Questions
1. Does this copy make sense to a [persona] user?
2. Is the tone appropriate for their emotional state?
3. Are there confusing terms or jargon?
4. Does the CTA clearly communicate what happens next?

### Personas to Test
- [ ] [Persona 1]: [key characteristics]
- [ ] [Persona 2]: [key characteristics]
```

---

## Prose → Polyglot (i18n Preparation)

```markdown
## Copy for Internationalization

### Source Language
[language, e.g., "English (US)"]

### Copy Inventory
| Key | Source Text | Max Length | Context | Notes |
|-----|-----------|-----------|---------|-------|
| `error.payment_failed` | "Your payment couldn't be processed." | 60 chars | Payment error banner | Keep formal tone |
| `cta.get_started` | "Get started" | 20 chars | Primary CTA button | Action-oriented |
| `empty.no_results` | "No results found. Try different keywords." | 80 chars | Search empty state | Helpful tone |

### Translation Guidelines
- **Tone**: [describe tone to maintain]
- **Formality**: [formal/informal/varies by locale]
- **Variables**: [list dynamic values: {name}, {count}]
- **Pluralization**: [list strings that need plural forms]
- **Cultural considerations**: [any locale-specific notes]

### Strings with Special Handling
- [key]: [reason, e.g., "Contains wordplay that won't translate directly"]
- [key]: [reason, e.g., "Legal text — needs professional translator"]
```

---

## Prose → Artisan (Implementation)

```markdown
## UI Copy for Implementation

### Feature
[Feature name and description]

### Copy Specifications
| Component | Copy | Variant/State | Notes |
|-----------|------|--------------|-------|
| Page title | "Account Settings" | — | h1, not truncatable |
| Button | "Save changes" | Default | Primary action |
| Button | "Saving..." | Loading | Disabled state |
| Button | "Saved ✓" | Success | Auto-dismiss 2s |
| Error | "Couldn't save. Try again." | Error | Toast, 5s dismiss |
| Tooltip | "Changes save automatically" | — | On auto-save icon |

### Copy Rules for This Feature
- [Rule 1: e.g., "All error messages follow what/why/next pattern"]
- [Rule 2: e.g., "Button labels use sentence case"]
- [Rule 3: e.g., "No emoji in error states"]

### Accessibility Requirements
- [ ] All icons have aria-labels as specified
- [ ] Error messages use aria-live="assertive"
- [ ] Loading states announce to screen readers
```

---

## Prose → Palette (UX Integration)

```markdown
## Copy-UX Alignment Review

### Feature/Flow
[Feature name]

### Copy-Design Considerations
| Copy Element | Design Constraint | Alignment Note |
|-------------|------------------|---------------|
| [heading] | Max width: 300px | May need shorter variant |
| [description] | Below fold on mobile | Must be self-sufficient without image |
| [error message] | Inline, 1 line | Keep under 60 characters |
| [empty state] | Center-aligned card | Include illustration suggestion |

### Responsive Copy Variants
| Breakpoint | Element | Copy |
|-----------|---------|------|
| Desktop | CTA | "Create your first project" |
| Mobile | CTA | "Create project" |
| Desktop | Empty state | "No projects yet. Create one to get started." |
| Mobile | Empty state | "No projects yet." + CTA |

### Interaction-Copy Sync
- [ ] Loading states have copy (not just spinners)
- [ ] Success states have confirmation copy
- [ ] Error states have recovery instructions
- [ ] Empty states have guidance copy
- [ ] Disabled states explain why (tooltip or help text)
```

---

## Echo → Prose (Feedback Input)

```markdown
## Input: Persona Feedback on Copy

### Feedback Source
- **Persona**: [persona name and description]
- **Flow tested**: [feature/flow]
- **Method**: [walkthrough/task analysis]

### Issues Found
| Screen | Current Copy | Issue | Severity |
|--------|-------------|-------|----------|
| [screen] | "[current text]" | [confusion/misunderstanding] | [High/Med/Low] |

### Requested Revisions
1. [Screen]: Rewrite "[text]" — [what's wrong and what would help]
2. [Screen]: Add help text for [element] — [persona didn't understand]

### Context
[Any additional observations about the user's mental model
or expectations that should inform copy revisions]
```
